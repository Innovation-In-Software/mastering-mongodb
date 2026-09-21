# Lab 8.8: Monitoring and Log Analysis

**Module 8:** MongoDB Best Practices, Security, and Troubleshooting  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 8)  
**Time:** 25 min  
**Difficulty:** Intermediate

**Objective:** Build an incident timeline from sample metrics and logs, name the first abnormal signal, correlate application and database evidence, propose a likely cause, an alert, and a runbook update.

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

### Step 1 — Build the timeline

**Do this:** Using the sample log and metric extract below, write a timeline with at least four rows: time, signal, source (app or mongod).

**Expected result:** Order is roughly: deploy at 14:02 → query shape change in app logs → documentsExamined rise at 14:04 → slow query log lines → customer checkout latency. No election in the replica-set log.

---

### Step 2 — Name cause and alert

**Do this:** State the likely root cause in one sentence. Write one alert (metric, threshold idea, severity) that would have paged sooner, and one runbook step to add.

**Expected result:** Cause: post-deploy filter no longer matches the index. Alert: slow query rate or examined/returned ratio vs baseline, high severity during checkout hours. Runbook: capture the exact query hash/shape and run explain before adding hardware.

---

### Step 3 — Recommend a dashboard change

**Do this:** Name two tiles that should sit next to each other so this incident is obvious next time.

**Expected result:** Application p99 latency beside mongod slow-ops / documents examined (or query planner collection-scan count). CPU-only would have missed it.

---

## Sample evidence (training fiction)

**Application log**

```text
14:02:11 INFO  deploy checkout-api 3.4.1 started
14:02:18 INFO  queryOrders filter={ status: "paid" }  // was paymentStatus: "PAID"
14:04:02 WARN  GET /orders/history p99=1800ms (baseline 90ms)
```

**mongod log (excerpt)**

```text
14:04:05 I COMMAND  slow query: find orders keysExamined:0 docsExamined:17 nreturned:0 protocol:op_msg 412ms
14:04:06 I COMMAND  slow query: find orders keysExamined:0 docsExamined:17 nreturned:0 protocol:op_msg 390ms
14:05:00 I REPL     member states unchanged; primary store1:27017
```

**Metrics (training fiction)**

| Time  | CPU | Connections | docsExamined/s | Elections |
|-------|-----|-------------|----------------|-----------|
| 13:50 | 12% | 18          | 20             | 0         |
| 14:04 | 28% | 19          | 900            | 0         |
| 14:20 | 27% | 19          | 880            | 0         |

Field-name mismatch (`status` vs `paymentStatus`) plus string case (`paid` vs `PAID`) explains nreturned: 0 with a collection scan.

## Success criteria

- [ ] Timeline has four or more events
- [ ] Election is not blamed
- [ ] Alert and runbook update are specific

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
