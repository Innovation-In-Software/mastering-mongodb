# Exercise 4.20: Lab 4.6 Update Operations Lab

**Module 4:** The MongoDB Query Language  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 4)  
**Time:** 30 min  
**Difficulty:** Intermediate

**Objective:** Practice `$set`, `$unset`, `$inc`, `$min`, `$max`, `$rename`, nested updates, and `updateMany` with the preview-update-verify loop.

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

### Step 1 — Preview + $set

**Do this:** Preview `{ sku: "A600" }` if you created it (otherwise use `A110`). `$set` `featured: true` and `updatedAt`. Inspect the write result and findOne.

**Expected result:** Four-part loop completed: preview, update, result, verify.

---

### Step 2 — $unset

**Do this:** Add `temporaryNote` with `$set`, verify, then `$unset` it.

**Expected result:** Field is present after set and absent after unset.

---

### Step 3 — $inc

**Do this:** `$inc` `stockQuantity` by 3 on that product.

**Expected result:** Quantity increased by exactly 3.

---

### Step 4 — $min and $max

**Do this:** On the same product, `$min` a `lowestPrice` of 40.00 and `$max` a `highestPrice` of 50.00 (use Decimal128). Run twice if needed.

**Expected result:** `$min` only lowers; `$max` only raises. Second run may yield `modifiedCount: 0`.

---

### Step 5 — $rename leftover

**Do this:** If `L190` still has `legacyName`, `$rename` it to `catalogName`. If already renamed, `matchedCount` may be 0.

**Expected result:** No document remains with `legacyName`.

---

### Step 6 — Nested-field update

**Do this:** `$set` `"contact.email"` for `C310` to a new address, without replacing `contact`.

**Expected result:** `phone` on C310 is still present.

---

### Step 7 — updateMany with preview

**Do this:** Preview `{ category: "ACCESSORY", active: true }`, count, then `$set` `taxable: true`. Check `matchedCount`.

**Expected result:** Count from preview equals `matchedCount`. You did not use `{}`.

---



## Success criteria

- [ ] Every write had preview and verification
- [ ] Did not replace a whole nested object accidentally
- [ ] Interpreted a `modifiedCount: 0` case

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
