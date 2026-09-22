# Lab 7: Production-Readiness Close

**Day 3 · Module 8**  
**PPT:** `decks/pptx/MongoDB_Module08_MongoDB_Best_Practices_Security_and_Troubleshooting.pptx`  
**Time:** 45–60 min (time-boxed) · up to 3 hours with the full lab block  
**Difficulty:** Intermediate

**Objective:** Treat `training_store` as a go-live candidate: fix one query, build one pipeline, add a validator on a **scratch** collection, restore into an isolated database, and score readiness.

**Prerequisite:** Reload if Day 2–3 writes remain. Never restore over `training_store`.

```powershell
mongosh "mongodb://localhost:27017" .\datasets\training_store\load.js
```

Time-boxed path (this file): Steps 1–5. Full path: [Labs 8.1–8.11](../slide-exercises/module-08/).

Driver-language wiring is **not** a new module — use [`sample-app/README.md`](../sample-app/README.md).

---

## Environment basics

**Demonstration environment:** Windows 10/11 · PowerShell · `mongosh`

Schema and restore work uses `training_store_ops` / `training_store_restore` so the class database stays intact.

---

## Steps from the training slides

### Step 1 — Stop the collection scan (Lab 8.2)

**Do this:** Rewrite a catalog page that currently uses `find({})`. Filter active laptops, project sku/name/price, sort price, limit 20, then `explain`:

```javascript
use training_store

db.products.find(
  { category: "LAPTOP", active: true },
  { _id: 0, sku: 1, name: 1, price: 1 }
).sort({ price: 1 }).limit(20).explain("executionStats")
```

If you still have Lab 5 indexes, note whether this shape uses them. Propose `{ category: 1, active: 1, price: 1 }` (ESR: equality, equality, sort/range) **without dropping** existing indexes.

**Expected result:** Filter is selective. Projection omits `attributes`. You recorded plan shape and did not run `find({})` in a “production” story.

Full write-up: [Lab 8.2](../slide-exercises/module-08/lab-8.2-query-and-projection-optimization.md).

---

### Step 2 — Monthly paid-order pipeline (Lab 8.3)

**Do this:** Complete [Lab 8.3](../slide-exercises/module-08/lab-8.3-aggregation-pipeline-construction.md) **or** produce month, order count, and total revenue for PAID orders:

```javascript
db.orders.aggregate([
  { $match: { paymentStatus: "PAID" } },
  {
    $group: {
      _id: { $dateToString: { format: "%Y-%m", date: "$createdAt" } },
      orderCount: { $sum: 1 },
      revenue: { $sum: "$total" }
    }
  },
  { $sort: { _id: 1 } }
])
```

**Expected result:** Months **2026-07**, **2026-08**, and **2026-09** appear. `$match` is first.

---

### Step 3 — Validator on a scratch collection (Lab 8.6)

**Do this:** Follow [Lab 8.6](../slide-exercises/module-08/lab-8.6-schema-validation-implementation.md) on `training_store_ops.orders_validated`. Required: `orderNumber` string, `total` decimal, `paymentStatus` enum.

Minimum sketch:

```javascript
use training_store_ops
db.createCollection("orders_validated", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["orderNumber", "total", "paymentStatus"],
      properties: {
        orderNumber: { bsonType: "string" },
        total: { bsonType: "decimal" },
        paymentStatus: { enum: ["PAID", "PENDING", "FAILED"] }
      }
    }
  },
  validationAction: "error"
})

db.orders_validated.insertOne({
  orderNumber: "OPS-1",
  total: NumberDecimal("10.00"),
  paymentStatus: "PAID"
})

db.orders_validated.insertOne({
  orderNumber: "OPS-BAD",
  total: "10.00",
  paymentStatus: "PAID"
})
```

**Expected result:** First insert succeeds. Second insert is **rejected** (`total` must be decimal, not a string). `training_store.orders` is unchanged.

---

### Step 4 — Restore to an isolated database (Lab 8.9)

**Do this:** Complete [Lab 8.9](../slide-exercises/module-08/lab-8.9-backup-and-restore-verification.md) **or** dump and restore into `training_store_restore` only:

```powershell
mkdir "$env:TEMP\mongodb-lab7" -Force
mongodump --uri="mongodb://localhost:27017" --db=training_store --out="$env:TEMP\mongodb-lab7"
mongorestore --uri="mongodb://localhost:27017" --db=training_store_restore --drop "$env:TEMP\mongodb-lab7\training_store"
```

Then in `mongosh`:

```javascript
use training_store_restore
db.products.countDocuments({})
use training_store
db.products.countDocuments({})
```

**Expected result:** Restore database has 13 products. **Class `training_store` still has 13 products.** You never pointed `mongorestore` at `training_store`.

Skip dump/restore if the classroom image has no Database Tools; write the RPO/RTO answers in [Exercise 8.8](../slide-exercises/module-08/exercise-8.8-define-rpo-and-rto.md) instead.

---

### Step 5 — Score go-live (Exercise 8.13 / 8.14)

**Do this:** Classify `training_store` as **ready**, **ready with conditions**, or **not ready**. Cite at least four of: string price on `XBAD`, no authentication in class, tiny data, missing stock field, reviews unbounded if moved onto products, no tested restore in *your* environment, indexes from Lab 5 may be leftover.

**Expected result:** **Not ready** for production. Conditions would include: typed money, auth + TLS, backup restore drill, least-privilege roles, monitored `explain` on real volume.

Full checklist: [Exercise 8.13](../slide-exercises/module-08/exercise-8.13-complete-a-production-readiness-assessment.md) · challenge: [Exercise 8.14](../slide-exercises/module-08/exercise-8.14-practical-challenge.md)

---

## Success criteria

- [ ] Catalog query is filtered, projected, sorted, and limited
- [ ] Paid-order pipeline groups by month with `$match` first
- [ ] Invalid validator insert was rejected on `training_store_ops`
- [ ] Restore target was `training_store_restore`, never `training_store`
- [ ] Go-live classification is **not ready**, with named evidence
