# Exercise 4.21: Lab 4.7 Array Manipulation Lab

**Module 4:** The MongoDB Query Language  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 4)  
**Time:** 30 min  
**Difficulty:** Intermediate

**Objective:** Add, unique-add, batch-add, and remove tags; update one, all, and filtered array elements on an order.

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

### Step 1 — $push a tag

**Do this:** `$push` `"clearance"` onto `A110`.

**Expected result:** Array gains `clearance` even if you run it twice (duplicates).

---

### Step 2 — $addToSet

**Do this:** `$addToSet` `"office"` on `A110`. Run twice.

**Expected result:** Second run does not duplicate `office`.

---

### Step 3 — $each

**Do this:** `$addToSet` with `$each` for `portable` and `featured`.

**Expected result:** Both values present once.

---

### Step 4 — $pull

**Do this:** `$pull` `"clearance"` from `A110`.

**Expected result:** No `clearance` values remain (all duplicates removed).

---

### Step 5 — Positional $

**Do this:** On `O5001`, match `"items.sku": "A410"` and `$set` `"items.$.quantity"` to 4.

**Expected result:** Only the mouse line changes.

---

### Step 6 — All elements $[]

**Do this:** `$set` `"items.$[].reviewed": true` on `O5001`.

**Expected result:** Every line item has `reviewed: true`.

---

### Step 7 — arrayFilters

**Do this:** On `O5001`, `$set` `"items.$[item].discounted": true` with `arrayFilters: [ { "item.unitPrice": { $gte: Decimal128("100.00") } } ]`.

**Expected result:** The L100 line is discounted; the cheaper mouse line is not.

---



## Success criteria

- [ ] Contrasted `$push` and `$addToSet`
- [ ] Updated one element with `$`
- [ ] Used `arrayFilters` for a price threshold

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
