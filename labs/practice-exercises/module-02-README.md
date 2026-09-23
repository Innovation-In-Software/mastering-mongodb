# Module 2 — Practice exercise solutions

**Deck:** `decks/pptx_new/MongoDB_Module02_Installation_and_Setup.pptx`  
**Story:** a learner's own MongoDB server and the `training_store` database (`datasets/training_store/load.js`)  
Attempt the slide activity first, then compare your answers here.

Official numbered checkpoints and lab for this module:
[Exercise 2.1](../day-01/exercises/exercise-2.1-select-a-deployment-option.md) ·
[Exercise 2.2](../day-01/exercises/exercise-2.2-interpret-a-connection-string.md) ·
[Exercise 2.3](../day-01/exercises/exercise-2.3-diagnose-connection-failures.md) ·
[Exercise 2.4](../day-01/exercises/exercise-2.4-environment-readiness-checklist.md) ·
[Lab 1](../day-01/lab1/LAB-1-GUIDE.md).

---

## Exercise: Is the Server Running?

**Slide 20** · **Time:** 5 minutes · **How to run:** individually for three minutes, then discuss. Ask for the layer first, before anyone suggests a fix.

### Scenario

A learner installed MongoDB on Windows. `mongosh` reports connection refused on `localhost:27017`.

```text
PS> Get-Service MongoDB

Status   Name     DisplayName
------   ----     -----------
Stopped  MongoDB  MongoDB Server (MongoDB)
```

### Tasks

1. Name the layer that failed.
2. Give the command that fixes it.
3. Say how you'll prove the fix.
4. Name a cause if it won't start.

### Solution

| Task | Answer |
| --- | --- |
| Layer | The **server process**: `mongod` is stopped, so nothing listens on port 27017. That is why `mongosh` gets connection refused rather than a timeout. |
| Fix | `Start-Service MongoDB`, in an **Administrator** PowerShell. |
| Proof | `mongosh`, then `db.runCommand({ ping: 1 })` → `{ ok: 1 }`. |
| If it won't start | Read the server log named by `systemLog.path`. Typical causes: a missing or unwritable `dbPath`, or port 27017 already in use by another process. |

### Why this is the answer

Connection refused usually means nothing is listening — check the server before the client. Reinstalling `mongosh` or editing the URI would change the wrong layer.

---

## Exercise: Build the Connection String

**Slide 29** · **Time:** 10 minutes · **How to run:** individually for five minutes, then compare in pairs. Collect one answer per learner on the board, without any password.

### Scenario

Three learners need to connect. Write the connection string or `mongosh` command for each one.

```text
A  Local server, default port
B  Local server, open training_store
C  Atlas: cluster0.example.mongodb.net
   as database user trainingUser
```

### Tasks

1. Write learner A's URI.
2. Add the database for learner B.
3. Write learner C's `mongosh` command.
4. Say where C's password goes.

### Solution

| Learner | Answer |
| --- | --- |
| A | `mongodb://localhost:27017` — also what `mongosh` uses with no arguments. |
| B | `mongodb://localhost:27017/training_store` — the database goes after the port. |
| C | `mongosh "mongodb+srv://cluster0.example.mongodb.net/" --username trainingUser` |
| C's password | Typed at the `Enter password:` prompt — never in the URI. In an application, it comes from an environment variable or a secret store, never from source code. |

C has **no port**: the SRV lookup supplies the members and ports, and TLS is on by default. `cluster0.example.mongodb.net` is a placeholder; a real host comes from Atlas **Connect → Shell**. In PowerShell the command can be split with a backtick; in bash, use a backslash.

### Why this is the answer

If you can write the connection string, you can place most connection errors: scheme, host, port, database and credentials each map to a layer.

---

## Exercise: Predict the Shell Output

**Slide 35** · **Time:** 5 minutes · **How to run:** two minutes to write predictions, then run the commands on the instructor screen, one at a time.

### Scenario

A brand-new local server. Nothing has been created yet.

```javascript
show dbs
use training_store
show dbs
db.environment_check.insertOne(
  { status: "READY" })
show dbs
show collections
```

### Tasks

1. Predict the first `show dbs`.
2. Say what `use` prints — and creates.
3. Predict `show dbs` after the insert.
4. Predict `show collections`.

### Solution

| Command | Output |
| --- | --- |
| First `show dbs` | `admin`, `config` and `local` only. |
| `use training_store` | `switched to db training_store` — but it creates **nothing** on disk. |
| Second `show dbs` | Unchanged: still `admin`, `config`, `local`. |
| `insertOne` | `{ acknowledged: true, insertedId: ObjectId('…') }` — creates the collection **and** the database together. |
| Third `show dbs` | `training_store` now appears (with `admin`, `config`, `local`). |
| `show collections` | `environment_check` |

### Why this is the answer

Databases and collections appear on the first write. Learners often think a typo in `use` created a new database; it didn't — nothing exists until the first write. Lab 1 creates `environment_check` explicitly with `createCollection`; this exercise shows the implicit way.
