# Lab 6.6: Implement Data-Integrity Indexes

**Module 6:** Indexing and Query Performance  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 6)  
**Time:** 20 min  
**Difficulty:** Intermediate

**Objective:** Create unique indexes for SKU, customer number, and order number, then prove duplicate inserts fail.

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

### Step 1 — Unique SKU

**Do this:** If `idx_products_sku` exists, drop it first (MongoDB cannot keep two indexes on the same keys). Then:

```javascript
db.products.dropIndex("idx_products_sku")
db.products.createIndex(
  { sku: 1 },
  { unique: true, name: "uq_products_sku" }
)
```

**Expected result:** uq_products_sku exists with unique: true. dropIndex errors if the non-unique index was never created — that is fine; proceed to createIndex.

---

### Step 2 — Unique customer and order numbers

**Do this:** Run:

```javascript
db.customers.createIndex(
  { customerNumber: 1 },
  { unique: true, name: "uq_customers_customer_number" }
)
db.orders.createIndex(
  { orderNumber: 1 },
  { unique: true, name: "uq_orders_order_number" }
)
```

**Expected result:** Both unique indexes build because the loader has no duplicates.

---

### Step 3 — Attempt a duplicate SKU

**Do this:** Run:

```javascript
db.products.insertOne({
  sku: "L100",
  name: "Duplicate SKU test",
  category: "LAPTOP",
  price: Decimal128("1.00"),
  active: false,
  tags: ["temp"],
  createdAt: new Date()
})
```

**Expected result:** Duplicate key error (E11000) mentioning sku / uq_products_sku. The extra document is not inserted.

---

### Step 4 — Cleanup discussion

**Do this:** Write what you would do if unique creation failed because duplicates already existed.

**Expected result:** Find duplicates with a `$group` on the key having `$sum: 1` and `$match` count > 1, merge or delete extras, then retry createIndex. Do not skip uniqueness because the build failed once.

---



## Success criteria

- [ ] Three unique indexes exist
- [ ] A duplicate SKU insert is rejected
- [ ] A duplicate-cleanup approach is noted

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
