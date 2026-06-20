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
