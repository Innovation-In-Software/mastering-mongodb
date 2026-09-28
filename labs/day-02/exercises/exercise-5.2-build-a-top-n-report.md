# Exercise 5.2 — Build a Top-N Report

**Module 5** (The Aggregation Framework) · Day 2 · **Checkpoint B**  
**Time:** 15 min · **Type:** hands-on in `mongosh`  
**Deck:** `decks/pptx_new/MongoDB_Module05_The_Aggregation_Framework.pptx`, slide 48

**Objective:** Build four top-N reports from `training_store`, each sorted before it is limited.

---

## Environment basics (read this first)

Windows 10/11 · PowerShell · `mongosh` connected with the Module 2 connection string.

```javascript
use training_store
```

The expected numbers assume a fresh load. If you ran Lab 3 or the Module 4 labs since the last load, reload from the repository root in PowerShell:

```powershell
mongosh "mongodb://localhost:27017" .\datasets\training_store\load.js
```

Real field names: `paymentStatus`, `customerId`, `total`, `orderNumber`, `items.sku`, `items.quantity`, `category`. Money (`total`) is Decimal128.

---

## Scenario

Build four top-N reports:

1. Top 5 customers by paid spend
2. Top 3 paid orders by total
3. Top 3 SKUs by units sold
4. Products per category: `{ $sortByCount: "$category" }`

---

## Do this

### Task 1 — Match PAID; group spend by `customerId`

Start from this skeleton and complete it:

```javascript
db.orders.aggregate([
  { $match: { paymentStatus: "PAID" } },
  { $group: { _id: "$customerId", totalSpent: { $sum: /* ? */ } } },
  { $sort: { /* ? */ } },
  { $limit: 5 }
])
```

### Task 2 — Sort `total` -1 with a tie-breaker

Return the three highest paid orders, showing only `orderNumber` and `total`. Two orders have the same total, so add a second sort key that makes the order repeatable.

### Task 3 — Unwind items; sum quantity by SKU

From paid orders, open the `items` array, sum `items.quantity` per `items.sku` as `unitsSold`, sort by `unitsSold` descending with `_id` as the tie-breaker, and keep three.

### Task 4 — Rank categories with `$sortByCount`

```javascript
db.products.aggregate([
  { $sortByCount: "$category" }
])
```

Note: there is no `$match`, so every product is counted, active or not.

---

## Expected result

Check your output against the slide after the debrief:

- Task 1: one customer is clearly first. Note the `_id` you get and find which customer it is.
- Task 2: the first two orders tie on total; your tie-breaker decides which is first.
- Task 3: one accessory leads on units.
- Task 4: four categories, largest count first.

## Reference solution

After the debrief, compare with the [Exercise 5.2 solution](solution/exercise-5.2-build-a-top-n-report.md) (instructor copy).

## Lab connection

Day 2 [Lab 4](../lab4/LAB-4-GUIDE.md) ends with the same `$sort` then `$limit` on its category report.

## Success criteria

- [ ] Every top-N pipeline sorts before it limits
- [ ] A tie-breaker field is used when values can tie
- [ ] Customer spend uses paid totals only, not pending orders
- [ ] Units are summed after `$unwind`, from `items.quantity`
