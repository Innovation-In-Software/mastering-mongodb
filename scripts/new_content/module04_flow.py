#!/usr/bin/env python3
"""Slide order for the Module 4 deck: one story from reading documents to safe writes.

Every concept diagram is merged with the slide that explains it (diagram plus the
points only that slide adds), so no idea appears twice. The diagrams draw small
sample documents; the slide text beside each one gives the real result on
training_store. Part openers, mongosh examples, in-flow practice exercises, a
knowledge check, four official checkpoints (Exercises 4.1-4.4, worksheets in
labs/day-02/exercises/), the Day 2 Lab 3 slide (labs/day-02/lab3/LAB-3-GUIDE.md)
and a hand-off to Module 5 connect the ideas.

Every count and result below is from a fresh load of datasets/training_store/load.js.
"""
from __future__ import annotations

import mdb_diagram_slides as DS
import mdb_flow_slides as F
import mdb_glossary as G
import mdb_visuals as V
from mdb_flow_slides import tp
from mdb_visuals import (
    GREEN, LEFT, NAVY, ORANGE, PURPLE, RED, RIGHT, TEAL,
)

PARTS = ["Part 1\nRead documents", "Part 2\nQuery operators", "Part 3\nNested and arrays",
         "Part 4\nInsert and update", "Part 5\nDelete and verify"]


# ---------------------------------------------------------------------------
# Custom slides
# ---------------------------------------------------------------------------
def _data(slide, y0, y1):
    lw = 7.70
    y = V.section(slide, LEFT, y0, lw, "Four collections on a fresh load", icon="🛒",
                  fill=NAVY)
    collections = [("customers", "6 documents", NAVY), ("products", "13 documents", TEAL),
                   ("orders", "17 documents", PURPLE), ("reviews", "6 documents", GREEN)]
    cw, cg = (lw - 3 * 0.14) / 4, 0.14
    for k, (name, count, fill) in enumerate(collections):
        V.box(slide, LEFT + k * (cw + cg), y + 0.02, cw, 0.72,
              [(name, {"size": 15}), (count, {"size": 12, "bold": False})],
              fill=fill, size=15, margin=0.04)
    y = V.section(slide, LEFT, y + 1.02, lw, "Field names to query — exactly as stored",
                  icon="🔑", fill=PURPLE)
    V.code(slide, LEFT, y + 0.02, lw, 1.62,
           "products   sku, name, category, price, tags, attributes, active\n"
           "customers  customerNumber, name.first, contact.email, addresses\n"
           "orders     orderNumber, customerId, items, paymentStatus,\n"
           "           fulfillmentStatus, total, createdAt\n"
           "reviews    sku, productId, customerId, rating, title, body", size=12)
    V.callout(slide, LEFT, y + 1.82, lw, y1 - (y + 1.82), "Values are uppercase",
              "category \"LAPTOP\", status \"ACTIVE\", paymentStatus \"PAID\" — and "
              "there is no order field called status.", size=14)

    rx = LEFT + lw + 0.40
    F.stack_items(slide, rx, y0, RIGHT - rx, y1 - y0, [
        {"checks": ["XBAD: price is the string \"49.99\"",
                    "C204: phone is null; C515 has none",
                    "L190: inactive, tagged discontinued",
                    "O5001: L100 × 1 and A410 × 2",
                    "No stock field on any product"],
         "h": "Planted on purpose", "c": RED, "mark": "!", "size": 13},
        {"callout": ("Reload", "Run load.js again before each lab so counts start fresh.")},
    ])


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
        *G.intro("module04"),
        F.story("From Module 3 to Module 4",
                "Module 3 designed the documents. Now we read and change them.",
                gave_title="Module 3 gave us",
                gave=["Documents shaped by access patterns",
                      "Items embedded, customers referenced",
                      "Decimal128 money, Date timestamps",
                      "Four collections in training_store"],
                now=("Now", "Query and change that model with filters shaped like the "
                            "documents."),
                path_title="The path through Module 4",
                path=[("Read: find, filters, projection, sort", "Part 1", NAVY),
                      ("Comparison, logical and element operators", "Part 2", PURPLE),
                      ("Nested fields and arrays", "Part 3", TEAL),
                      ("Insert, update, upsert and replace", "Part 4", GREEN),
                      ("Delete, bulk write and verify", "Part 5", ORANGE)],
                takeaway="The document design from Module 3 decides how every query in "
                         "Module 4 is written.",
                notes=[tp("Where we are",
                          "Module 4 opens Day 2. On Day 1, Module 3 designed the training_store "
                          "documents: products with category attributes, orders that embed "
                          "their items and reference their customer, and reviews in their own "
                          "collection."),
                       tp("Why it matters now",
                          "Queries follow the document shape. Because items are embedded, we "
                          "query \"items.sku\" instead of joining. Because prices are "
                          "Decimal128, we compare with Decimal128 values."),
                       tp("The path",
                          "Five parts: reading and shaping results, operators, nested fields "
                          "and arrays, inserts and updates, and finally deletes, bulk writes "
                          "and verification. Day 2 Lab 3 practises all of it."),
                       tp("Before class",
                          "Reload the dataset with mongosh and datasets/training_store/load.js "
                          "so everyone sees the same counts.")]),
        F.custom(_data, "The training_store Data We Query",
                 "Counts, field names and the traps planted for this module.",
                 takeaway="Look at the real field names, values and types before writing a "
                          "filter — MongoDB matches exactly what is stored.",
                 notes=[tp("The counts",
                           "On a fresh load: 6 customers, 13 products, 17 orders and 6 "
                           "reviews. 13 orders are PAID. These numbers come back in every "
                           "exercise."),
                        tp("Field names",
                           "Use the names exactly as stored: sku, category, price, tags, "
                           "attributes; customerNumber and contact.email; orderNumber, items, "
                           "paymentStatus and fulfillmentStatus. Orders have no status field, "
                           "and products have no stock field."),
                        tp("Planted fixtures",
                           "The loader plants traps on purpose. XBAD, Legacy Cable Pack, "
                           "stores its price as a string. C204's phone is null and C515 has no "
                           "phone field. L190 is inactive and tagged discontinued. O5001 has "
                           "L100 quantity 1 and A410 quantity 2 — the $elemMatch trap."),
                        tp("About the guides",
                           "Some older examples say Electronics, ELEC-1001, stock or status "
                           "Processing. Those are generic; the lab guide and these slides use "
                           "the real training_store fields."),
                        tp("Demo 4.1",
                           "Run show collections and one findOne() per collection. Ask the "
                           "class to point at a nested object, an array and a Decimal128 "
                           "before writing any filter.")]),

        # Part 1 ------------------------------------------------------------
        F.bridge(PARTS, 0, "Part 1: Reading Documents",
                 "find(), findOne() and the shape of a read query.",
                 so_far=["You know the module goals and key terms",
                         "You know the fields and planted traps"],
                 question="How do we ask for exactly the documents — and fields — we need?",
                 covers=["Query filters", "findOne() versus find()",
                         "Filter, projection, sort, limit", "Projection rules",
                         "Sort, skip and limit for pages", "Counting and distinct values"],
                 notes=[tp("Where we start",
                           "Every operation in this module starts with a filter, so we begin "
                           "with reading: which documents match, and what comes back."),
                        tp("What this part answers",
                           "How filters work, when to use findOne() or find(), how to shape "
                           "results with projection, sort, skip and limit, and how to count.")]),
        F.diagram(img(7), "Understanding Query Filters",
                  "The filter is a document; each document either matches or doesn't.",
                  items=[("A document of conditions", "{ field: value } pairs — every pair "
                                                      "must be true."),
                         ("Exact and case-sensitive", "\"LAPTOP\" matches 3 products; "
                                                      "\"Laptop\" matches none."),
                         {"code": "db.products.find({\n"
                                  "  category: \"BOOK\",\n"
                                  "  price: { $lt:\n"
                                  "    Decimal128(\"50.00\") }\n"
                                  "})\n"
                                  "// Query Cookbook (39.99)",
                          "label": "On training_store", "size": 11}],
                  takeaway="A filter is a document of conditions — a document matches only when "
                           "every condition is true.",
                  notes=dn(7)),
        F.diagram(img(8), "findOne() vs find()",
                  "One document or null — or a cursor over every match.",
                  items=[("findOne()", "Returns one document, or null when nothing matches."),
                         ("find()", "Returns a cursor; mongosh prints 20 at a time — type it "
                                    "for more."),
                         {"code": "db.products.findOne(\n"
                                  "  { sku: \"L100\" })\n"
                                  "// Business Laptop",
                          "label": "By a unique field", "size": 11},
                         {"callout": ("Tip", "sku has a unique index, so one match is "
                                             "guaranteed.")}],
                  takeaway="Use findOne() when you expect one document and find() when you "
                           "expect a list.",
                  notes=dn(8)),
        F.diagram(img(48), "Anatomy of a Read Query",
                  "Filter, projection, sort and limit — the four questions of a read.",
                  items=[{"code": "db.products.find(\n"
                                  "  { category: \"BOOK\" },\n"
                                  "  { _id: 0, name: 1,\n"
                                  "    price: 1 }\n"
                                  ").sort({ price: 1 })\n"
                                  " .limit(10)",
                          "label": "The same shape on training_store", "size": 11},
                         ("Result", "Query Cookbook 39.99, then MongoDB Fundamentals 59.99."),
                         ("Order of thought", "Which documents, which fields, which order, how "
                                              "many?")],
                  takeaway="Build a read in four steps: filter the documents, project the "
                           "fields, sort them, limit the count.",
                  notes=dn(48)),
        F.diagram(img(23), "Projection Fundamentals",
                  "The second argument of find() chooses the fields that come back.",
                  items=[("Include", "{ name: 1, price: 1 } — _id comes too unless you add "
                                     "_id: 0."),
                         ("Exclude", "{ attributes: 0, tags: 0 } — every other field comes "
                                     "back."),
                         ("Don't mix", "{ name: 1, tags: 0 } is an error; only _id may be "
                                       "mixed."),
                         {"code": "db.customers.find(\n"
                                  "  { customerNumber: \"C101\" },\n"
                                  "  { _id: 0, \"name.first\": 1 })\n"
                                  "// { name: { first: \"Aisha\" } }",
                          "label": "Nested paths work too", "size": 11}],
                  takeaway="Return only the fields the caller needs — projection shapes the "
                           "result, never the stored document.",
                  notes=dn(23)),
        F.diagram(img(26), "Sorting, Skipping and Limiting",
                  "sort() orders, skip() jumps, limit() caps — together they make a page.",
                  items=[("sort()", "1 ascending, -1 descending; add _id as a tie-breaker."),
                         ("skip() and limit()", "skip = (page − 1) × pageSize; limit = "
                                                "pageSize."),
                         {"code": "db.products\n"
                                  "  .find({ active: true })\n"
                                  "  .sort({ price: 1, _id: 1 })\n"
                                  "  .skip(5).limit(5)",
                          "label": "Page 2 of active products", "size": 11},
                         {"callout": ("Result", "B300, S210, S200, A500, L100.")}],
                  takeaway="Always sort before you page — without a stable order, pages can "
                           "repeat or skip documents.",
                  notes=dn(26)),
        F.code("Counting and Distinct Values",
               "How many documents match — and which values a field holds.",
               [{"label": "Count accurately", "kind": "info", "code":
                 "db.products\n"
                 "  .countDocuments({})\n"
                 "// 13\n"
                 "db.products.countDocuments(\n"
                 "  { active: true })\n"
                 "// 12 — L190 is inactive"},
                {"label": "Estimate from metadata", "kind": "info", "code":
                 "db.products\n"
                 "  .estimatedDocumentCount()\n"
                 "// 13 — takes no filter\n"
                 "\n"
                 "// legacy, avoid:\n"
                 "db.products.find().count()"},
                {"label": "Unique values", "kind": "info", "code":
                 "db.products.distinct(\n"
                 "  \"category\")\n"
                 "// [ \"ACCESSORY\", \"BOOK\",\n"
                 "//   \"LAPTOP\", \"SHOE\" ]\n"
                 "db.products.distinct(\n"
                 "  \"attributes.connection\",\n"
                 "  { category: \"ACCESSORY\" })\n"
                 "// [ \"Bluetooth\", \"USB-C\" ]"}],
               points=[("countDocuments()", "Exact count for a filter — your safety check."),
                       ("estimatedDocumentCount()", "Fast total from metadata, no filter."),
                       ("distinct()", "Unique values; an optional filter narrows them.")],
               takeaway="Count with countDocuments() before and after every change — it is the "
                        "cheapest check you have.",
               notes=[tp("countDocuments()",
                         "countDocuments({}) returns 13 and countDocuments({ active: true }) "
                         "returns 12, because L190 is inactive. It runs the filter, so the "
                         "number is exact."),
                      tp("estimatedDocumentCount()",
                         "Reads the collection's metadata, so it is fast but takes no filter. "
                         "It returns 13 here. The older find().count() still appears in old "
                         "examples; new code should use one of these two methods."),
                      tp("distinct()",
                         "distinct(\"category\") returns ACCESSORY, BOOK, LAPTOP and SHOE. With "
                         "a filter, distinct(\"attributes.connection\", { category: "
                         "\"ACCESSORY\" }) returns Bluetooth and USB-C. On an array field, "
                         "such as tags, each element counts as a separate value."),
                      tp("Link to the labs",
                         "Lab 3 changes documents from step 8 on. countDocuments({}) and "
                         "countDocuments({ active: true }) — 13 and 12 on a fresh load — are the "
                         "quickest way to prove the reload worked before you start.")]),
        F.exercise("Exercise: Predict the Sorted Result",
                   "Read the query, write your answer, then run it.",
                   scenario="The five accessories cost 19.99, 24.99, 49.99 and 249.99 — and "
                            "XBAD, whose price is stored as the string \"49.99\".",
                   scenario_code="db.products.find(\n"
                                 "  { category: \"ACCESSORY\" },\n"
                                 "  { _id: 0, sku: 1, price: 1 }\n"
                                 ").sort({ price: -1 })\n"
                                 " .limit(3)",
                   tasks=["Write the three SKUs you expect, in order",
                          "Say where XBAD lands, and why",
                          "Run it on the instructor's screen",
                          "Change the filter so only Decimal128 prices sort"],
                   expected=["XBAD first: strings sort after numbers",
                             "Then A500 (249.99) and P1001 (49.99)",
                             "Add price: { $type: \"decimal\" }",
                             "Then A500, P1001, A400"],
                   minutes=10,
                   takeaway="Mixed BSON types sort by type first, then value — one bad document "
                            "can top a price list.",
                   notes=[tp("How to run it",
                             "Two minutes to write a prediction, then run it on the instructor "
                             "screen. Most people predict A500 first."),
                          tp("Why XBAD is first",
                             "MongoDB compares different BSON types in a fixed order, and "
                             "numbers come before strings. In a descending sort the string "
                             "\"49.99\" therefore lands above every Decimal128 price."),
                          tp("The rest of the answer",
                             "After XBAD come A500 at 249.99 and P1001 at 49.99. The limit stops "
                             "there, so A400 and A410 are not shown."),
                          tp("The fix",
                             "Adding price: { $type: \"decimal\" } to the filter returns A500, "
                             "P1001 and A400. The real fix is to correct XBAD's price in the "
                             "data. The course leaves it as a string on purpose, so the same "
                             "trap tops any descending price sort — L110 is only first once "
                             "XBAD is filtered out.")]),

        # Part 2 ------------------------------------------------------------
        F.bridge(PARTS, 1, "Part 2: Query Operators",
                 "Comparison, logical and element operators.",
                 so_far=["Filters are documents of conditions",
                         "Projection, sort and limit shape the result",
                         "countDocuments() checks every step"],
                 question="How do we express ranges, lists, either-or and missing values?",
                 covers=["Comparison operators and ranges", "$in and $nin",
                         "$and and $or", "Building a filter step by step", "$not and $nor",
                         "Missing, null and BSON type", "Regular expressions and dates"],
                 notes=[tp("Connecting the parts",
                           "Part 1 used equality and one $lt. Part 2 adds the operators that "
                           "real business questions need."),
                        tp("Watch for",
                           "Two themes run through this part: the BSON type of the value you "
                           "compare, and negative operators that also match missing "
                           "fields.")]),
        F.diagram(img(12), "Comparison Operators",
                  "$gt, $gte, $lt and $lte — inside the field they test.",
                  items=[("Inside the field", "{ price: { $gt: … } } — never "
                                              "{ $gt: { price: … } }."),
                         ("Money is Decimal128", "Compare with Decimal128(\"100.00\"); a string "
                                                 "never matches a number."),
                         ("A range", "Two operators on one field; $gte and $lte include both "
                                     "ends."),
                         {"callout": ("On training_store",
                                      "50.00 to 500.00 returns L190, S200, S210, B300 and "
                                      "A500.")}],
                  takeaway="Put comparison operators inside the field, and compare with the same "
                           "BSON type that is stored.",
                  notes=dn(12)),
        F.code("Comparisons, $in and $nin on training_store",
               "Real results — and the product that never shows up.",
               [{"label": "Above 100", "kind": "info", "code":
                 "db.products.find(\n"
                 "  { price: { $gt:\n"
                 "    Decimal128(\"100.00\") } },\n"
                 "  { _id: 0, sku: 1 })\n"
                 "// L100 L110 L190\n"
                 "// S200 A500"},
                {"label": "Any value in a list", "kind": "info", "code":
                 "db.products.countDocuments({\n"
                 "  category: { $in:\n"
                 "    [\"LAPTOP\", \"BOOK\"] } })\n"
                 "// 5\n"
                 "db.reviews.countDocuments(\n"
                 "  { rating: { $gte: 4 } })\n"
                 "// 5 of 6 reviews"},
                {"label": "None of a list", "kind": "info", "code":
                 "db.products.find(\n"
                 "  { category: { $nin:\n"
                 "    [\"LAPTOP\", \"SHOE\"] } },\n"
                 "  { _id: 0, sku: 1 })\n"
                 "// B300 B310 P1001 A400\n"
                 "// A410 A500 XBAD"}],
               points=[("XBAD is missing above", "Its price is a string, so no numeric range "
                                                 "sees it."),
                       ("$in", "An OR on one field — shorter than $or."),
                       ("$nin and $ne", "Also match documents where the field is missing.")],
               takeaway="Use $in and $nin for lists on one field — and remember that negative "
                        "operators also match missing fields.",
               notes=[tp("Above 100",
                         "Five products cost more than 100: L100, L110, L190, S200 and the "
                         "Docking Station A500. Exercise 4.1, step 1, expects all five — A500 "
                         "at 249.99 is the one people forget."),
                      tp("XBAD",
                         "Legacy Cable Pack stores price as the string \"49.99\". Numeric "
                         "comparisons only match values of a comparable type, so XBAD never "
                         "appears in a Decimal128 range."),
                      tp("$in",
                         "category $in LAPTOP and BOOK counts 5: three laptops and two books. "
                         "It is an OR on one field. The five reviews rated 4 or 5 match "
                         "$gte: 4; the 3-star P1001 review does not."),
                      tp("$nin",
                         "Leaving out laptops and shoes keeps seven products: two books and "
                         "five accessories, including XBAD. $nin and $ne also match documents "
                         "that do not have the field at all. Add $exists: true when the field "
                         "must be present.")]),
        F.diagram(img(14), "Logical Operators: $and and $or",
                  "Both conditions true — or at least one.",
                  items=[("AND", "Commas mean AND; write $and only when a field or operator "
                                 "repeats."),
                         ("$or", "Any condition true. Same field? Use $in instead."),
                         {"code": "db.orders.find({ $or: [\n"
                                  "  { paymentStatus: \"PENDING\" },\n"
                                  "  { fulfillmentStatus:\n"
                                  "      \"PROCESSING\" } ] })\n"
                                  "// O5001 O6202 O6302 O6401 O6499",
                          "label": "Two different fields: $or", "size": 11}],
                  takeaway="Write AND with commas, OR with $or across fields, and $in when the "
                           "alternatives share one field.",
                  notes=dn(14)),
        S[50],
        F.diagram(img(16), "The $not and $nor Operators",
                  "Negate one expression — or reject every listed condition.",
                  items=[("$not", "Wraps an operator: { price: { $not: { $gt: … } } }. Missing "
                                  "or non-numeric prices pass too."),
                         ("$nor", "Keeps documents that fail every listed condition."),
                         ("Prefer $ne", "For a simple not-equal, $ne reads better than $not."),
                         {"callout": ("On training_store",
                                      "$nor: [{ category: \"BOOK\" }, { active: false }] keeps "
                                      "10 of 13 products.")}],
                  takeaway="Negations over-match easily: $not, $nor, $ne and $nin all keep "
                           "documents where the field is missing.",
                  notes=dn(16)),
        F.diagram(img(17), "Field Existence, BSON Type and Null",
                  "Missing, explicit null and the wrong type are three different questions.",
                  items=[("{ field: null }", "Explicit null or missing: C204 and C515."),
                         ("$type: \"null\"", "Explicit null only: C204's phone."),
                         ("$exists: false", "Missing only: C515 has no phone field."),
                         {"code": "db.products.find(\n"
                                  "  { price: { $type:\n"
                                  "    \"string\" } },\n"
                                  "  { _id: 0, sku: 1 })\n"
                                  "// { sku: \"XBAD\" }",
                          "label": "Find the planted type error", "size": 11}],
                  takeaway="Ask exactly what you mean: $exists for presence, $type for the BSON "
                           "type, null for null-or-missing.",
                  notes=dn(17)),
        F.code("Regular Expressions and Date Ranges",
               "Match text by pattern; match time with a start and an end.",
               [{"label": "Pattern match on a string", "kind": "info", "code":
                 "db.products.find(\n"
                 "  { name: { $regex: \"^MongoDB\" } },\n"
                 "  { _id: 0, name: 1 })\n"
                 "// MongoDB Fundamentals\n"
                 "\n"
                 "db.products.countDocuments({\n"
                 "  name: { $regex: \"wireless\",\n"
                 "          $options: \"i\" } })\n"
                 "// 2 — Keyboard and Mouse"},
                {"label": "Half-open date range", "kind": "good", "code":
                 "db.orders.find(\n"
                 "  { createdAt: {\n"
                 "    $gte: ISODate(\"2026-09-19T00:00:00Z\"),\n"
                 "    $lt:  ISODate(\"2026-09-20T00:00:00Z\")\n"
                 "  } },\n"
                 "  { _id: 0, orderNumber: 1 })\n"
                 "// O6402, O6499: every order\n"
                 "// placed on 19 September (UTC)"}],
               points=[("^ anchors", "Starts with: precise, and can use an index."),
                       ("The i option", "Case-insensitive; unanchored patterns scan every "
                                        "value."),
                       ("Half-open range", "$gte the start, $lt the next day: no time-of-day "
                                           "gaps.")],
               takeaway="Anchor regular expressions when you can, and query dates from an "
                        "inclusive start to an exclusive end.",
               notes=[tp("Anchored pattern",
                         "^MongoDB means the name starts with MongoDB. Only MongoDB "
                         "Fundamentals, B300, matches. An anchored, case-sensitive prefix can "
                         "use an index on the field."),
                      tp("Case-insensitive search",
                         "\"wireless\" with the i option matches Wireless Keyboard and Wireless "
                         "Mouse. It looks anywhere in every name, so on a large collection it "
                         "can be expensive. Module 6 covers index design."),
                      tp("Half-open date range",
                         "createdAt holds a Date with a time. Start inclusive at midnight on "
                         "19 September and end exclusive at midnight on 20 September. That "
                         "returns O6402 at 09:15 and O6499 at 19:00."),
                      tp("The common mistake",
                         "Writing $lte: ISODate(\"2026-09-19\") as the end means midnight at the "
                         "start of the day, so both orders would be missed. The guide's date "
                         "example uses an orderedAt field; training_store's field is "
                         "createdAt.")]),
        F.exercise("Exercise: Turn a Business Question into a Filter",
                   "From a merchandising request to a working query.",
                   scenario="Merchandising asks: which active products are on clearance or "
                            "premium? They want the SKU and name only.",
                   scenario_code="db.products.find(\n"
                                 "  { /* your filter */ },\n"
                                 "  { /* your projection */ }\n"
                                 ")",
                   tasks=["Choose the fields and operators",
                          "Write the filter and the projection",
                          "Predict the SKUs before you run it",
                          "Explain why L190 is not in the result"],
                   expected=["active: true plus tags: { $in: [ … ] }",
                             "{ _id: 0, sku: 1, name: 1 }",
                             "L110, S290 and A500",
                             "L190 is clearance but inactive"],
                   minutes=10,
                   takeaway="Translate each phrase of the request into one condition — then check "
                            "the result against the data.",
                   notes=[tp("How to run it",
                             "Pairs, five minutes. Ask one pair to type their query on the "
                             "instructor screen."),
                          tp("The answer",
                             "db.products.find({ active: true, tags: { $in: [\"clearance\", "
                             "\"premium\"] } }, { _id: 0, sku: 1, name: 1 }). An $or with two tag "
                             "conditions is also correct; $in is shorter because both "
                             "alternatives use the same field."),
                          tp("The result",
                             "L110 Ultrabook and A500 Docking Station are premium; S290 Clearance "
                             "Shoe is clearance. This is Day 2 Lab 3, step 2."),
                          tp("L190",
                             "The Refurbished Laptop is tagged clearance, but active is false, "
                             "so the implicit AND removes it. That is exactly what the business "
                             "asked for.")]),

        # Part 3 ------------------------------------------------------------
        F.bridge(PARTS, 2, "Part 3: Nested Fields and Arrays",
                 "Query inside embedded documents and arrays.",
                 so_far=["Comparison and logical operators",
                         "Missing, null and type are different",
                         "Negations also match missing fields"],
                 question="How do we reach inside embedded documents and arrays — and match the "
                          "right element?",
                 covers=["Dot notation for embedded fields",
                         "Contains, exact match, $all and $size",
                         "$elemMatch on arrays of documents", "Practice: choose the array query"],
                 notes=[tp("Why this part",
                           "Module 3 embedded attributes, addresses and order items. Those are "
                           "the fields business questions ask about most."),
                        tp("What to watch",
                           "The O5001 order is built to show the difference between dot "
                           "notation on an array and $elemMatch. That difference is the most "
                           "common array bug in real code.")]),
        F.diagram(img(11), "Querying Nested Fields",
                  "Dot notation reaches inside embedded documents.",
                  items=[("Quote the path", "\"attributes.memoryGB\" — unquoted dots are a "
                                            "syntax error."),
                         ("Through arrays too", "\"addresses.city\" looks at every address in "
                                                "the array."),
                         {"code": "db.customers.find(\n"
                                  "  { \"addresses.city\": { $in:\n"
                                  "    [\"Toronto\", \"Montreal\"] } },\n"
                                  "  { _id: 0, customerNumber: 1 })\n"
                                  "// C101, C412",
                          "label": "On training_store", "size": 11}],
                  takeaway="Dot notation reaches into embedded documents and arrays — quote the "
                           "path and match the stored value exactly.",
                  notes=dn(11)),
        F.diagram(img(20), "Exact Array Match vs $all vs $size",
                  "Contains a value, equals the array, contains all, or has N elements.",
                  items=[("Contains", "{ tags: \"wireless\" } — any element: P1001, A410."),
                         ("Exact array", "[\"database\", \"technology\"] → B300; reversed "
                                         "order finds nothing."),
                         ("$all", "All listed values, any order: [\"office\", \"premium\"] → "
                                  "A500."),
                         ("$size", "Exact length only: $size: 3 → L190. No \"at least\".")],
                  takeaway="Match one element by value and several with $all; use exact arrays or "
                           "$size only when order or length matters.",
                  notes=dn(20)),
        F.diagram(img(22), "Querying Arrays of Documents with $elemMatch",
                  "Every condition must be met by the same array element.",
                  items=[("Without $elemMatch", "\"items.sku\" and \"items.quantity\" can be met "
                                                "by different items."),
                         ("The O5001 trap", "L100 × 1 plus A410 × 2 — dot notation matches it; "
                                            "$elemMatch doesn't."),
                         {"code": "db.orders.find({ items: {\n"
                                  "  $elemMatch: {\n"
                                  "    sku: \"L100\",\n"
                                  "    quantity: { $gte: 2 }\n"
                                  "  } } })\n"
                                  "// only O6401 (L100 × 2)",
                          "label": "Same item, both conditions", "size": 11}],
                  takeaway="When several conditions must hold for the same array element, wrap "
                           "them in $elemMatch.",
                  notes=dn(22)),
        F.exercise("Exercise: Choose the Right Array Query",
                   "Four requests, four different array tools.",
                   scenario="The store team sends four requests. Pick containment, dot "
                            "notation, $all or $elemMatch for each.",
                   scenario_code="A  Shoes available in size 9\n"
                                 "B  Orders with L100 × 2 or more\n"
                                 "C  Customers in Toronto or Montreal\n"
                                 "D  Products tagged office AND premium",
                   tasks=["Choose the operator for each request",
                          "Write each filter",
                          "Predict the matching documents",
                          "Say which one dot notation gets wrong"],
                   expected=["A  \"attributes.sizes\": 9 → S200, S210, S290",
                             "B  items $elemMatch → O6401",
                             "C  \"addresses.city\" $in → C101, C412",
                             "D  tags $all → A500",
                             "B: dot notation adds O5001"],
                   minutes=10,
                   takeaway="Choose the array tool from the question: one value, all values, a "
                            "nested path, or one element meeting several conditions.",
                   notes=[tp("How to run it",
                             "Individually for five minutes, then compare in pairs. Run the "
                             "four answers on the instructor screen."),
                          tp("A and C",
                             "Containment through a dotted path: { \"attributes.sizes\": 9 } "
                             "returns the three shoes. { \"addresses.city\": { $in: [\"Toronto\", "
                             "\"Montreal\"] } } returns Aisha Khan, C101, and Jordan Lee, C412."),
                          tp("B",
                             "{ items: { $elemMatch: { sku: \"L100\", quantity: { $gte: 2 } } } } "
                             "returns only O6401, Luis Romero's order for two laptops. The dot-"
                             "notation version also returns O5001."),
                          tp("D",
                             "{ tags: { $all: [\"office\", \"premium\"] } } returns only A500, the "
                             "Docking Station. { tags: [\"office\", \"premium\"] } would be an exact "
                             "array match and depends on order.")]),

        # Part 4 ------------------------------------------------------------
        F.bridge(PARTS, 3, "Part 4: Inserts, Updates, Upserts and Replace",
                 "Change documents — and only the fields you mean.",
                 so_far=["Filters find exactly the right documents",
                         "Dot notation and $elemMatch reach inside",
                         "Every read can be counted first"],
                 question="How do we add and change documents without losing data we meant to "
                          "keep?",
                 covers=["insertOne() and insertMany()", "updateOne() and updateMany()",
                         "$set, $unset, $inc and $rename", "Array updates and positional $",
                         "replaceOne() versus $set", "Upserts with $setOnInsert",
                         "Reading write results"],
                 notes=[tp("The link",
                           "Every update and delete starts with a filter. Everything from Parts "
                           "1 to 3 now decides which documents a write touches."),
                        tp("Test data",
                           "Use the SKUs the labs reserve: DEMO-1, DEMO-REP, DEMO-BULK and "
                           "TEMP-100 for demos; A600 to A900 are created by the labs. Never "
                           "replace or delete L100.")]),
        F.diagram(img(28), "Inserting Documents",
                  "insertOne() or insertMany(); mongod adds _id when it is missing.",
                  items=[{"code": "db.products.insertOne({\n"
                                  "  sku: \"DEMO-1\", name: \"Demo Cable\",\n"
                                  "  category: \"ACCESSORY\",\n"
                                  "  price: Decimal128(\"9.99\"),\n"
                                  "  active: true })\n"
                                  "// acknowledged: true,\n"
                                  "// insertedId: ObjectId(…)",
                          "label": "Demo 4.5", "size": 11},
                         ("insertMany()", "Returns insertedIds, one per document."),
                         ("Unique sku", "A second DEMO-1 fails with E11000 duplicate key."),
                         {"callout": ("Verify", "findOne({ sku: \"DEMO-1\" }), then delete "
                                                "it.")}],
                  takeaway="Insert with real BSON types — Decimal128 for money, Date for time — "
                           "and read the document back to verify.",
                  notes=dn(28)),
        F.diagram(img(30), "Updating Documents",
                  "A filter, update operators and a write result.",
                  items=[("Three parts", "updateOne(filter, update, options): the filter picks, "
                                         "the operators change."),
                         ("One or many", "updateMany() changes every match — preview it with "
                                         "find() first."),
                         {"code": "db.products.updateOne(\n"
                                  "  { sku: \"L100\" },\n"
                                  "  { $set: { active: true } })\n"
                                  "// matchedCount: 1,\n"
                                  "// modifiedCount: 0",
                          "label": "Already true?", "size": 11},
                         {"callout": ("Why 0", "L100 is already active: found, nothing to "
                                               "change.")}],
                  takeaway="An update is a filter plus operators — the result says what was "
                           "found and what actually changed.",
                  notes=dn(30)),
        F.diagram(img(31), "$set, $unset, Numeric Operators and $rename",
                  "Four kinds of operator, one document, changed in place.",
                  items=[("$set / $unset", "Add or replace a field; remove one — A410's "
                                           "temporaryNote."),
                         ("$inc / $mul", "Change a number in place, atomically."),
                         ("$min / $max", "Change only if the new value is lower, or higher."),
                         ("$rename", "legacyName → catalogName on L190. Preview the filter "
                                     "first.")],
                  takeaway="Update operators change only the fields you name — the rest of the "
                           "document stays as it was.",
                  notes=dn(31)),
        F.code("Nested $set and a Guarded $inc",
               "Change one embedded field; decrement stock only when there is enough.",
               [{"label": "Set one nested field", "kind": "good", "code":
                 "db.products.updateOne(\n"
                 "  { sku: \"L100\" },\n"
                 "  { $set: {\n"
                 "    \"attributes.warrantyYears\": 2\n"
                 "  } })\n"
                 "// memoryGB, processor … kept"},
                {"label": "Decrement only if stock allows", "kind": "good", "code":
                 "// Lab 3 first sets stockQuantity: 18\n"
                 "db.products.updateOne(\n"
                 "  { sku: \"A410\",\n"
                 "    stockQuantity: { $gte: 2 } },\n"
                 "  { $inc: { stockQuantity: -2 },\n"
                 "    $currentDate: { updatedAt: true } })\n"
                 "// 18 → 16"}],
               points=[("Dotted path", "$set: { contact: { … } } would replace the object and "
                                       "lose phone."),
                       ("Atomic", "Check and change happen in one single-document write."),
                       {"callout": ("matchedCount: 0", "Not enough stock — or no such SKU.")}],
               takeaway="Set nested fields by their dotted path, and put the business rule in "
                        "the filter so check and change are one write.",
               notes=[tp("Nested $set",
                         "Setting \"attributes.warrantyYears\" adds one field inside attributes. "
                         "processor, memoryGB, storageGB and screenSizeInches stay."),
                      tp("The trap it avoids",
                         "$set: { attributes: { warrantyYears: 2 } } would replace the whole "
                         "attributes object. Exercise 4.4 shows the same mistake with "
                         "contact: C101 would lose her phone."),
                      tp("Guarded $inc",
                         "Products have no stock field on a fresh load, so Lab 3 first sets "
                         "stockQuantity to 18 on A410. The update matches only while at least "
                         "2 remain, and $inc subtracts 2: 18 becomes 16."),
                      tp("Why it is safe",
                         "The condition and the change are one single-document write, which "
                         "MongoDB applies atomically. Two buyers cannot both take the last "
                         "unit. Reading the value into the application and writing it back "
                         "would allow that race."),
                      tp("No stock field yet",
                         "On a fresh load L100 has no stockQuantity either. $inc on a missing "
                         "field creates it with the increment, so $inc: { stockQuantity: 5 } "
                         "gives 5. That is why Lab 3 sets A410's stockQuantity to 18 before "
                         "the guarded decrement.")]),
        F.diagram(img(33), "Array Update Operators",
                  "$push, $addToSet, $pull and $pop change arrays without rewriting them.",
                  items=[("$push", "Appends — run it twice and the value is there twice."),
                         ("$addToSet", "Adds only if absent; $each adds several."),
                         ("$pull / $pop", "Remove by value or condition / from one end."),
                         {"code": "db.products.updateOne(\n"
                                  "  { sku: \"A410\" },\n"
                                  "  { $addToSet: { tags: { $each:\n"
                                  "    [\"featured\", \"office\", \"wireless\"]\n"
                                  "  } } })",
                          "label": "Lab 3: wireless stays once", "size": 11}],
                  takeaway="Use $addToSet when duplicates are wrong, $push when repeats and order "
                           "matter, and $pull to remove by value.",
                  notes=dn(33)),
        F.diagram(img(35), "Positional Array Updates",
                  "$ updates the element the filter matched.",
                  items=[("$", "The first element the filter matched: items.$.quantity."),
                         ("$[]", "Every element: items.$[].reviewed."),
                         ("$[name] + arrayFilters", "Only the elements that pass a "
                                                    "condition."),
                         {"code": "db.orders.updateOne(\n"
                                  "  { orderNumber: \"O5001\",\n"
                                  "    \"items.sku\": \"L100\" },\n"
                                  "  { $set: {\n"
                                  "    \"items.$.quantity\": 2 } })\n"
                                  "// only the L100 line",
                          "label": "On O5001", "size": 11}],
                  takeaway="Put the array condition in the filter and use $ for the matched "
                           "element — or $[] and arrayFilters for many.",
                  notes=dn(35)),
        F.diagram(img(36), "Replace vs $set",
                  "replaceOne() rewrites the document; $set changes named fields.",
                  items=[("replaceOne()", "A new body for the whole document; only _id "
                                          "survives."),
                         ("$set", "Changes the named fields; the rest stays."),
                         ("Practise on a copy", "Use a test SKU such as DEMO-REP — never "
                                                "L100."),
                         {"callout": ("Rule", "Replace only when you mean to rewrite every "
                                              "field.")}],
                  takeaway="replaceOne() rewrites the whole document; when only some fields "
                           "should change, use update operators.",
                  notes=dn(36)),
        F.diagram(img(37), "The Upsert Pattern",
                  "One command: update if found, insert if not.",
                  items=[{"code": "db.products.updateOne(\n"
                                  "  { sku: \"A700\" },\n"
                                  "  { $set: {\n"
                                  "      name: \"Portable Charger\",\n"
                                  "      updatedAt: new Date() },\n"
                                  "    $setOnInsert: {\n"
                                  "      createdAt: new Date() } },\n"
                                  "  { upsert: true })",
                          "label": "Exercise 4.3 (trimmed)", "size": 10},
                         ("First run", "No match: inserts A700; upsertedCount 1 and the new _id."),
                         ("Second run", "Matches: updatedAt changes, createdAt stays.")],
                  takeaway="An upsert updates when the filter matches and inserts when it "
                           "doesn't — $setOnInsert applies only to the insert.",
                  notes=dn(37)),
        F.diagram(img(42), "Understanding Write Results",
                  "Matched is not the same as modified.",
                  items=[("acknowledged", "The server accepted the write."),
                         ("matchedCount / modifiedCount", "Found / really changed; 1 and 0 "
                                                          "means already right."),
                         ("upsertedId / deletedCount", "The new _id of an upsert; documents "
                                                       "removed."),
                         {"callout": ("On training_store",
                                      "updateMany({}, { $pull: { tags: \"discontinued\" } }) "
                                      "matches 13, modifies 1.")}],
                  takeaway="Read every field of the write result — matched, modified, upserted "
                           "and deleted each answer a different question.",
                  notes=dn(42)),

        # Part 5 ------------------------------------------------------------
        F.bridge(PARTS, 4, "Part 5: Deletes, Bulk Writes and Safe Practice",
                 "Remove data safely, batch writes, and fix queries that go wrong.",
                 so_far=["Insert with real BSON types",
                         "Update operators change only named fields",
                         "Upserts insert when nothing matches",
                         "Write results show what really changed"],
                 question="How do we delete and batch writes safely — and debug a query that "
                          "returns the wrong thing?",
                 covers=["deleteOne() and deleteMany()", "Preview, count, then delete",
                         "bulkWrite(): many writes, one result",
                         "Troubleshooting an empty result", "Common mistakes and safe habits",
                         "Module 4 at a glance"],
                 notes=[tp("Why this part",
                           "A delete cannot be undone from the shell. The habits in this part "
                           "protect real data."),
                        tp("Outcome",
                           "By the end, learners follow one routine for every risky write: "
                           "preview, count, write, verify.")]),
        F.diagram(img(38), "Deleting Documents Safely",
                  "Count, preview, check — then delete the verified set.",
                  items=[{"code": "const filter =\n"
                                  "  { sku: \"TEMP-100\" }\n"
                                  "db.products.find(filter)\n"
                                  "db.products\n"
                                  "  .countDocuments(filter)\n"
                                  "// 1\n"
                                  "db.products.deleteOne(filter)\n"
                                  "// deletedCount: 1",
                          "label": "Demo 4.9", "size": 11},
                         ("deleteOne / deleteMany", "The first match, or every match."),
                         {"callout": ("Never", "deleteMany({}) removes every document.")}],
                  takeaway="Delete with exactly the filter you previewed and counted — then "
                           "compare deletedCount with that count.",
                  notes=dn(38)),
        F.diagram(img(41), "Bulk Write Operations",
                  "Several writes in one request, one combined result.",
                  items=[{"code": "db.products.bulkWrite([\n"
                                  "  { insertOne: { document:\n"
                                  "    { sku: \"DEMO-BULK\" } } },\n"
                                  "  { updateOne: {\n"
                                  "    filter: { sku: \"DEMO-BULK\" },\n"
                                  "    update: { $set:\n"
                                  "      { active: false } } } },\n"
                                  "  { deleteOne: { filter:\n"
                                  "    { sku: \"TEMP-100\" } } } ])",
                          "label": "Demo 4.10 (trimmed)", "size": 10},
                         ("Result", "insertedCount 1, matchedCount 1, modifiedCount 1, "
                                    "deletedCount 0."),
                         ("Ordered by default", "Stops at the first error; ordered: false "
                                                "carries on.")],
                  takeaway="bulkWrite() sends many writes in one round trip — then read each "
                           "count in the combined result.",
                  notes=dn(41)),
        F.diagram(img(46), "Query Troubleshooting Workflow",
                  "Reproduce, confirm, sample, fix, test small, confirm.",
                  items=[("Reproduce", "find({ price: \"49.99\" }) returns only XBAD — the "
                                       "broken one."),
                         ("Compare", "findOne({ sku: \"P1001\" }) shows a Decimal128 "
                                     "price."),
                         ("Fix the type", "{ price: Decimal128(\"49.99\") } → P1001 only."),
                         {"callout": ("Rule", "Test the smallest query first, then add one "
                                              "condition.")}],
                  takeaway="When a query returns nothing — or the wrong thing — compare it field "
                           "by field with a real document.",
                  notes=dn(46)),
        F.myths("Common Query Mistakes and Safe-Write Habits",
                "Seven classic query errors — and the habits that prevent write disasters.",
                [("{ Category: \"LAPTOP\" }",
                  "Field names are case-sensitive: category"),
                 ("{ price: { $gt: \"100.00\" } }",
                  "Compare money as Decimal128(\"100.00\")"),
                 ("{ attributes.memoryGB: 16 }",
                  "Quote dotted paths: \"attributes.memoryGB\""),
                 ("{ $gt: { price: … } }",
                  "Operator inside the field: { price: { $gt: … } }"),
                 ("updateOne(f, { featured: true })",
                  "Use an operator: { $set: { featured: true } }")],
                ["updateMany({}) or deleteMany({})",
                 "$set on a parent object instead of one path",
                 "$push where values must be unique",
                 "skip() and limit() without sort()",
                 "Writing without reading the result"],
                remember=("Remember", "Preview, count, write, then verify."),
                takeaway="Most query bugs are a wrong name, case, type or path — most write "
                         "disasters are an unchecked filter.",
                notes=[tp("Why this slide",
                          "These are seven classic query errors and the write mistakes from "
                          "Exercise 4.4, gathered in one place before the checks."),
                       tp("Query mistakes",
                          "Category with a capital C matches nothing. A string \"100.00\" "
                          "compares only against strings: on training_store it returns XBAD "
                          "alone, because \"49.99\" sorts after \"100.00\" as text. An unquoted "
                          "dotted path is a JavaScript syntax error. An operator must sit "
                          "inside its field."),
                       tp("Update without an operator",
                          "updateOne(filter, { featured: true }) is rejected: the update "
                          "document must use operators such as $set. Replacing a document is "
                          "what replaceOne() is for. Mixing inclusion and exclusion in a "
                          "projection is the seventh error."),
                       tp("Anti-patterns",
                          "An empty filter on updateMany or deleteMany touches every "
                          "document. $set on a parent object drops its other fields. $push "
                          "creates duplicates. Paging without a sort gives unstable pages. And "
                          "a write you never check is a write you cannot trust.")]),
        F.diagram(img(47), "Module 4 at a Glance",
                  "Build a precise filter, send it, execute, read the result, verify.",
                  takeaway="Every query and every write follows one loop: precise filter, "
                           "execute, read the result, verify.",
                  notes=dn(47)),

        # Wrap-up ------------------------------------------------------------
        F.knowledge("Knowledge Check", "Answer in your own words — then compare with a partner.",
                    ["findOne() or find() — what does each return?",
                     "What does the filter {} match?",
                     "How do you query a nested field?",
                     "When is $elemMatch required?",
                     "What is the projection mixing rule?",
                     "$push or $addToSet — what is the difference?",
                     "updateOne() with $set, or replaceOne()?",
                     "What does upsert: true do?",
                     "matchedCount 1, modifiedCount 0 — meaning?",
                     "Why does XBAD miss every price range?"],
                    notes=[tp("1. findOne() and find()",
                              "findOne() returns one document or null. find() returns a cursor "
                              "over every match."),
                           tp("2. The empty filter",
                              "{} matches every document in the collection — 13 products. That "
                              "is why it is dangerous in updateMany and deleteMany."),
                           tp("3. Nested fields",
                              "With a quoted dotted path, such as \"attributes.memoryGB\" or "
                              "\"contact.email\"."),
                           tp("4. $elemMatch",
                              "When two or more conditions must be true for the same array "
                              "element, as in the O5001 example."),
                           tp("5. Projection",
                              "Use inclusion or exclusion, not both. _id is the only field you "
                              "may exclude in an inclusion projection."),
                           tp("6. $push and $addToSet",
                              "$push always appends, so repeats are possible. $addToSet adds a "
                              "value only if it is not already there."),
                           tp("7. $set or replaceOne()",
                              "$set changes the named fields and keeps the rest. replaceOne() "
                              "replaces everything except _id."),
                           tp("8. Upsert",
                              "It updates the matching document, or inserts a new one built "
                              "from the filter and the update when nothing matches."),
                           tp("9. Matched but not modified",
                              "The document was found but already had the requested values, so "
                              "nothing changed."),
                           tp("10. XBAD",
                              "Its price is the string \"49.99\". Numeric comparisons with "
                              "Decimal128 only match numeric values, so it is skipped.")]),
        F.exercise("Exercise 4.1 — Build Comparison Filters",
                   "Module 4 checkpoint A: ranges and lists with Decimal128.",
                   kind="OFFICIAL CHECKPOINT A", minutes=15,
                   worksheet="labs/day-02/exercises/exercise-4.1-build-comparison-filters.md",
                   scenario="Money in training_store is Decimal128 — except XBAD, planted with a "
                            "string price.",
                   scenario_code="1  products: price > 100\n"
                                 "2  products: 50 ≤ price ≤ 500\n"
                                 "3  orders:   total > 1000\n"
                                 "4  reviews:  rating ≥ 4\n"
                                 "5  products: not LAPTOP or SHOE",
                   tasks=["Write 1 and 2 with Decimal128 values",
                          "Write 3 and 4 on orders and reviews",
                          "Write 5 with $nin",
                          "Explain why XBAD never appears in 1–2"],
                   expected=["1  L100, L110, L190, S200, A500",
                             "2  L190, S200, S210, B300, A500",
                             "3  Six orders, O5001 to O6401",
                             "4  Five of the six reviews",
                             "5  Seven products, XBAD included"],
                   expected_title="Solution (after debrief)",
                   takeaway="Compare values of the stored BSON type — Decimal128 for money — and "
                            "check every result against the data.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 4.1, the first Module 4 checkpoint. "
                             "The worksheet is "
                             "labs/day-02/exercises/exercise-4.1-build-comparison-filters.md; "
                             "the answer key is in its solution folder. Fifteen minutes in "
                             "mongosh on a fresh load."),
                          tp("Solutions 1 and 2",
                             "Above 100: L100, L110, L190, S200 and A500 — people often stop at "
                             "the laptops and S200, but A500 at 249.99 also matches. Between 50 "
                             "and 500: L190 499.99, S200 129.99, S210 89.99, B300 59.99 and A500 "
                             "249.99. A400, at 24.99, is below the range and must not "
                             "appear."),
                          tp("Solutions 3 to 5",
                             "Orders over 1000: O5001, O6101, O6202, O6301, O6304 and O6401. "
                             "Five reviews have a rating of 4 or more. $nin LAPTOP and SHOE "
                             "leaves two books and five accessories, including XBAD."),
                          tp("What to listen for",
                             "Everyone should use Decimal128(\"100.00\"), not 100 or \"100\", and "
                             "explain that XBAD is skipped because its price is a string.")]),
        F.exercise("Exercise 4.2 — Query Arrays of Documents",
                   "Module 4 checkpoint B: prove the O5001 $elemMatch trap.",
                   kind="OFFICIAL CHECKPOINT B", minutes=15,
                   worksheet="labs/day-02/exercises/exercise-4.2-query-arrays-of-documents.md",
                   scenario="O5001 holds L100 × 1 and A410 × 2. Show why dot notation is not "
                            "enough.",
                   scenario_code="1  \"items.sku\": \"L100\"\n"
                                 "2  \"items.quantity\": { $gte: 2 }\n"
                                 "3  $elemMatch: L100 and qty ≥ 2\n"
                                 "4  1 and 2 with dot notation\n"
                                 "5  addresses $elemMatch:\n"
                                 "   SHIPPING in Toronto",
                   tasks=["Run steps 1 and 2; list the orders",
                          "Run steps 3 and 4 side by side",
                          "Name the false positive and why",
                          "Query addresses with $elemMatch"],
                   expected=["1  O5001, O6101, O6301, O6401",
                             "2  Six orders",
                             "3  O6401 only",
                             "4  O5001 and O6401",
                             "5  C101"],
                   expected_title="Solution (after debrief)",
                   takeaway="Dot notation lets different elements satisfy different conditions; "
                            "$elemMatch makes one element satisfy them all.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 4.2, the second checkpoint. The "
                             "worksheet is "
                             "labs/day-02/exercises/exercise-4.2-query-arrays-of-documents.md."),
                          tp("Steps 1 and 2",
                             "Four orders contain L100: O5001, O6101, O6301 and O6401. O6301, "
                             "a laptop and a USB Hub, is the one people miss. Six orders have some item with quantity 2 or more: O5001, "
                             "O6103, O6201, O6302, O6305 and O6401."),
                          tp("Steps 3 and 4",
                             "$elemMatch returns only O6401, two laptops. Dot notation also "
                             "returns O5001, because its L100 line has quantity 1 and its A410 "
                             "line has quantity 2 — different elements."),
                          tp("Step 5",
                             "addresses with $elemMatch type SHIPPING and city Toronto returns "
                             "C101, Aisha Khan. Type values are uppercase in this dataset.")]),
        F.exercise("Exercise 4.3 — Perform an Upsert",
                   "Module 4 checkpoint C: the same upsert, run twice.",
                   kind="OFFICIAL CHECKPOINT C", minutes=10,
                   worksheet="labs/day-02/exercises/exercise-4.3-perform-an-upsert.md",
                   scenario="A700 is not in the fresh dataset. Run one upsert twice and compare "
                            "the write results.",
                   scenario_code="db.products.updateOne(\n"
                                 "  { sku: \"A700\" },\n"
                                 "  { $set: { name, category,\n"
                                 "      price, active, updatedAt },\n"
                                 "    $setOnInsert: { createdAt,\n"
                                 "      stockQuantity: 25 } },\n"
                                 "  { upsert: true })",
                   tasks=["Run the upsert; read the result",
                          "findOne A700; note createdAt",
                          "Run the same upsert again",
                          "Compare both results in two bullets"],
                   expected=["Run 1: matched 0, upsertedCount 1",
                             "Run 2: matched 1, modified 1",
                             "createdAt unchanged after run 2",
                             "The filter uses the unique sku"],
                   expected_title="Solution (after debrief)",
                   takeaway="Upsert on a unique field and put creation-only fields in "
                            "$setOnInsert, so a rerun updates instead of duplicating.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 4.3, the third checkpoint. The "
                             "worksheet is labs/day-02/exercises/exercise-4.3-perform-an-upsert.md. "
                             "The full command sets name Portable Charger, category ACCESSORY, price "
                             "Decimal128 39.99, active true and updatedAt."),
                          tp("First run",
                             "Nothing matches sku A700, so MongoDB inserts a document from the "
                             "filter and both operators. The result shows matchedCount 0, "
                             "modifiedCount 0, upsertedCount 1 and the new _id. mongosh prints "
                             "that _id as insertedId; drivers call it upsertedId."),
                          tp("Second run",
                             "Now A700 matches. matchedCount is 1, and modifiedCount is 1 "
                             "because updatedAt gets a new date. upsertedCount is 0. createdAt "
                             "and stockQuantity keep their first values."),
                          tp("Why the unique field",
                             "sku has a unique index. Upserting on a field that isn't unique "
                             "could match the wrong document or insert duplicates.")]),
        F.exercise("Exercise 4.4 — Correct Unsafe Operations",
                   "Module 4 checkpoint D: rewrite three dangerous writes. Don't run them.",
                   kind="OFFICIAL CHECKPOINT D", minutes=10,
                   worksheet="labs/day-02/exercises/exercise-4.4-correct-unsafe-operations"
                             ".md",
                   scenario="A teammate wants to run these. Rewrite each one instead.",
                   scenario_code="db.products.updateMany({},\n"
                                 "  { $set: { active: false } })\n"
                                 "db.orders.deleteMany({})\n"
                                 "db.customers.updateOne(\n"
                                 "  { customerNumber: \"C101\" },\n"
                                 "  { $set: { contact:\n"
                                 "    { email: \"new@example.com\" } } })",
                   tasks=["Name what each command would damage",
                          "Rewrite 1 with a precise filter",
                          "Rewrite 2 as find → count → delete",
                          "Rewrite 3 with a dotted path"],
                   expected=["1  All 13 products go inactive",
                             "Safer: { tags: \"discontinued\" }: 1",
                             "2  All 17 orders are deleted",
                             "3  C101 loses her phone",
                             "Use \"contact.email\" instead"],
                   expected_title="Solution (after debrief)",
                   takeaway="Name the blast radius before every write — an empty filter or a "
                            "replaced parent object is rarely what you mean.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 4.4, the last checkpoint. The "
                             "worksheet is "
                             "labs/day-02/exercises/exercise-4.4-correct-unsafe-operations.md. "
                             "Nobody runs the unsafe commands."),
                          tp("Command 1",
                             "The empty filter makes all 13 products inactive. Safer: preview "
                             "{ tags: \"discontinued\" }, count it — 1, L190 — then run "
                             "updateMany with that filter."),
                          tp("Command 2",
                             "deleteMany({}) removes all 17 orders. Never use an empty delete "
                             "filter. Filter on the test orderNumber values, then find, "
                             "countDocuments and deleteMany with the same filter."),
                          tp("Command 3",
                             "$set on contact replaces the whole object, so C101's phone, "
                             "+1-555-0100, is lost. $set: { \"contact.email\": \"new@example.com\" } "
                             "changes only the email.")]),
        F.exercise("Lab 3 — Complex Queries and Updates",
                   "Day 2 hands-on: filters, arrays and guarded writes on training_store.",
                   kind="OFFICIAL LAB", minutes=75,
                   worksheet="labs/day-02/lab3/LAB-3-GUIDE.md",
                   scenario="Reload first. Steps 1–7 read, steps 8–12 write and verify, "
                            "step 13 is the challenge.",
                   scenario_code="# In PowerShell, from the repo root\n"
                                 "mongosh \"mongodb://localhost:27017\" `\n"
                                 "  .\\datasets\\training_store\\load.js",
                   tasks=["1–4 Filters, ranges and $nin",
                          "5–7 Cities, $elemMatch, PROCESSING",
                          "8–9 Guarded $inc, $addToSet on A410",
                          "10–12 $pull, ship O6202, $rename",
                          "13 Challenge: one precise filter"],
                   expected=["1  A410, A400, P1001",
                             "6  O5001, O6201, O6305",
                             "8  A410 stock 18 → 16",
                             "11 Second ship matches 0",
                             "13 A410, P1001, B310, B300"],
                   expected_title="Expected results",
                   takeaway="Lab 3 puts the whole module together: precise filters first, then "
                            "writes guarded by the filter and verified by the result.",
                   notes=[tp("Official lab",
                             "This is Day 2 Lab 3, labs/day-02/lab3/LAB-3-GUIDE.md, about 60 to "
                             "75 minutes. The expected output for every step is in "
                             "labs/day-02/lab3/solution/LAB-3-SOLUTION.md, for instructors."),
                          tp("Before you start",
                             "Reload load.js from the repository root in PowerShell, not inside "
                             "mongosh, then use training_store. The four checkpoints changed "
                             "data — A700 exists after Exercise 4.3 — so a fresh load keeps the "
                             "counts at 13 products, 6 customers, 17 orders and 6 reviews."),
                          tp("Steps 1 to 7: reads",
                             "Step 1 returns A410, A400 and P1001; XBAD's string price keeps it "
                             "out. Step 2 returns L110, S290 and A500 but not the inactive L190. "
                             "Step 6's $elemMatch — quantity 2 or more and unitPrice below 50 on "
                             "the same item — matches O5001, O6201 and O6305, not O6302 or "
                             "O6401. Step 7 uses fulfillmentStatus: O6401, O6302 and O6202."),
                          tp("Steps 8 to 12: writes",
                             "A410 has no stock field, so step 8 sets stockQuantity to 18 and "
                             "the guarded $inc takes it to 16. Step 9's $addToSet keeps wireless "
                             "once. Step 10 matches 13 products and modifies 1, L190. Step 11 "
                             "ships O6202; the rerun matches 0. Step 12 renames reviewText to "
                             "body on a throwaway review."),
                          tp("Step 13 and the debrief",
                             "The challenge returns A410, P1001, B310 and B300, sorted by "
                             "category then price. Ask who used $in versus $or, and who read "
                             "matchedCount before trusting a write.")]),
        F.wrapup("Module 4 Summary and What's Next",
                 "From precise filters to safe, verified writes.",
                 can=["Read with find(), findOne() and precise filters",
                      "Project, sort, page, count and list distinct values",
                      "Combine comparison, logical and element operators",
                      "Query nested fields and arrays with $elemMatch",
                      "Insert, update, upsert and replace documents",
                      "Delete safely and read every write result"],
                 next_title="Next: Module 5 — The Aggregation Framework",
                 questions=["How does a filter become a $match stage?",
                            "How does $group total the orders?",
                            "How do stages chain into a pipeline?"],
                 bring=("Bring along", "Your Lab 3 queries — and reload load.js so the counts "
                                       "start fresh."),
                 takeaway="Module 5 reuses today's filters and projections as the first stages of "
                          "an aggregation pipeline.",
                 notes=[tp("Recap",
                           "We read documents with filters, shaped results with projection, "
                           "sort and limit, combined operators, queried nested fields and "
                           "arrays, then inserted, updated, upserted, replaced and deleted — "
                           "checking every write result."),
                        tp("Day 2 Lab 3",
                           "The lab, labs/day-02/lab3/LAB-3-GUIDE.md, practises all of it on "
                           "training_store: 13 steps ending in a challenge query that returns "
                           "four SKUs — A410, P1001, B310 and B300."),
                        tp("Next module",
                           "Module 5 builds aggregation pipelines. $match uses the same filters "
                           "we wrote today and $project uses the same projections; $group and "
                           "accumulators are new."),
                        tp("Reload",
                           "Today's labs change the data. Reload load.js before Module 5 so "
                           "everyone's totals match.")]),
    ]
