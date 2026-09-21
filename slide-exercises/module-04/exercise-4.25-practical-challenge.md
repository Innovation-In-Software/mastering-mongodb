# Exercise 4.25: Module 4 Practical Challenge

**Module 4:** The MongoDB Query Language  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 4)  
**Time:** 30–45 min  
**Difficulty:** Intermediate

**Objective:** Turn business requests into a verified query script with safety controls.

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

### Step 1 — Find and project

**Do this:** Find active products priced below Decimal128("80.00"). Project name, category, price, no `_id`. Record the count.

**Expected result:** A saved query plus the list you got.

---

### Step 2 — Upsert a product

**Do this:** Upsert sku `A900` (or a SKU the instructor assigns) with `$set` + `$setOnInsert` createdAt.

**Expected result:** Write result shows insert or update depending on prior labs.

---

### Step 3 — Unique tags and inventory

**Do this:** `$addToSet` two tags; `$inc` stockQuantity.

**Expected result:** `modifiedCount` interpreted correctly on a second run.

---

### Step 4 — Find orders containing a product

**Do this:** Query `items.sku` for L100 (or the new SKU if ordered).

**Expected result:** Matching order numbers listed.

---

### Step 5 — Update matching item quantity and order status

**Do this:** Use `$elemMatch` or positional `$` to change quantity; `$set` status from NEW to PROCESSING on a test order only.

**Expected result:** You previewed the order filter first.

---

### Step 6 — Deactivate discontinued and remove test orders

**Do this:** updateMany discontinued → active false after preview. deleteMany only TEMP- or lab order numbers after count.

**Expected result:** Safety controls are written beside each write: filter, count, deletedCount.

---

### Step 7 — Assemble the deliverable

**Do this:** One mongosh script, expected results, write counts, before/after evidence, and a short safety paragraph.

**Expected result:** A teammate could replay the script on a reloaded `training_store`.

---



## Success criteria

- [ ] Accurate filters and BSON types
- [ ] Safe updates and deletes with previews
- [ ] Correct array handling
- [ ] Result verification for every write

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
