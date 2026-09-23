# Exercise 4.3 — solution (instructor)

**Module 4** · Day 2 · Checkpoint C  
**Type:** hands-on · **Do not hand this sheet to participants.**

Worksheet: [`../exercise-4.3-perform-an-upsert.md`](../exercise-4.3-perform-an-upsert.md) · Deck slide 48

## Running it

Ten minutes in `mongosh`. A700 must not exist before run 1 (load.js leaves it free on purpose). ObjectIds and dates below are placeholders; the counts are exact.

## Task 1 — Run 1 inserts

```text
{
  acknowledged: true,
  insertedId: ObjectId('…'),
  matchedCount: 0,
  modifiedCount: 0,
  upsertedCount: 1
}
```

Nothing matched `sku: "A700"`, so MongoDB inserted a new document built from the filter's equality field plus every `$set` and `$setOnInsert` field. **mongosh prints the new `_id` as `insertedId`**; drivers and the server call it `upsertedId`. Products now count 14.

## Task 2 — The inserted document

```text
{
  _id: ObjectId('…'),
  sku: 'A700',                       // from the filter
  name: 'Portable Charger',          // $set
  category: 'ACCESSORY',             // $set
  price: Decimal128('39.99'),        // $set
  active: true,                      // $set
  updatedAt: ISODate('…'),           // $set
  createdAt: ISODate('…'),           // $setOnInsert
  stockQuantity: 25                  // $setOnInsert
}
```

## Task 3 — Run 2 updates

```text
{
  acknowledged: true,
  insertedId: null,
  matchedCount: 1,
  modifiedCount: 1,
  upsertedCount: 0
}
```

Now A700 matches. `modifiedCount` is **1** because `updatedAt` gets a new `new Date()` value; every other `$set` value is unchanged. `$setOnInsert` is skipped on the update path, so `createdAt` and `stockQuantity` (25) keep their first values. The `createdAt` comparison returns `true`, and `countDocuments({ sku: "A700" })` is still `1`.

## Task 4 — The two bullets

- **Run 1:** no match → insert. `matchedCount: 0`, `upsertedCount: 1`, new `_id` shown as `insertedId`; `createdAt`, `updatedAt` and `stockQuantity: 25` all set.
- **Run 2:** match → update. `matchedCount: 1`, `modifiedCount: 1`, `upsertedCount: 0`, `insertedId: null`; only `updatedAt` changed, `createdAt` unchanged.

**Why `sku`:** it has the `sku_unique` index, so the filter can match at most one product and a rerun can never insert a duplicate. Upserting on a field that isn't unique could update the wrong document or insert duplicates.

## What you want to hear

- Insert versus update is read from `matchedCount` / `upsertedCount`, not from `acknowledged`.
- `$setOnInsert` is the reason `createdAt` survives the rerun.
- If run 1 shows `matchedCount: 1`, A700 was left over from an earlier attempt — reload.
- If someone puts `createdAt` in `$set` by mistake, it changes on every run: that is the bug this pattern prevents.
