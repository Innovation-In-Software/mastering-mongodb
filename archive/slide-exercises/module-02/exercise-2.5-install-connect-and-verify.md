# Exercise 2.5: Install, Connect, and Verify

**Module 2:** Installation and Setup  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 2, Lesson 2.6)  
**Time:** 40 min  
**Difficulty:** Beginner

**Objective:** Install or provision MongoDB, connect with `mongosh` and Compass, create `training_store`, and prove the environment with a write-and-read test.

**Paths:** The instructor will assign Path A (local), Path B (managed cloud), or Path C (instructor-provided URI). Complete **one** path in Step 2, then continue with the shared steps.

Complete [Exercise 2.3](exercise-2.3-environment-readiness-checklist.md) as you go. Do **not** paste real passwords into chat, slides, or screenshots.

---

## Environment basics (read this first)

**Demonstration environment:** Windows 10/11 · PowerShell in Cursor (``Ctrl+` ``)

| Task | Windows | Where |
|------|---------|-------|
| Open folder | `Ctrl+K Ctrl+O` | File → Open Folder |
| Terminal | ``Ctrl+` `` → PowerShell | Bottom panel |
| MongoDB shell | `mongosh` | Same terminal |
| Compass | Desktop app | Start menu |

Use placeholders in notes: `<connection-string>`, `<username>`. Store the real URI in a password manager or an environment variable.

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Choose your deployment path

**Do this:** Confirm with the instructor whether you will use Path A (local Community Edition), Path B (managed cloud / Atlas-style), or Path C (instructor-provided connection string). Write the path on your readiness checklist.

**Expected result:** You know which path you will complete. Neighbors may use a different path; the later `mongosh` commands are the same.

---

### Step 2 — Install or provision MongoDB

**Do this:** Complete only the path you chose.

**Path A — Local installation**

1. Confirm OS requirements using the instructor install sheet.
2. Install MongoDB Community (server). Note the configuration file location.
3. Start the MongoDB service.
4. Confirm service status and locate the server log.

**Path B — Managed cloud**

1. Sign in to the assigned project.
2. Create or open the training deployment.
3. Create a training database user (record username only here).
4. Configure approved network access (your current IP or the classroom range).
5. Copy the connection string and store it securely.

**Path C — Instructor-provided environment**

1. Obtain the assigned connection string and temporary credentials securely.
2. Confirm you are on an allowed network.
3. Do not share the URI in chat.

**Expected result:** A MongoDB server or cluster exists that you are allowed to use. You have not written a password into a shared file.

---

### Step 3 — Confirm the server is reachable

**Do this:** For Path A, confirm the MongoDB Windows service is Running (or that `mongod` is listening on `27017`). For Path B or C, confirm the portal or instructor shows the deployment as available. Record host and port (default `localhost:27017` for local).

**Expected result:** You can state that the server process or cluster is up, and you know the host and port you will put in the URI.

---

### Step 4 — Connect using `mongosh`

**Do this:** In PowerShell, connect with your URI. Local example:

```bash
mongosh "mongodb://localhost:27017"
```

Cloud-style example (placeholders only):

```bash
mongosh "<connection-string>"
```

**Expected result:** The shell prompt appears. Authentication succeeds if the URI includes credentials. You are not looking at a connection-refused error.

---

### Step 5 — Ping and inspect the environment

**Do this:** Run:

```javascript
db.runCommand({ ping: 1 })
db
show dbs
show collections
```

**Expected result:** Ping contains `ok: 1`. `db` prints the current database name (often `test` on a local default). `show dbs` lists databases you are allowed to see.

---

### Step 6 — Select `training_store` and create a collection

**Do this:** Run:

```javascript
use training_store
db.createCollection("environment_check")
show collections
db
```

**Expected result:** The prompt or `db` shows `training_store`. `show collections` includes `environment_check`.

---

### Step 7 — Insert and retrieve a test document

**Do this:** Run:

```javascript
db.environment_check.insertOne({
  participant: "Student",
  environment: "training",
  shellConnected: true,
  status: "READY",
  checkedAt: new Date()
})

db.environment_check.findOne({
  status: "READY"
})
```

**Expected result:** The insert is acknowledged and an `_id` is assigned. `findOne` returns the document, including `checkedAt` as a date.

---

### Step 8 — Insert multiple documents, count, and update

**Do this:** Run:

```javascript
db.environment_check.insertMany([
  { component: "MongoDB Server", available: true },
  { component: "MongoDB Shell", available: true },
  { component: "MongoDB Compass", available: true }
])

db.environment_check.countDocuments({})

db.environment_check.updateOne(
  { participant: "Student" },
  { $set: { participant: "Participant Name" } }
)

db.environment_check.findOne({ status: "READY" })
```

Replace `Participant Name` with your name.

**Expected result:** Count is at least 4. The READY document shows your name. Components for server, shell, and Compass are present.

---

### Step 9 — Connect with Compass and confirm the same data

**Do this:** Launch Compass, paste the same connection string (do not screenshot the password), connect, expand `training_store` → `environment_check`, and open the READY document. Switch between document views if offered.

**Expected result:** Compass shows the same collection and the same document you inserted from `mongosh`. Compass is a different interface, not a different database.

---

### Step 10 — Record environment validation

**Do this:** In `mongosh`, run:

```javascript
db.environment_check.insertOne({
  module: 2,
  validation: "COMPLETE",
  validatedAt: new Date()
})
```

Tick the remaining boxes on [Exercise 2.3](exercise-2.3-environment-readiness-checklist.md). If Compass or a write failed, leave those boxes unchecked and note the symptom.

**Expected result:** A COMPLETE validation document exists. The checklist matches what you actually observed. You can reconnect after closing the client.

---

## Success criteria

- [ ] Server or cluster is available on the assigned path
- [ ] `mongosh` connects and ping returns `ok: 1`
- [ ] `training_store.environment_check` exists
- [ ] At least one document was inserted and retrieved
- [ ] An update to the participant name is visible
- [ ] Compass shows the same document (if Compass is required)
- [ ] No real password was shared or committed

---

## Practical challenge (if time remains)

A new developer received a connection string but has not verified the environment.

1. Identify the URI components (no password on a shared screen).
2. Connect with `mongosh` and ping.
3. `use training_store` and `db.createCollection("developer_checks")`.
4. Insert:

```javascript
{
  developer: "New Developer",
  shellAccess: true,
  compassAccess: true,
  readAccess: true,
  writeAccess: true,
  status: "READY",
  checkedAt: new Date()
}
```

5. Retrieve the document, then locate the same document in Compass.

---

## Related files

- Readiness checklist: [`exercise-2.3-environment-readiness-checklist.md`](exercise-2.3-environment-readiness-checklist.md)
- Sample data (loaded in Module 3): [`datasets/training_store`](../../datasets/training_store)
- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
