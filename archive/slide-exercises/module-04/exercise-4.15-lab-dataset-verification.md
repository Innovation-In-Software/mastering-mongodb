# Exercise 4.15: Lab 4.1 Dataset Verification

**Module 4:** The MongoDB Query Language  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 4)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Confirm `training_store` collections, counts, field paths, and BSON types before querying.

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

### Step 1 — Select the database

**Do this:** Run `use training_store`.

**Expected result:** The prompt shows `training_store`.

---

### Step 2 — List collections

**Do this:** Run `show collections`.

**Expected result:** `products`, `customers`, `orders`, and `reviews` are listed.

---

### Step 3 — Count each collection

**Do this:** Run:

```javascript
db.products.countDocuments({})
db.customers.countDocuments({})
db.orders.countDocuments({})
db.reviews.countDocuments({})
```

**Expected result:** On a fresh load: products 13, customers 6, orders 17, reviews 6. If you already inserted lab SKUs, counts are higher — note that.

---

### Step 4 — Inspect one document from each collection

**Do this:** Run `findOne()` on `products`, `customers`, `orders`, and `reviews`.

**Expected result:** You can point to nested objects and arrays on the samples.

---

### Step 5 — Record field paths and BSON types

**Do this:** On the product and order, list at least: `sku` (string), `price` (decimal), `tags` (array), `attributes.memoryGB` (int, if present), `items.sku`, `createdAt` (date).

**Expected result:** The observation sheet names paths with dotted notation and types. `XBAD.price` is a string — record that exception.

---

## Observation sheet

| Collection | Count | Nested path | Array | Notable type |
|------------|-------|-------------|-------|--------------|
| products | | | | |
| customers | | | | |
| orders | | | | |
| reviews | | | | |


## Success criteria

- [ ] Listed four collections
- [ ] Recorded counts
- [ ] Named at least one nested path and one array
- [ ] Noted Decimal128 vs the string-price exception

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
