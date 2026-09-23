#!/usr/bin/env python3
"""Speaker notes for the new Course Introduction deck (Mastering MongoDB).

Written from course.config.yaml, README.md, FINAL_TABLE_OF_CONTENTS.md,
labs/README.md and the seven day labs, datasets/training_store/README.md and
sample-app/README.md, in plain short sentences. Composed into the notes pane by
mdb_speaker_notes.compose(), so the layout matches the module decks:
KEY TALKING POINTS / REAL-WORLD EXAMPLES / USE-CASE SCENARIO.

Keys are slide names used by build_course_intro_new.py.
"""
from __future__ import annotations


def tp(point: str, explain: str) -> dict:
    return {"point": point, "explain": explain}


NOTES: dict[str, dict] = {
    "cover": {
        "talking_points": [
            tp("Open the course",
               "Welcome everyone to Mastering MongoDB. "
               "This is an instructor-led course that goes from document thinking all the way to "
               "production-ready operations."),
            tp("The shape of the course",
               "Say the course runs three days and eight modules. "
               "Each day ends with hands-on labs on the same sample database, training_store."),
            tp("The three days",
               "Point to the three boxes. "
               "Day 1 runs MongoDB and models documents. "
               "Day 2 queries and transforms data. "
               "Day 3 tunes, scales and ships it."),
        ],
    },
    "welcome": {
        "talking_points": [
            tp("Welcome",
               "Welcome the group. "
               "Say the three days are about doing, not just listening: learners type in mongosh "
               "from the first morning."),
            tp("In this course",
               "Everyone works on one realistic dataset, training_store. "
               "The same customers, products, orders and reviews appear in every module, so each "
               "day builds on the last."),
            tp("Ground rules",
               "Be open means ask early, even the basic questions. "
               "Be respectful means value every experience level in the room. "
               "Be engaged means run each lab step yourself and check the expected result."),
        ],
    },
    "people": {
        "talking_points": [
            tp("Go first",
               "Introduce yourself first to set the tone and the length: about one minute."),
            tp("The prompts",
               "Name, role, team, experience with databases, a goal for the three days, and one "
               "thing about yourself."),
            tp("Use the answers",
               "Note who already knows SQL, who has used JSON or a document store, and who writes "
               "application code. "
               "Refer back to their goals in the Day 3 wrap-up."),
        ],
    },
    "goals": {
        "talking_points": [
            tp("The numbers",
               "Three days with about six hours of teaching each. "
               "Eight modules, seven day labs, one sample database with four collections, and a "
               "small sample application for connecting from code."),
            tp("You will learn to",
               "Explain NoSQL design and where MongoDB fits. "
               "Design schemas around access patterns. "
               "Create, read, update and delete documents. "
               "Transform and analyze data with aggregation. "
               "Apply indexes that make real queries faster."),
            tp("And to run it well",
               "Describe how replication and sharding give availability and scale. "
               "Connect MongoDB to application code. "
               "Diagnose common query and operational issues. "
               "Judge whether a deployment is production-ready: security, backup, monitoring and "
               "runbooks."),
        ],
    },
    "audience": {
        "talking_points": [
            tp("Who it's for",
               "Software engineers, DevOps engineers, data engineers, data scientists, and anyone "
               "who works with NoSQL or document data modeling."),
            tp("Prerequisites",
               "No prior MongoDB experience is needed. "
               "Familiarity with any programming language and basic command-line use is enough to "
               "move comfortably through the labs."),
            tp("Level and format",
               "The level is introductory to intermediate. "
               "The course is instructor-led, virtual or in a classroom, and runs on a local or a "
               "cloud MongoDB."),
        ],
        "use_case_scenario":
            "A learner who has only used SQL asks whether they will keep up. "
            "Tell them Module 1 starts from why document databases exist, and every lab lists the "
            "exact commands and the expected result.",
    },
    "roadmap": {
        "talking_points": [
            tp("Day 1: Run MongoDB and model documents",
               "Modules 1 to 3. "
               "Why NoSQL exists, a working instance for everyone, and document design. "
               "Lab 1 installs, connects and verifies. "
               "Lab 2 models and populates training_store."),
            tp("Day 2: Query and transform data",
               "Modules 4 and 5, the two skills used every day. "
               "Lab 3 writes complex queries and updates. "
               "Lab 4 builds a multi-stage aggregation pipeline."),
            tp("Day 3: Tune, scale and ship",
               "Modules 6 to 8. "
               "Lab 5 indexes and explains the Day 2 queries. "
               "Lab 6 chooses between replication and sharding. "
               "Lab 7 scores training_store for production readiness."),
            tp("Why this order",
               "Aggregation sits on Day 2, next to the query language. "
               "Indexing opens Day 3 by tuning the Day 2 workload. "
               "That leaves a full afternoon for scale, security and the wrap-up."),
        ],
    },
    "modules": {
        "talking_points": [
            tp("Day 1 modules",
               "Module 1 introduces NoSQL databases. "
               "Module 2 installs MongoDB and connects mongosh and Compass. "
               "Module 3 is data modeling: access patterns, embed or reference, schema patterns "
               "and validation."),
            tp("Day 2 modules",
               "Module 4 is the MongoDB Query Language, the longest module in the course. "
               "Module 5 is the Aggregation Framework."),
            tp("Day 3 modules",
               "Module 6 covers indexing and query performance. "
               "Module 7 introduces replication and sharding. "
               "Module 8 closes with best practices, security and troubleshooting."),
        ],
    },
    "dataset": {
        "talking_points": [
            tp("One database",
               "Every module and lab uses training_store. "
               "It has four collections: customers, products, orders and reviews."),
            tp("Design decisions built in",
               "Products keep category-specific attributes, so a laptop and a book live in one "
               "collection with different fields. "
               "Orders embed their line items and a shipping snapshot, and reference the customer. "
               "Reviews live in their own collection, not as an unbounded array on the product."),
            tp("Counts to remember",
               "After a fresh load: 6 customers, 13 products, 17 orders of which 13 are PAID, and "
               "6 reviews."),
            tp("Reset each day",
               "Run load.js at the start of Day 2 and Day 3 so everyone starts from the same "
               "counts. "
               "The command is on the slide."),
        ],
        "real_world_examples": [
            "Aisha Khan, customer C101, is the top customer by paid total. "
            "Learners meet her in Module 1 and find her again in the Module 5 reports and the "
            "Module 6 index labs.",
        ],
    },
    "rhythm": {
        "talking_points": [
            tp("Module rhythm",
               "Each module opens its parts with a roadmap. "
               "Then concepts and diagrams, mongosh examples on training_store, short practice "
               "exercises, a knowledge check, the official exercises, and a summary with what "
               "comes next."),
            tp("Then the day lab",
               "Each day closes with sequenced labs that apply the day's modules: two on Day 1, "
               "two on Day 2 and three on Day 3."),
            tp("Never stuck",
               "Every lab step has a Do this and an Expected result. "
               "If a step goes wrong, reload load.js and carry on."),
            tp("Low stakes",
               "Knowledge checks are for the learners. "
               "Answer in your own words, then compare with a partner."),
        ],
    },
    "labs": {
        "talking_points": [
            tp("Day 1 labs",
               "Lab 1 is 40 minutes: connect, ping, then insert, find, update and delete a test "
               "document. "
               "Lab 2 loads training_store and asks learners to justify embed versus reference."),
            tp("Day 2 labs",
               "Lab 3 writes filters, projections, array queries and verified updates. "
               "Lab 4 builds one pipeline that reports the top-selling categories for completed "
               "sales."),
            tp("Day 3 labs",
               "Lab 5 captures an explain baseline and adds compound and multikey indexes. "
               "Lab 6 picks replication or sharding and scores shard-key candidates. "
               "Lab 7 treats training_store as a go-live candidate and scores it."),
            tp("Tracks",
               "The time-boxed track is Labs 1 to 5 and Lab 7. "
               "Lab 6 needs a replica-set URI for its keyboard step; without one, do the "
               "discussion steps."),
        ],
    },
    "environment": {
        "talking_points": [
            tp("One path each",
               "The instructor assigns one path. "
               "Path A is a local Community Edition server. "
               "Path B is a managed cloud cluster such as Atlas. "
               "Path C is a URI the instructor provides. "
               "The mongosh steps are the same on every path."),
            tp("The toolkit",
               "mongosh is the main tool, with Compass as a graphical view of the same data. "
               "The demonstration environment is Windows with PowerShell in a Cursor or VS Code "
               "terminal. "
               "The sample-app folder connects from Node.js or Python."),
            tp("Password hygiene",
               "Let mongosh prompt for the password instead of typing it into the URI. "
               "Use placeholders such as <username> in notes. "
               "Keep the connection string in the MONGODB_URI environment variable. "
               "Never paste passwords into chat, slides or screenshots."),
        ],
        "use_case_scenario":
            "A learner on Path B wants to share their Atlas connection string in chat so the "
            "instructor can help. "
            "Ask them to share the error message and the host name only, never the password.",
    },
    "outcomes": {
        "talking_points": [
            tp("The success bar",
               "Read the seven rows. "
               "Each skill is proved in a specific lab, so learners can see their own progress "
               "through the three days."),
            tp("The last row",
               "By Lab 7, learners can say whether training_store is production-ready. "
               "It is not, and they will be able to name why."),
        ],
    },
    "closing": {
        "talking_points": [
            tp("Questions",
               "Invite questions about the schedule, the labs or the environment before the "
               "content starts."),
            tp("What happens next",
               "Move to Module 1, Introduction to NoSQL Databases. "
               "Module 2 then sets up MongoDB, and Lab 1 proves every learner's environment."),
        ],
    },
}
