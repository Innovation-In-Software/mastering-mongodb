# Exercise 3.7 — Select a Schema Design Pattern

**Module 3** (Data Modeling with MongoDB) · Day 1 · **Checkpoint G**  
**Deck:** `decks/pptx_new/MongoDB_Module03_Data_Modeling_with_MongoDB.pptx`, slide 48  
**Time:** 15 min · **Type:** discussion (pairs) · **MongoDB needed:** no

**Objective:** Match seven modeling requirements to a schema design pattern.

Choose from: **Attribute, Bucket, Subset, Computed, Extended reference, Outlier, Polymorphic.**

---

## Requirements

| # | Requirement | Pattern |
| --- | --- | --- |
| 1 | Sensor readings grouped by hour | |
| 2 | Latest three product reviews | |
| 3 | Stored average rating | |
| 4 | Dynamic product specifications | |
| 5 | Customer name copied into an order | |
| 6 | Rare products with a huge review volume | |
| 7 | Many product types in one collection | |

---

## Do this

1. Match requirements 1–4.
2. Match requirements 5–7.
3. For any two patterns, give one benefit and one cost.
4. Explain Bucket (versus one document per event) and why Outlier exists.

## Expected result

Seven matches, plus one benefit and one cost for two of them.

## Reference solution

After the debrief, compare with [Exercise 3.7 solution](solution/exercise-3.7-select-a-schema-pattern.md).

## Success criteria

- [ ] Seven matches recorded
- [ ] You can explain Bucket versus one document per event
- [ ] You can explain why Outlier exists
