# Module 2: Installation and Setup

## 1. Choosing a Deployment Option

MongoDB can be installed in two main ways:

### Local deployment

MongoDB Community Edition runs directly on the learner’s computer.

Best for:

* Classroom exercises
* Offline development
* Learning administration commands
* Testing applications locally
* Understanding the `mongod` server process

### Cloud deployment

MongoDB Atlas is MongoDB’s managed cloud platform. Atlas handles much of the infrastructure, maintenance and configuration.

Best for:

* Team projects
* Remote access
* Cloud application development
* High availability
* Production-style practice

| Factor                    | Local MongoDB                  | MongoDB Atlas                 |
| ------------------------- | ------------------------------ | ------------------------------ |
| Internet required         | No, after installation         | Yes                           |
| Infrastructure management | Learner manages it             | Atlas manages it              |
| Initial setup             | Software installation          | Cloud account and cluster     |
| Default address           | `localhost:27017`              | Atlas connection URI          |
| Remote access             | Requires configuration         | Built in with access controls |
| Best use                  | Learning and local development | Cloud and team projects       |

---

## 2. Installing MongoDB Locally

A local MongoDB environment normally contains:

* **MongoDB Community Server** – runs the database
* **MongoDB Shell (`mongosh`)** – command-line client
* **MongoDB Compass** – optional graphical interface
* **MongoDB Database Tools** – optional import, export and backup utilities

MongoDB provides operating-system-specific Community Edition installation instructions. ([MongoDB Docs][1])

### Windows installation

1. Download MongoDB Community Server from the official MongoDB website.
2. Run the MSI installer.
3. Select **Complete** installation.
4. Install MongoDB as a Windows service.
5. Optionally install MongoDB Compass.
6. Install `mongosh` if it is not included in the selected package.
7. Verify that the MongoDB service is running.

The service can be checked from:

```text
Windows Services → MongoDB Server
```

It can also be checked from PowerShell:

```powershell
Get-Service MongoDB
```

Start it if necessary:

```powershell
Start-Service MongoDB
```

### macOS installation with Homebrew

The precise formula can depend on the current MongoDB tap and version, so learners should follow MongoDB’s current macOS installation page.

The general process is:

```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

Verify the installed tools:

```bash
mongod --version
mongosh --version
```

### Linux installation

On Linux, use MongoDB’s official repository for the specific distribution instead of assuming that the distribution’s default repository contains the appropriate package.

After installation, the service is normally managed with `systemctl`:

```bash
sudo systemctl start mongod
sudo systemctl status mongod
sudo systemctl enable mongod
```

### Important local components

```text
mongosh ──connection──> mongod ──reads/writes──> data files
 Client                  Server
```

* `mongod` is the database server.
* `mongosh` is the interactive shell.
* Stopping `mongosh` does not stop the database.
* If `mongod` is not running, the shell cannot connect.

By default, a local MongoDB server commonly listens on:

```text
Host: localhost
Port: 27017
```

---

## 3. Provisioning a MongoDB Atlas Deployment

MongoDB Atlas provides managed database deployments in the cloud.

### Basic provisioning process

1. Create or sign in to a MongoDB Atlas account.
2. Create an organization or use an existing one.
3. Create a project.
4. Create a database deployment.
5. Select the available free or paid configuration.
6. Select a cloud provider and region.
7. Create a database user.
8. Add your current IP address to the IP access list.
9. Obtain the deployment’s connection string.

Atlas requires an appropriate database user and an allowed client IP address before the client can connect. ([MongoDB Docs][2])

### Database user versus Atlas user

These are separate identities:

* **Atlas user** signs in to the Atlas website.
* **Database user** authenticates when connecting to MongoDB.

Creating an Atlas account does not automatically mean the same credentials should be placed in the database connection string.

### Network access

Atlas blocks unapproved network locations. Add only the IP addresses that need access.

For a temporary learning environment, users sometimes allow access from anywhere:

```text
0.0.0.0/0
```

That setting is convenient but broad. It should be combined with strong credentials and should generally be avoided for production deployments.

### Atlas connection string

An Atlas URI normally follows this pattern:

```text
mongodb+srv://<username>:<password>@<cluster-host>/
```

Example:

```bash
mongosh "mongodb+srv://cluster0.example.mongodb.net/" \
  --username trainingUser
```

It is safer to let `mongosh` prompt for the password instead of placing the password directly in the command or shell history.

Atlas supports connecting through `mongosh`, application drivers and MongoDB Compass. ([MongoDB Docs][3])

---

## 4. Connecting Through the MongoDB Shell

`mongosh` is MongoDB’s interactive command-line shell.

It allows developers and administrators to:

* Create databases and collections
* Insert and query documents
* Create indexes
* Run aggregation pipelines
* Inspect server information
* Perform administrative operations

### Connecting to local MongoDB

If MongoDB is running locally on the standard port, enter:

```bash
mongosh
```

This is equivalent to connecting to:

```bash
mongosh "mongodb://localhost:27017"
```

MongoDB’s documentation confirms that `mongosh` without additional options connects to a local `mongod` using the default port. ([MongoDB Docs][4])

To connect directly to a database:

```bash
mongosh "mongodb://localhost:27017/training_store"
```

### Connecting with authentication

```bash
mongosh "mongodb://localhost:27017/training_store" \
  --username trainingUser
```

The shell prompts for the password.

### Connecting to Atlas

From the Atlas interface:

1. Open the database deployment.
2. Select **Connect**.
3. Choose **Shell**.
4. Copy the generated command.
5. Replace or enter the required username.
6. Enter the password when prompted.

Example:

```bash
mongosh "mongodb+srv://cluster0.example.mongodb.net/" \
  --username trainingUser
```

The exact Atlas connection command should be copied from the Atlas **Connect** dialog because the cluster hostname is deployment-specific. ([MongoDB Docs][2])

---

## 5. Verifying the Environment

After connecting, the shell displays a prompt similar to:

```text
test>
```

The word `test` represents the currently selected database.

### Check the shell version

Run this from the operating-system terminal:

```bash
mongosh --version
```

### Check the server version

Run this inside `mongosh`:

```javascript
db.version()
```

### Check the current database

```javascript
db
```

Expected initial result:

```text
test
```

### Check the connection

```javascript
db.getMongo()
```

This displays information about the current MongoDB connection.

### Display databases

```javascript
show dbs
```

A newly selected database does not appear in `show dbs` until it contains stored data.

### Display available collections

```javascript
show collections
```

If the current database is empty, no collections will be displayed.

---

## 6. First MongoDB Commands

We will use the `training_store` e-commerce case study.

### Select a database

```javascript
use training_store
```

This switches the current database context. It does not immediately create physical data.

Verify it:

```javascript
db
```

Expected output:

```text
training_store
```

### Create the first collection

A collection can be created explicitly:

```javascript
db.createCollection("products")
```

Expected result:

```javascript
{ ok: 1 }
```

MongoDB can also create a collection automatically when the first document is inserted.

### Insert the first document

```javascript
db.products.insertOne({
  name: "Wireless Mouse",
  category: "Electronics",
  price: 39.99,
  stock: 120
})
```

MongoDB adds an `_id` field if one is not supplied:

```javascript
{
  acknowledged: true,
  insertedId: ObjectId("...")
}
```

### Retrieve the document

```javascript
db.products.find()
```

A more targeted query is:

```javascript
db.products.find({
  category: "Electronics"
})
```

### Insert multiple documents

```javascript
db.products.insertMany([
  {
    name: "Mechanical Keyboard",
    category: "Electronics",
    price: 89.99,
    stock: 45
  },
  {
    name: "MongoDB Fundamentals",
    category: "Books",
    price: 49.99,
    stock: 75
  }
])
```

### Count documents

```javascript
db.products.countDocuments()
```

Expected result:

```text
3
```

### Verify the database and collection

```javascript
show dbs
show collections
```

The environment should now contain:

```text
training_store
    └── products
          ├── Wireless Mouse
          ├── Mechanical Keyboard
          └── MongoDB Fundamentals
```

---

## 7. Basic Update and Delete Verification

### Update a document

```javascript
db.products.updateOne(
  { name: "Wireless Mouse" },
  { $set: { stock: 110 } }
)
```

Verify the change:

```javascript
db.products.findOne({
  name: "Wireless Mouse"
})
```

### Delete a document

```javascript
db.products.deleteOne({
  name: "MongoDB Fundamentals"
})
```

Confirm the number of remaining documents:

```javascript
db.products.countDocuments()
```

These commands verify the four basic CRUD operations:

| Operation | MongoDB command         |
| --------- | ------------------------ |
| Create    | `insertOne()`           |
| Read      | `find()` or `findOne()` |
| Update    | `updateOne()`           |
| Delete    | `deleteOne()`           |

---

## 8. Common Connection Problems

### `mongosh: command not found`

Possible causes:

* `mongosh` is not installed.
* Its executable directory is not in the system `PATH`.
* The terminal was not reopened after installation.

### Connection refused on `localhost:27017`

Possible causes:

* The `mongod` service is stopped.
* MongoDB is listening on a different port.
* Its configuration file contains a different network binding.
* Another program or security setting is blocking the port.

### Atlas authentication failed

Check:

* Database username
* Database password
* Authentication database
* User permissions
* Special characters in credentials

### Atlas connection timeout

Check:

* The current IP is in the Atlas IP access list.
* The deployment is available.
* The internet connection is active.
* A corporate firewall is not blocking the connection.
* The correct connection string was copied.

---

## Practical Lab

By the end of this module, learners should be able to:

1. Install MongoDB locally or create an Atlas deployment.
2. Verify that `mongod` is running.
3. Connect using `mongosh`.
4. Create the `training_store` database.
5. Create the `products` collection.
6. Insert, retrieve, update and delete documents.
7. Diagnose basic installation and connection errors.

The successful final check is:

```javascript
use training_store

db.products.find()

db.runCommand({ ping: 1 })
```

A successful ping returns a result containing:

```javascript
{ ok: 1 }
```
