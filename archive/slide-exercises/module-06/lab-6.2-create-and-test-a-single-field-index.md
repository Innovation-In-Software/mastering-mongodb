# Lab 6.2: Create and Test a Single-Field Index

**Module 6:** Indexing and Query Performance  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 6)  
**Time:** 20 min  
**Difficulty:** Beginner

**Objective:** Index product SKU and compare explain output before and after.

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

### Step 1 — Baseline SKU lookup

**Do this:** Run:

```javascript
db.products.find({ sku: "L100" }).explain("executionStats")
```

**Expected result:** Record winning stage and examined counts. Expect COLLSCAN unless an earlier SKU index exists.

---

### Step 2 — Create the index

**Do this:** Run:

```javascript
db.products.createIndex(
  { sku: 1 },
  { name: "idx_products_sku" }
)
db.products.getIndexes()
```

**Expected result:** The index list includes `idx_products_sku` with key `{ sku: 1 }`.

---

### Step 3 — Re-explain

**Do this:** Repeat the L100 find explain. Confirm the winning index name.

**Expected result:** IXSCAN on idx_products_sku. Keys and docs examined should be near 1, nReturned 1.

---

### Step 4 — Tradeoff note

**Do this:** Write one sentence: what write and storage cost did you add, and which query shape it serves.

**Expected result:** Each product insert/update of sku maintains this index. It serves equality lookup by SKU.

---



## Success criteria

- [ ] Before and after explain numbers are recorded
- [ ] getIndexes shows idx_products_sku
- [ ] A write-cost sentence exists

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
