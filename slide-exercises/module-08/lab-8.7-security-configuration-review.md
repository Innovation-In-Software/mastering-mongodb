# Lab 8.7: Security Configuration Review

**Module 8:** MongoDB Best Practices, Security, and Troubleshooting  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 8)  
**Time:** 25 min  
**Difficulty:** Beginner

**Objective:** Review a sanitized training configuration for network exposure, authentication, roles, TLS, credential storage, backup access, logging, and environment separation, then produce a prioritized remediation list.

---

## Environment basics (read this first)

**Demonstration environment:** Windows 10/11 · PowerShell in Cursor (``Ctrl+` ``) · `mongosh` connected to the training instance.

| Task | Windows | Where |
|------|---------|-------|
| Open folder | `Ctrl+K Ctrl+O` | File → Open Folder |
| Terminal | ``Ctrl+` `` → PowerShell | Bottom panel |
| MongoDB shell | `mongosh` | Same terminal |

**Prerequisite:** `training_store` is loaded from [`datasets/training_store/load.js`](../../datasets/training_store/load.js). Reload at the start of Day 3 if Day 2 writes remain.

```javascript
use training_store
```

**Scratch database:** Labs that change validation, users, or restored data use `training_store_ops` so `training_store` stays intact for later work.

**Small-data note:** Twelve products and seventeen orders will not produce dramatic wall-clock wins. Record **plan shape**, **examined vs returned**, and **correctness**, not stopwatch time.


---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Mark every finding

**Do this:** Read the fictional configuration in the worksheet below. List every unsafe item under network, identity, encryption, secrets, backup, logging, and environment.

**Expected result:** Findings include `bindIp: 0.0.0.0` with no auth, disabled security, shared `admin/admin`, mongodb:// without TLS, URI in source, open backup bucket, verbose logs with the URI, prod dump loaded in dev.

---

### Step 2 — Prioritize remediation

**Do this:** Write a P1 / P2 / P3 list with owners (role names, not classmates’ personal emails). P1 must be items that would stop a go-live.

**Expected result:** P1: enable auth, restrict bind/firewall, TLS, remove secrets from git, stop public backup. P2: least-privilege roles, log redaction, env separation. P3: audit log destinations, rotation cadence.

---

### Step 3 — Design roles only

**Do this:** Do **not** enable authentication on the shared class database. Write `createRole` / `createUser` sketches for `appUser` and `reportUser` using placeholder names only.

**Expected result:** appUser: readWrite on `training_store`. reportUser: read on `training_store`. Neither is root. No real passwords in the notes.

---

## Fictional configuration worksheet (sanitized)

Never copy this into a real deployment.

```yaml
net:
  bindIp: 0.0.0.0
  port: 27017
  tls:
    mode: disabled
security:
  authorization: disabled
# connection used by the app (committed to Git)
# mongodb://admin:admin@store.example.com:27017/training_store
backup:
  destination: s3://public-training-backups
  encryption: off
logging:
  logAppend: true
  verbosity: 2
# last night: mongodump of production restored onto the intern laptop
```

## Role sketches (placeholders only)

```javascript
// Do not run on the shared class instance unless the instructor says so.
db.createUser({
  user: "appUser",
  pwd: "REDACTED",
  roles: [ { role: "readWrite", db: "training_store" } ]
})
db.createUser({
  user: "reportUser",
  pwd: "REDACTED",
  roles: [ { role: "read", db: "training_store" } ]
})
```

## Success criteria

- [ ] Unsafe configuration items are listed by category
- [ ] P1 items would block production
- [ ] No real credentials are written down

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
