# Exercise 3.4 — Model a Product Catalog

**Module 3** (Data Modeling with MongoDB) · Day 1 · **Checkpoint D**  
**Deck:** `decks/pptx_new/MongoDB_Module03_Data_Modeling_with_MongoDB.pptx`, slide 45  
**Time:** 20 min · **Type:** design (pairs) · **MongoDB needed:** optional — write documents in a scratch file

**Objective:** Design three products — a laptop, a shoe and a book — in one `products` collection with one consistent core.

---

## Requirements

**Common fields (every product):** sku, name, description, category, price, active, creation date.

**Type-specific fields:**

| Product | Fields |
| --- | --- |
| Laptop | processor, memory, storage, screen size |
| Shoe | size, color, material, gender category |
| Book | author, ISBN, publisher, language |

---

## Do this

1. List the core fields and give each a BSON type.
2. Decide where the type-specific fields go: at the top level or under an `attributes` object.
3. Write one laptop, one shoe and one book document.
4. Check that the names and types of the core fields match on all three.

## Expected result

Three documents in one collection. Queries such as `find({ category: "LAPTOP" })` and `find({ "attributes.isbn": "978-0000000000" })` could use them. No category-specific field is required for every product, and no document uses a different name (such as `productPrice`) for a core field.

## Reference solution

After the debrief, compare with [Exercise 3.4 solution](solution/exercise-3.4-model-a-product-catalog.md).

## Lab connection

Lab 2, Step 2 ([LAB-2-GUIDE.md](../lab2/LAB-2-GUIDE.md)) inserts `training_store`'s own laptop, shoe and book: L100, S200 and B300.

## Success criteria

- [ ] Common fields use the same names and types
- [ ] Three categories exist in one collection
- [ ] Type-specific fields are nested or clearly optional
