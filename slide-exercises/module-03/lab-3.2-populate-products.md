# Lab 3.2: Create and Populate the Products Collection

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.6)  
**Time:** 20 min  
**Difficulty:** Beginner

**Objective:** Replace starter products with three catalog documents that share a core and use nested `attributes`.

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

### Step 1 — Clear previous products (optional but recommended)

**Do this:** Run `db.products.deleteMany({})` so Day 2 queries see only the Module 3 catalog. Skip this only if the instructor told you to keep Module 1 documents.

**Expected result:** `deletedCount` is reported. `db.products.countDocuments()` is 0.

---

### Step 2 — Insert the three products

**Do this:** Run:

```javascript
db.products.insertMany([
  {
    sku: "L100",
    name: "Business Laptop",
    category: "LAPTOP",
    price: Decimal128("1299.99"),
    attributes: {
      processor: "Intel Core i7",
      memoryGB: 16,
      storageGB: 512,
      screenSizeInches: 14
    },
    tags: ["business", "portable"],
    active: true,
    createdAt: new Date()
  },
  {
    sku: "S200",
    name: "Running Shoe",
    category: "SHOE",
    price: Decimal128("129.99"),
    attributes: {
      sizes: [7, 8, 9, 10],
      color: "Blue",
      material: "Mesh"
    },
    tags: ["running", "sports"],
    active: true,
    createdAt: new Date()
  },
  {
    sku: "B300",
    name: "MongoDB Fundamentals",
    category: "BOOK",
    price: Decimal128("59.99"),
    attributes: {
      author: "A. Trainer",
      isbn: "978-0000000000",
      language: "English"
    },
    tags: ["database", "technology"],
    active: true,
    createdAt: new Date()
  }
])
db.products.find()
```

**Expected result:** Three documents. Each has the shared core. Category-specific fields live under `attributes`.

---

## Success criteria

- [ ] Three products inserted
- [ ] Prices are Decimal128
- [ ] `attributes` differs by category


## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
