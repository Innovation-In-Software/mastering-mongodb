# Exercise 2.2 — Interpret a Connection String

**Module 2** (Installation and Setup) · Day 1 · **Checkpoint B**  
**Time:** 10 min (8 min individual work + 2 min debrief) · **Type:** analysis · **Difficulty:** Beginner

**Deck:** `decks/pptx_new/MongoDB_Module02_Installation_and_Setup.pptx` — slide 45, "Exercise 2.2 — Interpret a Connection String"

## Purpose

Label every part of a MongoDB connection string, and keep the password secret. You read a URI left to right, decide which parts are secrets, and contrast the two connection-string schemes.

## Prerequisites

- Module 2, Part 3 ("Standard Connection-String Format" and "DNS Seed-List (SRV) Connection Strings")
- Paper, a notes file, or the tables at the end of this sheet
- You do **not** need a live connection for this exercise

## Scenario

Label each part of this URI. It is one line; `<password>` is a **placeholder**, never a real secret.

```text
mongodb://trainingUser:<password>@db.example.net:27017/training
```

On the slide it is split over four lines to fit:

```text
mongodb://
trainingUser:<password>@
db.example.net:27017
/training
```

Work individually, then compare with a neighbour.

## Tasks

### Task 1 — Label protocol, user, password, host, port, database

Fill in the first table in the deliverable. You should be able to point to where each value sits in the URI.

### Task 2 — Answer the four security questions

Write a short answer to each:

1. Which part must not appear in a screenshot?
2. Which values should be stored securely?
3. What could cause this connection to fail? (Name at least two causes.)
4. How should the password be supplied in a real application?

### Task 3 — Contrast `mongodb://` with `mongodb+srv://`

Write one sentence for each scheme. Note which form managed-cloud services such as MongoDB Atlas usually provide, and whether the `+srv` form carries a port.

### Task 4 — Check labels without reading secrets aloud

Compare your labels with your neighbour and then with the class debrief. Correct any swapped host/database or protocol mix-up. When you read your answer aloud, say "password placeholder" — never a value.

## Deliverable

| Part | Value in the sample |
| --- | --- |
| Protocol (scheme) | |
| Username | |
| Password | |
| Host | |
| Port | |
| Default database | |

| Question | Your answer |
| --- | --- |
| 1. Never in a screenshot | |
| 2. Store securely | |
| 3. Could fail because… | |
| 4. Password in a real application | |
| `mongodb://` | |
| `mongodb+srv://` | |

## Expected outcome

- All six parts are labelled correctly.
- The password is treated as a placeholder only, and secrets go in an environment variable or a secret store.
- You can say that `+srv` lets DNS discover the hosts.

## Success criteria

- [ ] All six URI parts are labelled
- [ ] The password is treated as a secret, not as slide or notes content
- [ ] You can distinguish `mongodb://` from `mongodb+srv://`
- [ ] You can name two realistic connection failures

## Next

[Exercise 2.3 — Diagnose Connection Failures](exercise-2.3-diagnose-connection-failures.md)
