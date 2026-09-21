"""Write Module 6 lab guides. Run: python scripts/module06_labs.py"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "slide-exercises" / "module-06"

ENV_MONGO = """## Environment basics (read this first)

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

**Small-data note:** Twelve products and seventeen orders will not produce dramatic wall-clock wins. Record the **plan** (`COLLSCAN` vs `IXSCAN`), **index name**, and **examined vs returned** counts. That is the teaching signal.
"""

ENV_DISCUSSION = """## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Capture answers in a notes file.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional |
| Timer | Instructor clocks this | — |

You may use `mongosh` to test ideas, but reasoning is the deliverable. You do not need to create production indexes during discussion exercises.
"""


def js(code: str) -> str:
    return f"```javascript\n{code.strip()}\n```"


def guide(
    kind: str,
    num: int,
    slug: str,
    title: str,
    time: str,
    difficulty: str,
    objective: str,
    steps: list[tuple[str, str, str]],
    success: list[str],
    *,
    discussion: bool = False,
    extra: str = "",
) -> tuple:
    env = ENV_DISCUSSION if discussion else ENV_MONGO
    label = "Exercise" if kind == "exercise" else "Lab"
    step_md = []
    for i, (stitle, do, exp) in enumerate(steps, 1):
        step_md.append(f"### Step {i} — {stitle}\n\n**Do this:** {do}\n\n**Expected result:** {exp}\n")
    steps_block = "\n---\n\n".join(step_md)
    checks = "\n".join(f"- [ ] {c}" for c in success)
    md = f"""# {label} 6.{num}: {title}

**Module 6:** Indexing and Query Performance  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 6)  
**Time:** {time}  
**Difficulty:** {difficulty}

**Objective:** {objective}

---

{env}

---

## Steps from the training slides

Follow these steps in order.

{steps_block}
---

{extra}

## Success criteria

{checks}

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
"""
    return (kind, num, slug, title, time, "discussion" if discussion else "hands-on", objective, md)


GUIDES: list[tuple] = []

GUIDES.append(
    guide(
        "exercise",
        1,
        "identify-candidate-indexes",
        "Identify Candidate Indexes",
        "15 min",
        "Beginner",
        "Name the fields that belong in an index for six recurring training_store queries.",
        [
            (
                "Identifier lookups",
                "For (1) product by SKU and (2) customer by email, write the collection, the filter field, and whether uniqueness is a business rule.",
                "products.sku (unique) and customers.contact.email (unique if the store treats email as a login). `_id` already covers ObjectId lookups.",
            ),
            (
                "History and catalog queries",
                "For (3) a customer’s orders newest first, (4) active products by category and price, (5) reviews by product and date, and (6) orders by payment status and creation date, list equality, sort, and range fields.",
                "(3) customerId equality, createdAt sort. (4) category + active equality, price sort/range. (5) productId equality, createdAt sort. (6) paymentStatus equality, createdAt sort/range.",
            ),
        ],
        [
            "Each query names a collection and indexed fields",
            "SKU and email are treated as identifier lookups",
            "Sort fields are listed separately from equality fields",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        2,
        "select-single-or-compound",
        "Select Single or Compound Indexes",
        "15 min",
        "Beginner",
        "Classify each requirement as a single-field index, a compound index, a specialized index, or not enough evidence.",
        [
            (
                "Classify four requirements",
                "Classify: (A) lookup product by SKU, (B) active accessories sorted by price, (C) expire session documents, (D) a manager’s one-time ad-hoc count of all orders.",
                "A single-field unique. B compound. C specialized TTL. D no new index without evidence — one-time reporting is not a standing query shape.",
            ),
            (
                "Justify one borderline case",
                "Write two sentences on why a boolean `active` field is a poor standalone index but a useful compound or partial-index field.",
                "Low selectivity: most products are active, so `{ active: 1 }` barely narrows the scan. Combined with category (and optionally a partial filter) it supports the catalog shape.",
            ),
        ],
        [
            "Four classifications match the intended types",
            "The one-time query is not indexed by default",
            "Low-selectivity fields are justified only in context",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        3,
        "arrange-compound-fields",
        "Arrange Compound-Index Fields",
        "15 min",
        "Intermediate",
        "Propose a compound-index field order for a paid high-value order query that also sorts by date.",
        [
            (
                "Label ESR roles",
                "Given:\n\n"
                + js(
                    """db.orders
  .find({
    customerId: customerId,
    paymentStatus: "PAID",
    total: { $gte: Decimal128("500.00") }
  })
  .sort({ createdAt: -1 })"""
                )
                + "\nLabel each field as equality, sort, or range.",
                "Equality: customerId, paymentStatus. Sort: createdAt. Range: total.",
            ),
            (
                "Propose order and an alternative",
                "Write a candidate key following Equality–Sort–Range. Then note when you might put the more selective equality field first if `paymentStatus` is a small set of values.",
                "Candidate `{ customerId: 1, paymentStatus: 1, createdAt: -1, total: 1 }`. Alternative: still lead with customerId (high selectivity) even if paymentStatus is low selectivity. Do not lead with total (range).",
            ),
        ],
        [
            "Equality, sort, and range are labeled correctly",
            "The range field is not first",
            "An alternative mentions selectivity without violating ESR blindly",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        4,
        "apply-equality-sort-range",
        "Apply Equality–Sort–Range",
        "15 min",
        "Intermediate",
        "For three query shapes, label equality, sort, and range fields and propose a compound index.",
        [
            (
                "Catalog and history shapes",
                "Shape A: active products in category ACCESSORY, price ≤ 100, sort by price. Shape B: one customerId, createdAt in a date range, sort createdAt descending. Label ESR and propose indexes.",
                "A: equality category+active, sort/range price → `{ category: 1, active: 1, price: 1 }`. B: equality customerId, sort createdAt, range createdAt (same field) → `{ customerId: 1, createdAt: -1 }`.",
            ),
            (
                "Reporting shape",
                "Shape C: paymentStatus PAID, createdAt ≥ start, sort createdAt descending. Propose an index and one sentence on why paymentStatus still belongs first even though it is low selectivity.",
                "`{ paymentStatus: 1, createdAt: -1 }`. Equality first partitions the index so the date sort/range walks one status’s keys instead of mixing statuses.",
            ),
        ],
        [
            "Three candidate indexes exist",
            "No design leads with a range field when an equality field is available",
            "Same-field sort and range (createdAt) is recognized as one indexed field",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        5,
        "identify-index-prefixes",
        "Identify Index Prefixes",
        "10 min",
        "Beginner",
        "State which query prefixes a compound index can support directly.",
        [
            (
                "List usable prefixes",
                "Given `{ customerId: 1, paymentStatus: 1, createdAt: -1 }`, list the prefixes MongoDB can use from the left.",
                "customerId; customerId + paymentStatus; customerId + paymentStatus + createdAt.",
            ),
            (
                "Mark unsupported shapes",
                "Decide whether these can use that index as a leading prefix: (1) filter only paymentStatus, (2) filter customerId, (3) filter customerId and sort createdAt without paymentStatus.",
                "(1) No — paymentStatus is not leading. (2) Yes. (3) Usually not for the sort: skipping paymentStatus breaks the sort prefix, so an extra SORT is likely.",
            ),
        ],
        [
            "Three prefixes are listed in left-to-right order",
            "A paymentStatus-only filter is not treated as supported",
            "Skipped-field sort is called out as a problem",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        6,
        "select-specialized-index-types",
        "Select Specialized Index Types",
        "15 min",
        "Beginner",
        "Match eight requirements to unique, partial, sparse, TTL, text, wildcard, geospatial, or hashed indexes.",
        [
            (
                "Match the first four",
                "Match: (1) product SKU must never duplicate, (2) index only active products, (3) optional discountCode present on few documents, (4) delete sessions after expiresAt.",
                "1 unique, 2 partial, 3 sparse (or a partial filter on $exists), 4 TTL.",
            ),
            (
                "Match the last four",
                "Match: (5) word search on product names, (6) unpredictable attributes.* paths, (7) nearby stores from a GeoJSON point, (8) hashed shard-key distribution on tenantId.",
                "5 text (or an external search product for advanced relevance), 6 wildcard, 7 geospatial 2dsphere, 8 hashed.",
            ),
        ],
        [
            "Eight matches are recorded",
            "Partial is preferred over sparse when an explicit subset filter exists",
            "Hashed is not chosen for range queries",
        ],
        discussion=True,
    )
)

SAMPLE_EXPLAIN = """```text
winningPlan.stage: FETCH
winningPlan.inputStage.stage: IXSCAN
winningPlan.inputStage.indexName: idx_products_category
nReturned: 4
totalKeysExamined: 4
totalDocsExamined: 4
executionTimeMillis: (small on training data)
```"""

GUIDES.append(
    guide(
        "exercise",
        7,
        "interpret-explain-output",
        "Interpret Explain Output",
        "20 min",
        "Intermediate",
        "Read essential explain fields and decide whether a plan is a collection scan, a targeted index scan, or an expensive index scan.",
        [
            (
                "Label the sample plan",
                "Using this training-style output, name the winning stage path, the index, and whether a FETCH occurred:\n\n" + SAMPLE_EXPLAIN,
                "IXSCAN on idx_products_category, then FETCH. Four keys, four docs, four returned — targeted for this dataset.",
            ),
            (
                "Contrast a bad ratio",
                "If another query showed COLLSCAN, totalDocsExamined 12, nReturned 1, write what you would try next. If it showed IXSCAN with keys examined 50,000 and nReturned 10, why is IXSCAN not enough?",
                "COLLSCAN: add an index on the filter/sort shape. High-key IXSCAN: the index is used but not selective (wrong order, low-selectivity leading field, or a wide range). Redesign the key; do not stop at “it used an index.”",
            ),
        ],
        [
            "COLLSCAN vs IXSCAN vs FETCH are identified",
            "nReturned, totalKeysExamined, and totalDocsExamined are interpreted together",
            "IXSCAN is not treated as automatically efficient",
        ],
        discussion=True,
        extra="You may instead run `db.products.find({ category: \"ACCESSORY\" }).explain(\"executionStats\")` after Demo 6.1 and interpret the live plan.",
    )
)

GUIDES.append(
    guide(
        "exercise",
        8,
        "identify-covered-queries",
        "Identify Covered Queries",
        "15 min",
        "Intermediate",
        "Given an index, decide which query and projection combinations can be covered.",
        [
            (
                "Index and three queries",
                "Index `{ category: 1, price: 1, name: 1 }`. Decide coverage for: (Q1) filter category, project name and price with `_id: 0`; (Q2) same filter, project name, price, and tags; (Q3) filter category, project name only but leave `_id` on.",
                "Q1 may be covered. Q2 is not — tags are not in the index, so FETCH. Q3 is not covered unless `_id` is in the index — default `_id` forces a document fetch.",
            ),
            (
                "State the confirmation rule",
                "Write the three conditions for coverage and the explain signal you would look for.",
                "Filter fields indexed, returned fields indexed, `_id` excluded or indexed. Confirm with explain: IXSCAN without FETCH (projection-covered plan).",
            ),
        ],
        [
            "Q1 is the only likely covered query",
            "_id exclusion is mentioned",
            "explain() is required for confirmation",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        9,
        "find-redundant-indexes",
        "Find Redundant Indexes",
        "15 min",
        "Intermediate",
        "Spot overlapping prefixes without dropping an index on appearance alone.",
        [
            (
                "Mark overlap",
                "Indexes: `{ category: 1 }`, `{ category: 1, price: 1 }`, `{ category: 1, price: 1, name: 1 }`, `{ price: 1 }`. Which pairs share a prefix? Which index is not a prefix of the others?",
                "The three category-leading indexes overlap; the two-field and three-field keys can serve category-only queries. `{ price: 1 }` is not a prefix of the category indexes.",
            ),
            (
                "Decide what evidence is required",
                "List four things to check before hiding `{ category: 1 }` in favor of a wider compound index.",
                "Query shapes and sort needs; covered-query projections; unique/partial/TTL options; `$indexStats` usage; index size vs write cost. Do not drop from visual similarity alone.",
            ),
        ],
        [
            "Prefix overlap is identified",
            "The price-only index is kept as a separate candidate",
            "A hide-then-measure approach is preferred over immediate drop",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        10,
        "balance-read-and-write",
        "Balance Read and Write Performance",
        "15 min",
        "Intermediate",
        "Plan how to investigate fourteen secondary indexes on a write-heavy (80/20) workload with rising insert latency.",
        [
            (
                "Evidence to collect",
                "List the measurements you would gather before dropping anything.",
                "Insert/update latency and opcounters; index sizes (`collStats` / `indexSizes`); `$indexStats` since last restart; slow query log / profiler; explain on the 20% reads; replication lag if replica set.",
            ),
            (
                "Safe test path",
                "Describe how to test removal of one unused-looking index and which metrics to watch afterward.",
                "Hide the index (it still costs writes until dropped). Rerun the read queries and explain. If reads stay healthy, drop in a maintenance window. Monitor insert latency, disk, and the previously indexed query shapes. Keep the createIndex command as rollback.",
            ),
        ],
        [
            "Write-path metrics are included, not only read explain",
            "Hiding is used before dropping",
            "A rollback (re-create) plan exists",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        11,
        "correct-indexing-anti-patterns",
        "Correct Indexing Anti-Patterns",
        "15 min",
        "Beginner",
        "Rewrite seven unsafe or wasteful indexing habits as safer practices.",
        [
            (
                "Correct the first four",
                "Rewrite: index every field; one new index per query without checking overlap; put a range field first in every compound index; drop unused indexes immediately.",
                "Index recurring query shapes. Reuse prefixes. Equality (then sort) before range. Hide, measure, then drop.",
            ),
            (
                "Correct the last three",
                "Rewrite: treat every IXSCAN as optimal; ignore write overhead; design indexes only on development-sized data.",
                "Read examined keys/docs. Count secondary indexes on the write path. Validate with production-like volume and distribution.",
            ),
        ],
        [
            "Seven corrections are written",
            "ESR and hide-before-drop appear in the rewrite",
            "Small-data caution is explicit",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        12,
        "build-an-indexing-recommendation",
        "Build an Indexing Recommendation",
        "20 min",
        "Intermediate",
        "Write a short recommendation for one training_store query shape with validation and rollback.",
        [
            (
                "Fill the template",
                "Pick the catalog query (active products in a category, sorted by price) or customer order history. Write: query shape, current plan assumption, proposed index, expected improvement, write/storage cost.",
                "A complete paragraph or bullet list covering those five items. Example: `{ category: 1, active: 1, price: 1 }` named `idx_products_category_active_price`.",
            ),
            (
                "Validation and rollback",
                "Add a validation procedure (explain before/after, examined counts) and a rollback procedure (dropIndex of the named index; keep the createIndex snippet).",
                "Baseline explain → createIndex → explain again → compare nReturned vs keys/docs examined and SORT absence. Rollback: `db.products.dropIndex(\"idx_products_category_active_price\")`.",
            ),
        ],
        [
            "One query shape is specified",
            "Field order is justified",
            "Write cost and rollback are included",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "lab",
        1,
        "establish-a-performance-baseline",
        "Establish a Performance Baseline",
        "20 min",
        "Beginner",
        "Capture explain baselines for assigned queries without creating new indexes.",
        [
            (
                "Confirm the dataset",
                "Run:\n\n"
                + js(
                    """use training_store
db.products.countDocuments()
db.orders.countDocuments()
db.products.getIndexes()
db.orders.getIndexes()"""
                ),
                "About 12 products and 17 orders. Each collection should show the default `_id_` index. Note any extra indexes left from a demo.",
            ),
            (
                "Explain the catalog query",
                "Run and record winning stage, nReturned, totalKeysExamined, totalDocsExamined, and any SORT:\n\n"
                + js(
                    """db.products.find(
  { category: "ACCESSORY", active: true }
).sort({ price: 1 }).explain("executionStats")"""
                ),
                "Likely COLLSCAN (unless a prior demo index remains). Record the numbers even if they are small.",
            ),
            (
                "Explain order history",
                "Replace `cid` with C101’s `_id` from `db.customers.findOne({ customerNumber: \"C101\" })`, then:\n\n"
                + js(
                    """db.orders.find({
  customerId: cid,
  paymentStatus: "PAID"
}).sort({ createdAt: -1 }).limit(10).explain("executionStats")"""
                ),
                "A baseline row exists: filter, sort, projection (none), winning plan, counts, in-memory sort yes/no.",
            ),
            (
                "Fill the baseline table",
                "In notes, one row per query: filter, sort, projection, winning plan, nReturned, keys examined, docs examined, extra sort.",
                "Two completed rows. No new indexes created in this lab.",
            ),
        ],
        [
            "Dataset counts match the loader",
            "Two explain summaries are written down",
            "No createIndex was run in this lab",
        ],
    )
)

GUIDES.append(
    guide(
        "lab",
        2,
        "create-and-test-a-single-field-index",
        "Create and Test a Single-Field Index",
        "20 min",
        "Beginner",
        "Index product SKU and compare explain output before and after.",
        [
            (
                "Baseline SKU lookup",
                "Run:\n\n"
                + js(
                    """db.products.find({ sku: "L100" }).explain("executionStats")"""
                ),
                "Record winning stage and examined counts. Expect COLLSCAN unless an earlier SKU index exists.",
            ),
            (
                "Create the index",
                "Run:\n\n"
                + js(
                    """db.products.createIndex(
  { sku: 1 },
  { name: "idx_products_sku" }
)
db.products.getIndexes()"""
                ),
                "The index list includes `idx_products_sku` with key `{ sku: 1 }`.",
            ),
            (
                "Re-explain",
                "Repeat the L100 find explain. Confirm the winning index name.",
                "IXSCAN on idx_products_sku. Keys and docs examined should be near 1, nReturned 1.",
            ),
            (
                "Tradeoff note",
                "Write one sentence: what write and storage cost did you add, and which query shape it serves.",
                "Each product insert/update of sku maintains this index. It serves equality lookup by SKU.",
            ),
        ],
        [
            "Before and after explain numbers are recorded",
            "getIndexes shows idx_products_sku",
            "A write-cost sentence exists",
        ],
    )
)

GUIDES.append(
    guide(
        "lab",
        3,
        "design-a-compound-index",
        "Design a Compound Index",
        "25 min",
        "Intermediate",
        "Build a compound index for active products by category sorted by price, then test prefix queries.",
        [
            (
                "Identify fields",
                "For `find({ category: \"ACCESSORY\", active: true }).sort({ price: 1 })`, write equality vs sort fields and propose a key.",
                "Equality: category, active. Sort: price. Proposal `{ category: 1, active: 1, price: 1 }`.",
            ),
            (
                "Create and explain",
                "Run:\n\n"
                + js(
                    """db.products.createIndex(
  { category: 1, active: 1, price: 1 },
  { name: "idx_products_category_active_price" }
)
db.products.find({
  category: "ACCESSORY",
  active: true
}).sort({ price: 1 }).explain("executionStats")"""
                ),
                "Winning index is the new compound index. Look for IXSCAN and no blocking SORT.",
            ),
            (
                "Test a prefix query",
                "Explain `db.products.find({ category: \"LAPTOP\" })` and `db.products.find({ active: true })`.",
                "Category-only can use the leading prefix. Active-only generally cannot.",
            ),
            (
                "Record unsupported shapes",
                "Write one query this index does **not** support well (for example sort by name, or filter only price).",
                "A concrete unsupported shape is written, with a one-line reason (prefix or sort mismatch).",
            ),
        ],
        [
            "Compound index exists with the intended name",
            "The target query uses that index",
            "A prefix success and a prefix failure are noted",
        ],
    )
)

GUIDES.append(
    guide(
        "lab",
        4,
        "support-filtering-and-sorting",
        "Support Filtering and Sorting",
        "25 min",
        "Intermediate",
        "Compare compound-index orders for a customer’s newest orders in a date range, limited to ten.",
        [
            (
                "Write the query",
                "Using C101’s `_id` as `cid` and a start date of `ISODate(\"2026-08-01T00:00:00Z\")`:\n\n"
                + js(
                    """db.orders.find({
  customerId: cid,
  createdAt: { $gte: ISODate("2026-08-01T00:00:00Z") }
}).sort({ createdAt: -1 }).limit(10)"""
                )
                + "\nExplain it before adding an orders index (besides `_id`).",
                "Baseline plan recorded. Equality customerId, sort/range createdAt.",
            ),
            (
                "Create the ESR-aligned index",
                "Run:\n\n"
                + js(
                    """db.orders.createIndex(
  { customerId: 1, createdAt: -1 },
  { name: "idx_orders_customer_created" }
)"""
                )
                + "\nRe-explain the query.",
                "IXSCAN on idx_orders_customer_created. Sort should be satisfied by the index.",
            ),
            (
                "Compare a worse order",
                "Create `{ createdAt: -1, customerId: 1 }` as `idx_orders_created_customer` only if you have time, explain the same query, then drop that experimental index.",
                "Leading with the range/sort field scans more keys across customers. Evidence favors customerId first. Drop the experimental index.",
            ),
            (
                "Choose and document",
                "Keep idx_orders_customer_created. Write why ESR put equality first here.",
                "A short justification: one customer’s keys are contiguous, then dates are ordered for newest-first and the range.",
            ),
        ],
        [
            "The customer+createdAt index exists",
            "Explain shows IXSCAN for the history query",
            "A worse field order is rejected with evidence or reasoning",
        ],
    )
)

GUIDES.append(
    guide(
        "lab",
        5,
        "index-nested-fields-and-arrays",
        "Index Nested Fields and Arrays",
        "25 min",
        "Intermediate",
        "Index a dotted customer email path and product tags, then confirm nested and multikey behavior.",
        [
            (
                "Nested email index",
                "Run:\n\n"
                + js(
                    """db.customers.createIndex(
  { "contact.email": 1 },
  { name: "idx_customers_contact_email" }
)
db.customers.find({ "contact.email": "aisha@example.com" }).explain("executionStats")"""
                ),
                "IXSCAN on idx_customers_contact_email. nReturned 1.",
            ),
            (
                "Multikey tags index",
                "Run:\n\n"
                + js(
                    """db.products.createIndex(
  { tags: 1 },
  { name: "idx_products_tags" }
)
db.products.find({ tags: "technology" }).explain("executionStats")
db.products.getIndexes()"""
                ),
                "The tags index is listed. Explain uses it. getIndexes / explain may show `multikey: true`.",
            ),
            (
                "Inspect multikey",
                "In getIndexes output for idx_products_tags, find `multikey` (and optional `multikeyPaths`). Query tags `\"wireless\"` as well.",
                "multikey is true because tags is an array. Several accessories match wireless.",
            ),
            (
                "Record examined counts",
                "Write keys examined and docs examined for the email query and the technology-tag query.",
                "Two rows of stats. Email should be a single-key lookup; tags examines keys for matching array values.",
            ),
        ],
        [
            "Email query uses the dotted-path index",
            "Tags index is identified as multikey",
            "Examined counts are recorded for both",
        ],
    )
)

GUIDES.append(
    guide(
        "lab",
        6,
        "implement-data-integrity-indexes",
        "Implement Data-Integrity Indexes",
        "20 min",
        "Intermediate",
        "Create unique indexes for SKU, customer number, and order number, then prove duplicate inserts fail.",
        [
            (
                "Unique SKU",
                "If `idx_products_sku` exists, drop it first (MongoDB cannot keep two indexes on the same keys). Then:\n\n"
                + js(
                    """db.products.dropIndex("idx_products_sku")
db.products.createIndex(
  { sku: 1 },
  { unique: true, name: "uq_products_sku" }
)"""
                ),
                "uq_products_sku exists with unique: true. dropIndex errors if the non-unique index was never created — that is fine; proceed to createIndex.",
            ),
            (
                "Unique customer and order numbers",
                "Run:\n\n"
                + js(
                    """db.customers.createIndex(
  { customerNumber: 1 },
  { unique: true, name: "uq_customers_customer_number" }
)
db.orders.createIndex(
  { orderNumber: 1 },
  { unique: true, name: "uq_orders_order_number" }
)"""
                ),
                "Both unique indexes build because the loader has no duplicates.",
            ),
            (
                "Attempt a duplicate SKU",
                "Run:\n\n"
                + js(
                    """db.products.insertOne({
  sku: "L100",
  name: "Duplicate SKU test",
  category: "LAPTOP",
  price: Decimal128("1.00"),
  active: false,
  tags: ["temp"],
  createdAt: new Date()
})"""
                ),
                "Duplicate key error (E11000) mentioning sku / uq_products_sku. The extra document is not inserted.",
            ),
            (
                "Cleanup discussion",
                "Write what you would do if unique creation failed because duplicates already existed.",
                "Find duplicates with a `$group` on the key having `$sum: 1` and `$match` count > 1, merge or delete extras, then retry createIndex. Do not skip uniqueness because the build failed once.",
            ),
        ],
        [
            "Three unique indexes exist",
            "A duplicate SKU insert is rejected",
            "A duplicate-cleanup approach is noted",
        ],
    )
)

GUIDES.append(
    guide(
        "lab",
        7,
        "implement-partial-and-ttl-indexes",
        "Implement Partial and TTL Indexes",
        "25 min",
        "Intermediate",
        "Create a partial index for active products and a TTL index on a dedicated sessions collection.",
        [
            (
                "Partial index",
                "Run:\n\n"
                + js(
                    """db.products.createIndex(
  { category: 1, price: 1 },
  {
    partialFilterExpression: { active: true },
    name: "idx_active_products_category_price"
  }
)
db.products.getIndexes()"""
                ),
                "The index lists partialFilterExpression `{ active: true }`.",
            ),
            (
                "Compatible vs incompatible query",
                "Explain both:\n\n"
                + js(
                    """db.products.find({ category: "LAPTOP", active: true, price: { $lte: Decimal128("2000.00") } }).explain("executionStats")
db.products.find({ category: "LAPTOP", price: { $lte: Decimal128("2000.00") } }).explain("executionStats")"""
                ),
                "The query that includes `active: true` can use the partial index. The query that omits it typically will not, because inactive laptops (L190) are not in that index.",
            ),
            (
                "Create sessions and TTL",
                "Run:\n\n"
                + js(
                    """db.sessions.drop()
db.sessions.insertMany([
  { sessionId: "S1", user: "aisha", expiresAt: new Date(Date.now() + 60 * 60 * 1000) },
  { sessionId: "S-EXPIRED", user: "temp", expiresAt: new Date(Date.now() - 60 * 1000) }
])
db.sessions.createIndex(
  { expiresAt: 1 },
  { expireAfterSeconds: 0, name: "ttl_sessions_expires_at" }
)
db.sessions.getIndexes()"""
                ),
                "ttl_sessions_expires_at exists with expireAfterSeconds: 0. Two documents are present immediately after insert.",
            ),
            (
                "Observe asynchronous expiration",
                "Wait about 60 seconds (TTL monitor interval), then `db.sessions.find()`. Do not block the class if the expired row is still there — record that expiration is asynchronous.",
                "S-EXPIRED may disappear after the TTL thread runs. The lab succeeds if the index is configured correctly even if the delete has not fired yet. Never treat TTL as a real-time guarantee.",
            ),
        ],
        [
            "Partial filter is visible on the product index",
            "A compatible query is distinguished from an incompatible one",
            "TTL index is created on sessions.expiresAt",
            "Asynchronous cleanup is stated",
        ],
    )
)

GUIDES.append(
    guide(
        "lab",
        8,
        "build-a-covered-query",
        "Build a Covered Query",
        "20 min",
        "Intermediate",
        "Create a covering index and test a projection that can be satisfied from the index alone.",
        [
            (
                "Create the covering index",
                "Run:\n\n"
                + js(
                    """db.products.createIndex(
  { category: 1, price: 1, name: 1 },
  { name: "idx_products_category_price_name" }
)"""
                ),
                "Index exists. `_id` is not in this key.",
            ),
            (
                "Query that can be covered",
                "Run:\n\n"
                + js(
                    """db.products.find(
  { category: "BOOK" },
  { _id: 0, name: 1, price: 1 }
).explain("executionStats")"""
                ),
                "Look for IXSCAN on idx_products_category_price_name and **no FETCH** (or a covering projection stage). totalDocsExamined is often 0 when covered.",
            ),
            (
                "Break coverage",
                "Re-explain the same filter with `{ name: 1, price: 1 }` ( `_id` included) and with `{ name: 1, tags: 1, _id: 0 }`.",
                "Including `_id` or tags should introduce FETCH / document examination.",
            ),
            (
                "Write the rule",
                "One sentence: when is this catalog projection covered, and how do you confirm?",
                "Covered when filter and output fields (including `_id` handling) live in the index; confirm with explain, not by guessing.",
            ),
        ],
        [
            "Covering index exists",
            "The `_id: 0` projection is tested",
            "A non-covered variant is contrasted",
        ],
    )
)

GUIDES.append(
    guide(
        "lab",
        9,
        "tune-an-aggregation-pipeline",
        "Tune an Aggregation Pipeline",
        "25 min",
        "Intermediate",
        "Index an early $match/$sort on paid orders, then explain which later stages still run in memory.",
        [
            (
                "Baseline pipeline explain",
                "Run:\n\n"
                + js(
                    """db.orders.explain("executionStats").aggregate([
  { $match: { paymentStatus: "PAID" } },
  { $sort: { createdAt: -1 } },
  { $group: {
      _id: "$fulfillmentStatus",
      revenue: { $sum: "$total" },
      orderCount: { $sum: 1 }
  }}
])"""
                ),
                "Record whether $match/$sort used COLLSCAN and whether a sort stage appears. Do not expect $group to use an index.",
            ),
            (
                "Create a supporting index",
                "Run:\n\n"
                + js(
                    """db.orders.createIndex(
  { paymentStatus: 1, createdAt: -1 },
  { name: "idx_orders_payment_created" }
)"""
                )
                + "\nRe-explain the same pipeline.",
                "Winning plan for the cursor should show IXSCAN on idx_orders_payment_created for the match/sort prefix.",
            ),
            (
                "Compare statistics",
                "Compare totalDocsExamined / keys examined before and after. Note nReturned from the group (number of fulfillment statuses).",
                "Examined counts should drop or the stage should switch from COLLSCAN to IXSCAN. Group output still has a few buckets (SHIPPED, DELIVERED, and similar).",
            ),
            (
                "Explain remaining memory work",
                "Write which stages still cannot be served by this index.",
                "$group (and accumulators) still process documents in the pipeline after the indexed match/sort. Indexing does not remove grouping work.",
            ),
        ],
        [
            "Baseline and post-index explains exist",
            "idx_orders_payment_created is used for $match/$sort",
            "$group is identified as remaining in-memory work",
        ],
    )
)

GUIDES.append(
    guide(
        "lab",
        10,
        "audit-and-rationalize-indexes",
        "Audit and Rationalize Indexes",
        "25 min",
        "Intermediate",
        "List indexes, spot overlapping prefixes, hide one candidate, test, unhide, and recommend retain/redesign/remove — without dropping a needed index.",
        [
            (
                "Inventory",
                "Run for products, customers, orders, reviews, and sessions:\n\n"
                + js(
                    """db.getCollectionNames()
db.products.getIndexes()
db.orders.getIndexes()
db.products.aggregate([{ $indexStats: {} }])"""
                ),
                "A table of indexes by collection. Usage counts may be low or zero depending on process uptime — interpret with that caveat.",
            ),
            (
                "Spot overlap",
                "On products, compare category-leading indexes (single-field category, category+active+price, category+price+name, partial category+price). Note prefix overlap.",
                "At least one overlapping prefix pair is written down.",
            ),
            (
                "Hide and test",
                "Hide a **non-unique, non-TTL** training index you suspect is redundant, for example `idx_products_category` if it exists:\n\n"
                + js(
                    """db.products.hideIndex("idx_products_category")
db.products.find({ category: "ACCESSORY" }).explain("queryPlanner")
db.products.unhideIndex("idx_products_category")"""
                ),
                "While hidden, the planner should not select that index. After unhide, it is eligible again. If the name does not exist, hide another secondary index from your list — never hide `_id_`.",
            ),
            (
                "Recommend",
                "For the hidden candidate, write retain, redesign, or remove, with one evidence sentence. Do **not** drop it in this lab.",
                "A recommendation exists. No production-style drop was performed.",
            ),
        ],
        [
            "Indexes are grouped by collection",
            "One index was hidden and unhidden",
            "No required unique/TTL index was dropped",
        ],
    )
)

GUIDES.append(
    guide(
        "lab",
        11,
        "integrated-query-tuning-challenge",
        "Integrated Query-Tuning Challenge",
        "40–45 min",
        "Intermediate",
        "Tune the product-catalog page and customer-order-history page using baselines, ESR, explain, and a write-cost note.",
        [
            (
                "Capture both shapes",
                "Catalog: active products, category ACCESSORY, optional price ≤ 100, sort price, return name, price, category. History: C101, PAID, newest first, createdAt ≥ 2026-08-01, limit 20. Write both queries.",
                "Two complete mongosh queries including projection and limit.",
            ),
            (
                "Baselines",
                "explain(\"executionStats\") both queries before changing indexes. Fill nReturned, keys, docs, SORT yes/no.",
                "Two baseline rows. Existing indexes from earlier labs are allowed; note them.",
            ),
            (
                "Propose and create ESR indexes",
                "Catalog candidate `{ category: 1, active: 1, price: 1 }` (may already exist). History candidate `{ customerId: 1, paymentStatus: 1, createdAt: -1 }` or `{ customerId: 1, createdAt: -1 }` depending on whether PAID is always present. Create any missing named indexes.",
                "Indexes exist. Field order is written with equality, sort, and range labeled.",
            ),
            (
                "Re-explain and compare",
                "Rerun both explains. Compare examined vs returned. For the catalog projection, optionally exclude `_id` and extra fields and note coverage.",
                "IXSCAN on the intended indexes. Examined counts are closer to returned counts than the baseline, or SORT is gone.",
            ),
            (
                "Cost and recommendation",
                "List the indexes you would keep for these two pages, their write/storage impact, and one index you would **not** add.",
                "A short recommendation: keep the two (or three) named indexes; do not index every catalog field; unique SKU remains a separate integrity index.",
            ),
        ],
        [
            "Both query shapes are written",
            "Before and after explain stats exist",
            "ESR field order is justified",
            "Write/storage impact is mentioned",
        ],
    )
)

GUIDES.append(
    guide(
        "exercise",
        13,
        "practical-challenge",
        "E-Commerce Index Review",
        "30–45 min",
        "Intermediate",
        "Produce an index recommendation for ten training-store query patterns, including specialized types and overlap checks.",
        [
            (
                "Tabulate ten patterns",
                "For each workload item (SKU lookup, category browse, tags, email, order number, order history, paid reporting, reviews newest first, session expiration, dynamic attributes), write query shape and a proposed index.",
                "A ten-row table exists. Unique, multikey, partial, TTL, and wildcard candidates are marked.",
            ),
            (
                "Justify field order and costs",
                "For every compound index, state ESR roles and one write/storage sentence. Flag any overlapping prefixes (for example category vs category+active+price).",
                "Compound orders are justified. At least one overlap is called out with a retain/hide plan.",
            ),
            (
                "Validation plan",
                "Write how you would prove two high-traffic indexes with explain (catalog and order history) and how you would roll back.",
                "Baseline → createIndex → executionStats comparison → dropIndex rollback with the original createIndex saved.",
            ),
        ],
        [
            "Ten query shapes have proposed indexes",
            "Specialized types are used appropriately (not everywhere)",
            "Overlap and write cost are considered",
            "Explain validation is part of the plan",
        ],
        discussion=True,
        extra="""## Workload checklist

1. Product lookup by SKU  
2. Product browsing by category, active status, and price  
3. Product searches by tag  
4. Customer lookup by email  
5. Order lookup by order number  
6. Customer-order history sorted by date  
7. Paid-order reporting by date  
8. Product-review retrieval sorted newest first  
9. Session expiration  
10. Product search over dynamic category attributes  
""",
    )
)


def write_all() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for kind, num, slug, title, time, typ, objective, md in GUIDES:
        prefix = "exercise" if kind == "exercise" else "lab"
        path = OUT / f"{prefix}-6.{num}-{slug}.md"
        path.write_text(md.strip() + "\n", encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)} ({typ}, {time}) — {title}")
    print(f"Done. {len(GUIDES)} lab guides.")


if __name__ == "__main__":
    write_all()
