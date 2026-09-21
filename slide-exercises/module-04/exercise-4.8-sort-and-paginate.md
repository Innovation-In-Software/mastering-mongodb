# Exercise 4.8: Sort and Paginate Results

**Module 4:** The MongoDB Query Language  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 4)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Sort, limit, skip, count, and retrieve distinct values with a deterministic tiebreaker.

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

### Step 1 — Sort products by price ascending

**Do this:** Run:

```javascript
db.products.find({}, { name: 1, price: 1 }).sort({ price: 1, _id: 1 })
```

**Expected result:** Cheapest Decimal128 prices first. `XBAD` may sort oddly because its price is a string — mention that.

---

### Step 2 — Sort by category then price descending

**Do this:** Run:

```javascript
db.products.find({}, { category: 1, name: 1, price: 1, _id: 0 })
  .sort({ category: 1, price: -1 })
```

**Expected result:** Within each category the highest price prints first.

---

### Step 3 — Five most expensive active products

**Do this:** Run:

```javascript
db.products.find({ active: true }, { name: 1, price: 1, _id: 0 })
  .sort({ price: -1, _id: 1 })
  .limit(5)
```

**Expected result:** Expect `L110`, `L100`, then `L190` if active were included — on active-only, `L110` then `L100` then `A500`.

---

### Step 4 — Page 1 and page 2 (five per page)

**Do this:** Run both:

```javascript
db.products.find({ active: true }).sort({ _id: 1 }).skip(0).limit(5)
db.products.find({ active: true }).sort({ _id: 1 }).skip(5).limit(5)
```

**Expected result:** Two disjoint pages. The sort key is required for stable pagination.

---

### Step 5 — Count and distinct

**Do this:** Run:

```javascript
db.products.countDocuments({ active: true })
db.products.distinct("category")
```

**Expected result:** Count is smaller than 16 because inactive items exist. Distinct includes `LAPTOP`, `BOOK`, `ACCESSORY`, `SHOE`.

---



## Success criteria

- [ ] Included a unique tiebreaker in sort
- [ ] Produced two pages of five
- [ ] Used `countDocuments` rather than the legacy `count()` API

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
