# Exercise 7.1 — Replication or Sharding?

**Module 7** (Introduction to Replication and Sharding) · Day 3 · **Checkpoint A**  
**Time:** 10 min (7 min pair work + 3 min debrief) · **Type:** design discussion · **Difficulty:** Beginner

**Deck:** `decks/pptx_new/MongoDB_Module07_Introduction_to_Replication_and_Sharding.pptx` — slide 45, "Exercise 7.1 — Replication or Sharding?"

## Purpose

Match each requirement to its mechanism. Replication keeps copies of the same data so the database stays available; sharding splits data across servers so it can grow. You decide which one each requirement needs — or whether it needs neither yet.

## Prerequisites

- Module 7, Part 1 ("Replication versus Sharding") and the "Deployment Decision Framework" slide
- Paper or a notes file
- You do **not** need MongoDB running. You may look at `training_store` or `rs.status()` to test an idea, but the reasoning is the deliverable.

## Scenario

For each requirement, write **Replication**, **Sharding**, **Both** or **Neither yet**.

| # | Requirement |
| --- | --- |
| 1 | Survive one server failure |
| 2 | Increase total data capacity |
| 3 | Elect a replacement primary automatically |
| 4 | Distribute write load |
| 5 | A local development database |
| 6 | Production availability + scale |

Work in pairs.

## Tasks

### Task 1 — Classify requirements 1–3

Write the mechanism for requirements 1, 2 and 3, with a one-line reason each.

### Task 2 — Classify requirements 4–6

Write the mechanism for requirements 4, 5 and 6, with a one-line reason each. For 6, say how the two mechanisms fit together.

### Task 3 — Explain why secondaries add no capacity

In two sentences, explain why copying data to more secondaries does **not** increase the total storage capacity for the application's data set.

### Task 4 — Compare with Lab 6: last week's delete

Day 3 Lab 6, Step 1, adds one more row: *recover an order deleted last week*. Which mechanism answers it — replication, sharding, both, or something else?

## Deliverable

| # | Requirement | Mechanism | One-line reason |
| --- | --- | --- | --- |
| 1 | Survive one server failure | | |
| 2 | Increase total data capacity | | |
| 3 | Elect a replacement primary | | |
| 4 | Distribute write load | | |
| 5 | A local development database | | |
| 6 | Production availability + scale | | |
| Lab 6 | Recover an order deleted last week | | |

Task 3 (two sentences):

## Expected outcome

- All six requirements have a mechanism and a reason.
- Local development is not forced into a replica set or a sharded cluster.
- Capacity is not confused with redundancy.

The instructor reveals the solution only after groups share their answers.

## Success criteria

- [ ] Six classifications match the intended mechanisms
- [ ] Local development is not forced into a replica set or shard
- [ ] Capacity is not confused with redundancy
- [ ] The Lab 6 row is answered with something that actually recovers deleted data
