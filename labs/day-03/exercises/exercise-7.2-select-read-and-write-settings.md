# Exercise 7.2 — Select Read and Write Settings

**Module 7** (Introduction to Replication and Sharding) · Day 3 · **Checkpoint B**  
**Time:** 20 min · **Type:** design discussion · **Difficulty:** Intermediate

**Deck:** `decks/pptx_new/MongoDB_Module07_Introduction_to_Replication_and_Sharding.pptx` — slide 46, "Exercise 7.2 — Select Read and Write Settings"

## Purpose

Choose settings per business operation. For each operation you pick a **read preference** (which member serves the read), a **read concern** (which data the read may return) and a **write concern** (how many members must acknowledge a write), and you say how much staleness you accept.

## Prerequisites

- Module 7, Part 3: "Read Preferences", "Write Concern", "Read Concern", "The Three Settings on training_store", "Replication Lag" and "Rollback"
- The practice exercise "What Did the Customer See?" (slide 25)
- Paper or a notes file. You do **not** need to run anything; do **not** update shared `training_store` data.

## Reference: the options

| Setting | Values you may use |
| --- | --- |
| Read preference | `primary`, `primaryPreferred`, `secondary`, `secondaryPreferred`, `nearest` |
| Read concern | `local`, `available`, `majority`, `snapshot` (inside a transaction) |
| Write concern | `w: 0`, `w: 1`, `w: "majority"` (optionally `j: true` and a `wtimeout`) |

The deck's `training_store` examples: confirming the payment of order **O6401** (Luis Romero, customer C204, `paymentStatus: "PENDING"`, total 2945.98) with `w: "majority"`; reading `paymentStatus: "PAID"` orders with `readConcern("majority")`; counting `fulfillmentStatus: "SHIPPED"` orders from a `secondaryPreferred` connection.

## Scenario

For each operation choose a read preference, a read concern and a write concern.

1. Payment confirmation
2. Financial reconciliation
3. Product-catalog browsing
4. Customer order status
5. Operational reporting
6. Noncritical analytics

## Tasks

### Task 1 — Set the two money paths

Fill in the three settings for **payment confirmation** and **financial reconciliation**.

### Task 2 — State what you refuse to trade away

For the two money paths, write one sentence each on what you will **not** give up (freshness, durability, or both) and why.

### Task 3 — Set catalog, status and reporting

Fill in the settings for **product-catalog browsing**, **customer order status**, **operational reporting** and **noncritical analytics**. If an operation only reads, write "n/a — read only" for the write concern and say what the related writes use.

### Task 4 — One sentence on staleness for each

For every operation, write one sentence: how stale may the answer be, and what happens if it is?

## Deliverable

| Operation | Read preference | Read concern | Write concern | Staleness accepted (one sentence) |
| --- | --- | --- | --- | --- |
| Payment confirmation | | | | |
| Financial reconciliation | | | | |
| Product-catalog browsing | | | | |
| Customer order status | | | | |
| Operational reporting | | | | |
| Noncritical analytics | | | | |

## Expected outcome

- Payment is never served from a lagging secondary as the truth.
- The three settings are not treated as interchangeable.
- Where staleness is accepted, it is accepted explicitly.

The instructor reveals the solution only after groups share their answers.

## Success criteria

- [ ] Both money paths use `w: "majority"` writes and fresh, majority-committed reads
- [ ] Read preference, read concern and write concern each answer a different question
- [ ] Every operation has a staleness sentence
- [ ] Analytics or reporting accepts staleness explicitly, not by accident
