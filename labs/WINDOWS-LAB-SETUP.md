# Windows lab setup — Mastering MongoDB

Technician handout (Word): [Mastering_MongoDB_Lab_Setup_Windows.docx](Mastering_MongoDB_Lab_Setup_Windows.docx).

Set up a Windows laptop **before Day 1**. Every hands-on lab in this course runs in PowerShell against a MongoDB server on `localhost:27017`, with the course folder open so paths such as `.\datasets\training_store\load.js` work.

| | |
|---|---|
| **Course** | Mastering MongoDB (3 days) |
| **Organization** | Innovation In Software Corporation |
| **OS** | Windows 10 or Windows 11, 64-bit |
| **Shell** | Windows PowerShell (the labs are written for PowerShell, not Command Prompt or Git Bash) |
| **Time** | About 30–45 minutes, plus downloads |

Day 1 Lab 1 walks through the same install in class. Completing this page first means that lab is a verification, not a download.

---

## What the laptop needs

| Item | Minimum |
|---|---|
| Windows | 10 or 11, 64-bit |
| Rights | A local account that can install software and start a Windows service (Administrator for `Start-Service`) |
| Memory | 8 GB RAM |
| Disk | 10 GB free (MongoDB plus the course folder) |
| Network | Internet for the installers. After that, Days 1–2 labs work offline on the local server. Day 3 Lab 6 needs the instructor’s replica-set or Atlas address, which does need a network. |

You do **not** need prior MongoDB experience. You do need to be comfortable opening PowerShell and pasting a command.

---

## Software to install

Install these from MongoDB’s own download pages. Use the current **MongoDB 8.x** Community Edition (the screens in this guide show **8.3.11**). The labs also run on 7.0 or later.

| Software | Required? | Used for | Download |
|---|---|---|---|
| **MongoDB Community Server** | Yes | The database (`mongod`), installed as a Windows service named `MongoDB`, listening on `localhost:27017` | [mongodb.com/try/download/community](https://www.mongodb.com/try/download/community) — screens show **8.3.11**, Windows x64, **msi** |
| **MongoDB Compass** | Yes | Opens at the end of the server install. Day 1 Lab 1, Step 10 uses the same saved connection | Installed by the server MSI. Separate download only if that checkbox was cleared: [mongodb.com/try/download/compass](https://www.mongodb.com/try/download/compass) |
| **MongoDB Shell (`mongosh`)** | Yes | Every lab command | [mongodb.com/try/download/shell](https://www.mongodb.com/try/download/shell) — screens show **2.12.0**, Windows x64, **msi** |
| **MongoDB Database Tools** | Yes for Day 3 Lab 7 | `mongodump` and `mongorestore` | [mongodb.com/try/download/database-tools](https://www.mongodb.com/try/download/database-tools) — screens show **100.19.0**, Windows x86_64, **msi** |
| **Course folder** | Yes | `datasets\training_store\load.js` and the lab guides | Git clone or the zip the instructor sends |
| **VS Code** or **Cursor** | Recommended | The lab terminal is PowerShell inside the editor (`` Ctrl+` ``) | [code.visualstudio.com](https://code.visualstudio.com/) |
| **Git for Windows** | Recommended | Clone the course repository | [git-scm.com/download/win](https://git-scm.com/download/win) |
| **Node.js 18+** | Optional | Module 8 connection demo in `sample-app/` | [nodejs.org](https://nodejs.org/) |
| **Python 3** | Optional | The same demo in Python (`pip install -r sample-app/requirements.txt`) | [python.org](https://www.python.org/downloads/) |

Compass is optional inside the Community Server installer. Install it anyway — Lab 1 asks you to open the same document in Compass.

Database Tools are a **separate** installer. They are not included in the server MSI. Without them, Lab 7 Step 4 falls back to a written exercise.

Docker is an optional substitute for the server install. See [Docker instead of the MSI](#docker-instead-of-the-msi) below. You still need `mongosh`, Compass, and Database Tools on the Windows PATH.

---

## 1. Install MongoDB Community Server

1. Open [MongoDB Community Server](https://www.mongodb.com/try/download/community).
2. Choose the current **8.x** (the screen shows **8.3.11**), **Windows x64**, package **msi**, then **Download**.

<img src="screenshots/lab1-01-download-community-server.png" alt="Community Server download: version 8.3.11, Windows x64, msi" width="640">

3. Run the MSI and choose **Complete**. The shell is not part of this package.

<img src="screenshots/lab1-02-choose-complete.png" alt="Choose Complete setup type" width="640">

4. Choose **Install MongoD as a Service**. Leave **Run service as Network Service user** selected. Do not type a password.
   - Service name: `MongoDB`
   - Data directory: `C:\Program Files\MongoDB\Server\8.3\data` (accept the path the installer shows)
   - Log directory: `C:\Program Files\MongoDB\Server\8.3\log`

<img src="screenshots/lab1-03-service-configuration.png" alt="Service configuration: Network Service user, service name MongoDB" width="640">

5. Leave **Install MongoDB Compass** checked.

<img src="screenshots/lab1-04-install-compass.png" alt="Install MongoDB Compass checkbox selected" width="640">

6. Click **Install** and wait until the wizard finishes. Do not click **Cancel**.

<img src="screenshots/lab1-05-ready-to-install.png" alt="Ready to install MongoDB; Install is selected" width="640">

<img src="screenshots/lab1-06-installing.png" alt="Installer progress while MongoDB is registering" width="640">

7. Click **Finish**. Do **not** change the server to listen on every network interface.

<img src="screenshots/lab1-07-setup-finished.png" alt="Setup wizard completed; Finish is selected" width="640">

Files you may need later (the `8.3` folder matches this installer; use the version you actually installed):

| File | Path |
|---|---|
| Server config | `C:\Program Files\MongoDB\Server\8.3\bin\mongod.cfg` |
| Server log | `C:\Program Files\MongoDB\Server\8.3\log\mongod.log` |

In `mongod.cfg`, leave these as they are:

```yaml
net:
  port: 27017
  bindIp: 127.0.0.1
```

`bindIp: 127.0.0.1` keeps the database on this machine only. A local install has access control off by default, which is acceptable only while nothing outside the laptop can reach port 27017. Do not set `bindIp: 0.0.0.0`.

---

## 2. Connect MongoDB Compass

The server installer opens Compass when it finishes. Connect it now, before you install the shell. Use the separate Compass download only if the checkbox in section 1 was cleared.

1. If a welcome dialog appears, click **Start**.

<img src="screenshots/lab1-08-compass-welcome.png" alt="Compass welcome dialog with the Start button" width="640">

2. Click **+ Add new connection**. Leave the URI as `mongodb://localhost:27017` (Compass may show a trailing slash). Do not type a username or password. Click **Save & Connect**.

<img src="screenshots/lab1-14-compass-new-connection.png" alt="Compass new connection with mongodb://localhost:27017" width="640">

3. The sidebar lists the saved connection. A brand-new server shows `admin`, `config`, and `local` only. `training_store` appears after the first lab write.

<img src="screenshots/lab1-15-compass-connected.png" alt="Compass connected to localhost:27017 showing admin, config, and local" width="640">

---

## 3. Install `mongosh`

The server MSI does not include `mongosh`. Install the shell from its own MSI (these screens show **2.12.0**). Use the **msi** package. A zip download leaves `mongosh.exe` in a `bin` folder that is not on your PATH.

1. Open [MongoDB Shell](https://www.mongodb.com/try/download/shell).
2. Choose the current version, **Windows x64 (10+)**, package **msi**, then **Download**.

<img src="screenshots/lab1-09-download-mongosh.png" alt="MongoDB Shell download: version 2.12.0, Windows x64, msi" width="640">

3. Run the MSI. On the welcome page, click **Next**.

<img src="screenshots/lab1-10-mongosh-welcome.png" alt="MongoDB Shell setup wizard welcome; Next is selected" width="640">

4. If a license page appears, accept it and click **Next**. On **Destination Folder**, leave the folder the wizard shows (under your own user profile) and leave **Install just for you** checked. Click **Next**.

<img src="screenshots/lab1-11-mongosh-destination.png" alt="Destination folder with Install just for you checked" width="640">

5. Click **Install**.

<img src="screenshots/lab1-12-mongosh-ready.png" alt="Ready to install MongoDB Shell; Install is selected" width="640">

6. Click **Finish**.

<img src="screenshots/lab1-13-mongosh-finished.png" alt="MongoDB Shell setup completed; Finish is selected" width="640">

7. Close any open PowerShell windows, including the terminal in VS Code or Cursor, so the new PATH is picked up. Open a new window before you run `mongosh --version`. It should print `2.12.0`.

---

## 4. Install MongoDB Database Tools

Database Tools are a separate MSI (these screens show **100.19.0**). The server installer does not include `mongodump` or `mongorestore`, and this MSI does not add them to your PATH.

1. Open [MongoDB Database Tools](https://www.mongodb.com/try/download/database-tools).
2. Choose the current **100.x** version, platform **Windows x86_64**, package **msi**, then **Download**.

<img src="screenshots/lab1-16-download-database-tools.png" alt="Database Tools download: version 100.19.0, Windows x86_64, msi" width="640">

3. Run the MSI. On the welcome page, click **Next**.

<img src="screenshots/lab1-17-tools-welcome.png" alt="MongoDB Tools 100 setup wizard welcome; Next is selected" width="640">

4. Check **I accept the terms in the License Agreement**, then click **Next**.

<img src="screenshots/lab1-18-tools-license.png" alt="Database Tools license agreement accepted" width="640">

5. On **Custom Setup**, leave **MongoDB Tools 100** selected and accept the location `C:\Program Files\MongoDB\Tools\100\`. Click **Next**. The wizard installs immediately. Do not click **Cancel**.

<img src="screenshots/lab1-19-tools-custom-setup.png" alt="Custom Setup location C:\Program Files\MongoDB\Tools\100" width="640">

<img src="screenshots/lab1-20-tools-installing.png" alt="Database Tools installer progress; Cancel is available but should not be clicked" width="640">

6. Click **Finish**.

<img src="screenshots/lab1-21-tools-finished.png" alt="MongoDB Tools 100 setup completed; Finish is selected" width="640">

7. The commands are in `C:\Program Files\MongoDB\Tools\100\bin`. Add that folder to your user **Path** (the `100` folder matches this installer):
   - Start → “environment variables” → **Edit environment variables for your account**
   - Select **Path** → **Edit** → **New** → paste `C:\Program Files\MongoDB\Tools\100\bin`
   - Click **OK** on the path list, then **OK** on the Environment Variables window

The new entry is the last line. The line above it is the `mongosh` folder from its own installer. Click **OK**. The other lines in that list are this computer’s existing folders. Leave them as they are.

<img src="screenshots/lab1-21b-tools-bin-on-path.png" alt="User Path with mongosh and MongoDB Tools 100 bin as the last entries" width="640">

8. A PowerShell window that was already open keeps the old Path, so `mongosh`, `mongodump`, and `mongorestore` all fail there even after the installers succeed.

<img src="screenshots/lab1-23-stale-powershell.png" alt="An already-open PowerShell does not recognize mongodump, mongorestore, or mongosh" width="640">

Close that window. In a new window, if `mongodump` is still not recognized, reload Path from the saved settings and try again:

```powershell
$env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User")
mongosh --version
mongodump --version
mongorestore --version
```

`mongosh --version` should print `2.12.0`. `mongodump --version` and `mongorestore --version` should print `100.19.0`.

<img src="screenshots/lab1-24-path-reload-versions.png" alt="After reloading Path, mongosh 2.12.0 and Database Tools 100.19.0" width="640">

An Administrator window can see this Path before a normal window does, because elevation reads the saved Path fresh. Sign out of Windows and back in so every new normal window sees it without the reload line.

---

## 5. Get the course folder

Labs load data with a path relative to the repository root. Open that folder in VS Code or Cursor; do not run the commands from `C:\Users\<you>`.

With Git:

```powershell
git clone <repository-url>
cd MasteringMongoDB
```

Or unzip the folder the instructor sends, then `cd` into `MasteringMongoDB`.

You should see `datasets\training_store\load.js` and `labs\`.

---

## 6. Confirm the machine is ready

Open a **new** PowerShell window (so PATH changes apply). Run these in order.

**Service is running**

```powershell
Get-Service MongoDB
```

Expected: `Status : Running`.

<img src="screenshots/lab1-25-service-and-port.png" alt="MongoDB service Running, and Test-NetConnection reports TcpTestSucceeded True" width="640">

If it says `Stopped`, open PowerShell **as Administrator** and run:

```powershell
Start-Service MongoDB
```

**Port 27017 answers on this machine**

```powershell
Test-NetConnection localhost -Port 27017
```

Expected: `TcpTestSucceeded : True`.

PowerShell may also print `WARNING: TCP connect to (::1 : 27017) failed`. That line is IPv6. This server listens on `127.0.0.1` only, so the IPv4 row is the one that matters: `RemoteAddress : 127.0.0.1` and `TcpTestSucceeded : True`. The warning does not mean the install failed.

**Clients are on PATH**

```powershell
mongosh --version
mongodump --version
mongorestore --version
```

Each command prints a version. On this walkthrough that is `mongosh` **2.12.0** and Database Tools **100.19.0**. `mongosh is not recognized` or `mongodump is not recognized` means that installer is missing or the terminal was opened before PATH was updated.

**Shell can talk to the server**

```powershell
mongosh "mongodb://localhost:27017" --eval "db.runCommand({ ping: 1 })"
```

Expected: a document with `ok: 1`. Then type `exit` if a prompt is still open.

These three commands work from any folder. An Administrator window is not required.

<img src="screenshots/lab1-22-version-and-ping.png" alt="mongodump and mongorestore 100.19.0, and a ping that returns ok: 1" width="640">

**Compass**

Start Compass from the Start menu. **+ Add new connection** → `mongodb://localhost:27017` → **Save & Connect**. You should see the server. A brand-new server lists `admin`, `config`, and `local` only. `training_store` appears after the first lab write.

---

## Readiness checklist

Tick these before class. This is the same list as [Exercise 2.4](day-01/exercises/exercise-2.4-environment-readiness-checklist.md), filled in early.

- [ ] Windows 10 or 11, and you can open PowerShell
- [ ] MongoDB service `MongoDB` is **Running**
- [ ] `Test-NetConnection localhost -Port 27017` shows `TcpTestSucceeded : True`
- [ ] `mongosh --version` prints a version
- [ ] `mongosh "mongodb://localhost:27017"` reaches a prompt, and `db.runCommand({ ping: 1 })` returns `ok: 1`
- [ ] Compass opens and connects to `mongodb://localhost:27017`
- [ ] `mongodump --version` and `mongorestore --version` both print a version
- [ ] The course folder is on disk and contains `datasets\training_store\load.js`
- [ ] `mongod.cfg` still has `bindIp: 127.0.0.1` and port `27017`
- [ ] No password or full Atlas URI is saved in a file you might commit or share

Class then continues with [Lab 1 — Install, Connect and Verify](day-01/lab1/LAB-1-GUIDE.md).

---

## How each lab uses this setup

| When | What must already work |
|---|---|
| Day 1 Lab 1 | Server service, `mongosh`, Compass |
| Day 1 Lab 2 through Day 3 Lab 5 | Same local server, plus the course folder so `load.js` reloads `training_store` |
| Day 3 Lab 6 | The instructor’s replica-set or Atlas URI. A standalone `mongod` on `localhost` is not a replica set. |
| Day 3 Lab 7 | `mongodump` and `mongorestore` on PATH, local server on `localhost:27017` |
| Module 8 `sample-app` (optional) | Node.js 18+ **or** Python 3, and `$env:MONGODB_URI = "mongodb://localhost:27017"` |

Reload the sample data from the repository root whenever a lab tells you to:

```powershell
mongosh "mongodb://localhost:27017" .\datasets\training_store\load.js
```

That script drops and reloads `training_store`. Run it from PowerShell at the repo root, not from inside an already-open `mongosh` prompt.

---

## Docker instead of the MSI

Use this only if you cannot install the Windows service. You still install `mongosh`, Compass, and Database Tools on Windows.

```powershell
docker run -d --name mongo `
  -p 127.0.0.1:27017:27017 `
  -v mongo-data:/data/db `
  mongodb/mongodb-community-server
```

`-p 127.0.0.1:27017:27017` publishes the port on this machine only. The named volume keeps data across container restarts. Connect the same way: `mongodb://localhost:27017`. There is no `MongoDB` Windows service in this path; `docker ps` should show `mongo` running.

---

## Atlas instead of a local server

Use Atlas only when the instructor assigns it. Days 1–2 can run against Atlas. Lab 7’s dump and restore commands in the guide target `localhost:27017`; a local server is the path those steps assume.

1. Sign in to the Atlas project the instructor names.
2. Create a database user with `readWrite` on `training_store`. Do not reuse your Atlas login as the database user.
3. Under **Network Access**, add **your current public IP**. Do not add `0.0.0.0/0`.
4. Store the `mongodb+srv://` host in an environment variable **without** the password:

```powershell
$env:MONGODB_URI = "mongodb+srv://<cluster-host>/"
mongosh $env:MONGODB_URI --username <username>
```

`mongosh` prompts for the password. Do not put the password in the command, in a slide, or in chat.

---

## Security rules for the whole course

- Placeholders only in notes and chat: `<connection-string>`, `<username>`, `<password>`.
- Let `mongosh` and Compass prompt for the password.
- Keep the local server on `127.0.0.1`. Do not open port 27017 on the Windows firewall for other machines.
- Do not enable authentication or create users on a shared classroom instance unless the instructor says to.

---

## If something fails

Change one thing, then retry `mongosh "mongodb://localhost:27017" --eval "db.runCommand({ ping: 1 })"`.

| What you see | What to do |
|---|---|
| `Get-Service MongoDB` → `Stopped` | Administrator PowerShell: `Start-Service MongoDB` |
| `Start-Service` says access denied | The window is not elevated. Close it and choose **Run as administrator**. |
| `ECONNREFUSED` on `localhost:27017` | The service is stopped, or another program owns port 27017. Check the service, then `Test-NetConnection localhost -Port 27017`. |
| Service will not start | Open `C:\Program Files\MongoDB\Server\8.3\log\mongod.log` (use your installed version). Typical causes: the data directory is missing or not writable, or port 27017 is already taken. |
| `mongosh`, `mongodump`, and `mongorestore` are all not recognized in a window that was already open | That window kept the Path from before the install. Close it. In a new window run `$env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User")`, then the version commands. Sign out and back in so later windows do not need that line. |
| `mongosh` is not recognized in a new window | Install the shell MSI (the **msi**, not the zip), then open a new PowerShell window. |
| `mongodump` is not recognized in a new window, but an Administrator window works | The tools `bin` folder is saved, and this sign-in has not reloaded it. Run the Path reload line above, then sign out and back in. |
| Compass connects but shows no new documents | Use the same URI as `mongosh` (`mongodb://localhost:27017`) and refresh the collection. |
| `mongosh` works in one terminal and not another | The second terminal was opened before install. Close it and open a new one. |

Full connection-failure table used in class: [Exercise 2.3](day-01/exercises/exercise-2.3-diagnose-connection-failures.md).

---

## Related pages

- [Lab 1 — Install, Connect and Verify](day-01/lab1/LAB-1-GUIDE.md)
- [Exercise 2.4 — Environment Readiness Checklist](day-01/exercises/exercise-2.4-environment-readiness-checklist.md)
- [Sample dataset load](../datasets/README.md)
- [Application connection demo](../sample-app/README.md) (optional, Module 8)
