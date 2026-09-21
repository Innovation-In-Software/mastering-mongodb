# Exercise 8.2: Find the Schema Anti-Patterns

**Module 8:** MongoDB Best Practices, Security, and Troubleshooting  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 8)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Identify unbounded arrays, textual prices, inconsistent names, deep nesting, duplicated live customer data, missing required fields, and string timestamps, then propose a corrected design.

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

### Step 1 — Name the anti-patterns

**Do this:** On the product document below, list every anti-pattern from the module list.

```javascript
{
  Product_Name: "Trail shoe",
  productPrice: "89.99",
  details: { catalog: { store: { web: { active: "yes" } } } },
  customer: { email: "aisha@example.com", lastOrderTotal: 210.50 },
  reviews: [ /* every review ever */ ],
  updated: "2026-09-01 09:00"
}
```

**Expected result:** Unbounded reviews; price as text; mixed names (`Product_Name` vs `productPrice`); unnecessary nesting; live customer data on a product; missing sku/category/Decimal128/Boolean/Date; string timestamp; boolean as text.

---

### Step 2 — Corrected sketch

**Do this:** Sketch the replacement: product core fields, where reviews live, and how customer data is removed.

**Expected result:** products: sku, name, category, Decimal128 price, Boolean active, Date updatedAt, bounded attributes. reviews collection keyed by productId. No customer object on the product.

---

## Success criteria

- [ ] Seven anti-pattern categories are identified
- [ ] Reviews are moved off the product
- [ ] Price and dates use BSON types, not strings

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
