# Exercise 3.9 — Design a Support-Ticket Data Model

**Module 3** (Data Modeling with MongoDB) · Day 1 · **Checkpoint I**  
**Deck:** `decks/pptx_new/MongoDB_Module03_Data_Modeling_with_MongoDB.pptx`, slide 50  
**Time:** 25 min · **Type:** design challenge (pairs) · **MongoDB needed:** no — design only, do not create indexes

**Objective:** Apply the whole Module 3 method — access patterns, relationships, growth, then rules — to a new application.

---

## Scenario

A support system must:

- create tickets
- assign agents
- set status and priority
- add comments and tags
- show recent comments with the ticket
- keep a complete audit history
- search by customer, agent, status and priority

---

## Do this

1. List the main access patterns and name the collections.
2. Mark what is embedded, what is referenced, and what could grow without limit.
3. Draft one ticket document with BSON types.
4. List the validation rules (required fields and types) and the indexes you would plan.

| Data | Embed or reference | Bounded or unbounded |
| --- | --- | --- |
| Current assignee | | |
| Tags | | |
| Recent comments | | |
| All comments | | |
| Audit history | | |
| Customer | | |
| Agent | | |

## Expected result

A collection list, one sample ticket document, a completed embed/reference table, the validation requirements, and a short justification that mentions the unbounded data.

## Reference solution

After the debrief, compare with [Exercise 3.9 solution](solution/exercise-3.9-support-ticket-challenge.md).

## Success criteria

- [ ] A collection list exists
- [ ] One sample ticket document
- [ ] An embed/reference table
- [ ] Validation requirements
- [ ] A brief justification that includes the unbounded data
