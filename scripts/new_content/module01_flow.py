#!/usr/bin/env python3
"""Slide order for the Module 1 deck: one story from relational tables to MongoDB.

Every concept diagram is merged with the slide that explains it (diagram plus the
points only that slide adds), so no idea appears twice. Part openers, mongosh
examples on the training_store sample database, in-flow practice exercises, a
knowledge check, the official Exercises 1.1-1.3 and a hand-off to Module 2
connect the ideas.
"""
from __future__ import annotations

import mdb_diagram_slides as DS
import mdb_flow_slides as F
import mdb_glossary as G
import mdb_visuals as V
from mdb_flow_slides import tp
from mdb_visuals import (
    DARK_GRAY, GREEN, LEFT, LIGHT_GRAY, LIGHT_NAVY, NAVY, ORANGE, PURPLE, RED, RIGHT, TEAL,
    WHITE,
)

PARTS = ["Part 1\nWhy NoSQL", "Part 2\nFour NoSQL models", "Part 3\nMongoDB's data model",
         "Part 4\nArchitecture and fit"]


# ---------------------------------------------------------------------------
# Custom slides
# ---------------------------------------------------------------------------
def _story(slide, y0, y1):
    lw = 7.70
    y = V.section(slide, LEFT, y0, lw, "The training_store sample database", icon="🛒",
                  fill=NAVY)
    collections = [("customers", "6 documents", NAVY), ("products", "13 documents", TEAL),
                   ("orders", "17 documents", PURPLE), ("reviews", "6 documents", GREEN)]
    cw, cg = (lw - 3 * 0.14) / 4, 0.14
    for k, (name, count, fill) in enumerate(collections):
        V.box(slide, LEFT + k * (cw + cg), y + 0.02, cw, 0.72,
              [(name, {"size": 15}), (count, {"size": 12, "bold": False})],
              fill=fill, size=15, margin=0.04)
    y = V.section(slide, LEFT, y + 1.02, lw, "One order, step by step", icon="🧾", fill=PURPLE)
    V.hflow(slide, LEFT, y + 0.02, ["Luis (C204) shops", "Adds shoe + keyboard",
                                    "Order O6102 placed", "Payment PAID", "Order DELIVERED"],
            box_w=(lw - 4 * 0.30) / 5, box_h=0.80, gap=0.30,
            fills=[LIGHT_GRAY, TEAL, PURPLE, GREEN, ORANGE],
            colors=[DARK_GRAY, WHITE, WHITE, WHITE, WHITE], size=12)
    V.callout(slide, LEFT, y + 1.10, lw, 1.00, "The module's question",
              "Where should data like this live — and in what shape should each record be "
              "stored?", size=14)

    rx = LEFT + lw + 0.40
    rw = RIGHT - rx
    body = V.card(slide, rx, y0, rw, y1 - y0, "Your lab: training_store", head_fill=RED,
                  title_size=14)
    V.text(slide, rx + 0.18, body, rw - 0.36, 1.05,
           "Exercise 1.3 opens this database in mongosh. The instructor loads it before class; "
           "Module 2 shows you how.", size=14)
    V.text(slide, rx + 0.18, body + 1.15, rw - 0.36, 0.34, "FIRST COMMANDS", size=13, bold=True,
           color=RED)
    V.code(slide, rx + 0.18, body + 1.52, rw - 0.36, 1.25,
           "show dbs\nuse training_store\nshow collections\ndb.orders.findOne()", size=13)


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
        *G.intro("module01"),
        F.custom(_story, "One Story Through the Module",
                 "The training_store sample database — and the exercises you will run on it.",
                 takeaway="The same store runs through every slide, so each new idea builds on "
                          "the last.",
                 notes=[tp("Why a running example",
                           "Instead of jumping between unrelated examples, we follow one online "
                           "store, training_store, through the whole module and the whole "
                           "course."),
                        tp("The four collections",
                           "customers holds 6 buyer profiles, products holds 13 catalog items "
                           "in four categories, orders holds 17 orders and reviews holds 6 "
                           "product reviews."),
                        tp("One order",
                           "Luis Romero, customer C204, bought a Running Shoe and a Wireless "
                           "Keyboard. That is order O6102: total 211.38, paid and delivered. "
                           "We will see this order as rows, as a document and in mongosh."),
                        tp("The question",
                           "Where should data like this live, and in what shape? "
                           "Every part of the module helps answer that."),
                        tp("Link to the lab",
                           "In Exercise 1.3 learners run these first commands against the "
                           "loaded dataset. If mongosh isn't installed yet, they follow on the "
                           "instructor's screen; Module 2 installs it.")]),

        # Part 1 ------------------------------------------------------------
        F.bridge(PARTS, 0, "Part 1: Why NoSQL",
                 "Start with the data modern applications produce.",
                 so_far=["You know the goals of this module",
                         "You met the training_store database"],
                 question="Why did databases beyond relational tables become necessary?",
                 covers=["Three kinds of application data", "Where relational databases work "
                                                         "well",
                         "Where they start to struggle", "What NoSQL means",
                         "Why organizations adopt it"],
                 notes=[tp("Where we start",
                           "Relational databases have run business applications for decades, "
                           "and they still do. We start by looking at the data itself."),
                        tp("What this part answers",
                           "We look at the kinds of data applications store, where tables work "
                           "well, and where they start to struggle. That explains why NoSQL "
                           "appeared.")]),
        F.diagram(img(3), "Structured, Semi-Structured and Unstructured Data",
                  "Rows and columns, nested fields — and data with no fixed fields.",
                  items=[("Structured", "Rows and columns with a fixed schema — prices and "
                                        "quantities."),
                         ("Semi-structured", "Nested fields and arrays whose shape can vary — "
                                             "product specs and tags."),
                         ("Unstructured", "No fixed fields at all — images, logs and video."),
                         {"callout": ("Our dataset", "training_store products are "
                                                     "semi-structured: each category has "
                                                     "its own attributes.")}],
                  takeaway="Tables are built for structured data — much of what modern apps "
                           "store is semi-structured.",
                  notes=dn(3)),
        F.diagram(img(4), "Where Relational Databases Work Well",
                  "A declared schema, enforced keys and well-known joins.",
                  items=[("Declared schema", "Tables, columns and types are fixed before data "
                                             "arrives."),
                         ("Enforced relationships", "Foreign keys tie every order to a real "
                                                    "customer."),
                         ("Well-known joins", "SQL rebuilds the full picture from customers, "
                                              "orders, items and products."),
                         {"callout": ("Still the right tool",
                                      "Stable structure plus strict integrity.")}],
                  takeaway="When the structure is stable and relationships must be enforced, "
                           "relational databases work very well.",
                  notes=dn(4)),
        F.diagram(img(5), "Challenges with Traditional Relational Models",
                  "One complete order means joining five tables.",
                  items=[("Many lookups", "Customer, address, order, items and payment — "
                                          "joined on every read."),
                         ("Rigid change", "A new product attribute needs a migration or more "
                                          "optional columns."),
                         ("Harder to scale out", "Joined tables are hard to spread across many "
                                                 "servers."),
                         {"callout": ("Costs, not failures",
                                      "They grow with change and volume.")}],
                  takeaway="The more pieces one business object is split into, the more work "
                           "every read and every change does.",
                  notes=dn(5)),
        F.code("Adding a New Kind of Product",
               "The catalog starts selling shoes — what has to change?",
               [{"label": "Relational: change the table first", "kind": "info", "code":
                 "ALTER TABLE products\n"
                 "  ADD COLUMN sizes    VARCHAR(40);\n"
                 "ALTER TABLE products\n"
                 "  ADD COLUMN color    VARCHAR(20);\n"
                 "ALTER TABLE products\n"
                 "  ADD COLUMN material VARCHAR(20);\n"
                 "-- laptops and books now carry\n"
                 "-- three empty columns each"},
                {"label": "Document: insert the new shape", "kind": "good", "code":
                 "db.products.insertOne({\n"
                 "  sku: \"S200\",\n"
                 "  name: \"Running Shoe\",\n"
                 "  category: \"SHOE\",\n"
                 "  price: Decimal128(\"129.99\"),\n"
                 "  attributes: {\n"
                 "    sizes: [7, 8, 9, 10],\n"
                 "    color: \"Blue\", material: \"Mesh\"\n"
                 "  }\n"
                 "})"}],
               points=[("Relational", "Every new attribute is a schema change, plus empty "
                                      "columns elsewhere."),
                       ("Document", "Each product carries only the fields it needs."),
                       {"callout": ("Still designed", "Flexible isn't random — Module 3 "
                                                      "models it.")}],
               takeaway="A fixed schema turns every new attribute into a migration; documents "
                        "let each product carry its own fields.",
               notes=[tp("The relational version",
                         "To sell shoes, the products table first needs new columns for sizes, "
                         "color and material. Every laptop and book row now has three empty "
                         "columns. The alternative is extra attribute tables, which means more "
                         "joins."),
                      tp("The document version",
                         "In MongoDB we insert the shoe with the fields it needs. This is the "
                         "shape of the real Running Shoe, SKU S200, in training_store, trimmed "
                         "for the slide; the real document also has tags, active and "
                         "createdAt."),
                      tp("Don't run it on the loaded data",
                         "training_store already contains S200, and sku has a unique index, so "
                         "this insert would fail with a duplicate key error. It shows how the "
                         "product got there."),
                      tp("The balance",
                         "Flexible doesn't mean random. Module 3 decides which fields every "
                         "product must share and which can vary.")]),
        F.diagram(img(6), "What Does NoSQL Mean?",
                  "Not Only SQL — relational and non-relational models side by side.",
                  items=[("Not Only SQL", "Databases that store data in models other than "
                                          "relational tables."),
                         ("Four families", "Document, key-value, column-family and graph."),
                         {"callout": ("Both exist",
                                      "Many real systems use SQL and NoSQL together.")}],
                  takeaway="NoSQL adds data models — it doesn't make SQL databases obsolete.",
                  notes=dn(6)),
        F.diagram(img(7), "Why Organizations Adopt NoSQL",
                  "Application growth creates four needs.",
                  items=[("Flexible schema", "Fields change as the product changes — no "
                                             "migration first."),
                         ("Horizontal scale", "Add servers instead of buying a bigger one."),
                         ("Availability", "Copies on several servers survive one failure."),
                         ("Faster delivery", "Store objects the way the application already "
                                             "uses them.")],
                  takeaway="The right database depends on the data, the access patterns, the "
                           "consistency needs and the scale.",
                  notes=dn(7)),
        F.exercise("Exercise: What Does One Order Page Cost?",
                   "Count the work behind a single page in the relational design.",
                   scenario="The order page shows O6102: Luis Romero's Running Shoe and "
                            "Wireless Keyboard, total 211.38.\n\nIn the relational design on "
                            "the challenges slide, that order lives in five tables.",
                   tasks=["List the tables the page must read",
                          "Count the joins needed",
                          "Name the key columns that link them",
                          "Sketch what one order document would hold"],
                   expected=["customers, addresses, orders, order_items, payments",
                             "Four joins — five with products for item names",
                             "customer_id, address_id, order_id, product_id",
                             "One document: order, items and shipping address"],
                   minutes=10,
                   takeaway="One page can hide many joins — a document shaped like the page "
                            "needs one read.",
                   notes=[tp("How to run it",
                             "Pairs, five minutes, then compare. Point back to the challenges "
                             "diagram with its five tables."),
                          tp("The joins",
                             "Five tables need four joins. Showing product names adds the "
                             "products table and a fifth join."),
                          tp("The keys",
                             "customer_id links customers to orders and addresses, address_id "
                             "links the order to its address, order_id links items and "
                             "payments, and product_id links items to products."),
                          tp("The document",
                             "In training_store, O6102 is one document. Its items and shipping "
                             "address are embedded, and it holds a customerId reference to "
                             "Luis. The payment is a paymentStatus field. We look at this shape "
                             "in Part 3.")]),

        # Part 2 ------------------------------------------------------------
        F.bridge(PARTS, 1, "Part 2: Four NoSQL Models",
                 "NoSQL is a family. Meet its four members.",
                 so_far=["Data comes structured, semi-structured and unstructured",
                         "Relational tables excel at stable, related data",
                         "NoSQL adds models for flexibility and scale"],
                 question="How do the four NoSQL models store data differently — and what is "
                          "each one best at?",
                 covers=["The four families at a glance", "Document databases",
                         "Key-value databases", "Column-family databases", "Graph databases",
                         "All five models side by side"],
                 notes=[tp("Connecting the parts",
                           "Part 1 explained why NoSQL appeared. Part 2 shows that NoSQL is "
                           "four quite different models."),
                        tp("Watch for",
                           "For each model, notice the access pattern it is fast at. That is "
                           "the skill Exercise 1.1 tests.")]),
        F.diagram(img(8), "The Four Major NoSQL Database Types",
                  "Document, key-value, column-family and graph.",
                  items=[("Document", "Whole records as JSON-like documents — MongoDB, "
                                      "Couchbase."),
                         ("Key-value", "One opaque value per key — Redis, Amazon DynamoDB."),
                         ("Column-family", "Wide rows with variable columns — Apache Cassandra, "
                                           "HBase."),
                         ("Graph", "Nodes and relationships — Neo4j, Amazon Neptune.")],
                  takeaway="Each NoSQL family is optimized for a different way of reading and "
                           "writing data.",
                  notes=dn(8)),
        F.diagram(img(9), "Document Databases",
                  "Store one application object as one self-contained document.",
                  items=[{"code": "{ sku: \"S210\",\n"
                                  "  name: \"Trail Shoe\",\n"
                                  "  category: \"SHOE\",\n"
                                  "  price: Decimal128(\"89.99\"),\n"
                                  "  attributes: {\n"
                                  "    sizes: [8, 9, 10, 11],\n"
                                  "    color: \"Grey\",\n"
                                  "    material: \"Synthetic\" },\n"
                                  "  tags: [\"trail\", \"sports\"] }",
                          "label": "A training_store product (trimmed)", "size": 11},
                         ("Good fit", "Catalogs, customer profiles, content and order "
                                      "management."),
                         {"callout": ("Main advantage",
                                      "One object stays one document — not many tables.")}],
                  takeaway="A document database keeps each business object together, in the "
                           "shape the application uses.",
                  notes=dn(9)),
        F.diagram(img(10), "Key-Value Databases",
                  "The application supplies the exact key; the store returns the value.",
                  items=[("How it works", "GET session:abc returns that session's value — "
                                          "nothing else."),
                         ("Good fit", "Caching, sessions, shopping carts, preferences, "
                                      "counters."),
                         ("Trade-off", "Very fast by key; weak for queries about what's inside "
                                       "the value."),
                         {"chips": ["Redis", "Amazon DynamoDB"], "h": "Examples", "c": RED,
                          "cols": 2}],
                  takeaway="Key-value stores are the fastest path when the application always "
                           "knows the key.",
                  notes=dn(10)),
        F.diagram(img(11), "Column-Family Databases",
                  "Rows found by row key, with related columns grouped into families.",
                  items=[("Row key", "Every lookup starts from the row key, e.g. customerId "
                                     "101."),
                         ("Column families", "Related columns sit together: profile, orders, "
                                             "activity."),
                         ("Sparse rows", "A row stores only the columns it has — gaps cost "
                                         "nothing."),
                         ("Good fit", "Huge write volumes: events, sensors, time series — "
                                      "Cassandra, HBase.")],
                  takeaway="Column-family stores handle huge, distributed write volumes looked "
                           "up by row key.",
                  notes=dn(11)),
        S[12],
        F.compare("Comparing the Data Models",
                  "The four NoSQL families — and relational — side by side.",
                  ["Model", "Data model", "Main strength", "Typical use"],
                  [("Relational", "Tables, fixed schema", "Integrity, joins, transactions",
                    "Ledgers, finance"),
                   ("Document", "JSON-like documents", "Flexible, app-friendly records",
                    "Catalogs, profiles, orders"),
                   ("Key-value", "A key mapped to a value", "Extremely fast lookup",
                    "Caching, sessions, carts"),
                   ("Column-family", "Wide rows by row key", "Huge distributed writes",
                    "Events, time series"),
                   ("Graph", "Nodes and relationships", "Relationship traversal",
                    "Fraud, recommendations")],
                  [1.75, 2.30, 2.40, 2.35], row_h=0.66,
                  items=[("More than one can work", "Many workloads have two workable models — "
                                                    "justify your first choice."),
                         ("Look at the access", "By key? Whole object? Huge writes? Deep "
                                                "relationships?"),
                         {"callout": ("Exercise 1.1", "You'll match six workloads to these "
                                                      "five models.")}],
                  takeaway="Start from how the data is read and written — then pick the model "
                           "built for that access pattern.",
                  notes=[tp("How to read the table",
                            "Each row is one model: how it stores data, what it is best at, "
                            "and where it is typically used."),
                         tp("Relational is on the list",
                            "Exercise 1.1 includes relational as one of five choices, because "
                            "for some workloads it is still the best one."),
                         tp("The questions to ask",
                            "Is the data read by an exact key? As a whole object? Written in "
                            "huge volumes? Or walked along relationships? Each answer points "
                            "to a different row."),
                         tp("No single winner",
                            "More than one model can often work. The justification, based on "
                            "the access pattern, matters more than the product name.")]),

        # Part 3 ------------------------------------------------------------
        F.bridge(PARTS, 2, "Part 3: MongoDB's Data Model",
                 "From the document family in general to MongoDB in particular.",
                 so_far=["Four NoSQL families, each with its strength",
                         "Choose the model from the access pattern",
                         "Document databases keep whole objects together"],
                 question="What exactly is a MongoDB document — and how is the data organized?",
                 covers=["MongoDB at a glance", "Database, collection, document, field",
                         "Relational terms in MongoDB", "BSON types in a document",
                         "From rows to documents", "Embed or reference",
                         "Flexible schema in one collection"],
                 notes=[tp("Why this part",
                           "MongoDB is the document database this course teaches. Now we look "
                           "closely at how it organizes data."),
                        tp("What to watch",
                           "Keep comparing with the relational tables from Part 1. By the end, "
                           "learners should be able to read a training_store document and name "
                           "every part of it.")]),
        F.diagram(img(13), "Introducing MongoDB",
                  "A document database that stores BSON documents in collections.",
                  items=[("Document database", "Data is stored as documents, grouped into "
                                               "collections."),
                         ("BSON", "Binary JSON — adds types JSON lacks: dates, decimals, "
                                  "ObjectIds."),
                         ("training_store", "products, customers, orders and reviews — our four "
                                            "collections."),
                         {"callout": ("Beyond storage",
                                      "Indexes and replica sets are built in.")}],
                  takeaway="MongoDB is a document database: BSON documents, grouped into "
                           "collections, with indexing and replication built in.",
                  notes=dn(13)),
        F.diagram(img(14), "The MongoDB Data Hierarchy",
                  "Deployment → database → collection → document → field.",
                  items=[{"code": "show dbs\n"
                                  "use training_store\n"
                                  "show collections\n"
                                  "db.products.findOne()",
                          "label": "Walk it in mongosh", "size": 12},
                         ("Created on first write", "A database or collection appears the "
                                                    "first time you insert into it."),
                         {"callout": ("Our dataset",
                                      "13 products — e.g. B300, MongoDB Fundamentals.")}],
                  takeaway="Every mongosh command works at one level of the hierarchy: database, "
                           "collection, document or field.",
                  notes=dn(14)),
        F.diagram(img(15), "Relational-to-MongoDB Terminology",
                  "The words map neatly — the designs often don't.",
                  items=[("Row → document", "A document can hold nested objects and arrays a "
                                            "row can't."),
                         ("JOIN → embed / reference", "Embed what is read together; reference "
                                                      "the rest. $lookup joins when needed."),
                         ("Schema → implicit", "Fields come from the documents; add validation "
                                               "rules when needed."),
                         {"callout": ("Not one-to-one",
                                      "Don't copy each table into a collection.")}],
                  takeaway="Table, row and column become collection, document and field — but "
                           "one document often replaces several joined rows.",
                  notes=dn(15)),
        F.diagram(img(16), "Anatomy of a MongoDB Document",
                  "Every field keeps its BSON type.",
                  items=[("_id", "Unique in its collection; an ObjectId is added if you don't "
                                 "supply one."),
                         ("Typed values", "String, Decimal128, Boolean, Date, Array and "
                                          "embedded document."),
                         ("BSON", "Stored as typed binary, shown as JSON-like text in "
                                  "mongosh."),
                         {"callout": ("Money", "Store prices as Decimal128, never as "
                                               "strings.")}],
                  takeaway="BSON keeps real types, so IDs, money and dates behave correctly in "
                           "queries.",
                  notes=dn(16)),
        F.diagram(img(17), "From Rows to Documents",
                  "Three normalized tables become one order document.",
                  items=[("Rows", "customers, orders and order_items — joined on customer_id "
                                  "and order_id."),
                         ("One document", "Order fields, a customer snapshot and an embedded "
                                          "items array."),
                         ("Purchase-time price", "Each item keeps the price paid, even if the "
                                                 "catalog changes."),
                         {"callout": ("Exercise 1.2", "You'll make this conversion "
                                                      "yourself.")}],
                  takeaway="Shape the document like the thing the application shows — here, one "
                           "complete order.",
                  notes=dn(17)),
        F.code("Embed or Reference? How training_store Decides",
               "Real documents from the orders and reviews collections.",
               [{"label": "orders: O6102 (trimmed)", "kind": "good", "code":
                 "{\n"
                 "  orderNumber: \"O6102\",\n"
                 "  customerId: ObjectId(\"…\"),  // reference\n"
                 "  items: [                    // embedded\n"
                 "    { sku: \"S200\", quantity: 1,\n"
                 "      unitPrice: Decimal128(\"129.99\") },\n"
                 "    { sku: \"P1001\", quantity: 1,\n"
                 "      unitPrice: Decimal128(\"49.99\") }\n"
                 "  ],\n"
                 "  shippingAddress: { city: \"Austin\", … },\n"
                 "  total: Decimal128(\"211.38\")\n"
                 "}"},
                {"label": "reviews: their own collection (trimmed)", "kind": "good", "code":
                 "{\n"
                 "  productId: ObjectId(\"…\"),   // reference\n"
                 "  sku: \"S200\",\n"
                 "  customerId: ObjectId(\"…\"),  // reference\n"
                 "  rating: 4,\n"
                 "  title: \"Comfortable\",\n"
                 "  body: \"Good for daily runs.\"\n"
                 "}"}],
               points=[("Embed", "Items and the shipping address are read with the order and "
                                 "keep purchase-time values."),
                       ("Reference", "Customers are shared and change; reviews grow without "
                                     "limit."),
                       {"callout": ("Rule of thumb", "Store together what the app reads "
                                                     "together.")}],
               takeaway="Embed what is read together and belongs to one object; reference what "
                        "is shared, changes or grows without limit.",
               notes=[tp("Read the order",
                         "Order O6102 embeds its two line items and its shipping address. Each "
                         "item keeps the unit price Luis paid. The customer is not embedded: "
                         "customerId points to Luis Romero's document in customers."),
                      tp("Compare with the last diagram",
                         "The rows-to-documents diagram embedded a customer snapshot. That is "
                         "valid too. training_store chose a reference, because a customer "
                         "changes their email or address independently of past orders."),
                      tp("Read the review",
                         "Reviews live in their own collection and reference both the product "
                         "and the customer. If every review were embedded in its product, a "
                         "popular product's document would grow without limit."),
                      tp("The rule",
                         "Store together what the application reads together. Module 3 turns "
                         "this rule into a full modeling method.")]),
        F.diagram(img(18), "Flexible Schema Within a Collection",
                  "Two products, one collection, different fields.",
                  items=[("Different fields", "The laptop has cpu and ram; the book has isbn "
                                              "and pages."),
                         ("A shared core", "Both keep _id, sku, name, category, price and "
                                           "active."),
                         ("In training_store", "LAPTOP, SHOE, BOOK and ACCESSORY each keep their "
                                               "own attributes."),
                         {"callout": ("Flexible ≠ unplanned",
                                      "Schema validation can require key fields.")}],
                  takeaway="Documents in one collection can differ — design the shared core, and "
                           "validate what must always be there.",
                  notes=dn(18)),
        F.exercise("Exercise: Translate SQL Thinking into MongoDB",
                   "Rewrite a relational description of the store in MongoDB terms.",
                   scenario="A teammate describes training_store in relational terms:",
                   scenario_code="\"The products table has 13 rows.\"\n"
                                 "\"Each row's key is product_id.\"\n"
                                 "\"Order lines live in order_items.\"\n"
                                 "\"We join them to show an order.\"",
                   tasks=["Rewrite each sentence in MongoDB terms",
                          "Name the field that replaces product_id",
                          "Say what replaces the order_items join",
                          "Write the mongosh command that counts products"],
                   expected=["The products collection holds 13 documents",
                             "_id — plus sku as a unique business key",
                             "An items array embedded in each order",
                             "db.products.countDocuments() returns 13"],
                   minutes=10,
                   takeaway="Speaking MongoDB's vocabulary is the first step to thinking in "
                            "documents.",
                   notes=[tp("How to run it",
                             "Individually for five minutes, then compare in pairs. Accept any "
                             "wording that uses collection, document, field and _id correctly."),
                          tp("product_id",
                             "Every product has an _id, an ObjectId in our dataset. The loader "
                             "also creates a unique index on sku, so sku works as the business "
                             "key people use."),
                          tp("The join",
                             "There is no order_items collection. Each order document embeds "
                             "its items array, so showing an order needs no join."),
                          tp("The count",
                             "db.products.countDocuments() returns 13 after the full load. If "
                             "learners don't have mongosh yet, run it on the instructor "
                             "screen.")]),

        # Part 4 ------------------------------------------------------------
        F.bridge(PARTS, 3, "Part 4: Architecture and Fit",
                 "How MongoDB runs — and when to choose it.",
                 so_far=["MongoDB stores BSON documents in collections",
                         "Embed what is read together; reference the rest",
                         "A flexible schema still needs design"],
                 question="How does MongoDB run — and when is it the right choice?",
                 covers=["Clients, mongod and the storage engine", "How a request is processed",
                         "Replica sets and sharded clusters", "Core features in mongosh",
                         "When MongoDB fits — and when it doesn't", "A modernization scenario",
                         "Misconceptions and anti-patterns"],
                 notes=[tp("Why this part",
                           "Knowing the data model isn't enough. We also need to know what runs "
                           "it, how it stays available and how it scales."),
                        tp("Outcome",
                           "By the end, learners should be able to argue for or against MongoDB "
                           "for a given workload.")]),
        F.diagram(img(19), "MongoDB Architecture Overview",
                  "Clients, the mongod server, the storage engine and the data files.",
                  items=[("Clients", "mongosh, MongoDB Compass and application drivers."),
                         ("mongod", "The server process: connections, queries, CRUD, indexes, "
                                    "authentication."),
                         ("Storage engine", "WiredTiger by default: cache, journal, reads and "
                                            "writes."),
                         {"callout": ("Module 2", "You'll install mongod and connect with "
                                                  "mongosh.")}],
                  takeaway="Every client talks to mongod — the server process that owns storage, "
                           "queries and indexes.",
                  notes=dn(19)),
        F.diagram(img(20), "How a MongoDB Request Is Processed",
                  "Follow one find request from the client to the result.",
                  items=[{"code": "db.products.find(\n"
                                  "  { category: \"LAPTOP\" }\n"
                                  ")",
                          "label": "Find products", "size": 12},
                         ("Parse and authorize", "mongod checks the request and the user's "
                                                 "rights."),
                         ("Choose a plan", "Use an index, or scan the whole collection."),
                         ("Return BSON", "Matching documents go back to the client.")],
                  takeaway="The query planner's choice — index or collection scan — decides how "
                           "much work each request does.",
                  notes=dn(20)),
        S[21],
        F.diagram(img(22), "Core MongoDB Features",
                  "Flexible documents, indexes, aggregation, replication, sharding and drivers.",
                  items=[("Rich queries", "Filter, sort, project and update — plus arrays, "
                                          "geospatial and text."),
                         ("Indexes", "Find documents without scanning the whole collection."),
                         ("Aggregation", "Pipelines of stages for reporting and analysis."),
                         ("Rules when needed", "Schema validation, atomic writes and "
                                               "multi-document transactions.")],
                  takeaway="MongoDB is more than flexible storage: it queries, indexes, "
                           "aggregates, replicates and scales.",
                  notes=dn(22)),
        F.code("Queries, Indexes and Aggregation in mongosh",
               "Three commands on training_store — covered in depth on Days 2 and 3.",
               [{"label": "Filter and project", "kind": "info", "code":
                 "db.products.find(\n"
                 "  { category: \"BOOK\" },\n"
                 "  { name: 1, price: 1, _id: 0 }\n"
                 ")"},
                {"label": "Index a common query", "kind": "info", "code":
                 "db.products.createIndex(\n"
                 "  { category: 1, price: 1 }\n"
                 ")"},
                {"label": "Aggregate paid orders", "kind": "info", "code":
                 "db.orders.aggregate([\n"
                 "  { $match: {\n"
                 "      paymentStatus: \"PAID\" } },\n"
                 "  { $group: {\n"
                 "      _id: \"$customerId\",\n"
                 "      spent: { $sum: \"$total\" } } },\n"
                 "  { $sort: { spent: -1 } }\n"
                 "])"}],
               points=[("find", "Returns the two books — name and price only."),
                       ("createIndex", "Supports queries that filter on category and price."),
                       ("aggregate", "Totals paid orders per customer; C101 comes first.")],
               takeaway="One query language filters, indexes and aggregates — all on the same "
                        "documents.",
               notes=[tp("find",
                         "The first argument is the filter, the second the projection. This "
                         "returns MongoDB Fundamentals at 59.99 and Query Cookbook at 39.99, "
                         "showing only name and price. Module 4 covers queries in depth."),
                      tp("createIndex",
                         "A compound index on category and price supports queries that filter "
                         "by category and sort or filter by price. Design indexes around real "
                         "query patterns; Module 6 covers this."),
                      tp("aggregate",
                         "The pipeline keeps the 13 paid orders, groups them by customerId and "
                         "sums the totals, then sorts. Aisha Khan, C101, comes first with "
                         "3418.62. Module 5 covers aggregation."),
                      tp("Field names",
                         "Our orders use paymentStatus, not a generic status field. Using the "
                         "real field names is the habit to build now.")]),
        F.exercise("Exercise: Predict the Query Result",
                   "Read a query and say what mongosh prints — before running it.",
                   scenario="training_store has three shoes: Running Shoe 129.99, Trail Shoe "
                            "89.99 and Clearance Shoe 44.99.",
                   scenario_code="db.products.find(\n"
                                 "  { category: \"SHOE\",\n"
                                 "    price: { $lt: 100 } },\n"
                                 "  { name: 1, price: 1, _id: 0 }\n"
                                 ").sort({ price: 1 })",
                   tasks=["Say which shoes match the filter",
                          "Put them in the order sort() returns",
                          "List the fields each result shows",
                          "Check your answer on the instructor's screen"],
                   expected=["Clearance Shoe (44.99), then Trail Shoe (89.99)",
                             "Running Shoe is excluded: 129.99 is not under 100",
                             "Only name and price — _id is hidden",
                             "Prices print as Decimal128 values"],
                   minutes=5,
                   takeaway="Reading a query before running it is the fastest way to learn the "
                            "query language.",
                   notes=[tp("How to run it",
                             "Give everyone two minutes to write their prediction, then run the "
                             "query on the instructor screen."),
                          tp("The filter",
                             "category must equal SHOE and price must be less than 100. Only "
                             "the Trail Shoe and the Clearance Shoe qualify."),
                          tp("Sort and projection",
                             "sort({ price: 1 }) is ascending, so Clearance Shoe comes first. "
                             "The projection shows name and price and hides _id."),
                          tp("Decimal128",
                             "Prices are stored as Decimal128, so mongosh prints them as "
                             "Decimal128('44.99'). MongoDB still compares them with the number "
                             "100 correctly.")]),
        F.diagram(img(23), "When to Use MongoDB",
                  "Five signals that point to a document database.",
                  items=[("Varied attributes", "Products with category-specific "
                                               "specifications."),
                         ("Accessed together", "An order and its line items, read in one "
                                               "call."),
                         ("Evolving schema", "New catalog fields without a migration."),
                         ("Horizontal growth", "Shard a fast-growing orders collection.")],
                  takeaway="The more of these signals a workload shows, the better MongoDB "
                           "fits.",
                  notes=dn(23)),
        F.diagram(img(24), "When MongoDB May Not Be the Best Choice",
                  "Five workloads where another model may fit better.",
                  items=[("Cross-entity transactions", "Supported — but if most work spans many "
                                                       "entities, relational may be simpler."),
                         ("Strict tabular reporting", "Fixed rows and columns suit relational "
                                                      "tools."),
                         ("Graph-first or pure cache", "Deep traversal → graph; session lookup "
                                                       "→ key-value."),
                         {"callout": ("Consider alternatives",
                                      "Check the workload — don't rule MongoDB out.")}],
                  takeaway="Knowing when not to use MongoDB is part of choosing it well.",
                  notes=dn(24)),
        F.diagram(img(25), "Scenario: Modernizing a Product Catalog",
                  "Reshape the data, load it, and serve the same API.",
                  items=[("Before", "products, categories, attributes and inventory tables — "
                                    "many joins."),
                         ("Reshape and load", "One product document: sku, name, price, tags, "
                                              "specifications."),
                         ("Same API", "GET /catalog/products keeps its contract; one read per "
                                      "product."),
                         {"callout": ("Model first", "Reshape around reads — don't copy "
                                                     "tables.")}],
                  takeaway="Modernizing starts by reshaping the data around how it is read — "
                           "not by copying the tables.",
                  notes=dn(25), mode="stack"),
        F.myths("Misconceptions and Anti-Patterns",
                "Beliefs that lead first MongoDB designs into trouble.",
                [("NoSQL means SQL is obsolete",
                  "Not Only SQL — relational still fits many workloads"),
                 ("Schemaless means no design",
                  "A flexible schema still needs a model — and can be validated"),
                 ("MongoDB has no transactions",
                  "Single-document writes are atomic; multi-document transactions exist"),
                 ("Copy each table into a collection",
                  "Model documents around how the app reads and writes"),
                 ("NoSQL is one technology",
                  "Four families with very different strengths")],
                ["One collection per relational table",
                 "Unbounded arrays, e.g. every review inside its product",
                 "Prices stored as strings",
                 "No indexes for common queries",
                 "A $lookup join on every read"],
                remember=("Remember", "Store together what the application reads together."),
                takeaway="Most first-design problems come from treating MongoDB like tables with "
                         "a new syntax.",
                notes=[tp("Why this slide",
                          "Before the checks, clear away the beliefs that cause the most "
                          "trouble in first designs."),
                       tp("NoSQL and schema",
                          "Not Only SQL means more options, not the end of SQL. And a flexible "
                          "schema still needs a deliberate model; schema validation can enforce "
                          "the fields that matter."),
                       tp("Transactions",
                          "Every single-document write is atomic. Multi-document ACID "
                          "transactions are available too, though a good document design needs "
                          "them less often."),
                       tp("Anti-patterns",
                          "Watch for one collection per table, arrays that grow forever, prices "
                          "stored as strings, missing indexes, and joining with $lookup on every "
                          "read. training_store keeps reviews in their own collection for "
                          "exactly this reason.")]),
        F.diagram(img(26), "Module 1 at a Glance",
                  "Why NoSQL, four models, MongoDB documents and architecture — on one page.",
                  takeaway="NoSQL is a family of models; MongoDB stores BSON documents shaped "
                           "around how the application reads them.",
                  notes=dn(26)),

        # Wrap-up ------------------------------------------------------------
        F.knowledge("Knowledge Check", "Answer in your own words — then compare with a partner.",
                    ["What does “Not Only SQL” communicate?",
                     "Name the four NoSQL model families.",
                     "Which model fits highly connected data?",
                     "What is MongoDB's equivalent of a table? Of a row?",
                     "Which field uniquely identifies a document?",
                     "What is BSON, and why not plain JSON?",
                     "Why might a product catalog fit a document database?",
                     "Does a flexible schema mean no schema design?",
                     "What do replica sets and sharding each provide?",
                     "Name one workload where MongoDB may not fit best."],
                    notes=[tp("1. Not Only SQL",
                              "NoSQL is a family of non-relational models that sits beside "
                              "SQL. It doesn't replace it."),
                           tp("2. Four families",
                              "Document, key-value, column-family and graph."),
                           tp("3. Connected data",
                              "A graph database, where relationships are first-class data."),
                           tp("4. Table and row",
                              "A table maps to a collection, and a row maps to a document."),
                           tp("5. Unique field",
                              "_id. It is unique within its collection, and an ObjectId by "
                              "default."),
                           tp("6. BSON",
                              "Binary JSON. It stores real types such as Date, Decimal128 and "
                              "ObjectId, which plain JSON can't represent."),
                           tp("7. Product catalog",
                              "Products have different attributes per category, and one product "
                              "is read as one object."),
                           tp("8. Flexible schema",
                              "No. You still design the document shape, and you can enforce "
                              "rules with schema validation."),
                           tp("9. Replica sets and sharding",
                              "Replica sets give redundancy and automatic failover. Sharding "
                              "spreads data across servers for horizontal scale."),
                           tp("10. Not the best fit",
                              "Examples: heavy cross-entity transactions, strict tabular "
                              "reporting, graph-first traversal, or a pure key-value cache.")]),
        F.exercise("Exercise 1.1 — Choose the Appropriate Data Model",
                   "Module 1 checkpoint A: match workloads to models, and justify each one.",
                   kind="OFFICIAL CHECKPOINT A", minutes=15,
                   worksheet="labs/day-01/exercises/exercise-1.1-choose-the-data-model.md",
                   scenario="Pick one starting model for each workload: relational, document, "
                            "key-value, column-family or graph.",
                   scenario_code="A  Online shopping sessions\n"
                                 "B  Product catalog\n"
                                 "C  Social recommendations\n"
                                 "D  Banking ledger\n"
                                 "E  Sensor platform\n"
                                 "F  Content management",
                   tasks=["Name each model's primary structure",
                          "Classify A–C with a one-line reason",
                          "Classify D–F the same way",
                          "Defend one controversial row to the class"],
                   expected=["A key-value · B document", "C graph · D relational",
                             "E column-family or time-series", "F document",
                             "Every reason names an access pattern"],
                   expected_title="Solution (after debrief)",
                   takeaway="More than one technology may work — start from the access pattern, "
                            "not popularity.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 1.1 for Module 1. The worksheet is "
                             "labs/day-01/exercises/exercise-1.1-choose-the-data-model.md. "
                             "No MongoDB is needed."),
                          tp("Running it",
                             "Twelve minutes of pair work, then a three-minute debrief. Reveal "
                             "the solution column only after groups share their answers."),
                          tp("The requirements",
                             "A: retrieve a session by a unique session ID. B: products with "
                             "different attributes. C: traverse relationships between users. "
                             "D: strongly structured financial transactions. E: large volumes "
                             "of distributed time-series writes. F: articles with nested and "
                             "optional sections."),
                          tp("What to listen for",
                             "Each justification should name the access pattern: lookup by "
                             "key, varied attributes, relationship traversal, strict "
                             "consistency, or write volume. Product names alone don't count.")]),
        F.exercise("Exercise 1.2 — Convert Relational Rows into a Document",
                   "Module 1 checkpoint B: one order, one document.",
                   kind="OFFICIAL CHECKPOINT B", minutes=20,
                   worksheet="labs/day-01/exercises/exercise-1.2-rows-to-documents.md",
                   scenario="Order O5001 lives in three tables. Make it one document the "
                            "application can read without joins.",
                   scenario_code="Customer  C101  Aisha Khan\n"
                                 "          aisha@example.com\n"
                                 "Order     O5001  PLACED  110.00\n"
                                 "Items     P10  Keyboard  2 × 25.00\n"
                                 "          P22  Mouse     1 × 60.00",
                   tasks=["Name the three tables and their join keys",
                          "Draft the order header: status and total",
                          "Embed the items and the customer; set _id",
                          "Decide what is a snapshot and what can go stale"],
                   expected=["One document with _id: \"O5001\"",
                             "A nested customer and an items array",
                             "Purchase-time price is a snapshot",
                             "An embedded email can go stale",
                             "Shaped for: get O5001 in one read"],
                   takeaway="Some duplication is intentional when it serves the access pattern "
                            "and preserves history.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 1.2. The worksheet is "
                             "labs/day-01/exercises/exercise-1.2-rows-to-documents.md. "
                             "Learners write the document in a scratch file; MongoDB is "
                             "optional."),
                          tp("The expected document",
                             "_id is O5001. customer holds customerId C101, name Aisha Khan and "
                             "her email. items is an array of two lines: P10 Keyboard, quantity "
                             "2 at 25.00, and P22 Mouse, quantity 1 at 60.00. status is PLACED "
                             "and total is 110.00."),
                          tp("Snapshot versus stale",
                             "The purchase-time price is a deliberate snapshot. An embedded "
                             "email can go stale if Aisha changes it later. The document is "
                             "shaped for one query: get order O5001 in one read."),
                          tp("A note on the dataset",
                             "The worksheet's O5001 is its own small example. The O5001 in the "
                             "loaded training_store is different: a Business Laptop and two "
                             "Wireless Mice, payment pending, with a customerId reference "
                             "instead of an embedded customer. Learners will see it in Exercise "
                             "1.3.")]),
        F.exercise("Exercise 1.3 — Explore a MongoDB Dataset",
                   "Module 1 checkpoint C: navigate training_store and read real documents.",
                   kind="OFFICIAL CHECKPOINT C", minutes=25,
                   worksheet="labs/day-01/exercises/exercise-1.3-explore-a-mongodb-dataset.md",
                   scenario="The instructor has loaded training_store. No mongosh yet? Follow "
                            "on screen.",
                   scenario_code="show dbs\n"
                                 "use training_store\n"
                                 "show collections\n"
                                 "db.products.findOne()\n"
                                 "db.orders.findOne()\n"
                                 "db.products.find().limit(2)\n"
                                 "// a laptop and a book:\n"
                                 "db.products.find(\n"
                                 "  { sku: { $in: [\"L100\", \"B300\"] } })",
                   tasks=["List the databases and collections",
                          "Read one product and one order",
                          "Label _id, scalars, objects, arrays, dates, numbers, Booleans",
                          "Compare two products' fields",
                          "Answer the observation sheet"],
                   expected=["customers, orders, products, reviews",
                             "_id: the unique document identifier",
                             "Order: shippingAddress object, items array",
                             "Products differ by category attributes",
                             "One row-versus-document difference"],
                   takeaway="A document looks like an application object: nested fields, "
                            "arrays and real types in one record.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 1.3. The worksheet is "
                             "labs/day-01/exercises/exercise-1.3-explore-a-mongodb-dataset.md. "
                             "The instructor loads training_store before class; if mongosh isn't "
                             "installed yet, learners follow on the instructor screen."),
                          tp("What they will see",
                             "show dbs lists training_store beside admin, config and local. "
                             "show collections lists customers, orders, products and reviews. "
                             "db.orders.findOne() prints O5001, with a shippingAddress object "
                             "and an items array; the customer is a customerId reference."),
                          tp("Comparing products",
                             "On a fresh load, find().limit(2) usually returns the two "
                             "laptops, L100 and L110, which share the same fields. Use the last "
                             "command on the slide to compare a laptop, with processor and "
                             "memoryGB, against a book, with author and isbn."),
                          tp("Observation sheet",
                             "Six questions: which databases and collections exist, the "
                             "purpose of _id, which document had an embedded object, which had "
                             "an array, which fields differed, and how a document resembles an "
                             "application object.")]),
        F.wrapup("Module 1 Summary and What's Next",
                 "From why NoSQL exists to reading real MongoDB documents.",
                 can=["Explain what NoSQL means and why it emerged",
                      "Compare document, key-value, column-family and graph models",
                      "Describe databases, collections, documents and BSON",
                      "Explain mongod, replica sets and sharding",
                      "Judge when MongoDB fits — and when it doesn't",
                      "Read training_store documents in mongosh"],
                 next_title="Next: Module 2 — Installation and Setup",
                 questions=["Local MongoDB or MongoDB Atlas?",
                            "How do I install and start mongod and mongosh?",
                            "How do I connect and load training_store?"],
                 bring=("Bring along", "Your Exercise 1.1 table, your O5001 document and your "
                                       "Exercise 1.3 observation sheet."),
                 takeaway="Module 2 gives you your own running MongoDB, so every later module "
                          "can use training_store hands-on.",
                 notes=[tp("Recap",
                           "We moved from the kinds of data applications store, to the four "
                           "NoSQL models, to MongoDB's documents and BSON types, to how MongoDB "
                           "runs and when it fits."),
                        tp("Next module",
                           "Module 2 answers the setup questions: local MongoDB or Atlas, how "
                           "to install and start mongod and mongosh, and how to connect and load "
                           "training_store."),
                        tp("Bring along",
                           "Keep the Exercise 1.1 table, the O5001 document from Exercise 1.2 "
                           "and the Exercise 1.3 observation sheet. Module 3 builds directly on "
                           "them.")]),
    ]
