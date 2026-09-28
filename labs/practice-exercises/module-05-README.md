# Module 5 — Practice exercise solutions

**Deck:** `decks/pptx_new/MongoDB_Module05_The_Aggregation_Framework.pptx`  
**Dataset:** `training_store`, fresh load of [`datasets/training_store/load.js`](../../datasets/training_store/load.js) (13 products, 6 customers, 17 orders with 13 PAID, 6 reviews)  
Attempt the slide activity first, then compare your answers here.

Official numbered checkpoints for this module: [Exercise 5.1](../day-02/exercises/exercise-5.1-arrange-pipeline-stages.md), [Exercise 5.2](../day-02/exercises/exercise-5.2-build-a-top-n-report.md), [Exercise 5.3](../day-02/exercises/exercise-5.3-join-related-collections.md), [Exercise 5.4](../day-02/exercises/exercise-5.4-correct-a-broken-pipeline.md). Day lab: [Lab 4 — Aggregation Pipeline](../day-02/lab4/LAB-4-GUIDE.md).

mongosh prints money as `Decimal128('…')`; the answers show the plain numbers.

---

## Exercise: Build a Shoe Price List

**Slide 19** (Part 2) · **Time:** 10 minutes · **How to run:** pairs, five minutes to write it, then run it on the instructor screen.

### Scenario

Marketing wants the two most expensive active shoes: name and price only, highest price first. `training_store` has three shoes: S200, S210 and S290.

### Tasks

1. Choose the four stages and their order
2. Write the `$match`
3. Write the `$project`
4. Add `$sort` and `$limit`; predict the output

### Solution

| Task | Answer |
| --- | --- |
| 1. Stages | `$match` → `$project` → `$sort` → `$limit` |
| 2. `$match` | `{ active: true, category: "SHOE" }` |
| 3. `$project` | `{ _id: 0, name: 1, price: 1 }` |
| 4. Output | Running Shoe 129.99, then Trail Shoe 89.99 |

```javascript
db.products.aggregate([
  { $match: { active: true, category: "SHOE" } },
  { $project: { _id: 0, name: 1, price: 1 } },
  { $sort: { price: -1 } },
  { $limit: 2 }
])
```

```javascript
{ name: "Running Shoe", price: Decimal128("129.99") }
{ name: "Trail Shoe", price: Decimal128("89.99") }
```

All three shoes are active. The Clearance Shoe (S290) at 44.99 is third, so `$limit` drops it.

### A variation to discuss

Put `$project` before `$match`. The projection removes `category` and `active`, so the `$match` then finds nothing: 0 documents. That is Part 1's lesson again: stage order is part of the question. (`$sort` can come before `$project` too; since it only needs `price`, both orders give the same answer.)

---

## Exercise: Orders by Payment Status

**Slide 26** (Part 3) · **Time:** 10 minutes · **How to run:** individually for five minutes, then compare.

### Scenario

Finance asks how many orders, and how much money, sit in each payment status. Use all 17 orders, not only the paid ones.

### Tasks

1. Group by `paymentStatus`
2. Count with `$sum: 1`; add `total` with `$sum`
3. Sort by revenue, highest first
4. Rename `_id` to `paymentStatus` in `$project`

### Solution

No `$match` this time: the question is about every order.

```javascript
db.orders.aggregate([
  { $group: {
      _id: "$paymentStatus",
      orders: { $sum: 1 },
      revenue: { $sum: "$total" } } },
  { $sort: { revenue: -1 } },
  { $project: { _id: 0, paymentStatus: "$_id", orders: 1, revenue: 1 } }
])
```

| paymentStatus | orders | revenue | Which orders |
| --- | ---: | ---: | --- |
| PAID | 13 | 9118.44 | O6101 … O6306 |
| PENDING | 3 | 4488.39 | O5001 (1514.17), O6401 (2945.98), O6499 (28.24) |
| FAILED | 1 | 45.19 | O6402 |

### The habit

13 + 3 + 1 = 17 orders, the collection size. Adding a grouped report's counts back to the input count catches most mistakes in a `$group`.

---

## Exercise: How Big Does the Stream Get?

**Slide 33** (Part 4) · **Time:** 5 minutes · **How to run:** two minutes to write predictions, then run it on the instructor screen.

### Scenario

Before building the product report, predict how many documents each stage passes on:

```javascript
db.orders.aggregate([
  { $match: { paymentStatus: "PAID" } },
  { $unwind: "$items" },
  { $count: "lines" }
])
```

### Tasks

1. Predict the count after `$match`
2. Predict the count after `$unwind`
3. Name the paid order with the most lines
4. What if `$unwind` came before `$match`?

### Solution

| Task | Answer |
| --- | --- |
| 1. After `$match` | 13 paid orders |
| 2. After `$unwind` | `{ lines: 21 }` |
| 3. Most lines | O6303, three items (MongoDB Fundamentals, Query Cookbook, Wireless Keyboard) |
| 4. Unwind first | 26 lines, filtered back to 21: the same answer for more work |

How the 21 add up: of the 13 paid orders, six have one item (O6101, O6103, O6202, O6302, O6304, O6305), six have two (O6102, O6201, O6203, O6204, O6301, O6306) and O6303 has three: 6 + 12 + 3 = 21.

All 17 orders hold 26 lines (the four unpaid orders add O5001's two lines and one line each for O6401, O6402 and O6499). Unwinding first creates all 26 documents and then throws 5 away.

### Why it matters

On a real store with millions of orders, that difference is the difference between a fast and a slow report. Filter before you unwind.
