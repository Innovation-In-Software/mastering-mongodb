# Exercise 8.3: Review a Query and Projection

**Module 8:** MongoDB Best Practices, Security, and Troubleshooting  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 8)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Improve a query that returns complete order documents by adding a selective filter, projection, deterministic sort, limit, and a candidate index.

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

### Step 1 — Rewrite the query

**Do this:** The application only needs C101’s paid orders, newest first, ten at a time, showing orderNumber, fulfillmentStatus, total, and createdAt. Rewrite:

```javascript
db.orders.find({})
```

**Expected result:** Filter on customerId + paymentStatus PAID; projection of the four fields (and usually `_id: 0`); `.sort({ createdAt: -1 })`; `.limit(10)`.

---

### Step 2 — Name a candidate index

**Do this:** Write one compound index that supports the filter and sort. Label equality vs sort fields.

**Expected result:** `{ customerId: 1, paymentStatus: 1, createdAt: -1 }` — equality, equality, sort. Do not lead with createdAt.

---

## Success criteria

- [ ] The rewrite is selective (not find({}))
- [ ] Projection, sort, and limit are present
- [ ] The candidate index follows Equality–Sort–Range

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
