# Lab 5.8: Multi-Metric Report

**Module 5:** The Aggregation Framework  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 5, Lesson 5.5)  
**Time:** 30 min  
**Difficulty:** Intermediate

**Objective:** Use `$facet` on paid orders to return counts, revenue, status groups, top customers, top products, and high-value count.

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

### Step 1 — Paid input then facet

**Do this:** Run:

```javascript
db.orders.aggregate([
  { $match: { paymentStatus: "PAID" } },
  {
    $facet: {
      totals: [
        {
          $group: {
            _id: null,
            orderCount: { $sum: 1 },
            totalRevenue: { $sum: "$total" }
          }
        }
      ],
      byFulfillment: [
        {
          $group: {
            _id: "$fulfillmentStatus",
            orderCount: { $sum: 1 },
            revenue: { $sum: "$total" }
          }
        },
        { $sort: { revenue: -1 } }
      ],
      topCustomers: [
        { $group: { _id: "$customerId", spent: { $sum: "$total" } } },
        { $sort: { spent: -1 } },
        { $limit: 3 }
      ],
      topProducts: [
        { $unwind: "$items" },
        {
          $group: {
            _id: "$items.sku",
            revenue: {
              $sum: { $multiply: ["$items.quantity", "$items.unitPrice"] }
            }
          }
        },
        { $sort: { revenue: -1 } },
        { $limit: 3 }
      ],
      highValue: [
        { $match: { total: { $gte: Decimal128("1000.00") } } },
        { $count: "highValueOrders" }
      ]
    }
  }
])
```

**Expected result:** One document. `highValue` count is 4. `topProducts` starts with L110. `totals.orderCount` is 13.

---

### Step 2 — Describe the shape

**Do this:** Sketch the keys of the single output document and note that each value is an array.

**Expected result:** This is a structured result for an API or report, not a UI dashboard widget.

---

## Success criteria

- [ ] One output document
- [ ] High-value count is 4
- [ ] Top-product facet unwinds items; customer facet does not

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
