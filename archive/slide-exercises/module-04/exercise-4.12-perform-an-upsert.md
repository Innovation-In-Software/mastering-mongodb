# Exercise 4.12: Perform an Upsert

**Module 4:** The MongoDB Query Language  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 4)  
**Time:** 10 min  
**Difficulty:** Intermediate

**Objective:** Upsert a product by SKU so `createdAt` is set only on insert and `updatedAt` is always set.

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

### Step 1 — Run the upsert for a new SKU

**Do this:** Run:

```javascript
db.products.updateOne(
  { sku: "A700" },
  {
    $set: {
      name: "Portable Charger",
      category: "ACCESSORY",
      price: Decimal128("39.99"),
      active: true,
      updatedAt: new Date()
    },
    $setOnInsert: { createdAt: new Date(), stockQuantity: 25 }
  },
  { upsert: true }
)
```

**Expected result:** `upsertedId` is present. `createdAt` exists.

---

### Step 2 — Inspect the inserted document

**Do this:** Run:

```javascript
db.products.findOne({ sku: "A700" })
```

**Expected result:** Fields from `$set` and `$setOnInsert` are present. Filter used the unique `sku`.

---

### Step 3 — Run the same upsert again

**Do this:** Repeat the `updateOne` from Step 1, then `findOne` again.

**Expected result:** `matchedCount: 1`, `modifiedCount` may be 1 because `updatedAt` changes. `createdAt` must be **unchanged**. `upsertedId` is absent.

---

### Step 4 — Compare insert vs update outcomes

**Do this:** Write two bullets: first-run result vs second-run result.

**Expected result:** First run inserts; second run updates. `$setOnInsert` does not overwrite `createdAt`.

---



## Success criteria

- [ ] Used a unique SKU filter
- [ ] Set `createdAt` only on insert
- [ ] Compared both runs' write results

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
