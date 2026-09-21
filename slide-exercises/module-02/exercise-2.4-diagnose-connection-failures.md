# Exercise 2.4: Diagnose Connection Failures

**Module 2:** Installation and Setup  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 2, Lesson 2.5)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** For each common MongoDB connection failure, record the likely cause, the first diagnostic check, a relevant log or setting, a corrective action, and a verification command.

---

## Environment basics (read this first)

**Demonstration environment:** Classroom analysis. The instructor may project Demo 2.5. Do **not** break a working classroom cluster unless the instructor sets up a sandbox.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Table in this guide |
| Timer | 12 minutes work + 3 minutes debrief | Instructor clocks this |

Use placeholders, not real passwords.

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Diagnose ECONNREFUSED and authentication failure

**Do this:** For `ECONNREFUSED` and authentication failure, fill likely cause, first check, relevant log or setting, corrective action, and verification command.

**Expected result:** Refused connection points at a stopped server or wrong port. Authentication failure points at user, password, or authentication database — not at DNS.

---

### Step 2 — Diagnose timeout and DNS failure

**Do this:** Repeat for server-selection timeout and DNS lookup failure.

**Expected result:** Timeout points at firewall, routing, or network allowlist. DNS failure points at hostname or DNS, not at a missing role.

---

### Step 3 — Diagnose unauthorized command and invalid URI

**Do this:** Repeat for unauthorized operation and invalid connection-string format.

**Expected result:** Unauthorized means the user authenticated but lacks the role. Invalid URI means syntax, unencoded special characters, or the wrong scheme.

---

### Step 4 — Compare with the instructor solution

**Do this:** Share one case with the class. Confirm you would change **one** variable, then retest with the simplest client (`mongosh` ping).

**Expected result:** You can walk the troubleshooting sequence without guessing at three settings at once.

---

## Deliverable

| Case | Likely cause | First check | Log or setting | Corrective action | Verification |
|------|--------------|-------------|----------------|-------------------|--------------|
| 1 `ECONNREFUSED` | | | | | |
| 2 Authentication failed | | | | | |
| 3 Server-selection timeout | | | | | |
| 4 DNS lookup failure | | | | | |
| 5 Unauthorized command | | | | | |
| 6 Invalid URI format | | | | | |

## Instructor solution (after discussion)

| Case | Likely cause | First check | Log or setting | Corrective action | Verification |
|------|--------------|-------------|----------------|-------------------|--------------|
| 1 | Server stopped or wrong port | Is `mongod` running? Port 27017? | Service status; `net.port` | Start service or fix port in URI | `mongosh` then ping |
| 2 | Wrong user, password, or auth DB | Retry with known-good user | Auth failure lines in mongod log | Correct credentials / authSource | Authenticated `show dbs` |
| 3 | Firewall, routing, or allowlist | Can you reach host:port? | Cloud IP access list; local firewall | Allow client IP; check TLS | Ping from same client |
| 4 | Bad hostname or DNS | Resolve the hostname | URI host; DNS | Fix hostname; check VPN | Fresh `mongosh` URI |
| 5 | Role too weak | Which user and role? | User privileges | Grant required role | Retry the command |
| 6 | Syntax or encoding | Read the whole URI | Scheme, `@`, encoding | Repair URI; encode password | Connect with repaired URI |

**Verification command for connectivity:** `db.runCommand({ ping: 1 })` — expect `ok: 1`.

---

## Success criteria

- [ ] All six cases have a likely cause and a first check
- [ ] Timeout is not confused with connection refused
- [ ] Unauthorized is not confused with authentication failed
- [ ] You would change one variable and retest

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
