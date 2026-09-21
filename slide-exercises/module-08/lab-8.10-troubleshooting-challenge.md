# Lab 8.10: Troubleshooting Challenge

**Module 8:** MongoDB Best Practices, Security, and Troubleshooting  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 8)  
**Time:** 30 min  
**Difficulty:** Intermediate

**Objective:** Separate five concurrent symptoms into independent problems and produce evidence, investigation order, immediate actions, long-term corrections, and verification steps.

---

## Environment basics (read this first)

**Demonstration environment:** Windows 10/11 · PowerShell in Cursor (``Ctrl+` ``) · `mongosh` connected to the training instance.

| Task | Windows | Where |
|------|---------|-------|
| Open folder | `Ctrl+K Ctrl+O` | File → Open Folder |
| Terminal | ``Ctrl+` `` → PowerShell | Bottom panel |
| MongoDB shell | `mongosh` | Same terminal |

**Prerequisite:** `training_store` is loaded from [`datasets/training_store/load.js`](../../datasets/training_store/load.js). Reload at the start of Day 3 if Day 2 writes remain.

```javascript
use training_store
```

**Scratch database:** Labs that change validation, users, or restored data use `training_store_ops` so `training_store` stays intact for later work.

**Small-data note:** Twelve products and seventeen orders will not produce dramatic wall-clock wins. Record **plan shape**, **examined vs returned**, and **correctness**, not stopwatch time.


---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Separate the incidents

**Do this:** Symptoms: product browsing is slow; some orders are missing from a report; secondary lag is increasing; authentication failures appear in logs; disk utilization is approaching its threshold. Write five problem statements that do **not** assume a single root cause.

**Expected result:** Five independent hypotheses exist (for example: missing catalog index; report `$match` type/status bug; secondary I/O or network; brute force or bad app secret; unbounded growth or large indexes). One sentence each.

---

### Step 2 — Order the investigation

**Do this:** Rank what you would check first for a live checkout site and why. Attach one evidence source per symptom (explain, log field, `rs.printSecondaryReplicationInfo()`, auth log, `db.stats()` / disk).

**Expected result:** Auth failures and disk may be P1 if they threaten availability; lag if oplog is at risk; slow browse if revenue is hurting; missing report rows if finance is blocked. Order is justified.

---

### Step 3 — Actions and verification

**Do this:** For each of the five: one immediate action, one long-term correction, one verification signal.

**Expected result:** Table with 5 rows. Immediate actions are reversible (hide index, rotate a leaked demo password, page storage). Verification is a metric or query result, not ‘looks better’.

---

## Instructor key (share after discussion)

These can all be true at once:

1. **Slow browse** — catalog query missing `{ category: 1, active: 1, price: 1 }` or filter/type mismatch.
2. **Missing report orders** — `paymentStatus` type/case, date TZ boundary, or `$unwind` drop of empty items.
3. **Secondary lag** — backup or compact on the secondary, network, or write burst from a job.
4. **Auth failures** — old URI after rotation, or scanning of a public port (ties to Lab 8.7).
5. **Disk** — journal + dumps on the same volume, or index bloat; not automatically “need sharding.”

## Success criteria

- [ ] Symptoms are not collapsed into one cause
- [ ] Investigation order is justified
- [ ] Each problem has immediate, long-term, and verify steps

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
