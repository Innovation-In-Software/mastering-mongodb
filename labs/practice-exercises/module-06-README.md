# Module 6 — Practice exercise solutions

**Deck:** `decks/pptx_new/MongoDB_Module06_Indexing_and_Query_Performance.pptx`  
**Story:** the `training_store` online store (`datasets/training_store/load.js`), freshly loaded  
Attempt the slide activity first, then compare your answers here.

Official numbered checkpoints for this module:
[Exercise 6.1](../day-03/exercises/exercise-6.1-apply-equality-sort-range.md) ·
[Exercise 6.2](../day-03/exercises/exercise-6.2-identify-covered-queries.md) ·
[Exercise 6.3](../day-03/exercises/exercise-6.3-e-commerce-index-review.md).
Official lab: [Lab 5 — Index and Explain](../day-03/lab5/LAB-5-GUIDE.md).

---

## Exercise: Index the Fulfillment Queue

**Slide 21** · **Time:** 10 minutes · **How to run:** pairs for five minutes, then compare. If `mongosh` is open, run the explain before and after. This is Lab 5, Step 4 — a query shape the history index can't serve.

### Scenario

Warehouse staff list PROCESSING orders, oldest first. `idx_orders_customer_date` already exists.

```javascript
db.orders.find(
  { fulfillmentStatus: "PROCESSING" }
).sort({ createdAt: 1 })
```

### Tasks

1. Label the equality and the sort field.
2. Say why `idx_orders_customer_date` can't help.
3. Write the `createIndex` command, with a name.
4. Predict the results and the new plan.

### Solution

| Task | Answer |
| --- | --- |
| E and S | **E:** `fulfillmentStatus` · **S:** `createdAt` (ascending). No range. |
| Why not the history index | Its leading field is `customerId`, and this query doesn't filter on `customerId`, so `fulfillmentStatus` is not a prefix. |
| Command | `db.orders.createIndex({ fulfillmentStatus: 1, createdAt: 1 }, { name: "idx_orders_fulfillment_date" })` — equality first, then the sort in its direction. |
| Results | **O6202** (11 August), **O6302** (7 September), **O6401** (18 September) |
| Plan before | `SORT` ← `COLLSCAN` · 0 keys · 17 docs · 3 returned |
| Plan after | `FETCH` ← `IXSCAN idx_orders_fulfillment_date` · 3 keys · 3 docs · 3 returned · **no `SORT`** |

Slide summary: E: fulfillmentStatus · S: createdAt · Its leading field is customerId · `{ fulfillmentStatus: 1, createdAt: 1 }` · Named idx_orders_fulfillment_date · O6202, O6302, O6401 — IXSCAN, no SORT.

### Why this is the answer

Every important query shape needs an index that **leads with its own equality fields**. `createdAt: -1` would also work (an index can be walked backwards), but matching the sort direction keeps it easy to read.

### Common wrong answers

- `status: "Processing"` with `orderedAt` — the content-source spelling. Our orders use `fulfillmentStatus`, upper-case values and `createdAt`.
- `{ createdAt: 1, fulfillmentStatus: 1 }` — sort field first; the scan would walk every order by date and filter out most of them.
- Adding `fulfillmentStatus` to the history index (`{ customerId: 1, fulfillmentStatus: 1, createdAt: 1 }`) — still leads with `customerId`, so still not a prefix for this query.

---

## Exercise: Diagnose Three Plans

**Slide 36** · **Time:** 10 minutes · **How to run:** individually for three minutes, then discuss. Ask for the ratio of documents examined to documents returned for each plan.

### Scenario

Three `explain("executionStats")` summaries on a fresh `training_store`. A: `name` "USB Hub". B: PROCESSING orders by date. C: `tags` "wireless".

```text
A  COLLSCAN
   keys 0 · docs 13 · returned 1
B  SORT ← COLLSCAN
   keys 0 · docs 17 · returned 3
C  FETCH ← IXSCAN idx_products_tags
   keys 2 · docs 2 · returned 2
```

### Tasks

1. Mark each plan targeted or wasteful.
2. Propose a fix for A.
3. Propose a fix for B.
4. Say why C needs no change.

### Solution

| Plan | Verdict | Ratio docs : returned | Fix |
| --- | --- | --- | --- |
| A — `find({ name: "USB Hub" })` | **Wasteful** | 13 : 1 | Index `name` (for example `{ name: 1 }` as `idx_products_name`) **if** the application really searches by name — then `IXSCAN`, 1 · 1 · 1. Or change the query to `find({ sku: "A400" })`, which `sku_unique` already serves. |
| B — `find({ fulfillmentStatus: "PROCESSING" }).sort({ createdAt: 1 })` | **Wasteful** | 17 : 3, plus an in-memory sort | `idx_orders_fulfillment_date` = `{ fulfillmentStatus: 1, createdAt: 1 }` → `FETCH` ← `IXSCAN`, 3 · 3 · 3, and the `SORT` disappears. |
| C — `find({ tags: "wireless" })` | **Targeted** | 2 : 2 | None. 2 keys, 2 documents, 2 results — the Wireless Keyboard (P1001) and the Wireless Mouse (A410). It is already as good as it gets. |

Slide summary: A and B wasteful · C targeted · A: index name, or query by sku · B: idx_orders_fulfillment_date · B's SORT disappears with it · C: 2 : 2 : 2 already.

### Why this is the answer

Read **stage, keys, documents and returned together** — any one alone can mislead. A `COLLSCAN` on 13 documents is fast today, but the ratio shows it reads every product for one result; a `SORT` stage shows the order came from memory, not from an index.

### One more case to discuss

An `IXSCAN` that examines 50,000 keys to return 10 results. Using an index doesn't make a plan efficient: the key order may be wrong (for example a range or sort field before the equality) or the leading field may not be selective. Fix the index order with ESR, then explain again.

### Common wrong answers

- "A is fine, it only took 0 ms" — timings on 13 documents prove nothing; read the counts.
- "C uses 2 keys for 2 results, so it could be covered" — it returns whole documents, and `tags` is multikey, so it can't be covered.
- Fixing B with `hint()` — a hint can't use an index that doesn't exist, and a permanent hint is not a fix.
