#!/usr/bin/env python3
"""Slide order for the Module 8 deck: from a functional database to a production-ready one.

Every concept diagram is merged with the slide that explains it (diagram plus the
points only that slide adds), so no idea appears twice. Part openers, mongosh examples
on the training_store sample database, in-flow practice exercises, a knowledge check,
three official checkpoints (Exercises 8.1-8.3, labs/day-03/exercises/), Lab 7
(labs/day-03/lab7/LAB-7-GUIDE.md) and a course wrap-up connect the ideas. Module 8 is the last module, so the deck closes the course.

Dataset notes. The content guide's generic examples use fields training_store doesn't
have (status, orderedAt, lineTotal, stock, category "Electronics"). Every command here
uses the real fields: paymentStatus (PAID / PENDING / FAILED), fulfillmentStatus
(NEW / PROCESSING / SHIPPED / DELIVERED), createdAt, items[].unitPrice and the four
categories LAPTOP, SHOE, BOOK and ACCESSORY. The speaker notes say where a diagram uses
a generic name.
"""
from __future__ import annotations

import mdb_diagram_slides as DS
import mdb_flow_slides as F
import mdb_glossary as G
import mdb_visuals as V
from mdb_flow_slides import tp
from mdb_visuals import (
    CARD_BG, CARD_LINE, DARK_GRAY, GREEN, INK, LEFT, NAVY, ORANGE, PURPLE, RED, RIGHT,
    TEAL, WIDTH,
)
from pptx.enum.text import MSO_ANCHOR

PARTS = ["Part 1\nData model", "Part 2\nPerformance", "Part 3\nSecurity",
         "Part 4\nBackup & recovery", "Part 5\nOperate & diagnose"]


# ---------------------------------------------------------------------------
# Custom slides
# ---------------------------------------------------------------------------
def _checklist(slide, y0, y1):
    areas = [
        ("Data model", NAVY, ["Arrays bounded; snapshots intentional",
                              "One name and one BSON type per field",
                              "Validator plus a migration plan"]),
        ("Queries and aggregation", PURPLE, ["Filtered, projected, limited",
                                             "$match first; no $unwind double count",
                                             "Results checked against a control"]),
        ("Indexes", TEAL, ["Each index serves a named shape",
                           "ESR order confirmed with explain",
                           "Redundant keys hidden, then dropped"]),
        ("Security", RED, ["Authentication on; least privilege",
                           "TLS; private network; no public 27017",
                           "Secrets in a manager, not in code"]),
        ("Availability and recovery", GREEN, ["Replica set; failover tested",
                                              "Backups separate from replication",
                                              "Restore tested against RPO and RTO"]),
        ("Operations", ORANGE, ["Metrics, slow queries, alerts",
                                "Runbooks with owners",
                                "Changes reviewed with explain"]),
    ]
    cols, gx, gy = 3, 0.25, 0.22
    cw = (WIDTH - gx * (cols - 1)) / cols
    ch = (y1 - y0 - gy) / 2
    for k, (title, fill, checks) in enumerate(areas):
        r, c = divmod(k, cols)
        x, y = LEFT + c * (cw + gx), y0 + r * (ch + gy)
        body = V.card(slide, x, y, cw, ch, title, head_fill=fill, title_size=14)
        rh = (y + ch - body - 0.10) / len(checks)
        for j, row in enumerate(checks):
            ry = body + j * rh
            V.badge(slide, x + 0.15, ry + (rh - 0.30) / 2, 0.30, "✓", fill=fill, size=11)
            V.text(slide, x + 0.55, ry, cw - 0.68, rh, row, size=13,
                   anchor=MSO_ANCHOR.MIDDLE)


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
        *G.intro("module08"),
        F.story("From Module 7 to Module 8",
                "The cluster stays up and scales — now make it safe to run for real.",
                gave_title="Module 7 gave us",
                gave=["Replica sets: primary and secondaries",
                      "Elections and automatic failover",
                      "Read and write concerns",
                      "Shard keys, chunks and mongos",
                      "Targeted versus scatter-gather"],
                now=("Now", "Put the practices around it: model, tune, secure, back up, "
                            "monitor and diagnose."),
                path_title="Our path through Module 8",
                path=[("Model and validate documents", "Part 1", NAVY),
                      ("Query, pipeline and index habits", "Part 2", PURPLE),
                      ("Authentication, roles, TLS, network", "Part 3", RED),
                      ("Backups, RPO, RTO and restore tests", "Part 4", GREEN),
                      ("Metrics and troubleshooting by layer", "Part 5", ORANGE),
                      ("Production-readiness review", "Part 5", ORANGE)],
                takeaway="Module 7 kept training_store available; Module 8 makes it "
                         "correct, secure and recoverable.",
                notes=[tp("Bridge from Module 7",
                          "Module 7 gave us a replica set for availability and sharding for "
                          "scale. Both are necessary for production, but neither makes the "
                          "data correct, secure or recoverable on its own."),
                       tp("The path",
                          "We review the data model, measure performance, lock down access, "
                          "prove we can recover, and learn a method for diagnosing problems. "
                          "The module ends with a readiness review of training_store."),
                       tp("The last module",
                          "This is the final module of the course. The closing slides look "
                          "back over all eight modules.")]),
        F.diagram(img(3), "From Functional to Production-Ready",
                  "What changes between “it works” and “we can run it”.",
                  items=[("Functional", "One mongod, no security — where our class instance "
                                        "is today."),
                         ("Hardened", "Auth + TLS, indexes, validation and backups."),
                         ("Production-ready", "A replica set with monitoring, alerts and "
                                              "automated backup."),
                         {"callout": ("Same data", "The four collections never change — the "
                                                   "controls do.")}],
                  takeaway="Production-ready is the same data with proven controls around "
                           "it.",
                  notes=dn(3)),

        # Part 1 ------------------------------------------------------------
        F.bridge(PARTS, 0, "Part 1: Data-Modeling Guidelines",
                 "Flexible schema, governed by explicit rules.",
                 so_far=["You modeled training_store in Module 3",
                         "You queried, aggregated and indexed it",
                         "You replicated and sharded it"],
                 question="Will this document model still hold up as data, features and "
                          "teams grow?",
                 covers=["Embed or reference: document boundaries",
                         "Consistent field names and BSON types",
                         "Historical snapshots",
                         "Schema validation",
                         "Planning schema evolution"],
                 notes=[tp("Why start with the model",
                           "Most performance and correctness problems start in the document "
                           "design. An index can't fix an unbounded array."),
                        tp("What this part does",
                           "We review training_store's model against six rules and find the "
                           "real defects the loader left in it on purpose.")]),
        F.diagram(img(7), "Choose Document Boundaries Carefully",
                  "Embed bounded, owned data — reference shared or unbounded data.",
                  items=[("Embed", "Order items and the shipping address: read with the "
                                   "order, bounded, owned."),
                         ("Reference", "Customers are shared; reviews grow without limit."),
                         {"callout": ("Anti-pattern", "Every review inside its product — "
                                                      "an unbounded array.")}],
                  takeaway="Embed what belongs to one parent and stays bounded; reference "
                           "the rest.",
                  notes=dn(7)),
        F.diagram(img(10), "Use Consistent Field Names and Types",
                  "One name and one BSON type per concept.",
                  items=[("Names", "camelCase, one spelling: productId — never product_id or "
                                   "prodId."),
                         ("Types", "Decimal128 for money, Date for time, ObjectId for "
                                   "references."),
                         {"callout": ("In our data", "XBAD stores price as the string "
                                                     "\"49.99\".")}],
                  takeaway="A field with two spellings or two types quietly breaks queries, "
                           "sorts and indexes.",
                  notes=dn(10)),
        F.code("Find the Drift in training_store",
               "Three queries that expose type and naming problems.",
               [{"label": "Prices stored with the wrong type", "kind": "info", "code":
                 "db.products.find(\n"
                 "  { price: { $type: \"string\" } },\n"
                 "  { _id: 0, sku: 1, price: 1 }\n"
                 ")\n"
                 "// { sku: 'XBAD', price: '49.99' }\n"
                 "\n"
                 "db.products.countDocuments(\n"
                 "  { price: { $type: \"decimal\" } })\n"
                 "// 12"},
                {"label": "Fields outside the model", "kind": "info", "code":
                 "db.products.find(\n"
                 "  { $or: [\n"
                 "    { legacyName: { $exists: true } },\n"
                 "    { temporaryNote: { $exists: true } }\n"
                 "  ] },\n"
                 "  { _id: 0, sku: 1 }\n"
                 ")\n"
                 "// { sku: 'L190' }, { sku: 'A410' }"}],
               points=[("$type", "Finds values whose BSON type differs from the rule."),
                       ("$exists", "Finds stray fields left by old code or manual edits."),
                       {"callout": ("Fix plan", "Migrate XBAD to Decimal128, then "
                                                "validate.")}],
               takeaway="Measure the drift before you fix it — $type and $exists turn a "
                        "hunch into a list.",
               notes=[tp("Wrong type",
                         "Twelve products store price as Decimal128. XBAD, the Legacy Cable "
                         "Pack, stores the string '49.99'. A query such as price less than "
                         "50 never matches it, and a price sort puts it after every number, "
                         "because BSON sorts numbers before strings."),
                      tp("Stray fields",
                         "L190, the Refurbished Laptop, has a legacyName. A410, the Wireless "
                         "Mouse, has a temporaryNote that says remove after review. Neither "
                         "field belongs to the product model."),
                      tp("The fix",
                         "Lab 7 counts XBAD's string price as not-ready evidence. Convert the "
                         "value with $toDecimal in a small, verified update, add a validator "
                         "so it "
                         "can't happen again, and remove the stray fields once nothing reads "
                         "them."),
                      tp("Don't change the shared class data",
                         "Other modules' labs rely on these defects, so demonstrate the fix "
                         "on training_store_ops or reload with load.js afterwards.")]),
        F.diagram(img(13), "Preserve Historical Snapshots",
                  "The order keeps what the customer actually paid.",
                  items=[("Copy at purchase", "The name and price are copied into the "
                                              "order."),
                         ("Later update", "The product's price changes; the order doesn't."),
                         ("In training_store", "Each item keeps sku, name, quantity and "
                                               "unitPrice."),
                         {"callout": ("Intentional", "Snapshot duplication records history "
                                                     "— it isn't a bug.")}],
                  takeaway="Copy the values that must stay historically true into the order "
                           "at the moment it is placed.",
                  notes=dn(13)),
        F.diagram(img(11), "Apply Schema Validation",
                  "The flexible model can still refuse bad data.",
                  items=[("Required", "Fields that must exist, e.g. orderNumber and "
                                      "total."),
                         ("Types and enums", "total must be decimal; paymentStatus one of "
                                             "three values."),
                         ("Rejected", "An invalid write fails with code 121, Document "
                                      "failed validation."),
                         {"callout": ("Not a replacement", "Keep validating in the "
                                                           "application too.")}],
                  takeaway="Schema validation turns the rules the model depends on into rules "
                           "the database enforces.",
                  notes=dn(11)),
        F.code("A Validator on a Scratch Collection",
               "Lab 7, Step 3 — training_store_ops, so the class orders stay untouched.",
               [{"label": "Create the collection with $jsonSchema", "kind": "good", "code":
                 "use training_store_ops\n"
                 "db.createCollection(\"orders_validated\", {\n"
                 "  validator: { $jsonSchema: {\n"
                 "    bsonType: \"object\",\n"
                 "    required: [\"orderNumber\", \"total\",\n"
                 "               \"paymentStatus\"],\n"
                 "    properties: {\n"
                 "      orderNumber: { bsonType: \"string\" },\n"
                 "      total: { bsonType: \"decimal\" },\n"
                 "      paymentStatus: {\n"
                 "        enum: [\"PAID\", \"PENDING\", \"FAILED\"] }\n"
                 "    } } },\n"
                 "  validationAction: \"error\"\n"
                 "})"},
                {"label": "Prove accept and reject", "kind": "info", "code":
                 "db.orders_validated.insertOne({\n"
                 "  orderNumber: \"OPS-1\",\n"
                 "  total: Decimal128(\"10.00\"),\n"
                 "  paymentStatus: \"PAID\" })\n"
                 "// acknowledged: true\n"
                 "\n"
                 "db.orders_validated.insertOne({\n"
                 "  orderNumber: \"OPS-BAD\",\n"
                 "  total: \"10.00\",\n"
                 "  paymentStatus: \"PAID\" })\n"
                 "// MongoServerError:\n"
                 "//   Document failed validation"}],
               takeaway="Test a validator with one good document and one bad one before you "
                        "trust it.",
               notes=[tp("Why a scratch database",
                         "Lab 7, Step 3 builds the validator on "
                         "training_store_ops.orders_validated. The class orders collection "
                         "stays loadable for everyone else."),
                      tp("The rule",
                         "Three fields are required. orderNumber must be a string, total "
                         "must be a Decimal128, and paymentStatus must be PAID, PENDING or "
                         "FAILED — the three values training_store really uses."),
                      tp("The two inserts",
                         "OPS-1 is accepted. OPS-BAD is rejected because total is the "
                         "string '10.00'. The error is code 121, and mongosh shows which "
                         "rule failed in the details."),
                      tp("Decimal128 or NumberDecimal",
                         "The lab guide writes NumberDecimal. In mongosh it is the same "
                         "constructor as Decimal128, which this deck uses everywhere."),
                      tp("Going further",
                         "A fuller validator adds customerId as objectId, items as an array "
                         "with at least one element, fulfillmentStatus as an enum and "
                         "createdAt as a date.")]),
        F.diagram(img(12), "Plan for Schema Evolution",
                  "Change the shape in compatible steps.",
                  items=[{"checks": ["Support both shapes in the app",
                                     "Start writing the new shape",
                                     "Migrate old documents in batches",
                                     "Measure progress and failures",
                                     "Tighten validation, remove old code"],
                          "h": "Migration order", "c": TEAL},
                         {"callout": ("Avoid", "One huge untested updateMany on "
                                               "production.")}],
                  takeaway="Evolve the schema in backward-compatible steps and tighten the "
                           "validator last.",
                  notes=dn(12)),
        F.exercise("Exercise: Predict the Validator's Verdict",
                   "Accepted or rejected? Decide before you run each insert.",
                   scenario="orders_validated requires orderNumber (string), total "
                            "(decimal) and paymentStatus (PAID, PENDING or FAILED).",
                   scenario_code="A {orderNumber:\"OPS-2\",\n"
                                 "   total:Decimal128(\"24.99\"),\n"
                                 "   paymentStatus:\"PENDING\"}\n"
                                 "B {orderNumber:\"OPS-3\",\n"
                                 "   total:Decimal128(\"5.00\"),\n"
                                 "   paymentStatus:\"PAID_NOW\"}\n"
                                 "C {total:Decimal128(\"5.00\"),\n"
                                 "   paymentStatus:\"PAID\"}\n"
                                 "D {orderNumber:\"OPS-4\",\n"
                                 "   total:9.99, paymentStatus:\"PAID\"}",
                   tasks=["Mark each insert accepted or rejected",
                          "Name the rule each rejection breaks",
                          "Say whether an extra field such as note is allowed",
                          "Run them on training_store_ops to check"],
                   expected=["A accepted", "B rejected: enum", "C rejected: required",
                             "D rejected: 9.99 is a double",
                             "Extra fields pass — no additionalProperties rule"],
                   minutes=10,
                   takeaway="A validator enforces only the rules you wrote — know exactly "
                            "which ones those are.",
                   notes=[tp("How to run it",
                             "Pairs, five minutes to predict, then run the four inserts on "
                             "the scratch collection from the previous slide."),
                          tp("A and B",
                             "A satisfies all three rules. B fails the enum: PAID_NOW is "
                             "not one of the allowed values."),
                          tp("C and D",
                             "C has no orderNumber, so it fails required. D fails the type "
                             "rule: the literal 9.99 is a double, not a Decimal128, even "
                             "though it looks like money."),
                          tp("Extra fields",
                             "The validator lists properties but doesn't set "
                             "additionalProperties to false, so a document with an extra "
                             "note field is accepted. That is usually what you want while a "
                             "schema evolves.")]),

        # Part 2 ------------------------------------------------------------
        F.bridge(PARTS, 1, "Part 2: Performance Habits",
                 "Observe → measure → diagnose → change → measure again.",
                 so_far=["Documents are bounded and consistently typed",
                         "Snapshots are intentional",
                         "Validation protects the essentials"],
                 question="How do we prove a query or a report is fast — and still correct?",
                 covers=["Filter, project, sort and limit",
                         "Reduce pipeline input early",
                         "Validate aggregation results",
                         "ESR compound indexes",
                         "Reading explain plans"],
                 notes=[tp("Evidence first",
                           "Performance work follows evidence. Don't start by creating many "
                           "speculative indexes."),
                        tp("Small data, real lessons",
                           "On 17 orders every query is fast. We watch the plan shape and "
                           "the examined counts, which are what change at production "
                           "volume.")]),
        F.code("Ask Only for What the Page Needs",
               "A catalog page: filter, project, sort and limit.",
               [{"label": "Anti-pattern: return everything", "kind": "bad", "code":
                 "db.products.find({})\n"
                 "// all 13 products, every field,\n"
                 "// including attributes"},
                {"label": "Better: one bounded, shaped query", "kind": "good", "code":
                 "db.products.find(\n"
                 "  { category: \"LAPTOP\", active: true },\n"
                 "  { _id: 0, sku: 1, name: 1, price: 1 }\n"
                 ").sort({ price: 1 }).limit(20)\n"
                 "// L100 Business Laptop  1299.99\n"
                 "// L110 Ultrabook        1899.99"}],
               points=[("Filter", "Selective predicates; L190 is inactive and drops out."),
                       ("Project", "Return three fields, not attributes."),
                       ("Limit", "Bound every user-facing list; paginate by range.")],
               takeaway="Every user-facing query should be filtered, projected, sorted and "
                        "limited.",
               notes=[tp("The anti-pattern",
                         "find with an empty filter returns every product with every field. "
                         "On 13 documents it is harmless. On a real catalog it moves "
                         "megabytes over the network for one page."),
                      tp("The better query",
                         "This is Lab 7, Step 1. Only active laptops match: the Business "
                         "Laptop at 1299.99 and the Ultrabook at 1899.99. The Refurbished "
                         "Laptop, L190, is inactive. Prices print as Decimal128 values."),
                      tp("Candidate index",
                         "Equality on category and active, then the price sort: category 1, "
                         "active 1, price 1. Lab 7 asks learners to propose it without "
                         "dropping existing indexes."),
                      tp("Pagination",
                         "For deep pages, prefer range pagination — the next page starts "
                         "after the last price and _id seen — over large skip values, which "
                         "still read every skipped document.")]),
        F.diagram(img(21), "Reduce Pipeline Input Early",
                  "$match and $project before the expensive stages.",
                  items=[("$match first", "Keep only paid orders; an early $match can use "
                                          "an index."),
                         ("$project early", "Carry only the fields later stages need."),
                         ("In training_store", "The field is paymentStatus: 13 of 17 orders "
                                               "are PAID."),
                         {"callout": ("Scale", "The diagram's 10,000 orders are "
                                               "illustrative.")}],
                  takeaway="Filter and trim at the start of the pipeline, so every later "
                           "stage has less to do.",
                  notes=dn(21)),
        F.code("Monthly Paid Revenue — Built Safely",
               "Lab 7, Step 2: group whole orders, not unwound items.",
               [{"label": "Pipeline", "kind": "good", "code":
                 "db.orders.aggregate([\n"
                 "  { $match: { paymentStatus: \"PAID\" } },\n"
                 "  { $group: {\n"
                 "      _id: { $dateToString: {\n"
                 "        format: \"%Y-%m\",\n"
                 "        date: \"$createdAt\" } },\n"
                 "      orderCount: { $sum: 1 },\n"
                 "      revenue: { $sum: \"$total\" } } },\n"
                 "  { $sort: { _id: 1 } }\n"
                 "])"},
                {"label": "Result", "kind": "info", "code":
                 "{ _id: '2026-07', orderCount: 3,\n"
                 "  revenue: Decimal128('1835.95') }\n"
                 "{ _id: '2026-08', orderCount: 4,\n"
                 "  revenue: Decimal128('2731.92') }\n"
                 "{ _id: '2026-09', orderCount: 6,\n"
                 "  revenue: Decimal128('4550.57') }"}],
               points=[("$match first", "Only the 13 paid orders enter the pipeline."),
                       ("Group whole orders", "total is summed once per order."),
                       ("Months in UTC", "$dateToString uses UTC unless you pass a "
                                         "timezone.")],
               takeaway="Put $match first and sum order-level fields before any $unwind.",
               notes=[tp("The pipeline",
                         "$match keeps the 13 paid orders. $group turns createdAt into a "
                         "year-month string and counts and sums per month. $sort puts the "
                         "months in order."),
                      tp("The result",
                         "July has 3 orders for 1835.95, August 4 for 2731.92 and September "
                         "6 for 4550.57. Together that is 13 orders and 9118.44."),
                      tp("Why not the guide's version",
                         "The content guide filters on status and orderedAt and sums "
                         "items.lineTotal. training_store has none of those fields; it has "
                         "paymentStatus, createdAt and items with quantity and unitPrice. "
                         "Line revenue would be quantity times unitPrice with $multiply."),
                      tp("Time zones",
                         "Month boundaries are in UTC. If the business reports in Toronto "
                         "time, pass a timezone to $dateToString, or orders near midnight "
                         "move month.")]),
        F.diagram(img(24), "Validate Aggregation Calculations",
                  "A fast report can still be wrong.",
                  items=[("Control total", "countDocuments({ paymentStatus: \"PAID\" }) → 13 "
                                           "orders."),
                         ("The $unwind trap", "Unwind items, then sum $total: 13 orders "
                                              "become 21 rows."),
                         ("Our numbers", "True revenue 9118.44 — the unwound sum says "
                                         "12119.25."),
                         {"callout": ("Rule", "Check every report against an independent "
                                              "control.")}],
                  takeaway="Verify a pipeline's totals against an independent control "
                           "before anyone trusts the report.",
                  notes=dn(24)),
        F.diagram(img(25), "Indexing Best Practices",
                  "Equality, then Sort, then Range — built from the real query shape.",
                  items=[{"code": "db.orders.createIndex({\n"
                                  "  customerId: 1,\n"
                                  "  paymentStatus: 1,\n"
                                  "  createdAt: -1 })",
                          "label": "The same shape in training_store", "size": 12},
                         ("ESR", "Equality fields first, the sort next, range fields last."),
                         ("Each index costs", "Disk, cache and extra work on every "
                                              "write."),
                         {"callout": ("Before dropping", "Hide the index, monitor, then "
                                                         "drop.")}],
                  takeaway="Build each compound index from a real query shape, in ESR "
                           "order, and know what it costs.",
                  notes=dn(25)),
        F.diagram(img(29), "Review Explain Plans",
                  "explain(\"executionStats\") is the evidence behind every index.",
                  items=[{"code": "db.orders.find({\n"
                                  "  customerId: c101,\n"
                                  "  paymentStatus: \"PAID\" })\n"
                                  ".sort({ createdAt: -1 })\n"
                                  ".explain(\"executionStats\")",
                          "label": "C101's paid history", "size": 12},
                         ("No index", "COLLSCAN: 17 documents examined, 4 returned, plus a "
                                      "SORT."),
                         ("ESR index", "IXSCAN: 4 keys, 4 documents, no SORT stage.")],
                  takeaway="Compare examined with returned — a large gap means a missing or "
                           "unsuitable index.",
                  notes=dn(29, [tp("Getting c101",
                                   "const c101 = db.customers.findOne({ customerNumber: "
                                   "\"C101\" })._id. customerId is an ObjectId in "
                                   "training_store, not the string C101.")])),
        F.exercise("Exercise: Design the Index for Each Shape",
                   "Three real training_store queries — one compound index each.",
                   scenario="Write the index for each shape, label each key E, S or R, then "
                            "confirm with explain.",
                   scenario_code="1 Catalog: category \"LAPTOP\",\n"
                                 "  active true, sort price asc\n"
                                 "2 History: customerId = c101,\n"
                                 "  sort createdAt desc\n"
                                 "3 Report: paymentStatus \"PAID\",\n"
                                 "  createdAt in September",
                   tasks=["Write an index for each shape",
                          "Label every key E, S or R",
                          "Check the plan with explain()",
                          "Name the extra cost of each index"],
                   expected=["1 { category, active, price }",
                             "2 { customerId: 1, createdAt: -1 }",
                             "3 { paymentStatus, createdAt }",
                             "IXSCAN and no SORT stage",
                             "Each slows inserts and updates"],
                   minutes=15,
                   takeaway="An index is designed for a query shape — write the shape down "
                            "first.",
                   notes=[tp("How to run it",
                             "Individually for eight minutes, then compare. Run explain on "
                             "the instructor screen for at least one shape."),
                          tp("Shapes 1 and 2",
                             "Catalog: two equality fields, then the sort — category 1, "
                             "active 1, price 1. History: equality on customerId, then the "
                             "sort on createdAt descending."),
                          tp("Shape 3",
                             "Equality on paymentStatus, then the date range: paymentStatus "
                             "1, createdAt 1. createdAt -1 works equally well, because an "
                             "index range can be scanned in either direction."),
                          tp("Overlap",
                             "If the history index also includes paymentStatus, as in "
                             "Exercise 8.1, the two order indexes overlap. Keep both only if "
                             "both shapes are hot; otherwise hide one and monitor.")]),

        # Part 3 ------------------------------------------------------------
        F.bridge(PARTS, 2, "Part 3: Security",
                 "Authentication, authorization, TLS and network exposure.",
                 so_far=["The model is bounded and validated",
                         "Queries are shaped and indexed",
                         "Results are checked for correctness"],
                 question="Who can reach the database, who are they, and what may they do?",
                 covers=["Security in layers",
                         "Authentication",
                         "Least-privilege roles",
                         "Network exposure and TLS",
                         "Configuration and credentials"],
                 notes=[tp("Why now",
                           "A correct, fast database that anyone can reach is not "
                           "production-ready. This part locks it down."),
                        tp("Safety in class",
                           "Don't enable authentication on the shared class instance. We "
                           "design users and roles, and demonstrate only on a disposable "
                           "environment. Never show a real password on screen.")]),
        F.diagram(img(30), "MongoDB Security Principles",
                  "Every request passes several controls.",
                  items=[("In transit", "TLS from every client and between members."),
                         ("Identity and rights", "Authenticate, authorize with roles, least "
                                                 "privilege."),
                         ("At rest and after", "Encrypted storage; audit logs of security "
                                               "events."),
                         {"callout": ("Defense in depth", "If one layer fails, the others "
                                                          "still hold.")}],
                  takeaway="Layer the controls, so one mistake never exposes everything.",
                  notes=dn(30)),
        F.diagram(img(31), "Authentication",
                  "Who is connecting?",
                  items=[{"code": "# mongod.conf\n"
                                  "security:\n"
                                  "  authorization: enabled",
                          "label": "Turn on access control", "size": 12},
                         ("First user first", "Create an administrator before enforcing "
                                              "it."),
                         ("Identity, not location", "A trusted network is not proof of "
                                                    "identity.")],
                  takeaway="Enable access control, so every connection must prove who it "
                           "is.",
                  notes=dn(31)),
        F.diagram(img(33), "Principle of Least Privilege",
                  "Grant only the access each job requires.",
                  items=[("Application", "readWrite on training_store — never "
                                         "clusterAdmin."),
                         ("Reporting", "read only."),
                         ("Support", "find on reviews, as in the diagram."),
                         ("Operations", "Monitoring, backup and DBA each get their own "
                                        "identity.")],
                  takeaway="Give every identity its own account and only the privileges "
                           "its job needs.",
                  notes=dn(33)),
        F.code("Users and Roles — Sketched, Not Run",
               "Placeholder names, prompted passwords; a disposable instance only.",
               [{"label": "Application and reporting users", "kind": "good", "code":
                 "use training_store\n"
                 "db.createUser({\n"
                 "  user: \"trainingStoreApp\",\n"
                 "  pwd: passwordPrompt(),\n"
                 "  roles: [{ role: \"readWrite\",\n"
                 "            db: \"training_store\" }]\n"
                 "})\n"
                 "db.createUser({\n"
                 "  user: \"reportUser\",\n"
                 "  pwd: passwordPrompt(),\n"
                 "  roles: [{ role: \"read\",\n"
                 "            db: \"training_store\" }]\n"
                 "})"},
                {"label": "A custom role: read reviews only", "kind": "good", "code":
                 "db.createRole({\n"
                 "  role: \"reviewReader\",\n"
                 "  privileges: [{\n"
                 "    resource: { db: \"training_store\",\n"
                 "                collection: \"reviews\" },\n"
                 "    actions: [\"find\"]\n"
                 "  }],\n"
                 "  roles: []\n"
                 "})"}],
               points=[("passwordPrompt()", "The password is typed, never stored in the "
                                            "script or history."),
                       ("Built-in roles", "readWrite and read cover most services."),
                       ("Custom roles", "Narrow a role to single collections and "
                                        "actions.")],
               takeaway="Create one identity per job, with the smallest role that works, "
                        "and never type a real password into a script.",
               notes=[tp("Don't run this in class",
                         "Exercise 8.2 is design only: don't enable authentication on the "
                         "shared "
                         "class database. Show these commands on a disposable instance if "
                         "you demonstrate them."),
                      tp("The two users",
                         "trainingStoreApp can read and write training_store and nothing "
                         "else. reportUser can only read. Neither can create users, drop "
                         "databases or touch other databases."),
                      tp("The custom role",
                         "reviewReader allows only find on the reviews collection. It is "
                         "the support analyst from the least-privilege diagram. Grant it "
                         "with db.grantRolesToUser."),
                      tp("Passwords",
                         "passwordPrompt() asks for the password interactively, so it "
                         "never appears in the script, in shell history or in a "
                         "screenshot.")]),
        F.diagram(img(34), "Network Security",
                  "Make the database unreachable to anyone who shouldn't reach it.",
                  items=[("Firewall", "Allow trusted IPs on 27017; block everything else."),
                         ("Private network", "mongod lives on a private subnet, never the "
                                             "public internet."),
                         ("bindIp", "Listen only on localhost and the private address "
                                    "clients use."),
                         {"callout": ("Atlas", "IP access lists and private endpoints.")}],
                  takeaway="Don't expose port 27017 broadly — restrict who can reach "
                           "mongod before anyone tries to log in.",
                  notes=dn(34)),
        F.code("Secure Configuration and Connection Strings",
               "A hardened mongod.conf — and the anti-pattern it replaces.",
               [{"label": "Hardened (sketch)", "kind": "good", "code":
                 "net:\n"
                 "  port: 27017\n"
                 "  bindIp: 127.0.0.1,10.0.1.15\n"
                 "  tls:\n"
                 "    mode: requireTLS\n"
                 "    certificateKeyFile: /etc/mongo/server.pem\n"
                 "    CAFile: /etc/mongo/ca.pem\n"
                 "security:\n"
                 "  authorization: enabled"},
                {"label": "Anti-pattern — never ship this", "kind": "bad", "code":
                 "net:\n"
                 "  bindIp: 0.0.0.0   # every interface\n"
                 "# no security section:\n"
                 "#   access control off, no TLS\n"
                 "\n"
                 "// URI with a password in source code\n"
                 "mongodb://admin:<password>@db:27017/"}],
               points=[("Listen narrowly", "Localhost plus one private address."),
                       ("TLS everywhere", "Validate certificates; never disable checks."),
                       ("Secrets", "Load the URI from a secret store at runtime.")],
               takeaway="Bind narrowly, require TLS and authentication, and keep "
                        "credentials out of code and configuration files.",
               notes=[tp("The hardened file",
                         "mongod listens on localhost and one private address, 10.0.1.15 in "
                         "this sketch. requireTLS refuses unencrypted connections, and "
                         "authorization enabled turns on access control. The paths and the "
                         "address are placeholders."),
                      tp("The anti-pattern",
                         "Binding to every interface on a reachable host with no security "
                         "section means anyone who can reach the port can read or delete "
                         "everything. This is shown only as a warning — never use it."),
                      tp("Connection strings",
                         "Treat a connection string as a secret. The application should "
                         "read it from a secret manager or protected environment variable, "
                         "with its own least-privilege user, never the admin account."),
                      tp("Client side",
                         "Production clients connect with tls=true, validate the server "
                         "certificate against a trusted certificate authority, and rotate "
                         "certificates before they expire.")]),
        F.myths("Security Misconceptions and Anti-Patterns",
                "Beliefs that leave real databases exposed.",
                [("It's on our network, so it's safe",
                  "Authenticate every connection — location isn't identity"),
                 ("The app needs admin to be safe",
                  "Least privilege: readWrite on its own database"),
                 ("TLS is only for the internet",
                  "Encrypt inside the data center and between members too"),
                 ("Encryption replaces password hashing",
                  "Hash application passwords; encrypt sensitive fields"),
                 ("Fix not-authorized by granting root",
                  "Grant the one missing privilege")],
                ["Port 27017 open to the internet",
                 "One shared administrator account",
                 "Passwords in code, Git or screenshots",
                 "Unencrypted backup files",
                 "Production data copied into development"],
                remember=("Remember", "Unreachable, authenticated, least privilege, "
                                      "encrypted."),
                takeaway="Most breaches come from simple gaps — exposure, shared accounts "
                         "and leaked credentials.",
                notes=[tp("Why this slide",
                          "Before we move on, clear away the beliefs that cause the most "
                          "common real incidents."),
                       tp("Network and identity",
                          "Being inside the network doesn't prove identity. Every connection "
                          "authenticates, and each service uses its own least-privilege "
                          "user."),
                       tp("Encryption",
                          "TLS protects traffic everywhere, not only on the internet. "
                          "Encryption at rest protects files and backups. Application "
                          "passwords are hashed, never just encrypted."),
                       tp("Anti-patterns",
                          "Look for these six risks in any review: a public endpoint, a "
                          "shared administrator, secrets in source control, no TLS, "
                          "unprotected backups and production data in development.")]),

        # Part 4 ------------------------------------------------------------
        F.bridge(PARTS, 3, "Part 4: Backups and Recovery",
                 "Replication keeps you running. Backups let you go back.",
                 so_far=["Access is authenticated and least-privilege",
                         "Traffic is encrypted; the network is closed",
                         "Credentials live outside the code"],
                 question="If someone deletes the orders tonight, what do we lose — and how "
                          "long until we are back?",
                 covers=["Replication versus backup",
                         "Recovery objectives: RPO and RTO",
                         "Restore testing"],
                 notes=[tp("The question",
                           "Security reduces the chance of damage; recovery limits its "
                           "cost. Mistakes and bad releases still happen."),
                        tp("The lab",
                           "Lab 7, Step 4 dumps training_store and restores it into an "
                           "isolated database, training_store_restore.")]),
        F.diagram(img(42), "Replication vs. Backup",
                  "Two different capabilities — you need both.",
                  items=[{"code": "db.orders.deleteMany({})\n"
                                  "// replicated to every member",
                          "label": "An accidental delete", "size": 12},
                         ("Replication", "Copies every change, good or bad, in seconds."),
                         ("Backup", "Immutable copies from before the mistake."),
                         {"callout": ("Rule", "Replication is not a backup.")}],
                  takeaway="Replication protects availability; only an independent backup "
                           "protects you from a bad change.",
                  notes=dn(42)),
        F.diagram(img(45), "Recovery Point and Recovery Time Objectives",
                  "How much data you may lose, and how long you may be down.",
                  items=[("RPO = 15 min", "Changes since the 10:00 backup are at risk."),
                         ("RTO = 30 min", "Service restored at 10:45 after a 10:15 "
                                          "failure."),
                         ("Set per data set", "Orders and payments tight; reviews more "
                                              "tolerant."),
                         {"callout": ("Exercise 8.3", "You'll set these for "
                                                      "training_store.")}],
                  takeaway="RPO and RTO are business targets in minutes — choose the backup "
                           "method that meets them.",
                  notes=dn(45)),
        F.diagram(img(46), "Restore Testing",
                  "A backup is proven only by a restore.",
                  items=[{"code": "mongodump --uri=\"mongodb://localhost:27017\"\n"
                                  "  --db=training_store --out=<dir>\n"
                                  "mongorestore --uri=\"mongodb://localhost:27017\"\n"
                                  "  --db=training_store_restore --drop\n"
                                  "  <dir>/training_store",
                          "label": "Lab 7, Step 4", "size": 10},
                         ("Verify", "17 orders, 13 products, a sample order and its "
                                    "indexes."),
                         {"callout": ("Never", "Restore over training_store itself.")}],
                  takeaway="Schedule restore tests into an isolated target, and measure the "
                           "time against the RTO.",
                  notes=dn(46, [tp("The commands",
                                   "mongodump writes a logical BSON copy of training_store. "
                                   "mongorestore loads it into training_store_restore; --drop "
                                   "replaces that restore database only. Then compare "
                                   "countDocuments in both databases.")])),

        # Part 5 ------------------------------------------------------------
        F.bridge(PARTS, 4, "Part 5: Operate and Diagnose",
                 "Monitor the right signals and troubleshoot from evidence.",
                 so_far=["Replication is not a backup",
                         "RPO and RTO are time targets",
                         "Restores are tested, not assumed"],
                 question="Something is wrong in production — how do we find out what, and "
                          "fix only that?",
                 covers=["Metrics that matter",
                         "A troubleshooting method",
                         "Common errors by layer",
                         "A slow-search investigation",
                         "Safe error handling",
                         "The production-readiness checklist"],
                 notes=[tp("Why this part",
                           "Production systems fail in ordinary ways. The skill is to "
                           "notice early and to diagnose from evidence instead of "
                           "guessing."),
                        tp("How it ends",
                           "The part closes with the readiness checklist that Lab 7 uses to "
                           "score training_store.")]),
        F.diagram(img(49), "Database, Query, and Resource Metrics",
                  "Three groups of signals — one health view.",
                  items=[{"code": "db.setProfilingLevel(1,\n"
                                  "  { slowms: 200, sampleRate: 0.2 })\n"
                                  "db.system.profile.find()\n"
                                  "  .sort({ ts: -1 }).limit(5)\n"
                                  "db.setProfilingLevel(0)",
                          "label": "Sample slow operations", "size": 11},
                         ("Also watch", "Disk space, oplog window, backup status, "
                                        "authentication failures."),
                         {"callout": ("Profiler", "Adds overhead — enable it "
                                                  "deliberately.")}],
                  takeaway="Monitor query evidence and replication, not only CPU — slow "
                           "queries show up there first.",
                  notes=dn(49)),
        F.diagram(img(54), "Troubleshooting Methodology",
                  "Symptom → scope → evidence → layer → cause → fix → verify.",
                  items=[("Precise symptom", "Not “MongoDB is slow” but “order history went "
                                             "from 100 ms to 2.5 s”."),
                         ("Scope and evidence", "One query or all? Logs, explain, metrics, "
                                                "recent changes."),
                         ("Smallest safe fix", "One index, one role, one setting — then "
                                               "verify."),
                         {"callout": ("Loop", "Re-run the same test after every fix.")}],
                  takeaway="Troubleshoot from evidence, one layer at a time, and verify with "
                           "the same test.",
                  notes=dn(54)),
        F.compare("Common Problems, by Layer",
                  "The error message usually names the layer.",
                  ["Symptom", "Likely layer", "First check"],
                  [("Connection refused", "Process, network", "mongod up? host, port, "
                                                              "firewall"),
                   ("Authentication failed", "Security", "user, password, authSource"),
                   ("not authorized", "Security: roles", "user's roles on that "
                                                         "collection"),
                   ("E11000 duplicate key", "Index", "which unique index"),
                   ("Document failed validation", "Schema", "missing field, type, enum"),
                   ("Slow query", "Query, index", "explain: COLLSCAN, SORT"),
                   ("Lag or no primary", "Replication", "rs.status(), majority"),
                   ("Every shard contacted", "Sharding", "shard key in the filter?")],
                  [2.55, 1.95, 3.30], row_h=0.50, size=12,
                  items=[("Authenticated ≠ authorized", "Wrong authSource fails login; a "
                                                        "missing role fails the command."),
                         ("Never", "Grant root, disable auth or bind to every interface to "
                                   "make an error go away."),
                         {"callout": ("Exercise", "Name the layer for five real "
                                                  "messages.")}],
                  takeaway="Read the error, name the layer, then check that layer first.",
                  notes=[tp("Process and network",
                            "Connection refused means nothing is listening where the client "
                            "points: mongod is stopped, the host or port is wrong, a "
                            "firewall or container port blocks it, or bindIp doesn't include "
                            "that interface. The fix is the correct interface — never every "
                            "interface."),
                         tp("Security",
                            "Authentication failed is about identity: check the user, the "
                            "password and authSource. A user created in admin needs "
                            "authSource=admin in the URI. not authorized means login "
                            "worked but a role is missing."),
                         tp("Data rules",
                            "E11000 comes from a unique index. In training_store, inserting "
                            "a second customer with aisha@example.com violates email_unique. "
                            "Code 121 is a validator rejection."),
                         tp("Cluster",
                            "For lag or no primary, run rs.status() and db.hello(): look for "
                            "a lost majority, an election or an undersized oplog. A query "
                            "that contacts every shard is missing the shard key.")]),
        F.diagram(img(59), "Slow Application Investigation",
                  "Follow the user's request down to the plan.",
                  items=[("Trace", "The slow search filters by category and sorts by "
                                   "price."),
                         ("Explain", "COLLSCAN — no index matches the shape."),
                         ("Fix and verify", "{ category: 1, price: 1 } → IXSCAN, 85 ms."),
                         {"callout": ("Same index", "The one Module 1 showed in "
                                                    "mongosh.")}],
                  takeaway="Start from the request the user felt, and verify with the same "
                           "request.",
                  notes=dn(59)),
        F.code("Handle Errors Safely",
               "Business messages, repeatable writes and bounded waits.",
               [{"label": "Expected conflict → safe message", "kind": "info", "code":
                 "db.customers.insertOne({\n"
                 "  customerNumber: \"C999\",\n"
                 "  contact: { email: \"aisha@example.com\" }\n"
                 "})\n"
                 "// MongoServerError: E11000 duplicate\n"
                 "//   key error ... index: email_unique\n"
                 "// user sees: \"An account already\n"
                 "//   exists for that email.\""},
                {"label": "Guarded, repeatable transition", "kind": "good", "code":
                 "db.orders.updateOne(\n"
                 "  { orderNumber: \"O6302\",\n"
                 "    fulfillmentStatus: \"PROCESSING\" },\n"
                 "  { $set: { fulfillmentStatus: \"SHIPPED\" },\n"
                 "    $currentDate: { shippedAt: true } }\n"
                 ")\n"
                 "// 1st run: modifiedCount 1\n"
                 "// 2nd run: matchedCount 0\n"
                 "\n"
                 "db.orders.find({ fulfillmentStatus:\n"
                 "  \"PROCESSING\" }).maxTimeMS(3000)"}],
               points=[("Log internally", "The raw error, securely, with a request ID."),
                       ("Idempotent", "A retry can't ship the order twice."),
                       ("Timeouts", "No operation waits forever.")],
               takeaway="Turn database errors into safe messages, and design writes that "
                        "are safe to retry.",
               notes=[tp("Duplicate key",
                         "customers has a unique index, email_unique, on contact.email. "
                         "Aisha Khan already uses aisha@example.com, so this insert fails "
                         "with E11000. The content guide calls the index "
                         "uq_customers_email; in training_store it is email_unique."),
                      tp("What the user sees",
                         "Log the full error internally, without credentials or complete "
                         "documents. Show the user a business message, never the stack "
                         "trace, host names or collection names."),
                      tp("Guarded update",
                         "O6302 is PROCESSING in the loaded data. The filter includes the "
                         "current state, so the first run ships it and a retry matches "
                         "nothing. Run it only on a copy, or reload with load.js "
                         "afterwards."),
                      tp("Timeouts",
                         "maxTimeMS(3000) stops this query after three seconds. Configure "
                         "server-selection, connection and socket timeouts in the driver "
                         "too, and choose values from the workload.")]),
        F.exercise("Exercise: Which Layer Is It?",
                   "Five messages from the training_store application.",
                   scenario="Name the layer and the first check for each message.",
                   scenario_code="A connect ECONNREFUSED\n"
                                 "  127.0.0.1:27017\n"
                                 "B Authentication failed\n"
                                 "  (user trainingStoreApp)\n"
                                 "C not authorized on training_store\n"
                                 "  to execute command { find:\n"
                                 "  \"orders\" }\n"
                                 "D E11000 ... index: email_unique\n"
                                 "E Document failed validation",
                   tasks=["Name the layer for A–E",
                          "Write the first check or command",
                          "Say what you would not do",
                          "Pick one to add to a runbook"],
                   expected=["A process or network: is mongod up?",
                             "B identity: authSource and user",
                             "C roles: grant only find on orders",
                             "D business conflict: safe message",
                             "E schema: which rule failed"],
                   minutes=10,
                   takeaway="The message names the layer — read it before you change "
                            "anything.",
                   notes=[tp("How to run it",
                             "Pairs for five minutes, then go round the room, one message "
                             "per pair."),
                          tp("A and B",
                             "A: nothing is listening on localhost 27017. Check that mongod "
                             "is running and the port is right, then connect and run "
                             "db.hello(). B: check the user name, the password source and "
                             "authSource."),
                          tp("C",
                             "Login worked; the role is missing. Grant find on orders or a "
                             "read role — never root."),
                          tp("D and E",
                             "D is a duplicate email: an expected business outcome, shown to "
                             "the user as a friendly message. E is a validator rejection, "
                             "code 121: read the details to see which rule failed."),
                          tp("What not to do",
                             "Don't disable authentication, grant root, or bind to every "
                             "interface to make an error disappear.")]),
        F.custom(_checklist, "Production-Readiness Checklist",
                 "Six areas — each needs evidence, not assumptions.",
                 takeaway="Go live only when every area has evidence — a single “not "
                          "ready” area blocks the launch.",
                 notes=[tp("How to use it",
                           "This is the checklist Lab 7, Step 5 uses. For each "
                           "area, ask for evidence: an explain output, a restore log, a "
                           "role list, an alert rule."),
                        tp("Model, queries, indexes",
                           "Bounded arrays, consistent types, a validator and a migration "
                           "plan. Queries filtered and limited, pipelines checked against a "
                           "control. Every index tied to a query shape and confirmed with "
                           "explain."),
                        tp("Security and recovery",
                           "Authentication and least privilege, TLS, a closed network, "
                           "secrets outside code. A replica set with tested failover, "
                           "backups separate from replication, and a restore measured "
                           "against RPO and RTO."),
                        tp("Operations",
                           "Metrics and alerts with owners, runbooks for the critical "
                           "alerts, and changes reviewed with explain before release."),
                        tp("training_store today",
                           "Against this list our class instance is not ready: no "
                           "authentication, one server, XBAD's string price, no validator "
                           "and no tested restore. That is the expected answer in Lab 7.")]),

        # Wrap-up ------------------------------------------------------------
        F.knowledge("Knowledge Check", "Answer in your own words — then compare with a partner.",
                    ["Why design documents around access patterns?",
                     "When should related data be referenced?",
                     "What does schema validation add?",
                     "Why can $unwind over-count revenue?",
                     "What does the ESR rule say?",
                     "Examined ≫ returned — what does it suggest?",
                     "Why is replication not a backup?",
                     "What do RPO and RTO measure?",
                     "Authentication vs. authorization?",
                     "How do you start on a slow endpoint?"],
                    notes=[tp("1. Access patterns",
                              "Store together what the application reads and updates "
                              "together, so common operations need one read."),
                           tp("2. Reference",
                              "When the data is shared, changes independently, is queried on "
                              "its own or grows without limit — like reviews."),
                           tp("3. Validation",
                              "The database enforces required fields, types, enums and "
                              "ranges, and rejects bad writes with code 121."),
                           tp("4. $unwind",
                              "Each order becomes one row per item, so summing the order "
                              "total counts it several times: 12119.25 instead of 9118.44 "
                              "for paid orders."),
                           tp("5. ESR",
                              "In a compound index, put equality fields first, then the "
                              "sort field, then range fields."),
                           tp("6. Examined versus returned",
                              "A missing or unsuitable index: the plan reads many more keys "
                              "or documents than it returns."),
                           tp("7. Replication",
                              "It copies every change, including mistakes such as "
                              "deleteMany, to every member within seconds."),
                           tp("8. RPO and RTO",
                              "RPO is how much data may be lost; RTO is how long recovery "
                              "may take. Both are measured in time."),
                           tp("9. Authentication and authorization",
                              "Authentication proves who you are; authorization decides "
                              "what you may do."),
                           tp("10. Slow endpoint",
                              "Define the symptom precisely, scope it, collect evidence — "
                              "the query shape and its explain, logs and recent changes — "
                              "then fix the layer at fault and verify.")]),
        F.exercise("Exercise 8.1 — Review a Query and Projection",
                   "Module 8 checkpoint A: from find({}) to a bounded, indexed query.",
                   kind="OFFICIAL CHECKPOINT A", minutes=15,
                   worksheet="labs/day-03/exercises/exercise-8.1-review-a-query-and-"
                             "projection.md",
                   scenario="The app needs C101's paid orders, newest first, ten at a time: "
                            "orderNumber, fulfillmentStatus, total and createdAt. Today it "
                            "runs:",
                   scenario_code="db.orders.find({})",
                   tasks=["Add a selective filter",
                          "Project the four fields",
                          "Sort newest first and limit to ten",
                          "Name a compound index, labelled E or S"],
                   expected=["customerId: c101, paymentStatus: \"PAID\"",
                             "{ _id: 0, orderNumber: 1, … }",
                             ".sort({ createdAt: -1 }).limit(10)",
                             "{ customerId: 1, paymentStatus: 1, createdAt: -1 }",
                             "4 orders: O6306, O6301, O6201, O6101"],
                   expected_title="Solution (after debrief)",
                   takeaway="A production query is selective, shaped, ordered, bounded — "
                            "and backed by an index.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 8.1. The worksheet is "
                             "labs/day-03/exercises/exercise-8.1-review-a-query-and-"
                             "projection.md. Lab 7, Step 1 applies the same habits to the "
                             "catalog query."),
                          tp("The customer id",
                             "customerId is an ObjectId, so first run const c101 = "
                             "db.customers.findOne({ customerNumber: \"C101\" })._id."),
                          tp("The answer",
                             "Filter on customerId and paymentStatus PAID; project "
                             "orderNumber, fulfillmentStatus, total and createdAt with _id "
                             "0; sort createdAt descending; limit 10. It returns Aisha "
                             "Khan's four paid orders: O6306, O6301, O6201 and O6101. Her "
                             "pending order O5001 is excluded."),
                          tp("The index",
                             "customerId 1, paymentStatus 1, createdAt -1: equality, "
                             "equality, sort. Don't lead with createdAt.")]),
        F.exercise("Exercise 8.2 — Design Least-Privilege Roles",
                   "Module 8 checkpoint B: a permit / deny matrix for six identities.",
                   kind="OFFICIAL CHECKPOINT B", minutes=20,
                   worksheet="labs/day-03/exercises/exercise-8.2-design-least-"
                             "privilege-roles.md",
                   scenario="For each identity, list one permitted and one prohibited "
                            "operation on training_store.",
                   scenario_code="1 Application service\n"
                                 "2 Reporting service\n"
                                 "3 Support engineer\n"
                                 "4 Monitoring service\n"
                                 "5 Backup service\n"
                                 "6 Database administrator",
                   tasks=["Fill the permit / deny matrix",
                          "Choose a role for each identity",
                          "Explain why the app never uses clusterAdmin",
                          "Use placeholder names only"],
                   expected=["App: readWrite, never userAdmin",
                             "Reporting: read only",
                             "Support: limited read, never drop",
                             "Monitoring: clusterMonitor, no writes",
                             "Backup: backup role; DBA: separate identity"],
                   expected_title="Solution (after debrief)",
                   takeaway="Least privilege limits the blast radius of any stolen "
                            "credential.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 8.2. The worksheet is "
                             "labs/day-03/exercises/exercise-8.2-design-least-privilege-"
                             "roles.md. It is a design exercise; no authentication is "
                             "enabled."),
                          tp("The matrix",
                             "The application reads and writes its collections but can't "
                             "administer users. Reporting reads approved collections but "
                             "can't update. Support reads, perhaps with limited personal "
                             "data, but can't drop. Monitoring gets clusterMonitor-style "
                             "rights and no data writes. Backup gets backup privileges, not "
                             "arbitrary deletes. The DBA has administration under change "
                             "control and is never used by the application."),
                          tp("The anti-pattern",
                             "If the application used a cluster administrator, one stolen "
                             "application credential would inherit every privilege. Least "
                             "privilege limits the blast radius and makes audit trails "
                             "meaningful.")]),
        F.exercise("Exercise 8.3 — Define RPO and RTO",
                   "Module 8 checkpoint C: recovery targets for each part of the store.",
                   kind="OFFICIAL CHECKPOINT C", minutes=15,
                   worksheet="labs/day-03/exercises/exercise-8.3-define-rpo-and-rto.md",
                   scenario="Treat training_store as a small retailer, not a global bank.",
                   scenario_code="Data sets to plan:\n"
                                 "  product catalog\n"
                                 "  customer profiles\n"
                                 "  orders\n"
                                 "  payments\n"
                                 "  reviews",
                   tasks=["Write RPO and RTO for each data set",
                          "Pick a backup frequency that meets each RPO",
                          "Describe how you would prove an orders restore"],
                   expected=["Orders, payments: RPO in minutes",
                             "Catalog: longer RPO is acceptable",
                             "Reviews: the most tolerant",
                             "Checkout RTO shorter than reviews",
                             "Prove it: counts, O5001, indexes, a read"],
                   expected_title="Solution (after debrief)",
                   takeaway="A backup job that succeeded is not a recovery plan — a "
                            "measured restore is.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 8.3. The worksheet is "
                             "labs/day-03/exercises/exercise-8.3-define-rpo-and-rto.md."),
                          tp("Objectives",
                             "Orders and payments usually get the tightest RPO, in minutes, "
                             "with tested point-in-time recovery. The catalog can often "
                             "tolerate a longer RPO because it can be rebuilt. Reviews are "
                             "the most tolerant. Checkout's RTO should be shorter than the "
                             "RTO for reviews."),
                          tp("Proving an orders restore",
                             "Compare countDocuments with the pre-restore note — 17 on a "
                             "fresh load. Find O5001 and check a paid total. Run "
                             "getIndexes(). Confirm the application can read an order. "
                             "Backup success alone is not enough.")]),
        F.exercise("Lab 7 — Production Readiness",
                   "The course's final lab: treat training_store as a go-live candidate.",
                   kind="OFFICIAL LAB 7", minutes=60,
                   worksheet="labs/day-03/lab7/LAB-7-GUIDE.md",
                   scenario="Reload first if Day 2–3 writes remain. Never restore over "
                            "training_store.",
                   scenario_code="1 Stop the catalog collection scan\n"
                                 "2 Monthly paid-order pipeline\n"
                                 "3 Validator on training_store_ops\n"
                                 "4 Restore to training_store_restore\n"
                                 "5 Score go-live with evidence",
                   tasks=["Filter, project, sort, limit, explain",
                          "Build the pipeline with $match first",
                          "Prove one accepted and one rejected insert",
                          "Restore and compare product counts",
                          "Classify: ready, conditional or not ready"],
                   expected=["Two active laptops returned",
                             "Three months: July to September",
                             "OPS-BAD rejected",
                             "13 products in both databases",
                             "Not ready — with named evidence"],
                   expected_title="Expected results",
                   takeaway="Lab 7 turns the whole course into one production-readiness "
                            "review.",
                   notes=[tp("Official lab",
                             "This is Lab 7, the Day 3 lab: labs/day-03/lab7/LAB-7-GUIDE.md. "
                             "It takes 45 to 60 minutes. Expected outputs for every step are "
                             "in labs/day-03/lab7/solution/LAB-7-SOLUTION.md."),
                          tp("Steps 1 to 3",
                             "Step 1 rewrites the catalog query and proposes category 1, "
                             "active 1, price 1 without dropping existing indexes. Step 2 is "
                             "the monthly pipeline from Part 2. Step 3 is the validator on "
                             "training_store_ops.orders_validated."),
                          tp("Step 4",
                             "Dump training_store and restore into training_store_restore. "
                             "Both databases show 13 products. If the classroom image has no "
                             "Database Tools, use the Exercise 8.3 restore-proof answer "
                             "instead."),
                          tp("Step 5",
                             "The defensible answer is not ready. Evidence includes XBAD's "
                             "string price, no authentication in class, tiny data, no stock "
                             "field, and no restore tested in the learner's own environment. "
                             "Conditions for go-live: typed money, authentication and TLS, a "
                             "restore drill, least-privilege roles and explain on real "
                             "volume.")]),
        F.diagram(img(67), "The Course at a Glance",
                  "One database, eight modules, one layer at a time.",
                  takeaway="Every module added one layer to the same training_store "
                           "database.",
                  notes=dn(67)),
        F.wrapup("Course Summary and Next Steps",
                 "From why NoSQL exists to running MongoDB securely and reliably.",
                 can=["Choose a data model and design documents",
                      "Install, connect and load MongoDB",
                      "Query, update and aggregate documents",
                      "Index from query shapes and explain",
                      "Replicate for availability; shard for scale",
                      "Secure, back up, monitor and troubleshoot"],
                 next_title="Next: Apply It to Your Own Systems",
                 questions=["Which query will you explain first?",
                            "When will you test a restore?",
                            "Which alert needs a runbook?"],
                 bring=("Take with you", "The readiness checklist, your Lab 7 scorecard "
                                         "and one action for next week."),
                 takeaway="Model around access patterns, measure before tuning, secure by "
                          "default and prove every recovery.",
                 notes=[tp("Recap",
                           "Across eight modules we chose a data model, set up MongoDB, "
                           "designed documents, queried and aggregated them, indexed with "
                           "evidence, replicated and sharded, and finally learned to run it "
                           "securely and reliably — all on training_store."),
                        tp("The ten principles",
                           "Model around how the application uses data. Embed bounded data "
                           "that belongs together; reference shared or unbounded data. Keep "
                           "names and types consistent. Design indexes around real query "
                           "shapes. Measure before and after. Filter early in pipelines. "
                           "Apply authentication, authorization, TLS and network limits. "
                           "Treat replication, sharding and backups as different "
                           "capabilities. Troubleshoot from evidence."),
                        tp("Next steps",
                           "Ask each participant for one action: a schema or validation "
                           "change, a query to explain, a security control to verify, a "
                           "restore test to schedule, or an alert that needs a runbook. "
                           "Recommend the current MongoDB security checklist and operations "
                           "documentation for their version."),
                        tp("Close",
                           "Thank the group, take final questions, and collect feedback.")]),
    ]
