# Exercise 3.8 — solution (instructor)

**Module 3** · Day 1 · Checkpoint H · slide 49  
**Type:** design · **Do not hand this sheet to participants.**

## Answer

```javascript
{
  $jsonSchema: {
    bsonType: "object",
    required: ["sku", "name", "category", "price", "active", "createdAt"],
    properties: {
      sku:       { bsonType: "string" },
      name:      { bsonType: "string" },
      category:  { bsonType: "string" },
      price:     { bsonType: "decimal", minimum: 0 },
      active:    { bsonType: "bool" },
      createdAt: { bsonType: "date" }
    }
  }
}
```

This is exactly the validator Lab 2 Step 6 creates on `validated_products`.

| Slide solution line | Detail |
| --- | --- |
| Six required field names | `sku`, `name`, `category`, `price`, `active`, `createdAt` |
| `price`: decimal, minimum 0 | `decimal` is the `$jsonSchema` name for Decimal128. Not `double`, not `string`, not `number` (which accepts any numeric type). |
| `active`: bool · `createdAt`: date | Not `Boolean` / `Date` — those are mongosh names, not `bsonType` names. |
| `bsonType: "object"` at the top | The document itself is an object. |
| Extra fields still allowed | No `additionalProperties: false`, so `attributes`, `tags` and so on pass. |

### Level and action (optional)

The defaults are `validationLevel: "strict"` (check every insert and update) and `validationAction: "error"` (reject). `moderate` skips documents that are already invalid; `warn` stores the write and logs a warning. Use them only while old data is being fixed:

```javascript
db.runCommand({
  collMod: "validated_products",
  validationLevel: "moderate",
  validationAction: "warn" })
```

## What you want to hear

Six required names, `decimal` for price with `minimum: 0`, `bool` and `date`. The most common mistakes are writing `Decimal128`, `Boolean` or `Date` as the `bsonType`, and using `double` for price. The diagram on slide 33 uses `number`; the lab is stricter.
