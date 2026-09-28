# Exercise 3.3 — solution (instructor)

**Module 3** · Day 1 · Checkpoint C · slide 44  
**Type:** discussion · **Do not hand this sheet to participants.**

## Answer

| # | Relationship | Choice | Why |
| --- | --- | --- | --- |
| 1 | Primary contact information | **Embed** | Owned by the customer, small, read with the profile (`contact` in `training_store`). |
| 2 | Complete order history | **Reference** | Grows without limit; each order stores `customerId`. |
| 3 | Order line items | **Embed** | Bounded, belongs to one order, read with it (`items` in `training_store`). |
| 4 | A product's millions of reviews | **Reference** | Unbounded; would hit the 16 MiB document limit. Each review stores `productId`. |
| 5 | An employee's office address | **It depends** | Embed if each employee has their own; reference if many employees share one office record that changes independently. |
| 6 | Blog post tags | **Embed** | A small, bounded array of values owned by the post. |
| 7 | Purchase-time product price | **Embed (snapshot)** | Must keep what the customer paid; it must not follow later catalog changes (`items[].unitPrice`). |
| 8 | Complete transaction history | **Reference** | Grows without limit. |

Slide solution line: **1 Embed · 2 Reference · 3 Embed · 4 Reference · 5 Depends on reuse · 6 Embed · 7 Embed (snapshot) · 8 Reference.**

## What you want to hear

- The justification says **bounded** or **unbounded**, not "it looks nested".
- Contact information, line items and tags are embedded; order history, millions of reviews and a complete transaction history are referenced because they grow without limit.
- Relationship 5 is the only "it depends", and the deciding question is **reuse**: is the office shared and changed independently?
- Relationship 7 is embedded on purpose even though the product price changes — this is the "Sometimes" under Embed on the "How to Choose Between Them" slide (slide 21).
