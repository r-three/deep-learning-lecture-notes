# Writing Persona & Voice Guide

Reference for writing the lecture notes (`lectures/*.qmd`) so that every lecture reads as if written by the same person, in the same measured voice, even though they are drafted individually over time.

The lectures are Colin Raffel's. This guide captures his writing voice so that new lecture notes match it. Lecture 1 (`lectures/01-intro-regression.qmd`) has been hand-edited by Colin and is the canonical reference — when in doubt, imitate its prose, not this description of it.

This guide covers **prose and structure**. It does not cover figures (see `style.md`) or symbol conventions (see `notation.qmd`).

Not a rendered book chapter — this file lives at the project root as an authoring reference only. Do not add it to `_quarto.yml`.

---

## 1. The voice, in one paragraph

Write calmly and precisely, as a knowledgeable person explaining something to a capable reader, not as a marketer selling it. Motivate before mechanism: pose the question a concept answers, then answer it. Prefer plain, direct sentences over clever ones. Hedge where the truth is qualified ("generally", "in practice", "typically", "under benign assumptions") rather than overstating. Be honest about conventions, limitations, and misnomers. Use "we" to walk the reader through the reasoning together. Never reach for excitement the material does not itself justify.

Reference material for calibrating the voice:

- Blogs: <https://colinraffel.com/blog/when-will-language-models-be-good-enough.html>, <https://colinraffel.com/blog/three-machine-learning-publication-venues-for-the-research-agent-era.html>
- Long-form papers (entire drafts written by Colin): T5, <https://arxiv.org/abs/1910.10683>; the transfer-learning survey, <https://dl.acm.org/doi/10.1145/3545111>

---

## 2. Do

- **Motivate first, then formalize.** Open a topic with the problem it solves, often as a plain question. E.g. *"How can we design computer programs for problems that are too complex to allow for simply writing down a set of rules?"* then answer it.
- **Define terms explicitly and bold them on first use.** Put the formal statement in a `::: {.definition-block}` and **bold** the term being defined.
- **Ground abstractions in a running example.** Lecture 1 carries the house-price example through linear regression. Reuse one concrete example across a section rather than inventing a fresh one per equation.
- **Hedge honestly.** "generally", "typically", "in practice", "often", "under benign assumptions", "for the past few decades". The truth in ML is usually qualified; say so.
- **Be candid about conventions and limitations.** *"The $\frac{1}{2}$ is a convenience: it cancels the exponent of 2 when we differentiate."* / *"We deliberately ignore it."* / *"Softmax is not 'soft max'. The name is a misnomer."*
- **Use "we" and "one".** Inclusive, walking the reader through: *"we introduce", "we study", "one could start by"*.
- **Let structure carry emphasis.** Semicolons join related clauses; em-dashes set off asides. A single bolded clause at the end of a derivation can mark the payoff — *"the gradient is simply the prediction error"* — but use this sparingly.
- **Point forward and backward.** *"(Lecture 2)"*, *"building blocks for everything else in this course"*. Situate each piece in the arc of the course.
- **State what a result means after deriving it.** Follow a clean equation with one sentence of interpretation, not an exclamation.

---

## 3. Don't (avoid punchy wording)

The single most important instruction: **do not use punchy, hype-y, or breathless wording.** Keep the register calm and even.

- **No hype adjectives:** avoid "powerful", "amazing", "incredible", "revolutionary", "magical", "beautiful", "elegant" as decoration. (A result can be "remarkably clean" when it genuinely is, as in Lecture 1 — but earn it, don't sprinkle it.)
- **No filler openers / transitions:** avoid "Let's dive in", "Buckle up", "Here's the thing", "Here's the kicker", "The magic happens when", "Now for the fun part", "It turns out that…" (as a recurring tic), "Believe it or not".
- **No manufactured surprise:** avoid "Surprisingly," / "Astonishingly," / "Amazingly," unless the result is genuinely counterintuitive and you then explain why.
- **No exclamation marks** in body prose.
- **No second-person hype** ("you'll be amazed", "you might think… but you'd be wrong").
- **Don't over-signpost** with "Importantly,", "Crucially,", "Note that" on every paragraph. Let the content rank itself.
- **Don't editorialize the difficulty:** avoid "this is easy", "trivially", "obviously", "simply just" — they alienate the reader who does not find it easy. ("Simple" as a technical descriptor of a model class is fine.)

---

## 4. Fidelity to source material

Each lecture is written from a **transcript** and the **lecture slides/notes PDF** (in `lecture_notes/Lecture N/`). The prose is a faithful write-up of that lecture, not a fresh essay on the topic.

- **Stay close to the content and ordering of the transcript and slides.** Cover what the lecture covers, in roughly the sequence the lecturer chose. Do not import material, framings, or examples the lecture did not use.
- **Smooth the flow, don't restructure.** The transcript is spoken and meandering; your job is to make it read naturally on the page — tighten, remove verbal tics, connect ideas — while preserving the substance and the through-line.
- **Preserve the lecture's own examples and analogies.** If the lecturer used a specific example, use that one.
- **Don't add unsourced claims** to sound authoritative. If the lecture hedges or leaves something open, keep it open.
- **When the transcript is thin on a step,** fill the gap with the minimal, standard explanation — do not editorialize or expand into a tangent.

---

## 5. Structural conventions (Quarto `.qmd`)

Match the scaffolding of `lectures/01-intro-regression.qmd`.

**Frontmatter + header block** (the `<style>` hides Quarto's default title so the custom header shows instead):

```markdown
---
title: "Lecture N: <Title>"
description: "<one-sentence description of what the lecture builds>"
bibliography: references.bib
---

```{=html}
<style>#title-block-header { display: none; }</style>
<div class="lecture-header">
  <h1>Lecture N: <Title></h1>
</div>
```

**Overview paragraph.** Open the body with a `**Overview.**` paragraph summarizing the lecture's arc in a few sentences.

**Section headers.** `##` for major sections with an explicit id, e.g. `## Linear Regression {#sec-linear-regression}`; `###` for subsections. Separate major sections with a `---` rule where Lecture 1 does.

**Available custom block classes** (defined in `styles/custom.css`; use them, don't invent new ones):

| Block | Purpose |
|---|---|
| `::: {.definition-block}` | Formal definition; lead with `**Definition.**` and bold the term |
| `::: {.boxed-eq}` | A key equation to highlight |
| `::: {.algorithm}` | A named procedure; use `#### Name` inside, then **Initialize** / **Repeat** steps |
| `::: {.callout-note}` | Clarification or aside worth flagging (e.g. "Closed form vs. gradient descent") |
| `::: {.callout-warning}` | A common misconception or pitfall (e.g. the softmax misnomer) |
| `::: {.callout-tip}` | Practical advice |
| `::: {.callout-important}` | Something the reader must not miss |

**Summary.** Close with `## Summary {#sec-summary}` containing a `::: {.callout-note}` of `**Key takeaways from Lecture N:**` as a bulleted list, followed by a `**Next lecture:**` sentence pointing forward.

**Math.** KaTeX. Use the notation from `notation.qmd` — `\bm{x}` for vectors, `\bm{W}` for weight matrices, `\mathcal{L}` for loss, `\bm{\theta}` for the parameter collection, `\hat{y}` for predictions, etc. Keep symbol → meaning consistent with that table.

**Interactive figures.** Where a concept benefits from interactivity (Lecture 1's gradient-descent demo), Observable JS (` ```{ojs} `) blocks are available. Static diagrams are inline SVG per `style.md`.

---

## 6. Figures & color

Figures follow `style.md` (Helvetica stack, Pastel Rainbow role palette, reserved red/yellow/green for start/error/success). For any **plotted data** (charts, not diagrams), prefer Paul Tol's qualitative schemes — the "bright" and "light" sets in particular — over ad-hoc colors:

- Overview of all schemes: <https://sronpersonalpages.nl/~pault/data/colourschemes.pdf>
- Python package: <https://pypi.org/project/tol-colors/>

These are the R3 lab's coloring preferences and are preferred over the single scheme on the colorblindness page.

---

## 7. Checklist for a new lecture write-up

- [ ] Frontmatter + `.lecture-header` block match Lecture 1
- [ ] Opens with an `**Overview.**` paragraph; closes with `## Summary` takeaways + `**Next lecture:**`
- [ ] Content and ordering faithful to the transcript and slides; no imported outside material
- [ ] Voice is calm and measured — no hype adjectives, no punchy openers, no exclamation marks in prose
- [ ] Concepts motivated before formalized; terms defined in `.definition-block` and bolded on first use
- [ ] One running example carried through each section rather than one-off examples per equation
- [ ] Notation consistent with `notation.qmd`
- [ ] Custom block classes drawn from the table in §5, not newly invented
- [ ] Figures follow `style.md`; plotted data uses Paul Tol schemes
