#!/usr/bin/env python3
"""Slide order for the Module 5 deck: from one pipeline to a full sales report.

Every concept diagram is merged with the slide that explains it (diagram plus the
points only that slide adds), so no idea appears twice. Part openers, pipelines
run on the training_store sample database with their real results, in-flow
practice exercises, a knowledge check, the four official exercises 5.1-5.4
(labs/day-02/exercises), Day 2 Lab 4 (labs/day-02/lab4/LAB-4-GUIDE.md) and a
hand-off to Module 6 connect the ideas.

Field names follow datasets/training_store/load.js: orders have paymentStatus
and fulfillmentStatus (no single status field), items hold quantity and
unitPrice (no lineTotal), customers have name.first / name.last, and dates are
createdAt. Where a guide or diagram disagrees, the slide follows the data and
the notes say why.
"""
from __future__ import annotations

from pptx.enum.text import MSO_ANCHOR, PP_ALIGN

import mdb_deck_kit as K
import mdb_diagram_slides as DS
import mdb_flow_slides as F
import mdb_glossary as G
import mdb_visuals as V
from mdb_flow_slides import tp
from mdb_visuals import (
    DARK_GRAY, GREEN, LEFT, LIGHT_GRAY, NAVY, ORANGE, PURPLE, RED, RIGHT, TEAL, WHITE, WIDTH,
)

PARTS = ["Part 1\nPipelines", "Part 2\nFilter and shape", "Part 3\nGroup",
         "Part 4\nArrays and joins", "Part 5\nReports", "Part 6\nPerformance"]


# ---------------------------------------------------------------------------
# Custom slides
# ---------------------------------------------------------------------------
def _fields(slide, y0, y1):
    lw = 7.30
    y = V.section(slide, LEFT, y0, lw, "training_store after a fresh load", icon="🛒",
                  fill=NAVY)
    collections = [("customers", "6 documents", NAVY), ("products", "13 documents", TEAL),
                   ("orders", "17 documents", PURPLE), ("reviews", "6 documents", GREEN)]
    cg = 0.14
    cw = (lw - 3 * cg) / 4
    for k, (name, count, fill) in enumerate(collections):
        V.box(slide, LEFT + k * (cw + cg), y + 0.02, cw, 0.70,
              [(name, {"size": 15}), (count, {"size": 12, "bold": False})],
              fill=fill, size=15, margin=0.04)
    y = V.section(slide, LEFT, y + 0.95, lw, "One order: the paths we aggregate", icon="🧾",
                  fill=PURPLE)
    V.code(slide, LEFT, y + 0.02, lw, y1 - y - 0.02,
           "{ orderNumber: \"O6301\",\n"
           "  customerId: ObjectId(\"…\"),    // → customers._id\n"
           "  items: [ { sku: \"L100\", name: \"Business Laptop\",\n"
           "             quantity: 1,\n"
           "             unitPrice: Decimal128(\"1299.99\") }, … ],\n"
           "  paymentStatus: \"PAID\",\n"
           "  fulfillmentStatus: \"SHIPPED\",\n"
           "  subtotal: …, tax: …, shippingFee: Decimal128(\"15.00\"),\n"
           "  total: Decimal128(\"1512.23\"),\n"
           "  createdAt: ISODate(\"2026-09-03T10:15:00Z\") }",
           size=13)

    rx = LEFT + lw + 0.40
    F.stack_items(slide, rx, y0, RIGHT - rx, y1 - y0, [
        {"checks": ["No status field: use paymentStatus and fulfillmentStatus",
                    "No lineTotal: compute quantity × unitPrice",
                    "shippingFee is missing on 6 orders",
                    "XBAD's price is the string \"49.99\"",
                    "O6499's customerId matches no customer"],
         "h": "Traps built into the data", "c": RED, "mark": "!", "size": 13},
        {"callout": ("Money", "Decimal128 — compare with Decimal128(\"1000.00\").")},
        ("Before Lab 4", "Count each collection and write down these paths before any "
                         "pipeline."),
    ])


def _stages(slide, y0, y1):
    labels = [
        [("training_store.orders", {"size": 14}), ("17 documents", {"size": 12, "bold": False})],
        [("$match", {"size": 15}), ("paymentStatus: \"PAID\" → 13", {"size": 12, "bold": False})],
        [("$group", {"size": 15}), ("by fulfillmentStatus → 4", {"size": 12, "bold": False})],
        [("$sort", {"size": 15}), ("revenue: -1 → 4 ranked", {"size": 12, "bold": False})],
    ]
    gap = 0.40
    bw = (WIDTH - 3 * gap) / 4
    V.hflow(slide, LEFT, y0, labels, box_w=bw, box_h=0.95, gap=gap,
            fills=[LIGHT_GRAY, PURPLE, TEAL, ORANGE], colors=[DARK_GRAY, WHITE, WHITE, WHITE],
            size=14, arrow_color=NAVY)

    lw = 6.30
    y = V.section(slide, LEFT, y0 + 1.25, lw, "The pipeline", icon="⚙️", fill=NAVY)
    V.code(slide, LEFT, y + 0.02, lw, 2.55,
           "db.orders.aggregate([\n"
           "  { $match: { paymentStatus: \"PAID\" } },\n"
           "  { $group: {\n"
           "      _id: \"$fulfillmentStatus\",\n"
           "      orders: { $sum: 1 },\n"
           "      revenue: { $sum: \"$total\" } } },\n"
           "  { $sort: { revenue: -1 } }\n"
           "])", size=13)

    rx = LEFT + lw + 0.40
    rw = RIGHT - rx
    y = V.section(slide, rx, y0 + 1.25, rw, "The result: 4 documents", icon="📊", fill=GREEN)
    V.table(slide, rx, y + 0.02, [2.20, 1.25, rw - 3.45], ["_id", "orders", "revenue"],
            [("SHIPPED", "6", "3809.48"), ("DELIVERED", "4", "2788.42"),
             ("PROCESSING", "2", "2448.77"), ("NEW", "1", "71.77")],
            row_h=0.44, size=14, first_col_bold=True)
    V.text(slide, rx, y + 2.30, rw, 0.40, "Check: 6 + 4 + 2 + 1 = 13 paid orders.", size=13,
           italic=True, color=DARK_GRAY)


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
        *G.intro("module05"),
        F.story("From Module 4 to Module 5",
                "find() reads what is stored — aggregate() computes what isn't.",
                gave_title="Module 4 gave us",
                gave=["find() filters with query operators",
                      "Projections pick the returned fields",
                      "Dotted paths reach nested fields",
                      "sort() and limit() rank results",
                      "Updates change stored documents"],
                now=("Now", "Answer questions find() can't: totals, rankings and joins."),
                path_title="Our path through Module 5",
                path=[("How a pipeline works; why order matters", "Part 1", NAVY),
                      ("Filter, reshape and compute fields", "Part 2", PURPLE),
                      ("Group and summarize with accumulators", "Part 3", TEAL),
                      ("Expand items; join customers", "Part 4", GREEN),
                      ("Dates, price bands and one report", "Part 5", ORANGE),
                      ("Stage order, cost and debugging", "Part 6", RED)],
                takeaway="Module 4's filters become the first stage of every pipeline in "
                         "Module 5.",
                notes=[tp("Bridge from Module 4",
                          "Module 4 taught the query language: filters with comparison and "
                          "logical operators, projections, dotted paths into nested fields "
                          "and arrays, sort and limit, and updates."),
                       tp("What changes now",
                          "find() can only return documents that are stored. "
                          "Questions like revenue per customer, the top five products or "
                          "orders with customer names need new documents computed from the "
                          "stored ones. That is aggregation."),
                       tp("Nothing is wasted",
                          "Every Module 4 filter works unchanged inside $match, and "
                          "projections return as $project."),
                       tp("Where this leads",
                          "The module ends in Day 2 Lab 4, one multi-stage pipeline. "
                          "Tomorrow, Module 6 makes these pipelines fast with indexes.")]),
        F.custom(_fields, "The Fields Every Pipeline Uses",
                 "The real paths in training_store — and the traps the data is built to "
                 "teach.",
                 takeaway="A pipeline is only as correct as its field paths — check them "
                          "against a real document first.",
                 notes=[tp("Reload first",
                           "Run datasets/training_store/load.js before class. "
                           "A fresh load has 6 customers, 13 products, 17 orders and 6 "
                           "reviews, with 13 paid orders. "
                           "Some lab guides say 12 products; the loader adds a 13th, XBAD, on "
                           "purpose."),
                        tp("The order document",
                           "Orders keep two status fields, paymentStatus and "
                           "fulfillmentStatus. "
                           "Each item stores sku, name, quantity and unitPrice. "
                           "Money is Decimal128 and createdAt is a Date. "
                           "customerId is a reference to the customer's _id."),
                        tp("Traps on purpose",
                           "Many generic examples use status: \"Shipped\" and "
                           "items.lineTotal. Neither exists here, so those pipelines return "
                           "nothing or zeros. "
                           "shippingFee is missing on O5001, O6201, O6202, O6304, O6402 and "
                           "O6499. "
                           "XBAD stores its price as a string, and O6499 points to a customer "
                           "that doesn't exist."),
                        tp("Before Lab 4",
                           "Lab 4 starts with exactly this check, its Step 0: reload, count "
                           "the collections, open one document of each kind and write down "
                           "the field paths.")]),

        # Part 1 ------------------------------------------------------------
        F.bridge(PARTS, 0, "Part 1: How a Pipeline Works",
                 "Documents in, stages in order, new documents out.",
                 so_far=["You know find(), projections and sort()",
                         "You know the training_store field paths"],
                 question="What does a pipeline do that find() can't — and why does the order "
                          "of its stages matter?",
                 covers=["Queries versus aggregation", "How documents flow through stages",
                         "One pipeline, stage by stage", "Why stage order matters"],
                 notes=[tp("Where we start",
                           "We begin with the model: what a pipeline is, and how documents "
                           "flow through it."),
                        tp("What this part answers",
                           "By the end of Part 1, learners can read a short pipeline and say "
                           "how many documents leave each stage, and what they look like.")]),
        F.diagram(img(3), "Operational Queries vs. Aggregation",
                  "find() returns stored documents; aggregate() computes new ones.",
                  items=[("find()", "Returns the stored documents that match — everyday CRUD "
                                    "reads."),
                         ("aggregate()", "Computes new documents: counts, totals, averages, "
                                         "rankings, joins."),
                         ("Our example", "find() lists Aisha's paid orders; aggregate() says "
                                         "they total 3418.62."),
                         {"callout": ("Rule of thumb",
                                      "Not stored in one document? Aggregate.")}],
                  takeaway="Use find() to retrieve documents and aggregate() to compute answers "
                           "from them.",
                  notes=dn(3)),
        F.diagram(img(6), "How Documents Move Through a Pipeline",
                  "An array of stages; each stage's output is the next stage's input.",
                  items=[{"code": "db.orders.aggregate([\n"
                                  "  { $match: { … } },\n"
                                  "  { $group: { … } },\n"
                                  "  { $sort:  { … } }\n"
                                  "])",
                          "label": "An array of stage documents", "size": 12},
                         ("A stream", "Stages run in array order; each sees only the last "
                                      "one's output."),
                         ("Count and shape change", "6 → 4 → 2: $match shrinks the stream, "
                                                    "$group reshapes it."),
                         {"callout": ("Read-only", "Stored orders never change.")}],
                  takeaway="A pipeline is a stream: each stage transforms the documents and "
                           "passes them on.",
                  notes=dn(6)),
        F.custom(_stages, "Demo: One Pipeline, Stage by Stage",
                 "Paid revenue by fulfillment status — run it one stage at a time.",
                 takeaway="Run each stage on its own first — the counts tell you whether it "
                          "did what you meant.",
                 notes=[tp("Demo 5.1",
                           "Type the pipeline in mongosh one stage at a time. "
                           "Run the $match alone first: 13 documents, the paid orders."),
                        tp("Add $group",
                           "Append $group. Seventeen orders became 13, and 13 become 4: one "
                           "per fulfillmentStatus. "
                           "orders counts with $sum: 1, and revenue adds total."),
                        tp("Add $sort",
                           "Append $sort on revenue, descending. "
                           "SHIPPED leads with six orders worth 3809.48, then DELIVERED "
                           "2788.42, PROCESSING 2448.77 and NEW 71.77."),
                        tp("Decimal128 output",
                           "mongosh prints revenue as Decimal128('3809.48'). "
                           "The slide shows the plain numbers."),
                        tp("Check the sum",
                           "Six plus four plus two plus one is 13. "
                           "If the counts don't add up to the $match count, something is "
                           "wrong.")]),
        F.diagram(img(9), "Stage Order Matters",
                  "Match then group is a report; group then match returns nothing.",
                  items=[("Match, then group", "Keep PAID orders, then total them: paid "
                                               "revenue per customer."),
                         ("Group, then match", "$group keeps only _id and totals — "
                                               "paymentStatus is gone."),
                         {"code": "{ $group: { _id: \"$customerId\",\n"
                                  "    spent: { $sum: \"$total\" } } },\n"
                                  "{ $match: { paymentStatus: \"PAID\" } }\n"
                                  "// → 0 documents",
                          "label": "Wrong order on training_store", "kind": "bad",
                          "size": 11}],
                  takeaway="Stage order is part of the question — filter on stored fields "
                           "before $group removes them.",
                  notes=dn(9)),

        # Part 2 ------------------------------------------------------------
        F.bridge(PARTS, 1, "Part 2: Filter and Shape",
                 "Choose the documents, then choose — or compute — their fields.",
                 so_far=["A pipeline is an ordered array of stages",
                         "Each stage sees only the previous output",
                         "Filter before $group removes fields"],
                 question="How do we keep only the documents we need, and give them the shape "
                          "the report needs?",
                 covers=["$match: filter the stream", "$match on real fields and dates",
                         "$project: include, exclude, rename", "Calculated fields and $set",
                         "$sort and $limit: top-N"],
                 notes=[tp("Connecting the parts",
                           "Part 1 showed the stream. Part 2 introduces the stages that "
                           "almost every pipeline uses: $match, $project, $set, $sort and "
                           "$limit."),
                        tp("Watch for",
                           "Real field names, Decimal128 money and missing fields. "
                           "They are where most first pipelines go wrong.")]),
        F.diagram(img(11), "The $match Stage",
                  "Keep only the documents that satisfy the filter.",
                  items=[{"code": "{ $match: {\n"
                                  "    paymentStatus: \"PAID\",\n"
                                  "    total: { $gte:\n"
                                  "      Decimal128(\"1000.00\") }\n"
                                  "} }",
                          "label": "Paid orders of 1000 or more", "size": 12},
                         ("Result", "4 orders: O6101, O6202, O6301 and O6304."),
                         ("Put it first", "Later stages then handle 4 documents, not 17."),
                         {"callout": ("Same language", "Every Module 4 filter works here.")}],
                  takeaway="$match filters with the find() query language — and belongs as "
                           "early as possible.",
                  notes=dn(11)),
        F.code("$match on Real training_store Fields",
               "Categories, a date range and a nested array path.",
               [{"label": "Active laptops and accessories", "kind": "info", "code":
                 "db.products.aggregate([\n"
                 "  { $match: {\n"
                 "      active: true,\n"
                 "      category: { $in:\n"
                 "        [\"LAPTOP\", \"ACCESSORY\"] }\n"
                 "  } }\n"
                 "])\n"
                 "// 7 products (XBAD is one)"},
                {"label": "Reviews written in August", "kind": "info", "code":
                 "db.reviews.aggregate([\n"
                 "  { $match: { createdAt: {\n"
                 "      $gte: ISODate(\"2026-08-01\"),\n"
                 "      $lt:  ISODate(\"2026-09-01\")\n"
                 "  } } }\n"
                 "])\n"
                 "// 3 reviews: L110, B300, P1001"},
                {"label": "Customers in Ontario or Quebec", "kind": "info", "code":
                 "db.customers.aggregate([\n"
                 "  { $match: {\n"
                 "      \"addresses.province\":\n"
                 "        { $in: [\"Ontario\", \"Quebec\"] }\n"
                 "  } }\n"
                 "])\n"
                 "// 3 customers: C101, C412, C515"}],
               points=[("Same operators", "$in, ranges and dotted paths behave exactly as in "
                                          "find()."),
                       ("Half-open dates", "$gte the first day, $lt the next month — no gap, "
                                           "no overlap."),
                       {"callout": ("Try it", "Run each filter and check the "
                                              "count.")}],
               takeaway="$match speaks the query language you already know — use the real "
                        "field paths and types.",
               notes=[tp("Categories",
                         "Active laptops and accessories: L100, L110, P1001, A400, A410, A500 "
                         "and XBAD. "
                         "L190 is a laptop but inactive, so it is filtered out."),
                      tp("Dates",
                         "The half-open range, $gte the first of August and $lt the first of "
                         "September, catches every August instant exactly once. "
                         "The August reviews are for L110, B300 and P1001."),
                      tp("Nested arrays",
                         "addresses is an array of documents. "
                         "\"addresses.province\" matches if any address is in Ontario or "
                         "Quebec: Aisha Khan (C101), Jordan Lee (C412) and Sam Okonkwo "
                         "(C515), who is inactive but still matches."),
                      tp("Try it",
                         "Have learners run these three filters, plus the paid and "
                         "high-value filter from the last slide, and check each count. "
                         "The high-value filter must use Decimal128, not a plain number "
                         "written as a string.")]),
        F.diagram(img(20), "$project: Include, Exclude, Rename",
                  "Decide exactly which fields leave the stage.",
                  items=[{"code": "db.products.aggregate([\n"
                                  "  { $project: { _id: 0,\n"
                                  "      productCode: \"$sku\",\n"
                                  "      name: 1, price: 1 } }\n"
                                  "])",
                          "label": "Rename sku, keep two fields", "size": 12},
                         ("1 or 0", "1 keeps a field, 0 drops it — never both, except _id."),
                         ("Rename", "productCode: \"$sku\" copies the value under a new "
                                    "name."),
                         {"callout": ("Output only", "Stored products are unchanged.")}],
                  takeaway="$project decides the output shape: keep, drop, rename — the "
                           "stored document stays the same.",
                  notes=dn(20)),
        F.diagram(img(25), "Calculated Fields",
                  "Expressions compute values that aren't stored.",
                  items=[{"code": "{ $set: { lineRevenue: {\n"
                                  "    $multiply: [\"$items.quantity\",\n"
                                  "                \"$items.unitPrice\"]\n"
                                  "} } }",
                          "label": "Line revenue (after $unwind)", "size": 12},
                         ("No lineTotal", "training_store stores quantity and unitPrice — "
                                          "compute the line."),
                         ("$project or $set", "$project keeps only listed fields; $set adds "
                                              "fields and keeps the rest.")],
                  takeaway="Compute what the report needs with expressions — $set for helper "
                           "fields, $project for the final shape.",
                  notes=dn(25)),
        F.code("Calculated Fields You Can Check",
               "Rebuild each order's total — and survive a missing shippingFee.",
               [{"label": "Pipeline", "kind": "info", "code":
                 "db.orders.aggregate([\n"
                 "  { $match: { orderNumber:\n"
                 "      { $in: [\"O6201\", \"O6301\"] } } },\n"
                 "  { $set: { shipping: { $ifNull:\n"
                 "      [\"$shippingFee\", Decimal128(\"0.00\")] } } },\n"
                 "  { $set: { checkTotal: { $add:\n"
                 "      [\"$subtotal\", \"$tax\", \"$shipping\"] } } },\n"
                 "  { $project: { _id: 0, orderNumber: 1,\n"
                 "      total: 1, shipping: 1, checkTotal: 1 } }\n"
                 "])"},
                {"label": "Result", "kind": "good", "code":
                 "{ orderNumber: \"O6201\",\n"
                 "  total: Decimal128(\"79.07\"),\n"
                 "  shipping: Decimal128(\"0.00\"),\n"
                 "  checkTotal: Decimal128(\"79.07\") }\n"
                 "{ orderNumber: \"O6301\",\n"
                 "  total: Decimal128(\"1512.23\"),\n"
                 "  shipping: Decimal128(\"15.00\"),\n"
                 "  checkTotal: Decimal128(\"1512.23\") }"}],
               points=[("$ifNull", "O6201 has no shippingFee, so 0.00 is used instead of "
                                   "null."),
                       ("$add", "subtotal + tax + shipping rebuilds the stored total."),
                       {"callout": ("Why check", "checkTotal ≠ total means bad data — or a "
                                                 "bad pipeline.")}],
               takeaway="Handle missing fields with $ifNull before calculating — one null "
                        "turns the whole result into null.",
               notes=[tp("The missing field",
                         "O6201 has no shippingFee at all. "
                         "$add with a missing value returns null, so without $ifNull, "
                         "checkTotal would be null for O6201."),
                      tp("$ifNull",
                         "$ifNull returns the first value that isn't null or missing, here "
                         "Decimal128 0.00. "
                         "Six orders have no shippingFee: O5001, O6201, O6202, O6304, O6402 "
                         "and O6499."),
                      tp("The check",
                         "For O6301, 1324.98 plus 172.25 plus 15.00 is 1512.23, the stored "
                         "total. For O6201, 69.97 plus 9.10 plus 0.00 is 79.07."),
                      tp("Field order",
                         "An inclusion $project keeps the input order, and $set appended "
                         "shipping and checkTotal at the end. "
                         "That is why total prints before them."),
                      tp("For fast finishers",
                         "Add the same shipping-safe total to every paid order, plus line "
                         "revenue, full names, an order-size class and a reporting month. "
                         "Each one returns in a later part of this module.")]),
        F.diagram(img(50), "$sort Before $limit",
                  "A top-N report sorts the whole stream, then keeps N.",
                  items=[{"code": "{ $match: {\n"
                                  "    paymentStatus: \"PAID\" } },\n"
                                  "{ $sort: { total: -1,\n"
                                  "           orderNumber: 1 } },\n"
                                  "{ $limit: 3 }",
                          "label": "Top three paid orders", "size": 12},
                         ("Result", "O6202 and O6304 tie at 2146.99; O6301 is third at "
                                    "1512.23."),
                         ("Tie-breaker", "orderNumber makes the order repeatable."),
                         ("$skip", "$sort → $skip → $limit pages through results.")],
                  takeaway="Every top-N report is $sort, then $limit — with a tie-breaker when "
                           "values can tie.",
                  notes=dn(50)),
        F.exercise("Exercise: Build a Shoe Price List",
                   "Filter, shape, sort and limit — then predict the output.",
                   scenario="Marketing wants the two most expensive active shoes: name and "
                            "price only, highest price first.\n\ntraining_store has three "
                            "shoes: S200, S210 and S290.",
                   tasks=["Choose the four stages and their order",
                          "Write the $match",
                          "Write the $project",
                          "Add $sort and $limit; predict the output"],
                   expected=["$match → $project → $sort → $limit",
                             "{ active: true, category: \"SHOE\" }",
                             "{ _id: 0, name: 1, price: 1 }",
                             "Running Shoe 129.99, then Trail Shoe 89.99"],
                   minutes=10,
                   takeaway="Filter first, shape the output, then sort before you limit.",
                   notes=[tp("How to run it",
                             "Pairs, five minutes to write it, then run it on the instructor "
                             "screen."),
                          tp("The stages",
                             "$match on active true and category SHOE, $project name and "
                             "price without _id, $sort price descending, $limit 2."),
                          tp("The answer",
                             "Running Shoe at 129.99, then Trail Shoe at 89.99. "
                             "The Clearance Shoe at 44.99 is third, so $limit drops it."),
                          tp("A variation",
                             "Ask what happens if $project comes before $match. "
                             "The projection removes category and active, so the $match then "
                             "finds nothing. "
                             "That is Part 1's lesson again.")]),

        # Part 3 ------------------------------------------------------------
        F.bridge(PARTS, 2, "Part 3: Group and Summarize",
                 "Many documents in, one summary per key out.",
                 so_far=["$match keeps the documents you need",
                         "$project and $set shape documents",
                         "Top-N is $sort, then $limit"],
                 question="How do we turn many documents into one summary per customer, "
                          "status or category?",
                 covers=["$group, _id and accumulators", "Products by category",
                         "Grouping by several fields", "What $group keeps — and loses",
                         "$count and $sortByCount"],
                 notes=[tp("Connecting the parts",
                           "Part 2 worked on one document at a time. "
                           "$group is different: it combines many documents into one."),
                        tp("Watch for",
                           "What _id means in the output, and which fields survive the "
                           "stage.")]),
        F.diagram(img(39), "$group: One Document per Key",
                  "_id is the grouping key; every other field is an accumulator.",
                  items=[("_id", "\"$customerId\" — one output per distinct value; null "
                                 "means one group."),
                         ("Accumulators", "$sum, $avg, $min, $max, $first, $last, $push, "
                                          "$addToSet."),
                         ("Count or total", "$sum: 1 counts documents; $sum: \"$total\" adds "
                                            "values."),
                         {"callout": ("Our data", "Aisha's 4 paid orders → spent 3418.62.")}],
                  takeaway="$group turns many documents into one per key — _id names the key, "
                           "accumulators compute the rest.",
                  notes=dn(39)),
        F.code("Products by Category",
               "Count, average, minimum and maximum price for active products.",
               [{"label": "Pipeline", "kind": "info", "code":
                 "db.products.aggregate([\n"
                 "  { $match: { active: true } },\n"
                 "  { $group: {\n"
                 "      _id: \"$category\",\n"
                 "      productCount: { $sum: 1 },\n"
                 "      averagePrice: { $avg: \"$price\" },\n"
                 "      minimumPrice: { $min: \"$price\" },\n"
                 "      maximumPrice: { $max: \"$price\" }\n"
                 "  } },\n"
                 "  { $sort: { averagePrice: -1 } }\n"
                 "])"}],
               points=[{"code": "_id        count  averagePrice\n"
                                "LAPTOP     2      1599.99\n"
                                "SHOE       3        88.32\n"
                                "ACCESSORY  5        86.24\n"
                                "BOOK       2        49.99",
                        "label": "Result (rounded)", "kind": "good", "size": 13},
                       ("L190 is inactive", "So LAPTOP counts 2, not 3."),
                       {"callout": ("XBAD trap", "Price \"49.99\" is a string: $avg skips it, "
                                                 "$max returns it.")}],
               mode="left",
               takeaway="Accumulators summarize each group — and a wrongly typed value "
                        "changes the answer quietly.",
               notes=[tp("The pipeline",
                         "$match keeps the 12 active products. "
                         "$group makes one document per category with four accumulators. "
                         "$sort ranks categories by average price."),
                      tp("The result",
                         "LAPTOP averages 1599.99 over two products, because L190 is "
                         "inactive. "
                         "SHOE averages 88.32 over three. "
                         "ACCESSORY averages 86.24 and BOOK 49.99. "
                         "The exact SHOE average is 88.3233…; add $round in a $project for "
                         "the report."),
                      tp("The XBAD trap",
                         "ACCESSORY counts five products, because XBAD is active. "
                         "Its price is the string \"49.99\". "
                         "$avg and $sum ignore non-numbers, so the average uses four prices. "
                         "But $max compares by BSON type order, where strings rank above "
                         "numbers, so ACCESSORY's maximumPrice is the string \"49.99\", not "
                         "249.99."),
                      tp("Guide differences",
                         "Older guides expect ACCESSORY 4 and the order LAPTOP, ACCESSORY, "
                         "SHOE, BOOK. "
                         "On a fresh load the counts are ACCESSORY 5 and the order is LAPTOP, "
                         "SHOE, ACCESSORY, BOOK. "
                         "The fix for the data is to match price with $type: \"decimal\", or "
                         "convert it with $toDecimal.")]),
        F.diagram(img(47), "Grouping by Several Fields",
                  "A document as _id: one group per combination of values.",
                  items=[{"code": "{ $group: {\n"
                                  "    _id: {\n"
                                  "      pay: \"$paymentStatus\",\n"
                                  "      ful: \"$fulfillmentStatus\" },\n"
                                  "    orders: { $sum: 1 },\n"
                                  "    revenue: { $sum: \"$total\" } } }",
                          "label": "Payment × fulfillment", "size": 11},
                         ("Result", "7 groups; PAID + SHIPPED is largest: 6 orders, "
                                    "3809.48."),
                         ("Read _id in words", "{ PENDING, NEW } = all pending, new orders: "
                                               "O5001, O6499.")],
                  takeaway="A compound _id groups by every combination — read it as a sentence "
                           "about the orders it holds.",
                  notes=dn(47)),
        F.diagram(img(46), "What $group Keeps — and Loses",
                  "Only _id and the accumulators leave the stage.",
                  items=[("Lost", "orderNumber, items and fulfillmentStatus don't carry "
                                  "forward."),
                         {"code": "{ $group: { _id: \"$customerId\",\n"
                                  "    spent: { $sum: \"$total\" },\n"
                                  "    orders: { $push: \"$orderNumber\" },\n"
                                  "    statuses: { $addToSet:\n"
                                  "      \"$fulfillmentStatus\" } } }",
                          "label": "Keep values with accumulators", "kind": "good",
                          "size": 11},
                         ("$first and $last", "Sort first — then they pick a meaningful "
                                              "document.")],
                  takeaway="Anything a report needs after $group must be kept by an "
                           "accumulator.",
                  notes=dn(46, [tp("On our data",
                                   "For Aisha Khan's paid orders, orders holds O6101, O6201, "
                                   "O6301 and O6306, and statuses holds SHIPPED and "
                                   "DELIVERED, each once.")])),
        F.diagram(img(51), "$count and $sortByCount",
                  "Count the stream — or count and rank each value.",
                  items=[{"code": "db.reviews.aggregate([\n"
                                  "  { $sortByCount: \"$rating\" }\n"
                                  "])",
                          "label": "Reviews per rating", "size": 12},
                         ("Result", "5 stars: 3 · 4 stars: 2 · 3 stars: 1 — our six "
                                    "reviews."),
                         ("$count", "{ $count: \"totalReviews\" } → { totalReviews: 6 }"),
                         {"callout": ("Shortcut", "$sortByCount = $group + $sum: 1 + "
                                                  "$sort.")}],
                  takeaway="$count counts what reaches it; $sortByCount counts and ranks each "
                           "value in one stage.",
                  notes=dn(51, [tp("Guide difference",
                                   "Exercise 5.2, the top-N checkpoint, runs $sortByCount on "
                                   "product category. "
                                   "On a fresh load it returns ACCESSORY 5, then LAPTOP 3 and "
                                   "SHOE 3, then BOOK 2. Older guides' ACCESSORY 4 predates "
                                   "the XBAD fixture.")])),
        F.exercise("Exercise: Orders by Payment Status",
                   "Group all orders — then check the counts add up.",
                   scenario="Finance asks how many orders — and how much money — sit in each "
                            "payment status.\n\nUse all 17 orders, not only the paid ones.",
                   tasks=["Group by paymentStatus",
                          "Count with $sum: 1; add total with $sum",
                          "Sort by revenue, highest first",
                          "Rename _id to paymentStatus in $project"],
                   expected=["PAID: 13 orders, 9118.44",
                             "PENDING: 3 orders, 4488.39",
                             "FAILED: 1 order, 45.19",
                             "13 + 3 + 1 = 17 orders"],
                   minutes=10,
                   takeaway="Check a grouped report by adding its counts back to the input "
                            "count.",
                   notes=[tp("How to run it",
                             "Individually for five minutes, then compare. "
                             "No $match this time: the question is about every order."),
                          tp("The pipeline",
                             "$group with _id \"$paymentStatus\", orders { $sum: 1 } and "
                             "revenue { $sum: \"$total\" }; $sort revenue -1; $project with "
                             "_id: 0 and paymentStatus: \"$_id\"."),
                          tp("The answer",
                             "PAID 13 orders worth 9118.44. PENDING 3 orders worth 4488.39: "
                             "O5001, O6401 and O6499. FAILED 1 order worth 45.19: O6402."),
                          tp("The habit",
                             "The counts add up to 17, the collection size. "
                             "That one check catches most mistakes in a $group.")]),

        # Part 4 ------------------------------------------------------------
        F.bridge(PARTS, 3, "Part 4: Arrays and Joins",
                 "Look inside the items array — and reach into other collections.",
                 so_far=["$group summarizes many documents per key",
                         "Accumulators keep what the report needs",
                         "Counts should add back up to the input"],
                 question="How do we report on individual order lines, and add customer names "
                          "that live in another collection?",
                 covers=["$unwind: one document per item", "Product sales from order lines",
                         "The double-counting trap", "$lookup: matched and unmatched",
                         "Customer spending with names"],
                 notes=[tp("Why this part",
                           "An order embeds its items, and refers to its customer by id. "
                           "To report on products we open the array; to show names we join "
                           "customers."),
                        tp("Watch for",
                           "How many documents each stage produces. $unwind multiplies them, "
                           "and $lookup adds arrays.")]),
        F.diagram(img(53), "$unwind: One Document per Array Element",
                  "An order with three items becomes three documents.",
                  items=[{"code": "db.orders.aggregate([\n"
                                  "  { $match: { orderNumber: \"O6303\" } },\n"
                                  "  { $unwind: \"$items\" }\n"
                                  "])",
                          "label": "Our three-item order", "size": 11},
                         ("Result", "3 documents — items is now one object, not an array."),
                         ("Scale", "The 13 paid orders become 21 line documents."),
                         {"callout": ("Output only", "Stored orders keep their arrays.")}],
                  takeaway="$unwind turns each array element into its own document — filter "
                           "first so it multiplies less.",
                  notes=dn(53)),
        F.code("Product Sales from Order Lines",
               "Paid orders → lines → line revenue → one row per SKU.",
               [{"label": "Pipeline (Exercises 5.1 and 5.4)", "kind": "info", "code":
                 "db.orders.aggregate([\n"
                 "  { $match: { paymentStatus: \"PAID\" } },\n"
                 "  { $unwind: \"$items\" },\n"
                 "  { $set: { lineRevenue: { $multiply:\n"
                 "      [\"$items.quantity\", \"$items.unitPrice\"] } } },\n"
                 "  { $group: {\n"
                 "      _id: \"$items.sku\",\n"
                 "      unitsSold: { $sum: \"$items.quantity\" },\n"
                 "      revenue: { $sum: \"$lineRevenue\" },\n"
                 "      orderCount: { $sum: 1 } } },\n"
                 "  { $sort: { revenue: -1 } },\n"
                 "  { $limit: 5 }\n"
                 "])"}],
               points=[{"code": "_id   units  revenue  orders\n"
                                "L110  2      3799.98  2\n"
                                "L100  2      2599.98  2\n"
                                "A500  2       499.98  2\n"
                                "S200  3       389.97  2\n"
                                "B300  3       179.97  2",
                        "label": "Result", "kind": "good", "size": 13},
                       ("orderCount", "$sum: 1 counts lines — equal to orders here, as no "
                                      "order repeats a SKU."),
                       {"callout": ("Order", "Match → unwind → compute → group.")}],
               mode="left",
               takeaway="Unwind after filtering, compute the line value, then group — that "
                        "is the product-report pattern.",
               notes=[tp("The pattern",
                         "Keep paid orders, open the items array, compute line revenue as "
                         "quantity times unitPrice, then group by SKU. "
                         "It is the answer to Exercise 5.1 and the corrected pipeline of "
                         "Exercise 5.4. Lab 4 uses the same pattern, grouped by product "
                         "category."),
                      tp("The result",
                         "L110, the Ultrabook, leads with two units worth 3799.98. "
                         "L100 follows with 2599.98 and A500 with 499.98. "
                         "S200 and B300 complete the top five."),
                      tp("Units versus revenue",
                         "Ranked by units instead, A410, the Wireless Mouse, leads with four. "
                         "The ranking depends on the metric."),
                      tp("Why no lineTotal",
                         "The content guide groups on $items.lineTotal. training_store has no "
                         "such field, so that sum would be 0. "
                         "Compute it, as here."),
                      tp("orderCount",
                         "$sum: 1 after $unwind counts lines. "
                         "No training_store order lists the same SKU twice, so it equals the "
                         "number of orders. "
                         "In general, $addToSet the orderNumber and take $size.")]),
        F.diagram(img(86), "Double-Counting After $unwind",
                  "Each line still carries the whole order's total.",
                  items=[("The trap", "O6303's total, 174.47, is summed three times — once "
                                      "per line."),
                         ("On our data", "Paid revenue is 9118.44; unwind first and it "
                                         "becomes 12119.25."),
                         ("The rule", "Sum order fields before $unwind; sum line values "
                                      "after it."),
                         {"callout": ("Check", "Known totals must not change.")}],
                  takeaway="After $unwind, sum line values — never the order total that every "
                           "line repeats.",
                  notes=dn(86)),
        F.diagram(img(61), "$lookup: Matched and Unmatched",
                  "Join another collection; the matches arrive as an array.",
                  items=[{"code": "{ $lookup: {\n"
                                  "    from: \"customers\",\n"
                                  "    localField: \"customerId\",\n"
                                  "    foreignField: \"_id\",\n"
                                  "    as: \"customer\" } }",
                          "label": "Orders → customers", "size": 12},
                         ("Always an array", "One match → [ {…} ]; no match → [ ]."),
                         ("O6499", "Its customerId matches no one, so customer is [ ]."),
                         {"callout": ("Keep it", "$unwind with preserveNullAndEmptyArrays: "
                                                 "true.")}],
                  takeaway="$lookup is a left outer join — it never drops an order, it just "
                           "leaves the array empty.",
                  notes=dn(61)),
        F.code("Customer Spending with Names",
               "Group first, then join — five lookups instead of thirteen.",
               [{"label": "Pipeline", "kind": "info", "code":
                 "db.orders.aggregate([\n"
                 "  { $match: { paymentStatus: \"PAID\" } },\n"
                 "  { $group: { _id: \"$customerId\",\n"
                 "      orders: { $sum: 1 },\n"
                 "      spent: { $sum: \"$total\" } } },\n"
                 "  { $lookup: { from: \"customers\",\n"
                 "      localField: \"_id\", foreignField: \"_id\",\n"
                 "      as: \"customer\" } },\n"
                 "  { $unwind: \"$customer\" },\n"
                 "  { $project: { _id: 0, orders: 1, spent: 1,\n"
                 "      name: { $concat: [\"$customer.name.first\",\n"
                 "                        \" \", \"$customer.name.last\"] } } },\n"
                 "  { $sort: { spent: -1 } }\n"
                 "])"}],
               points=[{"code": "name         orders  spent\n"
                                "Aisha Khan   4       3418.62\n"
                                "Maya Chen    2       2497.97\n"
                                "Jordan Lee   2       2321.46\n"
                                "Luis Romero  3        668.04\n"
                                "Priya Patel  2        212.35",
                        "label": "Result", "kind": "good", "size": 13},
                       ("No Sam Okonkwo", "C515's only order, O6402, failed payment."),
                       {"callout": ("Join late", "Look up after $group — one per "
                                                 "customer.")}],
               mode="left",
               takeaway="Group before you join — the lookup then runs once per customer, not "
                        "once per order.",
               notes=[tp("The pipeline",
                         "Match paid orders, group them by customerId, then look up each "
                         "customer. "
                         "The $group _id is the customer's ObjectId, so localField is _id."),
                      tp("The names",
                         "Customers store name.first and name.last, so the full name is a "
                         "$concat of the two. "
                         "The content guide's $firstName and $lastName don't exist here; they "
                         "would give null."),
                      tp("The result",
                         "Aisha Khan spent 3418.62 over four paid orders: O6101, O6201, O6301 "
                         "and O6306. "
                         "Maya Chen and Jordan Lee follow, each with one large laptop order."),
                      tp("Why no O6499 problem here",
                         "O6499 is pending, so the $match already removed it. "
                         "Every grouped customerId finds a customer, and a plain $unwind is "
                         "safe."),
                      tp("Email",
                         "To add the email, project \"$customer.contact.email\"; the email "
                         "is nested under contact.")]),
        F.exercise("Exercise: How Big Does the Stream Get?",
                   "Predict the document count after each stage.",
                   scenario="Before building the product report, predict how many documents "
                            "each stage passes on.",
                   scenario_code="db.orders.aggregate([\n"
                                 "  { $match: { paymentStatus: \"PAID\" } },\n"
                                 "  { $unwind: \"$items\" },\n"
                                 "  { $count: \"lines\" }\n"
                                 "])",
                   tasks=["Predict the count after $match",
                          "Predict the count after $unwind",
                          "Name the paid order with the most lines",
                          "What if $unwind came before $match?"],
                   expected=["13 paid orders",
                             "{ lines: 21 }",
                             "O6303 — three items",
                             "26 lines, filtered back to 21: more work"],
                   minutes=5,
                   takeaway="Know how many documents each stage emits — it is the first check "
                            "of any pipeline.",
                   notes=[tp("How to run it",
                             "Two minutes to write predictions, then run it on the "
                             "instructor screen."),
                          tp("The counts",
                             "13 paid orders. Six have one item, six have two and O6303 "
                             "has three: 6 + 12 + 3 = 21 lines."),
                          tp("The other order",
                             "All 17 orders hold 26 lines. Unwinding first creates all 26 "
                             "documents and then throws 5 away, the same result for more "
                             "work."),
                          tp("Why it matters",
                             "On a real store with millions of orders, that difference is "
                             "the difference between a fast and a slow report.")]),

        # Part 5 ------------------------------------------------------------
        F.bridge(PARTS, 4, "Part 5: Conditions, Dates and Reports",
                 "Per-document decisions, calendar reports and several metrics at once.",
                 so_far=["$unwind opens the items array",
                         "Sum line values, never repeated totals",
                         "$lookup joins as an array — group first"],
                 question="How do we label, bucket and date-group documents — and return a "
                          "whole dashboard from one call?",
                 covers=["$cond and $switch", "Dates and time zones", "Monthly paid sales",
                         "$bucket price bands", "$facet: several reports at once",
                         "A paid-orders dashboard"],
                 notes=[tp("Why this part",
                           "Real reports need labels, calendar periods and several metrics "
                           "side by side. These stages and expressions provide them."),
                        tp("Watch for",
                           "Time zones in date grouping, and the one-document shape of "
                           "$facet output.")]),
        F.diagram(img(37), "$cond: Decide per Document",
                  "If the condition is true use one value, otherwise the other.",
                  items=[{"code": "orderSize: { $cond: [\n"
                                  "  { $gte: [\"$total\",\n"
                                  "      Decimal128(\"1000.00\")] },\n"
                                  "  \"HIGH_VALUE\", \"STANDARD\" ] }",
                          "label": "Inside $set", "size": 11},
                         ("Result", "O6201 (79.07) → STANDARD; O6202 (2146.99) → "
                                    "HIGH_VALUE. Paid orders: 4 HIGH_VALUE, 9 STANDARD."),
                         ("$switch", "Several cases in order; the first true case wins, and "
                                     "default catches the rest.")],
                  takeaway="$cond and $switch put business rules into the pipeline — one "
                           "decision per document.",
                  notes=dn(37, [tp("The counts",
                                   "Among the 13 paid orders, four are HIGH_VALUE: O6101, "
                                   "O6202, O6301 and O6304, together 7290.20. The other nine "
                                   "are STANDARD.")])),
        F.diagram(img(35), "Dates and Time Zones",
                  "Dates are stored in UTC; reports need a local calendar.",
                  items=[{"code": "month: { $dateToString: {\n"
                                  "  format: \"%Y-%m\",\n"
                                  "  date: \"$createdAt\",\n"
                                  "  timezone: \"America/Toronto\"\n"
                                  "} }",
                          "label": "A month key", "size": 12},
                         ("Our order", "O5001's createdAt, 14:30 UTC, is 10:30 in "
                                       "Toronto."),
                         ("Name the zone", "Day and month boundaries depend on it."),
                         {"callout": ("Also", "$year, $month, $dateTrunc, $dateAdd.")}],
                  takeaway="Store dates in UTC; state the time zone every time a report "
                           "groups by day or month.",
                  notes=dn(35)),
        F.code("Monthly Paid Sales",
               "A month key, then one row per month in calendar order.",
               [{"label": "Pipeline", "kind": "info", "code":
                 "db.orders.aggregate([\n"
                 "  { $match: { paymentStatus: \"PAID\" } },\n"
                 "  { $set: { month: { $dateToString: {\n"
                 "      format: \"%Y-%m\", date: \"$createdAt\",\n"
                 "      timezone: \"America/Toronto\" } } } },\n"
                 "  { $group: { _id: \"$month\",\n"
                 "      orders: { $sum: 1 },\n"
                 "      revenue: { $sum: \"$total\" } } },\n"
                 "  { $sort: { _id: 1 } }\n"
                 "])"}],
               points=[{"code": "_id      orders  revenue\n"
                                "2026-07  3       1835.95\n"
                                "2026-08  4       2731.92\n"
                                "2026-09  6       4550.57",
                        "label": "Result", "kind": "good", "size": 13},
                       ("Sorts as text", "\"YYYY-MM\" strings sort in calendar order."),
                       ("O5001 excluded", "Its payment is still PENDING."),
                       {"callout": ("Check", "3 + 4 + 6 = 13 paid orders.")}],
               mode="left",
               takeaway="A date expression builds the key, $group builds the rows, $sort puts "
                        "them in calendar order.",
               notes=[tp("The pipeline",
                         "Keep paid orders, build a YYYY-MM month key from createdAt in the "
                         "Toronto time zone, group by it and sort ascending."),
                      tp("The result",
                         "July has three paid orders worth 1835.95: O6101, O6102 and O6103. "
                         "August has four worth 2731.92, and September six worth 4550.57."),
                      tp("Time zone",
                         "Without a timezone option, $dateToString uses UTC. "
                         "On this dataset no paid order is close to midnight at a month "
                         "boundary, so UTC gives the same months. "
                         "Real data will differ."),
                      tp("$dateTrunc",
                         "The content guide groups with $dateTrunc and unit month instead. "
                         "That returns a Date for the first of the month rather than a "
                         "string; both work.")]),
        F.diagram(img(64), "$bucket: Price Bands",
                  "Group values into ranges the business defines.",
                  items=[{"code": "{ $bucket: {\n"
                                  "    groupBy: \"$price\",\n"
                                  "    boundaries: [0, 50, 100, 500, 2000],\n"
                                  "    default: \"Other\",\n"
                                  "    output: { count: { $sum: 1 } } } }",
                          "label": "Price bands on products", "size": 11},
                         ("Result", "0: 5 · 50: 2 · 100: 3 · 500: 2 · Other: 1"),
                         ("Boundaries", "Lower bound in, upper bound out: 49.99 → the 0 "
                                        "band."),
                         {"callout": ("Other = XBAD", "A string price fits no band.")}],
                  takeaway="$bucket turns a number into a business band — and default catches "
                           "whatever doesn't fit.",
                  notes=dn(64, [tp("The bands on our data",
                                   "Under 50: USB Hub, Wireless Mouse, Query Cookbook, "
                                   "Clearance Shoe and Wireless Keyboard. 50 to 100: Trail "
                                   "Shoe and MongoDB Fundamentals. 100 to 500: Refurbished "
                                   "Laptop, Running Shoe and Docking Station. 500 to 2000: the "
                                   "two laptops."),
                                tp("Guide difference",
                                   "Older guides expect four buckets. A fresh load gives five, "
                                   "because XBAD's string price goes to the Other bucket.")])),
        F.diagram(img(65), "$facet: Several Reports in One Pass",
                  "Parallel sub-pipelines on the same input, one result document.",
                  items=[("Same input", "Every sub-pipeline sees the documents that reach "
                                        "$facet."),
                         ("One document", "Each facet name holds an array of results."),
                         ("Use it for", "Dashboards and API responses with several "
                                        "metrics."),
                         {"callout": ("Filter first", "One $match before $facet serves every "
                                                      "facet.")}],
                  takeaway="$facet returns a whole dashboard in one document — one array per "
                           "sub-pipeline.",
                  notes=dn(65)),
        F.code("A Paid-Orders Dashboard",
               "Totals, a status breakdown and a high-value count in one call.",
               [{"label": "Pipeline (trimmed)", "kind": "info", "code":
                 "db.orders.aggregate([\n"
                 "  { $match: { paymentStatus: \"PAID\" } },\n"
                 "  { $facet: {\n"
                 "      totals: [ { $group: { _id: null,\n"
                 "          orders: { $sum: 1 },\n"
                 "          revenue: { $sum: \"$total\" } } } ],\n"
                 "      byFulfillment: [\n"
                 "        { $sortByCount: \"$fulfillmentStatus\" } ],\n"
                 "      highValue: [\n"
                 "        { $match: { total:\n"
                 "            { $gte: Decimal128(\"1000.00\") } } },\n"
                 "        { $count: \"orders\" } ]\n"
                 "  } }\n"
                 "])"}],
               points=[{"code": "{ totals: [ { _id: null,\n"
                                "    orders: 13, revenue: 9118.44 } ],\n"
                                "  byFulfillment: [\n"
                                "    { _id: \"SHIPPED\", count: 6 },\n"
                                "    { _id: \"DELIVERED\", count: 4 },\n"
                                "    { _id: \"PROCESSING\", count: 2 },\n"
                                "    { _id: \"NEW\", count: 1 } ],\n"
                                "  highValue: [ { orders: 4 } ] }",
                        "label": "Result: one document", "kind": "good", "size": 12},
                       {"callout": ("Arrays", "Even one-row facets are arrays.")}],
               mode="left",
               takeaway="Filter once, then let each facet answer its own question — the "
                        "result is one document.",
               notes=[tp("The pipeline",
                         "One $match keeps the 13 paid orders. "
                         "Then three facets run on those same 13 documents."),
                      tp("The result",
                         "totals holds one document: 13 orders worth 9118.44. "
                         "byFulfillment ranks SHIPPED 6, DELIVERED 4, PROCESSING 2 and NEW 1. "
                         "highValue counts four orders of at least 1000."),
                      tp("Reading the shape",
                         "The output is one document, and every facet is an array, even "
                         "totals and highValue, which hold one element each. "
                         "Application code reads result.totals[0].revenue."),
                      tp("Extending it",
                         "A fuller dashboard adds topCustomers and topProducts facets. "
                         "topProducts starts with L110, as in the product sales report.")]),

        # Part 6 ------------------------------------------------------------
        F.bridge(PARTS, 5, "Part 6: Performance and Debugging",
                 "Right first, then cheap — and a method for finding what went wrong.",
                 so_far=["$cond, dates and $bucket label documents",
                         "$facet returns several reports at once",
                         "Every report was checked against the data"],
                 question="How do we order stages so a pipeline stays correct and cheap — and "
                          "find the stage that broke it?",
                 covers=["Early versus late $match", "Build and verify one stage at a time",
                         "Common aggregation mistakes"],
                 notes=[tp("Why this part",
                           "training_store is tiny, so every pipeline is fast here. "
                           "The habits in this part are what keep pipelines fast on real "
                           "data."),
                        tp("Link to Module 6",
                           "Module 6 adds indexes and explain plans. "
                           "This part explains why the first stage matters so much to "
                           "them.")]),
        F.diagram(img(79), "Early vs. Late $match",
                  "Filter first: fewer documents for every later stage.",
                  items=[("Early", "$match PAID first: 13 documents flow on, not 17."),
                         ("Late can be wrong", "After $group, the status field no longer "
                                               "exists."),
                         ("Join late", "$lookup after $group runs once per customer."),
                         {"callout": ("Index", "A first-stage $match can use one — Module "
                                               "6.")}],
                  takeaway="Filter as early as possible, and join after you have reduced the "
                           "stream.",
                  notes=dn(79, [tp("Applying it",
                                   "To speed up a slow customer report: match paid orders "
                                   "first, group by customerId without unwinding, then look "
                                   "up customers and keep ACTIVE ones. A supporting index "
                                   "later is { paymentStatus: 1, customerId: 1 }."),
                                tp("Lab 4, Step 5",
                                   "Lab 4's optional Step 5 runs explain(\"executionStats\") "
                                   "on the report and checks that $match is first. Comparing "
                                   "a late and an early $match on 17 orders, both plans may look "
                                   "alike, because the optimizer moves a $match ahead of a "
                                   "$sort. Read the plan shape, not the milliseconds.")])),
        F.diagram(img(76), "Build a Pipeline One Stage at a Time",
                  "Define the output, then add and check one stage at a time.",
                  items=[("One stage at a time", "Run the first stage and check the count "
                                                 "and one document; add the next, run "
                                                 "again."),
                         ("Prove one number", "Add Aisha's paid orders by hand: 3418.62 "
                                              "must match the pipeline."),
                         {"code": "db.orders\n"
                                  "  .explain(\"executionStats\")\n"
                                  "  .aggregate([ … ])",
                          "label": "Then inspect the plan", "size": 11}],
                  takeaway="Build incrementally and verify each stage — a wrong path shows up "
                           "the moment you add it.",
                  notes=dn(76, [tp("Day 2 Lab 4",
                                   "Lab 4 is built exactly this way: confirm the input set "
                                   "(10 paid orders that are shipped or delivered), add "
                                   "$unwind and line sales, then join products and group by "
                                   "category. Step 4 proves one number with a second "
                                   "pipeline.")])),
        F.myths("Common Aggregation Mistakes",
                "Why a pipeline returns nothing, too much or the wrong total.",
                [("\"total\" and \"$total\" mean the same",
                  "Without $ it is the text \"total\", not the field"),
                 ("$limit, then $sort gives a top N",
                  "Sort first — otherwise it is an arbitrary N"),
                 ("Sum total after $unwind",
                  "Each order's total repeats on every line"),
                 ("$match on paymentStatus after $group",
                  "$group dropped it — filter before grouping"),
                 ("$lookup returns one document",
                  "It returns an array — unwind it or take [0]")],
                ["status: \"Shipped\" — orders have no status field",
                 "$items.lineTotal — compute quantity × unitPrice",
                 "$lookup on every order before filtering",
                 "Unwinding just to sum order totals",
                 "Money compared with strings, not Decimal128"],
                remember=("Remember", "Filter early, group before joining, verify each "
                                      "stage."),
                takeaway="Most broken pipelines have a wrong field path or a stage in the "
                         "wrong place.",
                notes=[tp("Why this slide",
                          "Before the checks, collect the mistakes that cause most broken "
                          "pipelines. Exercise 5.4 contains several of them at once."),
                       tp("Field references",
                          "A $ turns a string into a field path. "
                          "\"items.sku\" as a group key is one constant, so everything lands "
                          "in one group; \"$items.sku\" is the SKU."),
                       tp("Order mistakes",
                          "$limit before $sort, $match after $group on a dropped field, and "
                          "$unwind before summing order totals all give plausible but wrong "
                          "answers. They don't raise errors."),
                       tp("Dataset traps",
                          "Generic examples use status and lineTotal. "
                          "training_store has paymentStatus, fulfillmentStatus, quantity and "
                          "unitPrice. "
                          "Money is Decimal128, so compare it with Decimal128(\"1000.00\").")]),
        F.diagram(img(88), "Module 5 at a Glance",
                  "Filter, shape, group, join — and verify each stage.",
                  takeaway="A pipeline is ordered transformations: filter, shape, group and "
                           "join — then check the numbers.",
                  notes=dn(88)),

        # Wrap-up ------------------------------------------------------------
        F.knowledge("Knowledge Check", "Answer in your own words — then compare with a partner.",
                    ["What does each pipeline stage receive and pass on?",
                     "Why can $group then $match on paymentStatus return nothing?",
                     "How is $project different from $set?",
                     "What does _id mean in a $group stage?",
                     "What does $sum: 1 calculate?",
                     "When do you need $unwind?",
                     "What does $lookup put in its as field?",
                     "Why must $sort come before $limit?",
                     "How do you handle a missing shippingFee?",
                     "What does a $facet stage return?"],
                    notes=[tp("1. Stages",
                              "Each stage receives the documents the previous stage output, "
                              "transforms them and passes the result on."),
                           tp("2. Group then match",
                              "$group outputs only _id and accumulators, so paymentStatus no "
                              "longer exists when $match runs. Filter before grouping."),
                           tp("3. $project and $set",
                              "$project returns only the fields you list. $set, or "
                              "$addFields, adds or replaces fields and keeps the rest."),
                           tp("4. _id in $group",
                              "The grouping key. Each distinct value becomes one output "
                              "document; null puts everything in one group."),
                           tp("5. $sum: 1",
                              "It adds one per document, so it counts the documents in each "
                              "group."),
                           tp("6. $unwind",
                              "When you need to work with individual array elements, such as "
                              "grouping order items by SKU."),
                           tp("7. $lookup",
                              "An array of the matching documents from the other collection: "
                              "empty when nothing matches, as for O6499."),
                           tp("8. Sort before limit",
                              "$limit keeps the first N documents it receives. Unsorted, "
                              "those are arbitrary, not the top N."),
                           tp("9. Missing values",
                              "$ifNull: [\"$shippingFee\", Decimal128(\"0.00\")], so the "
                              "calculation doesn't become null."),
                           tp("10. $facet",
                              "One document with one field per facet, each holding that "
                              "sub-pipeline's results as an array.")]),
        F.exercise("Exercise 5.1 — Arrange Pipeline Stages",
                   "Module 5 checkpoint A: put six stages in the right order.",
                   kind="OFFICIAL CHECKPOINT A", minutes=10,
                   worksheet="labs/day-02/exercises/exercise-5.1-arrange-pipeline-stages.md",
                   scenario="Top five products by line revenue from paid orders. Use each "
                            "stage once. No MongoDB needed.",
                   scenario_code="$limit    $unwind   $sort\n"
                                 "$match    $group    $set",
                   tasks=["Propose an order for the six stages",
                          "Describe the documents after each one",
                          "Compare with the instructor's reveal",
                          "Explain why $limit can't precede $sort"],
                   expected=["$match → $unwind → $set",
                             "→ $group → $sort → $limit",
                             "$unwind before grouping by SKU",
                             "$match after $group filters groups"],
                   expected_title="Solution (after debrief)",
                   takeaway="The right order follows the data: filter, expand, compute, group, "
                            "rank, cut.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 5.1. The worksheet is "
                             "labs/day-02/exercises/exercise-5.1-arrange-pipeline-stages.md; the "
                             "answer key is in labs/day-02/exercises/solution/. "
                             "Pairs, on paper; no MongoDB is needed."),
                          tp("The reveal",
                             "$match paid orders, $unwind items, $set lineRevenue, $group by "
                             "SKU, $sort by revenue descending, $limit 5."),
                          tp("What to listen for",
                             "$limit before $sort gives five arbitrary products. "
                             "$unwind must come before grouping by items.sku. "
                             "$set could also sit inside $group as a $sum of $multiply — a "
                             "defensible variation."),
                          tp("The follow-up question",
                             "A $match after $group would filter the grouped SKU rows, for "
                             "example keeping products with revenue over 500. "
                             "That is a different, valid question.")]),
        F.exercise("Exercise 5.2 — Build a Top-N Report",
                   "Module 5 checkpoint B: four rankings, each sorted before it is limited.",
                   kind="OFFICIAL CHECKPOINT B", minutes=15,
                   worksheet="labs/day-02/exercises/exercise-5.2-build-a-top-n-report.md",
                   scenario="Build four top-N reports from training_store.",
                   scenario_code="1  Top 5 customers by paid spend\n"
                                 "2  Top 3 paid orders by total\n"
                                 "3  Top 3 SKUs by units sold\n"
                                 "4  Products per category\n"
                                 "   { $sortByCount: \"$category\" }",
                   tasks=["Match PAID; group spend by customerId",
                          "Sort total -1 with a tie-breaker",
                          "Unwind items; sum quantity by SKU",
                          "Rank categories with $sortByCount"],
                   expected=["C101 first: 3418.62",
                             "O6202, O6304 (2146.99), O6301",
                             "A410 leads with 4 units",
                             "ACCESSORY 5, LAPTOP 3, SHOE 3, BOOK 2"],
                   expected_title="Solution (after debrief)",
                   takeaway="Every top-N is $sort then $limit — add a tie-breaker whenever "
                            "values can tie.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 5.2. The worksheet is "
                             "labs/day-02/exercises/exercise-5.2-build-a-top-n-report.md."),
                          tp("Customers and orders",
                             "C101, Aisha Khan, is the top paid spender with 3418.62. "
                             "The highest paid orders are O6202 and O6304 at 2146.99, then "
                             "O6301 at 1512.23; orderNumber breaks the tie."),
                          tp("Units",
                             "Sorted by unitsSold and then _id, A410 leads with 4 units, "
                             "followed by A400 and B300 with 3. P1001 and S200 also sold 3."),
                          tp("A dataset note",
                             "The worksheet lists ACCESSORY 4. On a fresh load $sortByCount "
                             "returns ACCESSORY 5, because the XBAD fixture is an accessory, "
                             "then LAPTOP 3 and SHOE 3, then BOOK 2. The inactive L190 is "
                             "counted, since there is no $match.")]),
        F.exercise("Exercise 5.3 — Join Related Collections",
                   "Module 5 checkpoint C: add customer names, keep the unmatched order.",
                   kind="OFFICIAL CHECKPOINT C", minutes=20,
                   worksheet="labs/day-02/exercises/exercise-5.3-join-related-collections.md",
                   scenario="List every order with its customer number and full name, "
                            "largest total first.",
                   scenario_code="{ $lookup: { from: \"customers\",\n"
                                 "    localField: \"customerId\",\n"
                                 "    foreignField: \"_id\",\n"
                                 "    as: \"customer\" } },\n"
                                 "{ $unwind: { path: \"$customer\",\n"
                                 "    preserveNullAndEmptyArrays:\n"
                                 "      true } },\n"
                                 "{ $project: … }, { $sort: … }",
                   tasks=["Join orders to customers",
                          "Unwind, keeping empty matches",
                          "Project number and $concat name",
                          "Find the order with no customer"],
                   expected=["17 rows; O6401 first (2945.98)",
                             "Names such as Aisha Khan",
                             "O6499: no customerNumber",
                             "Kept by preserveNullAndEmptyArrays"],
                   expected_title="Solution (after debrief)",
                   takeaway="$lookup returns an array — decide deliberately what happens when "
                            "it is empty.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 5.3. The worksheet is "
                             "labs/day-02/exercises/exercise-5.3-join-related-collections.md."),
                          tp("The projection",
                             "customerNumber: \"$customer.customerNumber\" and customerName: "
                             "$concat of \"$customer.name.first\", a space and "
                             "\"$customer.name.last\"."),
                          tp("The result",
                             "All 17 orders appear, sorted by total. O6401, Luis Romero's "
                             "pending 2945.98 order, is first. "
                             "O6499 has no customerNumber, and its customerName is null, "
                             "because $concat of missing fields returns null."),
                          tp("Without preserve",
                             "Remove preserveNullAndEmptyArrays and O6499 disappears: 16 "
                             "rows. Ask learners which behaviour a data-quality report "
                             "needs.")]),
        F.exercise("Exercise 5.4 — Correct a Broken Pipeline",
                   "Module 5 checkpoint D: find the defects, then rewrite and run it.",
                   kind="OFFICIAL CHECKPOINT D", minutes=15,
                   worksheet="labs/day-02/exercises/exercise-5.4-correct-a-broken-pipeline.md",
                   scenario="This pipeline should report product revenue.",
                   scenario_code="{ $limit: 3 },\n"
                                 "{ $group: { _id: \"items.sku\",\n"
                                 "    unitsSold: { $sum: \"$quantity\" },\n"
                                 "    revenue: { $sum: \"$total\" } } },\n"
                                 "{ $sort: { revenue: -1 } },\n"
                                 "{ $lookup: { from: \"customers\", … } },\n"
                                 "{ $project: { sku:\n"
                                 "    \"$customer.customerNumber\" } }",
                   tasks=["List at least five defects",
                          "Name the symptom each one causes",
                          "Rewrite: match, unwind, set, group, sort, limit",
                          "Run it and name the top SKU"],
                   expected=["$limit first; no PAID filter",
                             "\"items.sku\" lacks $: one group",
                             "No $unwind; quantity is under items",
                             "total is not line revenue",
                             "No $lookup needed; L110 is first"],
                   expected_title="Solution (after debrief)",
                   takeaway="Debug a pipeline stage by stage: field paths first, then stage "
                            "order.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 5.4. The worksheet is "
                             "labs/day-02/exercises/exercise-5.4-correct-a-broken-pipeline.md."),
                          tp("The seven defects",
                             "$limit before any sort; no paid-order filter; \"items.sku\" "
                             "without $, so every order falls in one group; quantity read "
                             "from the top level instead of items; no $unwind before grouping "
                             "by SKU; total is an order total, not line revenue; and the "
                             "$lookup output is treated like an object."),
                          tp("The correct core",
                             "Match PAID, unwind items, set lineRevenue as quantity times "
                             "unitPrice, group by \"$items.sku\" with unitsSold and revenue, "
                             "sort revenue descending, limit 5. "
                             "It returns L110 first with 3799.98."),
                          tp("The lesson",
                             "A product revenue report needs no customer join at all. "
                             "Removing a stage is often the best fix.")]),
        F.exercise("Lab 4 — Aggregation Pipeline",
                   "Day 2 hands-on: top product categories for completed paid sales.",
                   kind="OFFICIAL LAB", minutes=60,
                   worksheet="labs/day-02/lab4/LAB-4-GUIDE.md",
                   scenario="Rank categories for PAID orders that are SHIPPED or DELIVERED. "
                            "Reload load.js first.",
                   scenario_code="$match → $unwind → $set lineSales\n"
                                 "→ $lookup products → $unwind\n"
                                 "→ $group by category → $set\n"
                                 "→ $match ≥ 50 → $sort → $limit",
                   tasks=["0 Reload; count the collections",
                          "1 Count the completed paid orders",
                          "2 Unwind; compute lineSales",
                          "3 Join products; group by category",
                          "4 Prove one number; 5 explain"],
                   expected=["13 · 6 · 17 · 6; 13 PAID",
                             "10 orders, 18 lines",
                             "quantity × unitPrice, Decimal128",
                             "LAPTOP 4499.97; 4 categories",
                             "3 laptop units; $match first"],
                   expected_title="Expected results",
                   takeaway="One pipeline, built and checked stage by stage, turns 17 orders "
                            "into a ranked category report.",
                   notes=[tp("Official lab",
                             "This is Day 2 Lab 4, labs/day-02/lab4/LAB-4-GUIDE.md, about 45 to "
                             "60 minutes. The instructor answer key is "
                             "labs/day-02/lab4/solution/LAB-4-SOLUTION.md. "
                             "It is the outline hands-on, building an aggregation pipeline."),
                          tp("Before you start",
                             "Reload load.js from the repository root in PowerShell. Lab 3 "
                             "changed O6202 and A410, and the Module 4 labs added products, so "
                             "without a reload the numbers drift. "
                             "Step 0 checks 13 products, 6 customers, 17 orders, 6 reviews and "
                             "13 paid orders."),
                          tp("Steps 1 and 2",
                             "Step 1 counts the input: PAID and SHIPPED or DELIVERED gives 10 "
                             "orders; O6202 and O6302 are still PROCESSING and O6305 is NEW. "
                             "Step 2 runs $match, $unwind and $set: 18 line documents, each "
                             "with lineSales as quantity times unitPrice."),
                          tp("Step 3, the report",
                             "Join each line to products on items.productId, group by "
                             "product.category and rank. "
                             "LAPTOP 4499.97 from 3 units and 2 customers, ACCESSORY 744.91 from "
                             "9 units, SHOE 264.97 and BOOK 259.95. "
                             "All four clear 50, so $limit 5 returns four rows."),
                          tp("Steps 4 and 5",
                             "Step 4 proves one number: laptop units from a second pipeline "
                             "are 3, the same as LAPTOP totalUnitsSold. "
                             "Optional Step 5 runs explain and confirms the $match is the "
                             "first stage."),
                          tp("Debrief",
                             "Ask why the $match comes before $unwind, and why $lookup comes "
                             "after it. "
                             "Then ask which index would help the first $match: that is where "
                             "Module 6 begins.")]),
        F.wrapup("Module 5 Summary and What's Next",
                 "From one $match to a multi-metric sales report.",
                 can=["Explain how documents flow through a pipeline",
                      "Filter and shape with $match, $project, $set",
                      "Summarize with $group and accumulators",
                      "Expand items with $unwind; join with $lookup",
                      "Build monthly, banded and $facet reports",
                      "Order stages for correct, cheap pipelines"],
                 next_title="Next: Module 6 — Indexing and Query Performance",
                 questions=["Which index supports our first $match?",
                            "How do I read explain(\"executionStats\")?",
                            "When is a query covered by an index?"],
                 bring=("Bring along", "Your Day 2 Lab 4 pipeline and the index you would "
                                       "add for its first $match."),
                 takeaway="Module 6 makes these pipelines fast: the first $match is where an "
                          "index pays off.",
                 notes=[tp("Recap",
                           "We moved from one $match to reports that group, unwind, join and "
                           "facet, all on training_store with numbers we checked by hand."),
                        tp("Day 2 Lab 4",
                           "Next is Day 2 Lab 4: top product categories for paid orders that "
                           "are shipped or delivered. "
                           "It uses paymentStatus and fulfillmentStatus, computes line sales, "
                           "and on a fresh load LAPTOP comes first with 4499.97."),
                        tp("Next module",
                           "Module 6, on Day 3, covers index types, compound index order, "
                           "covered queries and explain plans. "
                           "The first $match of each pipeline is where those indexes help, "
                           "for example { paymentStatus: 1, createdAt: 1 }."),
                        tp("Bring along",
                           "Keep the Lab 4 pipeline and one proposed index. "
                           "Module 6 tests them with explain.")]),
    ]
