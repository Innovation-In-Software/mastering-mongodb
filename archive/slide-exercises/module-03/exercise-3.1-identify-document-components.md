# Exercise 3.1: Identify Document Components

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.1)  
**Time:** 10 min  
**Difficulty:** Beginner

**Objective:** Label `_id`, scalar fields, an embedded document, an array, a Boolean, a date, and candidate required fields on a sample customer document.

---

## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Work in pairs. Capture answers in a notes file or on paper.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional — a table is enough |
| Timer | Instructor clocks this | Stay on the slide timer |

You do **not** need MongoDB running for this exercise.

---

## Sample document

```javascript
{
  _id: ObjectId("..."),
  customerNumber: "C101",
  name: {
    first: "Aisha",
    last: "Khan"
  },
  email: "aisha@example.com",
  tags: ["premium", "newsletter"],
  active: true,
  createdAt: ISODate("...")
}
```

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Label identifier, scalars, and the nested name

**Do this:** On the sample document, mark `_id`, every scalar field (`customerNumber`, `email`), and the embedded `name` document. Write one sentence: what does `_id` guarantee inside a collection?

**Expected result:** `_id` is the unique identifier. `customerNumber` and `email` are scalars. `name` is an embedded document with `first` and `last`.

---

### Step 2 — Label array, Boolean, date, and required fields

**Do this:** Mark `tags` as an array, `active` as a Boolean, and `createdAt` as a Date. Then list candidate **required** fields for every customer document in this collection.

**Expected result:** You named `tags`, `active`, and `createdAt` correctly. Required-field candidates typically include `_id` (always), `customerNumber`, `name`, `email` or contact, `active`, and `createdAt`.

---

## Success criteria

- [ ] `_id` is identified as unique within the collection
- [ ] Embedded `name` is distinguished from scalar fields
- [ ] Array, Boolean, and Date are labeled
- [ ] A short required-field list exists


## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
