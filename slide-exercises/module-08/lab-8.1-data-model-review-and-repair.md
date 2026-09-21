# Lab 8.1: Data-Model Review and Repair

**Module 8:** MongoDB Best Practices, Security, and Troubleshooting  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 8)  
**Time:** 25 min  
**Difficulty:** Intermediate

**Objective:** Inspect training_store documents, identify inconsistent names and types, unbounded growth risks, and snapshot gaps, then propose validation and a migration note.

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

### Step 1 — Inspect types and names

**Do this:** Run and record field-name and type surprises:

```javascript
use training_store
db.products.find({}, { sku: 1, name: 1, price: 1, active: 1 }).limit(5)
db.products.find({ sku: "XBAD" }, { sku: 1, price: 1 })
db.products.aggregate([
  { $project: { sku: 1, priceType: { $type: "$price" } } }
])
```

**Expected result:** `XBAD` shows `price` as string. Healthy products show Decimal128. That mixed type is the catalog anti-pattern to repair.

---

### Step 2 — Check growth and snapshots

**Do this:** Compare `db.products.findOne({}, { reviews: 1, sku: 1 })` with `db.reviews.findOne()` and `db.orders.findOne({ orderNumber: "O5001" }, { items: 1, customerId: 1, shippingAddress: 1 })`. Note whether reviews are embedded and whether order items snapshot price.

**Expected result:** Reviews live in `reviews` (good). Orders embed line snapshots and reference `customerId` (good). Call out any missing snapshot fields you would still add (for example purchase-time product name if absent).

---

### Step 3 — Propose validation and migration

**Do this:** Write: (1) three validator rules for products, (2) what to do with `XBAD`, (3) whether to migrate in place or insert into a new collection first.

**Expected result:** Rules include sku string, Decimal128 price, Boolean active. `XBAD` is converted or quarantined. Prefer adding compatible fields and `validationAction: "warn"` or a staging collection before `error` on production data.

---

## Success criteria

- [ ] Mixed `price` types are documented
- [ ] Reviews are confirmed as a separate collection
- [ ] A migration note exists for `XBAD` and validation

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
