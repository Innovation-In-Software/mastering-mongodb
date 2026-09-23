# Lab 3.6: Add Collection Validation

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.6)  
**Time:** 20 min  
**Difficulty:** Beginner

**Objective:** Create `validated_products` with `$jsonSchema`, insert one valid document, and read the error from one invalid insert.

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

### Step 1 — Create the validated collection and insert a valid product

**Do this:** Run:

```javascript
db.createCollection("validated_products", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "sku",
        "name",
        "category",
        "price",
        "active",
        "createdAt"
      ],
      properties: {
        sku: { bsonType: "string" },
        name: { bsonType: "string" },
        category: { bsonType: "string" },
        price: { bsonType: "decimal", minimum: 0 },
        active: { bsonType: "bool" },
        createdAt: { bsonType: "date" }
      }
    }
  }
})

db.validated_products.insertOne({
  sku: "A100",
  name: "USB-C Adapter",
  category: "ACCESSORY",
  price: Decimal128("29.99"),
  active: true,
  createdAt: new Date()
})
```

If the collection already exists from a previous attempt, drop it first with `db.validated_products.drop()`.

**Expected result:** Collection created. Valid insert succeeds.

---

### Step 2 — Attempt an invalid insert and read the error

**Do this:**

```javascript
db.validated_products.insertOne({
  sku: "A101",
  name: "USB Hub",
  category: "ACCESSORY",
  price: "39.99",
  active: "yes"
})
```

Read the write error (`failingDocumentId`, `errmsg`, or schema rules).

**Expected result:** The insert is rejected. You can name which rules failed (type of `price`, type of `active`, missing `createdAt`).

---

## Success criteria

- [ ] Valid insert succeeded
- [ ] Invalid insert failed
- [ ] You can point to the validation error text


## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
