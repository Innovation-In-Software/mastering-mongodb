"""Emit Module 8 Marp slides and append them to the course deck.

Run after lab guides exist:

    python scripts/module08_labs.py
    python scripts/module08_diagrams.py
    python scripts/module08_slides.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from course_config import deck_md
from module08_labs import OUT as LAB_DIR

DECK = deck_md()
MARKER = "<!-- _header: 'Module 8 — MongoDB Best Practices, Security, and Troubleshooting' -->"
NEXT_MARKERS: tuple[str, ...] = ()


def notes(title: str, script: str) -> str:
    body = script.strip()
    return f"<!--\n{body}\n\nThe slide title is: {title}.\n-->"


def split_slide(title: str, bullets: list[str], img: str, alt: str, script: str, *, fit: str = "") -> str:
    cls = f"split {fit}".strip()
    items = "\n".join(f"- {b}" for b in bullets)
    return f"""<!-- _class: {cls} -->

# {title}

<div class="cols">
<div class="col-text">

{items}

</div>
<div class="col-visual">

<img src="assets/module-08/{img}" alt="{alt}" width="720">

</div>
</div>

{notes(title, script)}
"""


def content_slide(title: str, body: str, script: str, *, fit: str = "fit-md") -> str:
    return f"""<!-- _class: content {fit} -->

# {title}

{body.strip()}

{notes(title, script)}
"""


def parse_steps(kind: str, num: int) -> list[tuple[str, str, str]]:
    matches = sorted(LAB_DIR.glob(f"{kind}-8.{num}-*.md"))
    if not matches:
        return []
    text = matches[0].read_text(encoding="utf-8")
    start = text.find("## Steps from the training slides")
    if start < 0:
        return []
    section = text[start:]
    end = re.search(r"\n## (?!Steps)", section[10:])
    if end:
        section = section[: end.start() + 10]
    steps = []
    for m in re.finditer(
        r"### Step (\d+) — (.+?)\n\n\*\*Do this:\*\* (.*?)\n\n\*\*Expected result:\*\* (.*?)(?=\n---|\n### |\Z)",
        section,
        re.DOTALL,
    ):
        do = re.sub(r"```[\w-]*", "", m.group(3))
        do = re.sub(r"\s+", " ", do).strip()[:220]
        exp = re.sub(r"```[\w-]*", "", m.group(4))
        exp = re.sub(r"\s+", " ", exp).strip()[:160]
        steps.append((m.group(2).strip(), do, exp))
    return steps


def _step_slides(kind: str, num: int, rel: str, script: str) -> list[str]:
    label = "Exercise" if kind == "exercise" else "Lab"
    steps = parse_steps(kind, num)
    slides = []
    for i in range(0, len(steps), 2):
        pair = steps[i : i + 2]
        b = pair[1][0] if len(pair) > 1 else ""
        heading = f"## {label} 8.{num} — Steps {i + 1}–{i + 2 if b else i + 1}"
        lines = [
            "<!-- _class: fit-md -->",
            "",
            heading,
            "",
            f"**Lab guide:** [`{label} 8.{num}`](../slide-exercises/{rel})" if i == 0 else "",
            "",
            "**Follow along (Windows) — key steps:**",
            "",
        ]
        for n, (st, do, exp) in enumerate(pair, start=i + 1):
            lines += [
                f"**Step {n} — {st}**",
                f"- **Do:** {do}",
                f"- **Expected:** {exp}",
                "",
            ]
        lines.append(notes(heading[3:], f"Time-box this pair of steps. Open the lab guide for full commands.\n{script[:200]}"))
        slides.append("\n".join(line for line in lines if line is not None))
    return slides


def exercise_block(num: int, title: str, time: str, objective: str, img: str, alt: str, script: str) -> list[str]:
    lab = next(LAB_DIR.glob(f"exercise-8.{num}-*.md"))
    rel = lab.as_posix().split("slide-exercises/")[-1]
    intro = split_slide(
        f"Exercise 8.{num} — {title}",
        [f"**Time:** {time}", objective, f"**Lab guide:** [`Exercise 8.{num}`](../slide-exercises/{rel})"],
        img,
        alt,
        script,
        fit="fit-md",
    )
    return [intro] + _step_slides("exercise", num, rel, script)


def lab_block(num: int, title: str, time: str, objective: str, img: str, alt: str, script: str) -> list[str]:
    lab = next(LAB_DIR.glob(f"lab-8.{num}-*.md"))
    rel = lab.as_posix().split("slide-exercises/")[-1]
    intro = split_slide(
        f"Lab 8.{num} — {title}",
        [f"**Time:** {time}", objective, f"**Lab guide:** [`Lab 8.{num}`](../slide-exercises/{rel})"],
        img,
        alt,
        script,
        fit="fit-md",
    )
    return [intro] + _step_slides("lab", num, rel, script)


def demo_slide(n: str, title: str, body, script: str, img: str | None = None) -> str:
    if img:
        bullets = body if isinstance(body, list) else [body]
        return split_slide(f"Demo 8.{n} — {title}", bullets, img, title, script, fit="fit-md")
    text = body if isinstance(body, str) else "\n".join(f"- {b}" for b in body)
    return content_slide(f"Demo 8.{n} — {title}", text, script, fit="fit-sm")


def build_slides() -> str:
    s: list[str] = []

    s.append(f"""{MARKER}

<!-- _class: lead -->

# MongoDB Best Practices, Security, and Troubleshooting

A database is not production-ready merely because it accepts queries

{notes("MongoDB Best Practices, Security, and Troubleshooting", '''This is the last module of the three-day course. Modules 1–7 made training_store work. Module 8 asks whether you would sleep well if checkout ran on it tonight.

Time-box to about 90–120 minutes when Modules 6 and 7 already filled the morning: framework, security, backup/restore test, troubleshooting method, checklist, and Lab 8.11. Full delivery is 3–3.5 hours with the discussion exercises.

Never paste real credentials into slides or chat.
''')}
""")

    s.append(
        content_slide(
            "Module Learning Objectives",
            """Participants will learn to:

- Review MongoDB solutions systematically
- Recognize design and operational risks
- Protect databases and credentials
- Monitor health and performance
- Troubleshoot common problems
- Verify recovery capabilities
- Make controlled production changes
- Establish an improvement plan""",
            "Read the outcomes. The through-line is evidence: a checklist with owners beats a slide of slogans. Park driver-language questions unless they affect connection strings or secrets.",
        )
    )

    s.append(
        split_slide(
            "From Functional to Production-Ready",
            [
                "**Functional:** connects, stores, queries, returns rows",
                "**Production-ready also:**",
                "Secure · available · scalable",
                "Observable · recoverable · tested",
                "Documented · maintainable · cost-aware",
                "**Key:** correctness is only one requirement",
            ],
            "02-functional-vs-prod.svg",
            "Functional versus production-ready",
            "Ask who has shipped a demo that became production. That is this slide. Functional is the floor.",
        )
    )

    s.append(
        split_slide(
            "MongoDB Production-Readiness Framework",
            [
                "1. Data model",
                "2. Queries and indexes",
                "3. Security",
                "4. Availability and scalability",
                "5. Backup and recovery",
                "6. Monitoring and operations",
                "Each area needs standards, an owner, evidence, procedures, and periodic review",
            ],
            "03-framework.svg",
            "Six production-readiness review areas",
            "We will walk the six areas against training_store. Ownership without evidence is theater.",
        )
    )

    # --- Data modeling ---
    s.append(
        split_slide(
            "Data Modeling Best Practices",
            [
                "Begin with access patterns",
                "Keep related bounded data together",
                "Separate independent or unbounded data",
                "Use intentional duplication",
                "Preserve historical snapshots",
                "Consistent names and types",
                "Validate critical expectations",
                "Review document size and array growth",
            ],
            "01-module-map.svg",
            "Modeling sits inside production readiness",
            "This is Module 3 distilled into operating rules. If they only remember access patterns, bounds, and snapshots, that is a pass.",
        )
    )

    s.append(
        split_slide(
            "Design Around Access Patterns",
            [
                "Most frequent reads and writes",
                "Latency-sensitive operations",
                "Filter, sort, and returned fields",
                "Data retrieved together",
                "Expected growth and retention",
                "Avoid application-side joins on the hot path",
            ],
            "04-access-patterns.svg",
            "Access-pattern checklist per collection",
            "Walk products browse versus order history. Same store, different shapes, different indexes tomorrow.",
        )
    )

    s.append(
        split_slide(
            "Choose Document Boundaries Carefully",
            [
                "One business aggregate",
                "One ownership boundary",
                "One lifecycle",
                "One common read unit",
                "One atomic update boundary",
                "Orders embed items and snapshots; customers stay separate",
            ],
            "05-document-boundary.svg",
            "Order aggregate versus customer master",
            "Atomic update is the practical test: would you update this in one document on a paid checkout?",
        )
    )

    s.append(
        split_slide(
            "Embedding and Referencing Guidelines",
            [
                "**Embed when** owned, retrieved together, small and bounded, changes with the parent, atomicity matters",
                "**Reference when** unbounded, independent lifecycle, queried alone, widely shared, or would bloat the parent",
            ],
            "06-embed-vs-ref.svg",
            "Embed versus reference decision table",
            "Reviews were the Module 3 example of unbounded growth. Do not re-litigate every relationship — use the table.",
        )
    )

    s.append(
        split_slide(
            "Bound Arrays and Document Growth",
            [
                "Avoid arrays that grow forever",
                "Risky: all transactions, reviews, events, audits, logins",
                "Safer: separate collections, bucketing, subsets, archive, time partitions, retention",
            ],
            "07-unbounded.svg",
            "Move unbounded reviews off the product",
            "16 MiB is a hard stop; operational pain starts much earlier. training_store already uses a reviews collection — praise that.",
        )
    )

    s.append(
        content_slide(
            "Use Consistent Field Names and Types",
            """Avoid mixing:

```javascript
{ price: Decimal128("49.99") }
{ productPrice: "49.99" }
{ item_cost: 49.99 }
```

Standardize naming, capitalization, dates, money, identifiers, statuses, nulls, and nesting.

Consistency improves queries, validation, indexes, and application code.""",
            "XBAD in the dataset is the living example of a string price. Point at it in Compass if the room is drifting.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Apply Schema Validation",
            """Use `$jsonSchema` (and related rules) to enforce:

- Required identifiers
- Correct BSON types
- Allowed status values
- Nonnegative amounts
- Nested and array-element shape
- Valid dates

Protect invariants without blocking legitimate evolution — `warn` during migration, then `error`.""",
            "Validation is not a substitute for application checks. It is the last line on writes you do not fully control.",
            fit="fit-sm",
        )
    )

    s.append(
        split_slide(
            "Plan for Schema Evolution",
            [
                "Add compatible optional fields first",
                "Update readers before writers when you can",
                "Version documents if the shape forks",
                "Migrate history progressively",
                "Monitor mixed-schema documents",
                "Remove obsolete fields only after a dependency review",
                "Test validator changes before enforcement",
            ],
            "08-schema-evolution.svg",
            "Compatible evolution then tighter validation",
            "Expand-contract. Never flip a required field and a new name in the same deploy if old writers are still live.",
        )
    )

    s.append(
        split_slide(
            "Preserve Historical Snapshots",
            [
                "Purchase-time product name and price",
                "Billing and shipping addresses",
                "Tax, discount, currency, contract terms",
                "Status-change timestamps",
                "Current master data must not silently rewrite history",
            ],
            "09-snapshots.svg",
            "Orders snapshot facts; catalog stays live",
            "Finance and support tickets die when last week’s order shows this week’s sale price.",
        )
    )

    s.append(
        split_slide(
            "Avoid Common Schema Anti-Patterns",
            [
                "Copying relational tables into collections",
                "Unbounded arrays and oversized documents",
                "Inconsistent types and excessive nesting",
                "Uncontrolled duplication",
                "Unrelated entities in one collection — or too many tiny collections",
                "Modeling without access patterns",
                "Money as approximate floats or unplanned strings",
            ],
            "10-anti-patterns.svg",
            "Schema anti-pattern pairs",
            "Rapid-fire: which of these is still in their day job? Capture two for the action plan at the end.",
        )
    )

    s.append(
        demo_slide(
            "1",
            "Review and Improve a Data Model",
            [
                "**Time:** 15 min",
                "Start from mixed prices, unbounded reviews, string dates, and a password hash on the document",
                "Correct types, split reviews, standardize names, add validation, protect secrets",
                "Keep the catalog and order access patterns fast",
            ],
            "Live-edit a bad product on the projector. Do not use a real hash. End with reviews in their own collection — matching training_store.",
            img="41-demo-model.svg",
        )
    )

    s.extend(
        exercise_block(
            1,
            "Review a Document Model",
            "15 min",
            "Score an order-shaped document and rewrite the boundary, snapshots, and first validator.",
            "05-document-boundary.svg",
            "Order versus customer boundary",
            "Pairs. Collect passwordHash and string price on the board first.",
        )
    )

    s.extend(
        exercise_block(
            2,
            "Find the Schema Anti-Patterns",
            "15 min",
            "Name seven anti-patterns on a messy product document and sketch the repair.",
            "10-anti-patterns.svg",
            "Schema anti-patterns",
            "If time is short, skip the rewrite and keep the named list.",
        )
    )

    # --- Queries ---
    s.append(
        content_slide(
            "Query Design Best Practices",
            """- Use selective filters and correct BSON types
- Prefer indexed fields for recurring shapes
- Return only required documents and fields
- Sort deterministically; limit and paginate
- Avoid uncontrolled regular expressions
- Inspect important query plans""",
            "This is Module 4 and 6 as operating policy. The next slides are the ones people violate after lunch.",
            fit="fit-sm",
        )
    )

    s.append(
        split_slide(
            "Retrieve Only Required Documents",
            [
                "Avoid `db.orders.find({})` when you need one customer’s paid orders",
                "Prefer `customerId` + `paymentStatus: \"PAID\"`",
                "Precise filters cut server work, network, client memory, and app CPU",
            ],
            "11-selective-filter.svg",
            "Selective filter versus collection scan",
            "Type the two queries. Ask what the driver does with 17 documents versus 17 million.",
        )
    )

    s.append(
        split_slide(
            "Return Only Required Fields",
            [
                "Project `orderNumber`, `fulfillmentStatus`, `total`, `createdAt`",
                "Drop `_id` when the client does not need it",
                "Projection matters most when documents hold large arrays or embeds",
            ],
            "12-projection.svg",
            "Projection shrinks the payload",
            "Covered queries from Module 6 are the advanced form of this habit.",
        )
    )

    s.append(
        split_slide(
            "Use Appropriate BSON Types",
            [
                "Timestamps → Date",
                "Exact money → Decimal128",
                "Flags → Boolean",
                "Quantities → integer types",
                "Ids → ObjectId or a consistent business id",
                "Wrong types break filters, sorts, math, and indexes",
            ],
            "13-bson-types.svg",
            "BSON types for common fields",
            "status: \"paid\" versus paymentStatus: \"PAID\" is the afternoon incident in Lab 8.8.",
        )
    )

    s.append(
        split_slide(
            "Avoid Expensive Query Patterns",
            [
                "Leading-wildcard or unanchored regex",
                "Large skip-based pagination",
                "Broad negative filters",
                "Missing shard-key predicates",
                "Huge result sets and app-side joins",
                "Sorts without a supporting index",
                "Examining far more documents than you return",
            ],
            "14-expensive.svg",
            "Expensive query pattern grid",
            "Skip is the pagination trap. Keyset pagination is the adult version — mention, do not workshop.",
        )
    )

    s.append(
        demo_slide(
            "2",
            "Diagnose a Slow Query",
            [
                "**Time:** 20 min",
                "Capture the query → `explain(\"executionStats\")`",
                "Spot COLLSCAN or weak scanning",
                "Fix filter, sort, projection; add an index; compare examined vs returned",
                "Discuss write and storage cost",
            ],
            "Reuse a Module 6 catalog or history query. The teaching is the loop, not a new operator.",
            img="22-explain.svg",
        )
    )

    s.extend(
        exercise_block(
            3,
            "Review a Query and Projection",
            "15 min",
            "Rewrite find({}) into a selective, projected, sorted, limited query and name an ESR index.",
            "11-selective-filter.svg",
            "Selective query rewrite",
            "Two minutes of silence, then one volunteer query on the board.",
        )
    )

    # --- Aggregation ---
    s.append(
        content_slide(
            "Aggregation Pipeline Best Practices",
            """- Start from the correct collection
- Filter early when the logic allows
- Build one stage at a time and inspect output
- Control array expansion
- Avoid unnecessary `$lookup`
- Handle null and missing values
- Validate calculations on a tiny sample
- Shape the final output; review the plan""",
            "Module 5 habits become production policy. The monthly sales lab will punish double-counting.",
            fit="fit-sm",
        )
    )

    s.append(
        split_slide(
            "Reduce Pipeline Input Early",
            [
                "Large collection → selective `$match` → smaller working set → expensive stages",
                "`$match` after `$group` filters grouped results — different job",
                "Early filters reduce work in `$unwind`, `$lookup`, and `$group`",
            ],
            "15-early-match.svg",
            "Filter before expensive stages",
            "If they remember one aggregation rule, this is it.",
        )
    )

    s.append(
        split_slide(
            "Control `$unwind` Expansion",
            [
                "100,000 orders × 10 items → 1,000,000 documents",
                "Before unwind: filter, drop unused fields, confirm the array is required",
                "Estimate the expansion factor",
                "Do not sum parent totals after unwind",
            ],
            "16-unwind.svg",
            "Unwind multiplies document count",
            "Draw the 10× blob. Lab 8.3 uses two $group stages for this reason.",
        )
    )

    s.append(
        split_slide(
            "Use `$lookup` Deliberately",
            [
                "Is the data already embedded on purpose?",
                "Is the join required for this request?",
                "Is the foreign field indexed?",
                "How many matches? Will it create a large array?",
                "Can the foreign pipeline filter and project?",
                "Hot path versus occasional report?",
            ],
            "17-lookup.svg",
            "Questions before adding lookup",
            "customers._id is already indexed. Looking up before $match is still expensive because you join rows you will throw away.",
        )
    )

    s.append(
        split_slide(
            "Validate Aggregation Calculations",
            [
                "Pick a tiny known sample",
                "Hand-calculate expected totals",
                "Run the pipeline on that sample",
                "Compare counts and money",
                "Check nulls, duplicates, unwind, date boundaries and time zones",
            ],
            "18-validate-agg.svg",
            "Manual sample then pipeline",
            "C101 paid totals from find() are the classroom oracle. Do not trust a pretty $group on first run.",
        )
    )

    s.append(
        demo_slide(
            "3",
            "Tune an Aggregation Pipeline",
            [
                "**Time:** 20 min",
                "Start with `$lookup` → `$unwind` → `$match` → `$group` → `$sort`",
                "Aim for `$match` → `$project` → (maybe lookup) → controlled unwind → `$group` → `$sort`",
                "Business logic decides the exact order",
                "Measure before and after",
            ],
            "Show inflated revenue after summing total post-unwind. Then the two-group fix. That gasp is the demo.",
            img="15-early-match.svg",
        )
    )

    s.extend(
        exercise_block(
            4,
            "Optimize an Aggregation Pipeline",
            "20 min",
            "Name defects in a lookup-first pipeline and propose a safer stage order that does not double-count.",
            "16-unwind.svg",
            "Unwind expansion",
            "If they omit double-counting, stop and make them say it.",
        )
    )

    # --- Indexing ---
    s.append(
        content_slide(
            "Indexing Best Practices",
            """- Index recurring query shapes
- Use compound indexes deliberately
- Start from Equality–Sort–Range
- Review prefixes; measure with `explain()`
- Hide before you drop; monitor usage
- Account for write and storage cost
- Revisit indexes as the workload changes""",
            "Do not rebuild Module 6. This is the production policy layer on top of ESR.",
            fit="fit-sm",
        )
    )

    s.append(
        split_slide(
            "Design Indexes Around Query Shapes",
            [
                "Filter `customerId` + `paymentStatus: \"PAID\"`, sort `createdAt: -1`",
                "Candidate `{ customerId: 1, paymentStatus: 1, createdAt: -1 }`",
                "Do not index one filter field and ignore sort",
            ],
            "19-index-shape.svg",
            "Compound index matching a query shape",
            "Write the query then the index. Never the reverse.",
        )
    )

    s.append(
        split_slide(
            "Balance Read and Write Performance",
            [
                "Extra indexes can speed selected reads",
                "They add insert, update, delete work",
                "Plus storage, RAM, replication traffic, backup size",
                "The portfolio must match the whole workload",
            ],
            "20-index-cost.svg",
            "Index benefit versus write cost",
            "Fourteen secondary indexes on a write-heavy checkout is a pager, not a trophy.",
        )
    )

    s.append(
        split_slide(
            "Identify Redundant Indexes",
            [
                "Identical keys, overlapping prefixes, unused indexes, dead features",
                "A compound index may already cover a shorter prefix",
                "Before removal: review workload, explain, hide, monitor, drop with rollback",
            ],
            "21-redundant.svg",
            "Prefix overlap and hide-then-drop",
            "Hide does not reduce write cost. Drop does. Say that every time.",
        )
    )

    s.append(
        split_slide(
            "Review Explain Plans",
            [
                "`COLLSCAN` vs `IXSCAN`, index name, `FETCH`, SORT",
                "Keys examined, docs examined, docs returned",
                "Shard targeting and pipeline stage behavior",
                "An index scan only helps if it supports this query",
            ],
            "22-explain.svg",
            "Essential explain plan stages",
            "IXSCAN on the wrong predicate is still a failure. Examined vs returned is the honesty metric.",
        )
    )

    s.extend(
        exercise_block(
            5,
            "Rationalize an Index Portfolio",
            "20 min",
            "Map overlapping category indexes, low-selectivity `active`, and a hide-then-monitor plan.",
            "21-redundant.svg",
            "Overlapping category indexes",
            "Do not let them drop { category: 1, active: 1, price: 1 } on sight.",
        )
    )

    # --- Security ---
    s.append(
        split_slide(
            "MongoDB Security Principles",
            [
                "Identity, authentication, authorization",
                "Network isolation, encryption, secret protection",
                "Auditing, patching, backups, monitoring",
                "No single control is enough",
            ],
            "23-security-layers.svg",
            "Layered MongoDB security controls",
            "Defense in depth. Auth without network restriction still loses to a leaked URI.",
        )
    )

    s.append(
        content_slide(
            "Authentication",
            """Authentication verifies identity.

Sources may include database users, certificates, enterprise identity, cloud identity, and workload identities.

Avoid shared admin accounts, default or weak passwords, anonymous access, and long-lived secrets without rotation.""",
            "Who are you? Not what may you do. Separate those words; people mix them.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Authorization and Role-Based Access",
            """Authorization decides permitted operations:

- Read or read/write application data
- Manage indexes
- Inspect monitoring
- Administer users and backups
- Administer the cluster

Roles should match responsibilities — not job titles copied from email.""",
            "Show built-in read / readWrite / userAdmin / clusterMonitor as examples, not a catalog to memorize.",
            fit="fit-sm",
        )
    )

    s.append(
        split_slide(
            "Principle of Least Privilege",
            [
                "Grant only what the workload needs",
                "App: readWrite on its database",
                "Reporting: read on approved collections",
                "Backup and monitoring: their own roles",
                "Never put clusterAdmin in application code",
            ],
            "24-least-privilege.svg",
            "Least-privilege identity ceiling",
            "Stolen app credentials should not drop the replica set. That sentence is the slide.",
        )
    )

    s.append(
        split_slide(
            "Network Security",
            [
                "Private networks, firewalls, allowlists",
                "Segmentation and controlled admin paths",
                "No unnecessary public exposure",
                "Separate application and management access",
                "Review rules continuously",
            ],
            "25-network.svg",
            "Private network then allowlist",
            "27017 on 0.0.0.0 plus no auth is the Lab 8.7 horror config.",
        )
    )

    s.append(
        split_slide(
            "Encryption in Transit and at Rest",
            [
                "**Transit (TLS):** app, admins, replica members, shard components, backup paths",
                "Validate certificates — encryption without identity checks is weak",
                "**At rest:** disks, snapshots, backups, temp files, exports, logs",
                "Pair with key management and access policy",
            ],
            "26-encryption.svg",
            "TLS in transit and encryption at rest",
            "Atlas makes some of this default; self-managed classes must not assume magic.",
        )
    )

    s.append(
        split_slide(
            "Application Credential Management",
            [
                "Do not store secrets in source, images, screenshots, shared docs, or open config files",
                "Use a secret manager, protected injection, workload identity",
                "Rotate, separate environments, audit access",
            ],
            "27-secrets.svg",
            "Secrets stay out of source control",
            "Search their sample-app README later — placeholders only. No live URIs on this slide.",
        )
    )

    s.append(
        content_slide(
            "Data Classification and Sensitive Fields",
            """Classify PII, payment data, tokens, health, financial, and confidential business fields.

Then define who may access them, where they live, how long they stay, masking, field-level protection, and audit.

Do not put password hashes on orders. Do not copy production dumps to intern laptops.""",
            "Classification is a business activity. The database cannot invent it. Give two examples from training_store: email vs order total vs a hypothetical card number they must never store in class.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Auditing and Security Logging",
            """Log authentication success/failure, user and role changes, admin and config operations, collection changes, sensitive access, backup and restore.

Protect logs from tampering and from leaking the secrets they might contain.""",
            "Verbose logs plus a URI in the message is a finding in Lab 8.7. Audit is only useful if someone reads it.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Secure Configuration Practices",
            """- Enable authentication; restrict bindings; encrypt connections
- Least-privilege roles; disable unnecessary exposure
- Rotate secrets; separate dev, test, and production
- Patch; protect backups; review config changes
- Keep an asset and owner inventory""",
            "This is the go-live punch list. We will reuse it on the deployment checklist.",
            fit="fit-sm",
        )
    )

    s.append(
        split_slide(
            "Security Anti-Patterns",
            [
                "Public database port; authentication off",
                "Shared administrator credentials",
                "Secrets in source control; no TLS",
                "App running as cluster admin",
                "Dev accounts in production",
                "Unprotected backups; secrets in logs",
                "No monitoring or access review",
            ],
            "28-sec-anti.svg",
            "Security anti-pattern grid",
            "Demo 8.6 is this slide as a murder board. Let them shout findings.",
        )
    )

    s.append(
        demo_slide(
            "4",
            "Apply Collection Validation",
            [
                "**Time:** 15 min",
                "Require orderNumber, customerId, items, statuses, decimal total, createdAt",
                "Test valid insert, missing field, wrong type, illegal status",
                "Prefer `training_store_ops` so `orders` stays loadable",
            ],
            "collMod on a scratch collection. Show the error document. Do not lock the shared orders collection on error action if people still need Labs 8.3–8.5.",
        )
    )

    s.append(
        demo_slide(
            "5",
            "Demonstrate Role-Based Access",
            [
                "**Time:** 15 min",
                "Instructor-controlled environment only",
                "App user: readWrite data; reporter: read; monitor: metrics; admin: separate identity",
                "Never display real credentials",
            ],
            "If auth is not enabled in class, walk the createUser sketches and skip live denial. Do not enable auth on a shared mongod mid-afternoon.",
            img="24-least-privilege.svg",
        )
    )

    s.append(
        demo_slide(
            "6",
            "Identify an Unsafe Configuration",
            [
                "**Time:** 10 min",
                "Public bind, auth disabled, shared admin, no TLS, no backup, no monitoring",
                "Participants name risks and controls",
            ],
            "Project the Lab 8.7 YAML. Two minutes silent write, then a round-robin of findings. Rank P1 together.",
            img="28-sec-anti.svg",
        )
    )

    s.extend(
        exercise_block(
            6,
            "Design Least-Privilege Roles",
            "20 min",
            "Permit/deny matrix for app, reporting, support, monitoring, backup, and DBA identities.",
            "24-least-privilege.svg",
            "Least-privilege roles",
            "The fail is putting clusterAdmin on the app. Celebrate anyone who says reporting is read-only.",
        )
    )

    s.extend(
        exercise_block(
            7,
            "Identify Security Risks",
            "15 min",
            "Rank six fictional risks and attach one mitigation to each.",
            "28-sec-anti.svg",
            "Security anti-patterns",
            "Public endpoint and secrets in git should land in the top three.",
        )
    )

    # --- Backup ---
    s.append(
        content_slide(
            "Backup and Recovery Fundamentals",
            """A strategy must define what, how often, where, protection, retention, restore steps, owner, and test cadence.

A backup is valuable only if it can be restored.""",
            "Underline the last sentence. Green backup jobs with never-tested restore are a false comfort.",
            fit="fit-sm",
        )
    )

    s.append(
        split_slide(
            "Replication vs. Backup",
            [
                "Replication helps with server and some infrastructure failure and planned maintenance",
                "It does **not** independently protect against drops, malice, bad migrations, or slow corruption",
                "Mistakes replicate to every member",
            ],
            "29-repl-vs-backup.svg",
            "Replica sets versus backups",
            "Module 7 people will argue. Let them, then: dropDatabase on the primary is now on the secondaries too.",
        )
    )

    s.append(
        content_slide(
            "Backup Strategy",
            """Combine as the platform allows:

- Scheduled snapshots and/or continuous backup
- Point-in-time recovery
- Logical exports for subsets or migration
- Offsite or separate-account storage
- Retention, encryption, restore testing, named owners""",
            "Atlas continuous backup versus mongodump is a platform choice. The strategy questions stay the same.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Logical vs. Physical Backup",
            """| Logical | Physical |
|---------|----------|
| Exports database content | Copies files or snapshots |
| Portable subsets | Efficient full recovery |
| Slower at large scale | Needs compatible restore |
| Migration and selected data | Large deployments |

Choose from scale, RPO/RTO, and platform — not from habit.""",
            "Lab 8.9 uses mongodump (logical). Say that a production cluster may snapshot disks instead.",
            fit="fit-sm",
        )
    )

    s.append(
        split_slide(
            "Recovery Point and Recovery Time Objectives",
            [
                "**RPO:** maximum acceptable data loss measured in time (example: 15 minutes)",
                "**RTO:** maximum acceptable time to restore service (example: 2 hours)",
                "Backup frequency and restore design must beat those numbers",
            ],
            "30-rpo-rto.svg",
            "RPO versus RTO",
            "Have them say both expansions out loud. Orders tighter than reviews.",
        )
    )

    s.append(
        split_slide(
            "Restore Testing",
            [
                "Readable backup, credentials and keys, procedure, duration",
                "Data consistency, app connectivity, indexes, users/roles",
                "Documentation that someone else can follow",
                "Successful backup jobs do not prove recovery",
            ],
            "31-restore-test.svg",
            "Restore test goes beyond a green job",
            "If they only remember one backup slide, this is it.",
        )
    )

    s.append(
        content_slide(
            "Point-in-Time Recovery and Disaster Recovery",
            """**PITR** restores to a moment before a bad drop, deploy, bulk update, or app corruption — if the platform kept history.

A DR plan names scenarios, architecture, backup location, region strategy, RPO/RTO, people, comms, app reconnect, validation, test schedule, and return-to-normal.""",
            "Do not design a multi-region Atlas topology on this slide. Name the document they must own when they go home.",
            fit="fit-sm",
        )
    )

    s.append(
        demo_slide(
            "9",
            "Test a Backup and Restore Workflow",
            [
                "**Time:** 20 min",
                "Known test data → backup → change data → restore to an isolated target",
                "Validate counts, samples, indexes, access, duration",
                "Disposable environment only",
            ],
            "Restore to training_store_restore never training_store. Time the clock. Compare to a 30-minute classroom RTO.",
            img="31-restore-test.svg",
        )
    )

    s.extend(
        exercise_block(
            8,
            "Define RPO and RTO",
            "15 min",
            "Set RPO, RTO, frequency, method, and validation for catalog, customers, orders, payments, and reviews.",
            "30-rpo-rto.svg",
            "RPO and RTO",
            "Push back if payments and reviews get the same RPO.",
        )
    )

    # --- Monitoring ---
    s.append(
        split_slide(
            "Monitoring Fundamentals",
            [
                "Is it up? Is it fast enough?",
                "Is workload or capacity changing?",
                "Is replication healthy? Is data balanced?",
                "Are backups succeeding?",
                "Are security events happening?",
                "Are users seeing errors?",
            ],
            "32-monitor.svg",
            "Questions a dashboard must answer",
            "If a tile cannot answer one of these, it does not belong on the primary dashboard.",
        )
    )

    s.append(
        content_slide(
            "Database, Query, and Resource Metrics",
            """**Health:** availability, op rates, latency, queues, connections, cache/working set, errors, data and index size.

**Queries:** slow ops, latency percentiles, examined vs returned, COLLSCAN, in-memory sorts, timeouts, heavy aggregations.

**Resources:** CPU, memory, disk capacity/latency/throughput, network, filesystem, container limits.

Symptoms often start in infrastructure, not in BSON.""",
            "Do not read every bullet. Pick examined-vs-returned and disk latency as the two they will actually use this week.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Replication, Sharding, and Connection Metrics",
            """**Replication:** primary, member health, lag, oplog window, elections, rollbacks, errors, secondary resource use.

**Sharding:** distribution, hot shards, mongos/CSRS health, balancer, migrations, targeted vs scatter-gather, zone compliance.

**Connections:** current, spawn rate, pool use, rejected, auth failures, leaks, sudden load.

Application pools must be sized on purpose.""",
            "Park deep shard metrics unless they have a cluster. Connection leaks are the app team's MongoDB problem.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Logging Best Practices",
            """Logs should be centralized, time-synced, searchable, access-controlled, retained, tamper-resistant, correlated with app and infra, and free of unnecessary secrets.

Useful fields: timestamp, component, host, severity, operation, error code, correlation id.""",
            "Lab 8.8 only works because timestamps line up. Say NTP without making it a lecture.",
            fit="fit-sm",
        )
    )

    s.append(
        split_slide(
            "Alerting Principles",
            [
                "Actionable, prioritized, owned",
                "Meaningful thresholds; resistant to noise",
                "Linked to a runbook; tested periodically",
                "Avoid alerts that only name a metric",
            ],
            "33-alerts.svg",
            "Quality of a good alert",
            "CPU > 0 is not an alert. No primary is. Practice deleting alerts in the exercise.",
        )
    )

    s.append(
        split_slide(
            "Establishing a Performance Baseline",
            [
                "Record normal latency, volume, CPU/memory, disk, connections",
                "Replication lag, storage and index growth, backup duration, errors",
                "Without a baseline you cannot tell weather from climate",
            ],
            "44-baseline.svg",
            "Baseline the normal Tuesday",
            "Module 6 Lab 6.1 was a query-plan baseline. This is the operational cousin.",
        )
    )

    s.append(
        demo_slide(
            "7",
            "Inspect Health and Performance Metrics",
            [
                "**Time:** 15 min",
                "Ops rate, query latency, connections, CPU, memory, disk, lag, storage, slow queries",
                "Correlate with a simulated load bump",
            ],
            "If Atlas/Compass metrics are available, use them. Otherwise walk the Lab 8.8 table and pretend the load bump is the 14:04 deploy.",
            img="32-monitor.svg",
        )
    )

    s.append(
        demo_slide(
            "8",
            "Read and Correlate MongoDB Logs",
            [
                "**Time:** 15 min",
                "Trace connection failure, auth failure, slow query, election, replication and storage warnings",
                "Align timestamps with the application",
            ],
            "Use the Lab 8.8 excerpts. Highlight nreturned: 0 with docsExamined: 17 and no election.",
        )
    )

    s.extend(
        exercise_block(
            9,
            "Design a Monitoring Dashboard",
            "20 min",
            "Choose at most twelve on-call tiles, each with a purpose question, and drop two vanity metrics.",
            "32-monitor.svg",
            "Dashboard questions",
            "Cap at twelve. Force them to delete.",
        )
    )

    s.extend(
        exercise_block(
            10,
            "Set Alert Priorities",
            "15 min",
            "Classify eight alerts and attach first actions for critical and high.",
            "33-alerts.svg",
            "Alert priorities",
            "No primary is the only automatic critical. Argue about lag vs one secondary.",
        )
    )

    # --- Troubleshooting ---
    s.append(
        split_slide(
            "Troubleshooting Methodology",
            [
                "Define the symptom, users, start time, recent changes",
                "Collect metrics and logs; reproduce safely",
                "Isolate the layer; one hypothesis; one change",
                "Verify recovery; document cause and prevention",
            ],
            "34-troubleshoot.svg",
            "Structured troubleshooting loop",
            "Ban shotgun indexing. One change at a time is the adult move.",
        )
    )

    s.append(
        split_slide(
            "Connection Troubleshooting",
            [
                "URI, hostname/DNS, port, route, firewall",
                "TLS, server up, driver timeouts, pool health",
                "Replica-set or mongos discovery",
            ],
            "43-connection.svg",
            "Connection diagnostic order",
            "This replaces the old ‘connect a sample app’ Module 8. Same skills, production framing.",
        )
    )

    s.append(
        content_slide(
            "Authentication and Authorization Troubleshooting",
            """**Authentication failure:** username, password, auth source, certificate, expiry, URI encoding.

**Authorization failure:** roles, target database, operation, collection privileges, inheritance, recent grants/revokes.

A ping can succeed while inserts fail — that is authorization, not ‘Mongo is down’.""",
            "authSource=admin versus the app database is the classic URI bug. Mention percent-encoding of special characters in passwords without putting a real password on the slide.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Query, Aggregation, and Index Troubleshooting",
            """**Query:** db/collection, case, nested paths, BSON types, filter logic, arrays, projection, sort, indexes, explain, result size.

**Aggregation:** shape, stage order, field paths, per-stage output, group keys, nulls, types, unwind multiplication, lookup types, double count, time zones.

**Index not used:** leading fields, predicates, sort direction, types, partial filter, collation, selectivity, multikey, projection, competing indexes, actual stats.""",
            "This is a map, not a script. Lab 8.10 forces them to pick a starting door per symptom.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Replication, Sharding, and Capacity Troubleshooting",
            """**Replication:** primary, majority, member health, network, lag, oplog window, disk/CPU, elections, write concern, recent config.

**Sharding:** mongos, CSRS, shard health, shard-key predicates, targeting, hot shards, balancer, zones, migrations, cross-shard ops.

**Capacity:** latency, queues, disk, memory, CPU, connections, storage. Cause may be growth, bad queries, missing or extra indexes, huge documents, infra limits, or maintenance.""",
            "Do not open a sharded cluster on laptops. Name hot shards and scatter-gather so Module 7 connects.",
            fit="fit-sm",
        )
    )

    s.append(
        split_slide(
            "Slow Application Investigation",
            [
                "Slow request → application trace → database operation",
                "Then query shape → explain → db and infra metrics → cause",
                "Do not tune MongoDB until you have the actual slow operation",
            ],
            "35-slow-app.svg",
            "Trace from user request to explain",
            "Blame the database last. Exercise 8.11 is this picture with a filter change.",
        )
    )

    s.extend(
        exercise_block(
            11,
            "Diagnose an Operational Incident",
            "20 min",
            "Post-release slowness: examined docs up, no election, filter changed, indexes unchanged.",
            "35-slow-app.svg",
            "Slow application investigation",
            "If anyone says ‘add a node’, ask what the explain would show first.",
        )
    )

    s.extend(
        exercise_block(
            12,
            "Create an Operational Runbook",
            "20 min",
            "Fill a twelve-section runbook for one named alert.",
            "37-incident.svg",
            "Incident workflow",
            "Pick no-primary or backup-failed if they cannot choose. Ban empty ‘check logs’.",
        )
    )

    # --- Operations ---
    s.append(
        split_slide(
            "Safe Production Changes",
            [
                "Purpose, risk, representative test, baseline",
                "Backup when appropriate; define rollback",
                "Apply gradually; monitor; validate the business path",
                "Record the outcome",
            ],
            "36-safe-change.svg",
            "Safe production change loop",
            "Indexes, validators, and version upgrades all use this loop. Hide-index is a rollback story they already know.",
        )
    )

    s.append(
        content_slide(
            "Operational Runbooks",
            """A useful runbook includes alert name, meaning, business impact, required access, diagnostic commands, expected normal state, decision points, corrective actions, escalation, rollback, verification, and incident documentation.""",
            "Exercise 8.12 is the worksheet. Quality bar: another engineer can execute it at 2 a.m.",
            fit="fit-sm",
        )
    )

    s.append(
        split_slide(
            "Incident Response Workflow",
            [
                "Detect → assess impact → stabilize",
                "Diagnose → recover → validate",
                "Communicate → review and prevent",
                "Restoring service and finding root cause can run on different clocks",
            ],
            "37-incident.svg",
            "Detect, stabilize, recover, review",
            "Stabilize may be revert the release while diagnosis continues. That is not failure.",
        )
    )

    s.append(
        split_slide(
            "MongoDB Deployment Checklist",
            [
                "**Model:** access patterns, bounded arrays, types, validation",
                "**Performance:** important queries indexed, explain reviewed, baseline recorded",
                "**Security:** auth, least privilege, network, encryption, secrets",
                "**Reliability:** replica set, failover tested, restore tested",
                "**Operations:** monitoring, owned alerts, runbooks, named owners",
            ],
            "38-checklist.svg",
            "Five-section go-live checklist",
            "This is the scoring sheet for Exercise 8.13 and Lab 8.11. Print it mentally.",
        )
    )

    s.append(
        content_slide(
            "E-Commerce Production Readiness Review",
            """**Products:** unique SKU, governed attributes, category index, review summary.

**Customers:** unique customer number, protected PII, bounded addresses, email lookup.

**Orders:** snapshots, unique order number, history index, payment/fulfillment statuses, durability controls.

**Reviews:** separate growing collection, product/date index, moderation and retention.""",
            "This is training_store held to a production bar. Unique SKU and separate reviews are already in the design — call wins as well as gaps.",
            fit="fit-sm",
        )
    )

    s.append(
        split_slide(
            "Course-Wide Architecture Review",
            [
                "Application → secure connection → driver",
                "Replica set or mongos",
                "products | customers | orders | reviews",
                "Indexes and validation",
                "Replication, backup, monitoring, alerts",
                "Eight modules, one store",
            ],
            "39-architecture.svg",
            "Course-wide training_store architecture",
            "Pause. This is the course on one diagram. People take photos. Let them.",
        )
    )

    s.append(
        demo_slide(
            "10",
            "Conduct a Production-Readiness Review",
            [
                "**Time:** 20 min",
                "Score schema, queries, indexes, security, availability, backup, monitoring, runbooks, ownership",
                "Prioritize critical / high / medium / low improvements",
            ],
            "Use the fictional current environment on the challenge slide. Live-score two areas, then hand the rest to Exercise 8.13.",
            img="38-checklist.svg",
        )
    )

    s.extend(
        exercise_block(
            13,
            "Complete a Production-Readiness Assessment",
            "25 min",
            "Score nine areas of the fictional deployment and classify ready / conditional / not ready.",
            "38-checklist.svg",
            "Production-readiness checklist",
            "Not ready is the honest answer. Challenge any Production-ready vote.",
        )
    )

    s.append(
        split_slide(
            "Module Summary",
            [
                "Intentional data modeling and efficient queries",
                "Evidence-based indexes and layered security",
                "Tested backups, monitoring, and alerting",
                "Reliable replication and deliberate scaling",
                "Documented troubleshooting and controlled change",
            ],
            "40-course-map.svg",
            "Module 8 sits on Modules 1–7",
            "Time-box remaining clock to labs. Minimum path: 8.2, 8.3, 8.6, 8.9, 8.11.",
        )
    )

    s.append(
        split_slide(
            "Course Summary",
            [
                "Explain MongoDB and NoSQL",
                "Install or provision an environment",
                "Design documents and collections",
                "CRUD, aggregation, indexes",
                "Replication and sharding concepts",
                "Production best practices",
            ],
            "40-course-map.svg",
            "Eight-module course map",
            "This is the promise from Day 1. Do not rush it. Names of people who struggled on Day 1 get a nod if appropriate.",
        )
    )

    # --- Labs ---
    s.append(
        content_slide(
            "Hands-on Labs — Time-box Guide",
            """Full sequence: Labs 8.1–8.11 (~4 hours if every laptop does everything).

**In the 3-day package,** prefer:

1. Lab 8.2 query/projection
2. Lab 8.3 monthly pipeline (or 8.4 if 5.6 already landed)
3. Lab 8.6 validation on `training_store_ops`
4. Lab 8.9 backup/restore isolated
5. Lab 8.11 integrated challenge

Discussion labs 8.7, 8.8, 8.10 can be instructor-led with the worksheets.""",
            "Say the minimum path twice. Do not start Lab 8.9 restoring onto training_store.",
            fit="fit-sm",
        )
    )

    s.extend(lab_block(1, "Data-Model Review and Repair", "25 min", "Inspect types, growth, and snapshots; propose validation and an XBAD migration note.", "41-demo-model.svg", "Model repair", "XBAD string price is the guaranteed find."))
    s.extend(lab_block(2, "Query and Projection Optimization", "25 min", "Baseline find({}), then filter, project, sort, limit, explain, and recommend an ESR index.", "11-selective-filter.svg", "Query optimization lab", "C101 _id lookup trips people — remind findOne customerNumber."))
    s.extend(lab_block(3, "Aggregation Pipeline Construction", "30 min", "Monthly paid sales with six metrics; two $group stages so unwind does not inflate revenue.", "16-unwind.svg", "Monthly sales pipeline", "Walk the two-group pattern on the board before they type."))
    s.extend(lab_block(4, "Aggregation Pipeline Tuning", "25 min", "Compare lookup-first versus match-first; verify C101 revenue by hand.", "15-early-match.svg", "Pipeline tuning", "Skip if Lab 8.3 ate the clock; assign as homework."))
    s.extend(lab_block(5, "Index Design and Validation", "25 min", "Inventory indexes, create history and paid-report keys, explain, do not drop.", "19-index-shape.svg", "Index validation", "Module 6 leftovers are fine — label them."))
    s.extend(lab_block(6, "Schema Validation Implementation", "20 min", "Validator on training_store_ops.orders_validated; prove valid and three invalid inserts.", "41-demo-model.svg", "Collection validation", "Decimal128 in $jsonSchema is bsonType decimal."))
    s.extend(lab_block(7, "Security Configuration Review", "25 min", "Mark findings on the fictional YAML; P1–P3 remediation; role sketches with redacted passwords.", "28-sec-anti.svg", "Unsafe configuration", "Do not enable auth on the shared instance."))
    s.extend(lab_block(8, "Monitoring and Log Analysis", "25 min", "Timeline from sample logs; cause is the filter field/case change; propose an alert.", "35-slow-app.svg", "Log correlation", "nreturned 0 is the tell. Field is status vs paymentStatus."))
    s.extend(lab_block(9, "Backup and Restore Verification", "30 min", "Dump training_store; restore to training_store_restore; verify counts, sample, indexes, duration vs RTO.", "31-restore-test.svg", "Backup and restore", "Abort if anyone targets the original db name."))
    s.extend(lab_block(10, "Troubleshooting Challenge", "30 min", "Five concurrent symptoms; do not collapse them; ordered investigation plus verify steps.", "34-troubleshoot.svg", "Multi-incident challenge", "Share the instructor key only after they commit to five statements."))
    s.extend(lab_block(11, "Final Integrated Production Challenge", "45–60 min", "Schema fix, validation, pipeline, explains, ops pack, and a scored checklist.", "42-lab-challenge.svg", "Integrated production challenge", "Capstone. Classification must not be Production-ready without auth, restore test, and network restriction."))

    s.extend(
        exercise_block(
            14,
            "Production-Readiness Review for training_store",
            "45 min",
            "Six-part action plan and a classification with evidence. Not production-ready is the defensible call.",
            "42-lab-challenge.svg",
            "Practical challenge",
            "Can replace Lab 8.11 if laptops are gone. Rubric: all six sections, owners on alerts, honest classification.",
        )
    )

    s.append(
        content_slide(
            "Final Course Knowledge Assessment",
            """Write short answers (pairs or solo):

1. Why design schemas around access patterns?
2. Why are unbounded arrays dangerous?
3. Why return only required fields?
4. Why reduce aggregation input early?
5. What risk does `$unwind` introduce?
6. Why index `$lookup` foreign fields?
7. Why not index every field?
8. What is least privilege?
9. Authentication vs authorization?
10. Why TLS?""",
            "Ten now, ten next slide. Collect if the sponsor wants attendance evidence. These are the exit-ticket set from the outline.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Final Course Knowledge Assessment (continued)",
            """11. Why keep credentials out of source code?
12. Why is replication not a backup?
13. What do RPO and RTO mean?
14. Why test restores?
15. Metrics for a slow query?
16. Metrics for replication problems?
17. What makes an alert actionable?
18. What belongs in a runbook?
19. Why rollback plans for production changes?
20. What evidence is required before calling a deployment production-ready?""",
            "Debrief 12, 13, 14, and 20 if time is almost gone. Those four are the course closer.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Final Practical Assessment",
            """Design a production-oriented e-commerce MongoDB solution:

1. Collections and sample documents
2. Embed vs reference decisions
3. CRUD queries and one aggregation
4. Index strategy; replica-set architecture; sharding recommendation
5. Security checklist; backup/recovery; monitoring; one runbook

**Bar:** correct BSON types, access-pattern design, bounded growth, accurate queries and aggregations, evidence-based indexes, HA and scale that match the load, least privilege, tested recovery, actionable ops.""",
            "This can be a take-home. Do not start it live if Lab 8.11 just finished — it duplicates the capstone at design-doc fidelity.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Participant Action Plan",
            """Before the next work week, write:

- One schema or validation change you will propose
- One query or index you will `explain`
- One security control you will verify (auth, network, secrets)
- One restore test you will schedule
- One alert or runbook you will add
- A named owner for each item""",
            "Two minutes of silent writing. This is the course souvenir. Invite one share-out.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Module 8 Completion Checklist",
            """Participants can:

- [ ] Review and improve a MongoDB data model
- [ ] Spot query and aggregation inefficiencies
- [ ] Recommend and validate indexes
- [ ] Apply layered security and least privilege
- [ ] Explain backup/recovery, RPO, and RTO
- [ ] Select metrics and actionable alerts
- [ ] Diagnose common incidents and write a runbook
- [ ] Complete a production-readiness assessment""",
            "Gaps become the action plan. Do not invent extra homework.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Questions and Answers",
            """Open floor.

Parking-lot prompts if the room is quiet:

- Would you go live on training_store tonight? Why not?
- Where does your current team store the database URI?
- When did you last restore a backup on purpose?
- Which alert would you delete this week?

Driver-language wiring belongs in the sample-app README, not a new module.""",
            "Keep answers short. Collect parking-lot items for email follow-up rather than reopening Module 6.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Course Review",
            """Day 1 — Why documents, a working instance, a schema for training_store.

Day 2 — Query language and aggregation on the same data.

Day 3 — Indexes and explain; replica sets and sharding; production operations.

The dataset stayed still so the skills could compound.""",
            "Thank the room. If evaluations are required, now. Do not start a new technical topic.",
            fit="fit-sm",
        )
    )

    s.append(
        split_slide(
            "Next Steps and Continued Learning",
            [
                "Apply the six-area checklist to one real database",
                "Schedule a restore test and a failover test",
                "Read current MongoDB security and ops manuals for your version and platform",
                "Practice `explain` on the queries that pay the bills",
                "Keep secrets out of git",
            ],
            "45-day3-close.svg",
            "From indexed shapes to operable systems",
            "Point at manuals, not random blogs. Version matters. End on time.",
        )
    )

    return "\n\n---\n\n".join(x.strip() + "\n" for x in s)


def append_to_deck(fragment: str) -> None:
    text = DECK.read_text(encoding="utf-8")
    if MARKER in text:
        start = text.find(MARKER)
        prefix = text[:start].rstrip()
        if prefix.endswith("---"):
            prefix = prefix[: -3].rstrip()
        DECK.write_text(prefix + "\n\n---\n\n" + fragment.strip() + "\n", encoding="utf-8")
        print(f"Replaced existing Module 8 in {DECK}")
        return
    DECK.write_text(text.rstrip() + "\n\n---\n\n" + fragment.strip() + "\n", encoding="utf-8")
    print(f"Appended Module 8 to {DECK}")


if __name__ == "__main__":
    if not any(LAB_DIR.glob("exercise-8.1-*.md")):
        raise SystemExit("Lab guides missing. Run python scripts/module08_labs.py first.")
    fragment = build_slides()
    append_to_deck(fragment)
    print(f"Module 8 fragment length: {len(fragment):,} chars")
