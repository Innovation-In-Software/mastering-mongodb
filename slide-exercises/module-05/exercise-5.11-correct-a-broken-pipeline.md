# Exercise 5.11: Correct a Broken Pipeline

**Module 5:** The Aggregation Framework  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 5, Lesson 5.7)  
**Time:** 15 min  
**Difficulty:** Intermediate

**Objective:** Diagnose seven aggregation mistakes and rewrite the pipeline so the top product by revenue is correct.

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

## Broken pipeline

```javascript
db.orders.aggregate([
  { $limit: 3 },
  {
    $group: {
      _id: "items.sku",
      unitsSold: { $sum: "$quantity" },
      revenue: { $sum: "$total" }
    }
  },
  { $sort: { revenue: -1 } },
  {
    $lookup: {
      from: "customers",
      localField: "customerId",
      foreignField: "_id",
      as: "customer"
    }
  },
  { $project: { sku: "$customer.customerNumber" } }
])
```

Problems to find: `$limit` before `$sort`; missing `$` on the group key; quantity is under `items`; grouping before `$unwind`; `$lookup` result treated like an object; no paid-order filter; `total` is an order total, not line revenue.

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — List the defects

**Do this:** Write each defect and the symptom it causes (empty groups, wrong totals, dropped rows).

**Expected result:** At least five defects named, including stage order and nested field paths.

---

### Step 2 — Rewrite and run

**Do this:** A correct core is:

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
      revenue: { $sum: "$lineRevenue" }
    }
  },
  { $sort: { revenue: -1 } },
  { $limit: 5 }
])
```

**Expected result:** L110 is first. You did not need `$lookup` for a product-revenue report.

---

## Success criteria

- [ ] Defects include stage order and missing `$unwind`
- [ ] Rewritten pipeline groups on `$items.sku`
- [ ] Top SKU is L110

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
