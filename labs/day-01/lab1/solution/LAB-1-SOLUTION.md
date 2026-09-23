# Lab 1 solution — Install, Connect and Verify (instructor)

**Day 1** · Module 2 · Deck slide 48 (`OFFICIAL LAB`, 40 min)  
**Do not hand this sheet to participants.**

Participant guide: [`../LAB-1-GUIDE.md`](../LAB-1-GUIDE.md) · Checklist: [Exercise 2.4](../../exercises/exercise-2.4-environment-readiness-checklist.md) · Troubleshooting worksheet: [Exercise 2.3](../../exercises/exercise-2.3-diagnose-connection-failures.md)

## Running it

- Introduce Exercise 2.4 (slide 47), then start the lab. Learners tick the checklist as they go.
- Assign **one** path per learner before they start: A local, B Atlas, C instructor URI. Path C is the fastest recovery for a learner whose install fails — hand them a URI through the secure channel, never chat.
- Roughly: Steps 1–3 about 15 min (install is the long pole), Steps 4–9 about 15 min, Steps 10–11 about 10 min.
- Walk the room at Step 5: anyone without `{ ok: 1 }` goes straight to the Troubleshooting table.

## Expected output per step

Values in `…` differ per machine (ObjectIds, dates, sizes, versions).

### Steps 1–3 — Path, install, reachable

```text
PS> Get-Service MongoDB

Status   Name     DisplayName
------   ----     -----------
Running  MongoDB  MongoDB Server (MongoDB)

PS> Test-NetConnection localhost -Port 27017
...
TcpTestSucceeded : True

PS> mongosh --version
2.x.x
```

Path B: cluster shows as available; the learner's current IP is on the access list; a database user exists (username only on the checklist). Path C: URI received securely.

### Step 4 — Connect

```text
PS> mongosh "mongodb://localhost:27017"
Current Mongosh Log ID: …
Connecting to: mongodb://localhost:27017/?directConnection=true…
Using MongoDB: 8.0.x
Using Mongosh: 2.x.x
test>
```

Paths B/C: `Enter password:` prompt, then an `Atlas atlas-… [primary] test>` prompt (or similar).

### Step 5 — Ping and inspect

```text
test> db.runCommand({ ping: 1 })
{ ok: 1 }
test> db.version()
8.0.4            // example — yours may differ
test> db
test
test> show dbs
admin   40.00 KiB
config  60.00 KiB
local   40.00 KiB
test> show collections
                 // nothing
```

A brand-new server lists **only** `admin`, `config` and `local`. A server with `training_store` already loaded (instructor server, repeat run) also lists `training_store`. On Atlas, a restricted user may not see `admin`/`config`.

### Step 6 — `use` and `createCollection`

```text
test> use training_store
switched to db training_store
training_store> db.createCollection("environment_check")
{ ok: 1 }
training_store> show collections
environment_check
training_store> db
training_store
```

On a repeat run: `MongoServerError: Collection already exists` — expected; skip.

### Step 7 — Insert and read

```text
{ acknowledged: true, insertedId: ObjectId('…') }

{
  _id: ObjectId('…'),
  participant: 'Student',
  environment: 'training',
  shellConnected: true,
  status: 'READY',
  checkedAt: ISODate('…')
}
```

### Step 8 — insertMany, count, update

```text
{ acknowledged: true, insertedIds: { '0': ObjectId('…'), '1': ObjectId('…'), '2': ObjectId('…') } }
4
{ acknowledged: true, insertedId: null, matchedCount: 1, modifiedCount: 1, upsertedCount: 0 }
{ _id: ObjectId('…'), participant: '<learner name>', environment: 'training', shellConnected: true, status: 'READY', checkedAt: ISODate('…') }
```

Count is exactly **4** on a first run. Higher counts mean an earlier step was repeated — harmless, but if there are several READY documents, `updateOne` changes only the first match.

### Step 9 — `LAB1` probe

```text
// empty server only:
{ ok: 1 }                                         // createCollection("products")
{ acknowledged: true, insertedId: ObjectId('…') }
[ { _id: ObjectId('…'), sku: 'LAB1', name: 'Connectivity Probe', category: 'ACCESSORY', active: true } ]
{ acknowledged: true, insertedId: null, matchedCount: 1, modifiedCount: 1, upsertedCount: 0 }
{ acknowledged: true, deletedCount: 1 }
                                                  // final find: no output
```

Optional real-product read (loaded database only):

```text
{ name: 'MongoDB Fundamentals', price: Decimal128('59.99') }
```

### Step 10 — Compass

`training_store` → `environment_check` shows four documents: the READY document with the learner's name, and the three component documents. On an empty server `products` exists but is empty (`LAB1` was deleted).

### Step 11 — COMPLETE and reconnect

```text
{ acknowledged: true, insertedId: ObjectId('…') }
5
// after exit and reconnect:
{ _id: ObjectId('…'), module: 2, validation: 'COMPLETE', validatedAt: ISODate('…') }
admin           40.00 KiB
config          60.00 KiB
local           40.00 KiB
training_store  …
```

## End state (hand-off to Module 3)

| Collection | Documents (first run, empty server) |
| --- | --- |
| `training_store.environment_check` | 5 — READY (learner's name), 3 components, COMPLETE |
| `training_store.products` | 0 — created in Step 9; `LAB1` deleted |

`datasets/training_store/load.js` drops and reloads `customers`, `products`, `orders` and `reviews` (6 · 13 · 17 · 6) and leaves `environment_check` alone. Module 3's Lab 3.1 runs `createCollection("products")`; after Lab 1 it reports **Collection already exists**, which that lab already tells learners is fine.

## Common failures

| Symptom | Cause | Fix |
| --- | --- | --- |
| `connect ECONNREFUSED 127.0.0.1:27017` | Service stopped (MSI installed without "run as a service", or it failed to start) | `Start-Service MongoDB` as Administrator; if it fails, read `mongod.log` |
| Service starts then stops | `dbPath` missing or not writable; port 27017 in use (another `mongod` or a Docker container) | Fix `dbPath` in `mongod.cfg`; `Get-NetTCPConnection -LocalPort 27017` to find the other process |
| `mongosh` not recognized | Not installed, or PATH not refreshed | Install `mongosh`; open a new terminal |
| `mongod --version` not recognized (Windows) | `mongod.exe` is in the server's `bin` folder, not on PATH | Expected — check the service instead |
| Atlas: `Server selection timed out` | Current IP not on the access list; corporate firewall blocks 27017 | Add the current IP (never `0.0.0.0/0`); try another network or Path C |
| Atlas: `bad auth : authentication failed` | Atlas login used instead of the database user; wrong password | Use the database user; reset its password in Database Access |
| `querySrv ENOTFOUND` | Mistyped cluster host; DNS/VPN blocks SRV lookups | Copy the host again from Connect → Shell; try without the VPN |
| `not authorized on training_store to execute command { insert … }` | User has only `read`, or a role on another database | Grant `readWrite` on `training_store` |
| `Collection already exists` | Repeat run or loaded database | Expected; skip `createCollection` |
| `E11000 duplicate key error … sku: "LAB1"` | A previous run left `LAB1` on a database with the `sku_unique` index from `load.js` | `db.products.deleteOne({ sku: "LAB1" })`, then repeat Step 9 |
| Learner "fixed" it with `bindIp: 0.0.0.0` or `0.0.0.0/0` | Exposes the database to every network | Revert to `127.0.0.1` / the learner's own IP; restart the service |

## Practical challenge — answer

`developer_checks` receives the document; `findOne({ status: "READY" })` returns it with a generated `_id` and `checkedAt: ISODate('…')`; Compass shows it under `training_store` → `developer_checks`.
