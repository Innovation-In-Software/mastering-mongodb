# Exercise 4.22: Lab 4.8 Replace and Upsert Lab

**Module 4:** The MongoDB Query Language  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 4)  
**Time:** 20 min  
**Difficulty:** Intermediate

**Objective:** Compare `$set`, `replaceOne`, and a repeated upsert on a copied test document.

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

### Step 1 — Copy a test document

**Do this:** Insert a copy of `A410` as sku `TEMP-200` (new `_id`). Include extra field `notes: "lab copy"`.

**Expected result:** TEMP-200 exists with `notes`.

---

### Step 2 — Update selected fields with $set

**Do this:** `$set` `price` and `featured` on TEMP-200. Then findOne.

**Expected result:** `notes` and `tags` still exist.

---

### Step 3 — Replace the copied document

**Do this:** replaceOne TEMP-200 with a document that has sku, name, category, price, active, updatedAt only.

**Expected result:** `notes`, `tags`, and other omitted fields **disappear**. `_id` remains.

---

### Step 4 — Compare $set vs replaceOne

**Do this:** Write two bullets describing remaining fields after each operation.

**Expected result:** You can explain that replace is not a partial update.

---

### Step 5 — Perform an upsert

**Do this:** updateOne `{ sku: "A700" }` with `$set` + `$setOnInsert` and `upsert: true`.

**Expected result:** First run returns `upsertedId`.

---

### Step 6 — Run the same upsert again

**Do this:** Repeat Step 5.

**Expected result:** No new `upsertedId`. `createdAt` unchanged if it was in `$setOnInsert`.

---

### Step 7 — Compare insert and update outcomes

**Do this:** Record both write results in your notes.

**Expected result:** You can distinguish insert-via-upsert from update-via-upsert.

---



## Success criteria

- [ ] Showed fields lost after replaceOne
- [ ] Used a unique SKU for upsert
- [ ] Compared both upsert runs

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
