# Exercise 8.8: Define RPO and RTO

**Module 8:** MongoDB Best Practices, Security, and Troubleshooting  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 8)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Propose recovery point and recovery time objectives, backup frequency, recovery method, and validation for catalog, customers, orders, payments, and reviews.

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

### Step 1 — Assign objectives

**Do this:** For product catalog, customer profiles, orders, payments, and reviews, write RPO, RTO, and a backup frequency that could meet the RPO. Use the store as a small retailer, not a global bank.

**Expected result:** Payments and orders typically get the tightest RPO (minutes) and tested point-in-time recovery. Catalog can often tolerate a longer RPO. Reviews are usually the most tolerant. RTO for checkout should be shorter than for reviews.

---

### Step 2 — Name validation

**Do this:** For orders, write how you would prove a restore: counts, sample order numbers, indexes, and a checkout read.

**Expected result:** Compare `countDocuments` to the pre-restore note; find O5001 and a paid total; `getIndexes()`; application can read an order. Backup success alone is not enough.

---

## Success criteria

- [ ] RPO and RTO are defined as time quantities
- [ ] Orders/payments are stricter than reviews
- [ ] Restore validation includes data and access, not only the backup job

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
