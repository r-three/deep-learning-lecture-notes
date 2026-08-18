# CSC413 / 2516: Deep Learning — Fall 2026

Interactive lecture notes for CSC413 / CSC2516 Deep Learning at the University of Toronto.
Built with [Quarto](https://quarto.org/) and [Observable JS](https://observablehq.com/).

---

## Prerequisites

Install [Quarto](https://quarto.org/docs/get-started/) (v1.4 or later):

```bash
# macOS (Homebrew)
brew install quarto

# Verify
quarto --version
```

No Python or R installation is required — all interactive visualisations run
directly in the browser via Observable JS.

---

## Running Locally

```bash
cd website
quarto preview
```

This starts a local dev server (default `http://localhost:4848`) and
**live-reloads** whenever you save a `.qmd` or `.css` file.

---

## Building a Static Site

```bash
cd website
quarto render
```

Output is written to `website/_site/`. Those files are plain HTML/CSS/JS and
can be served from any static host — no server needed.

---

## Deploying to GitHub Pages

```bash
cd website
quarto publish gh-pages
```

Quarto pushes the rendered `_site/` to the `gh-pages` branch automatically.
Enable GitHub Pages in the repo settings (source: `gh-pages` branch, root `/`).

---

## Adding a New Lecture

1. Create `website/lectures/NN-topic.qmd` (copy the header from an existing file).
2. Add one line to `website/_quarto.yml` under `chapters:`:
   ```yaml
   chapters:
     - index.qmd
     - lectures/02-mlp-backprop.qmd
     - lectures/03-regularization.qmd   # ← new line
   ```
3. Save — the preview server picks up the change immediately.

---

## Authoring a Lecture from Notes (Transcript + Slides)

Each lecture is written from its **transcript** and **slides** in
`lecture_notes/Lecture <N>/`, following three reference guides:
`website/persona.md` (voice and structure), `website/notation.qmd` (symbols),
and `website/style.md` (figures). Three helper scripts at the repo root turn
this into a repeatable, three-stage pipeline: **draft → refine text → fix
figures**. Each script *generates a prompt* — you run that prompt in Claude Code,
which reads the sources plus the guides and does the writing or editing. The
scripts themselves only detect files and fill the prompt; they do not call a
model.

**Prerequisites for this pipeline** (not needed to build or view the site):
Python 3 (standard library only — no packages to install) for the scripts, and
Google Chrome for the figure-render check in the visual pass.

Expected source layout (filenames are auto-detected, case- and space-insensitive):

```
lecture_notes/Lecture 11/
  lecture11_transcript.txt   # the spoken transcript
  Lecture11.pdf              # the slides / notes PDF
  [anything *bonus* / *supplement* .pdf is picked up too]
```

### 1. Draft the `.qmd`

```bash
python gen_lecture_prompt.py 11 --title "Architecture Grab Bag, Part 2 — Transposed Convolution, the U-Net, Autoencoders, and VAEs" --write
```

Writes `lecture_notes/Lecture 11/generation-prompt.filled.md`. Hand that prompt
to Claude Code; it reads the transcript, slides, and the three guides, then
drafts `website/lectures/11-<slug>.qmd` — prose in the lecture's measured voice,
with inline SVG figures. Afterward, wire the file into `_quarto.yml` (see
[Adding a New Lecture](#adding-a-new-lecture)) and run `quarto render` to confirm
it compiles.

### 2. Refine the text for alignment (fidelity pass)

```bash
python gen_fidelity_prompt.py 11 --write
```

Writes `lecture_notes/Lecture 11/fidelity-prompt.filled.md`. Running that prompt
compares the drafted `.qmd` against the transcript and slides, records every
discrepancy — `MISSING`, `MISALIGNED / INCORRECT`, `UNSOURCED ADDITIONS`,
`ORDERING`, `NOTATION / VOICE` — in `lecture_notes/Lecture 11/fidelity-report.txt`,
and then edits the `.qmd` to add the missing substance and correct the
misaligned statements (targeted edits only, preserving voice and structure).

### 3. Adjust and fix the figures (visual pass)

```bash
python gen_visual_prompt.py 11 --write
```

Writes `lecture_notes/Lecture 11/visual-prompt.filled.md`. Running that prompt
renders each inline SVG (headless Chrome screenshot), *looks* at it next to the
hand-drawn slide, and flags wrong numbers/labels and layout problems (overlaps,
clipping, off-canvas text, misalignment, palette misuse). Findings go to
`lecture_notes/Lecture 11/visual-report.txt`, and the SVG coordinates, labels,
and values in the `.qmd` are corrected and re-rendered until each figure matches
its source.

**Options** (all three scripts):

- Omit `--write` to print the prompt to stdout instead of saving it.
- `--report <name>` overrides the report filename (passes 2 and 3).
- `gen_lecture_prompt.py` needs `--title "..."` unless the lecture is in its
  built-in registry; `--slug` is derived from the title if omitted.
- After each stage, `cd website && quarto render lectures/11-<slug>.qmd` to
  confirm the page still compiles (SVGs intact, no broken math or citations).

---

## Writing Interactive Widgets

Observable JS chunks are fenced with ` ```{ojs} `. They have access to:

| Global | Description |
|---|---|
| `Plot` | [Observable Plot](https://observablehq.com/plot/) for charts |
| `d3` | D3.js v7 for custom SVG |
| `Inputs` | Sliders, checkboxes, toggles |
| `html`, `svg`, `md` | Tagged template literals |

Example — a live slider controlling a plot:

````markdown
```{ojs}
viewof n = Inputs.range([1, 20], {step: 1, label: "n", value: 5})
Plot.plot({ marks: [Plot.line(Array.from({length: n}, (_, i) => ({x: i, y: i**2}))), {x:"x", y:"y"}] })
```
````

---

## Style Guide

The site follows the aesthetic of [visionbook.mit.edu](https://visionbook.mit.edu/) with UofT branding:

- **Body font:** Source Serif 4 (serif, academic)
- **Code font:** Source Code Pro
- **Theme:** Quarto `cosmo` (light) / `darkly` (dark)
- **Accent colour:** UofT navy `#002A5C` — headings, links, table headers, callout borders
- No gradients, no colour fills — borders and whitespace carry the hierarchy
- Callout boxes: left border only, near-white background
- Boxed equations: thin navy border, no fill

Custom CSS lives in `website/styles/custom.css`.
