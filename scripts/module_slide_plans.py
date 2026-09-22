#!/usr/bin/env python3
"""Per-module SLIDE_PLAN and preserve/replace config for merge_rich_content.py.

Each module's plan is a hand-authored (but content-free) list of SlideSpec:
which chunks from the parsed rich-content source go on which new slide, what
heading to give it, and which existing diagram PNG (if any) to reuse. This is
the "light per-module judgement call" the merge pipeline needs -- parsing,
splicing, and rendering are all generic and unchanged between modules.

To add module 3 (etc.) later: dump its section/subsection/chunk structure
with

    python -c "import merge_rich_content as m; ..."

(see the chunk preview helper below), decide the preserve-vs-replace global
indices from `python -c "...print manifest headings..."`, write a
MODULE0N_PLAN function here, and add it to MODULE_CONFIGS.
"""
from __future__ import annotations

from merge_rich_content import ModuleConfig, SlideSpec, make_auto_plan

DIAG1 = "scripts/chatgpt_diagrams/diagrams/module01"
DIAG2 = "scripts/chatgpt_diagrams/diagrams/module02"


# ---------------------------------------------------------------------------
# Module 1 -- Introduction to NoSQL Databases
# ---------------------------------------------------------------------------
def module01_plan(sections):
    S = sections  # noqa: N806

    def part(sec_num, sub_title="", start=0, stop=None):
        return (sec_num, sub_title, (start, stop))

    return [
        SlideSpec(
            heading="Defining NoSQL",
            parts=[part("1", "", 0, 4)],
            diagram=f"{DIAG1}/007 - What Does NoSQL Mean-.png",
            notes="NoSQL means 'Not Only SQL': databases built for data models other than "
                  "relational tables, addressing changing structures, scale, and speed.",
        ),
        SlideSpec(
            heading="NoSQL in Practice: Flexible Product Records",
            parts=[part("1", "", 4, None)],
            notes="Two JSON examples (a laptop, a book) show how a document can carry only "
                  "the fields that product needs, instead of many optional relational columns.",
        ),
        SlideSpec(
            heading="Document Databases",
            parts=[part("2", "Document databases", 0, 4)],
            diagram=f"{DIAG1}/010 - Document Databases.png",
            notes="Document databases (MongoDB, Couchbase) store self-contained JSON-like "
                  "documents -- one order example shown.",
        ),
        SlideSpec(
            heading="Document Databases — Use Cases",
            parts=[part("2", "Document databases", 4, None)],
            notes="Document databases suit catalogues, profiles, CMS, and order management -- "
                  "an application object often maps to one document.",
        ),
        SlideSpec(
            heading="Key-Value Databases",
            parts=[part("2", "Key-value databases", 0, 4)],
            diagram=f"{DIAG1}/011 - Key-Value Databases.png",
            notes="Key-value stores (Redis, DynamoDB) map a unique key straight to a value for "
                  "very fast lookups.",
        ),
        SlideSpec(
            heading="Key-Value Databases — Use Cases",
            parts=[part("2", "Key-value databases", 4, None)],
            notes="Best for caching, sessions, carts, and counters -- fast by key, but weaker "
                  "for complex relationship queries.",
        ),
        SlideSpec(
            heading="Graph Databases",
            parts=[part("2", "Graph databases", 0, 5)],
            diagram=f"{DIAG1}/013 - Graph Databases.png",
            notes="Graph databases (Neo4j, Neptune) model nodes, edges, and properties -- "
                  "relationships are first-class data.",
        ),
        SlideSpec(
            heading="Graph Databases — Use Cases",
            parts=[part("2", "Graph databases", 5, None)],
            notes="Graph databases shine for social networks, recommendations, fraud "
                  "detection, and access relationships.",
        ),
        SlideSpec(
            heading="Comparing Document, Key-Value, and Graph Stores",
            parts=[part("2", "Comparison")],
            notes="Side-by-side comparison: data model, main strength, and typical use for "
                  "each of the three store types.",
        ),
        SlideSpec(
            heading="Introducing MongoDB",
            parts=[part("3", "", 0, None), part("3", "MongoDB data hierarchy", 0, 3)],
            diagram=f"{DIAG1}/017 - MongoDB Data Hierarchy.png",
            notes="MongoDB is a document-oriented database storing BSON; deployment -> "
                  "database -> collection -> document -> field.",
        ),
        SlideSpec(
            heading="Anatomy of a MongoDB Document",
            parts=[part("3", "MongoDB data hierarchy", 3, None)],
            diagram=f"{DIAG1}/021 - Anatomy of a MongoDB Document.png",
            notes="A full example document for a wireless mouse product, including nested "
                  "specifications and a tags array.",
        ),
        SlideSpec(
            heading="MongoDB Architecture Overview",
            parts=[part("3", "Major architectural components", 0, 5)],
            diagram=f"{DIAG1}/024 - MongoDB Architecture Overview.png",
            notes="Clients (drivers, mongosh, Compass) talk to the mongod server process, "
                  "which owns storage, queries, indexes, auth, and replication.",
        ),
        SlideSpec(
            heading="Replica Sets",
            parts=[part("3", "Major architectural components", 5, 9)],
            notes="A replica set keeps copies of the same data on multiple servers; the "
                  "primary takes writes and an eligible secondary can be elected if it fails.",
        ),
        SlideSpec(
            heading="Sharded Clusters",
            parts=[part("3", "Major architectural components", 9, None)],
            notes="Sharding spreads data across shards, config servers, and mongos routers so "
                  "one server doesn't have to hold the whole dataset.",
        ),
        SlideSpec(
            heading="Flexible Document Model",
            parts=[part("4", "Flexible document model")],
            diagram=f"{DIAG1}/022 - Flexible Schema Within a Collection.png",
            notes="Documents in the same collection don't need identical fields -- a physical "
                  "and a digital product example side by side.",
        ),
        SlideSpec(
            heading="Embedded Documents and Arrays",
            parts=[part("4", "Embedded documents and arrays")],
            diagram=f"{DIAG1}/023 - Embedding vs Referencing Preview.png",
            notes="An order document embeds its line items and shipping address, cutting the "
                  "joins needed to read one business object.",
        ),
        SlideSpec(
            heading="Rich Query Language",
            parts=[part("4", "Rich query language")],
            notes="MongoDB's query language covers filtering, sorting, projection, updates, "
                  "geospatial and text search, and aggregation.",
        ),
        SlideSpec(
            heading="Indexing",
            parts=[part("4", "Indexing")],
            notes="Indexes let MongoDB find documents without scanning the whole collection; "
                  "design them around real query patterns.",
        ),
        SlideSpec(
            heading="Aggregation Framework",
            parts=[part("4", "Aggregation framework")],
            notes="Aggregation pipelines chain stages like $match, $group, and $sort for "
                  "reporting and analytics.",
        ),
        SlideSpec(
            heading="Replication, Scaling, and Transactions",
            parts=[
                part("4", "Replication and high availability"),
                part("4", "Horizontal scalability"),
                part("4", "Transactions and validation"),
            ],
            notes="Replica sets give high availability, sharding gives horizontal scale, and "
                  "MongoDB still supports schema validation and multi-document transactions.",
        ),
        SlideSpec(
            heading="Practical Benefits",
            parts=[part("Practical Benefits", "")],
            diagram=f"{DIAG1}/028 - MongoDB Use Cases.png",
            notes="MongoDB's benefits add up to faster development and natural object mapping "
                  "-- design around how the application actually reads and writes data.",
        ),
    ]


MODULE01_CONFIG = ModuleConfig(
    front_preserve=[3, 4],
    end_preserve=list(range(34, 54)),
    plan_fn=module01_plan,
)


# ---------------------------------------------------------------------------
# Module 2 -- Installation and Setup
# ---------------------------------------------------------------------------
def module02_plan(sections):
    def part(sec_num, sub_title="", start=0, stop=None):
        return (sec_num, sub_title, (start, stop))

    return [
        SlideSpec(
            heading="Local Deployment",
            parts=[part("1", "", 0, None), part("1", "Local deployment")],
            diagram=f"{DIAG2}/006 - Local MongoDB Deployment.png",
            notes="MongoDB Community Edition installed directly on the learner's machine -- "
                  "best for classroom exercises and offline development.",
        ),
        SlideSpec(
            heading="Cloud Deployment (MongoDB Atlas)",
            parts=[part("1", "Cloud deployment", 0, 3)],
            diagram=f"{DIAG2}/007 - Managed Cloud Deployment.png",
            notes="Atlas is MongoDB's managed cloud platform -- good for team projects, "
                  "remote access, and production-style practice.",
        ),
        SlideSpec(
            heading="Local vs. MongoDB Atlas",
            parts=[part("1", "Cloud deployment", 3, None)],
            diagram=f"{DIAG2}/011 - Local vs. Managed Cloud.png",
            notes="Side-by-side factors: internet requirement, who manages infrastructure, "
                  "default address, and remote access.",
        ),
        SlideSpec(
            heading="Local MongoDB Components",
            parts=[part("2", "", 0, None)],
            diagram=f"{DIAG2}/014 - MongoDB Server and Client Tools.png",
            notes="A local environment usually has the Community Server, mongosh, optionally "
                  "Compass, and the optional Database Tools.",
        ),
        SlideSpec(
            heading="Windows Installation",
            parts=[part("2", "Windows installation", 0, 1)],
            diagram=f"{DIAG2}/013 - MongoDB Installation Workflow.png",
            notes="Download the MSI, choose Complete install, install as a Windows service, "
                  "then optionally add Compass and mongosh.",
        ),
        SlideSpec(
            heading="Verifying the MongoDB Service (Windows)",
            parts=[part("2", "Windows installation", 1, None)],
            diagram=f"{DIAG2}/022 - Verifying the MongoDB Service.png",
            notes="Check the service from Windows Services or PowerShell's Get-Service / "
                  "Start-Service MongoDB.",
        ),
        SlideSpec(
            heading="macOS Installation with Homebrew",
            parts=[part("2", "macOS installation with Homebrew")],
            notes="brew tap and install the Community Edition formula, then start it as a "
                  "Homebrew service and verify with --version.",
        ),
        SlideSpec(
            heading="Linux Installation",
            parts=[part("2", "Linux installation")],
            notes="Use MongoDB's own repository for the distribution, then manage the service "
                  "with systemctl start / status / enable.",
        ),
        SlideSpec(
            heading="`mongod` vs. `mongosh`",
            parts=[part("2", "Important local components", 0, 2)],
            diagram=f"{DIAG2}/015 - mongod vs. mongosh.png",
            notes="mongod is the server that owns the data files; mongosh is just the client "
                  "shell -- stopping the shell never stops the database.",
        ),
        SlideSpec(
            heading="Default Host and Port",
            parts=[part("2", "Important local components", 2, None)],
            diagram=f"{DIAG2}/023 - Hosts and Ports.png",
            notes="A local server commonly listens on localhost, port 27017, by default.",
        ),
        SlideSpec(
            heading="Atlas Provisioning Process",
            parts=[part("3", "", 0, None), part("3", "Basic provisioning process")],
            diagram=f"{DIAG2}/008 - Cloud Provisioning Process.png",
            notes="Nine-step Atlas flow: account, org, project, deployment, tier, provider, "
                  "database user, IP access list, connection string.",
        ),
        SlideSpec(
            heading="Atlas User vs. Database User",
            parts=[part("3", "Database user versus Atlas user")],
            notes="The Atlas login and the database user that authenticates the connection "
                  "are two separate identities.",
        ),
        SlideSpec(
            heading="Atlas Network Access",
            parts=[part("3", "Network access")],
            notes="Atlas blocks unapproved network sources; 0.0.0.0/0 is convenient for a "
                  "classroom but broad, and should pair with strong credentials.",
        ),
        SlideSpec(
            heading="Atlas Connection String",
            parts=[part("3", "Atlas connection string")],
            diagram=f"{DIAG2}/027 - DNS Seed-List Connection Strings.png",
            notes="An Atlas URI follows mongodb+srv://<user>:<password>@<cluster-host>/ -- let "
                  "mongosh prompt for the password instead of typing it inline.",
        ),
        SlideSpec(
            heading="The MongoDB Shell (mongosh)",
            parts=[part("4", "", 0, None)],
            diagram=f"{DIAG2}/029 - Connecting with mongosh.png",
            notes="mongosh is the interactive shell for creating databases and collections, "
                  "running queries, indexes, and aggregations.",
        ),
        SlideSpec(
            heading="Connecting to Local MongoDB",
            parts=[
                part("4", "Connecting to local MongoDB"),
                part("4", "Connecting with authentication"),
            ],
            notes="Plain mongosh connects to localhost:27017 by default; adding --username "
                  "prompts for the matching password.",
        ),
        SlideSpec(
            heading="Connecting to Atlas",
            parts=[part("4", "Connecting to Atlas")],
            diagram=f"{DIAG2}/028 - Connection Establishment.png",
            notes="Copy the exact connect command from the Atlas Connect dialog -- the "
                  "cluster hostname is deployment-specific.",
        ),
        SlideSpec(
            heading="Verifying Your Connection",
            parts=[
                part("5", "", 0, None),
                part("5", "Check the shell version"),
                part("5", "Check the server version"),
            ],
            notes="The shell prompt shows the current database; mongosh --version and "
                  "db.version() confirm client and server versions.",
        ),
        SlideSpec(
            heading="Checking the Current Database and Connection",
            parts=[
                part("5", "Check the current database"),
                part("5", "Check the connection"),
            ],
            notes="`db` shows the active database (test, initially); db.getMongo() reports "
                  "the current connection.",
        ),
        SlideSpec(
            heading="Exploring Databases and Collections",
            parts=[
                part("5", "Display databases"),
                part("5", "Display available collections"),
            ],
            diagram=f"{DIAG2}/031 - Databases and Collections.png",
            notes="show dbs and show collections only list databases/collections that "
                  "already hold stored data.",
        ),
        SlideSpec(
            heading="Creating Your First Database",
            parts=[part("6", "", 0, None), part("6", "Select a database")],
            diagram=f"{DIAG2}/032 - Creating Your First Database.png",
            notes="`use training_store` switches context without creating anything physical "
                  "until data is written.",
        ),
        SlideSpec(
            heading="Creating Your First Collection",
            parts=[part("6", "Create the first collection")],
            diagram=f"{DIAG2}/033 - Creating Your First Collection.png",
            notes="db.createCollection() creates one explicitly; MongoDB can also create a "
                  "collection automatically on first insert.",
        ),
        SlideSpec(
            heading="Inserting Your First Document",
            parts=[part("6", "Insert the first document")],
            diagram=f"{DIAG2}/034 - Inserting Your First Document.png",
            notes="insertOne() adds a product document; MongoDB generates an _id "
                  "automatically when one isn't supplied.",
        ),
        SlideSpec(
            heading="Retrieving Documents",
            parts=[part("6", "Retrieve the document")],
            diagram=f"{DIAG2}/036 - Retrieving and Verifying Data.png",
            notes="find() returns everything in the collection; a filter narrows it to a "
                  "specific category.",
        ),
        SlideSpec(
            heading="Inserting Multiple Documents and Counting",
            parts=[part("6", "Insert multiple documents"), part("6", "Count documents")],
            notes="insertMany() adds several products at once; countDocuments() confirms the "
                  "total in the collection.",
        ),
        SlideSpec(
            heading="Verifying the Database and Collection",
            parts=[part("6", "Verify the database and collection")],
            notes="show dbs / show collections now surface training_store and products, "
                  "holding the three inserted documents.",
        ),
        SlideSpec(
            heading="Updating a Document",
            parts=[part("7", "Update a document")],
            notes="updateOne() with $set changes one field; findOne() verifies the change "
                  "took effect.",
        ),
        SlideSpec(
            heading="Deleting a Document",
            parts=[part("7", "Delete a document", 0, 3)],
            notes="deleteOne() removes a document by filter; countDocuments() confirms the "
                  "remaining count.",
        ),
        SlideSpec(
            heading="CRUD Operations Summary",
            parts=[part("7", "Delete a document", 3, None)],
            notes="The four CRUD verbs map directly to insertOne, find/findOne, updateOne, "
                  "and deleteOne.",
        ),
        SlideSpec(
            heading="Local Connection Problems",
            parts=[
                part("8", "`mongosh: command not found`"),
                part("8", "Connection refused on `localhost:27017`"),
            ],
            diagram=f"{DIAG2}/042 - Common Connection Problems.png",
            notes="'command not found' usually means PATH or a fresh terminal; 'connection "
                  "refused' usually means mongod isn't running or is on another port.",
        ),
        SlideSpec(
            heading="Atlas Connection Problems",
            parts=[
                part("8", "Atlas authentication failed"),
                part("8", "Atlas connection timeout"),
            ],
            notes="Authentication failures point to the database user/password/auth DB; "
                  "timeouts point to the IP access list or a blocking firewall.",
        ),
        SlideSpec(
            heading="Practical Lab",
            parts=[part("Practical Lab", "")],
            diagram=f"{DIAG2}/044 - Environment Readiness Checklist.png",
            notes="By the end of the module, learners install or provision MongoDB, connect, "
                  "run CRUD, and confirm the environment with a successful ping.",
        ),
    ]


MODULE02_CONFIG = ModuleConfig(
    front_preserve=[54, 55],
    end_preserve=[
        66, 67, 68, 79, 86, 87, 88, 90, 92, 99, 107, 108, 109, 110, 112, 113, 114, 115,
        116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131,
    ],
    plan_fn=module02_plan,
)


# ---------------------------------------------------------------------------
# Modules 3-7 -- built with the generic auto-planner (make_auto_plan) rather
# than hand-authored SlideSpecs: these sources have far more sections (19-37)
# and, for modules 4/5 especially, dozens of small code examples per section,
# so packing chunks into slides by a weight budget (see merge_rich_content.
# pack_chunks) does the "consolidate related short snippets, split dense
# subsections" judgement call generically. front_preserve/end_preserve below
# were derived by classifying each existing manifest slide's heading against
# the Exercise/Demo/Lab/Knowledge-Check/Summary/etc. naming conventions
# (everything else is a concept slide that gets replaced).
# ---------------------------------------------------------------------------
MODULE03_CONFIG = ModuleConfig(
    front_preserve=[132, 133],
    end_preserve=[
        147, 148, 149, 163, 164, 165, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209,
        238, 239, 241, 242, 243, 244, 245, 246, 257, 258, 262, 263, 264, 265, 266, 267,
        268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283,
        284, 285, 286,
    ],
    plan_fn=make_auto_plan(3, diagram_threshold=0.60),
)

MODULE04_CONFIG = ModuleConfig(
    front_preserve=[287, 288],
    end_preserve=[
        298, 299, 300, 301, 302, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320,
        321, 322, 323, 324, 325, 330, 331, 332, 333, 334, 335, 336, 337, 338, 344, 345,
        346, 347, 348, 349, 350, 351, 352, 355, 356, 357, 358, 359, 363, 364, 365, 366,
        367, 371, 372, 373, 374, 375, 378, 379, 380, 381, 384, 385, 386, 387, 390, 396,
        397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412,
        413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428,
        429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444,
        445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460,
        461, 462, 463, 464,
    ],
    plan_fn=make_auto_plan(4),
)

MODULE05_CONFIG = ModuleConfig(
    front_preserve=[465, 466],
    end_preserve=[
        477, 478, 479, 480, 481, 482, 511, 512, 513, 514, 515, 516, 517, 518, 528, 529,
        530, 531, 532, 533, 534, 535, 536, 547, 548, 549, 550, 551, 552, 553, 564, 565,
        566, 567, 568, 569, 570, 571, 572, 573, 582, 583, 584, 585, 598, 599, 600, 601,
        602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614,
    ],
    plan_fn=make_auto_plan(5),
)

MODULE06_CONFIG = ModuleConfig(
    front_preserve=[615, 616],
    end_preserve=[
        631, 632, 633, 641, 642, 643, 644, 645, 646, 647, 648, 649, 650, 651, 652, 655,
        657, 661, 663, 668, 669, 672, 686, 687, 688, 689, 690, 693, 694, 705, 706, 707,
        708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722, 723,
        724, 725, 726, 727, 728, 729, 730, 731, 732, 733, 734, 735, 736, 737, 738, 739,
        740, 741, 742, 743, 744, 745, 746, 747, 748, 749, 750, 751, 752, 753, 754, 755,
        756,
    ],
    plan_fn=make_auto_plan(6),
)

MODULE07_CONFIG = ModuleConfig(
    front_preserve=[757, 758, 759],
    end_preserve=[
        766, 767, 774, 775, 776, 777, 787, 788, 789, 790, 791, 799, 800, 801, 802, 809,
        810, 811, 812, 813, 814, 815, 816, 817, 818, 819, 820, 821, 822, 823, 824, 825,
        826, 834, 835, 836, 848, 849, 850, 851, 852, 853, 854, 862, 863, 864, 865, 874,
        875, 876, 877, 878, 879, 880, 881, 882, 883, 884, 885, 891, 892, 893, 894, 895,
        896, 897, 898, 899, 900, 901, 902, 903, 904,
    ],
    plan_fn=make_auto_plan(7),
)


MODULE08_CONFIG = ModuleConfig(
    front_preserve=[905, 906],
    end_preserve=[
        919, 920, 921, 922, 923, 929, 930, 931, 937, 938, 939, 945, 946, 958, 959, 960,
        961, 962, 963, 964, 972, 973, 974, 981, 982, 983, 984, 985, 986, 993, 994, 995,
        996, 1003, 1004, 1005, 1006, 1008, 1009, 1010, 1011, 1012, 1013, 1014, 1015,
        1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026, 1027, 1028,
        1029, 1030, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041,
        1042, 1043, 1044, 1045, 1046, 1047, 1048, 1049, 1050, 1051, 1052,
    ],
    plan_fn=make_auto_plan(8),
)


MODULE_CONFIGS = {
    1: MODULE01_CONFIG,
    2: MODULE02_CONFIG,
    3: MODULE03_CONFIG,
    4: MODULE04_CONFIG,
    5: MODULE05_CONFIG,
    6: MODULE06_CONFIG,
    7: MODULE07_CONFIG,
    8: MODULE08_CONFIG,
}
