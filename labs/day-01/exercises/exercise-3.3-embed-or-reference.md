# Exercise 3.3 — Embed or Reference?

**Module 3** (Data Modeling with MongoDB) · Day 1 · **Checkpoint C**  
**Deck:** `decks/pptx_new/MongoDB_Module03_Data_Modeling_with_MongoDB.pptx`, slide 44  
**Time:** 15 min · **Type:** discussion (pairs) · **MongoDB needed:** no

**Objective:** Decide eight relationships as Embed or Reference and justify each from ownership, size or growth.

---

## Relationships

| # | Relationship | Embed or Reference | One-line reason |
| --- | --- | --- | --- |
| 1 | Primary contact information | | |
| 2 | Complete order history | | |
| 3 | Order line items | | |
| 4 | A product's millions of reviews | | |
| 5 | An employee's office address | | |
| 6 | Blog post tags | | |
| 7 | Purchase-time product price | | |
| 8 | Complete transaction history | | |

---

## Do this

1. Decide relationships 1–4.
2. Decide relationships 5–8.
3. Justify each with **bounded** or **unbounded** (and ownership) — not just "it feels nested".
4. One relationship is an "it depends". Find it and explain what it depends on.

## Expected result

Eight rows, each with a choice and a reason. Unbounded histories are referenced. The purchase-time price is treated as a snapshot.

## Reference solution

After the debrief, compare with [Exercise 3.3 solution](solution/exercise-3.3-embed-or-reference.md).

## Lab connection

In Lab 2 ([LAB-2-GUIDE.md](../lab2/LAB-2-GUIDE.md)) you will see the same decisions in `training_store`: embedded `addresses` and `items`, referenced `customerId` and `productId`.

## Success criteria

- [ ] Eight rows have a choice and a reason
- [ ] Unbounded histories are referenced
- [ ] The purchase-time price is treated as a snapshot
