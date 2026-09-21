# Exercise 7.13: Scale the E-Commerce Order Platform

**Module 7:** Introduction to Replication and Sharding  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 7)  
**Time:** 30–45 min  
**Difficulty:** Intermediate

**Objective:** Produce an availability design, sharding decision, shard-key comparison, query-routing analysis, and operational plan for a growing order platform currently on one standalone server.

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

### Step 1 — Availability design

**Do this:** Specify member count, roles, failure-domain placement, election behavior, read preference, write concern, and monitoring. Start from today’s standalone server.

**Expected result:** Move to a replica set of at least three data-bearing voters across failure domains. Default app reads primary; writes majority. Monitor lag, elections, disk, and connections.

---

### Step 2 — Sharding decision and key comparison

**Do this:** Say whether sharding is required **today** vs after evidence. Which collection first? Compare `status`, `createdAt`, `customerId`, hashed `customerId`, `{tenantId, orderId}`, `{tenantId, createdAt}`.

**Expected result:** Do not shard before measuring. Orders first if a replica set cannot hold write/storage growth. Reject `status`. Flag monotonic `createdAt`. Prefer a customer/tenant-leading key.

---

### Step 3 — Routing and operations

**Do this:** Classify: lookup by full shard key; customer-order history; recent orders across all customers; monthly global revenue; tenant-specific reporting. Then list failover tests, backups, lag, distribution, balancer, app retries, and capacity thresholds.

**Expected result:** Full key and customer history: targeted if the key leads with customer/tenant. Recent global and monthly revenue: scatter-gather. Tenant reports: targeted if tenant is the leading field. Ops plan includes backups **and** replica sets (not either/or).

---

## Current situation

- One standalone MongoDB server
- Increasing order volume
- Maintenance downtime
- Customer-order queries and recent-order dashboards
- Global analytical reports
- Several large enterprise tenants
- Continuous operation required

## Success criteria

- [ ] Standalone is replaced for production availability
- [ ] Sharding is evidence-based
- [ ] Six key candidates are compared
- [ ] Query routing and an ops plan exist

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
