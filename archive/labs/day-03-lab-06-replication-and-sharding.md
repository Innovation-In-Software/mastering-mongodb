# Lab 6: Replication and Sharding Diagnostics

**Day 3 · Module 7**  
**PPT:** `decks/pptx/MongoDB_Day3_Tune_Scale_and_Ship.pptx` — Module 7 section (Diagnostic Exercises 1–3)  
**Time:** 30–40 min  
**Difficulty:** Intermediate

**Objective:** Choose replication vs sharding for stated requirements, score shard-key candidates for `orders`, and classify targeted vs scatter-gather queries.

Failover and `sh.enableSharding` commands run only on **instructor-controlled disposable infrastructure**. Atlas M0 is a replica set, not a sharded cluster.

**Companion labs:** [Lab 7.1](../slide-exercises/module-07/lab-7.1-verify-replica-set-health.md) (required if an Atlas URI is available) · [Exercise 7.1](../slide-exercises/module-07/exercise-7.1-replication-or-sharding.md)–[7.9](../slide-exercises/module-07/exercise-7.9-targeted-or-scatter-gather.md)

---

## Environment basics

**Discussion first.** Keyboard work in Step 4 needs a replica-set URI (Atlas or instructor set). You can finish Steps 1–3 on paper.

---

## Steps from the training slides

### Step 1 — Identify the mechanism (PPT Exercise 1)

**Do this:** For each requirement, write Replication, Sharding, Both, or Neither (backup).

| Requirement | Your answer |
|-------------|-------------|
| Continue after one database server fails | |
| Store data larger than one server can handle | |
| Distribute high write volume | |
| Automatically elect a replacement primary | |
| Scale data while tolerating server failures | |
| Recover an order deleted last week | |

**Expected result:** Replication · Sharding · Sharding · Replication · Both · **Backup** (neither replication nor sharding restores last week’s delete).

---

### Step 2 — Identify shard-key problems (PPT Exercise 2)

**Do this:** Score these candidates for `training_store.orders`.

| Candidate | Cardinality | Frequency | Monotonic writes | Targeted customer history? |
|-----------|-------------|-----------|------------------|----------------------------|
| `{ fulfillmentStatus: 1 }` | | | | |
| `{ createdAt: 1 }` | | | | |
| `{ customerId: "hashed" }` | | | | |
| `{ customerId: 1, createdAt: 1 }` | | | | |

**Expected result:**

- `fulfillmentStatus` — few values (`NEW` / `PROCESSING` / `SHIPPED` / `DELIVERED`); hotspot risk.
- `createdAt` — high cardinality but new orders land at the high end of the range (hot shard).
- hashed `customerId` — spreads writes; equality by customer can be targeted; range by raw customer id is weaker.
- compound `{ customerId: 1, createdAt: 1 }` — matches the history query from Lab 5; still needs a plan for a mega-customer.

---

### Step 3 — Targeted or scatter-gather? (PPT Exercise 3)

Assume the shard key is `{ customerId: 1, createdAt: 1 }`.

**Do this:** Classify each query.

```javascript
// A — customer history
db.orders.find({ customerId: customerId })

// B — status only
db.orders.find({ fulfillmentStatus: "PROCESSING" })

// C — _id only
db.orders.find({ _id: orderId })
```

**Expected result:**

| Query | Routing |
|-------|---------|
| A | Targeted (or bounded) — includes the shard-key prefix |
| B | Scatter-gather — no shard key in the filter |
| C | Scatter-gather unless `_id` is the shard key (it is not, in this design) |

---

### Step 4 — Inspect a replica set (if URI available)

**Do this:** Follow [Lab 7.1](../slide-exercises/module-07/lab-7.1-verify-replica-set-health.md):

```javascript
rs.status()
rs.conf()
```

**Expected result:** You can name the primary, the number of members, and whether the set is healthy. Skip this step on a standalone `localhost` Community install.

---

## Success criteria

- [ ] Backup is not listed as a replica-set feature
- [ ] `fulfillmentStatus` was rejected as a shard key
- [ ] Customer-history query classified as targeted for the compound key
- [ ] Status-only query classified as scatter-gather
