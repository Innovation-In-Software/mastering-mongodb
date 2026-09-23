# Exercise 3.4 — solution (instructor)

**Module 3** · Day 1 · Checkpoint D · slide 45  
**Type:** design · **Do not hand this sheet to participants.**

## Answer

### 1. Core fields and BSON types

| Field | BSON type |
| --- | --- |
| `_id` | ObjectId (generated) |
| `sku` | String — business key, unique index `sku_unique` in `training_store` |
| `name` | String |
| `description` | String (worksheet asks for it; `training_store` does not store it) |
| `category` | String: `LAPTOP`, `SHOE`, `BOOK` |
| `price` | **Decimal128** |
| `active` | **Boolean** |
| `createdAt` | **Date** |

### 2. Placement

Type-specific fields go under `attributes`. The core stays identical, so browsing by category and price uses the core, and category-specific searches use dotted paths such as `"attributes.isbn"`.

### 3. Model answer — training_store's L100, S200 and B300

These are the documents from `datasets/training_store/load.js` (Lab 2 Step 2 inserts the same shape with `createdAt: new Date()`):

```javascript
{ sku: "L100", name: "Business Laptop", category: "LAPTOP",
  price: Decimal128("1299.99"),
  attributes: { processor: "Intel Core i7", memoryGB: 16, storageGB: 512,
                screenSizeInches: 14 },
  tags: ["business", "portable"], active: true,
  createdAt: ISODate("2026-08-20T09:00:00Z") }

{ sku: "S200", name: "Running Shoe", category: "SHOE",
  price: Decimal128("129.99"),
  attributes: { sizes: [7, 8, 9, 10], color: "Blue", material: "Mesh" },
  tags: ["running", "sports"], active: true,
  createdAt: ISODate("2026-08-21T09:00:00Z") }

{ sku: "B300", name: "MongoDB Fundamentals", category: "BOOK",
  price: Decimal128("59.99"),
  attributes: { author: "A. Trainer", isbn: "978-0000000000", language: "English" },
  tags: ["database", "technology"], active: true,
  createdAt: ISODate("2026-08-22T09:00:00Z") }
```

The worksheet also asks for `description`, a shoe's gender category and a book's publisher, which `training_store` does not store. Learner answers that add `description` to the core and `genderCategory` / `publisher` under `attributes` are correct.

### 4. Queries the design supports

```javascript
db.products.find({ category: "LAPTOP" })
db.products.find({ "attributes.isbn": "978-0000000000" })   // returns B300
```

## Slide solution checklist

- `sku` string · `price` Decimal128
- `active` Boolean · `createdAt` Date
- Type-specific data in `attributes`
- Queryable by `category` and `attributes.isbn`
- No `productPrice` beside `price`

## What you want to hear

The same field names and types on all three documents, and no category-specific field required for every product. Watch for price as a string or a Double, and for `productName` / `title` on one product and `name` on another.
