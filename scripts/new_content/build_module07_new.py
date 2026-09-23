#!/usr/bin/env python3
"""Build the new-content Module 7 deck: Introduction to Replication and Sharding.

Content comes from scripts/module07_content_source.md, the Module 7 manifest, the
official Exercises 7.1 to 7.4 in labs/day-03/exercises/, Day 3 Lab 6
(labs/day-03/lab6/LAB-6-GUIDE.md) and the
training_store sample database. Styling reuses the house kit through
mdb_deck_kit (read-only): title block, red/black rail, footer, page numbers,
key-takeaway bar, fonts and colours. Hand-drawn visuals are native, editable
PowerPoint shapes; concept diagrams come from scripts/new_content/diagrams/module07/.

Writes decks/pptx_new/MongoDB_Module07_Introduction_to_Replication_and_Sharding.pptx
and never touches decks/pptx/.

    python scripts/new_content/build_module07_new.py
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
    BLACK, DARK_GRAY, GREEN, LEFT, LIGHT_GRAY, LIGHT_PURPLE, LIGHT_TEAL, MUTED, NAVY, ORANGE,
    PURPLE, RED, RIGHT, TEAL, WIDTH,
)
from module07_notes import NOTES  # noqa: E402

ROOT = HERE.parents[1]
OUT = ROOT / "decks" / "pptx_new" / "MongoDB_Module07_Introduction_to_Replication_and_Sharding.pptx"
MODULE_LABEL = "MODULE 7"


def notes(n: int) -> str:
    return SN.compose(NOTES[n])


def new(prs, layout, n, title, subtitle):
    return V.content_slide(prs, layout, number=n, title=title, subtitle=subtitle)


def done(slide, n, takeaway):
    V.finish(slide, number=n, takeaway=takeaway, notes=notes(n))


# ---------------------------------------------------------------------------
def s01(prs, layout):
    slide = K._chapter_slide(
        prs, layout, tag=MODULE_LABEL, title="Introduction to Replication and Sharding",
        subtitle="How replica sets keep training_store online through a failure — and how "
                 "sharding lets its orders grow past one server.",
        quote='"Replicate to stay online. Shard to grow."',
        module_label=MODULE_LABEL,
    )
    V.set_slide_label("slide 1")
    topics = [
        ("Availability vs scale", NAVY),
        ("Replica sets and failover", PURPLE),
        ("Read and write guarantees", TEAL),
        ("Sharded clusters and keys", GREEN),
        ("Routing and design", ORANGE),
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
        "1. Tell availability from scalability",
        "2. Explain replica-set roles, the oplog, failover",
        "3. Choose basic read and write settings",
        "4. Describe the parts of a sharded cluster",
        "5. Evaluate shard keys and query routing",
        "6. Decide when to replicate, shard, or both",
    ], icon="🎯", badge_color=RED, size=16)

    x = 6.75
    y = V.section(slide, x, top + 0.05, 6.05, "Six questions this module answers", icon="❓",
                  fill=NAVY)
    questions = [
        ("WHY", "do we need copies and pieces?", NAVY),
        ("HOW", "does a replica set survive failure?", PURPLE),
        ("WHICH", "member serves a read, and when?", TEAL),
        ("WHAT", "makes up a sharded cluster?", GREEN),
        ("HOW", "do we choose a shard key?", ORANGE),
        ("WHEN", "do we replicate, shard, or both?", RED),
    ]
    row_h, gap = 0.50, 0.09
    for i, (word, rest, fill) in enumerate(questions):
        ry = y + i * (row_h + gap)
        V.box(slide, x, ry, 2.05, row_h, word, fill=fill, size=13)
        V.text(slide, x + 2.2, ry, 3.85, row_h, rest, size=14, anchor=MSO_ANCHOR.MIDDLE)

    V.section(slide, LEFT, 5.02, WIDTH, "Module roadmap", icon="🗺️", fill=PURPLE)
    V.chevrons(slide, LEFT, 5.50, WIDTH, 0.80,
               ["Availability", "Replica sets", "Failover", "Guarantees", "Shard keys",
                "Routing", "Design"],
               [NAVY, PURPLE, TEAL, ORANGE, RED, GREEN, BLACK], size=13)
    done(slide, n, "Replication keeps the data available; sharding distributes the data and "
                   "the work.")


def s70(prs, layout):
    n = 70
    slide, top = new(prs, layout, n, "Replication and Sharding Together",
                     "A production-style cluster: orders sharded, every shard a replica set.")
    y0, y1 = top + 0.10, V.BODY_BOTTOM
    lw = 8.30
    # Application and routers ---------------------------------------------------
    ax, aw = LEFT + 1.00, 3.00
    V.box(slide, ax, y0, aw, 0.46, "Application (driver)", fill=LIGHT_GRAY, color=DARK_GRAY,
          size=14)
    my = y0 + 0.82
    mw, mh = 2.10, 0.62
    mx = [LEFT + 0.25, LEFT + 2.65]
    for k, x in enumerate(mx):
        V.arrow(slide, ax + aw / 2 + (-0.45 if k == 0 else 0.45), y0 + 0.49, x + mw / 2,
                my - 0.04, color=NAVY, width=1.75)
        V.box(slide, x, my, mw, mh,
              [(f"mongos {k + 1}", {"size": 14}), ("query router", {"size": 11, "bold": False})],
              fill=PURPLE, size=14)
    cx, cw = LEFT + lw - 2.35, 2.35
    V.cylinder(slide, cx, my - 0.22, cw, 1.02, "Config server\nreplica set", fill=ORANGE,
               size=12)
    V.arrow(slide, mx[1] + mw + 0.05, my + mh / 2, cx - 0.05, my + mh / 2, color=ORANGE,
            width=1.5, dash=True)
    V.text(slide, mx[1] + mw, my - 0.08, cx - mx[1] - mw, 0.30, "metadata", size=11, bold=True,
           color=ORANGE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # Shards -------------------------------------------------------------------
    sy = my + mh + 0.55
    gap = 0.20
    sw = (lw - 2 * gap) / 3
    shards = [("Shard A · primary shard", NAVY, "orders ranges 1 · 4"),
              ("Shard B", TEAL, "orders ranges 2 · 5"),
              ("Shard C", GREEN, "orders ranges 3 · 6")]
    for k, (name, fill, ranges) in enumerate(shards):
        x = LEFT + k * (sw + gap)
        for m in mx:
            V.arrow(slide, m + mw / 2, my + mh + 0.03, x + sw / 2, sy - 0.04, color=MUTED,
                    width=1.0)
        body = V.card(slide, x, sy, sw, y1 - sy, name, head_fill=fill, title_size=12)
        bw = (sw - 0.30 - 0.20) / 3
        for j, (lab, bf) in enumerate([("P", NAVY), ("S", TEAL), ("S", TEAL)]):
            V.box(slide, x + 0.15 + j * (bw + 0.10), body, bw, 0.42, lab, fill=bf, size=13)
        V.text(slide, x + 0.15, body + 0.46, sw - 0.30, 0.30, "replica set · own elections",
               size=11, color=MUTED, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        V.box(slide, x + 0.15, body + 0.84, sw - 0.30, 0.44, ranges, fill=LIGHT_PURPLE,
              color=PURPLE, size=12)
        if k == 0:
            V.box(slide, x + 0.15, body + 1.38, sw - 0.30, 0.80,
                  [("Unsharded: products,", {"size": 11}),
                   ("customers and reviews", {"size": 11}),
                   ("on the primary shard", {"size": 11, "bold": False})],
                  fill=LIGHT_TEAL, color=TEAL, size=11)

    px = LEFT + lw + 0.35
    F.stack_items(slide, px, y0, RIGHT - px, y1 - y0, [
        ("Sharding splits orders", "Its ranges are spread over three shards; mongos routes "
                                   "each request by shard key."),
        ("Replication protects each shard", "Every shard is its own replica set — P is the "
                                            "primary, S a secondary."),
        ("If a Shard B server fails", "Shard B elects a new primary; Shards A and C keep "
                                      "serving."),
        {"callout": ("Primary shard", "Unsharded collections live on one shard, not on "
                                      "all.")},
    ])
    done(slide, n, "Sharding distributes the data; replication protects every shard — "
                   "production clusters need both.")


# Hand-drawn slides, by topic number (see module07_flow.steps for the order).
SLIDES = {1: s01, 2: s02, 70: s70}


# ---------------------------------------------------------------------------
# Diagram slides: each diagram image is merged with the slide that explains it.
# Images live in scripts/new_content/diagrams/module07/ ("NN - Title.png"),
# copied from scripts/chatgpt_diagrams/diagrams/module07/ ("0NN - Title.png").
# ---------------------------------------------------------------------------
DIAGRAM_DIR = HERE / "diagrams" / "module07"

import mdb_diagram_slides as DS  # noqa: E402

_tp = DS.tp


DIAGRAMS: dict[int, tuple[str, str, list[dict]]] = {
    5: ("Requirement to Mechanism",
        "Stay online needs a replica set; handle growth needs a sharded cluster.",
        [_tp("What it shows",
             "mongosh and Compass use training_store. Below, two rows: the requirement stay "
             "online needs a replica set and delivers high availability; the requirement handle "
             "growth needs a sharded cluster and delivers horizontal scalability."),
         _tp("How to read it",
             "Read each row left to right: requirement, mechanism, result. In the replica set, "
             "the red node failure and the dashed automatic failover arrow show a secondary "
             "taking over."),
         _tp("A simplification to point out",
             "The sharded cluster draws each shard as one mongod and leaves out the config "
             "servers. In production every shard is a replica set, as we'll see in Part 4.")]),
    6: ("Vertical Scaling vs Horizontal Scaling",
        "Scale up one server, or scale out across servers.",
        [_tp("What it shows",
             "On the left, one mongod before and after an upgrade: the CPU, RAM and storage bars "
             "grow, and the red label says hardware limit. On the right, mongos distributes "
             "data and load to three shards, each with moderate CPU, RAM and storage use."),
         _tp("How to read it",
             "Compare the captions: scale up one server, or scale out across servers and add "
             "more shards."),
         _tp("A simplification to point out",
             "Again each shard is drawn as one mongod. In production each shard is a replica "
             "set.")]),
    10: ("Replica-Set Members",
         "One primary accepts writes; secondaries copy the data.",
         [_tp("What it shows",
              "mongosh and Compass send writes and reads to the PRIMARY, which accepts writes. "
              "Oplog replication arrows lead to two SECONDARY members, which copy data. Each "
              "member holds products, customers, orders and reviews."),
          _tp("How to read it",
              "The dashed lines underneath are heartbeats and voting between all members. The "
              "red line shows that when the primary is unavailable, a secondary is eligible "
              "for election."),
          _tp("Key point",
              "Every member holds the whole of training_store. Copies add redundancy, not "
              "capacity.")]),
    13: ("The Replication Oplog",
         "The primary records each change; secondaries tail the log and apply it.",
         [_tp("What it shows",
              "A new order is written on the primary. The primary records the operation in "
              "the oplog, local.oplog.rs, whose entries ts 101, 102 and 103 are an insert into "
              "orders, an update to products and an insert into reviews. Two secondaries tail "
              "the new entries and apply them in order."),
          _tp("How to read it",
              "Follow the red arrow into the capped, ordered log, then the teal arrows out to "
              "the secondaries."),
          _tp("About the sample document",
              "The diagram's { orderId: 1042, status: NEW } is simplified. A real training_store "
              "order has an orderNumber such as O6305 and a fulfillmentStatus of NEW.")]),
    16: ("Replica-Set Elections",
         "Heartbeat lost, vote, majority, new primary.",
         [_tp("What it shows",
              "A three-member set whose primary has lost its heartbeat. The election starts, "
              "Secondaries A and B vote, two of three votes are cast, and the winner is "
              "promoted: it now accepts writes, and Secondary B stays a secondary."),
          _tp("How to read it",
              "Follow the arrows: election starts, majority votes, promote winner. The line at "
              "the bottom says the most up-to-date eligible member wins."),
          _tp("Key point",
              "Two of three is a majority, so this set can lose one member and still elect a "
              "primary.")]),
    17: ("Automatic Failover",
         "Normal, detect, elect, recovered.",
         [_tp("What it shows",
              "Four stages. Normal: the client writes to the primary. Detect: the primary is "
              "down and heartbeats are missed. Elect: Secondary A wins the majority election. "
              "Recovered: writes resume on the new primary, mongod A, through the replica-set "
              "connection string."),
          _tp("How to read it",
              "At the end, Secondary B still copies data and the old primary is shown offline. "
              "When it returns, it rejoins as a secondary."),
          _tp("Key point",
              "No operator had to act: detection, election and recovery are automatic.")]),
    18: ("Application Behavior During Failover",
         "Transient error, topology refresh, retry.",
         [_tp("What it shows",
              "An application creates an order. The MongoDB driver, holding the replica-set "
              "URI and doing primary discovery, sends it to the primary. The primary is "
              "unavailable, so the write gets a transient error and pauses. The driver detects "
              "the topology change, discovers the new primary, reconnects and retries the "
              "eligible write, which succeeds and is acknowledged."),
          _tp("How to read it",
              "Left to right is time. The red box is the only moment the application sees a "
              "problem."),
          _tp("Key point",
              "Failover is survivable when the driver knows the whole replica set and the "
              "write can be retried safely.")]),
    34: ("Replica-Set Status and Health",
         "What rs.status() tells you.",
         [_tp("What it shows",
              "mongosh and Compass look at the replica set through rs.status(). The primary "
              "reports 12 ms and 10:00:08. Secondary A reports 18 ms, 10:00:08 and lag 0 s. "
              "Secondary B reports 240 ms, 10:00:03 and lag 5 s. The summary on the right: "
              "2 healthy, 1 delayed, majority available."),
          _tp("How to read it",
              "Compare the timestamps: Secondary B has applied the oplog up to five seconds "
              "earlier than the primary. Here delayed simply means lagging; it is not a "
              "configured delayed member."),
          _tp("Key point",
              "A lagging member is still healthy, and the majority is available, but the lag "
              "is worth watching.")]),
    24: ("Read Preferences",
         "Five modes decide which member serves a read.",
         [_tp("What it shows",
              "A read of products goes through the read preference. primary and "
              "primaryPreferred point to mongod-1, the primary with the freshest data; "
              "primaryPreferred can fall back to a secondary. secondary goes to mongod-2 or "
              "mongod-3; secondaryPreferred prefers them and can fall back to the primary. "
              "nearest picks the lowest-latency member."),
          _tp("How to read it",
              "Solid lines are the preferred targets, dashed lines the fallbacks."),
          _tp("Key point",
              "Only the primary is guaranteed to have the freshest data.")]),
    28: ("Common Write-Concern Levels",
         "w: 0, w: 1, w: majority, and majority plus journal.",
         [_tp("What it shows",
              "An insert of an orders document on the primary, replicated to two secondaries. "
              "Below, four panels. w: 0 has no acknowledgment. w: 1 is acknowledged by the "
              "primary. w: majority is acknowledged after the primary and one secondary have "
              "it. w: majority with j: true also has both members write the journal."),
          _tp("How to read it",
              "Count the green checks in each panel: none, one, two, and two with a disk "
              "icon."),
          _tp("Key point",
              "In a three-member set, majority means two members.")]),
    29: ("Read Concern",
         "readConcern: majority returns only majority-committed data.",
         [_tp("What it shows",
              "mongosh asks to find a confirmed order with readConcern majority. In the replica "
              "set, the primary and one secondary are marked majority committed. The result is "
              "committed order data and a consistent read."),
          _tp("How to read it",
              "The check marks show which members already have the data. Two of three is "
              "enough for a majority read."),
          _tp("Key point",
              "A majority read only returns data that can't be rolled back.")]),
    31: ("Replication Lag",
         "A lagging secondary returns stale data.",
         [_tp("What it shows",
              "An update sets an order's status to shipped on the primary at 10:00:00. "
              "Secondary A has applied it. Secondary B lags by five seconds and still shows "
              "confirmed at 09:59:55. Compass reads from the secondary and gets a stale "
              "result."),
          _tp("How to read it",
              "Compare the three status boxes and their clocks."),
          _tp("About the field",
              "The diagram's status field stands for fulfillmentStatus in training_store, "
              "whose values are upper case, such as SHIPPED.")]),
    33: ("Rollback Concepts",
         "An unreplicated write is undone when the old primary rejoins.",
         [_tp("What it shows",
              "The former primary accepted an update to shipped, but a network partition cut "
              "it off: an unreplicated write. The other two members held an election; the new "
              "primary and the secondary both have confirmed, the majority history. When the "
              "former primary rejoins and syncs, it rolls back the unreplicated write, and the "
              "replica set is consistent again."),
          _tp("How to read it",
              "Follow the red partition, the green election arrow, then the curved rejoin and "
              "sync arrows."),
          _tp("Key point",
              "Reads of the confirmed order go to the majority history.")]),
    39: ("Sharded-Cluster Components",
         "mongos, the config server replica set and replica-set shards.",
         [_tp("What it shows",
              "mongosh and Compass send queries to the mongos router, which routes them by "
              "shard key to three shards. Each shard is a replica set with a primary and two "
              "secondaries. The config server replica set, configsvr-1 to configsvr-3, "
              "exchanges cluster metadata with mongos."),
          _tp("A label to correct",
              "The box under the shards lists all four collections as sharded collections. In "
              "our design only orders is sharded; products, customers and reviews stay "
              "unsharded on the primary shard."),
          _tp("Key point",
              "Applications only ever talk to mongos.")]),
    40: ("Shards",
         "Each shard is a replica set holding part of the collection.",
         [_tp("What it shows",
              "mongosh and Compass connect to the mongos router, which routes by shard key to "
              "Shard A, B and C. Each is a replica set of a primary and two secondaries. The "
              "labels say Shard A holds orders for customerId A–H, Shard B I–P and Shard C Q–Z."),
          _tp("How to read it",
              "The bracket at the bottom: each shard stores part of the collection. The panel "
              "on the right shows the path training_store, orders, document, customerId."),
          _tp("About the labels",
              "The letter ranges are illustrative. In training_store, customerId is an "
              "ObjectId reference to a customer; the readable code, such as C101, is the "
              "customer's customerNumber.")]),
    46: ("Cardinality",
         "Many distinct values spread evenly; few values create hotspots.",
         [_tp("What it shows",
              "A sample of orders with a customerId and a status. Sharding on customerId, with "
              "high cardinality, spreads evenly: two documents on each shard. Sharding on "
              "status, with low cardinality, creates a hotspot: four documents on Shard A, one "
              "each on B and C."),
          _tp("How to read it",
              "Compare the two rows of cylinders. The document counts are illustrative; the "
              "point is that each status value is one bucket that can't be split."),
          _tp("Key point",
              "A key with a few values can never be divided into many ranges.")]),
    48: ("Monotonic Shard Keys",
         "Always-increasing values pile into the newest range.",
         [_tp("What it shows",
              "Four orders with orderDate 10:01, 10:02, 10:03 and 10:04 and a monotonic "
              "orderDate shard key. The ranges are below 10:00 on Shard A, 10:00 to 10:03 on "
              "Shard B, and above 10:03 on Shard C. The red arrows send every new order to "
              "Shard C, the newest range, marked as the write hotspot."),
          _tp("How to read it",
              "New values always increase, so all red arrows end at the same shard."),
          _tp("About the field",
              "orderDate stands for createdAt in training_store. The _id values are "
              "simplified; ours are ObjectIds.")]),
    50: ("Ranged Sharding",
         "Sorted shard-key values cut into contiguous ranges.",
         [_tp("What it shows",
              "Orders with customerId C1042, C4380, C6725 and C9011 are sorted by shard-key "
              "value into three chunks: C0000–C3999 on Shard A, C4000–C6999 on Shard B and "
              "C7000–C9999 on Shard C."),
          _tp("How to read it",
              "Follow each value down to its range and then to its shard. C4380 and C6725 "
              "share Chunk 2."),
          _tp("About the labels",
              "The C-numbers are readable stand-ins for customerId, which is an ObjectId in "
              "training_store.")]),
    51: ("Hashed Sharding",
         "Hash the value, then distribute the hash ranges.",
         [_tp("What it shows",
              "mongos routes through a hash shard key, hash(customerId). The hashed values, "
              "such as h001 and h4F3, are scattered evenly over Shards A, B and C. The panel "
              "below shows adjacent customers C101, C102 and C103 going to three different "
              "shards."),
          _tp("How to read it",
              "Each shard holds a mix of hash values, not a neat run of customers."),
          _tp("Key point",
              "Neighbours in the original order end up apart, which spreads writes but breaks "
              "range locality.")]),
    52: ("Zoned Sharding",
         "Zone ranges pin data to chosen shards.",
         [_tp("What it shows",
              "Queries go through mongos to the zone ranges on training_store.orders by "
              "shippingRegion: CA to the Canada zone on Shard A, US to the US zone on Shard B "
              "and EU to the EU zone on Shard C."),
          _tp("How to read it",
              "Each shard carries a zone tag and holds only that region's orders."),
          _tp("About the field",
              "shippingRegion is not in training_store; our orders have shippingAddress.country "
              "Canada or USA.")]),
    55: ("Chunks and Data Distribution",
         "The key space is cut into ranges; ranges are spread over shards.",
         [_tp("What it shows",
              "The orders collection, sharded on customerId, is divided into six chunks from "
              "C000–C199 to C900–C999. Shard A holds chunks 1 and 4, Shard B chunks 2 and 5, "
              "and Shard C chunks 3 and 6."),
          _tp("How to read it",
              "The line under the chunks says customerId in contiguous ranges; the note says "
              "chunks, not individual documents, are distributed."),
          _tp("Key point",
              "Placement is decided range by range.")]),
    57: ("The Balancer",
         "Detect imbalance, migrate chunks, even out the shards.",
         [_tp("What it shows",
              "The balancer detects that Shard A holds C1 to C4 while Shard B holds only C5 "
              "and Shard C only C6: 4, 1, 1. It migrates C3 to Shard B and C4 to Shard C. "
              "After balancing each shard has two chunks: 2, 2, 2."),
          _tp("How to read it",
              "Follow the red migrate-chunks arrows, then read the after row."),
          _tp("Key point",
              "Queries keep working while ranges move; mongos follows the updated "
              "metadata.")]),
    49: ("Query Isolation",
         "A query with the shard key goes to one shard.",
         [_tp("What it shows",
              "mongosh or Compass runs orders.find({ customerId: C1042 }). The query includes "
              "the shard key, so mongos maps customerId to Shard B and sends a targeted query "
              "there. Shards A and C are grey and idle. Shard B returns the matching orders."),
          _tp("How to read it",
              "Only one path is coloured: client, mongos, Shard B, result."),
          _tp("About the value",
              "C1042 is illustrative. In training_store you would look up the customer's _id "
              "first, as the next slide shows.")]),
    71: ("Deployment Decision Framework",
         "Standalone, replica set, scale up, or sharded cluster.",
         [_tp("What it shows",
              "A flowchart for the training_store workload. No need for high availability "
              "leads to a standalone mongod for development and learning. Data that fits one "
              "replica set leads to a replica set. Data that doesn't fit leads to the last "
              "question: no need for horizontal scale means scale vertically; yes means a "
              "sharded cluster whose shards are all replica sets."),
          _tp("How to read it",
              "Start at the top and answer each diamond in turn."),
          _tp("Key point",
              "Each step adds cost and operations work, so only take the next step when the "
              "previous one is not enough.")]),
}


def main() -> None:
    prs = K.new_presentation()
    layout = K.blank_layout(prs)
    from module07_flow import steps

    F.build_sequence(prs, layout, steps(SLIDES, NOTES, DIAGRAMS, DIAGRAM_DIR))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    K.save_presentation(prs, OUT)
    print(f"Wrote {len(prs.slides)} slides -> {OUT.relative_to(ROOT)}")
    for w in V.WARNINGS:
        print("  WARN", w)


if __name__ == "__main__":
    main()
