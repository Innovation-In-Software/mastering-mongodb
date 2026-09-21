"""One-shot writer for Module 3 lab guides. Run from repo root."""
from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "slide-exercises" / "module-03"


def write(name: str, text: str) -> None:
    path = OUT / name
    path.write_text(text.strip() + "\n", encoding="utf-8")
    print(f"Wrote {path.relative_to(OUT.parent.parent)}")


ENV_DISCUSSION = """
## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Work in pairs. Capture answers in a notes file or on paper.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional — a table is enough |
| Timer | Instructor clocks this | Stay on the slide timer |

You do **not** need MongoDB running for this exercise.
""".strip()

ENV_MONGO = """
## Environment basics (read this first)

**Demonstration environment:** Windows 10/11 · PowerShell in Cursor (``Ctrl+` ``) · `mongosh` connected to the training instance.

| Task | Windows | Where |
|------|---------|-------|
| Open folder | `Ctrl+K Ctrl+O` | File → Open Folder |
| Terminal | ``Ctrl+` `` → PowerShell | Bottom panel |
| MongoDB shell | `mongosh` | Same terminal |

Use the same connection string from Module 2. Do **not** paste real passwords into chat or screenshots.
""".strip()

RELATED = """
## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
"""


write(
    "exercise-3.1-identify-document-components.md",
    f"""
# Exercise 3.1: Identify Document Components

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.1)  
**Time:** 10 min  
**Difficulty:** Beginner

**Objective:** Label `_id`, scalar fields, an embedded document, an array, a Boolean, a date, and candidate required fields on a sample customer document.

---

{ENV_DISCUSSION}

---

## Sample document

```javascript
{{
  _id: ObjectId("..."),
  customerNumber: "C101",
  name: {{
    first: "Aisha",
    last: "Khan"
  }},
  email: "aisha@example.com",
  tags: ["premium", "newsletter"],
  active: true,
  createdAt: ISODate("...")
}}
```

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Label identifier, scalars, and the nested name

**Do this:** On the sample document, mark `_id`, every scalar field (`customerNumber`, `email`), and the embedded `name` document. Write one sentence: what does `_id` guarantee inside a collection?

**Expected result:** `_id` is the unique identifier. `customerNumber` and `email` are scalars. `name` is an embedded document with `first` and `last`.

---

### Step 2 — Label array, Boolean, date, and required fields

**Do this:** Mark `tags` as an array, `active` as a Boolean, and `createdAt` as a Date. Then list candidate **required** fields for every customer document in this collection.

**Expected result:** You named `tags`, `active`, and `createdAt` correctly. Required-field candidates typically include `_id` (always), `customerNumber`, `name`, `email` or contact, `active`, and `createdAt`.

---

## Success criteria

- [ ] `_id` is identified as unique within the collection
- [ ] Embedded `name` is distinguished from scalar fields
- [ ] Array, Boolean, and Date are labeled
- [ ] A short required-field list exists

{RELATED}
""",
)

write(
    "exercise-3.2-discover-access-patterns.md",
    f"""
# Exercise 3.2: Discover Application Access Patterns

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.2)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Turn e-commerce requirements into access patterns: frequency, data returned together, and a modeling implication.

---

{ENV_DISCUSSION}

---

## Scenario

The application must support product search, product-detail pages, customer profiles, order placement, order history, reviews, and inventory display.

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — List the high-frequency reads

**Do this:** Name the three operations you expect to run most often. For each, write the data that must come back in one user-facing response.

**Expected result:** Typical high-frequency reads: find product by SKU (full product), retrieve order by order number (items, totals, address, status), load customer profile (name, contact, addresses). Inventory and review lists may be medium frequency.

---

### Step 2 — Fill the access-pattern table

**Do this:** Complete at least four rows:

| Access pattern | Frequency | Required data | Modeling implication |
|----------------|----------:|---------------|----------------------|
| Find product by SKU | High | Product details | Single product document |
| Retrieve order | High | Items, totals, address | Embed order aggregate |

Add rows for list-orders-for-customer, paginated reviews, and any snapshot you must preserve (purchase-time price).

**Expected result:** Each row names frequency, the fields returned together, and whether that implies embed, reference, or a snapshot.

---

## Success criteria

- [ ] At least four access patterns are listed
- [ ] “Data returned together” is specific, not “everything”
- [ ] At least one row says embed and one says reference

{RELATED}
""",
)

write(
    "exercise-3.3-embed-or-reference.md",
    f"""
# Exercise 3.3: Embed or Reference?

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.3)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Choose embedding or referencing for eight relationships and justify each choice from ownership, cardinality, and growth.

---

{ENV_DISCUSSION}

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Decide relationships 1–4

**Do this:** For each, write Embed or Reference and a one-line why (ownership, size, or growth).

1. Customer’s primary contact information
2. Customer’s complete order history
3. Order line items
4. Product’s millions of reviews

**Expected result:** (1) Embed (2) Reference (3) Embed (4) Reference. The justification mentions bound vs unbounded, not only “it feels nested.”

---

### Step 2 — Decide relationships 5–8

**Do this:** Repeat for:

5. Employee’s office address
6. Blog post tags
7. Purchase-time product price
8. Account’s complete transaction history

Then compare with the instructor table.

**Expected result:** (5) Embed or reference depending on reuse across employees (6) Embed (7) Embed as a snapshot (8) Reference. You can explain why (5) is the only “it depends.”

---

## Expected direction

| Relationship | Likely choice |
|--------------|---------------|
| Primary contact information | Embed |
| Complete order history | Reference |
| Order line items | Embed |
| Millions of reviews | Reference |
| Office address | Embed or reference, depending on reuse |
| Blog post tags | Embed |
| Purchase-time price | Embed |
| Complete transaction history | Reference |

---

## Success criteria

- [ ] Eight rows have a choice and a reason
- [ ] Unbounded histories are referenced
- [ ] Purchase-time price is treated as a snapshot

{RELATED}
""",
)

write(
    "exercise-3.4-model-a-product-catalog.md",
    f"""
# Exercise 3.4: Model a Product Catalog

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.3)  
**Time:** 20 min  
**Difficulty:** Beginner

**Objective:** Create three product documents in one collection with a consistent core and category-specific attributes.

---

{ENV_DISCUSSION}

MongoDB is optional. Write JSON-like documents in a scratch file.

---

## Required common fields

SKU, name, description, category, price, active status, creation date.

### Type-specific fields

- **Laptop:** processor, memory, storage, screen size
- **Shoe:** size, color, material, gender category
- **Book:** author, ISBN, publisher, language

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Design the shared core

**Do this:** List the common field names and BSON types (`sku` string, `price` Decimal128, `active` Boolean, `createdAt` Date). Decide whether category-specific fields live at the top level or under `attributes`.

**Expected result:** One core field list used by all three products. You did not invent `productPrice` on one document and `price` on another.

---

### Step 2 — Write three documents

**Do this:** Draft one laptop, one shoe, and one book in the same `products` collection. Keep the core identical. Put type-specific data in `attributes` (or an equivalent nested object).

**Expected result:** Three documents that a later `find({{ category: "LAPTOP" }})` and `find({{ "attributes.isbn": ... }})` could use. Category-specific fields do not appear as required for every product.

---

## Success criteria

- [ ] Common fields use the same names and types
- [ ] Three categories exist in one collection
- [ ] Type-specific fields are nested or clearly optional

{RELATED}
""",
)

write(
    "exercise-3.5-model-an-order-document.md",
    f"""
# Exercise 3.5: Model an Order Document

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.3)  
**Time:** 20 min  
**Difficulty:** Beginner

**Objective:** Design one complete order document: embed snapshots, reference the customer, choose required fields and BSON types, and justify the shape.

---

{ENV_DISCUSSION}

---

## Requirements

The application must find an order by order number, display purchased items, preserve purchase-time prices, show the shipping address used, show payment and fulfillment status, and list orders for a customer.

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Decide embed versus reference

**Do this:** Write four decisions: line items, purchase-time price, shipping address, customer. Mark which of those are **historical snapshots**.

**Expected result:** Items, prices, and shipping address are embedded snapshots. Customer is a reference (`customerId`). Current product catalog is not copied in full.

---

### Step 2 — Write the document and required fields

**Do this:** Draft one order document including `orderNumber`, `customerId`, `items[]` (sku, name, quantity, unitPrice), `shippingAddress`, statuses, monetary totals as Decimal128, and `createdAt`. List required fields.

**Expected result:** A complete order JSON-like object plus a short justification: one read by order number, customer orders via `customerId`, prices never silently follow the catalog.

---

## Success criteria

- [ ] Items and prices are embedded
- [ ] Customer is referenced
- [ ] Money uses Decimal128 (or you noted why)
- [ ] Required fields are listed

{RELATED}
""",
)

write(
    "exercise-3.6-correct-schema-anti-patterns.md",
    f"""
# Exercise 3.6: Find and Correct Schema Anti-Patterns

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.4)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Identify anti-patterns in a flawed product document and rewrite it with correct types, a bounded relationship, and a Date.

---

{ENV_DISCUSSION}

---

## Flawed document

```javascript
{{
  productId: "P1001",
  price: "49.99",
  isActive: "yes",
  allReviews: [
    // unlimited growth
  ],
  created: "September 20, 2026"
}}
```

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Name the problems

**Do this:** List every issue you can see: types, growth, naming, identifier strategy.

**Expected result:** Price stored as a string; Boolean stored as text; unbounded `allReviews` array; nonstandard date string; identifier is `productId` rather than `_id` or `sku` with a stated convention.

---

### Step 2 — Rewrite the document

**Do this:** Produce a corrected document. Move reviews out (reference). Use Decimal128, Boolean, Date, and a clear `_id`/`sku` convention.

**Expected result:** Something like `sku`/`_id`, `price: Decimal128("49.99")`, `active: true`, `createdAt: ISODate(...)`, and **no** `allReviews` array.

---

## Success criteria

- [ ] At least four anti-patterns named
- [ ] Corrected types for money, Boolean, and date
- [ ] Reviews are not an unbounded embedded array

{RELATED}
""",
)

write(
    "exercise-3.7-select-a-schema-pattern.md",
    f"""
# Exercise 3.7: Select a Schema Design Pattern

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.5)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Match seven modeling requirements to Attribute, Bucket, Subset, Computed, Extended reference, Outlier, or Polymorphic.

---

{ENV_DISCUSSION}

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Match the first four requirements

**Do this:** Assign a pattern to:

- Sensor readings grouped by hour
- Latest three product reviews
- Stored average rating
- Dynamic product specifications

**Expected result:** Bucket, Subset, Computed, Attribute — in that order.

---

### Step 2 — Match the remaining three and debrief

**Do this:** Assign a pattern to:

- Customer name copied into an order
- Rare products with extremely high review volume
- Multiple product types in one collection

Compare with the instructor answer key.

**Expected result:** Extended reference, Outlier, Polymorphic. You can state one benefit and one tradeoff for any two patterns.

---

## Expected answers

| Requirement | Pattern |
|-------------|---------|
| Sensor readings grouped by hour | Bucket |
| Latest three product reviews | Subset |
| Stored average rating | Computed |
| Dynamic product specifications | Attribute |
| Customer name copied into an order | Extended reference |
| Rare products with extremely high review volume | Outlier |
| Multiple product types in one collection | Polymorphic |

---

## Success criteria

- [ ] Seven matches recorded
- [ ] You can explain Bucket vs one-document-per-event
- [ ] You can explain why Outlier exists

{RELATED}
""",
)

write(
    "exercise-3.8-design-collection-validation.md",
    f"""
# Exercise 3.8: Design Collection Validation

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.4)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Design a `$jsonSchema` validator that requires sku, name, category, non-negative decimal price, Boolean active, and Date createdAt.

---

{ENV_DISCUSSION}

You may type the validator in a scratch `.js` file. Running it is optional until Lab 3.6.

---

## Requirements

A valid product must contain:

- `sku`: string
- `name`: string
- `category`: string
- `price`: decimal and not negative
- `active`: Boolean
- `createdAt`: date

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — List required fields and bsonTypes

**Do this:** Write the `required` array and a `properties` map with `bsonType` for each field. Put `minimum: 0` on `price`.

**Expected result:** Six required names. `price` is `decimal` (not `double` or `string`). `active` is `bool`. `createdAt` is `date`.

---

### Step 2 — Assemble `$jsonSchema`

**Do this:** Wrap the design in:

```javascript
{{
  $jsonSchema: {{
    bsonType: "object",
    required: [ /* ... */ ],
    properties: {{ /* ... */ }}
  }}
}}
```

Note `validationAction` / `validationLevel` if you know them. You will apply a similar validator in Lab 3.6.

**Expected result:** A complete validator object you could pass to `db.createCollection`. Extra optional fields are still allowed.

---

## Success criteria

- [ ] All six fields are required
- [ ] Price is decimal with minimum 0
- [ ] Boolean and Date types are correct

{RELATED}
""",
)

LAB_HEADER = """**Prerequisite:** Module 2 — a working `mongosh` session. If `training_store` still holds the Module 1 starter documents, these labs **replace** that shape with the Day 2 application model.
"""

write(
    "lab-3.1-create-the-sample-database.md",
    f"""
# Lab 3.1: Create the Sample Application Database

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.6)  
**Time:** 10 min  
**Difficulty:** Beginner

**Objective:** Select `training_store` and create the `products`, `customers`, `orders`, and `reviews` collections.

{LAB_HEADER}

---

{ENV_MONGO}

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Select the database

**Do this:** In `mongosh`, run:

```javascript
use training_store
```

**Expected result:** The prompt shows `training_store`. The database may not appear in `show dbs` until it holds data.

---

### Step 2 — Create the four collections

**Do this:** Run:

```javascript
db.createCollection("products")
db.createCollection("customers")
db.createCollection("orders")
db.createCollection("reviews")
show collections
```

If a collection already exists from Module 1, `createCollection` reports that it exists — that is fine. Continue.

**Expected result:** `show collections` lists `products`, `customers`, `orders`, and `reviews`.

---

## Success criteria

- [ ] Prompt is `training_store`
- [ ] Four application collections are listed

{RELATED}
""",
)

write(
    "lab-3.2-populate-products.md",
    f"""
# Lab 3.2: Create and Populate the Products Collection

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.6)  
**Time:** 20 min  
**Difficulty:** Beginner

**Objective:** Replace starter products with three catalog documents that share a core and use nested `attributes`.

{LAB_HEADER}

---

{ENV_MONGO}

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Clear previous products (optional but recommended)

**Do this:** Run `db.products.deleteMany({{}})` so Day 2 queries see only the Module 3 catalog. Skip this only if the instructor told you to keep Module 1 documents.

**Expected result:** `deletedCount` is reported. `db.products.countDocuments()` is 0.

---

### Step 2 — Insert the three products

**Do this:** Run the `insertMany` from the slides (laptop `L100`, shoe `S200`, book `B300`) with `Decimal128` prices, `attributes`, `tags`, `active`, and `createdAt: new Date()`. Then `db.products.find()`.

**Expected result:** Three documents. Each has the shared core. Category-specific fields live under `attributes`.

---

## Success criteria

- [ ] Three products inserted
- [ ] Prices are Decimal128
- [ ] `attributes` differs by category

{RELATED}
""",
)

write(
    "lab-3.3-populate-customers.md",
    f"""
# Lab 3.3: Create and Populate the Customers Collection

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.6)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Insert customer `C101` with nested name, contact, a bounded `addresses` array, preferences, and status.

{LAB_HEADER}

---

{ENV_MONGO}

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Insert Aisha Khan

**Do this:** Optionally `db.customers.deleteMany({{}})` first. Then `insertOne` the customer document from the slides (`customerNumber: "C101"`, nested `name` and `contact`, one `SHIPPING` address in Toronto, `status: "ACTIVE"`).

**Expected result:** `acknowledged: true` and an `insertedId`.

---

### Step 2 — Verify by customer number

**Do this:**

```javascript
db.customers.findOne({{ customerNumber: "C101" }})
```

**Expected result:** One document. You can point to the embedded `name`, `contact`, and `addresses[0].city`.

---

## Success criteria

- [ ] Customer C101 exists
- [ ] Address is a bounded array, not a separate collection
- [ ] You can find the document by `customerNumber`

{RELATED}
""",
)

write(
    "lab-3.4-populate-orders.md",
    f"""
# Lab 3.4: Create and Populate the Orders Collection

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.6)  
**Time:** 20 min  
**Difficulty:** Beginner

**Objective:** Insert order `O5001` that references the customer, embeds line-item snapshots, and stores Decimal128 totals.

{LAB_HEADER}

---

{ENV_MONGO}

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Load the customer and product

**Do this:**

```javascript
const customer = db.customers.findOne({{ customerNumber: "C101" }})
const product = db.products.findOne({{ sku: "L100" }})
```

Confirm both are not `null`.

**Expected result:** `customer._id` and `product.price` print if you inspect them. You will copy those values into the order.

---

### Step 2 — Insert the order and verify

**Do this:** `insertOne` order `O5001` from the slides: `customerId: customer._id`, one item snapshot (`productId`, `sku`, `name`, `quantity`, `unitPrice: product.price`), shipping-address snapshot, payment and fulfillment status, Decimal128 `subtotal` / `tax` / `total`. Then `db.orders.findOne({{ orderNumber: "O5001" }})`.

**Expected result:** One order document. Items and address are embedded. Customer is an id reference, not a full customer copy.

---

## Success criteria

- [ ] Order O5001 exists
- [ ] `customerId` matches the customer `_id`
- [ ] Line item preserves sku, name, and unitPrice

{RELATED}
""",
)

write(
    "lab-3.5-query-nested-documents.md",
    f"""
# Lab 3.5: Query Nested Documents and Arrays

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.6)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Query category, dotted nested attributes, array values, nested address city, and order line-item sku.

{LAB_HEADER}

---

{ENV_MONGO}

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Query products by category and nested attribute

**Do this:** Run:

```javascript
db.products.find({{ category: "LAPTOP" }})
db.products.find({{ "attributes.memoryGB": 16 }})
db.products.find({{ tags: "technology" }})
```

**Expected result:** Laptop query returns `L100`. Memory query returns the laptop. Tags query returns the book (`B300`).

---

### Step 2 — Query nested customer address and order items

**Do this:**

```javascript
db.customers.find({{ "addresses.city": "Toronto" }})
db.orders.find({{ "items.sku": "L100" }})
```

**Expected result:** Customer C101 and order O5001. You used dot notation into an array of documents — Module 4 will go deeper.

---

## Success criteria

- [ ] Category, nested field, and array queries each returned a document
- [ ] Address city and item sku queries worked
- [ ] You can explain why `"attributes.memoryGB"` uses quotes

{RELATED}
""",
)

write(
    "lab-3.6-add-collection-validation.md",
    f"""
# Lab 3.6: Add Collection Validation

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.6)  
**Time:** 20 min  
**Difficulty:** Beginner

**Objective:** Create `validated_products` with `$jsonSchema`, insert one valid document, and read the error from one invalid insert.

{LAB_HEADER}

---

{ENV_MONGO}

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Create the validated collection and insert a valid product

**Do this:** Run `db.createCollection("validated_products", {{ validator: {{ $jsonSchema: ... }}}})` from the slides. Then insert adapter `A100` with Decimal128 price, `active: true`, and `createdAt: new Date()`.

**Expected result:** Collection created. Valid insert succeeds.

---

### Step 2 — Attempt an invalid insert and read the error

**Do this:** Insert a document with `price: "39.99"` (string) and `active: "yes"`, omitting `createdAt`. Read the write error (`failingDocumentId`, `errmsg`, or schema rules).

**Expected result:** The insert is rejected. You can name which rules failed (type of `price`, type of `active`, missing `createdAt`).

---

## Success criteria

- [ ] Valid insert succeeded
- [ ] Invalid insert failed
- [ ] You can point to the validation error text

{RELATED}
""",
)

write(
    "lab-3.7-validate-the-data-model.md",
    f"""
# Lab 3.7: Validate the Data Model

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.6)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Review `training_store` against a maintainability and performance checklist before Day 2 querying.

{LAB_HEADER}

---

{ENV_DISCUSSION}

Use `mongosh` only if you want to re-open a document while you check the list.

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Check togetherness, growth, and types

**Do this:** For products, customers, and orders, answer: Are frequently accessed values stored together? Are arrays bounded? Are financial values Decimal128 (or noted)? Are timestamps Dates?

**Expected result:** Order items and shipping address are together. Customer `addresses` is bounded. Reviews are a separate collection. Prices are decimal. `createdAt` is a date.

---

### Step 2 — Check relationships, snapshots, and naming

**Do this:** Confirm embed vs reference is deliberate, purchase-time snapshots exist on the order, collection names are plural and consistent, field names are consistent, and the main queries from Exercise 3.2 can run. Note one improvement you would make later (index, extra field, or validation on `orders`).

**Expected result:** A completed checklist with at least one future improvement. You are ready for Module 4.

---

## Checklist

- [ ] Frequently accessed values stored together
- [ ] Arrays bounded
- [ ] Financial values stored appropriately
- [ ] Timestamps stored as dates
- [ ] Required fields identified
- [ ] Relationships deliberately embedded or referenced
- [ ] Historical snapshots preserved
- [ ] Collection names consistent
- [ ] Field names consistent
- [ ] Main application queries can be supported

{RELATED}
""",
)

write(
    "exercise-3.9-support-ticket-challenge.md",
    f"""
# Exercise 3.9: Design a Support-Ticket Data Model

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Practical Challenge)  
**Time:** 25 min  
**Difficulty:** Intermediate

**Objective:** Design collections, embed/reference decisions, a sample ticket document, validation, and audit-history storage for a support system.

---

{ENV_DISCUSSION}

---

## Scenario

A support system must create tickets, assign agents, store status and priority, add comments, attach tags, display recent comments with the ticket, preserve a complete audit history, and search by customer, agent, status, and priority.

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Access patterns and collections

**Do this:** List the main access patterns. Name the collections. Mark what is embedded vs referenced, and what could grow without bound.

**Expected result:** Collections such as `tickets`, `customers`, `agents`, `comments` and/or `audit_events`. Recent comments and tags are bounded on the ticket. Full comment and audit history are separate.

---

### Step 2 — Sample document, validation, and indexes

**Do this:** Draft one ticket document with BSON types. List required fields for validation. Explain how complete audit history is stored. Name likely future indexes (do **not** create them yet).

**Expected result:** A ticket with `ticketNumber`, `customerId`, `assignee`, `status`, `priority`, `tags`, `recentComments[]`, timestamps. Validation requires those keys. Audit events live in their own collection. Indexes likely on `customerId`, `assignee.agentId`, `status`, `priority`.

---

## Suggested design direction

**Embed:** ticket summary, current assignment, tags, a bounded set of recent comments.

**Reference or separate:** complete comment history, complete audit-event history, customer master, agent master.

---

## Success criteria

- [ ] Collection list exists
- [ ] One sample ticket document
- [ ] Embed/reference table
- [ ] Validation requirements
- [ ] Brief justification including unbounded data

{RELATED}
""",
)

print("Done.")
