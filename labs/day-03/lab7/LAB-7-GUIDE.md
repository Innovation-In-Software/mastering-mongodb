# Lab 7 — Production Readiness

**Day:** 3 — Module 8 (MongoDB Best Practices, Security, and Troubleshooting)  
**Deck:** `decks/pptx_new/MongoDB_Module08_Best_Practices_Security_and_Troubleshooting.pptx` — slide 48, "Lab 7 — Production Readiness"  
**Time:** 45–60 minutes  
**Difficulty:** Intermediate

**Objective:** The course's final lab: treat `training_store` as a go-live candidate. You fix one query, build one pipeline, add a validator on a **scratch** collection, restore into an **isolated** database, and score readiness with evidence.

---

## What you will finish with

By the end of this lab you will have:

- A catalog query that is filtered, projected, sorted, limited and checked with `explain`
- A monthly paid-revenue pipeline with `$match` first
- A validator on `training_store_ops.orders_validated` that accepts one insert and rejects another
- A copy of `training_store` restored into `training_store_restore`, with counts compared
- A go-live score — **ready**, **ready with conditions** or **not ready** — with named evidence

---

## Knowledge you need (from Module 8)

| Module 8 idea | Where it appears in this lab |
| --- | --- |
| Filter, project, sort, limit ("Ask Only for What the Page Needs") | Step 1 |
| ESR compound indexes and `explain("executionStats")` | Step 1 |
| `$match` first; sum order-level fields before any `$unwind` ("Monthly Paid Revenue — Built Safely") | Step 2 |
| `$jsonSchema` validation on a scratch collection ("A Validator on a Scratch Collection") | Step 3 |
| Replication is not a backup; restore testing ("Restore Testing") | Step 4 |
| The production-readiness checklist | Step 5 |

### The data you will meet

`training_store` after a fresh load: **6 customers, 13 products, 17 orders, 6 reviews; 13 orders are PAID**.

Use the real field names:

| Concept | Field in `training_store` |
| --- | --- |
| Payment state | `paymentStatus`: `PAID`, `PENDING`, `FAILED` |
| Fulfilment state | `fulfillmentStatus`: `NEW`, `PROCESSING`, `SHIPPED`, `DELIVERED` |
| Order date | `createdAt` |
| Line price | `items[].unitPrice` × `items[].quantity` (there is no `lineTotal`) |
| Order money | `total` (Decimal128) |
| Categories | `LAPTOP`, `SHOE`, `BOOK`, `ACCESSORY` |

The loader leaves real defects on purpose: **XBAD** stores `price` as the string `"49.99"`; **L190** has a stray `legacyName`; **A410** has a stray `temporaryNote`. There is no `stock` field.

---

## Before you start

**Environment:** Windows 10/11 · PowerShell · `mongosh` · MongoDB Database Tools (`mongodump`, `mongorestore`) · a local `mongod` on `localhost:27017`.

| Task | How |
| --- | --- |
| Terminal 1 | PowerShell at the repo root (`MasteringMongoDB`). Used for `load.js`, `mongodump` and `mongorestore`. |
| Terminal 2 | `mongosh "mongodb://localhost:27017"`. Used for every JavaScript block. |
| Copy | One block at a time. Lines starting with `//` are expected output, not commands. |

**Safety rules for this lab**

- Schema work runs on **`training_store_ops`**; the restore goes to **`training_store_restore`**. `training_store` itself is only read.
- **Never** point `mongorestore` at `training_store`.
- Don't enable authentication or create users on the shared class instance.
- Never type a real password into a command. If your instance needs credentials, use `passwordPrompt()` in `mongosh` or a `<password>` placeholder in a URI you fill in privately.

### Step 0 — Reload and check tools

Reload if Day 2–3 writes remain (Terminal 1):

```powershell
mongosh "mongodb://localhost:27017" .\datasets\training_store\load.js
```

Expected output includes:

```text
Loaded training_store
customers: 6
products: 13
orders: 17
reviews: 6
paid orders: 13
```

Check the Database Tools (Terminal 1):

```powershell
mongodump --version
mongorestore --version
```

If either command is not found, you will do the written alternative in Step 4.

---

## Step 1 — Stop the catalog collection scan

A catalog page currently runs `db.products.find({})` and returns all 13 products with every field, including `attributes`. Rewrite it for the page's real need: **active laptops**, three fields, cheapest first, at most 20.

```javascript
use training_store

db.products.find(
  { category: "LAPTOP", active: true },
  { _id: 0, sku: 1, name: 1, price: 1 }
).sort({ price: 1 }).limit(20)
```

Then look at the plan:

```javascript
db.products.find(
  { category: "LAPTOP", active: true },
  { _id: 0, sku: 1, name: 1, price: 1 }
).sort({ price: 1 }).limit(20).explain("executionStats")
```

Record: the winning-plan stages, `nReturned`, `totalKeysExamined`, `totalDocsExamined`, and whether there is a `SORT` stage.

Propose the index for this shape — **equality, equality, sort**:

```javascript
// proposal — ESR: category (E), active (E), price (S)
{ category: 1, active: 1, price: 1 }
```

If you still have indexes from Lab 5, note whether this shape uses them. **Don't drop existing indexes.** Create the proposed index only if your instructor allows it, and then re-run the explain.

**Expected result:** two active laptops — L100 Business Laptop 1299.99 and L110 Ultrabook 1899.99. L190, the Refurbished Laptop, is inactive and drops out. The projection omits `attributes`. You recorded the plan shape.

---

## Step 2 — Monthly paid-order pipeline

Produce month, order count and revenue for **PAID** orders. Group whole orders — don't `$unwind` items before summing `total`.

```javascript
db.orders.aggregate([
  { $match: { paymentStatus: "PAID" } },
  { $group: {
      _id: { $dateToString: { format: "%Y-%m", date: "$createdAt" } },
      orderCount: { $sum: 1 },
      revenue: { $sum: "$total" } } },
  { $sort: { _id: 1 } }
])
```

Check the result against an independent control:

```javascript
db.orders.countDocuments({ paymentStatus: "PAID" })
```

**Expected result:** three months — 2026-07, 2026-08 and 2026-09. `$match` is the first stage. The order counts add up to the control count.

---

## Step 3 — Validator on a scratch collection

Create `orders_validated` in **`training_store_ops`**. Required: `orderNumber` string, `total` decimal, `paymentStatus` one of the three real values.

```javascript
use training_store_ops
db.createCollection("orders_validated", {
  validator: { $jsonSchema: {
    bsonType: "object",
    required: ["orderNumber", "total", "paymentStatus"],
    properties: {
      orderNumber: { bsonType: "string" },
      total: { bsonType: "decimal" },
      paymentStatus: { enum: ["PAID", "PENDING", "FAILED"] }
    } } },
  validationAction: "error"
})
```

Prove one accept and one reject:

```javascript
db.orders_validated.insertOne({
  orderNumber: "OPS-1",
  total: Decimal128("10.00"),
  paymentStatus: "PAID" })

db.orders_validated.insertOne({
  orderNumber: "OPS-BAD",
  total: "10.00",
  paymentStatus: "PAID" })
```

`Decimal128("10.00")` and `NumberDecimal("10.00")` are the same constructor in `mongosh`.

Confirm the class data is untouched:

```javascript
use training_store
db.orders.countDocuments({})
```

**Expected result:** OPS-1 is accepted. OPS-BAD is **rejected** — `total` must be a decimal, not a string. `training_store.orders` still has 17 orders.

---

## Step 4 — Restore to an isolated database

Dump `training_store` and restore it into **`training_store_restore` only** (Terminal 1):

```powershell
mkdir "$env:TEMP\mongodb-lab7" -Force
mongodump --uri="mongodb://localhost:27017" --db=training_store --out="$env:TEMP\mongodb-lab7"
mongorestore --uri="mongodb://localhost:27017" --db=training_store_restore --drop "$env:TEMP\mongodb-lab7\training_store"
```

`--drop` replaces collections in the **restore** database only.

Compare both databases (Terminal 2):

```javascript
use training_store_restore
db.products.countDocuments({})
db.orders.countDocuments({})
db.orders.findOne({ orderNumber: "O5001" }, { _id: 0, orderNumber: 1, paymentStatus: 1, total: 1 })
db.orders.getIndexes()

use training_store
db.products.countDocuments({})
```

Time the restore and write it down — that is your measured RTO for this data size.

**No Database Tools?** Skip the commands and write the orders restore proof from [Exercise 8.3](../exercises/exercise-8.3-define-rpo-and-rto.md), Task 3, instead.

**Expected result:** the restore database has 13 products (and 17 orders). **Class `training_store` still has 13 products.** You never pointed `mongorestore` at `training_store`.

---

## Step 5 — Score go-live with evidence

Use the Production-Readiness Checklist from the deck (data model · queries and aggregation · indexes · security · availability and recovery · operations). Classify `training_store` as **ready**, **ready with conditions** or **not ready**.

Cite at least **four** pieces of evidence, for example:

- `XBAD` stores `price` as a string
- no authentication in class
- one server, not a replica set
- no validator on `training_store.orders`
- tiny data — plans and timings not proven at real volume
- no `stock` field for the catalog
- reviews would be unbounded if moved onto products
- no restore tested in **your** environment (before today)
- indexes left over from Lab 5 that no named query shape needs

Then list the **conditions** that would have to be met before go-live.

| Area | Status (ready / conditional / not ready) | Evidence |
| --- | --- | --- |
| Data model | | |
| Queries and aggregation | | |
| Indexes | | |
| Security | | |
| Availability and recovery | | |
| Operations | | |
| **Overall** | | |

**Expected result:** **not ready**, with named evidence. Conditions include typed money, authentication and TLS, a restore drill, least-privilege roles and `explain` on real volume.

---

## Success criteria

- [ ] Catalog query is filtered, projected, sorted and limited, and you recorded its `explain`
- [ ] Paid-order pipeline groups by month with `$match` first, and its counts match the control
- [ ] The invalid insert (OPS-BAD) was rejected on `training_store_ops`
- [ ] Restore target was `training_store_restore`, never `training_store`; product counts match (13 and 13)
- [ ] Go-live classification is **not ready**, with at least four pieces of named evidence and a list of conditions

---

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Step 1 returns nothing | Wrong case (`"laptop"`) or wrong database | Use `"LAPTOP"`, `active: true`, and `use training_store` |
| Step 1 returns L190 | Missing `active: true` | Add the second equality condition |
| Step 1 plan shows `SORT` and `COLLSCAN` | Expected on a fresh load — there is no category index | That is the evidence for your proposal; don't create indexes on shared data unless allowed |
| Step 2 shows more than 13 orders or revenue 12119.25 | Items were `$unwind`-ed before summing `total` | Remove `$unwind`; sum `total` on whole orders |
| Step 2 has a `null` month | Grouping on a field that doesn't exist (`orderedAt`, `orderDate`) | Use `$createdAt` |
| Step 2 has no documents | Filtering on `status` | The field is `paymentStatus` |
| Step 3: `Collection ... already exists` | You ran `createCollection` before | `use training_store_ops` then `db.orders_validated.drop()` and re-run |
| Step 3: OPS-BAD was accepted | The collection was created without the validator, or in another database | Drop it in `training_store_ops` and re-create it with the validator |
| Step 3: OPS-1 rejected | `total: 10.00` typed as a plain number (a double) | Use `Decimal128("10.00")` |
| Step 4: `mongodump` not recognized | Database Tools not installed or not on `PATH` | Use the Exercise 8.3 written alternative |
| Step 4: warning that `--db` with a directory is deprecated | Newer `mongorestore` versions | The command still works; the alternative is `--nsFrom="training_store.*" --nsTo="training_store_restore.*"` with the dump folder |
| Step 4: restore database has 0 documents | Path points at the dump root, not the `training_store` subfolder | End the path with `\training_store` |
| Connection refused | `mongod` isn't running or the port is wrong | Start `mongod`; check `localhost:27017`. Never "fix" it by binding to every interface (`bindIp: 0.0.0.0`) |
| Authentication failed | Your instance has access control on | Connect with your own user and `passwordPrompt()`; check `authSource` |

---

## Clean up (optional)

The scratch databases can be dropped when you are done — they are not the class data:

```javascript
use training_store_ops
db.dropDatabase()
use training_store_restore
db.dropDatabase()
```

Driver-language wiring is not a new module — see [`sample-app/README.md`](../../../sample-app/README.md).
