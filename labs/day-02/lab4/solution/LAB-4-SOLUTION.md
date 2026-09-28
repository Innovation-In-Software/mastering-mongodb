# Lab 4 solution — Aggregation Pipeline

Instructor reference. **Do not hand this sheet to participants.** Participants work from [../LAB-4-GUIDE.md](../LAB-4-GUIDE.md) (deck slide 51).

Every result below was computed from a fresh `datasets/training_store/load.js`. mongosh prints money as `Decimal128('…')`; the tables show the plain numbers.

---

## Step 0 — Verify the dataset

| Check | Expected |
| --- | ---: |
| `db.products.countDocuments()` | 13 |
| `db.customers.countDocuments()` | 6 |
| `db.orders.countDocuments()` | 17 |
| `db.reviews.countDocuments()` | 6 |
| `db.orders.countDocuments({ paymentStatus: "PAID" })` | 13 |

The 13th product is the XBAD fixture (string price). It is never ordered, so it does not affect this lab. O6301 shows `paymentStatus: "PAID"`, `fulfillmentStatus: "SHIPPED"`, two items (L100 and A400) with `productId`, `quantity` and Decimal128 `unitPrice`, and `total: Decimal128("1512.23")`.

## Step 1 — Confirm the input set

**10** orders:

| Kept (PAID + SHIPPED/DELIVERED) | Excluded paid orders |
| --- | --- |
| O6101, O6102, O6103, O6201, O6203, O6204, O6301, O6303, O6304, O6306 | O6202 and O6302 (PROCESSING), O6305 (NEW) |

## Step 2 — Filter, unwind and compute line sales

The first two documents, in natural order (the exact two may vary):

```javascript
{ orderNumber: "O6101", …, items: { sku: "L100", name: "Business Laptop", quantity: 1,
  unitPrice: Decimal128("1299.99"), … }, lineSales: Decimal128("1299.99") }
{ orderNumber: "O6102", …, items: { sku: "S200", name: "Running Shoe", quantity: 1,
  unitPrice: Decimal128("129.99"), … }, lineSales: Decimal128("129.99") }
```

With `{ $count: "lines" }`: **{ lines: 18 }**.

| Order | Lines |
| --- | ---: |
| O6101, O6103, O6304 | 1 each |
| O6102, O6201, O6203, O6204, O6301, O6306 | 2 each |
| O6303 | 3 |
| **Total** | 3 + 12 + 3 = **18** |

## Step 3 — The report

Four documents (all four categories clear 50, so `$limit: 5` returns four):

| category | totalUnitsSold | totalSales | distinctCustomers | salesPerCustomer |
| --- | ---: | ---: | ---: | ---: |
| **LAPTOP** | 3 | 4499.97 | 2 | 2249.985 |
| ACCESSORY | 9 | 744.91 | 4 | 186.2275 |
| SHOE | 3 | 264.97 | 2 | 132.485 |
| BOOK | 5 | 259.95 | 3 | 86.65 |

Check: 4499.97 + 744.91 + 264.97 + 259.95 = 5769.80, the line sales of the 18 lines; 3 + 9 + 3 + 5 = 20 units.

Where the numbers come from:

- **LAPTOP:** L100 in O6101 and O6301 (1299.99 each), L110 in O6304 (1899.99). Customers C101 (Aisha Khan) and C620 (Maya Chen).
- **ACCESSORY:** P1001 ×3 lines (O6102, O6204, O6303), A400 ×2 in O6201 and ×1 in O6301, A410 ×1 in O6201, A500 in O6204 and O6306. Customers C101, C204, C412, C620.
- **SHOE:** S200 (O6102), S210 (O6203), S290 (O6306). Customers C204, C101.
- **BOOK:** B300 ×2 (O6103) and ×1 (O6303), B310 in O6203 and O6303. Customers C310, C204, C412.

All 18 lines find their product, so the plain `$unwind: "$product"` drops nothing. `salesPerCustomer` is an exact Decimal128 division; round it with `$round` in the `$project` if the report needs two decimals. The field order inside each output document may differ from the table.

## Step 4 — Prove one number

```javascript
{ _id: null, units: 3 }
```

Equal to LAPTOP's `totalUnitsSold` in Step 3: L100 ×1 (O6101), L100 ×1 (O6301), L110 ×1 (O6304). L190 is in the filter but was never sold.

## Step 5 — Optional plan check

The first stage is the `$match`, shown as the query of the initial cursor stage (or pushed down into the query plan on newer servers). With only the unique `orderNumber` index, the winning plan is a **COLLSCAN** with a filter on `paymentStatus` and `fulfillmentStatus`: 17 documents examined, 10 returned by the scan. The exact explain layout varies by server version; read the plan shape, not the milliseconds. The index Module 6 would add: `{ paymentStatus: 1, fulfillmentStatus: 1 }`.

---

## If the dataset was not reloaded after Lab 3

Lab 3 sets O6202 to SHIPPED. Step 1 then returns **11**, Step 2 **19** lines, and LAPTOP becomes 4 units, **6399.96**, 3 customers (C412 added), salesPerCustomer 2133.32. Step 4 then also returns 4, so the proof still agrees. Ask the learner to reload, or accept the numbers and say why they differ.

## Debrief questions

1. Why is `$match` before `$unwind`? *Filtering 17 orders to 10 before creating lines means 18 line documents instead of 26.*
2. Why is `$lookup` after `$unwind`? *The join key, `items.productId`, is one value per line only after unwinding.*
3. Why `$addToSet` and not `$sum: 1` for customers? *`$sum: 1` would count lines; `$addToSet` keeps each customer once.*
4. Why does the `$match` on 50 come after `$group`? *It filters categories on a computed total, which does not exist before grouping.*
5. Which number did you prove, and how? *LAPTOP units, with an independent pipeline.*

## Common mistakes seen in class

- `status: "Shipped"` or `"Paid"` → 0 documents. Fields are `paymentStatus` / `fulfillmentStatus`, values upper case.
- `$sum: "$items.lineTotal"` → 0; the field does not exist.
- `$sum: "$total"` after `$unwind` → order totals double-counted.
- `localField: "productId"` → no match after `$unwind`; the path is `items.productId`.
- `$group` on `"product.category"` without `$` → one group.
