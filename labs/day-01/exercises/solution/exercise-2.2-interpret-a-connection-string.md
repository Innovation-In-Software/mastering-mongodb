# Exercise 2.2 — solution (instructor)

**Module 2** · Day 1 · Checkpoint B  
**Type:** analysis · **Do not hand this sheet to participants.**

Worksheet: [`../exercise-2.2-interpret-a-connection-string.md`](../exercise-2.2-interpret-a-connection-string.md) · Deck slide 45

## Running it

Eight minutes of individual work, then a two-minute debrief. No live connection is needed. The worksheet and the slide both show the password as `<password>`, a placeholder, so no credential-looking value appears on screen.

## Task 1 — Labels

```text
mongodb://trainingUser:<password>@db.example.net:27017/training
```

| Part | Value |
| --- | --- |
| Protocol (scheme) | `mongodb://` |
| Username | `trainingUser` |
| Password | `<password>` — placeholder only, never a real secret |
| Host | `db.example.net` |
| Port | `27017` |
| Default database | `training` |

The default database is `training`, not `training_store`. That is deliberate: it is a generic example host, not the class server.

## Task 2 — Security answers

| Question | Answer |
| --- | --- |
| 1. Never in a screenshot | The password (and so the full URI once a real password is in it). |
| 2. Store securely | Username and password — in environment variables, a password manager or a secret store. |
| 3. Could fail because… | Wrong password; host not found (DNS); port 27017 blocked by a firewall; special characters in the password not percent-encoded; TLS mismatch; wrong `authSource`. |
| 4. Password in a real application | From an environment variable or a secret store, never from source code. For `mongosh`, pass `--username` and let it prompt for the password. |

## Task 3 — Schemes

| Scheme | One sentence |
| --- | --- |
| `mongodb://` | Lists the host(s) and optional port(s) explicitly. |
| `mongodb+srv://` | Gives one hostname and uses a DNS SRV lookup to discover the members and ports — so there is **no port** in the URI — and turns TLS on by default. MongoDB Atlas provides this form. |

## What you want to hear

- Nobody reads a password aloud or writes one into notes.
- Host and database are not swapped (`db.example.net` is the host; `/training` is the database).
- At least two concrete failure causes, not "it might not work".
