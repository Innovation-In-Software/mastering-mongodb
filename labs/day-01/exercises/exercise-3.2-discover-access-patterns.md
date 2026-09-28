# Exercise 3.2 — Discover Application Access Patterns

**Module 3** (Data Modeling with MongoDB) · Day 1 · **Checkpoint B**  
**Deck:** `decks/pptx_new/MongoDB_Module03_Data_Modeling_with_MongoDB.pptx`, slide 43  
**Time:** 15 min · **Type:** design (pairs) · **MongoDB needed:** no

**Objective:** Turn vague requirements into concrete access patterns: how often each runs, what it returns together, and what that means for the document shape.

---

## Scenario

The store must support product search, product pages, customer profiles, order placement, order history, reviews and inventory display.

---

## Do this

1. Name the three most frequent reads.
2. For each, write the data it must return together in one response.
3. Fill four or more rows of the table below. Two rows are started for you.
4. In the last column, mark **embed**, **reference** or **snapshot**.

| Access pattern | Frequency | Returned together | Modeling implication |
| --- | --- | --- | --- |
| Find product by SKU | High | Product details | Single product document |
| Retrieve order | High | Items, totals, address | Embed order aggregate |
| | | | |
| | | | |
| | | | |

Add at least: a customer's order history, a product's reviews (paginated), and any value you must preserve as it was at purchase time.

## Expected result

A table of at least four rows. "Returned together" names specific fields (for example items, totals, address, status), never "everything". At least one row says embed and one says reference.

## Reference solution

After the debrief, compare with [Exercise 3.2 solution](solution/exercise-3.2-discover-access-patterns.md).

## Lab connection

Lab 2, Step 7 ([LAB-2-GUIDE.md](../lab2/LAB-2-GUIDE.md)) checks that the main queries from this table can run against `training_store`.

## Success criteria

- [ ] At least four access patterns are listed
- [ ] "Returned together" is specific, not "everything"
- [ ] At least one row says embed and one says reference
