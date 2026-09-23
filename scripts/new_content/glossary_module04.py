"""Key terms and abbreviations for the Module 4 deck (The MongoDB Query Language).

Read by mdb_glossary.intro("module04"), which builds the Key Terms and Full Forms
slides that follow Learning Objectives.
"""
from __future__ import annotations

TERMS = [
    ("Query filter", "A document that says which documents match, e.g. { category: \"BOOK\" }. "
                     "{} matches every document."),
    ("Projection", "The second find() argument: it chooses which fields come back, e.g. "
                   "{ name: 1, _id: 0 }."),
    ("Cursor", "What find() returns: a pointer that hands back matching documents in "
               "batches, not all at once."),
    ("Dot notation", "A quoted path into nested fields and arrays, such as \"attributes.sizes\" "
                     "or \"items.sku\"."),
    ("$elemMatch", "Requires one array element to meet every condition — not different "
                   "elements for different conditions."),
    ("Update operator", "$set, $inc, $push and friends: change named fields in place instead "
                        "of replacing the document."),
    ("Upsert", "{ upsert: true }: update the match, or insert a new document when nothing "
               "matches the filter."),
    ("Write result", "What every write returns: acknowledged, matchedCount, modifiedCount, "
                     "insertedId, deletedCount."),
]

# Abbreviations that appear on the Module 4 slides (including the diagrams).
USED = ["BSON", "CRUD", "ID", "ISO", "JSON", "MQL", "SKU", "SQL", "USB", "UTC"]

# Full forms not in mdb_acronyms.ACRONYMS.
ACRONYMS = {
    "ISO": "International Organization for Standardization (ISODate uses the ISO 8601 date "
           "format)",
    "MQL": "MongoDB Query Language",
    "USB": "Universal Serial Bus",
}
