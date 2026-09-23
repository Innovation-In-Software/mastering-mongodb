# Lab 5.1: Aggregation Dataset Verification

**Module 5:** The Aggregation Framework  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 5, Lesson 5.1)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Confirm `training_store` counts, field paths, BSON types, and arrays you will unwind.

---

## Environment basics (read this first)

**Demonstration environment:** Windows 10/11 · PowerShell in Cursor (``Ctrl+` ``) · `mongosh` connected to the training instance.

| Task | Windows | Where |
|------|---------|-------|
| Open folder | `Ctrl+K Ctrl+O` | File → Open Folder |
| Terminal | ``Ctrl+` `` → PowerShell | Bottom panel |
| MongoDB shell | `mongosh` | Same terminal |

Use the same connection string from Module 2. If counts are far below 6 customers / 12 products / 17 orders / 6 reviews, reload [`datasets/training_store/load.js`](../../datasets/training_store/load.js).

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Select the database and count

**Do this:** Run:

```javascript
use training_store
db.customers.countDocuments()
db.products.countDocuments()
db.orders.countDocuments()
db.reviews.countDocuments()
db.orders.countDocuments({ paymentStatus: "PAID" })
```

**Expected result:** 6, 12, 17, 6, and 13 paid orders. If not, reload `load.js`.

---

### Step 2 — Inspect one document of each type

**Do this:** Run `findOne` on products, orders, customers, and reviews. Record paths you will need: `price`, `items.sku`, `items.quantity`, `items.unitPrice`, `paymentStatus`, `fulfillmentStatus`, `total`, `createdAt`, `customerId`, `name.first`, `addresses.province`, `active`, `shippingFee`.

**Expected result:** Order `items` is an array of documents. `price` and `total` are Decimal128. `createdAt` is Date.

---

### Step 3 — Confirm types and arrays

**Do this:** Run:

```javascript
db.products.findOne({ sku: "L100" }).price
db.orders.findOne({ orderNumber: "O5001" }).createdAt
db.orders.findOne({ orderNumber: "O6201" }).shippingFee
```

**Expected result:** Price prints as Decimal128. `createdAt` is a Date. O6201 has no `shippingFee` — that missing field is intentional.

---

## Success criteria

- [ ] Counts match the loader
- [ ] You listed `items` as the unwind path
- [ ] You noted Decimal128 money and Date `createdAt`

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
