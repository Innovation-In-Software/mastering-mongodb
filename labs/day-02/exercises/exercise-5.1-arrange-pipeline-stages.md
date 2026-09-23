# Exercise 5.1 — Arrange Pipeline Stages

**Module 5** (The Aggregation Framework) · Day 2 · **Checkpoint A**  
**Time:** 10 min · **Type:** design, in pairs, on paper  
**Deck:** `decks/pptx_new/MongoDB_Module05_The_Aggregation_Framework.pptx`, slide 47

**Objective:** Put six stages in the right order for a correct top-five-product report.

You do **not** need MongoDB running for this exercise.

---

## Scenario

You need the **top five products by line revenue from paid orders**. Use each stage **once**:

```text
$limit    $unwind   $sort
$match    $group    $set
```

What you know about `training_store` (from the slide "The Fields Every Pipeline Uses"):

- Orders have `paymentStatus` (`PAID`, `PENDING`, `FAILED`). There is no `status` field.
- Each order has an `items` array. Every item has `sku`, `name`, `quantity` and `unitPrice`.
- There is no `lineTotal` field. Line revenue is `quantity × unitPrice`.

---

## Do this

1. **Propose an order** for the six stages.
2. **Describe the documents after each one**: one sentence per stage (how many documents, what each looks like).
3. **Compare with the instructor's reveal** after the debrief.
4. **Explain why `$limit` can't precede `$sort`.**

Worksheet:

| # | Stage | What the documents look like afterwards |
|---|-------|------------------------------------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |
| 6 | | |

Follow-up question: what would a `$match` placed **after** `$group` mean instead?

---

## Expected result

A defensible sequence, not a guess, with one sentence per stage. If two orders could work, note the trade-off. You can say why `$limit` cannot come before `$sort`, and why `$unwind` must come before grouping by SKU.

## Reference solution

After the debrief, compare with the [Exercise 5.1 solution](solution/exercise-5.1-arrange-pipeline-stages.md) (instructor copy).

## Lab connection

The same stage order (filter, expand, compute, group, rank, cut) is the core of Day 2 [Lab 4](../lab4/LAB-4-GUIDE.md).

## Success criteria

- [ ] The stages are in an order that yields a true top five by revenue
- [ ] Each stage has a one-sentence description of its output
- [ ] You can say what `$match` after `$group` would mean instead
