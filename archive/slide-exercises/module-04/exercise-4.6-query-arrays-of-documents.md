# Exercise 4.6: Query Arrays of Documents

**Module 4:** The MongoDB Query Language  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 4)  
**Time:** 15 min  
**Difficulty:** Intermediate

**Objective:** Query nested arrays and use `$elemMatch` when two conditions must apply to the same element.

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

### Step 1 — Orders containing SKU L100

**Do this:** Run:

```javascript
db.orders.find({ "items.sku": "L100" })
```

**Expected result:** `O5001`, `O6101`, and `O6401` match.

---

### Step 2 — Orders with any item quantity ≥ 2

**Do this:** Run:

```javascript
db.orders.find({ "items.quantity": { $gte: 2 } })
```

**Expected result:** `O5001` (A410 qty 2) and `O6401` (L100 qty 2). Other orders may also match.

---

### Step 3 — Same item is L100 and qty ≥ 2

**Do this:** Run:

```javascript
db.orders.find({
  items: {
    $elemMatch: {
      sku: "L100",
      quantity: { $gte: 2 }
    }
  }
})
```

**Expected result:** Only `O6401`. `O5001` has L100 qty 1 **and** a different item (A410) qty 2 — that is the trap.

---

### Step 4 — Confirm the trap without $elemMatch

**Do this:** Run:

```javascript
db.orders.find({
  "items.sku": "L100",
  "items.quantity": { $gte: 2 }
})
```

**Expected result:** Both `O5001` and `O6401` match. Dot notation does **not** require the same array element.

---

### Step 5 — Customers with a Toronto shipping address

**Do this:** Run:

```javascript
db.customers.find({
  addresses: {
    $elemMatch: { type: "SHIPPING", city: "Toronto" }
  }
})
```

**Expected result:** `C101` matches. Address `type` values in this dataset are uppercase (`SHIPPING`).

---



## Success criteria

- [ ] Named the O5001 false-positive without `$elemMatch`
- [ ] Wrote a correct `$elemMatch` on `items`
- [ ] Queried `addresses` as an array of documents

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
