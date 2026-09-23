# Exercise 6.1 — solution (instructor)

**Module 6** · Day 3 · Checkpoint A  
**Type:** design discussion · **Do not hand this sheet to participants.**

Worksheet: [`../exercise-6.1-apply-equality-sort-range.md`](../exercise-6.1-apply-equality-sort-range.md) · Deck slide 46

## Running it

Fifteen minutes. Pairs label the three shapes, then the class compares. Reveal the "Solution (after debrief)" column only after groups share. `mongosh` is optional.

## Tasks 1–3 — Solution

| Shape | Equality | Sort | Range | Index |
| --- | --- | --- | --- | --- |
| A | `category`, `active` | `price` (ascending) | `price` ≤ 100 | `{ category: 1, active: 1, price: 1 }` |
| B | `customerId` | `createdAt` (descending) | `createdAt` in the range | `{ customerId: 1, createdAt: -1 }` |
| C | `paymentStatus` | `createdAt` (descending) | `createdAt` ≥ start | `{ paymentStatus: 1, createdAt: -1 }` |

Slide summary: A `{ category: 1, active: 1, price: 1 }` · B `{ customerId: 1, createdAt: -1 }` · C `{ paymentStatus: 1, createdAt: -1 }` · Equality first partitions the keys · No index leads with a range.

**The shared field (Task 2).** In B, `createdAt` is both the sort and the range. It appears **once**, as the second key, in the sort direction. The same is true of `price` in A.

**Names used in the course.** A is `idx_products_category_active_price` (Lab 5, Step 7). B is `idx_orders_customer_date` (Lab 5, Steps 2–3) — the one history-index name used everywhere. C is `idx_orders_payment_created` (Lab 5, Step 12).

## Task 4 — Why paymentStatus leads in C

`paymentStatus` has only three values on a fresh load (13 PAID, 3 PENDING, 1 FAILED). Putting the equality first still partitions the index, so the date sort and range walk **one status's keys in date order** instead of mixing statuses and filtering them out. An index that led with `createdAt` would read every order in the date range, of every status.

## If someone runs it (fresh `training_store`)

| Shape | Result | With the proposed index |
| --- | --- | --- |
| A | Wireless Mouse (A410, 19.99), USB Hub (A400, 24.99), Wireless Keyboard (P1001, 49.99) | `FETCH` ← `IXSCAN` · 3 keys · 3 docs · 3 returned · no `SORT` |
| B, C101, 1 Aug – 1 Oct 2026 | O5001, O6306, O6301, O6201 (newest first) | `FETCH` ← `IXSCAN` · 4 keys · 4 docs · 4 returned · no `SORT` |
| C, PAID since 1 Sep 2026 | O6306, O6305, O6304, O6303, O6302, O6301 | `FETCH` ← `IXSCAN` · 6 keys · 6 docs · 6 returned · no `SORT` |

Before any of these indexes the plans are `SORT` ← `COLLSCAN`: 13 products examined for A, 17 orders examined for B and C.

**XBAD.** The Legacy Cable Pack is an active ACCESSORY, but its price is the **string** `"49.99"`. A numeric range such as `$lte: Decimal128("100")` never matches a string, so A returns three products, not four. Without the price range (Lab 5, Step 7) it matches and sorts **after** the numbers.

## What to listen for

- "Range first because it is the most selective" — no: a range before the sort field breaks the index order and brings back a `SORT` stage.
- Listing `createdAt` twice (`{ customerId: 1, createdAt: -1, createdAt: 1 }`) — one field, one position.
- "`paymentStatus` is low selectivity, so leave it out" — then C has no equality to narrow on; low selectivity is a reason to put it **inside** a compound index, not a reason to skip it.
- Forgetting `active` in A, or putting it after `price`.

## Debrief points

- ESR is a strong **first** design, not a law. Confirm it with `explain("executionStats")`.
- The signal to look for after creating each index: `IXSCAN`, no `SORT`, and keys ≈ documents ≈ returned.
