# Lab 5 solution — Index and Explain (instructor)

**Day 3** · Module 6 · Deck slide 49  
Instructor reference. **Do not hand this sheet to participants.** Participants work from [`../LAB-5-GUIDE.md`](../LAB-5-GUIDE.md).

Every number below is computed from a fresh `datasets/training_store/load.js` (13 products, 6 customers, 17 orders, 6 reviews; 13 PAID orders) with the steps run in order. `explain()` output is trimmed to the fields learners record. On MongoDB 7.0+ the stages may sit under `queryPlanner.winningPlan.queryPlan`; the stage names and counts are the same.

Legend: **keys · docs · returned** = `totalKeysExamined` · `totalDocsExamined` · `nReturned`.

---

## Before you start

```text
Loaded training_store
customers: 6
products: 13
orders: 17
reviews: 6
paid orders: 13
```

```javascript
db.products.getIndexes().map(i => i.name)   // [ '_id_', 'sku_unique' ]
db.customers.getIndexes().map(i => i.name)  // [ '_id_', 'customerNumber_unique', 'email_unique' ]
db.orders.getIndexes().map(i => i.name)     // [ '_id_', 'orderNumber_unique' ]
db.reviews.getIndexes().map(i => i.name)    // [ '_id_' ]
```

`var cid = db.customers.findOne({ customerNumber: "C101" })._id` — Aisha Khan. The ObjectId differs on every load; that is why nobody copies it from a slide.

---

## Core steps

### Step 1 — Baseline

```text
winningPlan:
  stage: 'SORT'
  sortPattern: { createdAt: -1 }
  inputStage:
    stage: 'COLLSCAN'
    filter: { customerId: { '$eq': ObjectId('…') } }
executionStats:
  nReturned: 5
  totalKeysExamined: 0
  totalDocsExamined: 17
```

Summary: `SORT <- COLLSCAN` · 0 · 17 · 5 · SORT **yes**.

Orders, newest first:

| orderNumber | createdAt |
| --- | --- |
| O5001 | 2026-09-20T14:30:00Z |
| O6306 | 2026-09-16T14:10:00Z |
| O6301 | 2026-09-03T10:15:00Z |
| O6201 | 2026-08-04T09:40:00Z |
| O6101 | 2026-07-08T14:00:00Z |

Acceptable variant: an `_id_` index scan with a `FETCH` and a `SORT` on some versions. Either way the history index is missing.

### Step 2 — Create the history index

```text
idx_orders_customer_date
```

`mongosh` prints the name (not `{ ok: 1 }`).

### Step 3 — Measure again

```text
winningPlan:
  stage: 'FETCH'
  inputStage:
    stage: 'IXSCAN'
    keyPattern: { customerId: 1, createdAt: -1 }
    indexName: 'idx_orders_customer_date'
    direction: 'forward'
executionStats:
  nReturned: 5
  totalKeysExamined: 5
  totalDocsExamined: 5
```

Summary: `FETCH <- IXSCAN idx_orders_customer_date` · 5 · 5 · 5 · SORT **no**.

### Step 4 — PROCESSING orders

| | Plan | keys · docs · returned |
| --- | --- | --- |
| Before | `SORT <- COLLSCAN` | 0 · 17 · 3 |
| `createIndex` | prints `idx_orders_fulfillment_date` | |
| After | `FETCH <- IXSCAN idx_orders_fulfillment_date` | 3 · 3 · 3, no SORT |

Queue, oldest first: **O6202** (2026-08-11, C412), **O6302** (2026-09-07, C204), **O6401** (2026-09-18, C204).

Why the history index can't help: its first field is `customerId` and this query has no `customerId` filter, so `fulfillmentStatus` is not a prefix.

### Step 5 — Multikey tags

```text
winningPlan:
  stage: 'FETCH'
  inputStage:
    stage: 'IXSCAN'
    keyPattern: { tags: 1 }
    indexName: 'idx_products_tags'
    isMultiKey: true
    multiKeyPaths: { tags: [ 'tags' ] }
executionStats:
  nReturned: 2
  totalKeysExamined: 2
  totalDocsExamined: 2
```

```javascript
[
  { sku: 'P1001', name: 'Wireless Keyboard', tags: [ 'wireless', 'accessories' ] },
  { sku: 'A410',  name: 'Wireless Mouse',    tags: [ 'wireless', 'accessories' ] }
]
```

`tags: "technology"` → `[ { sku: 'B300', name: 'MongoDB Fundamentals' } ]`.

`db.products.validate().keysPerIndex` → `{ _id_: 13, sku_unique: 13, idx_products_tags: 26 }`. 26 = 2 keys for each of 11 products + 3 for L190 + 1 for XBAD.

### Step 6 — Inventory

| Collection | Index | Key | Supports | Sort? | Business rule? | Redundant? |
| --- | --- | --- | --- | --- | --- | --- |
| products | `sku_unique` | `{ sku: 1 }` | SKU lookup | — | Yes: one SKU per product | No |
| products | `idx_products_tags` | `{ tags: 1 }` (multikey) | tag search | — | No | No |
| customers | `customerNumber_unique` | `{ customerNumber: 1 }` | customer-number lookup | — | Yes | No |
| customers | `email_unique` | `{ "contact.email": 1 }` | email lookup / login | — | Yes: one email per customer | No |
| orders | `orderNumber_unique` | `{ orderNumber: 1 }` | order-number lookup | — | Yes | No |
| orders | `idx_orders_customer_date` | `{ customerId: 1, createdAt: -1 }` | order history | Yes, newest first | No | No |
| orders | `idx_orders_fulfillment_date` | `{ fulfillmentStatus: 1, createdAt: 1 }` | fulfillment queue | Yes, oldest first | No | No |

Four unique identity indexes from `load.js` + three created in the lab. `reviews`: `_id_` only. Write cost: an order insert now maintains four indexes, a product insert three (the tags index usually two keys per product).

---

## Go further

### Step 7 — Catalog index and prefixes

| Query | Plan | keys · docs · returned |
| --- | --- | --- |
| ACCESSORY + active, sort price — before | `SORT <- COLLSCAN` | 0 · 13 · 5 |
| same — after `idx_products_category_active_price` | `FETCH <- IXSCAN idx_products_category_active_price` | 5 · 5 · 5, no SORT |
| `{ category: "LAPTOP" }` | `FETCH <- IXSCAN idx_products_category_active_price` | 3 · 3 · 3 |
| `{ active: true }` | `COLLSCAN` | 0 · 13 · 12 |

Result order: A410 Wireless Mouse 19.99 · A400 USB Hub 24.99 · P1001 Wireless Keyboard 49.99 · A500 Docking Station 249.99 · XBAD Legacy Cable Pack `"49.99"` (string, sorts after all numbers).

Unsupported shapes: `{ price: { $lt: 50 } }` alone (skips the leading `category`), `sort({ name: 1 })` (not in the index → SORT).

### Step 8 — Nested field and date range

| Query | Plan | keys · docs · returned |
| --- | --- | --- |
| `{ "contact.email": "aisha@example.com" }` | `FETCH <- IXSCAN email_unique` (8.0: `EXPRESS_IXSCAN`) | 1 · 1 · 1 |
| C101, `createdAt ≥ 2026-08-01`, sort desc, limit 10 | `LIMIT <- FETCH <- IXSCAN idx_orders_customer_date` (the limit may be folded into the plan) | 4 · 4 · 4 |
| same, hinted to `idx_orders_created_customer` | `LIMIT <- FETCH <- IXSCAN idx_orders_created_customer` | well above 4 keys (the 14 orders since 1 Aug, all customers) · 4 · 4 |

Date-range result: O5001, O6306, O6301, O6201.

`createIndex({ "contact.email": 1 }, { name: "idx_customers_contact_email" })` → `MongoServerError: Index already exists with a different name: email_unique`. This is the correction to the older Lab 6.5, which tried to create it.

### Step 9 — Unique SKUs

```text
db.products.dropIndex("sku_unique")          → { nIndexesWas: 4, ok: 1 }
db.products.createIndex({ sku: 1 }, …)       → uq_products_sku
db.products.insertOne({ sku: "L100", … })    →
  MongoServerError: E11000 duplicate key error collection: training_store.products
  index: uq_products_sku dup key: { sku: "L100" }
db.products.countDocuments()                 → 13
```

`nIndexesWas: 4` = `_id_`, `sku_unique`, `idx_products_tags`, `idx_products_category_active_price`.

Customer and order numbers: already `customerNumber_unique` and `orderNumber_unique`. Creating `uq_customers_customer_number` or `uq_orders_order_number` fails with *Index already exists with a different name*.

Cleanup answer:

```javascript
db.products.aggregate([
  { $group: { _id: "$sku", n: { $sum: 1 }, ids: { $push: "$_id" } } },
  { $match: { n: { $gt: 1 } } }
])
```

Merge or delete the extras, then build the unique index again. Never skip uniqueness because the first build failed.

### Step 10 — Partial and TTL

```text
db.products.validate().keysPerIndex
{ _id_: 13, idx_products_tags: 26, idx_products_category_active_price: 13,
  uq_products_sku: 13, idx_active_products_category_price: 12 }
```

| Query | Plan | Returned |
| --- | --- | --- |
| LAPTOP + `active: true` + price ≤ 2000, hinted to the partial index | `FETCH <- IXSCAN idx_active_products_category_price` · 2 keys · 2 docs | 2 — L100 Business Laptop, L110 Ultrabook |
| LAPTOP + price ≤ 2000, no `active` | `FETCH <- IXSCAN idx_products_category_active_price` | 3 — L190 499.99, L100 1299.99, L110 1899.99 |
| same, hinted to the partial index | error: the hint does not correspond to a usable index | — |

TTL:

```text
db.sessions.createIndex(…)  → ttl_sessions_expires_at
db.sessions.getIndexes()    →
  [ { v: 2, key: { _id: 1 }, name: '_id_' },
    { v: 2, key: { expiresAt: 1 }, name: 'ttl_sessions_expires_at', expireAfterSeconds: 0 } ]
db.sessions.countDocuments()  → 2      (immediately)
db.sessions.find({}, { _id: 0, sessionId: 1 })  → [ { sessionId: 'S1' } ]   (after the TTL monitor runs)
```

### Step 11 — Covered query

| Projection | Plan | keys · docs · returned |
| --- | --- | --- |
| `{ _id: 0, name: 1, price: 1 }` | `PROJECTION_COVERED <- IXSCAN idx_products_category_price_name` | 2 · **0** · 2 |
| `{ name: 1, price: 1 }` | `PROJECTION_SIMPLE <- FETCH <- IXSCAN` | 2 · 2 · 2 |
| `{ _id: 0, name: 1, tags: 1 }` | `PROJECTION_SIMPLE <- FETCH <- IXSCAN` | 2 · 2 · 2 |

Covered result: `{ name: 'Query Cookbook', price: Decimal128('39.99') }`, then `{ name: 'MongoDB Fundamentals', price: Decimal128('59.99') }`.

Rule sentence: "Covered when the filter and every returned field are in the index and `_id` is excluded — confirmed by `PROJECTION_COVERED` and `totalDocsExamined: 0`."

### Step 12 — Aggregation

| | Cursor stage | keys · docs |
| --- | --- | --- |
| Before | `COLLSCAN` (with `SORT`; `GROUP` on top on 7.0+) | 0 · 17 |
| `createIndex` | prints `idx_orders_payment_created` | |
| After | `IXSCAN idx_orders_payment_created` (no `SORT`) | 13 · 13 |

```javascript
[
  { _id: 'SHIPPED',    revenue: Decimal128('3809.48'), orderCount: 6 },
  { _id: 'DELIVERED',  revenue: Decimal128('2788.42'), orderCount: 4 },
  { _id: 'PROCESSING', revenue: Decimal128('2448.77'), orderCount: 2 },
  { _id: 'NEW',        revenue: Decimal128('71.77'),   orderCount: 1 }
]
```

Group order may vary. Check: 6 + 4 + 2 + 1 = 13 PAID orders; revenue total 9118.44.

- SHIPPED: O6101, O6103, O6203, O6301, O6303, O6306
- DELIVERED: O6102, O6201, O6204, O6304
- PROCESSING: O6202, O6302
- NEW: O6305

Remaining work: `$group` and its accumulators still process all 13 matched documents.

### Step 13 — Audit

```javascript
db.products.getIndexes().map(i => i.name)
[ '_id_', 'idx_products_tags', 'idx_products_category_active_price',
  'uq_products_sku', 'idx_active_products_category_price',
  'idx_products_category_price_name' ]
```

Collections: `customers`, `orders`, `products`, `reviews`, `sessions` (order may vary).

Overlap: `idx_products_category_active_price`, `idx_active_products_category_price` and `idx_products_category_price_name` all lead with `category`.

While `idx_products_category_active_price` is hidden, `find({ category: "ACCESSORY" }).explain("queryPlanner")` shows `FETCH <- IXSCAN idx_products_category_price_name`. The partial index is not a candidate (no `active: true` in the filter). After `unhideIndex` either category-leading index may win.

`$indexStats`: `ops` values depend on what each learner ran and on server uptime — only check that they read `accesses.ops` and `accesses.since`, and that nobody treats a zero as an instruction to drop.

Model recommendation: **retain** `idx_products_category_active_price` (serves the catalog browse with 5 : 5 : 5 and no SORT); **review** `idx_active_products_category_price` — it duplicates the same job for active-only queries; keep one of the two, not both, after measuring. No drop in the lab.

---

## Optional stretch — model answer

- **Catalog page** (`_id: 0`, `name`, `price`, `category`): not covered by any lab index — `idx_products_category_price_name` lacks `active`, and `idx_products_category_active_price` lacks `name`. Covering it would need `{ category: 1, active: 1, price: 1, name: 1 }`; usually not worth a fourth category-leading index.
- **History page** (C101, PAID, since 1 Aug, limit 20): with `idx_orders_customer_date` → 4 keys · 4 docs · 3 returned (O6306, O6301, O6201; O5001 is PENDING). `{ customerId: 1, paymentStatus: 1, createdAt: -1 }` would give 3 · 3 · 3 — only worth it if PAID is always in the filter.
- **Keep:** `idx_products_category_active_price`, `idx_orders_customer_date`, the unique identity indexes. **Don't add:** an index on every catalog field, or a single `{ category: 1 }`.

---

## What changed versus the archived guides

- One history-index name, `idx_orders_customer_date` (the old Lab 6.4 used `idx_orders_customer_created`).
- The old module labs 6.1–6.11 are Steps 7–13 and the stretch, on the same data and in one sequence.
- 13 products (including XBAD), not twelve; `load.js` already builds four unique indexes, so no collection starts with only `_id_`.
- No second index on `sku`, `contact.email`, `customerNumber` or `orderNumber` under a new name; `sku_unique` is dropped before `uq_products_sku`.
- Multikey is read from `explain()` (`isMultiKey`), not from `getIndexes()`.
- The inventory lists three created indexes, not two.
