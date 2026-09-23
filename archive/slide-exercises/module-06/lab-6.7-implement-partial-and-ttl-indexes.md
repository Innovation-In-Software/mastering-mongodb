# Lab 6.7: Implement Partial and TTL Indexes

**Module 6:** Indexing and Query Performance  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 6)  
**Time:** 25 min  
**Difficulty:** Intermediate

**Objective:** Create a partial index for active products and a TTL index on a dedicated sessions collection.

---

## Environment basics (read this first)

**Demonstration environment:** Windows 10/11 · PowerShell in Cursor (``Ctrl+` ``) · `mongosh` connected to the training instance.

| Task | Windows | Where |
|------|---------|-------|
| Open folder | `Ctrl+K Ctrl+O` | File → Open Folder |
| Terminal | ``Ctrl+` `` → PowerShell | Bottom panel |
| MongoDB shell | `mongosh` | Same terminal |

**Prerequisite:** `training_store` is loaded from [`datasets/training_store/load.js`](../../datasets/training_store/load.js). Reload at the start of Day 3 if Day 2 writes remain.

```javascript
use training_store
```

**Small-data note:** Twelve products and seventeen orders will not produce dramatic wall-clock wins. Record the **plan** (`COLLSCAN` vs `IXSCAN`), **index name**, and **examined vs returned** counts. That is the teaching signal.


---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Partial index

**Do this:** Run:

```javascript
db.products.createIndex(
  { category: 1, price: 1 },
  {
    partialFilterExpression: { active: true },
    name: "idx_active_products_category_price"
  }
)
db.products.getIndexes()
```

**Expected result:** The index lists partialFilterExpression `{ active: true }`.

---

### Step 2 — Compatible vs incompatible query

**Do this:** Explain both:

```javascript
db.products.find({ category: "LAPTOP", active: true, price: { $lte: Decimal128("2000.00") } }).explain("executionStats")
db.products.find({ category: "LAPTOP", price: { $lte: Decimal128("2000.00") } }).explain("executionStats")
```

**Expected result:** The query that includes `active: true` can use the partial index. The query that omits it typically will not, because inactive laptops (L190) are not in that index.

---

### Step 3 — Create sessions and TTL

**Do this:** Run:

```javascript
db.sessions.drop()
db.sessions.insertMany([
  { sessionId: "S1", user: "aisha", expiresAt: new Date(Date.now() + 60 * 60 * 1000) },
  { sessionId: "S-EXPIRED", user: "temp", expiresAt: new Date(Date.now() - 60 * 1000) }
])
db.sessions.createIndex(
  { expiresAt: 1 },
  { expireAfterSeconds: 0, name: "ttl_sessions_expires_at" }
)
db.sessions.getIndexes()
```

**Expected result:** ttl_sessions_expires_at exists with expireAfterSeconds: 0. Two documents are present immediately after insert.

---

### Step 4 — Observe asynchronous expiration

**Do this:** Wait about 60 seconds (TTL monitor interval), then `db.sessions.find()`. Do not block the class if the expired row is still there — record that expiration is asynchronous.

**Expected result:** S-EXPIRED may disappear after the TTL thread runs. The lab succeeds if the index is configured correctly even if the delete has not fired yet. Never treat TTL as a real-time guarantee.

---



## Success criteria

- [ ] Partial filter is visible on the product index
- [ ] A compatible query is distinguished from an incompatible one
- [ ] TTL index is created on sessions.expiresAt
- [ ] Asynchronous cleanup is stated

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
