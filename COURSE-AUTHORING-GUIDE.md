# DrKaur Course Authoring Guide

Step-by-step playbook for designing instructor-led courses with Marp slides, lab guides, and the Python maintenance scripts in this template.

---

## Storage layout

All DrKaur courses live under **`D:\Current_work\`**:

| Path | Purpose |
|------|---------|
| `D:\Current_work\drkaur-course-template\` | Cloneable template (do not edit for a live course) |
| `D:\Current_work\<course-slug>\` | Each course you deliver |
| `D:\Current_work\Springpeople_AI_Cursor_Training_Montreal_May_2026\Cursor_Docs_Slides\` | Full-scale reference (Cursor training) |

---

## Prerequisites

1. **Node.js** — for Marp CLI: `npx @marp-team/marp-cli`
2. **Python 3** with PyYAML: `pip install pyyaml`
3. **Cursor or VS Code** with the [Marp extension](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode)
4. Do **not** use generic Markdown-PDF extensions — they ignore `marp: true` and break slide layout

---

## 1. Bootstrap a new course

From the template folder:

```powershell
cd D:\Current_work\drkaur-course-template
python scripts/scaffold_course.py `
  --name "Advanced Python Workshop" `
  --slug "advanced-python-workshop" `
  --days 2 `
  --modules 6 `
  --org "DrKaur"
```

This creates **`D:\Current_work\advanced-python-workshop\`** with:

- `course.config.yaml` — course metadata and module list
- `FINAL_TABLE_OF_CONTENTS.md` — skeleton outline
- `slides/course-complete-marp-with-notes.md` — title, agenda, module openers
- `slide-exercises/module-NN/` and `slides/assets/module-NN/` directories
- `README.md` and `COURSE-CHEATSHEET.md`

Optional: pre-fill module titles from an existing outline:

```powershell
python scripts/scaffold_course.py --name "My Course" --slug "my-course" --from-toc outline.md
```

Module titles are read from lines like `## Module 1. Title Here` in the outline file.

---

## 2. Design phase — write the TOC first

Edit [`FINAL_TABLE_OF_CONTENTS.md`](FINAL_TABLE_OF_CONTENTS.md) before writing slides:

- Module titles and day assignments
- Lesson numbers (e.g. 2.3 = Module 2, Lesson 3)
- Estimated durations
- Exercise list with links to lab guides

Keep **`course.config.yaml`** in sync — update the `modules:` list when module titles or durations change.

---

## 3. Lab-first for exercises

For every hands-on block, create a lab guide **before** (or in parallel with) exercise slides:

**Path:** `slide-exercises/module-NN/exercise-M.N-short-slug.md`

**Naming:** `exercise-{module}.{number}-{slug}.md` (zero-padded module folder: `module-02`)

**Required section for sync scripts:**

```markdown
## Steps from the training slides

### Step 1 — Short title

**Do this:** What the learner does.

**Expected result:** What they should see.

---

### Step 2 — Next step
...
```

See [`slide-exercises/module-01/exercise-1.1-sample-lab.md`](slide-exercises/module-01/exercise-1.1-sample-lab.md) for the full pattern including Cursor basics and success criteria.

---

## 4. Slide authoring

Edit the **single monolithic** Marp deck: [`slides/course-complete-marp-with-notes.md`](slides/course-complete-marp-with-notes.md)

Do **not** split into per-module source files unless you have a strong maintenance reason.

### Front matter

```yaml
---
marp: true
theme: flat-gaia
paginate: true
footer: '© 2026 by Innovation In Software Corporation'
---
```

Do **not** set `header:` — slide titles use `# h1` only (corporate deck style).

Put the first `<!-- _class: lead -->` slide **immediately** after front matter. Do not insert HTML comments or `---` between front matter and the title slide — that creates a blank first slide.

### Typography (`flat-gaia` theme)

Enforced in [`scripts/themes/flat-gaia.css`](scripts/themes/flat-gaia.css). Do not override in slide markdown.

| Element | Font | Size | Color |
|---------|------|------|-------|
| **Headings** (`h1`, `h2`, `h3`) | Leelawadee UI | 36px | Dark red (`#c00000`) |
| **Body** (paragraphs, lists, tables) | Nirmala UI | 22px | Black (`#000000`) |
| **Footer** | Nirmala UI | 13px | Grey (`#555555`) |
| **Page number** | Leelawadee UI | 18px | Dark red (`#c00000`) |

Dense slides (`fit-md`, `fit-sm`, `fit-xs`) scale both sizes down proportionally while keeping the same fonts and colors.

### Slide chrome

- **Accent bar:** red/black vertical stripe on the right edge of content slides
- **Footer:** copyright text left; page number right (via `paginate: true`)
- **Divider:** dark red vertical line (`#c00000`, same as headings) between columns on split slides

### Slide layouts (two content layouts)

| Layout | Class | Structure |
|--------|-------|-----------|
| **Single column** | `content` | `# Title` + body bullets, tables, or code |
| **Two column** | `split` | `# Title` + text left + image/diagram right |

**Split layout pattern:**

```markdown
<!-- _class: split -->

# Lesson Title

<div class="cols">
<div class="col-text">

- Key point one
- Key point two

</div>
<div class="col-visual">

![w:440](assets/module-01/diagram.svg)

</div>
</div>
```

Combine with `fit-md` / `fit-sm` on dense slides: `<!-- _class: split fit-md -->`.

### Slide types reference

| Type | Marp directives | When to use |
|------|-----------------|-------------|
| Title | `<!-- _class: lead -->` + `# Course Name` | Course opener |
| Agenda | `<!-- _class: content -->` + table or bullets | After title slide |
| Module opener | `<!-- _class: lead -->` | Start of each module |
| Lesson (visual) | `<!-- _class: split -->` + `.cols` / `.col-text` / `.col-visual` | Concept + diagram |
| Lesson (text) | `<!-- _class: content -->` + bullets or table | Text-only or dense tables |
| Dense content | Add `fit-md`, `fit-sm`, or `fit-xs` to layout class | Long lists or code |
| Exercise steps | `## Exercise M.N — Steps 1–2` | Two lab steps per slide |
| Diagram | Place in `.col-visual` (split) or inline (content) | Paths relative to `slides/` |

### Presenter notes

Add instructor script in HTML comments on each slide:

```markdown
<!--
Read this aloud: welcome the class, state the objective, mention timing.
-->
```

Regenerate standalone notes with:

```powershell
python scripts/generate-speaker-notes.py
```

---

## 5. Metadata

When you add exercises, update [`scripts/exercise_meta.py`](scripts/exercise_meta.py):

```python
EXERCISE_META: dict[tuple[int, int], dict] = {
    (2, 1): {
        "title": "First Exercise Title",
        "time": "20 min",
        "type": "hands-on",
        "objective": "What learners will accomplish.",
    },
}
```

Speaker-note generation uses this for exercise briefings.

---

## 6. Diagrams

- Store SVGs under `slides/assets/module-NN/`
- Reference from the deck: `<img src="assets/module-01/my-diagram.svg" alt="..." width="720">`
- Regenerate monospace-panel SVGs: `python scripts/regenerate-marp-diagram-svgs.py`
- Add custom generators in `scripts/custom_diagram_svgs.py` when needed (optional)
- **Cursor prompt:** copy from [`diagram-prompt.md`](diagram-prompt.md) when asking Agent to generate new SVGs

---

## 7. Maintenance commands

Run from the course repository root:

| Command | When |
|---------|------|
| `python scripts/inject-lab-guide-links.py` | After adding new exercises — links lab guides on first exercise slide |
| `python scripts/sync-exercise-steps-to-slides.py` | After editing lab guide steps — syncs key steps into exercise slides |
| `python scripts/generate-speaker-notes.py` | After slide edits — refreshes speaker notes |
| `python scripts/regenerate-marp-diagram-svgs.py` | After editing diagram SVG sources |

---

## 8. Export and present

**Always present from the HTML export**, not live Marp preview in production.

```powershell
npx @marp-team/marp-cli slides/course-complete-marp-with-notes.md `
  --html --allow-local-files `
  --theme-set scripts/themes/flat-gaia.css `
  --no-stdin `
  -o slides/course-complete-marp-with-notes.html
```

Or use VS Code tasks: **Marp: Export HTML (slides)** with the deck file open.

Optional PDF: task **Marp: Export PDF (slides)**

Optional editable PowerPoint: `scripts/export-editable-pptx.ps1`

---

## 9. Quality checklist

Before delivering a course:

- [ ] `FINAL_TABLE_OF_CONTENTS.md` matches deck headings and timings
- [ ] Every exercise in the TOC has a lab guide under `slide-exercises/`
- [ ] `python scripts/inject-lab-guide-links.py` has been run — exercise slides link to lab guides
- [ ] `course.config.yaml` module list matches the agenda slide and TOC
- [ ] Presenter notes exist on title, module openers, and exercise slides
- [ ] HTML export opens correctly in a browser with diagrams visible
- [ ] `COURSE-CHEATSHEET.md` covers acronyms introduced in each module

---

## 10. Working with Cursor Agent

Use the **`drkaur-course-design`** skill when asking Cursor to:

- Add a module, lesson, or exercise
- Write lab guides or slide content
- Run maintenance scripts or export the deck

Example prompts:

- "Add Module 3 Lesson 3.2 slides and a lab guide following our course conventions."
- "Sync exercise steps from the lab guide into the Marp deck and regenerate speaker notes."

The skill enforces this guide's conventions automatically.

---

## Reference implementation

The Cursor Training Program at:

`D:\Current_work\Springpeople_AI_Cursor_Training_Montreal_May_2026\Cursor_Docs_Slides\`

…is a complete 10-module, 40-exercise example of this pipeline at full scale.
