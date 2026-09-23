#!/usr/bin/env python3
"""Speaker notes for the new Module 7 deck (Introduction to Replication and Sharding).

Written from scripts/module07_content_source.md, the Module 7 manifest, the
official Exercises 7.1 to 7.4 in labs/day-03/exercises/, the Day 3 Lab 6 guide
(labs/day-03/lab6/LAB-6-GUIDE.md) and the training_store dataset, in plain short sentences. Composed into the notes
pane by mdb_speaker_notes.compose(), so the layout matches the day decks:
KEY TALKING POINTS / REAL-WORLD EXAMPLES / USE-CASE SCENARIO.

Keys are topic numbers. Diagram topics (see build_module07_new.DIAGRAMS) are
merged with the diagram's own "what it shows" notes on the same slide.
"""
from __future__ import annotations


def tp(point: str, explain: str) -> dict:
    return {"point": point, "explain": explain}


NOTES: dict[int, dict] = {
    1: {
        "talking_points": [
            tp("Two mechanisms, two problems",
               "MongoDB uses two mechanisms for demanding production workloads. "
               "Replication keeps several copies of the same data so the database stays "
               "available when a server fails. "
               "Sharding splits a collection across several servers so it can grow past one "
               "machine."),
            tp("What this module does",
               "We start by separating availability from scalability. "
               "Then we look inside a replica set: the primary, the secondaries, the oplog, "
               "elections and failover. "
               "Next come the read and write settings and what replication lag and rollback "
               "mean. "
               "Finally we build a sharded cluster, choose a shard key for training_store "
               "orders and see how queries are routed."),
            tp("Where this sits in the course",
               "This is the second module of Day 3. "
               "Module 6 made single queries fast with indexes. "
               "Module 7 keeps the whole database online and ready to grow, and Module 8 "
               "turns all of it into production practice."),
            tp("Lab safety",
               "Failover and sharding commands run only on instructor-controlled, disposable "
               "infrastructure. "
               "Say this now and repeat it whenever such a command appears."),
        ],
        "real_world_examples": [
            "An online store runs its database as a three-member replica set, so a failed "
            "server causes a pause of seconds, not an outage. "
            "Years later, when order volume outgrows one replica set, it shards the orders "
            "collection.",
        ],
    },
    2: {
        "talking_points": [
            tp("By the end of this module",
               "Walk through the six objectives on the left. "
               "Learners should be able to tell availability from scalability, and explain "
               "the roles in a replica set, the oplog and failover. "
               "They should be able to choose basic read and write settings and describe the "
               "parts of a sharded cluster. "
               "They should also be able to evaluate a shard key and its query routing, and "
               "decide when to replicate, shard, or both."),
            tp("Six questions this module answers",
               "Why do we need both copies and pieces? "
               "How does a replica set survive a failure? "
               "Which member serves a read, and when is a write safe? "
               "What makes up a sharded cluster? "
               "How do we choose a shard key? "
               "And when should we replicate, shard, or both?"),
            tp("The roadmap",
               "The five parts at the bottom follow that order. "
               "Official Exercises 7.1 to 7.4 come at the end, followed by the module's "
               "lab, Day 3 Lab 6."),
        ],
    },
    7: {
        "talking_points": [
            tp("How to read the table",
               "Each row is one requirement. "
               "The two columns say whether replication or sharding delivers it."),
            tp("The important distinction",
               "Replication does not divide the data. "
               "Every data-bearing member of a replica set holds a copy of the whole data set. "
               "Sharding divides a collection's documents, so each shard stores only its own "
               "part."),
            tp("Failover in a sharded cluster",
               "Sharding on its own gives no failover. "
               "It gets failover because each shard is itself a replica set."),
            tp("The last row",
               "Neither mechanism restores data that was deleted last week. "
               "A deleteMany on the primary is replicated to every secondary within seconds. "
               "Only a backup gives an independent recovery point. "
               "Module 8 covers backup and restore."),
        ],
    },
    5: {
        "talking_points": [
            tp("Start from the requirement",
               "Don't start from a technology. "
               "Start from what the business needs: stay online, or handle growth."),
            tp("Stay online",
               "Staying online needs a replica set. "
               "Several mongod servers keep the same data, and when a node fails, another "
               "member takes over automatically. "
               "The result is high availability."),
            tp("Handle growth",
               "Handling growth needs a sharded cluster. "
               "mongos spreads the data and the load across shards. "
               "The result is horizontal scalability."),
        ],
    },
    6: {
        "talking_points": [
            tp("Vertical scaling",
               "Vertical scaling means a bigger server: more CPU, more memory, faster and "
               "larger storage. "
               "It is simple and needs no data distribution. "
               "But a server has a maximum size, large hardware is expensive, and maintenance "
               "affects the whole workload. "
               "On its own, a bigger server also gives no high availability."),
            tp("Horizontal scaling",
               "Horizontal scaling adds servers and spreads the work. "
               "In MongoDB that is sharding: each shard holds part of the data, and each "
               "shard's CPU, memory and disk carry part of the load."),
            tp("Why growth happens",
               "More users, larger data, more writes, more queries, larger indexes, analytics "
               "and new regions all add load."),
            tp("Advice",
               "MongoDB recommends starting unsharded while the data and workload fit "
               "comfortably on one replica set. "
               "Tune the schema and indexes from Modules 3 and 6 first."),
        ],
    },
    10: {
        "talking_points": [
            tp("What a replica set is",
               "A replica set is a group of mongod processes that maintain the same data set. "
               "The common configuration is three data-bearing members."),
            tp("Primary and secondaries",
               "The primary receives every write. "
               "It applies the write, records it in its oplog and makes it available to the "
               "secondaries. "
               "Secondaries copy those operations and apply them locally, so each one keeps a "
               "full copy of training_store."),
            tp("One writable primary",
               "A replica set normally has one writable primary at a time. "
               "Applications can't write to a secondary. "
               "They can read from one only when a read preference allows it."),
            tp("Heartbeats",
               "Members send each other heartbeats, every two seconds by default. "
               "If the primary goes quiet for long enough, the eligible secondaries hold an "
               "election."),
        ],
    },
    13: {
        "talking_points": [
            tp("What the oplog is",
               "The operation log, or oplog, is a special capped collection, local.oplog.rs. "
               "It records every data-changing operation: inserts, updates, deletes and "
               "certain administrative changes."),
            tp("The flow",
               "A write reaches the primary. "
               "The primary applies it and records it in the oplog. "
               "Secondaries copy the new entries and apply them locally, in order."),
            tp("Asynchronous",
               "Replication is asynchronous. "
               "A secondary may lag behind the primary for a moment, and sometimes for longer."),
            tp("The replication window",
               "The oplog has a fixed size. When it is full, the oldest entries are "
               "overwritten. "
               "The time span it still holds is the replication window. "
               "A member offline for longer than the window can't catch up incrementally and "
               "needs a full resynchronization."),
        ],
    },
    16: {
        "talking_points": [
            tp("When an election happens",
               "If the primary becomes unreachable, the eligible voting members hold an "
               "election."),
            tp("Majority",
               "A candidate must win votes from a majority of voting members. "
               "Three voters need two votes, so the set survives the loss of one voter. "
               "Five voters need three, so the set survives the loss of two."),
            tp("Why odd numbers",
               "Four voters need three votes, so they tolerate only one failure, the same as "
               "three voters. "
               "A fourth voter adds cost but no extra failure tolerance. "
               "That is why odd numbers are common."),
            tp("Who wins",
               "Priority and how up to date a member is both matter. "
               "A member whose oplog is behind the others won't be elected ahead of a more "
               "current one."),
        ],
    },
    17: {
        "talking_points": [
            tp("The six steps",
               "The members detect the failure. "
               "An eligible secondary asks for an election. "
               "A majority selects the new primary, and that member becomes primary. "
               "Drivers discover the change. "
               "Application operations resume after reconnection and server selection."),
            tp("A short write pause",
               "There is normally a short period, often seconds, when writes can't complete "
               "because there is no primary. "
               "By default a member waits about ten seconds without heartbeats before it calls "
               "an election."),
            tp("The old primary",
               "When the old primary comes back, it rejoins as a secondary. "
               "It does not reclaim the primary role just because it was primary before."),
            tp("Lab safety",
               "The instructor can show this with rs.stepDown() on an instructor-controlled "
               "disposable replica set. "
               "Never step down a shared class cluster."),
        ],
    },
    18: {
        "talking_points": [
            tp("Give the driver the whole set",
               "Applications should get several hosts or an SRV connection string, plus the "
               "replica set name. "
               "The driver then discovers which member is primary and notices when that "
               "changes."),
            tp("What the application sees",
               "During the election a write fails with a transient error. "
               "The driver refreshes the topology, reconnects to the new primary and can "
               "retry an eligible write once."),
            tp("Design for it",
               "Applications should still handle timeouts, retryable write failures, the risk "
               "of duplicate requests and transaction retries. "
               "Idempotent operations make a retry safe."),
            tp("The anti-pattern",
               "Connecting to one host without replica-set discovery weakens failover. "
               "Nobody should have to restart the application by hand after an election."),
        ],
    },
    34: {
        "talking_points": [
            tp("rs.status()",
               "Connected to a replica-set member, rs.status() shows the set name, the current "
               "primary, the secondaries, each member's health and state, replication progress "
               "and election information."),
            tp("rs.conf() and db.hello()",
               "rs.conf() shows the configuration, including votes and priority. "
               "db.hello() says whether the connected server is writable: setName, "
               "isWritablePrimary and secondary."),
            tp("Lag",
               "rs.printSecondaryReplicationInfo() shows how far behind each secondary is. "
               "In a quiet training set it is usually zero to two seconds."),
            tp("Where to run it",
               "Atlas clusters, including the free tier, are replica sets. "
               "A local standalone mongod is not: rs.status() reports that it is not running "
               "with --replSet. "
               "Switch to the instructor's replica-set URI for Lab 6, Steps 4 to 7."),
        ],
    },
    24: {
        "talking_points": [
            tp("What read preference decides",
               "Read preference decides which members may serve a read."),
            tp("The five modes",
               "primary, the default, reads only from the primary. "
               "primaryPreferred uses the primary and falls back to a secondary. "
               "secondary reads only from eligible secondaries. "
               "secondaryPreferred prefers a secondary and falls back to the primary. "
               "nearest picks among eligible members partly by network latency."),
            tp("Why primary is the default",
               "Reading from the primary gives the simplest read-after-write behavior. "
               "An application sees its own write straight away."),
            tp("The secondary-read trade-off",
               "Secondary reads can move load off the primary, serve distant users and help "
               "reporting. "
               "But they may return data that is behind the primary, and they compete with "
               "replication for the secondary's resources. "
               "They are a conscious decision, not free scaling."),
        ],
    },
    28: {
        "talking_points": [
            tp("What write concern controls",
               "Write concern controls how much acknowledgment the application asks for "
               "before a write counts as done."),
            tp("The levels",
               "w: 0 asks for no acknowledgment at all. "
               "w: 1 means the primary accepted the write. "
               "w: majority means a majority of data-bearing voting members have it. "
               "Adding j: true also waits for the write to reach the on-disk journal."),
            tp("The trade-off",
               "Stronger acknowledgment gives better durability but can add latency. "
               "Since MongoDB 5.0 the default for most replica sets is majority."),
            tp("Match it to the operation",
               "A shopping-cart preference, a completed payment, an inventory deduction, an "
               "audit record and a temporary analytics event can each deserve a different "
               "setting."),
        ],
    },
    29: {
        "talking_points": [
            tp("What read concern controls",
               "Read concern controls the consistency and isolation of the data a read "
               "returns."),
            tp("The levels",
               "local, the default, returns the member's newest data, which could later be "
               "rolled back. "
               "available is similar and matters mainly on sharded clusters. "
               "majority returns only data a majority has acknowledged. "
               "linearizable gives the strongest single-document guarantee, and snapshot is "
               "used by transactions."),
            tp("Two different questions",
               "Read preference answers: which member may serve the read? "
               "Read concern answers: what visibility or consistency guarantee should the "
               "read have? "
               "Learners often mix them up, so ask them to say both questions aloud."),
        ],
    },
    31: {
        "talking_points": [
            tp("What lag is",
               "Replication lag is how far a secondary's applied oplog trails the primary. "
               "A little lag is normal. Growing lag is a warning."),
            tp("Why it matters",
               "A read from a lagging secondary returns stale data. "
               "Lag also stretches a failover, because an up-to-date member must be elected, "
               "and a member that falls outside the oplog window needs a full resync."),
            tp("Common causes",
               "Slow or saturated disks, heavy reporting on the secondary, network congestion, "
               "write bursts faster than the secondary can apply, long operations and a small "
               "oplog window."),
            tp("First checks",
               "Run rs.printSecondaryReplicationInfo() and compare member optimes in "
               "rs.status(). "
               "Then look at the secondary's CPU, disk and current operations before you think "
               "about rebuilding anything."),
        ],
    },
    33: {
        "talking_points": [
            tp("How a rollback starts",
               "The primary accepts a write with w: 1 and acknowledges it. "
               "Before any secondary copies it, the primary is cut off by a network partition."),
            tp("The majority moves on",
               "The other two members still form a majority. "
               "They elect a new primary that never saw that write."),
            tp("The rollback",
               "When the old primary rejoins, its history no longer matches the majority. "
               "It rolls back the unreplicated write, saves it to a rollback file for an "
               "operator to review, and syncs from the new primary."),
            tp("Prevention",
               "A write acknowledged with w: majority has reached a majority, so it is not "
               "rolled back. "
               "Reads with read concern majority never return data that could be rolled "
               "back."),
        ],
    },
    39: {
        "talking_points": [
            tp("Three components",
               "A sharded cluster has shards, config servers and mongos query routers."),
            tp("mongos",
               "Applications connect to mongos, not directly to shards. "
               "mongos reads the cluster metadata, finds the shard or shards that hold the "
               "data, sends the operation there, combines results and returns them. "
               "It does not store the application data itself. "
               "Production clusters usually run several mongos processes."),
            tp("Config servers",
               "The config servers store the metadata: sharded collections, shard membership, "
               "shard-key ranges and data distribution. "
               "They run as their own replica set, because the cluster can't route without "
               "them."),
            tp("Shards",
               "Each shard stores part of the sharded data. "
               "In production each shard is a replica set, so replication gives availability "
               "inside every shard."),
        ],
    },
    40: {
        "talking_points": [
            tp("A shard holds part of the data",
               "Each shard stores only its assigned part of a sharded collection. "
               "Here the orders collection is divided by customerId ranges."),
            tp("A shard is a replica set",
               "Each shard has a primary and two secondaries, with its own elections and "
               "failover. "
               "If a shard were a single unreplicated server, it would be a single point of "
               "failure for its data."),
            tp("Sharding plus replication",
               "Sharding distributes the data between shards. "
               "Replication provides availability within each shard. "
               "A production cluster needs both."),
        ],
    },
    46: {
        "talking_points": [
            tp("What makes a good shard key",
               "A strong key has high cardinality and even value frequency, does not grow in "
               "one direction, matches the common queries, spreads the writes, and keeps "
               "working as the data grows."),
            tp("Cardinality",
               "Cardinality is the number of distinct key values. "
               "A status field has only a few, and all documents with the same value must sit "
               "in the same range, so a very large collection can't be divided."),
            tp("Frequency",
               "Frequency is how often each value occurs. "
               "Even with many customers, one customer with fifty million orders makes one "
               "oversized, heavily used range."),
            tp("In training_store",
               "fulfillmentStatus has four values: NEW, PROCESSING, SHIPPED and DELIVERED. "
               "paymentStatus has three: PAID, PENDING and FAILED. "
               "Neither can be a shard key on its own. "
               "customerId, a reference to one of many customers, has high cardinality."),
        ],
    },
    48: {
        "talking_points": [
            tp("Monotonic values",
               "A monotonically increasing value keeps growing: timestamps, sequential order "
               "numbers, auto-incrementing identifiers. "
               "ObjectId values also start with a timestamp, so they grow over time too."),
            tp("The hotspot",
               "With ranged sharding, every new value is the largest so far. "
               "All new inserts land in the top range, on one shard, while the others sit "
               "idle for writes."),
            tp("The fixes",
               "A hashed key spreads such values evenly but loses efficient range targeting. "
               "A compound key that leads with a high-cardinality field, such as customerId, "
               "spreads writes across customers."),
            tp("Decide from the workload",
               "It depends on whether the workload needs even write distribution, efficient "
               "range reads, customer locality or time locality."),
        ],
    },
    50: {
        "talking_points": [
            tp("Ranged sharding",
               "Ranged sharding orders the shard-key values and cuts them into contiguous "
               "ranges. "
               "Each range lives on one shard."),
            tp("Benefits",
               "Range queries are efficient, related key values stay near each other, and a "
               "query for one customer or one time range can target the relevant shards."),
            tp("Risk",
               "If new values always increase, new writes concentrate in the last range. "
               "That is the monotonic hotspot from the previous slide."),
        ],
    },
    51: {
        "talking_points": [
            tp("Hashed sharding",
               "Hashed sharding computes a hash of the shard-key value and distributes ranges "
               "of hash values across the shards."),
            tp("Benefits",
               "It usually gives a more even distribution, spreads monotonically increasing "
               "identifiers and reduces write concentration."),
            tp("Trade-off",
               "The hash is not ordered like the original value. "
               "An equality query on customerId can still be targeted, because mongos can hash "
               "the value. "
               "But a range query on the original values may have to contact every shard."),
        ],
    },
    52: {
        "talking_points": [
            tp("What zones do",
               "Zoned sharding ties ranges of the shard key to chosen shards. "
               "Here Canadian orders stay on Shard A, US orders on Shard B and EU orders on "
               "Shard C."),
            tp("Why teams use zones",
               "The main reasons are data residency rules and keeping data close to the users "
               "who read it."),
            tp("What it needs",
               "The zone field must be part of the shard key, normally its first field, for "
               "example shippingRegion followed by customerId. "
               "training_store has no shippingRegion field today; its orders store "
               "shippingAddress.country as Canada or USA. "
               "You would add a region field before zoning on it."),
            tp("The catch",
               "Zones are not a free locality win. "
               "If 90 percent of users are in one region, that zone's shards take 90 percent "
               "of the load. "
               "For residency, also compare zones with separate regional clusters."),
        ],
    },
    55: {
        "talking_points": [
            tp("Chunks",
               "MongoDB divides the shard-key space into non-overlapping ranges, usually called "
               "chunks. "
               "Each range belongs to exactly one shard."),
            tp("Ranges, not documents",
               "MongoDB moves whole ranges between shards, not individual documents. "
               "Here Shard A owns chunks 1 and 4, Shard B chunks 2 and 5, and Shard C chunks 3 "
               "and 6."),
            tp("Metadata",
               "The config servers record which shard owns each range. "
               "That map is what mongos uses to route."),
            tp("Training data",
               "A tiny training data set may sit in one range on one shard. "
               "That is expected, not a fault."),
        ],
    },
    57: {
        "talking_points": [
            tp("The balancer",
               "The balancer is a background process that watches the distribution. "
               "When one shard holds far more than the others, it moves ranges to even them "
               "out."),
            tp("Reading the diagram",
               "Before: Shard A has four chunks, B and C one each. "
               "The balancer migrates C3 to Shard B and C4 to Shard C, so each shard ends with "
               "two."),
            tp("Migrations cost resources",
               "A migration copies the range, catches up on recent writes, commits the new "
               "owner in the metadata and deletes the old copy. "
               "That uses network, disk and CPU, so production teams monitor migrations and "
               "can schedule a balancing window."),
            tp("Modern versions",
               "Since MongoDB 6.0 the balancer compares the amount of data on each shard, not "
               "just the number of chunks. "
               "The diagram counts chunks to keep the idea simple."),
        ],
    },
    49: {
        "talking_points": [
            tp("Targeted query",
               "A query that includes the shard key, or its leading field, can be routed to "
               "one shard or a small set of shards."),
            tp("How mongos decides",
               "mongos looks up the value in the chunk map from the config servers. "
               "Here that value lives on Shard B, so only Shard B does the work."),
            tp("Why it matters",
               "MongoDB notes that the fastest sharded queries are generally routed to a "
               "single shard using shard-key information. "
               "Shards A and C stay free for other work."),
        ],
    },
    70: {
        "talking_points": [
            tp("The production picture",
               "Applications talk to mongos routers, usually more than one. "
               "The routers read metadata from the config server replica set. "
               "The data lives on three shards, and every shard is a three-member replica set."),
            tp("What is sharded and what is not",
               "Only the orders collection is sharded here. "
               "Its ranges are spread over all three shards. "
               "products, customers and reviews stay unsharded, and unsharded collections live "
               "on one shard, the database's primary shard. "
               "They are not copied to every shard."),
            tp("A server fails in Shard B",
               "The Shard B replica set elects another primary. "
               "Shards A and C keep working, and mongos updates its routing as the topology "
               "changes. "
               "The application keeps using the cluster, apart from the short failover pause "
               "for Shard B's ranges."),
            tp("Why draw it ourselves",
               "Some generated diagrams show every collection on every shard, or each shard as "
               "one mongod. "
               "Both are wrong for production, so this slide draws the architecture "
               "correctly."),
        ],
    },
    71: {
        "talking_points": [
            tp("Walk the questions",
               "Does the workload need high availability? If not, as in development and "
               "learning, a standalone mongod is enough. "
               "If it does, does the data fit one replica set? Then a replica set is the "
               "answer."),
            tp("When one replica set is not enough",
               "If it doesn't fit, either scale the replica set's servers up, or shard. "
               "The scale-vertically box still means a replica set, just on bigger servers."),
            tp("Shard with evidence",
               "Shard when measurements show that one replica set can't hold the data or the "
               "writes. "
               "Fix the schema and the indexes first; sharding a badly indexed collection "
               "spreads the problem."),
            tp("Which collection",
               "In training_store, orders grows fastest, so it is the first shard candidate. "
               "products and customers usually stay unsharded for a long time."),
        ],
    },
}
