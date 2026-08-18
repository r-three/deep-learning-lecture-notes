#!/usr/bin/env python3
"""Build a *visual-assessment* prompt for a lecture's figures (second pass).

`gen_fidelity_prompt.py` audits the prose; this script audits the pictures. It
produces the prompt that asks Claude to render each inline SVG figure in a
lecture `.qmd`, *look at the rendered image*, compare it against the hand-drawn
slide it came from (and the transcript's description), and fix the ones whose
numbers, labels, or layout are wrong — misplaced digits, mismatched dimensions,
overlapping or clipped text, elements that are not visually adjusted, or colors
that break `style.md`.

The assessment is inherently visual (a hand-drawn slide vs. a rendered SVG), so
it is done by Claude when the prompt is run — this script only detects the files
and fills the prompt, mirroring `gen_fidelity_prompt.py`. The prompt itself
carries the render-and-look loop (headless Chrome screenshot -> view the PNG).

Usage:
    python gen_visual_prompt.py 11                 # print prompt to stdout
    python gen_visual_prompt.py 11 --write         # save alongside the sources
    python gen_visual_prompt.py 12 --report vis.txt # custom report filename

By default the filled prompt is printed to stdout. Pass --write to save it to
`lecture_notes/Lecture <N>/visual-prompt.filled.md`.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Reuse the sibling scripts' conventions (folder layout, source + qmd detection).
from gen_fidelity_prompt import REPO, find_lecture_dir, detect_sources, find_qmd, rel

DEFAULT_REPORT = "visual-report.txt"

# The visual-assessment prompt. Placeholders (<...>) are substituted in fill().
PROMPT_TEMPLATE = """\
Run a **visual assessment** (second pass) on the figures in the Lecture <N>
write-up: render every inline SVG figure in the `.qmd`, look at each rendered
image, compare it against the hand-drawn slide it is based on and the
transcript, and fix the figures whose **numbers, labels, or layout** are wrong.
This pass is specifically about the pictures — misplaced or mismatched numbers,
overlapping or clipped text, and figures that were never visually adjusted.

**Files**

- Lecture notes (the figures under test): `<qmd>`
- Slides / notes PDF (the hand-drawn source figures): `<slides>`
- Transcript (describes what each figure shows): `<transcript>`<bonus_line>

**Reference guides — read first and apply throughout:**

1. `website/style.md` — the controlling figure guide: the Helvetica stack, the
   Pastel Rainbow role palette (red / yellow / green reserved for
   start / error / success — do not use them as decorative categories), and
   Paul Tol's "bright" / "light" schemes for any **plotted data**.
2. `website/persona.md` §6 (figures) — figures are inline SVG; caption text obeys
   the same calm register as the prose (no hype, no exclamations).
3. `website/notation.qmd` — symbols drawn inside a figure must match the notes.

**Step 1 — Inventory.** List every inline SVG figure in `<qmd>` (each lives in a
```{=html} ... <svg> ... </svg> ... ``` block; identify it by its `<text>`
title). For each, name the slide page in `<slides>` it corresponds to, and the
transcript passage that describes it.

**Step 2 — Render and LOOK.** Do not judge a figure from its SVG source — render
it and view the image. For each figure, extract the `<div>...<svg>...</svg></div>`
fragment, wrap it in a minimal HTML file, screenshot it with headless Chrome at
2x, and open the PNG:

```
f=figname   # one per figure
printf '<!doctype html><html><head><meta charset="utf-8"></head><body style="margin:0;background:#fff">' > /tmp/vis_$f.html
# append the figure's <div>...<svg>...</svg></div> fragment to /tmp/vis_$f.html
printf '</body></html>' >> /tmp/vis_$f.html
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \\
  --screenshot=/tmp/vis_$f.png --window-size=900,500 --force-device-scale-factor=2 \\
  "file:///tmp/vis_$f.html"
```

Then read `/tmp/vis_$f.png` to see it. (A raw `.svg` whose root is `<div>`
renders as XML source, so the HTML wrapper is required. qlmanage and cairosvg
are not reliable here; headless Chrome is.) Also view the matching slide page so
you are comparing the render against the source, not against your memory of it.

**Step 3 — Compare.** For each figure, check the render against the slide and
transcript on:

- `NUMBERS / LABELS` — every dimension, count, index, bit-width, coordinate,
  equation, and node label matches the slide/transcript exactly (e.g. a matrix
  shape, a bit count, a subscript range, a "×N" factor). This is the main
  reported problem: numbers sitting in the wrong place or disagreeing with the
  source.
- `LAYOUT / ALIGNMENT` — no overlapping text, no clipping or off-canvas content
  (nothing past the `viewBox`), boxes and rows aligned, arrows connecting the
  correct nodes, annotations (braces, bubbles, highlights) sitting over the
  region they describe, adequate spacing. Flag anything that looks unadjusted.
- `STRUCTURE` — the counts and topology match the slide: the same number of
  layers / boxes / arrows, the same connectivity and left-to-right (or
  top-to-bottom) order.
- `PALETTE / STYLE` — Helvetica; role colors used per `style.md` (reserved
  red/yellow/green not repurposed); plotted data uses Paul Tol schemes;
  legible font sizes and contrast.

**Step 4 — Write the report.** Record findings in a plain-text file at
`<report>` (overwrite if it exists), one section per figure. For each finding
give the figure title, the category above, what the slide/transcript shows vs.
what the render shows, and a severity (high / medium / low). If a figure is
visually faithful, say so in one line rather than padding. End with a
prioritized summary (high-severity items first).

**Step 5 — Fix and re-verify.** Edit the SVG in `<qmd>` to correct the flagged
numbers, labels, and layout — adjust coordinates, `viewBox`, text positions, and
values; keep the established figure style and the Python-generated look. After
each fix, re-render that figure (Step 2) and look again; iterate until the
render matches the source. Make targeted edits — do not redraw figures that are
already faithful.

**Step 6 — Verify and summarize.** Re-run `quarto render` on the `.qmd` and
confirm it compiles, every `<svg>` is still present and well-formed (no leftover
`FIG:` markers, no truncated fragments), and no math or citation anchors broke.
Then summarize what the report flagged and what you changed, and confirm the
report was written to `<report>`.

Keep any caption or label wording calm and precise — no hype, no exclamation
marks. Change only what the visual comparison shows to be wrong.
"""


def fill(n: int, qmd: Path, transcript: Path, slides: Path,
         bonus: list[Path], report: Path) -> str:
    if bonus:
        bonus_line = "\n- Bonus / supplementary PDF(s): " + ", ".join(
            f"`{rel(p)}`" for p in bonus
        )
    else:
        bonus_line = ""
    replacements = [
        ("<qmd>", rel(qmd)),
        ("<transcript>", rel(transcript)),
        ("<slides>", rel(slides)),
        ("<bonus_line>", bonus_line),
        ("<report>", rel(report)),
        ("<N>", str(n)),
    ]
    out = PROMPT_TEMPLATE
    for token, value in replacements:
        out = out.replace(token, value)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("number", type=int, help="lecture number, e.g. 11")
    ap.add_argument("--report", default=DEFAULT_REPORT,
                    help=f"report filename written under the lecture folder "
                         f"(default: {DEFAULT_REPORT})")
    ap.add_argument("--write", action="store_true",
                    help="save to lecture_notes/Lecture <N>/visual-prompt.filled.md "
                         "instead of printing to stdout")
    args = ap.parse_args()

    n = args.number
    lecture_dir = find_lecture_dir(n)
    transcript_stem, slides_stem, bonus_stems = detect_sources(lecture_dir, n)
    transcript = lecture_dir / f"{transcript_stem}.txt"
    slides = lecture_dir / f"{slides_stem}.pdf"
    bonus = [lecture_dir / f"{s}.pdf" for s in bonus_stems]
    qmd = find_qmd(n)
    report = lecture_dir / args.report

    filled = fill(n, qmd, transcript, slides, bonus, report)

    # Report detected sources to stderr so stdout stays clean for piping.
    print(f"Visual assessment — Lecture {n}", file=sys.stderr)
    print(f"  qmd:        {rel(qmd)}", file=sys.stderr)
    print(f"  slides:     {rel(slides)}", file=sys.stderr)
    print(f"  transcript: {rel(transcript)}", file=sys.stderr)
    for b in bonus:
        print(f"  bonus:      {rel(b)}", file=sys.stderr)
    print(f"  report:     {rel(report)}", file=sys.stderr)

    if args.write:
        out_path = lecture_dir / "visual-prompt.filled.md"
        out_path.write_text(filled + "\n", encoding="utf-8")
        print(f"  written:    {rel(out_path)}", file=sys.stderr)
    else:
        print(filled)


if __name__ == "__main__":
    main()
