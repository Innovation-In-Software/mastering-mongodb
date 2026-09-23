# Exercise 5.1 — solution (instructor)

**Module 5** · Day 2 · Checkpoint A  
**Type:** design · **Do not hand this sheet to participants.**  
Worksheet: [../exercise-5.1-arrange-pipeline-stages.md](../exercise-5.1-arrange-pipeline-stages.md) · Deck slide 47

## Answer

`$match` → `$unwind` → `$set` → `$group` → `$sort` → `$limit`

| # | Stage | Documents afterwards (fresh `load.js`) |
|---|-------|-----------------------------------------|
| 1 | `$match: { paymentStatus: "PAID" }` | 13 paid orders, whole order documents |
| 2 | `$unwind: "$items"` | 21 line documents; `items` is now one object, not an array |
| 3 | `$set: { lineRevenue: { $multiply: ["$items.quantity", "$items.unitPrice"] } }` | Still 21; each line gains `lineRevenue` (Decimal128) |
| 4 | `$group: { _id: "$items.sku", revenue: { $sum: "$lineRevenue" } }` | 11 documents, one per SKU sold in a paid order |
| 5 | `$sort: { revenue: -1 }` | The same 11, highest revenue first |
| 6 | `$limit: 5` | The true top five |

The full pipeline, as shown on the slide "Product Sales from Order Lines":

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

If the class runs it, the result is:

| _id | unitsSold | revenue |
|-----|-----------|---------|
| L110 | 2 | 3799.98 |
| L100 | 2 | 2599.98 |
| A500 | 2 | 499.98 |
| S200 | 3 | 389.97 |
| B300 | 3 | 179.97 |

## Why this order

- **`$match` first:** fewer documents for every later stage (13, not 17), and only paid revenue is counted.
- **`$unwind` before grouping by SKU:** `items.sku` is inside an array. Without `$unwind`, `$group` would key on the whole array of SKUs per order.
- **`$set` before `$group`:** the line value must exist before it is summed. There is no stored `lineTotal`.
- **`$sort` before `$limit`:** `$limit` keeps the first N documents it receives. Unsorted, those are five arbitrary products, not the top five.

## Acceptable variation

`$set` can be folded into `$group` as `revenue: { $sum: { $multiply: ["$items.quantity", "$items.unitPrice"] } }`. That removes one stage and gives the same answer, which is a defensible trade-off.

## Follow-up question

A `$match` **after** `$group` filters the grouped SKU rows, not the orders; for example `{ $match: { revenue: { $gt: Decimal128("500") } } }` keeps SKUs with more than 500 of revenue (L110 and L100). That is a different, valid question. A `$match` on `paymentStatus` after `$group` returns nothing, because `$group` removed that field.

## What you want to hear

"Filter, expand, compute, group, rank, cut." If a pair puts `$limit` before `$sort`, ask what the five documents would be; if they put `$group` before `$unwind`, ask what `_id: "$items.sku"` holds while `items` is still an array.
