# Exercise 6.9: Find Redundant Indexes

**Module 6:** Indexing and Query Performance  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 6)  
**Time:** 15 min  
**Difficulty:** Intermediate

**Objective:** Spot overlapping prefixes without dropping an index on appearance alone.

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

### Step 1 — Mark overlap

**Do this:** Indexes: `{ category: 1 }`, `{ category: 1, price: 1 }`, `{ category: 1, price: 1, name: 1 }`, `{ price: 1 }`. Which pairs share a prefix? Which index is not a prefix of the others?

**Expected result:** The three category-leading indexes overlap; the two-field and three-field keys can serve category-only queries. `{ price: 1 }` is not a prefix of the category indexes.

---

### Step 2 — Decide what evidence is required

**Do this:** List four things to check before hiding `{ category: 1 }` in favor of a wider compound index.

**Expected result:** Query shapes and sort needs; covered-query projections; unique/partial/TTL options; `$indexStats` usage; index size vs write cost. Do not drop from visual similarity alone.

---



## Success criteria

- [ ] Prefix overlap is identified
- [ ] The price-only index is kept as a separate candidate
- [ ] A hide-then-measure approach is preferred over immediate drop

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
