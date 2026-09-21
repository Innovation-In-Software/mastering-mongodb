# Exercise 1.1: Choose the Appropriate Data Model

**Module 1:** Introduction to NoSQL Databases  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 1, Lesson 1.4)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Match application requirements to relational, document, key-value, column-family, or graph models, and justify each choice from access patterns—not product names.

---

## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Work in pairs or small groups. Capture answers in a notes file or on paper.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional — a table is enough |
| Timer | 12 minutes work + 3 minutes debrief | Instructor clocks this |

You do **not** need MongoDB running for this exercise.

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Review the five database models

**Do this:** Confirm the models you may choose from: Relational, Document, Key-value, Column-family, Graph. For each, name the primary structure (tables, JSON-like documents, key→value, column families, nodes and edges).

**Expected result:** The group can name all five models and one sentence for what each optimizes.

---

### Step 2 — Classify scenarios A–C

**Do this:** For A, B, and C, pick one initial model and write a one-line justification.

| Scenario | Key requirement |
|----------|-----------------|
| A. Online shopping sessions | Retrieve session data by a unique session ID |
| B. Product catalog | Store products with different attributes |
| C. Social-network recommendations | Traverse relationships between users |

**Expected result:** Your table has a model and a justification for A, B, and C. The justification mentions the access pattern (lookup by key, varied attributes, or relationship traversal).

---

### Step 3 — Classify scenarios D–F

**Do this:** Repeat for D, E, and F.

| Scenario | Key requirement |
|----------|-----------------|
| D. Banking ledger | Preserve strongly structured financial transactions |
| E. Sensor platform | Accept large volumes of distributed time-series writes |
| F. Content-management system | Store articles containing nested and optional sections |

**Expected result:** All six rows of the deliverable table are filled. You can explain why another technology might also work, and why your first choice still fits.

---

### Step 4 — Compare with the instructor solution

**Do this:** Share one controversial row with the class. Listen for the instructor solution, then adjust your justification if needed. The justification matters more than naming a product.

**Expected result:** You can defend or revise each choice using workload requirements: access pattern, consistency, relationships, and scale.

---

## Deliverable

| Scenario | Selected model | Justification |
|----------|----------------|---------------|
| A | | |
| B | | |
| C | | |
| D | | |
| E | | |
| F | | |

## Instructor solution (after discussion)

| Scenario | Recommended model |
|----------|-------------------|
| A | Key-value |
| B | Document |
| C | Graph |
| D | Relational |
| E | Column-family or a specialized time-series platform |
| F | Document |

**Debrief:** More than one technology may be technically possible. Start from access patterns, not popularity.

---

## Success criteria

- [ ] All six scenarios have a selected model
- [ ] Each justification names an access pattern, not only a product
- [ ] At least one row was discussed against an alternative model

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
