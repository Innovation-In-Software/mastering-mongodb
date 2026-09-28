# Exercise 8.1 — Review a Query and Projection

**Module 8** (MongoDB Best Practices, Security, and Troubleshooting) · Day 3 · **Checkpoint A**  
**Time:** 15 min · **Type:** query review (hands-on optional) · **Difficulty:** Beginner

**Deck:** `decks/pptx_new/MongoDB_Module08_Best_Practices_Security_and_Troubleshooting.pptx` — slide 45, "Exercise 8.1 — Review a Query and Projection"

## Purpose

From `find({})` to a bounded, indexed query. You rewrite a query that returns every order document into one that is selective, shaped, ordered and bounded, and you name the compound index that should back it.

## Prerequisites

- Module 8, Part 2: "Ask Only for What the Page Needs", "Indexing Best Practices" and "Review Explain Plans"
- Optional: `mongosh` connected to `mongodb://localhost:27017` with a fresh `training_store` load. Reload if earlier labs changed the data:

  ```powershell
  mongosh "mongodb://localhost:27017" .\datasets\training_store\load.js
  ```

- This exercise only **reads** data. Don't create or drop indexes on the shared class instance unless the instructor says so.

## Scenario

The application needs **C101's paid orders, newest first, ten at a time**, showing only `orderNumber`, `fulfillmentStatus`, `total` and `createdAt`. Today it runs:

```javascript
db.orders.find({})
```

That returns all 17 orders, with every field, in no guaranteed order.

**Know the data before you write the filter.** In `training_store`, `orders.customerId` is an **ObjectId** that references `customers._id`. It is *not* the string `"C101"`. Look the customer up first:

```javascript
use training_store
const c101 = db.customers.findOne({ customerNumber: "C101" })._id
```

The payment state is stored in `paymentStatus` (`PAID`, `PENDING` or `FAILED`), and the order date is `createdAt`.

## Tasks

### Task 1 — Add a selective filter

Replace `{}` with a filter that returns only C101's paid orders.

### Task 2 — Project the four fields

Return `orderNumber`, `fulfillmentStatus`, `total` and `createdAt` only. Decide what to do with `_id`.

### Task 3 — Sort newest first and limit to ten

Make the order deterministic (newest first) and bound the result to ten documents.

### Task 4 — Name a compound index, labelled E or S

Write one compound index that supports both the filter and the sort. Label each key **E** (equality) or **S** (sort).

## Deliverable

```javascript
// Task 1–3: your rewritten query
db.orders.find(
  { /* filter */ },
  { /* projection */ }
)./* sort */./* limit */

// Task 4: your index, each key labelled E or S
db.orders.createIndex({ /* ... */ })
```

If you run the query, record:

| Question | Your answer |
| --- | --- |
| How many orders are returned? | |
| Order numbers, in the order returned | |
| Which C101 order is excluded, and why? | |

## Expected outcome

- The filter is selective — no `find({})`.
- The projection, sort and limit are all present.
- The index follows Equality–Sort–Range and does not lead with `createdAt`.

The instructor reveals the solution only after the debrief.

## Success criteria

- [ ] The filter uses the looked-up ObjectId for C101 and `paymentStatus: "PAID"`
- [ ] The projection returns only the four fields
- [ ] `.sort({ createdAt: -1 })` and `.limit(10)` are present
- [ ] The candidate index is written in ESR order with each key labelled
