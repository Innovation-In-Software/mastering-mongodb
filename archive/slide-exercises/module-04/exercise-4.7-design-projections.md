# Exercise 4.7: Design Projections

**Module 4:** The MongoDB Query Language  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 4)  
**Time:** 10 min  
**Difficulty:** Beginner

**Objective:** Return only required fields, including nested paths and a matching array element.

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

### Step 1 — Product name and price without _id

**Do this:** Run:

```javascript
db.products.find(
  { active: true },
  { name: 1, price: 1, _id: 0 }
)
```

**Expected result:** Each result has only `name` and `price`. Mixing inclusion of `name` with exclusion of `tags` would error.

---

### Step 2 — Customer name and email

**Do this:** Run:

```javascript
db.customers.find(
  { customerNumber: "C101" },
  { "name.first": 1, "name.last": 1, "contact.email": 1, _id: 0 }
)
```

**Expected result:** Nested inclusion. Sibling fields such as `addresses` are omitted.

---

### Step 3 — Order number, status, and total

**Do this:** Run:

```javascript
db.orders.find(
  {},
  { orderNumber: 1, status: 1, total: 1, _id: 0 }
)
```

**Expected result:** A compact operations list. `_id` is excluded explicitly.

---

### Step 4 — Exclude large attribute fields

**Do this:** Run:

```javascript
db.products.find({ sku: "L100" }, { attributes: 0, tags: 0 })
```

**Expected result:** Exclusion projection. All remaining fields are returned.

---

### Step 5 — Only the matching order item

**Do this:** Run:

```javascript
db.orders.find(
  { orderNumber: "O5001" },
  { items: { $elemMatch: { sku: "L100" } }, orderNumber: 1 }
)
```

**Expected result:** `items` contains only the L100 element. Other line items are omitted from the result shape.

---



## Success criteria

- [ ] Wrote an inclusion projection that excludes `_id`
- [ ] Projected nested customer fields with dotted paths
- [ ] Used `$elemMatch` in a projection on `items`

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
