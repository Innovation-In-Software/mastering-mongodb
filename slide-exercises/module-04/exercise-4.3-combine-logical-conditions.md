# Exercise 4.3: Combine Logical Conditions

**Module 4:** The MongoDB Query Language  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 4)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Combine implicit AND, `$or`, and `$nor` into precise product and order filters.

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

### Step 1 — Active laptops or books

**Do this:** Run:

```javascript
db.products.find({
  active: true,
  $or: [
    { category: "LAPTOP" },
    { category: "BOOK" }
  ]
})
```

**Expected result:** Active laptops and books match. Inactive `L190` is excluded by `active: true`.

---

### Step 2 — Active products under 100

**Do this:** Run:

```javascript
db.products.find({
  active: true,
  price: { $lt: Decimal128("100.00") }
})
```

**Expected result:** Implicit AND. Accessories and cheaper books match. `XBAD` does not, because of BSON type.

---

### Step 3 — Pending or processing orders

**Do this:** Run:

```javascript
db.orders.find({
  $or: [
    { paymentStatus: "PENDING" },
    { fulfillmentStatus: "PROCESSING" }
  ]
})
```

**Expected result:** `O5001` and `O6499` are PENDING payment; `O6401` is PROCESSING. Prefer `$in` when alternatives share **one** field.

---

### Step 4 — Neither discontinued nor inactive

**Do this:** Run:

```javascript
db.products.find({
  $nor: [
    { tags: "discontinued" },
    { active: false }
  ]
})
```

**Expected result:** Documents that are inactive **or** tagged `discontinued` are excluded. `L190` is both.

---



## Success criteria

- [ ] Used implicit AND for field combinations
- [ ] Used `$in` when alternatives share one field
- [ ] Stated what `$nor` excludes

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
