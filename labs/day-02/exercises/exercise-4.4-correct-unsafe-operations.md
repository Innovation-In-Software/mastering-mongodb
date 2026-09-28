# Exercise 4.4 — Correct Unsafe Operations

**Module 4** (The MongoDB Query Language) · Day 2 · **Checkpoint D**  
**Time:** 10 min · **Type:** analysis and rewrite · **Difficulty:** Intermediate

**Deck:** `decks/pptx_new/MongoDB_Module04_The_MongoDB_Query_Language.pptx` — slide 49, "Exercise 4.4 — Correct Unsafe Operations"

## Purpose

Rewrite three dangerous writes. **Don't run them.** Name the blast radius of each command, then replace it with a precise, previewed and counted alternative.

## Prerequisites

- Module 4, Parts 4 and 5 ("Nested $set and a Guarded $inc", "Deleting Documents Safely", "Common Query Mistakes and Safe-Write Habits")
- A notes file for your answers. You may use `mongosh` to run the **read-only** previews and counts; reasoning is the deliverable.

## Scenario

A teammate wants to run these. Rewrite each one instead.

```javascript
// 1
db.products.updateMany({},
  { $set: { active: false } })

// 2
db.orders.deleteMany({})

// 3
db.customers.updateOne(
  { customerNumber: "C101" },
  { $set: { contact:
    { email: "new@example.com" } } })
```

**Do not run any of the three commands above.**

## Tasks

### Task 1 — Name what each command would damage

For each command, write what it would change on a fresh load of `training_store`. These read-only checks help:

```javascript
db.products.countDocuments({})
db.orders.countDocuments({})
db.customers.findOne({ customerNumber: "C101" }, { _id: 0, contact: 1 })
```

### Task 2 — Rewrite 1 with a precise filter

The business goal is to deactivate **discontinued** products only. Write the filter, preview it with `find()`, count it with `countDocuments()`, and only then write the `updateMany` that uses the same filter.

### Task 3 — Rewrite 2 as find → count → delete

The goal is to remove leftover **test** orders only. Put the filter in a variable, then write the three commands — `find`, `countDocuments`, `deleteMany` — using that one variable. Say what you compare `deletedCount` with.

### Task 4 — Rewrite 3 with a dotted path

Rewrite the update so only the email changes and every other `contact` field is kept.

## Deliverable

| Command | What it would damage | Your safer rewrite |
| --- | --- | --- |
| 1. `updateMany({}, …)` | | |
| 2. `deleteMany({})` | | |
| 3. `$set: { contact: { … } }` | | |

## Expected outcome

The solution is revealed on the slide after the debrief. You can name the blast radius of an empty filter, and the difference between replacing an embedded document and setting one path.

## Success criteria

- [ ] Did not execute any of the three unsafe writes
- [ ] Named what each command would damage, with a count
- [ ] Gave a precise, previewed and counted alternative for 1 and 2
- [ ] Used a dotted `$set` path for the nested email

## Next

[Lab 3 — Complex Queries and Updates](../lab3/LAB-3-GUIDE.md)
