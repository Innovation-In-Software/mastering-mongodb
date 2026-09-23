# Exercise 6.7: Interpret Explain Output

**Module 6:** Indexing and Query Performance  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 6)  
**Time:** 20 min  
**Difficulty:** Intermediate

**Objective:** Read essential explain fields and decide whether a plan is a collection scan, a targeted index scan, or an expensive index scan.

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

### Step 1 — Label the sample plan

**Do this:** Using this training-style output, name the winning stage path, the index, and whether a FETCH occurred:

```text
winningPlan.stage: FETCH
winningPlan.inputStage.stage: IXSCAN
winningPlan.inputStage.indexName: idx_products_category
nReturned: 4
totalKeysExamined: 4
totalDocsExamined: 4
executionTimeMillis: (small on training data)
```

**Expected result:** IXSCAN on idx_products_category, then FETCH. Four keys, four docs, four returned — targeted for this dataset.

---

### Step 2 — Contrast a bad ratio

**Do this:** If another query showed COLLSCAN, totalDocsExamined 12, nReturned 1, write what you would try next. If it showed IXSCAN with keys examined 50,000 and nReturned 10, why is IXSCAN not enough?

**Expected result:** COLLSCAN: add an index on the filter/sort shape. High-key IXSCAN: the index is used but not selective (wrong order, low-selectivity leading field, or a wide range). Redesign the key; do not stop at “it used an index.”

---

You may instead run `db.products.find({ category: "ACCESSORY" }).explain("executionStats")` after Demo 6.1 and interpret the live plan.

## Success criteria

- [ ] COLLSCAN vs IXSCAN vs FETCH are identified
- [ ] nReturned, totalKeysExamined, and totalDocsExamined are interpreted together
- [ ] IXSCAN is not treated as automatically efficient

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
