"""Insert Module 3 diagram slides that do not yet have a home.

Idempotent: skips a slide if its heading already exists. Run from repo root:

    python scripts/_insert_module03_diagram_slides.py
"""
from __future__ import annotations

import re
from pathlib import Path

DECK = Path(__file__).resolve().parent.parent / "slides" / "course-complete-marp-with-notes.md"


def split_slide(title: str, bullets: list[str], img: str, alt: str, note: str, *, fit: bool = False) -> str:
    cls = "split fit-md" if fit else "split"
    lis = "\n".join(f"- {b}" for b in bullets)
    return f"""<!-- _class: {cls} -->

# {title}

<div class="cols">
<div class="col-text">

{lis}

</div>
<div class="col-visual">

<img src="assets/module-03/{img}" alt="{alt}" width="720">

</div>
</div>

<!--
{note}

The slide title is: {title}.
-->
"""


NEW = [
    split_slide(
        "Array of Embedded Documents",
        [
            "Order `items` is an array of documents",
            "Each element is a purchase-time snapshot",
            "Still keep a practical size limit",
        ],
        "008-array-of-embedded-documents.svg",
        "Order items as an array of documents",
        "Contrast with the previous scalar-array slide. Quantity plus unitPrice belong on the item, not as parallel scalar arrays.",
    ),
    split_slide(
        "Tables to Documents Transformation",
        [
            "Fold `order_items` and `addresses` into the order",
            "Keep `products` and `customers` as collections",
            "Reviews stay independent",
        ],
        "012-tables-to-documents.svg",
        "Relational tables transformed into MongoDB collections",
        "Demo 3.2 uses this picture. Count the joins they would have needed on the left.",
        fit=True,
    ),
    split_slide(
        "Join-Based Retrieval vs Document Retrieval",
        [
            "Relational: several joins to paint one screen",
            "Document: `find` the order number",
            "The document **is** the business object",
        ],
        "013-join-vs-document-retrieval.svg",
        "Multiple joins compared with one document read",
        "This is why we do not clone every table as a collection.",
    ),
    split_slide(
        "Relational Normalization vs MongoDB Aggregates",
        [
            "Normalization divides by entity",
            "Document modeling groups by operation",
            "Split only what must live apart",
        ],
        "014-normalization-vs-aggregates.svg",
        "Entity tables compared with an order aggregate",
        "Checkout and order-detail are one operation — that is the aggregate.",
    ),
    split_slide(
        "Avoid the Collection-per-Table Anti-Pattern",
        [
            "Tiny collections keep the joins",
            "Redesign around aggregates",
            "`training_store` uses four collections, not twelve tables",
        ],
        "015-collection-per-table-antipattern.svg",
        "Table copies versus a redesigned document model",
        "If they propose order_items as its own collection, send them back here.",
    ),
    split_slide(
        "Access Pattern to Document Shape",
        [
            "Start from one sentence",
            "List the fields that sentence needs",
            "That list **is** the document",
        ],
        "020-access-pattern-to-document-shape.svg",
        "Retrieve complete order by order number mapped to a document",
        "Demo 3.3 builds this document field by field.",
    ),
    split_slide(
        "Application Query Map",
        [
            "Every important screen becomes a row",
            "Name the collection and the shape",
            "This table is the modeling contract",
        ],
        "021-application-query-map.svg",
        "User actions mapped to collections and document shapes",
        "Use this when they argue about embed vs reference without naming a query.",
        fit=True,
    ),
    split_slide(
        "Read Optimization vs Write Complexity",
        [
            "Embedding speeds the hot read",
            "Writes may touch a larger document",
            "Accept that cost on purpose",
        ],
        "022-read-optimization-vs-write-complexity.svg",
        "Faster reads balanced against harder writes",
        "Catalog-wide price fixes are harder once prices are snapshots — and that is correct for orders.",
    ),
    split_slide(
        "One-to-Few Relationships",
        [
            "A handful of children, bounded",
            "Customer addresses, product images",
            "Embed as an array of documents",
        ],
        "025-one-to-few-relationship.svg",
        "Customer with a bounded addresses array",
        "Ask how many addresses a customer has. Few. Then ask how many orders. Unbounded.",
    ),
    split_slide(
        "One-to-Squillions Relationships",
        [
            "Reviews, events, transactions",
            "Will not fit in the parent",
            "Own collection, paginated",
        ],
        "027-one-to-squillions-relationship.svg",
        "High-cardinality children in a separate collection",
        "Squillions is informal on purpose — it means ‘do not embed.’",
    ),
    split_slide(
        "Relationship Cardinality Decision Flow",
        [
            "How many — and will it grow?",
            "One or few and bounded → embed",
            "Many or unbounded → reference",
        ],
        "029-relationship-cardinality-decision.svg",
        "Cardinality leading to embed or reference",
        "Leave this up during Exercise 3.3.",
    ),
    split_slide(
        "Relationship Ownership",
        [
            "Owned by the parent → embed candidate",
            "Independently managed → reference",
            "Cardinality without ownership is incomplete",
        ],
        "030-relationship-ownership.svg",
        "Owned child data versus independently managed related data",
        "An office address reused by many employees is independently managed even if each person has one.",
    ),
    split_slide(
        "Embedding Decision Tree",
        [
            "Read together?",
            "Same lifecycle?",
            "Bounded size?",
            "Yes to all → embed; otherwise reference",
        ],
        "034-embedding-decision-tree.svg",
        "Three yes-questions leading to embed",
        "This is the portable rule. The comparison table is the detail.",
    ),
    split_slide(
        "Customer Address: Embedded Model",
        [
            "A few addresses belong to the customer",
            "Retrieved with the profile",
            "Bounded array — not a collection",
        ],
        "035-customer-address-embedded.svg",
        "Customer document containing a small address array",
        "Lab 3.3 implements this exact shape.",
    ),
    split_slide(
        "Customer Orders: Referenced Model",
        [
            "Orders grow without a practical limit",
            "Query `orders` by `customerId`",
            "Do not append history onto the customer",
        ],
        "036-customer-orders-referenced.svg",
        "Customer connected to independently stored orders",
        "This is the same parent as the address slide — different representation.",
    ),
    split_slide(
        "Order Items: Embedded Model",
        [
            "Line items are the sale",
            "Prices are snapshots",
            "One document, one checkout write",
        ],
        "037-order-items-embedded.svg",
        "Order containing purchased-item snapshots",
        "Lab 3.4 inserts this array from the live product, then keeps the copy.",
    ),
    split_slide(
        "Product Reviews: Referenced Model",
        [
            "Review volume is unbounded",
            "Separate `reviews` collection",
            "Optional subset + computed rating on the product",
        ],
        "038-product-reviews-referenced.svg",
        "Product connected to a growing reviews collection",
        "This is also subset + computed — name those patterns when you reach Lesson 3.5.",
    ),
    split_slide(
        "Hybrid Embedding and Referencing",
        [
            "Reference the customer and product ids",
            "Embed purchase-time name, price, address",
            "Most real orders look like this",
        ],
        "039-hybrid-embedding-and-referencing.svg",
        "Order referencing people and catalog while embedding snapshots",
        "Demo 3.4 is this table spoken aloud.",
        fit=True,
    ),
    split_slide(
        "Single-Document Atomicity",
        [
            "Related fields in one document",
            "One write updates items, totals, and status",
            "Succeed or fail together",
        ],
        "040-single-document-atomicity.svg",
        "One update changing related fields as one atomic operation",
        "This is not a multi-document transaction lecture. It is why the aggregate exists.",
    ),
    split_slide(
        "Current State vs Historical State",
        [
            "Catalog price can change tomorrow",
            "The order keeps 49.99",
            "That is not a bug — it is the model",
        ],
        "043-current-vs-historical-state.svg",
        "Current product price changing while order price stays",
        "Finance and receipts depend on this slide.",
    ),
    split_slide(
        "Denormalization Tradeoff",
        [
            "Faster reads, fewer lookups",
            "Duplication and update cost",
            "Copy stable or historical fields",
        ],
        "045-denormalization-tradeoff.svg",
        "Faster reads balanced against duplication",
        "Do not copy a rapidly changing inventory count onto every order.",
    ),
    split_slide(
        "Extended Reference Example",
        [
            "Store `customerId` plus name and tier",
            "Full profile stays in `customers`",
            "Display the order without a second query",
        ],
        "046-extended-reference-example.svg",
        "Order storing customer id plus name and tier",
        "Contrast with a price snapshot: name/tier might be allowed to go stale; unit price must not.",
    ),
    split_slide(
        "Bounded vs Unbounded Arrays",
        [
            "Addresses: you can name a max",
            "All reviews: you cannot",
            "If you cannot name a max, do not embed",
        ],
        "047-bounded-vs-unbounded-arrays.svg",
        "Small address array compared with growing reviews",
        "This is the test they should apply in Exercise 3.3.",
    ),
    split_slide(
        "Unbounded Array Correction",
        [
            "Move reviews to their own collection",
            "Keep `productId` on each review",
            "Optional: three recent reviews on the product",
        ],
        "049-unbounded-array-correction.svg",
        "Reviews moved from an embedded array to a collection",
        "Exercise 3.6’s corrected document must look like the right column.",
    ),
    split_slide(
        "Document Growth Over Time",
        [
            "Small at insert time is not enough",
            "Embedded history accumulates",
            "Updates and reads get more expensive",
        ],
        "051-document-growth-over-time.svg",
        "A small document becoming expensive as records accumulate",
        "Even below 16 MiB this hurts. Growth is a design input, not a surprise.",
    ),
    split_slide(
        "Large Binary Data Decision",
        [
            "Keep metadata on the document",
            "Store files outside BSON",
            "Blobs are a common 16 MiB accident",
        ],
        "053-large-binary-data-decision.svg",
        "Small metadata in the document with files stored outside",
        "Mention GridFS or object storage only if asked — the rule is: not inside the product document.",
    ),
    split_slide(
        "Laptop Product Document",
        [
            "Shared core plus laptop attributes",
            "processor, memory, storage, screen",
            "Still one `products` collection",
        ],
        "056-laptop-product-document.svg",
        "Laptop document with category-specific attributes",
        "Lab 3.2 inserts L100. Keep sku/name/category/price identical to the other types.",
        fit=True,
    ),
    split_slide(
        "Shoe Product Document",
        [
            "Same core as the laptop",
            "`sizes` is a bounded scalar array",
            "color and material are attributes",
        ],
        "057-shoe-product-document.svg",
        "Shoe document with sizes, color, and material",
        "Point out sizes[] is bounded by the catalog, not a lifetime of events.",
        fit=True,
    ),
    split_slide(
        "Book Product Document",
        [
            "author, ISBN, language",
            "Same required core",
            "Lab 3.5 queries `tags: \"technology\"` on this document",
        ],
        "058-book-product-document.svg",
        "Book document with author, ISBN, and language",
        "Exercise 3.4’s deliverable is these three documents with identical core names.",
        fit=True,
    ),
    split_slide(
        "Product and Order Relationship",
        [
            "Item stores `productId` **and** a snapshot",
            "Current catalog can change",
            "The sale does not",
        ],
        "061-product-and-order-relationship.svg",
        "Current product referenced by an order item snapshot",
        "Two links, two jobs: reference for later lookup, snapshot for history.",
    ),
    split_slide(
        "Product Review Model",
        [
            "Computed rating on the product",
            "Optional recent-review subset",
            "Full history in `reviews`",
        ],
        "062-product-review-model.svg",
        "Product summary connected to separately stored reviews",
        "Subset + computed + reference — a realistic combination.",
    ),
    split_slide(
        "Complete E-Commerce Read Model",
        [
            "Each screen has a primary collection",
            "Order details do not join five tables",
            "Reviews are a second query when the user asks",
        ],
        "063-complete-ecommerce-read-model.svg",
        "Product page, profile, order, history, and reviews mapped to collections",
        "This is the payoff of the case study.",
        fit=True,
    ),
    split_slide(
        "E-Commerce Access-Pattern Map",
        [
            "User action → query → structure",
            "If a row is missing, the model is incomplete",
        ],
        "064-ecommerce-access-pattern-map.svg",
        "User actions mapped to queries and document structures",
        "Exercise 3.2 produced this table in draft. The case study is the instructor key.",
        fit=True,
    ),
    split_slide(
        "Required Fields Validation",
        [
            "sku, name, category, price, active, createdAt",
            "Missing any of these fails the write",
            "Extra optional fields remain allowed",
        ],
        "067-required-fields-validation.svg",
        "Required product fields checked before insertion",
        "Exercise 3.8 and Lab 3.6 use this exact list.",
        fit=True,
    ),
    split_slide(
        "BSON Type Validation",
        [
            "String, decimal, bool, date",
            "The rejected examples are the classroom bugs",
        ],
        "068-bson-type-validation.svg",
        "Expected BSON types compared with rejected examples",
        "String prices and yes/no booleans are the two they will actually type.",
        fit=True,
    ),
    split_slide(
        "Valid vs Invalid Product Document",
        [
            "Valid insert succeeds",
            "Invalid insert is rejected",
            "Read the error together",
        ],
        "069-valid-vs-invalid-product.svg",
        "Correctly typed product accepted; string price rejected",
        "Demo 3.5 and Lab 3.6 are this diagram executed in mongosh.",
    ),
    split_slide(
        "Nested Document Validation",
        [
            "Validate the parent object",
            "Then nested `attributes` if present",
            "Category-specific keys stay optional",
        ],
        "070-nested-document-validation.svg",
        "Product and nested attributes validated at multiple levels",
        "Do not require processor on a book. Require the core; leave attributes flexible.",
    ),
    split_slide(
        "Validation Level and Action",
        [
            "`error` rejects; `warn` logs",
            "`strict` vs `moderate`",
            "Labs use error + strict so mistakes are visible",
        ],
        "071-validation-level-and-action.svg",
        "Validation rules leading to warning or rejection",
        "Mention moderate only so they are not surprised in production docs later.",
        fit=True,
    ),
    split_slide(
        "Backward-Compatible Schema Change",
        [
            "Old documents remain readable",
            "New field is optional at first",
            "This is the default evolution move",
        ],
        "073-backward-compatible-schema-change.svg",
        "Existing documents readable while new documents gain an optional field",
        "Adding currency as an optional sibling of price is compatible. Renaming price is not.",
    ),
    split_slide(
        "Breaking vs Non-Breaking Schema Changes",
        [
            "Add optional field → non-breaking",
            "Rename or retarget a required type → breaking",
            "Breaking changes need a dual-read period",
        ],
        "074-breaking-vs-nonbreaking-changes.svg",
        "Adding an optional field compared with renaming a required field",
        "Demo 3.6 (price object) is a breaking shape change — that is why schemaVersion exists.",
    ),
    split_slide(
        "Incremental Data Migration",
        [
            "Read → transform → validate → save",
            "One document at a time",
            "No launch-night rewrite of the collection",
        ],
        "076-incremental-data-migration.svg",
        "Read old document, transform, validate, save",
        "They can migrate on read (lazy) or in a background job. Both beat a freeze-the-world cutover.",
    ),
    split_slide(
        "Reader-First Schema Evolution",
        [
            "Readers understand both shapes first",
            "Then new writers",
            "Then migrate, then retire v1",
        ],
        "077-reader-first-schema-evolution.svg",
        "Update readers, then writers, then migrate, then retire",
        "Writers-first is how mixed-schema outages happen.",
    ),
    split_slide(
        "Combining Schema Patterns",
        [
            "Patterns compose on one document",
            "Catalog: polymorphic + attribute + computed + subset",
            "Outlier handles the viral SKU",
        ],
        "087-combining-schema-patterns.svg",
        "Product using attribute, subset, computed, and outlier together",
        "The selection matrix is not ‘pick exactly one.’",
        fit=True,
    ),
    split_slide(
        "Numbers Stored as Strings",
        [
            '`"49.99"` sorts and aggregates wrongly',
            "Money → Decimal128",
        ],
        "089-numbers-stored-as-strings.svg",
        "String price compared with Decimal128",
        "Exercise 3.6’s first bug. Circle it on the projector.",
    ),
    split_slide(
        "Inconsistent Field Names",
        [
            "`price` vs `productPrice` vs `item_cost`",
            "Queries silently miss documents",
            "Pick one name and validate it",
        ],
        "090-inconsistent-field-names.svg",
        "Three field names for the same fact",
        "Flexible schema does not mean three names for the same fact.",
    ),
    split_slide(
        "Over-Normalized MongoDB Model",
        [
            "Five lookups to paint one screen",
            "That is a relational model wearing BSON",
            "Fold the aggregate",
        ],
        "091-over-normalized-mongodb-model.svg",
        "Simple operation requiring many collection lookups",
        "Same picture as the collection-per-table anti-pattern, now named as a query-time cost.",
    ),
    split_slide(
        "Oversized Document Anti-Pattern",
        [
            "Unrelated or unlimited data in one document",
            "Slow reads, heavy updates, 16 MiB risk",
        ],
        "092-oversized-document-antipattern.svg",
        "One document accumulating unlimited information",
        "Customer + all orders + logs + files is the cartoon version of this bug.",
    ),
    split_slide(
        "Mixed Unrelated Data Anti-Pattern",
        [
            "Customers, orders, logs, and products are not one collection",
            "Polymorphic is for **related** types with a shared workflow",
        ],
        "093-mixed-unrelated-data-antipattern.svg",
        "Unrelated types incorrectly placed in one collection",
        "Laptop vs book is polymorphic. Customer vs log line is not.",
    ),
    split_slide(
        "Deep Nesting Anti-Pattern",
        [
            "Nest only as deep as the access pattern needs",
            "Deep paths make updates and queries brittle",
        ],
        "094-deep-nesting-antipattern.svg",
        "Excessive nesting producing complicated paths",
        "`customer.profile.contact.home.address.geo.city` is a smell.",
    ),
    split_slide(
        "Schema Anti-Pattern Correction Flow",
        [
            "Detect → access pattern → new boundary → validate",
            "Exercise 3.6 is this flow on one document",
        ],
        "095-antipattern-correction-flow.svg",
        "Detect, redesign, validate",
        "Lab 3.7 is the same flow against the whole training_store model.",
    ),
    split_slide(
        "Schema-Version Strategy",
        [
            "Put `schemaVersion` on the document when the shape changes",
            "Readers branch on the version",
            "Demo 3.6 uses v1 scalar price → v2 `{ amount, currency }`",
        ],
        "075-schema-version-strategy.svg",
        "Documents carrying schemaVersion while the app supports both",
        "Not every optional field needs a version number — use it when the shape actually breaks.",
    ),
    split_slide(
        "Duplicated Data Synchronization Choices",
        [
            "Snapshot, sync, events, refresh, eventual",
            "Ask: must the copy always match the source?",
        ],
        "044-duplicated-data-sync-choices.svg",
        "Five strategies for keeping copies in sync",
        "For orders, pick snapshot and move on.",
        fit=True,
    ),
]


# After which existing heading should each new slide be inserted?
# Use the new slide's own title as key; value is the preceding existing heading.
AFTER = {
    "Array of Embedded Documents": "Arrays in MongoDB Documents",
    "Tables to Documents Transformation": "Relational Modeling vs Document Modeling",
    "Join-Based Retrieval vs Document Retrieval": "Tables to Documents Transformation",
    "Relational Normalization vs MongoDB Aggregates": "Join-Based Retrieval vs Document Retrieval",
    "Avoid the Collection-per-Table Anti-Pattern": "Relational Normalization vs MongoDB Aggregates",
    "Access Pattern to Document Shape": "Model Data Around Access Patterns",
    "Application Query Map": "Identify Application Workloads",
    "Read Optimization vs Write Complexity": "Read and Write Access Patterns",
    "One-to-Few Relationships": "One-to-One Relationships",
    "One-to-Squillions Relationships": "One-to-Many Relationships",
    "Relationship Cardinality Decision Flow": "Many-to-Many Relationships",
    "Relationship Ownership": "Relationship Cardinality Decision Flow",
    "Embedding Decision Tree": "Embedding vs Referencing",
    "Customer Address: Embedded Model": "Embedding Decision Tree",
    "Customer Orders: Referenced Model": "Customer Address: Embedded Model",
    "Order Items: Embedded Model": "Customer Orders: Referenced Model",
    "Product Reviews: Referenced Model": "Order Items: Embedded Model",
    "Hybrid Embedding and Referencing": "Product Reviews: Referenced Model",
    "Single-Document Atomicity": "Hybrid Embedding and Referencing",
    "Duplicated Data Synchronization Choices": "Maintaining Duplicated Data",
    "Current State vs Historical State": "Modeling Historical Snapshots",
    "Denormalization Tradeoff": "Current State vs Historical State",
    "Extended Reference Example": "Denormalization Tradeoff",
    "Bounded vs Unbounded Arrays": "Unbounded Arrays",
    "Unbounded Array Correction": "Bounded vs Unbounded Arrays",
    "Document Growth Over Time": "The 16 MiB Document Limit",
    "Large Binary Data Decision": "Document Growth Considerations",
    "Laptop Product Document": "Modeling Product Catalogs",
    "Shoe Product Document": "Laptop Product Document",
    "Book Product Document": "Shoe Product Document",
    "Product and Order Relationship": "Modeling Orders",
    "Product Review Model": "Product and Order Relationship",
    "Complete E-Commerce Read Model": "E-Commerce Case Study",
    "E-Commerce Access-Pattern Map": "Complete E-Commerce Read Model",
    "Required Fields Validation": "JSON Schema Validation",
    "BSON Type Validation": "Required Fields Validation",
    "Valid vs Invalid Product Document": "BSON Type Validation",
    "Nested Document Validation": "Valid vs Invalid Product Document",
    "Validation Level and Action": "Nested Document Validation",
    "Schema-Version Strategy": "Demo 3.6 — Evolve a Document Schema",
    "Backward-Compatible Schema Change": "Schema Evolution",
    "Breaking vs Non-Breaking Schema Changes": "Backward-Compatible Schema Change",
    "Incremental Data Migration": "Breaking vs Non-Breaking Schema Changes",
    "Reader-First Schema Evolution": "Incremental Data Migration",
    "Combining Schema Patterns": "Choosing an Appropriate Pattern",
    "Numbers Stored as Strings": "Schema Design Anti-Patterns",
    "Inconsistent Field Names": "Numbers Stored as Strings",
    "Over-Normalized MongoDB Model": "Inconsistent Field Names",
    "Oversized Document Anti-Pattern": "Over-Normalized MongoDB Model",
    "Mixed Unrelated Data Anti-Pattern": "Oversized Document Anti-Pattern",
    "Deep Nesting Anti-Pattern": "Mixed Unrelated Data Anti-Pattern",
    "Schema Anti-Pattern Correction Flow": "Deep Nesting Anti-Pattern",
}


IMG_REPLACEMENTS = {
    "assets/module-03/01-why-data-modeling-matters.svg": (
        "assets/module-03/000-why-data-modeling-matters.svg",
        "Good model outcomes versus poor model problems",
    ),
    "assets/module-03/02-mongodb-data-hierarchy.svg": (
        "assets/module-03/001-mongodb-data-hierarchy.svg",
        "MongoDB deployment to database to collection to document to field",
    ),
    "assets/module-03/03-databases-collections-documents.svg": (
        "assets/module-03/002-database-collection-document.svg",
        "training_store with products, customers, orders, and reviews",
    ),
    "assets/module-03/04-anatomy-of-a-document.svg": (
        "assets/module-03/003-anatomy-of-a-document.svg",
        "Document labeled with _id, strings, numbers, Boolean, date, array, nested document",
    ),
    "assets/module-03/05-bson-data-types.svg": (
        "assets/module-03/004-bson-data-type-map.svg",
        "BSON type catalog",
    ),
    "assets/module-03/06-objectid-and-id.svg": (
        "assets/module-03/005-id-field-and-objectid.svg",
        "Insert without _id, MongoDB generates ObjectId, stored unique document",
    ),
    "assets/module-03/07-nested-documents.svg": (
        "assets/module-03/006-embedded-document-structure.svg",
        "Customer with embedded name, contact, and address",
    ),
    "assets/module-03/08-arrays-in-documents.svg": (
        "assets/module-03/007-array-of-scalar-values.svg",
        "Product with tags, colors, and sizes arrays",
    ),
    "assets/module-03/09-flexible-schema.svg": (
        "assets/module-03/009-flexible-schema-within-collection.svg",
        "Laptop, shoe, and book sharing a collection",
    ),
    "assets/module-03/10-schema-conventions.svg": (
        "assets/module-03/010-flexible-vs-inconsistent-schema.svg",
        "Intentional variation versus uncontrolled field names",
    ),
    "assets/module-03/11-relational-vs-document.svg": (
        "assets/module-03/011-relational-vs-document-model.svg",
        "Relational approach compared with document approach",
    ),
    "assets/module-03/12-model-around-access-patterns.svg": (
        "assets/module-03/016-access-pattern-driven-modeling.svg",
        "Requirements to access patterns to document boundaries to collections",
    ),
    "assets/module-03/13-application-workloads.svg": (
        "assets/module-03/021-application-query-map.svg",
        "Application operations mapped to collections",
    ),
    "assets/module-03/14-read-write-access-patterns.svg": (
        "assets/module-03/017-read-and-write-access-patterns.svg",
        "Read and write considerations feeding schema decisions",
    ),
    "assets/module-03/15-data-accessed-together.svg": (
        "assets/module-03/018-data-accessed-together.svg",
        "Order details grouped into one aggregate",
    ),
    "assets/module-03/16-data-changes-together.svg": (
        "assets/module-03/019-data-that-changes-together.svg",
        "Same lifecycle embed versus different lifecycle reference",
    ),
    "assets/module-03/17-relationship-types.svg": (
        "assets/module-03/023-mongodb-relationship-types.svg",
        "One-to-one through many-to-many",
    ),
    "assets/module-03/18-one-to-one.svg": (
        "assets/module-03/024-one-to-one-relationship.svg",
        "Customer with embedded contact",
    ),
    "assets/module-03/19-one-to-many.svg": (
        "assets/module-03/026-one-to-many-relationship.svg",
        "Customer connected to separately stored orders",
    ),
    "assets/module-03/20-many-to-many.svg": (
        "assets/module-03/028-many-to-many-relationship.svg",
        "Products and categories many-to-many",
    ),
    "assets/module-03/21-embedding.svg": (
        "assets/module-03/031-embedding-related-data.svg",
        "Parent document containing related child information",
    ),
    "assets/module-03/22-referencing.svg": (
        "assets/module-03/032-referencing-related-data.svg",
        "Parent storing another document identifier",
    ),
    "assets/module-03/23-embed-vs-reference.svg": (
        "assets/module-03/033-embedding-vs-referencing.svg",
        "Side-by-side embed versus reference",
    ),
    "assets/module-03/24-denormalization.svg": (
        "assets/module-03/041-intentional-data-duplication.svg",
        "Stable summary copied into an order",
    ),
    "assets/module-03/25-historical-snapshots.svg": (
        "assets/module-03/042-historical-snapshot-modeling.svg",
        "Purchase-time name, price, and address on the order",
    ),
    "assets/module-03/26-product-catalog.svg": (
        "assets/module-03/055-product-document-model.svg",
        "Common product fields plus category-specific attributes",
    ),
    "assets/module-03/27-customer-profile.svg": (
        "assets/module-03/059-customer-profile-document.svg",
        "Customer with embedded name, contact, preferences, and addresses",
    ),
    "assets/module-03/28-order-aggregate.svg": (
        "assets/module-03/060-order-aggregate-document.svg",
        "Order with customer reference, embedded items, address snapshot, totals",
    ),
    "assets/module-03/29-time-series-events.svg": (
        "assets/module-03/000-time-series-events.svg",
        "Event document and bucket-oriented design",
    ),
    "assets/module-03/30-unbounded-arrays.svg": (
        "assets/module-03/048-unbounded-array-antipattern.svg",
        "Product expanding as reviews are appended",
    ),
    "assets/module-03/31-16mib-document-limit.svg": (
        "assets/module-03/050-16mib-bson-document-limit.svg",
        "Document-growth gauge approaching 16 MiB",
    ),
    "assets/module-03/32-document-growth.svg": (
        "assets/module-03/052-document-growth-decision-flow.svg",
        "Growth leading to embed, bucket, subset, archive, or reference",
    ),
    "assets/module-03/33-schema-anti-patterns.svg": (
        "assets/module-03/088-schema-antipatterns-overview.svg",
        "Overview of MongoDB schema anti-patterns",
    ),
    "assets/module-03/34-schema-validation.svg": (
        "assets/module-03/065-flexible-schema-with-validation.svg",
        "Flexible documents passing through validation guardrails",
    ),
    "assets/module-03/35-json-schema-validation.svg": (
        "assets/module-03/066-schema-validation-flow.svg",
        "Insert or update through validator to accept or error",
    ),
    "assets/module-03/36-schema-evolution.svg": (
        "assets/module-03/072-schema-evolution-timeline.svg",
        "Version 1 to optional fields to version 2 to migrated document",
    ),
    "assets/module-03/37-schema-patterns-overview.svg": (
        "assets/module-03/078-schema-pattern-overview.svg",
        "Seven named MongoDB schema patterns",
    ),
    "assets/module-03/38-attribute-pattern.svg": (
        "assets/module-03/079-attribute-pattern.svg",
        "Name-value attribute array",
    ),
    "assets/module-03/39-bucket-pattern.svg": (
        "assets/module-03/080-bucket-pattern.svg",
        "Hourly bucket of measurements",
    ),
    "assets/module-03/40-subset-pattern.svg": (
        "assets/module-03/081-subset-pattern.svg",
        "Recent reviews on the product, full set elsewhere",
    ),
    "assets/module-03/41-extended-reference-pattern.svg": (
        "assets/module-03/082-extended-reference-pattern.svg",
        "Order copies frequently displayed customer fields",
    ),
    "assets/module-03/42-computed-pattern.svg": (
        "assets/module-03/083-computed-pattern.svg",
        "Stored rating, count, or total",
    ),
    "assets/module-03/43-outlier-pattern.svg": (
        "assets/module-03/084-outlier-pattern.svg",
        "Typical documents versus exceptional large records",
    ),
    "assets/module-03/44-polymorphic-pattern.svg": (
        "assets/module-03/085-polymorphic-pattern.svg",
        "BOOK and LAPTOP in one collection",
    ),
    "assets/module-03/45-choosing-a-pattern.svg": (
        "assets/module-03/086-schema-pattern-selection-matrix.svg",
        "Business problems mapped to schema patterns",
    ),
    "assets/module-03/46-ecommerce-case-study.svg": (
        "assets/module-03/054-ecommerce-data-model-overview.svg",
        "customers, products, orders, and reviews with relationships",
    ),
    "assets/module-03/47-module-3-concept-map.svg": (
        "assets/module-03/000-module-3-concept-map.svg",
        "Module 3 concept map",
    ),
    "assets/module-03/48-ex-3-1-document-components.svg": (
        "assets/module-03/096-ex-3-1-label-the-document.svg",
        "Unlabeled sample document for Exercise 3.1",
    ),
    "assets/module-03/49-ex-3-2-access-patterns.svg": (
        "assets/module-03/097-ex-3-2-access-pattern-worksheet.svg",
        "Access-pattern worksheet",
    ),
    "assets/module-03/50-ex-3-3-embed-or-reference.svg": (
        "assets/module-03/098-ex-3-3-embed-or-reference-board.svg",
        "Embed or reference decision board",
    ),
    "assets/module-03/51-ex-3-7-select-pattern.svg": (
        "assets/module-03/102-ex-3-7-match-the-schema-pattern.svg",
        "Requirements matched to schema patterns",
    ),
    "assets/module-03/52-lab-3-populate-flow.svg": (
        "assets/module-03/104-lab-3-1-training-database-structure.svg",
        "training_store collections",
    ),
    "assets/module-03/53-practical-challenge-ticket.svg": (
        "assets/module-03/111-practical-challenge-support-ticket.svg",
        "Support-ticket data model",
    ),
    "assets/module-03/54-demo-embed-reference.svg": (
        "assets/module-03/039-hybrid-embedding-and-referencing.svg",
        "Hybrid embedding and referencing on an order",
    ),
    "assets/module-03/55-demo-schema-evolution.svg": (
        "assets/module-03/075-schema-version-strategy.svg",
        "schemaVersion strategy",
    ),
    "assets/module-03/56-day1-result-path.svg": (
        "assets/module-03/000-day1-result-path.svg",
        "Day 1 path to training_store",
    ),
}


LAB_VISUALS = [
    (
        "## Lab 3.2 — Steps 1–2",
        split_slide(
            "Lab 3.2 — Product Dataset Structure",
            [
                "L100 laptop, S200 shoe, B300 book",
                "Shared core + `attributes`",
                "Decimal128 prices",
            ],
            "105-lab-3-2-product-dataset-structure.svg",
            "Three product types with shared and category-specific fields",
            "Full insertMany is in the lab guide. Optionally deleteMany first.",
        ),
        "Lab 3.2 — Product Dataset Structure",
    ),
    (
        "## Lab 3.3 — Steps 1–2",
        split_slide(
            "Lab 3.3 — Customer Dataset Structure",
            [
                "C101 with nested name and contact",
                "One SHIPPING address in Toronto",
                "Bounded array — not a collection",
            ],
            "106-lab-3-3-customer-dataset-structure.svg",
            "Customer profile with embedded contact, addresses, and preferences",
            "Point at addresses[0].city — Lab 3.5 queries that path.",
        ),
        "Lab 3.3 — Customer Dataset Structure",
    ),
    (
        "## Lab 3.4 — Steps 1–2",
        split_slide(
            "Lab 3.4 — Order Dataset Structure",
            [
                "`customerId` is a reference",
                "Items and address are snapshots",
                "Totals are Decimal128",
            ],
            "107-lab-3-4-order-dataset-structure.svg",
            "Order with embedded line items, snapshots, totals, and statuses",
            "Load customer and product first so ids and prices are real.",
        ),
        "Lab 3.4 — Order Dataset Structure",
    ),
    (
        "# Lab 3.5 — Nested and array queries",
        None,  # replace image on this content slide by converting? keep as insert before steps
        None,
    ),
]


def _without_notes(slide: str) -> str:
    return re.sub(r"\n<!--\n[\s\S]*?-->", "", slide)


def heading_of(slide_md: str) -> str:
    for line in slide_md.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def insert_after(slides: list[str], after_title: str, new_md: str) -> bool:
    needles = {f"# {after_title}", f"## {after_title}"}
    new_h = heading_of(new_md)
    already = {f"# {new_h}", f"## {new_h}"}
    if any(
        line.strip() in already
        for s in slides
        for line in _without_notes(s).splitlines()
    ):
        return False
    for i, s in enumerate(slides):
        for line in _without_notes(s).splitlines():
            if line.strip() in needles:
                slides.insert(i + 1, new_md.strip())
                return True
    return False


def main() -> None:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from marp_tables import split_marp_slides

    text = DECK.read_text(encoding="utf-8")
    for old, (new, _alt) in IMG_REPLACEMENTS.items():
        text = text.replace(old, new)

    fm_end = text.find("\n---\n", 3) + 5
    front = text[:fm_end]
    slides = [s.strip("\n") for s in split_marp_slides(text)]

    by_title = {heading_of(s): s for s in NEW}
    inserted = 0
    # Insert in AFTER order repeatedly until stable so chains work
    changed = True
    while changed:
        changed = False
        for new_title, after in AFTER.items():
            md = by_title[new_title]
            if insert_after(slides, after, md):
                inserted += 1
                changed = True

    for after, md, title in [
        (
            "Lab 3.2 — Products to insert",
            by_title.get("Lab 3.2 — Product Dataset Structure")
            or LAB_VISUALS[0][1],
            "Lab 3.2 — Product Dataset Structure",
        ),
        (
            "Lab 3.3 — Steps 1–2",
            LAB_VISUALS[1][1],
            "Lab 3.3 — Customer Dataset Structure",
        ),
        (
            "Lab 3.4 — Steps 1–2",
            LAB_VISUALS[2][1],
            "Lab 3.4 — Order Dataset Structure",
        ),
    ]:
        if md and insert_after(slides, after, md):
            inserted += 1

    # Lab 3.5 nested query diagram: insert before steps
    lab35 = split_slide(
        "Lab 3.5 — Nested-Field Query Paths",
        [
            "Dot notation walks nested objects",
            "And into arrays of documents",
            "Quotes around dotted keys matter",
        ],
        "108-lab-3-5-nested-field-query-paths.svg",
        "Dot notation from document root to nested attributes and array elements",
        "This is a Module 4 preview. They only need these five finds to work.",
    )
    if insert_after(slides, "Lab 3.5 — Nested and array queries", lab35):
        inserted += 1

    lab36 = split_slide(
        "Lab 3.6 — Validation Test Flow",
        [
            "Valid A100 insert succeeds",
            "Invalid A101 is rejected",
            "Read the error text",
        ],
        "109-lab-3-6-validation-test-flow.svg",
        "Valid insert accepted and invalid insert rejected",
        "Use validated_products so you do not fight the products collection.",
    )
    if insert_after(slides, "Lab 3.6 — Steps 1–2", lab36):
        inserted += 1

    lab37 = split_slide(
        "Lab 3.7 — Data Model Review Checklist",
        [
            "Togetherness, growth, types",
            "Relationships, snapshots, names",
            "Note one future improvement — often an index",
        ],
        "110-lab-3-7-data-model-review-checklist.svg",
        "Checklist covering access patterns, relationships, growth, types, consistency",
        "Do not create indexes yet. Naming them is enough.",
    )
    if insert_after(slides, "Lab 3.7 — Steps 1–2", lab37):
        inserted += 1

    ex34 = split_slide(
        "Exercise 3.4 — Flexible Product Catalog",
        [
            "Laptop, shoe, book — one collection",
            "Identical core field names",
            "Type-specific data under `attributes`",
        ],
        "099-ex-3-4-flexible-product-catalog.svg",
        "Laptop, shoe, and book schemas sharing common fields",
        "If they create three collections, send them back.",
    )
    if insert_after(slides, "Exercise 3.4 — Model a Product Catalog", ex34):
        inserted += 1

    ex35 = split_slide(
        "Exercise 3.5 — Build an Order Aggregate",
        [
            "Reference the customer",
            "Embed items, prices, and ship-to",
            "That is the Lab 3.4 shape",
        ],
        "100-ex-3-5-build-an-order-aggregate.svg",
        "Customer, product, address, and payment arranged into an order",
        "Collect one volunteer document on the projector.",
    )
    if insert_after(slides, "Exercise 3.5 — Model an Order Document", ex35):
        inserted += 1

    ex36 = split_slide(
        "Exercise 3.6 — Find the Anti-Patterns",
        [
            "String price, text Boolean",
            "Unbounded reviews, display date",
        ],
        "101-ex-3-6-find-the-antipatterns.svg",
        "Problematic document with inconsistent types and unbounded arrays",
        "Reviews must leave the parent in the rewrite.",
    )
    if insert_after(slides, "Exercise 3.6 — Find and Correct Anti-Patterns", ex36):
        inserted += 1

    ex38 = split_slide(
        "Exercise 3.8 — Design Validation Rules",
        [
            "Six required fields",
            "decimal price ≥ 0, bool, date",
        ],
        "103-ex-3-8-design-validation-rules.svg",
        "Product requirements transformed into validation",
        "They apply this validator in Lab 3.6.",
        fit=True,
    )
    if insert_after(slides, "Exercise 3.8 — Design Collection Validation", ex38):
        inserted += 1

    out = front + "\n\n" + "\n\n---\n\n".join(s.rstrip() for s in slides) + "\n"
    DECK.write_text(out, encoding="utf-8")
    print(f"Inserted {inserted} new slides; replaced image paths; {len(slides)} total slides in body")


if __name__ == "__main__":
    main()
