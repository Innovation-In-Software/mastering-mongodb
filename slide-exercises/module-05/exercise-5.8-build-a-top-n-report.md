# Exercise 5.8: Build a Top-N Report

**Module 5:** The Aggregation Framework  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 5, Lesson 5.4)  
**Time:** 15 min  
**Difficulty:** Intermediate

**Objective:** Build top-N reports for customers, products, orders, and categories using group → sort → limit.

---

## Environment basics (read this first)

**Demonstration environment:** Windows 10/11 · PowerShell in Cursor (``Ctrl+` ``) · `mongosh` connected to the training instance.

| Task | Windows | Where |
|------|---------|-------|
| Open folder | `Ctrl+K Ctrl+O` | File → Open Folder |
| Terminal | ``Ctrl+` `` → PowerShell | Bottom panel |
| MongoDB shell | `mongosh` | Same terminal |

Use the same connection string from Module 2. **Dataset:** `use training_store`.

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Top customers and highest-value orders

**Do this:** Run:

```javascript
db.orders.aggregate([
  { $match: { paymentStatus: "PAID" } },
  { $group: { _id: "$customerId", totalSpent: { $sum: "$total" } } },
  { $sort: { totalSpent: -1 } },
  { $limit: 5 }
])
db.orders.aggregate([
  { $match: { paymentStatus: "PAID" } },
  { $sort: { total: -1, orderNumber: 1 } },
  { $limit: 3 },
  { $project: { _id: 0, orderNumber: 1, total: 1 } }
])
```

**Expected result:** Top spender is C101. Three highest paid orders include O6202 and O6304 (both `2146.99`).

---

### Step 2 — Top products by units and categories by count

**Do this:** Run:

```javascript
db.orders.aggregate([
  { $match: { paymentStatus: "PAID" } },
  { $unwind: "$items" },
  { $group: { _id: "$items.sku", unitsSold: { $sum: "$items.quantity" } } },
  { $sort: { unitsSold: -1, _id: 1 } },
  { $limit: 3 }
])
db.products.aggregate([
  { $sortByCount: "$category" }
])
```

**Expected result:** A410 is among the unit leaders (4). Category counts: ACCESSORY 4, then SHOE 3, LAPTOP 3, BOOK 2 (including inactive L190).

---

## Success criteria

- [ ] Every top-N pipeline sorts before it limits
- [ ] A tiebreaker field is used when values can tie
- [ ] Customer spend uses paid totals, not pending orders

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
