# Figure Style Guide

Reference for designing the hand-drawn SVG figures/diagrams embedded in the lecture `.qmd` files (via ` ```{=html} ` blocks). The goal is that every figure across all 12 lectures looks like it belongs to the same visual system, even though they're authored individually over time.

This guide covers **figures only** — flowcharts, plots, network diagrams, loss landscapes, etc. It does not cover the page's body typography, which is controlled separately by `_quarto.yml` (theme, base font size) and `styles/custom.css`.

Not a rendered book chapter — this file lives at the project root next to `notation.qmd` purely as an authoring reference.

---

## 1. Typography

**Font family:** Helvetica, applied once on the outer `<svg>` so every nested `<text>` inherits it:

```html
<svg viewBox="0 0 680 200" width="100%"
     style="max-width:680px;display:block;margin:auto;font-family:Helvetica,'Helvetica Neue',Arial,sans-serif;">
```

Always use the full fallback stack (`Helvetica, 'Helvetica Neue', Arial, sans-serif`) — plain `Helvetica` alone is not guaranteed to exist on every OS/browser, but this stack degrades gracefully everywhere.

**Minimum sizes** (figures are read at a distance / projected, so bias larger over smaller):

| Role | Min. size | Weight | Example |
|---|---|---|---|
| Figure / panel title | **24px** | 600 | "Classic ML", "Deep Learning" |
| Axis labels (x/y titles) | **16px** | 400 | "parameter", "train loss" |
| Node / box labels (primary content) | **16px** | 600 | "Layer 1", "Feature Extraction" |
| Axis tick labels | 14px | 400 | tick values, if shown |
| Secondary annotation / caption | 14px | 400 or italic | "hand-designed", "x ∈ ℝᵈ" |
| Legend text | 14px | 400 | swatch labels |

Never go below 14px anywhere in a figure, even for the smallest fine print. These are floors, not targets — round up rather than down when a label needs more room.

---

## 2. Color System

### 2.1 Primary palette — "Pastel Rainbow"

Use these six pastel fills as the default palette for boxes, nodes, and regions. Each has a matching **stroke** (medium, for borders/lines) and **ink** (dark, for text on/near that color) derived from the same hue, so contrast stays readable without leaving the pastel family.

| Role | Fill (pastel) | Stroke | Ink (text) |
|---|---|---|---|
| Input / data | `#C6DEF1` | `#5795C7` | `#205279` |
| Features / hidden layers / processing | `#C9E4DE` | `#57C7AE` | `#207965` |
| Neutral step / hand-designed / intermediate | `#FAEDCB` | `#C7A857` | `#796020` |
| Model parameters / weights | `#DBCDF0` | `#8457C7` | `#442079` |
| Classifier / decision / loss | `#F2C6DE` | `#C75794` | `#792051` |
| Output / prediction | `#F7D9C4` | `#C78557` | `#794520` |

Usage pattern for a box:
```html
<rect fill="#C9E4DE" stroke="#57C7AE" stroke-width="1.5" rx="6" .../>
<text fill="#207965" font-weight="600" ...>Layer 1</text>
```

Keep the same role → color mapping across lectures (e.g. input is always the blue swatch, output is always the peach swatch) so students build a visual vocabulary over time.

### 2.2 "Sharp mode" — reserved accent colors

Outside the pastel system, use these three saturated colors **only** when a figure needs to flag something unambiguously — correctness, state, or a semantic milestone (start/stuck/converged, right/wrong, pass/fail):

| Meaning | Color |
|---|---|
| Start / in-progress / caution | `#fbc02d` (yellow) |
| Error / stuck / incorrect / diverging | `#e53935` (red) |
| Success / converged / correct / optimum found | `#2e7d32` (green) |

Don't reach for red/yellow/green as generic decoration — reserve them so the "alert" meaning stays strong. (Established precedent: the loss-landscape figure in Lecture 1 uses exactly this trio for start/local-optimum/global-optimum.)

### 2.3 Neutral / structural colors

For axes, arrows, connecting lines, and de-emphasized captions, use grays rather than a palette color:

| Role | Color |
|---|---|
| Axis lines, arrows | `#555` or `#888` |
| Muted caption / secondary text | `#666` |
| Very light gridlines | `#ccc` |

---

## 3. Shapes, Lines & Layout

- **Boxes:** rounded rects, `rx="6"`–`8`. In any single flowchart, keep all top-level boxes the **same width and height** — pick one size (e.g. `115×66`) and stick to it rather than sizing boxes to fit their text.
- **Borders:** `stroke-width="1.5"` for boxes/nodes; `2–2.5` for plotted curves/lines that are the main subject of the figure.
- **Arrows:** define one `<marker>` per figure and reuse it for every connector:
  ```html
  <marker id="arr1" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
    <path d="M0,0 L0,6 L6,3 z" fill="#888"/>
  </marker>
  ```
- **Captions below boxes:** when a flowchart needs an annotation under each box (e.g. "hand-designed", "learned"), align them all on one shared caption row (same `y`) rather than at varying heights.
- **Curves that plot a real function** (loss landscapes, activation functions): sample the function explicitly and build a smooth path through exact points (e.g. Catmull-Rom → cubic Bézier) rather than hand-picked Bézier control points. Any dot/marker placed "on" the curve must be verified to sit at an exact sampled point — control points are not on the curve.

---

## 4. Minimal Template

A starting point for a new box-and-arrow figure that follows every rule above:

```html
<div style="overflow-x:auto; margin:1.5rem 0;">
<svg viewBox="0 0 500 160" width="100%"
     style="max-width:500px;display:block;margin:auto;font-family:Helvetica,'Helvetica Neue',Arial,sans-serif;">
  <defs>
    <marker id="arr1" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="#888"/>
    </marker>
  </defs>

  <text x="250" y="28" text-anchor="middle" font-size="24" font-weight="600" fill="#333">Figure Title</text>

  <rect x="20"  y="60" width="120" height="66" rx="6" fill="#C6DEF1" stroke="#5795C7" stroke-width="1.5"/>
  <text x="80" y="98" text-anchor="middle" font-size="16" font-weight="600" fill="#205279">Input</text>

  <line x1="140" y1="93" x2="176" y2="93" stroke="#888" stroke-width="1.5" marker-end="url(#arr1)"/>

  <rect x="178" y="60" width="120" height="66" rx="6" fill="#C9E4DE" stroke="#57C7AE" stroke-width="1.5"/>
  <text x="238" y="98" text-anchor="middle" font-size="16" font-weight="600" fill="#207965">Process</text>
</svg>
</div>
```

---

## 5. Checklist for New Figures

- [ ] `font-family` set to the Helvetica stack on the outer `<svg>`
- [ ] Title ≥ 24px, axis labels ≥ 16px, nothing anywhere below 14px
- [ ] Colors drawn from the Pastel Rainbow role table (§2.1), not one-off hex values
- [ ] Red/yellow/green used only for genuine start/error/success signaling
- [ ] All top-level boxes in a flowchart share one size
- [ ] Dots/markers on a plotted curve verified to sit exactly on a sampled point
- [ ] Rendered and visually checked (e.g. headless-Chrome screenshot) before considering the figure done

