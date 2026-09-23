#!/usr/bin/env python3
"""Build the new-content Module 3 deck: Data Modeling with MongoDB.

Content comes from scripts/module03_content_source.md, the Module 3 manifest,
the official Exercises 3.1-3.9, Day 1 Lab 2 (labs/day-01/lab2, Steps 1-7) and the
training_store sample database. Styling reuses the house kit through
mdb_deck_kit (read-only): title block, red/black rail, footer, page numbers,
key-takeaway bar, fonts and colours. Concept diagrams come from
scripts/new_content/diagrams/module03/.

Writes decks/pptx_new/MongoDB_Module03_Data_Modeling_with_MongoDB.pptx and never
touches decks/pptx/.

    python scripts/new_content/build_module03_new.py
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

from pptx.enum.text import MSO_ANCHOR  # noqa: E402

import mdb_deck_kit as K  # noqa: E402
import mdb_flow_slides as F  # noqa: E402
import mdb_speaker_notes as SN  # noqa: E402
import mdb_visuals as V  # noqa: E402
from mdb_visuals import (  # noqa: E402
    BLACK, GREEN, LEFT, NAVY, ORANGE, PURPLE, RED, TEAL, WIDTH,
)
from module03_notes import NOTES  # noqa: E402

ROOT = HERE.parents[1]
OUT = ROOT / "decks" / "pptx_new" / "MongoDB_Module03_Data_Modeling_with_MongoDB.pptx"
MODULE_LABEL = "MODULE 3"


def notes(n: int) -> str:
    return SN.compose(NOTES[n])


def new(prs, layout, n, title, subtitle):
    return V.content_slide(prs, layout, number=n, title=title, subtitle=subtitle)


def done(slide, n, takeaway):
    V.finish(slide, number=n, takeaway=takeaway, notes=notes(n))


# ---------------------------------------------------------------------------
def s01(prs, layout):
    slide = K._chapter_slide(
        prs, layout, tag=MODULE_LABEL, title="Data Modeling with MongoDB",
        subtitle="Design documents around how the application reads, writes and grows — "
                 "then build training_store.",
        quote='"Data that is accessed together should be stored together."',
        module_label=MODULE_LABEL,
    )
    V.set_slide_label("slide 1")
    topics = [
        ("Documents and types", NAVY),
        ("Access patterns", PURPLE),
        ("Embed or reference", TEAL),
        ("Schema patterns", GREEN),
        ("Validate and build", ORANGE),
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
        "1. Read the structure of a MongoDB document",
        "2. Select the right BSON type for each value",
        "3. Identify the application's access patterns",
        "4. Model relationships by embedding or referencing",
        "5. Keep documents and arrays bounded",
        "6. Apply schema patterns and validation",
        "7. Build and query training_store",
    ], icon="🎯", badge_color=RED, size=16)

    x = 6.75
    y = V.section(slide, x, top + 0.05, 6.05, "Six questions this module answers", icon="❓",
                  fill=NAVY)
    questions = [
        ("WHAT", "is inside a document?", NAVY),
        ("WHICH", "type fits each value?", PURPLE),
        ("HOW", "does the application use the data?", TEAL),
        ("WHEN", "do we embed — or reference?", GREEN),
        ("WHICH", "patterns and pitfalls matter?", ORANGE),
        ("HOW", "do we enforce and build the model?", RED),
    ]
    row_h, gap = 0.50, 0.09
    for i, (word, rest, fill) in enumerate(questions):
        ry = y + i * (row_h + gap)
        V.box(slide, x, ry, 2.05, row_h, word, fill=fill, size=13)
        V.text(slide, x + 2.2, ry, 3.85, row_h, rest, size=14, anchor=MSO_ANCHOR.MIDDLE)

    V.section(slide, LEFT, 5.02, WIDTH, "Module roadmap", icon="🗺️", fill=PURPLE)
    V.chevrons(slide, LEFT, 5.50, WIDTH, 0.80,
               ["Documents", "Types", "Access", "Relationships", "Embed / ref", "Patterns",
                "Validate"],
               [NAVY, PURPLE, TEAL, ORANGE, RED, GREEN, BLACK], size=13)
    done(slide, n, "Shape each document around how the application uses it — then justify "
                   "every choice.")


# Hand-drawn slides, by topic number (see module03_flow.steps for the order).
SLIDES = {1: s01, 2: s02}


# ---------------------------------------------------------------------------
# Diagram slides: each diagram image is merged with the slide that explains it.
# Images live in scripts/new_content/diagrams/module03/ ("NN - Title.png"),
# copied from scripts/chatgpt_diagrams/diagrams/module03/.
# ---------------------------------------------------------------------------
DIAGRAM_DIR = HERE / "diagrams" / "module03"

import mdb_diagram_slides as DS  # noqa: E402

_tp = DS.tp


DIAGRAMS: dict[int, tuple[str, str, list[dict]]] = {
    3: ("Array of Embedded Documents",
        "One order document with an items array.",
        [_tp("What it shows",
             "The orders collection in training_store holds one order document, ORD-1042, "
             "with a customerId and an items array of three embedded documents: a Trail "
             "Backpack, a Water Bottle and a Hiking Cap."),
         _tp("How to read it",
             "Each numbered box, 0 to 2, is one array element with its own productId, name "
             "and qty fields. The bracket on the right marks them as embedded documents."),
         _tp("Values in the diagram",
             "The IDs and product names are illustrative. Our training_store orders use "
             "orderNumber, and each item holds productId, sku, name, quantity and unitPrice.")]),
    4: ("Numbers Stored as Strings",
        "A string price sorts in the wrong order.",
        [_tp("What it shows",
             "A product document whose price field holds the string \"100\". Sorting by price "
             "gives \"100\", \"20\", \"9\" — the wrong numeric order."),
         _tp("How to read it",
             "Follow the arrows: after converting the field to a number, the same values sort "
             "correctly as 9, 20, 100."),
         _tp("Key point",
             "The type decides how values compare, sort and calculate. For money we use the "
             "Decimal128 number type.")]),
    5: ("Modeling Product Catalogs",
        "Shared core fields plus flexible attributes in one collection.",
        [_tp("What it shows",
             "The products collection holds three kinds of product — a course, a laptop and a "
             "book. Each has the same shared core fields, sku, name, price and category, plus "
             "its own flexible attributes."),
         _tp("How to read it",
             "The dark block in each card is the shared core; the green block is the "
             "category-specific part. All three feed one catalog, queried by category, price "
             "and attributes, with indexes on sku and category."),
         _tp("Diagram versus dataset",
             "training_store has no course category: its categories are LAPTOP, SHOE, BOOK "
             "and ACCESSORY, and laptops store processor and memoryGB rather than cpu and "
             "ramGB. The shape is the same.")]),
    6: ("Model Data Around Access Patterns",
        "Operations first, then collections, then indexes.",
        [_tp("What it shows",
             "Three operations on the left — browse products, view an order, read reviews — "
             "feed a Design around queries step, which produces the products, orders and "
             "reviews collections."),
         _tp("How to read it",
             "Each arrow asks one question: read together, update together, growth rate. The "
             "band at the bottom is the method: query shape, aggregate boundary, embed or "
             "reference, index."),
         _tp("Diagram versus dataset",
             "The sample order embeds a small customer snapshot, and the sample category is "
             "\"Laptops\". training_store orders keep a customerId reference instead, and the "
             "category value is LAPTOP.")]),
    7: ("Relationship Types",
        "One-to-one, one-to-many and many-to-many.",
        [_tp("What it shows",
             "Three panels: a customer that has one profile, a customer that places many "
             "orders, and orders that contain many products while each product appears in many "
             "orders."),
         _tp("How to read it",
             "The 1, N and M labels on the arrows give the cardinality of each side."),
         _tp("Key point",
             "Name the relationship type first; then count how many sit on the many side.")]),
    8: ("Bounded vs Unbounded Arrays",
        "Three featured reviews versus every review ever written.",
        [_tp("What it shows",
             "Two versions of the same product document. On the left, featuredReviews holds at "
             "most three reviews. On the right, reviews keeps growing past ten thousand "
             "entries."),
         _tp("How to read it",
             "The green lock says max 3, predictable size. The red warnings say large document "
             "and costly updates."),
         _tp("Key point",
             "Embed arrays that stay small; move arrays that keep growing into their own "
             "collection.")]),
    9: ("Modeling Customer Profiles",
        "One profile document, read in one query.",
        [_tp("What it shows",
             "A customer profile document with identity, preferences, an addresses array with a "
             "home and a work address, loyalty and activity counts. Orders and reviews point "
             "back to it by customerId."),
         _tp("How to read it",
             "Everything inside the green card is embedded, so loading the profile is one "
             "read. The arrows on the right are references from other collections."),
         _tp("Diagram versus dataset",
             "training_store's C101 is simpler: name, contact, one SHIPPING address, "
             "preferences and status. It has no loyalty or activity counts.")]),
    10: ("Referencing Related Data",
         "Many review documents point to one product.",
         [_tp("What it shows",
              "One product document, P1001, in the products collection and three review "
              "documents in the reviews collection. Each review stores productId P1001, its "
              "own customerId, a rating and a comment."),
          _tp("How to read it",
              "The arrow is the productId reference: 1 product on the left, many reviews on "
              "the right."),
          _tp("Diagram versus dataset",
              "training_store reviews store the text in title and body rather than comment, "
              "and also copy the product's sku.")]),
    11: ("Embedding Decision Tree",
         "Three questions decide embed or reference.",
         [_tp("What it shows",
              "A decision tree with three questions: read together, bounded size and same "
              "lifecycle. Three yes answers lead to EMBED; any no leads to REFERENCE."),
          _tp("How to read it",
              "The two example boxes show both outcomes for product reviews: embedded in the "
              "product, or referenced from a separate reviews collection by product_id."),
          _tp("Key point",
              "The embed example only illustrates the shape. Reviews fail the bounded-size "
              "question, which is why training_store references them.")]),
    12: ("Hybrid Embedding and Referencing",
         "Orders reference customers and products, and embed their items.",
         [_tp("What it shows",
              "An order document in the middle. It references the customer document on the "
              "left through customerId, embeds an items array, and each item references a "
              "product document on the right through productId."),
          _tp("How to read it",
              "Each item carries a name snapshot, qty and unitPrice. The product itself keeps "
              "sku, name, inventory and currentPrice."),
          _tp("Diagram versus dataset",
              "training_store orders use createdAt instead of orderDate and quantity instead "
              "of qty, and products keep their current price in price.")]),
    13: ("Product and Order Relationship",
         "Orders keep a purchase snapshot of each product.",
         [_tp("What it shows",
              "Two products on the left, MongoDB Basics at a current price of 54.00 and Compass "
              "Lab at 22.00, and two orders on the right that bought them."),
          _tp("How to read it",
              "Each order item references the product by productId, but locks the name and "
              "unitPrice at purchase: 49.00 and 19.00, not today's prices."),
          _tp("Key point",
              "The reference says which product; the snapshot says what the customer paid.")]),
    14: ("Over-Normalized MongoDB Model",
         "Four collections and three joins for one order summary.",
         [_tp("What it shows",
              "An order document holding only a customerId and an itemIds array. To show an "
              "order summary, mongod has to join customers, products and reviews with three "
              "$lookup stages."),
          _tp("How to read it",
              "The red arrows are the joins; the red labels name the cost: many joins, "
              "complex reads."),
          _tp("Key point",
              "This is a relational design with MongoDB syntax — it loses the benefit of "
              "documents.")]),
    15: ("Inconsistent Field Names",
         "One field, three spellings, missed documents.",
         [_tp("What it shows",
              "Three order documents that store the customer as customerId, customer_id and "
              "custId. A find by customerId matches only the first."),
          _tp("How to read it",
              "Red crosses mark the documents the query misses. After standardizing the field, "
              "all three show green ticks."),
          _tp("Key point",
              "Queries match exact field names, so one name per field is a correctness "
              "rule.")]),
    16: ("Attribute Pattern",
         "Many optional attributes become key-value pairs.",
         [_tp("What it shows",
              "Three products with different top-level attributes — color and size, ram and "
              "storage, material and volume — normalized into one attributes array of "
              "{ k, v } pairs."),
          _tp("How to read it",
              "One index on attributes.k plus attributes.v then serves queries such as color = "
              "Blue or size = 10."),
          _tp("Key point",
              "The pattern trades a simple document shape for one index that covers every "
              "attribute.")]),
    17: ("Subset Pattern",
         "The hot few reviews live with the product.",
         [_tp("What it shows",
              "A product document with ratingAvg 4.7 and a recentReviews array of three, the "
              "hot subset. The reviews collection holds the complete history of 248 reviews."),
          _tp("How to read it",
              "The product page uses the fast common read. Load all reviews goes to the reviews "
              "collection by productId."),
          _tp("Key point",
              "Embed only the part the common page needs; reference the rest.")]),
    18: ("Computed Pattern",
         "Compute once, read many times.",
         [_tp("What it shows",
              "Five review documents for product P100 are aggregated once: 23 ÷ 5 = 4.6. The "
              "result is written to the product as ratingAvg 4.6 and reviewCount 5."),
          _tp("How to read it",
              "Green arrows are fast repeated reads. The red arrow shows a new review triggering "
              "a recompute."),
          _tp("Key point",
              "Store a calculated value when it is read far more often than its inputs "
              "change.")]),
    19: ("JSON Schema Validation",
         "A $jsonSchema validator checks every write.",
         [_tp("What it shows",
              "A product document passes through a $jsonSchema validator: bsonType object, "
              "required sku, name and price, with a type for each and price minimum 0."),
          _tp("How to read it",
              "Valid documents continue to mongod and the products collection; invalid ones "
              "are rejected."),
          _tp("Diagram versus lab",
              "The diagram uses bsonType number, which accepts any numeric type. Lab 2, Step 6, is "
              "stricter: price must be decimal, the Decimal128 type.")]),
    20: ("Validation Level and Action",
         "When the rules run, and what happens on failure.",
         [_tp("What it shows",
              "An insert with price -10 reaches mongod, which applies the validationLevel and "
              "then the validationAction."),
          _tp("How to read it",
              "validationLevel strict checks all inserts and updates; moderate checks inserts "
              "and updates to valid documents. validationAction error rejects the write; warn "
              "stores it and logs a warning."),
          _tp("Key point",
              "Level decides when rules run; action decides what a failure does.")]),
    21: ("Schema-Version Strategy",
         "Two shapes in one collection, one model in the application.",
         [_tp("What it shows",
              "The products collection holds schemaVersion 1 documents with name and price, "
              "and schemaVersion 2 documents with title and a pricing object of amount and "
              "currency."),
          _tp("How to read it",
              "A version-aware reader transforms v1, reads v2 and normalizes both into the "
              "current product model."),
          _tp("Key point",
              "Old and new documents can coexist while the migration runs.")]),
    22: ("Module 3 at a Glance",
         "Six steps from access patterns to a read model.",
         [_tp("What it shows",
              "Six boxes across the top: access patterns, relationships, document shape, "
              "schema patterns, guardrails and read model. Each feeds the four training_store "
              "collections below."),
          _tp("How to use it",
              "Point to each box and ask the class for one training_store example before the "
              "knowledge check."),
          _tp("Key point",
              "Together these steps are the modeling method Module 4 now queries.")]),
}


def main() -> None:
    prs = K.new_presentation()
    layout = K.blank_layout(prs)
    from module03_flow import steps

    F.build_sequence(prs, layout, steps(SLIDES, NOTES, DIAGRAMS, DIAGRAM_DIR))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    K.save_presentation(prs, OUT)
    print(f"Wrote {len(prs.slides)} slides -> {OUT.relative_to(ROOT)}")
    for w in V.WARNINGS:
        print("  WARN", w)


if __name__ == "__main__":
    main()
