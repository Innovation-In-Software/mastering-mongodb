# Lab 5.5: Customer Order Summary

**Module 5:** The Aggregation Framework  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 5, Lesson 5.5)  
**Time:** 30 min  
**Difficulty:** Intermediate

**Objective:** Summarize paid spend per customer, join customer names, and return the top spenders.

---

## Environment basics (read this first)

**Demonstration environment:** Windows 10/11 · PowerShell in Cursor (``Ctrl+` ``) · `mongosh` connected to the training instance.

| Task | Windows | Where |
|------|---------|-------|
| Open folder | `Ctrl+K Ctrl+O` | File → Open Folder |
| Terminal | ``Ctrl+` `` → PowerShell | Bottom panel |
| MongoDB shell | `mongosh` | Same terminal |

Use the same connection string from Module 2. **Dataset:** `use training_store`.

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Group then lookup

**Do this:** Run:

```javascript
db.orders.aggregate([
  { $match: { paymentStatus: "PAID" } },
  {
    $group: {
      _id: "$customerId",
      orderCount: { $sum: 1 },
      totalSpending: { $sum: "$total" },
      averageOrderValue: { $avg: "$total" }
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
  {
    $project: {
      _id: 0,
      customerNumber: "$customer.customerNumber",
      customerName: {
        $concat: ["$customer.name.first", " ", "$customer.name.last"]
      },
      orderCount: 1,
      totalSpending: 1,
      averageOrderValue: 1
    }
  },
  { $sort: { totalSpending: -1 } }
])
```

**Expected result:** Aisha Khan (C101) is first. Maya Chen and Jordan Lee follow. C515 does not appear because O6402 is FAILED, not PAID.

---

### Step 2 — Confirm C101 spend

**Do this:** Sum C101 paid order totals from `find({ customerId: C101._id, paymentStatus: "PAID" })` (O6101, O6201, O6301, O6306).

**Expected result:** The hand total matches `totalSpending` for C101.

---

## Success criteria

- [ ] `$lookup` runs after `$group`
- [ ] Full name is concatenated
- [ ] Sort is by `totalSpending` descending

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
