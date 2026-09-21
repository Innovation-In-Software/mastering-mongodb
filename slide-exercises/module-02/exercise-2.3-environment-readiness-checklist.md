# Exercise 2.3: Complete the Environment Readiness Checklist

**Module 2:** Installation and Setup  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 2, Lesson 2.5)  
**Time:** 10 min  
**Difficulty:** Beginner

**Objective:** Confirm that MongoDB, client tools, authentication, and a write-and-read test are ready before Module 3.

Complete this checklist during or immediately after [Exercise 2.5](exercise-2.5-install-connect-and-verify.md). Mark any item you cannot prove as unresolved — do not invent a pass.

---

## Environment basics (read this first)

**Demonstration environment:** Windows 10/11 · PowerShell in Cursor (``Ctrl+` ``) · `mongosh` connected to the training instance.

| Task | Windows | Where |
|------|---------|-------|
| Terminal | ``Ctrl+` `` → PowerShell | Bottom panel |
| MongoDB shell | `mongosh` | Same terminal |
| Compass | Desktop app | If the instructor requires it |

Do **not** paste real passwords into the checklist, chat, or screenshots.

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Record environment details

**Do this:** Write down (without secrets) whether you are using local, container, managed cloud, or an instructor-provided instance. Note hostname or cluster name and port if it is not the default `27017`.

**Expected result:** You can state your deployment path and how you reach the server, with no password on the page.

---

### Step 2 — Confirm clients and connection information

**Do this:** Check that `mongosh` is available (`mongosh --version`). If Compass is required, confirm it launches. Confirm you have a connection string stored securely (password manager, instructor handout, or environment variable) — not in a shared slide.

**Expected result:** Shell version prints. Compass opens if required. You know where the URI lives without displaying the password.

---

### Step 3 — Confirm ping, write, and read

**Do this:** In `mongosh`, run `db.runCommand({ ping: 1 })`. Then confirm you can insert and retrieve a document in `training_store` (Exercise 2.5 covers the commands). Tick ping, insert, and read only if you saw the results.

**Expected result:** Ping contains `ok: 1`. A test document can be inserted and found. You did not tick a box you did not prove.

---

### Step 4 — List unresolved problems

**Do this:** For any unchecked item, write the symptom, the likely layer (process, network, credentials, or permission), and what you will try next. Report problems to the instructor without exposing credentials.

**Expected result:** Either every required box is checked, or every gap has a next diagnostic step.

---

## Deliverable

| Check | Pass? | Notes (no secrets) |
|-------|-------|--------------------|
| MongoDB installed or provisioned | | |
| Server or cluster available | | |
| `mongosh` available | | |
| Compass available (if required) | | |
| Connection string stored securely | | |
| Credentials available (not written here) | | |
| Network access configured | | |
| Ping returns `ok: 1` | | |
| Test insert successful | | |
| Test read successful | | |

Unresolved problems:

1.
2.

---

## Success criteria

- [ ] Deployment path is recorded without passwords
- [ ] Ping, insert, and read are each marked only if observed
- [ ] Unresolved items have a next diagnostic step
- [ ] No real connection string was pasted into chat, slides, or the checklist

---

## Related files

- Hands-on lab: [`exercise-2.5-install-connect-and-verify.md`](exercise-2.5-install-connect-and-verify.md)
- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
