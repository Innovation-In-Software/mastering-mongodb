#!/usr/bin/env python3
"""Build the new-content Course Introduction deck for Mastering MongoDB.

Welcome, ground rules, goals, audience, the three-day roadmap, the eight
modules, the training_store dataset, how each module and lab runs, the lab
environment and what learners can do by Day 3.

Content comes from course.config.yaml, README.md, FINAL_TABLE_OF_CONTENTS.md,
labs/README.md and the seven day labs, datasets/training_store/README.md,
sample-app/README.md and the covers of the Module 1-8 decks. Styling reuses the
house kit through mdb_deck_kit, mdb_visuals and mdb_flow_slides (read-only):
title block, red/black rail, footer, page numbers and the key-takeaway bar.
Every visual is an editable PowerPoint shape. Speaker notes live in
course_intro_notes.py.

Writes decks/pptx_new/MongoDB_Course_Introduction.pptx and never touches
decks/pptx/.

    python scripts/new_content/build_course_intro_new.py
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

from pptx.enum.text import MSO_ANCHOR, PP_ALIGN  # noqa: E402

import mdb_deck_kit as K  # noqa: E402
import mdb_flow_slides as F  # noqa: E402
import mdb_visuals as V  # noqa: E402
from mdb_visuals import (  # noqa: E402
    CARD_BG, CARD_LINE, GREEN, INK, LEFT, LIGHT_NAVY, MUTED, NAVY, ORANGE, PURPLE, RED,
    RIGHT, TEAL, WIDTH,
)
from course_intro_notes import NOTES  # noqa: E402

ROOT = HERE.parents[1]
OUT = ROOT / "decks" / "pptx_new" / "MongoDB_Course_Introduction.pptx"
TAG = "COURSE INTRODUCTION"

DAY_COLORS = [NAVY, PURPLE, TEAL]
DAY_THEMES = ["Run MongoDB and model documents", "Query and transform data",
              "Tune, scale and ship"]


def light(color):
    return F.LIGHT.get(color, LIGHT_NAVY)


def notes(key: str) -> str:
    return F.notes_text(NOTES[key])


# ---------------------------------------------------------------------------
# Title and closing
# ---------------------------------------------------------------------------
def cover(prs, layout):
    slide = K._chapter_slide(
        prs, layout, tag=TAG, title="Mastering MongoDB",
        subtitle="Document modeling, queries, aggregation and production operations — "
                 "three days on one training_store database.",
        quote='"Model it, query it, tune it, ship it."',
        module_label=TAG,
    )
    V.set_slide_label("slide 1")
    gap = 0.20
    w = (WIDTH - 2 * gap) / 3
    for i, theme in enumerate(DAY_THEMES):
        V.box(slide, LEFT + i * (w + gap), 5.15, w, 0.95, f"Day {i + 1}\n{theme}",
              fill=DAY_COLORS[i], size=14, radius=0.12, margin=0.12)
    K.set_notes(slide, notes("cover"))


def closing(prs, layout):
    slide = K._chapter_slide(
        prs, layout, tag="LET'S GET STARTED", title="Questions Before\nWe Begin?",
        subtitle="Next: Module 1 — Introduction to NoSQL Databases. Then Module 2 sets up "
                 "MongoDB for Lab 1.",
        quote='"Ask early — it helps the whole room."',
        module_label=TAG,
    )
    V.set_slide_label("closing")
    K.set_notes(slide, notes("closing"))


# ---------------------------------------------------------------------------
# Content slides
# ---------------------------------------------------------------------------
def draw_welcome(slide, y0, y1):
    cw = (WIDTH - 0.40) / 2
    left_bottom = V.panel(slide, LEFT, y0, cw, "Welcome", [
        "We're glad you're here",
        "Three days of learning, building and sharing ideas",
        "Practical MongoDB skills you can use right away",
    ], icon="👋", badge_color=NAVY, size=15)
    right_bottom = V.panel(slide, LEFT + cw + 0.40, y0, cw, "In this course, you will", [
        "Work hands-on in mongosh from the first morning",
        "Use one realistic dataset, training_store",
        "Compare answers and ideas with your peers",
        "Get guidance and feedback on your lab work",
    ], icon="🎯", badge_color=GREEN, size=15)

    ry = max(left_bottom, right_bottom) + 0.95
    rh = y1 - ry
    V.section(slide, LEFT, ry - 0.52, WIDTH, "Ground rules", icon="🤝", fill=PURPLE)
    rules = [("Be open", "Ask questions early — even the ones that feel basic.", NAVY),
             ("Be respectful", "Every experience level in the room adds something.", TEAL),
             ("Be engaged", "Run every lab step yourself and check the expected result.",
              GREEN)]
    gap = 0.25
    w = (WIDTH - 2 * gap) / 3
    for k, (head, body, color) in enumerate(rules):
        x = LEFT + k * (w + gap)
        top = V.card(slide, x, ry, w, rh, head, head_fill=color)
        V.text(slide, x + 0.18, top - 0.06, w - 0.36, ry + rh - top, body, size=15,
               anchor=MSO_ANCHOR.MIDDLE)


def draw_introductions(slide, y0, y1):
    prompts = [("👤", "Your name", "What should we call you?", NAVY),
               ("💼", "Your role", "What do you do day to day?", PURPLE),
               ("🏢", "Your team", "Which team or project are you joining from?", TEAL),
               ("🧰", "Your experience", "SQL, NoSQL, JSON — or a language with a driver?",
                GREEN),
               ("🎯", "Your goal", "What do you hope to take back to your team?", ORANGE),
               ("✨", "Something about you", "A hobby, a fun fact or a favourite place.", RED)]
    call_h = 0.80
    gap = 0.22
    rows_bottom = y1 - call_h - 0.25
    rh = (rows_bottom - y0 - gap) / 2
    cw = (WIDTH - 2 * gap) / 3
    for k, (icon, head, body, color) in enumerate(prompts):
        row, col = divmod(k, 3)
        x, y = LEFT + col * (cw + gap), y0 + row * (rh + gap)
        V.box(slide, x, y, cw, rh, "", fill=CARD_BG, line=CARD_LINE, radius=0.08)
        V.icon_badge(slide, x + 0.22, y + 0.24, 0.60, icon, color)
        V.text(slide, x + 0.98, y + 0.22, cw - 1.15, 0.64, head, size=16, bold=True,
               color=color, anchor=MSO_ANCHOR.MIDDLE)
        V.text(slide, x + 0.22, y + 0.98, cw - 0.44, rh - 1.10, body, size=15)
    V.callout(slide, LEFT, y1 - call_h, WIDTH, call_h, "How it works",
              "About one minute each. The instructor goes first.", size=15)


def draw_goals(slide, y0, y1):
    stats = [("3", "days", "~6 hours of teaching a day", NAVY),
             ("8", "modules", "From NoSQL to production", PURPLE),
             ("7", "day labs", "Two, two, then three", TEAL),
             ("4", "collections", "One training_store database", GREEN),
             ("1", "sample app", "Node.js or Python driver", ORANGE)]
    gap = 0.20
    w = (WIDTH - 4 * gap) / 5
    sh = 1.90
    for k, (num, label, sub, color) in enumerate(stats):
        x = LEFT + k * (w + gap)
        V.box(slide, x, y0, w, sh, "", fill=light(color), radius=0.10)
        V.text(slide, x, y0 + 0.08, w, 0.80, num, size=34, bold=True, color=color,
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        V.text(slide, x + 0.08, y0 + 0.88, w - 0.16, 0.50, label, size=15, bold=True,
               color=INK, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        V.text(slide, x + 0.10, y0 + 1.36, w - 0.20, 0.46, sub, size=12, color=MUTED,
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    py = y0 + sh + 0.35
    cw = (WIDTH - 0.40) / 2
    V.panel(slide, LEFT, py, cw, "You will learn to", [
        "Explain NoSQL design and where MongoDB fits",
        "Design schemas around access patterns",
        "Create, read, update and delete documents",
        "Transform and analyze data with aggregation",
        "Apply indexes that speed up real queries",
    ], icon="🎓", badge_color=NAVY, size=15)
    V.panel(slide, LEFT + cw + 0.40, py, cw, "And to run it well", [
        "Describe how replication and sharding help",
        "Connect MongoDB to application code",
        "Diagnose common query and operations issues",
        "Judge whether a deployment is production-ready",
    ], icon="🛡️", badge_color=GREEN, size=15)


def draw_audience(slide, y0, y1):
    call_h = 0.72
    body_bottom = y1 - call_h - 0.25
    lw = 6.55
    y = V.section(slide, LEFT, y0, lw, "Who this course is for", icon="👥", fill=NAVY)
    roles = [("💻", "Software engineers", "Build features on document data", NAVY),
             ("⚙️", "DevOps engineers", "Run, secure and monitor deployments", PURPLE),
             ("🔀", "Data engineers", "Move and reshape data with pipelines", TEAL),
             ("📊", "Data scientists", "Query and aggregate data for analysis", GREEN),
             ("🧩", "Document modelers", "Anyone modeling NoSQL documents", ORANGE)]
    rg = 0.10
    rh = (body_bottom - y - rg * (len(roles) - 1)) / len(roles)
    for k, (icon, head, body, color) in enumerate(roles):
        ry = y + k * (rh + rg)
        V.box(slide, LEFT, ry, lw, rh, "", fill=CARD_BG, line=CARD_LINE, radius=0.10)
        V.icon_badge(slide, LEFT + 0.14, ry + (rh - 0.44) / 2, 0.44, icon, color)
        V.text(slide, LEFT + 0.72, ry, 2.35, rh, head, size=15, bold=True, color=color,
               anchor=MSO_ANCHOR.MIDDLE)
        V.text(slide, LEFT + 3.10, ry, lw - 3.20, rh, body, size=14,
               anchor=MSO_ANCHOR.MIDDLE)

    rx = LEFT + lw + 0.45
    rw = RIGHT - rx
    y = V.section(slide, rx, y0, rw, "Prerequisites", icon="✅", fill=GREEN)
    for k, item in enumerate(["No prior MongoDB experience",
                              "Familiarity with any programming language",
                              "Basic command-line use"]):
        cy = y + k * 0.50
        V.check(slide, rx, cy + 0.04, 0.34)
        V.text(slide, rx + 0.48, cy, rw - 0.48, 0.42, item, size=15,
               anchor=MSO_ANCHOR.MIDDLE)
    y = V.section(slide, rx, y + 1.62, rw, "Course format", icon="🗓️", fill=PURPLE)
    V.chips(slide, rx, y, rw, ["Instructor-led", "Virtual or classroom",
                               "Introductory to intermediate", "Local or cloud MongoDB"],
            cols=2, h=0.52, gap=0.12, fill=light(PURPLE), color=PURPLE, size=13)
    V.callout(slide, LEFT, y1 - call_h, WIDTH, call_h, "New to NoSQL?",
              "Module 1 starts from the beginning: why document databases exist at all.",
              size=15)


DAY_PLAN = [
    ("Modules 1–3",
     "Why NoSQL exists, a working instance for everyone, then document design.",
     [("Lab 1", "Install, connect and verify"), ("Lab 2", "Model and populate")]),
    ("Modules 4–5",
     "Find, filter and change documents — then reshape them in pipelines.",
     [("Lab 3", "Complex queries and updates"), ("Lab 4", "Aggregation pipeline")]),
    ("Modules 6–8",
     "Make Day 2's queries fast, keep data available, and get production-ready.",
     [("Lab 5", "Index and explain"), ("Lab 6", "Replication and sharding"),
      ("Lab 7", "Production readiness")]),
]


def draw_roadmap(slide, y0, y1):
    V.section(slide, LEFT, y0, WIDTH, "Three days, one database", icon="🗺️", fill=NAVY)
    V.chevrons(slide, LEFT, y0 + 0.50, WIDTH, 0.95,
               [f"Day {d + 1}\n{t}" for d, t in enumerate(DAY_THEMES)], DAY_COLORS, size=15)
    cy = y0 + 1.72
    gap = 0.25
    w = (WIDTH - 2 * gap) / 3
    for d, (mods, focus, labs) in enumerate(DAY_PLAN):
        x = LEFT + d * (w + gap)
        color = DAY_COLORS[d]
        top = V.card(slide, x, cy, w, y1 - cy, mods, head_fill=color)
        V.text(slide, x + 0.18, top, w - 0.36, 0.80, focus, size=14)
        ly = top + 0.92
        for k, (lab, name) in enumerate(labs):
            by = ly + k * 0.56
            V.box(slide, x + 0.18, by, w - 0.36, 0.46, "", fill=light(color), radius=0.12)
            V.text(slide, x + 0.30, by, 0.80, 0.46, lab, size=13, bold=True, color=color,
                   anchor=MSO_ANCHOR.MIDDLE)
            V.text(slide, x + 1.05, by, w - 1.30, 0.46, name, size=13, color=INK,
                   anchor=MSO_ANCHOR.MIDDLE)


MODULE_DAYS = [
    [("1", "Introduction to NoSQL Databases",
      "Why NoSQL, four models, documents, architecture and fit"),
     ("2", "Installation and Setup",
      "Deploy, connect with mongosh and Compass, then verify"),
     ("3", "Data Modeling with MongoDB",
      "Access patterns, embed or reference, patterns, validation")],
    [("4", "The MongoDB Query Language",
      "Filter, project, insert, update, upsert and delete"),
     ("5", "The Aggregation Framework",
      "Totals, rankings and reports — one stage at a time")],
    [("6", "Indexing and Query Performance",
      "COLLSCAN vs IXSCAN, ESR, explain() and covered queries"),
     ("7", "Introduction to Replication and Sharding",
      "Replica sets, failover, read and write guarantees, shard keys"),
     ("8", "Best Practices, Security, and Troubleshooting",
      "Model, tune, secure, recover and diagnose")],
]


def draw_modules(slide, y0, y1):
    gap = 0.25
    w = (WIDTH - 2 * gap) / 3
    head_h = 0.80
    tile_gap = 0.14
    tile_h = (y1 - y0 - head_h - 0.14 - 2 * tile_gap) / 3
    for d, modules in enumerate(MODULE_DAYS):
        x = LEFT + d * (w + gap)
        color = DAY_COLORS[d]
        V.box(slide, x, y0, w, head_h, f"DAY {d + 1}\n{DAY_THEMES[d]}", fill=color, size=14,
              radius=0.08, margin=0.08)
        for m, (num, name, blurb) in enumerate(modules):
            ty = y0 + head_h + 0.14 + m * (tile_h + tile_gap)
            V.box(slide, x, ty, w, tile_h, "", fill=light(color), line=CARD_LINE, radius=0.08)
            V.badge(slide, x + 0.14, ty + 0.16, 0.48, num, fill=color, size=15)
            V.text(slide, x + 0.76, ty + 0.08, w - 0.88, 0.64, name, size=14, bold=True,
                   color=INK, anchor=MSO_ANCHOR.MIDDLE)
            V.text(slide, x + 0.76, ty + 0.72, w - 0.88, tile_h - 0.78, blurb, size=12,
                   color=MUTED)


COLLECTIONS = [
    ("customers · 6", "Nested name and contact, a bounded addresses array", NAVY),
    ("products · 13", "LAPTOP, SHOE, BOOK and ACCESSORY, each with its own attributes", TEAL),
    ("orders · 17", "13 PAID. Embeds line items; references the customer", PURPLE),
    ("reviews · 6", "Ratings 3–5, stored apart from the product", GREEN),
]


def draw_dataset(slide, y0, y1):
    gap = 0.22
    w = (WIDTH - 3 * gap) / 4
    ch = 1.62
    for k, (head, body, color) in enumerate(COLLECTIONS):
        x = LEFT + k * (w + gap)
        top = V.card(slide, x, y0, w, ch, head, head_fill=color, title_size=14)
        V.text(slide, x + 0.16, top, w - 0.32, y0 + ch - top - 0.06, body, size=14)

    y = V.section(slide, LEFT, y0 + ch + 0.25, WIDTH, "One database, every day", icon="🛒",
                  fill=PURPLE)
    V.chevrons(slide, LEFT, y, WIDTH, 0.80,
               ["Day 1\nModel, build and load", "Day 2\nQuery, update and aggregate",
                "Day 3\nIndex, replicate and ship"], DAY_COLORS, size=14)

    y = V.section(slide, LEFT, y + 1.02, WIDTH, "Fresh start on Day 2 and Day 3", icon="🔄",
                  fill=TEAL)
    V.code(slide, LEFT, y, WIDTH, y1 - y,
           "# PowerShell, from the course repository root\n"
           'mongosh "mongodb://localhost:27017" .\\datasets\\training_store\\load.js',
           size=15)


def draw_rhythm(slide, y0, y1):
    V.section(slide, LEFT, y0, WIDTH, "The rhythm of each module", icon="🔁", fill=NAVY)
    steps_ = ["Part\nopener", "Concepts and\ndiagrams", "mongosh\nexamples", "Practice\nexercises",
              "Knowledge\ncheck", "Official\nexercises", "Summary\nand next"]
    V.chevrons(slide, LEFT, y0 + 0.50, WIDTH, 0.95, steps_,
               [NAVY, PURPLE, TEAL, GREEN, ORANGE, RED, NAVY], size=13)

    cards = [("Then the day lab", "Each day closes with sequenced labs on training_store: two, "
                                  "two, then three.", TEAL),
             ("Never stuck", "Every step has a Do this and an Expected result. Reload load.js "
                             "to catch up.", GREEN),
             ("Ask any time", "Questions in the room or in chat are always welcome — lab time is "
                              "for trying things.", PURPLE)]
    cy = y0 + 1.80
    call_h = 0.80
    ch = y1 - cy - call_h - 0.30
    gap = 0.25
    w = (WIDTH - 2 * gap) / 3
    for k, (head, body, color) in enumerate(cards):
        x = LEFT + k * (w + gap)
        top = V.card(slide, x, cy, w, ch, head, head_fill=color)
        V.text(slide, x + 0.18, top, w - 0.36, cy + ch - top - 0.10, body, size=15,
               anchor=MSO_ANCHOR.MIDDLE)
    V.callout(slide, LEFT, y1 - call_h, WIDTH, call_h, "Low stakes",
              "Knowledge checks are for you — answer in your own words, then compare with a "
              "partner.", size=15)


LABS = [
    (1, "Lab 1 — Install, connect and verify", "Ping, then insert, find, update, delete",
     "40 min"),
    (1, "Lab 2 — Model and populate", "Load training_store; justify embed vs reference",
     "50–90 min"),
    (2, "Lab 3 — Complex queries and updates", "Filters, projections, arrays, verified updates",
     "60–75 min"),
    (2, "Lab 4 — Aggregation pipeline", "Rank top-selling categories for completed sales",
     "45–60 min"),
    (3, "Lab 5 — Index and explain", "Baseline, compound and multikey indexes",
     "40–50 min"),
    (3, "Lab 6 — Replication and sharding", "Pick the mechanism, score shard keys",
     "30–40 min"),
    (3, "Lab 7 — Production readiness", "Fix, validate, restore, then score go-live",
     "45–60 min"),
]


def draw_labs(slide, y0, y1):
    call_h = 0.62
    rows_bottom = y1 - call_h - 0.18
    gap = 0.08
    rh = (rows_bottom - y0 - gap * (len(LABS) - 1)) / len(LABS)
    day_w, time_w = 1.00, 1.45
    mx = LEFT + day_w + 0.12
    mw = WIDTH - day_w - time_w - 0.24
    for k, (day, name, what, mins) in enumerate(LABS):
        y = y0 + k * (rh + gap)
        color = DAY_COLORS[day - 1]
        V.box(slide, LEFT, y, day_w, rh, f"DAY {day}", fill=color, size=13, radius=0.10)
        V.box(slide, mx, y, mw, rh, "", fill=CARD_BG, line=CARD_LINE, radius=0.10)
        V.text(slide, mx + 0.16, y, 4.35, rh, name, size=14, bold=True, color=color,
               anchor=MSO_ANCHOR.MIDDLE)
        V.text(slide, mx + 4.60, y, mw - 4.70, rh, what, size=13, anchor=MSO_ANCHOR.MIDDLE)
        V.box(slide, RIGHT - time_w, y, time_w, rh, mins, fill=light(color), color=color,
              size=13, radius=0.10)
    V.callout(slide, LEFT, y1 - call_h, WIDTH, call_h, "Time-boxed track",
              "Labs 1–5 and 7. Lab 6 needs a replica-set URI — or do its discussion steps.",
              size=14)


PATHS = [
    ("A", "Local Community Edition", "mongod on your own machine at\nmongodb://localhost:27017",
     NAVY),
    ("B", "Managed cloud (Atlas)", "A database user, your IP allowed\nand a mongodb+srv:// URI",
     PURPLE),
    ("C", "Instructor URI", "A shared server — the URI is sent\nsecurely, never in chat", TEAL),
]


def draw_environment(slide, y0, y1):
    y = V.section(slide, LEFT, y0, WIDTH, "One path each — the instructor assigns it",
                  icon="🧭", fill=NAVY)
    gap = 0.25
    w = (WIDTH - 2 * gap) / 3
    ph = 1.40
    for k, (letter, head, body, color) in enumerate(PATHS):
        x = LEFT + k * (w + gap)
        V.box(slide, x, y, w, ph, "", fill=CARD_BG, line=CARD_LINE, radius=0.08)
        V.badge(slide, x + 0.16, y + 0.14, 0.50, letter, fill=color, size=16)
        V.text(slide, x + 0.80, y + 0.12, w - 0.95, 0.54, head, size=15, bold=True,
               color=color, anchor=MSO_ANCHOR.MIDDLE)
        V.text(slide, x + 0.18, y + 0.72, w - 0.36, ph - 0.78, body, size=13)

    by = y + ph + 0.30
    lw = 5.90
    cy = V.section(slide, LEFT, by, lw, "Your toolkit", icon="🧰", fill=TEAL)
    V.chips(slide, LEFT, cy, lw, ["mongosh", "MongoDB Compass", "PowerShell",
                                  "Cursor or VS Code", "training_store load.js",
                                  "sample-app: Node or Python"],
            cols=2, h=0.50, gap=0.12, fill=light(TEAL), color=TEAL, size=13)

    rx = LEFT + lw + 0.45
    rw = RIGHT - rx
    cy = V.section(slide, rx, by, rw, "Password hygiene", icon="🔐", fill=RED)
    rules = ["Let mongosh prompt — no password in the URI",
             "Use placeholders such as <username> in notes",
             "Keep the URI in the MONGODB_URI variable",
             "Never paste passwords in chat or screenshots"]
    step = (y1 - cy) / len(rules)
    for k, rule in enumerate(rules):
        ry = cy + k * step
        V.check(slide, rx, ry + (step - 0.34) / 2 - 0.04, 0.34)
        V.text(slide, rx + 0.48, ry - 0.04, rw - 0.48, step, rule, size=14,
               anchor=MSO_ANCHOR.MIDDLE)


OUTCOMES = [
    ("Connect to MongoDB and prove the environment works", "Lab 1"),
    ("Explain the document model — and when to embed or reference", "Lab 2"),
    ("Write filters, projections and verified updates", "Lab 3"),
    ("Build a multi-stage aggregation pipeline", "Lab 4"),
    ("Read an explain() plan: COLLSCAN or IXSCAN", "Lab 5"),
    ("Choose replication, sharding or both for a requirement", "Lab 6"),
    ("Say whether training_store is production-ready — and why", "Lab 7"),
]
OUTCOME_DAYS = [0, 0, 1, 1, 2, 2, 2]


def draw_outcomes(slide, y0, y1):
    call_h = 0.72
    rows_bottom = y1 - call_h - 0.22
    gap = 0.09
    rh = (rows_bottom - y0 - gap * (len(OUTCOMES) - 1)) / len(OUTCOMES)
    pill_w = 1.50
    for k, (skill, lab) in enumerate(OUTCOMES):
        y = y0 + k * (rh + gap)
        color = DAY_COLORS[OUTCOME_DAYS[k]]
        V.box(slide, LEFT, y, WIDTH, rh, "", fill=CARD_BG, line=CARD_LINE, radius=0.10)
        V.check(slide, LEFT + 0.14, y + (rh - 0.34) / 2, 0.34)
        V.text(slide, LEFT + 0.64, y, WIDTH - pill_w - 0.90, rh, skill, size=15,
               anchor=MSO_ANCHOR.MIDDLE)
        V.box(slide, RIGHT - pill_w - 0.10, y + 0.06, pill_w, rh - 0.12,
              f"{lab} · Day {OUTCOME_DAYS[k] + 1}", fill=light(color), color=color, size=12,
              radius=0.30)
    V.callout(slide, LEFT, y1 - call_h, WIDTH, call_h, "The success bar",
              "Do all seven by the end of Day 3. (It isn't production-ready yet — you'll "
              "name why.)", size=15)


# ---------------------------------------------------------------------------
def steps():
    return [
        cover,
        F.custom(draw_welcome, "Welcome to the Course",
                 "A warm welcome, a few ground rules and how we'll work together.",
                 takeaway="Three days of hands-on learning — ask early, try everything, share "
                          "ideas.",
                 notes=NOTES["welcome"]),
        F.custom(draw_introductions, "Let's Get to Know Each Other",
                 "Take a minute to introduce yourself to the group.",
                 takeaway="Knowing the room helps us connect MongoDB to your real work.",
                 notes=NOTES["people"]),
        F.custom(draw_goals, "Course Goals and Expected Outcomes",
                 "What's in the course — and what you'll be able to do with it.",
                 takeaway="Eight modules and seven labs take you from document thinking to "
                          "production-ready operations.",
                 notes=NOTES["goals"]),
        F.custom(draw_audience, "Who This Course Is For",
                 "The audience, the prerequisites and the format.",
                 takeaway="No MongoDB experience needed — any programming language and a "
                          "command line are enough.",
                 notes=NOTES["audience"]),
        F.custom(draw_roadmap, "The Three-Day Roadmap",
                 "Foundations, then daily data work, then performance and production.",
                 takeaway="Each day ends by applying its modules in hands-on labs on the same "
                          "data.",
                 notes=NOTES["roadmap"]),
        F.custom(draw_modules, "The Eight Modules at a Glance",
                 "Grouped by the day we teach them.",
                 takeaway="Aggregation sits next to the query language, and indexing opens Day 3 "
                          "by tuning it.",
                 notes=NOTES["modules"]),
        F.custom(draw_dataset, "One Dataset Through the Course",
                 "training_store: a small online store you model, query, tune and ship.",
                 takeaway="The same customers, products, orders and reviews appear in every "
                          "module and lab.",
                 notes=NOTES["dataset"]),
        F.custom(draw_rhythm, "How Each Module Runs",
                 "Short concept blocks, practice and checks — then build it in the lab.",
                 takeaway="Learn a concept, see it in mongosh, practise it, check it, then use "
                          "it in a lab.",
                 notes=NOTES["rhythm"]),
        F.custom(draw_labs, "Seven Hands-On Day Labs",
                 "Sequenced labs on training_store, each with Do this and Expected result "
                 "steps.",
                 takeaway="Every lab runs on live training_store data — reload it and you can "
                          "always catch up.",
                 notes=NOTES["labs"]),
        F.custom(draw_environment, "Lab Environment and Tools",
                 "Where your MongoDB runs, the tools you use, and how to keep secrets safe.",
                 takeaway="Every path uses the same mongosh steps — and no password ever lands "
                          "in chat.",
                 notes=NOTES["environment"]),
        F.custom(draw_outcomes, "What You'll Be Able to Do by Day 3",
                 "Seven skills, each proved in a lab.",
                 takeaway="You leave able to model, query, aggregate, tune, scale and assess "
                          "MongoDB.",
                 notes=NOTES["outcomes"]),
        closing,
    ]


def main() -> None:
    prs = K.new_presentation()
    layout = K.blank_layout(prs)
    F.build_sequence(prs, layout, steps())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    K.save_presentation(prs, OUT)
    print(f"Wrote {len(prs.slides)} slides -> {OUT.relative_to(ROOT)}")
    for w in V.WARNINGS:
        print("  WARN", w)


if __name__ == "__main__":
    main()
