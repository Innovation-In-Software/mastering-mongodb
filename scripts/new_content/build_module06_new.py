#!/usr/bin/env python3
"""Build the new-content Module 6 deck: Indexing and Query Performance.

Content comes from scripts/module06_content_source.md, the Module 6 manifest, the
official Module 6 exercises (labs/day-03/exercises/exercise-6.1 to 6.3), Day 3
Lab 5 (labs/day-03/lab5/LAB-5-GUIDE.md) and the training_store sample database.
Styling reuses the house kit through mdb_deck_kit (read-only): title block,
red/black rail, footer, page numbers, key-takeaway bar, fonts and colours.
Hand-drawn visuals are native, editable PowerPoint shapes; concept diagrams come
from scripts/new_content/diagrams/module06/.

Writes decks/pptx_new/MongoDB_Module06_Indexing_and_Query_Performance.pptx and
never touches decks/pptx/.

    python scripts/new_content/build_module06_new.py
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

from pptx.enum.text import MSO_ANCHOR, PP_ALIGN  # noqa: E402

import mdb_deck_kit as K  # noqa: E402
import mdb_flow_slides as F  # noqa: E402
import mdb_speaker_notes as SN  # noqa: E402
import mdb_visuals as V  # noqa: E402
from mdb_visuals import (  # noqa: E402
    BLACK, CARD_LINE, DARK_GRAY, GREEN, INK, LEFT, LIGHT_GRAY, LIGHT_GREEN, MUTED, NAVY,
    ORANGE, PURPLE, RED, RIGHT, TEAL, WHITE, WIDTH,
)
from module06_notes import NOTES  # noqa: E402

ROOT = HERE.parents[1]
OUT = ROOT / "decks" / "pptx_new" / "MongoDB_Module06_Indexing_and_Query_Performance.pptx"
MODULE_LABEL = "MODULE 6"


def notes(n: int) -> str:
    return SN.compose(NOTES[n])


def new(prs, layout, n, title, subtitle):
    return V.content_slide(prs, layout, number=n, title=title, subtitle=subtitle)


def done(slide, n, takeaway):
    V.finish(slide, number=n, takeaway=takeaway, notes=notes(n))


# ---------------------------------------------------------------------------
def s01(prs, layout):
    slide = K._chapter_slide(
        prs, layout, tag=MODULE_LABEL, title="Indexing and Query Performance",
        subtitle="How MongoDB finds documents, how to design indexes around real query "
                 "shapes, and how to prove the result with explain().",
        quote='"Index the query shape, not every field."',
        module_label=MODULE_LABEL,
    )
    V.set_slide_label("slide 1")
    topics = [
        ("COLLSCAN vs IXSCAN", NAVY),
        ("Compound + ESR", PURPLE),
        ("Specialized indexes", TEAL),
        ("explain() + covered", GREEN),
        ("Costs + clean-up", ORANGE),
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
        "1. Explain how an index avoids a full scan",
        "2. Create, list, hide and drop named indexes",
        "3. Order compound fields with ESR",
        "4. Choose multikey, unique, partial, sparse, TTL",
        "5. Read explain() and build a covered query",
        "6. Weigh selectivity, write cost and usage",
    ], icon="🎯", badge_color=RED, size=16)

    x = 6.75
    y = V.section(slide, x, top + 0.05, 6.05, "Six questions this module answers", icon="❓",
                  fill=NAVY)
    questions = [
        ("WHY", "does a query read every document?", NAVY),
        ("HOW", "do I create and manage indexes?", PURPLE),
        ("WHICH", "field order goes in an index?", TEAL),
        ("WHICH", "index type fits the query?", GREEN),
        ("WHAT", "does explain() really tell me?", ORANGE),
        ("WHEN", "is an index not worth its cost?", RED),
    ]
    row_h, gap = 0.50, 0.09
    for i, (word, rest, fill) in enumerate(questions):
        ry = y + i * (row_h + gap)
        V.box(slide, x, ry, 2.05, row_h, word, fill=fill, size=13)
        V.text(slide, x + 2.2, ry, 3.85, row_h, rest, size=14, anchor=MSO_ANCHOR.MIDDLE)

    V.section(slide, LEFT, 5.02, WIDTH, "Module roadmap", icon="🗺️", fill=PURPLE)
    V.chevrons(slide, LEFT, 5.50, WIDTH, 0.80,
               ["How indexes work", "Manage", "Compound + ESR", "Specialized", "explain()",
                "Costs + mistakes"],
               [NAVY, PURPLE, TEAL, ORANGE, GREEN, RED], size=13)
    done(slide, n, "Design indexes around the queries the application really runs — then "
                   "prove them with explain().")


def s24(prs, layout):
    n = 24
    slide, top = new(prs, layout, n, "Multikey Indexes on Arrays",
                     "One index key for every array value — real tags from training_store "
                     "products.")
    y0, y1 = top + 0.10, V.BODY_BOTTOM
    # Three products -----------------------------------------------------------
    lw = 3.35
    y = V.section(slide, LEFT, y0, lw, "Three products", icon="🏷️", fill=TEAL)
    docs = [
        ('sku: "P1001",\ntags: [ "wireless",\n        "accessories" ]', "Wireless Keyboard"),
        ('sku: "A400",\ntags: [ "office",\n        "accessories" ]', "USB Hub"),
        ('sku: "A410",\ntags: [ "wireless",\n        "accessories" ]', "Wireless Mouse"),
    ]
    dh, dg = 1.05, 0.28
    mids = []
    for k, (code, name) in enumerate(docs):
        dy = y + 0.02 + k * (dh + dg)
        V.text(slide, LEFT, dy - 0.02, lw, 0.26, name, size=11, bold=True, color=TEAL)
        V.code(slide, LEFT, dy + 0.24, lw, dh - 0.24, code, size=12)
        mids.append(dy + 0.24 + (dh - 0.24) / 2)

    # The index -----------------------------------------------------------------
    ix, iw = LEFT + lw + 0.45, 3.45
    rows = [("accessories", "P1001", False), ("accessories", "A400", False),
            ("accessories", "A410", False), ("…", "", None), ("office", "A400", False),
            ("wireless", "P1001", True), ("wireless", "A410", True)]
    rh, rg = 0.44, 0.07
    card_h = 0.58 + len(rows) * (rh + rg) + 0.05
    body = V.card(slide, ix, y0, iw, card_h, "idx_products_tags", head_fill=NAVY,
                  title_size=14)
    for k, (key, sku, hit) in enumerate(rows):
        ry = body + k * (rh + rg)
        if hit is None:
            V.text(slide, ix + 0.15, ry, iw - 0.30, rh, "…  (26 keys in all)", size=12,
                   italic=True, color=MUTED, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            continue
        V.box(slide, ix + 0.15, ry, iw - 0.30, rh, f"{key:<12}→ {sku}",
              fill=LIGHT_GREEN if hit else LIGHT_GRAY, color=GREEN if hit else INK,
              size=12, bold=hit, font=K.CODE_FONT, align=PP_ALIGN.LEFT, radius=0.10,
              margin=0.14)
    for my in mids:
        V.arrow(slide, LEFT + lw + 0.04, my, ix - 0.04, my, color=TEAL, width=1.75)
    V.text(slide, ix, y0 + card_h + 0.06, iw, 0.34, "13 products → 26 index keys", size=12,
           bold=True, color=NAVY, align=PP_ALIGN.CENTER)

    # What it means ---------------------------------------------------------------
    px = ix + iw + 0.40
    F.stack_items(slide, px, y0, RIGHT - px, y1 - y0, [
        {"code": 'db.products.find(\n  { tags: "wireless" })', "label": "Query",
         "kind": "good", "size": 12},
        ("Result", "P1001 and A410 — 2 keys and 2 documents examined."),
        ("multikey: true", "Set automatically once an indexed field holds an array."),
        ("Arrays of documents", "{ \"items.productId\": 1 } finds orders that contain a "
                                "product."),
    ])
    done(slide, n, "Index an array field and MongoDB makes a multikey index — one key per "
                   "value, so each array element is searchable.")


# Hand-drawn slides, by topic number (see module06_flow.steps for the order).
SLIDES = {1: s01, 2: s02, 24: s24}


# ---------------------------------------------------------------------------
# Diagram slides: each diagram image is merged with the slide that explains it.
# Images live in scripts/new_content/diagrams/module06/ ("NN - Title.png"),
# copied from scripts/chatgpt_diagrams/diagrams/module06/ ("0NN - Title.png").
# ---------------------------------------------------------------------------
DIAGRAM_DIR = HERE / "diagrams" / "module06"

import mdb_diagram_slides as DS  # noqa: E402

_tp = DS.tp


DIAGRAMS: dict[int, tuple[str, str, list[dict]]] = {
    3: ("Why Query Performance Matters",
        "An indexed lookup or a collection scan.",
        [_tp("What it shows",
             "mongosh and MongoDB Compass send a query to mongod for the orders collection in "
             "training_store. The green path is an indexed lookup; the red path is a "
             "collection scan."),
         _tp("How to read it",
             "Follow each row left to right. Indexed lookup, few documents scanned, fast "
             "response, more orders served. Collection scan, many documents scanned, slow "
             "response, users wait and the server works harder."),
         _tp("Key point",
             "The query is the same on both rows. Only the access path differs.")]),
    5: ("Collection Scan vs Index Scan",
        "Same query, same three matches — 8 examined versus 3.",
        [_tp("What it shows",
             "The same find on category Books, run twice against a small eight-document "
             "products collection: once as a collection scan and once through a category_1 "
             "index."),
         _tp("How to read it",
             "On the left, every one of the eight documents is checked: 3 matches, 8 "
             "examined, COLLSCAN. On the right, the index finds the Books key and fetches only "
             "documents 2, 4 and 6: 3 matches, 3 examined, IXSCAN."),
         _tp("About the data",
             "The diagram uses a simplified collection with category names like Books and "
             "Electronics. In training_store the categories are upper-case codes, LAPTOP, SHOE, "
             "BOOK and ACCESSORY, and there are 13 products, 2 of them books.")]),
    7: ("Inside an Index: A Sorted Tree",
        "A price_1 index as a B-tree.",
        [_tp("What it shows",
             "A price_1 index drawn as a tree: a root that splits at 50 and 100, three internal "
             "nodes, and sorted leaf entries that each point to one product document."),
         _tp("How to read it",
             "Follow the green path for find price 79: root, then the 50 to 99 node, then the "
             "leaf 79, which points to doc 6. The document pointer lands on the product with "
             "_id 6 and price 79."),
         _tp("Key point",
             "A few steps down a sorted tree replace a read of every document.")]),
    10: ("The Default _id Index",
         "Every collection is born with a unique index on _id.",
         [_tp("What it shows",
              "The products collection with its _id_ index, created automatically. A find on "
              "one ObjectId goes to the index, finds the key ending a12 and jumps straight to "
              "doc 3, the Keyboard."),
          _tp("How to read it",
              "The two notes at the bottom of the index are the rules: unique values, and it "
              "cannot be dropped."),
          _tp("About the data",
              "The five products in the diagram are illustrative. The rule is the same for all "
              "four training_store collections.")]),
    14: ("Hide an Index Before You Drop It",
         "hideIndex() and unhideIndex() on a products index.",
         [_tp("What it shows",
              "mongosh and Compass hide and unhide the sku_1 index on products. Hidden, it is "
              "removed from the query planner's choices but still maintained. Visible, it is "
              "available again. The documents never change."),
          _tp("How to read it",
              "The red arrow is hideIndex, the green arrow is unhideIndex. Both boxes say the "
              "index is still maintained, which is why hiding is instant to undo."),
          _tp("About the data",
              "In training_store the SKU index built by load.js is named sku_unique, not sku_1. "
              "In Lab 5, Step 13 you hide a non-unique helper index, "
              "idx_products_category_active_price, instead: never a unique rule or _id_.")]),
    17: ("Compound Indexes",
         "Sorted by category, then by price within each category.",
         [_tp("What it shows",
              "The index { category: 1, price: -1 }, named category_1_price_-1, built from "
              "Apparel and Footwear products. The keys are grouped by category and, inside "
              "each group, run from the highest price to the lowest."),
          _tp("How to read it",
              "The first key column is category, ascending; the second is price, descending. "
              "The supported query on the right, category Apparel sorted by price high to low, "
              "is one continuous run of keys."),
          _tp("About the data",
              "Apparel and Footwear are illustrative. In training_store the same idea is "
              "{ category: 1, price: 1 } over LAPTOP, SHOE, BOOK and ACCESSORY.")]),
    18: ("Field Order Matters",
         "The same two fields, two different indexes.",
         [_tp("What it shows",
              "Two indexes built from the same fields: category_1_price_1 on the left and "
              "price_1_category_1 on the right, each with its keys in order."),
          _tp("How to read it",
              "On the left, the Apparel keys sit together, so a category query reads one "
              "block and gets a green check. On the right, Apparel keys are scattered through "
              "the price order, so the same query cannot use the leading field efficiently."),
          _tp("Key point",
              "The banner says it: same fields does not mean same index order.")]),
    19: ("The Prefix Rule",
         "A compound index serves queries on its leading fields.",
         [_tp("What it shows",
              "The orders index { customerId: 1, status: 1, createdAt: -1 } and five query "
              "shapes. Three are prefixes and supported; two skip customerId and are not "
              "prefixes."),
          _tp("How to read it",
              "Read the green boxes left to right: customerId; customerId and status; all "
              "three. The red boxes, status alone and status with createdAt, start in the "
              "middle of the index."),
          _tp("About the data",
              "training_store orders have no plain status field. The diagram's status stands "
              "for paymentStatus, so the training_store version is { customerId: 1, "
              "paymentStatus: 1, createdAt: -1 }.")]),
    20: ("Equality, Sort, Range (ESR)",
         "A starting order for compound-index fields.",
         [_tp("What it shows",
              "A query on orders with an equality filter region = East, a sort on createdAt "
              "descending and a range total ≥ 100, mapped to the compound index region: 1, "
              "createdAt: -1, total: 1."),
          _tp("How to read it",
              "The E, S and R badges connect each query condition to its position in the "
              "index: 1 Equality, 2 Sort, 3 Range. The result is an efficient scan of already "
              "sorted orders."),
          _tp("About the data",
              "training_store orders have no region field; region is the diagram's example "
              "of an equality condition. In our data the equality fields are customerId, "
              "paymentStatus and fulfillmentStatus.")]),
    28: ("Sparse Indexes",
         "Only documents that have the field get an index entry.",
         [_tp("What it shows",
              "db.customers.createIndex({ phone: 1 }, { sparse: true }). Alice and Carol have "
              "a phone, so they are indexed. Bob and David have no phone field, so they are not "
              "indexed."),
          _tp("How to read it",
              "The green arrow is indexed and the red crossed arrow is not indexed. The query "
              "for one phone number uses the two-entry sparse index."),
          _tp("About the data",
              "The four customers are illustrative, and training_store keeps phone inside "
              "contact, so the real path is contact.phone.")]),
    31: ("Text, Wildcard, Geospatial and Hashed",
         "Four specialized types for four special query shapes.",
         [_tp("What it shows",
              "Four cards, one per type: text on products name plus description, wildcard on "
              "products attributes.$**, 2dsphere on a customers location field, and hashed on "
              "orders customerId."),
          _tp("How to read it",
              "Each card lists the collection, the field, the index definition, what it is "
              "used for and the query operator it serves: $text, dynamic attribute paths, $near "
              "and equality."),
          _tp("About the data",
              "Two cards are hypothetical for training_store: our products have no description "
              "field and our customers have no location. The wildcard card matches our data "
              "exactly: products store category-specific fields under attributes.")]),
    36: ("Covered Queries",
         "When the index holds every field the query needs, no document is read.",
         [_tp("What it shows",
              "A find on category Books with the projection name 1, price 1, _id 0, served by "
              "the index { category: 1, name: 1, price: 1 }. The results come from the index "
              "only: IXSCAN only, and a red cross marks no FETCH from the product documents."),
          _tp("How to read it",
              "Check the three index fields against the query: category is the filter, name "
              "and price are the output, and _id is switched off."),
          _tp("About the data",
              "The two books in the diagram are illustrative. In training_store the books are "
              "MongoDB Fundamentals at 59.99 and Query Cookbook at 39.99, in category BOOK.")]),
    37: ("Index Selectivity",
         "More distinct values means fewer keys scanned.",
         [_tp("What it shows",
              "Two indexes on products. sku_1 has many distinct keys, so the SKU lookup scans a "
              "few keys and returns one match. category_1 has a few repeated keys, so a Books "
              "query scans many keys and returns many matches."),
          _tp("How to read it",
              "Green is high selectivity, red is low. The dashed note in the middle is the "
              "rule: more distinct values means higher selectivity."),
          _tp("Key point",
              "An index narrows the search only as much as its values do.")]),
    44: ("explain(): Three Levels of Detail",
         "queryPlanner, executionStats and allPlansExecution.",
         [_tp("What it shows",
              "One find on products, category Laptop, sent with explain(mode). mongod returns "
              "one of three levels of detail."),
          _tp("How to read it",
              "Top to bottom is less to more detail. queryPlanner gives the plan only. "
              "executionStats runs the winning plan and reports nReturned, documents examined "
              "and time. allPlansExecution also tests the candidate plans and shows the "
              "rejected ones."),
          _tp("About the data",
              "Laptop is written as LAPTOP in training_store, where three laptops exist: L100, "
              "L110 and L190.")]),
    48: ("Spotting a Blocking Sort",
         "A SORT stage means documents were sorted in memory.",
         [_tp("What it shows",
              "find category Laptop sorted by price, with no supporting index. The plan reads "
              "with COLLSCAN, then a red SORT stage sorts in memory before the results go back."),
          _tp("How to read it",
              "The explain excerpt shows stage SORT with inputStage COLLSCAN and the warning "
              "In-memory sort. The crossed-out price_1 box explains why: no index supplies the "
              "order."),
          _tp("About the data",
              "The counts, 1,000 examined and 24 returned, are from a larger illustrative "
              "catalog. The pattern is what matters.")]),
    50: ("Index Usage Statistics",
         "$indexStats shows how often each index was used.",
         [_tp("What it shows",
              "db.products.aggregate([{ $indexStats: {} }]) returns usage counters since "
              "mongod started: _id_ with 420 operations, category_1 with 185, and price_1 "
              "with 0."),
          _tp("How to read it",
              "Green rows have ops greater than zero: index used. The red row, price_1 with "
              "zero, is flagged review index."),
          _tp("Key point",
              "Zero uses is a reason to investigate, not an instruction to drop.")]),
    54: ("Every Index Costs Writes",
         "Each insert or update also updates the indexes.",
         [_tp("What it shows",
              "An insert or update on training_store.orders writes the document and then "
              "updates each index: _id, customerId, status and orderDate. Each adds work "
              "before the write completes."),
          _tp("How to read it",
              "The clocks on the red index boxes are the extra work. The bottom bar compares "
              "two indexes, lower write cost, with six indexes, higher write cost."),
          _tp("About the data",
              "The diagram's orderDate and status are generic names. training_store orders "
              "use createdAt, paymentStatus and fulfillmentStatus.")]),
    57: ("Changing Indexes Safely in Production",
         "Analyze, test, build, monitor, confirm.",
         [_tp("What it shows",
              "Five steps for one index change: analyze with explain and $indexStats, test on "
              "staging, build { category: 1, price: 1 }, monitor CPU, I/O and latency, then "
              "confirm in production during a change window."),
          _tp("How to read it",
              "The red loop is the rollback: if monitoring shows degradation, drop the new "
              "index and return to testing."),
          _tp("Key point",
              "An index change is a production change. It gets a plan and a rollback.")]),
    59: ("Common Indexing Mistakes",
         "Too many, wrong order, never used — and the query-aligned fix.",
         [_tp("What it shows",
              "On the left, three mistakes on orders: too many single-field indexes, the wrong "
              "field order { createdAt: 1, status: 1 }, and an unused { customerId: 1 } index. "
              "Result: slow writes and more RAM."),
          _tp("How to read it",
              "On the right, the fix for the real query, status shipped sorted by createdAt "
              "newest first: one query-aligned compound index { status: 1, createdAt: -1 }. "
              "Result: fast reads and lean writes."),
          _tp("About the data",
              "In training_store the field is fulfillmentStatus and the value is upper case, "
              "SHIPPED. The same index there is { fulfillmentStatus: 1, createdAt: -1 }.")]),
    61: ("An Indexing Strategy for training_store",
         "One index per important query shape.",
         [_tp("What it shows",
              "The four training_store collections, each with one query-aligned index and the "
              "query it serves: category and price for the catalog, unique email to find a "
              "customer, customerId and createdAt for order history, productId and rating for "
              "product ratings."),
          _tp("How to read it",
              "Read each column top to bottom: collection, index, query. The banner sums it "
              "up: fast reads, controlled writes."),
          _tp("About the data",
              "The customer email lives at contact.email in training_store, and load.js already "
              "makes it unique as email_unique.")]),
    62: ("Module 6 at a Glance",
         "From query pattern to tuned index.",
         [_tp("What it shows",
              "The whole module as one workflow on training_store: query patterns, choose the "
              "index, validate the plan, monitor usage, tune, and the outcome, fast reads with "
              "controlled writes."),
          _tp("How to use it",
              "Point to each step and ask the class which command belongs there: find and sort, "
              "createIndex, explain, $indexStats, hide or drop."),
          _tp("About the data",
              "The orders example uses status shipped. In training_store that is "
              "fulfillmentStatus SHIPPED.")]),
}


def main() -> None:
    prs = K.new_presentation()
    layout = K.blank_layout(prs)
    from module06_flow import steps

    F.build_sequence(prs, layout, steps(SLIDES, NOTES, DIAGRAMS, DIAGRAM_DIR))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    K.save_presentation(prs, OUT)
    print(f"Wrote {len(prs.slides)} slides -> {OUT.relative_to(ROOT)}")
    for w in V.WARNINGS:
        print("  WARN", w)


if __name__ == "__main__":
    main()
