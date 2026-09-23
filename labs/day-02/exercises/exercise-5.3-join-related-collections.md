# Exercise 5.3 — Join Related Collections

**Module 5** (The Aggregation Framework) · Day 2 · **Checkpoint C**  
**Time:** 20 min · **Type:** hands-on in `mongosh`  
**Deck:** `decks/pptx_new/MongoDB_Module05_The_Aggregation_Framework.pptx`, slide 49

**Objective:** Add customer names to orders with `$lookup`, and keep the order that has no matching customer.

---

## Environment basics (read this first)

Windows 10/11 · PowerShell · `mongosh` connected with the Module 2 connection string.

```javascript
use training_store
```

Expected results assume a fresh `datasets/training_store/load.js` (17 orders, 6 customers).

Real field names: orders hold `customerId`, a reference to `customers._id`. Customers store `customerNumber`, `name.first` and `name.last` (not `firstName` / `lastName`) and `contact.email`.

---

## Scenario

List **every order** with its customer number and full name, **largest total first**.

```javascript
{ $lookup: { from: "customers",
    localField: "customerId",
    foreignField: "_id",
    as: "customer" } },
{ $unwind: { path: "$customer",
    preserveNullAndEmptyArrays:
      true } },
{ $project: … }, { $sort: … }
```

---

## Do this

1. **Join orders to customers** with the `$lookup` above. Run just that stage with `{ $limit: 1 }` and look at the `customer` field: what type is it?
2. **Unwind, keeping empty matches**: add the `$unwind` with `preserveNullAndEmptyArrays: true`.
3. **Project number and `$concat` name**: output `orderNumber`, `total`, `customerNumber` (from `$customer.customerNumber`) and `customerName` (a `$concat` of first name, a space and last name). Hide `_id`. Then sort by `total` descending.
4. **Find the order with no customer**: scan the output for a row without `customerNumber` and write down its `orderNumber`.

Extra question: remove `preserveNullAndEmptyArrays` and run again. How many rows now, and which one is gone?

---

## Expected result

One row per order, sorted by total. Most rows show a customer number and a full name. One order has no customer, and it still appears because of `preserveNullAndEmptyArrays`.

## Reference solution

After the debrief, compare with the [Exercise 5.3 solution](solution/exercise-5.3-join-related-collections.md) (instructor copy).

## Lab connection

Day 2 [Lab 4](../lab4/LAB-4-GUIDE.md) uses `$lookup` the same way, joining each order line to `products` for its category.

## Success criteria

- [ ] `$lookup` output is treated as an array
- [ ] The unmatched order is not dropped
- [ ] Names come from `name.first` and `name.last`
- [ ] Sort is on order total, not customer name
