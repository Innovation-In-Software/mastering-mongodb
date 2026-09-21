# Lab 6.11: Integrated Query-Tuning Challenge

**Module 6:** Indexing and Query Performance  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 6)  
**Time:** 40–45 min  
**Difficulty:** Intermediate

**Objective:** Tune the product-catalog page and customer-order-history page using baselines, ESR, explain, and a write-cost note.

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

### Step 1 — Capture both shapes

**Do this:** Catalog: active products, category ACCESSORY, optional price ≤ 100, sort price, return name, price, category. History: C101, PAID, newest first, createdAt ≥ 2026-08-01, limit 20. Write both queries.

**Expected result:** Two complete mongosh queries including projection and limit.

---

### Step 2 — Baselines

**Do this:** explain("executionStats") both queries before changing indexes. Fill nReturned, keys, docs, SORT yes/no.

**Expected result:** Two baseline rows. Existing indexes from earlier labs are allowed; note them.

---

### Step 3 — Propose and create ESR indexes

**Do this:** Catalog candidate `{ category: 1, active: 1, price: 1 }` (may already exist). History candidate `{ customerId: 1, paymentStatus: 1, createdAt: -1 }` or `{ customerId: 1, createdAt: -1 }` depending on whether PAID is always present. Create any missing named indexes.

**Expected result:** Indexes exist. Field order is written with equality, sort, and range labeled.

---

### Step 4 — Re-explain and compare

**Do this:** Rerun both explains. Compare examined vs returned. For the catalog projection, optionally exclude `_id` and extra fields and note coverage.

**Expected result:** IXSCAN on the intended indexes. Examined counts are closer to returned counts than the baseline, or SORT is gone.

---

### Step 5 — Cost and recommendation

**Do this:** List the indexes you would keep for these two pages, their write/storage impact, and one index you would **not** add.

**Expected result:** A short recommendation: keep the two (or three) named indexes; do not index every catalog field; unique SKU remains a separate integrity index.

---



## Success criteria

- [ ] Both query shapes are written
- [ ] Before and after explain stats exist
- [ ] ESR field order is justified
- [ ] Write/storage impact is mentioned

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
