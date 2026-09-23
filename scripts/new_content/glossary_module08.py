"""Key terms and abbreviations for the Module 8 deck (Best Practices, Security and
Troubleshooting).

Read by mdb_glossary.intro("module08"), which builds the Key Terms and Full Forms
slides that follow Learning Objectives.
"""
from __future__ import annotations

TERMS = [
    ("Schema validation", "$jsonSchema rules the server checks on every insert and update — "
                          "required fields, types, enums."),
    ("Query shape", "A query's filter, sort and projection. Indexes are designed around "
                    "shapes, not single queries."),
    ("ESR rule", "Order compound-index keys Equality first, then Sort, then Range."),
    ("Least privilege", "Give each identity only the actions and collections its job "
                        "needs — nothing more."),
    ("TLS", "Transport Layer Security: encrypts traffic between clients, servers and cluster "
            "members."),
    ("RPO and RTO", "How much data you may lose, and how long recovery may take — both are "
                    "time targets."),
    ("Restore test", "Proving a backup by restoring it to an isolated target and checking "
                     "counts, samples and indexes."),
    ("Runbook", "Written steps for one alert: checks, fixes, escalation, rollback and "
                "verification."),
]

# Abbreviations that appear on the Module 8 slides (including the diagrams).
USED = ["BSON", "COLLSCAN", "CPU", "DBA", "ESR", "ID", "IP", "IXSCAN", "RBAC", "RPO",
        "RTO", "TLS", "URI", "UTC"]

# Full forms not in mdb_acronyms.ACRONYMS.
ACRONYMS: dict[str, str] = {}
