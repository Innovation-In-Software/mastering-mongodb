# Exercise 5.4 — solution (instructor)

**Module 5** · Day 2 · Checkpoint D  
**Type:** debugging + hands-on · **Do not hand this sheet to participants.**  
Worksheet: [../exercise-5.4-correct-a-broken-pipeline.md](../exercise-5.4-correct-a-broken-pipeline.md) · Deck slide 50

## What the broken pipeline returns

It runs without error and returns **one meaningless document** (fresh load, natural order):

```javascript
{ _id: "items.sku", sku: [] }
```

- `$limit: 3` keeps the first three stored orders (typically O5001, O6101, O6102), one of them pending.
- `_id: "items.sku"` has no `$`, so it is the constant text `"items.sku"`: one group for everything.
- Inside that group `unitsSold` is 0 (there is no top-level `quantity`) and `revenue` is 3209.54, the three order totals added up; `$project` then drops both.
- The grouped document has no `customerId`, so `$lookup` finds nothing and `customer` is `[ ]`.
- `sku: "$customer.customerNumber"` on an empty array is `[ ]`.

## The seven defects

| # | Defect | Symptom |
|---|--------|---------|
| 1 | `$limit` first, before any sort | Three arbitrary orders; the report ignores the other 14 |
| 2 | No paid-order filter | Pending and failed orders would count as revenue |
| 3 | `"items.sku"` without `$` | A string constant: every order falls into one group |
| 4 | `"$quantity"` at the top level | The field is `items.quantity`; the sum is 0 |
| 5 | No `$unwind` before grouping by SKU | `items.sku` is an array per order; SKUs can't be grouped one by one |
| 6 | `revenue: { $sum: "$total" }` | `total` is the order total, not line revenue; after `$unwind` it would double-count |
| 7 | `$lookup` to customers, and its array output treated like an object | Not needed for product revenue; `customerNumber` from an array gives `[ ]` or `["C101"]`, never a SKU |

Five or more with the right symptoms is a pass. Stage order (1) and nested paths (3, 4, 5) must be among them.

## Corrected pipeline

```javascript
db.orders.aggregate([
  { $match: { paymentStatus: "PAID" } },
  { $unwind: "$items" },
  { $set: { lineRevenue: { $multiply: ["$items.quantity", "$items.unitPrice"] } } },
  { $group: {
      _id: "$items.sku",
      unitsSold: { $sum: "$items.quantity" },
      revenue: { $sum: "$lineRevenue" } } },
  { $sort: { revenue: -1 } },
  { $limit: 5 }
])
```

| _id | unitsSold | revenue |
|-----|----------:|--------:|
| **L110** | 2 | 3799.98 |
| L100 | 2 | 2599.98 |
| A500 | 2 | 499.98 |
| S200 | 3 | 389.97 |
| B300 | 3 | 179.97 |

**Top SKU: L110** (Ultrabook), 3799.98 from O6202 and O6304.

## The lesson

A product revenue report needs no customer join at all. Removing a stage is often the best fix. To add product names, `$lookup` to **products** after `$group`, or take `$first: "$items.name"` inside the `$group`.
