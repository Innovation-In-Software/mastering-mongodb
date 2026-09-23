#!/usr/bin/env python3
"""Build the new-content Module 8 deck: Best Practices, Security and Troubleshooting.

Content comes from scripts/module08_content_source.md, the Module 8 manifest, the
official exercises 8.1-8.3 (labs/day-03/exercises/), Lab 7 (labs/day-03/lab7/) and
the training_store sample database. Styling reuses the house kit through mdb_deck_kit (read-only): title
block, red/black rail, footer, page numbers, key-takeaway bar, fonts and colours.
Hand-drawn visuals are native, editable PowerPoint shapes; concept diagrams come from
scripts/new_content/diagrams/module08/ (copied from scripts/chatgpt_diagrams/diagrams/
module08/, keeping the source number).

Module 8 is the last module of the course, so the deck closes with a course wrap-up
instead of a hand-off to another module.

Writes decks/pptx_new/MongoDB_Module08_Best_Practices_Security_and_Troubleshooting.pptx
and never touches decks/pptx/.

    python scripts/new_content/build_module08_new.py
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

from pptx.enum.text import MSO_ANCHOR  # noqa: E402

import mdb_deck_kit as K  # noqa: E402
import mdb_diagram_slides as DS  # noqa: E402
import mdb_flow_slides as F  # noqa: E402
import mdb_speaker_notes as SN  # noqa: E402
import mdb_visuals as V  # noqa: E402
from mdb_visuals import (  # noqa: E402
    BLACK, GREEN, LEFT, NAVY, ORANGE, PURPLE, RED, TEAL, WIDTH,
)
from module08_notes import NOTES  # noqa: E402

ROOT = HERE.parents[1]
OUT = (ROOT / "decks" / "pptx_new"
       / "MongoDB_Module08_Best_Practices_Security_and_Troubleshooting.pptx")
MODULE_LABEL = "MODULE 8"


def notes(n: int) -> str:
    return SN.compose(NOTES[n])


def new(prs, layout, n, title, subtitle):
    return V.content_slide(prs, layout, number=n, title=title, subtitle=subtitle)


def done(slide, n, takeaway):
    V.finish(slide, number=n, takeaway=takeaway, notes=notes(n))


# ---------------------------------------------------------------------------
def s01(prs, layout):
    slide = K._chapter_slide(
        prs, layout, tag=MODULE_LABEL,
        title="MongoDB Best Practices, Security, and Troubleshooting",
        subtitle="Model, tune, secure, recover and diagnose training_store — and decide "
                 "whether it is ready for production.",
        quote='"Production-ready is proven, not assumed."',
        module_label=MODULE_LABEL,
    )
    V.set_slide_label("slide 1")
    topics = [
        ("Data modeling", NAVY),
        ("Performance", PURPLE),
        ("Security", TEAL),
        ("Backup and recovery", GREEN),
        ("Troubleshooting", ORANGE),
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
        "1. Apply modeling, validation and evolution rules",
        "2. Tune queries, pipelines and indexes with explain",
        "3. Secure access with auth, roles, TLS, network",
        "4. Plan backups and prove restores (RPO, RTO)",
        "5. Monitor health and troubleshoot by layer",
        "6. Judge training_store's production readiness",
    ], icon="🎯", badge_color=RED, size=16)

    x = 6.75
    y = V.section(slide, x, top + 0.05, 6.05, "Six questions this module answers", icon="❓",
                  fill=NAVY)
    questions = [
        ("IS", "the model safe to grow?", NAVY),
        ("HOW", "do we prove it is fast?", PURPLE),
        ("WHO", "may do what — and from where?", TEAL),
        ("CAN", "we recover from a mistake?", GREEN),
        ("WHAT", "is wrong right now?", ORANGE),
        ("ARE", "we ready to go live?", RED),
    ]
    row_h, gap = 0.50, 0.09
    for i, (word, rest, fill) in enumerate(questions):
        ry = y + i * (row_h + gap)
        V.box(slide, x, ry, 2.05, row_h, word, fill=fill, size=13)
        V.text(slide, x + 2.2, ry, 3.85, row_h, rest, size=14, anchor=MSO_ANCHOR.MIDDLE)

    V.section(slide, LEFT, 5.02, WIDTH, "Module roadmap", icon="🗺️", fill=PURPLE)
    V.chevrons(slide, LEFT, 5.50, WIDTH, 0.80,
               ["Model", "Validate", "Tune", "Secure", "Recover", "Diagnose", "Go-live?"],
               [NAVY, PURPLE, TEAL, ORANGE, GREEN, RED, BLACK], size=13)
    done(slide, n, "Production-ready is a claim you prove with evidence — not a feeling "
                   "you have.")


# Hand-drawn slides, by topic number (see module08_flow.steps for the order).
SLIDES = {1: s01, 2: s02}


# ---------------------------------------------------------------------------
# Diagram slides: each diagram image is merged with the slide that explains it.
# Images live in scripts/new_content/diagrams/module08/ ("NN - Title.png"), where NN
# is the diagram's number in scripts/chatgpt_diagrams/diagrams/module08/.
# ---------------------------------------------------------------------------
DIAGRAM_DIR = HERE / "diagrams" / "module08"

_tp = DS.tp


DIAGRAMS: dict[int, tuple[str, str, list[dict]]] = {
    3: ("From Functional to Production-Ready",
        "Functional, hardened, production-ready.",
        [_tp("What it shows",
             "Three columns. Functional: clients and one mongod with training_store. "
             "Hardened: the same server plus Auth + TLS, indexes, validation and backups. "
             "Production-ready: Auth + TLS in front of a three-member replica set, with "
             "monitoring, alerts and automated backup."),
         _tp("How to read it",
             "Follow the arrows: secure and optimize, then replicate and operate."),
         _tp("Key point",
             "Each step adds controls around the same data; the collections don't "
             "change.")]),
    7: ("Choose Document Boundaries Carefully",
        "Two questions decide embed or reference.",
        [_tp("What it shows",
             "A decision tree: read and updated together? Then bounded size? Otherwise "
             "shared by many? Each leaf is EMBED or REFERENCE with a training_store "
             "example."),
         _tp("How to read it",
             "Left branch: order items embed; reviews are referenced because they grow "
             "without limit. Right branch: customers are referenced because they are "
             "shared; product dimensions embed because they are owned."),
         _tp("Key point",
             "Embed bounded, owned data. Reference shared, independent or unbounded "
             "data.")]),
    10: ("Use Consistent Field Names and Types",
         "Mixed input is normalized into one canonical document.",
         [_tp("What it shows",
              "Three product documents with different names and types are standardized, "
              "normalized and validated, then written as one canonical shape: _id "
              "ObjectId, productId ObjectId, name String, price Decimal128, createdAt "
              "Date."),
          _tp("How to read it",
              "Left: the drift. Middle: the four fixes. Right: camelCase names and "
              "stable BSON types."),
          _tp("Key point",
              "One name and one type per concept, enforced by validation.")]),
    11: ("Apply Schema Validation",
         "mongod checks every insert and update.",
         [_tp("What it shows",
              "Inserts and updates from mongosh and Compass reach mongod, where a "
              "$jsonSchema rule on products checks the document. Valid documents are "
              "stored; invalid ones are rejected with a validation error."),
          _tp("How to read it",
              "Green path valid, red path invalid."),
          _tp("Key point",
              "A flexible schema can still refuse bad data at the database.")]),
    12: ("Plan for Schema Evolution",
         "v1, v2 compatible, v3 migrated.",
         [_tp("What it shows",
              "Three document versions with schemaVersion 1, 2 and 3. Version 2 adds an "
              "optional category; version 3 backfills it and updates the validator."),
          _tp("How to read it",
              "The old app still reads v1 and v2: that is backward compatibility during "
              "the migration."),
          _tp("Key point",
              "Evolve in compatible steps; tighten validation last.")]),
    13: ("Preserve Historical Snapshots",
         "The order keeps the price paid.",
         [_tp("What it shows",
              "Product P101, Course Bundle, costs 89 at purchase. The order copies the "
              "name and price into a productSnapshot. Later the product price becomes 99, "
              "but the order still keeps 89."),
          _tp("How to read it",
              "Copy at purchase, later update, historical truth."),
          _tp("Key point",
              "Snapshot duplication is deliberate: it records what happened.")]),
    21: ("Reduce Pipeline Input Early",
         "Filter and trim before you group.",
         [_tp("What it shows",
              "10,000 orders enter; $match keeps 1,200 paid orders; $project keeps two "
              "fields; $group totals by customer."),
          _tp("How to read it",
              "Each box shows how much data flows to the next stage."),
          _tp("Key point",
              "Less input to $unwind and $group means less work everywhere after.")]),
    24: ("Validate Aggregation Calculations",
         "Compare the pipeline with a control total.",
         [_tp("What it shows",
              "Three sample orders totalling 120, 80 and 100. The $group result says 300; "
              "a separate control total also says 300; the report is validated."),
          _tp("How to read it",
              "Aggregate, recalculate, compare, then validate."),
          _tp("Key point",
              "A fast report that is wrong is still wrong.")]),
    25: ("Indexing Best Practices",
         "A frequent query shape becomes an ESR compound index.",
         [_tp("What it shows",
              "The frequent query filters by customerId and status and sorts by orderDate. "
              "The compound index customerId + status + orderDate follows Equality, "
              "Equality, Sort. IXSCAN examines 20 keys and returns 20 documents; no "
              "COLLSCAN."),
          _tp("How to read it",
              "The coloured arrows map each query field to its index position."),
          _tp("Key point",
              "Design indexes around the query shapes the application really runs.")]),
    29: ("Review Explain Plans",
         "Read the plan and four numbers.",
         [_tp("What it shows",
              "orders.find by customerId with explain('executionStats'). The winning plan "
              "is IXSCAN on customerId_1, then FETCH, returning 24 documents. nReturned, "
              "keysExamined and docsExamined are all 24; executionTimeMillis is 3."),
          _tp("How to read it",
              "Examined roughly equal to returned is an efficient plan."),
          _tp("Key point",
              "explain() is the evidence behind every index decision.")]),
    30: ("MongoDB Security Principles",
         "TLS, authenticate, authorize, least privilege, encrypt, audit.",
         [_tp("What it shows",
              "Clients connect over TLS, pass through authenticate, authorize with RBAC and "
              "least privilege, and reach training_store over an encrypted connection. The "
              "data is encrypted at rest and activity goes to audit logs."),
          _tp("How to read it",
              "Left to right is the path of every request."),
          _tp("Key point",
              "Security is layered: no single control is enough.")]),
    31: ("Authentication",
         "Prove who is connecting.",
         [_tp("What it shows",
              "Credentials go over TLS to authenticate the identity. mongod verifies them "
              "against its user records. Success opens an authenticated session; invalid "
              "credentials are locked out."),
          _tp("How to read it",
              "Green path success, red path refusal."),
          _tp("Key point",
              "No valid identity, no access.")]),
    33: ("Principle of Least Privilege",
         "Grant only the access the job requires.",
         [_tp("What it shows",
              "A support analyst needs to read reviews. The minimum role grants find on "
              "reviews only. Products, customers and orders stay locked; there is no write "
              "and no access to other collections."),
          _tp("How to read it",
              "One green unlocked row; everything else is locked."),
          _tp("Key point",
              "Least privilege limits the damage any one identity can do.")]),
    34: ("Network Security",
         "TLS, a firewall and a private network.",
         [_tp("What it shows",
              "mongosh and Compass connect over TLS to a firewall that allows trusted IPs "
              "on port 27017. mongod lives in a trusted network and requires TLS. An "
              "untrusted source is blocked."),
          _tp("How to read it",
              "Only the green path reaches the database."),
          _tp("Key point",
              "Unreachable is the strongest protection.")]),
    42: ("Replication vs. Backup",
         "High availability versus point-in-time recovery.",
         [_tp("What it shows",
              "Left: a primary replicating continuously to two secondaries with automatic "
              "failover; a bad change is replicated to all three. Right: scheduled "
              "immutable backups in a repository, used to restore an earlier state."),
          _tp("How to read it",
              "The red marks on the left are the same damaged data on every member."),
          _tp("Key point",
              "Replication keeps you running; backups let you go back.")]),
    45: ("Recovery Point and Recovery Time Objectives",
         "Last backup 10:00, failure 10:15, restored 10:45.",
         [_tp("What it shows",
              "A timeline. The last backup is at 10:00, the failure at 10:15, and service "
              "is restored at 10:45. RPO is 15 minutes of possible data loss; RTO is 30 "
              "minutes of downtime."),
          _tp("How to read it",
              "RPO looks back from the failure; RTO looks forward to recovery."),
          _tp("Key point",
              "Both are business targets measured in time.")]),
    46: ("Restore Testing",
         "Restore to an isolated environment and prove it.",
         [_tp("What it shows",
              "A mongodump snapshot is restored into an isolated test environment. "
              "Automated checks confirm collections, document counts and sample queries. "
              "The restore is verified: data intact, RTO measured."),
          _tp("How to read it",
              "Restore, validate, confirm."),
          _tp("Key point",
              "A backup is only proven when a restore has worked.")]),
    49: ("Database, Query, and Resource Metrics",
         "Three groups of signals feed one health dashboard.",
         [_tp("What it shows",
              "Database metrics: operations per second, connections, replication lag. "
              "Query metrics: query latency, scanned versus returned, slow queries. "
              "Resource metrics: CPU, memory, disk I/O."),
          _tp("How to read it",
              "All three groups feed the health dashboard on the right."),
          _tp("Key point",
              "Watch the query metrics, not only CPU.")]),
    54: ("Troubleshooting Methodology",
         "Symptom, layer, cause, fix — then verify.",
         [_tp("What it shows",
              "The orders query is slow. The layer is query execution in mongod. The cause "
              "is a collection scan for customerId: a missing index. The fix creates "
              "orders.customerId_1 and latency is restored."),
          _tp("How to read it",
              "Reproduce, isolate the layer, confirm with explain, then verify from the "
              "symptom again."),
          _tp("Key point",
              "Evidence first, then the smallest safe fix.")]),
    59: ("Slow Application Investigation",
         "From a 2.8-second search to an 85-millisecond one.",
         [_tp("What it shows",
              "A slow product search is traced to training_store.products with a category "
              "filter and a price sort. explain() shows COLLSCAN; a compound index on "
              "category and price makes it IXSCAN at 85 ms."),
          _tp("How to read it",
              "Trace, inspect, explain, fix, verify."),
          _tp("Key point",
              "Start from the request the user felt, not from the server.")]),
    67: ("Course Summary",
         "training_store from CRUD to production.",
         [_tp("What it shows",
              "mongosh and Compass connect to mongod and training_store; the course moves "
              "through CRUD and aggregation, indexes and validation, replication and "
              "sharding, and security, backup and monitoring."),
          _tp("How to use it",
              "Point to each block and ask the class what they can now do with it."),
          _tp("Key point",
              "Each module added one layer to the same database.")]),
}


def main() -> None:
    prs = K.new_presentation()
    layout = K.blank_layout(prs)
    from module08_flow import steps

    F.build_sequence(prs, layout, steps(SLIDES, NOTES, DIAGRAMS, DIAGRAM_DIR))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    K.save_presentation(prs, OUT)
    print(f"Wrote {len(prs.slides)} slides -> {OUT.relative_to(ROOT)}")
    for w in V.WARNINGS:
        print("  WARN", w)


if __name__ == "__main__":
    main()
