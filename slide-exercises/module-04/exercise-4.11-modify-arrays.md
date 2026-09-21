# Exercise 4.11: Modify Arrays

**Module 4:** The MongoDB Query Language  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 4)  
**Time:** 15 min  
**Difficulty:** Intermediate

**Objective:** Use `$push`, `$addToSet`, `$each`, `$pull`, positional `$`, and `$[]`.

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

### Step 1 — Push a tag (may duplicate)

**Do this:** Run twice:

```javascript
db.products.updateOne({ sku: "A620" }, { $push: { tags: "featured" } })
```

**Expected result:** The second run adds a second `featured` if you used `$push` both times. That is the teaching point.

---

### Step 2 — Add a tag without duplicates

**Do this:** Run twice:

```javascript
db.products.updateOne({ sku: "A620" }, { $addToSet: { tags: "office" } })
```

**Expected result:** Second run: `matchedCount: 1`, `modifiedCount: 0` if `office` is already present.

---

### Step 3 — Add several tags

**Do this:** Run:

```javascript
db.products.updateOne(
  { sku: "A620" },
  { $addToSet: { tags: { $each: ["portable", "usb-c"] } } }
)
```

**Expected result:** `usb-c` is already on A620 from insert — `$addToSet` leaves it unique. `portable` is added.

---

### Step 4 — Remove a deprecated tag

**Do this:** Run:

```javascript
db.products.updateOne({ sku: "L190" }, { $pull: { tags: "discontinued" } })
```

**Expected result:** `discontinued` is removed from `L190`. The product can still be `active: false`.

---

### Step 5 — Update one order item and mark all items reviewed

**Do this:** Run:

```javascript
db.orders.updateOne(
  { orderNumber: "O5001", "items.sku": "L100" },
  { $set: { "items.$.quantity": 2 } }
)
db.orders.updateOne(
  { orderNumber: "O5001" },
  { $set: { "items.$[].reviewed": false } }
)
```

**Expected result:** The L100 line quantity becomes 2. Every item on that order gets `reviewed: false`.

---



## Success criteria

- [ ] Explained why `$push` can duplicate
- [ ] Used `$addToSet` with `$each`
- [ ] Used `$` and `$[]` correctly

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
