# Lab 6.3: Design a Compound Index

**Module 6:** Indexing and Query Performance  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 6)  
**Time:** 25 min  
**Difficulty:** Intermediate

**Objective:** Build a compound index for active products by category sorted by price, then test prefix queries.

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

### Step 1 — Identify fields

**Do this:** For `find({ category: "ACCESSORY", active: true }).sort({ price: 1 })`, write equality vs sort fields and propose a key.

**Expected result:** Equality: category, active. Sort: price. Proposal `{ category: 1, active: 1, price: 1 }`.

---

### Step 2 — Create and explain

**Do this:** Run:

```javascript
db.products.createIndex(
  { category: 1, active: 1, price: 1 },
  { name: "idx_products_category_active_price" }
)
db.products.find({
  category: "ACCESSORY",
  active: true
}).sort({ price: 1 }).explain("executionStats")
```

**Expected result:** Winning index is the new compound index. Look for IXSCAN and no blocking SORT.

---

### Step 3 — Test a prefix query

**Do this:** Explain `db.products.find({ category: "LAPTOP" })` and `db.products.find({ active: true })`.

**Expected result:** Category-only can use the leading prefix. Active-only generally cannot.

---

### Step 4 — Record unsupported shapes

**Do this:** Write one query this index does **not** support well (for example sort by name, or filter only price).

**Expected result:** A concrete unsupported shape is written, with a one-line reason (prefix or sort mismatch).

---



## Success criteria

- [ ] Compound index exists with the intended name
- [ ] The target query uses that index
- [ ] A prefix success and a prefix failure are noted

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
