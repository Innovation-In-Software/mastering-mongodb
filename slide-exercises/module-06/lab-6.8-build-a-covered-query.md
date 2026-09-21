# Lab 6.8: Build a Covered Query

**Module 6:** Indexing and Query Performance  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 6)  
**Time:** 20 min  
**Difficulty:** Intermediate

**Objective:** Create a covering index and test a projection that can be satisfied from the index alone.

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

### Step 1 — Create the covering index

**Do this:** Run:

```javascript
db.products.createIndex(
  { category: 1, price: 1, name: 1 },
  { name: "idx_products_category_price_name" }
)
```

**Expected result:** Index exists. `_id` is not in this key.

---

### Step 2 — Query that can be covered

**Do this:** Run:

```javascript
db.products.find(
  { category: "BOOK" },
  { _id: 0, name: 1, price: 1 }
).explain("executionStats")
```

**Expected result:** Look for IXSCAN on idx_products_category_price_name and **no FETCH** (or a covering projection stage). totalDocsExamined is often 0 when covered.

---

### Step 3 — Break coverage

**Do this:** Re-explain the same filter with `{ name: 1, price: 1 }` ( `_id` included) and with `{ name: 1, tags: 1, _id: 0 }`.

**Expected result:** Including `_id` or tags should introduce FETCH / document examination.

---

### Step 4 — Write the rule

**Do this:** One sentence: when is this catalog projection covered, and how do you confirm?

**Expected result:** Covered when filter and output fields (including `_id` handling) live in the index; confirm with explain, not by guessing.

---



## Success criteria

- [ ] Covering index exists
- [ ] The `_id: 0` projection is tested
- [ ] A non-covered variant is contrasted

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
