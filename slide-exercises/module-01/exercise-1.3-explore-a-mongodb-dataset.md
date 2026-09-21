# Exercise 1.3: Explore a MongoDB Dataset

**Module 1:** Introduction to NoSQL Databases  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 1, Lesson 1.6)  
**Time:** 25 min  
**Difficulty:** Beginner

**Objective:** Identify databases, collections, documents, fields, arrays, and embedded objects in the `training_store` dataset.

**Prerequisite:** The instructor has MongoDB running (local or Atlas) and has loaded [`datasets/training_store`](../../datasets/training_store). If `mongosh` is not on your machine yet, follow on the instructor screen — Module 2 covers install.

---

## Environment basics (read this first)

**Demonstration environment:** Windows 10/11 · PowerShell in Cursor (``Ctrl+` ``) · `mongosh` connected to the training instance.

| Task | Windows | Where |
|------|---------|-------|
| Open folder | `Ctrl+K Ctrl+O` | File → Open Folder |
| Terminal | ``Ctrl+` `` → PowerShell | Bottom panel |
| MongoDB shell | `mongosh` | Same terminal, after the instructor shares the connection string |

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — View available databases

**Do this:** In `mongosh`, run:

```javascript
show dbs
```

**Expected result:** The database list includes `training_store` (and usually `admin`, `config`, and `local`).

---

### Step 2 — Select the training database and list collections

**Do this:** Run:

```javascript
use training_store
show collections
```

**Expected result:** The prompt shows `training_store`. Collections include `customers`, `products`, and `orders`.

---

### Step 3 — Retrieve one product document

**Do this:** Run:

```javascript
db.products.findOne()
```

**Expected result:** One product document prints. You can see `_id`, scalar fields such as `name` and `price`, and at least one nested or category-specific field.

---

### Step 4 — Retrieve one order document

**Do this:** Run:

```javascript
db.orders.findOne()
```

**Expected result:** One order document prints. You can point to an embedded object (for example `customer` or `shippingAddress`) and an array (`items`).

---

### Step 5 — Identify document structures

**Do this:** On the product and order you retrieved, label: `_id`, scalar fields, embedded documents, arrays, dates, numeric values, and boolean values. Write them on the observation sheet below.

**Expected result:** Your sheet names at least one example of each structure. `_id` is described as the unique document identifier.

---

### Step 6 — Compare two product documents

**Do this:** Run:

```javascript
db.products.find().limit(2)
```

Then list fields that appear on one product and not the other (for example laptop `attributes.processor` versus book `attributes.isbn`).

**Expected result:** You can explain that documents in the same collection may contain different category-specific fields, and that this is expected in a flexible schema.

---

### Step 7 — Complete the observation sheet

**Do this:** Answer the six questions on the observation sheet. Be ready to share how the document structure resembles an application object.

**Expected result:** You can navigate to a database, list collections, read a document, identify MongoDB’s core structural elements, and state one difference between a table row and a document.

---

## Observation sheet

1. Which databases and collections were available?
2. What is the purpose of `_id`?
3. Which document contained an embedded object?
4. Which document contained an array?
5. Which fields differed between product documents?
6. How does the document structure resemble an application object?

---

## Success criteria

- [ ] Navigated to `training_store` and listed collections
- [ ] Retrieved and read a product document and an order document
- [ ] Identified `_id`, an embedded object, and an array
- [ ] Explained one difference between a table row and a document
- [ ] Observation sheet is complete

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
