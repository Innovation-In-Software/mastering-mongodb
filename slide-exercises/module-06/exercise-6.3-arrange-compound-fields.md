# Exercise 6.3: Arrange Compound-Index Fields

**Module 6:** Indexing and Query Performance  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 6)  
**Time:** 15 min  
**Difficulty:** Intermediate

**Objective:** Propose a compound-index field order for a paid high-value order query that also sorts by date.

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

### Step 1 — Label ESR roles

**Do this:** Given:

```javascript
db.orders
  .find({
    customerId: customerId,
    paymentStatus: "PAID",
    total: { $gte: Decimal128("500.00") }
  })
  .sort({ createdAt: -1 })
```
Label each field as equality, sort, or range.

**Expected result:** Equality: customerId, paymentStatus. Sort: createdAt. Range: total.

---

### Step 2 — Propose order and an alternative

**Do this:** Write a candidate key following Equality–Sort–Range. Then note when you might put the more selective equality field first if `paymentStatus` is a small set of values.

**Expected result:** Candidate `{ customerId: 1, paymentStatus: 1, createdAt: -1, total: 1 }`. Alternative: still lead with customerId (high selectivity) even if paymentStatus is low selectivity. Do not lead with total (range).

---



## Success criteria

- [ ] Equality, sort, and range are labeled correctly
- [ ] The range field is not first
- [ ] An alternative mentions selectivity without violating ESR blindly

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
