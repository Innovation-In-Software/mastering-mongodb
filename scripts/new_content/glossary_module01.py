"""Key terms and abbreviations for the Module 1 deck (Introduction to NoSQL Databases).

Read by mdb_glossary.intro("module01"), which builds the Key Terms and Full Forms
slides that follow Learning Objectives.
"""
from __future__ import annotations

TERMS = [
    ("NoSQL", "Not Only SQL: databases that store data in models other than relational "
              "tables."),
    ("Document", "One record stored as field-value pairs, like a JSON object — one product or "
                 "one order."),
    ("Collection", "A group of related documents inside a database, such as products or "
                   "orders."),
    ("BSON", "Binary JSON: MongoDB's typed storage format, with dates, decimals and "
             "ObjectIds."),
    ("_id and ObjectId", "_id uniquely identifies a document in its collection; ObjectId is "
                         "its default value."),
    ("Flexible schema", "Documents in one collection may have different fields; validation "
                        "rules are optional."),
    ("Access pattern", "How the application reads and writes its data — it drives the model "
                       "you choose."),
    ("Replica set", "Several mongod servers holding copies of the same data, for high "
                    "availability."),
]

# Abbreviations that appear on the Module 1 slides (including the diagrams).
USED = ["ACID", "API", "BSON", "CPU", "CRUD", "FK", "ID", "IoT", "ISBN", "JSON", "NoSQL",
        "PK", "RAM", "SKU", "SQL", "USB"]

# Full forms not in mdb_acronyms.ACRONYMS.
ACRONYMS = {
    "FK": "Foreign Key",
    "IoT": "Internet of Things",
    "ISBN": "International Standard Book Number",
    "PK": "Primary Key",
    "USB": "Universal Serial Bus",
}
