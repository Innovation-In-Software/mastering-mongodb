"""Generate Module 5 Marp section and append it to the course deck.

Run from repo root:
    python scripts/_gen_module05_slides.py
"""
from __future__ import annotations

from pathlib import Path

DECK = Path(__file__).resolve().parent.parent / "slides" / "course-complete-marp-with-notes.md"
MARKER = "<!-- _header: 'Module 5 — The Aggregation Framework' -->"
NEXT_MODULE = "<!-- _header: 'Module 6 — Indexing and Query Performance' -->"
ASSETS = "assets/module-05"


def notes(title: str, body: str) -> str:
    return f"<!--\n{body.strip()}\n\nThe slide title is: {title}.\n-->"


def slide(directive: str, body: str) -> str:
    return f"<!-- _class: {directive} -->\n\n{body.strip()}\n"


def split(title: str, bullets: list[str], img: str, alt: str, script: str, *, fit: str | None = None) -> str:
    cls = "split" + (f" {fit}" if fit else "")
    lis = "\n".join(f"- {b}" for b in bullets)
    body = f"""# {title}

<div class="cols">
<div class="col-text">

{lis}

</div>
<div class="col-visual">

<img src="{ASSETS}/{img}" alt="{alt}" width="720">

</div>
</div>

{notes(title, script)}"""
    return slide(cls, body)


def content(title: str, inner: str, script: str, *, fit: str | None = None) -> str:
    cls = "content" + (f" {fit}" if fit else "")
    body = f"""# {title}

{inner.strip()}

{notes(title, script)}"""
    return slide(cls, body)


def lead(title: str, subtitle: str, script: str) -> str:
    body = f"""# {title}

{subtitle}

{notes(title, script)}"""
    return slide("lead", body)


def ex_intro(title: str, bullets: list[str], img: str, alt: str, guide: str, label: str, script: str) -> str:
    lis = "\n".join(f"- {b}" for b in bullets)
    body = f"""# {title}

<div class="cols">
<div class="col-text">

{lis}

**Lab guide:** [`{label}`](../slide-exercises/module-05/{guide})

</div>
<div class="col-visual">

<img src="{ASSETS}/{img}" alt="{alt}" width="720">

</div>
</div>

{notes(title, script)}"""
    return slide("split", body)


def ex_steps(heading: str, steps: list[tuple[str, str, str]], script: str, guide: str | None, label: str | None) -> str:
    blocks = []
    if guide and label:
        blocks.append(f"**Lab guide:** [`{label}`](../slide-exercises/module-05/{guide})")
        blocks.append("")
        blocks.append("**Follow along (Windows) — key steps:**")
        blocks.append("")
    for title, do, exp in steps:
        blocks.append(f"**{title}**")
        blocks.append(f"- **Do:** {do}")
        blocks.append(f"- **Expected:** {exp}")
        blocks.append("")
    inner = "\n".join(blocks).rstrip()
    body = f"""## {heading}

{inner}

{notes(heading, script)}"""
    return slide("fit-md", body)


def build() -> str:
    s: list[str] = []

    s.append(
        """<!-- _header: 'Module 5 — The Aggregation Framework' -->

<!-- _class: lead -->

# The Aggregation Framework

Pipelines transform raw MongoDB documents into summaries, calculations, and reports

"""
        + notes(
            "The Aggregation Framework",
            "Open Module 5 after Module 4 queries. Same training_store. Today they reshape documents instead of only finding them. Reload load.js if anyone still has the Day 1 three-product set.",
        )
    )

    s.append(
        content(
            "Module Learning Objectives",
            """By the end of this module you will be able to:

- Construct pipelines one stage at a time
- Understand how stage order changes results
- Group and summarize documents
- Create calculated fields
- Analyze embedded arrays
- Combine related collections
- Produce multiple metrics from one input set
- Improve pipeline clarity and efficiency""",
            "Read the outcomes. The product is working pipelines on paid orders, not a memorized operator list.",
        )
    )

    s.append(
        split(
            "Operational Queries vs. Aggregation",
            [
                "**find()** retrieves application records",
                "**aggregate()** transforms them into reports",
                "Stored fields versus calculated fields",
                "One filter versus ordered stages",
            ],
            "001-operational-query-vs-aggregation.svg",
            "Operational query versus aggregation",
            "Show both snippets live if time: find SHIPPED versus group by fulfillmentStatus.",
        )
    )

    s.append(
        content(
            "Operational vs. aggregation — code",
            """Operational:

```javascript
db.orders.find({ fulfillmentStatus: "SHIPPED" })
```

Analytical:

```javascript
db.orders.aggregate([
  { $group: { _id: "$fulfillmentStatus", orderCount: { $sum: 1 } } }
])
```

| Operational        | Aggregation              |
|--------------------|--------------------------|
| Retrieve documents | Transform documents      |
| Return stored fields | Calculate new fields   |
| Application lookup | Reporting and analysis   |""",
            "Comma in find is a filter. Array in aggregate is a pipeline. Do not mix the two APIs.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "What Is an Aggregation Pipeline?",
            [
                "An ordered list of processing stages",
                "Each stage receives documents",
                "Each stage performs one operation",
                "Output of one stage is input of the next",
            ],
            "002-aggregation-pipeline-overview.svg",
            "Collection through stages to result",
            "Draw the vertical flow on the board once. They will reuse it all afternoon.",
        )
    )

    s.append(
        split(
            "Pipeline Anatomy",
            [
                "Collection plus `aggregate()`",
                "Pipeline is an array of stage documents",
                "Stages run in listed order",
                "Final output is new documents",
            ],
            "003-aggregation-pipeline-anatomy.svg",
            "aggregate method and pipeline array",
            "Point at the square brackets. A pipeline with one stage is still a pipeline.",
        )
    )

    s.append(
        content(
            "Pipeline anatomy — code",
            """```javascript
db.orders.aggregate([
  { $match: { paymentStatus: "PAID" } },
  {
    $group: {
      _id: "$fulfillmentStatus",
      orderCount: { $sum: 1 },
      revenue: { $sum: "$total" }
    }
  },
  { $sort: { revenue: -1 } }
])
```""",
            "Leave this up while you type Demo 5.1. They should see match, group, sort as three objects.",
            fit="fit-sm",
        )
    )

    s.append(
        split(
            "How Documents Move Through a Pipeline",
            [
                "Each stage’s output is the next stage’s input",
                "Documents are not updated in the collection",
                "A later stage never sees the original source shape unless you kept it",
            ],
            "004-how-documents-move.svg",
            "Documents flowing from one stage to the next",
            "Say this out loud: the collection is the first input only. Everything after that is pipeline documents.",
        )
    )

    s.append(
        split(
            "Document Count and Shape Through a Pipeline",
            [
                "100 orders → `$match` → 65 paid",
                "Then `$group` → 4 status groups",
                "Then `$sort` → 4 ranked summaries",
                "**Key:** count, content, and shape can all change",
            ],
            "007-document-count-and-shape.svg",
            "Document counts shrinking through stages",
            "On this dataset: 17 orders → 13 paid → a handful of status groups.",
        )
    )

    s.append(
        split(
            "Pipeline Funnel",
            [
                "Large input set",
                "Filtered set (`$match`)",
                "Transformed set (`$set` / `$project`)",
                "Grouped summaries (`$group`)",
                "Final report (`$sort` / `$limit` / `$facet`)",
            ],
            "005-pipeline-funnel.svg",
            "Funnel from collection to report",
            "This is the picture they should draw on a whiteboard before typing stages.",
        )
    )

    s.append(
        split(
            "Stage Order Matters",
            [
                "`$match` → `$group` filters source documents",
                "`$group` → `$match` filters summaries",
                "Order changes meaning, shape, volume, cost",
            ],
            "006-stage-order-matters.svg",
            "Two different meanings of the same stages",
            "Ask: if I match SHIPPED after grouping, what am I filtering? Groups, not orders.",
        )
    )

    s.append(
        split(
            "The Sample Analytical Dataset",
            [
                "**products** — category, price, tags, active",
                "**orders** — items, payment, fulfillment, totals, dates",
                "**customers** — name, location, status",
                "**reviews** — product, rating, createdAt",
            ],
            "009-analytical-dataset.svg",
            "Four training_store collections",
            "13 paid orders July–September 2026. O6499 has no customer. Some orders omit shippingFee.",
        )
    )

    s.append(
        split(
            "Demo 5.1 — Build a Pipeline One Stage at a Time",
            [
                "15 minutes · instructor `mongosh`",
                "Start with paid orders",
                "Add `$group`, then `$sort`, then `$project`",
                "Inspect after every stage",
            ],
            "010-development-workflow.svg",
            "Match, group, sort, project",
            "Do not paste the finished pipeline first. The habit is the lesson.",
        )
    )

    s.append(
        content(
            "Demo 5.1 — commands",
            """```javascript
db.orders.aggregate([
  { $match: { paymentStatus: "PAID" } }
])
```

Then append:

```javascript
{ $group: {
    _id: "$fulfillmentStatus",
    orderCount: { $sum: 1 },
    revenue: { $sum: "$total" }
} }
{ $sort: { revenue: -1 } }
```

Finish with a `$project` that renames `_id` to `fulfillmentStatus`.""",
            "Cold-call: how many documents after match? After group? Why did the number drop?",
            fit="fit-sm",
        )
    )

    s.append(
        ex_intro(
            "Exercise 5.1 — Arrange Pipeline Stages",
            [
                "10 minutes · pairs",
                "Top five products by line revenue",
                "Six stages, one correct teaching order",
            ],
            "149-ex-5-1-arrange-pipeline.svg",
            "Match unwind set group sort limit",
            "exercise-5.1-arrange-pipeline-stages.md",
            "Exercise 5.1",
            "Reveal only after they commit. Wrong answers are useful: limit-before-sort is the classic.",
        )
    )

    s.append(
        ex_steps(
            "Exercise 5.1 — Steps 1–2",
            [
                (
                    "Step 1 — Propose an order",
                    "Sequence the six stages and describe the documents after each.",
                    "A defensible sequence, not a guess.",
                ),
                (
                    "Step 2 — Check the pattern",
                    "`$match` → `$unwind` → `$set` → `$group` → `$sort` → `$limit`.",
                    "You can explain why limit cannot precede sort.",
                ),
            ],
            "Time-box 10 minutes. Then show the diagram.",
            "exercise-5.1-arrange-pipeline-stages.md",
            "Exercise 5.1",
        )
    )

    s.append(
        ex_intro(
            "Lab 5.1 — Aggregation Dataset Verification",
            [
                "15 minutes · every laptop",
                "Count collections; inspect types",
                "Record field paths for later labs",
            ],
            "009-analytical-dataset.svg",
            "training_store collections",
            "lab-5.1-aggregation-dataset-verification.md",
            "Lab 5.1",
            "If counts are wrong, stop and reload load.js. Everything else depends on 13 paid orders.",
        )
    )

    s.append(
        ex_steps(
            "Lab 5.1 — Steps 1–2",
            [
                (
                    "Step 1 — Select and count",
                    "`use training_store` and count customers, products, orders, reviews, paid orders.",
                    "6, 12, 17, 6, and 13 paid.",
                ),
                (
                    "Step 2 — Inspect documents",
                    "`findOne` on each collection; note Decimal128, Date, and `items`.",
                    "O6201 has no shippingFee. That gap is intentional.",
                ),
            ],
            "Walk the room. Confirm Decimal128 before anyone groups prices as Doubles.",
            "lab-5.1-aggregation-dataset-verification.md",
            "Lab 5.1",
        )
    )

    s.append(
        split(
            "The `$match` Stage",
            [
                "Filters pipeline documents",
                "Uses the Module 4 query language",
                "Place selective `$match` early when logic allows",
            ],
            "011-match-stage.svg",
            "$match filters pipeline input",
            "Same operators as find(). The difference is where it sits in a pipeline.",
        )
    )

    s.append(
        split(
            "`find()` Filter vs. `$match`",
            [
                "Same comparison and logical operators",
                "`find()` returns a cursor of stored documents",
                "`$match` is one stage in a transformation",
            ],
            "014-find-vs-match.svg",
            "find filter versus match stage",
            "They already think in filters. Today the filter is stage one, not the whole job.",
        )
    )

    s.append(
        split(
            "Early `$match` Optimization",
            [
                "Reduce the collection before expensive stages",
                "Paid-only is selective on this dataset (13 of 17)",
                "A nonselective `$match` still scans most documents",
            ],
            "012-early-match-optimization.svg",
            "Large collection reduced before transforms",
            "Lab 5.9 will contrast this with a late match. Do not promise milliseconds on 17 documents.",
        )
    )

    s.append(
        content(
            "`$match` with Comparison Operators",
            """```javascript
db.orders.aggregate([
  { $match: { total: { $gte: Decimal128("500.00") } } }
])
```

Supported: `$eq` `$ne` `$gt` `$gte` `$lt` `$lte` `$in` `$nin`.

Money comparisons must use **Decimal128**, not `500` as a Double.""",
            "If they type 500 they may match nothing. Same trap as Module 4.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "Comparison Conditions in `$match`",
            [
                "`$gte` / `$lte` for ranges",
                "`$in` / `$nin` for lists",
                "Money ranges use **Decimal128**",
            ],
            "015-match-comparison.svg",
            "Comparison operators in match",
            "High-value paid orders use 1000.00 as Decimal128 — four documents.",
        )
    )

    s.append(
        content(
            "`$match` with Logical Operators",
            """```javascript
db.products.aggregate([
  {
    $match: {
      active: true,
      $or: [
        { category: "LAPTOP" },
        { category: "ACCESSORY" }
      ]
    }
  }
])
```

Comma-separated fields are AND. `$or` needs an array of expressions.""",
            "This is the same logical-query lesson as find(). Do not re-teach the whole operator set.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "Logical Conditions in `$match`",
            [
                "Comma-separated fields are AND",
                "`$or` needs an array of expressions",
                "`$nor` is none of the branches",
            ],
            "016-match-logical.svg",
            "AND and OR branches",
            "Exercise 5.2 combines active plus category $in — implicit AND.",
        )
    )

    s.append(
        split(
            "Date-Range Filtering",
            [
                "Inclusive start, exclusive end",
                "`createdAt: { $gte, $lt }`",
                "Then group by period — do not skip the window",
            ],
            "017-date-range-filtering.svg",
            "Start and end boundaries for a reporting period",
            "Exercise 5.13 uses 2026-07-01 through 2026-10-01 exclusive.",
        )
    )

    s.append(
        split(
            "The `$project` Stage",
            [
                "Include, exclude, rename, calculate",
                "Build nested output",
                "Does **not** change stored documents",
            ],
            "019-project-stage.svg",
            "Include rename calculate with project",
            "Contrast with find projection: aggregation $project can compute new fields.",
        )
    )

    s.append(
        content(
            "Inclusion and Exclusion with `$project`",
            """Inclusion:

```javascript
{ $project: { name: 1, price: 1, _id: 0 } }
```

Exclusion:

```javascript
{ $project: { attributes: 0, tags: 0 } }
```

Do not mix inclusion and exclusion except for `_id`.""",
            "Same rule as find projection. Mixing is the error they will hit in the first lab.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "Inclusion Projection",
            [
                "Listed fields are kept",
                "Everything else is dropped",
                "`_id` is kept unless you set `_id: 0`",
            ],
            "020-inclusion-projection.svg",
            "Selected fields retained",
            "This is how Exercise 5.3 starts: sku, name, category, price only.",
        )
    )

    s.append(
        split(
            "Exclusion Projection",
            [
                "Listed fields are removed",
                "Other fields remain",
                "Do not mix with inclusion except `_id`",
            ],
            "021-exclusion-projection.svg",
            "Selected fields removed",
            "Useful when you only want to drop attributes and tags.",
        )
    )

    s.append(
        content(
            "Renaming Fields with `$project`",
            """```javascript
{ $project: {
    _id: 0,
    productCode: "$sku",
    productName: "$name",
    sellingPrice: "$price"
} }
```

The `$` prefix means “use the value from this field.” Without it, you store the literal string `sku`.""",
            "Write a wrong version without $ on the board. That bug appears in Exercise 5.11.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "Field Renaming with `$project`",
            [
                "Stored `sku` → report `productCode`",
                "The `$` copies the value",
                "Without `$` you emit the literal text",
            ],
            "022-field-renaming.svg",
            "Stored names mapped to report names",
            "Have them say the dollar sign out loud once. It sticks.",
        )
    )

    s.append(
        content(
            "Calculated Fields with `$project`",
            """```javascript
{ $project: {
    orderNumber: 1,
    subtotal: 1,
    tax: 1,
    calculatedTotal: { $add: ["$subtotal", "$tax"] }
} }
```

The source collection is unchanged. Only the pipeline document gains the field.""",
            "Ask whether they should persist this. Often yes later (computed pattern) — not today.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "The `$set` Stage",
            [
                "Adds or replaces named fields",
                "Every other field stays on the document",
                "`$addFields` is the same operator here",
            ],
            "024-set-stage.svg",
            "New fields added while existing fields remain",
            "Prefer $set while calculating. Save $project for the report shape.",
        )
    )

    s.append(
        split(
            "The `$set` and `$addFields` Stages",
            [
                "Add or replace fields",
                "Unspecified fields are kept",
                "`$set` and `$addFields` are aliases here",
                "`$project` lists what remains",
            ],
            "025-project-vs-set.svg",
            "set keeps fields project lists them",
            "Prefer $set when you are adding a calculation. Prefer $project for the final report shape.",
        )
    )

    s.append(
        split(
            "Removing Fields with `$unset`",
            [
                "Drops named fields from **pipeline** documents",
                "Stored orders are untouched",
                "O5001 has `internalNotes` for a live demo",
            ],
            "026-unset-stage.svg",
            "Unwanted fields removed without modifying stored data",
            "This is not deleteMany. Make that joke once, then move on.",
        )
    )

    s.append(
        split(
            "Nested Output Construction",
            [
                "Flat source fields can become nested report sections",
                "`customer: { name, city }` is still one pipeline document",
                "Use this for readable executive output",
            ],
            "027-nested-output.svg",
            "Flat fields reorganized into nested report sections",
            "Exercise 5.3 asks for this shape. They often emit sibling fields instead of nesting.",
        )
    )

    s.append(
        split(
            "Aggregation Expressions",
            [
                "Used inside `$project`, `$set`, `$group`",
                "Also `$match` with `$expr`",
                "Arithmetic, string, date, array, conditional, conversion",
            ],
            "029-expression-categories.svg",
            "Expression categories",
            "They do not need every operator. They need to recognize that $add is an expression, not a stage.",
        )
    )

    s.append(
        split(
            "Field Reference Syntax",
            [
                "`\"category\"` is the literal string category",
                "`\"$category\"` is the value of that field",
                "Forgetting `$` is the most common silent bug",
            ],
            "030-field-reference-syntax.svg",
            "Dollar fieldName retrieves the current document value",
            "Write both forms on the board. Exercise 5.11 plants a missing dollar.",
        )
    )

    s.append(
        content(
            "Arithmetic Expressions",
            """`$add` `$subtract` `$multiply` `$divide` `$round`

```javascript
{ $project: {
    orderNumber: 1,
    calculatedLineTotal: {
      $multiply: ["$quantity", "$unitPrice"]
    }
} }
```

After `$unwind`, those fields are `$items.quantity` and `$items.unitPrice`.""",
            "The nested path is the bug they will hit in Lab 5.4 if they skip unwind.",
            fit="fit-md",
        )
    )

    s.append(
        content(
            "String Expressions",
            """`$concat` `$toUpper` `$toLower` `$trim` `$substrCP`

```javascript
{ $project: {
    customerName: {
      $concat: ["$name.first", " ", "$name.last"]
    }
} }
```

Missing first or last name yields null for the whole concat unless you `$ifNull` the parts.""",
            "C101 becomes Aisha Khan. Show that in Demo 5.6.",
            fit="fit-md",
        )
    )

    s.append(
        content(
            "Date Expressions",
            """`$year` `$month` `$dayOfMonth` `$dayOfWeek` `$dateToString` `$dateTrunc`

```javascript
{ $set: {
    orderMonth: {
      $dateToString: { format: "%Y-%m", date: "$createdAt" }
    }
} }
```

Name a time zone in production reports.""",
            "YYYY-MM strings sort chronologically. That is why we use that format in Lab 5.6.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "Time-Zone-Aware Reporting",
            [
                "`createdAt` is stored in UTC",
                "Name the reporting time zone explicitly",
                "Otherwise month boundaries shift with the classroom clock",
            ],
            "112-timezone-aware-reporting.svg",
            "UTC timestamps converted to a named reporting zone",
            "For this course, use UTC so every laptop agrees. Production reports name America/Toronto or similar.",
        )
    )

    s.append(
        content(
            "Conditional Expressions",
            """`$cond` — two-way:

```javascript
{ $cond: [
  { $gte: ["$total", Decimal128("1000.00")] },
  "HIGH_VALUE",
  "STANDARD"
] }
```

`$switch` — several branches plus `default`. High-value paid orders in this set: O6101, O6202, O6301, O6304.""",
            "Threshold must be Decimal128. Four high-value paid orders is a useful check in $facet labs.",
            fit="fit-sm",
        )
    )

    s.append(
        split(
            "`$cond` Decision Flow",
            [
                "One condition",
                "True result or false result",
                "HIGH_VALUE vs STANDARD on this course",
            ],
            "037-cond-decision-flow.svg",
            "Condition to true or false result",
            "Two-way only. Several bands belong on the next slide.",
        )
    )

    s.append(
        split(
            "`$switch` Decision Flow",
            [
                "Ordered branches",
                "First matching `case` wins",
                "`default` catches the rest",
            ],
            "038-switch-decision-flow.svg",
            "Multiple conditions to one classification",
            "LOW / MEDIUM / HIGH is the teaching example. Order the branches from high to low.",
        )
    )

    s.append(
        split(
            "Demo 5.2 — Filter and Reshape Documents",
            [
                "15 minutes",
                "Active products: sku, name, category, price",
                "Add a price band with `$cond`",
            ],
            "019-project-stage.svg",
            "Project reshape",
            "Keep $match active: true. L190 should disappear.",
        )
    )

    s.append(
        split(
            "Demo 5.3 — Add Calculated Fields",
            [
                "15 minutes",
                "Subtotal + tax + shipping",
                "`$ifNull` on shippingFee",
                "HIGH_VALUE class and reporting month",
            ],
            "025-project-vs-set.svg",
            "set versus project",
            "Use O6201 (no shippingFee) and O6301 (has shippingFee). That contrast is the point.",
        )
    )

    s.append(
        ex_intro(
            "Exercise 5.2 — Build a `$match` Stage",
            [
                "10 minutes",
                "Paid, high-value, categories, dates, provinces",
            ],
            "011-match-stage.svg",
            "Match stage",
            "exercise-5.2-build-a-match-stage.md",
            "Exercise 5.2",
            "Watch Decimal128 on the 1000.00 threshold.",
        )
    )

    s.append(
        ex_steps(
            "Exercise 5.2 — Steps 1–2",
            [
                (
                    "Step 1 — Paid and high-value",
                    "`paymentStatus: PAID` then add `total $gte Decimal128 1000.00`.",
                    "13 paid; four high-value.",
                ),
                (
                    "Step 2 — Products, reviews, provinces",
                    "Active LAPTOP/ACCESSORY; August reviews; Ontario/Quebec addresses.",
                    "Dotted path addresses.province.",
                ),
            ],
            "If province query is empty they forgot quotes on the dotted key.",
            "exercise-5.2-build-a-match-stage.md",
            "Exercise 5.2",
        )
    )

    s.append(
        ex_intro(
            "Exercise 5.3 — Reshape Documents with `$project`",
            [
                "15 minutes",
                "Rename fields; then nest product and pricing",
            ],
            "019-project-stage.svg",
            "Project reshape",
            "exercise-5.3-reshape-documents-with-project.md",
            "Exercise 5.3",
            "The $ prefix is the whole exercise.",
        )
    )

    s.append(
        ex_steps(
            "Exercise 5.3 — Steps 1–2",
            [
                (
                    "Step 1 — Flat renamed projection",
                    "productCode, productName, category, sellingPrice; `_id: 0`.",
                    "Twelve documents, no `_id`.",
                ),
                (
                    "Step 2 — Nested output",
                    "Match L100; project `product` and `pricing` objects.",
                    "product.code is L100.",
                ),
            ],
            "Collect one nested document on the projector.",
            "exercise-5.3-reshape-documents-with-project.md",
            "Exercise 5.3",
        )
    )

    s.append(
        ex_intro(
            "Exercise 5.4 — Create Calculated Fields",
            [
                "15 minutes",
                "Line revenue, shipping-safe total, name, class, month",
            ],
            "029-expression-categories.svg",
            "Expression categories",
            "exercise-5.4-create-calculated-fields.md",
            "Exercise 5.4",
            "Unwind before line revenue. $ifNull before $add.",
        )
    )

    s.append(
        ex_steps(
            "Exercise 5.4 — Steps 1–2",
            [
                (
                    "Step 1 — Line revenue and shipping",
                    "Unwind O6301 items; multiply; `$ifNull` shippingFee.",
                    "Line revenues 1299.99 and 24.99.",
                ),
                (
                    "Step 2 — Name, class, month",
                    "`$concat` names; `$cond` HIGH_VALUE; `$dateToString` month.",
                    "O6202 is HIGH_VALUE in 2026-08.",
                ),
            ],
            "If concat is null they used name instead of name.first.",
            "exercise-5.4-create-calculated-fields.md",
            "Exercise 5.4",
        )
    )

    s.append(
        split(
            "The `$group` Stage",
            [
                "Combines documents that share a key",
                "Output is one document per group",
                "Original fields are not kept automatically",
            ],
            "041-group-stage.svg",
            "Many documents to one summary per key",
            "This is the mental shift from find(). They are inventing new documents.",
        )
    )

    s.append(
        split(
            "Understanding the Group `_id`",
            [
                '`"$_id": "$category"` — one group per category',
                "`null` — one group for everything",
                "Object `_id` — one group per combination",
            ],
            "042-group-id.svg",
            "Three forms of group id",
            "Say out loud: this _id is not the order’s ObjectId.",
        )
    )

    s.append(
        split(
            "Group All Documents Together",
            [
                "`_id: null` — one bucket",
                "Whole-collection totals",
                "Paid revenue and order count in one document",
            ],
            "043-group-all-documents.svg",
            "id null producing one summary",
            "Useful for the totals facet. Not useful when they still need a category breakdown.",
        )
    )

    s.append(
        split(
            "Group by One Field vs. Many",
            [
                "One field: `_id: \"$category\"`",
                "Many fields: object `_id` with two paths",
                "Each unique combination is one output document",
            ],
            "045-group-by-multiple-fields.svg",
            "Orders grouped by payment and fulfillment",
            "Exercise 5.6. PAID+SHIPPED will look like the revenue winner.",
        )
    )

    s.append(
        split(
            "Accumulator Operators",
            [
                "`$sum` `$avg` `$min` `$max`",
                "`$first` `$last` need a prior sort when order matters",
                "`$push` keeps duplicates; `$addToSet` unique values",
            ],
            "047-accumulator-operators.svg",
            "Accumulator table",
            "$sum: 1 counts documents. $sum: \"$total\" adds a field. Both are $sum.",
        )
    )

    s.append(
        content(
            "Counting, Sums, Averages, Min and Max",
            """Count: `{ productCount: { $sum: 1 } }`

Revenue: `{ totalRevenue: { $sum: "$total" } }`

Average: `{ averagePrice: { $avg: "$price" } }`

Range: `{ minimumPrice: { $min: "$price" }, maximumPrice: { $max: "$price" } }`

Inputs must be compatible numeric types — Decimal128 for money.""",
            "Lab 5.2 is this slide typed against active products.",
            fit="fit-md",
        )
    )

    s.append(
        content(
            "Preserving Values During Grouping",
            """```javascript
{ $group: {
    _id: "$category",
    firstProduct: { $first: "$name" },
    productNames: { $push: "$name" },
    uniqueTags: { $addToSet: "$tags" }
} }
```

`$addToSet: "$tags"` collects **arrays of tags**, not individual tag strings. Flatten first if you need unique tag values.""",
            "Do not skip this footnote. Otherwise uniqueTags looks nested and confusing.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "Fields Lost During Grouping",
            [
                "After `$group`, only `_id` and accumulators remain",
                "Need a name? `$first` or `$push`",
                "Need uniqueness? `$addToSet`",
            ],
            "055-fields-lost-during-grouping.svg",
            "Original fields disappear unless accumulated",
            "This is the surprise after their first $group. Lab 5.2 projects category from _id because name is gone.",
        )
    )

    s.append(
        content(
            "Grouping by Multiple Fields",
            """```javascript
{ $group: {
    _id: {
      paymentStatus: "$paymentStatus",
      fulfillmentStatus: "$fulfillmentStatus"
    },
    orderCount: { $sum: 1 },
    revenue: { $sum: "$total" }
} }
```

Each unique pair is one output document.""",
            "Exercise 5.6. PAID+SHIPPED will be a large-revenue cell.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "Demo 5.4 — Group and Summarize Product Data",
            [
                "15 minutes",
                "Count, average, min, max by category",
                "Sort by average price",
            ],
            "162-lab-5-2-product-summary.svg",
            "Product summary flow",
            "Exclude inactive. LAPTOP average should look expensive next to BOOK.",
        )
    )

    s.append(
        ex_intro(
            "Exercise 5.5 — Group and Calculate Totals",
            [
                "15 minutes",
                "Active products by category",
            ],
            "162-lab-5-2-product-summary.svg",
            "Category stats",
            "exercise-5.5-group-and-calculate-totals.md",
            "Exercise 5.5",
            "L190 must not appear in LAPTOP count.",
        )
    )

    s.append(
        ex_steps(
            "Exercise 5.5 — Steps 1–2",
            [
                (
                    "Step 1 — Group active products",
                    "`$match active` then `$group` by category with count/avg/min/max.",
                    "Four groups; LAPTOP count 2.",
                ),
                (
                    "Step 2 — Sort by average",
                    "`$sort: { averagePrice: -1 }`.",
                    "LAPTOP first.",
                ),
            ],
            "This is the warm-up for Lab 5.2.",
            "exercise-5.5-group-and-calculate-totals.md",
            "Exercise 5.5",
        )
    )

    s.append(
        ex_intro(
            "Exercise 5.6 — Group by Multiple Dimensions",
            [
                "15 minutes",
                "Payment × fulfillment",
            ],
            "042-group-id.svg",
            "Compound group id",
            "exercise-5.6-group-by-multiple-dimensions.md",
            "Exercise 5.6",
            "Make someone read _id aloud as a sentence.",
        )
    )

    s.append(
        ex_steps(
            "Exercise 5.6 — Steps 1–2",
            [
                (
                    "Step 1 — Compound `_id`",
                    "Group by paymentStatus and fulfillmentStatus; sum count and revenue.",
                    "Several combination documents.",
                ),
                (
                    "Step 2 — Read the key",
                    "Rewrite one `_id` in words.",
                    "`_id` is the group key, not the order id.",
                ),
            ],
            "If they group only one field they skipped the object _id syntax.",
            "exercise-5.6-group-by-multiple-dimensions.md",
            "Exercise 5.6",
        )
    )

    s.append(
        ex_intro(
            "Lab 5.2 — Product Summary Pipeline",
            [
                "25 minutes",
                "Category report with renamed fields",
            ],
            "162-lab-5-2-product-summary.svg",
            "Product summary pipeline",
            "lab-5.2-product-summary-pipeline.md",
            "Lab 5.2",
            "Final $project should hide _id. That is the report shape.",
        )
    )

    s.append(
        ex_steps(
            "Lab 5.2 — Steps 1–2",
            [
                (
                    "Step 1 — Filter and group",
                    "Active products; group by category with four accumulators.",
                    "Four categories; LAPTOP count 2.",
                ),
                (
                    "Step 2 — Sort and rename",
                    "Sort averagePrice descending; project `category: $_id`.",
                    "LAPTOP first; field is category.",
                ),
            ],
            "Compare averages on the board. BOOK should be cheapest on average.",
            "lab-5.2-product-summary-pipeline.md",
            "Lab 5.2",
        )
    )

    s.append(
        ex_intro(
            "Lab 5.3 — Order Revenue Pipeline",
            [
                "25 minutes",
                "Paid revenue by fulfillment status",
            ],
            "041-group-stage.svg",
            "Group summaries",
            "lab-5.3-order-revenue-pipeline.md",
            "Lab 5.3",
            "Validate SHIPPED count with countDocuments = 6.",
        )
    )

    s.append(
        ex_steps(
            "Lab 5.3 — Steps 1–2",
            [
                (
                    "Step 1 — Match, group, sort, project",
                    "Paid only; group fulfillmentStatus; sort totalRevenue.",
                    "SHIPPED highest revenue; PENDING absent.",
                ),
                (
                    "Step 2 — Spot-check",
                    "countDocuments PAID + SHIPPED versus pipeline orderCount.",
                    "Both are 6.",
                ),
            ],
            "Validation is the habit Module 6 will need when indexes change plans but not results.",
            "lab-5.3-order-revenue-pipeline.md",
            "Lab 5.3",
        )
    )

    s.append(
        content(
            "The `$sort`, `$limit`, and `$skip` Stages",
            """Sort: `{ $sort: { totalRevenue: -1 } }` — add a tiebreaker for stable results.

Limit: `{ $limit: 5 }` — top N.

Skip: `{ $skip: 10 }` — basic paging; large skips are inefficient.

**Top-N pattern:** `$group` → `$sort` → `$limit`. Limit before sort is the wrong five documents.""",
            "Write the three-stage pattern on the board and leave it up.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "Top-N Reporting Pattern",
            [
                "Compute the metric first",
                "Sort that metric",
                "Then keep N",
            ],
            "062-top-n-pattern.svg",
            "Group sort limit",
            "Exercise 5.8. If they limit first they get three random expensive-looking orders.",
        )
    )

    s.append(
        split(
            "Why Sort Must Precede Limit",
            [
                "Sort then limit → the true top N",
                "Limit then sort → an arbitrary subset, then ordered",
                "Wrong five documents still look “sorted”",
            ],
            "063-sort-must-precede-limit.svg",
            "Correct top results versus sorting a limited subset",
            "Leave this comparison up during Exercise 5.1.",
        )
    )

    s.append(
        split(
            "`$count` and `$sortByCount`",
            [
                "`$count: \"paidOrderCount\"` → one named total",
                "`$sortByCount: \"$category\"` → group + sort by frequency",
            ],
            "065-sortbycount-stage.svg",
            "count versus sortByCount",
            "sortByCount is sugar. They should still be able to write group+sort by hand.",
        )
    )

    s.append(
        split(
            "The `$unwind` Stage",
            [
                "One pipeline document per array element",
                "Parent fields are copied onto each row",
                "Required before grouping line items by SKU",
            ],
            "068-unwind-stage.svg",
            "One order becomes two item documents",
            "Draw O6301: L100 and A400. Two rows, same orderNumber.",
        )
    )

    s.append(
        split(
            "Document Multiplication Through `$unwind`",
            [
                "One order with three items → three documents",
                "Pipeline count follows array lengths",
                "After unwind, `$sum: \"$total\"` repeats the order total",
            ],
            "070-document-multiplication.svg",
            "Input count increasing with array sizes",
            "Exercise 5.12 double-counts multi-item orders this way. Line revenue is the fix.",
        )
    )

    s.append(
        content(
            "Preserving Empty and Null Arrays",
            """```javascript
{ $unwind: { path: "$items", preserveNullAndEmptyArrays: true } }
```

Without this option, documents with missing, null, or empty `items` disappear.

Use it when the business still needs those parent documents.""",
            "All teaching orders have items. Still teach the option — production data will not be as clean.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "Filtering Array Elements",
            [
                "`$filter` keeps matching elements **inside** the array",
                "`$unwind` explodes the array into documents",
                "`$$item` is the current element",
            ],
            "074-filter-vs-unwind.svg",
            "filter versus unwind",
            "If they still need one document per order, filter. If they need product totals, unwind.",
        )
    )

    s.append(
        split(
            "Unwind, Group, and Reassemble",
            [
                "Paid orders → unwind items",
                "Line revenue → group by SKU",
                "Sort → ranked products",
            ],
            "076-unwind-calculate-group.svg",
            "Unwind group sort flow",
            "This is Demo 5.5 and Lab 5.4. Memorize the flow, not the punctuation.",
        )
    )

    s.append(
        content(
            "Working with Order Items",
            """After `$unwind: "$items"`:

```javascript
{ $set: {
    lineRevenue: {
      $multiply: ["$items.quantity", "$items.unitPrice"]
    }
} }
{ $group: {
    _id: "$items.sku",
    unitsSold: { $sum: "$items.quantity" },
    revenue: { $sum: "$lineRevenue" }
} }
```

Do not `$sum: "$total"` after unwind — that repeats the **order** total on every line.""",
            "Exercise 5.12’s inefficient pipeline makes this exact mistake.",
            fit="fit-sm",
        )
    )

    s.append(
        split(
            "Demo 5.5 — Analyze Order Items with `$unwind`",
            [
                "20 minutes",
                "Paid → unwind → line revenue → group SKU",
                "Sort by revenue; top products",
            ],
            "164-lab-5-4-product-sales.svg",
            "Product sales pipeline",
            "Reveal L110 as top SKU. Two units at 1899.99 beats two L100s.",
        )
    )

    s.append(
        ex_intro(
            "Exercise 5.7 — Analyze Arrays with `$unwind`",
            [
                "15 minutes",
                "Units, revenue, order count per SKU",
            ],
            "076-unwind-calculate-group.svg",
            "Unwind then group",
            "exercise-5.7-analyze-arrays-with-unwind.md",
            "Exercise 5.7",
            "No duplicate SKUs per order, so $sum:1 is order count.",
        )
    )

    s.append(
        ex_steps(
            "Exercise 5.7 — Steps 1–2",
            [
                (
                    "Step 1 — Unwind and group",
                    "Paid, unwind, lineRevenue, group by items.sku.",
                    "L110 first at 3799.98.",
                ),
                (
                    "Step 2 — Name the top SKU",
                    "Write `_id` and unitsSold.",
                    "L110, 2 units.",
                ),
            ],
            "If laptop is missing they forgot $match PAID or grouped sku not items.sku.",
            "exercise-5.7-analyze-arrays-with-unwind.md",
            "Exercise 5.7",
        )
    )

    s.append(
        ex_intro(
            "Exercise 5.8 — Build a Top-N Report",
            [
                "15 minutes",
                "Customers, products, orders, categories",
            ],
            "062-top-n-pattern.svg",
            "Top-N pattern",
            "exercise-5.8-build-a-top-n-report.md",
            "Exercise 5.8",
            "Sort before limit on every pipeline.",
        )
    )

    s.append(
        ex_steps(
            "Exercise 5.8 — Steps 1–2",
            [
                (
                    "Step 1 — Customers and high-value orders",
                    "Top five spenders; three highest paid orders.",
                    "C101 first; O6202 and O6304 in the top three.",
                ),
                (
                    "Step 2 — Units and categories",
                    "Top three SKUs by units; `$sortByCount` category.",
                    "A410 among unit leaders; ACCESSORY has four products.",
                ),
            ],
            "Tiebreakers: orderNumber or sku.",
            "exercise-5.8-build-a-top-n-report.md",
            "Exercise 5.8",
        )
    )

    s.append(
        ex_intro(
            "Lab 5.4 — Product Sales Pipeline",
            [
                "30 minutes",
                "Top five SKUs by line revenue",
            ],
            "164-lab-5-4-product-sales.svg",
            "Top five products",
            "lab-5.4-product-sales-pipeline.md",
            "Lab 5.4",
            "Must unwind before group. Must not sum order total.",
        )
    )

    s.append(
        ex_steps(
            "Lab 5.4 — Steps 1–2",
            [
                (
                    "Step 1 — Full pipeline",
                    "Match, unwind, set lineRevenue, group, sort, limit 5.",
                    "L110, L100, A500 lead.",
                ),
                (
                    "Step 2 — Explain orderCount",
                    "Is `$sum: 1` orders or lines?",
                    "Orders, because SKUs are unique per order here.",
                ),
            ],
            "If someone gets 13 products they limited too late or not at all — fine, then add limit.",
            "lab-5.4-product-sales-pipeline.md",
            "Lab 5.4",
        )
    )

    s.append(
        split(
            "The `$lookup` Stage",
            [
                "Combines documents from another collection",
                "Result is **always an array**",
                "Useful — not a reason to copy every SQL join",
            ],
            "079-lookup-stage.svg",
            "orders lookup customers",
            "Remind them of Module 3: orders reference customers. Today we join when the report needs names.",
        )
    )

    s.append(
        split(
            "Local and Foreign Fields",
            [
                "`from` — other collection",
                "`localField` — current document",
                "`foreignField` — other collection",
                "`as` — output array name",
            ],
            "080-local-foreign-mapping.svg",
            "customerId equals customers _id",
            "Types must match. ObjectId to ObjectId. O6499 matches nothing.",
        )
    )

    s.append(
        split(
            "Lookup Result Is an Array",
            [
                "Zero matches → `[]`",
                "One match → `[ doc ]` — still an array",
                "O6499 is the empty-array teaching trap",
            ],
            "082-lookup-result-is-array.svg",
            "Zero, one, or multiple matches in as",
            "Show the array in mongosh before they unwind. Never skip that shape.",
        )
    )

    s.append(
        split(
            "Matched vs. Unmatched Lookup",
            [
                "Most orders match exactly one customer",
                "O6499 receives an empty array",
                "`preserveNullAndEmptyArrays` keeps it after unwind",
            ],
            "085-matched-vs-unmatched-lookup.svg",
            "Orders with matches versus empty array",
            "Exercise 5.9 success criterion is that O6499 still appears.",
        )
    )

    s.append(
        content(
            "Joining Customers and Orders",
            """```javascript
db.orders.aggregate([
  { $lookup: {
      from: "customers",
      localField: "customerId",
      foreignField: "_id",
      as: "customer"
  } },
  { $unwind: "$customer" },
  { $project: {
      _id: 0,
      orderNumber: 1,
      customerName: {
        $concat: ["$customer.name.first", " ", "$customer.name.last"]
      },
      total: 1
  } }
])
```

Plain `$unwind: "$customer"` **drops** O6499. Add `preserveNullAndEmptyArrays: true` to keep it.""",
            "Demo 5.6 should show both behaviors once.",
            fit="fit-sm",
        )
    )

    s.append(
        split(
            "`$replaceRoot` and `$replaceWith`",
            [
                "Replace the pipeline document with a nested document",
                "`$mergeObjects` to keep a few parent fields",
                "Other parent fields are discarded",
            ],
            "090-replace-root.svg",
            "replaceWith and mergeObjects",
            "Rare in this course. Mention so they are not surprised in Compass recipes.",
        )
    )

    s.append(
        split(
            "The `$bucket` and `$bucketAuto` Stages",
            [
                "`$bucket` — you name the boundaries",
                "`$bucketAuto` — MongoDB picks approximate bins",
                "Lower bound inclusive, upper exclusive",
            ],
            "094-bucket-stage.svg",
            "Price bands",
            "Lab 5.7. A price of 50 enters the bucket that starts at 50.",
        )
    )

    s.append(
        split(
            "The `$facet` Stage",
            [
                "Same input, several sub-pipelines",
                "One output document",
                "Each facet value is an array",
            ],
            "101-facet-stage.svg",
            "One input many report arrays",
            "This is not a UI dashboard. It is one structured result.",
        )
    )

    s.append(
        content(
            "Multi-Metric Reports with `$facet`",
            """One report can return:

- Total order count and revenue
- Revenue by status
- Top customers
- Top products
- High-value order count

Filter **once** before `$facet` when every branch needs the same input (paid orders).""",
            "Lab 5.8. Product catalog facets belong on db.products, not inside the orders facet.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "Facet Output Structure",
            [
                "Exactly one output document",
                "Each facet key holds an **array**",
                "A single total is still `[{ orderCount: 13 }]`",
            ],
            "104-facet-output-structure.svg",
            "One document containing an array per report section",
            "Ask how many documents came back. The answer is one. That is Exercise 5.10.",
        )
    )

    s.append(
        split(
            "Demo 5.6 — Join Customers and Orders",
            [
                "20 minutes",
                "`$lookup` then unwind",
                "Build customerName; keep O6499 with preserve",
            ],
            "079-lookup-stage.svg",
            "Lookup customers",
            "Show the array first, then unwind. Never skip the array shape.",
        )
    )

    s.append(
        split(
            "Demo 5.7 — Multi-Metric Dashboard Result",
            [
                "20 minutes",
                "One `$facet` document",
                "Count, revenue, status, top customers, high-value",
            ],
            "101-facet-stage.svg",
            "Facet dashboard result",
            "Say dashboard result, then immediately: this is JSON, not Grafana.",
        )
    )

    s.append(
        ex_intro(
            "Exercise 5.9 — Join Related Collections",
            [
                "20 minutes",
                "Names, sort by total, unmatched O6499",
            ],
            "080-local-foreign-mapping.svg",
            "Local and foreign fields",
            "exercise-5.9-join-related-collections.md",
            "Exercise 5.9",
            "preserveNullAndEmptyArrays is the success criterion.",
        )
    )

    s.append(
        ex_steps(
            "Exercise 5.9 — Steps 1–2",
            [
                (
                    "Step 1 — Join and flatten",
                    "Lookup customers; unwind with preserve; project name and total; sort.",
                    "Most rows have names; totals descending.",
                ),
                (
                    "Step 2 — Find the unmatched order",
                    "Look for missing customerNumber.",
                    "O6499 still present.",
                ),
            ],
            "If O6499 vanished they used plain unwind.",
            "exercise-5.9-join-related-collections.md",
            "Exercise 5.9",
        )
    )

    s.append(
        ex_intro(
            "Exercise 5.10 — Build a `$facet` Report",
            [
                "20 minutes",
                "Five product facets in one document",
            ],
            "101-facet-stage.svg",
            "Facet report",
            "exercise-5.10-build-a-facet-report.md",
            "Exercise 5.10",
            "Run it. Ask how many documents came back. The answer is one.",
        )
    )

    s.append(
        ex_steps(
            "Exercise 5.10 — Steps 1–2",
            [
                (
                    "Step 1 — Build five facets",
                    "totals, byCategory, averagePrice, priceBands, mostExpensive.",
                    "One document; 12 products; L110 most expensive.",
                ),
                (
                    "Step 2 — Read each array",
                    "Which facets are one-element arrays?",
                    "totals and averagePrice.",
                ),
            ],
            "priceBands need numeric boundaries; Decimal128 prices still bucket.",
            "exercise-5.10-build-a-facet-report.md",
            "Exercise 5.10",
        )
    )

    s.append(
        ex_intro(
            "Lab 5.5 — Customer Order Summary",
            [
                "30 minutes",
                "Group paid spend, then lookup names",
            ],
            "116-customer-activity-pipeline.svg",
            "Customer activity pipeline",
            "lab-5.5-customer-order-summary.md",
            "Lab 5.5",
            "Lookup after group — one join per customer, not per order.",
        )
    )

    s.append(
        ex_steps(
            "Lab 5.5 — Steps 1–2",
            [
                (
                    "Step 1 — Group then lookup",
                    "Paid group by customerId; lookup; concat name; sort spending.",
                    "Aisha Khan first.",
                ),
                (
                    "Step 2 — Confirm C101",
                    "Sum O6101, O6201, O6301, O6306 totals by hand.",
                    "Matches totalSpending.",
                ),
            ],
            "C515 must not appear — only a FAILED order.",
            "lab-5.5-customer-order-summary.md",
            "Lab 5.5",
        )
    )

    s.append(
        ex_intro(
            "Lab 5.8 — Multi-Metric Report",
            [
                "30 minutes",
                "`$facet` on paid orders",
            ],
            "101-facet-stage.svg",
            "Multi-metric facet",
            "lab-5.8-multi-metric-report.md",
            "Lab 5.8",
            "High-value count 4 is the quick correctness check.",
        )
    )

    s.append(
        ex_steps(
            "Lab 5.8 — Steps 1–2",
            [
                (
                    "Step 1 — Paid then facet",
                    "totals, byFulfillment, topCustomers, topProducts, highValue.",
                    "orderCount 13; highValue 4; L110 top product.",
                ),
                (
                    "Step 2 — Describe the shape",
                    "Sketch keys; each value is an array.",
                    "Structured result, not a UI.",
                ),
            ],
            "Top-product branch must unwind; customer branch must not.",
            "lab-5.8-multi-metric-report.md",
            "Lab 5.8",
        )
    )

    s.append(
        content(
            "Pipeline Variables",
            """- `$fieldName` — current document field
- `$$variable` — defined variable
- `$$ROOT` — whole current document
- `$$CURRENT` — current processing context

```javascript
{ $map: {
    input: "$items",
    as: "item",
    in: { sku: "$$item.sku", quantity: "$$item.quantity" }
} }
```

`$filter` uses the same `$$item` convention.""",
            "One dollar for document fields, two for variables. Write that on the board.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "Handling Null and Missing Values",
            [
                "`$ifNull` supplies a default",
                "Missing shippingFee would break `$add`",
                "O6201, O6202, O6304 omit shippingFee",
            ],
            "039-ifnull-handling.svg",
            "ifNull default",
            "Prefer storing consistent data. Convert in the pipeline only when you must.",
        )
    )

    s.append(
        split(
            "Type Conversion in Aggregations",
            [
                "`$toDecimal` `$toDate` `$toString` `$toInt`",
                "`$convert` when you need onError / onNull",
                "Better: store consistent types",
            ],
            "040-type-conversion-flow.svg",
            "Conversion operators",
            "Do not $toDouble money. Stay on Decimal128.",
        )
    )

    s.append(
        split(
            "Date-Based Reporting",
            [
                "Group by `$dateToString` `%Y-%m`",
                "Or `$dateTrunc` to month",
                "State the time zone in production",
            ],
            "107-date-based-reporting.svg",
            "Date grouping operators",
            "Lab 5.6. Three months in this dataset: 2026-07 through 2026-09.",
        )
    )

    s.append(
        content(
            "Daily, Monthly, and Yearly Grouping",
            """`$dateToString` · `$dateTrunc` · `$year` · `$month` · `$dayOfMonth`

```javascript
{ $set: {
    month: { $dateTrunc: { date: "$createdAt", unit: "month" } }
} }
```

`$dateTrunc` returns a Date. `$dateToString` returns a sortable string. Pick one and stay consistent in the report.""",
            "String YYYY-MM is easier for them to read in mongosh.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "Building a Sales Summary Pipeline",
            [
                "`$match` paid",
                "`$set` reporting period",
                "`$group` by period with count, revenue, AOV",
                "`$sort` chronological; `$project` labels",
            ],
            "114-sales-summary-pipeline.svg",
            "Sales summary stages",
            "This is Lab 5.6 in eight words.",
        )
    )

    s.append(
        split(
            "Building a Product Performance Pipeline",
            [
                "Paid → unwind items → line revenue",
                "Group SKU → units and revenue",
                "Sort and limit to top products",
            ],
            "115-product-performance-pipeline.svg",
            "Product performance stages",
            "They already built this in Lab 5.4. Repeat so it becomes a pattern.",
        )
    )

    s.append(
        split(
            "Building a Customer Activity Pipeline",
            [
                "Paid → group customerId",
                "Lookup customer; concat name",
                "Sort by spending",
            ],
            "116-customer-activity-pipeline.svg",
            "Customer activity stages",
            "Join after grouping. That sentence is also Exercise 5.12.",
        )
    )

    s.append(
        ex_intro(
            "Lab 5.6 — Date-Based Sales Report",
            [
                "25 minutes",
                "Paid orders by calendar month",
            ],
            "107-date-based-reporting.svg",
            "Date reporting",
            "lab-5.6-date-based-sales-report.md",
            "Lab 5.6",
            "Sort _id ascending so July precedes September.",
        )
    )

    s.append(
        ex_steps(
            "Lab 5.6 — Steps 1–2",
            [
                (
                    "Step 1 — Month key and metrics",
                    "`$dateToString %Y-%m`; group; sort; rename reportingMonth.",
                    "Three rows: 2026-07, 2026-08, 2026-09.",
                ),
                (
                    "Step 2 — Optional time zone",
                    "Add `timezone: America/Toronto` and compare.",
                    "Production reports must name a zone.",
                ),
            ],
            "O5001 is September PENDING and must not appear.",
            "lab-5.6-date-based-sales-report.md",
            "Lab 5.6",
        )
    )

    s.append(
        ex_intro(
            "Lab 5.7 — Price-Band Analysis",
            [
                "20 minutes",
                "`$bucket` with business boundaries",
            ],
            "094-bucket-stage.svg",
            "Price bands",
            "lab-5.7-price-band-analysis.md",
            "Lab 5.7",
            "L190 at 499.99 is in 100–500. Ask someone why.",
        )
    )

    s.append(
        ex_steps(
            "Lab 5.7 — Steps 1–2",
            [
                (
                    "Step 1 — Define boundaries",
                    "`boundaries: [0, 50, 100, 500, 2000]`; push names.",
                    "Four buckets; under-50 has five products.",
                ),
                (
                    "Step 2 — Boundary rule",
                    "Where does price 50 go?",
                    "Into the bucket that starts at 50.",
                ),
            ],
            "default: Other catches anything outside the list — none today.",
            "lab-5.7-price-band-analysis.md",
            "Lab 5.7",
        )
    )

    s.append(
        split(
            "Pipeline Development Workflow",
            [
                "Start small; add one stage; inspect",
                "Verify calculations on a sample",
                "Shape output last",
                "Review performance after correctness",
            ],
            "010-development-workflow.svg",
            "Incremental pipeline workflow",
            "This is Demo 5.1 turned into a habit. Exercise 5.11 is what happens when they skip it.",
        )
    )

    s.append(
        split(
            "Pipeline Optimization Principles",
            [
                "Filter early when possible",
                "Do not carry huge unused fields",
                "Control `$unwind` and `$lookup`",
                "Correctness before milliseconds",
            ],
            "125-optimization-overview.svg",
            "Optimization practices",
            "Module 6 will add real indexes. Today they learn what those indexes will support.",
        )
    )

    s.append(
        split(
            "`$match` Placement",
            [
                "Early `$match` filters source documents",
                "Late `$match` filters grouped results",
                "Both are valid — different questions",
            ],
            "013-source-vs-group-match.svg",
            "Match placement",
            "Paid then group by status versus group then match SHIPPED summaries.",
        )
    )

    s.append(
        split(
            "Early vs. Late `$match`",
            [
                "Early: fewer documents enter expensive stages",
                "Late: you are filtering **groups**, not source rows",
                "Put source filters first; put summary filters after `$group`",
            ],
            "126-early-vs-late-match.svg",
            "Filtering before expensive stages versus processing extra documents",
            "This is the performance version of stage-order-matters. Same picture, cost language.",
        )
    )

    s.append(
        content(
            "`$project` Placement",
            """Projection can shrink documents, but:

- Do not drop fields you still need
- MongoDB may optimize field use anyway
- Correctness and readability come first
- Final `$project` is for the report shape

Early `$unset` of `shippingAddress` is fine if no later stage needs it.""",
            "Do not project away items before unwind. That silence is the tip.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "Index Use in Aggregation",
            [
                "Helps when the pipeline starts with `$match` / `$sort`",
                "Example: PAID then sort `createdAt`",
                "Compound index design is Module 6",
            ],
            "127-index-supported-match.svg",
            "Indexes help early match and sort",
            "Do not create a dozen indexes today. Name one candidate.",
        )
    )

    s.append(
        split(
            "Collection Scan vs. Index Scan",
            [
                "COLLSCAN reads every document",
                "IXSCAN navigates matching keys",
                "Seventeen docs will not prove speed — prove the **plan**",
            ],
            "134-collscan-vs-ixscan.svg",
            "Every document examined versus targeted index navigation",
            "Lab 5.9. Reset the goal: winning plan shape, not milliseconds.",
        )
    )

    s.append(
        content(
            "Reading Aggregation Explain Output",
            """```javascript
db.orders.explain("executionStats").aggregate([
  { $match: { paymentStatus: "PAID" } },
  { $sort: { createdAt: -1 } }
])
```

Look for: collection scan vs index scan, documents examined, keys examined, sort behavior, time.

Seventeen documents will not produce a dramatic speedup — read the **plan shape**.""",
            "Lab 5.9. If they hunt for milliseconds they will be disappointed. Reset the goal.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "Common Aggregation Mistakes",
            [
                "Wrong stage order; missing `$` on fields",
                "Grouping before unwind; summing order total per line",
                "`$lookup` treated as an object; `$limit` before `$sort`",
            ],
            "159-ex-5-11-broken-stage.svg",
            "Common mistakes",
            "Exercise 5.11 packs these into one broken pipeline. Leave this grid visible.",
        )
    )

    s.append(
        split(
            "Missing `$` Field Reference",
            [
                "`\"category\"` groups everything into one literal bucket",
                "`\"$category\"` groups by the field value",
                "The pipeline still runs. The numbers look wrong.",
            ],
            "139-missing-dollar-reference.svg",
            "Literal text compared with the document field value",
            "Show both $group outputs side by side before they debug Exercise 5.11.",
        )
    )

    s.append(
        split(
            "Double-Counting After `$unwind`",
            [
                "Parent `total` is copied onto every item row",
                "`$sum: \"$total\"` repeats the order once per SKU",
                "Sum line revenue instead: quantity × unitPrice",
            ],
            "147-double-counting-after-unwind.svg",
            "Parent-level values summed once per array element",
            "Exercise 5.12. O6301 would contribute its total twice if they sum order total after unwind.",
        )
    )

    s.append(
        split(
            "Aggregation Troubleshooting Workflow",
            [
                "Confirm collection and a sample document",
                "Run one stage; add one; inspect shape",
                "Check paths, types, arrays, group keys",
                "Manual sample, then explain()",
            ],
            "138-troubleshooting-workflow.svg",
            "Troubleshooting steps",
            "If they jump to explain() on a wrong result they will optimize a bug.",
        )
    )

    s.append(
        split(
            "Demo 5.8 — Inspect Pipeline Execution",
            [
                "15 minutes",
                "Late `$match` versus early `$match`",
                "Name an index for Module 6",
            ],
            "127-index-supported-match.svg",
            "Explain aggregation",
            "Optionally create { paymentStatus: 1, createdAt: -1 }, show IXSCAN, then drop it so Module 6 starts clean — your call.",
        )
    )

    s.append(
        ex_intro(
            "Exercise 5.11 — Correct a Broken Pipeline",
            [
                "15 minutes",
                "Seven defects in one pipeline",
            ],
            "159-ex-5-11-broken-stage.svg",
            "Common mistakes",
            "exercise-5.11-correct-a-broken-pipeline.md",
            "Exercise 5.11",
            "Do not let them rewrite from memory without naming defects first.",
        )
    )

    s.append(
        ex_steps(
            "Exercise 5.11 — Steps 1–2",
            [
                (
                    "Step 1 — List the defects",
                    "Stage order, missing `$`, nested paths, no unwind, lookup as object.",
                    "At least five defects named.",
                ),
                (
                    "Step 2 — Rewrite and run",
                    "Paid, unwind, lineRevenue, group sku, sort, limit 5.",
                    "L110 first; lookup not required.",
                ),
            ],
            "Celebrate the defect list more than the pretty pipeline.",
            "exercise-5.11-correct-a-broken-pipeline.md",
            "Exercise 5.11",
        )
    )

    s.append(
        ex_intro(
            "Exercise 5.12 — Optimize a Pipeline",
            [
                "15 minutes · discussion",
                "Lookup later; do not unwind to sum totals",
            ],
            "125-optimization-overview.svg",
            "Optimization",
            "exercise-5.12-optimize-a-pipeline.md",
            "Exercise 5.12",
            "Equivalence matters. Cheaper but wrong is not an optimization.",
        )
    )

    s.append(
        ex_steps(
            "Exercise 5.12 — Steps 1–2",
            [
                (
                    "Step 1 — Name the costs",
                    "Early lookup, unwind before match, summing total after unwind.",
                    "Multi-item orders would be double-counted.",
                ),
                (
                    "Step 2 — Write the cheaper equivalent",
                    "Match paid, group customerId, lookup, match ACTIVE.",
                    "Named index paymentStatus + customerId.",
                ),
            ],
            "Optional: paste both versions in mongosh and compare spent for C101.",
            "exercise-5.12-optimize-a-pipeline.md",
            "Exercise 5.12",
        )
    )

    s.append(
        ex_intro(
            "Lab 5.9 — Pipeline Performance Review",
            [
                "20 minutes",
                "`explain(\"executionStats\")` two orderings",
            ],
            "127-index-supported-match.svg",
            "Explain output",
            "lab-5.9-pipeline-performance-review.md",
            "Lab 5.9",
            "Tiny data. Grade the written plan notes, not the elapsed millis.",
        )
    )

    s.append(
        ex_steps(
            "Lab 5.9 — Steps 1–2",
            [
                (
                    "Step 1 — Explain a late filter",
                    "Sort createdAt then match PAID; record examined docs.",
                    "Likely COLLSCAN of 17 orders.",
                ),
                (
                    "Step 2 — Match earlier",
                    "Match then sort; name `{ paymentStatus: 1, createdAt: -1 }`.",
                    "Same question, better stage order.",
                ),
            ],
            "Park index creation for Module 6 unless you demo and drop.",
            "lab-5.9-pipeline-performance-review.md",
            "Lab 5.9",
        )
    )

    s.append(
        split(
            "Module Summary",
            [
                "Pipelines are ordered transformations",
                "`$match` `$project` `$set` `$group` `$unwind` `$lookup` `$facet`",
                "Stage order changes meaning and cost",
            ],
            "000-module-5-concept-map.svg",
            "Module 5 concept map",
            "Point at each box. Tomorrow those pipelines get indexes.",
        )
    )

    s.append(
        content(
            "Module Knowledge Check",
            """1. What does a pipeline do?
2. Why does stage order matter?
3. `$project` versus `$set`?
4. What is `$group._id`?
5. How is `$sum: 1` used?
6. When is `$unwind` required?
7. What does `$lookup` return?
8. Purpose of `$facet`?
9. How do you handle nulls?
10. Why put selective `$match` early?
11. Why is `$limit` before `$sort` wrong for top-N?
12. What must be true before you optimize?""",
            "Paper or chat. You need evidence they can unwind and group, not only recite stage names.",
            fit="fit-sm",
        )
    )

    s.append(
        ex_intro(
            "Lab 5.10 — Integrated Aggregation Challenge",
            [
                "40 minutes",
                "Monthly performance report",
                "Required stages listed in the guide",
            ],
            "171-practical-challenge.svg",
            "Monthly report challenge",
            "lab-5.10-integrated-aggregation-challenge.md",
            "Lab 5.10",
            "July check: O6101–O6103. If unique customer count is 17 they counted orders not customers.",
        )
    )

    s.append(
        ex_steps(
            "Lab 5.10 — Steps 1–2",
            [
                (
                    "Step 1 — Monthly core metrics",
                    "Paid, month key, group count/revenue/AOV/`$addToSet` customers.",
                    "Three months; `$size` unique customers.",
                ),
                (
                    "Step 2 — Units, top product, status",
                    "Other facet branches; sort months; save sample output.",
                    "Every required stage used; July validated by hand.",
                ),
            ],
            "Step 3 in the guide is the index recommendation.",
            "lab-5.10-integrated-aggregation-challenge.md",
            "Lab 5.10",
        )
    )

    s.append(
        ex_intro(
            "Exercise 5.13 — Executive Sales Summary",
            [
                "30–45 minutes",
                "Date-bounded paid report plus catalog bands",
            ],
            "171-practical-challenge.svg",
            "Executive sales summary",
            "exercise-5.13-executive-sales-summary.md",
            "Exercise 5.13",
            "If time is short, assign as take-home. Grade stage order and sources, not pixel-perfect JSON.",
        )
    )

    s.append(
        ex_steps(
            "Exercise 5.13 — Steps 1–2",
            [
                (
                    "Step 1 — Collections and date filter",
                    "Orders for 1–6; products for 7–8; ISODate range; PAID.",
                    "Pending orders excluded.",
                ),
                (
                    "Step 2 — Structure the output",
                    "`$facet`; lookup only on top customers; defend order and one index.",
                    "Top product L110; top customer C101.",
                ),
            ],
            "Evaluation criteria are in the lab guide. Use them as a rubric.",
            "exercise-5.13-executive-sales-summary.md",
            "Exercise 5.13",
        )
    )

    s.append(
        content(
            "Module Completion Checklist",
            """Participants can:

- Explain pipeline processing
- Build multi-stage aggregations
- Filter and reshape documents
- Create calculated fields
- Group by one or more fields
- Use accumulator operators
- Process arrays with `$unwind`
- Join with `$lookup`
- Build bucketed and `$facet` reports
- Handle missing values and types
- Validate calculations
- Identify basic performance improvements""",
            "If a laptop failed Lab 5.10, Demo 5.1 plus Lab 5.4 still meet the conceptual bar.",
            fit="fit-md",
        )
    )

    s.append(
        content(
            "Questions and Answers",
            """Open questions on:

- Stage order in *their* reports
- When to unwind versus `$filter`
- Whether `$lookup` means they modeled wrong
- What they will index tomorrow

Park replica-set and shard-key questions for Module 7.""",
            "Time-box 10 minutes. Write parking-lot items for Day 3.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "Day 2 path through aggregation",
            [
                "Filter with `$match`",
                "Shape with `$set` / `$project`",
                "Summarize with `$group`",
                "Report with `$facet`",
            ],
            "008-business-question-to-pipeline.svg",
            "Day 2 aggregation path",
            "Congratulate them. They wrote analytical queries on the same store they modeled yesterday.",
        )
    )

    s.append(
        content(
            "Transition to Module 6: Indexing",
            """Module 6 connects these pipelines to performance:

- Index structures
- Single-field and compound indexes
- Multikey, unique, text, and specialized indexes
- Prefixes and field order
- Covered queries
- Execution plans
- Maintenance and tradeoffs

Bring tomorrow’s laptop on the same connection string. Keep today’s pipelines.""",
            "If data is missing, run load.js before they leave.",
            fit="fit-md",
        )
    )

    return "\n\n---\n\n".join(s) + "\n"


def main() -> None:
    section = build()
    text = DECK.read_text(encoding="utf-8")
    if MARKER in text:
        start = text.index(MARKER)
        if NEXT_MODULE in text[start:]:
            end = text.index(NEXT_MODULE, start)
            text = text[:start].rstrip() + "\n\n---\n\n" + section.rstrip() + "\n\n---\n\n" + text[end:]
            print("Replaced Module 5 section (kept later modules)")
        else:
            text = text[:start].rstrip() + "\n\n---\n\n" + section
            print("Replaced Module 5 section through end of deck")
    else:
        if NEXT_MODULE in text:
            end = text.index(NEXT_MODULE)
            prefix = text[:end].rstrip()
            if prefix.endswith("---"):
                prefix = prefix[: -3].rstrip()
            text = prefix + "\n\n---\n\n" + section.rstrip() + "\n\n---\n\n" + text[end:]
            print("Inserted Module 5 section before Module 6")
        else:
            text = text.rstrip() + "\n\n---\n\n" + section
            print("Appended Module 5 section")
    DECK.write_text(text, encoding="utf-8")
    slides = text.count("\n---\n")
    print(f"Wrote {DECK} (~{slides} slide separators)")


if __name__ == "__main__":
    main()
