# Exercise 5.12: Optimize a Pipeline

**Module 5:** The Aggregation Framework  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 5, Lesson 5.7)  
**Time:** 15 min  
**Difficulty:** Intermediate

**Objective:** Rewrite an expensive pipeline so it stays equivalent but filters earlier and looks up later.

---

## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Work in pairs. Capture answers in a notes file or on paper.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional — a table is enough |
| Timer | Instructor clocks this | Stay on the slide timer |

MongoDB is optional. If you have `mongosh`, you may paste both versions after the discussion.

---

## Inefficient pipeline

```javascript
db.orders.aggregate([
  {
    $lookup: {
      from: "customers",
      localField: "customerId",
      foreignField: "_id",
      as: "customer"
    }
  },
  { $unwind: "$items" },
  { $match: { paymentStatus: "PAID", "customer.status": "ACTIVE" } },
  { $project: { items: 1, customer: 1, paymentStatus: 1, total: 1, shippingAddress: 1, internalNotes: 1 } },
  { $group: { _id: "$customer.customerNumber", spent: { $sum: "$total" } } }
])
```

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Name the costs

**Do this:** Identify early `$lookup`, `$unwind` before the paid filter, grouping by order `total` after unwind (which repeats the order total per item), and unused large fields.

**Expected result:** You can explain that joining every pending order is wasted work, and that unwinding then summing `total` double-counts multi-item orders.

---

### Step 2 — Write an equivalent cheaper pipeline

**Do this:** Match paid orders first, group by `customerId` on the order document (no unwind), then `$lookup`, then filter ACTIVE if still required.

```javascript
db.orders.aggregate([
  { $match: { paymentStatus: "PAID" } },
  {
    $group: {
      _id: "$customerId",
      spent: { $sum: "$total" }
    }
  },
  {
    $lookup: {
      from: "customers",
      localField: "_id",
      foreignField: "_id",
      as: "customer"
    }
  },
  { $unwind: "$customer" },
  { $match: { "customer.status": "ACTIVE" } },
  { $project: { _id: 0, customerNumber: "$customer.customerNumber", spent: 1 } }
])
```

A supporting index later: `{ paymentStatus: 1, customerId: 1 }`.

**Expected result:** Same business question: paid spend by active customer. No item unwind. Lookup runs on one row per customer.

---

## Success criteria

- [ ] Early `$match` is justified
- [ ] You did not unwind to sum order totals
- [ ] `$lookup` happens after grouping
- [ ] You named one supporting index for Module 6

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
