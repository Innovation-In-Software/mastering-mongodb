# Exercise 5.4 — Correct a Broken Pipeline

**Module 5** (The Aggregation Framework) · Day 2 · **Checkpoint D**  
**Time:** 15 min · **Type:** debugging, then hands-on in `mongosh`  
**Deck:** `decks/pptx_new/MongoDB_Module05_The_Aggregation_Framework.pptx`, slide 50

**Objective:** Find the defects in a pipeline that should report product revenue, then rewrite it and name the top SKU.

---

## Environment basics (read this first)

Windows 10/11 · PowerShell · `mongosh` connected with the Module 2 connection string.

```javascript
use training_store
```

Expected results assume a fresh `datasets/training_store/load.js`.

Real field names: orders have `paymentStatus` and an `items` array; each item has `sku`, `quantity` and `unitPrice`. `total` is the whole order's total. There is no `lineTotal`.

---

## Scenario

This pipeline should report **product revenue**: revenue and units sold per SKU from paid orders, highest revenue first.

```javascript
db.orders.aggregate([
  { $limit: 3 },
  { $group: {
      _id: "items.sku",
      unitsSold: { $sum: "$quantity" },
      revenue: { $sum: "$total" } } },
  { $sort: { revenue: -1 } },
  { $lookup: {
      from: "customers",
      localField: "customerId",
      foreignField: "_id",
      as: "customer" } },
  { $project: { sku: "$customer.customerNumber" } }
])
```

Run it once as it is. It returns no error. Write down what it returns.

---

## Do this

1. **List at least five defects.** Look at stage order, field paths (`$` or no `$`, top level or inside `items`), missing stages, the wrong measure, and stages that are not needed.
2. **Name the symptom each one causes** (one group, zeros, wrong totals, arbitrary rows, empty arrays).

   | # | Defect | Symptom |
   |---|--------|---------|
   | 1 | | |
   | 2 | | |
   | 3 | | |
   | 4 | | |
   | 5 | | |

3. **Rewrite it** in this order: `$match`, `$unwind`, `$set`, `$group`, `$sort`, `$limit` (top five).
4. **Run it and name the top SKU.**

---

## Expected result

At least five defects named, including stage order and nested field paths. Your rewritten pipeline returns five SKUs, highest revenue first, with no customer join.

## Reference solution

After the debrief, compare with the [Exercise 5.4 solution](solution/exercise-5.4-correct-a-broken-pipeline.md) (instructor copy).

## Lab connection

Day 2 [Lab 4](../lab4/LAB-4-GUIDE.md) is built stage by stage so that defects like these show up the moment they are added.

## Success criteria

- [ ] The defects include stage order and the missing `$unwind`
- [ ] The rewritten pipeline filters `paymentStatus: "PAID"` first
- [ ] It groups on `"$items.sku"` and sums `quantity × unitPrice`, not `total`
- [ ] You named the top SKU
