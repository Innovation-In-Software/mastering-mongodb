# Exercise 4.4 — solution (instructor)

**Module 4** · Day 2 · Checkpoint D  
**Type:** analysis and rewrite · **Do not hand this sheet to participants.**

Worksheet: [`../exercise-4.4-correct-unsafe-operations.md`](../exercise-4.4-correct-unsafe-operations.md) · Deck slide 49

## Running it

Ten minutes, mostly discussion. **Nobody runs the unsafe commands.** Counts are for a fresh load.

## Command 1 — `updateMany({}, { $set: { active: false } })`

**Damage:** the empty filter matches every product, so **all 13 products go inactive** — the whole catalog disappears from any `active: true` page.

**Safer:**

```javascript
const f = { tags: "discontinued" }
db.products.find(f, { _id: 0, sku: 1, active: 1 })   // { sku: 'L190', active: false }
db.products.countDocuments(f)                         // 1
db.products.updateMany(f, { $set: { active: false } })
```

The preview and count show **1** product, L190. The update returns `matchedCount: 1, modifiedCount: 0` on a fresh load, because L190 is already inactive — matched is not modified. A `discontinuedAt: { $exists: true }` filter is equally good in a schema that has that field (training_store does not).

## Command 2 — `deleteMany({})`

**Damage:** **all 17 orders are deleted**, and a shell delete cannot be undone.

**Safer:** never use an empty delete filter. Filter on the test `orderNumber` values, and use one variable for all three commands:

```javascript
const testOrders = { orderNumber: { $in: ["TEST-001", "TEST-002"] } }
db.orders.find(testOrders, { _id: 0, orderNumber: 1 })
db.orders.countDocuments(testOrders)    // note the number
db.orders.deleteMany(testOrders)        // deletedCount must equal that number
```

On a fresh load there are no test orders, so the count is 0 and the delete removes nothing — the correct outcome. If `deletedCount` differs from the count, stop and investigate. Use `deleteOne()` when exactly one document should go.

## Command 3 — `$set: { contact: { email: … } }`

**Damage:** `$set` on the parent object **replaces the whole `contact` object**, so **C101 loses her phone** (`+1-555-0100`).

Before: `{ contact: { email: 'aisha@example.com', phone: '+1-555-0100' } }`  
After the unsafe command: `{ contact: { email: 'new@example.com' } }`

**Safer — use `"contact.email"` instead:**

```javascript
db.customers.updateOne(
  { customerNumber: "C101" },
  { $set: { "contact.email": "new@example.com" } }
)
```

Result: `matchedCount: 1, modifiedCount: 1`; `contact` becomes `{ email: 'new@example.com', phone: '+1-555-0100' }`. If a learner does run this rewrite, reload before Lab 3 so C101's email matches the lab.

## What you want to hear

- The blast radius as a number: 13 products, 17 orders, one lost phone.
- The routine for 1 and 2: preview → count → write with the **same** filter → compare the result with the count.
- Dotted paths change one embedded field; `$set` on the parent replaces it.
