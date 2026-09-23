# Exercise 5.2 — solution (instructor)

**Module 5** · Day 2 · Checkpoint B  
**Type:** hands-on · **Do not hand this sheet to participants.**  
Worksheet: [../exercise-5.2-build-a-top-n-report.md](../exercise-5.2-build-a-top-n-report.md) · Deck slide 48

All results are for a fresh `datasets/training_store/load.js`. mongosh prints money as `Decimal128('…')`; the tables show the plain numbers.

## Task 1 — Top 5 customers by paid spend

```javascript
db.orders.aggregate([
  { $match: { paymentStatus: "PAID" } },
  { $group: { _id: "$customerId", totalSpent: { $sum: "$total" } } },
  { $sort: { totalSpent: -1 } },
  { $limit: 5 }
])
```

`_id` is the customer's ObjectId. Translated to customer numbers:

| Customer | Name | totalSpent | Paid orders |
|----------|------|-----------:|------------:|
| C101 | Aisha Khan | 3418.62 | 4 (O6101, O6201, O6301, O6306) |
| C620 | Maya Chen | 2497.97 | 2 |
| C412 | Jordan Lee | 2321.46 | 2 |
| C204 | Luis Romero | 668.04 | 3 |
| C310 | Priya Patel | 212.35 | 2 |

C515 (Sam Okonkwo) is absent: his only order, O6402, failed payment. Only five customers have paid orders, so `$limit: 5` returns all of them. To show `customerNumber` instead of the ObjectId, add a `$lookup` to customers after `$group`, which is Exercise 5.3's technique.

## Task 2 — Top 3 paid orders by total

```javascript
db.orders.aggregate([
  { $match: { paymentStatus: "PAID" } },
  { $sort: { total: -1, orderNumber: 1 } },
  { $limit: 3 },
  { $project: { _id: 0, orderNumber: 1, total: 1 } }
])
```

| orderNumber | total |
|-------------|------:|
| O6202 | 2146.99 |
| O6304 | 2146.99 |
| O6301 | 1512.23 |

O6202 and O6304 tie; `orderNumber: 1` puts O6202 first every time. O6401 (2945.98) is larger but is PENDING, so the `$match` removes it.

## Task 3 — Top 3 SKUs by units sold

```javascript
db.orders.aggregate([
  { $match: { paymentStatus: "PAID" } },
  { $unwind: "$items" },
  { $group: { _id: "$items.sku", unitsSold: { $sum: "$items.quantity" } } },
  { $sort: { unitsSold: -1, _id: 1 } },
  { $limit: 3 }
])
```

| _id | unitsSold |
|-----|----------:|
| A410 | 4 |
| A400 | 3 |
| B300 | 3 |

Four SKUs tie on 3 units (A400, B300, P1001, S200). The `_id: 1` tie-breaker keeps A400 and B300; P1001 and S200 also sold 3 but fall outside the top three. A410 (Wireless Mouse) leads with 1 unit in O6201 and 3 in O6305.

## Task 4 — Products per category

```javascript
db.products.aggregate([
  { $sortByCount: "$category" }
])
```

| _id | count |
|-----|------:|
| ACCESSORY | 5 |
| LAPTOP | 3 |
| SHOE | 3 |
| BOOK | 2 |

LAPTOP and SHOE tie at 3, so they can print in either order. `$sortByCount` has no tie-breaker; for a fixed order use `$group` + `$sort: { count: -1, _id: 1 }`.

**Dataset note:** the old worksheet listed ACCESSORY 4. A fresh load has ACCESSORY 5, because the XBAD fixture (Legacy Cable Pack) is an active accessory. The inactive L190 is counted too, since there is no `$match`.

## What you want to hear

"Sort, then limit, and add a tie-breaker whenever values can tie." Ask one pair to run Task 2 without `orderNumber: 1` several times and discuss why a report must not depend on luck.
