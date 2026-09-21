# Exercise 8.5: Rationalize an Index Portfolio

**Module 8:** MongoDB Best Practices, Security, and Troubleshooting  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 8)  
**Time:** 20 min  
**Difficulty:** Intermediate

**Objective:** Review overlapping category indexes, name supported queries, flag low-selectivity keys, and describe evidence required before removal.

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

### Step 1 — Map overlap

**Do this:** Given these indexes, mark which prefixes overlap and which queries each can support:

```javascript
{ category: 1 }
{ category: 1, price: 1 }
{ category: 1, price: 1, name: 1 }
{ active: 1 }
{ category: 1, active: 1, price: 1 }
```

**Expected result:** The three category+price variants overlap; `{ category: 1 }` is a prefix of the others. `{ active: 1 }` is low-selectivity and does not overlap those prefixes. `{ category: 1, active: 1, price: 1 }` is a different leading pair than category+price.

---

### Step 2 — Safe testing plan

**Do this:** Write the sequence before dropping any index: workload review, explain, hide, monitor, drop with rollback. Name one index you would not hide on appearance alone.

**Expected result:** Hide `{ category: 1 }` only after catalog and reporting explains still use a remaining compound index. Do not hide `{ category: 1, active: 1, price: 1 }` without measuring the active-catalog shape. `{ active: 1 }` is a hide candidate after proving no query needs it.

---

## Success criteria

- [ ] Overlapping prefixes are identified
- [ ] `active` is treated as low-selectivity
- [ ] Hide-then-monitor is required before drop

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
