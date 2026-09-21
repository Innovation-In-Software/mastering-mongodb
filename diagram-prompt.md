# Diagram generation prompt

Copy-paste into Cursor when creating SVG diagrams for Marp slides. Matches the visual style used in the DrKaur / Cursor training slide decks.

---

## Full prompt

```text
Create a Marp slide diagram for my instructor-led course.

## Context
- Course: [COURSE NAME]
- Module: [N] — [MODULE TITLE]
- Slide / lesson: [e.g. Lesson 3.2 — Authentication flow]
- Diagram purpose: [one sentence — e.g. "Show request flow from browser to API to database"]

## Output requirements
1. Save as SVG at: slides/assets/module-[NN]/[short-slug].svg
   Example: slides/assets/module-03/auth-request-flow.svg
2. Use this exact visual style (match the Cursor training slides):
   - Canvas width: 920px (height as needed, max ~500px for dense slides)
   - Panel background: #f7f7f7, border: #d0d0d0, rounded corners (rx=10)
   - Accent / arrows / box borders: #cc0000
   - Primary text: #1a1a1a, muted captions: #666666
   - Box fill: #ffffff with #cc0000 stroke
   - Fonts: Arial, Helvetica, sans-serif for labels (22px body, 20px small)
   - Monospace blocks: Consolas, Courier New (23px) on #f7f7f7 panel
   - Red arrow markers on flow lines (bidirectional where needed)
3. Diagram type: [pick one]
   - Flow diagram (boxes + arrows)
   - Architecture diagram (layers / components)
   - Comparison (left vs right, or table-style with header row #ffebeb)
   - Monospace panel (ASCII-style steps, commands, or pseudo-code)
   - Timeline / pipeline (left-to-right stages)
4. Keep text short — labels must be readable when embedded at width 720 in Marp
5. No photos, icons from external URLs, or dark backgrounds — light theme only

## Content to visualize
[Paste bullets, steps, or concepts from your slide here]

Example:
- User submits login form
- API validates credentials
- JWT returned to client
- Client stores token and calls protected routes

## Slide embed
After creating the SVG, add this to the Marp deck slide:
<img src="assets/module-[NN]/[short-slug].svg" alt="[description]" width="720">

## Optional: register for regeneration
If this diagram will be updated often, add a generator function in scripts/custom_diagram_svgs.py
using colors from scripts/marp_svg_common.py, then run:
python scripts/regenerate-marp-diagram-svgs.py
```

---

## Short prompt (quick diagrams)

```text
Generate an SVG diagram for module [N] of [COURSE NAME].

Style: 920px wide, light panel (#f7f7f7), red accents (#cc0000), Arial labels,
white rounded boxes, red arrows. Match DrKaur / Cursor training slide diagrams.

Show: [describe the concept in 2–4 bullets]

Save to: slides/assets/module-[NN]/[slug].svg
Embed in slide: <img src="assets/module-[NN]/[slug].svg" alt="..." width="720">
```

---

## Style reference (tokens)

These values are defined in `scripts/marp_svg_common.py`:

| Token | Value | Use |
|-------|-------|-----|
| Accent / arrows | `#cc0000` | Box borders, flow lines, headings |
| Primary text | `#1a1a1a` | Labels inside boxes |
| Muted text | `#666666` | Captions, footnotes |
| Panel background | `#f7f7f7` | Diagram canvas fill |
| Table header | `#ffebeb` | Comparison / table-style diagrams |
| Border | `#d0d0d0` | Outer panel stroke |
| Box fill | `#ffffff` | Component boxes |
| Label font | Arial, 22px | Box labels |
| Monospace font | Consolas, 23px | Code / ASCII panels |

---

## Tips

1. **Be specific about diagram type** — “flow with 4 boxes left-to-right” works better than “make a diagram about auth.”
2. **One idea per diagram** — same rule as full-scale reference courses.
3. **Use the `drkaur-course-design` skill** — add “following our course conventions” so paths and Marp embed syntax stay consistent.
4. **Code-heavy slides** → ask for a **monospace panel** (commands, API examples, step lists).
5. **Concept slides** → ask for a **flow or architecture diagram**.

## Reference examples

Full-scale diagram examples live in the reference Cursor course:

`D:\Current_work\Springpeople_AI_Cursor_Training_Montreal_May_2026\Cursor_Docs_Slides\slides\assets\`

Notable examples:

- `module-03/the-mode-continuum.svg` — flow with labeled boxes and arrows
- `module-01/tool-calling-flow.svg` — pipeline / sequence
- `module-01/context-pyramid.svg` — layered hierarchy
- Monospace panels — generated via `scripts/marp_svg_common.py` → `monospace_panel_svg()`
