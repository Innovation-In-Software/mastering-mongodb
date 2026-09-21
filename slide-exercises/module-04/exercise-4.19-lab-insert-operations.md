# Exercise 4.19: Lab 4.5 Insert Operations Lab

**Module 4:** The MongoDB Query Language  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 4)  
**Time:** 25 min  
**Difficulty:** Beginner

**Objective:** Insert a product, several products, a customer, and a related order; inspect ids and types.

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

### Step 1 — Insert one product

**Do this:** Insert SKU `A600` Wireless Presenter, ACCESSORY, Decimal128 44.99, active true.

**Expected result:** `insertedId` present. Skip if A600 already exists from a demo.

---

### Step 2 — Insert several products

**Do this:** insertMany two more accessories with unique SKUs `A610` and `A611`.

**Expected result:** `insertedIds` has two entries.

---

### Step 3 — Insert a customer

**Do this:** customerNumber `C601` with nested name, contact, and one shipping address.

**Expected result:** Document round-trips with the same shape.

---

### Step 4 — Insert an order referencing the customer

**Do this:** Order `O5200` with an embedded customer snapshot and an item for A600.

**Expected result:** Order stores name/email snapshot, not only the id.

---

### Step 5 — Inspect inserted IDs

**Do this:** Print the insert results you saved, or query by SKU / customerNumber.

**Expected result:** You can name each new `_id`.

---

### Step 6 — Query every new document

**Do this:** find the products, customer, and order.

**Expected result:** All four (or more) documents exist.

---

### Step 7 — Correct inconsistent types

**Do this:** If any price was a number or string, `$set` it to Decimal128 and re-query `$type`.

**Expected result:** New money fields are decimal.

---



## Success criteria

- [ ] Used Decimal128 on insert
- [ ] Embedded a customer snapshot on the order
- [ ] Verified with queries, not only insert acknowledgements

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
