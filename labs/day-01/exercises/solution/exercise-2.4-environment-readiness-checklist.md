# Exercise 2.4 — solution (instructor)

**Module 2** · Day 1 · Checkpoint D  
**Type:** verification checklist · **Do not hand this sheet to participants.**

Worksheet: [`../exercise-2.4-environment-readiness-checklist.md`](../exercise-2.4-environment-readiness-checklist.md) · Deck slide 47 · Evidence comes from [Lab 1](../../lab1/LAB-1-GUIDE.md) (slide 48)

## Running it

Introduce the sheet on slide 47, then run Lab 1. Learners complete it during or right after Lab 1. There is no single "answer" — a correct checklist is one that matches what the learner actually observed.

## What to record

- Path: local, container, managed cloud or instructor-provided.
- Hostname or cluster name, and the port if it isn't 27017. Local default: `localhost:27017`.
- **No** password and **no** full connection string on the page.

## Evidence for each row

| Check | A pass means the learner saw… | Lab 1 step |
| --- | --- | --- |
| MongoDB installed or provisioned | Path A: MSI/brew/package installed. Path B: Atlas cluster exists. Path C: URI received securely. | 2 |
| Server or cluster available | `Get-Service MongoDB` → `Running`, or `Test-NetConnection localhost -Port 27017` → `TcpTestSucceeded : True`; Atlas shows the cluster as available. | 3 |
| `mongosh` available | `mongosh --version` prints a version (for example `2.x.x`). | 3 |
| Compass available (if required) | Compass launches and connects. | 10 |
| Connection string stored securely | Password manager, instructor handout or environment variable — not a shared file. | 2 |
| Credentials available | The learner can authenticate (only relevant for Paths B and C, or a local server with access control on). | 4 |
| Network access configured | Path B: current IP on the Atlas IP access list (not `0.0.0.0/0`). Path C: on the allowed network. Path A: n/a (localhost). | 2 |
| Ping returns `ok: 1` | `{ ok: 1 }` from `db.runCommand({ ping: 1 })`. | 5 |
| Test insert successful | `{ acknowledged: true, insertedId: ObjectId('…') }` | 7 |
| Test read successful | `findOne({ status: "READY" })` returns the document with `_id` and `checkedAt: ISODate('…')`. | 7 |

## Gaps: symptom → layer → next check

| Symptom | Layer | Next check |
| --- | --- | --- |
| Connection refused on `localhost:27017` | Process | `Get-Service MongoDB`; start it as Administrator; read the log if it won't start |
| Server-selection timeout (Atlas) | Network | Add the current IP to the Atlas access list; check the firewall / VPN |
| Authentication failed | Credentials | Retry with the known-good user; check `authSource`; percent-encode the password |
| Insert returns "not authorized" | Permission | The user needs `readWrite` on `training_store` |
| Compass won't connect but `mongosh` does | Client | Same URI? Password typed in the password field? |

## What you want to hear

- A learner who couldn't open Compass leaves that row unticked and writes the symptom. That is a **good** checklist.
- A checklist with every box ticked but no ping output seen is not acceptable — ask to see the terminal.
