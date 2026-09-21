# Exercise 6.13: E-Commerce Index Review

**Module 6:** Indexing and Query Performance  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 6)  
**Time:** 30–45 min  
**Difficulty:** Intermediate

**Objective:** Produce an index recommendation for ten training-store query patterns, including specialized types and overlap checks.

---

## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Capture answers in a notes file.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional |
| Timer | Instructor clocks this | — |

You may use `mongosh` to test ideas, but reasoning is the deliverable. You do not need to create production indexes during discussion exercises.


---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Tabulate ten patterns

**Do this:** For each workload item (SKU lookup, category browse, tags, email, order number, order history, paid reporting, reviews newest first, session expiration, dynamic attributes), write query shape and a proposed index.

**Expected result:** A ten-row table exists. Unique, multikey, partial, TTL, and wildcard candidates are marked.

---

### Step 2 — Justify field order and costs

**Do this:** For every compound index, state ESR roles and one write/storage sentence. Flag any overlapping prefixes (for example category vs category+active+price).

**Expected result:** Compound orders are justified. At least one overlap is called out with a retain/hide plan.

---

### Step 3 — Validation plan

**Do this:** Write how you would prove two high-traffic indexes with explain (catalog and order history) and how you would roll back.

**Expected result:** Baseline → createIndex → executionStats comparison → dropIndex rollback with the original createIndex saved.

---

## Workload checklist

1. Product lookup by SKU  
2. Product browsing by category, active status, and price  
3. Product searches by tag  
4. Customer lookup by email  
5. Order lookup by order number  
6. Customer-order history sorted by date  
7. Paid-order reporting by date  
8. Product-review retrieval sorted newest first  
9. Session expiration  
10. Product search over dynamic category attributes  


## Success criteria

- [ ] Ten query shapes have proposed indexes
- [ ] Specialized types are used appropriately (not everywhere)
- [ ] Overlap and write cost are considered
- [ ] Explain validation is part of the plan

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
