"""Key terms and abbreviations for the Module 2 deck (Installation and Setup).

Read by mdb_glossary.intro("module02"), which builds the Key Terms and Full Forms
slides that follow Learning Objectives.
"""
from __future__ import annotations

TERMS = [
    ("mongod", "The MongoDB server process: it listens on a port, stores the data files and "
               "answers every request."),
    ("mongosh", "The MongoDB Shell: a command-line client that sends commands to mongod and "
                "prints the results."),
    ("MongoDB Compass", "MongoDB's graphical client for browsing and editing the same data "
                        "that mongosh sees."),
    ("MongoDB Atlas", "MongoDB's managed cloud service: the vendor runs, backs up and scales "
                      "the cluster."),
    ("Connection string", "A URI such as mongodb://localhost:27017 that tells a client where "
                          "and how to connect."),
    ("localhost:27017", "The default address of a local mongod: this machine, port 27017."),
    ("Authentication vs authorization", "Authentication proves who you are; authorization "
                                        "(roles) decides what you may do."),
    ("Ping", "db.runCommand({ ping: 1 }) returns ok: 1 when the server answers — reachability, "
             "not write access."),
]

# Abbreviations that appear on the Module 2 slides (including the diagrams).
USED = ["CLI", "CRUD", "DB", "DNS", "GUI", "IP", "MSI", "OS", "SRV", "TLS", "URI", "VM"]

# Full forms not in mdb_acronyms.ACRONYMS.
ACRONYMS = {
    "MSI": "Microsoft Installer (Windows Installer package)",
}
