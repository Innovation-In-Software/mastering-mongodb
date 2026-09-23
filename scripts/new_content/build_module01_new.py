#!/usr/bin/env python3
"""Build the new-content Module 1 deck: Introduction to NoSQL Databases.

Content comes from scripts/module01_content_source.md, the Module 1 manifest,
the official Exercises 1.1-1.3 and the training_store sample database. Styling
reuses the house kit through mdb_deck_kit (read-only): title block, red/black
rail, footer, page numbers, key-takeaway bar, fonts and colours. Hand-drawn
visuals are native, editable PowerPoint shapes; concept diagrams come from
scripts/new_content/diagrams/module01/.

Writes decks/pptx_new/MongoDB_Module01_Introduction_to_NoSQL_Databases.pptx and
never touches decks/pptx/.

    python scripts/new_content/build_module01_new.py
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
    BLACK, CARD_BG, CARD_LINE, DARK_GRAY, GREEN, INK, LEFT, LIGHT_GRAY, LIGHT_GREEN,
    LIGHT_NAVY, LIGHT_PURPLE, LIGHT_RED, LIGHT_TEAL, MID_GRAY, MUTED, NAVY, ORANGE,
    PURPLE, RED, RIGHT, TEAL, WHITE, WIDTH,
)
from module01_notes import NOTES  # noqa: E402

ROOT = HERE.parents[1]
OUT = ROOT / "decks" / "pptx_new" / "MongoDB_Module01_Introduction_to_NoSQL_Databases.pptx"
MODULE_LABEL = "MODULE 1"


def notes(n: int) -> str:
    return SN.compose(NOTES[n])


def new(prs, layout, n, title, subtitle):
    return V.content_slide(prs, layout, number=n, title=title, subtitle=subtitle)


def done(slide, n, takeaway):
    V.finish(slide, number=n, takeaway=takeaway, notes=notes(n))


# ---------------------------------------------------------------------------
def s01(prs, layout):
    slide = K._chapter_slide(
        prs, layout, tag=MODULE_LABEL, title="Introduction to NoSQL Databases",
        subtitle="Why NoSQL databases exist, how the four NoSQL models differ, and where "
                 "MongoDB's document model fits.",
        quote='"NoSQL means Not Only SQL."',
        module_label=MODULE_LABEL,
    )
    V.set_slide_label("slide 1")
    topics = [
        ("Why NoSQL", NAVY),
        ("Four NoSQL models", PURPLE),
        ("MongoDB documents", TEAL),
        ("MongoDB architecture", GREEN),
        ("When MongoDB fits", ORANGE),
    ]
    w, gap = 2.34, 0.15
    for i, (label, fill) in enumerate(topics):
        x = LEFT + i * (w + gap)
        V.box(slide, x, 5.15, w, 0.95, label, fill=fill, size=15, radius=0.12, margin=0.14)
    K.set_notes(slide, notes(1))


def s02(prs, layout):
    n = 2
    slide, top = new(prs, layout, n, "Learning Objectives",
                     "What you will understand by the end of this module.")
    V.panel(slide, LEFT, top + 0.05, 5.9, "By the end of this module, you can", [
        "1. Define NoSQL as a category, not one product",
        "2. Compare the four NoSQL data models",
        "3. Explain documents, collections and BSON",
        "4. Describe the basic MongoDB architecture",
        "5. Judge when MongoDB is — and isn't — a fit",
        "6. Explore training_store in mongosh",
    ], icon="🎯", badge_color=RED, size=16)

    x = 6.75
    y = V.section(slide, x, top + 0.05, 6.05, "Six questions this module answers", icon="❓",
                  fill=NAVY)
    questions = [
        ("WHY", "did NoSQL databases appear?", NAVY),
        ("WHAT", "are the four NoSQL models?", PURPLE),
        ("WHAT", "exactly is a MongoDB document?", TEAL),
        ("HOW", "is MongoDB built?", GREEN),
        ("WHEN", "is MongoDB the right choice?", ORANGE),
        ("HOW", "do we read real data in mongosh?", RED),
    ]
    row_h, gap = 0.50, 0.09
    for i, (word, rest, fill) in enumerate(questions):
        ry = y + i * (row_h + gap)
        V.box(slide, x, ry, 2.05, row_h, word, fill=fill, size=13)
        V.text(slide, x + 2.2, ry, 3.85, row_h, rest, size=14, anchor=MSO_ANCHOR.MIDDLE)

    V.section(slide, LEFT, 5.02, WIDTH, "Module roadmap", icon="🗺️", fill=PURPLE)
    V.chevrons(slide, LEFT, 5.50, WIDTH, 0.80,
               ["Data today", "Why NoSQL", "Four models", "Documents", "BSON",
                "Architecture", "Fit"],
               [NAVY, PURPLE, TEAL, ORANGE, RED, GREEN, BLACK], size=13)
    done(slide, n, "Choose a data model from the access pattern — not from a product's "
                   "popularity.")


def _node(slide, x, y, w, h, name, role, fill):
    V.box(slide, x, y, w, h,
          [(name, {"size": 15}), (role, {"size": 12, "bold": False})],
          fill=fill, size=15, kind=MSO_SHAPE.OVAL, margin=0.05)


def _edge_label(slide, x, y, w, text, color=NAVY, align=PP_ALIGN.CENTER):
    V.text(slide, x, y, w, 0.30, text, size=12, bold=True, color=color, align=align,
           anchor=MSO_ANCHOR.MIDDLE)


def s12(prs, layout):
    n = 12
    slide, top = new(prs, layout, n, "Graph Databases",
                     "Nodes, relationships and properties — real training_store facts drawn "
                     "as a graph.")
    y0, y1 = top + 0.10, V.BODY_BOTTOM
    nw, nh = 2.35, 1.00
    lx, rx_ = LEFT + 0.10, LEFT + 4.20          # left and right node columns
    ty, by = y0 + 0.25, y0 + 2.45               # top and bottom node rows
    _node(slide, lx, ty, nw, nh, "Luis Romero", "Customer C204", NAVY)
    _node(slide, rx_, ty, nw, nh, "Business Laptop", "Product L100", TEAL)
    _node(slide, lx, by, nw, nh, "USB Hub", "Product A400", TEAL)
    _node(slide, rx_, by, nw, nh, "Aisha Khan", "Customer C101", NAVY)

    # Luis -> Laptop
    V.arrow(slide, lx + nw + 0.05, ty + nh / 2, rx_ - 0.05, ty + nh / 2, color=NAVY, width=2.0)
    _edge_label(slide, lx + nw, ty + nh / 2 - 0.36, rx_ - lx - nw, "ORDERED")
    # Aisha -> Laptop (ordered, reviewed)
    ax1, ax2 = rx_ + 0.70, rx_ + nw - 0.70
    V.arrow(slide, ax1, by - 0.05, ax1, ty + nh + 0.05, color=NAVY, width=2.0)
    _edge_label(slide, ax1 - 1.35, (ty + nh + by) / 2 - 0.15, 1.28, "ORDERED",
                align=PP_ALIGN.RIGHT)
    V.arrow(slide, ax2, by - 0.05, ax2, ty + nh + 0.05, color=ORANGE, width=2.0)
    V.text(slide, ax2 + 0.10, (ty + nh + by) / 2 - 0.30, 1.50, 0.60,
           [("REVIEWED", {"bold": True, "color": ORANGE}),
            ("rating: 5", {"color": ORANGE, "font": K.CODE_FONT, "size": 11})],
           size=12, anchor=MSO_ANCHOR.MIDDLE)
    # Aisha -> USB Hub
    V.arrow(slide, rx_ - 0.05, by + nh / 2, lx + nw + 0.05, by + nh / 2, color=NAVY, width=2.0)
    _edge_label(slide, lx + nw, by + nh / 2 - 0.36, rx_ - lx - nw, "ORDERED")
    # Recommendation: Luis -> USB Hub
    cx = lx + nw / 2
    V.arrow(slide, cx, ty + nh + 0.05, cx, by - 0.05, color=RED, width=2.0, dash=True)
    _edge_label(slide, cx + 0.12, (ty + nh + by) / 2 - 0.15, 1.60, "SUGGEST?", color=RED,
                align=PP_ALIGN.LEFT)

    lw = 6.75
    V.callout(slide, LEFT, by + nh + 0.35, lw, y1 - (by + nh + 0.35), "Traversal",
              "Luis → L100 ← Aisha → A400: suggest the USB Hub to Luis.", size=14)

    px = LEFT + lw + 0.45
    F.stack_items(slide, px, y0, RIGHT - px, y1 - y0, [
        ("Nodes and edges", "Nodes are things, edges are relationships — and both can carry "
                            "properties."),
        ("Good fit", "Social networks, recommendations, fraud detection and access "
                     "relationships."),
        {"chips": ["Neo4j", "Amazon Neptune"], "h": "Examples", "c": GREEN, "cols": 2},
        {"callout": ("Strength", "Multi-step walks along relationships stay fast.")},
    ])
    done(slide, n, "Choose a graph database when the relationships matter as much as the "
                   "things they connect.")


def s21(prs, layout):
    n = 21
    slide, top = new(prs, layout, n, "Replica Sets and Sharded Clusters",
                     "Copies of the data for availability — and pieces of the data for scale.")
    y0, y1 = top + 0.10, V.BODY_BOTTOM
    lw = 5.95
    # Replica set -----------------------------------------------------------
    y = V.section(slide, LEFT, y0, lw, "Replica set: copies for availability", icon="🔁",
                  fill=GREEN)
    cx = LEFT + lw / 2
    V.box(slide, cx - 1.30, y + 0.02, 2.60, 0.52, "Application (driver)", fill=LIGHT_GRAY,
          color=DARK_GRAY, size=14)
    V.arrow(slide, cx, y + 0.57, cx, y + 0.92, color=NAVY, width=2.0)
    V.text(slide, cx + 0.10, y + 0.57, 1.40, 0.35, "writes", size=12, bold=True, color=NAVY,
           anchor=MSO_ANCHOR.MIDDLE)
    V.box(slide, cx - 1.30, y + 0.95, 2.60, 0.72,
          [("PRIMARY", {"size": 14}), ("accepts writes", {"size": 12, "bold": False})],
          fill=NAVY, size=14)
    sw = 2.45
    sx = [LEFT + 0.10, LEFT + lw - sw - 0.10]
    sy = y + 2.25
    for k, x in enumerate(sx):
        V.arrow(slide, cx + (-0.60 if k == 0 else 0.60), y + 1.70, x + sw / 2, sy - 0.04,
                color=TEAL, width=2.0)
        V.box(slide, x, sy, sw, 0.72,
              [("SECONDARY", {"size": 14}), ("copies the oplog", {"size": 12, "bold": False})],
              fill=TEAL, size=14)
    V.text(slide, cx - 0.80, y + 1.78, 1.60, 0.34, "replicate", size=12, bold=True, color=TEAL,
           align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    V.callout(slide, LEFT, sy + 0.95, lw, y1 - (sy + 0.95), "Failover",
              "If the primary fails, the members elect a secondary as the new primary.",
              size=14)

    # Sharded cluster ---------------------------------------------------------
    rx = LEFT + lw + 0.45
    rw = RIGHT - rx
    y = V.section(slide, rx, y0, rw, "Sharded cluster: split data for scale", icon="🧩",
                  fill=PURPLE)
    mx = rx + 0.10
    V.box(slide, mx, y + 0.02, 2.60, 0.52, "Application (driver)", fill=LIGHT_GRAY,
          color=DARK_GRAY, size=14)
    V.arrow(slide, mx + 1.30, y + 0.57, mx + 1.30, y + 0.92, color=PURPLE, width=2.0)
    V.box(slide, mx, y + 0.95, 2.60, 0.72,
          [("mongos", {"size": 14}), ("query router", {"size": 12, "bold": False})],
          fill=PURPLE, size=14)
    V.arrow(slide, mx + 2.65, y + 1.31, rx + rw - 2.05, y + 1.31, color=ORANGE, width=1.75,
            dash=True)
    V.text(slide, mx + 2.60, y + 0.95, rx + rw - 2.05 - mx - 2.60, 0.34, "metadata", size=12,
           bold=True, color=ORANGE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    V.cylinder(slide, rx + rw - 2.00, y + 0.80, 2.00, 1.02, "Config servers", fill=ORANGE,
               size=13)
    gap = 0.18
    shw = (rw - 2 * gap) / 3
    for k, (name, fill) in enumerate([("Shard A", NAVY), ("Shard B", TEAL), ("Shard C", GREEN)]):
        x = rx + k * (shw + gap)
        V.arrow(slide, mx + 1.30, y + 1.70, x + shw / 2, sy - 0.04, color=PURPLE, width=1.75)
        V.box(slide, x, sy, shw, 0.72,
              [(name, {"size": 14}), ("a replica set", {"size": 12, "bold": False})],
              fill=fill, size=14)
    V.callout(slide, rx, sy + 0.95, rw, y1 - (sy + 0.95), "Shard key",
              "Decides which shard stores each document — Module 7.", size=14)
    done(slide, n, "Replica sets keep the data available through a failure; sharding lets it "
                   "grow past one server.")


# Hand-drawn slides, by topic number (see module01_flow.steps for the order).
SLIDES = {1: s01, 2: s02, 12: s12, 21: s21}


# ---------------------------------------------------------------------------
# Diagram slides: each diagram image is merged with the slide that explains it.
# Images live in scripts/new_content/diagrams/module01/ ("NN - Title.png"),
# copied from scripts/chatgpt_diagrams/diagrams/module01/.
# ---------------------------------------------------------------------------
DIAGRAM_DIR = HERE / "diagrams" / "module01"

import mdb_diagram_slides as DS  # noqa: E402

_tp = DS.tp


DIAGRAMS: dict[int, tuple[str, str, list[dict]]] = {
    3: ("Structured vs Semi-Structured vs Unstructured",
        "Rows and columns, nested fields, and data with no fixed fields.",
        [_tp("What it shows",
             "Three kinds of data side by side: a structured table of SKU, price and quantity; "
             "a semi-structured JSON product with nested specs and a tags array; and "
             "unstructured images, logs and video."),
         _tp("How to read it",
             "Read the caption under each panel: rows, columns and a fixed schema; nested "
             "fields and a flexible schema; no fixed fields."),
         _tp("Key point",
             "Relational tables are built for the first panel. Much of what modern applications "
             "store looks like the second.")]),
    4: ("Where Relational Databases Work Well",
        "A declared schema with keys and well-known joins.",
        [_tp("What it shows",
             "The training_store application sends SQL queries and joins to a declared schema of "
             "four tables: customers, orders, order_items and products."),
         _tp("How to read it",
             "PK marks each table's primary key and FK its foreign keys. The one-to-many lines "
             "show that a customer has many orders and an order has many items."),
         _tp("Key point",
             "When the structure is stable and the joins are well known, this model works very "
             "well.")]),
    5: ("Challenges with Traditional Relational Models",
        "One complete order needs joins across five tables.",
        [_tp("What it shows",
             "To build Complete Order #1048, the application joins customers, addresses, orders, "
             "order_items and payments."),
         _tp("How to read it",
             "Follow the JOIN arrows up to the order. The red text sums up the cost: multiple "
             "lookups, more work and higher latency."),
         _tp("Key point",
             "The more pieces one business object is split into, the more work every read "
             "does.")]),
    6: ("What Does NoSQL Mean?",
        "Not Only SQL: relational and non-relational models both exist.",
        [_tp("What it shows",
             "A SQL table on the left and the four NoSQL families on the right: document, "
             "key-value, column-family and graph."),
         _tp("How to read it",
             "The plus sign and the two-way arrow say both exist. NoSQL adds models; it doesn't "
             "remove SQL."),
         _tp("Key point",
             "NoSQL is a family of models, and SQL remains one of the options.")]),
    7: ("Why Organizations Adopt NoSQL",
        "Application growth drives four needs.",
        [_tp("What it shows",
             "Application growth in the center, pointing to four needs: flexible schema, "
             "horizontal scale, availability and faster delivery."),
         _tp("How to read it",
             "Each circle is one reason teams reach for a NoSQL database as the application "
             "grows."),
         _tp("Key point",
             "Teams adopt NoSQL for concrete needs, not because it is newer.")]),
    8: ("The Four Major NoSQL Database Types",
        "Document, key-value, column-family and graph.",
        [_tp("What it shows",
             "The four NoSQL families, each with a small example: a JSON-like document, a "
             "cart:1001 key pointing to a value, a wide row with stock_CA and stock_US columns, "
             "and a customer who bought a product and wrote a review."),
         _tp("How to read it",
             "Read the subtitle in each box: JSON-like aggregates, opaque value by key, wide rows "
             "with variable columns, nodes plus relationships."),
         _tp("Key point",
             "Each family is optimized for a different way of reading and writing data.")]),
    9: ("Document Databases and Their Use Cases",
        "Self-contained documents — shown with MongoDB and training_store.",
        [_tp("What it shows",
             "MongoDB and training_store in the center, surrounded by six use cases: product "
             "catalog, customer profile, order history, personalization, IoT and events, and "
             "content."),
         _tp("How to read it",
             "Each box is a kind of application object that maps naturally to one document."),
         _tp("Key point",
             "Document databases shine when one business object can live in one document.")]),
    10: ("Key-Value Databases",
         "Get a value by its exact key.",
         [_tp("What it shows",
              "A Session Service asks for session:abc and a Shopping Cart Service asks for "
              "cart:42. The key-value store returns each opaque value blob."),
          _tp("How to read it",
              "Solid red arrows are GET requests by key. Dashed arrows are the values coming "
              "back. The store matches the exact key only."),
          _tp("Key point",
              "Very fast when you know the key, but the store doesn't search inside the "
              "value.")]),
    11: ("Column-Family Databases",
         "Rows found by row key, with columns grouped into families.",
         [_tp("What it shows",
              "A table keyed by customerId with three column families: profile, orders and "
              "activity."),
          _tp("How to read it",
              "Look along a row. Customer 205 has no tier and no lastSeen, and customer 318 has "
              "no orders — the dashes are simply missing columns."),
          _tp("Key point",
              "Lookups start from the row key, and rows only store the columns they have.")]),
    13: ("Introducing MongoDB",
         "A document database: documents, collections, flexible schema, indexes and replica "
         "sets.",
         [_tp("What it shows",
              "MongoDB, a NoSQL document database, in the center, linked to documents, "
              "collections, flexible schema, indexes and replica sets."),
          _tp("How to read it",
              "The collections box lists our four training_store collections: products, "
              "customers, orders and reviews."),
          _tp("Key point",
              "These five ideas are the building blocks of the rest of the course.")]),
    14: ("The MongoDB Data Hierarchy",
         "Deployment → database → collection → document → field.",
         [_tp("What it shows",
              "Five levels, each containing the next: a deployment, the training_store "
              "database, the products collection, one document, and one field."),
          _tp("How to read it",
              "Read top to bottom and say contains at each arrow."),
          _tp("Key point",
              "Every command you type in mongosh works at one of these levels.")]),
    15: ("Relational-to-MongoDB Terminology",
         "Table → collection, row → document, column → field.",
         [_tp("What it shows",
              "Relational terms on the left and their MongoDB equivalents on the right, from "
              "database down to JOIN."),
          _tp("How to read it",
              "Schema maps to implicit, primary key maps to _id, and JOIN maps to embed or "
              "reference."),
          _tp("Key point",
              "The words map neatly; the designs often don't. A document can replace several "
              "joined rows.")]),
    16: ("Anatomy of a MongoDB Document",
         "Every field keeps a BSON type.",
         [_tp("What it shows",
              "One document from training_store.products with each field labeled by its BSON "
              "type."),
          _tp("How to read it",
              "_id is an ObjectId, sku a String, price a Decimal128, active a Boolean, "
              "createdAt a Date, tags an Array and specifications an embedded document."),
          _tp("Key point",
              "Unlike JSON, BSON stores real types, so money, dates and IDs behave "
              "correctly.")]),
    17: ("From Rows to Documents",
         "Three normalized tables become one order document.",
         [_tp("What it shows",
              "On the left, one order spread across the customers, orders and order_items "
              "tables. On the right, the same order as one document."),
          _tp("How to read it",
              "The customer becomes an embedded customer snapshot and the order items become an "
              "embedded items array. The total, 108.98, is carried across."),
          _tp("Key point",
              "The document is shaped like the thing the application shows: one order.")]),
    18: ("Flexible Schema Within a Collection",
         "Two products, one collection, different fields.",
         [_tp("What it shows",
              "A laptop document and a book document in the same products collection."),
          _tp("How to read it",
              "The highlighted fields are category-specific: cpu and ram for the laptop, isbn "
              "and pages for the book."),
          _tp("Key point",
              "Schema follows the product, not a single table shape.")]),
    19: ("MongoDB Architecture Overview",
         "Clients, the mongod server, the storage engine and the data files.",
         [_tp("What it shows",
              "Clients send a request to mongod, which passes the operation to the storage "
              "engine, which reads and writes the data files. The result returns to the "
              "client."),
          _tp("How to read it",
              "Follow the arrows left to right, then the red result arrow back. The faded "
              "servers above mongod are an optional replica set."),
          _tp("Key point",
              "mongod is the server process at the center of every MongoDB deployment.")]),
    20: ("How a MongoDB Request Is Processed",
         "Client → network → mongod → planner → documents → result.",
         [_tp("What it shows",
              "One find request for products, step by step, from the client to the result."),
          _tp("How to read it",
              "Each box is one stage: connect over the MongoDB protocol, parse and authorize, "
              "choose a plan, fetch matching documents, return BSON results."),
          _tp("Key point",
              "The query planner's choice, index or scan, decides how much work the request "
              "does.")]),
    22: ("Core MongoDB Features",
         "Six capabilities around training_store.",
         [_tp("What it shows",
              "MongoDB and training_store in the center, with six features around it: flexible "
              "documents, indexes, aggregation, replication, sharding and drivers."),
          _tp("How to read it",
              "Each circle is a capability we practise later in the course."),
          _tp("Key point",
              "MongoDB is more than flexible storage: it queries, indexes, aggregates and "
              "scales.")]),
    23: ("When to Use MongoDB",
         "Five signals that point to a document database.",
         [_tp("What it shows",
              "Five checked cards: varied attributes, data accessed together, evolving schema, "
              "document aggregates and horizontal growth."),
          _tp("How to read it",
              "Each card has a training_store example underneath, from product specifications "
              "to sharding growing orders."),
          _tp("Key point",
              "The more of these signals a workload shows, the better MongoDB fits.")]),
    24: ("When MongoDB May Not Be the Best Choice",
         "Five workloads where another model may fit better.",
         [_tp("What it shows",
              "Five warning cards: heavy cross-entity transactions, strict tabular reporting, "
              "tiny rows with no aggregate, graph-first traversal and a pure key-value cache."),
          _tp("How to read it",
              "Each card says consider alternatives. That means check the workload, not avoid "
              "MongoDB."),
          _tp("Key point",
              "Knowing when not to use a tool is part of choosing it well.")]),
    25: ("Scenario: Modernizing an Application",
         "Relational catalog → product document → products collection → same API.",
         [_tp("What it shows",
              "A relational catalog with many joins is reshaped into a product document, loaded "
              "into the products collection and served through the same catalog API."),
          _tp("How to read it",
              "Follow the arrows: reshape, load, serve."),
          _tp("Key point",
              "Modernizing starts with reshaping the data, not with copying the tables.")]),
    26: ("Module 1 at a Glance",
         "Six ideas around one module.",
         [_tp("What it shows",
              "A concept map of Module 1: why NoSQL, four models, MongoDB documents, hierarchy, "
              "embed versus reference, and architecture."),
          _tp("How to use it",
              "Point to each box and ask the class for one sentence about it before the "
              "knowledge check."),
          _tp("Key point",
              "Together these ideas are the vocabulary Module 2 and Module 3 build on.")]),
}


def main() -> None:
    prs = K.new_presentation()
    layout = K.blank_layout(prs)
    from module01_flow import steps

    F.build_sequence(prs, layout, steps(SLIDES, NOTES, DIAGRAMS, DIAGRAM_DIR))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    K.save_presentation(prs, OUT)
    print(f"Wrote {len(prs.slides)} slides -> {OUT.relative_to(ROOT)}")
    for w in V.WARNINGS:
        print("  WARN", w)


if __name__ == "__main__":
    main()
