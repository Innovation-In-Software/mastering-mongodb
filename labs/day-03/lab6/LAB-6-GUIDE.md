# Lab 6 — Replication and Sharding

**Day:** 3 — Tune, Scale and Ship · **Module 7** (Introduction to Replication and Sharding)  
**Time:** 30–40 minutes  
**Difficulty:** Intermediate

**Deck:** `decks/pptx_new/MongoDB_Module07_Introduction_to_Replication_and_Sharding.pptx` — slide 49, "Lab 6 — Replication and Sharding"

**Objective:** Choose replication, sharding or a backup for stated requirements, reason about shard keys and query routing for `training_store.orders`, then inspect a real replica set and write a short health report.

> **Safety.** Failover and sharding commands run only on instructor-controlled, disposable infrastructure. Never step down or shard a shared class cluster. Every command **you** run in this lab only reads status or data.

---

## What you will finish with

- A mechanism (Replication, Sharding, Both, or Backup) for six requirements
- A short evaluation of four shard-key candidates for `training_store.orders`
- A routing classification (targeted or scatter-gather) for three queries
- A table of replica-set members: state, health, votes, priority and lag
- A one-paragraph replica-set health report another operator could act on

Keep the health report and your answers: Module 8's production-readiness review builds on them.

---

## Knowledge you need (from Module 7)

| Module 7 idea | How it appears in this lab |
| --- | --- |
| **Availability vs scale** | Step 1: replication keeps copies online; sharding adds capacity and write throughput. |
| **Replication is not a backup** | Step 1: a delete is replicated to every member. |
| **Cardinality, frequency, monotonic keys** | Step 2: why `fulfillmentStatus` and ranged `createdAt` are poor shard keys. |
| **Targeted vs scatter-gather** | Step 3: only filters with the shard-key prefix can be targeted. |
| **Primary, secondaries, votes, majority** | Steps 4–5: read them from `rs.status()`, `rs.conf()` and `db.hello()`. |
| **Replication lag** | Step 6: measure it with `rs.printSecondaryReplicationInfo()`. |

### The `training_store.orders` facts you'll use

Loaded by `datasets/training_store/load.js`:

- 17 orders. Each has `orderNumber` (for example `O6401`), `customerId` (an **ObjectId** reference to a customer), `createdAt`, `paymentStatus`, `fulfillmentStatus`, `items`, `shippingAddress.country` (`Canada` or `USA`) and totals.
- The readable customer code, such as `C101`, is the customer's `customerNumber`, **not** what orders store. Customer C101 (Aisha Khan) has **5** orders.
- `fulfillmentStatus` has four values: `NEW`, `PROCESSING`, `SHIPPED`, `DELIVERED`. **3** orders are `PROCESSING`: O6202, O6302 and O6401.
- `paymentStatus` has three values: 13 orders are `PAID`.
- There is **no** `region` or `tenantId` field. Any key built on them is a what-if.

---

## Before you start

| Task | How |
| --- | --- |
| Steps 1–3 | Paper or a notes file. No database needed; the optional checks run on any `training_store`. |
| Steps 4–7 | `mongosh` connected with the **instructor's replica-set or Atlas URI** (`mongodb+srv://…`). A local standalone `mongod` on `localhost` is **not** a replica set. |
| Terminal | PowerShell in VS Code or Cursor (``Ctrl+` ``). |
| Credentials | The instructor gives you the URI and a lab user. Type the password only at the `mongosh` prompt; never put a real password in notes, slides or chat. |
| Data | `training_store` loaded with `load.js` (the instructor has loaded it on the shared cluster). Do **not** update or delete shared data. |

Connect (placeholders only — use the values your instructor gives you):

```powershell
mongosh "mongodb+srv://<cluster-host>/training_store" --username <lab-user>
```

`mongosh` prompts for the password. Then:

```javascript
use training_store
```

No replica-set URI available? Do Steps 1–3, then follow Steps 4–7 on the instructor's screen and write the report from their output.

---

## Steps

Follow the steps in order. Finish one step before starting the next.

### Step 1 — Identify the mechanism

**Do this:** For each requirement, write **Replication**, **Sharding**, **Both**, or **Neither — backup**.

| Requirement | Your answer |
| --- | --- |
| Continue after one database server fails | |
| Store data larger than one server can handle | |
| Distribute high write volume | |
| Automatically elect a replacement primary | |
| Scale data while tolerating server failures | |
| Recover an order deleted last week | |

**Expected:** Replication · Sharding · Sharding · Replication · Both · **Backup** — neither replication nor sharding restores last week's delete.

---

### Step 2 — Identify shard-key problems

**Do this:** Evaluate these candidates for `training_store.orders`.

| Candidate | Cardinality | Frequency | Monotonic writes? | Targets customer history? |
| --- | --- | --- | --- | --- |
| `{ fulfillmentStatus: 1 }` | | | | |
| `{ createdAt: 1 }` | | | | |
| `{ customerId: "hashed" }` | | | | |
| `{ customerId: 1, createdAt: 1 }` | | | | |

Optional evidence (read-only, on any `training_store`):

```javascript
db.orders.aggregate([
  { $group: { _id: "$fulfillmentStatus", n: { $sum: 1 } } },
  { $sort: { n: -1 } }
])
```

**Expected:** Four groups: `SHIPPED` 6, `NEW` 4, `DELIVERED` 4, `PROCESSING` 3.

- `fulfillmentStatus` — only four values, so at most four ranges; high frequency per value; a hotspot risk. **Rejected.**
- `createdAt` — high cardinality, but monotonic: every new order lands in the newest range, on one hot shard.
- hashed `customerId` — spreads writes evenly; equality on a customer is still targeted; ranges on `customerId` scatter.
- `{ customerId: 1, createdAt: 1 }` — matches the customer-history query from Module 6 (Lab 5); still needs a plan for a very large customer.

---

### Step 3 — Targeted or scatter-gather?

Assume the shard key is `{ customerId: 1, createdAt: 1 }`.

**Do this:** Classify each query.

```javascript
const c = db.customers.findOne({ customerNumber: "C101" })
const o = db.orders.findOne({ orderNumber: "O6401" })

// A — customer history
db.orders.find({ customerId: c._id }).sort({ createdAt: -1 })

// B — status only
db.orders.find({ fulfillmentStatus: "PROCESSING" })

// C — _id only
db.orders.find({ _id: o._id })
```

You may run them on the replica set to see the results. A replica set keeps all the data in one place, so it cannot show routing — that is a sharded-cluster behaviour.

**Expected:**

| Query | Routing | Result on a fresh load |
| --- | --- | --- |
| A | **Targeted** — the filter includes the shard-key prefix `customerId` | 5 orders for C101 |
| B | **Scatter-gather** — no shard-key field in the filter | 3 orders: O6202, O6302, O6401 |
| C | **Scatter-gather** — `_id` is not part of this shard key | 1 order: O6401 |

---

### Step 4 — Confirm you are on a replica set

**Do this:** Connected with the replica-set URI, run:

```javascript
db.hello()
rs.status()
```

**Expected:** `db.hello()` shows a `setName`, a `hosts` list, the `primary`, and `isWritablePrimary: true` (you are on the primary) or `secondary: true`. `rs.status()` shows the set name, exactly **one** `PRIMARY`, one or more `SECONDARY` members, and `health: 1` on each reachable member.

If you see *"not running with --replSet"*, you are on a standalone server: stop and switch to the instructor's URI.

---

### Step 5 — Record identity, votes and priority

**Do this:** Run:

```javascript
rs.conf()
rs.status().members.map(m => ({ name: m.name, state: m.stateStr, health: m.health }))
rs.conf().members.map(m => ({ host: m.host, votes: m.votes, priority: m.priority,
                              arbiterOnly: m.arbiterOnly }))
```

Fill in:

| Member host | State | health | votes | priority | Arbiter? |
| --- | --- | --- | --- | --- | --- |
| | | | | | |
| | | | | | |
| | | | | | |

**Expected:** Set name, one primary host, the secondary hosts. Atlas typically shows **three data-bearing members, each with 1 vote, and no arbiter**; the majority is 2 of 3.

---

### Step 6 — Record replication lag

**Do this:** Run:

```javascript
rs.printSecondaryReplicationInfo()
```

**Expected:** For each secondary, how far it is behind the primary — often **0–2 seconds** on a quiet training set. Record the values even when they are zero. A secondary a few seconds behind (like Secondary B, 5 s, on the "Checking Replica-Set Health" slide) is still healthy, but worth watching.

---

### Step 7 — Write the health report

**Do this:** Write one short paragraph that answers:

1. Is a primary present? Which host?
2. Is a majority of voting members reachable?
3. Is the lag a concern?
4. Any configuration smell — for example an arbiter carrying durability, or `priority: 0` on the only nearby member?

**Expected:** A report that would make sense to another operator, with the lag **measured, not guessed**, and concerns listed even if the set is healthy. No unexplained red states.

---

## Instructor demonstration — watch only

On an **instructor-controlled, disposable** replica set or sharded cluster, the instructor may show a failover (`rs.stepDown()`) and the result of sharding a scratch collection (`sh.status()`, `getShardDistribution()`, `explain()` on queries A and B). Participants do **not** run these commands, and nobody runs them on the shared class cluster. Atlas free-tier clusters are replica sets, not sharded clusters.

---

## Success criteria

- [ ] Backup — not replication — recovers last week's deleted order
- [ ] `fulfillmentStatus` is rejected as a shard key; ranged `createdAt` is flagged as a write hotspot
- [ ] The customer-history query is targeted for the compound key; the status-only and `_id`-only queries are scatter-gather
- [ ] The primary is identified and the voting configuration is recorded
- [ ] Lag is measured, not guessed
- [ ] The health report lists concerns even if the set is healthy

---

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `rs.status()`: *not running with --replSet* | Connected to a local standalone `mongod` | Reconnect with the instructor's replica-set / Atlas URI. |
| `not authorized … replSetGetStatus` or `replSetGetConfig` | The lab user lacks monitoring privileges, or the tier restricts the command | Use `db.hello()` for Steps 4–5 and take `rs.status()` / `rs.conf()` output from the instructor's screen. |
| `db.hello()` shows `secondary: true` | The shell reached a secondary (for example a `readPreference` in the URI) | Fine for reading status. Note it in the report; don't try to write. |
| `Authentication failed` | Wrong user or password | Re-enter the password at the prompt. Never paste real credentials into notes or chat. |
| Step 3 counts differ (not 5, 3, 1) | `training_store` was changed by an earlier lab | Ask the instructor; reload only your own local copy with `load.js`, never the shared cluster. |
| `c` or `o` is `null` | Wrong database, or data not loaded | Run `use training_store`, then check `db.orders.countDocuments()` returns 17. |
| Lag is large or growing | Busy or slow secondary, write burst | Record it; say what you'd check next (member optimes, then the secondary's CPU and disk). |
