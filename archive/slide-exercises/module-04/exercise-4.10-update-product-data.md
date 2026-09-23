# Exercise 4.10: Update Product Data

**Module 4:** The MongoDB Query Language  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 4)  
**Time:** 15 min  
**Difficulty:** Intermediate

**Objective:** Use `$set`, `$inc`, `$rename`, `$unset`, and a filtered `updateMany`.

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

### Step 1 — Preview then change a price

**Do this:** Run the filter first, then:

```javascript
db.products.find({ sku: "A620" })
db.products.updateOne(
  { sku: "A620" },
  { $set: { price: Decimal128("64.99"), updatedAt: new Date() } }
)
```

**Expected result:** `matchedCount: 1`, `modifiedCount: 1` if the price changed. If A620 is missing, complete Exercise 4.9 first.

---

### Step 2 — Add a nested warranty field

**Do this:** Run:

```javascript
db.products.updateOne(
  { sku: "L100" },
  { $set: { "attributes.warrantyYears": 2 } }
)
```

**Expected result:** `attributes` still contains `memoryGB`. The warranty field is added beside it.

---

### Step 3 — Increase inventory

**Do this:** Run:

```javascript
db.products.updateOne({ sku: "L100" }, { $inc: { stockQuantity: 5 } })
```

**Expected result:** `stockQuantity` increases by 5 (from 8 to 13 on a fresh load).

---

### Step 4 — Rename an incorrect field

**Do this:** Run:

```javascript
db.products.updateMany(
  { legacyName: { $exists: true } },
  { $rename: { legacyName: "catalogName" } }
)
```

**Expected result:** `L190` now has `catalogName` instead of `legacyName`.

---

### Step 5 — Remove a temporary field and deactivate discontinued

**Do this:** Run:

```javascript
db.products.updateOne({ sku: "A410" }, { $unset: { temporaryNote: "" } })
db.products.updateMany(
  { tags: "discontinued" },
  { $set: { active: false } }
)
```

**Expected result:** `A410` no longer has `temporaryNote`. Discontinued items stay inactive. Preview `updateMany` with `find` before running it in production.

---



## Success criteria

- [ ] Previewed filters with `find()` before `updateMany`
- [ ] Used dotted `$set` for nested warranty
- [ ] Interpreted `matchedCount` vs `modifiedCount`

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
