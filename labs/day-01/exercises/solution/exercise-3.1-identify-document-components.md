# Exercise 3.1 — solution (instructor)

**Module 3** · Day 1 · Checkpoint A · slide 42  
**Type:** discussion · **Do not hand this sheet to participants.**

## Answer

```javascript
{ _id: ObjectId("..."),            // ObjectId — unique identifier, always indexed
  customerNumber: "C101",          // scalar (String) — business key
  name: { first: "Aisha",          // embedded document with two scalars
          last: "Khan" },
  email: "aisha@example.com",      // scalar (String)
  tags: ["premium", "newsletter"], // Array of strings
  active: true,                    // Boolean
  createdAt: ISODate("...") }      // Date
```

| Slide solution line | Detail |
| --- | --- |
| `_id`: unique in the collection | Every document must have one. mongosh or the driver generates an ObjectId if the application does not supply one. It always has a unique index and cannot be changed after the insert. |
| Scalars: `customerNumber`, `email` | Single values (strings). |
| `name`: embedded, `first` and `last` | A document used as a value. Query it with dot notation: `"name.last"`. |
| `tags` array · `active` · `createdAt` | Array of strings · Boolean · Date. |
| Required: `_id`, `customerNumber`, `name`, `email`, `active`, `createdAt` | `_id` is always present. `tags` is optional — not every customer has tags. |

### Worksheet versus the loaded dataset

The worksheet customer is a teaching sample. The real C101 inserted by Lab 2 Step 3 and by `load.js` is:

```javascript
{ customerNumber: "C101",
  name: { first: "Aisha", last: "Khan" },
  contact: { email: "aisha@example.com", phone: "+1-555-0100" },
  addresses: [ { type: "SHIPPING", street: "100 King Street", city: "Toronto",
                 province: "Ontario", postalCode: "M5X 1A9", country: "Canada" } ],
  preferences: { newsletter: true, language: "English" },
  status: "ACTIVE",
  createdAt: ISODate("2026-09-01T10:00:00Z") }   // load.js; the hand insert uses new Date()
```

Differences to point out: email lives at `contact.email` (and `load.js` puts a unique index `email_unique` on it), `status: "ACTIVE"` replaces the `active` flag, there are no `tags`, and there are an `addresses` array and a `preferences` object. Both are valid designs.

## What you want to hear

- "`_id` is unique in the collection" — bonus if someone adds "indexed automatically" and "immutable".
- `name` is called an embedded (nested) document, not "a field with two fields".
- `createdAt` is a Date, not a string.
- The required list leaves `tags` out.

Run it as ten minutes in pairs; reveal the solution column after two pairs have shared their labels.
