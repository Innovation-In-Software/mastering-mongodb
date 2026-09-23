# Lab 3 solution — Complex Queries and Updates

**Instructor reference. Do not hand this sheet to participants.**

Guide: [`../LAB-3-GUIDE.md`](../LAB-3-GUIDE.md) · Deck slide 50

Every result below is from a fresh load of `datasets/training_store/load.js`, running the steps in order. ObjectIds and `new Date()` values are shown as `…`. `find()` output without a sort comes back in insertion order on a fresh load; that order is not guaranteed in general.

---

## Before you start

`load.js` prints `customers: 6`, `products: 13`, `orders: 17`, `reviews: 6`, `paid orders: 13`. `db.products.countDocuments({})` returns `13`.

## Step 1 — Affordable, available accessories

```text
[
  { sku: 'A410', name: 'Wireless Mouse', price: Decimal128('19.99') },
  { sku: 'A400', name: 'USB Hub', price: Decimal128('24.99') },
  { sku: 'P1001', name: 'Wireless Keyboard', price: Decimal128('49.99') }
]
```

`A500` (249.99) fails the price rule; `XBAD` (string `"49.99"`) is skipped by the Decimal128 `$lt`.

## Step 2 — Priority products

```text
[
  { sku: 'L110', name: 'Ultrabook', tags: [ 'business', 'premium' ] },
  { sku: 'S290', name: 'Clearance Shoe', tags: [ 'clearance', 'sports' ] },
  { sku: 'A500', name: 'Docking Station', tags: [ 'office', 'premium' ] }
]
```

`L190` (clearance, `active: false`) is removed by the implicit AND. The `$in` version returns the same three.

## Step 3 — Price range, most expensive first

```text
[
  { sku: 'S210', name: 'Trail Shoe', category: 'SHOE', price: Decimal128('89.99') },
  { sku: 'B300', name: 'MongoDB Fundamentals', category: 'BOOK', price: Decimal128('59.99') },
  { sku: 'P1001', name: 'Wireless Keyboard', category: 'ACCESSORY', price: Decimal128('49.99') },
  { sku: 'S290', name: 'Clearance Shoe', category: 'SHOE', price: Decimal128('44.99') }
]
```

Out of range: `B310` 39.99 (below), `S200` 129.99 (above). `XBAD` is not in the range, so it does not top the sort.

## Step 4 — Exclude selected categories

Eight products:

```text
L100 LAPTOP · L110 LAPTOP · L190 LAPTOP · P1001 ACCESSORY · A400 ACCESSORY · A410 ACCESSORY · A500 ACCESSORY · XBAD ACCESSORY
```

`countDocuments` returns `8`.

## Step 5 — Customers in selected cities

```text
[
  { customerNumber: 'C101', name: { first: 'Aisha', last: 'Khan' },
    contact: { email: 'aisha@example.com' }, addresses: [ { city: 'Toronto' } ] },
  { customerNumber: 'C412', name: { first: 'Jordan', last: 'Lee' },
    contact: { email: 'jordan@example.com' }, addresses: [ { city: 'Montreal' } ] }
]
```

`C515` (Ottawa) is absent.

## Step 6 — High-quantity, inexpensive line items

Three orders:

| Order | The item that passes both conditions | total |
| --- | --- | --- |
| O5001 | A410 × 2 at 19.99 | 1514.17 |
| O6201 | A400 × 2 at 24.99 | 79.07 |
| O6305 | A410 × 3 at 19.99 | 71.77 |

Rejected: `O6302` (S200 × 2 at 129.99), `O6401` (L100 × 2 at 1299.99), `O6103` (B300 × 2 at 59.99). The older guide listed only O5001; O6201 and O6305 also match.

## Step 7 — Recent processing orders

```text
[
  { orderNumber: 'O6401', paymentStatus: 'PENDING', fulfillmentStatus: 'PROCESSING', createdAt: ISODate('2026-09-18T11:00:00.000Z') },
  { orderNumber: 'O6302', paymentStatus: 'PAID', fulfillmentStatus: 'PROCESSING', createdAt: ISODate('2026-09-07T12:00:00.000Z') },
  { orderNumber: 'O6202', paymentStatus: 'PAID', fulfillmentStatus: 'PROCESSING', createdAt: ISODate('2026-08-11T13:05:00.000Z') }
]
```

All three are `PROCESSING`; O6401's *payment* is still PENDING.

## Step 8 — Guarded inventory update

| Command | Result |
| --- | --- |
| `$set: { stockQuantity: 18 }` | `matchedCount: 1, modifiedCount: 1` |
| `findOne` with `stockQuantity: { $gte: 2 }` | `{ sku: 'A410', stockQuantity: 18 }` |
| Guarded `$inc: -2` | `matchedCount: 1, modifiedCount: 1` |
| Final `findOne` | `{ sku: 'A410', stockQuantity: 16, updatedAt: ISODate('…') }` |
| Rerun with `$gte: 100` | `matchedCount: 0, modifiedCount: 0` — stock stays 16 |

Without the `$set` first the guarded update matches 0: no product has a stock field on a fresh load.

## Step 9 — Unique tags

`matchedCount: 1, modifiedCount: 1`, then:

```text
{ sku: 'A410', tags: [ 'wireless', 'accessories', 'featured', 'office' ] }
```

`wireless` stays once.

## Step 10 — Remove discontinued tags

```text
{ acknowledged: true, insertedId: null, matchedCount: 13, modifiedCount: 1, upsertedCount: 0 }
```

All 13 products match the empty filter; only L190 had a tag to pull. `find({ tags: "discontinued" })` returns nothing, and:

```text
{ sku: 'L190', tags: [ 'clearance', 'refurbished' ] }
```

## Step 11 — Ship a processing order

First run: `matchedCount: 1, modifiedCount: 1`.

```text
{
  orderNumber: 'O6202',
  fulfillmentStatus: 'SHIPPED',
  statusHistory: [ { status: 'SHIPPED', changedAt: ISODate('…') } ]
}
```

Second run: `matchedCount: 0, modifiedCount: 0` — O6202 is no longer PROCESSING, so the guard stops a double ship and no second history entry is pushed.

## Step 12 — Rename a mistaken review field

| Command | Result |
| --- | --- |
| `insertOne` | `{ acknowledged: true, insertedId: ObjectId('…') }` — reviews now 7 |
| `find({ reviewText: { $exists: true } })` | one document: the A400 "Lab rename fixture" |
| `updateMany` with `$rename` | `matchedCount: 1, modifiedCount: 1` |
| Final `find` | `{ sku: 'A400', title: 'Lab rename fixture', body: 'Temporary field name for $rename practice.' }` — no `reviewText` |

The `body: { $exists: false }` guard makes sure no catalog review is touched.

## Step 13 — Challenge query

```text
[
  { sku: 'A410', name: 'Wireless Mouse', category: 'ACCESSORY', price: Decimal128('19.99'),
    tags: [ 'wireless', 'accessories', 'featured', 'office' ] },
  { sku: 'P1001', name: 'Wireless Keyboard', category: 'ACCESSORY', price: Decimal128('49.99'),
    tags: [ 'wireless', 'accessories' ] },
  { sku: 'B310', name: 'Query Cookbook', category: 'BOOK', price: Decimal128('39.99'),
    tags: [ 'database', 'reference' ] },
  { sku: 'B300', name: 'MongoDB Fundamentals', category: 'BOOK', price: Decimal128('59.99'),
    tags: [ 'database', 'technology' ] }
]
```

**A410, P1001, B310, B300.** Excluded: `A400` (no wireless or database tag), `A500` (249.99), `XBAD` (string price, `legacy` tag), all laptops and shoes (category).

## Debrief questions

- Who used `$in` and who used `$or` in step 2? Both are right; `$in` is shorter on one field.
- Why did step 10 match 13 but modify 1?
- What stopped step 11 from shipping twice — and what would have happened with `{ orderNumber: "O6202" }` alone?
- Reload before Module 5.
