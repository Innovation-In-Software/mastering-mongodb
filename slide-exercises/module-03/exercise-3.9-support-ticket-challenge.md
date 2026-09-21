# Exercise 3.9: Design a Support-Ticket Data Model

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Practical Challenge)  
**Time:** 25 min  
**Difficulty:** Intermediate

**Objective:** Design collections, embed/reference decisions, a sample ticket document, validation, and audit-history storage for a support system.

---

## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Work in pairs. Capture answers in a notes file or on paper.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional — a table is enough |
| Timer | Instructor clocks this | Stay on the slide timer |

You do **not** need MongoDB running for this exercise.

---

## Scenario

A support system must create tickets, assign agents, store status and priority, add comments, attach tags, display recent comments with the ticket, preserve a complete audit history, and search by customer, agent, status, and priority.

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Access patterns and collections

**Do this:** List the main access patterns. Name the collections. Mark what is embedded vs referenced, and what could grow without bound.

**Expected result:** Collections such as `tickets`, `customers`, `agents`, `comments` and/or `audit_events`. Recent comments and tags are bounded on the ticket. Full comment and audit history are separate.

---

### Step 2 — Sample document, validation, and indexes

**Do this:** Draft one ticket document with BSON types. List required fields for validation. Explain how complete audit history is stored. Name likely future indexes (do **not** create them yet).

**Expected result:** A ticket with `ticketNumber`, `customerId`, `assignee`, `status`, `priority`, `tags`, `recentComments[]`, timestamps. Validation requires those keys. Audit events live in their own collection. Indexes likely on `customerId`, `assignee.agentId`, `status`, `priority`.

---

## Suggested design direction

**Embed:** ticket summary, current assignment, tags, a bounded set of recent comments.

**Reference or separate:** complete comment history, complete audit-event history, customer master, agent master.

---

## Success criteria

- [ ] Collection list exists
- [ ] One sample ticket document
- [ ] Embed/reference table
- [ ] Validation requirements
- [ ] Brief justification including unbounded data


## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
