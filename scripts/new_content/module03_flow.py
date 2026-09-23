#!/usr/bin/env python3
"""Slide order for the Module 3 deck: from document structure to a modeled training_store.

Every concept diagram is merged with the slide that explains it (diagram plus the
points only that slide adds), so no idea appears twice. A bridge from Module 2,
five part openers, mongosh examples on the training_store sample database, two
in-flow practice exercises, a knowledge check, the official Exercises 3.1-3.9, the
Day 1 Lab 2 guide (labs/day-01/lab2, Steps 1-7) and a hand-off to Module 4 connect the ideas.

Where a guide and the dataset disagree, the slide follows
datasets/training_store/load.js and the notes explain the difference.
"""
from __future__ import annotations

import mdb_diagram_slides as DS
import mdb_flow_slides as F
import mdb_glossary as G
from mdb_flow_slides import tp
from mdb_visuals import GREEN, NAVY, ORANGE, PURPLE, RED, TEAL

PARTS = ["Part 1\nDocuments and types", "Part 2\nAccess patterns", "Part 3\nEmbed or reference",
         "Part 4\nPatterns", "Part 5\nValidate and build"]


# ---------------------------------------------------------------------------
# Sequence
# ---------------------------------------------------------------------------
def steps(S, NOTES, DIAGRAMS, DIAGRAM_DIR):
    def img(n):
        return DS.diagram_file(DIAGRAM_DIR, n)

    def dn(n, *extra):
        return F.merge_units(NOTES[n], DIAGRAMS[n][2], *extra)

    return [
        S[1],
        S[2],
        *G.intro("module03"),
        F.story("From Module 2 to Module 3",
                "MongoDB is running — now we decide what the documents should look like.",
                gave_title="Module 2 gave us",
                gave=["A running MongoDB — local or Atlas",
                      "mongosh connected and verified",
                      "use, createCollection and insertOne",
                      "A first starter products collection",
                      "Fixes for common connection errors"],
                now=("Now", "Design the documents before we insert many more of them."),
                path_title="Our path through Module 3",
                path=[("Documents, BSON types and a shared core", "Part 1", NAVY),
                      ("Access patterns, relationships and growth", "Part 2", PURPLE),
                      ("Embed, reference and snapshots", "Part 3", TEAL),
                      ("Anti-patterns and schema patterns", "Part 4", ORANGE),
                      ("Validation, evolution and the labs", "Part 5", GREEN)],
                takeaway="Module 2 gave us a working database; Module 3 decides the shape of "
                         "everything we store in it.",
                notes=[tp("Bridge from Module 2",
                          "In Module 2 everyone installed or provisioned MongoDB, connected with "
                          "mongosh, verified the environment and ran the first commands: use, "
                          "createCollection, insertOne, find and countDocuments."),
                       tp("What those first documents lacked",
                          "The Module 2 starter products stored price as a plain number, 39.99, "
                          "which mongosh saves as a Double, and had no shared design. "
                          "That was fine for checking the installation. "
                          "It is not how we want to store a real catalog."),
                       tp("What changes now",
                          "Module 3 designs the documents first. "
                          "Lab 2, Step 2, then replaces the starter products with the modeled catalog, "
                          "so Day 2 starts from a deliberate design."),
                       tp("The path",
                          "Five parts: documents and types, access patterns, embed or "
                          "reference, patterns and anti-patterns, and finally validation and "
                          "the labs that build training_store.")]),

        # Part 1 ------------------------------------------------------------
        F.bridge(PARTS, 0, "Part 1: Documents and BSON Types",
                 "Start with what a document can hold.",
                 so_far=["MongoDB is installed and mongosh connects",
                         "training_store has its first collection"],
                 question="What can one document hold — and which type should each value "
                          "have?",
                 covers=["Anatomy of a training_store document", "Nested documents and arrays",
                         "Common BSON types", "Choosing types that match the meaning",
                         "One collection, a shared core"],
                 notes=[tp("Where we start",
                           "Module 1 introduced documents, collections and BSON. "
                           "Now we look at them as designers: what a document can hold, and "
                           "how each value should be typed."),
                        tp("What this part answers",
                           "We read a real training_store product field by field, look at "
                           "nested documents and arrays, choose BSON types, and see how one "
                           "collection holds different products with a shared core.")]),
        F.code("Anatomy of a training_store Document",
               "Product L100, field by field — every value keeps its BSON type.",
               [{"label": "db.products.findOne({ sku: \"L100\" })", "kind": "info", "code":
                 "{\n"
                 "  _id: ObjectId(\"…\"),              // ObjectId\n"
                 "  sku: \"L100\",                      // String\n"
                 "  name: \"Business Laptop\",\n"
                 "  category: \"LAPTOP\",\n"
                 "  price: Decimal128(\"1299.99\"),     // Decimal128\n"
                 "  attributes: {                     // embedded document\n"
                 "    processor: \"Intel Core i7\",\n"
                 "    memoryGB: 16, storageGB: 512    // Int32\n"
                 "  },\n"
                 "  tags: [\"business\", \"portable\"],   // Array\n"
                 "  active: true,                     // Boolean\n"
                 "  createdAt: ISODate(\"2026-08-20T09:00:00Z\")  // Date\n"
                 "}"}],
               points=[("_id rules", "Unique in its collection, indexed automatically, and "
                                     "can't be changed after insert."),
                       ("Any unique value", "ObjectId by default — a string or a number works "
                                            "too, if it stays unique."),
                       ("Business key", "sku is a separate field with its own unique index — "
                                        "it is what people search by."),
                       {"callout": ("Exercise 3.1", "You'll label a customer document the same "
                                                    "way.")}],
               mode="left", left_w=7.70,
               takeaway="A document is a set of typed field-value pairs — and _id is the one "
                        "field every document must have.",
               notes=[tp("Read it top to bottom",
                         "This is product L100 as mongosh prints it, trimmed: the real document "
                         "also has screenSizeInches in attributes. "
                         "Each comment names the BSON type of the value."),
                      tp("Fields and values",
                         "A field is a named piece of information: sku, name, price. "
                         "A value can be a scalar such as a string or number, an embedded "
                         "document such as attributes, or an array such as tags."),
                      tp("The _id field",
                         "Every document must have a unique _id. "
                         "If the application doesn't supply one, mongosh or the driver "
                         "generates an ObjectId. "
                         "_id always has a unique index, and it can't be changed after the "
                         "insert. "
                         "It may be an ObjectId, a string, a number or another unique value."),
                      tp("_id versus sku",
                         "training_store keeps the ObjectId as _id and uses sku as the business "
                         "key. "
                         "load.js creates a unique index on sku, named sku_unique."),
                      tp("Databases and collections",
                         "use training_store selects the database; MongoDB creates it on the "
                         "first write. "
                         "A collection can be created explicitly with db.createCollection, or "
                         "implicitly by the first insert. "
                         "Lab 2, Step 1, creates all four explicitly.")]),
        F.diagram(img(3), "Nested Documents and Arrays",
                  "A value can be a whole document — or a list of them.",
                  items=[("Embedded document", "A document as a value: a product's "
                                               "attributes, a customer's name and contact."),
                         ("Array", "Several values in one field: tags, or whole documents like "
                                   "order items and addresses."),
                         {"code": "db.products.find(\n"
                                  "  { \"attributes.memoryGB\": 16 })\n"
                                  "db.orders.find(\n"
                                  "  { \"items.sku\": \"L100\" })",
                          "label": "Reach inside with dot notation", "size": 11},
                         {"callout": ("Quotes", "Dotted paths must be in quotes.")}],
                  takeaway="Nested documents and arrays let one document hold a whole "
                           "business object — dot notation reaches inside.",
                  notes=dn(3)),
        F.compare("Common BSON Types",
                  "Each type with a real training_store value.",
                  ["Type", "training_store example", "Typical use"],
                  [("String", "sku: \"L100\"", "Names, codes, statuses"),
                   ("Int32", "memoryGB: 16", "Quantities, counters"),
                   ("Decimal128", "price: Decimal128(\"1299.99\")", "Money"),
                   ("Double", "4.6 (an average)", "Measurements"),
                   ("Boolean", "active: true", "Flags"),
                   ("Date", "createdAt: ISODate(\"2026-08-20…\")", "Timestamps"),
                   ("ObjectId", "customerId: ObjectId(\"…\")", "Identifiers"),
                   ("Array", "tags: [\"business\", \"portable\"]", "Lists"),
                   ("Embedded", "attributes: { processor: … }", "Grouped fields"),
                   ("Null", "contact.phone: null (C204)", "Known but empty")],
                  [1.55, 4.00, 2.45], row_h=0.42, size=13,
                  items=[("Int32 or Double?", "mongosh stores a whole number like 16 as Int32 "
                                              "and 4.6 as a Double."),
                         ("Null or missing?", "C204's phone is null; C515 has no phone field "
                                              "at all."),
                         {"callout": ("Money", "Decimal128 — never a string or a Double.")}],
                  takeaway="BSON adds the types JSON lacks — dates, decimals and ObjectIds — so "
                           "choose the one that matches the meaning.",
                  notes=[tp("BSON",
                            "MongoDB stores documents as BSON, Binary JSON. "
                            "It supports the JSON structures plus extra types such as Date, "
                            "Decimal128, ObjectId and specific integer sizes."),
                         tp("Read the table",
                            "Every example is a real value from training_store after load.js. "
                            "The only exception is the Double row: the dataset has no "
                            "floating-point fields, so 4.6 stands for a value such as an "
                            "average rating."),
                         tp("Int32 and Double in mongosh",
                            "mongosh stores a whole number such as 16 as a 32-bit integer, and "
                            "a number with a fraction such as 4.6 as a Double. "
                            "That is why prices are always written with Decimal128."),
                         tp("Null versus missing",
                            "Luis Romero, C204, has contact.phone set to null: we know he has no "
                            "phone number. "
                            "Sam Okonkwo, C515, has no phone field at all. "
                            "Module 4 shows the queries that tell these apart."),
                         tp("Aliases",
                            "The content guide writes NumberDecimal(...) and ISODate(...). "
                            "Our labs write Decimal128(...) and new Date(...). "
                            "Both pairs create the same BSON types.")]),
        F.diagram(img(4), "Choose Types That Match the Meaning",
                  "Strings make comparisons, sorting and calculations wrong.",
                  items=[{"code": "// poor\n"
                                  "{ price: \"49.99\", active: \"yes\",\n"
                                  "  createdAt: \"September 20, 2026\" }\n"
                                  "// better\n"
                                  "{ price: Decimal128(\"49.99\"),\n"
                                  "  active: true,\n"
                                  "  createdAt: ISODate(\"2026-09-20\") }",
                          "label": "Poor versus better", "size": 11},
                         ("Why it matters", "\"100\" sorts before \"20\"; \"yes\" is not a "
                                            "Boolean; text dates don't sort by time."),
                         {"callout": ("In training_store", "XBAD's price is the string "
                                                           "\"49.99\" — on purpose.")}],
                  takeaway="Store money as Decimal128, flags as Booleans and times as Dates — "
                           "the type decides how values behave.",
                  notes=dn(4, [tp("A deliberate fixture",
                                  "training_store contains one product, XBAD, the Legacy Cable "
                                  "Pack, whose price is the string \"49.99\". "
                                  "It is there on purpose: Module 4 uses it in the $type labs to "
                                  "find values stored with the wrong type. "
                                  "Don't fix it now.")])),
        F.diagram(img(5), "One Collection, a Shared Core",
                  "Different products, the same core fields, flexible attributes.",
                  items=[("Shared core", "sku, name, category, price, tags, active, createdAt — "
                                         "same names, same types."),
                         ("Flexible attributes", "LAPTOP: processor, memoryGB · SHOE: sizes, "
                                                 "color · BOOK: author, isbn."),
                         ("One name per field", "name everywhere — never productName on one "
                                                "product and title on another."),
                         {"callout": ("Exercise 3.4", "You'll design this catalog yourself.")}],
                  takeaway="Keep the core identical across products and put category-specific "
                           "fields under attributes.",
                  notes=dn(5, [tp("Querying the flexible part",
                                  "Because the variable fields live under attributes, queries "
                                  "stay predictable: find({ category: \"LAPTOP\" }) uses the "
                                  "core, and find({ \"attributes.isbn\": \"978-0000000000\" }) "
                                  "finds the book B300.")])),

        # Part 2 ------------------------------------------------------------
        F.bridge(PARTS, 1, "Part 2: Designing Around Access Patterns",
                 "Flexible doesn't mean unplanned.",
                 so_far=["A document holds typed fields, nested documents and arrays",
                         "Choose each BSON type by its meaning",
                         "One collection can hold varied products"],
                 question="How does the application actually use the data — and how should "
                          "that shape the documents?",
                 covers=["Model around access patterns", "training_store's access patterns",
                         "Relationship types", "Estimating growth: bounded or not"],
                 notes=[tp("Why this part",
                           "MongoDB has a flexible schema, but a good schema supports the "
                           "application's common reads and writes efficiently."),
                        tp("The four steps",
                           "Identify the entities, identify their relationships, list the "
                           "important operations, and estimate how the data grows. "
                           "This part walks through all four for training_store.")]),
        F.diagram(img(6), "Model Data Around Access Patterns",
                  "Start from the operations — not from the tables.",
                  items=[("Operations first", "Browse products, view an order, read reviews — "
                                              "before any collection exists."),
                         ("Three questions", "Read together? Updated together? How fast does "
                                             "it grow?"),
                         ("Then shape and index", "Aggregate boundary → embed or reference → "
                                                  "indexes."),
                         {"callout": ("Principle", "Data accessed together is stored "
                                                   "together.")}],
                  takeaway="The application's most important operations decide the document "
                           "shape — design around the queries.",
                  notes=dn(6)),
        F.compare("training_store Access Patterns",
                  "The operations that shape our four collections.",
                  ["Access pattern", "Frequency", "Returned together", "Modeling implication"],
                  [("Find product by SKU", "High", "The whole product", "One product document"),
                   ("Browse category and price", "High", "Name, price", "Shared core fields"),
                   ("Show customer profile", "High", "Name, contact, addresses",
                    "Embed addresses"),
                   ("Show one order", "High", "Items, totals, address", "Embed items, snapshot"),
                   ("Customer order history", "Medium", "Order summaries",
                    "customerId on each order"),
                   ("Reviews for a product", "Medium", "Recent reviews", "Separate collection"),
                   ("Change order status", "Medium", "One order", "One-document update")],
                  [2.75, 1.25, 2.55, 2.55], row_h=0.54, size=13,
                  items=[("Entities", "Product, Customer, Order, Review."),
                         ("Relationships", "Customer → orders and reviews; product → reviews; "
                                           "order → items."),
                         {"callout": ("Exercise 3.2", "You'll build this table from the "
                                                      "requirements.")}],
                  takeaway="List each operation with how often it runs and what it returns "
                           "together — the implications follow.",
                  notes=[tp("Steps 1 and 2",
                            "The entities are Product, Customer, Order and Review. "
                            "A customer places many orders and writes many reviews, a product "
                            "receives many reviews, and an order contains many items."),
                         tp("Step 3: the operations",
                            "The content guide lists ten: find a product by SKU, browse by "
                            "category, search a price range, show a profile with addresses, "
                            "show one order, show order history, show a product's reviews, "
                            "calculate an average rating, update inventory and change an "
                            "order's status. "
                            "The table groups the ones that shape the documents most."),
                         tp("Read the last column",
                            "High-frequency reads that return one object become one document. "
                            "Lists that grow, such as order history and reviews, become "
                            "references. "
                            "A status change touches one order, so it is a single-document "
                            "update."),
                         tp("Frequencies",
                            "The frequencies are estimates for a typical store, like the ones "
                            "Exercise 3.2 asks for. "
                            "In a real project you would measure them.")]),
        F.diagram(img(7), "Relationship Types",
                  "One-to-one, one-to-many and many-to-many.",
                  items=[("One-to-one", "Customer → preferences: embedded as one "
                                        "sub-document."),
                         ("One-to-many", "Customer → orders: each order stores customerId."),
                         ("Many-to-many", "Orders ↔ products: linked through "
                                          "items[].productId."),
                         {"callout": ("Also ask", "How many on the many side — a few or "
                                                  "millions?")}],
                  takeaway="Name each relationship's type, then count the many side before "
                           "choosing a model.",
                  notes=dn(7)),
        F.diagram(img(8), "Estimate Growth: Bounded or Unbounded?",
                  "Small arrays can be embedded — growing ones can't.",
                  items=[("Bounded", "A customer's few addresses; an order's handful of line "
                                     "items."),
                         ("Unbounded", "Every review a product will ever get — it keeps "
                                       "growing."),
                         ("Hard limit", "One BSON document can be at most 16 MiB."),
                         {"callout": ("training_store", "Reviews live in their own "
                                                        "collection.")}],
                  takeaway="Ask how large every array can become — embed the bounded ones, "
                           "move the unbounded ones out.",
                  notes=dn(8)),
        F.exercise("Exercise: Classify the training_store Relationships",
                   "Name the cardinality and the growth before you pick a model.",
                   scenario="Five relationships from the dataset. For each, decide how many sit "
                            "on the many side and whether it grows without limit.",
                   scenario_code="1  customer → addresses\n"
                                 "2  order → line items\n"
                                 "3  customer → orders\n"
                                 "4  product → reviews\n"
                                 "5  orders ↔ products",
                   tasks=["Name each relationship's type",
                          "Say bounded or unbounded, and why",
                          "Decide: embed or reference",
                          "Find the field that links each pair"],
                   expected=["1, 2: one-to-few, bounded — embed",
                             "3: one-to-many, grows — customerId",
                             "4: grows without limit — productId",
                             "5: many-to-many — items[].productId",
                             "Growth, not nesting, decides"],
                   minutes=10,
                   takeaway="Cardinality and growth decide the model — the same question works "
                            "for any relationship.",
                   notes=[tp("How to run it",
                             "Pairs, five minutes, then compare with the expected column. "
                             "Ask each pair to justify one answer out loud."),
                          tp("Addresses and items",
                             "A customer has a few addresses and an order has a few items. "
                             "Both are bounded and read with their parent, so they are embedded."),
                          tp("Orders and reviews",
                             "A customer's order history keeps growing, so each order stores "
                             "customerId instead of the customer holding an array of orders. "
                             "Reviews can grow without limit, so each review stores productId."),
                          tp("Orders and products",
                             "One order contains many products and one product appears in many "
                             "orders. "
                             "training_store links them through items[].productId, plus a "
                             "snapshot of sku, name and unitPrice — Part 3 explains why.")]),

        # Part 3 ------------------------------------------------------------
        F.bridge(PARTS, 2, "Part 3: Embedding Versus Referencing",
                 "The two ways MongoDB represents a relationship.",
                 so_far=["Design starts from access patterns",
                         "Name the relationship and count the many side",
                         "Arrays must stay bounded"],
                 question="When should related data live inside the document — and when in "
                          "another collection?",
                 covers=["Embedding: customer profiles", "Referencing: product reviews",
                         "How to choose between them", "A decision tree",
                         "Orders: a hybrid model", "Historical snapshots"],
                 notes=[tp("The two approaches",
                           "MongoDB represents relationships in two main ways: embed the related "
                           "data inside a document, or reference a document stored in another "
                           "collection."),
                        tp("Where this part ends",
                           "By the end, learners should be able to explain every embed and "
                           "reference choice in training_store, and why an order copies some "
                           "product fields.")]),
        F.diagram(img(9), "Embedding: Customer Profiles",
                  "Addresses belong to the customer and are read with the profile.",
                  items=[{"code": "{ customerNumber: \"C101\",\n"
                                  "  name: { first: \"Aisha\",\n"
                                  "          last: \"Khan\" },\n"
                                  "  addresses: [ {\n"
                                  "    type: \"SHIPPING\",\n"
                                  "    city: \"Toronto\", … } ] }",
                          "label": "customers: C101 (trimmed)", "size": 11},
                         ("Advantages", "One read, no join, atomic updates inside one "
                                        "document."),
                         ("Limitations", "Duplication, bigger documents — and never for "
                                         "unbounded data.")],
                  takeaway="Embed data that belongs to the parent, stays small and is read with "
                           "it.",
                  notes=dn(9)),
        F.diagram(img(10), "Referencing: Product Reviews",
                  "Each review points to its product and its author.",
                  items=[{"code": "{ productId: ObjectId(\"…\"),\n"
                                  "  sku: \"L100\",\n"
                                  "  customerId: ObjectId(\"…\"),\n"
                                  "  rating: 5,\n"
                                  "  title: \"Excellent for travel\" }",
                          "label": "reviews: the L100 review (trimmed)", "size": 11},
                         ("Advantages", "Small documents, independent growth, no large "
                                        "duplication."),
                         ("Limitations", "A second query or $lookup; multi-document changes may "
                                         "need a transaction.")],
                  takeaway="Reference data that is shared, changes on its own or grows without "
                           "limit.",
                  notes=dn(10)),
        F.compare("How to Choose Between Them",
                  "Nine considerations from the modeling guide.",
                  ["Consideration", "Embed", "Reference"],
                  [("Normally read together", "Yes", "Possibly"),
                   ("Small and bounded", "Yes", "Not required"),
                   ("Belongs to one parent", "Yes", "Possibly"),
                   ("Grows continuously", "No", "Yes"),
                   ("Shared by many records", "No", "Yes"),
                   ("Changes independently", "Sometimes", "Yes"),
                   ("One-query retrieval matters", "Yes", "Needs $lookup"),
                   ("Duplication would be large", "No", "Yes"),
                   ("Atomic update required", "Strong choice", "Transaction")],
                  [3.85, 1.95, 2.40], row_h=0.44, size=13,
                  items=[("Rule", "Embed bounded data that belongs to the parent; reference "
                                  "independent, shared or unbounded data."),
                         {"callout": ("Exercise 3.3", "Eight relationships to decide.")}],
                  takeaway="Embed bounded data that belongs to the parent; reference "
                           "independent, shared or unbounded data.",
                  notes=[tp("How to read the table",
                            "Each row is one question about the relationship. "
                            "Most rows point clearly one way; a few say sometimes or possibly, "
                            "which is where judgement comes in."),
                         tp("The strongest signals",
                            "Continuous growth and sharing across many records point to "
                            "referencing. "
                            "Being read together, small and owned by one parent point to "
                            "embedding."),
                         tp("Atomicity",
                            "A write to one document is atomic. "
                            "If several related values must change together, embedding them "
                            "gives that for free; referenced data may need a multi-document "
                            "transaction."),
                         tp("Changes independently",
                            "Sometimes appears under embed because a snapshot is embedded on "
                            "purpose even though the source changes. "
                            "The order's copy of a product price is the classic example.")]),
        F.diagram(img(11), "An Embedding Decision Tree",
                  "Three questions — all yes means embed.",
                  items=[("Read together?", "Is it shown with the parent on the common "
                                            "page?"),
                         ("Bounded size?", "Does it have a small, known maximum?"),
                         ("Same lifecycle?", "Is it created and deleted with the parent?"),
                         {"callout": ("Reviews", "Fail bounded size — so they are "
                                                 "referenced.")}],
                  takeaway="Embed only when the data is read together, bounded and shares the "
                           "parent's lifecycle.",
                  notes=dn(11)),
        F.diagram(img(12), "Modeling Orders: A Hybrid Approach",
                  "Reference the customer and products; embed items and the address.",
                  items=[{"code": "{ orderNumber: \"O5001\",\n"
                                  "  customerId: ObjectId(\"…\"),\n"
                                  "  items: [\n"
                                  "    { productId: ObjectId(\"…\"),\n"
                                  "      sku: \"L100\",\n"
                                  "      name: \"Business Laptop\",\n"
                                  "      quantity: 1,\n"
                                  "      unitPrice: Decimal128(\"1299.99\") },\n"
                                  "    … ],               // A410 × 2\n"
                                  "  shippingAddress: { city: \"Toronto\", … },\n"
                                  "  total: Decimal128(\"1514.17\") }",
                          "label": "orders: O5001 (trimmed)", "size": 10},
                         ("Reference", "customerId → the customer; productId → the catalog."),
                         ("Embed", "Line items and the shipping address, read with the "
                                   "order.")],
                  takeaway="One order document answers \"show this order\" — while customers "
                           "and products keep changing on their own.",
                  notes=dn(12, [tp("The real O5001",
                                   "After load.js, O5001 is Aisha Khan's order: one Business "
                                   "Laptop at 1299.99 and two Wireless Mice at 19.99, subtotal "
                                   "1339.97, tax 174.20, total 1514.17. "
                                   "Payment is PENDING and fulfillment is NEW."),
                                tp("Lab 2, Step 4, builds a smaller O5001",
                                   "In the hand-insert path, Lab 2, Step 4, creates O5001 with the "
                                   "laptop only, so its total is 1468.99. "
                                   "Reloading load.js at the start of Day 2 replaces it with the "
                                   "full version.")]),
                  panel_w=4.45),
        F.diagram(img(13), "Historical Snapshots",
                  "The order keeps what the customer paid, not today's price.",
                  items=[("Snapshot", "unitPrice and name are copied at purchase — and never "
                                      "synced."),
                         ("Current price", "Lives only in products; the catalog can change "
                                           "freely."),
                         ("In training_store", "If L100's price changes, O5001 still shows "
                                               "1299.99."),
                         {"callout": ("Copy with care", "Freeze history — don't copy data that "
                                                        "must stay current.")}],
                  takeaway="Duplication is deliberate when it preserves history — a snapshot "
                           "should never follow the catalog.",
                  notes=dn(13, [tp("Customer data is different",
                                   "training_store orders don't copy the customer's email or "
                                   "profile, because those must stay current. "
                                   "They reference the customer and copy only the shipping "
                                   "address, which is part of the order's history.")])),

        # Part 4 ------------------------------------------------------------
        F.bridge(PARTS, 3, "Part 4: Anti-Patterns and Schema Patterns",
                 "What goes wrong — and the proven fixes.",
                 so_far=["Embed bounded data that belongs to the parent",
                         "Reference shared, independent or unbounded data",
                         "Snapshots preserve history on purpose"],
                 question="Which mistakes do first designs make — and which patterns solve "
                          "common modeling problems?",
                 covers=["Collections copied from tables", "Inconsistent names and types",
                         "Seven schema patterns", "Attribute, Subset and Computed up close"],
                 notes=[tp("Why this part",
                           "A technically valid model can still perform badly. "
                           "We look at the mistakes first designs make, then at named patterns "
                           "that experienced teams reuse."),
                        tp("Link to the exercises",
                           "Exercise 3.6 corrects a flawed product document, and Exercise 3.7 "
                           "matches requirements to the seven patterns.")]),
        F.diagram(img(14), "Anti-Pattern: Collections Copied from Tables",
                  "One collection per table turns every page into joins.",
                  items=[("The mistake", "A collection for every small component; the app "
                                         "rebuilds each order."),
                         ("The cost", "$lookup × 3 — more round trips, more code, slower "
                                      "pages."),
                         ("The fix", "Embed what the page reads together; reference the "
                                     "rest."),
                         {"callout": ("training_store", "One O5001 document is one read.")}],
                  takeaway="Don't translate tables into collections — model the documents the "
                           "application reads.",
                  notes=dn(14)),
        F.diagram(img(15), "Anti-Pattern: Inconsistent Names and Types",
                  "One field should have one name — and one type.",
                  items=[("Names", "customerId, customer_id, custId — a query on one misses "
                                   "the others."),
                         {"code": "{ price: 29.99 }\n"
                                  "{ price: \"29.99\" }\n"
                                  "{ price: { amount: 29.99 } }",
                          "label": "Types: three shapes, one field", "kind": "bad",
                          "size": 11},
                         ("The fix", "One name, one structure per field — then enforce it "
                                     "with validation."),
                         {"callout": ("training_store", "camelCase everywhere: customerId, "
                                                        "createdAt.")}],
                  takeaway="Consistency is a correctness rule: queries match exact names and "
                           "compare by type.",
                  notes=dn(15, [tp("More mistakes to watch",
                                   "Two more from the guide. "
                                   "Don't copy frequently changing shared data, such as a "
                                   "customer's current profile, into thousands of documents. "
                                   "And don't design without the queries: a valid model can "
                                   "still be slow if it doesn't support the common queries and "
                                   "indexes.")])),
        F.compare("Seven Common Schema Patterns",
                  "Named solutions to recurring modeling problems.",
                  ["Pattern", "Use it when", "Example"],
                  [("Attribute", "Many optional, searchable fields", "Product specifications"),
                   ("Bucket", "Many small time-based events", "Sensor readings per hour"),
                   ("Subset", "The page needs only the hot few", "Latest three reviews"),
                   ("Computed", "The same calculation repeats", "Stored average rating"),
                   ("Extended reference", "A few fields read with the link",
                    "Customer name on an order"),
                   ("Outlier", "A few documents are far larger", "A viral product's reviews"),
                   ("Polymorphic", "Different shapes, shared queries",
                    "Laptops, shoes, books")],
                  [2.30, 3.45, 3.00], row_h=0.56, size=13,
                  items=[("Every pattern costs", "Faster reads usually mean extra writes or "
                                                 "extra code."),
                         ("Already here", "products is polymorphic; order items use extended "
                                          "references."),
                         {"callout": ("Exercise 3.7", "Match seven requirements to these "
                                                      "patterns.")}],
                  takeaway="Patterns are proven trade-offs — pick one only when its problem is "
                           "really in your access patterns.",
                  notes=[tp("Attribute and Polymorphic",
                            "Attribute handles many optional fields that must be searchable. "
                            "Polymorphic keeps different shapes in one collection because the "
                            "application queries them together, like our products."),
                         tp("Bucket and Outlier",
                            "Bucket groups many small events, such as sensor readings, into one "
                            "document per time window. "
                            "Outlier gives the rare very large case, like a product with an "
                            "extreme number of reviews, special overflow handling so ordinary "
                            "documents stay simple."),
                         tp("Subset, Computed and Extended reference",
                            "Subset embeds only the hot part of a large relationship. "
                            "Computed stores a calculated result. "
                            "Extended reference copies a few frequently read fields next to the "
                            "reference, as our order items copy sku and name, and as our reviews "
                            "copy sku."),
                         tp("Trade-offs",
                            "Every pattern makes some reads cheaper by making writes or code "
                            "more complex. "
                            "Apply one only when its problem appears in the access patterns.")]),
        F.diagram(img(16), "The Attribute Pattern",
                  "Many optional attributes, one index.",
                  items=[("The problem", "Every searchable attribute would need its own "
                                         "index."),
                         ("The pattern", "Store { k, v } pairs; index attributes.k and "
                                         "attributes.v together."),
                         ("training_store today", "attributes is a plain object — fine for a "
                                                  "few known fields."),
                         {"callout": ("Trade-off", "Simpler indexing, less natural "
                                                   "documents.")}],
                  takeaway="Use the Attribute pattern when many optional fields must all be "
                           "searchable.",
                  notes=dn(16)),
        F.diagram(img(17), "The Subset Pattern",
                  "Embed the hot few; keep the full history separate.",
                  items=[("The problem", "The product page needs three reviews, not all 248."),
                         ("The pattern", "Embed a small recentReviews array; keep every review "
                                         "in reviews."),
                         ("Trade-off", "A new review is written in two places."),
                         {"callout": ("training_store", "Not used yet — reviews live only in "
                                                        "reviews.")}],
                  takeaway="Subset keeps the common page to one read without embedding an "
                           "unbounded array.",
                  notes=dn(17)),
        F.diagram(img(18), "The Computed Pattern",
                  "Calculate once, store the result, read it many times.",
                  items=[("The problem", "Averaging every review on every page view."),
                         ("The pattern", "Store ratingAvg and reviewCount on the product."),
                         ("Trade-off", "Recompute on each new review, or on a schedule."),
                         {"callout": ("Module 5", "You'll compute averages with $group.")}],
                  takeaway="Store a calculated value when it is read far more often than its "
                           "inputs change.",
                  notes=dn(18)),

        # Part 5 ------------------------------------------------------------
        F.bridge(PARTS, 4, "Part 5: Validate, Evolve and Build",
                 "Enforce the model, plan for change, then build it.",
                 so_far=["Avoid table-shaped collections and mixed types",
                         "Seven patterns solve recurring problems",
                         "Every pattern is a trade-off"],
                 question="How do we enforce the model, change it safely — and build it in "
                          "training_store?",
                 covers=["$jsonSchema validation", "Validation level and action",
                         "Evolving a schema", "Querying nested fields and arrays",
                         "Joining references with $lookup", "Indexes for the access patterns"],
                 notes=[tp("Why this part",
                           "A flexible schema still needs guardrails. "
                           "We add validation, plan how the schema can change, and then build "
                           "and query the model in the labs."),
                        tp("Lab link",
                           "The slides in this part follow Steps 5 and 6 of Lab 2. "
                           "The full lab, labs/day-01/lab2/LAB-2-GUIDE.md, comes after the "
                           "knowledge check and Exercises 3.1 to 3.9.")]),
        F.diagram(img(19), "Schema Validation with $jsonSchema",
                  "Flexible fields, enforced rules.",
                  items=[("required", "Fields every document must have."),
                         ("bsonType", "The type each field must hold: string, decimal, bool, "
                                      "date."),
                         ("minimum", "Range rules — price can't be negative."),
                         {"callout": ("Lab 2, Step 6", "Requires decimal for price — stricter than "
                                                 "number.")}],
                  takeaway="Validation lets the database reject documents that break the "
                           "model's contract.",
                  notes=dn(19, [tp("The Lab 2, Step 6 validator",
                                   "Step 6 creates a separate validated_products collection "
                                   "that requires sku, name, category, price, active and "
                                   "createdAt. "
                                   "price must be decimal with minimum 0, active must be bool "
                                   "and createdAt must be date. "
                                   "Extra optional fields are still allowed."),
                                tp("Why a separate collection",
                                   "The main products collection keeps XBAD's string price for "
                                   "Module 4, so the lab tries validation on a new collection "
                                   "instead.")])),
        F.diagram(img(20), "Validation Level and Action",
                  "When rules run — and what a failure does.",
                  items=[("validationLevel", "strict checks every write; moderate skips "
                                             "already-invalid documents."),
                         ("validationAction", "error rejects the write; warn stores it and "
                                              "logs a warning."),
                         {"code": "db.runCommand({\n"
                                  "  collMod: \"validated_products\",\n"
                                  "  validationLevel: \"moderate\",\n"
                                  "  validationAction: \"warn\" })",
                          "label": "Relax rules on old data", "size": 11},
                         {"callout": ("Default", "strict + error.")}],
                  takeaway="Keep strict and error for new data; use moderate or warn only while "
                           "old documents are fixed.",
                  notes=dn(20)),
        F.diagram(img(21), "Evolving a Schema Safely",
                  "Old and new shapes can coexist while you migrate.",
                  items=[("Non-breaking first", "Adding an optional field keeps old readers "
                                                "working."),
                         ("Version the shape", "schemaVersion tells the reader which shape it "
                                               "has."),
                         ("Migrate in steps", "Tolerant readers → new writes → backfill → "
                                              "require."),
                         {"callout": ("Demo 3.6", "v1 price becomes v2 pricing: { amount, "
                                                  "currency }.")}],
                  takeaway="Evolve a schema in steps — readers first, backfill later, validation "
                           "last.",
                  notes=dn(21)),
        F.code("Query Nested Fields and Arrays",
               "Lab 2, Step 5: dot notation walks into documents and arrays.",
               [{"label": "Products", "kind": "info", "code":
                 "db.products.find({ category: \"LAPTOP\" })\n"
                 "db.products.find(\n"
                 "  { \"attributes.memoryGB\": 16 })\n"
                 "db.products.find({ tags: \"technology\" })"},
                {"label": "Customers and orders", "kind": "info", "code":
                 "db.customers.find(\n"
                 "  { \"addresses.city\": \"Toronto\" })\n"
                 "db.orders.find(\n"
                 "  { \"items.sku\": \"L100\" })"}],
               points=[("Hand-built core", "L100 · L100 · B300 · C101 · O5001."),
                       ("After load.js", "LAPTOP returns L100, L110, L190; items.sku finds "
                                         "four orders."),
                       ("Arrays", "tags: \"technology\" matches any element of the array.")],
               takeaway="Dot notation reaches into embedded documents and arrays of "
                        "documents — always in quotes.",
               notes=[tp("Products",
                         "category LAPTOP returns the laptop. "
                         "\"attributes.memoryGB\": 16 walks into the embedded attributes "
                         "document and also returns L100. "
                         "tags: \"technology\" matches any element of the tags array, so it "
                         "returns the book, B300."),
                      tp("Customers and orders",
                         "\"addresses.city\": \"Toronto\" looks inside every element of the "
                         "addresses array and returns Aisha Khan, C101. "
                         "\"items.sku\": \"L100\" returns every order with a laptop line."),
                      tp("Two result sets",
                         "On the hand-built core from Lab 2, Steps 1-4, the results are L100, L100, B300, "
                         "C101 and O5001. "
                         "After load.js, the LAPTOP query returns three products, L100, L110 "
                         "and L190, and the items.sku query returns O5001, O6101, O6301 and "
                         "O6401. The other three queries return the same documents."),
                      tp("Why the quotes",
                         "A dotted path is not a valid JavaScript identifier, so mongosh needs "
                         "it as a quoted string. "
                         "Module 4 goes further with $elemMatch and array operators.")]),
        F.code("Join Referenced Data with $lookup",
               "The cost of referencing: combining needs another query or a join.",
               [{"label": "Reviews for L100, with the product name", "kind": "info", "code":
                 "const l100 = db.products.findOne({ sku: \"L100\" })\n"
                 "db.reviews.aggregate([\n"
                 "  { $match: { productId: l100._id } },\n"
                 "  { $lookup: { from: \"products\",\n"
                 "      localField: \"productId\",\n"
                 "      foreignField: \"_id\", as: \"product\" } },\n"
                 "  { $unwind: \"$product\" },\n"
                 "  { $project: { _id: 0, rating: 1, title: 1,\n"
                 "      productName: \"$product.name\" } }\n"
                 "])"},
                {"label": "Result (full load)", "kind": "good", "code":
                 "[\n"
                 "  {\n"
                 "    rating: 5,\n"
                 "    title: 'Excellent for travel',\n"
                 "    productName: 'Business Laptop'\n"
                 "  }\n"
                 "]"}],
               points=[("$lookup", "Joins each review to the product whose _id equals its "
                                   "productId."),
                       ("Needs the full load", "The hand-built core has no reviews yet."),
                       ("Shortcut", "Reviews copy sku, so find({ sku: \"L100\" }) needs no "
                                    "join.")],
               takeaway="Referenced data stays independent — combining it costs a $lookup or a "
                        "second query.",
               notes=[tp("Read the pipeline",
                         "The first line looks up the L100 product to get its _id. "
                         "$match keeps the reviews for that product. "
                         "$lookup adds a product array holding the matching product, $unwind "
                         "turns that array into a single embedded document, and $project keeps "
                         "rating, title and the product's name."),
                      tp("The result",
                         "After load.js, L100 has one review: Aisha Khan's rating 5, titled "
                         "Excellent for travel. "
                         "The product name comes from the products collection: Business "
                         "Laptop."),
                      tp("Dataset note",
                         "The content guide's version matches on a hard-coded mouseId and "
                         "projects a comment field. "
                         "training_store reviews have no comment; their text is in title and "
                         "body. "
                         "The hand-insert labs don't add reviews, so run this after load.js."),
                      tp("The trade-off",
                         "This is the price of referencing. "
                         "training_store softens it by copying sku into each review, an "
                         "extended reference, so the most common lookup needs no join. "
                         "Module 5 covers $lookup in depth.")]),
        F.code("Indexes That Follow the Access Patterns",
               "Design them now — Module 6 creates and tests them.",
               [{"label": "Already created by load.js", "kind": "good", "code":
                 "db.products.getIndexes()\n"
                 "// _id_, sku_unique\n"
                 "db.customers.getIndexes()\n"
                 "// _id_, customerNumber_unique,\n"
                 "// email_unique on contact.email\n"
                 "db.orders.getIndexes()\n"
                 "// _id_, orderNumber_unique"},
                {"label": "Planned from the access patterns", "kind": "info", "code":
                 "// browse by category and price\n"
                 "{ category: 1, price: 1 }      // products\n"
                 "// a customer's order history\n"
                 "{ customerId: 1, createdAt: -1 }  // orders\n"
                 "// a product's reviews, newest first\n"
                 "{ productId: 1, createdAt: -1 }   // reviews"}],
               points=[("Unique keys", "sku, customerNumber, orderNumber and email can't "
                                       "repeat."),
                       ("Pattern → index", "Each planned index serves one row of the access "
                                           "table."),
                       ("Module 6", "explain() will show each index being used.")],
               takeaway="Every important access pattern should have an index to support it — "
                        "plan them with the model.",
               notes=[tp("What already exists",
                         "load.js creates four unique indexes: sku_unique on products, "
                         "customerNumber_unique and email_unique on customers, and "
                         "orderNumber_unique on orders. "
                         "Every collection also has the automatic _id index."),
                      tp("What we plan",
                         "Browsing by category and price, a customer's order history newest "
                         "first, and a product's reviews newest first each get a compound "
                         "index. "
                         "We only design them here; Module 6 creates them and checks them with "
                         "explain()."),
                      tp("Dataset note",
                         "The content guide indexes { email: 1 } and { customerId: 1, "
                         "orderedAt: -1 }. "
                         "In training_store the email lives at contact.email and orders use "
                         "createdAt, so the slide uses those field names."),
                      tp("Don't re-run the unique ones",
                         "Creating the unique sku index again without its name would fail, "
                         "because an index with the same key already exists under the name "
                         "sku_unique.")]),
        F.exercise("Exercise: Predict the Nested Query Results",
                   "Read each query and say what it returns — before you run it.",
                   scenario="Run after load.js. Use the dataset facts: shoe sizes, accessory "
                            "connections, customer countries and order items.",
                   scenario_code="db.products.find(\n"
                                 "  { \"attributes.sizes\": 11 })\n"
                                 "db.products.find(\n"
                                 "  { \"attributes.connection\": \"USB-C\" })\n"
                                 "db.customers.find(\n"
                                 "  { \"addresses.country\": \"USA\" })\n"
                                 "db.orders.countDocuments(\n"
                                 "  { \"items.sku\": \"A410\" })",
                   tasks=["Predict each query's result",
                          "Name the embedded path it follows",
                          "Say where an array is crossed",
                          "Check on the instructor's screen"],
                   expected=["sizes 11 → Trail Shoe (S210)",
                             "USB-C → USB Hub, Docking Station",
                             "USA → Luis (C204), Maya (C620)",
                             "A410 → 3 orders",
                             "Arrays: sizes, addresses, items"],
                   minutes=10,
                   takeaway="Dot notation follows the document's shape — arrays and embedded "
                            "documents alike.",
                   notes=[tp("How to run it",
                             "Two minutes to write predictions, then run each query on the "
                             "instructor screen after load.js."),
                          tp("Shoe sizes",
                             "\"attributes.sizes\": 11 walks into attributes and then matches "
                             "any element of the sizes array. "
                             "Only the Trail Shoe, S210, with sizes 8 to 11, has an 11."),
                          tp("Connections and countries",
                             "Two accessories use USB-C: the USB Hub, A400, and the Docking "
                             "Station, A500. "
                             "The keyboard and the mouse are Bluetooth. "
                             "Two customers ship to the USA: Luis Romero, C204, in Austin, and "
                             "Maya Chen, C620, in San Francisco."),
                          tp("Wireless Mouse orders",
                             "A410 appears in O5001, O6201 and O6305, so countDocuments returns "
                             "3.")]),

        # Wrap-up ------------------------------------------------------------
        F.diagram(img(22), "Module 3 at a Glance",
                  "From access patterns to a read model, on one page.",
                  takeaway="Model from the access patterns, embed what is bounded and owned, "
                           "reference the rest — then enforce it.",
                  notes=dn(22)),
        F.knowledge("Knowledge Check", "Answer in your own words — then compare with a partner.",
                    ["What is the difference between a collection and a document?",
                     "What does BSON add to JSON?",
                     "What three things does _id guarantee?",
                     "When is embedding appropriate?",
                     "When is referencing appropriate?",
                     "Why are unbounded arrays dangerous?",
                     "What is the maximum size of one BSON document?",
                     "Why does an order copy the product price?",
                     "What does schema validation enforce?",
                     "Which pattern stores a calculated result?"],
                    notes=[tp("1. Collection and document",
                              "A document is one record of field-value pairs. "
                              "A collection is a group of related documents."),
                           tp("2. BSON",
                              "Binary JSON. It adds types such as Date, Decimal128, ObjectId and "
                              "Int32 that plain JSON doesn't have."),
                           tp("3. _id",
                              "It is unique within the collection, it always has an index, and "
                              "it can't change after the insert."),
                           tp("4. Embedding",
                              "When the data is read with the parent, stays bounded and belongs "
                              "to the parent — like addresses or order items."),
                           tp("5. Referencing",
                              "When the data is shared, changes independently or grows without "
                              "limit — like orders per customer or reviews per product."),
                           tp("6. Unbounded arrays",
                              "The document keeps growing, updates get more expensive, and it can "
                              "reach the size limit."),
                           tp("7. Size limit",
                              "16 MiB per BSON document."),
                           tp("8. Price on the order",
                              "To keep the price the customer actually paid. "
                              "It is a snapshot, so it must not follow later catalog changes."),
                           tp("9. Validation",
                              "Required fields, BSON types and value rules such as a minimum, "
                              "checked on inserts and updates. "
                              "It doesn't design the model for you."),
                           tp("10. Calculated result",
                              "The Computed pattern. "
                              "For time-based measurements the answer would be Bucket, and for "
                              "copied referenced fields, Extended reference.")]),
        F.exercise("Exercise 3.1 — Identify Document Components",
                   "Module 3 checkpoint A: label every part of a customer document.",
                   kind="OFFICIAL CHECKPOINT A", minutes=10,
                   worksheet="labs/day-01/exercises/exercise-3.1-identify-document-components.md",
                   scenario="Pairs. Label the sample customer, then list candidate required "
                            "fields.",
                   scenario_code="{ _id: ObjectId(\"...\"),\n"
                                 "  customerNumber: \"C101\",\n"
                                 "  name: { first: \"Aisha\",\n"
                                 "          last: \"Khan\" },\n"
                                 "  email: \"aisha@example.com\",\n"
                                 "  tags: [\"premium\", \"newsletter\"],\n"
                                 "  active: true,\n"
                                 "  createdAt: ISODate(\"...\") }",
                   tasks=["Mark _id and say what it guarantees",
                          "Mark the scalars and the embedded name",
                          "Label the array, Boolean and date",
                          "List candidate required fields"],
                   expected=["_id: unique in the collection",
                             "Scalars: customerNumber, email",
                             "name: embedded, first and last",
                             "tags array · active · createdAt",
                             "Required: _id, customerNumber, name, email, active, createdAt"],
                   expected_title="Solution (after debrief)",
                   takeaway="Naming each part of a document is the first step to designing "
                            "one.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 3.1. The worksheet is "
                             "labs/day-01/exercises/exercise-3.1-identify-document-components.md; "
                             "the answer key is labs/day-01/exercises/solution/exercise-3.1-identify-document-components.md. "
                             "No MongoDB is needed."),
                          tp("Running it",
                             "Ten minutes in pairs. Reveal the solution column after two pairs "
                             "share their labels."),
                          tp("Worksheet versus dataset",
                             "The worksheet's customer is a teaching sample. "
                             "The loaded C101 keeps email inside a contact object, has a status "
                             "of ACTIVE instead of an active flag, and has no tags. "
                             "Both are valid designs; the labelling skill is the same.")]),
        F.exercise("Exercise 3.2 — Discover Application Access Patterns",
                   "Module 3 checkpoint B: turn requirements into access patterns.",
                   kind="OFFICIAL CHECKPOINT B", minutes=15,
                   worksheet="labs/day-01/exercises/exercise-3.2-discover-access-patterns.md",
                   scenario="The store must support product search, product pages, customer "
                            "profiles, order placement, order history, reviews and inventory "
                            "display.",
                   tasks=["Name the three most frequent reads",
                          "Write the data each returns together",
                          "Fill four or more table rows",
                          "Mark embed, reference or snapshot"],
                   expected=["Product by SKU · order by number · profile",
                             "Returned data is specific, not everything",
                             "Add order history and paginated reviews",
                             "Purchase-time price is a snapshot",
                             "At least one embed and one reference"],
                   expected_title="Solution (after debrief)",
                   takeaway="Access patterns turn vague requirements into concrete document "
                            "shapes.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 3.2. The worksheet is "
                             "labs/day-01/exercises/exercise-3.2-discover-access-patterns.md; "
                             "the answer key is labs/day-01/exercises/solution/exercise-3.2-discover-access-patterns.md."),
                          tp("Table columns",
                             "Each row needs the access pattern, its frequency, the data "
                             "returned together, and the modeling implication. "
                             "The worksheet starts two rows for them: find product by SKU and "
                             "retrieve order."),
                          tp("What to listen for",
                             "Returned together must be specific, such as items, totals, "
                             "address and status, not just everything. "
                             "Compare their table with the training_store access-pattern slide "
                             "from Part 2.")]),
        F.exercise("Exercise 3.3 — Embed or Reference?",
                   "Module 3 checkpoint C: decide eight relationships and justify each.",
                   kind="OFFICIAL CHECKPOINT C", minutes=15,
                   worksheet="labs/day-01/exercises/exercise-3.3-embed-or-reference.md",
                   scenario="Write Embed or Reference and a one-line reason: ownership, size or "
                            "growth.",
                   scenario_code="1  Primary contact information\n"
                                 "2  Complete order history\n"
                                 "3  Order line items\n"
                                 "4  A product's millions of reviews\n"
                                 "5  An employee's office address\n"
                                 "6  Blog post tags\n"
                                 "7  Purchase-time product price\n"
                                 "8  Complete transaction history",
                   tasks=["Decide relationships 1–4",
                          "Decide relationships 5–8",
                          "Justify with bounded or unbounded",
                          "Explain the one 'it depends'"],
                   expected=["1 Embed · 2 Reference",
                             "3 Embed · 4 Reference",
                             "5 Depends on reuse",
                             "6 Embed · 7 Embed (snapshot)",
                             "8 Reference"],
                   expected_title="Solution (after debrief)",
                   takeaway="Unbounded histories are referenced; owned, bounded data is "
                            "embedded.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 3.3. The worksheet is "
                             "labs/day-01/exercises/exercise-3.3-embed-or-reference.md; "
                             "the answer key is labs/day-01/exercises/solution/exercise-3.3-embed-or-reference.md."),
                          tp("The answers",
                             "Contact information, line items and tags are embedded. "
                             "Order history, millions of reviews and a complete transaction "
                             "history are referenced because they grow without limit. "
                             "The purchase-time price is embedded as a snapshot."),
                          tp("The 'it depends'",
                             "An office address is embedded if each employee has their own, and "
                             "referenced if many employees share the same office record that "
                             "changes independently.")]),
        F.exercise("Exercise 3.4 — Model a Product Catalog",
                   "Module 3 checkpoint D: three products, one consistent core.",
                   kind="OFFICIAL CHECKPOINT D", minutes=20,
                   worksheet="labs/day-01/exercises/exercise-3.4-model-a-product-catalog.md",
                   scenario="Common fields: sku, name, description, category, price, active, "
                            "creation date.",
                   scenario_code="Laptop  processor, memory,\n"
                                 "        storage, screen size\n"
                                 "Shoe    size, color, material,\n"
                                 "        gender category\n"
                                 "Book    author, ISBN, publisher,\n"
                                 "        language",
                   tasks=["List core fields and BSON types",
                          "Decide: top level or attributes",
                          "Write one laptop, shoe and book",
                          "Check names and types match"],
                   expected=["sku string · price Decimal128",
                             "active Boolean · createdAt Date",
                             "Type-specific data in attributes",
                             "Queryable by category and attributes.isbn",
                             "No productPrice beside price"],
                   expected_title="Solution (after debrief)",
                   takeaway="A consistent core with nested attributes keeps a varied catalog "
                            "queryable.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 3.4. The worksheet is "
                             "labs/day-01/exercises/exercise-3.4-model-a-product-catalog.md; "
                             "the answer key is labs/day-01/exercises/solution/exercise-3.4-model-a-product-catalog.md. "
                             "MongoDB is optional; learners write documents in a scratch file."),
                          tp("A model answer",
                             "training_store's L100, S200 and B300 are a good reference answer: "
                             "the same core fields, with processor and memoryGB, sizes and "
                             "material, or author and isbn under attributes. "
                             "The worksheet also asks for description, gender category and "
                             "publisher, which training_store doesn't store."),
                          tp("What to check",
                             "The same field names and types on all three, and no "
                             "category-specific field required for every product.")]),
        F.exercise("Exercise 3.5 — Model an Order Document",
                   "Module 3 checkpoint E: one order aggregate, justified.",
                   kind="OFFICIAL CHECKPOINT E", minutes=20,
                   worksheet="labs/day-01/exercises/exercise-3.5-model-an-order-document.md",
                   scenario="Find an order by number, show items and purchase-time prices, the "
                            "shipping address used, payment and fulfillment status, and list a "
                            "customer's orders.",
                   tasks=["Decide items, price, address, customer",
                          "Mark the historical snapshots",
                          "Write the order document",
                          "List the required fields"],
                   expected=["Items, prices, address: embedded",
                             "Customer: customerId reference",
                             "Money as Decimal128",
                             "One read by orderNumber",
                             "Same shape as Lab 2, Step 4"],
                   expected_title="Solution (after debrief)",
                   takeaway="An order is a hybrid: reference the customer, embed the purchase "
                            "facts.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 3.5. The worksheet is "
                             "labs/day-01/exercises/exercise-3.5-model-an-order-document.md; "
                             "the answer key is labs/day-01/exercises/solution/exercise-3.5-model-an-order-document.md."),
                          tp("Expected document",
                             "orderNumber, customerId, an items array with sku, name, quantity "
                             "and unitPrice, a shippingAddress, paymentStatus and "
                             "fulfillmentStatus, Decimal128 subtotal, tax and total, and "
                             "createdAt."),
                          tp("Justification",
                             "One read by order number returns everything the page shows. "
                             "A customer's orders are found by customerId. "
                             "Prices never silently follow the catalog.")]),
        F.exercise("Exercise 3.6 — Find and Correct Schema Anti-Patterns",
                   "Module 3 checkpoint F: fix a flawed product document.",
                   kind="OFFICIAL CHECKPOINT F", minutes=15,
                   worksheet="labs/day-01/exercises/exercise-3.6-correct-schema-anti-patterns.md",
                   scenario="A teammate wrote this product document:",
                   scenario_code="{\n"
                                 "  productId: \"P1001\",\n"
                                 "  price: \"49.99\",\n"
                                 "  isActive: \"yes\",\n"
                                 "  allReviews: [\n"
                                 "    // unlimited growth\n"
                                 "  ],\n"
                                 "  created: \"September 20, 2026\"\n"
                                 "}",
                   tasks=["Name every problem you see",
                          "Fix the types",
                          "Move the reviews out",
                          "Choose an _id / sku convention"],
                   expected=["String price, text Boolean",
                             "Unbounded allReviews array",
                             "Display-text date",
                             "Decimal128, true, a real Date",
                             "Reviews in their own collection"],
                   expected_title="Solution (after debrief)",
                   takeaway="Most anti-patterns are wrong types or unbounded growth — both are "
                            "easy to spot once you look.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 3.6. The worksheet is "
                             "labs/day-01/exercises/exercise-3.6-correct-schema-anti-patterns.md; "
                             "the answer key is labs/day-01/exercises/solution/exercise-3.6-correct-schema-anti-patterns.md."),
                          tp("The problems",
                             "The price is a string, the Boolean is the text yes, allReviews "
                             "grows without limit, created is a display string rather than a "
                             "date, and productId is used instead of a clear _id or sku "
                             "convention."),
                          tp("The corrected document",
                             "sku: \"P1001\" with an ObjectId _id, price: Decimal128(\"49.99\"), "
                             "active: true, createdAt as a real date, and no reviews array. "
                             "That is exactly the shape of training_store's Wireless Keyboard, "
                             "P1001.")]),
        F.exercise("Exercise 3.7 — Select a Schema Design Pattern",
                   "Module 3 checkpoint G: match seven requirements to patterns.",
                   kind="OFFICIAL CHECKPOINT G", minutes=15,
                   worksheet="labs/day-01/exercises/exercise-3.7-select-a-schema-pattern.md",
                   scenario="Choose Attribute, Bucket, Subset, Computed, Extended reference, "
                            "Outlier or Polymorphic.",
                   scenario_code="1  Sensor readings grouped by hour\n"
                                 "2  Latest three product reviews\n"
                                 "3  Stored average rating\n"
                                 "4  Dynamic product specifications\n"
                                 "5  Customer name copied into order\n"
                                 "6  Rare products, huge review volume\n"
                                 "7  Many product types, one collection",
                   tasks=["Match requirements 1–4",
                          "Match requirements 5–7",
                          "Give one benefit and one cost",
                          "Explain Bucket and Outlier"],
                   expected=["1 Bucket · 2 Subset",
                             "3 Computed · 4 Attribute",
                             "5 Extended reference",
                             "6 Outlier · 7 Polymorphic"],
                   expected_title="Solution (after debrief)",
                   takeaway="Each pattern answers one recurring problem — name the problem "
                            "first.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 3.7. The worksheet is "
                             "labs/day-01/exercises/exercise-3.7-select-a-schema-pattern.md; "
                             "the answer key is labs/day-01/exercises/solution/exercise-3.7-select-a-schema-pattern.md."),
                          tp("Bucket versus one document per event",
                             "Bucket stores an hour of readings in one document, so there are "
                             "far fewer documents and index entries, at the cost of updating a "
                             "growing bucket."),
                          tp("Why Outlier exists",
                             "Most products have a few reviews. "
                             "Outlier keeps the normal design for them and adds overflow "
                             "handling only for the rare product with a huge volume.")]),
        F.exercise("Exercise 3.8 — Design Collection Validation",
                   "Module 3 checkpoint H: a $jsonSchema for products.",
                   kind="OFFICIAL CHECKPOINT H", minutes=15,
                   worksheet="labs/day-01/exercises/exercise-3.8-design-collection-validation.md",
                   scenario="A valid product must contain these fields:",
                   scenario_code="sku        string\n"
                                 "name       string\n"
                                 "category   string\n"
                                 "price      decimal, not negative\n"
                                 "active     Boolean\n"
                                 "createdAt  date",
                   tasks=["Write the required array",
                          "Give each field a bsonType",
                          "Add minimum: 0 to price",
                          "Wrap it in $jsonSchema"],
                   expected=["Six required field names",
                             "price: decimal, minimum 0",
                             "active: bool · createdAt: date",
                             "bsonType: \"object\" at the top",
                             "Extra fields still allowed"],
                   expected_title="Solution (after debrief)",
                   takeaway="A validator turns the model's contract into rules the database "
                            "enforces.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 3.8. The worksheet is "
                             "labs/day-01/exercises/exercise-3.8-design-collection-validation.md; "
                             "the answer key is labs/day-01/exercises/solution/exercise-3.8-design-collection-validation.md. "
                             "Learners may type the validator in a scratch file; running it "
                             "comes in Lab 2, Step 6."),
                          tp("Watch the type names",
                             "In $jsonSchema the BSON type names are decimal, bool and date, not "
                             "Decimal128, Boolean and Date. "
                             "price must be decimal, not double or string."),
                          tp("Level and action",
                             "Learners who know them can add validationLevel and "
                             "validationAction; the defaults are strict and error.")]),
        F.exercise("Exercise 3.9 — Design a Support-Ticket Data Model",
                   "Module 3 checkpoint I: a complete design challenge.",
                   kind="OFFICIAL CHECKPOINT I", minutes=25,
                   worksheet="labs/day-01/exercises/exercise-3.9-support-ticket-challenge.md",
                   scenario="Create tickets, assign agents, set status and priority, add "
                            "comments and tags, show recent comments with the ticket, keep a "
                            "complete audit history, and search by customer, agent, status "
                            "and priority.",
                   tasks=["List access patterns and collections",
                          "Mark embedded, referenced, unbounded",
                          "Draft one ticket with BSON types",
                          "List validation rules and indexes"],
                   expected=["tickets, customers, agents, audit_events",
                             "Embed: assignee, tags, recentComments",
                             "Full comments and audit: separate",
                             "Indexes: customerId, agentId, status, priority"],
                   expected_title="Suggested direction",
                   takeaway="The same method works for any application: patterns, "
                            "relationships, growth, then rules.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 3.9, the practical challenge. The worksheet is "
                             "labs/day-01/exercises/exercise-3.9-support-ticket-challenge.md; "
                             "the answer key is labs/day-01/exercises/solution/exercise-3.9-support-ticket-challenge.md. Design only; don't create indexes."),
                          tp("The ticket document",
                             "ticketNumber, customerId, an assignee summary, status, priority, "
                             "tags, a bounded recentComments array and timestamps. "
                             "Validation requires those keys."),
                          tp("What grows",
                             "The complete comment history and the audit trail grow without "
                             "limit, so they live in their own collections, such as comments "
                             "and audit_events. "
                             "Likely indexes are customerId, assignee.agentId, status and "
                             "priority.")]),
        F.exercise("Lab 2 — Create and Populate training_store",
                   "Day 1 hands-on: Steps 1–7 by hand, or the time-boxed load.js path.",
                   kind="OFFICIAL LAB", minutes=90,
                   worksheet="labs/day-01/lab2/LAB-2-GUIDE.md",
                   scenario="Path A (50 min): the instructor loads the full dataset. Path B "
                            "(90 min): type the core by hand.",
                   scenario_code="# Path A, in PowerShell\n"
                                 "mongosh \"mongodb://localhost:27017\" `\n"
                                 "  .\\datasets\\training_store\\load.js",
                   tasks=["Step 1 Create the four collections",
                          "Steps 2–3 Insert L100, S200, B300, C101",
                          "Step 4 Insert O5001 with references",
                          "Step 5 Query nested fields and arrays",
                          "Step 6 Validate · Step 7 Review"],
                   expected=["Path A: 13 · 6 · 17 · 6",
                             "Path B: 3 · 1 · 1 · 0",
                             "O5001 customerId = C101's _id",
                             "Invalid insert rejected",
                             "XBAD's string price noted"],
                   expected_title="Expected counts",
                   takeaway="By the end of Day 1, training_store exists with a model you can "
                            "explain field by field.",
                   notes=[tp("Official lab",
                             "This is Day 1 Lab 2, labs/day-01/lab2/LAB-2-GUIDE.md. "
                             "The expected output of every step is in "
                             "labs/day-01/lab2/solution/LAB-2-SOLUTION.md. "
                             "Path A takes about 50 minutes: load.js replaces Steps 1 to 4, "
                             "then learners do Steps 5 to 7. "
                             "Path B, all seven steps by hand, takes about 90."),
                          tp("Path A",
                             "Run load.js from the repository root in PowerShell, not inside "
                             "mongosh. The backtick ending the first line is PowerShell's line continuation, so "
                             "both lines run as one command. "
                             "Counts are products 13, customers 6, orders 17 and reviews 6. "
                             "Then inspect L100, C101, O5001 and the L100 review."),
                          tp("Path B",
                             "Step 1 creates the collections, Step 2 inserts L100, S200 and "
                             "B300, Step 3 inserts C101, and Step 4 inserts O5001 using the "
                             "customer's _id and the product's price. "
                             "Step 5 runs the nested queries, Step 6 creates "
                             "validated_products and Step 7 reviews the model against a "
                             "checklist."),
                          tp("Counts in the order products, customers, orders, reviews",
                             "The hand-built core has 3 products, 1 customer, 1 order and no "
                             "reviews. "
                             "Step 4's O5001 has only the laptop, total 1468.99; the load.js "
                             "version also has two Wireless Mice, total 1514.17."),
                          tp("Before Day 2",
                             "Whichever path was used, reload load.js at the start of Day 2 so "
                             "Modules 4 and 5 have the full analytical data.")]),
        F.wrapup("Module 3 Summary and What's Next",
                 "From document structure to a modeled, populated training_store.",
                 can=["Read a document's fields, nesting and _id",
                      "Choose BSON types that match the meaning",
                      "Turn requirements into access patterns",
                      "Embed or reference — and justify it",
                      "Spot anti-patterns and pick a schema pattern",
                      "Validate, evolve and query the model"],
                 next_title="Next: Module 4 — The MongoDB Query Language",
                 questions=["How do I filter, project and sort documents?",
                            "How do I query arrays and embedded fields precisely?",
                            "How do I update and delete documents safely?"],
                 bring=("Day 2", "Reload training_store with load.js, and bring your Lab 2, "
                                 "Step 7 checklist."),
                 takeaway="Day 1 ends with a designed database; Day 2 starts querying it.",
                 notes=[tp("Recap",
                           "We read documents field by field, chose BSON types, discovered "
                           "access patterns, decided embed or reference with a snapshot where "
                           "history matters, learned the anti-patterns and seven schema "
                           "patterns, and added validation."),
                        tp("End of Day 1",
                           "Day 1 took us from the NoSQL landscape, to a running MongoDB, to "
                           "documents designed around access patterns. "
                           "training_store is ready for querying."),
                        tp("Next module",
                           "Module 4 uses training_store to teach find and findOne, filters and "
                           "operators, projection, array queries, sorting and counting, and "
                           "safe inserts, updates and deletes."),
                        tp("Before tomorrow",
                           "Reload load.js at the start of Day 2 and keep the same connection "
                           "string. "
                           "Bring the Lab 2, Step 7 checklist and its one planned improvement.")]),
    ]
