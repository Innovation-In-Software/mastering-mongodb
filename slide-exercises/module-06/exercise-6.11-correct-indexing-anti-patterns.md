# Exercise 6.11: Correct Indexing Anti-Patterns

**Module 6:** Indexing and Query Performance  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 6)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Rewrite seven unsafe or wasteful indexing habits as safer practices.

---

## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Capture answers in a notes file.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional |
| Timer | Instructor clocks this | — |

You may use `mongosh` to test ideas, but reasoning is the deliverable. You do not need to create production indexes during discussion exercises.


---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Correct the first four

**Do this:** Rewrite: index every field; one new index per query without checking overlap; put a range field first in every compound index; drop unused indexes immediately.

**Expected result:** Index recurring query shapes. Reuse prefixes. Equality (then sort) before range. Hide, measure, then drop.

---

### Step 2 — Correct the last three

**Do this:** Rewrite: treat every IXSCAN as optimal; ignore write overhead; design indexes only on development-sized data.

**Expected result:** Read examined keys/docs. Count secondary indexes on the write path. Validate with production-like volume and distribution.

---



## Success criteria

- [ ] Seven corrections are written
- [ ] ESR and hide-before-drop appear in the rewrite
- [ ] Small-data caution is explicit

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
