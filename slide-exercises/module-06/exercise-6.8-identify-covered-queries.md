# Exercise 6.8: Identify Covered Queries

**Module 6:** Indexing and Query Performance  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 6)  
**Time:** 15 min  
**Difficulty:** Intermediate

**Objective:** Given an index, decide which query and projection combinations can be covered.

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

### Step 1 — Index and three queries

**Do this:** Index `{ category: 1, price: 1, name: 1 }`. Decide coverage for: (Q1) filter category, project name and price with `_id: 0`; (Q2) same filter, project name, price, and tags; (Q3) filter category, project name only but leave `_id` on.

**Expected result:** Q1 may be covered. Q2 is not — tags are not in the index, so FETCH. Q3 is not covered unless `_id` is in the index — default `_id` forces a document fetch.

---

### Step 2 — State the confirmation rule

**Do this:** Write the three conditions for coverage and the explain signal you would look for.

**Expected result:** Filter fields indexed, returned fields indexed, `_id` excluded or indexed. Confirm with explain: IXSCAN without FETCH (projection-covered plan).

---



## Success criteria

- [ ] Q1 is the only likely covered query
- [ ] _id exclusion is mentioned
- [ ] explain() is required for confirmation

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
