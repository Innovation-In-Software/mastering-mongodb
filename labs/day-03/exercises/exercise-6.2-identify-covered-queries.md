# Exercise 6.2 — Identify Covered Queries

**Module 6** (Indexing and Query Performance) · Day 3 · **Checkpoint B**  
**Time:** 15 min · **Type:** design discussion · **Difficulty:** Intermediate

**Deck:** `decks/pptx_new/MongoDB_Module06_Indexing_and_Query_Performance.pptx` — slide 47, "Exercise 6.2 — Identify Covered Queries"

## Purpose

Decide which projections the index can answer **alone**, without reading a single document, and name the `explain()` signal that proves it.

## Prerequisites

- Module 6, Part 5: "Covered Queries" and "Proving Coverage in mongosh"
- Paper or a notes file
- You do **not** need MongoDB running. Lab 5, Step 11 lets you test your answers in `mongosh`.

## Scenario

The index `{ category: 1, price: 1, name: 1 }` exists on `products`. Decide which queries can be covered.

```javascript
// Q1
db.products.find({ category: "BOOK" },
                 { _id: 0, name: 1, price: 1 })

// Q2
db.products.find({ category: "BOOK" },
                 { _id: 0, name: 1, price: 1, tags: 1 })

// Q3
db.products.find({ category: "BOOK" },
                 { name: 1 })
```

## Tasks

### Task 1 — Decide coverage for Q1

Covered or not? One-line reason.

### Task 2 — Decide coverage for Q2 and Q3

Covered or not? One-line reason for each. Name the field that causes the problem.

### Task 3 — Write the three coverage conditions

Complete: "A query is covered when …, … and …"

### Task 4 — Name the explain() signal to look for

Which stages and which number in `explain("executionStats")` prove that a query was covered?

## Deliverable

| Query | Covered? | Reason |
| --- | --- | --- |
| Q1 | | |
| Q2 | | |
| Q3 | | |

Three conditions:

1.
2.
3.

explain() signal:

## Expected outcome

- Exactly one of the three queries can be covered.
- `_id` is part of your answer.
- You say you would **confirm** with `explain()`, not by reading the query.

The instructor reveals the solution only after the debrief.

## Success criteria

- [ ] Q1 is the only query marked as covered
- [ ] `_id` exclusion is mentioned
- [ ] `explain()` is required for confirmation
