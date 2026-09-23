# Exercise 4.1 — Build Comparison Filters

**Module 4** (The MongoDB Query Language) · Day 2 · **Checkpoint A**  
**Time:** 15 min · **Type:** hands-on in `mongosh` · **Difficulty:** Beginner

**Deck:** `decks/pptx_new/MongoDB_Module04_The_MongoDB_Query_Language.pptx` — slide 46, "Exercise 4.1 — Build Comparison Filters"

## Purpose

Write `$gt`, `$gte`, `$lte`, range and `$nin` filters, comparing money as Decimal128 — and check every result against the data.

## Prerequisites

- Module 4, Part 2 ("Comparison Operators" and "Comparisons, $in and $nin on training_store")
- `mongosh` connected to the class instance
- A fresh load of `training_store`. From the repository root, in PowerShell (not inside `mongosh`):

```powershell
mongosh "mongodb://localhost:27017" .\datasets\training_store\load.js
```

The script prints `customers: 6`, `products: 13`, `orders: 17`, `reviews: 6` and `paid orders: 13`. Then:

```javascript
use training_store
```

## Scenario

Money in `training_store` is Decimal128 — except `XBAD`, planted with a string price. Write one filter for each request:

```text
1  products: price > 100
2  products: 50 ≤ price ≤ 500
3  orders:   total > 1000
4  reviews:  rating ≥ 4
5  products: not LAPTOP or SHOE
```

## Tasks

### Task 1 — Write 1 and 2 with Decimal128 values

Products priced above 100:

```javascript
db.products.find(
  { price: { $gt: Decimal128("100.00") } },
  { _id: 0, sku: 1, price: 1 }
)
```

Products priced from 50 to 500 (both ends included):

```javascript
db.products.find(
  { price: { $gte: Decimal128("50.00"), $lte: Decimal128("500.00") } },
  { _id: 0, sku: 1, price: 1 }
)
```

Write down every SKU that comes back. `NumberDecimal("100.00")` is the same as `Decimal128("100.00")`.

### Task 2 — Write 3 and 4 on orders and reviews

```javascript
db.orders.find(
  { total: { $gt: Decimal128("1000.00") } },
  { _id: 0, orderNumber: 1, total: 1 }
)

db.reviews.find(
  { rating: { $gte: 4 } },
  { _id: 0, sku: 1, rating: 1 }
)
```

`rating` is a plain number, so `4` needs no Decimal128. Record every order number and how many reviews match.

### Task 3 — Write 5 with `$nin`

```javascript
db.products.find(
  { category: { $nin: ["LAPTOP", "SHOE"] } },
  { _id: 0, sku: 1, category: 1 }
)
```

Use one `$nin` on one field, not two `$ne` clauses.

### Task 4 — Explain why XBAD never appears in 1–2

Run this and look at the type of the price:

```javascript
db.products.findOne({ sku: "XBAD" }, { _id: 0, sku: 1, price: 1 })
```

Write one sentence: why does a Decimal128 range never return `XBAD`, although it does appear in task 3?

## Deliverable

| Filter | Your result |
| --- | --- |
| 1. price > 100 | |
| 2. 50 ≤ price ≤ 500 | |
| 3. total > 1000 | |
| 4. rating ≥ 4 | |
| 5. not LAPTOP or SHOE | |
| Why XBAD is missing from 1–2 | |

## Expected outcome

The solution is revealed on the slide after the debrief. Your filters are right when every money comparison uses Decimal128, each result can be checked against the stored prices and totals, and you can explain `XBAD` in one sentence.

## Success criteria

- [ ] Used Decimal128 for every money comparison (not `100` or `"100"`)
- [ ] Listed every matching SKU or order number, not just the obvious ones
- [ ] Used `$nin` on one field
- [ ] Explained why `XBAD` misses numeric price ranges

## Next

[Exercise 4.2 — Query Arrays of Documents](exercise-4.2-query-arrays-of-documents.md)
