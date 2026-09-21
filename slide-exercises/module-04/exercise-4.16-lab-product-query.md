# Exercise 4.16: Lab 4.2 Product Query Lab

**Module 4:** The MongoDB Query Language  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 4)  
**Time:** 30 min  
**Difficulty:** Intermediate

**Objective:** Build ten product queries covering equality, range, nested fields, tags, missing fields, types, sort, and distinct.

---

## Environment basics (read this first)

**Demonstration environment:** Windows 10/11 · PowerShell in Cursor (``Ctrl+` ``) · `mongosh` connected to the training instance.

| Task | Windows | Where |
|------|---------|-------|
| Open folder | `Ctrl+K Ctrl+O` | File → Open Folder |
| Terminal | ``Ctrl+` `` → PowerShell | Bottom panel |
| MongoDB shell | `mongosh` | Same terminal |

**Prerequisite:** `training_store` is loaded from [`datasets/training_store/load.js`](../../datasets/training_store/load.js). If writes from an earlier lab remain, reload that script unless the exercise says otherwise.

```javascript
use training_store
```


---

## Steps from the training slides

Follow these steps in order.

### Step 1 — All active products

**Do this:** Write and run a filter on `active: true`.

**Expected result:** Inactive SKU `L190` is absent.

---

### Step 2 — Specified category

**Do this:** Find `{ category: "LAPTOP" }`.

**Expected result:** Three laptops: `L100`, `L110`, `L190`.

---

### Step 3 — Price range

**Do this:** Find price `$gte` 50 and `$lte` 150 as Decimal128.

**Expected result:** Includes `S200`, `S210`, `B300`.

---

### Step 4 — Any of several categories

**Do this:** Use `$in: ["BOOK", "ACCESSORY"]`.

**Expected result:** Books and accessories, not laptops or shoes.

---

### Step 5 — Nested hardware attribute

**Do this:** Find `{ "attributes.memoryGB": { $gte: 16 } }`.

**Expected result:** `L100` (16) and `L110` (32). `L190` has 8 GB.

---

### Step 6 — Selected tags

**Do this:** Use `$all: ["database", "technology"]`.

**Expected result:** `B300`.

---

### Step 7 — Missing optional field

**Do this:** Find `{ discountPrice: { $exists: false } }`.

**Expected result:** Most products; `P1001` and `B310` are excluded.

---

### Step 8 — Inconsistent price types

**Do this:** Find `{ price: { $type: "string" } }`.

**Expected result:** `XBAD` only.

---

### Step 9 — Five most expensive active

**Do this:** Filter active, sort price descending with `_id` tiebreaker, limit 5, project name and price.

**Expected result:** Top of the list is `L110` at 1899.99.

---

### Step 10 — Distinct categories

**Do this:** Run `db.products.distinct("category")`.

**Expected result:** Array including `ACCESSORY`, `BOOK`, `LAPTOP`, `SHOE`.

---



## Success criteria

- [ ] Completed all ten queries
- [ ] Used Decimal128 for price ranges
- [ ] Quoted dotted paths
- [ ] Saved or can re-run each query

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
