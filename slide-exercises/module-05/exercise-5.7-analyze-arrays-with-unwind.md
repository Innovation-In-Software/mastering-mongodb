# Exercise 5.7: Analyze Arrays with $unwind

**Module 5:** The Aggregation Framework  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 5, Lesson 5.4)  
**Time:** 15 min  
**Difficulty:** Intermediate

**Objective:** Unwind paid order items and compute units, revenue, and order count per SKU.

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

### Step 1 — Unwind and compute line revenue

**Do this:** Run:

```javascript
db.orders.aggregate([
  { $match: { paymentStatus: "PAID" } },
  { $unwind: "$items" },
  {
    $set: {
      lineRevenue: { $multiply: ["$items.quantity", "$items.unitPrice"] }
    }
  },
  {
    $group: {
      _id: "$items.sku",
      unitsSold: { $sum: "$items.quantity" },
      revenue: { $sum: "$lineRevenue" },
      orderCount: { $sum: 1 }
    }
  },
  { $sort: { revenue: -1 } }
])
```

**Expected result:** L110 is first by revenue (`3799.98`). No order repeats a SKU, so `$sum: 1` is the number of orders containing that SKU.

---

### Step 2 — Name the highest-revenue SKU

**Do this:** Write the top `_id` and its `unitsSold`.

**Expected result:** L110, 2 units. L100 is second by revenue.

---

## Success criteria

- [ ] Only PAID orders are included
- [ ] Line revenue is calculated after `$unwind`
- [ ] You can explain why `$sum: 1` equals order count in this dataset

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
