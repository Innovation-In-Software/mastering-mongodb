"""Write Module 8 lab guides. Run: python scripts/module08_labs.py"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "slide-exercises" / "module-08"

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

**Scratch database:** Labs that change validation, users, or restored data use `training_store_ops` so `training_store` stays intact for later work.

**Small-data note:** Twelve products and seventeen orders will not produce dramatic wall-clock wins. Record **plan shape**, **examined vs returned**, and **correctness**, not stopwatch time.
"""

ENV_DISCUSSION = """## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Capture answers in a notes file.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional |
| Timer | Instructor clocks this | — |

You may use `mongosh` to inspect `training_store`, but reasoning is the deliverable unless a step says otherwise. Do not enable authentication on a shared training instance unless the instructor provides a disposable environment.
"""


def js(code: str) -> str:
    return f"```javascript\n{code.strip()}\n```"


def yaml_block(code: str) -> str:
    return f"```yaml\n{code.strip()}\n```"


def text_block(code: str) -> str:
    return f"```text\n{code.strip()}\n```"


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
    extra_block = f"{extra.strip()}\n\n" if extra.strip() else ""
    md = f"""# {label} 8.{num}: {title}

**Module 8:** MongoDB Best Practices, Security, and Troubleshooting  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 8)  
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

{extra_block}## Success criteria

{checks}

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
"""
    return (kind, num, slug, title, time, "discussion" if discussion else "hands-on", objective, md)


GUIDES: list[tuple] = []

# ---------------------------------------------------------------------------
# Discussion exercises 8.1–8.13 + practical challenge 8.14
# ---------------------------------------------------------------------------

GUIDES.append(
    guide(
        "exercise",
        1,
        "review-a-document-model",
        "Review a Document Model",
        "15 min",
        "Beginner",
        "Evaluate a customer-order document for access-pattern alignment, ownership, duplication, types, growth, snapshots, sensitive data, and validation.",
        [
            (
                "Score the document",
                "Review this order-shaped document and mark each area as strong, risky, or missing: access patterns, ownership, duplication, BSON types, array growth, historical snapshots, sensitive fields, and validation.\n\n"
                + js(
                    """{
  _id: ObjectId("..."),
  orderNumber: "O5001",
  customer: {
    customerNumber: "C101",
    name: "Aisha Khan",
    email: "aisha@example.com",
    passwordHash: "sha256:demo-not-real",
    loyaltyPoints: 1840
  },
  items: [ { sku: "L100", qty: 1, price: "1299.00" } ],
  createdAt: "2026-07-12",
  notes: []
}"""
                ),
                "Risky/missing: price as string, date as string, unbounded `notes`, live customer fields (email, loyalty, password hash) instead of a snapshot plus a reference, no statuses or Decimal128 total, sensitive hash stored on the order.",
            ),
            (
                "Rewrite the boundary",
                "Write the corrected document boundary: what stays on the order, what is referenced, and one validation rule you would add first.",
                "Order keeps orderNumber, customerId, purchase-time name/address/price snapshots, items, statuses, Decimal128 total, Date createdAt. Customer master stays in customers. First validator: required orderNumber, customerId, items, paymentStatus, total, createdAt.",
            ),
        ],
        [
            "At least four risks are named with evidence from the document",
            "The rewrite separates customer master data from the order aggregate",
            "A first validation rule is specific (field + type or enum)",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        2,
        "find-the-schema-anti-patterns",
        "Find the Schema Anti-Patterns",
        "15 min",
        "Beginner",
        "Identify unbounded arrays, textual prices, inconsistent names, deep nesting, duplicated live customer data, missing required fields, and string timestamps, then propose a corrected design.",
        [
            (
                "Name the anti-patterns",
                "On the product document below, list every anti-pattern from the module list.\n\n"
                + js(
                    """{
  Product_Name: "Trail shoe",
  productPrice: "89.99",
  details: { catalog: { store: { web: { active: "yes" } } } },
  customer: { email: "aisha@example.com", lastOrderTotal: 210.50 },
  reviews: [ /* every review ever */ ],
  updated: "2026-09-01 09:00"
}"""
                ),
                "Unbounded reviews; price as text; mixed names (`Product_Name` vs `productPrice`); unnecessary nesting; live customer data on a product; missing sku/category/Decimal128/Boolean/Date; string timestamp; boolean as text.",
            ),
            (
                "Corrected sketch",
                "Sketch the replacement: product core fields, where reviews live, and how customer data is removed.",
                "products: sku, name, category, Decimal128 price, Boolean active, Date updatedAt, bounded attributes. reviews collection keyed by productId. No customer object on the product.",
            ),
        ],
        [
            "Seven anti-pattern categories are identified",
            "Reviews are moved off the product",
            "Price and dates use BSON types, not strings",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        3,
        "review-a-query-and-projection",
        "Review a Query and Projection",
        "15 min",
        "Beginner",
        "Improve a query that returns complete order documents by adding a selective filter, projection, deterministic sort, limit, and a candidate index.",
        [
            (
                "Rewrite the query",
                "The application only needs C101’s paid orders, newest first, ten at a time, showing orderNumber, fulfillmentStatus, total, and createdAt. Rewrite:\n\n"
                + js("db.orders.find({})"),
                "Filter on customerId + paymentStatus PAID; projection of the four fields (and usually `_id: 0`); `.sort({ createdAt: -1 })`; `.limit(10)`.",
            ),
            (
                "Name a candidate index",
                "Write one compound index that supports the filter and sort. Label equality vs sort fields.",
                "`{ customerId: 1, paymentStatus: 1, createdAt: -1 }` — equality, equality, sort. Do not lead with createdAt.",
            ),
        ],
        [
            "The rewrite is selective (not find({}))",
            "Projection, sort, and limit are present",
            "The candidate index follows Equality–Sort–Range",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        4,
        "optimize-an-aggregation-pipeline",
        "Optimize an Aggregation Pipeline",
        "20 min",
        "Intermediate",
        "Reorder and simplify a pipeline that looks up customers before filtering orders, unwinds every item, carries unused fields, groups incorrectly, and sorts too early.",
        [
            (
                "Name the defects",
                "The pipeline runs `$lookup` customers, then `$unwind` items, then `$match` PAID, then `$sort` by date, then `$group` summing `total`. List what is wrong and why `$group` after `$unwind` can over-count revenue.",
                "Lookup and unwind happen before filtering; unused customer fields travel the pipeline; sort before the final metric is wasted work; summing parent `total` after unwind multiplies revenue by item count.",
            ),
            (
                "Propose a safer order",
                "Write a conceptual stage order that preserves paid-order monthly revenue and unique customers. State where `$unwind` is allowed.",
                "`$match` PAID (and date window if any) → `$project` needed fields → `$set` month → group for order-level metrics first, or unwind only to sum line quantities. `$lookup` only if the report needs names, after grouping. `$sort` last.",
            ),
        ],
        [
            "Early `$match` is required in the rewrite",
            "Double-counting of `total` after `$unwind` is named",
            "`$lookup` is delayed or justified",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        5,
        "rationalize-an-index-portfolio",
        "Rationalize an Index Portfolio",
        "20 min",
        "Intermediate",
        "Review overlapping category indexes, name supported queries, flag low-selectivity keys, and describe evidence required before removal.",
        [
            (
                "Map overlap",
                "Given these indexes, mark which prefixes overlap and which queries each can support:\n\n"
                + js(
                    """{ category: 1 }
{ category: 1, price: 1 }
{ category: 1, price: 1, name: 1 }
{ active: 1 }
{ category: 1, active: 1, price: 1 }"""
                ),
                "The three category+price variants overlap; `{ category: 1 }` is a prefix of the others. `{ active: 1 }` is low-selectivity and does not overlap those prefixes. `{ category: 1, active: 1, price: 1 }` is a different leading pair than category+price.",
            ),
            (
                "Safe testing plan",
                "Write the sequence before dropping any index: workload review, explain, hide, monitor, drop with rollback. Name one index you would not hide on appearance alone.",
                "Hide `{ category: 1 }` only after catalog and reporting explains still use a remaining compound index. Do not hide `{ category: 1, active: 1, price: 1 }` without measuring the active-catalog shape. `{ active: 1 }` is a hide candidate after proving no query needs it.",
            ),
        ],
        [
            "Overlapping prefixes are identified",
            "`active` is treated as low-selectivity",
            "Hide-then-monitor is required before drop",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        6,
        "design-least-privilege-roles",
        "Design Least-Privilege Roles",
        "20 min",
        "Beginner",
        "Define permitted and prohibited operations for application, reporting, support, monitoring, backup, and administrator identities.",
        [
            (
                "Fill the permission matrix",
                "For each identity — application service, reporting service, support engineer, monitoring service, backup service, database administrator — list one permitted operation and one prohibited operation on `training_store`.",
                "App: read/write app collections, not userAdmin. Reporting: read approved collections, not update. Support: read (maybe limited PII), not drop. Monitoring: clusterMonitor-style, not data writes. Backup: backup privileges, not arbitrary deletes. DBA: admin with change control, not used by the app.",
            ),
            (
                "Call out the anti-pattern",
                "Write two sentences on why the application must not use a cluster-administrator account, even in training-like environments that later become production.",
                "A stolen app credential would inherit every privilege. Least privilege limits blast radius and makes audit trails meaningful.",
            ),
        ],
        [
            "Six identities have permit and deny examples",
            "The application is not given clusterAdmin",
            "Reporting is read-only",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        7,
        "identify-security-risks",
        "Identify Security Risks",
        "15 min",
        "Beginner",
        "Rank risks in a fictional environment with a public endpoint, shared admin account, plaintext connection string, no TLS, unprotected backups, and production data in development.",
        [
            (
                "Rank the six risks",
                "Rank these from most urgent to least: public database endpoint; shared administrator account; plaintext URI in source control; no TLS; unprotected backups; production data copied to development. Give a one-line business impact for the top three.",
                "Typical top three: public endpoint (internet attack surface), no TLS (credential and data interception), secrets in source control (credential leak). Shared admin and prod-in-dev and open backups remain high.",
            ),
            (
                "Propose mitigations",
                "For each of the six, write one concrete control (network, identity, encryption, secret storage, or data handling).",
                "Private network + allowlist; named accounts + MFA/rotation; secret manager; TLS with validation; encrypted backups with access control; masked or synthetic non-prod data.",
            ),
        ],
        [
            "A ranked list exists",
            "Top risks include exposure and credential leakage",
            "Each risk has a mitigation",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        8,
        "define-rpo-and-rto",
        "Define RPO and RTO",
        "15 min",
        "Beginner",
        "Propose recovery point and recovery time objectives, backup frequency, recovery method, and validation for catalog, customers, orders, payments, and reviews.",
        [
            (
                "Assign objectives",
                "For product catalog, customer profiles, orders, payments, and reviews, write RPO, RTO, and a backup frequency that could meet the RPO. Use the store as a small retailer, not a global bank.",
                "Payments and orders typically get the tightest RPO (minutes) and tested point-in-time recovery. Catalog can often tolerate a longer RPO. Reviews are usually the most tolerant. RTO for checkout should be shorter than for reviews.",
            ),
            (
                "Name validation",
                "For orders, write how you would prove a restore: counts, sample order numbers, indexes, and a checkout read.",
                "Compare `countDocuments` to the pre-restore note; find O5001 and a paid total; `getIndexes()`; application can read an order. Backup success alone is not enough.",
            ),
        ],
        [
            "RPO and RTO are defined as time quantities",
            "Orders/payments are stricter than reviews",
            "Restore validation includes data and access, not only the backup job",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        9,
        "design-a-monitoring-dashboard",
        "Design a Monitoring Dashboard",
        "20 min",
        "Beginner",
        "Select essential metrics for availability, query performance, resources, connections, replication, sharding, storage, backups, and security — each with an operational purpose.",
        [
            (
                "Pick twelve tiles",
                "Choose at most twelve dashboard tiles that a weekday on-call would actually use. For each, write the metric and the question it answers. Reject vanity metrics.",
                "Examples: primary/alive, request latency p99, slow ops, CPU, disk %, connections vs limit, replication lag, oplog window, targeted vs scatter (if sharded), backup last success, auth failures. Not: ‘documents in collection’ with no threshold.",
            ),
            (
                "Drop two candidates",
                "Name two metrics you would leave off the primary dashboard and why.",
                "Per-collection document counts or raw opcounters without a baseline are noise. Shard-balancer internals may belong on a secondary view unless the cluster is sharded and balancing is a live risk.",
            ),
        ],
        [
            "Each tile has a purpose question",
            "Availability, latency, replication, backup, and security appear",
            "At least one metric is explicitly excluded",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        10,
        "set-alert-priorities",
        "Set Alert Priorities",
        "15 min",
        "Beginner",
        "Classify operational alerts as critical, high, medium, or informational and name the first action for each.",
        [
            (
                "Classify eight alerts",
                "Classify: no primary; increasing replication lag; disk 90% full; backup failed; authentication-failure spike; slow-query increase; one secondary unavailable; high connection usage.",
                "Critical: no primary. High: disk 90%, backup failed, auth-failure spike, lag still growing toward oplog risk. Medium: one secondary down (if majority remains), high connections, slow-query increase. Informational: brief lag blip with a known backup window — if you alert at all.",
            ),
            (
                "Attach first actions",
                "For critical and high items, write the first action and the runbook name you would open.",
                "No primary → check replica-set status and network, do not reconfigure hastily. Disk 90% → identify growth, free space, page the owner. Backup failed → verify job, storage, credentials. Auth spike → confirm not a deploy, then lock down.",
            ),
        ],
        [
            "No primary is critical",
            "Each high alert has a first action",
            "Not every metric is critical",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        11,
        "diagnose-an-operational-incident",
        "Diagnose an Operational Incident",
        "20 min",
        "Intermediate",
        "Determine likely cause, mitigation, evidence, permanent correction, and prevention when the order API slows after a release with higher documentsExamined and an unchanged index set.",
        [
            (
                "Form the hypothesis",
                "Evidence: CPU moderately up; documents examined up sharply; no election; connections normal; a query filter changed; indexes unchanged. What is the likely cause, and what is not the cause?",
                "Likely: the new filter no longer uses the existing index (predicate, type, or field name), causing a collection scan or a weakly selective plan. Not: failover, connection exhaustion, or a missing replica set.",
            ),
            (
                "Mitigate and prevent",
                "Write immediate mitigation, evidence to collect, permanent correction, and one prevention action for the next release.",
                "Mitigate: revert the filter or add a matching index if the new shape is intended. Collect: the exact query, explain before/after, deploy diff. Permanent: index for the new shape or restore the selective predicate. Prevent: explain the changed query in staging; include query-shape review in the release checklist.",
            ),
        ],
        [
            "Hypothesis ties the filter change to examined-document growth",
            "Failover is ruled out with evidence",
            "Prevention includes testing explain on the new shape",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        12,
        "create-an-operational-runbook",
        "Create an Operational Runbook",
        "20 min",
        "Intermediate",
        "Write a runbook for one event: no primary, rising replication lag, disk nearing capacity, backup failure, authentication failures, or a slow-query spike.",
        [
            (
                "Fill the template",
                "Pick one event. Write: alert name, meaning, business impact, required access, diagnostic commands, expected normal state, decision points, corrective actions, escalation, rollback, verification, and where the incident is documented.",
                "A complete page exists. Diagnostics are real commands (`rs.status()`, `explain`, disk checks). Corrective actions are sequenced. Escalation has a person or role, not ‘tell someone’.",
            ),
            (
                "Add a verification step",
                "Write how you know the incident is over (metric + user-facing check) and what you will change so it does not recur silently.",
                "Example: primary exists for 15 minutes, checkout succeeds, lag < baseline. Follow-up: alert threshold, dashboard tile, or change-review item.",
            ),
        ],
        [
            "The runbook is for a single named alert",
            "Diagnostics and verification are concrete",
            "Escalation and rollback are present",
        ],
        discussion=True,
        extra="""## Runbook template

| Section | Your notes |
|---------|------------|
| Alert name | |
| Meaning | |
| Business impact | |
| Required access | |
| Diagnostic commands | |
| Expected normal state | |
| Decision points | |
| Corrective actions | |
| Escalation | |
| Rollback | |
| Verification | |
| Incident documentation | |
""",
    )
)

GUIDES.append(
    guide(
        "exercise",
        13,
        "complete-a-production-readiness-assessment",
        "Complete a Production-Readiness Assessment",
        "25 min",
        "Intermediate",
        "Assess a fictional deployment across data model, queries, indexes, security, availability, backup, monitoring, documentation, and ownership, then classify it as ready, ready with conditions, or not ready.",
        [
            (
                "Score nine areas",
                "Using the fictional `training_store` production story on the slides (no validation, mixed price types, embedded unbounded reviews, broad queries, overlapping indexes, shared admin credentials, public network, untested failover, untested restore, CPU-only monitoring, no runbooks), mark each area Ready / Conditional / Not ready with one evidence sentence.",
                "Most areas are Not ready. Indexes might be Conditional if some useful keys exist but overlap is unproven. Availability is Conditional (replica set exists, failover untested).",
            ),
            (
                "Classify the deployment",
                "Choose one overall label and list the three conditions that would have to be true before a go-live.",
                "Not production-ready. Conditions typically: authentication + network restriction, tested backup restore, and indexed selective queries with a baseline. Shared admin and public exposure alone are enough to fail the gate.",
            ),
        ],
        [
            "Nine areas are scored with evidence",
            "Overall classification is Not ready (or Ready with conditions only if the learner tightens scope unrealistically — instructor challenges that)",
            "Three go-live conditions are specific",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        14,
        "practical-challenge",
        "Production-Readiness Review for training_store",
        "45 min",
        "Intermediate",
        "Produce a six-part action plan covering data model, performance, security, reliability, monitoring, and a final production-readiness classification with evidence.",
        [
            (
                "Write model and performance recommendations",
                "Correct BSON types; separate unbounded reviews; preserve order snapshots; add validation; plan migration. Then rewrite broad queries, add projections, tune the sales aggregation, recommend indexes, flag redundant indexes, and name baseline metrics.",
                "A two-section note exists. Reviews are a collection. Prices are Decimal128. Queries are selective. Indexes follow ESR. At least one overlapping index is flagged. Baseline includes latency, examined counts, and connections.",
            ),
            (
                "Write security, reliability, and monitoring",
                "Restrict network access; replace shared credentials; least privilege; TLS; secret storage; audit privileged activity. Test failover; review lag and oplog; define RPO/RTO; test restore. Add query, connection, storage, replication, backup, and security monitoring with three critical alerts and named owners.",
                "Security list includes network, authn, authz, TLS, secrets. Reliability includes tested failover and restore plus RPO/RTO. Monitoring has owners, not only metrics.",
            ),
            (
                "Classify with evidence",
                "Select Production-ready, Ready with conditions, or Not production-ready. Cite evidence from the current environment list (no validation, public network, untested restore, CPU-only monitoring, and the rest).",
                "Not production-ready is the defensible call. Ready with conditions is acceptable only if conditions are explicit and blocking. Production-ready is not justified.",
            ),
        ],
        [
            "All six deliverable sections are present",
            "Classification is supported by evidence",
            "Critical alerts have owners",
        ],
        discussion=True,
        extra="""## Current environment (do not treat as ready)

- Flexible documents without validation
- Several inconsistent price types
- Large review arrays embedded in products (in the scenario; `training_store` already separates reviews — call that out as the target state)
- Broad queries returning complete documents
- Multiple overlapping indexes
- Shared administrative credentials
- Public network access
- Replica set but no failover test
- Successful backups but no restore test
- Basic CPU monitoring only
- No operational runbooks

## Final classification

Choose one: **Production-ready** · **Ready with conditions** · **Not production-ready**
""",
    )
)

# ---------------------------------------------------------------------------
# Hands-on labs 8.1–8.11
# ---------------------------------------------------------------------------

GUIDES.append(
    guide(
        "lab",
        1,
        "data-model-review-and-repair",
        "Data-Model Review and Repair",
        "25 min",
        "Intermediate",
        "Inspect training_store documents, identify inconsistent names and types, unbounded growth risks, and snapshot gaps, then propose validation and a migration note.",
        [
            (
                "Inspect types and names",
                "Run and record field-name and type surprises:\n\n"
                + js(
                    """use training_store
db.products.find({}, { sku: 1, name: 1, price: 1, active: 1 }).limit(5)
db.products.find({ sku: "XBAD" }, { sku: 1, price: 1 })
db.products.aggregate([
  { $project: { sku: 1, priceType: { $type: "$price" } } }
])"""
                ),
                "`XBAD` shows `price` as string. Healthy products show Decimal128. That mixed type is the catalog anti-pattern to repair.",
            ),
            (
                "Check growth and snapshots",
                "Compare `db.products.findOne({}, { reviews: 1, sku: 1 })` with `db.reviews.findOne()` and `db.orders.findOne({ orderNumber: \"O5001\" }, { items: 1, customerId: 1, shippingAddress: 1 })`. Note whether reviews are embedded and whether order items snapshot price.",
                "Reviews live in `reviews` (good). Orders embed line snapshots and reference `customerId` (good). Call out any missing snapshot fields you would still add (for example purchase-time product name if absent).",
            ),
            (
                "Propose validation and migration",
                "Write: (1) three validator rules for products, (2) what to do with `XBAD`, (3) whether to migrate in place or insert into a new collection first.",
                "Rules include sku string, Decimal128 price, Boolean active. `XBAD` is converted or quarantined. Prefer adding compatible fields and `validationAction: \"warn\"` or a staging collection before `error` on production data.",
            ),
        ],
        [
            "Mixed `price` types are documented",
            "Reviews are confirmed as a separate collection",
            "A migration note exists for `XBAD` and validation",
        ],
    )
)

GUIDES.append(
    guide(
        "lab",
        2,
        "query-and-projection-optimization",
        "Query and Projection Optimization",
        "25 min",
        "Intermediate",
        "Tighten assigned application queries with filters, correct BSON types, projection, stable sort, limit, explain output, and index recommendations.",
        [
            (
                "Baseline the broad query",
                "Run and record nReturned and totalDocsExamined:\n\n"
                + js(
                    """use training_store
db.orders.find({}).explain("executionStats")"""
                ),
                "The plan examines every order. nReturned equals the collection size. This is the ‘return everything’ anti-pattern.",
            ),
            (
                "Add filter, projection, sort, and limit",
                "Look up C101’s `_id`, then run:\n\n"
                + js(
                    """const c101 = db.customers.findOne({ customerNumber: "C101" })._id
db.orders.find(
  { customerId: c101, paymentStatus: "PAID" },
  { _id: 0, orderNumber: 1, fulfillmentStatus: 1, total: 1, createdAt: 1 }
).sort({ createdAt: -1 }).limit(10)"""
                ),
                "Only C101 paid orders, shaped fields, newest first, at most ten documents.",
            ),
            (
                "Explain and recommend an index",
                "Run `.explain(\"executionStats\")` on the improved query. Record winning stage, docs examined, and whether a SORT stage appears. Write one candidate index.",
                "Likely COLLSCAN on this small set unless Module 6 indexes remain. Candidate `{ customerId: 1, paymentStatus: 1, createdAt: -1 }`. Note examined vs returned.",
            ),
        ],
        [
            "Broad find({}) baseline is recorded",
            "Improved query uses filter, projection, sort, and limit",
            "An ESR-style index is recommended",
        ],
    )
)

GUIDES.append(
    guide(
        "lab",
        3,
        "aggregation-pipeline-construction",
        "Aggregation Pipeline Construction",
        "30 min",
        "Intermediate",
        "Build a monthly paid-sales report with month, order count, revenue, average order value, unique customers, and units sold using $match, $set or $project, $unwind, $group, $sort, and a final $project.",
        [
            (
                "Filter and stamp the month",
                "Start a pipeline that matches `paymentStatus: \"PAID\"` and sets `month` from `createdAt` (UTC date-to-string `YYYY-MM` is acceptable in training).\n\n"
                + js(
                    """db.orders.aggregate([
  { $match: { paymentStatus: "PAID" } },
  { $set: { month: { $dateToString: { format: "%Y-%m", date: "$createdAt" } } } }
])"""
                ),
                "About 13 paid orders remain. Each document has a `month` such as `2026-07`.",
            ),
            (
                "Unwind safely, then group twice",
                "Unwind `items`, group by `{ month: \"$month\", orderNumber: \"$orderNumber\" }` keeping `total` with `$first`, `customerId` with `$first`, and `units` as `$sum` of `$items.quantity`. Then group by month: `orderCount: { $sum: 1 }`, `revenue: { $sum: \"$total\" }`, `uniqueCustomers: { $addToSet: \"$customerId\" }`, `unitsSold: { $sum: \"$units\" }`.",
                "Revenue is not multiplied by line count. Units come from item quantities. July–September 2026 months appear.",
            ),
            (
                "Sort and shape",
                "Add `$set` for `uniqueCustomerCount: { $size: \"$uniqueCustomers\" }` and `averageOrderValue: { $divide: [\"$revenue\", \"$orderCount\"] }`, `$sort` by `_id` / month, and a final `$project` that outputs month, orderCount, revenue, averageOrderValue, uniqueCustomers, unitsSold.",
                "One document per month, sorted, with all six business metrics. No leftover `_id` object unless you alias it to `month`.",
            ),
        ],
        [
            "Required stages are present",
            "Revenue is not double-counted after `$unwind`",
            "Report includes unique customers and units sold",
        ],
        extra="""## Why two `$group` stages?

`$unwind` turns one order with three items into three documents. Summing the parent `total` there counts the order three times. Grouping back to one row per order (or summing only line-level quantity and line revenue) keeps the arithmetic honest.
""",
    )
)

GUIDES.append(
    guide(
        "lab",
        4,
        "aggregation-pipeline-tuning",
        "Aggregation Pipeline Tuning",
        "25 min",
        "Intermediate",
        "Capture an inefficient pipeline’s output and explain stats, then filter earlier, drop unused fields, control $unwind, review $lookup, and confirm identical business results.",
        [
            (
                "Run the slow shape",
                "Run this inefficient pipeline once and save the result documents plus `explain(\"executionStats\")` notes (stage order, docs leaving `$lookup`):\n\n"
                + js(
                    """db.orders.aggregate([
  { $lookup: {
      from: "customers",
      localField: "customerId",
      foreignField: "_id",
      as: "customer"
  }},
  { $unwind: "$items" },
  { $match: { paymentStatus: "PAID" } },
  { $group: { _id: "$customer.name.full", revenue: { $sum: "$total" } } }
])"""
                ),
                "Lookup and unwind run on unpaid orders too. Revenue is inflated where orders have multiple items. Record the output even if the numbers look ‘busy’.",
            ),
            (
                "Rewrite and compare",
                "Rewrite: `$match` PAID first, `$project` only fields you need, `$group` by `customerId` summing `$total` **without** unwinding, then `$lookup` names, then `$sort`. Compare revenue to a manual `find` of paid totals for C101.",
                "C101’s paid `total` sum matches the grouped revenue. Unpaid orders never enter `$lookup`. Explain shows a smaller working set after `$match`.",
            ),
            (
                "Index recommendation",
                "Write whether `{ paymentStatus: 1, createdAt: -1 }` (or `{ paymentStatus: 1 }`) would help this pipeline’s `$match`, and whether a `$lookup` on `customers._id` already has an index.",
                "`_id` is already indexed. A `paymentStatus` (and optional date) index can support the early `$match`. Do not index every grouped field.",
            ),
        ],
        [
            "Before and after outputs are recorded",
            "Early `$match` is in the rewrite",
            "C101 revenue is checked against a manual sum",
        ],
    )
)

GUIDES.append(
    guide(
        "lab",
        5,
        "index-design-and-validation",
        "Index Design and Validation",
        "25 min",
        "Intermediate",
        "Identify query shapes for the sales report and application queries, propose a small index set, create training indexes, and compare explain examined vs returned counts.",
        [
            (
                "List current indexes",
                "Run `db.orders.getIndexes()`, `db.products.getIndexes()`, and `db.reviews.getIndexes()`. Note leftovers from Module 6.",
                "A written inventory exists. `_id_` is present. Extra indexes from Day 3 morning are labeled, not blindly dropped.",
            ),
            (
                "Create or reuse two useful indexes",
                "If missing, create training indexes (names optional):\n\n"
                + js(
                    """db.orders.createIndex(
  { customerId: 1, paymentStatus: 1, createdAt: -1 },
  { name: "ix_orders_cust_pay_date" }
)
db.orders.createIndex(
  { paymentStatus: 1, createdAt: -1 },
  { name: "ix_orders_pay_date" }
)"""
                )
                + "\nExplain the C101 paid-history query and the paid `$match` of the monthly report.",
                "Winning plans show IXSCAN (unless a better leftover index wins). Examined counts are written down. Prefix overlap between the two new indexes is noted.",
            ),
            (
                "Overlap decision",
                "State whether both new indexes should survive in production, or whether one prefix makes the other a hide candidate. Do **not** drop indexes in this lab.",
                "A sentence exists: keep both only if both query shapes are hot; otherwise hide the redundant one after monitoring. No `dropIndex` in this lab.",
            ),
        ],
        [
            "Index inventory is written",
            "Two explains are recorded after index creation",
            "No index is dropped",
        ],
    )
)

GUIDES.append(
    guide(
        "lab",
        6,
        "schema-validation-implementation",
        "Schema Validation Implementation",
        "20 min",
        "Intermediate",
        "Implement order validation on a scratch collection requiring orderNumber, customerId, nonempty items, permitted statuses, nonnegative Decimal128 total, and Date createdAt, then test valid and invalid inserts.",
        [
            (
                "Create a scratch collection",
                "Copy two paid orders into a new collection so production-shaped data exists without locking `orders`:\n\n"
                + js(
                    """use training_store_ops
db.orders_validated.drop()
db.getSiblingDB("training_store").orders.find({ paymentStatus: "PAID" }).limit(2).forEach(d => {
  delete d._id
  db.orders_validated.insertOne(d)
})
db.orders_validated.countDocuments()"""
                ),
                "`training_store_ops.orders_validated` has two documents.",
            ),
            (
                "Attach the validator",
                "Run `collMod` (or `createCollection`) with `$jsonSchema` requiring `orderNumber` (string), `customerId` (objectId), `items` (array `minItems: 1`), `paymentStatus` enum `PAID`/`PENDING`/`FAILED`, `fulfillmentStatus` enum that matches your data, `total` decimal (or a number type you can justify), `createdAt` date. Use `validationAction: \"error\"`.",
                "`collMod` / create succeeds. `db.getCollectionInfos({ name: \"orders_validated\" })` shows the validator.",
            ),
            (
                "Prove accept and reject",
                "Insert one valid order (new `orderNumber`). Then attempt: missing `orderNumber`; `total: \"9.99\"`; `paymentStatus: \"PAID_NOW\"`. Record the error messages.",
                "Valid insert succeeds. Each invalid insert is rejected. Existing copied documents remain.",
            ),
        ],
        [
            "Validator is on `training_store_ops.orders_validated`",
            "One valid insert works",
            "Missing field, wrong type, and illegal status are rejected",
        ],
    )
)

GUIDES.append(
    guide(
        "lab",
        7,
        "security-configuration-review",
        "Security Configuration Review",
        "25 min",
        "Beginner",
        "Review a sanitized training configuration for network exposure, authentication, roles, TLS, credential storage, backup access, logging, and environment separation, then produce a prioritized remediation list.",
        [
            (
                "Mark every finding",
                "Read the fictional configuration in the worksheet below. List every unsafe item under network, identity, encryption, secrets, backup, logging, and environment.",
                "Findings include `bindIp: 0.0.0.0` with no auth, disabled security, shared `admin/admin`, mongodb:// without TLS, URI in source, open backup bucket, verbose logs with the URI, prod dump loaded in dev.",
            ),
            (
                "Prioritize remediation",
                "Write a P1 / P2 / P3 list with owners (role names, not classmates’ personal emails). P1 must be items that would stop a go-live.",
                "P1: enable auth, restrict bind/firewall, TLS, remove secrets from git, stop public backup. P2: least-privilege roles, log redaction, env separation. P3: audit log destinations, rotation cadence.",
            ),
            (
                "Design roles only",
                "Do **not** enable authentication on the shared class database. Write `createRole` / `createUser` sketches for `appUser` and `reportUser` using placeholder names only.",
                "appUser: readWrite on `training_store`. reportUser: read on `training_store`. Neither is root. No real passwords in the notes.",
            ),
        ],
        [
            "Unsafe configuration items are listed by category",
            "P1 items would block production",
            "No real credentials are written down",
        ],
        discussion=False,
        extra="""## Fictional configuration worksheet (sanitized)

Never copy this into a real deployment.

"""
        + yaml_block(
            """net:
  bindIp: 0.0.0.0
  port: 27017
  tls:
    mode: disabled
security:
  authorization: disabled
# connection used by the app (committed to Git)
# mongodb://admin:admin@store.example.com:27017/training_store
backup:
  destination: s3://public-training-backups
  encryption: off
logging:
  logAppend: true
  verbosity: 2
# last night: mongodump of production restored onto the intern laptop
"""
        )
        + """

## Role sketches (placeholders only)

```javascript
// Do not run on the shared class instance unless the instructor says so.
db.createUser({
  user: "appUser",
  pwd: "REDACTED",
  roles: [ { role: "readWrite", db: "training_store" } ]
})
db.createUser({
  user: "reportUser",
  pwd: "REDACTED",
  roles: [ { role: "read", db: "training_store" } ]
})
```
""",
    )
)

GUIDES.append(
    guide(
        "lab",
        8,
        "monitoring-and-log-analysis",
        "Monitoring and Log Analysis",
        "25 min",
        "Intermediate",
        "Build an incident timeline from sample metrics and logs, name the first abnormal signal, correlate application and database evidence, propose a likely cause, an alert, and a runbook update.",
        [
            (
                "Build the timeline",
                "Using the sample log and metric extract below, write a timeline with at least four rows: time, signal, source (app or mongod).",
                "Order is roughly: deploy at 14:02 → query shape change in app logs → documentsExamined rise at 14:04 → slow query log lines → customer checkout latency. No election in the replica-set log.",
            ),
            (
                "Name cause and alert",
                "State the likely root cause in one sentence. Write one alert (metric, threshold idea, severity) that would have paged sooner, and one runbook step to add.",
                "Cause: post-deploy filter no longer matches the index. Alert: slow query rate or examined/returned ratio vs baseline, high severity during checkout hours. Runbook: capture the exact query hash/shape and run explain before adding hardware.",
            ),
            (
                "Recommend a dashboard change",
                "Name two tiles that should sit next to each other so this incident is obvious next time.",
                "Application p99 latency beside mongod slow-ops / documents examined (or query planner collection-scan count). CPU-only would have missed it.",
            ),
        ],
        [
            "Timeline has four or more events",
            "Election is not blamed",
            "Alert and runbook update are specific",
        ],
        extra="""## Sample evidence (training fiction)

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
""",
    )
)

GUIDES.append(
    guide(
        "lab",
        9,
        "backup-and-restore-verification",
        "Backup and Restore Verification",
        "30 min",
        "Intermediate",
        "Record source counts and sample ids, take an approved backup, restore to an isolated database, verify documents and indexes, and compare duration to a stated RTO.",
        [
            (
                "Record the source",
                "In notes: `db.orders.countDocuments()`, `db.products.countDocuments()`, three `orderNumber` values, and `db.orders.getIndexes()`. Use `training_store`.",
                "Counts match the loader (about 17 orders, 13 products) unless the class mutated data — write the actual numbers. Three order numbers and index names are recorded.",
            ),
            (
                "Take a backup",
                "From the course repo in PowerShell (MongoDB Database Tools must be on PATH), run:\n\n"
                + text_block(
                    r"""New-Item -ItemType Directory -Force -Path .\datasets\backups | Out-Null
mongodump --uri="mongodb://localhost:27017" --db=training_store --out=".\datasets\backups\lab89"
"""
                )
                + "\nIf `mongodump` is not installed, use Compass export of `orders` and `products` JSON into `datasets/backups/lab89` and note that it is a logical export, not a full physical snapshot.",
                "A dump directory (or JSON export) exists. The command finished without authentication errors (or the instructor supplied a URI).",
            ),
            (
                "Restore isolated and verify",
                "Restore into a **new** database name:\n\n"
                + text_block(
                    r"""mongorestore --uri="mongodb://localhost:27017" --nsFrom="training_store.*" --nsTo="training_store_restore.*" --drop ".\datasets\backups\lab89\training_store"
"""
                )
                + "\nThen in `mongosh`: compare counts, `find` one recorded `orderNumber`, and `getIndexes()` on `training_store_restore.orders`. Record start/end time. Do not restore over `training_store`.",
                "Counts match the source note. Sample order exists. Indexes are present (rebuild may apply for some logical imports). Elapsed time is written and compared to a classroom RTO such as 30 minutes.",
            ),
        ],
        [
            "Source counts and sample ids are written before backup",
            "Restore target is not `training_store`",
            "Verification includes counts, a sample document, and indexes",
        ],
        extra="""## RPO / RTO for this lab

Assume classroom targets: **RPO = since last dump** (here: minutes, because you dumped just now) and **RTO = 30 minutes**. If restore exceeded 30 minutes, the procedure failed the RTO even if data looks correct.

Atlas users: take a snapshot in a disposable project or follow the instructor’s restore-to-new-cluster path. Still verify counts and sample ids.
""",
    )
)

GUIDES.append(
    guide(
        "lab",
        10,
        "troubleshooting-challenge",
        "Troubleshooting Challenge",
        "30 min",
        "Intermediate",
        "Separate five concurrent symptoms into independent problems and produce evidence, investigation order, immediate actions, long-term corrections, and verification steps.",
        [
            (
                "Separate the incidents",
                "Symptoms: product browsing is slow; some orders are missing from a report; secondary lag is increasing; authentication failures appear in logs; disk utilization is approaching its threshold. Write five problem statements that do **not** assume a single root cause.",
                "Five independent hypotheses exist (for example: missing catalog index; report `$match` type/status bug; secondary I/O or network; brute force or bad app secret; unbounded growth or large indexes). One sentence each.",
            ),
            (
                "Order the investigation",
                "Rank what you would check first for a live checkout site and why. Attach one evidence source per symptom (explain, log field, `rs.printSecondaryReplicationInfo()`, auth log, `db.stats()` / disk).",
                "Auth failures and disk may be P1 if they threaten availability; lag if oplog is at risk; slow browse if revenue is hurting; missing report rows if finance is blocked. Order is justified.",
            ),
            (
                "Actions and verification",
                "For each of the five: one immediate action, one long-term correction, one verification signal.",
                "Table with 5 rows. Immediate actions are reversible (hide index, rotate a leaked demo password, page storage). Verification is a metric or query result, not ‘looks better’.",
            ),
        ],
        [
            "Symptoms are not collapsed into one cause",
            "Investigation order is justified",
            "Each problem has immediate, long-term, and verify steps",
        ],
        extra="""## Instructor key (share after discussion)

These can all be true at once:

1. **Slow browse** — catalog query missing `{ category: 1, active: 1, price: 1 }` or filter/type mismatch.
2. **Missing report orders** — `paymentStatus` type/case, date TZ boundary, or `$unwind` drop of empty items.
3. **Secondary lag** — backup or compact on the secondary, network, or write burst from a job.
4. **Auth failures** — old URI after rotation, or scanning of a public port (ties to Lab 8.7).
5. **Disk** — journal + dumps on the same volume, or index bloat; not automatically “need sharding.”
""",
    )
)

GUIDES.append(
    guide(
        "lab",
        11,
        "final-integrated-production-challenge",
        "Final Integrated Production Challenge",
        "45–60 min",
        "Intermediate",
        "Prepare training_store for a production-readiness review: one schema fix, validation, monthly sales pipeline, indexes, least-privilege notes, RPO/RTO, monitoring, alerts, one runbook, and a completed checklist.",
        [
            (
                "Fix one schema problem",
                "Document `XBAD`’s string `price` (or another real defect you found). On `training_store_ops`, copy products and convert the bad price **or** quarantine the document. Do not silently rewrite historical orders.",
                "A before/after note exists. `training_store` catalog may stay unchanged; the ops copy shows the repaired type.",
            ),
            (
                "Validation + monthly pipeline",
                "Reuse or complete Lab 8.6 validation on `orders_validated`. Run your Lab 8.3/8.4 monthly paid-sales pipeline against `training_store.orders` and save the result documents.",
                "Validator rejects a bad insert. Pipeline output has month, order count, revenue, AOV, unique customers, units sold.",
            ),
            (
                "Indexes and explain",
                "Ensure at least one history index and one paid-report index exist (create on `training_store` only if the instructor allows Day 3 leftovers). Explain the C101 history query and the pipeline `$match`. Record IXSCAN vs COLLSCAN.",
                "Two explain summaries are in the notes. Overlap is mentioned if both indexes share a prefix.",
            ),
            (
                "Ops pack",
                "In one page: least-privilege table (app vs report vs admin); RPO/RTO for orders; three critical alerts; one runbook (backup failed or no primary); checklist scores for the six production-readiness areas.",
                "The page is complete. Classification is Ready with conditions or Not ready, with evidence. No production-ready claim without auth, tested restore, and restricted network.",
            ),
        ],
        [
            "One schema defect is repaired in a scratch space",
            "Validation and monthly pipeline evidence exist",
            "Explains are recorded",
            "Ops pack includes alerts, runbook, and checklist",
        ],
        extra="""## Production-readiness checklist (score each)

| Area | Ready / Conditional / Not ready | Evidence |
|------|----------------------------------|----------|
| Data model | | |
| Queries and indexes | | |
| Security | | |
| Availability and scalability | | |
| Backup and recovery | | |
| Monitoring and operations | | |

**Overall:** Production-ready / Ready with conditions / Not production-ready
""",
    )
)


def write_all() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for kind, num, slug, title, time, typ, objective, md in GUIDES:
        prefix = "exercise" if kind == "exercise" else "lab"
        path = OUT / f"{prefix}-8.{num}-{slug}.md"
        path.write_text(md.strip() + "\n", encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)} ({typ}, {time}) — {title}")
    print(f"Done. {len(GUIDES)} lab guides.")


if __name__ == "__main__":
    write_all()
