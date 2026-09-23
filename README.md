# Mastering MongoDB

Instructor-led course for teams that need working command of MongoDB — from document thinking through queries, aggregation, indexing, and production-ready operations.

| | |
|---|---|
| **Duration** | 3 days |
| **Modality** | Instructor-led (virtual or classroom) |
| **Platform** | MongoDB (local or cloud) |
| **Level** | Introductory to intermediate |
| **Organization** | Innovation In Software Corporation |

Source outline: [`Mastering_MongoDB_Course_Outline.docx`](Mastering_MongoDB_Course_Outline.docx)

---

## Course overview

Participants learn why document storage exists, then practice the skills teams use day to day: modeling documents, writing queries, shaping data through aggregation pipelines, tuning with indexes, and planning for availability at scale.

Instruction alternates between short concept segments and hands-on keyboard work. Exercises are drawn from realistic application scenarios so participants can apply the material to their own projects, not only recognize syntax.

---

## Objectives

Upon completion, participants will be able to:

- Explain the design principles behind NoSQL databases and where MongoDB fits among them
- Design and implement document schemas suited to an application's access patterns
- Perform create, read, update, and delete operations using the MongoDB query language
- Transform and analyze data using the aggregation framework
- Apply indexing strategies that improve query performance
- Describe how sharding and replication support scalability and high availability
- Connect MongoDB to applications and external services
- Diagnose and resolve common operational and query issues
- Assess whether a MongoDB deployment is production-ready (security, backup, monitoring, runbooks)

---

## Audience and prerequisites

**Audience:** software engineers, DevOps engineers, data engineers, data scientists, and anyone working with NoSQL or document data modeling.

**Prerequisites:** no prior MongoDB experience. Familiarity with any programming language and basic command-line use is enough to move comfortably through the labs.

---

## Three-day outline

The source outline put all of querying on Day 2 and four topics on Day 3. This schedule ignores that split and balances **instructional weight** (~6 hours/day): foundations, then daily data work, then production.

| Day | Theme | Modules | Teaching | Labs |
|-----|-------|---------|----------|------|
| **1** | Run MongoDB and model documents | 1–3 | ~6 h | Install/connect · model and populate |
| **2** | Query and transform data | 4–5 | ~6 h | Complex queries/updates · aggregation pipeline |
| **3** | Tune, scale, and ship | 6–8 | ~6 h | Index and `explain` · replica sets · production readiness |

Aggregation moves to Day 2 so it sits next to the query language. Indexing opens Day 3 by tuning the pipeline from Day 2. Sharding, security, and wrap-up then have a full afternoon instead of being squeezed in.

### Day 1 — Foundations (~6 hours)

Get every participant onto a working instance, then shift into document thinking: how data that would span several relational tables becomes one document, and what that means for schema design.

| Time | Module | Title | Topics |
|------|--------|-------|--------|
| ~1.5 h | 1 | Introduction to NoSQL Databases | Defining NoSQL; document vs key-value vs graph; MongoDB architecture; core features |
| ~1.5–2 h | 2 | Installation and Setup | Deployment options; `mongod` / `mongosh` / Compass; connection strings; first write-and-read |
| ~3 h | 3 | Data Modeling with MongoDB | Documents, collections, databases; schemas and access patterns; embed vs reference |

**Labs:** [`Lab 1`](labs/day-01/lab1/LAB-1-GUIDE.md) install/connect · [`Lab 2`](labs/day-01/lab2/LAB-2-GUIDE.md) model and populate. Exercises 1.1–3.9: [`labs/day-01/exercises/`](labs/day-01/exercises/).

### Day 2 — Working with data (~6 hours)

The two skills used every day: retrieve and change documents, then reshape them through aggregation. Same sample dataset as Day 1.

| Time | Module | Title | Topics |
|------|--------|-------|--------|
| ~3 h (or 6–7 h full) | 4 | The MongoDB Query Language | `find` / `findOne`; comparison, logical, array, and update operators; projections; safe writes |
| ~3 h | 5 | The Aggregation Framework | Pipeline structure; `$match`, `$group`, `$project`, `$sort`, `$limit`; multi-stage analytics |

**Labs:** [`Lab 3`](labs/day-02/lab3/LAB-3-GUIDE.md) queries and updates · [`Lab 4`](labs/day-02/lab4/LAB-4-GUIDE.md) aggregation pipeline. Reload `datasets/training_store/load.js` first. Exercises 4.1–5.4: [`labs/day-02/exercises/`](labs/day-02/exercises/).

### Day 3 — Performance and production (~6 hours)

Make Day 2’s queries and pipelines fast, then cover how MongoDB stays available at scale and what to carry back to the team.

| Time | Module | Title | Topics |
|------|--------|-------|--------|
| ~2 h (or 3–3.5 h full) | 6 | Indexing and Query Performance | Create and manage indexes; ESR and prefixes; `explain()`; specialized types |
| ~2 h (or 3–3.5 h full) | 7 | Introduction to Replication and Sharding | Replica sets, elections, read/write guarantees; shards, keys, routing |
| ~2 h (or 3–3.5 h full) | 8 | MongoDB Best Practices, Security, and Troubleshooting | Modeling, queries, indexes, security, backup/restore, monitoring, troubleshooting, production-readiness checklist |

**Labs:** [`Lab 5`](labs/day-03/lab5/LAB-5-GUIDE.md) index and `explain` · [`Lab 6`](labs/day-03/lab6/LAB-6-GUIDE.md) replica set / shard key · [`Lab 7`](labs/day-03/lab7/LAB-7-GUIDE.md) production readiness. Exercises 6.1–8.3: [`labs/day-03/exercises/`](labs/day-03/exercises/). Application connection: [`sample-app/`](sample-app/README.md).

---

## Folder structure

The instructor decks follow the MD287 "new content" build: one PowerPoint per module plus a course
introduction, each written as a slide flow with speaker notes. Hands-on material lives under
`labs/`, sequenced exactly as it appears on the slides.

```text
MasteringMongoDB/
├── README.md                              # This file
├── course.config.yaml                     # Course name, days, module list
├── Mastering_MongoDB_Course_Outline.docx  # Source outline (reference)
│
├── decks/pptx_new/                        # Instructor decks (current)
│   ├── MongoDB_Course_Introduction.pptx
│   └── MongoDB_ModuleNN_<Title>.pptx      # Modules 1–8
│
├── labs/                                  # Hands-on, in slide order
│   ├── README.md · EXERCISES-INDEX.md · LABS-INDEX.md
│   ├── day-01/  exercises/ (1.1–3.9)  exercises/solution/  lab1/  lab2/
│   ├── day-02/  exercises/ (4.1–5.4)  exercises/solution/  lab3/  lab4/
│   ├── day-03/  exercises/ (6.1–8.3)  exercises/solution/  lab5/  lab6/  lab7/
│   └── practice-exercises/            # answers to the in-slide practice exercises
│
├── datasets/training_store/load.js        # The one sample database used everywhere
├── sample-app/                            # Node.js + Python connection demo
├── kahoot/                                # One 15-question quiz per module (Excel)
│
├── scripts/new_content/                   # Deck build (current)
│   ├── mdb_*.py                           # Shared kit: layouts, visuals, notes, glossary
│   ├── moduleNN_flow.py · moduleNN_notes.py · glossary_moduleNN.py
│   ├── build_moduleNN_new.py · build_course_intro_new.py
│   ├── build_lab_indexes.py               # Regenerates the labs/ indexes
│   └── diagrams/moduleNN/                 # Diagrams chosen for each module deck
├── scripts/chatgpt_diagrams/diagrams/     # Full diagram library (source images)
│
├── archive/                               # Superseded guides (reference only)
│   ├── slide-exercises/module-NN/
│   └── labs/
│
├── decks/pptx/ · slides/ · scripts/*.py   # Earlier day-deck / Marp pipeline (legacy)
```

### Why this layout

| Folder | Role |
|--------|------|
| `decks/pptx_new/` | The current instructor decks: Course Introduction + Modules 1–8 (38–52 slides each), MD287 house style. Each module: cover, objectives, key terms, full forms, parts with diagrams and code, practice exercises, knowledge check, official exercises, the module's day lab, summary. |
| `labs/day-0N/exercises/` | Participant worksheets for the official exercises, numbered *M.N* in slide order; answer keys in `exercises/solution/`. |
| `labs/day-0N/labN/` | The seven day labs (`LAB-N-GUIDE.md`), each the last official slide of the module it follows; expected outputs in `labN/solution/`. |
| `labs/practice-exercises/` | Reference answers for the unnumbered in-slide practice exercises. |
| `datasets/` | One sample application dataset reused on Days 1–3, so modeling, queries, aggregation and indexes stay consistent. Every slide, worksheet and lab result matches a fresh `load.js`. |
| `sample-app/` | Small Node.js + Python connection demo. URI from `MONGODB_URI` only. |
| `kahoot/` | One Kahoot bank per module (15 questions, 30 seconds), aligned to `decks/pptx_new/`. Import the Excel file in Kahoot. See [kahoot/README.md](kahoot/README.md). |
| `archive/` | The earlier `slide-exercises/` guides and flat day-lab files, kept for reference. Not part of the participant path. |
| `decks/pptx/`, `slides/`, `scripts/*.py` | The earlier Marp / day-deck pipeline. Kept for reference; the current decks come from `scripts/new_content/`. |

---

## Building the decks and indexes

```powershell
# one module deck (repeat per module), or the course introduction
python scripts/new_content/build_module01_new.py
python scripts/new_content/build_course_intro_new.py

# regenerate labs/README.md, labs/EXERCISES-INDEX.md and labs/LABS-INDEX.md
python scripts/new_content/build_lab_indexes.py

# regenerate the eight Kahoot Excel banks from scripts/mongodb_kahoot_questions.py
python scripts/check_kahoot_length_tells.py
python scripts/regenerate_kahoot_xlsx.py
```

When a slide changes an exercise or lab, update the matching worksheet in `labs/` (and its
solution) in the same change, then rerun `build_lab_indexes.py`. Expected results in the
worksheets and solutions were worked out from `load.js`; run the key examples once in mongosh
before teaching.

---

## Conventions

| Item | Rule |
|------|------|
| Decks | One per module plus a course introduction, built from `scripts/new_content/` into `decks/pptx_new/` |
| Footer | `© 2026 by Innovation In Software Corporation` |
| Official exercises | Numbered *M.N* in slide order; worksheet in `labs/day-0N/exercises/`, answer key in `exercises/solution/` |
| Day labs | Lab 1–7, each the last official slide of its module; guide `labs/day-0N/labN/LAB-N-GUIDE.md`, solution in `labN/solution/` |
| Practice exercises | Unnumbered in-slide activities; answers in `labs/practice-exercises/module-0N-README.md` |
| Sample data | Every value and result matches a fresh `datasets/training_store/load.js`; passwords only as prompts or `<password>` |

---

## Prerequisites for authors

- [Node.js](https://nodejs.org/) for `npx @marp-team/marp-cli`
- Python 3 with PyYAML: `pip install pyyaml`
- Cursor or VS Code with the [Marp extension](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode)
- MongoDB Community (local) or Atlas (cloud) for lab verification
