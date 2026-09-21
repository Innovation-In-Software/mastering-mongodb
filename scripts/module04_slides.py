"""Emit Module 4 Marp slides and append them to the course deck.

Run after lab guides exist:

    python scripts/module04_labs.py
    python scripts/module04_slides.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from course_config import deck_md
from module04_labs import OUT as LAB_DIR

DECK = deck_md()
MARKER = "<!-- _header: 'Module 4 — The MongoDB Query Language' -->"


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

<img src="assets/module-04/{img}" alt="{alt}" width="720">

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


def lead_slide(title: str, subtitle: str, script: str) -> str:
    return f"""<!-- _class: lead -->

# {title}

{subtitle}

{notes(title, script)}
"""


def parse_steps(num: int) -> list[tuple[str, str, str]]:
    matches = sorted(LAB_DIR.glob(f"exercise-4.{num}-*.md"))
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


def exercise_block(num: int, title: str, time: str, objective: str, img: str, alt: str, script: str) -> list[str]:
    lab = next(LAB_DIR.glob(f"exercise-4.{num}-*.md"))
    rel = lab.as_posix().split("slide-exercises/")[-1]
    intro = split_slide(
        f"Exercise 4.{num} — {title}",
        [
            f"**Time:** {time}",
            objective,
            f"**Lab guide:** [`Exercise 4.{num}`](../slide-exercises/{rel})",
        ],
        img,
        alt,
        script,
        fit="fit-md",
    )
    # Heading must be `#` for intro; inject script looks for `## Exercise N.N —`
    # Keep a `##` steps slide as the first matching slide.
    slides = [intro]
    steps = parse_steps(num)
    for i in range(0, len(steps), 2):
        pair = steps[i : i + 2]
        if len(pair) == 2:
            heading = f"## Exercise 4.{num} — Steps {i + 1}–{i + 2}"
        else:
            heading = f"## Exercise 4.{num} — Step {i + 1}"
        lines = [
            "<!-- _class: fit-md -->",
            "",
            heading,
            "",
        ]
        if i == 0:
            lines.extend(
                [
                    f"**Lab guide:** [`Exercise 4.{num}`](../slide-exercises/{rel})",
                    "",
                ]
            )
        lines.extend(["**Follow along (Windows) — key steps:**", ""])
        for n, (st, do, exp) in enumerate(pair, start=i + 1):
            do_clean = do.replace("```javascript", "`").replace("```", "`").strip()
            lines += [
                f"**Step {n} — {st}**",
                f"- **Do:** {do_clean}",
                f"- **Expected:** {exp}",
                "",
            ]
        lines.append(
            notes(
                heading[3:],
                f"Time-box this pair of steps. Open the lab guide for full commands.\nInstructor script: {script[:180]}",
            )
        )
        slides.append("\n".join(lines))
    return slides


def demo_slide(n: str, title: str, body: str, script: str, img: str | None = None) -> str:
    if img:
        return split_slide(
            f"Demo 4.{n} — {title}",
            body if isinstance(body, list) else [body],
            img,
            title,
            script,
            fit="fit-md",
        )
    return content_slide(f"Demo 4.{n} — {title}", body, script, fit="fit-sm")


def build_slides() -> str:
    s: list[str] = []

    s.append(f"""{MARKER}

<!-- _class: lead -->

# The MongoDB Query Language

Document-shaped filters and updates — create, read, update, replace, delete

{notes("The MongoDB Query Language", '''Open Day 2 on the same training_store dataset from Day 1. Today is not theory: every operator is a command they will type.

MongoDB operations use documents as filters and as update descriptions. The skill is precision — which documents, which fields, which array element — and verification after every write.

Ask who has written SQL WHERE clauses. Map SELECT to find, SET to $set, JOIN pain to embedding they already modeled.
''')}
""")

    s.append(
        content_slide(
            "Module Learning Objectives",
            """By the end of this module you will be able to:

- Write accurate query filters
- Retrieve required fields with projections
- Work with nested values and arrays
- Insert valid documents and verify writes
- Update scalar, nested, and array fields
- Replace or upsert documents
- Delete test records safely
- Interpret write-operation results""",
            "Read the outcomes. The through-line is: filter, operate, verify. Unsafe empty filters are a safety topic, not an afterthought.",
        )
    )

    s.append(
        split_slide(
            "MongoDB CRUD Operations",
            [
                "**Create** `insertOne()` · `insertMany()`",
                "**Read** `findOne()` · `find()`",
                "**Update** `updateOne()` · `updateMany()`",
                "**Replace** `replaceOne()`",
                "**Delete** `deleteOne()` · `deleteMany()`",
                "Always verify the result",
            ],
            "001-crud-operations-overview.svg",
            "CRUD operations and common methods",
            "Stay on methods they will type in mongosh. replaceOne is not updateOne. Bulk write comes later as a grouping of these same operations.",
        )
    )

    s.append(
        split_slide(
            "The Sample Application Dataset",
            [
                "`training_store` collections:",
                "`products` · `customers` · `orders` · `reviews`",
                "Products: SKU, category, Decimal128 price, tags",
                "Customers: nested name, contact, addresses",
                "Orders: items[], status, totals",
                "Reload `load.js` before labs if data drifted",
            ],
            "005-training-dataset.svg",
            "Four training_store collections",
            "If Module 3 populate lab was skipped, load datasets/training_store/load.js now. Point at Decimal128 prices and the planted XBAD string price.",
        )
    )

    s.append(
        split_slide(
            "CRUD Flow",
            [
                "Start from a business requirement",
                "Name the collection and the filter",
                "Choose the CRUD method",
                "Read matchedCount / insertedId / deletedCount",
                "Query again to confirm",
            ],
            "003-business-requirement-to-query.svg",
            "Requirement to filter to operation to verification",
            "This flow is the safety culture for the rest of the day. Preview filters with find() before updateMany or deleteMany.",
        )
    )

    s.append(
        split_slide(
            "MongoDB Query Anatomy",
            [
                "`db` — current database",
                "`products` — collection",
                "`find()` — operation",
                "First document — **filter**",
                "Second document — **projection**",
                "General: `db.collection.method(filter, options)`",
            ],
            "002-query-anatomy.svg",
            "Anatomy of a find call",
            "Type the example. Quote dotted paths later. Empty filter is legal and dangerous on writes.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Understanding Query Filters",
            [
                "`{}` matches **every** document",
                '`{ category: "LAPTOP" }` is equality',
                "Two fields → **implicit AND**",
                "Empty filters are legal on `find`",
                "Empty filters are disastrous on `deleteMany`",
            ],
            "008-empty-vs-targeted-filter.svg",
            "Empty filter versus a targeted category filter",
            "Empty filter on find is a scan. Empty filter on deleteMany is a disaster. Implicit AND is the default — they do not need $and for two different fields.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "`findOne()` vs `find()`",
            [
                "`findOne()` returns one document or `null`",
                "`find()` returns a **cursor** of 0..n documents",
                "Use `findOne` when one result is expected",
                "Use `find` when you may have many — then sort/limit",
            ],
            "007-findone-vs-find.svg",
            "findOne returns one document; find returns a cursor",
            "findOne does not take skip in the same casual way as a cursor chain. For 'the cheapest laptop' they will sort+limit on find, not findOne with a hope.",
        )
    )

    s.append(
        split_slide(
            "Retrieving All Documents",
            [
                "`db.products.find({})` matches every document",
                "`mongosh` prints from the cursor",
                "Fine on the training catalog",
                "On large collections: filter, project, and limit",
                "Empty `find` is a scan, not a dump strategy",
            ],
            "012-query-result-set.svg",
            "Entire collection reduced to a matching subset",
            "On 16 training products this is fine. Say out loud: this is not how you dump a million-document catalog.",
        )
    )

    s.append(
        split_slide(
            "Equality Filters",
            [
                '`{ active: true }` is one-field equality',
                '`{ category: "BOOK", active: true }` is implicit AND',
                "Field names are case-sensitive",
                "String values are case-sensitive",
                '`{ Category: "laptop" }` matches nothing here',
            ],
            "009-equality-filter.svg",
            "Product documents passing a category equality filter",
            "Live-demo a wrong-case filter and show zero documents. That failure mode returns all day.",
        )
    )

    s.append(
        split_slide(
            "Querying Nested Fields",
            [
                "Use **dot notation**",
                '`"attributes.memoryGB": 16`',
                '`"contact.email": "aisha@example.com"`',
                '`"addresses.city": "Toronto"`',
                "Always quote dotted field paths",
            ],
            "011-nested-field-dot-notation.svg",
            "Dot notation into a nested attributes object",
            "Unquoted attributes.memoryGB is a syntax error. addresses.city matches if ANY address has that city — $elemMatch later when type+city must be the same element.",
        )
    )

    s.append(demo_slide(
        "1",
        "Explore the Training Dataset",
        """**Duration:** 10 minutes

```javascript
use training_store
show collections
db.products.findOne()
db.customers.findOne()
db.orders.findOne()
db.reviews.findOne()
```

Identify field names, nesting, arrays, and BSON types **before** writing filters.""",
        "Instructor types this. Ask the room to shout field paths. Point at Decimal128 on price, Date on createdAt, and XBAD if you findOne the wrong product — better: find the string price with $type later.",
    ))

    s.extend(exercise_block(
        15,
        "Lab 4.1 Dataset Verification",
        "15 min",
        "Confirm collections, counts, field paths, and BSON types before querying.",
        "152-lab-4-1-dataset-verification.svg",
        "Four training_store collections",
        "Do this immediately after Demo 4.1 so everyone has seen the same documents. Record Decimal128 vs the XBAD string price.",
    ))

    s.append(
        split_slide(
            "Comparison Operators",
            [
                "`$eq` `$ne` equal / not equal",
                "`$gt` `$gte` greater / or equal",
                "`$lt` `$lte` less / or equal",
                "Put operators **inside** the field",
                "Money: `Decimal128(\"50.00\")`",
            ],
            "014-comparison-operators-overview.svg",
            "Comparison operator table",
            "Wrong: { $gt: { price: 100 } }. Right: { price: { $gt: Decimal128(...) } }. String '100.00' will not compare as they expect against Decimal128.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "The `$in` and `$nin` Operators",
            [
                "`$in` — field matches **any** listed value",
                '`category: { $in: ["BOOK", "ACCESSORY"] }`',
                "`$nin` — field matches **none** of the list",
                "`$in` is cleaner than `$or` on one field",
                "One accepted value vs several accepted values",
            ],
            "017-in-operator.svg",
            "One field matching any value from a permitted list",
            "If they write $or of two category equalities, show $in as the rewrite. $nin of an empty array matches everything — do not dwell unless asked.",
        )
    )

    s.append(
        split_slide(
            "Logical Operators",
            [
                "`$and` — all expressions match",
                "`$or` — at least one matches",
                "`$nor` — none may match",
                "`$not` — negate a field-level condition",
                "Prefer implicit AND when fields differ",
            ],
            "021-logical-operators-overview.svg",
            "Logical operator meanings",
            "$not is easy to misuse with missing fields. Preview $nor with a small example on the board.",
        )
    )

    s.append(
        split_slide(
            "Combining Query Conditions",
            [
                "Implicit AND: two fields in one document",
                "Explicit `$and`: same field, two tests",
                "Nest `$or` inside an AND document",
                "Read the filter out loud as English",
            ],
            "026-combined-logical-query.svg",
            "Implicit AND, explicit AND, nested OR",
            "Explicit $and is required when you cannot put two operators on one key in the same JSON object... actually you CAN put $gte and $lte on the same price key. $and is needed when the same field key would collide, e.g. two $or groups. Keep it practical: price range is one object; category OR tag is $or.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "The `$not` and `$nor` Operators",
            [
                "`$not` negates a **field-level** condition",
                "`$nor` rejects documents matching **any** listed condition",
                "Negation can also match **missing** fields",
                "Preview `$not` / `$nor` before using them in writes",
                "Prefer `$ne` or `$nin` when the intent is simpler",
            ],
            "024-nor-operator.svg",
            "Documents rejected if they match any prohibited condition",
            "This is the slide to slow down. Run a $not example and findOne a document that has no price if you can; otherwise remind them missing-field matching is why $exists exists.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Field Existence, BSON Type, Null",
            [
                "`$exists: true/false` — field present?",
                '`$type: "decimal"` vs `"string"`',
                "`{ phone: null }` matches null **or missing**",
                '`$type: "null"` — explicitly null',
                "`$exists: false` — field absent",
            ],
            "030-null-vs-missing.svg",
            "Null query versus type null versus missing field",
            "C204 has phone: null. C515 has no phone field. Live this trio. XBAD is the string price.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Regular-Expression Queries",
            [
                'Prefix: `{ $regex: "^Mongo", $options: "i" }`',
                "Regex can be expensive",
                "Anchored (`^`) is more index-friendly",
                "Unanchored search scans the field",
                "Atlas Search is better for real full-text",
            ],
            "035-prefix-search.svg",
            "Anchored prefix search matching names that start with Mongo",
            "Do not turn this into a regex workshop. One anchored example. Module 6 will talk indexes; unanchored /mongo/i is a collection scan.",
            fit="fit-md",
        )
    )

    s.append(demo_slide(
        "2",
        "Build Queries Incrementally",
        [
            "**Duration:** 15 minutes",
            "Start with `{}`, then add **one** condition at a time",
            '`find({ category: "ACCESSORY" })`',
            "Then add `active: true`",
            "Then `price: { $lte: Decimal128(\"100.00\") }`",
            "Count after each step",
        ],
        "Type these live. Count after each step. This is the troubleshooting habit: simple equality first, then tighten.",
        img="136-query-building-workflow.svg",
    ))

    s.extend(exercise_block(
        1,
        "Read Basic Documents",
        "10 min",
        "Retrieve all products, one SKU, active products, ACTIVE customers, and one order.",
        "138-ex-4-1-basic-query-builder.svg",
        "Five starter find tasks",
        "Ten minutes. Pair work. Circulate for case-sensitivity mistakes.",
    ))
    s.extend(exercise_block(
        2,
        "Build Comparison Filters",
        "15 min",
        "Use $gt, ranges, $nin, and Decimal128. Notice why XBAD misses numeric comparisons.",
        "139-ex-4-2-comparison-number-line.svg",
        "Comparison-operator number line",
        "If anyone uses JS numbers for price, show zero or weird matches. Decimal128 is non-negotiable for money.",
    ))
    s.extend(exercise_block(
        3,
        "Combine Logical Conditions",
        "15 min",
        "Implicit AND, $or / $in, and $nor on products and orders.",
        "140-ex-4-3-logical-query-builder.svg",
        "Logical query builder",
        "Prefer $in when one field has several allowed values.",
    ))
    s.extend(exercise_block(
        4,
        "Query Missing and Null Fields",
        "10 min",
        "Separate exists, BSON null, missing fields, and wrong types.",
        "141-ex-4-4-null-or-missing.svg",
        "Value, null, or missing field",
        "Do not let them leave thinking { phone: null } means 'explicitly null only'.",
    ))

    s.append(
        split_slide(
            "Querying Arrays",
            [
                '`tags: "technology"` — **contains** that element',
                "Does **not** require matching the whole array",
                "Exact array: values **and** order **and** length",
                "`$all` — contains all values, any order",
                "`$size` — exact length only, not a range",
            ],
            "038-array-query-fundamentals.svg",
            "Array containment versus exact match versus all versus size",
            "Live: tags: ['database','technology'] vs $all. Exact match fails if a third tag exists (L100 has three).",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Exact Array Matching vs `$all` vs `$size`",
            [
                "Exact match: values **and** order **and** length",
                "`$all` — contains all values, any order, extras allowed",
                "`$size` — exact element count only",
                "L100 has three tags — exact two-element match fails",
                "`$size` cannot express “at least two”",
            ],
            "041-all-operator.svg",
            "Array required to contain all specified values regardless of order",
            "L100 has three tags so exact two-element match fails and $all succeeds. $size cannot say 'at least two' — that pattern is tags.0 $exists or aggregation later.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "The `$elemMatch` Operator",
            [
                "Use when **two conditions** must hit the **same** array element",
                "Without it, `items.sku` and `items.quantity` can match **different** lines",
                "Teaching trap: **O5001** has L100 qty 1 and A200 qty 2",
                "Only **O6401** has L100 qty 2",
            ],
            "045-why-elemmatch.svg",
            "elemMatch versus matching different array elements",
            "This is the most important read-path slide in the module. Run both queries live. Pause until they see O5001 in the wrong result.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Querying Arrays of Documents",
            [
                '`"items.sku": "L100"` — any line item with that SKU',
                "`$elemMatch` when two conditions must hit **one** element",
                "O5001 has L100 qty 1 and A410 qty 2 — the trap",
                "Only O6401 has L100 qty 2 on the **same** line",
                "Dot notation is enough for “contains this product”",
            ],
            "044-querying-field-inside-array.svg",
            "Dot notation navigating from items to sku",
            "items.sku is enough for 'orders that contain this product'. $elemMatch is for compound conditions on one line item.",
            fit="fit-md",
        )
    )

    s.append(demo_slide(
        "3",
        "Query Nested Documents and Arrays",
        """**Duration:** 15 minutes

```javascript
db.products.find({ "attributes.memoryGB": { $gte: 16 } })
db.customers.find({ "addresses.city": "Toronto" })
db.orders.find({
  items: { $elemMatch: { sku: "L100", quantity: { $gte: 1 } } }
})
```

Then contrast the **without** `$elemMatch` form on O5001.""",
        "Three live queries. End on the O5001 trap even if quantity >= 1 matches both — switch to >= 2 to make the trap visible.",
    ))

    s.extend(exercise_block(5, "Query Arrays", "15 min", "Containment, $all, $size, availableSizes, and excluding a tag.", "142-ex-4-5-array-query-challenge.svg", "Array query forms", "Watch for exact-array matches copied from $all examples."))
    s.extend(exercise_block(6, "Query Arrays of Documents", "15 min", "Prove the O5001 $elemMatch trap, then query Toronto shipping addresses.", "143-ex-4-6-elemmatch-challenge.svg", "elemMatch", "If they skip the 'without $elemMatch' step, they will not feel the bug."))

    s.append(
        split_slide(
            "Projection Fundamentals",
            [
                "Projection controls **which fields** return",
                "Inclusion: `{ name: 1, price: 1 }`",
                "Exclusion: `{ attributes: 0, tags: 0 }`",
                "Do **not** mix inclusion and exclusion",
                "Exception: `_id` may be excluded from an inclusion",
            ],
            "048-filter-vs-projection.svg",
            "Inclusion versus exclusion projections",
            "Live the mixed projection error. Network and clarity are the motivations — not 'hiding secrets'.",
        )
    )

    s.append(
        split_slide(
            "Inclusion, Exclusion, Nested, and Array Projection",
            [
                "Inclusion: `{ name: 1, price: 1, _id: 0 }`",
                "Nested: `{ \"name.first\": 1, \"contact.email\": 1 }`",
                "Array `$elemMatch` in projection returns **one** matching element",
                "`$slice` returns first or most recent elements",
                "Projection `$elemMatch` is not the same as the filter form",
            ],
            "049-inclusion-projection.svg",
            "Complete document reduced to selected fields",
            "$elemMatch in projection is not the same as in the filter — it shapes the returned array. $slice is positional, not a query.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Cursor Fundamentals",
            [
                "`find()` returns a cursor, not an array",
                "Chain `.sort()` `.limit()` `.skip()`",
                "Iterate; do not always `.toArray()` a huge result",
                "Conceptual order: filter → project → sort → limit",
            ],
            "057-filter-sort-limit.svg",
            "find then sort then skip/limit then iterate",
            "They do not need executor internals. They do need: always sort if you skip, and limit in development.",
        )
    )

    s.append(
        split_slide(
            "Sorting, Limiting, Skipping, Pagination",
            [
                "`.sort({ category: 1, price: -1, _id: 1 })` — tiebreaker",
                "`.limit(5)` then `.skip(5).limit(5)` for page 2",
                "`skip()` is fine for shallow pages",
                "Deep skip is expensive — range on last-seen value instead",
                "Always sort if you paginate",
            ],
            "062-skip-limit-pagination.svg",
            "Sorted results divided into pages using offset and page size",
            "Add _id as tiebreaker whenever 'page 1 vs page 2' must be stable. Deep skip is a Module 6 performance teaser, not a rabbit hole.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Counting and Distinct Values",
            [
                "`countDocuments(filter)` — accurate filtered count",
                "`estimatedDocumentCount()` — fast estimate",
                '`distinct("category")` — unique values',
                "Prefer `countDocuments` over legacy `count()`",
            ],
            "065-count-operations.svg",
            "countDocuments versus estimated versus distinct",
            "estimatedDocumentCount ignores the filter. distinct can be heavy; fine on training_store.",
        )
    )

    s.append(demo_slide(
        "4",
        "Use Projections and Cursor Methods",
        """**Duration:** 15 minutes

```javascript
db.products
  .find({ active: true }, { name: 1, category: 1, price: 1, _id: 0 })
  .sort({ price: -1 })
  .limit(5)
```

Discuss execution conceptually: **filter, shape, sort, limit**.""",
        "Type it as a chain. Ask what happens if they omit sort: 'five active products' is not 'five most expensive'.",
    ))

    s.extend(exercise_block(7, "Design Projections", "10 min", "Inclusion, nested paths, exclusion, and projecting one matching item.", "144-ex-4-7-projection-designer.svg", "Projection", "Catch mixed inclusion/exclusion immediately."))
    s.extend(exercise_block(8, "Sort and Paginate Results", "15 min", "Sort, top-N, two pages of five, countDocuments, distinct.", "145-ex-4-8-pagination-planner.svg", "Pagination pages", "Require the _id tiebreaker on the expensive-products query."))

    s.append(
        split_slide(
            "Inserting Documents",
            [
                "`insertOne(document)`",
                "`insertMany([ ... ])`",
                "Result: `acknowledged`, `insertedId(s)`",
                "Then `findOne` by SKU — always",
                "Keep money as Decimal128, dates as Date",
            ],
            "067-insertone-flow.svg",
            "New document validated, assigned _id, stored, and acknowledged",
            "Unique index on sku will reject a duplicate insert. Seed already has A400 and A500 — labs use A620 / A700.",
        )
    )

    s.append(
        split_slide(
            "Insert One and Many",
            [
                "`insertOne` — one document, one `insertedId`",
                "`insertMany` — one request, several documents",
                "Keep money as Decimal128 and dates as Date",
                "Reserved lab SKUs: `A620`, `A610`–`A612`, `A700`, `A800`, `TEMP-*`",
                "Always `findOne` by SKU after insert",
            ],
            "073-single-vs-batch-insert.svg",
            "One operation per document compared with one request containing several",
            "Do not invent JS numbers for price. Show the insert result document before findOne.",
            fit="fit-md",
        )
    )

    s.append(demo_slide(
        "5",
        "Insert and Verify Documents",
        [
            "**Duration:** 10 minutes",
            "Insert one product with demo SKU `DEMO-1`",
            "Inspect `acknowledged` and `insertedId`",
            "`findOne({ sku: \"DEMO-1\" })` to verify",
            "Keep price as Decimal128, dates as Date",
        ],
        "Use DEMO-1, not A400/A500 — those SKUs are already in load.js.",
        img="071-insert-and-verify.svg",
    ))

    s.extend(exercise_block(9, "Insert New Application Data", "15 min", "insertOne, insertMany, a customer, an order; verify types.", "146-ex-4-9-insert-workflow.svg", "Insert and verify", "Watch for duplicate key errors; reload if needed."))

    s.append(
        split_slide(
            "Updating Documents",
            [
                "`updateOne` — first match only",
                "`updateMany` — every match; **preview first**",
                "`$set` changes listed fields only",
                "`$unset` removes a field",
                "`$inc` `$mul` `$min` `$max` `$rename`",
            ],
            "074-update-anatomy.svg",
            "Update operator table",
            "matchedCount 1 and modifiedCount 0 means already that value — not a failed update. Live that by setting featured true twice.",
            fit="fit-md",
        )
    )

    s.append(
        content_slide(
            "`$set`, `$unset`, Numeric Operators, `$rename`",
            """```javascript
{ $set: { featured: true, "attributes.warrantyYears": 2 } }
{ $unset: { temporaryNote: "" } }
{ $inc: { stockQuantity: 5 } }
{ $mul: { price: 1.05 } }   // beware Decimal128 vs double
{ $min: { lowestPrice: Decimal128("45.00") } }
{ $rename: { productName: "name" } }
```

Use consistent numeric types. Prefer `$inc` on integers. Be careful multiplying money.""",
            "$unset value is ignored. $rename breaks app code still using the old name — POLD is the fixture. Skip a long $mul rabbit hole on Decimal128.",
            fit="fit-xs",
        )
    )

    s.append(
        split_slide(
            "Updating Nested Fields",
            [
                '`$set: { "contact.email": "new@..." }` — targeted',
                "`$set: { contact: { email: ... } }` — **replaces** the object",
                "Sibling fields such as `phone` disappear",
                "Dot notation is the default safe habit",
            ],
            "084-targeted-vs-object-replacement.svg",
            "Targeted nested set versus replacing the whole object",
            "This is the write-path twin of the $elemMatch slide. Exercise 4.13 will force them to rewrite it.",
        )
    )

    s.append(demo_slide(
        "6",
        "Update Scalar and Nested Fields",
        [
            "**Duration:** 15 minutes",
            "On **L100** or a demo copy: price, `active`, warranty, `updatedAt`",
            "Show **before** and **after** `findOne`",
            "Read `matchedCount` and `modifiedCount`",
            "Reload before Lab 4.10 if you mutate L100",
        ],
        "Prefer a copied SKU if you do not want to disturb L100 for later array labs. Otherwise reload before Lab 4.10.",
        img="085-update-and-verify.svg",
    ))

    s.extend(exercise_block(10, "Update Product Data", "15 min", "$set price, nested warranty, $inc stock, $rename, $unset, filtered updateMany.", "147-ex-4-10-update-operator-selection.svg", "Update operators", "Insist on find() before updateMany."))

    s.append(
        split_slide(
            "Array Update Operators",
            [
                "`$push` — add; **may duplicate**",
                "`$addToSet` — add if absent",
                "`$pull` / `$pullAll` — remove by match / values",
                "`$pop` — first (`-1`) or last (`1`)",
                "Modifiers: `$each` `$position` `$sort` `$slice`",
            ],
            "089-array-update-operators.svg",
            "Array update operators",
            "Push twice in the demo. Then addToSet twice. The modifiedCount 0 on the second addToSet is the lesson.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "`$push` Modifiers",
            [
                "`$each` — several values",
                "`$position` — insert index",
                "`$sort` — order the array",
                "`$slice` — bound length (recent events)",
            ],
            "093-push-sort-slice.svg",
            "Push modifiers each position sort slice",
            "The bounded recent-events pattern is the real-world reason for $position 0 + $slice. One example is enough.",
        )
    )

    s.append(
        split_slide(
            "Positional Array Updates",
            [
                "`items.$` — first **matched** element (query must identify it)",
                "`items.$[]` — **all** elements",
                "`items.$[item]` — filtered elements",
                "Requires `arrayFilters` for the identifier",
            ],
            "099-positional-dollar.svg",
            "Positional dollar, all, and filtered positional",
            "Classic $ needs the array field in the filter. $[] is blunt. arrayFilters is the precise tool — Demo 4.7.",
            fit="fit-md",
        )
    )

    s.append(demo_slide(
        "7",
        "Modify Array Fields",
        [
            "**Duration:** 15 minutes",
            "On a throwaway product and on **O5001**",
            "`$push` vs `$addToSet`, then `$pull`",
            "Positional `$`, `$[]`, and `arrayFilters`",
            "Filter: `unitPrice >= 100`",
            "Reload afterwards if later labs need a clean O5001",
        ],
        "Narrate which array element changes. Project items only so the room can see it.",
        img="102-array-filter-execution.svg",
    ))

    s.extend(exercise_block(11, "Modify Arrays", "15 min", "$push, $addToSet, $each, $pull, positional $, and $[].", "148-ex-4-11-array-operator-selection.svg", "Array updates", "Second $push is supposed to duplicate. Do not 'fix' it for them."))

    s.append(
        split_slide(
            "Replace vs `$set` vs Upsert",
            [
                "`$set` keeps fields you did not mention",
                "`replaceOne` **drops** omitted fields (keeps `_id`)",
                "`upsert: true` updates or **inserts**",
                "`$setOnInsert` for fields only on insert",
                "Unique filter (`sku`) prevents duplicate upserts",
            ],
            "103-field-update-vs-replacement.svg",
            "set versus replaceOne versus upsert",
            "Live replaceOne on a copy with a notes field. Gasps when notes vanish. Upsert without unique filter is how you get duplicates.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Upsert Pattern",
            [
                "Match found? Update the existing document",
                "No match? Insert a new document",
                "`$set` runs on **every** execution",
                "`$setOnInsert` runs **only** on insert (`createdAt`)",
                "Filter on unique `sku` so the second run updates",
            ],
            "106-upsert-decision-flow.svg",
            "Match found updates; no match inserts",
            "This is Exercise 4.12. If they put createdAt in $set, the second run overwrites it — that is a useful wrong answer.",
            fit="fit-md",
        )
    )

    s.append(demo_slide(
        "8",
        "Replace and Upsert Documents",
        [
            "**Duration:** 15 minutes",
            "`$set` on selected fields — unspecified fields remain",
            "`replaceOne()` of the same test document — omitted fields vanish",
            "`updateOne(..., { upsert: true })` twice",
            "Use `TEMP-200` or `DEMO-REP` — never replace L100",
        ],
        "Use TEMP-200 or DEMO-REP. Never replace L100 in the demo.",
        img="109-first-vs-second-upsert.svg",
    ))

    s.extend(exercise_block(12, "Perform an Upsert", "10 min", "Match by SKU; createdAt only on insert; updatedAt always; run twice.", "149-ex-4-12-upsert-lifecycle.svg", "Replace and upsert", "Compare write results on the projector after both runs."))

    s.append(
        split_slide(
            "Deleting Documents Safely",
            [
                "`deleteOne` with a unique identifier",
                "`deleteMany` only after find + count + review",
                "`deleteMany({})` removes **all** documents",
                "Inspect `deletedCount`, then query again",
                "Consider **soft delete**: `active: false`, `deletedAt`",
            ],
            "112-safe-delete-workflow.svg",
            "Preview count delete verify sequence",
            "The safety sequence is non-negotiable. Soft delete is how catalogs usually 'remove' products.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Soft Delete vs Hard Delete",
            [
                "Hard: document is gone",
                "Soft: still queryable for audit",
                "Application reads add `{ active: true }`",
                "Never begin with an empty filter",
            ],
            "114-hard-vs-soft-delete.svg",
            "Hard delete versus soft delete",
            "Lab 4.10 ends on a soft delete. Lab 4.9 is hard delete of TEMP- records only.",
        )
    )

    s.append(demo_slide(
        "9",
        "Delete Documents Safely",
        """**Duration:** 10 minutes

```javascript
const filter = { sku: "TEMP-100" }
db.products.find(filter)
db.products.countDocuments(filter)
db.products.deleteOne(filter)
```

Insert TEMP-100 first if needed. Verify it is gone and L100 remains.""",
        "Const filter reused three times is the habit. If they retype {}, they will someday type it on deleteMany.",
    ))

    s.extend(exercise_block(13, "Correct Unsafe Operations", "10 min", "Rewrite empty updateMany, empty deleteMany, and nested-object replacement. Do not run the unsafe commands.", "150-ex-4-13-find-the-unsafe-operation.svg", "Safe practices", "Discussion. Do not let anyone paste deleteMany({}) 'to see what happens' on a shared Atlas cluster."))

    s.append(
        split_slide(
            "Bulk Write Operations",
            [
                "`bulkWrite([ insertOne, updateOne, deleteOne, ... ])`",
                "Fewer application round trips",
                "Group related operations",
                "Still inspect the returned counts",
            ],
            "117-bulk-write-overview.svg",
            "insert update and delete in one bulkWrite",
            "They do not need ordered vs unordered depth unless asked. Default ordered stops on first error.",
        )
    )

    s.append(
        content_slide(
            "Bulk Write Example",
            """```javascript
db.products.bulkWrite([
  { insertOne: { document: { sku: "A600", name: "Wireless Presenter", category: "ACCESSORY", price: Decimal128("44.99"), active: true } } },
  { updateOne: { filter: { sku: "A400" }, update: { $set: { featured: true } } } },
  { deleteOne: { filter: { sku: "OLD-100" } } }
])
```

A400 already exists in the seed catalog. OLD-100 may match 0 documents — that is OK.""",
            "Read insertedCount, matchedCount, deletedCount from the result. delete of missing filter is not an exception.",
            fit="fit-xs",
        )
    )

    s.append(demo_slide(
        "10",
        "Perform a Bulk Write",
        [
            "**Duration:** 10 minutes",
            "One insert, one update, one delete through `bulkWrite()`",
            "Interpret inserted, matched, modified, and deleted counts",
            "Use `DEMO-BULK` if `A600` is reserved for Lab 4.5",
            "`deletedCount: 0` is a normal outcome",
        ],
        "If A600 is reserved, use DEMO-BULK. Show a 0 deletedCount as a normal outcome.",
        img="118-bulk-write-request-flow.svg",
    ))

    s.append(
        split_slide(
            "Understanding Write Results",
            [
                "Update: `acknowledged` `matchedCount` `modifiedCount` `upsertedId`",
                "Delete: `acknowledged` `deletedCount`",
                "`matchedCount: 1`, `modifiedCount: 0` — already that value",
                "`matchedCount: 0` — filter missed (types, case, db)",
            ],
            "087-update-result-anatomy.svg",
            "How to read write results",
            "This is the literacy test. Cold-call: what does modifiedCount 0 mean if matchedCount is 1?",
        )
    )

    s.append(
        split_slide(
            "Atomicity and Concurrency",
            [
                "A write to **one document** is atomic",
                "Embed data that must change together",
                "Example: order status + total + line items",
                "Multi-document work may need transactions",
                "Transactions are a later, advanced topic",
            ],
            "122-single-document-atomicity.svg",
            "Single document atomic versus multi-document",
            "Tie back to Module 3 embedding. Do not teach session.startTransaction() today unless asked — name that it exists.",
        )
    )

    s.append(
        split_slide(
            "Safe Update and Delete Practices",
            [
                "Precise filters; unique ids when possible",
                "`find()` the filter before mass writes",
                "Correct BSON types; dotted nested paths",
                "Never start deletes with `{}`",
                "Soft delete + audit when policy requires",
                "Back up before true mass updates",
            ],
            "128-safe-update-workflow.svg",
            "Safe update and delete rules",
            "This is a checklist slide. Leave it up during Exercise 4.13 debrief.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Common Query Mistakes",
            [
                "Misspelled or wrong-case field names",
                "String dates / string money",
                "Unquoted dotted paths",
                "`$push` when uniqueness is required",
                "Omitting `$elemMatch`",
                "Mixed projections; broad write filters",
            ],
            "131-common-query-mistakes.svg",
            "Common query mistakes and symptoms",
            "Each row is a 10-second story from this morning. Exercise 4.14 is this table as broken commands.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Query Troubleshooting Workflow",
            [
                "Confirm database and collection",
                "Inspect one sample document",
                "Check names, nesting, BSON types",
                "Start simple; add one condition",
                "Write, read the result, query again",
            ],
            "130-troubleshooting-layers.svg",
            "Twelve-step troubleshooting condensed",
            "Walk it once against a 'failing' query you plant (Category vs category).",
        )
    )

    s.extend(exercise_block(14, "Diagnose Query Errors", "15 min", "Fix seven broken queries: case, types, dots, operators, projection, elemMatch, missing $set.", "151-ex-4-14-query-error-diagnosis.svg", "Common mistakes", "Reveal answers after attempts. The missing $set update is a modern mongosh error — good."))

    # Labs 4.1–4.10 = exercises 15–24
    lab_meta = [
        (16, "Lab 4.2 Product Query Lab", "30 min", "Ten product queries from equality through distinct.", "153-lab-4-2-product-query.svg"),
        (17, "Lab 4.3 Customer and Order Query Lab", "30 min", "Nested customer fields, $elemMatch, dates, totals.", "154-lab-4-3-customer-order-paths.svg"),
        (18, "Lab 4.4 Projection and Pagination Lab", "20 min", "Summaries, sort, two pages, count.", "155-lab-4-4-projection-pagination.svg"),
        (19, "Lab 4.5 Insert Operations Lab", "25 min", "Insert product, customer, order; fix types.", "156-lab-4-5-insert-operations.svg"),
        (20, "Lab 4.6 Update Operations Lab", "30 min", "Preview–update–result–verify for each operator.", "157-lab-4-6-update-operations.svg"),
        (21, "Lab 4.7 Array Manipulation Lab", "30 min", "Tags plus positional and arrayFilters on orders.", "158-lab-4-7-array-manipulation.svg"),
        (22, "Lab 4.8 Replace and Upsert Lab", "20 min", "Copy, $set, replaceOne, upsert twice.", "159-lab-4-8-replace-upsert.svg"),
        (23, "Lab 4.9 Delete Operations Lab", "20 min", "TEMP- records only. Preview, count, delete, verify.", "160-lab-4-9-safe-deletion.svg"),
        (24, "Lab 4.10 Integrated CRUD Challenge", "45 min", "New product, customer, order, status, soft-delete.", "161-lab-4-10-integrated-crud.svg"),
    ]
    for num, title, time, obj, img in lab_meta:
        s.extend(exercise_block(num, title, time, obj, img, title, f"Hands-on {time}. Full commands in the lab guide. Circulate. {obj}"))

    s.append(
        split_slide(
            "Module Summary",
            [
                "Filters choose documents; projections choose fields",
                "Dot notation for nested fields",
                "`$elemMatch` for one array element",
                "Update operators ≠ `replaceOne`",
                "Upsert may insert; unique filter required",
                "Verify every write",
            ],
            "001-crud-operations-overview.svg",
            "Module 4 concept map",
            "Stay here while they start the knowledge check if you are short on time.",
            fit="fit-md",
        )
    )

    s.append(
        content_slide(
            "Module Knowledge Check",
            """1. `findOne()` vs `find()`?
2. What does `{}` match?
3. How do you query a nested field?
4. When is `$elemMatch` required?
5. Inclusion/exclusion projection rule?
6. `$push` vs `$addToSet`?
7. `updateOne()` vs `replaceOne()`?
8. What does `upsert: true` do?
9. `matchedCount: 1`, `modifiedCount: 0`?
10. Why preview a delete filter?
11. What does `deleteMany({})` do?
12. Why prefer `countDocuments()`?""",
            "Cold-call or paper. Answers: (1) one doc vs cursor (2) all docs (3) dotted path (4) two conditions on same array element (5) do not mix except _id (6) duplicates vs unique (7) operators vs full replace (8) update or insert (9) already that value (10) blast radius (11) deletes every document (12) accurate filtered count.",
            fit="fit-xs",
        )
    )

    s.extend(exercise_block(
        25,
        "Module 4 Practical Challenge",
        "30–45 min",
        "Business requests: find+project, upsert, tags, inventory, order item, status, safe deactivate/delete. Deliver a script with evidence.",
        "162-practical-challenge.svg",
        "Practical challenge ticket",
        "Capstone. Rubric: accurate filters, types, safe writes, array handling, verification. Time-box 30 minutes if Module 5 is this afternoon.",
    ))

    s.append(
        content_slide(
            "Module 4 Exit Ticket",
            """Write answers in one sentence each:

1. One filter you would always preview before `updateMany`
2. Why O5001 fools a query without `$elemMatch`
3. One field you would never `$set` by replacing its parent object
4. What you check after every write

**Completion:** retrieve with precise filters; query nested arrays; project, sort, paginate; insert/update/replace/upsert; delete TEMP records safely; read write results.""",
            "Collect tickets if you use them for attendance. The four questions are the bar for Module 5.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Module Completion Checklist",
            """Participants can:

- [ ] Combine comparison and logical operators
- [ ] Query nested fields and arrays with `$elemMatch`
- [ ] Shape results with projections, sort, skip, limit
- [ ] `countDocuments` and `distinct`
- [ ] Insert one and many; verify ids and types
- [ ] Update scalar, nested, and array fields
- [ ] Replace and upsert without losing fields accidentally
- [ ] Delete only intended test records
- [ ] Interpret `matchedCount` / `modifiedCount` / `deletedCount`""",
            "Use as a self-check before lunch or before Module 5. Gaps become homework on the lab guides.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Questions and Answers",
            """Open floor.

Parking-lot prompts if the room is quiet:

- How would you page products after the 10,000th document?
- When is a transaction required for an order update?
- Should `reviews` stay a separate collection?

Capture unanswered items for Module 5–6.""",
            "Do not start aggregation syntax here. Point range pagination and transactions at later modules.",
        )
    )

    s.append(
        split_slide(
            "Day 2 Review — Query Fluency",
            [
                "Translate a business question into a filter",
                "Return only required fields",
                "Safely modify application data",
                "Work with embedded documents and arrays",
                "Verify and troubleshoot results",
            ],
            "003-business-requirement-to-query.svg",
            "Filter project update verify path into Module 5",
            "If Module 5 is this afternoon, this is the bridge. If Module 4 filled the day, this is the close.",
        )
    )

    s.append(
        content_slide(
            "Transition to Module 5: Aggregation Framework",
            """Module 5 builds on these query skills:

- Pipeline structure
- `$match` (you already think in filters)
- `$project` (you already think in projections)
- `$group` and accumulators
- `$sort` · `$limit`
- Calculated fields and array processing
- Multi-stage analytical pipelines

Same `training_store` data. Reloading `load.js` is wise after today's writes.""",
            "Aggregation is find+project+sort with extra stages, especially $group. Reload the dataset so tomorrow's counts match the notes.",
            fit="fit-sm",
        )
    )

    return "\n\n---\n\n".join(x.strip() + "\n" for x in s)


def append_to_deck(fragment: str) -> None:
    text = DECK.read_text(encoding="utf-8")
    if MARKER in text:
        start = text.find(MARKER)
        # Drop a leading --- before the marker if we re-replace
        prefix = text[:start].rstrip()
        if prefix.endswith("---"):
            prefix = prefix[: -3].rstrip()
        DECK.write_text(prefix + "\n\n---\n\n" + fragment.strip() + "\n", encoding="utf-8")
        print(f"Replaced existing Module 4 in {DECK}")
        return
    DECK.write_text(text.rstrip() + "\n\n---\n\n" + fragment.strip() + "\n", encoding="utf-8")
    print(f"Appended Module 4 to {DECK}")


if __name__ == "__main__":
    if not any(LAB_DIR.glob("exercise-4.1-*.md")):
        raise SystemExit("Lab guides missing. Run python scripts/module04_labs.py first.")
    fragment = build_slides()
    append_to_deck(fragment)
    print(f"Module 4 fragment length: {len(fragment):,} chars")
