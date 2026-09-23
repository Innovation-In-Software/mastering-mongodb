# Exercise 2.2: Interpret a Connection String

**Module 2:** Installation and Setup  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 2, Lesson 2.3)  
**Time:** 10 min  
**Difficulty:** Beginner

**Objective:** Label the parts of a MongoDB connection string and identify how credentials must be handled.

---

## Environment basics (read this first)

**Demonstration environment:** Classroom analysis. Work individually, then compare with a neighbor.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | A labeled URI is enough |
| Timer | 8 minutes work + 2 minutes debrief | Instructor clocks this |

You do **not** need a live connection for this exercise. Treat `password` as a placeholder, never a real secret.

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Label the connection-string parts

**Do this:** Using this sample, identify protocol, username, password placeholder, host, port, and default database:

```text
mongodb://trainingUser:password@db.example.net:27017/training
```

**Expected result:** Your notes name all six parts. You can point to where each value sits in the URI.

---

### Step 2 — Answer the security questions

**Do this:** Write a short answer for each:

1. Which part must not appear in a screenshot?
2. Which values should be stored securely?
3. What could cause this connection to fail?
4. How should the password be supplied in a real application?

**Expected result:** You refuse to put the password in slides or source. You can name at least two failure causes (wrong password, host unreachable, port, DNS, TLS).

---

### Step 3 — Compare `mongodb://` and `mongodb+srv://`

**Do this:** Write one sentence for each scheme. Note which form managed-cloud services commonly provide.

**Expected result:** You can say that `mongodb://` lists hosts (and optional port) and `mongodb+srv://` uses DNS to discover deployment information.

---

### Step 4 — Compare with the instructor solution

**Do this:** Check your labels against the class debrief. Correct any swapped host/database or protocol mix-up.

**Expected result:** You can parse a URI aloud without reading credentials onto a shared screen.

---

## Deliverable

| Part | Value in the sample |
|------|---------------------|
| Protocol | |
| Username | |
| Password | |
| Host | |
| Port | |
| Default database | |

## Instructor solution (after discussion)

| Part | Value |
|------|-------|
| Protocol | `mongodb://` |
| Username | `trainingUser` |
| Password | `password` (placeholder — never a real secret) |
| Host | `db.example.net` |
| Port | `27017` |
| Default database | `training` |

**Security:** Do not screenshot the password. Store username and password in environment variables or a secret store. Typical failures: wrong password, host not found, port blocked, special characters not URI-encoded, TLS mismatch.

---

## Success criteria

- [ ] All six URI parts are labeled
- [ ] Password is treated as a secret, not as slide content
- [ ] You can distinguish `mongodb://` from `mongodb+srv://`
- [ ] You can name two realistic connection failures

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
