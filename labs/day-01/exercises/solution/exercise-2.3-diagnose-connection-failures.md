# Exercise 2.3 — solution (instructor)

**Module 2** · Day 1 · Checkpoint C  
**Type:** troubleshooting analysis · **Do not hand this sheet to participants.**

Worksheet: [`../exercise-2.3-diagnose-connection-failures.md`](../exercise-2.3-diagnose-connection-failures.md) · Deck slide 46

## Running it

Twelve minutes of work, then a three-minute debrief. You may project the "Common Connection Problems" and "A Troubleshooting Workflow" slides. Don't break a working classroom cluster unless you have set up a sandbox.

## Solution

| Case | Likely cause | First check | Log or setting | Fix | Verification |
| --- | --- | --- | --- | --- | --- |
| 1 `ECONNREFUSED` | Server stopped or wrong port (or `bindIp` doesn't include the address) | Is `mongod` running? On port 27017? | Service status (`Get-Service MongoDB`); `net.port`, `net.bindIp` in `mongod.conf` | Start the service (`Start-Service MongoDB`, Administrator) or fix the port in the URI | `mongosh`, then ping |
| 2 Authentication failed | Wrong user, password or `authSource`; unencoded special characters | Retry with a known-good user | Authentication failure lines in the `mongod` log | Correct the credentials or `authSource`; percent-encode the password | Authenticated `show dbs` |
| 3 Server-selection timeout | Firewall, routing or the Atlas IP access list | Can you reach host:port? (`Test-NetConnection <host> -Port 27017`) | Atlas IP access list; local firewall; TLS settings | Allow **your current IP** (not `0.0.0.0/0`); check TLS | Ping from the same client |
| 4 DNS lookup failure | Bad hostname or DNS | Resolve the hostname (`Resolve-DnsName <host>`) | Host in the URI; DNS; VPN | Fix the hostname; check the VPN | Fresh `mongosh` with the corrected URI |
| 5 Unauthorized command | The user authenticated, but the role is too weak | Which user and which role? | User privileges (`db.getUser("<username>")`) | Grant the required role (for example `readWrite` on `training_store`) | Retry the command |
| 6 Invalid URI format | Syntax or encoding: wrong scheme, extra or missing `@`, unencoded characters | Read the whole URI | Scheme, `@`, percent-encoding | Repair the URI; percent-encode the password | Connect with the repaired URI |

**Verification command for connectivity:** `db.runCommand({ ping: 1 })` — expect `{ ok: 1 }`.

## Distinctions to insist on

- **Refused vs timeout.** Refused comes back fast: the host answered, but nothing listens on that port. Timeout means no answer at all: something (firewall, routing, allowlist) is dropping the traffic.
- **Unauthenticated vs unauthorized.** Authentication failed = "who are you?" failed. Unauthorized = you logged in, but your role doesn't allow the command.

## The habit

Change **one** variable, then retest with the simplest client: `mongosh` and `db.runCommand({ ping: 1 })`. Walk the layers in order: process → port and bindIp → credentials → network and TLS.
