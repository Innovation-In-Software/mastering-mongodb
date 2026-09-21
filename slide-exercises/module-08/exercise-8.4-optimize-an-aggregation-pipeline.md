# Exercise 8.4: Optimize an Aggregation Pipeline

**Module 8:** MongoDB Best Practices, Security, and Troubleshooting  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 8)  
**Time:** 20 min  
**Difficulty:** Intermediate

**Objective:** Reorder and simplify a pipeline that looks up customers before filtering orders, unwinds every item, carries unused fields, groups incorrectly, and sorts too early.

---

## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Capture answers in a notes file.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional |
| Timer | Instructor clocks this | — |

You may use `mongosh` to inspect `training_store`, but reasoning is the deliverable unless a step says otherwise. Do not enable authentication on a shared training instance unless the instructor provides a disposable environment.


---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Name the defects

**Do this:** The pipeline runs `$lookup` customers, then `$unwind` items, then `$match` PAID, then `$sort` by date, then `$group` summing `total`. List what is wrong and why `$group` after `$unwind` can over-count revenue.

**Expected result:** Lookup and unwind happen before filtering; unused customer fields travel the pipeline; sort before the final metric is wasted work; summing parent `total` after unwind multiplies revenue by item count.

---

### Step 2 — Propose a safer order

**Do this:** Write a conceptual stage order that preserves paid-order monthly revenue and unique customers. State where `$unwind` is allowed.

**Expected result:** `$match` PAID (and date window if any) → `$project` needed fields → `$set` month → group for order-level metrics first, or unwind only to sum line quantities. `$lookup` only if the report needs names, after grouping. `$sort` last.

---

## Success criteria

- [ ] Early `$match` is required in the rewrite
- [ ] Double-counting of `total` after `$unwind` is named
- [ ] `$lookup` is delayed or justified

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
