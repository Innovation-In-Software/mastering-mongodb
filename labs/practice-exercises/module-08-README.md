# Module 8 — Practice exercise solutions

**Deck:** `decks/pptx_new/MongoDB_Module08_Best_Practices_Security_and_Troubleshooting.pptx`  
**Dataset:** `training_store` (fresh load of `datasets/training_store/load.js`)  
Attempt the slide activity first, then compare your answers here.

Official numbered checkpoints for this module: [Exercise 8.1](../day-03/exercises/exercise-8.1-review-a-query-and-projection.md) · [Exercise 8.2](../day-03/exercises/exercise-8.2-design-least-privilege-roles.md) · [Exercise 8.3](../day-03/exercises/exercise-8.3-define-rpo-and-rto.md) · Lab: [Lab 7 — Production Readiness](../day-03/lab7/LAB-7-GUIDE.md)

---

## Exercise: Predict the Validator's Verdict

**Slide 15** · **Time:** 10 minutes · **How to run:** pairs, five minutes to predict, then run the four inserts.

### Scenario

`training_store_ops.orders_validated` (built on slide 13, "A Validator on a Scratch Collection") requires `orderNumber` (string), `total` (decimal) and `paymentStatus` (`PAID`, `PENDING` or `FAILED`). Accepted or rejected? Decide before you run each insert.

```javascript
use training_store_ops
// A
db.orders_validated.insertOne({ orderNumber: "OPS-2", total: Decimal128("24.99"), paymentStatus: "PENDING" })
// B
db.orders_validated.insertOne({ orderNumber: "OPS-3", total: Decimal128("5.00"), paymentStatus: "PAID_NOW" })
// C
db.orders_validated.insertOne({ total: Decimal128("5.00"), paymentStatus: "PAID" })
// D
db.orders_validated.insertOne({ orderNumber: "OPS-4", total: 9.99, paymentStatus: "PAID" })
```

### Tasks

1. Mark each insert accepted or rejected.
2. Name the rule each rejection breaks.
3. Say whether an extra field such as `note` is allowed.
4. Run them on `training_store_ops` to check — never on `training_store`.

### Solution

| Insert | Verdict | Rule |
| --- | --- | --- |
| A | **Accepted** | Satisfies all three rules |
| B | **Rejected** | `enum` — `PAID_NOW` is not one of the allowed values |
| C | **Rejected** | `required` — no `orderNumber` |
| D | **Rejected** | `bsonType: "decimal"` — the literal `9.99` is a double, even though it looks like money |

Every rejection is `MongoServerError: Document failed validation`, **code 121**; the error details name the failing rule.

**Extra fields pass.** The validator lists `properties` but doesn't set `additionalProperties: false`, so a document with an extra `note` field is accepted. That is usually what you want while a schema evolves.

### Why this is the answer

A validator enforces only the rules you wrote. Knowing exactly which ones are there — and which are not — is what makes it trustworthy.

---

## Exercise: Design the Index for Each Shape

**Slide 23** · **Time:** 15 minutes · **How to run:** individually for eight minutes, then compare; run `explain` on the instructor screen for at least one shape.

### Scenario

Three real `training_store` queries — one compound index each. Write the index for each shape, label each key **E**, **S** or **R**, then confirm with `explain`.

1. **Catalog:** `category: "LAPTOP"`, `active: true`, sort `price` ascending
2. **History:** `customerId = c101`, sort `createdAt` descending
3. **Report:** `paymentStatus: "PAID"`, `createdAt` in September

`c101` is an ObjectId: `const c101 = db.customers.findOne({ customerNumber: "C101" })._id`.

### Tasks

1. Write an index for each shape.
2. Label every key E, S or R.
3. Check the plan with `explain()`.
4. Name the extra cost of each index.

### Solution

| Shape | Index | Labels | Query |
| --- | --- | --- | --- |
| 1 Catalog | `{ category: 1, active: 1, price: 1 }` | E, E, S | `db.products.find({ category: "LAPTOP", active: true }).sort({ price: 1 })` → L100, L110 |
| 2 History | `{ customerId: 1, createdAt: -1 }` | E, S | `db.orders.find({ customerId: c101 }).sort({ createdAt: -1 })` → 5 orders: O5001, O6306, O6301, O6201, O6101 |
| 3 Report | `{ paymentStatus: 1, createdAt: 1 }` | E, R | `db.orders.find({ paymentStatus: "PAID", createdAt: { $gte: ISODate("2026-09-01"), $lt: ISODate("2026-10-01") } })` → 6 orders |

For shape 3, `createdAt: -1` works equally well — an index range can be scanned in either direction.

**Check with explain:** each plan should show `IXSCAN` and **no `SORT` stage**, with keys examined close to documents returned.

**Cost:** each index uses disk and cache and slows every insert, update and delete on its collection.

**Overlap:** if the history index also includes `paymentStatus` — `{ customerId: 1, paymentStatus: 1, createdAt: -1 }`, as in Exercise 8.1 — the two order indexes overlap. Keep both only if both shapes are hot; otherwise hide one (`db.orders.hideIndex(...)`), monitor, then drop.

### Why this is the answer

An index is designed for a query shape. Write the shape down first — equality fields, then the sort, then the range — and let `explain` prove it.

---

## Exercise: Which Layer Is It?

**Slide 42** · **Time:** 10 minutes · **How to run:** pairs for five minutes, then go round the room, one message per pair.

### Scenario

Five messages from the `training_store` application. Name the layer and the first check for each.

```text
A  connect ECONNREFUSED 127.0.0.1:27017
B  Authentication failed (user trainingStoreApp)
C  not authorized on training_store to execute command { find: "orders" }
D  E11000 ... index: email_unique
E  Document failed validation
```

### Tasks

1. Name the layer for A–E.
2. Write the first check or command.
3. Say what you would not do.
4. Pick one to add to a runbook.

### Solution

| Message | Layer | First check | Don't |
| --- | --- | --- | --- |
| A `ECONNREFUSED 127.0.0.1:27017` | Process or network | Nothing is listening on localhost 27017: is `mongod` running, is the port right? Then connect and run `db.hello()` | Bind to every interface (`bindIp: 0.0.0.0`) to make it go away |
| B `Authentication failed` | Security — identity | The user name, where the password comes from, and `authSource` (a user created in `admin` needs `authSource=admin`) | Disable authentication |
| C `not authorized ... { find: "orders" }` | Security — roles | Login worked; the role is missing. Grant `find` on `orders` or a `read` role | Grant `root` |
| D `E11000 ... email_unique` | Data rules — unique index | A duplicate email: `customers` has the unique index `email_unique` on `contact.email` (for example a second `aisha@example.com`). An expected business outcome — show a friendly message | Drop the unique index |
| E `Document failed validation` | Schema | Code 121 — read the error details to see which rule failed (missing field, type, enum) | Remove the validator or set it to `warn` |

A good runbook entry: **A** (service down) or **C** (a release that forgot a role), with the exact first command and the owner.

### Why this is the answer

The message names the layer — read it before you change anything. The fix is always the smallest one at that layer; never disable authentication, grant root or bind to every interface to make an error disappear.
