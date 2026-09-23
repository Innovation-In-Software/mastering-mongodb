# Lab 1: Install, Connect, and Verify

**Day 1 · Module 2**  
**PPT:** `decks/pptx/MongoDB_Day1_Run_MongoDB_and_Model_Documents.pptx` — Module 2 section (Practical Lab)  
**Time:** 40 min  
**Difficulty:** Beginner

**Objective:** Provision MongoDB, connect with `mongosh` (and Compass if installed), create `training_store`, and prove the environment with ping, insert, find, update, and delete.

**Detailed guide:** [`slide-exercises/module-02/exercise-2.5-install-connect-and-verify.md`](../slide-exercises/module-02/exercise-2.5-install-connect-and-verify.md)

---

## Environment basics

**Demonstration environment:** Windows 10/11 · PowerShell in Cursor (``Ctrl+` ``)

| Task | Windows | Where |
|------|---------|-------|
| Open folder | `Ctrl+K Ctrl+O` | File → Open Folder |
| Terminal | ``Ctrl+` `` → PowerShell | Bottom panel |
| MongoDB shell | `mongosh` | Same terminal |

Use placeholders in notes: `<connection-string>`, `<username>`. Do **not** paste real passwords into chat or screenshots.

The instructor assigns **one** path: A local Community Edition, B managed cloud (Atlas-style), or C instructor URI.

---

## Steps from the training slides

### Step 1 — Connect

**Do this:** Open `mongosh` with your assigned URI.

```powershell
mongosh "mongodb://localhost:27017"
```

Cloud: `mongosh "<your-atlas-connection-string>"`.

**Expected result:** A prompt. Connection errors map to host, port, IP access list, or credentials — see [Exercise 2.4](../slide-exercises/module-02/exercise-2.4-diagnose-connection-failures.md).

---

### Step 2 — Ping

**Do this:**

```javascript
db.runCommand({ ping: 1 })
```

**Expected result:** `{ ok: 1 }`. Ping proves reachability, not write permission.

---

### Step 3 — Create the training database

**Do this:**

```javascript
use training_store
db.createCollection("products")
show collections
```

**Expected result:** Prompt is `training_store`. `products` is listed. The database may not appear in `show dbs` until it holds data.

---

### Step 4 — Insert, retrieve, update, delete

**Do this:** Run as a block, then confirm each write:

```javascript
db.products.insertOne({
  sku: "LAB1",
  name: "Connectivity Probe",
  category: "ACCESSORY",
  active: true
})

db.products.find({ sku: "LAB1" })

db.products.updateOne(
  { sku: "LAB1" },
  { $set: { verified: true } }
)

db.products.deleteOne({ sku: "LAB1" })
db.products.find({ sku: "LAB1" })
```

**Expected result:** Insert returns an `insertedId`. Find shows the document. Update `matchedCount` is 1. After delete, find returns nothing. **Remove `LAB1` before Lab 2** so it is not confused with catalog SKUs.

---

### Step 5 — Compass (if installed)

**Do this:** Paste the same URI, browse `training_store.products`.

**Expected result:** The GUI shows the same collections as `mongosh`.

---

### Step 6 — Readiness checklist

**Do this:** Complete [Exercise 2.3](../slide-exercises/module-02/exercise-2.3-environment-readiness-checklist.md).

**Expected result:** Server, client, ping, write, and read are all checked.

---

## Success criteria

- [ ] `ping` returns `ok: 1`
- [ ] `use training_store` works
- [ ] Insert / find / update / delete on a probe document succeeded
- [ ] Probe document `LAB1` was deleted
