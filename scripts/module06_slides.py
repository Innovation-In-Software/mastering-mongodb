"""Emit Module 6 Marp slides and append them to the course deck.

Run after lab guides exist:

    python scripts/module06_labs.py
    python scripts/module06_diagrams.py
    python scripts/module06_slides.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from course_config import deck_md
from module06_labs import OUT as LAB_DIR

DECK = deck_md()
MARKER = "<!-- _header: 'Module 6 — Indexing and Query Performance' -->"
NEXT_MARKERS = (
    "<!-- _header: 'Module 7 — Introduction to Replication and Sharding' -->",
    "<!-- _header: 'Module 7 — Introduction to Sharding and Replication' -->",
    "<!-- _header: 'Module 8 — Best Practices' -->",
    "<!-- _header: 'Module 8 — MongoDB Best Practices, Security, and Troubleshooting' -->",
)


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

<img src="assets/module-06/{img}" alt="{alt}" width="720">

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
    matches = sorted(LAB_DIR.glob(f"{kind}-6.{num}-*.md"))
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
        do = re.sub(r"\s+", " ", m.group(3)).strip()[:220]
        exp = re.sub(r"\s+", " ", m.group(4)).strip()[:160]
        steps.append((m.group(2).strip(), do, exp))
    return steps


def _step_slides(kind: str, num: int, rel: str, script: str) -> list[str]:
    label = "Exercise" if kind == "exercise" else "Lab"
    steps = parse_steps(kind, num)
    slides = []
    for i in range(0, len(steps), 2):
        pair = steps[i : i + 2]
        b = pair[1][0] if len(pair) > 1 else ""
        heading = f"## {label} 6.{num} — Steps {i + 1}–{i + 2 if b else i + 1}"
        lines = [
            "<!-- _class: fit-md -->",
            "",
            heading,
            "",
            f"**Lab guide:** [`{label} 6.{num}`](../slide-exercises/{rel})" if i == 0 else "",
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
    lab = next(LAB_DIR.glob(f"exercise-6.{num}-*.md"))
    rel = lab.as_posix().split("slide-exercises/")[-1]
    intro = split_slide(
        f"Exercise 6.{num} — {title}",
        [f"**Time:** {time}", objective, f"**Lab guide:** [`Exercise 6.{num}`](../slide-exercises/{rel})"],
        img,
        alt,
        script,
        fit="fit-md",
    )
    return [intro] + _step_slides("exercise", num, rel, script)


def lab_block(num: int, title: str, time: str, objective: str, img: str, alt: str, script: str) -> list[str]:
    lab = next(LAB_DIR.glob(f"lab-6.{num}-*.md"))
    rel = lab.as_posix().split("slide-exercises/")[-1]
    intro = split_slide(
        f"Lab 6.{num} — {title}",
        [f"**Time:** {time}", objective, f"**Lab guide:** [`Lab 6.{num}`](../slide-exercises/{rel})"],
        img,
        alt,
        script,
        fit="fit-md",
    )
    return [intro] + _step_slides("lab", num, rel, script)


def demo_slide(n: str, title: str, body, script: str, img: str | None = None) -> str:
    if img:
        bullets = body if isinstance(body, list) else [body]
        return split_slide(f"Demo 6.{n} — {title}", bullets, img, title, script, fit="fit-md")
    return content_slide(f"Demo 6.{n} — {title}", body if isinstance(body, str) else "\n".join(f"- {b}" for b in body), script, fit="fit-sm")


def build_slides() -> str:
    s: list[str] = []

    s.append(f"""{MARKER}

<!-- _class: lead -->

# Indexing and Query Performance

An index trades storage and write cost for faster access to selected data

{notes("Indexing and Query Performance", '''Open Day 3 on the same training_store data they queried and aggregated on Day 2. Today is evidence: explain() before opinions.

The module covers index structures, field order, specialized types, covered queries, execution plans, and maintenance. The dataset is small — teach the plan, not the stopwatch.

Ask who has waited on a slow catalog page. That pain is a missing or wrong index, not "MongoDB is slow."
''')}
""")

    s.append(
        content_slide(
            "Module Learning Objectives",
            """By the end of this module you will be able to:

- Recognize queries that need indexes
- Create, inspect, hide, and remove indexes
- Design compound indexes around query shapes
- Apply Equality–Sort–Range as a starting guideline
- Choose specialized index types appropriately
- Read essential `explain()` statistics
- Compare collection scans with index scans
- Remove unnecessary index overhead
- Recommend indexes based on evidence""",
            "Read the outcomes. The through-line is: shape → smallest useful index → explain → write cost. Not every field gets an index.",
        )
    )

    s.append(
        split_slide(
            "Why Query Performance Matters",
            [
                "Slow user experiences and API timeouts",
                "More CPU and disk reads",
                "Higher cloud cost",
                "Resource contention",
                "Reduced system capacity",
                "Longer reporting jobs",
                "**Key:** one bad plan often hurts the whole workload",
            ],
            "009-read-vs-write-cost.svg",
            "Faster reads balanced against write cost",
            "Performance is a capacity problem. A collection scan on a hot query steals I/O from everything else, including writes.",
        )
    )

    s.append(
        split_slide(
            "How MongoDB Finds Documents",
            [
                "Without a suitable index, MongoDB may inspect many or all documents",
                "With a suitable index it can:",
                "1. Navigate index keys",
                "2. Identify candidate documents",
                "3. Fetch only required records",
                "4. Return matching results",
            ],
            "006-index-lookup-flow.svg",
            "Query, index search, document references, results",
            "Keep this binary for now: no suitable index versus suitable index. Later we add 'index exists but is a poor fit.'",
        )
    )

    s.append(
        split_slide(
            "Collection Scan vs. Index Scan",
            [
                "**COLLSCAN** — check documents in turn",
                "**IXSCAN** — search ordered keys, then selected documents",
                "**FETCH** — load full documents from index hits",
                "An index scan is not automatically efficient",
                "Examined keys and documents still matter",
            ],
            "003-collscan-vs-ixscan.svg",
            "COLLSCAN versus IXSCAN",
            "Write COLLSCAN, IXSCAN, FETCH on the board. They will read these in explain() within 15 minutes.",
        )
    )

    s.append(
        split_slide(
            "What Is an Index?",
            [
                "A separate, ordered data structure",
                "Stores values from indexed fields",
                "Stores references to documents",
                "Example key: category + price",
                "ACCESSORY | 49.99 → a product document",
            ],
            "004-what-is-an-index.svg",
            "Ordered field values connected to documents",
            "Likening this to a book index is fine. The collection is the book; the index is the back-of-book lookup.",
        )
    )

    s.append(
        split_slide(
            "Conceptual Index Structure",
            [
                "Common indexes are conceptually tree-based and ordered",
                "Direct value lookup",
                "Ordered traversal",
                "Range lookup",
                "Sorted retrieval",
                "Prefix matching on compound keys",
                "Internal engine details are out of scope here",
            ],
            "005-conceptual-index-structure.svg",
            "Tree-based navigation from a search key",
            "Do not dive into WiredTiger B-tree internals. Ordered keys are enough to motivate ESR and prefixes.",
        )
    )

    s.append(
        split_slide(
            "Index Benefits",
            [
                "Equality and range searches",
                "Sorting and pagination",
                "Uniqueness enforcement",
                "Early aggregation `$match` / `$sort`",
                "`$lookup` on the foreign key",
                "Geospatial and text search",
                "TTL expiration of temporary data",
            ],
            "007-index-benefits.svg",
            "Faster filtering, sorting, lookup, uniqueness, pagination",
            "Indexes are not only for find(). Preview aggregation and $lookup so Module 5 work still feels relevant.",
        )
    )

    s.append(
        split_slide(
            "Index Costs and Tradeoffs",
            [
                "Storage and memory pressure",
                "Insert, update, and delete cost",
                "Backup size and replication work",
                "Operational complexity",
                "**Key:** index real query patterns, not every field",
            ],
            "008-index-costs.svg",
            "Storage, memory, write work, replication, maintenance",
            "Every createIndex is a permanent write tax until you drop it. That sentence should follow them out of the room.",
        )
    )

    s.append(
        split_slide(
            "The Default `_id` Index",
            [
                "Created automatically",
                "Fast `_id` lookups",
                "Enforces `_id` uniqueness",
                "Cannot normally be dropped on a regular collection",
                "Does **not** cover SKU, email, or orderNumber",
            ],
            "012-business-id-vs-id.svg",
            "Automatic _id index versus SKU or order-number indexes",
            "Show db.products.getIndexes() in a moment — they will see _id_. Business keys still need indexes.",
        )
    )

    s.append(
        split_slide(
            "Listing Existing Indexes",
            [
                "`db.products.getIndexes()`",
                "Review name, key pattern, direction",
                "Uniqueness, partial filter, TTL",
                "Hidden flag and other options",
            ],
            "018-listing-collection-indexes.svg",
            "Collection connected to _id, single-field, compound, and specialized indexes",
            "Live: run getIndexes() on products. Name the _id_ index. Any extras from a previous demo become a teaching moment.",
            fit="fit-md",
        )
    )

    s.append(
        content_slide(
            "Creating an Index",
            """```javascript
db.products.createIndex({ sku: 1 })
```

With a custom name:

```javascript
db.products.createIndex(
  { sku: 1 },
  { name: "idx_products_sku" }
)
```

`1` is ascending; `-1` is descending. **Name indexes on purpose.**""",
            "Default names like sku_1 become unreadable in explain. Adopt idx_ / uq_ / ttl_ now.",
            fit="fit-sm",
        )
    )

    s.append(
        split_slide(
            "Removing an Index",
            [
                "`db.products.dropIndex(\"idx_products_sku\")`",
                "Confirm the exact name",
                "Review query dependencies",
                "Review `$indexStats`",
                "Test safely — hide first when unsure",
                "Keep a rollback `createIndex`",
            ],
            "127-safe-index-removal.svg",
            "Identify, hide, monitor, remove, validate",
            "Dropping is easy; restoring under load is not. Hide is the rehearsal.",
        )
    )

    s.append(
        split_slide(
            "Hiding and Unhiding an Index",
            [
                "Still stored and maintained",
                "Planner will not select it",
                "`hideIndex` / `unhideIndex`",
                "Test whether the index is still required",
                "**Tradeoff:** writes and storage still paid",
            ],
            "126-hidden-vs-dropped.svg",
            "Reversible planner exclusion compared with physical removal",
            "Hide ≠ drop. Writes still pay. That is why hide is a planner test, not a write-cost test.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Single-Field Indexes",
            [
                "`{ category: 1 }` supports `find({ category: \"LAPTOP\" })`",
                "May also support sorting by that field",
                "Strong candidate: unique business identifiers",
                "Weak standalone candidate: booleans",
            ],
            "013-single-field-index.svg",
            "One indexed field in ordered key sequence",
            "SKU is the poster child. active is not. We will put active in a compound or partial index later.",
        )
    )

    s.append(
        split_slide(
            "Ascending and Descending Index Direction",
            [
                "Single-field indexes can usually be traversed either way",
                "`{ createdAt: 1 }` can serve `sort({ createdAt: 1 })` and reverse",
                "Direction matters more on compound indexes with mixed sorts",
            ],
            "016-ascending-vs-descending.svg",
            "Direction on single-field versus compound indexes",
            "Do not over-teach 1 vs -1 on one field. Save the energy for compound mixed directions.",
        )
    )

    s.append(demo_slide(
        "1",
        "Compare a Collection Scan and Index Scan",
        [
            "**Time:** 15 min",
            "Explain `find({ category: \"ACCESSORY\" })` — record stage, keys, docs, nReturned",
            "Create `idx_products_category`",
            "Explain again and compare",
            "training_store is small — teach the plan, not the clock",
        ],
        "Run live. Write COLLSCAN numbers, createIndex, write IXSCAN numbers. Four ACCESSORY products should match.",
        "100-explain-before-after.svg",
    ))

    s.append(
        content_slide(
            "Demo 6.1 — Commands",
            """```javascript
db.products.find({ category: "ACCESSORY" }).explain("executionStats")

db.products.createIndex(
  { category: 1 },
  { name: "idx_products_category" }
)

db.products.find({ category: "ACCESSORY" }).explain("executionStats")
```

Record winning stage, `totalKeysExamined`, `totalDocsExamined`, `nReturned`.""",
            "If an index already exists from a rehearsal, drop it first so the room sees COLLSCAN.",
            fit="fit-sm",
        )
    )

    s.append(demo_slide(
        "2",
        "Create and Inspect a Single-Field Index",
        [
            "**Time:** 10 min",
            "Create `idx_products_sku` on `{ sku: 1 }`",
            "`getIndexes()` — name, key, unique flag",
            "Explain `find({ sku: \"L100\" })`",
        ],
        "Point at the name and key pattern. Later Demo 6.6 will drop this to create a unique index on the same keys.",
        "014-equality-lookup-sku.svg",
    ))

    s.append(
        split_slide(
            "Compound Indexes",
            [
                "More than one field in one index",
                "`{ category: 1, price: 1 }`",
                "May support equality plus a range on the later field",
                "One well-ordered compound index often beats two single-field indexes",
            ],
            "019-compound-index-structure.svg",
            "Compound index on category and price",
            "This is the heart of the module. Field order is a design decision, not a cosmetic one.",
        )
    )

    s.append(
        split_slide(
            "Compound-Index Field Order",
            [
                "`{ category: 1, price: 1 }` and `{ price: 1, category: 1 }` are different",
                "Affects supported query shapes",
                "Usable prefixes",
                "Sort support and scan size",
            ],
            "020-compound-field-order.svg",
            "Two compound indexes with reversed fields",
            "Ask the room which one helps 'all ACCESSORY under $50' before you show the answer.",
        )
    )

    s.append(
        split_slide(
            "Compound-Index Prefixes",
            [
                "For `{ category: 1, price: 1, name: 1 }`",
                "Usable: category",
                "Usable: category + price",
                "Usable: category + price + name",
                "A query on price alone does not use that leading prefix",
                "**Key:** leftmost fields organize the index",
            ],
            "021-compound-index-prefixes.svg",
            "Left-to-right compound prefixes",
            "Walk three queries: category only; category+price; price only. The last one is the trap.",
        )
    )

    s.append(
        split_slide(
            "Equality–Sort–Range Guideline",
            [
                "1. Equality fields",
                "2. Sort fields",
                "3. Range fields",
                "Example history query: customerId, sort total, range createdAt",
                "Candidate `{ customerId: 1, total: -1, createdAt: 1 }`",
                "ESR is a **guideline** — validate with data and explain",
            ],
            "025-equality-sort-range.svg",
            "Equality then sort then range",
            "Work the example on the whiteboard. Stress guideline, not law. Selectivity can swap equality fields; it should not put a wide range first without evidence.",
        )
    )

    s.append(
        split_slide(
            "Indexes for Equality, Range, and Sort",
            [
                "Equality: jump to matching keys — `{ sku: 1 }`",
                "Range: scan a key interval — `{ price: 1 }`",
                "Sort: traverse already-ordered keys",
                "Equality on a leading field lets the next field provide order",
            ],
            "026-classifying-esr-fields.svg",
            "Equality, range, and sort index behavior",
            "SKU is a seek. Price between 100 and 500 is a walk. Mix them wrongly and the walk gets wide.",
        )
    )

    s.append(
        split_slide(
            "Supporting Filter and Sort Together",
            [
                "Query: ACCESSORY, active true, sort price",
                "Candidate `{ category: 1, active: 1, price: 1 }`",
                "Equality on category and active",
                "Then sorted price",
                "Validate selectivity before deploying",
            ],
            "024-filter-and-sort-compound.svg",
            "Compound index supporting filter and sort",
            "This is Demo 6.3 and Lab 6.3. active is a poor index alone and a useful second equality field here.",
        )
    )

    s.append(
        split_slide(
            "Sort Direction and Index Direction",
            [
                "`{ category: 1, price: -1 }` supports that sort pair",
                "Complete reverse `{ category: -1, price: 1 }` can use the same index",
                "Arbitrary mixed directions may add a SORT stage",
            ],
            "035-mixed-sort-directions.svg",
            "Matching and reversing compound sort directions",
            "If they need category 1 + price 1, this index does not give that order for free. Show SORT in explain if you have time.",
        )
    )

    s.append(demo_slide(
        "3",
        "Design a Compound Index",
        [
            "**Time:** 15 min",
            "Query: ACCESSORY + active, sort price",
            "Create `idx_products_category_active_price`",
            "Compare explain before and after — watch for SORT",
        ],
        "If Demo 6.1's category index wins instead, say so — the planner picks a candidate. The compound index is the one that can also sort.",
        "024-filter-and-sort-compound.svg",
    ))

    s.append(demo_slide(
        "4",
        "Apply Equality–Sort–Range",
        [
            "**Time:** 20 min",
            "Customer order history: equality customerId, sort createdAt, range total — or date range on createdAt",
            "Test alternative field orders",
            "Compare examined keys",
        ],
        "On 17 orders the difference is modest. Narrate what would happen with millions of orders: leading with total scans every high-value order in the store.",
        "025-equality-sort-range.svg",
    ))

    s.extend(exercise_block(
        1,
        "Identify Candidate Indexes",
        "15 min",
        "Name indexed fields for six recurring training_store queries.",
        "162-ex-6-1-candidates.svg",
        "Candidate index fields for common queries",
        "Discussion. Do not create indexes yet. SKU and email are identifiers; history queries need sort fields named.",
    ))

    s.extend(exercise_block(
        2,
        "Select Single or Compound Indexes",
        "15 min",
        "Classify requirements as single-field, compound, specialized, or not enough evidence.",
        "163-ex-6-2-single-or-compound.svg",
        "Choosing an index type",
        "The one-time ad-hoc count is the trick: no standing index. TTL is specialized.",
    ))

    s.extend(exercise_block(
        3,
        "Arrange Compound-Index Fields",
        "15 min",
        "Propose field order for a paid high-value order query that sorts by date.",
        "164-ex-6-3-arrange-fields.svg",
        "ESR field order",
        "Range total must not lead. customerId is the selective equality field.",
    ))

    s.extend(exercise_block(
        4,
        "Apply Equality–Sort–Range",
        "15 min",
        "Label equality, sort, and range on three shapes and propose compound indexes.",
        "165-ex-6-4-esr-classification.svg",
        "Three ESR shapes",
        "Shape B uses createdAt as both sort and range — one field in the index, not two.",
    ))

    s.extend(exercise_block(
        5,
        "Identify Index Prefixes",
        "10 min",
        "List prefixes of `{ customerId: 1, paymentStatus: 1, createdAt: -1 }` and mark unsupported shapes.",
        "166-ex-6-5-prefix-challenge.svg",
        "Compound index prefixes",
        "paymentStatus-only is the trap. Skipping paymentStatus while sorting createdAt breaks the sort prefix.",
    ))

    s.append(
        split_slide(
            "Multikey Indexes",
            [
                "An array-valued indexed path creates an entry per element",
                "`{ tags: 1 }` supports `find({ tags: \"technology\" })`",
                "The index is reported as multikey",
                "Array cardinality multiplies index keys",
            ],
            "039-multikey-index.svg",
            "Array field becoming a multikey index",
            "B300 has tags technology. Wireless matches several accessories. Mention write cost if tags arrays grow.",
        )
    )

    s.append(
        split_slide(
            "Indexing Nested Fields",
            [
                "Use quoted dot notation",
                '`"contact.email"` on customers',
                '`"addresses.city"` may be multikey — addresses is an array',
                "Index the path the query uses",
            ],
            "017-indexing-nested-field.svg",
            "Dot-notation paths for nested indexes",
            "contact.email is a nested scalar. addresses.city is an array of documents. Same syntax, different multikey behavior.",
        )
    )

    s.append(demo_slide(
        "5",
        "Create a Multikey Index",
        [
            "**Time:** 10 min",
            "Create `idx_products_tags`",
            "Query `tags: \"technology\"`",
            "Show multikey in getIndexes or explain",
        ],
        "Point at multikey: true. If Compass is open, the Indexes tab also shows it.",
        "040-querying-array-multikey.svg",
    ))

    s.append(
        split_slide(
            "Unique Indexes",
            [
                "Database-level enforcement",
                "SKU, customerNumber, orderNumber, email, idempotency keys",
                "`unique: true` plus a clear name `uq_...`",
                "Build fails if duplicates already exist",
            ],
            "042-unique-index.svg",
            "Unique indexes on business identifiers",
            "Application checks are not enough. Two app servers will race. Unique index is the lock.",
        )
    )

    s.append(demo_slide(
        "6",
        "Enforce Uniqueness",
        [
            "**Time:** 10 min",
            "Drop `idx_products_sku` if present (same keys)",
            "Create `uq_products_sku`",
            "Insert a second L100 — read the duplicate-key error",
        ],
        "E11000 is the badge of success. Do not leave the duplicate document in the collection.",
        "043-unique-enforcement-flow.svg",
    ))

    s.append(
        split_slide(
            "Partial Indexes",
            [
                "Index only documents matching a filter",
                "Example: `partialFilterExpression: { active: true }`",
                "Smaller index, lower maintenance",
                "Queries generally need to be compatible with the filter",
            ],
            "047-partial-vs-sparse.svg",
            "Partial versus sparse selection rules",
            "Catalog pages that always send active: true can use this. A query that wants inactive clearance items cannot.",
        )
    )

    s.append(
        content_slide(
            "Sparse Indexes",
            """A sparse index omits documents that **do not contain** the indexed field.

```javascript
db.products.createIndex(
  { discountCode: 1 },
  { sparse: true }
)
```

Less flexible than a partial index: the rule is only “field exists,” not an arbitrary filter.""",
            "training_store has no discountCode — keep this conceptual or insert one demo doc if you want a live sparse example.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Partial vs. Sparse Indexes",
            """| Consideration | Partial | Sparse |
| --- | --- | --- |
| Selection rule | Explicit filter | Indexed field exists |
| Flexibility | Higher | Lower |
| Common use | Active / status subset | Optional field |
| Query compatibility | Must align with filter | Respect missing fields |

**Preference:** partial when you can state the subset clearly.""",
            "If they remember one row: partial = filter expression. Sparse = field present.",
            fit="fit-sm",
        )
    )

    s.append(demo_slide(
        "7",
        "Use a Partial Index",
        [
            "**Time:** 15 min",
            "Create `idx_active_products_category_price` with `active: true`",
            "Explain a query that includes `active: true`",
            "Explain the same category/price query that omits it",
        ],
        "L190 is an inactive LAPTOP — that is why the incompatible query cannot rely on the partial index.",
        "045-active-products-partial.svg",
    ))

    s.append(
        split_slide(
            "TTL Indexes",
            [
                "Expire documents from a date field",
                "`expireAfterSeconds: 0` with an `expiresAt` timestamp",
                "Sessions, tokens, short-lived logs, cache rows",
                "Expiration is **asynchronous**, not exact-timestamp",
            ],
            "048-ttl-index.svg",
            "TTL index lifecycle",
            "The TTL monitor runs periodically (about 60s). Lab 6.7 inserts an already-expired session so they can watch it vanish — or not yet.",
        )
    )

    s.append(demo_slide(
        "8",
        "Create a TTL Index",
        [
            "**Time:** 10 min",
            "Use a dedicated `sessions` collection — not a second app dataset",
            "Index `expiresAt` with expireAfterSeconds 0",
            "Insert one future and one past document",
            "Explain async cleanup",
        ],
        "Do not wait out the full minute in silence — set a reminder and keep teaching specialized types.",
        "049-session-expiration-ttl.svg",
    ))

    s.append(
        split_slide(
            "Text, Wildcard, Geospatial, and Hashed",
            [
                "**Text:** `$text` word search — one text index per collection",
                "**Wildcard:** `attributes.$**` for dynamic paths",
                "**Geospatial:** `2dsphere` on GeoJSON points",
                "**Hashed:** equality distribution; no ordered range",
                "Advanced search often belongs in a dedicated search product",
            ],
            "037-index-types-overview.svg",
            "Specialized index types",
            "Hashed is a teaser for Module 7 shard keys. Wildcard is a last resort, not a substitute for ESR design.",
        )
    )

    s.append(
        content_slide(
            "Text and Wildcard Examples",
            """```javascript
db.products.createIndex({ name: "text", description: "text" })
db.products.find({ $text: { $search: "wireless keyboard" } })

db.products.createIndex({ "attributes.$**": 1 })
```

training_store product `attributes` vary by category (laptop vs shoe vs book). Wildcard can index those paths; it is still a write and storage cost.""",
            "Do not build both a heavy text index and a wildcard index in every demo — pick one live if time is short.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Geospatial and Hashed Examples",
            """```javascript
db.stores.createIndex({ location: "2dsphere" })
```

Use for nearby stores, delivery zones, asset locations.

```javascript
db.events.createIndex({ tenantId: "hashed" })
```

Hashed keys support hashed sharding and equality distribution. They do **not** preserve sort order or range scans.""",
            "No stores collection in training_store. Keep geo conceptual unless you insert two Point documents in a scratch collection.",
            fit="fit-sm",
        )
    )

    s.append(
        split_slide(
            "Choosing the Appropriate Index Type",
            [
                "One field lookup → single-field",
                "Filter and sort on several fields → compound",
                "Unique identifier → unique",
                "Array elements → multikey",
                "Active subset → partial",
                "Expire rows → TTL",
                "Dynamic attributes → wildcard (with caution)",
            ],
            "038-index-type-selection-map.svg",
            "Requirement to index-type mapping",
            "This table is the exercise 6.6 answer key. Pause for questions before covered queries.",
        )
    )

    s.extend(exercise_block(
        6,
        "Select Specialized Index Types",
        "15 min",
        "Match eight requirements to unique, partial, sparse, TTL, text, wildcard, geospatial, or hashed.",
        "167-ex-6-6-specialized-matching.svg",
        "Specialized index chooser",
        "Hashed is not for date ranges. Partial beats sparse when they can write the filter.",
    ))

    s.append(
        split_slide(
            "Covered Queries",
            [
                "All filter fields are in the index",
                "All returned fields are in the index",
                "MongoDB does not need to FETCH full documents",
                "Exclude `_id` if it is not in the index",
                "Confirm with `explain()` — do not assume",
            ],
            "072-covered-vs-noncovered.svg",
            "Conditions for a covered query",
            "_id is the gotcha. Default projection includes it and breaks coverage.",
        )
    )

    s.append(
        split_slide(
            "Covered Query Example",
            [
                "Index `{ category: 1, price: 1, name: 1 }`",
                'Filter `category: "BOOK"`',
                "Project name and price with `_id: 0`",
                "Potential plan: IXSCAN → projection (no FETCH)",
            ],
            "077-covered-product-summary.svg",
            "Category filter returning only indexed name and price",
            "Two BOOK products. Live explain in Demo 6.9. If FETCH remains, debug projection and _id.",
            fit="fit-md",
        )
    )

    s.append(demo_slide(
        "9",
        "Identify a Covered Query",
        [
            "**Time:** 15 min",
            "Create `idx_products_category_price_name`",
            "Query BOOK with `_id: 0`, name, price",
            "Inspect whether FETCH is absent",
        ],
        "Then add tags to the projection and watch FETCH return. That contrast is the lesson.",
        "072-covered-vs-noncovered.svg",
    ))

    s.append(
        split_slide(
            "Index Selectivity",
            [
                "**Higher:** email, SKU, order number",
                "**Lower:** `active`, small status sets, a few countries",
                "Low-selectivity fields still help in compound or partial indexes",
                "A leading boolean can make an IXSCAN almost a COLLSCAN",
            ],
            "078-high-vs-low-selectivity.svg",
            "High versus low selectivity fields",
            "Most training_store products are active. Indexing active alone is a cautionary tale.",
        )
    )

    s.append(
        split_slide(
            "Query Shapes",
            [
                "Filter fields and operators",
                "Sort fields and projection",
                "Collation and query options",
                "Same shape → same index design",
                "Index recurring shapes, not isolated example values",
            ],
            "082-query-shape-anatomy.svg",
            "Parts of a query shape",
            "ACCESSORY vs LAPTOP is the same shape. Do not create one index per category value.",
        )
    )

    s.append(
        split_slide(
            "Index Intersection",
            [
                "MongoDB may combine two single-field indexes",
                "`{ category: 1 }` and `{ active: 1 }`",
                "A designed compound index is usually more predictable",
                "Especially when a sort is required",
            ],
            "087-intersection-vs-compound.svg",
            "Index intersection versus a compound index",
            "Mention intersection so they do not think two indexes are always combined. Prefer one compound for the catalog sort.",
        )
    )

    s.append(
        split_slide(
            "Indexes and Regular Expressions",
            [
                'Anchored prefix `^Mongo` may use an index',
                "Unanchored `/Mongo/` often scans broadly",
                "Leading wildcards, case, and collation change eligibility",
                "Do not use regex as a substitute for a structured field",
            ],
            "069-prefix-regex-index.svg",
            "Anchored versus unanchored regular expressions",
            "If they need contains-search, talk text index or external search — not a leading-wildcard regex on name.",
        )
    )

    s.append(
        split_slide(
            "Indexes, Aggregation, and `$lookup`",
            [
                "Helpful early: `$match`, `$sort`, some geo stages",
                "Paid orders newest first → `{ paymentStatus: 1, createdAt: -1 }`",
                "`$group` still runs after the indexed prefix",
                "`$lookup`: index the **foreign** field",
                "`customers._id` is already indexed",
            ],
            "108-indexes-in-aggregation.svg",
            "Indexes for aggregation and lookup",
            "Lab 6.9 is this slide in mongosh. $lookup onto customerNumber would need an index; onto _id does not.",
        )
    )

    s.append(
        split_slide(
            "Query Execution Plans",
            [
                "The planner evaluates strategies and picks a winner",
                "Stages include COLLSCAN, IXSCAN, FETCH, SORT",
                "Plus projection and limit-related stages",
                "The plan is how MongoDB actually accessed the data",
            ],
            "098-ixscan-fetch-plan.svg",
            "Common execution plan stages",
            "From here to Demo 6.10 is the literacy block. Slow down.",
        )
    )

    s.append(
        content_slide(
            "Using `explain()`",
            """```javascript
db.products.find({ category: "ACCESSORY" }).explain("executionStats")

db.products.explain("executionStats").find({ category: "ACCESSORY" })

db.orders.explain("executionStats").aggregate([
  { $match: { paymentStatus: "PAID" } }
])
```""",
            "Both find styles are valid. Prefer executionStats in class. Aggregation uses explain on the collection helper.",
            fit="fit-sm",
        )
    )

    s.append(
        split_slide(
            "Explain Verbosity Modes",
            [
                "**queryPlanner** — parsed query, winning and rejected plans",
                "**executionStats** — adds nReturned, keys, docs, timing",
                "**allPlansExecution** — candidate race during selection",
                "Training default: `executionStats`",
            ],
            "094-explain-verbosity.svg",
            "Three explain verbosity modes",
            "allPlansExecution is noisy. Use it when two indexes compete and they ask why the winner won.",
        )
    )

    s.append(
        content_slide(
            "Reading `queryPlanner` and `executionStats`",
            """**queryPlanner — ask:**

- Expected index or COLLSCAN?
- Extra SORT?
- Which candidates were rejected?

**executionStats — record:**

- `nReturned`
- `totalKeysExamined`
- `totalDocsExamined`
- Stage tree and execution-time indicators

**Healthy direction:** examined counts stay close to the data the query actually needs.""",
            "Have them write the three numbers every time. Ritual beats theory.",
            fit="fit-sm",
        )
    )

    s.append(
        split_slide(
            "`COLLSCAN` vs `IXSCAN` vs `FETCH`",
            [
                "COLLSCAN — collection documents",
                "IXSCAN — index keys",
                "FETCH — documents after index hits",
                "Common: IXSCAN → FETCH → result",
                "Covered: IXSCAN → projection → result",
            ],
            "076-ixscan-projection-vs-fetch.svg",
            "Stage flow for indexed and covered queries",
            "Covered queries are the FETCH-free special case they just practiced.",
        )
    )

    s.append(
        split_slide(
            "Examined vs. Returned Documents",
            [
                "100,000 examined / 10 returned → high scan cost",
                "10 keys / 10 docs / 10 returned → targeted",
                "Ratios are signals, not SLAs",
                "training_store numbers stay small — still record them",
            ],
            "101-keys-docs-returned.svg",
            "Examined versus returned ratios",
            "Do not let them think 12 examined / 4 returned on accessories is a production crisis. Translate to 'imagine 12 million.'",
        )
    )

    s.append(
        split_slide(
            "In-Memory Sort Indicators",
            [
                "If the index cannot provide order, MongoDB adds SORT",
                "More CPU and memory",
                "Higher latency",
                "Large sorts may spill depending on configuration",
                "A matching compound index may remove the extra sort",
            ],
            "063-index-vs-inmemory-sort.svg",
            "Index-provided order versus extra SORT",
            "Look for SORT in the plan, not only in the query text. limit does not always save you from sorting the full match set first.",
        )
    )

    s.append(
        split_slide(
            "Winning and Rejected Plans",
            [
                "**Winning plan** — selected for execution",
                "**Rejected plans** — eligible but not chosen",
                "Rejected ≠ bad index",
                "It may simply be less suitable for this shape",
            ],
            "096-winning-and-rejected.svg",
            "Winning versus rejected plans",
            "If both category and compound indexes exist, show rejectedPlans. Great Demo 6.10 moment.",
        )
    )

    s.append(demo_slide(
        "10",
        "Evaluate Indexes with explain()",
        [
            "**Time:** 20 min",
            "Walk winning plan, index name, nReturned, keys, docs",
            "Find SORT if present",
            "Glance at rejected plans",
        ],
        "Use the catalog query and the C101 history query. This is the literacy exam before labs.",
        "098-ixscan-fetch-plan.svg",
    ))

    s.extend(exercise_block(
        7,
        "Interpret Explain Output",
        "20 min",
        "Identify COLLSCAN vs IXSCAN, examined counts, extra sort, and poor selectivity.",
        "168-ex-6-7-read-explain.svg",
        "Interpreting explain statistics",
        "They can use the printed sample in the lab guide or a live explain after Demo 6.1.",
    ))

    s.extend(exercise_block(
        8,
        "Identify Covered Queries",
        "15 min",
        "Decide which query/projection pairs may be covered by `{ category: 1, price: 1, name: 1 }`.",
        "169-ex-6-8-covered-challenge.svg",
        "Covered query combinations",
        "Q1 yes, Q2 tags no, Q3 _id no. Confirmation is always explain.",
    ))

    s.append(
        split_slide(
            "Index Usage Statistics",
            [
                "`db.products.aggregate([{ $indexStats: {} }])`",
                "Frequently used vs rarely used",
                "Candidate unused indexes",
                "**Caution:** process lifetime only — not month-end proof",
            ],
            "124-index-usage-monitoring.svg",
            "Query workload to index-usage statistics",
            "Lab 6.10 will run this. Prefacing the caveat now prevents false drops after lunch.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Redundant and Overlapping Indexes",
            [
                "`{ category: 1 }` may be a prefix of `{ category: 1, price: 1 }`",
                "Compare performance, size, coverage, sort, unique/partial, usage",
                "Do not drop from visual similarity alone",
            ],
            "088-overlapping-indexes.svg",
            "Overlapping compound prefixes",
            "The wider index can serve category-only queries but may be larger. Coverage of name is a reason to keep the three-field index.",
        )
    )

    s.append(demo_slide(
        "11",
        "Hide an Index for Testing",
        [
            "**Time:** 10 min",
            "Hide a noncritical training index (not `_id_`, not unique SKU)",
            "Rerun explain — planner should skip it",
            "Unhide",
            "Writes still paid the whole time",
        ],
        "hideIndex on idx_products_category if the compound index can cover the demo query.",
        "125-hidden-index-testing.svg",
    ))

    s.append(demo_slide(
        "12",
        "Identify a Redundant Index",
        [
            "**Time:** 15 min",
            "Compare `{ category: 1 }` with `{ category: 1, price: 1 }` (or the active+price compound)",
            "Review prefix support, plans, stats, size",
            "Do not drop until evidence supports it",
        ],
        "Use hiding from Demo 6.11 on this pair. Do not drop until evidence supports it.",
        "088-overlapping-indexes.svg",
    ))

    s.append(
        split_slide(
            "Over-Indexing",
            [
                "Slow inserts and updates",
                "Large index storage and memory pressure",
                "Longer maintenance operations",
                "Many similar indexes",
                "Indexes with no corresponding query",
                "The right number is workload-dependent",
            ],
            "123-over-indexing-symptoms.svg",
            "Symptoms of too many indexes",
            "Exercise 6.10 is the 80/20 write-heavy story. Fourteen secondary indexes is a smell, not a number to memorize.",
        )
    )

    s.append(
        split_slide(
            "Index Maintenance",
            [
                "Review usage and duplicates",
                "Test with hidden indexes",
                "Remove obsolete indexes",
                "Monitor size",
                "Update indexes as access patterns change",
                "Indexes should evolve with the application",
            ],
            "010-index-lifecycle.svg",
            "Ongoing index maintenance",
            "A new report is a new shape. A retired screen is a hide candidate. Treat indexes like code.",
        )
    )

    s.append(
        split_slide(
            "Indexes and Write Performance",
            [
                "Each insert updates the document, `_id`, and every affected secondary index",
                "More indexes → more write work",
                "Updates to indexed fields cost more than updates to non-indexed fields",
            ],
            "118-insert-with-multiple-indexes.svg",
            "Write path touching document and indexes",
            "Changing price maintains price-related indexes. Changing a non-indexed description field does not.",
        )
    )

    s.append(
        content_slide(
            "Storage and Working Memory",
            """**Index size depends on:** document count, key size, field count, array cardinality, index count, value repetition, and type.

Monitor collection data size **and** total index size.

Frequently used index pages may stay in memory. If the working set exceeds RAM:

- Disk access rises
- Latency becomes less predictable
- Competing queries evict useful pages

Smaller, targeted indexes are easier to keep hot.""",
            "training_store will not fill RAM. Translate: production catalogs with wide wildcard indexes often will not stay hot.",
            fit="fit-sm",
        )
    )

    s.append(
        split_slide(
            "Index Naming Standards",
            [
                "`idx_<collection>_<fields>`",
                "`uq_<collection>_<fields>`",
                "`ttl_<collection>_<field>`",
                "`geo_<collection>_<field>`",
                "Examples: `uq_products_sku`, `ttl_sessions_expires_at`",
                "Names should state operational intent",
            ],
            "129-index-naming-convention.svg",
            "Index naming convention examples",
            "If Compass and explain show sku_1, they will not remember why it exists next quarter.",
        )
    )

    s.append(
        split_slide(
            "Production Index-Change Safety",
            [
                "Capture the query shape and baseline explain",
                "Estimate size and build impact",
                "Test in a representative environment",
                "Schedule or control the change",
                "Monitor query and write latency; check replication",
                "Keep a rollback path and document the reason",
            ],
            "128-safe-index-creation.svg",
            "Safe production index changes",
            "Building a large index on a primary can hurt. Mention background/rolling builds at a high level without turning this into an ops course.",
        )
    )

    s.append(
        split_slide(
            "Query-Tuning Workflow",
            [
                "Identify the slow operation and exact shape",
                "Baseline + `explain(\"executionStats\")`",
                "Check types and predicates",
                "Smallest useful index",
                "Create or hide-test; re-explain",
                "Compare examined keys and documents",
                "Check write/storage impact; monitor under load",
            ],
            "131-query-tuning-lifecycle.svg",
            "Query-tuning workflow",
            "This is Labs 6.1–6.4 in twelve steps. Point at it during the integrated challenge.",
        )
    )

    s.append(
        content_slide(
            "Common Indexing Mistakes",
            """- Indexing every field
- Ignoring compound-field order
- Creating duplicate / overlapping indexes
- Placing a range field too early
- Ignoring sort requirements
- Indexing low-selectivity fields without context
- Indexing a one-time query
- Ignoring write overhead
- Assuming every `IXSCAN` is efficient
- Not verifying with `explain()`
- Removing an index without dependency analysis
- Ignoring data types and collation""",
            "Exercise 6.11 is this list as a rewrite activity. Read three aloud if time is short.",
            fit="fit-sm",
        )
    )

    s.append(
        split_slide(
            "Index Troubleshooting Workflow",
            [
                "Confirm database, collection, filter types",
                "Inspect the winning plan and eligibility",
                "Review prefixes and sort compatibility",
                "Check keys/docs examined and result size",
                "Consider multikey expansion and working-set size",
                "Compare against production-like data",
            ],
            "136-optimization-decision-tree.svg",
            "Troubleshooting a still-slow query",
            "The classic bug: string vs ObjectId on customerId, so the index is never used. Types first.",
        )
    )

    s.append(
        split_slide(
            "E-Commerce Indexing Strategy",
            [
                "SKU → unique `{ sku: 1 }`",
                "Catalog → `{ category: 1, active: 1, price: 1 }`",
                "Tags → multikey `{ tags: 1 }`",
                "Email → `{ \"contact.email\": 1 }`",
                "Order number → unique",
                "History → `{ customerId: 1, createdAt: -1 }`",
                "Paid reports → `{ paymentStatus: 1, createdAt: -1 }`",
                "Sessions → TTL on `expiresAt`",
            ],
            "161-ecommerce-query-index-matrix.svg",
            "training_store query patterns and candidate indexes",
            "Every row still needs explain on real distributions. This is the practical challenge answer sketch, not a paste-into-production list.",
        )
    )

    s.append(
        split_slide(
            "Module Summary",
            [
                "Indexes speed selected reads and tax writes/storage",
                "Compound order and prefixes define supported shapes",
                "ESR is a starting guideline",
                "Arrays become multikey; specialized types solve specific jobs",
                "`explain()` is evidence; IXSCAN is not a trophy",
                "Hide, measure, maintain",
            ],
            "150-ecommerce-strategy-overview.svg",
            "Module 6 concept map",
            "Pause. Remaining time goes to labs. Time-box to Labs 6.1–6.4 plus 6.11 if the afternoon includes Modules 7–8.",
        )
    )

    s.extend(exercise_block(
        9,
        "Find Redundant Indexes",
        "15 min",
        "Spot overlapping prefixes and list evidence required before hiding one.",
        "170-ex-6-9-redundant.svg",
        "Overlapping index prefixes",
        "price-only is not redundant with category-leading indexes.",
    ))

    s.extend(exercise_block(
        10,
        "Balance Read and Write Performance",
        "15 min",
        "Plan evidence, hide-testing, and metrics for a write-heavy cluster with 14 secondary indexes.",
        "171-ex-6-10-read-vs-write.svg",
        "Write-heavy over-indexing scenario",
        "Hide does not reduce write cost — they must say that. Drop is what helps inserts.",
    ))

    s.extend(exercise_block(
        11,
        "Correct Indexing Anti-Patterns",
        "15 min",
        "Rewrite seven unsafe indexing habits as safer practices.",
        "172-ex-6-11-fix-antipattern.svg",
        "Indexing anti-patterns",
        "Rapid-fire pairs. Collect two rewrites on the board: range-first and drop-immediately.",
    ))

    s.extend(exercise_block(
        12,
        "Build an Indexing Recommendation",
        "20 min",
        "Write query shape, plan, proposed index, benefit, cost, validation, and rollback.",
        "173-ex-6-12-recommendation-canvas.svg",
        "Indexing recommendation template",
        "This is the professional deliverable. Use it as a dry run for the practical challenge.",
    ))

    s.append(
        content_slide(
            "Hands-on Labs",
            """Same `training_store` database. Reload `load.js` if data or indexes are messy — then **re-create only the indexes the lab asks for**.

| Lab | Focus |
| --- | --- |
| 6.1 | Baseline explain — no new indexes |
| 6.2–6.4 | Single-field, compound, filter+sort |
| 6.5–6.7 | Nested/multikey, unique, partial/TTL |
| 6.8–6.9 | Covered query, aggregation |
| 6.10–6.11 | Audit/hide, integrated challenge |

**3-day time-box (~2 h module):** Labs 6.1, 6.2, 6.3, 6.4, and 6.11. Remaining labs are stretch.""",
            "If they reload load.js, unique and compound indexes from demos disappear. That is OK — labs recreate what they need.",
            fit="fit-sm",
        )
    )

    s.extend(lab_block(
        1,
        "Establish a Performance Baseline",
        "20 min",
        "Record explain baselines for catalog and order-history queries without creating indexes.",
        "174-lab-6-1-baseline.svg",
        "Baseline before indexing",
        "No createIndex. If demo indexes remain, note them as part of the baseline — or reload for a clean COLLSCAN story.",
    ))

    s.extend(lab_block(
        2,
        "Create and Test a Single-Field Index",
        "20 min",
        "Index SKU and compare examined documents before and after.",
        "175-lab-6-2-single-field-test.svg",
        "Single-field SKU index lab",
        "L100 is in the loader. Unique comes in Lab 6.6 — they may drop this non-unique index then.",
    ))

    s.extend(lab_block(
        3,
        "Design a Compound Index",
        "25 min",
        "Build `{ category, active, price }` and test which prefixes it supports.",
        "176-lab-6-3-compound-test.svg",
        "Compound catalog index lab",
        "active-only query is the expected failure. category-only should use the prefix.",
    ))

    s.extend(lab_block(
        4,
        "Support Filtering and Sorting",
        "25 min",
        "Compare compound orders for C101’s newest orders in a date range, limit 10.",
        "177-lab-6-4-filter-sort-design.svg",
        "Order-history compound index lab",
        "Keep idx_orders_customer_created. Drop any experimental createdAt-first index.",
    ))

    s.extend(lab_block(
        5,
        "Index Nested Fields and Arrays",
        "25 min",
        "Index contact.email and tags; confirm dotted lookup and multikey.",
        "178-lab-6-5-nested-and-array.svg",
        "Nested and multikey lab",
        "aisha@example.com and tags technology are in the dataset.",
    ))

    s.extend(lab_block(
        6,
        "Implement Data-Integrity Indexes",
        "20 min",
        "Unique SKU, customerNumber, and orderNumber; prove a duplicate SKU fails.",
        "179-lab-6-6-unique-validation.svg",
        "Unique index lab",
        "dropIndex idx_products_sku first. Cleanup discussion is oral if unique build succeeds on clean data.",
    ))

    s.extend(lab_block(
        7,
        "Implement Partial and TTL Indexes",
        "25 min",
        "Partial index for active products; TTL on a sessions collection.",
        "180-lab-6-7-partial-and-ttl.svg",
        "Partial and TTL lab",
        "Do not stall on TTL deletion. Configuration plus async caveat is the pass.",
    ))

    s.extend(lab_block(
        8,
        "Build a Covered Query",
        "20 min",
        "Cover category/price/name and confirm FETCH disappears when `_id` is excluded.",
        "181-lab-6-8-covered-test.svg",
        "Covered query lab",
        "If their MongoDB version labels the stage differently, still look for no FETCH and docs examined 0.",
    ))

    s.extend(lab_block(
        9,
        "Tune an Aggregation Pipeline",
        "25 min",
        "Index paid-order $match/$sort; explain why $group still needs memory.",
        "182-lab-6-9-agg-tuning.svg",
        "Aggregation index lab",
        "13 paid orders. Group by fulfillmentStatus. Index does not accelerate $sum itself.",
    ))

    s.extend(lab_block(
        10,
        "Audit and Rationalize Indexes",
        "25 min",
        "Inventory indexes, hide one candidate, test, unhide, recommend — do not drop.",
        "183-lab-6-10-audit-workflow.svg",
        "Index audit lab",
        "Never hide _id_. Unique SKU and TTL are poor hide targets for this exercise.",
    ))

    s.extend(lab_block(
        11,
        "Integrated Query-Tuning Challenge",
        "40–45 min",
        "Tune catalog and order-history pages with baselines, ESR, explain, and a cost note.",
        "184-lab-6-11-integrated.svg",
        "Integrated catalog and history tuning",
        "Capstone lab. If short on time, this plus Lab 6.1 is the minimum hands-on path after demos.",
    ))

    s.extend(exercise_block(
        13,
        "E-Commerce Index Review",
        "30–45 min",
        "Recommend indexes for ten application query patterns, including specialized types and overlap.",
        "185-practical-challenge-review.svg",
        "Practical challenge workload",
        "Discussion/table deliverable. Rubric: shape support, ESR, specialized types, explain plan, write cost, overlap.",
    ))

    s.append(
        content_slide(
            "Module 6 Exit Ticket",
            """Write a short answer for each:

1. COLLSCAN vs IXSCAN?
2. Why compound field order matters
3. What is an index prefix?
4. What does ESR mean?
5. When is an index multikey?
6. What does a unique index provide?
7. Partial vs sparse
8. What is a TTL index for?
9. What is a covered query?
10. Which explain values compare work vs results?
11. Why can an index slow writes?
12. Why hide before drop?
13. Does IXSCAN always mean efficient?
14. Why design around query shapes?

**Completion:** explain cost; create/inspect indexes; design compound keys; use prefixes and ESR; apply specialized types; read explain; recommend with evidence.""",
            "Collect if you use tickets for attendance. Questions 2, 4, 10, and 13 are the bar for Module 7.",
            fit="fit-xs",
        )
    )

    s.append(
        content_slide(
            "Module Completion Checklist",
            """Participants can:

- [ ] Explain the role and cost of indexes
- [ ] Create, list, hide, and drop indexes
- [ ] Design single-field and compound indexes
- [ ] Apply prefixes and Equality–Sort–Range
- [ ] Create multikey and unique indexes
- [ ] Explain partial, sparse, TTL, wildcard, text, geo, hashed
- [ ] Identify possible covered queries
- [ ] Read essential explain output
- [ ] Distinguish COLLSCAN from IXSCAN
- [ ] Detect redundant indexes
- [ ] Recommend indexes using measured evidence""",
            "Gaps become homework on the lab guides. Unique SKU and one compound catalog index are the must-keep artifacts in training_store.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Questions and Answers",
            """Open floor.

Parking-lot prompts if the room is quiet:

- Would you index `active` by itself?
- How would you prove a hidden index is safe to drop?
- When is a wildcard index the wrong answer?
- Why might `$lookup` still be slow with an index on `_id`?

Park replica-set lag and shard-key design for Module 7.""",
            "Do not start sharding. If they ask about building indexes in production, repeat the safety slide and move on.",
            fit="fit-sm",
        )
    )

    s.append(
        split_slide(
            "Day 3 Path — From Query Shape to Scale",
            [
                "Index the recurring shape",
                "Prove it with explain",
                "Watch write and storage cost",
                "Next: replica sets and sharding",
            ],
            "010-index-lifecycle.svg",
            "Path from indexing into Module 7",
            "Indexing tunes one node’s access path. Module 7 distributes data and roles.",
        )
    )

    s.append(
        content_slide(
            "Transition to Module 7: Replication and Sharding",
            """Module 7 moves from individual query performance to distributed availability and scale:

- Replica-set architecture
- Primary and secondary members
- Elections and automatic failover
- Read and write concerns
- Sharding architecture and shard keys
- Routers and configuration servers
- Balancing and data distribution
- Replication versus sharding
- High-availability and scaling decisions

Hashed indexes you saw today reappear as hashed shard keys.""",
            "Same training_store mental model. They do not need a sharded cluster on the laptop for Module 7 concepts.",
            fit="fit-sm",
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
        rest = text[start + len(MARKER) :]
        nxt = None
        for marker in NEXT_MARKERS:
            pos = rest.find(marker)
            if pos >= 0:
                nxt = rest[pos:]
                break
        suffix = ("\n\n---\n\n" + nxt.lstrip()) if nxt else ""
        DECK.write_text(prefix + "\n\n---\n\n" + fragment.strip() + suffix, encoding="utf-8")
        print(f"Replaced existing Module 6 in {DECK}")
        return
    insert_at = None
    for marker in NEXT_MARKERS:
        pos = text.find(marker)
        if pos >= 0:
            insert_at = pos
            break
    if insert_at is not None:
        prefix = text[:insert_at].rstrip()
        if prefix.endswith("---"):
            prefix = prefix[: -3].rstrip()
        DECK.write_text(
            prefix + "\n\n---\n\n" + fragment.strip() + "\n\n---\n\n" + text[insert_at:].lstrip(),
            encoding="utf-8",
        )
        print(f"Inserted Module 6 before the next module in {DECK}")
        return
    DECK.write_text(text.rstrip() + "\n\n---\n\n" + fragment.strip() + "\n", encoding="utf-8")
    print(f"Appended Module 6 to {DECK}")


if __name__ == "__main__":
    if not any(LAB_DIR.glob("exercise-6.1-*.md")):
        raise SystemExit("Lab guides missing. Run python scripts/module06_labs.py first.")
    fragment = build_slides()
    append_to_deck(fragment)
    print(f"Module 6 fragment length: {len(fragment):,} chars")
