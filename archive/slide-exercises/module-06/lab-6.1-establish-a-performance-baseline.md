# Lab 6.1: Establish a Performance Baseline

**Module 6:** Indexing and Query Performance  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 6)  
**Time:** 20 min  
**Difficulty:** Beginner

**Objective:** Capture explain baselines for assigned queries without creating new indexes.

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

### Step 1 — Confirm the dataset

**Do this:** Run:

```javascript
use training_store
db.products.countDocuments()
db.orders.countDocuments()
db.products.getIndexes()
db.orders.getIndexes()
```

**Expected result:** About 12 products and 17 orders. Each collection should show the default `_id_` index. Note any extra indexes left from a demo.

---

### Step 2 — Explain the catalog query

**Do this:** Run and record winning stage, nReturned, totalKeysExamined, totalDocsExamined, and any SORT:

```javascript
db.products.find(
  { category: "ACCESSORY", active: true }
).sort({ price: 1 }).explain("executionStats")
```

**Expected result:** Likely COLLSCAN (unless a prior demo index remains). Record the numbers even if they are small.

---

### Step 3 — Explain order history

**Do this:** Replace `cid` with C101’s `_id` from `db.customers.findOne({ customerNumber: "C101" })`, then:

```javascript
db.orders.find({
  customerId: cid,
  paymentStatus: "PAID"
}).sort({ createdAt: -1 }).limit(10).explain("executionStats")
```

**Expected result:** A baseline row exists: filter, sort, projection (none), winning plan, counts, in-memory sort yes/no.

---

### Step 4 — Fill the baseline table

**Do this:** In notes, one row per query: filter, sort, projection, winning plan, nReturned, keys examined, docs examined, extra sort.

**Expected result:** Two completed rows. No new indexes created in this lab.

---



## Success criteria

- [ ] Dataset counts match the loader
- [ ] Two explain summaries are written down
- [ ] No createIndex was run in this lab

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
