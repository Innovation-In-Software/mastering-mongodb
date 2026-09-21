# Exercise 4.4: Query Missing and Null Fields

**Module 4:** The MongoDB Query Language  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 4)  
**Time:** 10 min  
**Difficulty:** Beginner

**Objective:** Distinguish `$exists`, BSON `null`, missing fields, and incorrect types.

---

## Environment basics (read this first)

**Demonstration environment:** Windows 10/11 · PowerShell in Cursor (``Ctrl+` ``) · `mongosh` connected to the training instance.

| Task | Windows | Where |
|------|---------|-------|
| Open folder | `Ctrl+K Ctrl+O` | File → Open Folder |
| Terminal | ``Ctrl+` `` → PowerShell | Bottom panel |
| MongoDB shell | `mongosh` | Same terminal |

**Prerequisite:** `training_store` is loaded from [`datasets/training_store/load.js`](../../datasets/training_store/load.js). If writes from an earlier lab remain, reload that script unless the exercise says otherwise.

```javascript
use training_store
```


---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Products with a discount field

**Do this:** Run:

```javascript
db.products.find({ discountPrice: { $exists: true } })
```

**Expected result:** `P1001` and `B310` match. Presence of the field is enough — the value may still be inspected later.

---

### Step 2 — Products without a discount field

**Do this:** Run:

```javascript
db.products.find({ discountPrice: { $exists: false } })
```

**Expected result:** Most catalog items match, including laptops that never had a discount field.

---

### Step 3 — Customers with a null phone

**Do this:** Run:

```javascript
db.customers.find({ "contact.phone": { $type: "null" } })
```

**Expected result:** `C204` matches. `{ phone: null }` on a dotted path is easy to get wrong — query `{ "contact.phone": { $type: "null" } }`.

---

### Step 4 — Customers without a phone field

**Do this:** Run:

```javascript
db.customers.find({ "contact.phone": { $exists: false } })
```

**Expected result:** `C515` matches (no phone field). `C204` has the field with BSON null. Everyone else has a string phone.

---

### Step 5 — Incorrect price BSON type

**Do this:** Run:

```javascript
db.products.find({ price: { $type: "string" } })
```

**Expected result:** `XBAD` (Legacy Cable Pack) is the planted type error. Money in this course is Decimal128.

---



## Success criteria

- [ ] Did not treat `{ field: null }` as “explicitly null only”
- [ ] Separated missing vs null vs wrong type
- [ ] Found `XBAD` with `$type`

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
