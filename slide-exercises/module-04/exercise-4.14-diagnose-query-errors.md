# Exercise 4.14: Diagnose Query Errors

**Module 4:** The MongoDB Query Language  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 4)  
**Time:** 15 min  
**Difficulty:** Intermediate

**Objective:** Correct seven broken queries covering case, BSON type, dotted paths, operators, projection, `$elemMatch`, and update operators.

---

## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Capture answers in a notes file.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional |
| Timer | Instructor clocks this | — |

You may use `mongosh` to test rewrites, but reasoning is the deliverable.


---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Wrong field capitalization

**Do this:** This returns nothing:

```javascript
db.products.find({ Category: "LAPTOP" })
```

Rewrite it.

**Expected result:** Field is `category` (lowercase). MongoDB does not fold identifier case.

---

### Step 2 — String instead of Decimal128

**Do this:** This comparison is unreliable:

```javascript
db.products.find({ price: { $gt: "100.00" } })
```

Rewrite it.

**Expected result:** Use `{ price: { $gt: Decimal128("100.00") } }`. Types must match stored BSON.

---

### Step 3 — Unquoted dotted path

**Do this:** This is invalid:

```javascript
db.products.find({ attributes.memoryGB: 16 })
```

Rewrite it.

**Expected result:** Quote the path: `{ "attributes.memoryGB": 16 }`.

---

### Step 4 — Incorrect operator placement

**Do this:** This is wrong:

```javascript
db.products.find({ $gt: { price: Decimal128("100.00") } })
```

Rewrite it.

**Expected result:** Comparison operators live **inside** the field: `{ price: { $gt: Decimal128("100.00") } }`.

---

### Step 5 — Mixed projection

**Do this:** This errors:

```javascript
db.products.find({}, { name: 1, tags: 0 })
```

Provide two legal alternatives.

**Expected result:** Inclusion `{ name: 1, price: 1, _id: 0 }` **or** exclusion `{ tags: 0, attributes: 0 }`. `_id` is the only mix allowed.

---

### Step 6 — Incorrect $elemMatch

**Do this:** Rewrite so both conditions apply to one item:

```javascript
db.orders.find({ "items.sku": "L100", "items.quantity": { $gte: 2 } })
```

**Expected result:** Use `items: { $elemMatch: { sku: "L100", quantity: { $gte: 2 } } }`.

---

### Step 7 — Missing update operator

**Do this:** This replacement-style document is rejected by modern `updateOne`:

```javascript
db.products.updateOne({ sku: "L100" }, { featured: true })
```

Rewrite it.

**Expected result:** Use `{ $set: { featured: true } }`. Bare field assignment is not an update operator.

---



## Success criteria

- [ ] Corrected all seven queries
- [ ] Named the class of each mistake
- [ ] Did not run the mixed projection as-is expecting success

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
