# Exercise 5.3 — solution (instructor)

**Module 5** · Day 2 · Checkpoint C  
**Type:** hands-on · **Do not hand this sheet to participants.**  
Worksheet: [../exercise-5.3-join-related-collections.md](../exercise-5.3-join-related-collections.md) · Deck slide 49

## Pipeline

```javascript
db.orders.aggregate([
  { $lookup: {
      from: "customers",
      localField: "customerId",
      foreignField: "_id",
      as: "customer" } },
  { $unwind: { path: "$customer", preserveNullAndEmptyArrays: true } },
  { $project: {
      _id: 0,
      orderNumber: 1,
      total: 1,
      customerNumber: "$customer.customerNumber",
      customerName: { $concat: ["$customer.name.first", " ", "$customer.name.last"] } } },
  { $sort: { total: -1, orderNumber: 1 } }
])
```

The slide's sort is `{ total: -1 }`. O6202 and O6304 tie at 2146.99, so add `orderNumber: 1` if you want a repeatable order.

## Task 1 — what `$lookup` returns

`customer` is always an **array**: `[ { …Aisha Khan… } ]` for a match, `[ ]` for no match. It is a left outer join and never drops an order.

## Result (fresh load): 17 rows

| orderNumber | total | customerNumber | customerName |
|-------------|------:|----------------|--------------|
| O6401 | 2945.98 | C204 | Luis Romero |
| O6202 | 2146.99 | C412 | Jordan Lee |
| O6304 | 2146.99 | C620 | Maya Chen |
| O5001 | 1514.17 | C101 | Aisha Khan |
| O6301 | 1512.23 | C101 | Aisha Khan |
| O6101 | 1483.99 | C101 | Aisha Khan |
| O6204 | 350.98 | C620 | Maya Chen |
| O6306 | 343.33 | C101 | Aisha Khan |
| O6302 | 301.78 | C204 | Luis Romero |
| O6102 | 211.38 | C204 | Luis Romero |
| O6303 | 174.47 | C412 | Jordan Lee |
| O6203 | 154.88 | C204 | Luis Romero |
| O6103 | 140.58 | C310 | Priya Patel |
| O6201 | 79.07 | C101 | Aisha Khan |
| O6305 | 71.77 | C310 | Priya Patel |
| O6402 | 45.19 | C515 | Sam Okonkwo |
| O6499 | 28.24 | *(missing)* | `null` |

O6401, Luis Romero's **pending** 2945.98 order, is first: there is no `$match`, so every payment status is listed.

## Task 4 — the unmatched order

**O6499.** Its `customerId` is `ObjectId("000000000000000000000001")`, which matches no customer, so `customer` is `[ ]`.

- `preserveNullAndEmptyArrays: true` keeps it; after `$unwind` the `customer` field is simply absent.
- `customerNumber` is **missing** from its output row: `$project` omits a field whose path resolves to nothing.
- `customerName` is **`null`**: `$concat` returns null when any argument is missing.

## Extra question — without preserve

A plain `{ $unwind: "$customer" }` drops documents whose array is empty: **16 rows**, O6499 gone. Ask which behaviour a data-quality report needs (keep it, so the orphan is visible) versus a customer-facing report (dropping may be acceptable, but say so deliberately).

## Common wrong answers

- `$customer.firstName` / `$customer.lastName` → `customerName` null on every row. The fields are `name.first` and `name.last`.
- `$project` of `customerNumber: "$customer.customerNumber"` **without** `$unwind` → an array such as `["C101"]`, because `customer` is still an array.
- Sorting on `customerName` instead of `total`.

## What you want to hear

"`$lookup` always gives an array; decide deliberately what happens when it is empty."
