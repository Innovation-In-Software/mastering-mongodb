# Exercise 4.1: Read Basic Documents

**Module 4:** The MongoDB Query Language  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 4)  
**Time:** 10 min  
**Difficulty:** Beginner

**Objective:** Retrieve documents with empty, equality, and unique-identifier filters.

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

### Step 1 — Retrieve all products

**Do this:** Run:

```javascript
db.products.find({})
```

**Expected result:** A cursor of product documents prints. This is unbounded — acceptable on the training set only.

---

### Step 2 — Find one product by SKU

**Do this:** Run:

```javascript
db.products.findOne({ sku: "L100" })
```

**Expected result:** One laptop document is returned. `findOne()` returns a document or `null`, not a cursor.

---

### Step 3 — Find active products

**Do this:** Run:

```javascript
db.products.find({ active: true })
```

**Expected result:** Inactive items such as `L190` are excluded. Field names and booleans are case-sensitive.

---

### Step 4 — Find ACTIVE customers

**Do this:** Run:

```javascript
db.customers.find({ status: "ACTIVE" })
```

**Expected result:** `C101`, `C204`, `C310`, `C412`, and `C620` match. `C515` (`INACTIVE`) does not.

---

### Step 5 — Find one order by number

**Do this:** Run:

```javascript
db.orders.findOne({ orderNumber: "O5001" })
```

**Expected result:** The order includes an embedded `customer` object and an `items` array.

---



## Success criteria

- [ ] Used `find()` and `findOne()` correctly
- [ ] Filtered on `active` and `status` with exact case
- [ ] Located `O5001` by `orderNumber`

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
