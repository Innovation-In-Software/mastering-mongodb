# Exercise 6.4: Apply Equality–Sort–Range

**Module 6:** Indexing and Query Performance  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 6)  
**Time:** 15 min  
**Difficulty:** Intermediate

**Objective:** For three query shapes, label equality, sort, and range fields and propose a compound index.

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

### Step 1 — Catalog and history shapes

**Do this:** Shape A: active products in category ACCESSORY, price ≤ 100, sort by price. Shape B: one customerId, createdAt in a date range, sort createdAt descending. Label ESR and propose indexes.

**Expected result:** A: equality category+active, sort/range price → `{ category: 1, active: 1, price: 1 }`. B: equality customerId, sort createdAt, range createdAt (same field) → `{ customerId: 1, createdAt: -1 }`.

---

### Step 2 — Reporting shape

**Do this:** Shape C: paymentStatus PAID, createdAt ≥ start, sort createdAt descending. Propose an index and one sentence on why paymentStatus still belongs first even though it is low selectivity.

**Expected result:** `{ paymentStatus: 1, createdAt: -1 }`. Equality first partitions the index so the date sort/range walks one status’s keys instead of mixing statuses.

---



## Success criteria

- [ ] Three candidate indexes exist
- [ ] No design leads with a range field when an equality field is available
- [ ] Same-field sort and range (createdAt) is recognized as one indexed field

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
