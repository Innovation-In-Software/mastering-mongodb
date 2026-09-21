# Exercise 2.1: Select a Deployment Option

**Module 2:** Installation and Setup  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 2, Lesson 2.1)  
**Time:** 10 min  
**Difficulty:** Beginner

**Objective:** Choose an appropriate MongoDB deployment approach for different environments and name the main risk of each choice.

---

## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Work in pairs. Capture answers in a notes file or on paper.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional — a table is enough |
| Timer | 8 minutes work + 2 minutes debrief | Instructor clocks this |

You do **not** need MongoDB running for this exercise.

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Review the four deployment options

**Do this:** Confirm the options you may choose from: local installation, self-managed server or VM, containerized MongoDB, and managed cloud. For each, write one sentence for when it is a good fit.

**Expected result:** The pair can name all four options and one typical use for each.

---

### Step 2 — Classify scenarios 1–3

**Do this:** For each scenario, pick one deployment option, write a one-line justification, and name the main risk.

| Scenario | Situation |
|----------|-----------|
| 1 | A developer needs an offline learning environment. |
| 2 | A temporary automated-test environment must be created and removed quickly. |
| 3 | A distributed team needs access to a shared training database. |

**Expected result:** Rows 1–3 of the deliverable table are filled. The justification mentions internet, persistence, or shared access — not only a product name.

---

### Step 3 — Classify scenarios 4–6

**Do this:** Repeat for scenarios 4–6.

| Scenario | Situation |
|----------|-----------|
| 4 | A regulated organization requires infrastructure under its direct control. |
| 5 | A startup wants a database without managing servers. |
| 6 | A classroom has restricted internet access. |

**Expected result:** All six rows are filled. You can explain an alternative that might also work, and why your first choice still fits.

---

### Step 4 — Compare with the instructor solution

**Do this:** Share one controversial row with the class. Listen for the instructor solution, then adjust the risk column if needed.

**Expected result:** You can defend or revise each choice using training versus production, internet availability, operations load, and control requirements.

---

## Deliverable

| Scenario | Deployment option | Justification | Main risk |
|----------|-------------------|---------------|-----------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |

## Instructor solution (after discussion)

| Scenario | Recommended option |
|----------|--------------------|
| 1 Offline learner | Local installation |
| 2 Temporary testing | Container |
| 3 Distributed team | Managed cloud |
| 4 Direct infrastructure control | Self-managed server or VM |
| 5 Minimal operations | Managed cloud |
| 6 Restricted internet | Local installation or local server |

**Debrief:** The database commands are largely similar across options. Infrastructure responsibility is what changes.

---

## Success criteria

- [ ] All six scenarios have a selected option
- [ ] Each justification names a constraint (offline, disposable, shared, control, ops, network)
- [ ] Each row names a main risk
- [ ] At least one row was discussed against an alternative

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
