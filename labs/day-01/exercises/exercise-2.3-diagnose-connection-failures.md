# Exercise 2.3 — Diagnose Connection Failures

**Module 2** (Installation and Setup) · Day 1 · **Checkpoint C**  
**Time:** 15 min (12 min work + 3 min debrief) · **Type:** troubleshooting analysis · **Difficulty:** Beginner

**Deck:** `decks/pptx_new/MongoDB_Module02_Installation_and_Setup.pptx` — slide 46, "Exercise 2.3 — Diagnose Connection Failures"

## Purpose

Six failures, one layer at a time. For each common connection failure you record the likely cause, the first check, a relevant log or setting, the fix, and the command that verifies it.

## Prerequisites

- Module 2, Part 5 ("Common Connection Problems" and "A Troubleshooting Workflow": process → port and bindIp → credentials → network and TLS)
- Paper, a notes file, or the table at the end of this sheet
- Classroom analysis: do **not** break a working classroom cluster unless the instructor has set up a sandbox. Use placeholders, never real passwords.

You will use this table again if a step of [Lab 1](../lab1/LAB-1-GUIDE.md) fails.

## Scenario

For each case: likely cause, first check, log or setting, fix and the command that verifies it.

| # | Error the learner sees |
| --- | --- |
| 1 | `ECONNREFUSED` |
| 2 | Authentication failed |
| 3 | Server-selection timeout |
| 4 | DNS lookup failure |
| 5 | Unauthorized command |
| 6 | Invalid URI format |

## Tasks

### Task 1 — Diagnose cases 1 and 2

Fill the row for `ECONNREFUSED` and for authentication failure.

### Task 2 — Diagnose cases 3 and 4

Repeat for server-selection timeout and DNS lookup failure. Make sure your timeout answer is different from your refused answer.

### Task 3 — Diagnose cases 5 and 6

Repeat for unauthorized command and invalid URI format. Make sure your unauthorized answer is different from your authentication-failed answer.

### Task 4 — Share one case: change one thing, retest

Pick one case to present. Say the **one** variable you would change, then how you retest with the simplest client:

```javascript
db.runCommand({ ping: 1 })
```

## Deliverable

| Case | Likely cause | First check | Log or setting | Fix | Verification |
| --- | --- | --- | --- | --- | --- |
| 1 `ECONNREFUSED` | | | | | |
| 2 Authentication failed | | | | | |
| 3 Server-selection timeout | | | | | |
| 4 DNS lookup failure | | | | | |
| 5 Unauthorized command | | | | | |
| 6 Invalid URI format | | | | | |

## Expected outcome

- Every case names a layer: process, port/bindIp, credentials, permission, network/TLS, or URI syntax.
- Timeout is not confused with refused; unauthorized is not confused with unauthenticated.
- The verification is a ping that returns `ok: 1` (plus the failed command, where relevant).

The instructor reveals the solution after the debrief.

## Success criteria

- [ ] All six cases have a likely cause and a first check
- [ ] Timeout is not confused with connection refused
- [ ] Unauthorized is not confused with authentication failed
- [ ] You would change one variable and retest with a ping

## Next

[Exercise 2.4 — Environment Readiness Checklist](exercise-2.4-environment-readiness-checklist.md), filled in during Lab 1
