#!/usr/bin/env python3
"""Fill the lecture-generation prompt template for a given lecture.

Reads the `## Prompt` section of `website/lecture-generation-prompt.md` (the
single source of truth) and substitutes the `<...>` placeholders with concrete
values for one lecture: number, title, slug, and the source filenames detected
in `lecture_notes/Lecture <N>/`.

Usage:
    python gen_lecture_prompt.py 4 --title "Optimization"
    python gen_lecture_prompt.py 4 --title "Optimization" --slug optimization
    python gen_lecture_prompt.py 1                 # uses the built-in registry
    python gen_lecture_prompt.py 4 -t "Optimization" --write

By default the filled prompt is printed to stdout. Pass --write to save it to
`lecture_notes/Lecture <N>/generation-prompt.filled.md`.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
TEMPLATE = REPO / "website" / "lecture-generation-prompt.md"

# Known lecture titles/slugs. Anything not listed can be supplied via --title/--slug.
LECTURES: dict[int, tuple[str, str]] = {
    1: ("Introduction, Linear & Logistic Regression", "intro-regression"),
    2: ("Multilayer Perceptrons & Backpropagation", "mlp-backprop"),
    3: ("Regularization", "regularization"),
}


def slugify(title: str) -> str:
    """Turn a title into a kebab-case slug (matches the existing file names)."""
    slug = title.lower()
    slug = slug.replace("&", " and ")
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


def load_prompt_template() -> str:
    """Extract the `## Prompt` section from the template markdown file."""
    if not TEMPLATE.exists():
        sys.exit(f"error: template not found at {TEMPLATE}")
    text = TEMPLATE.read_text(encoding="utf-8")
    # Everything before the "Notes for the requester" section, after "## Prompt".
    before_notes = text.split("## Notes for the requester", 1)[0]
    if "## Prompt" not in before_notes:
        sys.exit("error: could not find a '## Prompt' section in the template")
    prompt = before_notes.split("## Prompt", 1)[1]
    # Trim surrounding whitespace and any trailing horizontal rules.
    lines = prompt.strip().splitlines()
    while lines and lines[-1].strip() in ("", "---"):
        lines.pop()
    return "\n".join(lines).strip()


def find_lecture_dir(n: int) -> Path:
    d = REPO / "lecture_notes" / f"Lecture {n}"
    if not d.is_dir():
        sys.exit(f"error: no source folder at {d}")
    return d


def detect_sources(lecture_dir: Path, n: int) -> tuple[str, str, list[str]]:
    """Return (transcript_stem, slides_stem, bonus_stems) detected in the folder.

    The canonical naming convention is `lecture<N>.pdf` for the notes and
    `lecture<N>_transcript.txt` for the transcript (case- and space-insensitive,
    so `Lecture4.pdf` or `Lecture 3.pdf` also match). Those exact patterns win;
    anything else in the folder is only used as a fallback.
    """
    def norm(stem: str) -> str:  # ignore case and spaces when matching
        return stem.lower().replace(" ", "")

    txts = sorted(lecture_dir.glob("*.txt"))
    pdfs = sorted(lecture_dir.glob("*.pdf"))

    if not txts:
        sys.exit(f"error: no transcript (.txt) found in {lecture_dir}")
    # Canonical: lecture<N>_transcript.txt; else any *transcript*; else first .txt.
    transcript = (
        next((p for p in txts if norm(p.stem) == f"lecture{n}_transcript"), None)
        or next((p for p in txts if "transcript" in p.stem.lower()), None)
        or txts[0]
    )

    if not pdfs:
        sys.exit(f"error: no slides (.pdf) found in {lecture_dir}")
    bonus_kw = ("bonus", "supplement", "extra", "appendix")
    # Canonical: lecture<N>.pdf; else the first PDF that isn't a bonus/supplement.
    non_bonus = [p for p in pdfs if not any(k in p.stem.lower() for k in bonus_kw)]
    slides = (
        next((p for p in pdfs if norm(p.stem) == f"lecture{n}"), None)
        or (non_bonus[0] if non_bonus else pdfs[0])
    )
    bonus_pdfs = [p for p in pdfs if p != slides]

    return transcript.stem, slides.stem, [p.stem for p in bonus_pdfs]


def fill(n: int, title: str, slug: str, transcript: str, slides: str) -> str:
    template = load_prompt_template()
    # Order matters: replace the longer/compound tokens before the bare "<N>".
    replacements = [
        ("<Title>", title),
        ("<NN>", f"{n:02d}"),
        ("<slug>", slug),
        ("<transcript>", transcript),
        ("<slides>", slides),
        ("<N>", str(n)),
    ]
    out = template
    for token, value in replacements:
        out = out.replace(token, value)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("number", type=int, help="lecture number, e.g. 4")
    ap.add_argument("-t", "--title", help="lecture title (required if not in the registry)")
    ap.add_argument("-s", "--slug", help="kebab-case slug (derived from the title if omitted)")
    ap.add_argument("--write", action="store_true",
                    help="save to lecture_notes/Lecture <N>/generation-prompt.filled.md "
                         "instead of printing to stdout")
    args = ap.parse_args()

    n = args.number
    title = args.title or (LECTURES[n][0] if n in LECTURES else None)
    if not title:
        sys.exit(f"error: no title for Lecture {n}; pass --title \"...\"")
    slug = args.slug or (LECTURES[n][1] if n in LECTURES and not args.title else None) or slugify(title)

    lecture_dir = find_lecture_dir(n)
    transcript, slides, bonus = detect_sources(lecture_dir, n)

    filled = fill(n, title, slug, transcript, slides)

    # Report detected sources to stderr so stdout stays clean for piping.
    print(f"Lecture {n}: {title}  (slug: {slug})", file=sys.stderr)
    print(f"  transcript: {transcript}.txt", file=sys.stderr)
    print(f"  slides:     {slides}.pdf", file=sys.stderr)
    for b in bonus:
        print(f"  bonus:      {b}.pdf", file=sys.stderr)
    print(f"  target:     website/lectures/{n:02d}-{slug}.qmd", file=sys.stderr)

    if args.write:
        out_path = lecture_dir / "generation-prompt.filled.md"
        out_path.write_text(filled + "\n", encoding="utf-8")
        print(f"  written:    {out_path.relative_to(REPO)}", file=sys.stderr)
    else:
        print(filled)


if __name__ == "__main__":
    main()
