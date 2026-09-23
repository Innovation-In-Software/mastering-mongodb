# Exercise 1.1 — Choose the Appropriate Data Model

**Module 1** (Introduction to NoSQL Databases) · Day 1 · **Checkpoint A**  
**Time:** 15 min (12 min pair work + 3 min debrief) · **Type:** design discussion · **Difficulty:** Beginner

**Deck:** `decks/pptx_new/MongoDB_Module01_Introduction_to_NoSQL_Databases.pptx` — slide 43, "Exercise 1.1 — Choose the Appropriate Data Model"

## Purpose

Match workloads to models, and justify each one. You pick a starting model for six application workloads and explain each choice from the **access pattern**, not from a product name or from popularity.

## Prerequisites

- Module 1, Part 2 (the four NoSQL models and the "All five models side by side" comparison)
- Paper, a notes file, or the table at the end of this sheet
- You do **not** need MongoDB running for this exercise

## Scenario

Pick one starting model for each workload. The five models you may choose from are **relational, document, key-value, column-family or graph**.

| Workload | Key requirement |
| --- | --- |
| A. Online shopping sessions | Retrieve session data by a unique session ID |
| B. Product catalog | Store products with different attributes |
| C. Social recommendations | Traverse relationships between users |
| D. Banking ledger | Preserve strongly structured financial transactions |
| E. Sensor platform | Accept large volumes of distributed time-series writes |
| F. Content management | Store articles containing nested and optional sections |

Work in pairs or small groups.

## Tasks

### Task 1 — Name each model's primary structure

For each of the five models, write its primary structure (how it stores data) and one sentence on what it is fast at.

| Model | Primary structure | What it is fast at |
| --- | --- | --- |
| Relational | | |
| Document | | |
| Key-value | | |
| Column-family | | |
| Graph | | |

### Task 2 — Classify A–C with a one-line reason

For workloads A, B and C, pick one starting model and write a one-line justification. The justification must name the access pattern (for example: lookup by key, varied attributes, relationship traversal).

### Task 3 — Classify D–F the same way

Repeat for D, E and F. For at least one row, note another model that could also work and say why your first choice still fits.

### Task 4 — Defend one controversial row to the class

Choose the row your group argued about most. Be ready to defend it — or revise it — in the debrief using the workload requirements: access pattern, consistency, relationships and scale.

## Deliverable

| Workload | Selected model | Justification (name the access pattern) |
| --- | --- | --- |
| A. Online shopping sessions | | |
| B. Product catalog | | |
| C. Social recommendations | | |
| D. Banking ledger | | |
| E. Sensor platform | | |
| F. Content management | | |

## Expected outcome

- All six workloads have a selected model.
- Every reason names an access pattern, not only a product.
- At least one row was discussed against an alternative model.

The instructor reveals the solution only after groups share their answers.

## Success criteria

- [ ] Task 1 table names the structure of all five models
- [ ] All six workloads have a selected model and a one-line justification
- [ ] Every justification names an access pattern
- [ ] One controversial row is ready to defend in the debrief
