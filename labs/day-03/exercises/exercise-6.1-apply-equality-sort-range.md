# Exercise 6.1 — Apply Equality–Sort–Range

**Module 6** (Indexing and Query Performance) · Day 3 · **Checkpoint A**  
**Time:** 15 min · **Type:** design discussion · **Difficulty:** Intermediate

**Deck:** `decks/pptx_new/MongoDB_Module06_Indexing_and_Query_Performance.pptx` — slide 46, "Exercise 6.1 — Apply Equality–Sort–Range"

## Purpose

Three query shapes, three compound indexes. For each shape you label the **equality**, **sort** and **range** fields, then propose one compound index in ESR order.

## Prerequisites

- Module 6, Part 3: "Compound Indexes", "Field Order Matters", "The Prefix Rule" and "Equality, Sort, Range (ESR)"
- Paper or a notes file
- You do **not** need MongoDB running. You may test an idea in `mongosh` on `training_store`, but the reasoning is the deliverable.

## Scenario

Label equality, sort and range in each shape, then propose one compound index per shape.

| Shape | Collection | Query |
| --- | --- | --- |
| **A** | `products` | `category` is `"ACCESSORY"`, `active` is `true`, `price` ≤ 100, sort by `price` |
| **B** | `orders` | one `customerId`, `createdAt` in a date range, sort `createdAt` descending |
| **C** | `orders` | `paymentStatus` is `"PAID"`, `createdAt` ≥ a start date, sort `createdAt` descending |

The same shapes written for `mongosh` (for reference — you don't have to run them):

```javascript
// A
db.products.find({
  category: "ACCESSORY",
  active: true,
  price: { $lte: Decimal128("100") }
}).sort({ price: 1 })

// B — cid is C101's _id: db.customers.findOne({ customerNumber: "C101" })._id
db.orders.find({
  customerId: cid,
  createdAt: { $gte: ISODate("2026-08-01T00:00:00Z"),
               $lt:  ISODate("2026-10-01T00:00:00Z") }
}).sort({ createdAt: -1 })

// C
db.orders.find({
  paymentStatus: "PAID",
  createdAt: { $gte: ISODate("2026-09-01T00:00:00Z") }
}).sort({ createdAt: -1 })
```

## Tasks

### Task 1 — Label E, S and R in shape A

Write which fields are equality, which is the sort and which is the range.

### Task 2 — Label shape B — spot the shared field

Label shape B the same way. One field plays two roles. Which one, and how many times does it appear in the index?

### Task 3 — Propose one index per shape

Write the key specification for A, B and C, in ESR order, with the sort direction.

### Task 4 — Say why paymentStatus leads in C

`paymentStatus` has only a few values. In one sentence, say why it still goes first.

## Deliverable

| Shape | Equality | Sort | Range | Proposed index |
| --- | --- | --- | --- | --- |
| A | | | | |
| B | | | | |
| C | | | | |

Task 4 (one sentence):

## Expected outcome

- Three compound indexes, one per shape.
- Equality fields lead every index.
- A field used for both sort and range appears once.
- No index leads with a range field.

The instructor reveals the solution only after the debrief.

## Lab connection

Lab 5 builds two of these indexes for real: shape A in Step 7 (`idx_products_category_active_price`) and shape C in Step 12 (`idx_orders_payment_created`). Shape B is the order-history index from Steps 2–3 (`idx_orders_customer_date`).

## Success criteria

- [ ] Three candidate indexes exist
- [ ] No design leads with a range field when an equality field is available
- [ ] Same-field sort and range (`createdAt`, `price`) is recognised as one indexed field
- [ ] Task 4 explains why equality comes first even for a low-selectivity field
