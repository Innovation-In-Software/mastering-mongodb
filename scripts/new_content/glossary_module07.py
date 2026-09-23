"""Key terms and abbreviations for the Module 7 deck (Introduction to Replication and Sharding).

Read by mdb_glossary.intro("module07"), which builds the Key Terms and Full Forms
slides that follow Learning Objectives.
"""
from __future__ import annotations

TERMS = [
    ("Replica set", "A group of mongod servers holding the same data: one primary and its "
                    "secondaries."),
    ("Oplog", "The operation log: a capped collection of every change, which secondaries copy "
              "and apply."),
    ("Election and failover", "When the primary is lost, a majority of voters elects a "
                              "secondary as the new primary."),
    ("Write concern", "How many members must confirm a write before the application gets an "
                      "answer."),
    ("Read preference and read concern", "Which member serves a read — and which data it may "
                                         "return."),
    ("Sharded cluster", "Shards hold the data, config servers hold the metadata, mongos routes "
                        "every request."),
    ("Shard key", "The indexed field or fields that decide which shard stores each "
                  "document."),
    ("Chunk and balancer", "A chunk is one range of shard-key values; the balancer moves ranges "
                           "between shards."),
]

# Abbreviations that appear on the Module 7 slides (including the diagrams).
USED = ["CA", "COLLSCAN", "CPU", "ESR", "EU", "HA", "IXSCAN", "oplog", "RAM", "URI", "US"]

# Full forms not in mdb_acronyms.ACRONYMS.
ACRONYMS = {
    "CA": "Canada (zone label)",
    "EU": "European Union (zone label)",
    "HA": "High Availability",
    "US": "United States (zone label)",
}
