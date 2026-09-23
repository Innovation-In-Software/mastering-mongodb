#!/usr/bin/env python3
"""Build the new-content Module 4 deck: The MongoDB Query Language.

Content comes from scripts/module04_content_source.md, the Module 4 manifest,
the official Exercises 4.1-4.4, Day 2 Lab 3 and the training_store sample
database (datasets/training_store/load.js). Every query result on the slides and
in the notes is the result on a fresh load of that dataset. Styling reuses the
house kit through mdb_deck_kit (read-only): title block, red/black rail, footer,
page numbers, key-takeaway bar, fonts and colours. Hand-drawn visuals are
native, editable PowerPoint shapes; concept diagrams come from
scripts/new_content/diagrams/module04/.

Writes decks/pptx_new/MongoDB_Module04_The_MongoDB_Query_Language.pptx and
never touches decks/pptx/.

    python scripts/new_content/build_module04_new.py
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

from pptx.enum.shapes import MSO_SHAPE  # noqa: E402
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN  # noqa: E402

import mdb_deck_kit as K  # noqa: E402
import mdb_flow_slides as F  # noqa: E402
import mdb_speaker_notes as SN  # noqa: E402
import mdb_visuals as V  # noqa: E402
from mdb_visuals import (  # noqa: E402
    BLACK, DARK_GRAY, GREEN, INK, LEFT, LIGHT_GRAY, LIGHT_GREEN, LIGHT_NAVY, LIGHT_RED,
    MUTED, NAVY, ORANGE, PURPLE, RED, RIGHT, TEAL, WHITE, WIDTH,
)
from module04_notes import NOTES  # noqa: E402

ROOT = HERE.parents[1]
OUT = ROOT / "decks" / "pptx_new" / "MongoDB_Module04_The_MongoDB_Query_Language.pptx"
MODULE_LABEL = "MODULE 4"


def notes(n: int) -> str:
    return SN.compose(NOTES[n])


def new(prs, layout, n, title, subtitle):
    return V.content_slide(prs, layout, number=n, title=title, subtitle=subtitle)


def done(slide, n, takeaway):
    V.finish(slide, number=n, takeaway=takeaway, notes=notes(n))


# ---------------------------------------------------------------------------
def s01(prs, layout):
    slide = K._chapter_slide(
        prs, layout, tag=MODULE_LABEL, title="The MongoDB Query Language",
        subtitle="Read, filter, shape, insert, update, upsert and delete training_store "
                 "documents — and prove every write did what you meant.",
        quote='"Filters choose documents; projections choose fields."',
        module_label=MODULE_LABEL,
    )
    V.set_slide_label("slide 1")
    topics = [
        ("Read and filter", NAVY),
        ("Query operators", PURPLE),
        ("Nested fields and arrays", TEAL),
        ("Insert, update, upsert", GREEN),
        ("Delete and verify", ORANGE),
    ]
    w, gap = 2.34, 0.15
    for i, (label, fill) in enumerate(topics):
        x = LEFT + i * (w + gap)
        V.box(slide, x, 5.15, w, 0.95, label, fill=fill, size=15, radius=0.12, margin=0.14)
    K.set_notes(slide, notes(1))


def s02(prs, layout):
    n = 2
    slide, top = new(prs, layout, n, "Learning Objectives",
                     "What you will be able to do by the end of this module.")
    V.panel(slide, LEFT, top + 0.05, 5.9, "By the end of this module, you can", [
        "1. Read documents with find() and findOne()",
        "2. Shape results: project, sort, page, count",
        "3. Combine comparison and logical operators",
        "4. Query nested fields and arrays",
        "5. Insert, update, upsert and replace",
        "6. Delete safely and read write results",
    ], icon="🎯", badge_color=RED, size=16)

    x = 6.75
    y = V.section(slide, x, top + 0.05, 6.05, "Six questions this module answers", icon="❓",
                  fill=NAVY)
    questions = [
        ("WHICH", "documents does my filter match?", NAVY),
        ("WHAT", "fields should come back?", PURPLE),
        ("HOW", "do operators combine?", TEAL),
        ("WHEN", "is $elemMatch required?", ORANGE),
        ("HOW", "do I change only what I mean?", GREEN),
        ("HOW", "do I prove a write was right?", RED),
    ]
    row_h, gap = 0.50, 0.09
    for i, (word, rest, fill) in enumerate(questions):
        ry = y + i * (row_h + gap)
        V.box(slide, x, ry, 2.05, row_h, word, fill=fill, size=13)
        V.text(slide, x + 2.2, ry, 3.85, row_h, rest, size=14, anchor=MSO_ANCHOR.MIDDLE)

    V.section(slide, LEFT, 5.02, WIDTH, "Module roadmap", icon="🗺️", fill=PURPLE)
    V.chevrons(slide, LEFT, 5.50, WIDTH, 0.80,
               ["Filters", "Shape results", "Operators", "Arrays", "Insert, update",
                "Upsert, replace", "Delete, verify"],
               [NAVY, PURPLE, TEAL, ORANGE, GREEN, RED, BLACK], size=13)
    done(slide, n, "A good query starts from the real field names, values and BSON types in "
                   "the documents.")


def s50(prs, layout):
    """Demo 4.2: build one filter a condition at a time, counting after each step."""
    n = len(prs.slides) + 1
    slide, top = new(prs, layout, n, "Build a Filter One Condition at a Time",
                     "Demo 4.2 on products: add one condition, count, and explain the "
                     "number.")
    y0, y1 = top + 0.10, V.BODY_BOTTOM
    lw = 8.05
    V.text(slide, LEFT, y0, 4.8, 0.34, "FILTER SO FAR", size=13, bold=True, color=NAVY)
    V.text(slide, LEFT + 4.95, y0, 3.1, 0.34, "COUNT  ·  WHO IS LEFT", size=13, bold=True,
           color=NAVY)
    rows = [
        ("{}", 13, "Every product", NAVY),
        ("{ category: \"ACCESSORY\" }", 5, "P1001, A400, A410, A500, XBAD", PURPLE),
        ("{ category: \"ACCESSORY\",\n  active: true }", 5, "All five accessories are "
                                                           "active", TEAL),
        ("{ category: \"ACCESSORY\",\n  active: true,\n  price: { $lte:\n"
         "    Decimal128(\"100.00\") } }", 3, "P1001, A400, A410", GREEN),
    ]
    heights = [0.55, 0.55, 0.80, 1.30]
    gap = (y1 - y0 - 0.45 - sum(heights)) / (len(rows) - 1)
    ry = y0 + 0.45
    for (query, count, who, fill), rh in zip(rows, heights):
        V.code(slide, LEFT, ry, 4.60, rh, query, size=12)
        V.arrow(slide, LEFT + 4.65, ry + rh / 2, LEFT + 4.92, ry + rh / 2, color=MUTED)
        V.badge(slide, LEFT + 4.95, ry + rh / 2 - 0.29, 0.58, str(count), fill=fill, size=16)
        V.text(slide, LEFT + 5.68, ry, lw - 5.68, rh, who, size=13,
               anchor=MSO_ANCHOR.MIDDLE)
        ry += rh + gap

    px = LEFT + lw + 0.35
    F.stack_items(slide, px, y0, RIGHT - px, y1 - y0, [
        ("Why one at a time", "When the result is wrong, you know which condition caused it."),
        {"code": "db.products.countDocuments({\n  category: \"ACCESSORY\" })  // 5",
         "label": "Count after each step", "size": 11},
        ("Two drops explained", "A500 costs 249.99. XBAD's price is the string \"49.99\", "
                                "so a Decimal128 range skips it."),
        {"callout": ("Surprised?", "Check the field name, case and BSON type first.")},
    ])
    V.finish(slide, number=n, notes=notes(50),
             takeaway="Grow a filter one condition at a time and count after each step — "
                      "every drop should have a reason.")


# Hand-drawn slides, by topic number (see module04_flow.steps for the order).
SLIDES = {1: s01, 2: s02, 50: s50}


# ---------------------------------------------------------------------------
# Diagram slides: each diagram image is merged with the slide that explains it.
# Images live in scripts/new_content/diagrams/module04/ ("NN - Title.png"),
# copied from scripts/chatgpt_diagrams/diagrams/module04/ (0NN - Title.png).
# The diagrams draw simplified sample documents (ProBook, "Courses", K100 ...);
# each slide's text pairs the picture with the real training_store result.
# ---------------------------------------------------------------------------
DIAGRAM_DIR = HERE / "diagrams" / "module04"

import mdb_diagram_slides as DS  # noqa: E402

_tp = DS.tp


DIAGRAMS: dict[int, tuple[str, str, list[dict]]] = {
    7: ("Understanding Query Filters",
        "The filter is a document; each document either matches or doesn't.",
        [_tp("What it shows",
             "mongosh or Compass sends a query to mongod, which reads the products "
             "collection. Five sample documents, A to E, pass through the filter "
             "{ category: \"Training\", price: { $lt: 50 } }."),
         _tp("How to read it",
             "A green check means both conditions are true. A (Training, 29) and D (Training, "
             "39) match. B is Office, C costs 65 and E is Books, so they get a red cross. "
             "Matched documents: 2."),
         _tp("Key point",
             "Every condition in one filter document must be true for a document to match.")]),
    8: ("findOne() vs find()",
        "One document or null — or a cursor over every match.",
        [_tp("What it shows",
             "The same filter, { category: \"Laptop\" }, sent two ways. findOne() returns "
             "the first match as a single document. find() returns a cursor over all three "
             "matching documents."),
         _tp("How to read it",
             "Follow the arrows: request, then first match on the left, and cursor or "
             "matches on the right."),
         _tp("Key point",
             "Use findOne() for one document by a unique field; use find() when you expect "
             "a list.")]),
    48: ("Anatomy of a Read Query",
         "Filter, projection, sort and limit — in that order of thought.",
         [_tp("What it shows",
              "A query on products built from four parts: filter category Books, projection "
              "name and price, sort price ascending, limit 10. mongod runs it and returns a "
              "small table of names and prices."),
          _tp("How to read it",
              "Read the query card top to bottom. Each part narrows or shapes what comes "
              "back from the products collection."),
          _tp("Key point",
              "Think in this order: which documents, which fields, which order, how many.")]),
    23: ("Projection Fundamentals",
         "The second argument of find() chooses the fields that come back.",
         [_tp("What it shows",
              "A source product with _id, name, category, price, stock and internalCost. The "
              "filter { category: \"Courses\" } and the projection { name: 1, price: 1, "
              "_id: 0 } return only name and price."),
          _tp("How to read it",
              "The projection table marks name and price include and every other field, "
              "_id included, omit."),
          _tp("Key point",
              "Projection changes what comes back, never what is stored.")]),
    26: ("Sorting, Skipping and Limiting",
         "sort() orders, skip() jumps, limit() caps — and together they make a page.",
         [_tp("What it shows",
              "Eight Courses products sorted by price, skip(4) removes the first four, "
              "limit(4) keeps the next four. Page 2 of 3 returns four products."),
          _tp("How to read it",
              "The skip panel shows the formula: skip = (page − 1) × pageSize, so page 2 with "
              "a page size of 4 skips 4."),
          _tp("Key point",
              "Only the selected page travels back to the client.")]),
    12: ("Comparison Operators",
         "$gt, $gte, $lt and $lte — inside the field they test.",
         [_tp("What it shows",
              "The query { price: { $gte: 500, $lte: 1500 } } on four sample products. "
              "DataPad 699, AirLite 999 and ProBook 1299 match; DevStation 1799 is outside "
              "the range."),
          _tp("How to read it",
              "The number line shows an inclusive range from 500 to 1500. Both ends count."),
          _tp("Key point",
              "Two operators on one field make a range.")]),
    14: ("Logical Operators: $and and $or",
         "Both conditions true — or at least one.",
         [_tp("What it shows",
              "Two queries with the same predicates: A is category Laptop, B is price below "
              "1000. $and returns 1 document, AirLite. $or returns 3: AirLite, ProBook and "
              "DataPad."),
          _tp("How to read it",
              "The Venn symbols show the difference: the overlap for $and, both circles for "
              "$or."),
          _tp("Key point",
              "$or widens a result; $and narrows it.")]),
    16: ("The $not and $nor Operators",
         "Negate one expression — or reject every listed condition.",
         [_tp("What it shows",
              "$not wraps { $gte: 100 } on price, so documents with price below 100 or no "
              "price at all remain. $nor lists category Books and stock 0, and keeps only "
              "documents that match neither."),
          _tp("How to read it",
              "The red boxes show what each operator excludes; the green boxes show what "
              "remains."),
          _tp("Key point",
              "Negation also keeps documents where the field is missing.")]),
    17: ("Field Existence, BSON Type and Null",
         "Missing, explicit null and the wrong type are three different things.",
         [_tp("What it shows",
              "One product with sku as a string, discount set to null and no supplier field. "
              "$exists: false finds the missing field, $type: \"string\" checks the type, "
              "and { discount: null } matches both explicit null and a missing field."),
          _tp("How to read it",
              "Follow the two arrows out of the null box. The red box, $type: 10, is BSON "
              "type 10, null, and matches explicit null only."),
          _tp("Key point",
              "Ask exactly the question you mean: present, null, or of a given type.")]),
    11: ("Querying Nested Fields",
         "Dot notation reaches inside embedded documents.",
         [_tp("What it shows",
              "db.customers.find({ \"address.city\": \"Brampton\" }). Customers 201 and 202 "
              "live in Brampton and match; customer 203 lives in Toronto and doesn't."),
          _tp("How to read it",
              "The highlighted city line in each customer is the field the dotted path "
              "reads: address, then city."),
          _tp("Key point",
              "Quote the dotted path and match the nested value exactly.")]),
    20: ("Exact Array Match vs $all vs $size",
         "Same values in the same order — or contains all — or exactly N elements.",
         [_tp("What it shows",
              "One product with tags database, mongodb, backend. The exact array matches; "
              "the same values in a different order don't. $all with mongodb and database "
              "matches in any order. $size: 3 matches; $size: 2 doesn't."),
          _tp("How to read it",
              "Left panel: exact array. Right panels: $all at the top, $size below."),
          _tp("Key point",
              "Exact array match is rarely what you want; $all usually is.")]),
    22: ("Querying Arrays of Documents with $elemMatch",
         "All conditions must be met by the same array element.",
         [_tp("What it shows",
              "An order with three items and the filter items: { $elemMatch: { qty: "
              "{ $gte: 2 }, price: { $lt: 100 } } }. Only the Python Course item, qty 3 at 49, "
              "meets both conditions, so the whole order is returned."),
          _tp("How to read it",
              "MongoDB Course fails qty and Cloud Lab fails price. One item that passes both "
              "is enough to return the order."),
          _tp("Key point",
              "The filter selects the order; the returned document still has every item.")]),
    28: ("Inserting Documents",
         "insertOne() or insertMany(); mongod adds _id if it is missing.",
         [_tp("What it shows",
              "One document, or an array of documents, goes to mongod, which validates it, "
              "generates _id if missing and writes it into products. The client receives "
              "acknowledged: true and the insertedId."),
          _tp("How to read it",
              "Follow the arrows left to right, then the insert result back to the client."),
          _tp("Key point",
              "Check the acknowledgement and the new _id — then read the document back.")]),
    30: ("Updating Documents",
         "A filter, update operators and a write result.",
         [_tp("What it shows",
              "db.products.updateOne() with filter { name: \"MongoDB Basics\" }, $set price "
              "44.99 and $inc inventory.stock 10. Before, the price is 49.99 and stock 120; "
              "after, 44.99 and 130. matchedCount 1, modifiedCount 1."),
          _tp("How to read it",
              "mongod matches the document, applies the operators, then writes the change."),
          _tp("Key point",
              "The yellow note matters: updateMany() applies the same change to every "
              "match.")]),
    31: ("$set, $unset, Numeric Operators and $rename",
         "Four operators, one document, changed in place.",
         [_tp("What it shows",
              "One combined update on the MongoDB Basics product: $set price to 44.99, "
              "$unset discount, $inc inventory.stock by 10 and $rename oldSku to sku."),
          _tp("How to read it",
              "Compare BEFORE and AFTER. The price changes, discount disappears, stock goes "
              "from 120 to 130 and oldSku becomes sku with the same value."),
          _tp("Key point",
              "Operators modify selected fields in place without replacing the whole "
              "document.")]),
    33: ("Array Update Operators",
         "$push, $addToSet, $pull and $pop change arrays without rewriting them.",
         [_tp("What it shows",
              "Tags start as audio and clearance, ratings as 5, 4, 3. After the updates, tags "
              "are audio, wireless, sale, and ratings are 5, 4."),
          _tp("How to read it",
              "$pull removed clearance, $push added wireless, $addToSet added sale once and "
              "$pop removed the last rating."),
          _tp("One caution",
              "Run these as separate updates. One update may not both $push to and $pull "
              "from the same array; MongoDB reports a conflict.")]),
    35: ("Positional Array Updates",
         "$ updates the element the filter matched.",
         [_tp("What it shows",
              "updateOne on order 501 with the filter \"items.sku\": \"KB-10\" and "
              "$set \"items.$.qty\": 2. Only element 1, KB-10, changes from qty 1 to 2."),
          _tp("How to read it",
              "The $ stands for the first matched element. Elements 0 and 2 are untouched."),
          _tp("Key point",
              "The array field must appear in the filter for $ to know which element.")]),
    36: ("Replace vs $set",
         "replaceOne() rewrites the document; $set changes named fields.",
         [_tp("What it shows",
              "Left: replaceOne keeps _id 101 but drops stock, because the replacement lists "
              "only name and price. Right: updateOne with $set changes price to 69 and keeps "
              "stock 12. Below, a preview of upsert: match, or insert."),
          _tp("How to read it",
              "The red cross over stock: 12 is the whole lesson of replaceOne."),
          _tp("Key point",
              "Use update operators when only some fields should change.")]),
    37: ("The Upsert Pattern",
         "One command: update if found, insert if not.",
         [_tp("What it shows",
              "updateOne on sku KB-NEW with $set price and stock, $setOnInsert name and "
              "{ upsert: true }. If the SKU exists, price and stock change and $setOnInsert "
              "is not applied. If not, a new document is inserted with the filter field plus "
              "every set field."),
          _tp("How to read it",
              "Follow the diamond: YES goes to update, NO goes to insert."),
          _tp("Key point",
              "$setOnInsert only acts on the insert path.")]),
    42: ("Understanding Write Results",
         "Matched is not the same as modified.",
         [_tp("What it shows",
              "A $set of stock 24 on product K100 and the write result: acknowledged true, "
              "matchedCount 1, modifiedCount 1, upsertedCount 0, upsertedId null."),
          _tp("How to read it",
              "Each row of the result answers one question: found, changed, inserted, new "
              "_id."),
          _tp("Key point",
              "Read the whole result, not just \"acknowledged\".")]),
    38: ("Deleting Documents Safely",
         "Count, preview, check — then delete the verified set.",
         [_tp("What it shows",
              "The filter status cancelled, archived true and archivedAt before 2025 is "
              "counted, previewed with find() and limit(3), checked against the expected "
              "count, and only then used by deleteMany(). deletedCount: 3."),
          _tp("How to read it",
              "The NO path loops back: stop and refine the filter. Active orders are "
              "untouched."),
          _tp("Key point",
              "The delete uses exactly the filter you counted and previewed.")]),
    41: ("Bulk Write Operations",
         "Several writes in one request and one response.",
         [_tp("What it shows",
              "products.bulkWrite with three operations: insertOne a Keyboard, updateOne "
              "sku K100 to stock 24, deleteOne sku OLD9. The single response shows "
              "insertedCount 1, modifiedCount 1, deletedCount 1."),
          _tp("How to read it",
              "The numbered steps run in order, and the numbers match the documents on the "
              "right."),
          _tp("Key point",
              "Fewer round trips, one combined result.")]),
    46: ("Query Troubleshooting Workflow",
         "Reproduce, confirm, sample, fix, test small, confirm.",
         [_tp("What it shows",
              "find({ sku: \"K100\", price: \"49.99\" }) returns 0 results. A sample document "
              "shows price is a number, 49.99. Changing the string to a number returns 1 "
              "document."),
          _tp("How to read it",
              "Six steps left to right. Step 5 tests the smallest query first, sku alone, "
              "then adds the price."),
          _tp("Key point",
              "When a query returns nothing, compare it with a real document.")]),
    47: ("Module 4 at a Glance",
         "Build a precise filter, send it, execute, read the result, verify.",
         [_tp("What it shows",
              "The loop: build a precise filter with find, updateOne, deleteOne or bulkWrite; "
              "send it to mongod; execute on training_store; return acknowledged, "
              "matchedCount and modifiedCount; verify with findOne."),
          _tp("How to use it",
              "Ask the class which part of the loop each Part of the module taught."),
          _tp("A detail to notice",
              "The product card writes _id: \"K100\" as shorthand. In training_store, _id "
              "is an ObjectId and K100-style codes live in sku, which is what the "
              "findOne verifies.")]),
}


def main() -> None:
    prs = K.new_presentation()
    layout = K.blank_layout(prs)
    from module04_flow import steps

    F.build_sequence(prs, layout, steps(SLIDES, NOTES, DIAGRAMS, DIAGRAM_DIR))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    K.save_presentation(prs, OUT)
    print(f"Wrote {len(prs.slides)} slides -> {OUT.relative_to(ROOT)}")
    for w in V.WARNINGS:
        print("  WARN", w)


if __name__ == "__main__":
    main()
