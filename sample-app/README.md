# sample-app — Connect MongoDB from application code

Thin connection demo for the course objective *Connect MongoDB to applications and external services*.

This is **not** a new teaching module. Module 8 slides send driver wiring here. Run it after [Lab 1](../labs/day-01-lab-01-install-connect-verify.md), once `training_store` is loaded.

Pick **one** language. Both programs:

1. Read `MONGODB_URI` from the environment (never a password in source control)
2. Ping the server
3. List five active products from `training_store.products`

---

## Safety

| Do | Do not |
|----|--------|
| `setx` / `$env:MONGODB_URI` / a local `.env` that is gitignored | Commit connection strings |
| Placeholders in notes: `<username>` | Paste Atlas passwords into chat or slides |
| `mongodb://localhost:27017` for local class | Hard-code production URIs |

Copy [`.env.example`](.env.example) to `.env` if your tooling loads dotenv. The scripts below use the process environment only.

---

## 1. Set the URI (PowerShell)

Local:

```powershell
$env:MONGODB_URI = "mongodb://localhost:27017"
```

Atlas (placeholder):

```powershell
$env:MONGODB_URI = "mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority"
```

---

## 2. Node.js

Requires Node.js 18+.

```powershell
cd sample-app
npm install
node connect.mjs
```

**Expected result:** `ok: 1` from ping, then up to five documents with `sku`, `name`, `category`, `price`. Inactive `L190` is absent because the filter is `{ active: true }`.

---

## 3. Python

```powershell
cd sample-app
pip install -r requirements.txt
python connect.py
```

**Expected result:** Same as Node: ping ok, then active products.

---

## What this is not

- Not an ORM, REST API, or storefront
- Not a substitute for `mongosh` labs
- Not a place to enable classroom authentication experiments on a shared database

When you return to Module 8, store the URI in a password manager or environment variable — the same rule this folder already follows.
