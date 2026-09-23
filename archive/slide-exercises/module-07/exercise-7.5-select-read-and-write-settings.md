# Exercise 7.5: Select Read and Write Settings

**Module 7:** Introduction to Replication and Sharding  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 7)  
**Time:** 20 min  
**Difficulty:** Intermediate

**Objective:** Choose read preference, read concern, and write concern for six business operations and justify staleness versus durability.

---

## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Capture answers in a notes file.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional |
| Timer | Instructor clocks this | — |

You may inspect `training_store` or `rs.status()` to test ideas. Reasoning is the deliverable unless a step asks you to run a command.


---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Critical money paths

**Do this:** For **payment confirmation** and **financial reconciliation**, choose read preference, read concern, and write concern. State what you refuse to trade away.

**Expected result:** Payment: read `primary` (or primaryPreferred only with a documented reason), write concern `majority`, read concern `majority` or `snapshot` in a transaction. Reconciliation: same freshness/durability bias — not secondary reads of unpaid lag.

---

### Step 2 — Catalog, status, reporting

**Do this:** For **product-catalog browsing**, **customer order status**, **operational reporting**, and **noncritical analytics**, choose settings and one sentence on staleness.

**Expected result:** Catalog: `primaryPreferred` or `nearest` with local/available reads is often acceptable. Order status: prefer primary or majority if the customer just paid. Reporting/analytics: `secondaryPreferred` can be fine if the report may be minutes behind and the secondary has capacity.

---

## Success criteria

- [ ] Payment is not served from a lagging secondary as truth
- [ ] The three settings are not treated as interchangeable
- [ ] Analytics may accept staleness explicitly

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
