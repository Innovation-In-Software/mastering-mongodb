# Exercise 8.3 — solution (instructor)

**Module 8** · Day 3 · Checkpoint C  
**Type:** design · **Do not hand this sheet to participants.**

Worksheet: [`../exercise-8.3-define-rpo-and-rto.md`](../exercise-8.3-define-rpo-and-rto.md) · Deck slide 47

## Running it

Fifteen minutes in pairs. There is no single right number — accept any targets that are time quantities, ranked correctly, and backed by a method that can meet them. Lab 7, Step 4 does a real restore; if the classroom has no Database Tools, Lab 7 uses this exercise's restore proof instead.

## Tasks 1 and 2 — Reference answer

| Data set | RPO | RTO | Backup frequency / method | Reason |
| --- | --- | --- | --- | --- |
| Orders | ≤ 5 minutes | 30–60 minutes | Continuous / oplog-based point-in-time recovery on a replica set, plus daily snapshots | Every lost order is lost revenue and a customer complaint |
| Payments (`orders.paymentStatus`) | ≤ 5 minutes (same as orders) | 30–60 minutes | Same as orders — the state lives in the order document | Money state must match the payment provider |
| Customer profiles | 15–60 minutes | 1–2 hours | Hourly snapshots plus the oplog | Sign-ups and address changes are costly to lose but can be re-entered |
| Product catalog | 24 hours | 4 hours | Nightly `mongodump` or snapshot | Changes are rare and can be rebuilt from the source catalog or `load.js` |
| Reviews | 24 hours | 24 hours | Nightly backup | The most tolerant: nice to keep, not needed to take money |

Slide summary: Orders, payments: RPO in minutes · Catalog: longer RPO is acceptable · Reviews: the most tolerant · Checkout RTO shorter than reviews.

Key rules to check in every answer:

- **Orders and payments** usually get the tightest RPO, in minutes, with **tested point-in-time recovery**.
- The **catalog** can often tolerate a longer RPO because it can be rebuilt.
- **Reviews** are the most tolerant.
- **Checkout's RTO** should be shorter than the RTO for reviews.
- A nightly backup can't meet a 5-minute RPO. Frequency must match the target.
- Replication is **not** a backup: `db.orders.deleteMany({})` reaches every member in seconds.

## Task 3 — Proving an orders restore

Restore into an isolated database, never over `training_store`, then:

```javascript
use training_store_restore
db.orders.countDocuments({})                           // compare with the pre-restore note: 17 on a fresh load
db.orders.findOne({ orderNumber: "O5001" },
  { _id: 0, orderNumber: 1, paymentStatus: 1, total: 1 })
// { orderNumber: 'O5001', paymentStatus: 'PENDING', total: Decimal128('1514.17') }
db.orders.findOne({ orderNumber: "O6101" }, { _id: 0, paymentStatus: 1, total: 1 })
// a paid total: { paymentStatus: 'PAID', total: Decimal128('1483.99') }
db.orders.getIndexes()                                 // _id_ and orderNumber_unique (plus any lab indexes you had)
```

1. **Counts** — `countDocuments` matches the note taken before the restore (17 orders on a fresh load; 13 paid).
2. **A sample order** — find O5001 and check a paid total.
3. **Indexes** — `getIndexes()` shows the unique `orderNumber_unique` index, so duplicates are still refused.
4. **Access** — the application (or `sample-app`) can read an order through its normal connection.
5. **Time** — record how long the restore took and compare it with the RTO.

Backup success alone is not enough: a restore is proven only when the data, the indexes and the application read all check out, in a measured time.

## What you want to hear

- Time quantities, not "high" or "low".
- Orders and payments stricter than reviews.
- A validation plan that checks data **and** access.
