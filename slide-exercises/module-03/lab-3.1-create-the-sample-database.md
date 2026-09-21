# Lab 3.1: Create the Sample Application Database

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.6)  
**Time:** 10 min  
**Difficulty:** Beginner

**Objective:** Select `training_store` and create the `products`, `customers`, `orders`, and `reviews` collections.

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

### Step 1 — Select the database

**Do this:** In `mongosh`, run:

```javascript
use training_store
```

**Expected result:** The prompt shows `training_store`. The database may not appear in `show dbs` until it holds data.

---

### Step 2 — Create the four collections

**Do this:** Run:

```javascript
db.createCollection("products")
db.createCollection("customers")
db.createCollection("orders")
db.createCollection("reviews")
show collections
```

If a collection already exists from Module 1, `createCollection` reports that it exists — that is fine. Continue.

**Expected result:** `show collections` lists `products`, `customers`, `orders`, and `reviews`.

---

## Success criteria

- [ ] Prompt is `training_store`
- [ ] Four application collections are listed


## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
