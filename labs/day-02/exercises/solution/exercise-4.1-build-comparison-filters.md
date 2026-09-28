# Exercise 4.1 — solution (instructor)

**Module 4** · Day 2 · Checkpoint A  
**Type:** hands-on · **Do not hand this sheet to participants.**

Worksheet: [`../exercise-4.1-build-comparison-filters.md`](../exercise-4.1-build-comparison-filters.md) · Deck slide 46

## Running it

Fifteen minutes in `mongosh` on a fresh load of `datasets/training_store/load.js`. Every result below is from that fresh load. Reveal the slide's "Solution (after debrief)" column only after the class has shared answers.

## Task 1 — Price filters

### 1. price > 100 → five products

```javascript
db.products.find(
  { price: { $gt: Decimal128("100.00") } },
  { _id: 0, sku: 1, price: 1 }
)
```

```text
{ sku: 'L100', price: Decimal128('1299.99') }
{ sku: 'L110', price: Decimal128('1899.99') }
{ sku: 'L190', price: Decimal128('499.99') }
{ sku: 'S200', price: Decimal128('129.99') }
{ sku: 'A500', price: Decimal128('249.99') }
```

**L100, L110, L190, S200, A500.** People often stop at the laptops and `S200`; the Docking Station `A500` at 249.99 also matches. `L190` is inactive, but the filter does not ask about `active`.

### 2. 50 ≤ price ≤ 500 → five products

```javascript
db.products.find(
  { price: { $gte: Decimal128("50.00"), $lte: Decimal128("500.00") } },
  { _id: 0, sku: 1, price: 1 }
)
```

```text
{ sku: 'L190', price: Decimal128('499.99') }
{ sku: 'S200', price: Decimal128('129.99') }
{ sku: 'S210', price: Decimal128('89.99') }
{ sku: 'B300', price: Decimal128('59.99') }
{ sku: 'A500', price: Decimal128('249.99') }
```

**L190, S200, S210, B300, A500.** `A400` (24.99) is **below** the range and must not appear. `B310` (39.99), `S290` (44.99) and `P1001` (49.99) are below 50 too.

## Task 2 — Orders and reviews

### 3. total > 1000 → six orders

```text
{ orderNumber: 'O5001', total: Decimal128('1514.17') }
{ orderNumber: 'O6101', total: Decimal128('1483.99') }
{ orderNumber: 'O6202', total: Decimal128('2146.99') }
{ orderNumber: 'O6301', total: Decimal128('1512.23') }
{ orderNumber: 'O6304', total: Decimal128('2146.99') }
{ orderNumber: 'O6401', total: Decimal128('2945.98') }
```

**O5001, O6101, O6202, O6301, O6304, O6401** — every order with a laptop in it. The next-highest total, `O6204`, is only 350.98.

### 4. rating ≥ 4 → five of the six reviews

`L100` 5, `L110` 5, `S200` 4, `B300` 5, `A500` 4. The 3-star `P1001` review does not match. `db.reviews.countDocuments({ rating: { $gte: 4 } })` returns `5`.

## Task 3 — `$nin` → seven products

```text
{ sku: 'B300', category: 'BOOK' }
{ sku: 'B310', category: 'BOOK' }
{ sku: 'P1001', category: 'ACCESSORY' }
{ sku: 'A400', category: 'ACCESSORY' }
{ sku: 'A410', category: 'ACCESSORY' }
{ sku: 'A500', category: 'ACCESSORY' }
{ sku: 'XBAD', category: 'ACCESSORY' }
```

Two books and five accessories, **XBAD included** — the filter is on `category`, which XBAD stores normally. `$nin` (like `$ne`) also matches documents that have no `category` field at all; add `category: { $exists: true, $nin: [...] }` when the field must be present.

## Task 4 — Why XBAD is missing from 1–2

```text
{ sku: 'XBAD', price: '49.99' }
```

`XBAD`'s price is the **string** `"49.99"`. Comparison operators only match values of a comparable BSON type, so a Decimal128 range never compares a string and `XBAD` is skipped — even though `"49.99"` would be inside range 2 as a number.

## What you want to hear

- `Decimal128("100.00")`, not `100` and not `"100"`. A string such as `"100.00"` compares only with strings (on this dataset `{ price: { $gt: "100.00" } }` returns `XBAD` alone).
- A500 in answers 1 and 2; A400 **not** in answer 2.
- All six orders over 1000, not just O5001 and O6401.
- A one-sentence type explanation for XBAD.
