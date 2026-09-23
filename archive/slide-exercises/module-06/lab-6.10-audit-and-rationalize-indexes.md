# Lab 6.10: Audit and Rationalize Indexes

**Module 6:** Indexing and Query Performance  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 6)  
**Time:** 25 min  
**Difficulty:** Intermediate

**Objective:** List indexes, spot overlapping prefixes, hide one candidate, test, unhide, and recommend retain/redesign/remove — without dropping a needed index.

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

### Step 1 — Inventory

**Do this:** Run for products, customers, orders, reviews, and sessions:

```javascript
db.getCollectionNames()
db.products.getIndexes()
db.orders.getIndexes()
db.products.aggregate([{ $indexStats: {} }])
```

**Expected result:** A table of indexes by collection. Usage counts may be low or zero depending on process uptime — interpret with that caveat.

---

### Step 2 — Spot overlap

**Do this:** On products, compare category-leading indexes (single-field category, category+active+price, category+price+name, partial category+price). Note prefix overlap.

**Expected result:** At least one overlapping prefix pair is written down.

---

### Step 3 — Hide and test

**Do this:** Hide a **non-unique, non-TTL** training index you suspect is redundant, for example `idx_products_category` if it exists:

```javascript
db.products.hideIndex("idx_products_category")
db.products.find({ category: "ACCESSORY" }).explain("queryPlanner")
db.products.unhideIndex("idx_products_category")
```

**Expected result:** While hidden, the planner should not select that index. After unhide, it is eligible again. If the name does not exist, hide another secondary index from your list — never hide `_id_`.

---

### Step 4 — Recommend

**Do this:** For the hidden candidate, write retain, redesign, or remove, with one evidence sentence. Do **not** drop it in this lab.

**Expected result:** A recommendation exists. No production-style drop was performed.

---



## Success criteria

- [ ] Indexes are grouped by collection
- [ ] One index was hidden and unhidden
- [ ] No required unique/TTL index was dropped

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
