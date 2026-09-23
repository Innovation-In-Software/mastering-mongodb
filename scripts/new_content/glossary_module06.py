"""Key terms and abbreviations for the Module 6 deck (Indexing and Query Performance).

Read by mdb_glossary.intro("module06"), which builds the Key Terms and Full Forms
slides that follow Learning Objectives.
"""
from __future__ import annotations

TERMS = [
    ("Index", "A sorted structure of field values with pointers to documents, so MongoDB "
              "can skip the full scan."),
    ("COLLSCAN and IXSCAN", "Plan stages: read every document, or walk the matching keys "
                            "of one index."),
    ("Compound index", "One index on several fields, sorted by the first field, then the "
                       "next."),
    ("ESR guideline", "Order compound fields Equality first, then Sort, then Range — a "
                      "starting point, not a law."),
    ("Multikey index", "An index on an array field: one index key for each array value."),
    ("explain()", "Shows the plan MongoDB chose and, with executionStats, the keys and "
                  "documents it examined."),
    ("Covered query", "Filter and returned fields all come from one index, so no document "
                      "is fetched."),
    ("Selectivity", "How small a share of the collection a condition matches — sku is high, "
                    "active is low."),
]

# Abbreviations that appear on the Module 6 slides (including the diagrams).
USED = ["COLLSCAN", "CPU", "ESR", "I/O", "IXSCAN", "JSON", "RAM", "SKU", "TTL"]

# Full forms not in mdb_acronyms.ACRONYMS.
ACRONYMS = {
    "I/O": "Input/Output",
}
