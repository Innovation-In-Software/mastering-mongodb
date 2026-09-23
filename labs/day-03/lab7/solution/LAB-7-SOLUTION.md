# Lab 7 — Production Readiness — solution (instructor)

**Day 3** · Module 8 · Deck slide 48  
**Do not hand this sheet to participants.**

Guide: [`../LAB-7-GUIDE.md`](../LAB-7-GUIDE.md)

Expected outputs assume a **fresh load** of `datasets/training_store/load.js` on a standalone local `mongod`. Object ids, timings and exact explain layouts vary by version; the counts and values below do not.

---

## Step 0 — Reload and check tools

```text
Loaded training_store
customers: 6
products: 13
orders: 17
reviews: 6
paid orders: 13
Module 4 fixtures: XBAD string price; C204 phone null; C515 missing phone; O5001 elemMatch trap; O6401 L100 qty 2.
Do not insert sku A600, A610, A611, A612, A700, A800, A900, TEMP-100 — Module 4 labs create those.
```

`mongodump --version` / `mongorestore --version` print a Database Tools version (for example `100.x`). "Not recognized" means the learner does the written alternative in Step 4.

---

## Step 1 — Stop the catalog collection scan

Query output:

```text
{ sku: 'L100', name: 'Business Laptop', price: Decimal128('1299.99') }
{ sku: 'L110', name: 'Ultrabook', price: Decimal128('1899.99') }
```

L190 (Refurbished Laptop, 499.99) is `active: false` and is excluded. No `attributes` field is returned.

Explain on a fresh load (`products` has only `_id_` and `sku_unique`):

| Measure | Value |
| --- | --- |
| Winning plan | `SORT` (limit 20) over `COLLSCAN` — a projection stage may sit on top |
| `nReturned` | 2 |
| `totalKeysExamined` | 0 |
| `totalDocsExamined` | 13 |
| In-memory `SORT` | Yes |

Proposed index: `{ category: 1, active: 1, price: 1 }` — category (E), active (E), price (S). If the instructor allows it to be created:

| Measure | Value |
| --- | --- |
| Winning plan | `IXSCAN` on `category_1_active_1_price_1`, then `FETCH` |
| `nReturned` | 2 |
| `totalKeysExamined` | 2 |
| `totalDocsExamined` | 2 |
| `SORT` stage | None — the index delivers price order |

If Lab 5's `idx_products_tags` is still present it is **not** used — its leading field is `tags`. Learners must not drop existing indexes.

---

## Step 2 — Monthly paid-order pipeline

```text
{ _id: '2026-07', orderCount: 3, revenue: Decimal128('1835.95') }
{ _id: '2026-08', orderCount: 4, revenue: Decimal128('2731.92') }
{ _id: '2026-09', orderCount: 6, revenue: Decimal128('4550.57') }
```

Control: `db.orders.countDocuments({ paymentStatus: "PAID" })` → `13`. 3 + 4 + 6 = 13 orders; total paid revenue **9118.44**.

| Month | Paid orders |
| --- | --- |
| 2026-07 | O6101 1483.99, O6102 211.38, O6103 140.58 |
| 2026-08 | O6201 79.07, O6202 2146.99, O6203 154.88, O6204 350.98 |
| 2026-09 | O6301 1512.23, O6302 301.78, O6303 174.47, O6304 2146.99, O6305 71.77, O6306 343.33 |

The two PENDING orders O5001 and O6401, the PENDING orphan O6499 and the FAILED order O6402 are excluded.

Common wrong answer: `$unwind: "$items"` before summing `$total` turns 13 orders into 21 rows and reports **12119.25**. Line revenue, if asked, is `$multiply: ["$items.quantity", "$items.unitPrice"]` after the `$unwind` — never the order total. Month boundaries are UTC.

---

## Step 3 — Validator on a scratch collection

```text
use training_store_ops
switched to db training_store_ops

db.createCollection(...)
{ ok: 1 }

insertOne OPS-1
{ acknowledged: true, insertedId: ObjectId('...') }

insertOne OPS-BAD
MongoServerError: Document failed validation
```

The error is **code 121**. Its details (`errInfo.details.schemaRulesNotSatisfied`) show `properties` → `total` → `bsonType: 'decimal'`, reason `type did not match`, considered value `'10.00'` of type `string`.

`use training_store` then `db.orders.countDocuments({})` → **17**. The class data is unchanged.

---

## Step 4 — Restore to an isolated database

`mongodump` ends with lines like:

```text
done dumping training_store.orders (17 documents)
done dumping training_store.products (13 documents)
done dumping training_store.customers (6 documents)
done dumping training_store.reviews (6 documents)
```

`mongorestore` ends with:

```text
42 document(s) restored successfully. 0 document(s) failed to restore.
```

(A deprecation warning about `--db` with a directory path is harmless.)

Verification:

| Command | `training_store_restore` | `training_store` |
| --- | --- | --- |
| `db.products.countDocuments({})` | **13** | **13** |
| `db.orders.countDocuments({})` | 17 | 17 |
| `findOne({ orderNumber: "O5001" }, …)` | `{ orderNumber: 'O5001', paymentStatus: 'PENDING', total: Decimal128('1514.17') }` | — |
| `db.orders.getIndexes()` | `_id_` and `orderNumber_unique` (indexes are restored from the dump) | — |

The restore takes a few seconds on this data. That is the measured RTO for 42 documents — not for production volume.

**Written alternative** (no Database Tools): see the [Exercise 8.3 solution](../../exercises/solution/exercise-8.3-define-rpo-and-rto.md), Task 3 — counts, O5001 and a paid total, `getIndexes()`, an application read, and the time taken.

---

## Step 5 — Score go-live

**Classification: not ready.**

| Area | Status | Evidence |
| --- | --- | --- |
| Data model | Not ready | XBAD `price` is the string `"49.99"`; stray `legacyName` (L190) and `temporaryNote` (A410); no `stock` field; reviews would be unbounded if moved onto products |
| Queries and aggregation | Conditional | Step 1 and Step 2 are shaped correctly and checked against a control, but only on 17 orders |
| Indexes | Conditional | Proposed ESR index confirmed with explain on tiny data; Lab 5 leftovers not tied to named shapes |
| Security | Not ready | No authentication, no TLS, no roles on the class instance |
| Availability and recovery | Not ready | One server, not a replica set; the restore drill ran today for the first time, with no RPO / RTO agreed |
| Operations | Not ready | No metrics, alerts or runbooks |
| **Overall** | **Not ready** | A single not-ready area blocks the launch |

**Conditions for go-live:** typed money (convert XBAD with `$toDecimal` in a small verified update, then validate); authentication and TLS; least-privilege roles (Exercise 8.2); a scheduled restore drill measured against RPO and RTO (Exercise 8.3); a replica set; `explain` monitored on real volume.

Accept "ready with conditions" only for individual areas, never for the whole system in this state.

---

## Clean up

`training_store_ops` and `training_store_restore` can be dropped with `db.dropDatabase()` after the debrief. Never drop `training_store` — reload it with `load.js` instead.
