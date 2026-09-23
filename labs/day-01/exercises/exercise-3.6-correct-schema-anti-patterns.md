# Exercise 3.6 — Find and Correct Schema Anti-Patterns

**Module 3** (Data Modeling with MongoDB) · Day 1 · **Checkpoint F**  
**Deck:** `decks/pptx_new/MongoDB_Module03_Data_Modeling_with_MongoDB.pptx`, slide 47  
**Time:** 15 min · **Type:** design (pairs) · **MongoDB needed:** no

**Objective:** Find the anti-patterns in a flawed product document and rewrite it with correct types, no unbounded array and a clear identifier convention.

---

## Flawed document

A teammate wrote this product document:

```javascript
{
  productId: "P1001",
  price: "49.99",
  isActive: "yes",
  allReviews: [
    // unlimited growth
  ],
  created: "September 20, 2026"
}
```

---

## Do this

1. Name every problem you see: types, growth, naming, identifier strategy.
2. Fix the types.
3. Move the reviews out.
4. Choose an `_id` / `sku` convention.

## Expected result

A list of at least four anti-patterns and one corrected document with no reviews array.

## Reference solution

After the debrief, compare with [Exercise 3.6 solution](solution/exercise-3.6-correct-schema-anti-patterns.md).

## Lab connection

`training_store` keeps one wrong-type product on purpose: XBAD, whose `price` is the string `"49.99"`. You will note it in Lab 2 ([LAB-2-GUIDE.md](../lab2/LAB-2-GUIDE.md)) and query it in Module 4. Do not fix it.

## Success criteria

- [ ] At least four anti-patterns named
- [ ] Corrected types for money, Boolean and date
- [ ] Reviews are not an unbounded embedded array
