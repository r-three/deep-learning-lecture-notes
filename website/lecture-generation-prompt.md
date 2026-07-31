# Lecture Generation Prompt

A reusable prompt for drafting a lecture `.qmd` from its source materials. Fill in the `<...>` placeholders and paste it as the task. Not a rendered book chapter — an authoring reference only; do not add it to `_quarto.yml`.

---

## Prompt

Write the lecture notes for **Lecture <N>: <Title>** as a Quarto file at `website/lectures/<NN>-<slug>.qmd`.

**Source material** (the notes must be a faithful write-up of these, not a fresh essay on the topic):

- Transcript: `lecture_notes/Lecture <N>/<transcript>.txt`
- Slides / notes PDF: `lecture_notes/Lecture <N>/<slides>.pdf`
- Any bonus/supplementary PDF in that folder.

**Read these three reference files first and follow them throughout:**

1. `website/persona.md` — the writing voice and page structure. This is the controlling guide. Colin Raffel's measured voice: motivate before formalize, hedge honestly, and **no punchy or hype wording** (see its §2–§3). Match the scaffolding in §5 (frontmatter, `.lecture-header` block, `.definition-block` / `.boxed-eq` / `.algorithm` / `callout-*` classes, `**Overview.**` opener, `## Summary` + `**Next lecture:**` closer).
2. `website/notation.qmd` — symbol conventions. Use `\bm{x}`, `\bm{W}`, `\mathcal{L}`, `\bm{\theta}`, `\hat{y}`, etc. consistently; keep each symbol's meaning aligned with that table.
3. `website/style.md` — figure style. Any diagrams are inline SVG using the Helvetica stack and the Pastel Rainbow role palette (reserve red/yellow/green for start/error/success). For plotted data, use Paul Tol's "bright"/"light" schemes.

**The canonical prose reference** is `website/lectures/01-intro-regression.qmd` (hand-edited by Colin). When the guides leave something ambiguous, imitate that file's prose and structure.

**Process:**

1. Read `persona.md`, `notation.qmd`, and `style.md` in full, then skim Lecture 1 for tone.
2. Read the transcript and slides PDF for Lecture <N>. Build the section outline from the ordering the lecturer actually used — do not restructure or import outside material.
3. Draft the `.qmd`, smoothing the spoken transcript into natural written prose while preserving its substance, examples, and through-line. Carry one running example through each section where the lecture does.
4. Add figures only where they aid understanding, following `style.md`. Render and visually check any figure before considering it done.
5. Verify the checklist in `persona.md` §7. Add the new chapter to `_quarto.yml` under `book.chapters`.
6. Build with `quarto render` (or preview) and confirm the page compiles without errors before finishing.

**Do not** add hype adjectives, filler openers, manufactured surprise, or exclamation marks in body prose. Keep the register calm and precise throughout.

---

## Notes for the requester

- Replace `<N>`, `<Title>`, `<NN>` (zero-padded, e.g. `04`), `<slug>` (kebab-case, e.g. `optimization`), and the exact source filenames before sending.
- Confirm the source files exist in `lecture_notes/Lecture <N>/` first — as of this writing only Lectures 1 and 3 have materials on disk.
- If the lecture warrants an interactive demo, mention it — Observable JS (` ```{ojs} `) blocks are available (see Lecture 1's gradient-descent figure).
