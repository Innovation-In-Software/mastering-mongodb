# Exercise 4.3 — Perform an Upsert

**Module 4** (The MongoDB Query Language) · Day 2 · **Checkpoint C**  
**Time:** 10 min · **Type:** hands-on in `mongosh` · **Difficulty:** Intermediate

**Deck:** `decks/pptx_new/MongoDB_Module04_The_MongoDB_Query_Language.pptx` — slide 48, "Exercise 4.3 — Perform an Upsert"

## Purpose

Run the same upsert twice and compare the write results: the first run inserts, the second updates, and `createdAt` is set only once.

## Prerequisites

- Module 4, Part 4 ("The Upsert Pattern" and "Understanding Write Results")
- `training_store` loaded from `datasets/training_store/load.js`. `A700` is **not** in the fresh dataset; if an earlier run created it, reload first:

```powershell
mongosh "mongodb://localhost:27017" .\datasets\training_store\load.js
```

Then `use training_store`, and confirm `db.products.countDocuments({ sku: "A700" })` returns `0`.

## Scenario

A700 is not in the fresh dataset. Run one upsert twice and compare the write results.

```javascript
db.products.updateOne(
  { sku: "A700" },
  {
    $set: {
      name: "Portable Charger",
      category: "ACCESSORY",
      price: Decimal128("39.99"),
      active: true,
      updatedAt: new Date()
    },
    $setOnInsert: { createdAt: new Date(), stockQuantity: 25 }
  },
  { upsert: true }
)
```

## Tasks

### Task 1 — Run the upsert; read the result

Run the command above. Copy the whole write result: `acknowledged`, `insertedId`, `matchedCount`, `modifiedCount` and `upsertedCount`.

### Task 2 — `findOne` A700; note `createdAt`

```javascript
db.products.findOne({ sku: "A700" })
const firstCreatedAt = db.products.findOne({ sku: "A700" }).createdAt
```

Which fields came from the filter, which from `$set` and which from `$setOnInsert`?

### Task 3 — Run the same upsert again

Run the identical `updateOne` from the scenario again (use the up arrow in `mongosh`). Copy the write result, then compare `createdAt`:

```javascript
db.products.findOne({ sku: "A700" }, { _id: 0, sku: 1, createdAt: 1, updatedAt: 1, stockQuantity: 1 })
db.products.findOne({ sku: "A700" }).createdAt.getTime() === firstCreatedAt.getTime()
db.products.countDocuments({ sku: "A700" })
```

### Task 4 — Compare both results in two bullets

Write one bullet for the first run and one for the second. Say why the filter uses `sku`.

## Deliverable

| | Run 1 | Run 2 |
| --- | --- | --- |
| `matchedCount` | | |
| `modifiedCount` | | |
| `upsertedCount` | | |
| `insertedId` | | |
| `createdAt` changed? | — | |

- Run 1:
- Run 2:
- Why filter on `sku`:

## Expected outcome

The solution is revealed on the slide after the debrief. You are done when your two bullets explain insert versus update, and `createdAt` is the same after both runs.

## Success criteria

- [ ] Used the unique `sku` as the upsert filter
- [ ] `createdAt` and `stockQuantity` are set only on insert (`$setOnInsert`)
- [ ] Compared both runs' write results field by field
- [ ] Exactly one A700 document exists after two runs

## Clean up

Lab 3 expects a fresh dataset; reload `load.js` before it (or `db.products.deleteOne({ sku: "A700" })`).

## Next

[Exercise 4.4 — Correct Unsafe Operations](exercise-4.4-correct-unsafe-operations.md)
