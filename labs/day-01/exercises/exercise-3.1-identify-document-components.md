# Exercise 3.1 — Identify Document Components

**Module 3** (Data Modeling with MongoDB) · Day 1 · **Checkpoint A**  
**Deck:** `decks/pptx_new/MongoDB_Module03_Data_Modeling_with_MongoDB.pptx`, slide 42  
**Time:** 10 min · **Type:** discussion (pairs) · **MongoDB needed:** no

**Objective:** Label every part of a customer document: `_id`, scalar fields, an embedded document, an array, a Boolean, a date, and the candidate required fields.

---

## Sample document

This is a teaching sample of customer C101. Label it on paper or in a notes file.

```javascript
{ _id: ObjectId("..."),
  customerNumber: "C101",
  name: { first: "Aisha",
          last: "Khan" },
  email: "aisha@example.com",
  tags: ["premium", "newsletter"],
  active: true,
  createdAt: ISODate("...") }
```

---

## Do this

1. Mark `_id` and write one sentence: what does `_id` guarantee inside a collection?
2. Mark the scalar fields and the embedded `name` document.
3. Label the array, the Boolean and the date.
4. List the candidate **required** fields that every customer document in this collection should have.

## Expected result

A labelled document plus a short required-field list. Each label names the kind of value (scalar, embedded document, array, Boolean, Date, ObjectId), not just the field name.

## Reference solution

After the debrief, compare with [Exercise 3.1 solution](solution/exercise-3.1-identify-document-components.md).

## Lab connection

Lab 2, Step 3 ([LAB-2-GUIDE.md](../lab2/LAB-2-GUIDE.md)) inserts the real C101. It keeps `email` inside a `contact` object, uses `status: "ACTIVE"` instead of an `active` flag, and has no `tags`. The labelling skill is the same.

## Success criteria

- [ ] `_id` is identified as unique within the collection
- [ ] The embedded `name` is told apart from the scalar fields
- [ ] The array, Boolean and Date are labelled
- [ ] A short required-field list exists
