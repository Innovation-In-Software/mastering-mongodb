# Exercise 7.4 — solution (instructor)

**Module 7** · Day 3 · Checkpoint D  
**Type:** design discussion · **Do not hand this sheet to participants.**

Worksheet: [`../exercise-7.4-targeted-or-scatter-gather.md`](../exercise-7.4-targeted-or-scatter-gather.md) · Deck slide 48

## Running it

Fifteen minutes: about eight in pairs, then debrief A to E. As on the slide, `c` holds C101's customer document, so `c._id` is the ObjectId stored in `orders.customerId`. On the class replica set every query finds its data in one place; routing only shows on a sharded cluster, and any `explain()` comparison there is an **instructor-only demonstration on a disposable cluster**.

## Tasks 1–3 — Solution

Shard key `{ customerId: 1, createdAt: 1 }` (ranged) for A–D; `{ customerId: "hashed" }` for E.

| Query | Filter uses | Routing | Why | Fresh-load result on the replica set |
| --- | --- | --- | --- | --- |
| A `{ customerId: c._id }` | Key prefix (equality) | **Targeted** — one shard, or a few if C101's range was split | `mongos` routes to the ranges that hold that customer | 5 orders (O5001, O6101, O6201, O6301, O6306) |
| B `{ customerId: c._id, createdAt: { $gte: start } }` | Full key: prefix equality + range on the second field | **Targeted** — a range inside the customer prefix | Narrower than A: only the part of C101's range from `start` | 3 orders (O6301, O6306, O5001) |
| C `{ paymentStatus: "PAID" }` | No key field | **Scatter-gather** | `paymentStatus` is not in the key; every shard must search | 13 orders |
| D `{ createdAt: { $gte: start } }` | Second key field only, not the prefix | **Many shards or all** (multi-shard / scatter-gather) | Without `customerId`, the dates are spread through every customer's ranges | 10 orders |
| E D again, key hashed `customerId` | No key field | **Scatter-gather** | Hashed `customerId` has no `createdAt` at all; every shard searches | 10 orders |

`start` is `ISODate("2026-09-01T00:00:00Z")`. Slide summary: A, B targeted: key prefix · C scatter-gather · D many shards or all · E scatter-gather · Pre-aggregate, don't re-key.

"Insufficient information" is not the expected answer for any row here, but accept it for D if the group explains that the answer depends on how dates map onto the chunk ranges.

## Task 4 — The redesign

**A different reporting design, not a new shard key.** Don't pick a key that hurts the order path (customer history) to speed up a monthly job. Options:

- Pre-aggregate revenue per day or month (for example with `$merge` into a summary collection) and read the summary.
- Run the report on an analytics node or a separate analytics cluster.
- Accept scatter-gather for a rare job — a monthly report may scatter and that's fine.

## What to listen for

- "D is targeted because `createdAt` is in the key" — only the **leading** field (prefix) enables targeting.
- "Hashed keys make every query fast" — ranges on any field scatter under a hashed key.
- Using `C101` as the `customerId` value — orders store the ObjectId; `C101` is the `customerNumber`.
- An `_id`-only lookup (Lab 6, Step 3) also scatters, because `_id` is not part of this shard key.

## Debrief points

- The leading shard-key field decides routing.
- Frequent, high-volume scatter-gather in the hot path means the shard key doesn't match the workload; rare reports need a different design, not a new key.
