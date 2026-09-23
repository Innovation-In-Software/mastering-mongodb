# Lab 5.3: Order Revenue Pipeline

**Module 5:** The Aggregation Framework  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 5, Lesson 5.3)  
**Time:** 25 min  
**Difficulty:** Beginner

**Objective:** Report paid-order count, revenue, and average order value by fulfillment status.

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

### Step 1 — Match paid orders and group

**Do this:** Run:

```javascript
db.orders.aggregate([
  { $match: { paymentStatus: "PAID" } },
  {
    $group: {
      _id: "$fulfillmentStatus",
      orderCount: { $sum: 1 },
      totalRevenue: { $sum: "$total" },
      averageOrderValue: { $avg: "$total" }
    }
  },
  { $sort: { totalRevenue: -1 } },
  {
    $project: {
      _id: 0,
      fulfillmentStatus: "$_id",
      orderCount: 1,
      totalRevenue: 1,
      averageOrderValue: 1
    }
  }
])
```

**Expected result:** SHIPPED is the highest-revenue paid status. NEW has one paid order (O6305). PENDING orders are absent.

---

### Step 2 — Spot-check one status

**Do this:** Manually count paid SHIPPED orders:

```javascript
db.orders.countDocuments({ paymentStatus: "PAID", fulfillmentStatus: "SHIPPED" })
```

Compare that number with `orderCount` from the pipeline.

**Expected result:** The grouped count matches the find count (6).

---

## Success criteria

- [ ] Only PAID orders are included
- [ ] Field names are `fulfillmentStatus`, `orderCount`, `totalRevenue`, `averageOrderValue`
- [ ] One status was validated with `countDocuments`

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
