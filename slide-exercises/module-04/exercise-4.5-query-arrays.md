# Exercise 4.5: Query Arrays

**Module 4:** The MongoDB Query Language  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 4)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Query arrays with containment, `$all`, `$size`, `$ne`, and `$nin`.

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

### Step 1 — Tagged technology

**Do this:** Run:

```javascript
db.products.find({ tags: "technology" })
```

**Expected result:** Any product whose `tags` array contains `technology`, regardless of other tags.

---

### Step 2 — Both database and technology

**Do this:** Run:

```javascript
db.products.find({ tags: { $all: ["database", "technology"] } })
```

**Expected result:** `B300` matches (`database` and `technology`). Order of tags does not matter.

---

### Step 3 — Exactly two tags

**Do this:** Run:

```javascript
db.products.find({ tags: { $size: 2 } })
```

**Expected result:** Most catalog products have exactly two tags. `$size` cannot express “at least two”.

---

### Step 4 — Specified available size

**Do this:** Run:

```javascript
db.products.find({ "attributes.sizes": 9 })
```

**Expected result:** `S200`, `S210`, and `S290` match. Nested array containment uses a dotted path.

---

### Step 5 — Not containing discontinued

**Do this:** Run:

```javascript
db.products.find({ tags: { $ne: "discontinued" } })
```

**Expected result:** `L190` is excluded once it carries a `discontinued` tag. `$ne` on an array field also matches documents that **lack** the field.

---



## Success criteria

- [ ] Explained containment vs exact-array match
- [ ] Used `$all` instead of two separate `tags` equalities when both values are required
- [ ] Stated the `$size` limitation

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
