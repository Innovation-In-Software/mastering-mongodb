# Module 7 — Practice exercise solutions

**Deck:** `decks/pptx_new/MongoDB_Module07_Introduction_to_Replication_and_Sharding.pptx`  
**Story:** the `training_store` online store (`datasets/training_store/load.js`)  
Attempt the slide activity first, then compare your answers here.

Official numbered checkpoints for this module:
[Exercise 7.1](../day-03/exercises/exercise-7.1-replication-or-sharding.md) ·
[Exercise 7.2](../day-03/exercises/exercise-7.2-select-read-and-write-settings.md) ·
[Exercise 7.3](../day-03/exercises/exercise-7.3-evaluate-shard-key-candidates.md) ·
[Exercise 7.4](../day-03/exercises/exercise-7.4-targeted-or-scatter-gather.md) ·
and the module's lab, [Lab 6 — Replication and Sharding](../day-03/lab6/LAB-6-GUIDE.md).

Both practice exercises are thought experiments. Failover and sharding commands run only on instructor-controlled, disposable infrastructure; never step down or shard a shared class cluster.

---

## Exercise: Count the Votes

**Slide 17** · **Time:** 10 minutes · **How to run:** pairs for five minutes, then take one answer per set. Point back to the voters / majority / can-lose table on the "Replica-Set Elections" slide.

### Scenario

Decide whether each replica set can still elect a primary. Every member is a voting, data-bearing member.

| Set | Situation |
| --- | --- |
| A | 3 members, 1 down |
| B | 3 members, 2 down |
| C | 4 members, 2 down |
| D | 5 members split 3 \| 2 across two data centers; the link between them fails |

### Tasks

1. Work out the majority for each set.
2. Say whether a primary can exist.
3. Say what happens to writes.
4. Explain why D is split 3 | 2.

### Solution

| Set | Voters | Majority | Reachable | Primary? | Writes |
| --- | --- | --- | --- | --- | --- |
| A | 3 | 2 | 2 | **Yes** — 2 of 3 still vote | Continue after a short election pause |
| B | 3 | 2 | 1 | **No** — the survivor stays SECONDARY | Fail; reads only work with a secondary read preference |
| C | 4 | 3 | 2 | **No** — needs 3 of 4 | Fail |
| D | 5 | 3 | 3 on one side, 2 on the other | **The 3-member side** keeps or elects the primary | Continue on the 3-member side; the 2-member side cannot accept writes |

Slide summary: A yes — 2 of 3 still vote · B no — 1 of 3: no writes · C no — needs 3 of 4 · D the 3-member side elects · Odd voter counts decide cleanly.

### Why this is the answer

A primary needs votes from a **majority of all voting members**, not of the members that are still up — so only one side of a split can ever elect a primary. Four members tolerate one failure, the same as three, which is why odd voter counts (3, 5) are common. For D, teams place a majority of voters — or a tie-breaking member — in a third location, so losing one data center or one link never leaves both sides without a majority.

---

## Exercise: What Did the Customer See?

**Slide 25** · **Time:** 10 minutes · **How to run:** pairs for five minutes. It is a thought experiment on the diagrams from Part 3; nobody runs it on the shared cluster.

### Scenario

Replay a failover during Luis Romero's payment. Order **O6401** (customer C204, two Business Laptops, total 2945.98) has `paymentStatus: "PENDING"`. The payment service sets `paymentStatus` to `PAID` with `w: 1`. The status page reads with `secondaryPreferred`.

```text
10:00:00  PAID written on primary
10:00:00  acknowledged (w: 1)
10:00:01  primary partitioned
10:00:12  secondary elected
10:00:30  old primary rejoins
```

### Tasks

1. State `paymentStatus` on the new primary.
2. Say what happens to the PAID write.
3. Say what the status page showed.
4. Pick the settings you would change.

### Solution

| Task | Answer |
| --- | --- |
| New primary | **PENDING** — the PAID update reached only the old primary; the elected secondary never saw it. |
| The PAID write | **Rolled back** when the old primary rejoins, and saved to a rollback file. The payment service was told it succeeded, so someone must reconcile it by hand. |
| Status page | **PENDING** — first stale (with `secondaryPreferred` it may have shown PENDING even while the old primary had PAID, because of lag), then, after the rollback, PENDING is the true state — but the customer was told the payment went through. |
| Settings to change | Payment writes: **`w: "majority"`** (with a `wtimeout`). Status page right after a payment: **primary reads**, or read concern `majority`. |

The safer write, as on the "Three Settings on training_store" slide (example only — later labs expect O6401 to stay `PENDING`, so don't run it on the shared data):

```javascript
db.orders.updateOne(
  { orderNumber: "O6401" },
  { $set: { paymentStatus: "PAID" } },
  { writeConcern: { w: "majority", wtimeout: 5000 } }
)
```

### Why this is the answer

`w: 1` acknowledges a write once the primary alone has it; if that primary is cut off before a secondary copies the change, the majority moves on without it and the write is undone. A `w: "majority"` write is only acknowledged once it can't be rolled back. Reading the order from the primary (or with read concern `majority`) right after a payment keeps the customer's view true. Exercise 7.2 practises exactly these choices.
