# Exercise 8.1 — solution (instructor)

**Module 8** · Day 3 · Checkpoint A  
**Type:** query review · **Do not hand this sheet to participants.**

Worksheet: [`../exercise-8.1-review-a-query-and-projection.md`](../exercise-8.1-review-a-query-and-projection.md) · Deck slide 45

## Running it

Fifteen minutes. Let learners write the query on paper or in a notes file first, then run it on the instructor screen. Reveal the solution column on the slide only after the debrief.

## The customer id

`customerId` is an ObjectId, so the first line is always the lookup:

```javascript
use training_store
const c101 = db.customers.findOne({ customerNumber: "C101" })._id
```

A filter such as `{ customerId: "C101" }` returns **nothing** — that is the most common mistake.

## Tasks 1–3 — The rewritten query

```javascript
db.orders.find(
  { customerId: c101, paymentStatus: "PAID" },
  { _id: 0, orderNumber: 1, fulfillmentStatus: 1, total: 1, createdAt: 1 }
).sort({ createdAt: -1 }).limit(10)
```

Expected output on a fresh load — Aisha Khan's **four** paid orders:

```text
{ orderNumber: 'O6306', fulfillmentStatus: 'SHIPPED',   total: Decimal128('343.33'),  createdAt: ISODate('2026-09-16T14:10:00.000Z') }
{ orderNumber: 'O6301', fulfillmentStatus: 'SHIPPED',   total: Decimal128('1512.23'), createdAt: ISODate('2026-09-03T10:15:00.000Z') }
{ orderNumber: 'O6201', fulfillmentStatus: 'DELIVERED', total: Decimal128('79.07'),   createdAt: ISODate('2026-08-04T09:40:00.000Z') }
{ orderNumber: 'O6101', fulfillmentStatus: 'SHIPPED',   total: Decimal128('1483.99'), createdAt: ISODate('2026-07-08T14:00:00.000Z') }
```

C101 has five orders in total. Her **pending** order **O5001** (2026-09-20, 1514.17) is excluded by `paymentStatus: "PAID"`.

| Part | Answer | Why |
| --- | --- | --- |
| Filter | `{ customerId: c101, paymentStatus: "PAID" }` | Selective: 4 of 17 orders |
| Projection | `{ _id: 0, orderNumber: 1, fulfillmentStatus: 1, total: 1, createdAt: 1 }` | Only what the page shows; `_id: 0` because the page doesn't need it |
| Sort | `.sort({ createdAt: -1 })` | Newest first, deterministic |
| Limit | `.limit(10)` | Bounded page; the next page starts after the last `createdAt` seen |

## Task 4 — The index

```javascript
db.orders.createIndex({ customerId: 1, paymentStatus: 1, createdAt: -1 })
//                      E              E                 S
```

Equality, equality, sort. **Don't lead with `createdAt`** — a date-first index would scan every customer's orders in the date range.

## Optional: show the evidence with explain

```javascript
db.orders.find({ customerId: c101, paymentStatus: "PAID" })
  .sort({ createdAt: -1 })
  .explain("executionStats")
```

| State | Winning plan | Examined | Returned | SORT stage |
| --- | --- | --- | --- | --- |
| Fresh load (only `_id_` and `orderNumber_unique` on orders) | COLLSCAN | 17 documents | 4 | Yes (in memory) |
| With the ESR index | IXSCAN | 4 keys, 4 documents | 4 | No |

If Lab 5's `idx_orders_customer_date` (`{ customerId: 1, createdAt: -1 }`) is still present, the planner may pick it: 5 keys and 5 documents examined, `paymentStatus` filtered in FETCH, 4 returned. That is close enough on this data; the ESR index is exact.

## What you want to hear

- The lookup of C101's ObjectId before the query.
- All four habits: filter, project, sort, limit.
- An index written from the query shape, in ESR order.

If a learner proposes a separate index on each field, point out that MongoDB normally uses one index per query plan, and a single-field `createdAt` index can't serve the equality filter.
