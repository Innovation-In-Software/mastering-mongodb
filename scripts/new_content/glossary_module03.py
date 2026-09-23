"""Key terms and abbreviations for the Module 3 deck (Data Modeling with MongoDB).

Read by mdb_glossary.intro("module03"), which builds the Key Terms and Full Forms
slides that follow Learning Objectives.
"""
from __future__ import annotations

TERMS = [
    ("Access pattern", "One read or write the application runs often — it decides the "
                       "document shape."),
    ("Embedding", "Storing related data inside the parent document, like addresses inside a "
                  "customer."),
    ("Referencing", "Storing another document's _id instead of its data, like customerId in "
                    "an order."),
    ("Cardinality", "How many items sit on each side of a relationship: one, a few, many or "
                    "millions."),
    ("Bounded array", "An array with a known, small maximum size — an order's line items, "
                      "not every review."),
    ("Snapshot", "A copy taken at one moment and never synced, like the price paid on an "
                 "order."),
    ("Schema pattern", "A reusable modeling solution, such as Attribute, Subset, Computed or "
                       "Bucket."),
    ("Schema validation", "$jsonSchema rules on a collection that check required fields and "
                          "types on writes."),
]

# Abbreviations that appear on the Module 3 slides (including the diagrams).
USED = ["BSON", "CAD", "CPU", "ID", "ISBN", "JSON", "MiB", "RAM", "SKU", "SQL", "USB"]

# Full forms not in mdb_acronyms.ACRONYMS.
ACRONYMS = {
    "CAD": "Canadian Dollar",
    "ISBN": "International Standard Book Number",
    "MiB": "Mebibyte (1,048,576 bytes)",
    "USB": "Universal Serial Bus",
}
