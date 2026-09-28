# Exercise 8.2 — solution (instructor)

**Module 8** · Day 3 · Checkpoint B  
**Type:** design · **Do not hand this sheet to participants.**

Worksheet: [`../exercise-8.2-design-least-privilege-roles.md`](../exercise-8.2-design-least-privilege-roles.md) · Deck slide 46

## Running it

Twenty minutes: about twelve in pairs, then go round the room one identity per pair. It is a design exercise; **no authentication is enabled** on the class instance. If you demonstrate commands, do it only on a disposable instance and use `passwordPrompt()`.

## Task 1 and 2 — The matrix

| # | Identity | Placeholder user | Role | Permitted | Prohibited |
| --- | --- | --- | --- | --- | --- |
| 1 | Application service | `trainingStoreApp` | `readWrite` on `training_store` | Insert an order; update `fulfillmentStatus` | Create or drop users (`userAdmin`); touch other databases; `clusterAdmin` |
| 2 | Reporting service | `reportUser` | `read` on `training_store` (or a custom role on approved collections) | `find` and `aggregate` on `orders` for the revenue report | Any `insert`, `update` or `delete` |
| 3 | Support engineer | `supportAnalyst` | Custom role, e.g. `reviewReader`: `find` on `reviews` (add `orders` if the job needs it; hide contact details through a view) | Read a customer's order or review to answer a ticket | `drop`, `remove`, bulk export of `customers` contact data |
| 4 | Monitoring service | `monitorAgent` | `clusterMonitor` (granted in `admin`) | `serverStatus`, `rs.status()`, `currentOp` | Any data read or write on `training_store` collections |
| 5 | Backup service | `backupAgent` | `backup` (granted in `admin`); `restore` given to a separate, controlled identity | `mongodump` of `training_store` | Arbitrary deletes; `dropDatabase`; restoring over `training_store` |
| 6 | Database administrator | `dbaOperator1` (one per named person, not a shared account) | `dbAdmin` / `userAdmin` on `training_store`; `root` only as audited break-glass | Create an index or a user under change control | Being used by the application; shared logins; routine work as `root` |

Slide summary: App: readWrite, never userAdmin · Reporting: read only · Support: limited read, never drop · Monitoring: clusterMonitor, no writes · Backup: backup role; DBA: separate identity.

## Sketch (disposable instance only — do not run in class)

```javascript
use training_store
db.createUser({
  user: "trainingStoreApp",
  pwd: passwordPrompt(),
  roles: [{ role: "readWrite", db: "training_store" }]
})
db.createUser({
  user: "reportUser",
  pwd: passwordPrompt(),
  roles: [{ role: "read", db: "training_store" }]
})
db.createRole({
  role: "reviewReader",
  privileges: [{
    resource: { db: "training_store", collection: "reviews" },
    actions: ["find"]
  }],
  roles: []
})
db.createUser({ user: "supportAnalyst", pwd: passwordPrompt(), roles: [] })
db.grantRolesToUser("supportAnalyst", [{ role: "reviewReader", db: "training_store" }])
```

`passwordPrompt()` asks for the password interactively, so it never appears in the script, in shell history or in a screenshot. The application reads its connection string (`mongodb://trainingStoreApp:<password>@host:27017/training_store?authSource=training_store&tls=true`) from a secret manager at runtime.

## Task 3 — Why the app never uses clusterAdmin

If the application used a cluster administrator, one stolen application credential would inherit every privilege — every database, every user, the cluster itself. Least privilege limits the blast radius and makes audit trails meaningful, because each action is traceable to one identity with one purpose.

## What you want to hear

- Six separate identities — no shared account.
- The application is `readWrite` on its own database only.
- Reporting is read-only; monitoring reads metrics, not data.
- Backup and restore are separate privileges.
- Only placeholder names; passwords only as `passwordPrompt()` or `<password>`.

If someone suggests "grant root to fix a not-authorized error", use it as the anti-pattern: grant the one missing privilege instead.
