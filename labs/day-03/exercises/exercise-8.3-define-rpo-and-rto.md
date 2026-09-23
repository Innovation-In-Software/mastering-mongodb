# Exercise 8.3 — Define RPO and RTO

**Module 8** (MongoDB Best Practices, Security, and Troubleshooting) · Day 3 · **Checkpoint C**  
**Time:** 15 min · **Type:** design · **Difficulty:** Beginner

**Deck:** `decks/pptx_new/MongoDB_Module08_Best_Practices_Security_and_Troubleshooting.pptx` — slide 47, "Exercise 8.3 — Define RPO and RTO"

## Purpose

Recovery targets for each part of the store. You set a Recovery Point Objective (how much data you may lose) and a Recovery Time Objective (how long you may be down) for each data set, choose a backup frequency that can meet each RPO, and describe how you would **prove** an orders restore.

## Prerequisites

- Module 8, Part 4: "Replication vs. Backup", "Recovery Point and Recovery Time Objectives" (the 10:00 / 10:15 / 10:45 timeline) and "Restore Testing"
- A notes file or the tables at the end of this sheet
- You do **not** need to run anything. Lab 7, Step 4 performs a real dump and restore.

## Scenario

Treat `training_store` as a **small retailer, not a global bank**.

Data sets to plan:

- product catalog (`products`)
- customer profiles (`customers`)
- orders (`orders`)
- payments (in `training_store` the payment state is `orders.paymentStatus` — there is no separate payments collection)
- reviews (`reviews`)

Reminder from the slide: **RPO** looks back from the failure — the data at risk since the last recoverable point. **RTO** looks forward — the time until service is restored. Both are measured in **time**.

## Tasks

### Task 1 — Write RPO and RTO for each data set

Give each data set an RPO and an RTO as time quantities (minutes or hours), with a one-line business reason.

### Task 2 — Pick a backup frequency that meets each RPO

For each data set, name how often you would back it up (or which method — for example snapshots plus point-in-time recovery) so the RPO can actually be met.

### Task 3 — Describe how you would prove an orders restore

Write the checks you would run after restoring `orders` into an isolated database, so you know the restore worked — not only that the backup job succeeded.

## Deliverable

| Data set | RPO | RTO | Backup frequency / method | Reason |
| --- | --- | --- | --- | --- |
| Product catalog | | | | |
| Customer profiles | | | | |
| Orders | | | | |
| Payments | | | | |
| Reviews | | | | |

Proving an orders restore (Task 3):

1. 
2. 
3. 
4. 

## Expected outcome

- Every RPO and RTO is a time quantity.
- Orders and payments are stricter than reviews.
- The restore proof checks data **and** access, not only the backup job.

The instructor reveals the solution only after the debrief.

## Success criteria

- [ ] RPO and RTO are defined as time quantities for all five data sets
- [ ] Orders and payments have tighter targets than reviews
- [ ] Each backup frequency can actually meet its RPO
- [ ] The restore proof includes counts, a sample order, indexes and an application read
