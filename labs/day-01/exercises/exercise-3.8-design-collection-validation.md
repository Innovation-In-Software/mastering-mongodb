# Exercise 3.8 — Design Collection Validation

**Module 3** (Data Modeling with MongoDB) · Day 1 · **Checkpoint H**  
**Deck:** `decks/pptx_new/MongoDB_Module03_Data_Modeling_with_MongoDB.pptx`, slide 49  
**Time:** 15 min · **Type:** design (pairs) · **MongoDB needed:** no — type the validator in a scratch `.js` file

**Objective:** Design a `$jsonSchema` validator for products.

---

## Requirements

A valid product must contain these fields:

| Field | Rule |
| --- | --- |
| `sku` | string |
| `name` | string |
| `category` | string |
| `price` | decimal, not negative |
| `active` | Boolean |
| `createdAt` | date |

---

## Do this

1. Write the `required` array.
2. Give each field a `bsonType` in a `properties` map.
3. Add `minimum: 0` to `price`.
4. Wrap it in `$jsonSchema`:

```javascript
{
  $jsonSchema: {
    bsonType: "object",
    required: [ /* ... */ ],
    properties: { /* ... */ }
  }
}
```

If you know them, note `validationLevel` and `validationAction` too.

## Expected result

A complete validator object you could pass to `db.createCollection(..., { validator: ... })`. Watch the type names: `$jsonSchema` uses its own `bsonType` names, which are not the mongosh constructor names.

## Reference solution

After the debrief, compare with [Exercise 3.8 solution](solution/exercise-3.8-design-collection-validation.md).

## Lab connection

Lab 2, Step 6 ([LAB-2-GUIDE.md](../lab2/LAB-2-GUIDE.md)) runs this validator on a new `validated_products` collection and tests one valid and one invalid insert.

## Success criteria

- [ ] All six fields are required
- [ ] Price is decimal with minimum 0
- [ ] Boolean and Date types are correct
