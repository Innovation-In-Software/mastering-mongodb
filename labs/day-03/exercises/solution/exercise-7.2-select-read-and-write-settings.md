# Exercise 7.2 — solution (instructor)

**Module 7** · Day 3 · Checkpoint B  
**Type:** design discussion · **Do not hand this sheet to participants.**

Worksheet: [`../exercise-7.2-select-read-and-write-settings.md`](../exercise-7.2-select-read-and-write-settings.md) · Deck slide 46

## Running it

Twenty minutes: about twelve in pairs, then a debrief row by row. Reveal the solution only after the groups share. Nobody runs the O6401 update on the shared `training_store` — later labs expect O6401's `paymentStatus` to be `PENDING`.

## Tasks 1 and 3 — Solution

| Operation | Read preference | Read concern | Write concern |
| --- | --- | --- | --- |
| Payment confirmation | `primary` (`primaryPreferred` only with a documented reason) | `majority`, or `snapshot` inside a transaction | `w: "majority"` with a `wtimeout` (optionally `j: true`) |
| Financial reconciliation | `primary` | `majority` (or `snapshot` in a transaction) | `w: "majority"` for any adjustment it writes |
| Product-catalog browsing | `primaryPreferred` or `nearest` | `local` | n/a — read only; catalog edits use the default `w: "majority"` |
| Customer order status | `primary` (right after a payment) | `majority` | n/a — read only; the payment service writes with `w: "majority"` |
| Operational reporting | `secondaryPreferred` | `local` | n/a — read only |
| Noncritical analytics | `secondaryPreferred` | `local` (or `available`) | n/a — read only |

Slide summary: Payment: primary + majority · Reconciliation: same bias · Catalog: primaryPreferred ok · Status: primary after payment · Analytics: secondaryPreferred.

The deck's payment example:

```javascript
db.orders.updateOne(
  { orderNumber: "O6401" },
  { $set: { paymentStatus: "PAID" } },
  { writeConcern: { w: "majority", wtimeout: 5000 } }
)
```

Example only — do not run it on the shared class data.

## Task 2 — What you refuse to trade away

- **Payment confirmation:** durability *and* freshness. A `w: 1` write can be acknowledged and then rolled back after a failover (the "What Did the Customer See?" exercise); a `w: "majority"` write cannot. Reading from the primary with `majority` means the customer never sees a state that is about to disappear.
- **Financial reconciliation:** freshness and consistency. Never reconcile from a lagging secondary: an order paid a few seconds ago would still read as unpaid. On a fresh load `readConcern("majority")` on `{ paymentStatus: "PAID" }` returns **13** orders.

## Task 4 — Staleness sentences (model answers)

| Operation | Staleness accepted |
| --- | --- |
| Payment confirmation | None — a stale or rolled-back answer means charging or shipping on a false state. |
| Financial reconciliation | None — the books must match what a majority has committed. |
| Product-catalog browsing | Seconds are fine; a price or description a few seconds old is harmless, and checkout re-reads the price. |
| Customer order status | None right after payment; later, a few seconds of delay is acceptable. |
| Operational reporting | Minutes are acceptable if the report says so and the secondary has spare capacity. The deck's `SHIPPED` count (6 on a fresh load) may be slightly behind the primary. |
| Noncritical analytics | Minutes or more; the trend matters, not the last order. |

## What to listen for

- The three settings answer three different questions: **where** a read runs, **what** it may return, **how many** members confirm a write. Mixing them up ("use majority read preference") is the most common error.
- Secondary reads may be stale and compete with replication work — they are not "free speed".
- `w: 0` or `w: 1` for payments is a miss, however fast it is.
- Note for sharp groups: since MongoDB 5.0 the default write concern is usually `majority`; the point is to choose it deliberately.

## Debrief points

- Money paths: primary reads, majority reads, majority writes.
- Staleness is accepted only where it is harmless, and it is written down.
