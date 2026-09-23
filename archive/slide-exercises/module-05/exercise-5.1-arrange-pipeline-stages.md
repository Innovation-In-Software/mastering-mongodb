# Exercise 5.1: Arrange Pipeline Stages

**Module 5:** The Aggregation Framework  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 5, Lesson 5.1)  
**Time:** 10 min  
**Difficulty:** Beginner

**Objective:** Put aggregation stages in the order required for a correct top-five-product report.


---

## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Work in pairs. Capture answers in a notes file or on paper.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional — a table is enough |
| Timer | Instructor clocks this | Stay on the slide timer |

You do **not** need MongoDB running for this exercise.

---

## Scenario

You need **top five products by line revenue** from paid orders. You may use each stage once:

`$limit` · `$unwind` · `$sort` · `$match` · `$group` · `$set`

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Propose an order

**Do this:** Write the six stages in the sequence you would run. Next to each stage, write one sentence on what the documents look like afterwards.

**Expected result:** A defensible sequence, not a guess. If two orders could work, note the trade-off.

---

### Step 2 — Check against the teaching pattern

**Do this:** Compare your list with the instructor’s reveal: `$match` → `$unwind` → `$set` → `$group` → `$sort` → `$limit`.

**Expected result:** You can explain why `$limit` cannot come before `$sort`, and why `$unwind` must come before grouping by SKU.

---

## Success criteria

- [ ] Stages are in an order that yields a true top-five by revenue
- [ ] You can say what `$match` after `$group` would mean instead


## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
