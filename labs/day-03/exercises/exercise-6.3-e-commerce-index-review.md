# Exercise 6.3 — E-Commerce Index Review

**Module 6** (Indexing and Query Performance) · Day 3 · **Checkpoint C** (practical challenge)  
**Time:** 30–45 min · **Type:** design review · **Difficulty:** Intermediate

**Deck:** `decks/pptx_new/MongoDB_Module06_Indexing_and_Query_Performance.pptx` — slide 48, "Exercise 6.3 — E-Commerce Index Review"

## Purpose

Produce an index recommendation for ten recurring `training_store` workloads: the query shape, the index, its type, its cost, and how you would prove it and undo it.

## Prerequisites

- All of Module 6, especially "Choosing the Right Index Type", "Every Index Costs Writes", "Changing Indexes Safely in Production" and "An Indexing Strategy for training_store"
- A notes file or spreadsheet
- You may inspect `training_store` in `mongosh` (for example `db.products.findOne()` or `getIndexes()`), but you do not need to create indexes. The recommendation is the deliverable.

Remember what a fresh `load.js` already builds: `sku_unique` on products, `customerNumber_unique` and `email_unique` (on `contact.email`) on customers, and `orderNumber_unique` on orders. MongoDB rejects a second index on the same key under another name.

## Scenario

Recommend indexes for ten recurring `training_store` workloads.

| # | Workload |
| --- | --- |
| 1 | Product lookup by SKU |
| 2 | Product browsing by category, active status, and price |
| 3 | Product searches by tag |
| 4 | Customer lookup by email |
| 5 | Order lookup by order number |
| 6 | Customer order history sorted by date, newest first |
| 7 | Paid-order reporting by date |
| 8 | Product reviews, newest first |
| 9 | Session expiration |
| 10 | Product search over dynamic category attributes |

Real field names: `sku`, `category`, `active`, `price`, `tags` (array), `attributes` (differs by category), `contact.email`, `orderNumber`, `customerId`, `createdAt`, `paymentStatus`, `fulfillmentStatus`, `reviews.productId`, `sessions.expiresAt`.

## Tasks

### Task 1 — Tabulate shape and index for all ten

For each workload write the query shape (filter + sort) and a proposed index key.

### Task 2 — Mark unique, multikey, partial, TTL, wildcard

Mark each index with its type. Use specialized types where they fit — not everywhere. Say which indexes already exist after `load.js`.

### Task 3 — Give ESR roles and a cost note per compound

For every compound index, label equality, sort and range fields, and write one sentence about its write, storage or memory cost.

### Task 4 — Flag an overlap; plan validation and rollback

- Flag at least one overlapping prefix and say what you would do with it.
- For the two highest-traffic indexes (catalog browse and order history), write how you would prove each with `explain()` and how you would roll it back.

## Deliverable

| # | Query shape | Index key | Type | Name | Already exists? | ESR roles / cost note |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |
| 5 | | | | | | |
| 6 | | | | | | |
| 7 | | | | | | |
| 8 | | | | | | |
| 9 | | | | | | |
| 10 | | | | | | |

Overlap and plan:

Validation and rollback (catalog, order history):

## Expected outcome

- A ten-row table.
- Unique, multikey, TTL and wildcard marked where they belong (for example a unique SKU and a multikey tags index).
- TTL on sessions, never on orders; wildcard on `attributes`.
- One overlap called out (for example `category` versus `category + active + price`) with a hide-and-measure plan.
- A validation plan: baseline → create → explain → rollback.

The instructor reveals the solution only after the debrief.

## Success criteria

- [ ] Ten query shapes have proposed indexes
- [ ] Specialized types are used appropriately (not everywhere)
- [ ] Existing `load.js` unique indexes are reused, not duplicated
- [ ] Overlap and write cost are considered
- [ ] `explain()` validation and a rollback are part of the plan
