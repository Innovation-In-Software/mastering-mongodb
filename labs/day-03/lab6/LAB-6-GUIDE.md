# Lab 6 — Replication and Sharding

**Day:** 3 — Tune, Scale and Ship · **Module 7** (Introduction to Replication and Sharding)  
**Time:** 30–40 minutes  
**Difficulty:** Intermediate

**Deck:** `decks/pptx_new/MongoDB_Module07_Introduction_to_Replication_and_Sharding.pptx` — slide 49, "Lab 6 — Replication and Sharding"

**Objective:** Choose replication, sharding or a backup for stated requirements, reason about shard keys and query routing for `training_store.orders`, confirm the class VM is a standalone server, then read a sample replica-set status and write a short health report.

> **Safety.** Run this lab on the class VM (`mongodb://localhost:27017`). Every command reads status or data. Do not add `--replSet` to the local MongoDB service, and do not run failover or sharding commands.

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
| **Primary, secondaries, votes, majority** | Step 4 shows the VM is standalone. Steps 5–6 read those fields from the sample status in this guide. |
| **Replication lag** | Step 6: read each secondary's lag from the sample `rs.printSecondaryReplicationInfo()` output. |

### The `training_store.orders` facts you'll use

Loaded by `datasets/training_store/load.js`:

- 17 orders. Each has `orderNumber` (for example `O6401`), `customerId` (an **ObjectId** reference to a customer), `createdAt`, `paymentStatus`, `fulfillmentStatus`, `items`, `shippingAddress.country` (`Canada` or `USA`) and totals.
- The readable customer code, such as `C101`, is the customer's `customerNumber`, **not** what orders store. Customer C101 (Aisha Khan) has **5** orders.
- `fulfillmentStatus` has four values: `NEW`, `PROCESSING`, `SHIPPED`, `DELIVERED`. **3** orders are `PROCESSING`: O6202, O6302 and O6401.
- `paymentStatus` has three values: 13 orders are `PAID`.
- There is **no** `region` or `tenantId` field. Any key built on them is a what-if.

---

## Before you start

The whole lab runs on the class Windows VM. Steps 5–7 use the sample status printed later in this guide. This VM is not a replica set, so those steps have no live screenshot.

| Task | How |
| --- | --- |
| Steps 1–3 | Paper or a notes file. No database required. Optional read-only checks use the local `training_store` after `load.js`. |
| Step 4 | The `mongosh` session on `mongodb://localhost:27017`. Record `db.hello()` and the `rs.status()` error. That error is the correct result. |
| Steps 5–7 | Read the sample `rs0` status in this guide. Fill the member table and write the health report from those lines. Do **not** add `--replSet` to the local MongoDB service. Lab 7 uses that same standalone server. |
| Terminal | PowerShell in VS Code or Cursor (``Ctrl+` ``). |
| Data | Local `training_store` only. Do not change another server's data. |

Connect:

```powershell
mongosh "mongodb://localhost:27017"
```

```javascript
use training_store
```

Continue to Lab 7 on this same `localhost` server.

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
```

```javascript
const o = db.orders.findOne({ orderNumber: "O6401" })
```

```javascript
// A — customer history
db.orders.find({ customerId: c._id }).sort({ createdAt: -1 })
```

```javascript
// B — status only
db.orders.find({ fulfillmentStatus: "PROCESSING" })
```

```javascript
// C — _id only
db.orders.find({ _id: o._id })
```

You may run them on the class VM to see the documents. This server is not sharded, so the shell cannot show targeted versus scatter-gather routing. Classify each query from the shard key, and use the fresh-load counts as the results.

**Expected:**

| Query | Routing | Result on a fresh load |
| --- | --- | --- |
| A | **Targeted** — the filter includes the shard-key prefix `customerId` | 5 orders for C101 |
| B | **Scatter-gather** — no shard-key field in the filter | 3 orders: O6202, O6302, O6401 |
| C | **Scatter-gather** — `_id` is not part of this shard key | 1 order: O6401 |

---

### Step 4 — Confirm the class VM is standalone

**Do this:** On the class Windows VM, run these in the `mongosh` session already connected to `mongodb://localhost:27017`.

```javascript
db.hello()
```

```javascript
rs.status()
```

**Expected:** this server is standalone. `db.hello()` returns `isWritablePrimary: true` and `ok: 1`, and it has no `setName`, no `hosts` list and no `primary`. `rs.status()` fails with:

```text
MongoServerError[NoReplicationEnabled]: not running with --replSet
```

Record that pair of results. They are the correct reading for this install. Do not add `--replSet` to the local MongoDB service. Steps 5–7 use the sample below. Lab 7 continues on this same server.

---

### Sample replica-set status

Steps 5–7 read this fixed output from a three-member set named `rs0`. Do not run these commands on the class VM.

```text
db.hello()
  setName: "rs0"
  hosts: [ "rs0-a:27017", "rs0-b:27017", "rs0-c:27017" ]
  primary: "rs0-a:27017"
  isWritablePrimary: true

rs.status().members
  rs0-a:27017  PRIMARY    health 1
  rs0-b:27017  SECONDARY  health 1
  rs0-c:27017  SECONDARY  health 1

rs.conf().members
  rs0-a:27017  votes 1  priority 1  arbiterOnly false
  rs0-b:27017  votes 1  priority 1  arbiterOnly false
  rs0-c:27017  votes 1  priority 1  arbiterOnly false

rs.printSecondaryReplicationInfo()
  source: rs0-b:27017  0 secs (0 hrs) behind the primary
  source: rs0-c:27017  1 secs (0 hrs) behind the primary
```

---

### Step 5 — Record identity, votes and priority

**Do this:** From the sample, fill in:

| Member host | State | health | votes | priority | Arbiter? |
| --- | --- | --- | --- | --- | --- |
| | | | | | |
| | | | | | |
| | | | | | |

**Expected:** Set name `rs0`. One primary (`rs0-a:27017`) and two secondaries. Each member has health 1, 1 vote, priority 1, and is not an arbiter. The majority is 2 of 3.

---

### Step 6 — Record replication lag

**Do this:** From `rs.printSecondaryReplicationInfo()` in the sample, write how far each secondary is behind the primary.

**Expected:** `rs0-b` is 0 seconds behind. `rs0-c` is 1 second behind. Record both, including the zero. A secondary a few seconds behind (like Secondary B, 5 s, on the "Checking Replica-Set Health" slide) is still healthy, but worth watching. One second is not a concern.

---

### Step 7 — Write the health report

**Do this:** Write one short paragraph about the `rs0` sample that answers:

1. Is a primary present? Which host?
2. Is a majority of voting members reachable?
3. Is the lag a concern?
4. Any configuration smell — for example an arbiter carrying durability, or `priority: 0` on the only nearby member?

**Expected:** A report another operator could act on. Name `rs0-a:27017` as the primary, state that 2 of 3 voters are a majority and all three are healthy, and quote the measured lag (0 s and 1 s). Note that the set has no arbiter and no `priority: 0` member.

---

## Success criteria

- [ ] Backup — not replication — recovers last week's deleted order
- [ ] `fulfillmentStatus` is rejected as a shard key; ranged `createdAt` is flagged as a write hotspot
- [ ] The customer-history query is targeted for the compound key; the status-only and `_id`-only queries are scatter-gather
- [ ] The class VM records `not running with --replSet`
- [ ] The member table matches the `rs0` sample, including votes, priority and the measured lag
- [ ] The health report names the primary, the majority and the measured lag

---

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `rs.status()`: *not running with --replSet* | Connected to the class VM's standalone `mongod` | Expected in Step 4. Record the error, then complete Steps 5–7 from the sample. |
| Step 3 counts differ (not 5, 3, 1) | `training_store` was changed by an earlier lab | From the repository root, reload the local copy: `mongosh "mongodb://localhost:27017" .\datasets\training_store\load.js` |
| `c` or `o` is `null` | Wrong database, or data not loaded | Run `use training_store`, then check `db.orders.countDocuments()` returns 17. |
| Steps 5–7 commands fail on the VM | This server has no replica set | Leave the service standalone. Read the sample status in this guide. |
