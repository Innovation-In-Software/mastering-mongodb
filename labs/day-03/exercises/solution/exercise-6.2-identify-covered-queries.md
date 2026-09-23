# Exercise 6.2 — solution (instructor)

**Module 6** · Day 3 · Checkpoint B  
**Type:** design discussion · **Do not hand this sheet to participants.**

Worksheet: [`../exercise-6.2-identify-covered-queries.md`](../exercise-6.2-identify-covered-queries.md) · Deck slide 47

## Running it

Fifteen minutes: individually for five, then compare in pairs, then debrief. Lab 5, Step 11 lets learners test the answers in `mongosh`; in the course the index is named `idx_products_category_price_name`.

## Tasks 1 and 2 — Solution

| Query | Covered? | Why |
| --- | --- | --- |
| Q1 `{ _id: 0, name: 1, price: 1 }` | **Yes — may be covered** | Filter on `category`, output `name` and `price`, `_id` switched off: every field is in the index. |
| Q2 `{ _id: 0, name: 1, price: 1, tags: 1 }` | **No** | `tags` isn't in the index, so MongoDB must `FETCH` each document to read it. (`tags` is an array, and a multikey field can't be covered anyway.) |
| Q3 `{ name: 1 }` | **No** | `_id` is returned by default and isn't in the index, so MongoDB fetches the document just to read it. |

Slide summary: Q1 may be covered · Q2 not — tags needs a FETCH · Q3 not — _id returns by default · Filter, output, _id handled · IXSCAN with no FETCH.

"May be" in Q1 is deliberate: coverage is decided by the planner, so you confirm it with `explain()`.

## Task 3 — The three conditions

1. Every **filter** field is in the index.
2. Every **returned** field is in the index.
3. `_id` is **excluded** (`_id: 0`) or is itself part of the index.

Field order doesn't decide coverage — the fields only have to be present. Order still decides which filters and sorts the index serves.

## Task 4 — The explain() signal

`IXSCAN` with **no `FETCH`** above it — the plan is `PROJECTION_COVERED` ← `IXSCAN` — and `totalDocsExamined: 0`.

## If someone runs it (fresh `training_store`, index created)

| Query | Plan (trimmed) | keys · docs · returned |
| --- | --- | --- |
| Q1 | `PROJECTION_COVERED` ← `IXSCAN idx_products_category_price_name` | 2 · **0** · 2 |
| Q2 | `PROJECTION_SIMPLE` ← `FETCH` ← `IXSCAN` | 2 · 2 · 2 |
| Q3 | `PROJECTION_SIMPLE` ← `FETCH` ← `IXSCAN` | 2 · 2 · 2 |

Q1 returns the two books in index order — by price inside BOOK: **Query Cookbook** 39.99, then **MongoDB Fundamentals** 59.99.

## What to listen for

- "Q3 only asks for one field, so it must be covered" — the hidden `_id` is the trap.
- "Q2 is covered because the filter uses the index" — using an index is not the same as being covered; the output needs `tags`.
- Claiming coverage without an `explain()` check.

## Debrief points

- Covered queries are a tuning tool for hot, narrow read paths (a catalog list, a lookup that returns two fields), not a goal for every query.
- Adding fields to an index to cover a query makes the index bigger and every write more expensive — weigh it like any other index.
