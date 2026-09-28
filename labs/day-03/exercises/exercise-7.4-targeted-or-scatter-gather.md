# Exercise 7.4 — Targeted or Scatter-Gather?

**Module 7** (Introduction to Replication and Sharding) · Day 3 · **Checkpoint D**  
**Time:** 15 min · **Type:** design discussion · **Difficulty:** Intermediate

**Deck:** `decks/pptx_new/MongoDB_Module07_Introduction_to_Replication_and_Sharding.pptx` — slide 48, "Exercise 7.4 — Targeted or Scatter-Gather?"

## Purpose

Classify five queries by their routing. On a sharded cluster, `mongos` sends a query that includes the shard key (or its prefix) to one or a few shards; a query without it goes to every shard and `mongos` merges the results.

## Prerequisites

- Module 7, Part 5: "Chunks and Data Distribution", "Targeted Queries" and "Targeted or Scatter-Gather on training_store?"
- Exercise 7.3 (the shard-key candidates)
- Paper or a notes file. You may run the queries on your `training_store` replica set to see the results, but a replica set holds all the data in one place, so it cannot show routing.

## Scenario

Assume `training_store.orders` is sharded on the ranged key **`{ customerId: 1, createdAt: 1 }`**. `c` is customer **C101** (Aisha Khan):

```javascript
use training_store
const c = db.customers.findOne({ customerNumber: "C101" })
const start = ISODate("2026-09-01T00:00:00Z")
```

`c._id` is the ObjectId stored in `orders.customerId`; `C101` itself is the readable `customerNumber`, not what orders store.

```javascript
// A
db.orders.find({ customerId: c._id })
// B
db.orders.find({ customerId: c._id, createdAt: { $gte: start } })
// C
db.orders.find({ paymentStatus: "PAID" })
// D
db.orders.find({ createdAt: { $gte: start } })
// E — query D again, but the shard key is { customerId: "hashed" }
```

Classify each as **single-shard targeted**, **multi-shard targeted**, **scatter-gather** or **insufficient information**.

## Tasks

### Task 1 — Classify queries A and B

Say which part of the shard key each filter uses.

### Task 2 — Classify queries C and D

Say whether the filter contains the leading shard-key field.

### Task 3 — Classify E under the hashed key

The key is now `{ customerId: "hashed" }` and the filter is a `createdAt` range.

### Task 4 — Fix a slow monthly revenue report

A monthly global revenue report (all customers, one month) must stay fast. Is a different shard key the fix, or a different reporting design? Name one option.

## Deliverable

| Query | Filter uses | Routing | One-line reason |
| --- | --- | --- | --- |
| A | | | |
| B | | | |
| C | | | |
| D | | | |
| E | | | |

Task 4 answer:

## Expected outcome

- Filters with the shard-key prefix can be targeted.
- Filters without the leading shard-key field are scatter-gather or touch many shards.
- The global report is not assumed to be single-shard, and the fix does not hurt the order path.

The instructor reveals the solution only after groups share their answers.

## Success criteria

- [ ] Non-shard-key filters are classified as scatter-gather
- [ ] Prefix equality on `customerId` is classified as targeted
- [ ] A range on a field that is not the key's prefix is not called targeted
- [ ] Global reports are not assumed to be single-shard
