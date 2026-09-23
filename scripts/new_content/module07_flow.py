#!/usr/bin/env python3
"""Slide order for the Module 7 deck: from one replica set to a sharded cluster.

Every concept diagram is merged with the slide that explains it (diagram plus the
points only that slide adds), so no idea appears twice. Part openers, mongosh
examples on the training_store sample database, in-flow practice exercises, a
knowledge check, the official checkpoints (Exercises 7.1 to 7.4), the module's
official lab (Day 3 Lab 6) and a hand-off to Module 8 connect the ideas.
Worksheets live in labs/day-03/exercises/, the lab guide in labs/day-03/lab6/.

Failover and sharding commands appear only as instructor demonstrations on
disposable infrastructure; every slide that shows one says so.
"""
from __future__ import annotations

import mdb_diagram_slides as DS
import mdb_flow_slides as F
import mdb_glossary as G
from mdb_flow_slides import tp
from mdb_visuals import GREEN, NAVY, ORANGE, PURPLE, RED, TEAL

PARTS = ["Part 1\nAvailability and scale", "Part 2\nReplica sets", "Part 3\nGuarantees and lag",
         "Part 4\nShard keys", "Part 5\nRouting and design"]

DISPOSABLE = ("Failover and sharding commands run only on instructor-controlled, disposable "
              "infrastructure. Never step down or shard a shared class cluster.")


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
        *G.intro("module07"),
        F.story("From Module 6 to Module 7",
                "Our queries are fast on one server — now keep the data online and ready to grow.",
                gave_title="Module 6 gave us",
                gave=["Indexes shaped like our queries",
                      "explain(): IXSCAN versus COLLSCAN",
                      "The ESR guideline for compound keys",
                      "{ customerId: 1, createdAt: -1 } for history",
                      "Evidence before changing the design"],
                now=("Now", "Survive a server failure — and plan how orders can outgrow one "
                            "server."),
                path_title="Our path through Module 7",
                path=[("Availability versus scalability", "Part 1", NAVY),
                      ("Replica sets, the oplog and elections", "Part 2", PURPLE),
                      ("Failover and what the application sees", "Part 2", PURPLE),
                      ("Read preference, read and write concern", "Part 3", TEAL),
                      ("Replication lag and rollback", "Part 3", TEAL),
                      ("Sharded clusters and shard keys", "Part 4", GREEN),
                      ("Chunks, routing and the design decision", "Part 5", ORANGE)],
                takeaway="Module 6 made one server fast; Module 7 keeps training_store online and "
                         "lets it grow.",
                notes=[tp("Bridge from Module 6",
                          "In Module 6 we built indexes that match our query shapes and proved "
                          "them with explain. The customer-history index { customerId: 1, "
                          "createdAt: -1 } made one customer's orders fast."),
                       tp("The new question",
                          "A fast query doesn't help if the server is down, or if the orders "
                          "collection no longer fits on one server. This module answers both."),
                       tp("The same example",
                          "We stay with training_store: 17 orders from 6 customers today. The "
                          "customerId field from Module 6 comes back as our main shard-key "
                          "candidate."),
                       tp("Lab safety", DISPOSABLE)]),

        # Part 1 ------------------------------------------------------------
        F.bridge(PARTS, 0, "Part 1: Availability and Scale",
                 "Two different problems — and two different mechanisms.",
                 so_far=["Indexes make single queries fast",
                         "explain() shows the work each query does",
                         "training_store runs on one server so far"],
                 question="What should happen when a server fails — and when the data outgrows "
                          "one server?",
                 covers=["Requirement to mechanism", "Scaling up versus scaling out",
                         "Replication versus sharding", "What neither mechanism does"],
                 notes=[tp("Why start here",
                           "Replication and sharding are often confused. We first separate the "
                           "two problems: availability and scale."),
                        tp("What this part covers",
                           "Which mechanism solves which requirement, vertical and horizontal "
                           "scaling, and a side-by-side comparison.")]),
        F.diagram(img(5), "High Availability and Horizontal Scalability",
                  "Stay online needs a replica set; handle growth needs a sharded cluster.",
                  items=[("Stay online → replica set", "Copies of the same data; if the primary "
                                                       "fails, a secondary takes over."),
                         ("Handle growth → sharded cluster", "mongos spreads data and load "
                                                             "across several shards."),
                         ("Different problems", "Copies add availability, not capacity. Shards "
                                                "add capacity, not copies."),
                         {"callout": ("Simplified", "Each shard is drawn as one mongod; in "
                                                    "production it is a replica set.")}],
                  takeaway="Name the requirement first: staying online needs replication, "
                           "growing needs sharding.",
                  notes=dn(5)),
        F.diagram(img(6), "Vertical Scaling vs Horizontal Scaling",
                  "Scale up one server — or scale out across servers.",
                  items=[("Vertical: scale up", "More CPU, RAM and storage on one server — "
                                                "simple, until the hardware limit."),
                         ("Horizontal: scale out", "Add shards behind mongos; each holds part of "
                                                   "the data."),
                         ("The cost of scaling out", "More servers, routing, balancing and "
                                                     "monitoring."),
                         {"callout": ("Start simple", "Tune schema and indexes before you "
                                                      "shard.")}],
                  takeaway="Scale up while one server is enough; scale out when the data or the "
                           "writes outgrow it.",
                  notes=dn(6)),
        F.compare("Replication versus Sharding",
                  "What each mechanism delivers — and what neither does.",
                  ["Requirement", "Replication", "Sharding"],
                  [("Keep several copies", "Yes", "Not by itself"),
                   ("Automatic failover", "Yes", "Per shard, via replication"),
                   ("Grow data capacity", "Limited", "Yes"),
                   ("Spread write load", "Not normally", "Yes"),
                   ("Survive one server failure", "Yes", "Only with replicated shards"),
                   ("Main objective", "Availability", "Capacity and throughput"),
                   ("Undo last week's delete", "No — restore a backup", "No — restore a backup")],
                  [3.20, 2.45, 3.05], row_h=0.58, size=13,
                  items=[("Replication", "Every member holds the same data — redundancy, not "
                                         "more room."),
                         ("Sharding", "Each shard holds part of a collection — room and "
                                      "throughput."),
                         {"callout": ("Together", "Production clusters shard the data and "
                                                  "replicate every shard.")}],
                  takeaway="Replication copies the data; sharding divides it — and only a backup "
                           "undoes a mistake.",
                  notes=NOTES[7]),

        # Part 2 ------------------------------------------------------------
        F.bridge(PARTS, 1, "Part 2: Replica Sets and Failover",
                 "How several copies of training_store stay in step — and take over.",
                 so_far=["Availability and scale are different problems",
                         "Replication keeps copies for availability",
                         "Sharding divides data for capacity"],
                 question="How does a replica set keep every copy in step — and pick a new "
                          "primary?",
                 covers=["Primary and secondary members", "The oplog", "Elections and majority",
                         "Automatic failover", "What the application sees",
                         "Checking replica-set health", "Exercise: count the votes"],
                 notes=[tp("Why this part",
                           "Replica sets are the foundation of MongoDB high availability, and "
                           "every production shard is one. We look inside one now."),
                        tp("What to watch",
                           "Keep asking two questions: where do writes go, and who decides "
                           "the new primary?"),
                        tp("Lab safety", DISPOSABLE)]),
        F.diagram(img(10), "Replica-Set Members",
                  "One primary accepts writes; the secondaries copy the data.",
                  items=[("Primary", "The one member that accepts writes; by default it also "
                                     "serves reads."),
                         ("Secondaries", "Copy the primary's oplog and apply it — each keeps a "
                                         "full copy."),
                         ("Heartbeats and votes", "Members check each other every 2 seconds and "
                                                  "vote in elections."),
                         {"callout": ("Three members", "The common minimum for automatic "
                                                       "failover.")}],
                  takeaway="A replica set has one writable primary; the secondaries keep full "
                           "copies, ready to take over.",
                  notes=dn(10)),
        F.diagram(img(13), "The Replication Oplog",
                  "Every change is recorded once — and replayed on every secondary.",
                  items=[("Record every change", "The primary logs each insert, update and "
                                                 "delete in local.oplog.rs."),
                         ("Secondaries tail it", "They pull new entries and apply them in "
                                                 "order."),
                         ("Capped", "Fixed size: the oldest entries are overwritten — that span "
                                    "is the replication window."),
                         {"callout": ("Too far behind", "A member offline longer than the window "
                                                        "needs a full resync.")}],
                  takeaway="The oplog is the replication stream: secondaries replay it in "
                           "order to stay in step.",
                  notes=dn(13)),
        F.diagram(img(16), "Replica-Set Elections",
                  "A candidate needs votes from a majority of voting members.",
                  items=[("Trigger", "The members stop hearing the primary's heartbeat."),
                         ("Majority vote", "Two of three votes win; the most up-to-date "
                                           "eligible member is chosen."),
                         {"code": "voters  majority  can lose\n"
                                  "  3        2          1\n"
                                  "  4        3          1\n"
                                  "  5        3          2",
                          "label": "Why odd numbers are common", "size": 12},
                         {"callout": ("A fourth voter", "Adds cost, not failure tolerance.")}],
                  takeaway="Elections need a majority of voters — so three or five members, not "
                           "two or four.",
                  notes=dn(16)),
        F.diagram(img(17), "Automatic Failover",
                  "Normal, detect, elect, recovered — without an operator.",
                  items=[("1  Normal", "Writes go to the primary; the secondaries copy."),
                         ("2  Detect", "Heartbeats are missed — about 10 seconds by default."),
                         ("3  Elect", "Secondary A wins the majority vote and becomes "
                                      "primary."),
                         ("4  Recovered", "Writes resume; the old primary rejoins as a "
                                          "secondary.")],
                  takeaway="Failover is automatic, but there is a short window with no primary "
                           "and no writes.",
                  notes=dn(17)),
        F.diagram(img(18), "Application Behavior During Failover",
                  "Transient error, topology refresh, retry.",
                  items=[{"code": "mongodb://db1:27017,\n"
                                  "  db2:27017,db3:27017/\n"
                                  "  training_store\n"
                                  "  ?replicaSet=trainingRS",
                          "label": "Connect to the whole set", "size": 11},
                         ("Transient error", "Writes pause during the election; the driver sees "
                                             "a retryable error."),
                         ("Retryable writes", "The driver retries an eligible write once, on the "
                                              "new primary."),
                         {"callout": ("Design for it", "Idempotent operations and timeouts — "
                                                       "never a pinned host.")}],
                  takeaway="Use a replica-set connection string and retryable, idempotent "
                           "operations — failover becomes a pause.",
                  notes=dn(18)),
        F.diagram(img(34), "Checking Replica-Set Health",
                  "What rs.status() tells you — and what to watch.",
                  items=[{"code": "rs.status()\n"
                                  "rs.conf()\n"
                                  "rs.printSecondaryReplicationInfo()\n"
                                  "db.hello()",
                          "label": "Check health in mongosh", "size": 11},
                         ("Read the states", "One PRIMARY, the SECONDARY members, health: 1 on "
                                             "each reachable member."),
                         ("Watch the lag", "Secondary B is 5 s behind — healthy, but worth "
                                           "watching."),
                         {"callout": ("Lab 6", "Steps 4–7: you'll write this health "
                                               "report on a real replica set.")}],
                  takeaway="Measure replica-set health — the primary, the majority and the lag "
                           "— don't guess it.",
                  notes=dn(34)),
        F.exercise("Exercise: Count the Votes",
                   "Decide whether each replica set can still elect a primary.",
                   scenario="Every member below is a voting, data-bearing member.",
                   scenario_code="A  3 members, 1 down\n"
                                 "B  3 members, 2 down\n"
                                 "C  4 members, 2 down\n"
                                 "D  5 members split 3 | 2\n"
                                 "   across two data centers;\n"
                                 "   the link between them fails",
                   tasks=["Work out the majority for each set",
                          "Say whether a primary can exist",
                          "Say what happens to writes",
                          "Explain why D is split 3 | 2"],
                   expected=["A  yes — 2 of 3 still vote",
                             "B  no — 1 of 3: no writes",
                             "C  no — needs 3 of 4",
                             "D  the 3-member side elects",
                             "Odd voter counts decide cleanly"],
                   minutes=10,
                   takeaway="A primary needs a reachable majority of voters — count them before "
                            "you design.",
                   notes=[tp("How to run it",
                             "Pairs, five minutes, then take one answer per set. Point back to "
                             "the voters, majority, can-lose table on the elections slide."),
                          tp("A and B",
                             "Three voters need two. With one member down, two remain and a "
                             "primary can be elected. With two down, the survivor stays "
                             "SECONDARY: writes fail, and reads only work with a secondary read "
                             "preference."),
                          tp("C",
                             "Four voters need three. With two down only two remain, so there "
                             "is no primary. Four members tolerate one failure, the same as "
                             "three."),
                          tp("D",
                             "With five voters split three and two, the side with three still "
                             "has a majority and keeps or elects the primary. The side with two "
                             "can't. That is why teams place a majority of voters, or a tie-"
                             "breaking member, in a third location.")]),

        # Part 3 ------------------------------------------------------------
        F.bridge(PARTS, 2, "Part 3: Read and Write Guarantees, Lag and Rollback",
                 "Choose where reads go and when a write counts as safe.",
                 so_far=["Writes go to one primary",
                         "Secondaries replay the oplog",
                         "A majority elects a new primary"],
                 question="Which member should serve a read — and when is a write really "
                          "safe?",
                 covers=["Read preference", "Write concern", "Read concern",
                         "The three settings in mongosh", "Replication lag", "Rollback",
                         "Exercise: what did the customer see?"],
                 notes=[tp("Why this part",
                           "Replication is asynchronous. The settings in this part decide how "
                           "much that matters for each operation."),
                        tp("Three knobs",
                           "Read preference, read concern and write concern are three different "
                           "settings. By the end, learners should be able to say what each "
                           "one controls.")]),
        F.diagram(img(24), "Read Preferences",
                  "Five modes decide which members may serve a read.",
                  items=[("primary (default)", "Freshest data — the application reads its own "
                                               "writes."),
                         ("The Preferred modes", "primaryPreferred and secondaryPreferred prefer "
                                                 "one side, then fall back."),
                         ("secondary, nearest", "Any eligible secondary, or the lowest-latency "
                                                "member — may be stale."),
                         {"callout": ("Not free scaling", "Secondary reads can lag and compete "
                                                          "with replication.")}],
                  takeaway="Read from the primary by default; read from secondaries only where "
                           "stale data is acceptable.",
                  notes=dn(24)),
        F.diagram(img(28), "Write Concern",
                  "How many members must have a write before you get an answer.",
                  items=[("w: 0", "No acknowledgment — errors go unseen."),
                         ("w: 1", "The primary has it — lost if the primary fails before "
                                  "replicating."),
                         ("w: \"majority\"", "A majority has it — it survives a failover."),
                         ("j: true", "Also wait for the on-disk journal.")],
                  takeaway="Stronger write concern costs some latency and buys durability — match "
                           "it to the operation.",
                  notes=dn(28)),
        F.diagram(img(29), "Read Concern",
                  "Which data a read may return.",
                  items=[("local (default)", "The member's newest data — it could still roll "
                                             "back."),
                         ("majority", "Only data a majority has — it will not roll back."),
                         ("snapshot, linearizable", "Transactions, and the strongest "
                                                    "single-document reads."),
                         {"callout": ("Different question", "Read preference picks the member; "
                                                            "read concern the guarantee.")}],
                  takeaway="Read preference chooses where a read runs; read concern chooses what "
                           "it may return.",
                  notes=dn(29)),
        F.code("The Three Settings on training_store",
               "Write concern, read concern and read preference in mongosh.",
               [{"label": "Write concern: confirm a payment", "kind": "info", "code":
                 "db.orders.updateOne(\n"
                 "  { orderNumber: \"O6401\" },\n"
                 "  { $set: { paymentStatus: \"PAID\" } },\n"
                 "  { writeConcern: {\n"
                 "      w: \"majority\",\n"
                 "      wtimeout: 5000 } }\n"
                 ")"},
                {"label": "Read concern: committed data", "kind": "info", "code":
                 "db.orders.find(\n"
                 "  { paymentStatus: \"PAID\" }\n"
                 ").readConcern(\"majority\")"},
                {"label": "Read preference: a report", "kind": "info", "code":
                 "db.getMongo()\n"
                 "  .setReadPref(\n"
                 "    \"secondaryPreferred\")\n"
                 "db.orders.countDocuments(\n"
                 "  { fulfillmentStatus:\n"
                 "      \"SHIPPED\" })"}],
               points=[("Write concern", "How many members confirm the write before the answer."),
                       ("Read concern", "Local data, or only majority-committed data."),
                       ("Read preference", "Which member serves it — this report may lag.")],
               takeaway="Three different settings: who confirms a write, what a read returns, "
                        "and where it runs.",
               notes=[tp("Write concern",
                         "Order O6401 is Luis Romero's pending order for two Business Laptops, "
                         "total 2945.98. Confirming the payment with w majority means the "
                         "application only hears success once a majority has the change. "
                         "wtimeout stops it from waiting forever."),
                      tp("Don't change the shared data",
                         "This update is an example. Don't run it on the shared training_store: "
                         "later labs expect O6401's paymentStatus to be PENDING. To practise "
                         "write concerns, the instructor uses a scratch collection, repl_lab, "
                         "and deletes the probes afterwards."),
                      tp("Read concern",
                         "readConcern majority returns only paid orders that a majority has "
                         "acknowledged. On a fresh load that is 13 orders."),
                      tp("Read preference",
                         "setReadPref secondaryPreferred sends this shell's reads to a "
                         "secondary when one is available. The count of SHIPPED orders, 6 on a "
                         "fresh load, may be slightly behind the primary. db.hello() on "
                         "each connection shows which member answered.")]),
        F.diagram(img(31), "Replication Lag",
                  "A lagging secondary returns stale data.",
                  items=[("What it is", "How far a secondary's applied oplog trails the "
                                        "primary — 5 s here."),
                         ("Stale read", "The secondary still says confirmed; the primary says "
                                        "shipped."),
                         ("Common causes", "Slow disk, busy secondary, slow network, write "
                                           "bursts, long operations."),
                         ("First checks", "Member optimes and lag — then the secondary's CPU and "
                                          "disk.")],
                  takeaway="Small lag is normal; growing lag means stale reads and slower "
                           "failover — measure it.",
                  notes=dn(31)),
        F.diagram(img(33), "Rollback",
                  "A write the majority never saw is undone.",
                  items=[("Unreplicated write", "The old primary accepted shipped with w: 1, "
                                                "then lost its network."),
                         ("The majority moves on", "The other two members elect a primary that "
                                                   "never saw it."),
                         ("Rollback", "The old primary rejoins, undoes the write and saves it to "
                                      "a rollback file."),
                         {"callout": ("Prevention", "w: \"majority\" writes are not rolled "
                                                    "back.")}],
                  takeaway="Only majority-acknowledged writes survive a failover — use them for "
                           "anything that matters.",
                  notes=dn(33)),
        F.exercise("Exercise: What Did the Customer See?",
                   "Replay a failover during Luis Romero's payment.",
                   scenario="O6401 is PENDING. The payment service sets paymentStatus to PAID "
                            "with w: 1. The status page reads with secondaryPreferred.",
                   scenario_code="10:00:00  PAID written on primary\n"
                                 "10:00:00  acknowledged (w: 1)\n"
                                 "10:00:01  primary partitioned\n"
                                 "10:00:12  secondary elected\n"
                                 "10:00:30  old primary rejoins",
                   tasks=["State paymentStatus on the new primary",
                          "Say what happens to the PAID write",
                          "Say what the status page showed",
                          "Pick the settings you would change"],
                   expected=["PENDING — it never got PAID",
                             "Rolled back, saved to a file",
                             "PENDING: stale, then wrong",
                             "Payment: w: \"majority\"",
                             "Status page: primary reads"],
                   minutes=10,
                   takeaway="w: 1 can lose an acknowledged write; majority writes plus primary "
                            "reads keep the customer's view true.",
                   notes=[tp("How to run it",
                             "Give pairs five minutes. It is a thought experiment on the "
                             "diagrams from this part; nobody runs it on the shared cluster."),
                          tp("The new primary",
                             "The PAID update reached only the old primary. The elected "
                             "secondary never saw it, so on the new primary O6401 is still "
                             "PENDING."),
                          tp("The rollback",
                             "When the old primary rejoins, it rolls the PAID write back and "
                             "saves it to a rollback file. The payment service was told the "
                             "write succeeded, so someone now has to reconcile it by hand."),
                          tp("The status page",
                             "With secondaryPreferred, the page may have shown PENDING even "
                             "while the old primary had PAID, because of lag. After the "
                             "rollback, PENDING is the true state, but the customer was told "
                             "the payment went through."),
                          tp("The fix",
                             "Write payments with w majority, so success is only reported once "
                             "the write can't be rolled back. Read the order status from the "
                             "primary, or with read concern majority, right after a payment. "
                             "Exercise 7.2 practises exactly these choices.")]),

        # Part 4 ------------------------------------------------------------
        F.bridge(PARTS, 3, "Part 4: Sharded Clusters and Shard Keys",
                 "Split orders across servers — and choose the key that splits them.",
                 so_far=["Replica sets survive a server failure",
                         "Settings trade freshness for load and latency",
                         "Majority writes survive failover"],
                 question="How is a collection split across shards — and which field should "
                          "split it?",
                 covers=["Sharded-cluster components", "Shards as replica sets",
                         "Cardinality and frequency", "Monotonic keys", "Ranged sharding",
                         "Hashed and zoned sharding", "Candidate keys for orders"],
                 notes=[tp("Why this part",
                           "When orders outgrow one replica set, we shard. The most important "
                           "sharding decision is the shard key, and it is hard to change "
                           "later."),
                        tp("Our running candidate",
                           "Keep Module 6's customer-history query in mind: find one customer's "
                           "orders, newest first. A good shard key should keep that query on "
                           "one shard."),
                        tp("Lab safety", DISPOSABLE)]),
        F.diagram(img(39), "Sharded-Cluster Components",
                  "mongos routers, a config server replica set and replica-set shards.",
                  items=[("mongos", "The router applications connect to; it stores no "
                                    "collection data."),
                         ("Config server replica set", "Holds the metadata: which ranges live on "
                                                       "which shard."),
                         ("Shards", "Each is a replica set holding part of the sharded data."),
                         {"callout": ("Only sharded collections split", "The rest stay on one "
                                                                        "shard.")}],
                  takeaway="Applications talk to mongos; config servers hold the map; shards "
                           "hold the data.",
                  notes=dn(39)),
        F.diagram(img(40), "Shards",
                  "Each shard is a replica set holding part of the collection.",
                  items=[("Part of the collection", "Each shard owns its own ranges of orders — "
                                                    "here by customerId."),
                         ("A replica set per shard", "A primary and two secondaries, with its "
                                                     "own elections."),
                         ("Illustrative labels", "A–H, I–P, Q–Z stand in for ranges; our "
                                                 "customerId is an ObjectId."),
                         {"callout": ("Never a single mongod", "An unreplicated shard is a "
                                                               "single point of failure.")}],
                  takeaway="Sharding distributes the data between shards; replication keeps "
                           "each shard available.",
                  notes=dn(40)),
        F.diagram(img(46), "Cardinality and Frequency",
                  "Many distinct values spread evenly; a few values create hotspots.",
                  items=[("customerId: high", "Many distinct values — many split points, an even "
                                              "spread."),
                         ("status: low", "A handful of values — each one is a bucket that can't "
                                         "split."),
                         ("Frequency matters too", "One huge customer can still make one range "
                                                   "hot."),
                         {"callout": ("training_store", "fulfillmentStatus has only four "
                                                        "values.")}],
                  takeaway="Choose a shard key with many values that occur evenly — never a "
                           "status field.",
                  notes=dn(46)),
        F.diagram(img(48), "Monotonic Shard Keys",
                  "Always-increasing values pile into the newest range.",
                  items=[("Always increasing", "createdAt, sequential order numbers, "
                                               "ObjectId-based _id."),
                         ("Ranged key → hotspot", "Every new order lands in the top range, on "
                                                  "one shard."),
                         ("Fixes", "Hash the value, or lead with a high-cardinality field such "
                                   "as customerId."),
                         {"callout": ("Diagram field", "orderDate stands for our "
                                                       "createdAt.")}],
                  takeaway="A monotonic ranged key sends every new write to one shard — hash it "
                           "or lead with another field.",
                  notes=dn(48)),
        F.diagram(img(50), "Ranged Sharding",
                  "Sorted shard-key values cut into contiguous ranges.",
                  items=[("Contiguous ranges", "Sorted values are cut into ranges; each range "
                                               "lives on one shard."),
                         ("Good for ranges", "One customer's orders, or a date span, stay on "
                                             "few shards."),
                         ("Risk", "A monotonic key sends all new writes to the last range."),
                         {"code": "{ customerId: 1, createdAt: 1 }",
                          "label": "A ranged compound key", "size": 11}],
                  takeaway="Ranged sharding keeps neighbours together — great for range queries, "
                           "risky for rising keys.",
                  notes=dn(50)),
        F.diagram(img(51), "Hashed Sharding",
                  "Hash the value, then distribute the hash ranges.",
                  items=[("Hash first", "MongoDB hashes customerId and ranges the hash "
                                        "values."),
                         ("Even spread", "Neighbours C101, C102 and C103 land on different "
                                         "shards."),
                         ("Trade-off", "Equality finds stay targeted; range queries on the "
                                       "field scatter."),
                         {"code": "{ customerId: \"hashed\" }",
                          "label": "A hashed key", "size": 11}],
                  takeaway="Hashed sharding spreads writes evenly — and gives up efficient range "
                           "queries on that field.",
                  notes=dn(51)),
        F.diagram(img(52), "Zoned Sharding",
                  "Zone ranges pin chosen data to chosen shards.",
                  items=[("Pin ranges to shards", "Canadian orders stay on the Canada-zone "
                                                  "shard."),
                         ("Why", "Data residency, and keeping data near its users."),
                         ("Needs a key prefix", "We'd add a region field and lead the shard key "
                                                "with it."),
                         {"callout": ("Watch the skew", "A popular zone means hot shards.")}],
                  takeaway="Zones place data deliberately — for residency or locality — but "
                           "can concentrate load.",
                  notes=dn(52)),
        F.compare("Comparing Candidate Shard Keys for orders",
                  "Six candidates for training_store.orders — five on real fields, one what-if.",
                  ["Candidate", "Strength", "Concern"],
                  [("{ fulfillmentStatus: 1 }", "Status queries", "4 values: low cardinality"),
                   ("{ createdAt: 1 }", "Date-range queries", "Monotonic: write hotspot"),
                   ("{ customerId: 1 }", "Customer history", "A huge customer concentrates"),
                   ("{ customerId: \"hashed\" }", "Even write spread", "Ranges scatter"),
                   ("{ customerId: 1,\n  createdAt: 1 }", "History + date range",
                    "Depends on customer skew"),
                   ("{ region: 1, customerId: 1 }", "Regional placement",
                    "Needs a new region field")],
                  [3.30, 2.50, 2.90], row_h=0.60, size=13,
                  items=[("Our pick to test", "{ customerId: 1, createdAt: 1 } — it matches "
                                              "Module 6's history query."),
                         ("Validate it", "Test with production-like data and traffic before "
                                         "you choose."),
                         {"callout": ("No universal key", "Choose from the workload.")}],
                  takeaway="No shard key is universally right — score each candidate against the "
                           "real workload.",
                  notes=[tp("How to read the table",
                            "Each row is one candidate for training_store.orders, with what it "
                            "helps and what worries us."),
                         tp("The weak candidates",
                            "fulfillmentStatus has four values, so it can never make more than "
                            "four ranges. createdAt has many values, but every new order is the "
                            "newest, so ranged sharding on it makes a write hotspot."),
                         tp("The customer candidates",
                            "customerId targets one customer's history but a very large "
                            "customer can concentrate data. Hashed customerId spreads writes "
                            "evenly, and equality lookups are still targeted, but ranges on "
                            "customerId scatter."),
                         tp("The compound candidates",
                            "{ customerId: 1, createdAt: 1 } keeps each customer's orders "
                            "together in date order, so the history query and a customer's "
                            "date range are targeted. A region-first key allows zones, but our "
                            "orders have no region field; we would have to add one."),
                         tp("Link to Exercise 7.3",
                            "Checkpoint C scores these candidates on seven criteria. The "
                            "worksheet adds a tenantId candidate, which training_store doesn't "
                            "have; treat it as a what-if for multi-tenant platforms.")]),
        F.code("Sharding a Collection — Instructor Demonstration",
               "Run through mongos, on a disposable cluster only.",
               [{"label": "Ranged compound key", "kind": "info", "code":
                 "// disposable lab cluster only\n"
                 "db.orders.createIndex(\n"
                 "  { customerId: 1, createdAt: 1 })\n"
                 "sh.shardCollection(\n"
                 "  \"training_store.orders\",\n"
                 "  { customerId: 1, createdAt: 1 })"},
                {"label": "Or a hashed key", "kind": "info", "code":
                 "sh.shardCollection(\n"
                 "  \"training_store.orders\",\n"
                 "  { customerId: \"hashed\" })"},
                {"label": "Inspect the result", "kind": "info", "code":
                 "sh.status()\n"
                 "db.orders\n"
                 "  .getShardDistribution()"}],
               points=[("Through mongos", "Sharding commands run on a mongos connection."),
                       ("Index first", "The shard key needs a supporting index."),
                       ("Disposable only", "Never shard the shared class cluster.")],
               takeaway="Shard with a supporting index, through mongos, on a disposable cluster "
                        "— then inspect the result.",
               notes=[tp("What the commands do",
                         "createIndex builds the index that supports the shard key. "
                         "sh.shardCollection shards training_store.orders on that key. "
                         "sh.status shows shards, sharded collections, keys and ranges, and "
                         "getShardDistribution shows how much data each shard holds."),
                      tp("Choose one key",
                         "The second block is an alternative, not a second step. A collection "
                         "has one shard key; changing it later needs resharding."),
                      tp("Safety", DISPOSABLE),
                      tp("A hands-on demonstration",
                         "On the disposable cluster, use a scratch namespace, "
                         "training_shard.orders_lab, with the same key { customerId: 1, "
                         "createdAt: 1 }. Older versions also need "
                         "sh.enableSharding on the database first; follow the instructor's "
                         "exact commands. Atlas free-tier clusters are replica sets, not "
                         "sharded clusters, so learners without a mongos URI follow the "
                         "demonstration.")]),

        # Part 5 ------------------------------------------------------------
        F.bridge(PARTS, 4, "Part 5: Distribution, Routing and Design",
                 "How ranges move, how queries find them — and when to shard at all.",
                 so_far=["mongos, config servers and replica-set shards",
                         "A good key: many values, even use, not monotonic",
                         "Ranged, hashed and zoned sharding"],
                 question="How do ranges stay balanced and queries find them — and when should "
                          "we shard?",
                 covers=["Chunks", "The balancer", "Targeted queries",
                         "Targeted versus scatter-gather", "Replication and sharding together",
                         "The deployment decision", "Misconceptions and anti-patterns"],
                 notes=[tp("Why this part",
                           "The shard key decides placement. Now we see how placement stays "
                           "balanced, how mongos uses it to route queries, and how to decide "
                           "whether to shard at all."),
                        tp("Outcome",
                           "By the end, learners should be able to sketch a production "
                           "architecture for training_store and defend it.")]),
        F.diagram(img(55), "Chunks and Data Distribution",
                  "The key space is cut into ranges; ranges are spread over shards.",
                  items=[("Chunks are ranges", "Each non-overlapping range of the key lives on "
                                               "one shard."),
                         ("Not documents", "MongoDB moves whole ranges, never single "
                                           "documents."),
                         ("Metadata", "The config servers record which shard owns each "
                                      "range."),
                         {"callout": ("Training data", "Tiny data sets often sit in "
                                                       "one range.")}],
                  takeaway="Data is placed and moved range by range — the chunk map is what "
                           "mongos routes with.",
                  notes=dn(55)),
        F.diagram(img(57), "The Balancer",
                  "Detect imbalance, migrate ranges, even out the shards.",
                  items=[("Detect imbalance", "Shard A holds four chunks; Shards B and C "
                                              "hold one each."),
                         ("Migrate ranges", "C3 moves to Shard B, C4 to Shard C — two "
                                            "chunks each."),
                         ("Costs resources", "Migrations use network, disk and CPU — monitor "
                                             "them."),
                         {"callout": ("Modern versions", "Balance by data size, not chunk "
                                                         "count.")}],
                  takeaway="The balancer evens out the shards automatically — but migrations "
                           "have a cost, so watch them.",
                  notes=dn(57)),
        F.diagram(img(49), "Targeted Queries",
                  "A query that includes the shard key goes to one shard.",
                  items=[("Includes the shard key", "find({ customerId: … }) names the key."),
                         ("mongos routes", "The chunk map says Shard B — only Shard B works."),
                         ("The fastest shape", "Shards A and C stay free for other "
                                               "queries."),
                         {"callout": ("Value shown", "C1042 is illustrative; ours is an "
                                                     "ObjectId.")}],
                  takeaway="Put the shard key in your hot-path queries so mongos can target one "
                           "shard.",
                  notes=dn(49)),
        F.code("Targeted or Scatter-Gather on training_store?",
               "Assume orders is sharded on { customerId: 1, createdAt: 1 }.",
               [{"label": "Targeted: shard-key prefix", "kind": "good", "code":
                 "const c = db.customers.findOne(\n"
                 "  { customerNumber: \"C101\" })\n"
                 "db.orders\n"
                 "  .find({ customerId: c._id })\n"
                 "  .sort({ createdAt: -1 })"},
                {"label": "Scatter-gather: no shard key", "kind": "bad", "code":
                 "db.orders.find(\n"
                 "  { fulfillmentStatus:\n"
                 "      \"PROCESSING\" })\n"
                 "db.orders.find(\n"
                 "  { _id: someOrderId })"},
                {"label": "Check it with explain", "kind": "info", "code":
                 "db.orders\n"
                 "  .find({ customerId: c._id })\n"
                 "  .explain()\n"
                 "// winningPlan lists\n"
                 "// the shards used"}],
               points=[("Targeted", "mongos sends it to the shard owning that customer's "
                                    "range."),
                       ("Scatter-gather", "Every shard runs it; mongos merges the results."),
                       ("Not always wrong", "Fine for rare reports — costly in the hot path.")],
               takeaway="Queries with the shard-key prefix are targeted; the rest ask every "
                        "shard — keep those rare.",
               notes=[tp("The targeted query",
                         "We look up Aisha Khan, customer C101, and use her _id. The filter "
                         "names the leading field of the shard key, so mongos can send it to the "
                         "shard that owns her range. On a fresh load she has 5 orders."),
                      tp("The scatter-gather queries",
                         "fulfillmentStatus is not in the shard key, so every shard must search. "
                         "Three orders are PROCESSING on a fresh load: O6202, O6302 and O6401. "
                         "A lookup by _id alone also scatters, because _id is not part of this "
                         "shard key."),
                      tp("Proving it",
                         "On a sharded cluster, explain shows which shards took part; the "
                         "instructor can compare a targeted plan with a scatter-gather one on "
                         "the disposable cluster. On our replica set there is only one place "
                         "the data can be, so the difference "
                         "doesn't appear."),
                      tp("Not always wrong",
                         "A monthly report may scatter and that's fine. Frequent, high-volume "
                         "scatter-gather in the hot path means the shard key doesn't match the "
                         "workload.")]),
        S[70],
        F.diagram(img(71), "Deployment Decision Framework",
                  "Standalone, replica set, scale up — or shard.",
                  items=[("Development or learning", "A standalone mongod is enough."),
                         ("Production", "Start with a replica set of at least three members."),
                         ("Outgrown one replica set?", "Scale up first; shard when one set can't "
                                                       "hold the data or writes."),
                         {"callout": ("Shard with evidence", "Fix schema and indexes first.")}],
                  takeaway="Replicate every production deployment; shard only when measurements "
                           "show you must.",
                  notes=dn(71)),
        F.myths("Misconceptions and Anti-Patterns",
                "Beliefs that lead first distributed designs into trouble.",
                [("A replica set spreads writes over its members",
                  "All writes go to the primary; the secondaries copy them"),
                 ("Secondary reads always make apps faster",
                  "They may be stale and compete with replication"),
                 ("Sharding speeds up every query",
                  "Queries without the shard key ask every shard"),
                 ("Replication is a backup",
                  "A deleteMany is replicated too — keep real backups"),
                 ("The shard key is just another index",
                  "It decides placement and routing — and is hard to change")],
                ["Connecting to one host, not the set",
                 "Two or four voters instead of three or five",
                 "Sharding on fulfillmentStatus",
                 "A ranged key on createdAt",
                 "Sharding before fixing indexes"],
                remember=("Remember", "Replicate to stay online, shard to grow, back up to "
                                      "recover."),
                takeaway="Most distributed-design problems come from mixing up availability, "
                         "scale and recovery.",
                notes=[tp("Why this slide",
                          "Before the checks, clear away the beliefs that cause the most "
                          "trouble."),
                       tp("Writes and reads",
                          "A replica set does not spread writes: every write goes to the "
                          "primary. Secondary reads can help reporting, but they may be stale "
                          "and they compete with replication work."),
                       tp("Sharding",
                          "Sharding doesn't speed up every query: a query without the shard key "
                          "may contact every shard. More shards also mean more servers, "
                          "routing, monitoring and balancing. And the shard key is not just an "
                          "index: it decides where data lives and how queries are routed."),
                       tp("Backups",
                          "If someone runs db.orders.deleteMany({}), the delete is replicated "
                          "to every secondary. Replication also copies application bugs, bad "
                          "updates and malicious deletes. Resilience means replication, plus "
                          "backups, plus tested restores — Module 8 covers the last two.")]),

        # Wrap-up ------------------------------------------------------------
        F.knowledge("Knowledge Check", "Answer in your own words — then compare with a partner.",
                    ["What is the main purpose of replication? Of sharding?",
                     "What does the oplog do?",
                     "What starts an election, and why is a majority needed?",
                     "What is replication lag, and why does it matter?",
                     "Read preference, read concern, write concern: what does each control?",
                     "What does mongos do? What do config servers store?",
                     "Why is fulfillmentStatus a poor shard key?",
                     "Why can a ranged key on createdAt create a hotspot?",
                     "Targeted versus scatter-gather: what is the difference?",
                     "Is replication a replacement for backups?"],
                    notes=[tp("1. Purpose",
                              "Replication keeps copies of the same data for high availability "
                              "and automatic failover. Sharding divides data across servers for "
                              "capacity and write throughput."),
                           tp("2. Oplog",
                              "It is a capped collection that records every data change on the "
                              "primary. Secondaries copy the entries and apply them in order."),
                           tp("3. Elections",
                              "Members stop receiving the primary's heartbeats. A candidate "
                              "needs votes from a majority of voting members, so only one side "
                              "of a split can ever elect a primary."),
                           tp("4. Lag",
                              "How far a secondary's applied oplog trails the primary. It causes "
                              "stale secondary reads, and a member that falls outside the oplog "
                              "window needs a full resync."),
                           tp("5. Three settings",
                              "Read preference chooses which member serves a read. Read concern "
                              "chooses which data it may return. Write concern chooses how many "
                              "members must acknowledge a write."),
                           tp("6. mongos and config servers",
                              "mongos routes every application request to the right shards and "
                              "merges results. The config servers store the cluster metadata: "
                              "sharded collections, shard-key ranges and their shards."),
                           tp("7. fulfillmentStatus",
                              "It has only four values, so it can make at most four ranges, "
                              "and most writes go to the NEW range."),
                           tp("8. createdAt",
                              "Every new order has the largest createdAt so far, so every insert "
                              "lands in the last range, on one shard."),
                           tp("9. Routing",
                              "A targeted query includes the shard key or its prefix, so mongos "
                              "sends it to one or a few shards. A scatter-gather query goes to "
                              "every shard and mongos merges the results."),
                           tp("10. Backups",
                              "No. Replication copies deletes and mistakes to every member. Only "
                              "backups and tested restores recover from them.")]),
        F.exercise("Exercise 7.1 — Replication or Sharding?",
                   "Module 7 checkpoint A: match each requirement to its mechanism.",
                   kind="OFFICIAL CHECKPOINT A", minutes=10,
                   worksheet="labs/day-03/exercises/exercise-7.1-replication-or-sharding.md",
                   scenario="Write Replication, Sharding, Both or Neither yet for each "
                            "requirement.",
                   scenario_code="1  Survive one server failure\n"
                                 "2  Increase total data capacity\n"
                                 "3  Elect a replacement primary\n"
                                 "4  Distribute write load\n"
                                 "5  A local development database\n"
                                 "6  Production availability + scale",
                   tasks=["Classify requirements 1–3",
                          "Classify requirements 4–6",
                          "Explain why secondaries add no capacity",
                          "Compare with Lab 6: last week's delete"],
                   expected=["1 Replication · 2 Sharding",
                             "3 Replication · 4 Sharding",
                             "5 Neither yet: standalone",
                             "6 Both: sharded replica sets",
                             "Same data on each member"],
                   expected_title="Solution (after debrief)",
                   takeaway="Copies give availability, shards give capacity — and development "
                            "needs neither yet.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 7.1. The worksheet is "
                             "labs/day-03/exercises/exercise-7.1-replication-or-sharding.md. "
                             "It is classroom discussion; learners may look at training_store or "
                             "rs.status() to test ideas."),
                          tp("Running it",
                             "Seven minutes in pairs, then a three-minute debrief. Reveal the "
                             "solution column only after the groups share."),
                          tp("The borderline case",
                             "Copying data to secondaries does not increase capacity: each "
                             "member stores the same logical data set. Extra members add "
                             "redundancy, not a larger working set."),
                          tp("Link to Lab 6",
                             "Day 3 Lab 6, Step 1, adds one more row: recover an order deleted "
                             "last week. The answer is a backup, because replication and "
                             "sharding both copy or keep the delete.")]),
        F.exercise("Exercise 7.2 — Select Read and Write Settings",
                   "Module 7 checkpoint B: choose settings per business operation.",
                   kind="OFFICIAL CHECKPOINT B", minutes=20,
                   worksheet="labs/day-03/exercises/exercise-7.2-select-read-and-write-"
                             "settings.md",
                   scenario="For each operation choose a read preference, a read concern and a "
                            "write concern.",
                   scenario_code="Payment confirmation\n"
                                 "Financial reconciliation\n"
                                 "Product-catalog browsing\n"
                                 "Customer order status\n"
                                 "Operational reporting\n"
                                 "Noncritical analytics",
                   tasks=["Set the two money paths",
                          "State what you refuse to trade away",
                          "Set catalog, status and reporting",
                          "One sentence on staleness for each"],
                   expected=["Payment: primary + majority",
                             "Reconciliation: same bias",
                             "Catalog: primaryPreferred ok",
                             "Status: primary after payment",
                             "Analytics: secondaryPreferred"],
                   expected_title="Solution (after debrief)",
                   takeaway="Money paths get primary reads and majority writes; staleness is "
                            "accepted only where it's harmless.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 7.2. The worksheet is "
                             "labs/day-03/exercises/exercise-7.2-select-read-and-write-"
                             "settings.md."),
                          tp("Money paths",
                             "Payment confirmation reads from the primary, or primaryPreferred "
                             "only with a documented reason, writes with w majority, and reads "
                             "with majority, or snapshot inside a transaction. Reconciliation "
                             "has the same bias: never read unpaid state from a lagging "
                             "secondary."),
                          tp("The other four",
                             "Catalog browsing can use primaryPreferred or nearest with local "
                             "reads. Order status should read from the primary, or with "
                             "majority, right after a customer pays. Reporting and analytics can "
                             "use secondaryPreferred if minutes of delay are acceptable and the "
                             "secondary has capacity."),
                          tp("What to listen for",
                             "The three settings are not interchangeable, and staleness is "
                             "accepted explicitly, never by accident.")]),
        F.exercise("Exercise 7.3 — Evaluate Shard-Key Candidates",
                   "Module 7 checkpoint C: score keys for training_store.orders.",
                   kind="OFFICIAL CHECKPOINT C", minutes=20,
                   worksheet="labs/day-03/exercises/exercise-7.3-evaluate-shard-key-"
                             "candidates.md",
                   scenario="Score each candidate 1–5 on cardinality, distribution, write "
                            "scale, targeting, hotspot risk, locality and growth. tenantId is "
                            "a what-if: training_store has none.",
                   scenario_code="{ paymentStatus: 1 }\n"
                                 "{ createdAt: 1 }\n"
                                 "{ customerId: 1 }\n"
                                 "{ customerId: \"hashed\" }\n"
                                 "{ tenantId: 1, orderNumber: 1 }\n"
                                 "{ customerId: 1, createdAt: 1 }",
                   tasks=["Score all six candidates",
                          "Reject the low-cardinality key",
                          "Flag the monotonic key",
                          "Recommend one; name two risks"],
                   expected=["paymentStatus: rejected",
                             "createdAt: write hotspot",
                             "Hashed: even, no ranges",
                             "Pick customerId + createdAt",
                             "Risks: big customers, reports"],
                   expected_title="Solution (after debrief)",
                   takeaway="A defensible shard key matches the hot query — and still names the "
                            "risks you'll monitor.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 7.3. The worksheet is "
                             "labs/day-03/exercises/exercise-7.3-evaluate-shard-key-"
                             "candidates.md. Use training_store.orders as the mental model: "
                             "few statuses, many customers, dates that only increase."),
                          tp("Expected scores",
                             "paymentStatus has three values: low cardinality, a hotspot and "
                             "poor targeting. Ranged createdAt is a monotonic write hotspot. "
                             "customerId targets history but may suffer customer skew. Hashed "
                             "customerId gives even writes and weak range locality."),
                          tp("The compound keys",
                             "{ customerId: 1, createdAt: 1 } targets history queries, and "
                             "ranged writes per customer are usually fine. The tenantId key only "
                             "works if queries lead with the tenant; training_store has no "
                             "tenantId, so treat it as a what-if. Its second field is the real "
                             "orderNumber, such as O6401."),
                          tp("The recommendation",
                             "{ customerId: 1, createdAt: 1 } or hashed customerId, depending on "
                             "whether date ranges across customers matter. Risks to monitor: "
                             "very large customers and scatter-gather global reports.")]),
        F.exercise("Exercise 7.4 — Targeted or Scatter-Gather?",
                   "Module 7 checkpoint D: classify five queries by their routing.",
                   kind="OFFICIAL CHECKPOINT D", minutes=15,
                   worksheet="labs/day-03/exercises/exercise-7.4-targeted-or-scatter-"
                             "gather.md",
                   scenario="Shard key: { customerId: 1, createdAt: 1 }. c is customer C101.",
                   scenario_code="A { customerId: c._id }\n"
                                 "B { customerId: c._id,\n"
                                 "    createdAt: { $gte: start } }\n"
                                 "C { paymentStatus: \"PAID\" }\n"
                                 "D { createdAt: { $gte: start } }\n"
                                 "E D again, key hashed customerId",
                   tasks=["Classify queries A and B",
                          "Classify queries C and D",
                          "Classify E under the hashed key",
                          "Fix a slow monthly revenue report"],
                   expected=["A, B targeted: key prefix",
                             "C scatter-gather",
                             "D many shards or all",
                             "E scatter-gather",
                             "Pre-aggregate, don't re-key"],
                   expected_title="Solution (after debrief)",
                   takeaway="The leading shard-key field decides routing — reports without it "
                            "need a different design, not a new key.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 7.4. The worksheet is "
                             "labs/day-03/exercises/exercise-7.4-targeted-or-scatter-"
                             "gather.md. As on the slide, c holds C101's customer document, so "
                             "c._id is the ObjectId stored in orders.customerId."),
                          tp("A to E",
                             "A is targeted: one or a few chunks for that customer. B is a "
                             "targeted range inside the customer prefix. C is scatter-gather: "
                             "paymentStatus is not in the key. D usually touches many shards, "
                             "depending on how dates map. E, a createdAt range under a hashed "
                             "customerId key, is scatter-gather."),
                          tp("The redesign",
                             "If monthly global revenue must be fast, don't pick a shard key "
                             "that hurts the order path. Pre-aggregate the report, run it on an "
                             "analytics node, or accept scatter-gather for a rare job."),
                          tp("Link to Lab 6",
                             "Day 3 Lab 6, Step 3, repeats this with fulfillmentStatus and an "
                             "_id-only lookup, both scatter-gather.")]),
        F.exercise("Lab 6 — Replication and Sharding",
                   "Day 3 hands-on: choose the mechanism, reason about shard keys, check a "
                   "replica set.",
                   kind="OFFICIAL LAB", minutes=40,
                   worksheet="labs/day-03/lab6/LAB-6-GUIDE.md",
                   scenario="Steps 1–3 work on paper. Steps 4–7 need the instructor's "
                            "replica-set or Atlas URI; a standalone mongod is not a replica "
                            "set.",
                   scenario_code="use training_store\n"
                                 "rs.status()\n"
                                 "rs.conf()\n"
                                 "db.hello()\n"
                                 "rs.printSecondaryReplicationInfo()",
                   tasks=["1 Mechanism for six requirements",
                          "2–3 Shard keys and query routing",
                          "4 Confirm a replica set",
                          "5–6 Record members, votes and lag",
                          "7 Write a short health report"],
                   expected=["Last week's delete: a backup",
                             "fulfillmentStatus rejected",
                             "Status-only query scatters",
                             "One PRIMARY, health: 1",
                             "Lag measured, often 0–2 s"],
                   takeaway="Name the mechanism, defend the shard key, and report health as "
                            "measured — not assumed.",
                   notes=[tp("Official lab",
                             "This is Day 3 Lab 6, Replication and Sharding. The guide is "
                             "labs/day-03/lab6/LAB-6-GUIDE.md. Allow 30 to 40 minutes. Steps 1 "
                             "to 3 are reasoning on training_store.orders; Steps 4 to 7 inspect "
                             "a real replica set."),
                          tp("Steps 1 to 3",
                             "Step 1 repeats Exercise 7.1 and adds last week's deleted order: "
                             "the answer is a backup. Step 2 rejects fulfillmentStatus, flags "
                             "createdAt and prefers { customerId: 1, createdAt: 1 }. Step 3 "
                             "classifies customer history as targeted and the "
                             "fulfillmentStatus and _id-only lookups as scatter-gather. On a "
                             "fresh load 3 orders are PROCESSING: O6202, O6302 and O6401."),
                          tp("Environment",
                             "Atlas clusters are replica sets; a local standalone mongod is "
                             "not. If rs.status() says the server is not running with "
                             "--replSet, stop and switch to the instructor's URI. These "
                             "commands only read status, so they are safe on a shared cluster; "
                             "nobody steps anything down. " + DISPOSABLE),
                          tp("Steps 4 to 6: what to record",
                             "The set name, the primary host, the secondary hosts, each "
                             "member's votes and priority, any arbiter, what db.hello() says "
                             "about the connected member, and the lag of each secondary, even "
                             "when it is zero."),
                          tp("Step 7: the report",
                             "One short paragraph: is there a primary, is a majority reachable, "
                             "is the lag a concern, and is there any configuration smell, such "
                             "as an arbiter carrying durability or priority 0 on the only nearby "
                             "member.")]),
        F.wrapup("Module 7 Summary and What's Next",
                 "From one replica set to a sharded cluster.",
                 can=["Tell availability from scalability",
                      "Explain the primary, secondaries, oplog and elections",
                      "Choose read preference, read and write concern",
                      "Explain replication lag and rollback",
                      "Evaluate shard keys and query routing",
                      "Decide when to replicate, shard, or both"],
                 next_title="Next: Module 8 — Best Practices",
                 questions=["What will we actually run in production?",
                            "How do we secure, back up and restore it?",
                            "How do we monitor and troubleshoot it?"],
                 bring=("Bring along", "Your Lab 6 health report and answers, and your "
                                       "shard-key scores from Exercise 7.3."),
                 takeaway="Module 8 turns replication, sharding and backups into a production "
                          "checklist.",
                 notes=[tp("Recap",
                           "We separated availability from scale, looked inside a replica set, "
                           "chose read and write settings, saw lag and rollback, and designed a "
                           "sharded cluster with a shard key for training_store orders."),
                        tp("Next module",
                           "Module 8 consolidates the course: sustainable modeling, query and "
                           "index optimization, security, backup and recovery, monitoring, "
                           "troubleshooting and deployment readiness."),
                        tp("Day 3 labs",
                           "Day 3 Lab 6, Replication and Sharding, is this module's hands-on "
                           "lab: the reasoning steps plus the replica-set health check. "
                           + DISPOSABLE),
                        tp("Bring along",
                           "Keep the Lab 6 health report and answers and the Exercise 7.3 "
                           "scores. Module 8's production-readiness review builds on "
                           "them.")]),
    ]
