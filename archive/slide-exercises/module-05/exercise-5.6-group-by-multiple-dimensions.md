# Exercise 5.6: Group by Multiple Dimensions

**Module 5:** The Aggregation Framework  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 5, Lesson 5.3)  
**Time:** 15 min  
**Difficulty:** Intermediate

**Objective:** Group orders by payment status and fulfillment status with count, revenue, and average.

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

### Step 1 — Compound `_id`

**Do this:** Run:

```javascript
db.orders.aggregate([
  {
    $group: {
      _id: {
        paymentStatus: "$paymentStatus",
        fulfillmentStatus: "$fulfillmentStatus"
      },
      orderCount: { $sum: 1 },
      revenue: { $sum: "$total" },
      averageOrderValue: { $avg: "$total" }
    }
  },
  { $sort: { revenue: -1 } }
])
```

**Expected result:** Several combination documents. PAID + SHIPPED is a high-revenue group. PENDING + NEW includes O5001 and O6499.

---

### Step 2 — Read the grouping key

**Do this:** Pick one output document and rewrite `_id` in words: “this is all orders that are X and Y.”

**Expected result:** You do not treat `_id` as the original order ObjectId. It is the grouping key of the summary document.

---

## Success criteria

- [ ] `_id` is an object with two fields
- [ ] Each unique pair produces one document
- [ ] Revenue uses `$sum` of `total`, not `$sum: 1`

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
