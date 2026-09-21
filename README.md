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

**Labs:** choose a deployment, interpret a URI, install or provision MongoDB, connect with `mongosh` and Compass · create and populate collections against the sample application dataset.

### Day 2 — Working with data (~6 hours)

The two skills used every day: retrieve and change documents, then reshape them through aggregation. Same sample dataset as Day 1.

| Time | Module | Title | Topics |
|------|--------|-------|--------|
| ~3 h (or 6–7 h full) | 4 | The MongoDB Query Language | `find` / `findOne`; comparison, logical, array, and update operators; projections; safe writes |
| ~3 h | 5 | The Aggregation Framework | Pipeline structure; `$match`, `$group`, `$project`, `$sort`, `$limit`; multi-stage analytics |

**Labs:** construct complex queries and perform data manipulations · build a multi-stage aggregation pipeline.

### Day 3 — Performance and production (~6 hours)

Make Day 2’s queries and pipelines fast, then cover how MongoDB stays available at scale and what to carry back to the team.

| Time | Module | Title | Topics |
|------|--------|-------|--------|
| ~2 h (or 3–3.5 h full) | 6 | Indexing and Query Performance | Create and manage indexes; ESR and prefixes; `explain()`; specialized types |
| ~2 h (or 3–3.5 h full) | 7 | Introduction to Replication and Sharding | Replica sets, elections, read/write guarantees; shards, keys, routing |
| ~2 h (or 3–3.5 h full) | 8 | MongoDB Best Practices, Security, and Troubleshooting | Modeling, queries, indexes, security, backup/restore, monitoring, troubleshooting, production-readiness checklist |

**Labs:** add indexes and read `explain` output on the Day 2 queries and pipeline · inspect a replica set (`rs.status()`) and reason about shard keys · production-readiness labs (validation, restore to an isolated database, runbooks). Time-box Module 6 to Labs 6.1–6.4 and 6.11, Module 7 to Lab 7.1 plus the challenge, and Module 8 to Labs 8.2, 8.3, 8.6, 8.9, and 8.11 when the afternoon is shared.

---

## Recommended folder structure

This course should follow the DrKaur instructor-led layout: one Marp deck, lab guides per module, and shared sample data. Scaffold from `D:\Current_work\drkaur-course-template` rather than inventing a parallel tree.

```text
MasteringMongoDB/
├── README.md                              # This file
├── Mastering_MongoDB_Course_Outline.docx  # Source outline (keep as reference)
├── FINAL_TABLE_OF_CONTENTS.md             # Master lesson/exercise index
├── COURSE-AUTHORING-GUIDE.md              # Copied from the course template
├── COURSE-CHEATSHEET.md                   # Operator and concept glossary by module
├── course.config.yaml                     # Course name, days, module list
├── diagram-prompt.md                      # Prompt for generating slide SVGs
│
├── slides/
│   ├── course-complete-marp-with-notes.md     # Single monolithic deck (do not split)
│   ├── course-complete-marp-with-notes.html   # Presenter export
│   ├── course-complete-speaker-notes.md       # Generated notes extract
│   └── assets/
│       ├── module-01/                     # NoSQL vs RDBMS, store types, architecture
│       ├── module-02/                     # Install / connect diagrams
│       ├── module-03/                     # Embed vs reference, document model
│       ├── module-04/                     # Query / operator visuals
│       ├── module-05/                     # Aggregation pipeline stages
│       ├── module-06/                     # Index selection / explain plans
│       ├── module-07/                     # Replica sets and sharding
│       └── module-08/                     # Ops / security checklist visuals
│
├── slide-exercises/                       # In-class lab guides (lab-first)
│   ├── module-01/
│   │   ├── exercise-1.1-choose-the-data-model.md
│   │   ├── exercise-1.2-rows-to-documents.md
│   │   └── exercise-1.3-explore-a-mongodb-dataset.md
│   ├── module-02/
│   │   ├── exercise-2.1-select-a-deployment-option.md
│   │   ├── exercise-2.2-interpret-a-connection-string.md
│   │   ├── exercise-2.3-environment-readiness-checklist.md
│   │   ├── exercise-2.4-diagnose-connection-failures.md
│   │   └── exercise-2.5-install-connect-and-verify.md
│   ├── module-03/
│   │   ├── exercise-3.1-identify-document-components.md
│   │   ├── exercise-3.2-discover-access-patterns.md
│   │   ├── exercise-3.3-embed-or-reference.md
│   │   ├── exercise-3.4-model-a-product-catalog.md
│   │   ├── exercise-3.5-model-an-order-document.md
│   │   ├── exercise-3.6-correct-schema-anti-patterns.md
│   │   ├── exercise-3.7-select-a-schema-pattern.md
│   │   ├── exercise-3.8-design-collection-validation.md
│   │   ├── exercise-3.9-support-ticket-challenge.md
│   │   ├── lab-3.1-create-the-sample-database.md
│   │   ├── lab-3.2-populate-products.md
│   │   ├── lab-3.3-populate-customers.md
│   │   ├── lab-3.4-populate-orders.md
│   │   ├── lab-3.5-query-nested-documents.md
│   │   ├── lab-3.6-add-collection-validation.md
│   │   └── lab-3.7-validate-the-data-model.md
│   ├── module-04/
│   │   └── exercise-4.1-queries-and-updates.md
│   ├── module-05/
│   │   └── exercise-5.1-aggregation-pipeline.md
│   ├── module-06/
│   │   ├── exercise-6.1-identify-candidate-indexes.md
│   │   ├── lab-6.1-establish-a-performance-baseline.md
│   │   └── … (12 exercises, 11 labs, practical challenge)
│   └── module-08/
│       ├── exercise-8.1-review-a-document-model.md
│       ├── lab-8.1-data-model-review-and-repair.md
│       └── … (14 exercises, 11 labs, practical challenge)
│
├── datasets/                              # Shared sample application data
│   ├── README.md                          # How to load catalogs / orders / users
│   └── training_store/
│       ├── README.md
│       └── load.js
│
├── sample-app/                            # Thin app used for "connect MongoDB"
│   └── README.md                          # Language + connection string only
│
└── scripts/                               # Deck maintenance (from the template)
    ├── themes/flat-gaia.css
    ├── course_config.py
    ├── exercise_meta.py                   # Register each Exercise M.N here
    ├── inject-lab-guide-links.py
    ├── sync-exercise-steps-to-slides.py
    └── generate-speaker-notes.py
```

### Why this layout

| Folder | Role |
|--------|------|
| `slides/` | One deck for all three days. Module openers use `<!-- _header: 'Module N — Title' -->`. |
| `slides/assets/module-NN/` | SVGs only; referenced as `<img src="assets/module-NN/file.svg" width="720">`. |
| `slide-exercises/module-NN/` | Lab guides named `exercise-M.N-slug.md`. Each must include `## Steps from the training slides`. |
| `datasets/` | One sample application dataset reused on Days 1–3 so modeling, queries, aggregation, and indexes stay consistent. |
| `sample-app/` | Small, language-agnostic connection demo for the “connect MongoDB to applications” objective. Keep it thin. |
| `scripts/` | Template maintenance pipeline. Do not invent a second build system. |

Module 7 includes replica-set inspection labs (Atlas URI) plus optional instructor-controlled failover and sharding labs. Module 1 now includes classification, a rows-to-document exercise, and a first `mongosh` exploration of `training_store`.

---

## Authoring order

1. Design index — [`FINAL_TABLE_OF_CONTENTS.md`](FINAL_TABLE_OF_CONTENTS.md) and [`course.config.yaml`](course.config.yaml).
2. Load `datasets/` and write lab guides in `slide-exercises/` **before** exercise slides.
3. Author the monolithic deck in `slides/course-complete-marp-with-notes.md`.
4. Register exercises in `scripts/exercise_meta.py`.
5. Run maintenance scripts, then export HTML with Marp CLI.

```powershell
python scripts/inject-lab-guide-links.py
python scripts/sync-exercise-steps-to-slides.py
python scripts/generate-speaker-notes.py

npx @marp-team/marp-cli slides/course-complete-marp-with-notes.md `
  --html --allow-local-files `
  --theme-set scripts/themes/flat-gaia.css `
  --no-stdin `
  -o slides/course-complete-marp-with-notes.html
```

To bootstrap the empty tree from the template (after this README is in place, copy it back if the scaffold overwrites it):

```powershell
cd D:\Current_work\drkaur-course-template
python scripts/scaffold_course.py `
  --name "Mastering MongoDB" `
  --slug "mastering-mongodb" `
  --days 3 `
  --modules 8 `
  --org "Innovation In Software"
```

The current working folder is `Innovation in Software\MasteringMongoDB`. Either scaffold here by pointing the script at this directory, or scaffold under `D:\Current_work\mastering-mongodb` and move the generated files in.

---

## Conventions

| Item | Rule |
|------|------|
| Deck | Single file: `slides/course-complete-marp-with-notes.md` |
| Theme | `flat-gaia` from `scripts/themes/flat-gaia.css` |
| Footer | `© 2026 by Innovation In Software Corporation` |
| Lab steps | `### Step N — Title` with **Do this:** and **Expected result:** |
| Exercise slides | Two steps per slide; link the lab guide on the first slide of each exercise |

---

## Prerequisites for authors

- [Node.js](https://nodejs.org/) for `npx @marp-team/marp-cli`
- Python 3 with PyYAML: `pip install pyyaml`
- Cursor or VS Code with the [Marp extension](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode)
- MongoDB Community (local) or Atlas (cloud) for lab verification
