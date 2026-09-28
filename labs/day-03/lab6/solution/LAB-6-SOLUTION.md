# Lab 6 solution — Replication and Sharding

**Day 3** · Module 7 · **Instructor reference. Do not hand this sheet to participants.**

Guide: [`../LAB-6-GUIDE.md`](../LAB-6-GUIDE.md) · Deck slide 49

## Running it

Allow 30–40 minutes. Steps 1–3 are reasoning on `training_store.orders` (about 15 minutes); Steps 4–7 inspect a real replica set (about 20 minutes). Learners without a replica-set URI follow Steps 4–7 on your screen.

Everything learners run only reads status or data, so it is safe on a shared cluster; nobody steps anything down. Failover and sharding commands run only on **instructor-controlled, disposable infrastructure** — never step down or shard a shared class cluster.

Before class: load `training_store` on the shared cluster with `datasets/training_store/load.js`, and give learners a lab user that can run `rs.status()` and `rs.conf()` (the `clusterMonitor` role, or equivalent on Atlas). Hand out the URI and credentials privately; never show a real password on screen.

---

## Step 1 — Identify the mechanism

| Requirement | Answer | Why |
| --- | --- | --- |
| Continue after one database server fails | **Replication** | Copies on other members keep serving. |
| Store data larger than one server can handle | **Sharding** | Each shard holds part of the data. |
| Distribute high write volume | **Sharding** | A replica set has one primary for all writes. |
| Automatically elect a replacement primary | **Replication** | A majority of voters elects a new primary. |
| Scale data while tolerating server failures | **Both** | Sharded cluster; every shard is a replica set. |
| Recover an order deleted last week | **Backup** | A delete is replicated to every secondary; sharding keeps it too. Only backups and a tested restore recover it (Module 8). |

## Step 2 — Shard-key problems

Fresh-load evidence from the `$group`: `SHIPPED` 6, `NEW` 4, `DELIVERED` 4, `PROCESSING` 3 (17 total).

| Candidate | Cardinality | Frequency | Monotonic writes? | Targets customer history? |
| --- | --- | --- | --- | --- |
| `{ fulfillmentStatus: 1 }` | Low — 4 values | High — each value is one large bucket | No, but most new orders start as `NEW`, so writes pile into one range | No |
| `{ createdAt: 1 }` | High | Low | **Yes** — every insert lands in the newest range (hot shard) | No |
| `{ customerId: "hashed" }` | High (many customers) | Depends on customer skew | No — hashing spreads writes | Equality yes; ranges on `customerId` scatter |
| `{ customerId: 1, createdAt: 1 }` | High | Low per combination | Only within one customer — usually fine | **Yes** — matches the Module 6 history query |

Verdict: reject `fulfillmentStatus`; flag ranged `createdAt`; prefer `{ customerId: 1, createdAt: 1 }` and name the remaining risk — a very large customer (and scatter-gather global reports).

## Step 3 — Targeted or scatter-gather?

| Query | Routing | Fresh-load result |
| --- | --- | --- |
| A `{ customerId: c._id }` | **Targeted** — shard-key prefix | 5 orders for C101: O5001, O6101, O6201, O6301, O6306 |
| B `{ fulfillmentStatus: "PROCESSING" }` | **Scatter-gather** — no shard key | 3 orders: O6202, O6302, O6401 |
| C `{ _id: o._id }` | **Scatter-gather** — `_id` is not in this shard key | 1 order: O6401 |

Remind learners: `c._id` is an ObjectId; `C101` is the `customerNumber`. On the replica set all three queries find their data in one place — routing only shows on a sharded cluster.

## Steps 4–6 — What a healthy Atlas set looks like

Hosts vary; the shape should be:

| Member | State | health | votes | priority | Arbiter? |
| --- | --- | --- | --- | --- | --- |
| `…-shard-00-00…:27017` | PRIMARY | 1 | 1 | same as the others | No |
| `…-shard-00-01…:27017` | SECONDARY | 1 | 1 | same | No |
| `…-shard-00-02…:27017` | SECONDARY | 1 | 1 | same | No |

- `db.hello()`: `setName` (Atlas sets are named like `atlas-xxxxxx-shard-0`), three `hosts`, a `primary`, and `isWritablePrimary: true` or `secondary: true`.
- Majority = 2 of 3 voters; the set tolerates one member down.
- `rs.printSecondaryReplicationInfo()`: each secondary 0–2 seconds behind the primary on a quiet set.

In a single-region Atlas cluster the electable members typically share one priority; exact priorities and host names depend on the deployment, so check for **one** PRIMARY, `health: 1`, three voters and no arbiter.

## Step 7 — A model health report

> Replica set `atlas-xxxxxx-shard-0` has one PRIMARY (`…-shard-00-00`) and two SECONDARY members, all `health: 1`, each with one vote and no arbiter, so a majority (2 of 3) is reachable and the set can lose one member and still elect a primary. Both secondaries were 0 seconds behind the primary at 10:15 (measured with `rs.printSecondaryReplicationInfo()`), so lag is not a concern now. No configuration smells: no arbiter carries durability and no nearby member has priority 0. To watch: lag during write bursts and backups.

Accept any report that names the primary, the majority, the measured lag and at least one thing to watch.

## Instructor demonstration (disposable infrastructure only)

Optional, on a cluster you can throw away — never on the shared class cluster:

```javascript
// Disposable replica set only: force an election, then watch a new primary appear
rs.stepDown(60)
rs.status().members.map(m => ({ name: m.name, state: m.stateStr }))
```

```javascript
// Disposable sharded cluster only, through mongos, on a scratch namespace
use training_shard
db.orders_lab.createIndex({ customerId: 1, createdAt: 1 })
sh.shardCollection("training_shard.orders_lab", { customerId: 1, createdAt: 1 })
sh.status()
db.orders_lab.getShardDistribution()
db.orders_lab.find({ customerId: someCustomerId }).explain()        // targeted
db.orders_lab.find({ fulfillmentStatus: "PROCESSING" }).explain()   // scatter-gather
```

Older versions also need `sh.enableSharding("training_shard")` first. A tiny training data set may sit in one range on one shard; that is expected, not a fault.

## What to listen for

- "Replication is our backup" — Step 1's last row exists to catch it.
- `fulfillmentStatus` or `paymentStatus` accepted as a shard key.
- Calling `{ createdAt: { $gte: … } }` targeted under `{ customerId: 1, createdAt: 1 }` — only the prefix enables targeting.
- Guessing lag ("it's fine") instead of measuring it.
- Any suggestion to run `rs.stepDown()` or `sh.shardCollection()` on the shared cluster.
