# Exercise 2.1 — Select a Deployment Option

**Module 2** (Installation and Setup) · Day 1 · **Checkpoint A**  
**Time:** 10 min (8 min pair work + 2 min debrief) · **Type:** design discussion · **Difficulty:** Beginner

**Deck:** `decks/pptx_new/MongoDB_Module02_Installation_and_Setup.pptx` — slide 44, "Exercise 2.1 — Select a Deployment Option"

## Purpose

Match six scenarios to a deployment, with a risk. For each scenario you pick one place for MongoDB to run, justify it from the **constraint** (offline, disposable, shared, control, operations load or network), and name the main risk of that choice.

## Prerequisites

- Module 2, Part 1 (deployment options, local versus managed cloud, and the "Choosing a Deployment Option" decision flow)
- Paper, a notes file, or the table at the end of this sheet
- You do **not** need MongoDB running for this exercise

## Scenario

Pick one option — **local installation, self-managed server or VM, container, or managed cloud**. Justify it and name the main risk.

| # | Situation |
| --- | --- |
| 1 | A developer needs an offline learning environment. |
| 2 | A temporary automated-test environment must be created and removed quickly. |
| 3 | A distributed team needs access to a shared training database. |
| 4 | A regulated organization requires infrastructure under its direct control. |
| 5 | A startup wants a database without managing servers. |
| 6 | A classroom has restricted internet access. |

Work in pairs.

## Tasks

### Task 1 — Name one good fit for each option

For each of the four options, write one sentence on when it is a good fit.

| Option | A good fit when… |
| --- | --- |
| Local installation (Community Edition) | |
| Self-managed server or VM | |
| Container (Docker) | |
| Managed cloud (MongoDB Atlas) | |

### Task 2 — Classify scenarios 1–3

Pick one option for each scenario, write a one-line justification, and name the main risk. The justification must mention the constraint (internet, persistence, shared access…), not only a product name.

### Task 3 — Classify scenarios 4–6

Repeat for scenarios 4, 5 and 6.

### Task 4 — Defend one row against an alternative

Choose one row where another option could also work. Be ready to say why your first choice still fits, using training versus production, internet availability, operations load and control requirements.

## Deliverable

| # | Deployment option | Justification (name the constraint) | Main risk |
| --- | --- | --- | --- |
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |

## Expected outcome

- All six scenarios have a selected option, a justification and a main risk.
- Every justification names a constraint.
- At least one row was discussed against an alternative.

The instructor reveals the solution only after pairs share one controversial row.

## Success criteria

- [ ] Task 1 names one good fit for each of the four options
- [ ] All six scenarios have a selected option
- [ ] Each justification names a constraint (offline, disposable, shared, control, ops, network)
- [ ] Each row names a main risk
- [ ] One row is ready to defend against an alternative

## Next

[Exercise 2.2 — Interpret a Connection String](exercise-2.2-interpret-a-connection-string.md)
