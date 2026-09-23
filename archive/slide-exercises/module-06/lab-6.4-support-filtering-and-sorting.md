# Lab 6.4: Support Filtering and Sorting

**Module 6:** Indexing and Query Performance  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 6)  
**Time:** 25 min  
**Difficulty:** Intermediate

**Objective:** Compare compound-index orders for a customer’s newest orders in a date range, limited to ten.

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

### Step 1 — Write the query

**Do this:** Using C101’s `_id` as `cid` and a start date of `ISODate("2026-08-01T00:00:00Z")`:

```javascript
db.orders.find({
  customerId: cid,
  createdAt: { $gte: ISODate("2026-08-01T00:00:00Z") }
}).sort({ createdAt: -1 }).limit(10)
```
Explain it before adding an orders index (besides `_id`).

**Expected result:** Baseline plan recorded. Equality customerId, sort/range createdAt.

---

### Step 2 — Create the ESR-aligned index

**Do this:** Run:

```javascript
db.orders.createIndex(
  { customerId: 1, createdAt: -1 },
  { name: "idx_orders_customer_created" }
)
```
Re-explain the query.

**Expected result:** IXSCAN on idx_orders_customer_created. Sort should be satisfied by the index.

---

### Step 3 — Compare a worse order

**Do this:** Create `{ createdAt: -1, customerId: 1 }` as `idx_orders_created_customer` only if you have time, explain the same query, then drop that experimental index.

**Expected result:** Leading with the range/sort field scans more keys across customers. Evidence favors customerId first. Drop the experimental index.

---

### Step 4 — Choose and document

**Do this:** Keep idx_orders_customer_created. Write why ESR put equality first here.

**Expected result:** A short justification: one customer’s keys are contiguous, then dates are ordered for newest-first and the range.

---



## Success criteria

- [ ] The customer+createdAt index exists
- [ ] Explain shows IXSCAN for the history query
- [ ] A worse field order is rejected with evidence or reasoning

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
