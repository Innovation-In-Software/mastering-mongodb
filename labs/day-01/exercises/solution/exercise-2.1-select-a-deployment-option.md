# Exercise 2.1 — solution (instructor)

**Module 2** · Day 1 · Checkpoint A  
**Type:** design discussion · **Do not hand this sheet to participants.**

Worksheet: [`../exercise-2.1-select-a-deployment-option.md`](../exercise-2.1-select-a-deployment-option.md) · Deck slide 44

## Running it

Eight minutes of pair work, then a two-minute debrief. Reveal the solution column only after pairs share one controversial row. No MongoDB is needed.

## Task 1 — A good fit for each option

| Option | A good fit when… |
| --- | --- |
| Local installation (Community Edition) | You are learning or developing on one machine, possibly offline; `localhost:27017`, private by default. |
| Self-managed server or VM | You need direct control of the operating system, network and data location — and accept patching, backups and monitoring. |
| Container (Docker) | You need a portable, isolated server that is quick to create and remove — tests and demos. Mount a named volume if the data must survive. |
| Managed cloud (MongoDB Atlas) | A team needs shared access, or you want the vendor to run servers, patches, backups and scaling. You still own database users, the IP access list and the secret URI. |

## Tasks 2 and 3 — Solution

| # | Recommended option | Justification (constraint) | Main risk | A workable alternative |
| --- | --- | --- | --- | --- |
| 1 Offline learner | **Local installation** | No internet needed after installation. | Data lost with the laptop; no shared access. | Docker on localhost, if Docker is already installed |
| 2 Temporary testing | **Container** | Disposable: created and removed in seconds, same image every run. | Data lost when the container is removed without a volume (acceptable for tests). | A throwaway Atlas free-tier cluster, but it needs internet and credentials |
| 3 Distributed team | **Managed cloud** | Shared access from many places, no server to run. | Needs internet; the IP access list and credentials must be managed. | Self-managed server with VPN access — more operations work |
| 4 Direct infrastructure control | **Self-managed server or VM** | The organization must control the OS, network and data location. | You own patching, backups, monitoring and security hardening. | Managed cloud in an approved region, if the regulator accepts it |
| 5 Minimal operations | **Managed cloud** | No servers to manage; the vendor patches, backs up and scales. | Cost grows with use; credentials and the IP allowlist are still your job. | — |
| 6 Restricted internet | **Local installation or a local server** | The classroom cannot rely on the internet. | Each machine must be installed and verified; no shared data unless a local server is provided. | Docker, if the image was pulled in advance |

## Debrief

The database commands are largely the same across options. **Infrastructure responsibility** is what changes — who runs the server, who patches it and who controls network access.

## What you want to hear

- Each justification names a constraint: offline, disposable, shared, control, operations load or network. A product name alone ("Atlas, because it's popular") doesn't count.
- Container risk mentions the volume.
- Managed cloud risk mentions internet access **and** that the customer still manages users and the IP access list.
- No one proposes opening a server or an Atlas access list to `0.0.0.0/0` to make a shared option "easier".
