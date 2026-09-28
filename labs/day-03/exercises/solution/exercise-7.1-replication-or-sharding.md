# Exercise 7.1 — solution (instructor)

**Module 7** · Day 3 · Checkpoint A  
**Type:** design discussion · **Do not hand this sheet to participants.**

Worksheet: [`../exercise-7.1-replication-or-sharding.md`](../exercise-7.1-replication-or-sharding.md) · Deck slide 45

## Running it

Seven minutes in pairs, then a three-minute debrief. Reveal the solution column only after the groups share. It is classroom discussion; learners may look at `training_store` or `rs.status()` to test ideas, but nobody needs to run anything.

## Tasks 1 and 2 — Solution

| # | Requirement | Mechanism | Why |
| --- | --- | --- | --- |
| 1 | Survive one server failure | **Replication** | A replica set keeps copies on several members; if one fails, the others keep serving. |
| 2 | Increase total data capacity | **Sharding** | Each shard holds part of the collection, so adding shards adds capacity. |
| 3 | Elect a replacement primary | **Replication** | Elections are a replica-set feature: a majority of voters promotes a secondary. |
| 4 | Distribute write load | **Sharding** | In a replica set every write goes to the one primary; only sharding spreads writes over several primaries. |
| 5 | A local development database | **Neither yet** | A standalone `mongod` is enough for development and learning. |
| 6 | Production availability + scale | **Both** | A sharded cluster whose every shard is a replica set: sharding distributes the data, replication protects each shard. |

Slide summary: 1 Replication · 2 Sharding · 3 Replication · 4 Sharding · 5 Neither yet: standalone · 6 Both: sharded replica sets.

## Task 3 — The borderline case

Each member of a replica set stores the **same logical data set** — all of `training_store`. Extra members add redundancy (and read options), not a larger working set; capacity grows only when the data is split across shards.

## Task 4 — The Lab 6 row

**Recover an order deleted last week → a backup.** Neither replication nor sharding restores it: a delete (even `db.orders.deleteMany({})`) is replicated to every secondary, and sharding just keeps the delete on whichever shard owned the document. Only backups and a tested restore recover it (Module 8).

## What to listen for

- "Replication gives us more space" — correct it with Task 3.
- "A replica set spreads writes over its members" — no: all writes go to the primary.
- Forcing requirement 5 into a replica set. A single-member replica set is sometimes used locally for features such as change streams, but the requirement itself needs neither mechanism.
- "Replication is a backup" — the Lab 6 row exists to catch this.

## Debrief points

- Replicate to stay online. Shard to grow. Back up to recover.
- Production clusters usually need both, and each step adds cost and operations work — take it only when the previous one is not enough.
