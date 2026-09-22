# Lab 5: Index and Explain

**Day 3 · Module 6**  
**PPT:** `decks/pptx/MongoDB_Module06_Indexing_and_Query_Performance.pptx` (Hands-On Indexing Lab, Exercises 1–6)  
**Time:** 40–50 min  
**Difficulty:** Intermediate

**Objective:** Capture an `explain` baseline, create a compound index for customer order history, compare a mismatched query shape, add a multikey index, and inventory indexes.

This is the outline hands-on: *Tuning with indexes.* Teach **plan shape** (`COLLSCAN` vs `IXSCAN`) and **examined vs returned** counts. Twelve products will not produce dramatic wall-clock wins.

**Prerequisite:** Reload so Lab 3 writes are gone:

```powershell
mongosh "mongodb://localhost:27017" .\datasets\training_store\load.js
```

```javascript
use training_store
```

Do **not** copy `ObjectId("66a100000000000000000001")` from the PPT example — that id is not in this dataset. Look up `C101` by `customerNumber`. Orders sort on `createdAt`, not `orderedAt`.

**Companion labs:** [Lab 6.1](../slide-exercises/module-06/lab-6.1-establish-a-performance-baseline.md)–[Lab 6.11](../slide-exercises/module-06/lab-6.11-integrated-query-tuning-challenge.md)

---

## Environment basics

**Demonstration environment:** Windows 10/11 · PowerShell · `mongosh`

---

## Steps from the training slides

### Step 1 — Establish the baseline (PPT Exercise 1)

**Do this:**

```javascript
const customer = db.customers.findOne({ customerNumber: "C101" })
const customerId = customer._id

db.orders.find({ customerId: customerId })
  .sort({ createdAt: -1 })
  .explain("executionStats")
```

Record:

```text
winningPlan.stage:
nReturned:
totalKeysExamined:
totalDocsExamined:
```

**Expected result:** Before the history index, the winning plan is typically `COLLSCAN` (or `IXSCAN` on `_id` only if a fetch+sort appears). `nReturned` is C101’s order count (several documents, including `O5001`, `O6101`, `O6301`, …).

---

### Step 2 — Create the history index (PPT Exercise 2)

**Do this:** Equality on `customerId`, sort on `createdAt` descending:

```javascript
db.orders.createIndex(
  { customerId: 1, createdAt: -1 },
  { name: "idx_orders_customer_date" }
)
```

**Expected result:** `{ ok: 1 }` and the name `idx_orders_customer_date`. Unique indexes on `orderNumber` already exist from `load.js`.

---

### Step 3 — Measure again (PPT Exercise 3)

**Do this:** Re-run the same `explain("executionStats")` from Step 1.

**Expected result:** Winning plan includes `IXSCAN` on `idx_orders_customer_date`. `totalDocsExamined` should not exceed a small multiple of `nReturned`. A sort stage should be unnecessary if the index order matches.

---

### Step 4 — Test a different query shape (PPT Exercise 4)

**Do this:** This query does **not** lead with `customerId`:

```javascript
db.orders.find({ fulfillmentStatus: "PROCESSING" })
  .sort({ createdAt: 1 })
  .explain("executionStats")
```

Then create a workload-specific index and explain again:

```javascript
db.orders.createIndex(
  { fulfillmentStatus: 1, createdAt: 1 },
  { name: "idx_orders_fulfillment_date" }
)

db.orders.find({ fulfillmentStatus: "PROCESSING" })
  .sort({ createdAt: 1 })
  .explain("executionStats")
```

**Expected result:** The customer-history index does not support this shape (leading field is `customerId`). After the second index, the PROCESSING query can `IXSCAN` `idx_orders_fulfillment_date`. Three PROCESSING orders exist on a fresh load (`O6202`, `O6302`, `O6401`).

---

### Step 5 — Multikey index on tags (PPT Exercise 5)

**Do this:**

```javascript
db.products.createIndex(
  { tags: 1 },
  { name: "idx_products_tags" }
)

db.products.find({ tags: "wireless" }).explain("executionStats")
db.products.find({ tags: "wireless" }, { sku: 1, tags: 1, _id: 0 })
```

**Expected result:** Plan is `IXSCAN` on `idx_products_tags`. Matching SKUs include `P1001` and `A410`. The index is **multikey** because `tags` is an array.

---

### Step 6 — Review all indexes (PPT Exercise 6)

**Do this:**

```javascript
db.products.getIndexes()
db.customers.getIndexes()
db.orders.getIndexes()
db.reviews.getIndexes()
```

For every non-`_id` index, write:

| Index | Query it supports | Sort? | Business rule? | Write cost | Redundant? |
|-------|-------------------|-------|----------------|------------|------------|
| | | | | | |

**Expected result:** You listed at least `sku` unique (products), `customerNumber` unique (customers), `orderNumber` unique (orders), plus the two indexes you created. Do **not** drop unique identity indexes.

---

## Success criteria

- [ ] Baseline `explain` recorded **before** creating `idx_orders_customer_date`
- [ ] History query uses `customerId` from `C101`, not a copied ObjectId
- [ ] Second query shape needed a different leading field
- [ ] Tags query used a multikey index
- [ ] Index inventory names a purpose for each extra index
