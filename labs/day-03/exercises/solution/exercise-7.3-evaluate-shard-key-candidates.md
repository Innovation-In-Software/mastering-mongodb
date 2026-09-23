# Exercise 7.3 — solution (instructor)

**Module 7** · Day 3 · Checkpoint C  
**Type:** design discussion · **Do not hand this sheet to participants.**

Worksheet: [`../exercise-7.3-evaluate-shard-key-candidates.md`](../exercise-7.3-evaluate-shard-key-candidates.md) · Deck slide 47

## Running it

Twenty minutes: about twelve in pairs, then debrief the table candidate by candidate. Use `training_store.orders` as the mental model: few statuses, many customers, dates that only increase. The exact scores are judgment calls — accept ±1 if the reason is right; reject answers whose reasoning is wrong.

## Task 1 — Reference scores

5 = best. For **hotspot risk**, 5 = low risk.

| Candidate | Card. | Distrib. | Write scale | Targeting | Hotspot risk | Locality | Growth | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `{ paymentStatus: 1 }` | 1 | 1 | 1 | 2 | 1 | 2 | 1 | **Rejected** — 3 values, most orders `PAID` |
| `{ createdAt: 1 }` | 5 | 2 | 1 | 3 | 1 | 4 | 2 | **Write hotspot** — every insert lands in the last range |
| `{ customerId: 1 }` | 4 | 3 | 4 | 5 | 3 | 4 | 3 | Good for history; a huge customer concentrates data |
| `{ customerId: "hashed" }` | 4 | 5 | 5 | 3 | 5 | 1 | 4 | Even writes; equality targeted, ranges scatter |
| `{ tenantId: 1, orderNumber: 1 }` (what-if) | 4 | 3 | 4 | 4 | 3 | 3 | 4 | Works only if queries lead with the tenant |
| `{ customerId: 1, createdAt: 1 }` | 5 | 4 | 4 | 5 | 4 | 5 | 4 | **Recommended** |

Slide summary: paymentStatus: rejected · createdAt: write hotspot · Hashed: even, no ranges · Pick customerId + createdAt · Risks: big customers, reports.

### Reasons, candidate by candidate

- **`paymentStatus`** has three values — `PAID`, `PENDING`, `FAILED` — so it can make at most three ranges, and **13 of 17** orders are `PAID`: one bucket holds most of the data and cannot be split. Poor targeting too: the hot query filters by customer, not status. (`fulfillmentStatus` has the same problem with its four values, and is the candidate on the deck's comparison slide and in Lab 6.)
- **`createdAt` (ranged)** has high cardinality, but it is **monotonic**: every new order has the largest `createdAt` so far, so every insert goes to the newest range on one shard. Date-range reports are targeted, which is its one strength.
- **`customerId`** targets one customer's history (the Module 6 query), but a very large customer can concentrate data and writes on one range.
- **Hashed `customerId`** spreads writes evenly and keeps equality lookups (`{ customerId: c._id }`) targeted, but adjacent customers land on different shards, so ranges on `customerId` scatter.
- **`{ tenantId: 1, orderNumber: 1 }`** — `training_store` has **no** `tenantId`; this is a what-if for multi-tenant platforms. Its second field is the real `orderNumber` (such as `O6401`). It targets well only if every query leads with `tenantId`, and one large tenant becomes a hotspot.
- **`{ customerId: 1, createdAt: 1 }`** keeps each customer's orders together in date order, so the history query and a customer's date range are targeted. Ranged writes per customer are usually fine, because many customers write at once.

## Tasks 2 and 3

- **Rejected:** `{ paymentStatus: 1 }` — low cardinality and high frequency of `PAID`.
- **Flagged:** `{ createdAt: 1 }` — monotonic; the shard owning the highest range takes every insert.

## Task 4 — Recommendation

`{ customerId: 1, createdAt: 1 }`, or hashed `customerId` if even write spread matters more than date ranges within a customer. Both are defensible; the deck's pick is the compound key because it matches Module 6's history index `{ customerId: 1, createdAt: -1 }`.

Risks to monitor:

1. **Very large customers** — one customer's range can grow hot or large (jumbo ranges).
2. **Scatter-gather global reports** — anything filtered by status or date without `customerId` asks every shard.

Also acceptable: resharding cost if the workload changes; validating with production-like data before choosing.

## What to listen for

- "Status is a good key because we query by status" — cardinality and frequency beat query convenience.
- "Dates are unique, so createdAt is fine" — cardinality is not the only criterion; monotonic values create a write hotspot.
- Any answer that treats `tenantId` or a `region` field as present in `training_store`.

## Debrief points

- No shard key is universally right; score candidates against the real workload.
- A defensible key matches the hot query — and still names the risks you'll monitor.
