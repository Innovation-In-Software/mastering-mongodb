# Exercise 2.4 — Environment Readiness Checklist

**Module 2** (Installation and Setup) · Day 1 · **Checkpoint D**  
**Time:** 10 min · **Type:** verification checklist · **Difficulty:** Beginner

**Deck:** `decks/pptx_new/MongoDB_Module02_Installation_and_Setup.pptx` — slide 47, "Exercise 2.4 — Environment Readiness Checklist"

## Purpose

Tick only what you have seen. The checklist confirms that MongoDB, the client tools, authentication and a write-and-read test are ready before Module 3.

**When:** the instructor introduces this sheet just before [Lab 1 — Install, Connect and Verify](../lab1/LAB-1-GUIDE.md) (the next slide). Fill it in **during or right after Lab 1**, because it records what Lab 1 proves. Mark anything you could not prove as unresolved — do not invent a pass.

## Prerequisites

- Lab 1 open in another window
- PowerShell (Windows) or a terminal (macOS/Linux) with `mongosh`
- Do **not** paste real passwords or full connection strings into this checklist, chat or screenshots

## Scenario

Fill it in during or right after Lab 1. No passwords on the page.

## Tasks

### Task 1 — Record your path, host and port

Write down (without secrets) whether you use **local, container, managed cloud, or an instructor-provided** instance. Note the hostname or cluster name, and the port if it is not `27017`.

### Task 2 — Confirm `mongosh --version` and Compass

```powershell
mongosh --version
```

The version prints. If the instructor requires Compass, confirm it launches. Confirm you know where your connection string is stored (password manager, instructor handout or environment variable) — without displaying the password.

### Task 3 — Tick ping, insert and read — if seen

Tick each only if you saw the result in Lab 1:

- `db.runCommand({ ping: 1 })` returned `ok: 1` (Lab 1 Step 5)
- `insertOne` into `training_store.environment_check` was acknowledged (Lab 1 Step 7)
- `findOne({ status: "READY" })` returned the document (Lab 1 Step 7)

### Task 4 — List each gap: symptom, layer, next step

For every unticked item, write the symptom, the likely layer (**process, network, credentials or permission**) and the next check. [Exercise 2.3](exercise-2.3-diagnose-connection-failures.md) gives the first check for each common error. Report problems to the instructor without exposing credentials.

## Deliverable

**Deployment path:** local / container / managed cloud / instructor-provided (circle one)  
**Host or cluster name (no password):** ______________________ **Port (if not 27017):** ______

| Check | Pass? | Notes (no secrets) |
| --- | --- | --- |
| MongoDB installed or provisioned | | |
| Server or cluster available | | |
| `mongosh` available (`mongosh --version`) | | |
| Compass available (if required) | | |
| Connection string stored securely | | |
| Credentials available (not written here) | | |
| Network access configured | | |
| Ping returns `ok: 1` | | |
| Test insert successful | | |
| Test read successful | | |

The slide groups a few of these rows: mongosh and Compass share a line, credentials sit with the stored URI, and insert and read share a line.

**Unresolved problems** (symptom · likely layer · next check):

1.
2.

## Expected outcome

- Path recorded, no secrets.
- Only observed boxes ticked.
- Every gap has a next step.
- Ready for Module 3.

## Success criteria

- [ ] Deployment path is recorded without passwords
- [ ] Ping, insert and read are each ticked only if observed
- [ ] Every unresolved item has a next diagnostic step
- [ ] No real connection string was pasted into chat, slides or the checklist

## Next

Bring this checklist, your working connection and your Exercise 2.1 table to Module 3. Anyone with an unresolved item should see the instructor before Module 3's first lab.
