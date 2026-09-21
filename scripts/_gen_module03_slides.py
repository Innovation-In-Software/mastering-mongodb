"""Generate Module 3 Marp section and append it to the course deck.

Run from repo root:
    python scripts/_gen_module03_slides.py
"""
from __future__ import annotations

from pathlib import Path

DECK = Path(__file__).resolve().parent.parent / "slides" / "course-complete-marp-with-notes.md"
MARKER = "<!-- _header: 'Module 3 — Data Modeling with MongoDB' -->"


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

<img src="assets/module-03/{img}" alt="{alt}" width="720">

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

**Lab guide:** [`{label}`](../slide-exercises/module-03/{guide})

</div>
<div class="col-visual">

<img src="assets/module-03/{img}" alt="{alt}" width="720">

</div>
</div>

{notes(title, script)}"""
    return slide("split", body)


def ex_steps(heading: str, steps: list[tuple[str, str, str]], script: str, guide: str | None, label: str | None) -> str:
    blocks = []
    if guide and label:
        blocks.append(f"**Lab guide:** [`{label}`](../slide-exercises/module-03/{guide})")
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
        """<!-- _header: 'Module 3 — Data Modeling with MongoDB' -->

<!-- _class: lead -->

# Data Modeling with MongoDB

Effective MongoDB schemas are designed around how an application reads, writes, and changes data

"""
        + notes(
            "Data Modeling with MongoDB",
            "Open Module 3. They have a working mongosh session from Module 2 and have already seen documents in Module 1. Today they design the training_store schema they will query on Day 2. Flexible schema is not an excuse to skip design.",
        )
    )

    s.append(
        content(
            "Module Learning Objectives",
            """By the end of this module you will be able to:

- Interpret MongoDB document structures
- Select appropriate BSON types
- Identify common access patterns
- Model relationships with embedding or references
- Control document and array growth
- Apply schema-validation rules
- Design the course sample application database""",
            "Read the outcomes. The product of this module is a justified schema plus populated collections — not a diagram that copies relational tables.",
        )
    )

    s.append(
        split(
            "Why Data Modeling Matters",
            [
                "Efficient retrieval",
                "Safer related updates",
                "Predictable document shape",
                "Indexes that match queries",
                "**Key message:** MongoDB removes rigid tables, not the need for design",
            ],
            "01-why-data-modeling-matters.svg",
            "Good model outcomes versus poor model problems",
            "A poor model shows up as application-side joins, unbounded arrays, oversized documents, and inconsistent field names. Ask who has seen a collection that grew into an accidental dumping ground.",
        )
    )

    s.append(
        split(
            "MongoDB Data Hierarchy",
            [
                "Deployment → database → collection → document",
                "A document holds fields, nested documents, and arrays",
                "This course uses **training_store**",
            ],
            "02-mongodb-data-hierarchy.svg",
            "Hierarchy from deployment down to fields",
            "Repeat the hierarchy from Module 1, then name the four collections they will own: products, customers, orders, reviews.",
        )
    )

    s.append(
        split(
            "Databases, Collections, and Documents",
            [
                "**Database:** logical container",
                "**Collection:** related documents",
                "**Document:** field-value pairs",
                "**Field:** a named element inside a document",
            ],
            "03-databases-collections-documents.svg",
            "Database to collection to document to field",
            "Show the tiny product example on the next slide. Do not linger on syntax — they already inserted a test document in Module 2.",
        )
    )

    s.append(
        content(
            "A Product Document",
            """```javascript
{
  _id: ObjectId("..."),
  sku: "P1001",
  name: "Wireless Keyboard",
  price: 49.99
}
```

Collection: `products` in database `training_store`.

`sku` is a **business** identifier. `_id` is the **document** identifier.""",
            "Point at each field. Price as a plain number is a teaching shortcut — Decimal128 is the production type for money, coming in two slides.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "Anatomy of a MongoDB Document",
            [
                "Unique identifier",
                "String, decimal, Boolean, date",
                "Array",
                "Embedded document",
            ],
            "04-anatomy-of-a-document.svg",
            "Document labeled with BSON shapes",
            "Have the room shout the type of each field before you reveal. Decimal128 versus Double is the money trap.",
            fit="fit-md",
        )
    )

    s.append(
        content(
            "Anatomy — labeled example",
            """```javascript
{
  _id: ObjectId("..."),
  name: "Wireless Keyboard",
  price: Decimal128("49.99"),
  active: true,
  tags: ["wireless", "accessories"],
  specifications: {
    connection: "Bluetooth",
    batteryLifeMonths: 12
  },
  createdAt: ISODate("2026-09-20T10:00:00Z")
}
```""",
            "Walk top to bottom. specifications is a nested document, not an array. tags is an array of strings.",
            fit="fit-sm",
        )
    )

    s.append(
        split(
            "Understanding BSON Data Types",
            [
                "Type choice affects precision, sorting, comparison, and storage",
                "Money → **Decimal128**, not Double",
                "Timestamps → **Date**, not display strings",
            ],
            "05-bson-data-types.svg",
            "BSON types and typical uses",
            "Null is an intentional empty value. Missing field and null are not the same in queries — Module 4 will show that.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "ObjectId and the `_id` Field",
            [
                "Every document needs a unique `_id`",
                "MongoDB often generates an ObjectId",
                "You may supply a business key instead",
                "Indexed automatically and treated as immutable",
            ],
            "06-objectid-and-id.svg",
            "Default ObjectId versus application-defined _id",
            "Either ObjectId or sku-as-_id is valid. Mixing both in one collection without a rule is not. References usually store the target _id.",
        )
    )

    s.append(
        split(
            "Nested Documents",
            [
                "Related data as an embedded object",
                "Fits when the child belongs to the parent",
                "Retrieved with the parent",
                "Stays bounded",
            ],
            "07-nested-documents.svg",
            "Customer with embedded address",
            "Aisha’s address is a classic embed. If many employees share one office record that is updated centrally, you might reference instead.",
        )
    )

    s.append(
        split(
            "Arrays in MongoDB Documents",
            [
                "Scalar arrays: tags, colors",
                "Arrays of documents: order items",
                "**Warning:** growth must stay predictable",
            ],
            "08-arrays-in-documents.svg",
            "Scalar array versus array of documents",
            "Order items for a checkout are bounded. All reviews ever written are not. That distinction is the rest of this module.",
        )
    )

    s.append(
        split(
            "Flexible Schema Explained",
            [
                "Documents in one collection may have different fields",
                "Laptop, book, and shoe can share `products`",
                "New fields do not require a table migration",
            ],
            "09-flexible-schema.svg",
            "Three product categories in one collection",
            "This is why catalogs fit MongoDB. Shared core still exists — they will write it in Exercise 3.4.",
        )
    )

    s.append(
        split(
            "Flexible Schema Does Not Mean No Schema",
            [
                "Required fields and names",
                "Data types and allowed values",
                "How relationships are represented",
                "Date formats and versioning",
            ],
            "10-schema-conventions.svg",
            "Inconsistent price fields versus a single Decimal128 convention",
            "Show the anti-example: price, productPrice, item_cost. That is not flexibility — that is three bugs.",
        )
    )

    s.append(
        content(
            "Demo 3.1 — Inspect a BSON Document",
            """**Duration:** 10 minutes · instructor `mongosh`

```javascript
use training_store
db.products.findOne()
```

Identify live: `_id`, strings, numbers, Boolean, Date, array, nested document.

If the collection is empty, insert the anatomy example first.""",
            "Project mongosh. Cold-call types. If they still have Module 1 data, a product findOne is enough. If empty, insert one document and inspect it.",
            fit="fit-md",
        )
    )

    s.append(
        ex_intro(
            "Exercise 3.1 — Identify Document Components",
            [
                "10 minutes · pairs",
                "Label every shape on the sample customer",
                "Then list candidate required fields",
            ],
            "48-ex-3-1-document-components.svg",
            "Callouts for _id, scalars, embedded name, tags, date",
            "exercise-3.1-identify-document-components.md",
            "Exercise 3.1",
            "Time-box 10 minutes. Do not skip required fields — that list becomes validation later.",
        )
    )

    s.append(
        ex_steps(
            "Exercise 3.1 — Steps 1–2",
            [
                (
                    "Step 1 — Label identifier, scalars, and the nested name",
                    "Mark `_id`, scalar fields, and embedded `name`. What does `_id` guarantee?",
                    "`_id` unique; `customerNumber`/`email` scalars; `name` nested.",
                ),
                (
                    "Step 2 — Label array, Boolean, date, and required fields",
                    "Mark `tags`, `active`, `createdAt`. List fields every customer should have.",
                    "Array, Boolean, Date labeled; required list includes identity and contact.",
                ),
            ],
            "Debrief by pointing at the slide document. Required-field candidates: customerNumber, name, email, active, createdAt.",
            "exercise-3.1-identify-document-components.md",
            "Exercise 3.1",
        )
    )

    s.append(
        split(
            "Relational Modeling vs Document Modeling",
            [
                "Relational: normalize first, join later",
                "Document: start with access patterns",
                "Store related data together when it is used together",
            ],
            "11-relational-vs-document.svg",
            "Relational approach compared with document approach",
            "The failure mode is cloning every table as a collection of tiny documents. That keeps the joins and loses the document benefit.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "Model Data Around Access Patterns",
            [
                "What is requested, how often, which filters",
                "What must return together",
                "How the data changes and how large it gets",
            ],
            "12-model-around-access-patterns.svg",
            "Questions that define an access pattern",
            "Read the order example aloud. That single sentence is why an order is usually one aggregate, not four tables at read time.",
        )
    )

    s.append(
        split(
            "Identify Application Workloads",
            [
                "Hot reads and hot writes",
                "Critical transactions and reports",
                "Retention, growth, ownership, consistency",
            ],
            "13-application-workloads.svg",
            "Workload questions before drawing collections",
            "Ask the room for their current app’s hottest query. Modeling without that answer is guessing.",
        )
    )

    s.append(
        split(
            "Read and Write Access Patterns",
            [
                "Reads: locate, return, latency",
                "Writes: which fields, how often, concurrency",
                "One fast read can make writes harder",
            ],
            "14-read-write-access-patterns.svg",
            "Read considerations versus write considerations",
            "Embedding order items makes checkout reads fast and catalog-wide price fixes harder. That is an acceptable tradeoff when the item price is a snapshot.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "Data That Is Accessed Together",
            [
                "Often stored together",
                "Order number, items, prices, address, status",
                "A **signal**, not an unconditional rule",
            ],
            "15-data-accessed-together.svg",
            "Order fields retrieved in one read",
            "If they always paint those fields on one screen, one document is the default. Reviews on the same screen as the product are the counterexample — too many to embed.",
        )
    )

    s.append(
        split(
            "Data That Changes Together",
            [
                "Same aggregate and lifecycle → embed",
                "Order quantity and purchase-time price",
                "Current catalog description has a different lifecycle",
            ],
            "16-data-changes-together.svg",
            "Same lifecycle embed versus different lifecycle reference",
            "Created together, updated together, removed together is the embed checklist.",
        )
    )

    s.append(
        content(
            "Demo 3.2 — Compare Relational and Document Models",
            """**Duration:** 15 minutes

Show five tables: `customers`, `orders`, `order_items`, `products`, `addresses`.

Then one **order document**: customer reference, embedded items, shipping snapshot, status, total.

**Outcome:** modeling focuses on aggregates and access patterns, not on 1:1 table copies.""",
            "Sketch the star of tables on a whiteboard if you can. Then paste the order document. Count the joins they would have needed.",
            fit="fit-md",
        )
    )

    s.append(
        ex_intro(
            "Exercise 3.2 — Discover Access Patterns",
            [
                "15 minutes · requirements analysis",
                "E-commerce: search, PDP, profile, orders, reviews",
                "Fill frequency, required data, modeling implication",
            ],
            "49-ex-3-2-access-patterns.svg",
            "Access-pattern table with modeling implications",
            "exercise-3.2-discover-access-patterns.md",
            "Exercise 3.2",
            "They will use this table to justify embed vs reference for the rest of the day. Do not accept ‘store everything in one document.’",
        )
    )

    s.append(
        ex_steps(
            "Exercise 3.2 — Steps 1–2",
            [
                (
                    "Step 1 — List the high-frequency reads",
                    "Name the three hottest operations and the data each response must include.",
                    "Typically: product by SKU, order by number, customer profile.",
                ),
                (
                    "Step 2 — Fill the access-pattern table",
                    "At least four rows: frequency, required data, embed / reference / snapshot.",
                    "Retrieve-order implies an embedded aggregate; reviews imply a separate collection.",
                ),
            ],
            "Collect two tables on the board. Align on find-product, retrieve-order, list-orders-for-customer, paginate-reviews.",
            "exercise-3.2-discover-access-patterns.md",
            "Exercise 3.2",
        )
    )

    s.append(
        split(
            "Relationship Types",
            [
                "One-to-one, one-to-few, one-to-many",
                "One-to-squillions, many-to-many",
                "Size, growth, ownership, and access direction decide the shape",
            ],
            "17-relationship-types.svg",
            "Cardinality spectrum from 1:1 to many-to-many",
            "Squillions is informal on purpose — it means ‘will not fit in the parent document.’ Reviews and transactions live there.",
        )
    )

    s.append(
        split(
            "One-to-One Relationships",
            [
                "Embed when the child exists only as part of the parent",
                "Reference when the child has its own lifecycle",
            ],
            "18-one-to-one.svg",
            "Embedded contact versus referenced profile",
            "Most 1:1 owned data should be embedded. Splitting a customer from their only email object is usually relational habit.",
        )
    )

    s.append(
        split(
            "One-to-Many Relationships",
            [
                "**One-to-few:** addresses, images, order items — embed",
                "**One-to-many / unbounded:** orders, reviews, transactions — reference",
            ],
            "19-one-to-many.svg",
            "One-to-few embed versus one-to-many reference",
            "Ask how many addresses a customer has (few) versus how many orders (unbounded). Same parent, different representation.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "Many-to-Many Relationships",
            [
                "Products belong to many categories",
                "Store `categoryIds` on the product — or the reverse",
                "Choice depends on navigation and update cost",
            ],
            "20-many-to-many.svg",
            "Products and categories linked by identifier arrays",
            "If the UI always starts from a product, put category ids on the product. If it always starts from a category browse, you may store product ids on the category — or accept $lookup.",
        )
    )

    s.append(
        split(
            "Embedding Related Data",
            [
                "One operation retrieves the aggregate",
                "Single-document updates are atomic",
                "Risks: duplication, growth, bulk updates",
            ],
            "21-embedding.svg",
            "Advantages and risks of embedding",
            "Atomic here means one document, one write. It is not a multi-document transaction lecture — that is later if they ask.",
        )
    )

    s.append(
        split(
            "Referencing Related Data",
            [
                "Store the other document’s `_id`",
                "Independent lifecycle, high cardinality",
                "Tradeoff: extra queries or `$lookup`",
            ],
            "22-referencing.svg",
            "Order referencing a customer document",
            "Do not pretend references are free. Application code must fetch or join. That cost is why we copy a few stable fields later (extended reference).",
        )
    )

    s.append(
        split(
            "Embedding vs Referencing",
            [
                "Embed owned, bounded, read-together data",
                "Reference independent or unbounded data",
                "Use the table; do not memorize slogans only",
            ],
            "23-embed-vs-reference.svg",
            "Considerations for embed versus reference",
            "Leave this slide up during Exercise 3.3. It is the decision card.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "Data Duplication and Denormalization",
            [
                "Copy selected fields to speed reads",
                "Order item stores name and purchase-time price",
                "The catalog may change later — that is the point",
            ],
            "24-denormalization.svg",
            "Intentional copies of name and unit price",
            "Duplication is a design choice with an update policy, not an accident.",
        )
    )

    s.append(
        content(
            "Maintaining Duplicated Data",
            """Ask: **must the copy always match the source?**

Possible strategies:

- Treat it as a historical snapshot
- Update in the application
- Update asynchronously
- Rebuild periodically
- Allow eventual consistency
- Copy only stable fields""",
            "For orders, the answer is almost always snapshot. For a denormalized customer name on an invoice PDF, same. For a denormalized ‘member tier’ on every order, maybe sync.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "Modeling Historical Snapshots",
            [
                "Orders keep purchase-time name, price, tax, address",
                "A later catalog change must not rewrite history",
            ],
            "25-historical-snapshots.svg",
            "Purchase-time facts preserved on the order",
            "Legal and finance care about this. If they only remember one slide from relationships, make it this one.",
        )
    )

    s.append(
        split(
            "Modeling Product Catalogs",
            [
                "Shared core: sku, name, category, price, active",
                "Category-specific data under `attributes`",
            ],
            "26-product-catalog.svg",
            "Core product fields plus nested attributes",
            "This is the polymorphic / attribute hybrid they will type in Exercise 3.4 and Lab 3.2.",
        )
    )

    s.append(
        split(
            "Modeling Customer Profiles",
            [
                "Identity, contact, bounded addresses",
                "Preferences, status, timestamps",
                "Orders are **not** an array on the customer",
            ],
            "27-customer-profile.svg",
            "Customer profile with nested name, contact, and addresses",
            "A lifetime of orders on the customer document is the unbounded-array trap with a friendly name.",
        )
    )

    s.append(
        split(
            "Modeling Orders",
            [
                "The order is usually one aggregate",
                "Embed: items, prices, shipping snapshot",
                "Reference: customer, current product",
            ],
            "28-order-aggregate.svg",
            "Embedded order fields versus referenced ids",
            "Demo 3.3 builds this document field by field. Keep this diagram visible while you type.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "Modeling Time-Series and Event Data",
            [
                "Source, type, timestamp, value, metadata",
                "High write volume and retention dominate the design",
                "Often a **bucket**, not one document per event",
            ],
            "29-time-series-events.svg",
            "Event document and design concerns",
            "Do not deep-dive time-series collections unless asked. The bucket pattern is the portable idea.",
        )
    )

    s.append(
        content(
            "Demo 3.3 — Model an E-Commerce Order",
            """**Duration:** 15 minutes

Access pattern: *Retrieve a complete order by order number.*

Build live:

1. Order identity
2. Customer reference
3. Embedded items
4. Purchase-time price
5. Shipping-address snapshot
6. Status and timestamps
7. Monetary totals""",
            "Type this in mongosh or a scratch file. After each step, ask whether that field is snapshot, reference, or live. Do not skip totals as Decimal128.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "Demo 3.4 — Embed and Reference Related Data",
            [
                "Address on customer → embed",
                "Orders for a customer → reference",
                "Items on an order → embed",
                "Reviews for a product → reference",
            ],
            "54-demo-embed-reference.svg",
            "Four relationships with embed or reference and why",
            "For each row, walk ownership, cardinality, growth, query, and update frequency. Fifteen minutes if you include class debate.",
            fit="fit-md",
        )
    )

    s.append(
        ex_intro(
            "Exercise 3.3 — Embed or Reference?",
            [
                "15 minutes · eight relationships",
                "Justify with ownership, cardinality, growth",
                "Only office address is a true ‘it depends’",
            ],
            "50-ex-3-3-embed-or-reference.svg",
            "Expected embed versus reference choices",
            "exercise-3.3-embed-or-reference.md",
            "Exercise 3.3",
            "Reveal the answer table only after Step 2. Challenge anyone who embeds millions of reviews.",
        )
    )

    s.append(
        ex_steps(
            "Exercise 3.3 — Steps 1–2",
            [
                (
                    "Step 1 — Decide relationships 1–4",
                    "Contact, complete order history, line items, millions of reviews.",
                    "Embed, reference, embed, reference.",
                ),
                (
                    "Step 2 — Decide relationships 5–8",
                    "Office address, blog tags, purchase-time price, full transaction history.",
                    "Depends / embed / embed snapshot / reference.",
                ),
            ],
            "Office address: embed if it belongs only to that employee; reference if many people share a managed office record.",
            "exercise-3.3-embed-or-reference.md",
            "Exercise 3.3",
        )
    )

    s.append(
        ex_intro(
            "Exercise 3.4 — Model a Product Catalog",
            [
                "20 minutes · laptop, shoe, book",
                "Same core fields, different attributes",
                "One `products` collection",
            ],
            "09-flexible-schema.svg",
            "Three product types sharing a collection",
            "exercise-3.4-model-a-product-catalog.md",
            "Exercise 3.4",
            "If they create three collections, send them back. Polymorphic pattern is the point.",
        )
    )

    s.append(
        ex_steps(
            "Exercise 3.4 — Steps 1–2",
            [
                (
                    "Step 1 — Design the shared core",
                    "Name fields and BSON types. Decide where type-specific data lives.",
                    "sku, name, description, category, price, active, createdAt — same names for all.",
                ),
                (
                    "Step 2 — Write three documents",
                    "One laptop, one shoe, one book with nested `attributes`.",
                    "Core is identical; processor versus isbn lives under attributes.",
                ),
            ],
            "Spot-check Decimal128 and Date. Inconsistent price field names are the fail.",
            "exercise-3.4-model-a-product-catalog.md",
            "Exercise 3.4",
        )
    )

    s.append(
        ex_intro(
            "Exercise 3.5 — Model an Order Document",
            [
                "20 minutes · one aggregate",
                "Find by order number; list by customer",
                "Preserve purchase-time prices and ship-to address",
            ],
            "28-order-aggregate.svg",
            "Order aggregate with embedded items and referenced customer",
            "exercise-3.5-model-an-order-document.md",
            "Exercise 3.5",
            "This is the shape Lab 3.4 will insert. Collect one volunteer document on the projector.",
        )
    )

    s.append(
        ex_steps(
            "Exercise 3.5 — Steps 1–2",
            [
                (
                    "Step 1 — Decide embed versus reference",
                    "Items, price, shipping address, customer — mark snapshots.",
                    "Items/prices/address embedded snapshots; customerId referenced.",
                ),
                (
                    "Step 2 — Write the document and required fields",
                    "Include statuses, Decimal128 totals, createdAt, and a required list.",
                    "A complete order object plus a one-read-by-order-number justification.",
                ),
            ],
            "If they embed the entire current product, ask what happens when the catalog description changes.",
            "exercise-3.5-model-an-order-document.md",
            "Exercise 3.5",
        )
    )

    s.append(
        split(
            "Unbounded Arrays",
            [
                "`allReviews: [ /* millions */ ]` will hurt",
                "Large docs, expensive updates, 16 MiB risk",
                "Put high-cardinality children in their own collection",
            ],
            "30-unbounded-arrays.svg",
            "Danger of unbounded reviews array and the better design",
            "This is the anti-pattern they must be able to name on the exit ticket.",
        )
    )

    s.append(
        split(
            "The 16 MiB Document Limit",
            [
                "Hard maximum per BSON document",
                "Stay **comfortably** smaller",
                "Forces bounded aggregates and references",
            ],
            "31-16mib-document-limit.svg",
            "16 MiB is a ceiling not a target",
            "Binary blobs inside documents are a common way to hit the limit accidentally. GridFS or object storage is the real answer — mention only if asked.",
        )
    )

    s.append(
        split(
            "Document Growth Considerations",
            [
                "Will arrays, strings, or nested objects keep growing?",
                "Does every update rewrite a large document?",
                "Mitigations: reference, bucket, archive, subset",
            ],
            "32-document-growth.svg",
            "Approaches when documents keep growing",
            "Even below 16 MiB, a 2 MiB document that is updated on every page view is a problem.",
        )
    )

    s.append(
        split(
            "Schema Design Anti-Patterns",
            [
                "Collections that clone tables",
                "Inconsistent names and stringified numbers",
                "Designing without access patterns",
            ],
            "33-schema-anti-patterns.svg",
            "Eight common schema anti-patterns",
            "Exercise 3.6 is a scavenger hunt on a single bad document. Keep this grid up.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "Introduction to Schema Validation",
            [
                "MongoDB can check documents on write",
                "Required fields, types, allowed values, nested shape",
                "Flexibility remains; the contract is enforced",
            ],
            "34-schema-validation.svg",
            "What collection validation can enforce",
            "Validation is not a substitute for application checks. It is the last line for shape and type.",
        )
    )

    s.append(
        split(
            "JSON Schema Validation",
            [
                "`bsonType`, `required`, `properties`",
                "Nested rules and array items",
                "`validationAction` and `validationLevel`",
            ],
            "35-json-schema-validation.svg",
            "Core $jsonSchema keywords",
            "Demo 3.5 runs this. Mention error: reject versus warn, and strict versus moderate level, without a full options lecture.",
        )
    )

    s.append(
        content(
            "JSON Schema — product example",
            """```javascript
db.createCollection("products", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["sku", "name", "price"],
      properties: {
        sku: { bsonType: "string" },
        name: { bsonType: "string" },
        price: { bsonType: "decimal", minimum: 0 }
      }
    }
  }
})
```""",
            "bsonType decimal maps to Decimal128. Double would silently accept binary floats — the thing we are trying to stop for money.",
            fit="fit-sm",
        )
    )

    s.append(
        split(
            "Schema Evolution",
            [
                "Add optional fields first",
                "Readers before writers",
                "Migrate old documents incrementally",
                "`schemaVersion` when the shape changes",
            ],
            "36-schema-evolution.svg",
            "Safe evolution sequence",
            "A hard cut-over that requires every document to change tonight is how training classes create outages. Incremental is the habit.",
        )
    )

    s.append(
        content(
            "Demo 3.5 — Create a Collection with Validation",
            """**Duration:** 15 minutes

Create `products_validated` with required `sku`, `name`, `category`, `price`.

- Insert a valid document → success
- Insert `price` as a string → rejected
- Read the validation error together""",
            "Use a throwaway collection so you do not fight existing products. Show the error JSON; do not rush past it.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "Demo 3.6 — Evolve a Document Schema",
            [
                "v1: `price` as Decimal128",
                "v2: `price: { amount, currency }` plus `schemaVersion`",
                "Keep old documents readable",
            ],
            "55-demo-schema-evolution.svg",
            "Price field evolving from scalar to object",
            "Application readers must understand both shapes during migration. Writers start emitting v2 only after readers are deployed.",
        )
    )

    s.append(
        ex_intro(
            "Exercise 3.6 — Find and Correct Anti-Patterns",
            [
                "15 minutes · flawed product document",
                "String price, text Boolean, unbounded reviews, string date",
            ],
            "33-schema-anti-patterns.svg",
            "Anti-pattern grid used as a checklist",
            "exercise-3.6-correct-schema-anti-patterns.md",
            "Exercise 3.6",
            "Collect the rewritten document. Reviews must leave the parent.",
        )
    )

    s.append(
        ex_steps(
            "Exercise 3.6 — Steps 1–2",
            [
                (
                    "Step 1 — Name the problems",
                    "List type, growth, naming, and identifier issues.",
                    "String price, text Boolean, unbounded array, display date, unclear id.",
                ),
                (
                    "Step 2 — Rewrite the document",
                    "Decimal128, Boolean, Date, sku/_id convention, reviews referenced.",
                    "A corrected document with no allReviews array.",
                ),
            ],
            "isActive: 'yes' is a classic bug. Boolean is true/false, not yes/no strings.",
            "exercise-3.6-correct-schema-anti-patterns.md",
            "Exercise 3.6",
        )
    )

    s.append(
        ex_intro(
            "Exercise 3.8 — Design Collection Validation",
            [
                "15 minutes · `$jsonSchema` on paper or in a scratch file",
                "Required sku, name, category, price, active, createdAt",
            ],
            "35-json-schema-validation.svg",
            "jsonSchema keywords for the product validator",
            "exercise-3.8-design-collection-validation.md",
            "Exercise 3.8",
            "They apply a similar validator in Lab 3.6. This exercise is the design; the lab is the proof.",
        )
    )

    s.append(
        ex_steps(
            "Exercise 3.8 — Steps 1–2",
            [
                (
                    "Step 1 — List required fields and bsonTypes",
                    "Six required names; price decimal minimum 0; active bool; createdAt date.",
                    "A properties map that Lab 3.6 can paste.",
                ),
                (
                    "Step 2 — Assemble `$jsonSchema`",
                    "Wrap in bsonType object. Optional extra fields remain allowed.",
                    "A validator object ready for createCollection.",
                ),
            ],
            "If someone uses bsonType double for price, correct it immediately.",
            "exercise-3.8-design-collection-validation.md",
            "Exercise 3.8",
        )
    )

    s.append(
        split(
            "Common MongoDB Schema Patterns",
            [
                "Reusable approaches, not mandatory templates",
                "Attribute, Bucket, Subset, Extended reference",
                "Computed, Outlier, Polymorphic",
            ],
            "37-schema-patterns-overview.svg",
            "Seven named MongoDB schema patterns",
            "Spend about a minute per pattern. The choosing table at the end is the takeaway.",
        )
    )

    s.append(
        split(
            "Attribute Pattern",
            [
                "Many similar optional attributes",
                "`attributes: [ { name, value } ]`",
                "Easier to index than fifty sparse fields",
            ],
            "38-attribute-pattern.svg",
            "Named fields versus name-value attribute array",
            "Product specifications and dynamic metadata are the usual examples. Our catalog labs use a nested object instead — both are valid; name the tradeoff.",
        )
    )

    s.append(
        split(
            "Bucket Pattern",
            [
                "Group measurements into a bounded document",
                "Sensor hour, metrics, events",
                "Fewer documents, controlled growth",
            ],
            "39-bucket-pattern.svg",
            "Hour bucket containing a bounded readings array",
            "One document per reading explodes collection size and index keys. Bucketing is the default mental model for time-series.",
        )
    )

    s.append(
        split(
            "Subset Pattern",
            [
                "Keep the hot subset on the parent",
                "Full set lives elsewhere",
                "Example: three recent reviews plus average rating",
            ],
            "40-subset-pattern.svg",
            "Product subset versus full reviews collection",
            "This is how you get a fast product page without embedding millions of reviews.",
        )
    )

    s.append(
        split(
            "Extended Reference Pattern",
            [
                "Copy frequently displayed fields onto the reference",
                "Order stores customer name and tier",
                "Tradeoff: those copies may need sync",
            ],
            "41-extended-reference-pattern.svg",
            "Order carrying a small customer summary",
            "Contrast with a purchase-time snapshot: name/tier might be allowed to go stale or be updated; unit price must not.",
        )
    )

    s.append(
        split(
            "Computed Pattern",
            [
                "Store the result instead of recomputing on every read",
                "Average rating, order total, lifetime value",
                "Must update when the source changes",
            ],
            "42-computed-pattern.svg",
            "Stored rating summary on a product",
            "Order total can be computed at write time and stored. That is cheaper than summing line items on every read.",
        )
    )

    s.append(
        split(
            "Outlier Pattern",
            [
                "Most documents follow the normal design",
                "Rare extremes get a different store",
                "Do not distort the schema for one viral product",
            ],
            "43-outlier-pattern.svg",
            "Typical products versus viral products",
            "If 99% of products have under 100 reviews, design for that. The million-review SKU is a special case.",
        )
    )

    s.append(
        split(
            "Polymorphic Pattern",
            [
                "Different types share one collection and a core",
                "A `type` or `category` field distinguishes them",
                "Same workflows, varied attributes",
            ],
            "44-polymorphic-pattern.svg",
            "BOOK and LAPTOP documents in one collection",
            "They already did this in Exercise 3.4. Name the pattern so they can defend it in a design review.",
        )
    )

    s.append(
        split(
            "Choosing an Appropriate Pattern",
            [
                "Start from the requirement, then pick a pattern",
                "You may combine patterns in one model",
            ],
            "45-choosing-a-pattern.svg",
            "Requirements mapped to schema patterns",
            "Leave this table up for Exercise 3.7. Combinations are normal: polymorphic catalog plus computed rating plus subset of reviews.",
            fit="fit-md",
        )
    )

    s.append(
        ex_intro(
            "Exercise 3.7 — Select a Schema Design Pattern",
            [
                "15 minutes · match seven requirements",
                "One pattern each; then name a tradeoff",
            ],
            "51-ex-3-7-select-pattern.svg",
            "Answer key mapping requirements to patterns",
            "exercise-3.7-select-a-schema-pattern.md",
            "Exercise 3.7",
            "Reveal answers after Step 2. If two patterns could fit, the justification matters.",
        )
    )

    s.append(
        ex_steps(
            "Exercise 3.7 — Steps 1–2",
            [
                (
                    "Step 1 — Match the first four requirements",
                    "Hourly sensors, latest three reviews, stored average, dynamic specs.",
                    "Bucket, Subset, Computed, Attribute.",
                ),
                (
                    "Step 2 — Match the remaining three and debrief",
                    "Customer name on an order, viral review volume, multiple product types.",
                    "Extended reference, Outlier, Polymorphic.",
                ),
            ],
            "Ask why Bucket is not ‘just use time-series collection’ — the idea travels even when the feature set differs by server version.",
            "exercise-3.7-select-a-schema-pattern.md",
            "Exercise 3.7",
        )
    )

    s.append(
        split(
            "E-Commerce Case Study",
            [
                "Collections: products, customers, orders, reviews",
                "This is the model Labs 3.1–3.7 implement",
            ],
            "46-ecommerce-case-study.svg",
            "Modeling decisions for the training store",
            "Walk each row. Primary access patterns: product by SKU, browse by category, customer profile, order by number, customer’s orders, rating summary, paginated reviews.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "Lab sequence — build training_store",
            [
                "One `mongosh` session",
                "Replace the Module 1 starter shape",
                "This is the Day 2 dataset",
            ],
            "52-lab-3-populate-flow.svg",
            "Seven lab steps from database through model review",
            "Time-box the block at about 50–70 minutes. Stragglers can load datasets/training_store/load.js if you updated it to this schema.",
        )
    )

    s.append(
        ex_steps(
            "Lab 3.1 — Steps 1–2",
            [
                (
                    "Step 1 — Select the database",
                    "Run `use training_store`.",
                    "Prompt shows training_store.",
                ),
                (
                    "Step 2 — Create the four collections",
                    "`createCollection` for products, customers, orders, reviews; then `show collections`.",
                    "All four names are listed. Existing collections from Module 1 are fine.",
                ),
            ],
            "createCollection errors if the name exists — tell them that is OK and to continue.",
            "lab-3.1-create-the-sample-database.md",
            "Lab 3.1",
        )
    )

    s.append(
        content(
            "Lab 3.2 — Products to insert",
            """Shared core: `sku`, `name`, `category`, `price`, `tags`, `active`, `createdAt`.

| sku | category | notable attributes |
|-----|----------|--------------------|
| L100 | LAPTOP | processor, memoryGB 16 |
| S200 | SHOE | sizes, color, material |
| B300 | BOOK | author, isbn, language |

Full `insertMany` is in the lab guide. Optionally `deleteMany` first.""",
            "Watch Decimal128. If they paste 1299.99 as a Double, Lab 3.6’s validator will later reject similar mistakes — good teaching moment.",
            fit="fit-md",
        )
    )

    s.append(
        ex_steps(
            "Lab 3.2 — Steps 1–2",
            [
                (
                    "Step 1 — Clear previous products",
                    "`db.products.deleteMany({})` unless the instructor says to keep Module 1 docs.",
                    "countDocuments is 0.",
                ),
                (
                    "Step 2 — Insert the three products",
                    "Run insertMany from the lab guide; then `db.products.find()`.",
                    "Three documents with nested attributes and Decimal128 prices.",
                ),
            ],
            "Confirm category values are LAPTOP, SHOE, BOOK — Lab 3.5 filters on those strings.",
            "lab-3.2-populate-products.md",
            "Lab 3.2",
        )
    )

    s.append(
        ex_steps(
            "Lab 3.3 — Steps 1–2",
            [
                (
                    "Step 1 — Insert Aisha Khan",
                    "insertOne customer C101 with nested name, contact, one Toronto shipping address.",
                    "acknowledged true and an insertedId.",
                ),
                (
                    "Step 2 — Verify by customer number",
                    "`db.customers.findOne({ customerNumber: \"C101\" })`.",
                    "You can point at name, contact, and addresses[0].city.",
                ),
            ],
            "Addresses must be an array of one — that is the bounded-embed lesson.",
            "lab-3.3-populate-customers.md",
            "Lab 3.3",
        )
    )

    s.append(
        ex_steps(
            "Lab 3.4 — Steps 1–2",
            [
                (
                    "Step 1 — Load the customer and product",
                    "findOne C101 and sku L100 into `customer` and `product`. Confirm not null.",
                    "You will copy `_id` and `price` into the order.",
                ),
                (
                    "Step 2 — Insert the order and verify",
                    "insertOne O5001 with customerId, item snapshot, address snapshot, Decimal128 totals.",
                    "findOne by orderNumber shows embedded items and a referenced customer.",
                ),
            ],
            "If product is null they skipped Lab 3.2. If customer is null they skipped 3.3. Do not invent ids.",
            "lab-3.4-populate-orders.md",
            "Lab 3.4",
        )
    )

    s.append(
        content(
            "Lab 3.5 — Nested and array queries",
            """```javascript
db.products.find({ category: "LAPTOP" })
db.products.find({ "attributes.memoryGB": 16 })
db.products.find({ tags: "technology" })
db.customers.find({ "addresses.city": "Toronto" })
db.orders.find({ "items.sku": "L100" })
```

Dot notation walks into nested documents and into arrays of documents.""",
            "This is a preview of Module 4, not the full operator set. Quotes around dotted keys matter.",
            fit="fit-md",
        )
    )

    s.append(
        ex_steps(
            "Lab 3.5 — Steps 1–2",
            [
                (
                    "Step 1 — Query products by category and nested attribute",
                    "category LAPTOP, attributes.memoryGB 16, tags technology.",
                    "Laptop, laptop, book.",
                ),
                (
                    "Step 2 — Query nested customer address and order items",
                    "addresses.city Toronto; items.sku L100.",
                    "C101 and O5001.",
                ),
            ],
            "If tags technology returns nothing, they omitted tags on the book.",
            "lab-3.5-query-nested-documents.md",
            "Lab 3.5",
        )
    )

    s.append(
        ex_steps(
            "Lab 3.6 — Steps 1–2",
            [
                (
                    "Step 1 — Create validated_products and insert a valid product",
                    "createCollection with $jsonSchema; insert A100 with Decimal128, Boolean, Date.",
                    "Insert succeeds.",
                ),
                (
                    "Step 2 — Attempt an invalid insert and read the error",
                    "String price, active 'yes', missing createdAt. Read the write error.",
                    "Insert rejected; you can name the failed rules.",
                ),
            ],
            "Use a new collection name so you do not collide with products. Paste the validator from the lab guide.",
            "lab-3.6-add-collection-validation.md",
            "Lab 3.6",
        )
    )

    s.append(
        ex_steps(
            "Lab 3.7 — Steps 1–2",
            [
                (
                    "Step 1 — Check togetherness, growth, and types",
                    "Together? Arrays bounded? Money decimal? Timestamps dates?",
                    "Order aggregate together; addresses bounded; reviews separate.",
                ),
                (
                    "Step 2 — Check relationships, snapshots, and naming",
                    "Complete the lab checklist. Note one future improvement (often an index).",
                    "You can defend the model and you are ready for Module 4.",
                ),
            ],
            "Do not create indexes yet. Naming them is enough.",
            "lab-3.7-validate-the-data-model.md",
            "Lab 3.7",
        )
    )

    s.append(
        split(
            "Module Summary",
            [
                "Model around access patterns",
                "Embed bounded owned data; reference the rest",
                "Duplication can be intentional — snapshots often should not sync",
                "Avoid unbounded arrays; validate the contract; plan evolution",
            ],
            "47-module-3-concept-map.svg",
            "Module 3 concept map",
            "Stay on this map for the knowledge check. Day 2 queries this exact shape.",
            fit="fit-md",
        )
    )

    s.append(
        content(
            "Knowledge Check",
            """1. Collection vs document?
2. What is BSON?
3. Purpose of `_id`?
4. When is embedding appropriate?
5. When is referencing appropriate?
6. Why are unbounded arrays dangerous?
7. Maximum BSON document size?
8. Why copy product price onto an order?
9. What does schema validation enforce?
10. Pattern for time-based measurements?
11. Pattern that copies referenced fields?
12. Pattern that stores calculated results?""",
            "Cold-call. Answers: group of docs vs one record; binary JSON; unique id; owned bounded together; independent/unbounded; growth and 16 MiB; 16 MiB; snapshot; shape/types/rules; Bucket; Extended reference; Computed.",
            fit="fit-sm",
        )
    )

    s.append(
        split(
            "Practical Challenge — Support Tickets",
            [
                "25 minutes · design only",
                "Embed summary, assignment, tags, recent comments",
                "Separate unbounded comments and audit history",
            ],
            "53-practical-challenge-ticket.svg",
            "Support-ticket embed versus reference guidance",
            "This is the capstone. No mongosh required. Collect one volunteer design.",
        )
    )

    s.append(
        ex_steps(
            "Exercise 3.9 — Steps 1–2",
            [
                (
                    "Step 1 — Access patterns and collections",
                    "List patterns, collections, embed vs reference, unbounded data.",
                    "tickets plus people plus history collections; recent comments bounded.",
                ),
                (
                    "Step 2 — Sample document, validation, and indexes",
                    "Draft a ticket, required fields, audit storage, likely indexes — do not create them.",
                    "A complete deliverable: collections, sample, table, validation, justification.",
                ),
            ],
            "If they embed the entire audit log, send them back to unbounded arrays.",
            "exercise-3.9-support-ticket-challenge.md",
            "Exercise 3.9",
        )
    )

    s.append(
        content(
            "Exit Ticket",
            """1. Database vs collection vs document?
2. Why is `_id` important?
3. JSON vs BSON?
4. What is an access pattern?
5. When to embed? When to reference?
6. Why are unbounded arrays dangerous?
7. Why duplicate product info on an order?
8. Purpose of collection validation?
9. How can a schema evolve safely?
10. Pattern for time-series? For calculated values?""",
            "Paper or chat. You need evidence they can justify embed vs reference, not only recites BSON types from Module 1.",
            fit="fit-sm",
        )
    )

    s.append(
        content(
            "Module Completion Checklist",
            """Participants can:

- Design a valid BSON document and choose types
- Identify access patterns and relationship types
- Justify embedding and referencing
- Recognize unbounded arrays
- Apply at least one named schema pattern
- Create and populate related collections
- Query embedded fields and arrays
- Create basic collection validation""",
            "If a laptop failed the labs, load.js plus a neighbor’s notes can still meet the conceptual bar. Keyboard work matters more than perfect typing.",
            fit="fit-md",
        )
    )

    s.append(
        content(
            "Questions and Answers",
            """Open questions on:

- Embed vs reference in *their* application
- Snapshots vs live copies
- Validation versus application rules
- Which pattern they would apply on Monday

Park index and `$lookup` depth for Modules 4 and 6 unless a short answer unblocks them.""",
            "Time-box 10 minutes. Write parking-lot items on the board for Day 2.",
            fit="fit-md",
        )
    )

    s.append(
        split(
            "Day 1 Review and Closure",
            [
                "NoSQL landscape and a working instance",
                "Documents designed around access patterns",
                "`training_store` ready for querying",
            ],
            "56-day1-result-path.svg",
            "Day 1 path from landscape to populated dataset",
            "Congratulate them. Tomorrow is find, filter, project, and update on this data — not a new domain.",
        )
    )

    s.append(
        content(
            "Transition to Module 4",
            """Module 4 uses `training_store` to teach:

- `find()` and `findOne()`
- Query filters and operators
- Projection
- Array queries
- Sort, limit, count
- Insert, update, replace, delete
- Update operators
- Precise, safe data changes

Keep tomorrow’s laptop on the same connection string.""",
            "If anyone’s data is missing, run load.js before they leave or first thing on Day 2.",
            fit="fit-md",
        )
    )

    return "\n\n---\n\n".join(s) + "\n"


def main() -> None:
    section = build()
    text = DECK.read_text(encoding="utf-8")
    if MARKER in text:
        start = text.index(MARKER)
        text = text[:start].rstrip() + "\n\n---\n\n" + section
        print("Replaced existing Module 3 section")
    else:
        text = text.rstrip() + "\n\n---\n\n" + section
        print("Appended Module 3 section")
    DECK.write_text(text, encoding="utf-8")
    slides = text.count("\n---\n")
    print(f"Wrote {DECK} (~{slides} slide separators)")


if __name__ == "__main__":
    main()
