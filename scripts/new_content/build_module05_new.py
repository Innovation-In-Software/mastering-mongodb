#!/usr/bin/env python3
"""Build the new-content Module 5 deck: The Aggregation Framework.

Content comes from scripts/module05_content_source.md, the Module 5 manifest, the
official Exercises 5.1-5.4 (labs/day-02/exercises), Day 2 Lab 4
(labs/day-02/lab4/LAB-4-GUIDE.md) and the training_store sample database. Every pipeline, sample document and result uses
the real field names in datasets/training_store/load.js (paymentStatus,
fulfillmentStatus, items.quantity × items.unitPrice, name.first, ...). Styling
reuses the house kit through mdb_deck_kit (read-only). Hand-drawn visuals are
native, editable PowerPoint shapes; concept diagrams come from
scripts/new_content/diagrams/module05/.

Writes decks/pptx_new/MongoDB_Module05_The_Aggregation_Framework.pptx and never
touches decks/pptx/.

    python scripts/new_content/build_module05_new.py
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
from module05_notes import NOTES  # noqa: E402

ROOT = HERE.parents[1]
OUT = ROOT / "decks" / "pptx_new" / "MongoDB_Module05_The_Aggregation_Framework.pptx"
MODULE_LABEL = "MODULE 5"


def notes(n: int) -> str:
    return SN.compose(NOTES[n])


def new(prs, layout, n, title, subtitle):
    return V.content_slide(prs, layout, number=n, title=title, subtitle=subtitle)


def done(slide, n, takeaway):
    V.finish(slide, number=n, takeaway=takeaway, notes=notes(n))


# ---------------------------------------------------------------------------
def s01(prs, layout):
    slide = K._chapter_slide(
        prs, layout, tag=MODULE_LABEL, title="The Aggregation Framework",
        subtitle="Turn training_store documents into totals, rankings and reports — one "
                 "pipeline stage at a time.",
        quote='"Each stage receives documents, transforms them and passes them on."',
        module_label=MODULE_LABEL,
    )
    V.set_slide_label("slide 1")
    topics = [
        ("Pipelines", NAVY),
        ("Filter and shape", PURPLE),
        ("Group", TEAL),
        ("Arrays and joins", GREEN),
        ("Reports", ORANGE),
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
        "1. Explain how documents flow through a pipeline",
        "2. Filter and reshape with $match, $project, $set",
        "3. Summarize with $group and accumulators",
        "4. Expand items with $unwind; join with $lookup",
        "5. Build one report with several metrics",
        "6. Order stages for correct, cheap pipelines",
    ], icon="🎯", badge_color=RED, size=16)

    x = 6.75
    y = V.section(slide, x, top + 0.05, 6.05, "Six questions this module answers", icon="❓",
                  fill=NAVY)
    questions = [
        ("WHAT", "is an aggregation pipeline?", NAVY),
        ("HOW", "do we filter and shape documents?", PURPLE),
        ("HOW", "do we summarize many documents?", TEAL),
        ("HOW", "do we use arrays and other collections?", GREEN),
        ("HOW", "do we build one multi-metric report?", ORANGE),
        ("WHY", "does stage order matter?", RED),
    ]
    row_h, gap = 0.50, 0.09
    for i, (word, rest, fill) in enumerate(questions):
        ry = y + i * (row_h + gap)
        V.box(slide, x, ry, 2.05, row_h, word, fill=fill, size=13)
        V.text(slide, x + 2.2, ry, 3.85, row_h, rest, size=14, anchor=MSO_ANCHOR.MIDDLE)

    V.section(slide, LEFT, 5.02, WIDTH, "Module roadmap", icon="🗺️", fill=PURPLE)
    V.chevrons(slide, LEFT, 5.50, WIDTH, 0.80,
               ["Pipelines", "Filter", "Shape", "Group", "Arrays + joins", "Reports",
                "Performance"],
               [NAVY, PURPLE, TEAL, ORANGE, RED, GREEN, BLACK], size=13)
    done(slide, n, "A pipeline answers questions no single stored document can — one stage "
                   "at a time.")


# Hand-drawn slides, by topic number (see module05_flow.steps for the order).
SLIDES = {1: s01, 2: s02}


# ---------------------------------------------------------------------------
# Diagram slides: each diagram image is merged with the slide that explains it.
# Images live in scripts/new_content/diagrams/module05/ ("NN - Title.png"),
# copied from scripts/chatgpt_diagrams/diagrams/module05/ (NNN - Title.png).
# ---------------------------------------------------------------------------
DIAGRAM_DIR = HERE / "diagrams" / "module05"

import mdb_diagram_slides as DS  # noqa: E402

_tp = DS.tp


DIAGRAMS: dict[int, tuple[str, str, list[dict]]] = {
    3: ("Operational Queries vs. Aggregation",
        "find() returns stored documents; aggregate() computes new ones.",
        [_tp("What it shows",
             "On the left, find() with a filter on customerId C-104 and status completed returns "
             "three matching order documents. On the right, aggregate() runs $match, $group and "
             "$project and returns one computed result: C-104, three orders, totalSpent 428."),
         _tp("How to read it",
             "Compare the bottom bars: fast CRUD lookup of current records, versus computed "
             "summaries."),
         _tp("About the data",
             "The diagram uses a simplified status field and made-up customer numbers. "
             "training_store orders have paymentStatus and fulfillmentStatus instead."),
         _tp("Key point",
             "find() gives back what is stored. aggregate() gives back something new.")]),
    6: ("How Documents Move Through a Pipeline",
        "Six orders in, four after $match, two groups out.",
        [_tp("What it shows",
             "mongosh or Compass calls aggregate() on the orders collection. Six input "
             "documents stream into $match, four pass to $group by customerId, and $sort orders "
             "the two groups by totalSpent."),
         _tp("How to read it",
             "Follow the counts under each arrow: 6, 4, 2. The two result documents are C-104 "
             "with three orders and C-207 with one."),
         _tp("Key point",
             "Each stage only sees what the previous stage passed on.")]),
    9: ("Stage Order Matters",
        "Match then group is a report; group then match is an empty result.",
        [_tp("What it shows",
             "Top row: ten orders, $match on status completed keeps six, and $group by "
             "customerId makes two groups. Bottom row: $group runs first and outputs only _id "
             "and totalSpent, so the later $match has no status field to test."),
         _tp("How to read it",
             "Green is the correct order. Red marks the wrong one: status field removed, wrong "
             "or unusable filter."),
         _tp("Key point",
             "Filter on stored fields before $group removes them.")]),
    11: ("The $match Stage",
         "Keep only the documents that satisfy the filter.",
         [_tp("What it shows",
              "Eight orders enter $match with status PAID and total at least 100. Three "
              "documents come out, with totals 145, 320 and 210."),
          _tp("How to read it",
              "The pending order and the shipped order are dropped. Each remaining order meets "
              "both conditions."),
          _tp("About the data",
              "The diagram's status field stands for training_store's paymentStatus."),
          _tp("Key point",
              "$match uses the same filter language as find().")]),
    20: ("Inclusion and Exclusion with $project",
         "Keep the fields you list, or drop the fields you list.",
         [_tp("What it shows",
              "One product, a Laptop Stand, projected two ways. Inclusion keeps name, category "
              "and price. Exclusion drops supplierCost, stock and _id. Both give the same "
              "result document."),
          _tp("How to read it",
              "The banner at the bottom states the rule: do not mix inclusion and exclusion, "
              "except _id."),
          _tp("Key point",
              "Pick one style per projection; _id is the only exception.")]),
    25: ("Calculated Fields with $project",
         "Expressions compute new values for each document.",
         [_tp("What it shows",
              "An order with quantity 3, unitPrice 40.00, subtotal 120.00 and taxRate 0.13 goes "
              "through $project. It outputs lineTotal 120.00, tax 15.60 and grandTotal 135.60."),
          _tp("How to read it",
              "Read the three calculator rows: 3 × 40.00, then 120.00 × 0.13, then 120.00 + "
              "15.60. The stored document stays unchanged."),
          _tp("About the data",
              "training_store has no taxRate field; it stores tax as an amount. The line "
              "calculation, quantity times unitPrice, is exactly the one we use."),
          _tp("Key point",
              "Compute what isn't stored — the stored document never changes.")]),
    35: ("Time-Zone-Aware Reporting",
         "One UTC instant, three local times.",
         [_tp("What it shows",
              "An order's createdAt, 2026-09-20T14:30:00Z, goes through $dateToString with a "
              "timezone. Toronto shows Sep 20 10:30, Vancouver 07:30 and Delhi 20:00."),
          _tp("How to read it",
              "The red note says it all: same UTC instant, different local reporting times."),
          _tp("Key point",
              "Name the time zone whenever a report groups by day or month.")]),
    37: ("$cond Decision Flow",
         "If the condition is true use one value, otherwise the other.",
         [_tp("What it shows",
              "An order with total 120 and status PAID goes through $project with $cond. The "
              "test is total at least 100. True gives total × 0.90, false gives total. The "
              "result is finalTotal 108."),
          _tp("How to read it",
              "Follow the green TRUE path: 120 passes the test, so 10 percent comes off."),
          _tp("Key point",
              "$cond chooses a value for each document.")]),
    39: ("The $group Stage",
         "One output document per value of _id.",
         [_tp("What it shows",
              "Three orders: C101 with 120, C102 with 80 and C101 with 60. $group by customerId "
              "sums total and counts orders. The output is C101 with 180 and two orders, and "
              "C102 with 80 and one order."),
          _tp("How to read it",
              "Follow the two C101 arrows into the same group."),
          _tp("Key point",
              "_id is the grouping key; the other fields are accumulators.")]),
    46: ("Fields Lost During Grouping",
         "Only _id and the accumulators leave $group.",
         [_tp("What it shows",
              "Three orders with orderId, product, total and status. $group by customer with "
              "totalSpent gives C001 1225 and C002 75."),
          _tp("How to read it",
              "The red tags orderId, product and status are not carried forward into the "
              "grouped documents."),
          _tp("Key point",
              "If the report needs a field, keep it with an accumulator.")]),
    47: ("Grouping by Multiple Fields",
         "A compound _id: one group per combination.",
         [_tp("What it shows",
              "Four orders grouped with _id: { customer, status }. The result is three groups: "
              "C001 and completed, C001 and shipped, and C002 and completed with two orders "
              "totaling 250."),
          _tp("How to read it",
              "The key icon joins customerId and status into one grouping key."),
          _tp("About the data",
              "training_store has two status fields, so our version groups by paymentStatus "
              "and fulfillmentStatus."),
          _tp("Key point",
              "Every unique pair of values becomes its own summary document.")]),
    50: ("Why $sort Must Precede $limit",
         "Sort first, or the top N is an arbitrary N.",
         [_tp("What it shows",
              "Five products. On the left, $limit 3 runs before $sort, so the result is Laptop, "
              "Keyboard and Mouse: the top 3 of an arbitrary subset. On the right, $sort by "
              "price then $limit 3 gives Laptop, Monitor and Webcam: the true top 3."),
          _tp("How to read it",
              "Compare the two output rows. The Monitor at 300 is missing from the wrong one."),
          _tp("Key point",
              "Every top-N report is $sort, then $limit.")]),
    51: ("$count and $sortByCount",
         "Count the stream, or count and rank each value.",
         [_tp("What it shows",
              "Six reviews with ratings 5, 4, 5, 3, 4 and 5. $count totalReviews returns 6. "
              "$sortByCount on rating returns 5 stars 3, 4 stars 2 and 3 stars 1."),
          _tp("How to read it",
              "The upper path counts everything; the lower path groups, counts and sorts."),
          _tp("Key point",
              "These are exactly the six reviews in training_store.")]),
    53: ("Document Multiplication Through $unwind",
         "One document with a three-element array becomes three documents.",
         [_tp("What it shows",
              "Order 1042 with items Laptop, Mouse and Bag goes through $unwind \"$items\". "
              "Three order documents come out, each with a single item object."),
          _tp("How to read it",
              "In each output, items is one object, no longer an array."),
          _tp("Key point",
              "$unwind multiplies documents: one per array element.")]),
    61: ("Matched vs. Unmatched Lookup",
         "A match gives a one-element array; no match gives an empty one.",
         [_tp("What it shows",
              "Left: order O1001 with customerId C101 finds customer Asha, so customer holds "
              "one document. Right: order O1002 with customerId C999 finds nothing, so customer "
              "is an empty array."),
          _tp("How to read it",
              "Both orders stay in the output. Only the customer array differs."),
          _tp("About the data",
              "The diagram stores string ids for readability. In training_store, customerId "
              "holds the customer's ObjectId, and C101 is Aisha Khan."),
          _tp("Key point",
              "$lookup never drops an input document; an empty array means no match.")]),
    64: ("The $bucket and $bucketAuto Stages",
         "Fixed boundaries you choose, or ranges MongoDB chooses.",
         [_tp("What it shows",
              "Six prices, 25 to 900. $bucket with boundaries 0, 100, 500 and 1000 gives groups "
              "of 2, 3 and 1. $bucketAuto with three buckets gives three groups of two."),
          _tp("How to read it",
              "Left, you choose ranges; right, MongoDB balances them."),
          _tp("Key point",
              "Use $bucket when the business defines the bands.")]),
    65: ("The $facet Stage",
         "Several sub-pipelines, one input, one result document.",
         [_tp("What it shows",
              "Products flow into $facet with three parallel sub-pipelines: byCategory with "
              "$group, priceBands with $bucket and topRated with $sort and $limit 3. The output "
              "is a single result document with one array per facet."),
          _tp("How to read it",
              "Each coloured box in the result matches the sub-pipeline of the same colour."),
          _tp("About the data",
              "The diagram's products have ratings; in training_store ratings live in the "
              "reviews collection."),
          _tp("Key point",
              "$facet returns one document; each facet is an array.")]),
    76: ("Pipeline Development Workflow",
         "Define the output, then add and check one stage at a time.",
         [_tp("What it shows",
              "Six steps: define the output, inspect the input, add one stage, run and inspect "
              "in mongosh or Compass, build gradually with $set, $group and $sort, and finalize "
              "a correct, readable, reusable pipeline."),
          _tp("How to read it",
              "Steps 3 to 5 repeat until the result is right."),
          _tp("Key point",
              "Never write a ten-stage pipeline in one go.")]),
    79: ("Early vs. Late $match",
         "Filter first: less data, less work.",
         [_tp("What it shows",
              "Left: $match status PAID runs first, then $project and $group — fast, low work. "
              "Right: $project and $group handle all the data, and $match runs last — slow, "
              "high work."),
          _tp("How to read it",
              "Count the document icons between stages: fewer on the left."),
          _tp("Key point",
              "Put the most selective $match as early as possible.")]),
    86: ("Double-Counting After $unwind",
         "The order total repeats on every line.",
         [_tp("What it shows",
              "Order O-101 with orderTotal 120 and three items is unwound into three documents, "
              "each still carrying 120. $sum gives 360, double-counted. Grouping once per order "
              "gives the correct 120."),
          _tp("How to read it",
              "Red is the wrong sum, green the correct total."),
          _tp("Key point",
              "Don't sum an order field after unwinding its lines.")]),
    88: ("Module 5 at a Glance",
         "Filter, shape, group, join — and verify each stage.",
         [_tp("What it shows",
              "training_store orders flow through Filter ($match), Shape ($project), Group "
              "($group) and Join or arrays ($lookup, $unwind) to business insight."),
          _tp("How to use it",
              "Point to each box and ask the class for the stage they would use for one "
              "question, before the knowledge check."),
          _tp("Key point",
              "Stage order, $ field references and checking each stage are what make a pipeline "
              "right.")]),
}


def main() -> None:
    prs = K.new_presentation()
    layout = K.blank_layout(prs)
    from module05_flow import steps

    F.build_sequence(prs, layout, steps(SLIDES, NOTES, DIAGRAMS, DIAGRAM_DIR))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    K.save_presentation(prs, OUT)
    print(f"Wrote {len(prs.slides)} slides -> {OUT.relative_to(ROOT)}")
    for w in V.WARNINGS:
        print("  WARN", w)


if __name__ == "__main__":
    main()
