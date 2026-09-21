# Exercise 8.7: Identify Security Risks

**Module 8:** MongoDB Best Practices, Security, and Troubleshooting  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 8)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Rank risks in a fictional environment with a public endpoint, shared admin account, plaintext connection string, no TLS, unprotected backups, and production data in development.

---

## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Capture answers in a notes file.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional |
| Timer | Instructor clocks this | — |

You may use `mongosh` to inspect `training_store`, but reasoning is the deliverable unless a step says otherwise. Do not enable authentication on a shared training instance unless the instructor provides a disposable environment.


---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Rank the six risks

**Do this:** Rank these from most urgent to least: public database endpoint; shared administrator account; plaintext URI in source control; no TLS; unprotected backups; production data copied to development. Give a one-line business impact for the top three.

**Expected result:** Typical top three: public endpoint (internet attack surface), no TLS (credential and data interception), secrets in source control (credential leak). Shared admin and prod-in-dev and open backups remain high.

---

### Step 2 — Propose mitigations

**Do this:** For each of the six, write one concrete control (network, identity, encryption, secret storage, or data handling).

**Expected result:** Private network + allowlist; named accounts + MFA/rotation; secret manager; TLS with validation; encrypted backups with access control; masked or synthetic non-prod data.

---

## Success criteria

- [ ] A ranked list exists
- [ ] Top risks include exposure and credential leakage
- [ ] Each risk has a mitigation

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
