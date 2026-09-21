# Exercise 4.13: Correct Unsafe Operations

**Module 4:** The MongoDB Query Language  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 4)  
**Time:** 10 min  
**Difficulty:** Intermediate

**Objective:** Explain the risk of three unsafe writes and replace them with safer alternatives.

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

### Step 1 — Unfiltered updateMany

**Do this:** The unsafe command is:

```javascript
db.products.updateMany({}, { $set: { active: false } })
```

Write the risk and a safer filter (for example discontinued items only). Do **not** run the unsafe command.

**Expected result:** Risk: every product becomes inactive. Safer: preview `{ tags: "discontinued" }` or `{ discontinuedAt: { $exists: true } }`, count, then `updateMany` with that filter.

---

### Step 2 — Empty deleteMany

**Do this:** The unsafe command is:

```javascript
db.orders.deleteMany({})
```

Write the risk and a safer sequence.

**Expected result:** Risk: all orders are removed. Safer: never use `{}`; filter on test `orderNumber` values; `find` → `countDocuments` → `deleteMany`.

---

### Step 3 — Replacing a nested object

**Do this:** This update wipes sibling `contact` fields:

```javascript
db.customers.updateOne(
  { customerNumber: "C101" },
  { $set: { contact: { email: "new@example.com" } } }
)
```

Rewrite it so only email changes.

**Expected result:** Safer:

```javascript
db.customers.updateOne(
  { customerNumber: "C101" },
  { $set: { "contact.email": "new@example.com" } }
)
```

---

### Step 4 — Class debrief

**Do this:** Share one rewrite. Listen for the instructor solution and adjust your notes.

**Expected result:** You can name the blast radius of `{}` and the difference between replacing an embedded document and setting one path.

---



## Success criteria

- [ ] Did not execute the empty-filter writes
- [ ] Provided a precise alternative for each case
- [ ] Used dotted `$set` for nested email

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
