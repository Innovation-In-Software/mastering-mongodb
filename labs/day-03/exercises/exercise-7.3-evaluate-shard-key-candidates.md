# Exercise 7.3 — Evaluate Shard-Key Candidates

**Module 7** (Introduction to Replication and Sharding) · Day 3 · **Checkpoint C**  
**Time:** 20 min · **Type:** design discussion · **Difficulty:** Intermediate

**Deck:** `decks/pptx_new/MongoDB_Module07_Introduction_to_Replication_and_Sharding.pptx` — slide 47, "Exercise 7.3 — Evaluate Shard-Key Candidates"

## Purpose

Score shard keys for `training_store.orders`. A shard key decides where each order lives and how each query is routed, and it is hard to change later. You score six candidates on seven criteria and recommend one.

## Prerequisites

- Module 7, Part 4: "Cardinality and Frequency", "Monotonic Shard Keys", "Ranged Sharding", "Hashed Sharding", "Zoned Sharding" and "Comparing Candidate Shard Keys for orders"
- Paper or a notes file. You may run the read-only queries below on `training_store`; nothing is sharded in this exercise.

## The mental model: `training_store.orders`

- 17 orders; each has `orderNumber` (such as `O6401`), `customerId` (an **ObjectId** reference to a customer — the readable code, such as `C101`, is the customer's `customerNumber`), `createdAt`, `paymentStatus`, `fulfillmentStatus`, `items`, `shippingAddress.country` and totals.
- **Few statuses:** `paymentStatus` has 3 values (`PAID`, `PENDING`, `FAILED`); 13 orders are `PAID`.
- **Many customers:** in production, many customers — each with a growing order history.
- **Dates only increase:** every new order has the largest `createdAt` so far.
- The hot query is Module 6's customer history: `find({ customerId: … }).sort({ createdAt: -1 })`.

Optional evidence (read-only):

```javascript
use training_store
db.orders.distinct("paymentStatus")
db.orders.aggregate([{ $group: { _id: "$paymentStatus", n: { $sum: 1 } } }])
```

## Scenario

Score each candidate **1–5** (5 = best) on **cardinality, distribution, write scale, targeting, hotspot risk (5 = low risk), locality and growth**.

```javascript
{ paymentStatus: 1 }
{ createdAt: 1 }
{ customerId: 1 }
{ customerId: "hashed" }
{ tenantId: 1, orderNumber: 1 }     // what-if: training_store has no tenantId
{ customerId: 1, createdAt: 1 }
```

`tenantId` is a **what-if** for multi-tenant platforms; `training_store` has no such field. Score it as if every order carried one.

## Tasks

### Task 1 — Score all six candidates

Fill in the scoring table below.

### Task 2 — Reject the low-cardinality key

Name the candidate that can never be split into many ranges, and say why.

### Task 3 — Flag the monotonic key

Name the candidate that sends every new order to the same range, and say which shard gets hot.

### Task 4 — Recommend one; name two risks

Pick one key for customer-order lookup plus high write volume. List two risks you would still monitor.

## Deliverable

| Candidate | Cardinality | Distribution | Write scale | Targeting | Hotspot risk | Locality | Growth |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `{ paymentStatus: 1 }` | | | | | | | |
| `{ createdAt: 1 }` | | | | | | | |
| `{ customerId: 1 }` | | | | | | | |
| `{ customerId: "hashed" }` | | | | | | | |
| `{ tenantId: 1, orderNumber: 1 }` (what-if) | | | | | | | |
| `{ customerId: 1, createdAt: 1 }` | | | | | | | |

Recommendation: ______________________  Risk 1: ______________  Risk 2: ______________

## Expected outcome

- The low-cardinality status key is rejected as a standalone key.
- Ranged `createdAt` is flagged as a write hotspot.
- The recommendation matches the hot query and still names a remaining risk.

The instructor reveals the solution only after groups share their answers.

## Success criteria

- [ ] All six candidates are scored on all seven criteria
- [ ] `paymentStatus` is rejected as a standalone key
- [ ] Monotonic ranged `createdAt` is flagged for hotspots
- [ ] The recommendation names two risks to monitor
- [ ] `tenantId` is treated as a what-if, not as a real `training_store` field
