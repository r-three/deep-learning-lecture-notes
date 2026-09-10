#!/usr/bin/env python3
"""Build a *fidelity-test* prompt for a lecture write-up.

Where `gen_lecture_prompt.py` produces the prompt that drafts a lecture, this
script produces the prompt that *audits* an already-drafted lecture: it asks
Claude to compare the `.qmd` against its source transcript and slides (and any
bonus PDF), write every discrepancy to a plain-text report, and then update the
`.qmd` to add the missing content and fix the misaligned content — without
importing anything the lecture did not cover, and preserving Colin Raffel's
voice per `website/persona.md`.

The comparison itself is semantic (prose vs. a spoken transcript vs. hand-drawn
slides), so it is done by Claude when the prompt is run — this script only
detects the files and fills the prompt, mirroring `gen_lecture_prompt.py`.

Usage:
    python gen_fidelity_prompt.py 11                 # print prompt to stdout
    python gen_fidelity_prompt.py 11 --write         # save alongside the sources
    python gen_fidelity_prompt.py 12 --report qa.txt # custom report filename

By default the filled prompt is printed to stdout. Pass --write to save it to
`lecture_notes/Lecture <N>/fidelity-prompt.filled.md`.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Reuse the sibling script's conventions (folder layout, source detection).
from gen_lecture_prompt import REPO, find_lecture_dir, detect_sources

LECTURES_DIR = REPO / "website" / "lectures"
DEFAULT_REPORT = "fidelity-report.txt"

# The fidelity-test prompt. Placeholders (<...>) are substituted in fill().
PROMPT_TEMPLATE = """\
Run a **fidelity test** on the Lecture <N> write-up: check that the drafted
Quarto notes faithfully and accurately reflect the lecture's transcript and
slides, record every discrepancy in a plain-text report, and then correct the
`.qmd`.

**Files**

- Lecture notes (the file under test): `<qmd>`
- Transcript (spoken source of truth): `<transcript>`
- Slides / notes PDF (visual source of truth): `<slides>`<bonus_line>

**Reference guides — read first and apply throughout:**

1. `website/persona.md` — the controlling voice and structure guide. §4
   ("Fidelity to source material") and §7 (the checklist) define what "faithful"
   means here: stay close to the content and ordering of the transcript and
   slides; do not import material, framings, or examples the lecture did not
   use; keep the calm, measured register (no hype, no exclamations in prose).
2. `website/notation.qmd` — symbol conventions the `.qmd` must follow.
3. `website/style.md` — figure conventions (only relevant if a figure misstates
   the source).

The canonical prose reference is `website/lectures/01-intro-regression.qmd`.

**Step 1 — Compare.** Read the `.qmd` in full, then the transcript and the
slides (every page). Work through the lecture in the order the lecturer actually
presented it and check the write-up against the sources.

**Step 2 — Write the report.** Record every discrepancy in a plain-text file at
`<report>` (overwrite it if it exists). Group findings under these headings, and
for each finding give the `.qmd` location (section heading and a short quote),
what the source says vs. what the `.qmd` says, and a severity (high / medium /
low):

- `MISSING` — substantive content, examples, definitions, equations, caveats, or
  steps that appear in the transcript or slides but are absent from the `.qmd`.
- `MISALIGNED / INCORRECT` — statements in the `.qmd` that contradict or misstate
  the source: wrong equations, wrong numbers, swapped meanings, an example
  attributed to the wrong concept, a hedge dropped or overstated.
- `UNSOURCED ADDITIONS` — claims, framings, or examples in the `.qmd` that the
  transcript and slides do not support (persona §4 forbids imported material).
- `ORDERING` — places where the `.qmd` reorders the lecturer's actual sequence in
  a way that changes the through-line.
- `NOTATION / VOICE` — symbols inconsistent with `notation.qmd`, or wording that
  breaks the measured register of persona §3 (flag only if genuinely present).

If a section is fully faithful, say so briefly rather than padding the report.
End the report with a short prioritized summary (the high-severity items first).

**Step 3 — Fix the `.qmd`.** Update `<qmd>` to resolve the `MISSING` and
`MISALIGNED / INCORRECT` findings: add the missing substance and correct the
misaligned statements, drawing only on the transcript and slides. Make targeted
edits — do not rewrite faithful passages, and preserve the existing structure,
notation, figures, and Colin's voice. For `UNSOURCED ADDITIONS`, remove or
rein in the unsupported material unless it is a minimal, standard bridging
explanation (persona §4 allows the latter). Leave `ORDERING` and
`NOTATION / VOICE` items to your judgement, noting in the report which you chose
not to change and why.

**Step 4 — Verify and summarize.** Re-run `quarto render` on the updated `.qmd`
and confirm it compiles with no broken math, figures, or citation anchors. Then
give a concise summary of what the report flagged and what you changed, and
confirm the report was written to `<report>`.

Do not introduce hype adjectives, filler openers, manufactured surprise, or
exclamation marks. Keep the register calm and precise throughout.
"""


def find_qmd(n: int) -> Path:
    """Locate the drafted `.qmd` by its zero-padded number prefix."""
    matches = sorted(LECTURES_DIR.glob(f"{n:02d}-*.qmd"))
    if not matches:
        sys.exit(f"error: no lecture .qmd matching {n:02d}-*.qmd in {LECTURES_DIR}")
    if len(matches) > 1:
        names = ", ".join(p.name for p in matches)
        sys.exit(f"error: multiple .qmd files match {n:02d}-*.qmd: {names}")
    return matches[0]


def rel(p: Path) -> str:
    """Repo-relative POSIX path for embedding in the prompt."""
    return p.resolve().relative_to(REPO).as_posix()


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
                    help="save to lecture_notes/Lecture <N>/fidelity-prompt.filled.md "
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
    print(f"Fidelity test — Lecture {n}", file=sys.stderr)
    print(f"  qmd:        {rel(qmd)}", file=sys.stderr)
    print(f"  transcript: {rel(transcript)}", file=sys.stderr)
    print(f"  slides:     {rel(slides)}", file=sys.stderr)
    for b in bonus:
        print(f"  bonus:      {rel(b)}", file=sys.stderr)
    print(f"  report:     {rel(report)}", file=sys.stderr)

    if args.write:
        out_path = lecture_dir / "fidelity-prompt.filled.md"
        out_path.write_text(filled + "\n", encoding="utf-8")
        print(f"  written:    {rel(out_path)}", file=sys.stderr)
    else:
        print(filled)


if __name__ == "__main__":
    main()
