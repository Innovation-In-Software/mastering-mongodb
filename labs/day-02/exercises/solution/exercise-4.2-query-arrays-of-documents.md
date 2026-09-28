# Exercise 4.2 — solution (instructor)

**Module 4** · Day 2 · Checkpoint B  
**Type:** hands-on · **Do not hand this sheet to participants.**

Worksheet: [`../exercise-4.2-query-arrays-of-documents.md`](../exercise-4.2-query-arrays-of-documents.md) · Deck slide 47

## Running it

Fifteen minutes in `mongosh` on a fresh load. If anyone ran the positional-update demo on O5001 (`items.$.quantity` → 2), the trap is gone: reload `load.js` first.

The trap document:

```text
{ orderNumber: 'O5001', items: [ { sku: 'L100', quantity: 1 }, { sku: 'A410', quantity: 2 } ] }
```

## Task 1 — Steps 1 and 2

### Step 1 → four orders contain L100

**O5001, O6101, O6301, O6401.** `O6301` (a laptop and a USB Hub) is the one people miss.

### Step 2 → six orders have some item with quantity ≥ 2

| Order | The item with quantity ≥ 2 |
| --- | --- |
| O5001 | A410 × 2 |
| O6103 | B300 × 2 |
| O6201 | A400 × 2 |
| O6302 | S200 × 2 |
| O6305 | A410 × 3 |
| O6401 | L100 × 2 |

## Task 2 — Steps 3 and 4

| Step | Result |
| --- | --- |
| 3. `$elemMatch: { sku: "L100", quantity: { $gte: 2 } }` | **O6401 only** — Luis Romero's order for two laptops |
| 4. `"items.sku": "L100", "items.quantity": { $gte: 2 }` | **O5001 and O6401** |

## Task 3 — The false positive

**O5001.** With dot notation each condition is tested against the whole array: the L100 line (quantity 1) satisfies `"items.sku": "L100"`, and the A410 line (quantity 2) satisfies `"items.quantity": { $gte: 2 }`. Different elements, so the order matches. `$elemMatch` requires one element to pass both, and no single O5001 item is L100 with quantity 2 or more.

The other four orders from step 2 have no L100 at all, so they drop out of step 4.

## Task 4 — Step 5

```text
{ customerNumber: 'C101', name: { first: 'Aisha', last: 'Khan' } }
```

**C101.** `type` must be the uppercase `"SHIPPING"`; `"shipping"` matches nothing. (C412 ships to Montreal, and C515's only address is a BILLING address in Ottawa.)

## What you want to hear

- The false positive is named — O5001 — with the two items that caused it.
- `$elemMatch` wraps the conditions on the array field (`items`), and the inner field names drop the `items.` prefix.
- The filter selects the order; the returned order still contains every item. To return only the matching line, use `$elemMatch` in the projection.
