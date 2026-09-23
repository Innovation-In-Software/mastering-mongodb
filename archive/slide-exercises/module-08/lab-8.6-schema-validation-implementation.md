# Lab 8.6: Schema Validation Implementation

**Module 8:** MongoDB Best Practices, Security, and Troubleshooting  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 8)  
**Time:** 20 min  
**Difficulty:** Intermediate

**Objective:** Implement order validation on a scratch collection requiring orderNumber, customerId, nonempty items, permitted statuses, nonnegative Decimal128 total, and Date createdAt, then test valid and invalid inserts.

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

**Scratch database:** Labs that change validation, users, or restored data use `training_store_ops` so `training_store` stays intact for later work.

**Small-data note:** Twelve products and seventeen orders will not produce dramatic wall-clock wins. Record **plan shape**, **examined vs returned**, and **correctness**, not stopwatch time.


---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Create a scratch collection

**Do this:** Copy two paid orders into a new collection so production-shaped data exists without locking `orders`:

```javascript
use training_store_ops
db.orders_validated.drop()
db.getSiblingDB("training_store").orders.find({ paymentStatus: "PAID" }).limit(2).forEach(d => {
  delete d._id
  db.orders_validated.insertOne(d)
})
db.orders_validated.countDocuments()
```

**Expected result:** `training_store_ops.orders_validated` has two documents.

---

### Step 2 — Attach the validator

**Do this:** Run `collMod` (or `createCollection`) with `$jsonSchema` requiring `orderNumber` (string), `customerId` (objectId), `items` (array `minItems: 1`), `paymentStatus` enum `PAID`/`PENDING`/`FAILED`, `fulfillmentStatus` enum that matches your data, `total` decimal (or a number type you can justify), `createdAt` date. Use `validationAction: "error"`.

**Expected result:** `collMod` / create succeeds. `db.getCollectionInfos({ name: "orders_validated" })` shows the validator.

---

### Step 3 — Prove accept and reject

**Do this:** Insert one valid order (new `orderNumber`). Then attempt: missing `orderNumber`; `total: "9.99"`; `paymentStatus: "PAID_NOW"`. Record the error messages.

**Expected result:** Valid insert succeeds. Each invalid insert is rejected. Existing copied documents remain.

---

## Success criteria

- [ ] Validator is on `training_store_ops.orders_validated`
- [ ] One valid insert works
- [ ] Missing field, wrong type, and illegal status are rejected

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
