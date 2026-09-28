# Exercise 1.1 — solution (instructor)

**Module 1** · Day 1 · Checkpoint A  
**Type:** design discussion · **Do not hand this sheet to participants.**

Worksheet: [`../exercise-1.1-choose-the-data-model.md`](../exercise-1.1-choose-the-data-model.md) · Deck slide 43

## Running it

Twelve minutes of pair work, then a three-minute debrief. Reveal the solution column only after groups share their answers. No MongoDB is needed.

## Task 1 — Primary structure of each model

| Model | Primary structure | What it is fast at |
| --- | --- | --- |
| Relational | Tables with a fixed schema | Integrity, joins and transactions across related rows |
| Document | JSON-like (BSON) documents | Flexible, application-shaped records read as a whole object |
| Key-value | A key mapped to an opaque value | Extremely fast lookup by an exact key |
| Column-family | Wide rows grouped by row key, variable columns | Huge distributed write volumes |
| Graph | Nodes and relationships (edges) | Traversing relationships many hops deep |

## Tasks 2 and 3 — Solution

| Workload | Recommended model | Justification (access pattern) | A workable alternative |
| --- | --- | --- | --- |
| A. Online shopping sessions | **Key-value** | Session data is read and written by one exact key, the session ID. | Document, if the session holds a rich cart the app queries by field |
| B. Product catalog | **Document** | Products have different attributes per category and each product is read as one object. | Relational with an attribute table (many joins) |
| C. Social recommendations | **Graph** | The core query walks relationships between users ("friends of friends who bought…"). | Document with references, but multi-hop traversal becomes slow and complex |
| D. Banking ledger | **Relational** | Strongly structured transactions that need strict consistency and integrity across entities. | Document with multi-document transactions — possible, but relational is simpler here |
| E. Sensor platform | **Column-family** or a specialized time-series platform | Very large volumes of distributed time-series writes. | Document database with time-series collections |
| F. Content management | **Document** | Articles have nested and optional sections that vary per article. | Relational with many optional tables |

Slide summary: A key-value · B document · C graph · D relational · E column-family or time-series · F document.

## Task 4 — What to listen for

- Each justification should name the access pattern: **lookup by key, varied attributes, relationship traversal, strict consistency, or write volume**. Product names alone ("use Redis", "use Neo4j") don't count.
- Common controversial rows:
  - **E** — column-family and a time-series platform are both correct. MongoDB time-series collections also work; the answer depends on write volume and distribution.
  - **D** — some learners say "MongoDB has transactions". True, but when most work spans many strictly structured entities, relational is usually simpler.
  - **A** — a document store also works; key-value wins because the only access is by session ID.

## Debrief points

- More than one technology may be technically possible. Start from access patterns, not popularity.
- Relational is on the list on purpose: for some workloads it is still the best choice. NoSQL means "Not Only SQL".
- The justification matters more than the product name.
