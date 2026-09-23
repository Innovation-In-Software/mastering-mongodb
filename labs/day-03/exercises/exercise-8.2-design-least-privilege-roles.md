# Exercise 8.2 — Design Least-Privilege Roles

**Module 8** (MongoDB Best Practices, Security, and Troubleshooting) · Day 3 · **Checkpoint B**  
**Time:** 20 min · **Type:** design (no commands run) · **Difficulty:** Beginner

**Deck:** `decks/pptx_new/MongoDB_Module08_Best_Practices_Security_and_Troubleshooting.pptx` — slide 46, "Exercise 8.2 — Design Least-Privilege Roles"

## Purpose

A permit / deny matrix for six identities. You decide what each identity that touches `training_store` may do — and what it must never do — so that a stolen credential can do as little damage as possible.

## Prerequisites

- Module 8, Part 3: "Principle of Least Privilege" and "Users and Roles — Sketched, Not Run"
- A notes file or the table at the end of this sheet

**This is a design exercise.** Don't enable authentication or create users on the shared class instance. If you sketch commands, use placeholder user names and `passwordPrompt()` — never type a real password into a script, a slide or a chat.

## Scenario

For each identity, list one **permitted** and one **prohibited** operation on `training_store` (collections: `customers`, `products`, `orders`, `reviews`).

1. Application service
2. Reporting service
3. Support engineer
4. Monitoring service
5. Backup service
6. Database administrator

## Tasks

### Task 1 — Fill the permit / deny matrix

For each of the six identities, write one operation it is permitted and one it is prohibited.

### Task 2 — Choose a role for each identity

Name a built-in role (for example `read`, `readWrite`, `clusterMonitor`, `backup`) or describe a custom role (which actions, on which collections).

### Task 3 — Explain why the app never uses clusterAdmin

Write two sentences on why the application must not connect as a cluster administrator — even in a training-like environment that might later become production.

### Task 4 — Use placeholder names only

Give each identity a placeholder user name. Passwords are written as `passwordPrompt()` or `<password>` — nothing else.

## Deliverable

| # | Identity | Placeholder user | Role (built-in or custom) | Permitted | Prohibited |
| --- | --- | --- | --- | --- | --- |
| 1 | Application service | | | | |
| 2 | Reporting service | | | | |
| 3 | Support engineer | | | | |
| 4 | Monitoring service | | | | |
| 5 | Backup service | | | | |
| 6 | Database administrator | | | | |

Task 3 — why the app never uses clusterAdmin:

> 

## Expected outcome

- Six identities, each with a permit and a deny example.
- The application is not given `clusterAdmin` or any user-administration role.
- Reporting is read-only.
- No real password appears anywhere.

The instructor reveals the solution only after the debrief.

## Success criteria

- [ ] All six rows have a role, a permitted and a prohibited operation
- [ ] The application gets `readWrite` on `training_store` only
- [ ] Reporting is read-only
- [ ] The DBA is a separate identity the application never uses
- [ ] Only placeholder names and `passwordPrompt()` / `<password>` are used
