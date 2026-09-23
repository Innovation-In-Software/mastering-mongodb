# Exercise 4.23: Lab 4.9 Delete Operations Lab

**Module 4:** The MongoDB Query Language  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 4)  
**Time:** 20 min  
**Difficulty:** Intermediate

**Objective:** Delete only temporary lab records using a preview-count-delete-verify sequence.

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

### Step 1 — Insert temporary documents

**Do this:** insertMany products `TEMP-100` and `TEMP-101` with `labTag: "module4"` plus a throwaway order `TEMP-O1`.

**Expected result:** Two products and one order exist for this lab only.

---

### Step 2 — Build a precise deletion filter

**Do this:** Use `{ sku: /^TEMP-/ }` or `{ labTag: "module4" }` — not `{}`.

**Expected result:** The filter cannot match L100 or production-like SKUs.

---

### Step 3 — Preview matches

**Do this:** find(filter) on products.

**Expected result:** Only TEMP-100 and TEMP-101.

---

### Step 4 — Count matches

**Do this:** countDocuments(filter).

**Expected result:** Count is 2.

---

### Step 5 — Delete one document

**Do this:** deleteOne `{ sku: "TEMP-100" }`. Inspect `deletedCount`.

**Expected result:** `deletedCount: 1`. TEMP-101 remains.

---

### Step 6 — Delete multiple temporary documents

**Do this:** deleteMany with the remaining TEMP filter. Then delete the throwaway order by `orderNumber`.

**Expected result:** `deletedCount` matches the preview of what was left.

---

### Step 7 — Inspect deletedCount

**Do this:** Record both delete results.

**Expected result:** Sums equal the documents you intended to remove.

---

### Step 8 — Verify no unintended removals

**Do this:** countDocuments on products; findOne L100 and O5001.

**Expected result:** Catalog SKUs and real orders remain. Reloading `load.js` restores a clean set if needed.

---



## Success criteria

- [ ] Never used `deleteMany({})`
- [ ] Previewed and counted before deleting
- [ ] Confirmed L100 / O5001 still exist

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
