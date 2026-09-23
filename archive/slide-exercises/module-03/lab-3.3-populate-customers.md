# Lab 3.3: Create and Populate the Customers Collection

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.6)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Insert customer `C101` with nested name, contact, a bounded `addresses` array, preferences, and status.

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

### Step 1 — Insert Aisha Khan

**Do this:** Optionally run `db.customers.deleteMany({})` first. Then:

```javascript
db.customers.insertOne({
  customerNumber: "C101",
  name: {
    first: "Aisha",
    last: "Khan"
  },
  contact: {
    email: "aisha@example.com",
    phone: "+1-555-0100"
  },
  addresses: [
    {
      type: "SHIPPING",
      street: "100 King Street",
      city: "Toronto",
      province: "Ontario",
      postalCode: "M5X 1A9",
      country: "Canada"
    }
  ],
  preferences: {
    newsletter: true,
    language: "English"
  },
  status: "ACTIVE",
  createdAt: new Date()
})
```

**Expected result:** `acknowledged: true` and an `insertedId`.

---

### Step 2 — Verify by customer number

**Do this:**

```javascript
db.customers.findOne({ customerNumber: "C101" })
```

**Expected result:** One document. You can point to the embedded `name`, `contact`, and `addresses[0].city`.

---

## Success criteria

- [ ] Customer C101 exists
- [ ] Address is a bounded array, not a separate collection
- [ ] You can find the document by `customerNumber`


## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
