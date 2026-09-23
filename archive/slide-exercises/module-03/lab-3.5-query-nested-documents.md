# Lab 3.5: Query Nested Documents and Arrays

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.6)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Query category, dotted nested attributes, array values, nested address city, and order line-item sku.

**Prerequisite:** Module 2 — a working `mongosh` session. If `training_store` still holds the Module 1 starter documents, these labs **replace** that shape with the Day 2 application model.


---

## Environment basics (read this first)

**Demonstration environment:** Windows 10/11 · PowerShell in Cursor (``Ctrl+` ``) · `mongosh` connected to the training instance.

| Task | Windows | Where |
|------|---------|-------|
| Open folder | `Ctrl+K Ctrl+O` | File → Open Folder |
| Terminal | ``Ctrl+` `` → PowerShell | Bottom panel |
| MongoDB shell | `mongosh` | Same terminal |

Use the same connection string from Module 2. Do **not** paste real passwords into chat or screenshots.

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Query products by category and nested attribute

**Do this:** Run:

```javascript
db.products.find({ category: "LAPTOP" })
db.products.find({ "attributes.memoryGB": 16 })
db.products.find({ tags: "technology" })
```

**Expected result:** Laptop query returns `L100`. Memory query returns the laptop. Tags query returns the book (`B300`).

---

### Step 2 — Query nested customer address and order items

**Do this:**

```javascript
db.customers.find({ "addresses.city": "Toronto" })
db.orders.find({ "items.sku": "L100" })
```

**Expected result:** Customer C101 and order O5001. You used dot notation into an array of documents — Module 4 will go deeper.

---

## Success criteria

- [ ] Category, nested field, and array queries each returned a document
- [ ] Address city and item sku queries worked
- [ ] You can explain why `"attributes.memoryGB"` uses quotes


## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
