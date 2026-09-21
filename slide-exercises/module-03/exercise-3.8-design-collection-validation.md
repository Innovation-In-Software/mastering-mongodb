# Exercise 3.8: Design Collection Validation

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.4)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Design a `$jsonSchema` validator that requires sku, name, category, non-negative decimal price, Boolean active, and Date createdAt.

---

## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Work in pairs. Capture answers in a notes file or on paper.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional — a table is enough |
| Timer | Instructor clocks this | Stay on the slide timer |

You do **not** need MongoDB running for this exercise.

You may type the validator in a scratch `.js` file. Running it is optional until Lab 3.6.

---

## Requirements

A valid product must contain:

- `sku`: string
- `name`: string
- `category`: string
- `price`: decimal and not negative
- `active`: Boolean
- `createdAt`: date

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — List required fields and bsonTypes

**Do this:** Write the `required` array and a `properties` map with `bsonType` for each field. Put `minimum: 0` on `price`.

**Expected result:** Six required names. `price` is `decimal` (not `double` or `string`). `active` is `bool`. `createdAt` is `date`.

---

### Step 2 — Assemble `$jsonSchema`

**Do this:** Wrap the design in:

```javascript
{
  $jsonSchema: {
    bsonType: "object",
    required: [ /* ... */ ],
    properties: { /* ... */ }
  }
}
```

Note `validationAction` / `validationLevel` if you know them. You will apply a similar validator in Lab 3.6.

**Expected result:** A complete validator object you could pass to `db.createCollection`. Extra optional fields are still allowed.

---

## Success criteria

- [ ] All six fields are required
- [ ] Price is decimal with minimum 0
- [ ] Boolean and Date types are correct


## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
