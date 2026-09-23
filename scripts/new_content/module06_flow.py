#!/usr/bin/env python3
"""Slide order for the Module 6 deck: from a collection scan to a tuned index set.

Every concept diagram is merged with the slide that explains it (diagram plus the
points only that slide adds), so no idea appears twice. Part openers, mongosh
examples and real explain() excerpts on the training_store sample database,
in-flow practice exercises, a knowledge check, official Exercises 6.1, 6.2 and
6.3, the official Day 3 Lab 5 slide and a bridge to Module 7 connect the ideas.
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
    DARK_GRAY, GREEN, LEFT, LIGHT_GRAY, MUTED, NAVY, ORANGE, PURPLE, RED, RIGHT, TEAL,
)

PARTS = ["Part 1\nHow indexes work", "Part 2\nManage indexes", "Part 3\nCompound + ESR",
         "Part 4\nSpecialized types", "Part 5\nexplain()", "Part 6\nCosts + mistakes"]


# ---------------------------------------------------------------------------
# Custom slides
# ---------------------------------------------------------------------------
LAB5_GUIDE = "labs/day-03/lab5/LAB-5-GUIDE.md"


def _lab5(slide, y0, y1):
    # Official-lab header row, in the same style as the checkpoint slides.
    kind = "OFFICIAL LAB"
    tag_w = 0.25 + len(kind) * 0.115
    V.box(slide, LEFT, y0, tag_w, 0.42, kind, fill=RED, size=13)
    V.box(slide, LEFT + tag_w + 0.15, y0, 1.25, 0.42, "40–50 MIN", fill=LIGHT_GRAY,
          color=DARK_GRAY, size=13)
    ww = min(7.2, 0.45 + len(LAB5_GUIDE) * 0.085)
    V.code(slide, RIGHT - ww, y0, ww, 0.42, LAB5_GUIDE, size=11, align=PP_ALIGN.CENTER)
    y0 += 0.62

    lw = 7.25
    y = V.section(slide, LEFT, y0, lw, "Six core steps on a fresh load", icon="🧪", fill=NAVY)
    steps = [
        ("Baseline: C101's orders, newest first", "explain → SORT + COLLSCAN", NAVY),
        ("Create the history index", "idx_orders_customer_date", PURPLE),
        ("Measure again", "IXSCAN · 5 keys · 5 docs · no SORT", TEAL),
        ("A new shape: PROCESSING orders", "idx_orders_fulfillment_date", GREEN),
        ("Multikey: tags = \"wireless\"", "idx_products_tags", ORANGE),
        ("Inventory every index", "getIndexes() on all four collections", RED),
    ]
    rh = (y1 - y - 0.05) / len(steps)
    for k, (head, detail, fill) in enumerate(steps):
        ry = y + k * rh
        V.badge(slide, LEFT, ry + (rh - 0.42) / 2, 0.42, str(k + 1), fill=fill, size=13)
        V.text(slide, LEFT + 0.58, ry, lw - 0.58, rh,
               [(head, {"bold": True, "size": 15}),
                (detail, {"size": 12, "color": MUTED, "font": K.CODE_FONT})],
               size=15, anchor=MSO_ANCHOR.MIDDLE)

    rx = LEFT + lw + 0.40
    rw = RIGHT - rx
    avail = y1 - y0
    ch = min(2.05, 0.42 * avail)
    body = V.card(slide, rx, y0, rw, ch, "Before you start", head_fill=RED, title_size=14)
    V.code(slide, rx + 0.15, body, rw - 0.30, y0 + ch - body - 0.12,
           'mongosh "mongodb://localhost:27017" `\n'
           '  .\\datasets\\training_store\\load.js\n'
           'use training_store', size=11)
    c1 = (avail - ch - 0.30) / 2
    V.callout(slide, rx, y0 + ch + 0.15, rw, c1, "C101",
              "Look it up by customerNumber — don't copy an ObjectId from a slide.", size=13)
    V.callout(slide, rx, y0 + ch + 0.30 + c1, rw, y1 - (y0 + ch + 0.30 + c1), "Go further",
              "Steps 7–13 add catalog, unique, partial, TTL, covered, aggregation and audit "
              "practice.", size=13)


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
        *G.intro("module06"),
        F.story("From Module 5 to Module 6",
                "Day 2 taught us to ask questions — Day 3 makes them fast.",
                gave_title="Module 5 gave us",
                gave=["Pipelines of $match, $group and $sort",
                      "Reports over orders and reviews",
                      "$lookup joins between collections",
                      "Filter early to shrink the work",
                      "Results checked against real data"],
                now=("Now", "Index the query shapes Day 2 wrote — and prove each one with "
                            "explain()."),
                path_title="Our path through Module 6",
                path=[("See why a query reads every document", "Part 1", NAVY),
                      ("Create, list, hide and drop indexes", "Part 2", PURPLE),
                      ("Order compound fields with ESR", "Part 3", TEAL),
                      ("Pick a specialized index type", "Part 4", GREEN),
                      ("Read explain() and cover a query", "Part 5", ORANGE),
                      ("Weigh selectivity, costs and mistakes", "Part 6", RED)],
                takeaway="Module 5 asked the questions; Module 6 makes MongoDB answer them "
                         "without reading every document.",
                notes=[tp("Bridge from Module 5",
                          "In Module 5 we built pipelines over training_store: $match, $group, "
                          "$sort, $lookup and more. "
                          "We learned to put $match early so later stages see fewer "
                          "documents."),
                       tp("The missing piece",
                          "An early $match or a find is only fast if MongoDB can locate the "
                          "matching documents without reading them all. "
                          "That is what indexes do, and it is today's first module."),
                       tp("The path",
                          "Six parts: how indexes work, managing them, compound indexes and ESR, "
                          "specialized types, explain() and covered queries, and finally costs "
                          "and mistakes. "
                          "Lab 5 at the end puts it all into practice."),
                       tp("Same dataset",
                          "Reload training_store with load.js before the lab so earlier writes "
                          "are gone. "
                          "Every example on these slides uses the freshly loaded data.")]),

        # Part 1 ------------------------------------------------------------
        F.bridge(PARTS, 0, "Part 1: How Indexes Work",
                 "Start with how MongoDB finds a document at all.",
                 so_far=["Module 5 built pipelines over our data",
                         "Every query so far ran without asking how"],
                 question="How does MongoDB find documents — and why does an index make it "
                          "faster?",
                 covers=["Why query performance matters", "Collection scan versus index scan",
                         "What an index looks like inside", "The _id index every collection "
                                                            "has"],
                 notes=[tp("Where we start",
                           "Until now we asked what a query returns. "
                           "Now we ask how MongoDB found it."),
                        tp("What this part answers",
                           "We compare a collection scan with an index scan, look inside an "
                           "index, and meet the one index every collection already has.")]),
        F.diagram(img(3), "Why Query Performance Matters",
                  "The same query: an indexed lookup or a full collection scan.",
                  items=[("Indexed lookup", "Few documents read — fast, predictable "
                                            "responses."),
                         ("Collection scan", "Every document read — the cost grows with the "
                                             "collection."),
                         ("At scale", "Slow queries queue up: users wait and the server works "
                                      "harder."),
                         {"callout": ("Our dataset", "13 products and 17 orders scan "
                                                     "instantly — watch counts, not the "
                                                     "clock.")}],
                  takeaway="An index changes how much work a query does — the result stays "
                           "the same.",
                  notes=dn(3)),
        F.diagram(img(5), "Collection Scan vs Index Scan",
                  "Same query, same three matches — 8 documents examined versus 3.",
                  items=[("COLLSCAN", "Reads every document and tests the filter on each "
                                      "one."),
                         ("IXSCAN", "Finds the matching keys in the category index, then "
                                    "fetches only those documents."),
                         ("The signal", "Examined versus returned: 8 : 3 against 3 : 3."),
                         {"callout": ("In training_store", "category is \"BOOK\": 2 of 13 "
                                                           "products.")}],
                  takeaway="Compare documents examined with documents returned — the closer "
                           "they are, the better the plan.",
                  notes=dn(5)),
        F.diagram(img(7), "Inside an Index: A Sorted Tree",
                  "An index is a B-tree of sorted keys, each pointing to a document.",
                  items=[("Root and internal nodes", "Split the key range: below 50, 50–99, "
                                                     "100 and above."),
                         ("Sorted leaf entries", "Each key points to its document: 79 → "
                                                 "doc 6."),
                         ("Why it's fast", "A few steps down the tree instead of reading every "
                                           "document."),
                         {"callout": ("Sorted", "The same order also serves ranges and "
                                                "sorts.")}],
                  takeaway="An index keeps values in sorted order with pointers to documents — "
                           "so lookups, ranges and sorts need no full scan.",
                  notes=dn(7)),
        F.diagram(img(10), "The Default _id Index",
                  "Every collection gets a unique index on _id — automatically.",
                  items=[("Created for you", "Named _id_; it exists before you create "
                                             "anything."),
                         ("Unique", "Two documents in one collection can't share an _id."),
                         ("Can't be dropped", "dropIndexes() removes every other index but "
                                              "keeps _id_."),
                         {"code": "db.products.find({\n  _id: ObjectId(\"…\")\n})",
                          "label": "Always an index scan", "size": 12}],
                  takeaway="Lookups by _id are always indexed — every other query shape needs "
                           "an index you design.",
                  notes=dn(10)),

        # Part 2 ------------------------------------------------------------
        F.bridge(PARTS, 1, "Part 2: Manage Indexes",
                 "Create, list, hide and drop — by name.",
                 so_far=["COLLSCAN reads every document; IXSCAN reads matching keys",
                         "An index is a sorted tree of keys and pointers",
                         "Every collection has a unique _id index"],
                 question="How do we create, inspect, hide and remove indexes safely?",
                 covers=["What load.js already built", "Creating indexes with clear names",
                         "Listing and dropping indexes", "Hiding an index to test a removal"],
                 notes=[tp("Connecting the parts",
                           "Part 1 showed why indexes help. "
                           "Part 2 is the everyday toolkit for managing them."),
                        tp("Watch for",
                           "Names. "
                           "The course uses idx_ for helper indexes, uq_ for unique rules and "
                           "ttl_ for TTL indexes, so every explain() and $indexStats result is "
                           "easy to read.")]),
        F.code("Create, List and Drop Named Indexes",
               "On a fresh training_store — the output is what mongosh prints.",
               [{"label": "What load.js already built", "kind": "info", "code":
                 "db.products.getIndexes()\n"
                 "  .map(i => i.name)\n"
                 "\n"
                 "[ '_id_', 'sku_unique' ]"},
                {"label": "Create with a clear name", "kind": "good", "code":
                 "db.products.createIndex(\n"
                 "  { category: 1, price: 1 },\n"
                 "  { name:\n"
                 "    \"idx_products_category_price\" }\n"
                 ")\n"
                 "\n"
                 "idx_products_category_price"},
                {"label": "Drop by name — never _id_", "kind": "info", "code":
                 "db.products.dropIndex(\n"
                 "  \"idx_products_category_price\"\n"
                 ")\n"
                 "\n"
                 "{ nIndexesWas: 3, ok: 1 }"}],
               points=[("Names", "idx_<collection>_<fields> — easy to spot in explain() and "
                                 "$indexStats."),
                       ("Several at once", "createIndexes([ … ]) builds a list of index "
                                           "specifications in one command."),
                       ("dropIndexes()", "Removes all but _id_ — including unique rules like "
                                         "sku_unique.")],
               takeaway="Name every index after its collection and fields — and list before "
                        "you create or drop anything.",
               notes=[tp("What is already there",
                         "load.js ends by creating four unique indexes: sku_unique on products, "
                         "customerNumber_unique and email_unique on customers, and "
                         "orderNumber_unique on orders. "
                         "So a fresh products collection lists _id_ and sku_unique."),
                      tp("Create",
                         "createIndex takes the key specification and an options document. "
                         "The name option replaces the default category_1_price_1. "
                         "mongosh prints the index name when it succeeds."),
                      tp("Several at once",
                         "The content source creates uq_products_sku, "
                         "idx_products_category_price and idx_products_tags together with "
                         "createIndexes. "
                         "On a fresh load the SKU entry fails, because sku_unique already "
                         "covers the same key; Lab 5, Step 9 drops sku_unique first."),
                      tp("Drop",
                         "dropIndex takes a name or the key specification. "
                         "nIndexesWas 3 counts _id_, sku_unique and the new index. "
                         "dropIndexes() with no argument removes every index except _id_, "
                         "unique rules included, so confirm no query depends on them first.")]),
        F.diagram(img(14), "Hide an Index Before You Drop It",
                  "hideIndex() takes an index out of the planner's choices without deleting "
                  "it.",
                  items=[{"code": "db.products.hideIndex(\n"
                                  "  \"idx_products_category_price\")\n"
                                  "// run the queries + explain()\n"
                                  "db.products.unhideIndex(\n"
                                  "  \"idx_products_category_price\")",
                          "label": "Test a removal", "size": 11},
                         ("Hidden", "The planner ignores it; every write still maintains it."),
                         ("Visible again", "unhideIndex() restores it at once — no rebuild."),
                         {"callout": ("Unique still applies", "A hidden unique index still "
                                                              "blocks duplicates.")}],
                  takeaway="Hide, measure, then drop — hiding is instant to undo, dropping means "
                           "a rebuild.",
                  notes=dn(14)),

        # Part 3 ------------------------------------------------------------
        F.bridge(PARTS, 2, "Part 3: Compound Indexes and ESR",
                 "Real queries filter and sort on several fields.",
                 so_far=["Indexes are created, listed and dropped by name",
                         "Hide first, measure, then drop",
                         "load.js already enforces a unique sku"],
                 question="Which fields go into one index — and in what order?",
                 covers=["Compound indexes", "Why field order matters", "The prefix rule",
                         "Equality, Sort, Range", "Order history before and after",
                         "Sort direction and reverse scans", "Exercise: the fulfillment queue"],
                 notes=[tp("Why this part",
                           "Real queries rarely use one field. "
                           "The order history filters by customer and sorts by date; the catalog "
                           "filters by category and sorts by price."),
                        tp("Outcome",
                           "By the end, learners can write a compound index for a query and "
                           "defend its field order with ESR.")]),
        F.diagram(img(17), "Compound Indexes",
                  "One index, several fields: sorted by category, then by price.",
                  items=[("Sorted by the first key", "All Apparel keys, then all Footwear "
                                                     "keys."),
                         ("Then by the second", "Inside each category, price runs high to low "
                                                "because of price: -1."),
                         ("Filter + sort", "category = Apparel sorted by price is one run of "
                                           "keys."),
                         {"callout": ("Default name", "category_1_price_-1 — unless you set "
                                                      "name.")}],
                  takeaway="A compound index sorts by its first field, then the next — so one "
                           "index can filter and sort at once.",
                  notes=dn(17)),
        F.diagram(img(18), "Field Order Matters",
                  "Same two fields, two different indexes.",
                  items=[("category first", "Keys grouped by category — a category query reads "
                                            "one block."),
                         ("price first", "Categories are scattered through the price order."),
                         ("Our catalog", "It always filters by category — so category leads."),
                         {"callout": ("Same fields ≠ same index",
                                      "Choose the order from the query.")}],
                  takeaway="{ category: 1, price: 1 } and { price: 1, category: 1 } serve "
                           "different queries — field order is a design decision.",
                  notes=dn(18)),
        F.diagram(img(19), "The Prefix Rule",
                  "A compound index serves queries on its leading fields.",
                  items=[("Supported prefixes", "customerId · customerId + status · all "
                                                "three."),
                         ("Not a prefix", "status alone, or status + createdAt, skips the first "
                                          "field."),
                         ("In training_store", "status stands for paymentStatus: "
                                               "{ customerId, paymentStatus, createdAt }."),
                         {"callout": ("Redundancy", "{ customerId: 1 } adds little once this "
                                                    "index exists.")}],
                  takeaway="Queries can use a compound index through its leading fields — read "
                           "the prefixes from the left.",
                  notes=dn(19)),
        F.diagram(img(20), "Equality, Sort, Range (ESR)",
                  "A starting order for compound-index fields.",
                  items=[("E — Equality", "Exact matches first: region = East."),
                         ("S — Sort", "Then the sort field in its direction: createdAt: -1."),
                         ("R — Range", "Range conditions last: total ≥ 100."),
                         {"callout": ("A guideline", "Confirm with explain() — data can change "
                                                     "the order.")}],
                  takeaway="Equality, then Sort, then Range: the index narrows first, delivers "
                           "the order next, and scans the range last.",
                  notes=dn(20)),
        F.code("Order History: Before and After the Index",
               "Lab 5, Steps 1–3: C101's orders, newest first (explain output trimmed).",
               [{"label": "Before: no matching index", "kind": "bad", "code":
                 "db.orders.find({ customerId: cid })\n"
                 "  .sort({ createdAt: -1 })\n"
                 "  .explain(\"executionStats\")\n"
                 "\n"
                 "winningPlan: SORT\n"
                 "  inputStage: COLLSCAN\n"
                 "nReturned:          5\n"
                 "totalKeysExamined:  0\n"
                 "totalDocsExamined: 17"},
                {"label": "After: idx_orders_customer_date", "kind": "good", "code":
                 "db.orders.createIndex(\n"
                 "  { customerId: 1, createdAt: -1 },\n"
                 "  { name: \"idx_orders_customer_date\" })\n"
                 "\n"
                 "winningPlan: FETCH\n"
                 "  inputStage: IXSCAN\n"
                 "nReturned:          5\n"
                 "totalKeysExamined:  5\n"
                 "totalDocsExamined:  5"}],
               points=[("cid", "db.customers.findOne({ customerNumber: \"C101\" })._id — never "
                               "a copied ObjectId."),
                       ("Before", "All 17 orders read, then sorted in memory by the SORT "
                                  "stage."),
                       ("After", "5 keys, 5 documents, 5 orders — the index order replaces "
                                 "SORT.")],
               takeaway="Equality on customerId and a matching sort on createdAt turn 17 reads "
                        "and a sort into 5 reads in order.",
               notes=[tp("The query",
                         "Aisha Khan, C101, has five orders: O5001, O6306, O6301, O6201 and "
                         "O6101, newest first. "
                         "Look up her _id with findOne on customerNumber and store it in cid."),
                      tp("Before",
                         "On a fresh load, orders has only _id_ and orderNumber_unique, so the "
                         "plan is a collection scan of all 17 orders plus a SORT stage. "
                         "On some versions you might instead see an _id index scan with a "
                         "fetch and sort; either way the history index is missing."),
                      tp("After",
                         "The index groups keys by customerId and orders each customer's keys "
                         "by createdAt descending. "
                         "The plan becomes FETCH over IXSCAN on idx_orders_customer_date: 5 "
                         "keys, 5 documents, 5 returned, and no SORT."),
                      tp("Guide differences",
                         "The content source writes this query with orderedAt and a fixed "
                         "ObjectId; our orders use createdAt, and that ObjectId is not in the "
                         "dataset. "
                         "Older guides built the same key as idx_orders_customer_created; Lab 5 "
                         "uses one name, idx_orders_customer_date, everywhere. "
                         "MongoDB can't hold two indexes with the same key under different names, "
                         "so a second createIndex under another name fails with an "
                         "index-options conflict.")]),
        F.compare("Which Sorts Can One Index Serve?",
                  "Index { customerId: 1, createdAt: -1 }, filtering one customer.",
                  ["Sort requested", "Index walk", "SORT stage?"],
                  [("{ createdAt: -1 }", "Forward", "No"),
                   ("{ createdAt: 1 }", "Backward", "No"),
                   ("{ customerId: -1, createdAt: 1 }", "Full reverse", "No"),
                   ("{ customerId: 1, createdAt: 1 }", "Mixed directions", "Yes"),
                   ("{ createdAt: -1 }, no customer filter", "Not in date order", "Yes")],
                  [4.25, 2.15, 1.45], row_h=0.62, size=13,
                  items=[("Same or full reverse", "An index can be walked forwards or backwards "
                                                  "— never half of each."),
                         ("Mixed directions", "Need an index built in that mix, such as "
                                              "{ customerId: 1, createdAt: 1 }."),
                         {"callout": ("One field", "For a single-field index, direction "
                                                   "doesn't matter.")}],
                  takeaway="One compound index serves its own sort order and the exact reverse "
                           "— mixed directions need their own index.",
                  notes=[tp("Forward and backward",
                            "With customerId fixed by equality, the keys for that customer are "
                            "already newest first. "
                            "Walking them backwards gives oldest first, so both date sorts need "
                            "no SORT stage."),
                         tp("Full reverse",
                            "{ customerId: -1, createdAt: 1 } flips both fields, which is the "
                            "same index walked backwards."),
                         tp("Mixed",
                            "{ customerId: 1, createdAt: 1 } flips only one field. "
                            "Neither walk produces that order, so MongoDB adds a SORT."),
                         tp("No customer filter",
                            "Across all customers the keys are grouped by customer first, so "
                            "they are not in global date order. "
                            "A sort on createdAt alone needs a different index, such as "
                            "{ createdAt: -1 }.")]),
        F.exercise("Exercise: Index the Fulfillment Queue",
                   "Lab 5, Step 4: a query shape the history index can't serve.",
                   scenario="Warehouse staff list PROCESSING orders, oldest first. "
                            "idx_orders_customer_date already exists.",
                   scenario_code="db.orders.find(\n"
                                 "  { fulfillmentStatus:\n"
                                 "      \"PROCESSING\" }\n"
                                 ").sort({ createdAt: 1 })",
                   tasks=["Label the equality and the sort field",
                          "Say why idx_orders_customer_date can't help",
                          "Write the createIndex command, with a name",
                          "Predict the results and the new plan"],
                   expected=["E: fulfillmentStatus · S: createdAt",
                             "Its leading field is customerId",
                             "{ fulfillmentStatus: 1, createdAt: 1 }",
                             "Named idx_orders_fulfillment_date",
                             "O6202, O6302, O6401 — IXSCAN, no SORT"],
                   minutes=10,
                   takeaway="Every important query shape needs an index that leads with its "
                            "own equality fields.",
                   notes=[tp("How to run it",
                             "Pairs, five minutes, then compare. "
                             "If mongosh is open, run the explain before and after."),
                          tp("Why the history index can't help",
                             "Its first field is customerId, and this query doesn't filter on "
                             "customerId, so fulfillmentStatus is not a prefix."),
                          tp("The answer",
                             "db.orders.createIndex({ fulfillmentStatus: 1, createdAt: 1 }, "
                             "{ name: \"idx_orders_fulfillment_date\" }). "
                             "Equality first, then the sort in its direction."),
                          tp("The data",
                             "Three orders are PROCESSING on a fresh load: O6202 on 11 August, "
                             "O6302 on 7 September and O6401 on 18 September. "
                             "Baseline: COLLSCAN, 17 documents examined, 3 returned, with a SORT."),
                          tp("Guide difference",
                             "The content source writes this as status Processing with "
                             "orderedAt and names the index idx_orders_status_date. "
                             "Our orders use fulfillmentStatus, upper-case values and createdAt, "
                             "and Lab 5 names the index idx_orders_fulfillment_date.")]),

        # Part 4 ------------------------------------------------------------
        F.bridge(PARTS, 3, "Part 4: Specialized Index Types",
                 "Arrays, business rules, subsets and expiry.",
                 so_far=["Compound indexes sort by the first field, then the next",
                         "Queries use an index through its prefix",
                         "ESR: equality, then sort, then range"],
                 question="What if the field is an array, must be unique, or matters only for "
                          "some documents?",
                 covers=["Multikey indexes on arrays", "Unique indexes", "Partial indexes",
                         "Sparse indexes", "TTL indexes", "Text, wildcard, geospatial, hashed",
                         "Choosing the right type"],
                 notes=[tp("Why this part",
                           "Plain and compound indexes cover most queries. "
                           "Some needs are special: arrays, uniqueness, optional fields, "
                           "expiring data and word search."),
                        tp("Watch for",
                           "Each type has a rule the query must follow to use it. "
                           "Partial indexes are the clearest example.")]),
        S[24],
        F.code("Unique Indexes Enforce Business Rules",
               "A duplicate SKU is rejected by the database — not just by the application.",
               [{"label": "Rebuild with the course name", "kind": "info", "code":
                 "// load.js built sku_unique\n"
                 "db.products.dropIndex(\n"
                 "  \"sku_unique\")\n"
                 "db.products.createIndex(\n"
                 "  { sku: 1 },\n"
                 "  { unique: true,\n"
                 "    name: \"uq_products_sku\" })"},
                {"label": "A duplicate is rejected", "kind": "bad", "code":
                 "db.products.insertOne({\n"
                 "  sku: \"L100\",\n"
                 "  name: \"Duplicate SKU test\"\n"
                 "})\n"
                 "\n"
                 "MongoServerError: E11000\n"
                 "duplicate key error …\n"
                 "index: uq_products_sku\n"
                 "dup key: { sku: \"L100\" }"},
                {"label": "Case-insensitive email", "kind": "info", "code":
                 "db.customers.createIndex(\n"
                 "  { \"contact.email\": 1 },\n"
                 "  { unique: true,\n"
                 "    name:\n"
                 "     \"uq_customers_email_ci\",\n"
                 "    collation: { locale: \"en\",\n"
                 "                 strength: 2 } })"}],
               points=[("One key, one index", "Two indexes can't share { sku: 1 } — drop "
                                              "sku_unique first."),
                       ("E11000", "The insert fails and nothing is written."),
                       ("Collation", "strength: 2 ignores case; queries must use the same "
                                     "collation.")],
               takeaway="A unique index turns a business rule — one SKU, one email — into "
                        "something the database guarantees.",
               notes=[tp("Why unique",
                         "SKUs, customer numbers, order numbers and emails must never repeat. "
                         "A unique index makes the database reject the duplicate, whatever the "
                         "application does."),
                      tp("The rebuild",
                         "Lab 5, Step 9 wants the course name uq_products_sku, but load.js "
                         "already built the same key as sku_unique. "
                         "MongoDB won't create a second index on { sku: 1 } with a different "
                         "name, so drop sku_unique first. "
                         "customerNumber_unique and orderNumber_unique already enforce the other "
                         "two identity rules, so the lab checks them rather than rebuilding them."),
                      tp("The duplicate",
                         "Inserting another L100 fails with E11000 duplicate key error and "
                         "names the index and the duplicate value. "
                         "The lab's insert has more fields; they are trimmed here."),
                      tp("Case-insensitive email",
                         "priya@example.com and PRIYA@EXAMPLE.COM differ as strings. "
                         "An index with collation strength 2 compares them without case. "
                         "Our email lives at contact.email, not email as in the content source. "
                         "A query must specify the same collation to use this index."),
                      tp("If creation fails",
                         "A unique build fails when duplicates already exist. "
                         "Find them with $group on the key and $match on a count above 1, clean "
                         "them up, then build again.")]),
        F.code("Partial Indexes: Index Only What You Query",
               "Lab 5, Step 10: only active products enter this index.",
               [{"label": "Create it", "kind": "info", "code":
                 "db.products.createIndex(\n"
                 "  { category: 1, price: 1 },\n"
                 "  {\n"
                 "    name: \"idx_active_products_category_price\",\n"
                 "    partialFilterExpression: { active: true }\n"
                 "  }\n"
                 ")\n"
                 "\n"
                 "// 12 of 13 products are indexed:\n"
                 "// L190 is inactive"},
                {"label": "With and without active: true", "kind": "info", "code":
                 "// can use the partial index\n"
                 "db.products.find({ category: \"LAPTOP\",\n"
                 "  active: true,\n"
                 "  price: { $lte: Decimal128(\"2000.00\") } })\n"
                 "// → L100, L110\n"
                 "\n"
                 "// can't: L190 would be missing\n"
                 "db.products.find({ category: \"LAPTOP\",\n"
                 "  price: { $lte: Decimal128(\"2000.00\") } })"}],
               points=[("Smaller", "Fewer keys to store and to update on every write."),
                       ("The query must match", "Only queries that include active: true can "
                                                "use it."),
                       ("vs sparse", "Partial takes any filter; sparse only checks that a field "
                                     "exists.")],
               takeaway="A partial index covers only the documents the application asks for — "
                        "and only queries that ask the same can use it.",
               notes=[tp("What it does",
                         "partialFilterExpression decides which documents get index keys. "
                         "Here only active products are indexed. "
                         "In training_store that is 12 of 13: the Refurbished Laptop, L190, is "
                         "inactive."),
                      tp("The rule",
                         "A query can use a partial index only if its filter guarantees the "
                         "partial condition. "
                         "The first query includes active: true, so it can; it returns the "
                         "Business Laptop and the Ultrabook."),
                      tp("The second query",
                         "Without active: true the answer must include L190, which isn't in the "
                         "index, so MongoDB can't use it for this query."),
                      tp("Why bother",
                         "If nearly every catalog query asks for active products, the partial "
                         "index is smaller and cheaper to maintain than a full one. "
                         "The content source's example uses category Electronics; our "
                         "categories are LAPTOP, SHOE, BOOK and ACCESSORY.")]),
        F.diagram(img(28), "Sparse Indexes",
                  "Only documents that have the field get an index entry.",
                  items=[("Field present", "Indexed — Alice and Carol have a phone."),
                         ("Field missing", "No entry — Bob and David are skipped."),
                         ("training_store twist", "C204's phone is null: it exists, so it's "
                                                  "indexed. C515 has none."),
                         {"callout": ("Prefer partial", "A partial filter on $exists says the "
                                                        "same, explicitly.")}],
                  takeaway="Sparse indexes skip documents without the field — partial indexes "
                           "do the same job with a clearer rule.",
                  notes=dn(28)),
        F.code("TTL Indexes Remove Expired Documents",
               "Lab 5, Step 10: a dedicated sessions collection — never orders.",
               [{"label": "Sessions that expire", "kind": "info", "code":
                 "db.sessions.insertMany([\n"
                 "  { sessionId: \"S1\", user: \"aisha\",\n"
                 "    expiresAt: new Date(\n"
                 "      Date.now() + 60 * 60 * 1000) },\n"
                 "  { sessionId: \"S-EXPIRED\",\n"
                 "    user: \"temp\",\n"
                 "    expiresAt: new Date(\n"
                 "      Date.now() - 60 * 1000) }\n"
                 "])"},
                {"label": "The TTL index", "kind": "good", "code":
                 "db.sessions.createIndex(\n"
                 "  { expiresAt: 1 },\n"
                 "  { expireAfterSeconds: 0,\n"
                 "    name: \"ttl_sessions_expires_at\" })\n"
                 "\n"
                 "// about 60 s later the TTL monitor\n"
                 "// deletes S-EXPIRED; S1 stays"}],
               points=[("expireAfterSeconds: 0", "Each document expires at its own expiresAt "
                                                 "date."),
                       ("Not instant", "A background task runs about every 60 seconds."),
                       ("Never for records you keep", "Orders, payments and audit data stay "
                                                      "out of TTL.")],
               takeaway="A TTL index deletes expired documents for you — use it only for data "
                        "that is meant to disappear.",
               notes=[tp("The setup",
                         "Lab 5, Step 10 creates a separate sessions collection with two "
                         "documents: S1 expires in an hour, S-EXPIRED expired a minute ago."),
                      tp("The index",
                         "A TTL index is a single-field index on a date field with "
                         "expireAfterSeconds. "
                         "With 0, each document expires exactly at the date it stores. "
                         "Lab 5 names it ttl_sessions_expires_at; the content source spells "
                         "it ttl_sessions_expiresAt. We follow the lab."),
                      tp("Asynchronous",
                         "Right after the insert both documents are there. "
                         "The TTL monitor runs about once a minute, so S-EXPIRED disappears "
                         "some time later, not at an exact instant."),
                      tp("Where it belongs",
                         "Sessions, verification codes and short-lived events. "
                         "Never orders, payments or anything you must keep for legal or audit "
                         "reasons.")]),
        F.diagram(img(31), "Text, Wildcard, Geospatial and Hashed",
                  "Four specialized types for four special query shapes.",
                  items=[("Text", "$text word search — on name, since our products have no "
                                  "description."),
                         ("Wildcard", "{ \"attributes.$**\": 1 } — our attributes differ by "
                                      "category."),
                         ("Geospatial", "2dsphere on GeoJSON points, longitude first; "
                                        "$near."),
                         ("Hashed", "Equality only; spreads values for hashed sharding — "
                                    "Module 7.")],
                  takeaway="Specialized indexes serve special query shapes — word search, "
                           "dynamic fields, location and shard distribution.",
                  notes=dn(31)),
        F.compare("Choosing the Right Index Type",
                  "Start from what the query must do.",
                  ["The query must…", "Index type", "training_store example"],
                  [("Match or sort one field", "Single-field", "{ sku: 1 }"),
                   ("Filter and sort on several", "Compound", "{ customerId: 1, createdAt: -1 }"),
                   ("Forbid duplicates", "Unique", "sku, customerNumber, orderNumber"),
                   ("Match array values", "Multikey", "{ tags: 1 }"),
                   ("Cover some documents only", "Partial", "active: true products"),
                   ("Skip a missing field", "Sparse", "contact.phone"),
                   ("Expire documents", "TTL", "sessions.expiresAt"),
                   ("Search words / dynamic paths", "Text / Wildcard", "name / attributes.$**")],
                  [2.95, 1.75, 3.55], row_h=0.50, size=13,
                  items=[("Location and sharding", "2dsphere for coordinates; hashed for "
                                                   "hashed shard keys."),
                         ("One index, many shapes", "A compound index often serves several "
                                                    "queries through its prefix."),
                         {"callout": ("Rule", "Pick the type from the query, not from the "
                                              "field.")}],
                  takeaway="Name the query's job first — the index type follows from it.",
                  notes=[tp("How to use the table",
                            "Read it left to right: what the query must do, the index type, and "
                            "where training_store uses it."),
                         tp("Combinations",
                            "Types combine. "
                            "idx_active_products_category_price is compound and partial; "
                            "uq_products_sku is single-field and unique; idx_products_tags is "
                            "single-field and multikey."),
                         tp("Practice",
                            "Ask the class to match eight requirements to these types: unique "
                            "SKU, active-only, an optional discountCode, session expiry, word "
                            "search, attribute paths, nearby stores and a hashed tenantId. "
                            "Exercise 6.3 at the end of the module applies these types to ten "
                            "workloads.")]),

        # Part 5 ------------------------------------------------------------
        F.bridge(PARTS, 4, "Part 5: explain() and Covered Queries",
                 "Stop guessing — read the plan.",
                 so_far=["Arrays get multikey indexes automatically",
                         "Unique, partial, sparse and TTL add rules and limits",
                         "The query decides the index type"],
                 question="How do we prove an index works — and when can a query skip the "
                          "documents entirely?",
                 covers=["explain() verbosity modes", "Reading executionStats",
                         "Spotting a blocking sort", "Covered queries",
                         "Proving coverage in mongosh", "Exercise: diagnose three plans"],
                 notes=[tp("Why this part",
                           "Every earlier slide claimed a plan. "
                           "This part shows how to check the claim yourself."),
                        tp("Watch for",
                           "Three numbers read together: nReturned, totalKeysExamined and "
                           "totalDocsExamined. "
                           "One stage to watch for: SORT.")]),
        F.diagram(img(44), "explain(): Three Levels of Detail",
                  "queryPlanner, executionStats and allPlansExecution.",
                  items=[("queryPlanner", "The winning plan only — the query isn't run."),
                         ("executionStats", "Runs the winning plan: returned, keys and documents "
                                            "examined, time."),
                         ("allPlansExecution", "Adds the candidate plans the planner tried and "
                                               "rejected."),
                         {"callout": ("For tuning", "explain(\"executionStats\") — as in every "
                                                    "lab.")}],
                  takeaway="explain() shows the plan; executionStats shows what that plan "
                           "actually cost.",
                  notes=dn(44)),
        F.code("Reading executionStats",
               "Lab 5, Step 7: active accessories by price, with "
               "idx_products_category_active_price.",
               [{"label": "The query and its plan (trimmed)", "kind": "good", "code":
                 "db.products.find(\n"
                 "  { category: \"ACCESSORY\", active: true }\n"
                 ").sort({ price: 1 }).explain(\"executionStats\")\n"
                 "\n"
                 "queryPlanner.winningPlan:\n"
                 "  stage: \"FETCH\"\n"
                 "  inputStage:\n"
                 "    stage: \"IXSCAN\"\n"
                 "    indexName: \"idx_products_category_active_price\"\n"
                 "executionStats:\n"
                 "  nReturned: 5\n"
                 "  totalKeysExamined: 5\n"
                 "  totalDocsExamined: 5"}],
               points=[("winningPlan", "FETCH over IXSCAN: keys first, then the matching "
                                       "documents. No SORT."),
                       ("Keys : docs : returned", "5 : 5 : 5 — nothing wasted."),
                       ("Before the index", "SORT over COLLSCAN: 0 keys, 13 documents, 5 "
                                            "returned."),
                       {"callout": ("XBAD", "Its price is the string \"49.99\" — it matches, and "
                                            "sorts after the numbers.")}],
               mode="left", left_w=7.70,
               takeaway="Read the stage path first, then compare keys and documents examined "
                        "with documents returned.",
               notes=[tp("The index",
                         "Lab 5, Step 7 creates { category: 1, active: 1, price: 1 } as "
                         "idx_products_category_active_price. "
                         "category and active are equality, price is the sort."),
                      tp("Reading the plan",
                         "Read winningPlan from the inside out: IXSCAN walks the index, FETCH "
                         "reads each document. "
                         "There is no SORT stage, because the keys are already in price order."),
                      tp("The counts",
                         "Five keys, five documents, five returned: the Wireless Mouse, USB Hub, "
                         "Wireless Keyboard, Docking Station, and the Legacy Cable Pack."),
                      tp("A dataset trap",
                         "XBAD stores its price as the string \"49.99\", a Module 4 fixture. "
                         "It still matches category and active, and strings sort after numbers, "
                         "so it comes last. "
                         "A range such as price ≤ 100 would skip it."),
                      tp("The baseline",
                         "On a fresh load the same query is SORT over COLLSCAN: 0 keys, all 13 "
                         "products examined, 5 returned. "
                         "Lab 5, Step 7 records that baseline first. "
                         "Older sample output shows 4 returned; on the live data it's 5, "
                         "because XBAD counts.")]),
        F.diagram(img(48), "Spotting a Blocking Sort",
                  "A SORT stage means documents were sorted in memory.",
                  items=[("The signal", "stage: SORT above COLLSCAN or IXSCAN in "
                                        "winningPlan."),
                         ("Why it hurts", "Every match is held and sorted before the first "
                                          "result returns."),
                         ("The fix", "An index whose order matches the sort — after the "
                                     "equality fields."),
                         {"callout": ("Memory", "Large sorts use up to 100 MB, then spill to "
                                                "disk.")}],
                  takeaway="A SORT stage is a missing or mis-ordered index — fix the index, not "
                           "the query.",
                  notes=dn(48)),
        F.diagram(img(36), "Covered Queries",
                  "When the index holds every field the query needs, no document is read.",
                  items=[("Filter in the index", "category is the first key."),
                         ("Output in the index", "name and price are keys too."),
                         ("_id excluded", "_id isn't in the index, so the projection sets "
                                          "_id: 0."),
                         {"callout": ("The signal", "IXSCAN with no FETCH; totalDocsExamined: "
                                                    "0.")}],
                  takeaway="A covered query answers from the index alone — every filtered and "
                           "returned field must be in it.",
                  notes=dn(36)),
        F.code("Proving Coverage in mongosh",
               "Lab 5, Step 11: idx_products_category_price_name on the two books (trimmed).",
               [{"label": "Covered", "kind": "good", "code":
                 "db.products.createIndex(\n"
                 "  { category: 1, price: 1, name: 1 },\n"
                 "  { name: \"idx_products_category_price_name\" })\n"
                 "\n"
                 "db.products.find({ category: \"BOOK\" },\n"
                 "  { _id: 0, name: 1, price: 1 })\n"
                 "\n"
                 "stage: PROJECTION_COVERED\n"
                 "  inputStage: IXSCAN\n"
                 "totalDocsExamined: 0"},
                {"label": "Not covered", "kind": "bad", "code":
                 "// _id comes back by default\n"
                 "db.products.find({ category: \"BOOK\" },\n"
                 "  { name: 1, price: 1 })\n"
                 "\n"
                 "// tags isn't in the index\n"
                 "db.products.find({ category: \"BOOK\" },\n"
                 "  { _id: 0, name: 1, tags: 1 })\n"
                 "\n"
                 "stage: PROJECTION_SIMPLE\n"
                 "  inputStage: FETCH\n"
                 "totalDocsExamined: 2"}],
               points=[("Three conditions", "Filter indexed · output indexed · _id excluded or "
                                            "indexed."),
                       ("The result", "Query Cookbook 39.99, then MongoDB Fundamentals 59.99."),
                       ("Arrays", "A multikey field such as tags can't be covered.")],
               takeaway="Confirm coverage with explain() — IXSCAN with no FETCH and zero "
                        "documents examined.",
               notes=[tp("The covered query",
                         "Filter on category, return name and price, and switch _id off. "
                         "All three fields are in idx_products_category_price_name, so the plan "
                         "is PROJECTION_COVERED over IXSCAN: 2 keys, 0 documents, 2 returned."),
                      tp("Results",
                         "The index is ordered by price inside BOOK, so the output is Query "
                         "Cookbook at 39.99, then MongoDB Fundamentals at 59.99."),
                      tp("Breaking coverage",
                         "Leaving _id on, or asking for tags, needs a field that isn't in the "
                         "index. "
                         "The plan gains a FETCH and totalDocsExamined becomes 2."),
                      tp("Field order",
                         "The index is { category, price, name }. "
                         "Coverage needs the fields to be present; their order still matters "
                         "for which filters and sorts the index serves.")]),
        F.exercise("Exercise: Diagnose Three Plans",
                   "Read the numbers, name the problem, propose the fix.",
                   scenario="Three explain(\"executionStats\") summaries on a fresh "
                            "training_store. A: name \"USB Hub\". B: PROCESSING orders by "
                            "date. C: tags \"wireless\".",
                   scenario_code="A  COLLSCAN\n"
                                 "   keys 0 · docs 13 · returned 1\n"
                                 "B  SORT ← COLLSCAN\n"
                                 "   keys 0 · docs 17 · returned 3\n"
                                 "C  FETCH ← IXSCAN idx_products_tags\n"
                                 "   keys 2 · docs 2 · returned 2",
                   tasks=["Mark each plan targeted or wasteful",
                          "Propose a fix for A",
                          "Propose a fix for B",
                          "Say why C needs no change"],
                   expected=["A and B wasteful · C targeted",
                             "A: index name, or query by sku",
                             "B: idx_orders_fulfillment_date",
                             "B's SORT disappears with it",
                             "C: 2 : 2 : 2 already"],
                   minutes=10,
                   takeaway="Read stage, keys, documents and returned together — any one alone "
                            "can mislead.",
                   notes=[tp("How to run it",
                             "Individually for three minutes, then discuss. "
                             "Ask for the ratio of documents examined to returned for each "
                             "plan."),
                          tp("Plan A",
                             "13 products read for one USB Hub. "
                             "Either index name, if the application really searches by name, or "
                             "change the query to use sku, which is already uniquely indexed."),
                          tp("Plan B",
                             "All 17 orders read and sorted in memory for 3 results. "
                             "idx_orders_fulfillment_date gives an IXSCAN with 3 keys and no "
                             "SORT."),
                          tp("Plan C",
                             "Two keys, two documents, two results: the Wireless Keyboard and the "
                             "Wireless Mouse. "
                             "It is already as good as it gets."),
                          tp("One more case",
                             "Add a fourth plan out loud: an IXSCAN that examines 50,000 keys for "
                             "10 results. "
                             "Using an index doesn't make a plan efficient; the key order may be "
                             "wrong or not selective.")]),

        # Part 6 ------------------------------------------------------------
        F.bridge(PARTS, 5, "Part 6: Selectivity, Costs and Common Mistakes",
                 "Every index is a trade-off.",
                 so_far=["explain(\"executionStats\") proves what a query did",
                         "A SORT stage means an in-memory sort",
                         "Covered queries skip the documents entirely"],
                 question="Is every index worth what it costs — and how do we keep the set "
                          "healthy?",
                 covers=["Index selectivity", "Write, storage and memory costs",
                         "Usage statistics with $indexStats",
                         "Changing indexes safely in production", "Common indexing mistakes",
                         "An indexing strategy for training_store"],
                 notes=[tp("Why this part",
                           "So far every index made a query faster. "
                           "Now we count what indexes cost and how to keep only the useful "
                           "ones."),
                        tp("Outcome",
                           "Learners can audit an index list and recommend retain, redesign or "
                           "remove, with evidence.")]),
        F.diagram(img(37), "Index Selectivity",
                  "The more distinct values, the fewer keys a lookup scans.",
                  items=[("High", "sku: 13 distinct values in 13 products — one key per "
                                  "lookup."),
                         ("Low", "active: 12 of 13 products are true — barely narrows the "
                                 "search."),
                         ("Combine", "Put low-selectivity fields in a compound or partial "
                                     "index."),
                         {"callout": ("Measure", "Selectivity comes from your data — check it "
                                                 "with explain().")}],
                  takeaway="An index narrows a search only as much as its values do — lead with "
                           "fields that really narrow it.",
                  notes=dn(37)),
        F.diagram(img(54), "Every Index Costs Writes",
                  "Each insert or update also updates the indexes it touches.",
                  items=[("Write path", "One order insert updates the document, _id_, "
                                        "orderNumber_unique and every secondary index."),
                         ("Storage and memory", "Indexes take disk space and compete for RAM "
                                                "with the data."),
                         ("Updates", "Changing an indexed field rewrites its index keys."),
                         {"callout": ("Balance", "Keep indexes that serve real, frequent "
                                                 "queries.")}],
                  takeaway="Every index speeds some reads and slows every write — keep the ones "
                           "that earn their cost.",
                  notes=dn(54)),
        F.diagram(img(50), "Index Usage Statistics",
                  "$indexStats counts how often each index was used.",
                  items=[{"code": "db.products.aggregate([\n"
                                  "  { $indexStats: {} }\n"
                                  "]).map(s => ({ name: s.name,\n"
                                  "  ops: s.accesses.ops }))",
                          "label": "Usage per index", "size": 11},
                         ("ops > 0", "The planner is using the index."),
                         ("ops = 0", "Review it: hide, measure, then decide."),
                         {"callout": ("Since restart", "Counters reset when mongod "
                                                       "restarts.")}],
                  takeaway="$indexStats shows which indexes earn their keep — zero uses starts "
                           "an investigation, not a drop.",
                  notes=dn(50)),
        F.diagram(img(57), "Changing Indexes Safely in Production",
                  "Analyze, test, build, monitor, confirm — with a rollback ready.",
                  items=[("Analyze and test", "explain() and $indexStats; try it on staging "
                                              "data first."),
                         ("Build and monitor", "Build in a change window; watch CPU, I/O and "
                                               "latency."),
                         ("Rollback", "If it degrades, drop the new index — keep the "
                                      "createIndex command."),
                         {"callout": ("Removing", "Hide first; drop only when the queries stay "
                                                  "healthy.")}],
                  takeaway="Treat every index change as a production change: measured, "
                           "monitored and reversible.",
                  notes=dn(57)),
        F.diagram(img(59), "Common Indexing Mistakes",
                  "Too many, wrong order, never used — and the query-aligned fix.",
                  items=[("Too many indexes", "Every extra index slows writes and uses RAM."),
                         ("Wrong field order", "{ createdAt, status } can't serve status + "
                                               "newest first."),
                         ("Unused indexes", "$indexStats ops = 0 — review them."),
                         ("Also avoid", "hint() as a permanent fix · timing tiny data · "
                                        "trusting any IXSCAN.")],
                  takeaway="Index the real query shapes, in ESR order — and review what nothing "
                           "uses.",
                  notes=dn(59)),
        F.diagram(img(61), "An Indexing Strategy for training_store",
                  "One index per important query shape — plus the integrity rules.",
                  items=[("products", "{ category: 1, price: 1 } for the catalog; unique sku."),
                         ("customers", "Unique contact.email — the diagram shortens it to "
                                       "email."),
                         ("orders", "{ customerId: 1, createdAt: -1 } for order history."),
                         ("reviews", "{ productId: 1, rating: -1 } for top ratings — or "
                                     "createdAt: -1 for newest.")],
                  takeaway="A small set of query-aligned indexes gives fast reads with "
                           "controlled writes.",
                  notes=dn(61)),

        # Wrap-up ------------------------------------------------------------
        F.diagram(img(62), "Module 6 at a Glance",
                  "Query patterns → choose index → validate plan → monitor usage → tune.",
                  takeaway="Start from the query, prove the index with explain(), and keep "
                           "reviewing what the index set costs.",
                  notes=dn(62)),
        F.knowledge("Knowledge Check", "Answer in your own words — then compare with a partner.",
                    ["What does a COLLSCAN stage tell you?",
                     "Which index does every collection have?",
                     "Why does field order matter in a compound index?",
                     "What does ESR stand for, and what is it for?",
                     "What makes an index on tags multikey?",
                     "How is a partial index different from a sparse one?",
                     "Why should a TTL index never go on orders?",
                     "Which three explain() numbers do you compare?",
                     "What three conditions make a query covered?",
                     "Why hide an index before dropping it?"],
                    notes=[tp("1. COLLSCAN",
                              "No usable index: MongoDB read every document in the collection "
                              "and tested the filter on each one."),
                           tp("2. Every collection",
                              "The unique _id index, named _id_. It can't be dropped."),
                           tp("3. Field order",
                              "The index is sorted by its first field, then the next. "
                              "{ category: 1, price: 1 } serves category queries; "
                              "{ price: 1, category: 1 } scatters each category through the "
                              "price order. Same fields, different index."),
                           tp("4. ESR",
                              "Equality, Sort, Range: a starting order for compound-index "
                              "fields. Check it with explain()."),
                           tp("5. Multikey",
                              "tags is an array, so MongoDB stores one key per array value and "
                              "sets multikey: true automatically."),
                           tp("6. Partial versus sparse",
                              "Partial indexes documents that match any filter expression. "
                              "Sparse only skips documents that lack the field."),
                           tp("7. TTL on orders",
                              "TTL deletes documents automatically. Orders must be kept for "
                              "business, legal and audit reasons."),
                           tp("8. explain() numbers",
                              "nReturned, totalKeysExamined and totalDocsExamined, together "
                              "with the stage path, especially SORT."),
                           tp("9. Covered",
                              "Filter fields indexed, returned fields indexed, and _id "
                              "excluded or indexed. Confirm: IXSCAN with no FETCH."),
                           tp("10. Hide first",
                              "Hiding is instant to undo and keeps the index maintained. "
                              "Dropping means a full rebuild if a query turns out to need "
                              "it.")]),
        F.exercise("Exercise 6.1 — Apply Equality–Sort–Range",
                   "Module 6 checkpoint A: three query shapes, three compound indexes.",
                   kind="OFFICIAL CHECKPOINT A", minutes=15,
                   worksheet="labs/day-03/exercises/exercise-6.1-apply-equality-sort-range"
                             ".md",
                   scenario="Label equality, sort and range in each shape, then propose one "
                            "compound index per shape.",
                   scenario_code="A  products: ACCESSORY, active,\n"
                                 "   price ≤ 100, sort by price\n"
                                 "B  orders: one customerId,\n"
                                 "   createdAt in a date range,\n"
                                 "   sort createdAt descending\n"
                                 "C  orders: paymentStatus PAID,\n"
                                 "   createdAt ≥ start, sort desc",
                   tasks=["Label E, S and R in shape A",
                          "Label shape B — spot the shared field",
                          "Propose one index per shape",
                          "Say why paymentStatus leads in C"],
                   expected=["A { category: 1, active: 1, price: 1 }",
                             "B { customerId: 1, createdAt: -1 }",
                             "C { paymentStatus: 1, createdAt: -1 }",
                             "Equality first partitions the keys",
                             "No index leads with a range"],
                   expected_title="Solution (after debrief)",
                   takeaway="ESR gives a strong first design — equality narrows, sort orders, "
                            "range scans last.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 6.1. The worksheet is "
                             "labs/day-03/exercises/exercise-6.1-apply-equality-sort-range.md; "
                             "the answer key is in its solution folder. "
                             "It is a discussion exercise; mongosh is optional."),
                          tp("Shape A",
                             "category and active are equality, price is both the sort and the "
                             "range. "
                             "{ category: 1, active: 1, price: 1 } is the same index Lab 5, "
                             "Step 7 builds as idx_products_category_active_price. "
                             "On a fresh load it returns the Wireless Mouse, USB Hub and Wireless "
                             "Keyboard; XBAD's string price is outside a numeric range."),
                          tp("Shape B",
                             "customerId is equality; createdAt is both the sort and the range, "
                             "so it appears once: { customerId: 1, createdAt: -1 }."),
                          tp("Shape C",
                             "{ paymentStatus: 1, createdAt: -1 }. "
                             "paymentStatus has only a few values, but putting equality first "
                             "means the date sort and range walk one status's keys instead of "
                             "mixing statuses. Lab 5, Step 12 builds it as "
                             "idx_orders_payment_created.")]),
        F.exercise("Exercise 6.2 — Identify Covered Queries",
                   "Module 6 checkpoint B: which projections can the index answer alone?",
                   kind="OFFICIAL CHECKPOINT B", minutes=15,
                   worksheet="labs/day-03/exercises/exercise-6.2-identify-covered-queries"
                             ".md",
                   scenario="The index { category: 1, price: 1, name: 1 } exists. Decide which "
                            "queries can be covered.",
                   scenario_code="Q1 find({ category: \"BOOK\" },\n"
                                 "     { _id: 0, name: 1, price: 1 })\n"
                                 "Q2 find({ category: \"BOOK\" },\n"
                                 "     { _id: 0, name: 1, price: 1,\n"
                                 "       tags: 1 })\n"
                                 "Q3 find({ category: \"BOOK\" },\n"
                                 "     { name: 1 })",
                   tasks=["Decide coverage for Q1",
                          "Decide coverage for Q2 and Q3",
                          "Write the three coverage conditions",
                          "Name the explain() signal to look for"],
                   expected=["Q1 may be covered",
                             "Q2 not — tags needs a FETCH",
                             "Q3 not — _id returns by default",
                             "Filter, output, _id handled",
                             "IXSCAN with no FETCH"],
                   expected_title="Solution (after debrief)",
                   takeaway="A covered query needs every filtered and returned field in the index "
                            "— including the decision about _id.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 6.2. The worksheet is "
                             "labs/day-03/exercises/exercise-6.2-identify-covered-queries.md. "
                             "Lab 5, Step 11 lets learners test the answers in mongosh."),
                          tp("Q1",
                             "Filter on category, output name and price, _id off: every field is "
                             "in the index, so it can be covered."),
                          tp("Q2 and Q3",
                             "Q2 asks for tags, which isn't in the index, so MongoDB must fetch "
                             "the documents. "
                             "Q3 leaves _id on by default, and _id isn't in the index, so it "
                             "fetches too."),
                          tp("The rule and the signal",
                             "Filter fields indexed, returned fields indexed, _id excluded or "
                             "indexed. "
                             "Confirm with explain: IXSCAN and no FETCH, "
                             "PROJECTION_COVERED, and totalDocsExamined 0.")]),
        F.exercise("Exercise 6.3 — E-Commerce Index Review",
                   "Module 6 checkpoint C: an index recommendation for ten workloads.",
                   kind="OFFICIAL CHECKPOINT C", minutes="30–45",
                   worksheet="labs/day-03/exercises/exercise-6.3-e-commerce-index-review.md",
                   scenario="Recommend indexes for ten recurring training_store workloads.",
                   scenario_code=" 1 SKU lookup      6 order history\n"
                                 " 2 category browse 7 paid reporting\n"
                                 " 3 tag search      8 newest reviews\n"
                                 " 4 email lookup    9 session expiry\n"
                                 " 5 order number   10 dynamic attrs",
                   tasks=["Tabulate shape and index for all ten",
                          "Mark unique, multikey, partial, TTL, wildcard",
                          "Give ESR roles and a cost note per compound",
                          "Flag an overlap; plan validation and rollback"],
                   expected=["A ten-row table",
                             "uq_products_sku, idx_products_tags",
                             "TTL on sessions · wildcard attributes",
                             "Overlap: category vs category + active + price",
                             "Baseline → create → explain → rollback"],
                   expected_title="Solution (after debrief)",
                   takeaway="A good index plan names the query, the index, its cost and how to "
                            "prove it — and how to undo it.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 6.3, the module's practical "
                             "challenge. The worksheet is "
                             "labs/day-03/exercises/exercise-6.3-e-commerce-index-review.md. "
                             "Allow 30 to 45 minutes."),
                          tp("Expected table",
                             "SKU: unique sku. Category browse: { category: 1, active: 1, "
                             "price: 1 }, or partial on active. Tags: multikey. Email: unique "
                             "contact.email. Order number: unique orderNumber. History: "
                             "{ customerId: 1, createdAt: -1 }. Paid reporting: { paymentStatus: "
                             "1, createdAt: -1 }. Reviews: { productId: 1, createdAt: -1 }. "
                             "Sessions: TTL on expiresAt. Attributes: wildcard attributes.$**."),
                          tp("Overlap",
                             "A single { category: 1 } index overlaps with every category-leading "
                             "compound. Plan: hide it, measure, then decide."),
                          tp("Validation",
                             "For the catalog and history indexes: baseline explain, createIndex, "
                             "explain again, compare examined with returned and check that SORT "
                             "is gone. Rollback is dropIndex by name, with the createIndex "
                             "command saved.")]),
        F.custom(_lab5, "Lab 5 — Index and Explain",
                 "Day 3 official lab: measure, index and measure again on a fresh "
                 "training_store.",
                 takeaway="Record the plan shape and the counts before and after every index — "
                          "that evidence is the lab.",
                 notes=[tp("Official lab",
                           "This is Day 3 Lab 5, labs/day-03/lab5/LAB-5-GUIDE.md; expected "
                           "explain excerpts are in lab5/solution/LAB-5-SOLUTION.md. "
                           "Reload training_store first so Lab 3's writes are gone, then work "
                           "through the six core steps."),
                        tp("Steps 1 to 3",
                           "Baseline explain of C101's order history, create "
                           "idx_orders_customer_date, and explain again. "
                           "Expect SORT over COLLSCAN before, IXSCAN with 5 keys and 5 documents "
                           "after."),
                        tp("Steps 4 and 5",
                           "The PROCESSING queue needs idx_orders_fulfillment_date: 3 orders. "
                           "The tags index is multikey; wireless matches P1001 and A410."),
                        tp("Step 6",
                           "Inventory every index: products has sku_unique, customers has "
                           "customerNumber_unique and email_unique, orders has "
                           "orderNumber_unique, plus the three indexes created in Steps 2, 4 "
                           "and 5. "
                           "Don't drop the unique identity indexes."),
                        tp("Go further",
                           "Steps 7 to 13 fold in the extra module practice: the catalog index "
                           "and its prefixes, a nested-field lookup, unique SKUs, partial and "
                           "TTL indexes, a covered query, an aggregation, and a hide-and-test "
                           "audit with $indexStats."),
                        tp("Data notes",
                           "A fresh load has 13 products, including the XBAD fixture, and 17 "
                           "orders. "
                           "Never copy the ObjectId shown in older slides; it isn't in this "
                           "dataset.")]),
        F.wrapup("Module 6 Summary and What's Next",
                 "From a collection scan to a small, proven set of indexes.",
                 can=["Explain COLLSCAN, IXSCAN, FETCH and SORT",
                      "Create, list, hide and drop named indexes",
                      "Order compound fields with ESR and prefixes",
                      "Choose multikey, unique, partial, sparse and TTL",
                      "Read explain() and build a covered query",
                      "Weigh selectivity, write cost and index usage"],
                 next_title="Next: Module 7 — Replication and Sharding",
                 questions=["How do replica sets keep data available?",
                            "How does sharding split a collection?",
                            "Why does a shard key need an index?"],
                 bring=("Bring along", "Your Lab 5 index inventory and the explain() numbers "
                                       "you recorded before and after each index."),
                 takeaway="Fast queries on one server come first — Module 7 keeps them "
                          "available and spreads them across many.",
                 notes=[tp("Recap",
                           "We moved from collection scans to index scans, managed named indexes, "
                           "designed compound indexes with ESR, used specialized types, read "
                           "explain() and covered a query, and weighed what indexes cost."),
                        tp("Next module",
                           "Module 7 answers the next Day 3 questions: how replica sets keep "
                           "data available through a failure, and how sharding spreads a "
                           "collection across servers."),
                        tp("The link",
                           "Every sharded collection needs an index that supports its shard key, "
                           "and hashed indexes, which we met today, support hashed sharding. "
                           "Good indexes still matter on every shard.")]),
    ]
