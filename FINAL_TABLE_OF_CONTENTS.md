# Mastering MongoDB — Table of Contents

Master lesson and exercise index. Author lab guides and slides against this file. Keep [`course.config.yaml`](course.config.yaml) in sync when module titles or durations change.

Day assignments follow the redistributed schedule in [`README.md`](README.md), not the source outline’s original day split.

---

## At a Glance

| | |
|---|---|
| **Duration** | 3 days (~18 hours) |
| **Modules** | 8 |
| **Lessons** | 53 |
| **Slide exercises** | 144 lab guides in `slide-exercises/` |
| **Day labs** | [`labs/`](labs/README.md) (7 sequenced labs matching the outline + PPT hands-on) |
| **Slide deck (present)** | [`slides/course-complete-marp-with-notes.html`](slides/course-complete-marp-with-notes.html) |
| **Slide deck (source)** | [`slides/course-complete-marp-with-notes.md`](slides/course-complete-marp-with-notes.md) |
| **Cheatsheet** | [`COURSE-CHEATSHEET.md`](COURSE-CHEATSHEET.md) |

### Day 1 — Foundations (~6 hours)

Modules 1–3: why document storage exists, a working instance, and schema design against a sample application dataset.

### Day 2 — Working with data (~6 hours)

Modules 4–5: retrieve and change documents, then reshape them through aggregation pipelines. Same dataset as Day 1.

### Day 3 — Performance and production (~6 hours)

Modules 6–8: index and `explain` the Day 2 workload, then replica sets, sharding, and production-ready operations (security, backup, monitoring, troubleshooting).

---

## Module Index

| # | Day | Module | Format | Duration | Lessons | Exercises | Slide deck |
|---|-----|--------|--------|----------|---------|-----------|------------|
| **1** | Day 1 | Introduction to NoSQL Databases | Concept + lab | ~90 min | 6 | 3 | [`course-complete-marp-with-notes.md`](slides/course-complete-marp-with-notes.md) |
| **2** | Day 1 | Installation and Setup | Concept + lab | ~90–120 min | 6 | 5 | [`course-complete-marp-with-notes.md`](slides/course-complete-marp-with-notes.md) |
| **3** | Day 1 | Data Modeling with MongoDB | Concept + lab | ~180–210 min | 7 | 9 + 7 labs | [`course-complete-marp-with-notes.md`](slides/course-complete-marp-with-notes.md) |
| **4** | Day 2 | The MongoDB Query Language | Concept + lab | 6–7 h full / ~180 min time-boxed | 6 | 14 + 10 labs | [`course-complete-marp-with-notes.md`](slides/course-complete-marp-with-notes.md) |
| **5** | Day 2 | The Aggregation Framework | Concept + lab | ~180–210 min | 8 | 13 + 10 labs | [`course-complete-marp-with-notes.md`](slides/course-complete-marp-with-notes.md) |
| **6** | Day 3 | Indexing and Query Performance | Concept + demo + exercises + labs | 3–3.5 h full / ~120 min time-boxed | 8 | 12 + 11 labs | [`course-complete-marp-with-notes.md`](slides/course-complete-marp-with-notes.md) |
| **7** | Day 3 | Introduction to Replication and Sharding | Concept + lab | ~180–210 min | 8 | 13 + 10 labs | [`course-complete-marp-with-notes.md`](slides/course-complete-marp-with-notes.md) |
| **8** | Day 3 | MongoDB Best Practices, Security, and Troubleshooting | Concept + demo + exercises + labs | 3–3.5 h full / ~90–120 min time-boxed | 8 | 14 + 11 labs | [`course-complete-marp-with-notes.md`](slides/course-complete-marp-with-notes.md) |

---

## Module 1. Introduction to NoSQL Databases

**Day:** Day 1 · **Duration:** ~90 min (75–90 recommended) · **Format:** Concept + lab

**Module goal:** Explain why NoSQL emerged, compare the four major models, describe MongoDB’s document model and architecture, and justify when MongoDB is — and is not — a fit.

**Prerequisites:** None — this is the starting point.

**Slide deck:** [`slides/course-complete-marp-with-notes.md`](slides/course-complete-marp-with-notes.md)

| Lesson | Title | Duration | Exercise |
|--------|-------|----------|----------|
| 1.1 | Why NoSQL emerged | ~15 min | — |
| 1.2 | Four NoSQL database types | ~15 min | — |
| 1.3 | MongoDB documents and architecture | ~20 min | — |
| 1.4 | Choose the appropriate data model | ~15 min | [Exercise 1.1](slide-exercises/module-01/exercise-1.1-choose-the-data-model.md) |
| 1.5 | Convert relational rows into a document | ~20 min | [Exercise 1.2](slide-exercises/module-01/exercise-1.2-rows-to-documents.md) |
| 1.6 | Explore a MongoDB dataset | ~25 min | [Exercise 1.3](slide-exercises/module-01/exercise-1.3-explore-a-mongodb-dataset.md) |

Concept slides 1–24 are Lessons 1.1–1.3 (plus knowledge check). Time-box the three exercises at the lower end if the day must stay near 90 minutes; budget ~120 minutes if Lab 1.3 is fully hands-on on every laptop.

---

## Module 2. Installation and Setup

**Day:** Day 1 · **Duration:** ~90–120 min · **Format:** Concept + lab

**Module goal:** Get every participant connected to a local, containerized, or managed-cloud MongoDB instance, using `mongosh` and Compass, with a verified write-and-read test.

**Prerequisites:** Module 1.

**Slide deck:** [`slides/course-complete-marp-with-notes.md`](slides/course-complete-marp-with-notes.md)

| Lesson | Title | Duration | Exercise |
|--------|-------|----------|----------|
| 2.1 | Deployment options | ~15 min | [Exercise 2.1](slide-exercises/module-02/exercise-2.1-select-a-deployment-option.md) |
| 2.2 | Server, tools, and configuration | ~15 min | Demo 2.1 |
| 2.3 | Connection strings and clients | ~20 min | [Exercise 2.2](slide-exercises/module-02/exercise-2.2-interpret-a-connection-string.md) · Demos 2.2–2.3 |
| 2.4 | First database and documents | ~15 min | Demo 2.4 |
| 2.5 | Security, troubleshooting, and readiness | ~15 min | [Exercise 2.3](slide-exercises/module-02/exercise-2.3-environment-readiness-checklist.md) · [Exercise 2.4](slide-exercises/module-02/exercise-2.4-diagnose-connection-failures.md) · Demo 2.5 |
| 2.6 | Install, connect, and verify | ~40 min | [Exercise 2.5](slide-exercises/module-02/exercise-2.5-install-connect-and-verify.md) |

Concept slides cover deployment, `mongod`, `mongosh`, Compass, connection strings, first documents, credentials, and troubleshooting. Time-box the discussion exercises if the day must stay near 90 minutes; budget ~120 minutes when every laptop completes the install lab.

---

## Module 3. Data Modeling with MongoDB

**Day:** Day 1 · **Duration:** ~180–210 min (3–3.5 h) · **Format:** Concept + lab

**Module goal:** Design document schemas around application access patterns; choose embedding versus referencing with intent; apply named schema patterns and basic validation; populate `training_store` for Day 2.

**Prerequisites:** Module 2 — a working `mongosh` session.

**Slide deck:** [`slides/course-complete-marp-with-notes.md`](slides/course-complete-marp-with-notes.md)

Time-box discussion exercises if the day must stay near 3 hours; budget ~3.5 hours when every laptop completes Labs 3.1–3.7.

| Lesson | Title | Duration | Exercise / demo |
|--------|-------|----------|-----------------|
| 3.1 | Documents, BSON, and flexible schema | ~30 min | Demo 3.1 · [Exercise 3.1](slide-exercises/module-03/exercise-3.1-identify-document-components.md) |
| 3.2 | Designing schemas for access patterns | ~25 min | Demo 3.2 · [Exercise 3.2](slide-exercises/module-03/exercise-3.2-discover-access-patterns.md) |
| 3.3 | Relationships, embedding, and referencing | ~40 min | Demos 3.3–3.4 · [Exercise 3.3](slide-exercises/module-03/exercise-3.3-embed-or-reference.md) · [Exercise 3.4](slide-exercises/module-03/exercise-3.4-model-a-product-catalog.md) · [Exercise 3.5](slide-exercises/module-03/exercise-3.5-model-an-order-document.md) |
| 3.4 | Growth, anti-patterns, validation, and evolution | ~30 min | Demos 3.5–3.6 · [Exercise 3.6](slide-exercises/module-03/exercise-3.6-correct-schema-anti-patterns.md) · [Exercise 3.8](slide-exercises/module-03/exercise-3.8-design-collection-validation.md) |
| 3.5 | Schema design patterns | ~20 min | [Exercise 3.7](slide-exercises/module-03/exercise-3.7-select-a-schema-pattern.md) |
| 3.6 | Create and populate the sample application | ~50 min | [Lab 3.1](slide-exercises/module-03/lab-3.1-create-the-sample-database.md) · [Lab 3.2](slide-exercises/module-03/lab-3.2-populate-products.md) · [Lab 3.3](slide-exercises/module-03/lab-3.3-populate-customers.md) · [Lab 3.4](slide-exercises/module-03/lab-3.4-populate-orders.md) · [Lab 3.5](slide-exercises/module-03/lab-3.5-query-nested-documents.md) · [Lab 3.6](slide-exercises/module-03/lab-3.6-add-collection-validation.md) · [Lab 3.7](slide-exercises/module-03/lab-3.7-validate-the-data-model.md) |
| 3.7 | Challenge, Day 1 wrap, and transition | ~25 min | [Exercise 3.9](slide-exercises/module-03/exercise-3.9-support-ticket-challenge.md) |

---

## Module 4. The MongoDB Query Language

**Day:** Day 2 · **Duration:** 6–7 h full delivery · **Format:** Concept + demo + exercises + labs

In the 3-day package, time-box to **~180 min** (Lessons 4.1–4.3 plus Lab 4.10) when Module 5 shares the afternoon.

**Module goal:** Create, read, update, replace, and delete documents with precise filters, projections, array operators, and verified writes.

**Prerequisites:** Module 3 — populated `training_store` (`products`, `customers`, `orders`, `reviews`). Reload [`datasets/training_store/load.js`](datasets/training_store/load.js) before the labs.

**Slide deck:** [`slides/course-complete-marp-with-notes.md`](slides/course-complete-marp-with-notes.md)

| Lesson | Title | Duration | Hands-on |
|--------|-------|----------|----------|
| 4.1 | Filters, equality, comparison, logic, null/type | ~90 min | Demos 4.1–4.2 · [Ex 4.1](slide-exercises/module-04/exercise-4.1-read-basic-documents.md)–[4.4](slide-exercises/module-04/exercise-4.4-query-missing-and-null.md) · [Lab 4.1](slide-exercises/module-04/exercise-4.15-lab-dataset-verification.md) |
| 4.2 | Arrays, nested documents, `$elemMatch` | ~50 min | Demo 4.3 · [Ex 4.5](slide-exercises/module-04/exercise-4.5-query-arrays.md)–[4.6](slide-exercises/module-04/exercise-4.6-query-arrays-of-documents.md) · [Labs 4.2–4.3](slide-exercises/module-04/exercise-4.16-lab-product-query.md) |
| 4.3 | Projection, cursors, sort, pagination, count | ~45 min | Demo 4.4 · [Ex 4.7](slide-exercises/module-04/exercise-4.7-design-projections.md)–[4.8](slide-exercises/module-04/exercise-4.8-sort-and-paginate.md) · [Lab 4.4](slide-exercises/module-04/exercise-4.18-lab-projection-pagination.md) |
| 4.4 | Inserts and scalar/nested updates | ~55 min | Demos 4.5–4.6 · [Ex 4.9](slide-exercises/module-04/exercise-4.9-insert-new-application-data.md)–[4.10](slide-exercises/module-04/exercise-4.10-update-product-data.md) · [Labs 4.5–4.6](slide-exercises/module-04/exercise-4.19-lab-insert-operations.md) |
| 4.5 | Array updates, replace, upsert | ~50 min | Demos 4.7–4.8 · [Ex 4.11](slide-exercises/module-04/exercise-4.11-modify-arrays.md)–[4.12](slide-exercises/module-04/exercise-4.12-perform-an-upsert.md) · [Labs 4.7–4.8](slide-exercises/module-04/exercise-4.21-lab-array-manipulation.md) |
| 4.6 | Deletes, bulk writes, safety, troubleshooting | ~70 min | Demos 4.9–4.10 · [Ex 4.13](slide-exercises/module-04/exercise-4.13-correct-unsafe-operations.md)–[4.14](slide-exercises/module-04/exercise-4.14-diagnose-query-errors.md) · [Labs 4.9–4.10](slide-exercises/module-04/exercise-4.23-lab-delete-operations.md) · [Challenge](slide-exercises/module-04/exercise-4.25-practical-challenge.md) |

---

## Module 5. The Aggregation Framework

**Day:** Day 2 · **Duration:** ~180–210 min (3–3.5 h) · **Format:** Concept + lab

**Module goal:** Build multi-stage pipelines that filter, reshape, calculate, group, unwind arrays, join collections, and produce facet reports on `training_store`.

**Prerequisites:** Module 4 — fluent `find()` filters and the same collections. Reload [`datasets/training_store/load.js`](datasets/training_store/load.js) so the analytical volume is present (6 customers, 13 products, 17 orders including **13 PAID**, 6 reviews).

**Slide deck:** [`slides/course-complete-marp-with-notes.md`](slides/course-complete-marp-with-notes.md)

Time-box discussion exercises if the afternoon must stay near 3 hours; budget ~3.5 hours when every laptop completes Labs 5.1–5.10.

| Lesson | Title | Duration | Exercise / demo |
|--------|-------|----------|-----------------|
| 5.1 | Pipeline fundamentals | ~25 min | Demo 5.1 · [Exercise 5.1](slide-exercises/module-05/exercise-5.1-arrange-pipeline-stages.md) · [Lab 5.1](slide-exercises/module-05/lab-5.1-aggregation-dataset-verification.md) |
| 5.2 | Filter, reshape, and calculate | ~35 min | Demos 5.2–5.3 · [Exercises 5.2](slide-exercises/module-05/exercise-5.2-build-a-match-stage.md)–[5.4](slide-exercises/module-05/exercise-5.4-create-calculated-fields.md) |
| 5.3 | `$group` and accumulators | ~30 min | Demo 5.4 · [Exercises 5.5](slide-exercises/module-05/exercise-5.5-group-and-calculate-totals.md)–[5.6](slide-exercises/module-05/exercise-5.6-group-by-multiple-dimensions.md) · [Labs 5.2](slide-exercises/module-05/lab-5.2-product-summary-pipeline.md)–[5.3](slide-exercises/module-05/lab-5.3-order-revenue-pipeline.md) |
| 5.4 | Sort, unwind, and top-N | ~30 min | Demo 5.5 · [Exercises 5.7](slide-exercises/module-05/exercise-5.7-analyze-arrays-with-unwind.md)–[5.8](slide-exercises/module-05/exercise-5.8-build-a-top-n-report.md) · [Lab 5.4](slide-exercises/module-05/lab-5.4-product-sales-pipeline.md) |
| 5.5 | `$lookup`, buckets, and `$facet` | ~35 min | Demos 5.6–5.7 · [Exercises 5.9](slide-exercises/module-05/exercise-5.9-join-related-collections.md)–[5.10](slide-exercises/module-05/exercise-5.10-build-a-facet-report.md) · [Labs 5.5](slide-exercises/module-05/lab-5.5-customer-order-summary.md), [5.8](slide-exercises/module-05/lab-5.8-multi-metric-report.md) |
| 5.6 | Dates, nulls, and report patterns | ~25 min | [Labs 5.6](slide-exercises/module-05/lab-5.6-date-based-sales-report.md)–[5.7](slide-exercises/module-05/lab-5.7-price-band-analysis.md) |
| 5.7 | Workflow, optimization, and troubleshooting | ~25 min | Demo 5.8 · [Exercises 5.11](slide-exercises/module-05/exercise-5.11-correct-a-broken-pipeline.md)–[5.12](slide-exercises/module-05/exercise-5.12-optimize-a-pipeline.md) · [Lab 5.9](slide-exercises/module-05/lab-5.9-pipeline-performance-review.md) |
| 5.8 | Challenge, knowledge check, and transition | ~30 min | [Lab 5.10](slide-exercises/module-05/lab-5.10-integrated-aggregation-challenge.md) · [Exercise 5.13](slide-exercises/module-05/exercise-5.13-executive-sales-summary.md) |

---

## Module 6. Indexing and Query Performance

**Day:** Day 3 · **Duration:** 3–3.5 h full delivery · **Format:** Concept + demo + exercises + labs

In the 3-day package, time-box to **~120 min** (Lessons 6.1–6.3 concepts, Demos 6.1–6.4, Labs 6.1–6.4, and Lab 6.11) when Modules 7–8 share the afternoon.

**Module goal:** Design, create, and prove indexes for the Day 2 `training_store` query shapes; read `explain()`; and balance read speed against write and storage cost.

**Prerequisites:** Modules 4 and 5 — the queries and pipeline to tune.

**Slide deck:** [`slides/course-complete-marp-with-notes.md`](slides/course-complete-marp-with-notes.md)

`training_store` is small by design. Teach **plan shape** (`COLLSCAN` vs `IXSCAN`), **examined vs returned** counts, and field order — not wall-clock time.

| Lesson | Title | Duration | Hands-on |
|--------|-------|----------|----------|
| 6.1 | Why indexes exist; COLLSCAN vs IXSCAN | ~25 min | Demo 6.1 |
| 6.2 | Create, inspect, hide, and remove indexes | ~25 min | Demos 6.2, 6.11 |
| 6.3 | Compound indexes and Equality–Sort–Range | ~40 min | Demos 6.3–6.4 · [Ex 6.1](slide-exercises/module-06/exercise-6.1-identify-candidate-indexes.md)–[6.5](slide-exercises/module-06/exercise-6.5-identify-index-prefixes.md) |
| 6.4 | Specialized index types | ~35 min | Demos 6.5–6.8 · [Ex 6.6](slide-exercises/module-06/exercise-6.6-select-specialized-index-types.md) |
| 6.5 | Covered queries and `explain()` | ~40 min | Demos 6.9–6.10 · [Ex 6.7](slide-exercises/module-06/exercise-6.7-interpret-explain-output.md)–[6.8](slide-exercises/module-06/exercise-6.8-identify-covered-queries.md) |
| 6.6 | Maintenance, tradeoffs, and strategy | ~25 min | Demos 6.11–6.12 · [Ex 6.9](slide-exercises/module-06/exercise-6.9-find-redundant-indexes.md)–[6.12](slide-exercises/module-06/exercise-6.12-build-an-indexing-recommendation.md) |
| 6.7 | Hands-on labs | ~80 min time-boxed / full sequence | [Labs 6.1](slide-exercises/module-06/lab-6.1-establish-a-performance-baseline.md)–[6.11](slide-exercises/module-06/lab-6.11-integrated-query-tuning-challenge.md) |
| 6.8 | Challenge, assessment, and transition | ~30 min | [Challenge](slide-exercises/module-06/exercise-6.13-practical-challenge.md) |

---

## Module 7. Introduction to Replication and Sharding

**Day:** Day 3 · **Duration:** ~180–210 min (3–3.5 h) · **Format:** Concept + lab

**Module goal:** Distinguish high availability from horizontal scale; explain replica-set architecture, oplog replication, elections, and read/write guarantees; describe sharded-cluster components, shard-key selection, routing, and balancing; decide when to replicate, shard, or both.

**Prerequisites:** Modules 1–6 recommended so distribution is discussed against a known data model and indexed workload.

**Slide deck:** [`slides/course-complete-marp-with-notes.md`](slides/course-complete-marp-with-notes.md)

Time-box for 3–3.5 hours: concept slides, Demos 7.1 / 7.3 / 7.7 / 7.8, Exercises 7.1 / 7.5 / 7.8 / 7.9, Lab 7.1, and the practical challenge. Remaining items are extra lab block or homework. Failover and sharding commands use instructor-controlled disposable infrastructure. Atlas M0 is a replica set, not a sharded cluster.

| Lesson | Title | Duration | Exercise |
|--------|-------|----------|----------|
| 7.1 | High availability vs horizontal scale | ~20 min | [Exercise 7.1](slide-exercises/module-07/exercise-7.1-replication-or-sharding.md) |
| 7.2 | Replica-set architecture and the oplog | ~35 min | [Exercise 7.2](slide-exercises/module-07/exercise-7.2-label-a-replica-set.md) · [Exercise 7.3](slide-exercises/module-07/exercise-7.3-trace-a-replicated-write.md) · Demos 7.1–7.2 |
| 7.3 | Elections, failover, and member roles | ~30 min | [Exercise 7.4](slide-exercises/module-07/exercise-7.4-sequence-a-failover.md) · Demo 7.3 |
| 7.4 | Read/write settings, lag, and replica-set operations | ~35 min | [Exercise 7.5](slide-exercises/module-07/exercise-7.5-select-read-and-write-settings.md) · [Exercise 7.6](slide-exercises/module-07/exercise-7.6-diagnose-replication-lag.md) · Demos 7.4–7.6 · [Labs 7.1–7.5](slide-exercises/module-07/) |
| 7.5 | Sharded-cluster components | ~25 min | [Exercise 7.7](slide-exercises/module-07/exercise-7.7-label-a-sharded-cluster.md) · Demo 7.7 |
| 7.6 | Shard keys and distribution strategies | ~35 min | [Exercise 7.8](slide-exercises/module-07/exercise-7.8-evaluate-shard-key-candidates.md) · [Exercise 7.10](slide-exercises/module-07/exercise-7.10-compare-ranged-and-hashed.md) · [Exercise 7.11](slide-exercises/module-07/exercise-7.11-diagnose-hotspot-risks.md) · Demo 7.10 |
| 7.7 | Routing, chunks, and balancing | ~30 min | [Exercise 7.9](slide-exercises/module-07/exercise-7.9-targeted-or-scatter-gather.md) · Demos 7.8–7.9 · [Labs 7.6–7.9](slide-exercises/module-07/) |
| 7.8 | Deploy, troubleshoot, and decide | ~30 min | [Exercise 7.12](slide-exercises/module-07/exercise-7.12-design-a-scalable-deployment.md) · [Lab 7.10](slide-exercises/module-07/lab-7.10-integrated-availability-and-scaling.md) · [Challenge](slide-exercises/module-07/exercise-7.13-scale-the-order-platform.md) |

---

## Module 8. MongoDB Best Practices, Security, and Troubleshooting

**Day:** Day 3 · **Duration:** ~180–210 min (3–3.5 h) full / **~90–120 min** time-boxed · **Format:** Concept + demo + exercises + labs

**Module goal:** Review `training_store` as a production candidate: modeling, queries, indexes, layered security, backup and restore, monitoring, troubleshooting, and a scored readiness checklist.

**Prerequisites:** Modules 1–7 recommended. Reload [`datasets/training_store/load.js`](datasets/training_store/load.js) if Day 2–3 writes remain. Schema and restore labs use `training_store_ops` / `training_store_restore` so the class database stays intact.

**Slide deck:** [`slides/course-complete-marp-with-notes.md`](slides/course-complete-marp-with-notes.md)

Time-box discussion exercises if the afternoon must stay near 2 hours; budget ~3.5 hours when every laptop completes Labs 8.2, 8.3, 8.6, 8.9, and 8.11.

| Lesson | Title | Duration | Hands-on |
|--------|-------|----------|----------|
| 8.1 | Production-readiness framework | ~15 min | — |
| 8.2 | Data-modeling best practices | ~30 min | Demo 8.1 · [Ex 8.1](slide-exercises/module-08/exercise-8.1-review-a-document-model.md)–[8.2](slide-exercises/module-08/exercise-8.2-find-the-schema-anti-patterns.md) |
| 8.3 | Queries, aggregations, and indexes | ~40 min | Demos 8.2–8.3 · [Ex 8.3](slide-exercises/module-08/exercise-8.3-review-a-query-and-projection.md)–[8.5](slide-exercises/module-08/exercise-8.5-rationalize-an-index-portfolio.md) |
| 8.4 | Security | ~35 min | Demos 8.4–8.6 · [Ex 8.6](slide-exercises/module-08/exercise-8.6-design-least-privilege-roles.md)–[8.7](slide-exercises/module-08/exercise-8.7-identify-security-risks.md) |
| 8.5 | Backup, recovery, and monitoring | ~35 min | Demos 8.7–8.9 · [Ex 8.8](slide-exercises/module-08/exercise-8.8-define-rpo-and-rto.md)–[8.10](slide-exercises/module-08/exercise-8.10-set-alert-priorities.md) |
| 8.6 | Troubleshooting and operational readiness | ~30 min | Demo 8.10 · [Ex 8.11](slide-exercises/module-08/exercise-8.11-diagnose-an-operational-incident.md)–[8.13](slide-exercises/module-08/exercise-8.13-complete-a-production-readiness-assessment.md) |
| 8.7 | Hands-on labs | ~80 min time-boxed / full sequence | [Labs 8.1](slide-exercises/module-08/lab-8.1-data-model-review-and-repair.md)–[8.11](slide-exercises/module-08/lab-8.11-final-integrated-production-challenge.md) |
| 8.8 | Challenge, assessment, and course wrap-up | ~30 min | [Challenge](slide-exercises/module-08/exercise-8.14-practical-challenge.md) |

---

## Slide exercises

Two labs per day in the original outline; Module 3 expands that with design exercises plus a sequenced populate lab. Lab guides are written **before** exercise slides. File names are stable; do not renumber without updating this table, `course.config.yaml`, and `scripts/exercise_meta.py`.

| Day | Module | Exercise | Lab guide | Time | Objective |
|-----|--------|----------|-----------|------|-----------|
| 1 | 1 | 1.1 Choose the data model | [`exercise-1.1-choose-the-data-model.md`](slide-exercises/module-01/exercise-1.1-choose-the-data-model.md) | 15 min | Match workloads to relational, document, key-value, column-family, or graph |
| 1 | 1 | 1.2 Rows to documents | [`exercise-1.2-rows-to-documents.md`](slide-exercises/module-01/exercise-1.2-rows-to-documents.md) | 20 min | Represent related rows as one document and decide what to snapshot |
| 1 | 1 | 1.3 Explore a MongoDB dataset | [`exercise-1.3-explore-a-mongodb-dataset.md`](slide-exercises/module-01/exercise-1.3-explore-a-mongodb-dataset.md) | 25 min | Identify databases, collections, documents, fields, arrays, and embedded objects |
| 1 | 2 | 2.1 Select a deployment option | [`exercise-2.1-select-a-deployment-option.md`](slide-exercises/module-02/exercise-2.1-select-a-deployment-option.md) | 10 min | Match training and production scenarios to local, container, self-managed, or cloud |
| 1 | 2 | 2.2 Interpret a connection string | [`exercise-2.2-interpret-a-connection-string.md`](slide-exercises/module-02/exercise-2.2-interpret-a-connection-string.md) | 10 min | Label URI parts and identify credential risks |
| 1 | 2 | 2.3 Environment readiness checklist | [`exercise-2.3-environment-readiness-checklist.md`](slide-exercises/module-02/exercise-2.3-environment-readiness-checklist.md) | 10 min | Confirm server, clients, ping, write, and read |
| 1 | 2 | 2.4 Diagnose connection failures | [`exercise-2.4-diagnose-connection-failures.md`](slide-exercises/module-02/exercise-2.4-diagnose-connection-failures.md) | 15 min | Map common errors to the first check and the fix |
| 1 | 2 | 2.5 Install, connect, and verify | [`exercise-2.5-install-connect-and-verify.md`](slide-exercises/module-02/exercise-2.5-install-connect-and-verify.md) | 40 min | Provision MongoDB, connect with `mongosh` and Compass, insert and retrieve test documents |
| 1 | 3 | 3.1 Identify document components | [`exercise-3.1-identify-document-components.md`](slide-exercises/module-03/exercise-3.1-identify-document-components.md) | 10 min | Label `_id`, scalars, nested documents, arrays, booleans, dates, and required fields |
| 1 | 3 | 3.2 Discover access patterns | [`exercise-3.2-discover-access-patterns.md`](slide-exercises/module-03/exercise-3.2-discover-access-patterns.md) | 15 min | Turn e-commerce requirements into frequency, data, and modeling implications |
| 1 | 3 | 3.3 Embed or reference? | [`exercise-3.3-embed-or-reference.md`](slide-exercises/module-03/exercise-3.3-embed-or-reference.md) | 15 min | Choose embed vs reference for eight relationships |
| 1 | 3 | 3.4 Model a product catalog | [`exercise-3.4-model-a-product-catalog.md`](slide-exercises/module-03/exercise-3.4-model-a-product-catalog.md) | 20 min | Three product types in one collection with a shared core |
| 1 | 3 | 3.5 Model an order document | [`exercise-3.5-model-an-order-document.md`](slide-exercises/module-03/exercise-3.5-model-an-order-document.md) | 20 min | Order aggregate with snapshots, a customer reference, and BSON types |
| 1 | 3 | 3.6 Correct schema anti-patterns | [`exercise-3.6-correct-schema-anti-patterns.md`](slide-exercises/module-03/exercise-3.6-correct-schema-anti-patterns.md) | 15 min | Fix string prices, text booleans, unbounded arrays, and display dates |
| 1 | 3 | 3.7 Select a schema pattern | [`exercise-3.7-select-a-schema-pattern.md`](slide-exercises/module-03/exercise-3.7-select-a-schema-pattern.md) | 15 min | Match seven requirements to named MongoDB schema patterns |
| 1 | 3 | 3.8 Design collection validation | [`exercise-3.8-design-collection-validation.md`](slide-exercises/module-03/exercise-3.8-design-collection-validation.md) | 15 min | Write a `$jsonSchema` validator for products |
| 1 | 3 | Lab 3.1 Create the sample database | [`lab-3.1-create-the-sample-database.md`](slide-exercises/module-03/lab-3.1-create-the-sample-database.md) | 10 min | Create `training_store` collections |
| 1 | 3 | Lab 3.2 Populate products | [`lab-3.2-populate-products.md`](slide-exercises/module-03/lab-3.2-populate-products.md) | 20 min | Insert laptop, shoe, and book documents |
| 1 | 3 | Lab 3.3 Populate customers | [`lab-3.3-populate-customers.md`](slide-exercises/module-03/lab-3.3-populate-customers.md) | 15 min | Insert customer C101 with a bounded address array |
| 1 | 3 | Lab 3.4 Populate orders | [`lab-3.4-populate-orders.md`](slide-exercises/module-03/lab-3.4-populate-orders.md) | 20 min | Insert order O5001 with embedded snapshots |
| 1 | 3 | Lab 3.5 Query nested documents | [`lab-3.5-query-nested-documents.md`](slide-exercises/module-03/lab-3.5-query-nested-documents.md) | 15 min | Query dotted fields and arrays |
| 1 | 3 | Lab 3.6 Add collection validation | [`lab-3.6-add-collection-validation.md`](slide-exercises/module-03/lab-3.6-add-collection-validation.md) | 20 min | Valid insert succeeds; invalid insert is rejected |
| 1 | 3 | Lab 3.7 Validate the data model | [`lab-3.7-validate-the-data-model.md`](slide-exercises/module-03/lab-3.7-validate-the-data-model.md) | 15 min | Review the model against a maintainability checklist |
| 1 | 3 | 3.9 Support-ticket challenge | [`exercise-3.9-support-ticket-challenge.md`](slide-exercises/module-03/exercise-3.9-support-ticket-challenge.md) | 25 min | Design collections, embed/reference, validation, and audit history |
| 2 | 4 | 4.1 Read basic documents | [`exercise-4.1-read-basic-documents.md`](slide-exercises/module-04/exercise-4.1-read-basic-documents.md) | 10 min | Empty, equality, and identifier filters |
| 2 | 4 | 4.2 Comparison filters | [`exercise-4.2-build-comparison-filters.md`](slide-exercises/module-04/exercise-4.2-build-comparison-filters.md) | 15 min | `$gt` / ranges / `$nin` with Decimal128 |
| 2 | 4 | 4.3 Logical conditions | [`exercise-4.3-combine-logical-conditions.md`](slide-exercises/module-04/exercise-4.3-combine-logical-conditions.md) | 15 min | Implicit AND, `$or`, `$in`, `$nor` |
| 2 | 4 | 4.4 Missing and null | [`exercise-4.4-query-missing-and-null.md`](slide-exercises/module-04/exercise-4.4-query-missing-and-null.md) | 10 min | `$exists`, `$type`, null vs missing |
| 2 | 4 | 4.5 Query arrays | [`exercise-4.5-query-arrays.md`](slide-exercises/module-04/exercise-4.5-query-arrays.md) | 15 min | Containment, `$all`, `$size` |
| 2 | 4 | 4.6 Arrays of documents | [`exercise-4.6-query-arrays-of-documents.md`](slide-exercises/module-04/exercise-4.6-query-arrays-of-documents.md) | 15 min | `$elemMatch` on order items |
| 2 | 4 | 4.7 Design projections | [`exercise-4.7-design-projections.md`](slide-exercises/module-04/exercise-4.7-design-projections.md) | 10 min | Inclusion, exclusion, nested, matching item |
| 2 | 4 | 4.8 Sort and paginate | [`exercise-4.8-sort-and-paginate.md`](slide-exercises/module-04/exercise-4.8-sort-and-paginate.md) | 15 min | Sort, skip/limit, count, distinct |
| 2 | 4 | 4.9 Insert data | [`exercise-4.9-insert-new-application-data.md`](slide-exercises/module-04/exercise-4.9-insert-new-application-data.md) | 15 min | insertOne, insertMany, verify types |
| 2 | 4 | 4.10 Update product data | [`exercise-4.10-update-product-data.md`](slide-exercises/module-04/exercise-4.10-update-product-data.md) | 15 min | `$set` `$inc` `$rename` `$unset` updateMany |
| 2 | 4 | 4.11 Modify arrays | [`exercise-4.11-modify-arrays.md`](slide-exercises/module-04/exercise-4.11-modify-arrays.md) | 15 min | `$push` `$addToSet` `$pull` positional `$` |
| 2 | 4 | 4.12 Upsert | [`exercise-4.12-perform-an-upsert.md`](slide-exercises/module-04/exercise-4.12-perform-an-upsert.md) | 10 min | `$setOnInsert` createdAt; run twice |
| 2 | 4 | 4.13 Correct unsafe operations | [`exercise-4.13-correct-unsafe-operations.md`](slide-exercises/module-04/exercise-4.13-correct-unsafe-operations.md) | 10 min | Empty filters and nested-object replace |
| 2 | 4 | 4.14 Diagnose query errors | [`exercise-4.14-diagnose-query-errors.md`](slide-exercises/module-04/exercise-4.14-diagnose-query-errors.md) | 15 min | Seven broken queries |
| 2 | 4 | Lab 4.1 Dataset verification | [`exercise-4.15-lab-dataset-verification.md`](slide-exercises/module-04/exercise-4.15-lab-dataset-verification.md) | 15 min | Collections, counts, field paths, types |
| 2 | 4 | Lab 4.2 Product query | [`exercise-4.16-lab-product-query.md`](slide-exercises/module-04/exercise-4.16-lab-product-query.md) | 30 min | Ten product queries |
| 2 | 4 | Lab 4.3 Customer and order query | [`exercise-4.17-lab-customer-order-query.md`](slide-exercises/module-04/exercise-4.17-lab-customer-order-query.md) | 30 min | Nested fields, `$elemMatch`, dates, totals |
| 2 | 4 | Lab 4.4 Projection and pagination | [`exercise-4.18-lab-projection-pagination.md`](slide-exercises/module-04/exercise-4.18-lab-projection-pagination.md) | 20 min | Shape, sort, two pages, count |
| 2 | 4 | Lab 4.5 Insert operations | [`exercise-4.19-lab-insert-operations.md`](slide-exercises/module-04/exercise-4.19-lab-insert-operations.md) | 25 min | Product, customer, order inserts |
| 2 | 4 | Lab 4.6 Update operations | [`exercise-4.20-lab-update-operations.md`](slide-exercises/module-04/exercise-4.20-lab-update-operations.md) | 30 min | Preview–update–verify loop |
| 2 | 4 | Lab 4.7 Array manipulation | [`exercise-4.21-lab-array-manipulation.md`](slide-exercises/module-04/exercise-4.21-lab-array-manipulation.md) | 30 min | Tags and positional / arrayFilters |
| 2 | 4 | Lab 4.8 Replace and upsert | [`exercise-4.22-lab-replace-and-upsert.md`](slide-exercises/module-04/exercise-4.22-lab-replace-and-upsert.md) | 20 min | `$set` vs `replaceOne` vs upsert |
| 2 | 4 | Lab 4.9 Delete operations | [`exercise-4.23-lab-delete-operations.md`](slide-exercises/module-04/exercise-4.23-lab-delete-operations.md) | 20 min | TEMP- records only |
| 2 | 4 | Lab 4.10 Integrated CRUD | [`exercise-4.24-lab-integrated-crud-challenge.md`](slide-exercises/module-04/exercise-4.24-lab-integrated-crud-challenge.md) | 45 min | Product through order to soft-delete |
| 2 | 4 | Practical challenge | [`exercise-4.25-practical-challenge.md`](slide-exercises/module-04/exercise-4.25-practical-challenge.md) | 30–45 min | Scripted business requests with evidence |
| 2 | 5 | 5.1 Arrange pipeline stages | [`exercise-5.1-arrange-pipeline-stages.md`](slide-exercises/module-05/exercise-5.1-arrange-pipeline-stages.md) | 10 min | Order `$match` `$unwind` `$set` `$group` `$sort` `$limit` |
| 2 | 5 | 5.2 Build a `$match` stage | [`exercise-5.2-build-a-match-stage.md`](slide-exercises/module-05/exercise-5.2-build-a-match-stage.md) | 10 min | Paid, high-value, categories, dates, provinces |
| 2 | 5 | 5.3 Reshape with `$project` | [`exercise-5.3-reshape-documents-with-project.md`](slide-exercises/module-05/exercise-5.3-reshape-documents-with-project.md) | 15 min | Rename fields and nest product/pricing |
| 2 | 5 | 5.4 Calculated fields | [`exercise-5.4-create-calculated-fields.md`](slide-exercises/module-05/exercise-5.4-create-calculated-fields.md) | 15 min | Line revenue, `$ifNull`, `$cond`, month |
| 2 | 5 | 5.5 Group and totals | [`exercise-5.5-group-and-calculate-totals.md`](slide-exercises/module-05/exercise-5.5-group-and-calculate-totals.md) | 15 min | Category count, avg, min, max |
| 2 | 5 | 5.6 Multiple dimensions | [`exercise-5.6-group-by-multiple-dimensions.md`](slide-exercises/module-05/exercise-5.6-group-by-multiple-dimensions.md) | 15 min | Payment × fulfillment groups |
| 2 | 5 | 5.7 Analyze arrays | [`exercise-5.7-analyze-arrays-with-unwind.md`](slide-exercises/module-05/exercise-5.7-analyze-arrays-with-unwind.md) | 15 min | Units and revenue per SKU |
| 2 | 5 | 5.8 Top-N reports | [`exercise-5.8-build-a-top-n-report.md`](slide-exercises/module-05/exercise-5.8-build-a-top-n-report.md) | 15 min | Group → sort → limit |
| 2 | 5 | 5.9 Join collections | [`exercise-5.9-join-related-collections.md`](slide-exercises/module-05/exercise-5.9-join-related-collections.md) | 20 min | `$lookup` customers; keep O6499 |
| 2 | 5 | 5.10 `$facet` report | [`exercise-5.10-build-a-facet-report.md`](slide-exercises/module-05/exercise-5.10-build-a-facet-report.md) | 20 min | One document, five product facets |
| 2 | 5 | 5.11 Correct a broken pipeline | [`exercise-5.11-correct-a-broken-pipeline.md`](slide-exercises/module-05/exercise-5.11-correct-a-broken-pipeline.md) | 15 min | Diagnose stage-order and path bugs |
| 2 | 5 | 5.12 Optimize a pipeline | [`exercise-5.12-optimize-a-pipeline.md`](slide-exercises/module-05/exercise-5.12-optimize-a-pipeline.md) | 15 min | Filter early; lookup after group |
| 2 | 5 | Lab 5.1 Dataset verification | [`lab-5.1-aggregation-dataset-verification.md`](slide-exercises/module-05/lab-5.1-aggregation-dataset-verification.md) | 15 min | Counts, types, unwind paths |
| 2 | 5 | Lab 5.2 Product summary | [`lab-5.2-product-summary-pipeline.md`](slide-exercises/module-05/lab-5.2-product-summary-pipeline.md) | 25 min | Category stats for active products |
| 2 | 5 | Lab 5.3 Order revenue | [`lab-5.3-order-revenue-pipeline.md`](slide-exercises/module-05/lab-5.3-order-revenue-pipeline.md) | 25 min | Paid revenue by fulfillment |
| 2 | 5 | Lab 5.4 Product sales | [`lab-5.4-product-sales-pipeline.md`](slide-exercises/module-05/lab-5.4-product-sales-pipeline.md) | 30 min | Top five SKUs by line revenue |
| 2 | 5 | Lab 5.5 Customer summary | [`lab-5.5-customer-order-summary.md`](slide-exercises/module-05/lab-5.5-customer-order-summary.md) | 30 min | Paid spend plus `$lookup` names |
| 2 | 5 | Lab 5.6 Date-based sales | [`lab-5.6-date-based-sales-report.md`](slide-exercises/module-05/lab-5.6-date-based-sales-report.md) | 25 min | Paid orders by calendar month |
| 2 | 5 | Lab 5.7 Price-band analysis | [`lab-5.7-price-band-analysis.md`](slide-exercises/module-05/lab-5.7-price-band-analysis.md) | 20 min | `$bucket` product prices |
| 2 | 5 | Lab 5.8 Multi-metric report | [`lab-5.8-multi-metric-report.md`](slide-exercises/module-05/lab-5.8-multi-metric-report.md) | 30 min | `$facet` on paid orders |
| 2 | 5 | Lab 5.9 Performance review | [`lab-5.9-pipeline-performance-review.md`](slide-exercises/module-05/lab-5.9-pipeline-performance-review.md) | 20 min | `explain` and `$match` placement |
| 2 | 5 | Lab 5.10 Integrated challenge | [`lab-5.10-integrated-aggregation-challenge.md`](slide-exercises/module-05/lab-5.10-integrated-aggregation-challenge.md) | 40 min | Monthly performance report |
| 2 | 5 | 5.13 Executive sales summary | [`exercise-5.13-executive-sales-summary.md`](slide-exercises/module-05/exercise-5.13-executive-sales-summary.md) | 30–45 min | Date-bounded multi-metric report |
| 3 | 6 | 6.1 Identify candidate indexes | [`exercise-6.1-identify-candidate-indexes.md`](slide-exercises/module-06/exercise-6.1-identify-candidate-indexes.md) | 15 min | Name indexed fields for six recurring queries |
| 3 | 6 | 6.2 Select single or compound | [`exercise-6.2-select-single-or-compound.md`](slide-exercises/module-06/exercise-6.2-select-single-or-compound.md) | 15 min | Classify single-field, compound, specialized, or wait for evidence |
| 3 | 6 | 6.3 Arrange compound fields | [`exercise-6.3-arrange-compound-fields.md`](slide-exercises/module-06/exercise-6.3-arrange-compound-fields.md) | 15 min | Order equality, sort, and range fields |
| 3 | 6 | 6.4 Apply Equality–Sort–Range | [`exercise-6.4-apply-equality-sort-range.md`](slide-exercises/module-06/exercise-6.4-apply-equality-sort-range.md) | 15 min | Propose compound indexes for three shapes |
| 3 | 6 | 6.5 Identify index prefixes | [`exercise-6.5-identify-index-prefixes.md`](slide-exercises/module-06/exercise-6.5-identify-index-prefixes.md) | 10 min | List supported prefixes and unsupported shapes |
| 3 | 6 | 6.6 Select specialized types | [`exercise-6.6-select-specialized-index-types.md`](slide-exercises/module-06/exercise-6.6-select-specialized-index-types.md) | 15 min | Match eight requirements to index types |
| 3 | 6 | 6.7 Interpret explain output | [`exercise-6.7-interpret-explain-output.md`](slide-exercises/module-06/exercise-6.7-interpret-explain-output.md) | 20 min | Read COLLSCAN, IXSCAN, examined counts, extra sort |
| 3 | 6 | 6.8 Identify covered queries | [`exercise-6.8-identify-covered-queries.md`](slide-exercises/module-06/exercise-6.8-identify-covered-queries.md) | 15 min | Decide coverage from index + projection |
| 3 | 6 | 6.9 Find redundant indexes | [`exercise-6.9-find-redundant-indexes.md`](slide-exercises/module-06/exercise-6.9-find-redundant-indexes.md) | 15 min | Spot overlapping prefixes; require evidence before drop |
| 3 | 6 | 6.10 Balance read and write | [`exercise-6.10-balance-read-and-write.md`](slide-exercises/module-06/exercise-6.10-balance-read-and-write.md) | 15 min | Investigate over-indexing on a write-heavy workload |
| 3 | 6 | 6.11 Correct anti-patterns | [`exercise-6.11-correct-indexing-anti-patterns.md`](slide-exercises/module-06/exercise-6.11-correct-indexing-anti-patterns.md) | 15 min | Rewrite seven unsafe indexing habits |
| 3 | 6 | 6.12 Build a recommendation | [`exercise-6.12-build-an-indexing-recommendation.md`](slide-exercises/module-06/exercise-6.12-build-an-indexing-recommendation.md) | 20 min | Shape, index, cost, validation, rollback |
| 3 | 6 | Lab 6.1 Performance baseline | [`lab-6.1-establish-a-performance-baseline.md`](slide-exercises/module-06/lab-6.1-establish-a-performance-baseline.md) | 20 min | Capture explain baselines without creating indexes |
| 3 | 6 | Lab 6.2 Single-field index | [`lab-6.2-create-and-test-a-single-field-index.md`](slide-exercises/module-06/lab-6.2-create-and-test-a-single-field-index.md) | 20 min | Index SKU and compare examined documents |
| 3 | 6 | Lab 6.3 Compound index | [`lab-6.3-design-a-compound-index.md`](slide-exercises/module-06/lab-6.3-design-a-compound-index.md) | 25 min | Category + active + price; test prefixes |
| 3 | 6 | Lab 6.4 Filter and sort | [`lab-6.4-support-filtering-and-sorting.md`](slide-exercises/module-06/lab-6.4-support-filtering-and-sorting.md) | 25 min | Customer order history with ESR field order |
| 3 | 6 | Lab 6.5 Nested fields and arrays | [`lab-6.5-index-nested-fields-and-arrays.md`](slide-exercises/module-06/lab-6.5-index-nested-fields-and-arrays.md) | 25 min | `contact.email` and multikey `tags` |
| 3 | 6 | Lab 6.6 Data-integrity indexes | [`lab-6.6-implement-data-integrity-indexes.md`](slide-exercises/module-06/lab-6.6-implement-data-integrity-indexes.md) | 20 min | Unique SKU, customer number, order number |
| 3 | 6 | Lab 6.7 Partial and TTL | [`lab-6.7-implement-partial-and-ttl-indexes.md`](slide-exercises/module-06/lab-6.7-implement-partial-and-ttl-indexes.md) | 25 min | Active-product partial index; sessions TTL |
| 3 | 6 | Lab 6.8 Covered query | [`lab-6.8-build-a-covered-query.md`](slide-exercises/module-06/lab-6.8-build-a-covered-query.md) | 20 min | Cover category, price, and name; exclude `_id` |
| 3 | 6 | Lab 6.9 Tune aggregation | [`lab-6.9-tune-an-aggregation-pipeline.md`](slide-exercises/module-06/lab-6.9-tune-an-aggregation-pipeline.md) | 25 min | Index `$match`/`$sort`; `$group` still in memory |
| 3 | 6 | Lab 6.10 Audit indexes | [`lab-6.10-audit-and-rationalize-indexes.md`](slide-exercises/module-06/lab-6.10-audit-and-rationalize-indexes.md) | 25 min | Hide, test, unhide; do not drop |
| 3 | 6 | Lab 6.11 Integrated challenge | [`lab-6.11-integrated-query-tuning-challenge.md`](slide-exercises/module-06/lab-6.11-integrated-query-tuning-challenge.md) | 40–45 min | Catalog page and order-history tuning |
| 3 | 6 | Practical challenge | [`exercise-6.13-practical-challenge.md`](slide-exercises/module-06/exercise-6.13-practical-challenge.md) | 30–45 min | Ten-pattern e-commerce index review |
| 3 | 7 | 7.1 Replication or sharding? | [`exercise-7.1-replication-or-sharding.md`](slide-exercises/module-07/exercise-7.1-replication-or-sharding.md) | 10 min | Choose replication, sharding, both, or neither yet |
| 3 | 7 | 7.2 Label a replica set | [`exercise-7.2-label-a-replica-set.md`](slide-exercises/module-07/exercise-7.2-label-a-replica-set.md) | 10 min | Label members, oplog, heartbeats, read/write paths |
| 3 | 7 | 7.3 Trace a replicated write | [`exercise-7.3-trace-a-replicated-write.md`](slide-exercises/module-07/exercise-7.3-trace-a-replicated-write.md) | 15 min | Sequence write, oplog, apply, write-concern ack |
| 3 | 7 | 7.4 Sequence a failover | [`exercise-7.4-sequence-a-failover.md`](slide-exercises/module-07/exercise-7.4-sequence-a-failover.md) | 15 min | Detection, election, driver discovery, retry |
| 3 | 7 | 7.5 Select read and write settings | [`exercise-7.5-select-read-and-write-settings.md`](slide-exercises/module-07/exercise-7.5-select-read-and-write-settings.md) | 20 min | Preference, concern, and write concern by operation |
| 3 | 7 | 7.6 Diagnose replication lag | [`exercise-7.6-diagnose-replication-lag.md`](slide-exercises/module-07/exercise-7.6-diagnose-replication-lag.md) | 15 min | Cause, impact, evidence, first action |
| 3 | 7 | 7.7 Label a sharded cluster | [`exercise-7.7-label-a-sharded-cluster.md`](slide-exercises/module-07/exercise-7.7-label-a-sharded-cluster.md) | 10 min | mongos, config servers, shards, flows |
| 3 | 7 | 7.8 Evaluate shard-key candidates | [`exercise-7.8-evaluate-shard-key-candidates.md`](slide-exercises/module-07/exercise-7.8-evaluate-shard-key-candidates.md) | 20 min | Score six order-key candidates |
| 3 | 7 | 7.9 Targeted or scatter-gather? | [`exercise-7.9-targeted-or-scatter-gather.md`](slide-exercises/module-07/exercise-7.9-targeted-or-scatter-gather.md) | 15 min | Classify query routing |
| 3 | 7 | 7.10 Ranged vs hashed | [`exercise-7.10-compare-ranged-and-hashed.md`](slide-exercises/module-07/exercise-7.10-compare-ranged-and-hashed.md) | 15 min | Compare strategies for two workloads |
| 3 | 7 | 7.11 Diagnose hotspot risks | [`exercise-7.11-diagnose-hotspot-risks.md`](slide-exercises/module-07/exercise-7.11-diagnose-hotspot-risks.md) | 15 min | Five hotspot patterns and mitigations |
| 3 | 7 | 7.12 Design a scalable deployment | [`exercise-7.12-design-a-scalable-deployment.md`](slide-exercises/module-07/exercise-7.12-design-a-scalable-deployment.md) | 25 min | Availability, key, routing, residency |
| 3 | 7 | Lab 7.1 Replica-set health | [`lab-7.1-verify-replica-set-health.md`](slide-exercises/module-07/lab-7.1-verify-replica-set-health.md) | 20 min | `rs.status()` / `rs.conf()` health report |
| 3 | 7 | Lab 7.2 Write and verify replication | [`lab-7.2-write-and-verify-replication.md`](slide-exercises/module-07/lab-7.2-write-and-verify-replication.md) | 20 min | Insert through replica-set URI; delete probe |
| 3 | 7 | Lab 7.3 Observe failover | [`lab-7.3-observe-election-and-failover.md`](slide-exercises/module-07/lab-7.3-observe-election-and-failover.md) | 25 min | Instructor-controlled step-down |
| 3 | 7 | Lab 7.4 Read preference and write concern | [`lab-7.4-test-read-preference-and-write-concern.md`](slide-exercises/module-07/lab-7.4-test-read-preference-and-write-concern.md) | 25 min | Compare serving members and `w` |
| 3 | 7 | Lab 7.5 Investigate lag | [`lab-7.5-investigate-replication-lag.md`](slide-exercises/module-07/lab-7.5-investigate-replication-lag.md) | 20 min | Optimes, oplog window, actions |
| 3 | 7 | Lab 7.6 Inspect sharded cluster | [`lab-7.6-inspect-sharded-cluster-components.md`](slide-exercises/module-07/lab-7.6-inspect-sharded-cluster-components.md) | 20 min | `sh.status()` components |
| 3 | 7 | Lab 7.7 Shard a training collection | [`lab-7.7-shard-a-training-collection.md`](slide-exercises/module-07/lab-7.7-shard-a-training-collection.md) | 25 min | Disposable cluster only |
| 3 | 7 | Lab 7.8 Analyze query routing | [`lab-7.8-analyze-query-routing.md`](slide-exercises/module-07/lab-7.8-analyze-query-routing.md) | 25 min | Explain targeted vs scatter-gather |
| 3 | 7 | Lab 7.9 Review chunk distribution | [`lab-7.9-review-chunk-distribution.md`](slide-exercises/module-07/lab-7.9-review-chunk-distribution.md) | 20 min | Balancer, ranges, hotspot notes |
| 3 | 7 | Lab 7.10 Integrated challenge | [`lab-7.10-integrated-availability-and-scaling.md`](slide-exercises/module-07/lab-7.10-integrated-availability-and-scaling.md) | 40–45 min | Topology, key, routing, monitoring |
| 3 | 7 | Practical challenge | [`exercise-7.13-scale-the-order-platform.md`](slide-exercises/module-07/exercise-7.13-scale-the-order-platform.md) | 30–45 min | Scale the e-commerce order platform |
| 3 | 8 | 8.1 Review a document model | [`exercise-8.1-review-a-document-model.md`](slide-exercises/module-08/exercise-8.1-review-a-document-model.md) | 15 min | Score access patterns, snapshots, types, growth, PII, validation |
| 3 | 8 | 8.2 Find schema anti-patterns | [`exercise-8.2-find-the-schema-anti-patterns.md`](slide-exercises/module-08/exercise-8.2-find-the-schema-anti-patterns.md) | 15 min | Unbounded arrays, string prices, mixed names, repair sketch |
| 3 | 8 | 8.3 Review a query and projection | [`exercise-8.3-review-a-query-and-projection.md`](slide-exercises/module-08/exercise-8.3-review-a-query-and-projection.md) | 15 min | Filter, project, sort, limit, ESR index |
| 3 | 8 | 8.4 Optimize an aggregation | [`exercise-8.4-optimize-an-aggregation-pipeline.md`](slide-exercises/module-08/exercise-8.4-optimize-an-aggregation-pipeline.md) | 20 min | Early `$match`; avoid double-count after `$unwind` |
| 3 | 8 | 8.5 Rationalize indexes | [`exercise-8.5-rationalize-an-index-portfolio.md`](slide-exercises/module-08/exercise-8.5-rationalize-an-index-portfolio.md) | 20 min | Overlap, low-selectivity `active`, hide then monitor |
| 3 | 8 | 8.6 Least-privilege roles | [`exercise-8.6-design-least-privilege-roles.md`](slide-exercises/module-08/exercise-8.6-design-least-privilege-roles.md) | 20 min | Permit/deny for app, report, support, monitor, backup, DBA |
| 3 | 8 | 8.7 Identify security risks | [`exercise-8.7-identify-security-risks.md`](slide-exercises/module-08/exercise-8.7-identify-security-risks.md) | 15 min | Rank six risks and name mitigations |
| 3 | 8 | 8.8 Define RPO and RTO | [`exercise-8.8-define-rpo-and-rto.md`](slide-exercises/module-08/exercise-8.8-define-rpo-and-rto.md) | 15 min | Objectives and restore validation by collection |
| 3 | 8 | 8.9 Monitoring dashboard | [`exercise-8.9-design-a-monitoring-dashboard.md`](slide-exercises/module-08/exercise-8.9-design-a-monitoring-dashboard.md) | 20 min | Twelve purpose-driven tiles; drop vanity metrics |
| 3 | 8 | 8.10 Set alert priorities | [`exercise-8.10-set-alert-priorities.md`](slide-exercises/module-08/exercise-8.10-set-alert-priorities.md) | 15 min | Critical / high / medium / informational |
| 3 | 8 | 8.11 Diagnose an incident | [`exercise-8.11-diagnose-an-operational-incident.md`](slide-exercises/module-08/exercise-8.11-diagnose-an-operational-incident.md) | 20 min | Filter change, examined docs up, no election |
| 3 | 8 | 8.12 Create a runbook | [`exercise-8.12-create-an-operational-runbook.md`](slide-exercises/module-08/exercise-8.12-create-an-operational-runbook.md) | 20 min | Twelve-section runbook for one alert |
| 3 | 8 | 8.13 Production-readiness assessment | [`exercise-8.13-complete-a-production-readiness-assessment.md`](slide-exercises/module-08/exercise-8.13-complete-a-production-readiness-assessment.md) | 25 min | Score nine areas; classify go-live |
| 3 | 8 | Lab 8.1 Data-model review | [`lab-8.1-data-model-review-and-repair.md`](slide-exercises/module-08/lab-8.1-data-model-review-and-repair.md) | 25 min | Types, growth, snapshots, XBAD, validation plan |
| 3 | 8 | Lab 8.2 Query and projection | [`lab-8.2-query-and-projection-optimization.md`](slide-exercises/module-08/lab-8.2-query-and-projection-optimization.md) | 25 min | Replace `find({})`; explain; ESR index |
| 3 | 8 | Lab 8.3 Monthly sales pipeline | [`lab-8.3-aggregation-pipeline-construction.md`](slide-exercises/module-08/lab-8.3-aggregation-pipeline-construction.md) | 30 min | Six metrics; two `$group` stages |
| 3 | 8 | Lab 8.4 Pipeline tuning | [`lab-8.4-aggregation-pipeline-tuning.md`](slide-exercises/module-08/lab-8.4-aggregation-pipeline-tuning.md) | 25 min | `$match` first; verify C101 revenue |
| 3 | 8 | Lab 8.5 Index design | [`lab-8.5-index-design-and-validation.md`](slide-exercises/module-08/lab-8.5-index-design-and-validation.md) | 25 min | History and paid-report indexes; no drops |
| 3 | 8 | Lab 8.6 Schema validation | [`lab-8.6-schema-validation-implementation.md`](slide-exercises/module-08/lab-8.6-schema-validation-implementation.md) | 20 min | `training_store_ops.orders_validated` |
| 3 | 8 | Lab 8.7 Security review | [`lab-8.7-security-configuration-review.md`](slide-exercises/module-08/lab-8.7-security-configuration-review.md) | 25 min | Fictional config; P1–P3; role sketches |
| 3 | 8 | Lab 8.8 Logs and metrics | [`lab-8.8-monitoring-and-log-analysis.md`](slide-exercises/module-08/lab-8.8-monitoring-and-log-analysis.md) | 25 min | Timeline, cause, alert, runbook update |
| 3 | 8 | Lab 8.9 Backup and restore | [`lab-8.9-backup-and-restore-verification.md`](slide-exercises/module-08/lab-8.9-backup-and-restore-verification.md) | 30 min | Restore to `training_store_restore`; vs RTO |
| 3 | 8 | Lab 8.10 Troubleshooting challenge | [`lab-8.10-troubleshooting-challenge.md`](slide-exercises/module-08/lab-8.10-troubleshooting-challenge.md) | 30 min | Five independent symptoms |
| 3 | 8 | Lab 8.11 Integrated challenge | [`lab-8.11-final-integrated-production-challenge.md`](slide-exercises/module-08/lab-8.11-final-integrated-production-challenge.md) | 45–60 min | Schema, pipeline, indexes, ops pack, checklist |
| 3 | 8 | Practical challenge | [`exercise-8.14-practical-challenge.md`](slide-exercises/module-08/exercise-8.14-practical-challenge.md) | 45 min | Six-part production-readiness review |

Module 7 replica-set labs run against Atlas or an instructor replica set. Failover and sharding labs require a disposable instructor cluster. Module 8 restore labs target `training_store_restore`, never `training_store`. Module 1 Lab 1.3 uses `training_store` (`customers`, `products`, `orders`) from [`datasets/training_store`](datasets/training_store). Module 3 adds `reviews` and replaces the starter documents with the Day 2 application model.

---

## Sample data (shared across days)

All labs reuse one application dataset under `datasets/training_store`:

| Collection | Role |
|------------|------|
| `products` | Catalog items with category-specific `attributes` (laptop, shoe, book, accessory) |
| `customers` | Buyer profiles with nested name, contact, and a bounded `addresses` array |
| `orders` | Line-item snapshots that exercise embed vs reference, queries, aggregation, and indexes |
| `reviews` | Product reviews stored separately so product documents stay bounded |

Do not invent a second application dataset for later modules. Day 3 indexes the same queries and pipeline written on Day 2. Module 6 Lab 6.7 may create a scratch `sessions` collection only to demonstrate TTL expiration.

After `load.js`, expect **6 customers, 13 products, 17 orders (13 PAID), 6 reviews**. Reload at the start of Day 2 so Module 5 has paid orders across July–September 2026. O6499 has no matching customer (for `$lookup`). Some paid orders omit `shippingFee` (for `$ifNull`).

**Student day labs** (outline hands-on + PPT Exercises rewritten for this dataset): [`labs/README.md`](labs/README.md). **Application connection demo:** [`sample-app/README.md`](sample-app/README.md).
