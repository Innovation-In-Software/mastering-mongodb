#!/usr/bin/env python3
"""Expand collapsed bullet lists so every numbered point carries an explanation.

Some bullets in `moduleNN_content.py` list several numbered items bare --
"4. Chatty Services, 5. Anemic Services, 6. Centralized Data" -- while their
neighbours read "1. Too Many Services: creating a service for every feature
leads to unnecessary complexity". This module supplies the missing explanations
so each point stands on its own.

Applied at build time by `mdb_deck_kit.expand_bullets()`, keyed on the
original text with whitespace collapsed. Keeping the mapping here rather than
rewriting the content modules leaves those files free for separate editing.
"""
from __future__ import annotations

EXPANSIONS: dict[str, list[str]] = {
    # ---- Module 1 ------------------------------------------------------
    "4. Testing Complexity, 5. Organizational Overhead, 6. Higher Cost at Small Scale": [
        "4. Testing Complexity: end-to-end paths span services, so contract and integration tests replace simple in-process tests",
        "5. Organizational Overhead: more teams means more coordination, on-call rotas, and shared standards to agree",
        "6. Higher Cost at Small Scale: fixed platform and tooling costs are hard to justify for a small product or team",
    ],
    "4. Low Scale Needs, 5. Limited Budget, 6. Fast Time to Market, 7. Tight Feedback Loop, 8. Low Operational Maturity": [
        "4. Low Scale Needs: traffic fits comfortably on one deployable, so independent scaling buys nothing",
        "5. Limited Budget: one runtime, one pipeline, and one database keep infrastructure and tooling spend low",
        "6. Fast Time to Market: no service boundaries to negotiate means features ship as soon as they are written",
        "7. Tight Feedback Loop: a single codebase is quick to run, debug, and refactor end to end",
        "8. Low Operational Maturity: without CI/CD, observability, and on-call in place, distribution adds risk you cannot absorb",
    ],
    "4. Technology Diversity, 5. Improve Resilience, 6. Faster Feature Delivery, 7. Integration and Ecosystem, 8. Data Ownership": [
        "4. Technology Diversity: pick the language, framework, or data store each workload actually needs",
        "5. Improve Resilience: isolate failures so one struggling service cannot take the whole platform down",
        "6. Faster Feature Delivery: small, independently deployable units release without a system-wide cycle",
        "7. Integration and Ecosystem: expose capabilities as APIs and events for partners and internal consumers",
        "8. Data Ownership: each service owns its schema and lifecycle, ending contention over one shared database",
    ],
    "4. Slow Feature Delivery, 5. High Defect Impact, 6. Data and Technology Constraints, 7. Tight Coupling, 8. Business Agility Needs": [
        "4. Slow Feature Delivery: release cycles stretch because every change waits on a full regression and deploy",
        "5. High Defect Impact: one bad change can take down unrelated functionality; the blast radius is the whole app",
        "6. Data and Technology Constraints: one schema and one stack force compromises on workloads with different needs",
        "7. Tight Coupling: modules reach into each other's internals, so no part can change or deploy on its own",
        "8. Business Agility Needs: the business wants to fund, staff, and release capabilities independently",
    ],
    "4. Chatty Services, 5. Anemic Services, 6. Centralized Data or Business Logic": [
        "4. Chatty Services: one user action fans out into many small calls, multiplying latency and failure points",
        "5. Anemic Services: a service that only forwards CRUD to a table carries cost without owning any behaviour",
        "6. Centralized Data or Business Logic: a shared database or rules engine recreates the monolith behind the services",
    ],
    "7. Big Bang Migration, 8. Distributed Monolith, 9. Over-Engineering Resilience, 10. Ignoring Observability": [
        "7. Big Bang Migration: rewriting everything at once maximises risk and delays any delivered value",
        "8. Distributed Monolith: services that must deploy together give you network cost with none of the autonomy",
        "9. Over-Engineering Resilience: retries and breakers everywhere add complexity and can amplify load",
        "10. Ignoring Observability: without logs, metrics, and traces a distributed failure is effectively undebuggable",
    ],

    # ---- Module 3 ------------------------------------------------------
    "1. Evaluate before adding 2. Use official sources 3. Pin versions": [
        "1. Evaluate before adding: check licence, maintenance activity, and whether the standard library already covers it",
        "2. Use official sources: pull from Maven Central or an approved internal mirror, never an untrusted copy",
        "3. Pin versions: declare exact versions so every build and environment resolves the same artifacts",
    ],
    "4. Manage transitive dependencies 5. Scan continuously": [
        "4. Manage transitive dependencies: use dependencyManagement or a BOM so indirect versions cannot drift",
        "5. Scan continuously: run vulnerability scanning in the pipeline, not as an occasional manual review",
    ],
    "6. Update regularly 7. Review licenses 8. Remove unused dependencies": [
        "6. Update regularly: small frequent upgrades are far cheaper than a forced jump several major versions later",
        "7. Review licenses: confirm each licence is compatible with how the bank distributes and runs the software",
        "8. Remove unused dependencies: every unused library is attack surface and build time you gain nothing from",
    ],

    # ---- Module 7 ------------------------------------------------------
    "1. Perimeter security 2. Identity and access management 3. Network security": [
        "1. Perimeter security: gateways, WAF, and TLS termination filter hostile traffic before it reaches a service",
        "2. Identity and access management: authenticate every caller and authorise each request against roles and scopes",
        "3. Network security: segment traffic and default to deny so services reach only what they must",
    ],
    "4. Workload security 5. Application security 6. Data protection 7. Monitoring and response": [
        "4. Workload security: run containers non-root and read-only, from scanned and signed images",
        "5. Application security: validate input, encode output, and handle errors without leaking internals",
        "6. Data protection: encrypt in transit and at rest, and minimise what is stored and logged",
        "7. Monitoring and response: detect, alert, and act, because prevention alone will not hold indefinitely",
    ],
    "1. Input validation 2. Authentication & authorization 3. Data protection 4. Error handling & logging": [
        "1. Input validation: constrain type, length, format, and range at the edge; reject rather than sanitise",
        "2. Authentication & authorization: verify who is calling and what they may do, on every request",
        "3. Data protection: encrypt sensitive fields and keep secrets out of code and configuration files",
        "4. Error handling & logging: return a safe, consistent error shape and keep the detail in server-side logs",
    ],
    "5. Dependencies & components 6. Session management 7. Communication security 8. Code quality & best practices": [
        "5. Dependencies & components: pin, scan, and patch third-party libraries as part of the build",
        "6. Session management: prefer short-lived tokens and never trust client-supplied identity claims",
        "7. Communication security: require TLS between services and validate certificates properly",
        "8. Code quality & best practices: review, lint, and test, because most vulnerabilities enter as ordinary defects",
    ],
    "1. Preparation 2. Detection & analysis 3. Containment": [
        "1. Preparation: agree roles, runbooks, and contacts before an incident, not during one",
        "2. Detection & analysis: confirm what is happening, how far it reaches, and what data is involved",
        "3. Containment: stop the spread first -- isolate, revoke, or disable before cleaning up",
    ],
    "4. Eradication & recovery 5. Lessons learned": [
        "4. Eradication & recovery: remove the cause, restore service, and verify the system is genuinely clean",
        "5. Lessons learned: run a blameless review and turn the findings into concrete engineering work",
    ],

    # ---- Module 8 ------------------------------------------------------
    "1. Functional testing 2. Data & persistence testing 3. Integration testing": [
        "1. Functional testing: business rules and API contracts behave as specified for valid and invalid input",
        "2. Data & persistence testing: migrations apply cleanly and repositories read and write what you expect",
        "3. Integration testing: the service works against real collaborators, not only against mocks",
    ],
    "4. Resilience & reliability testing 5. Performance testing": [
        "4. Resilience & reliability testing: timeouts, retries, breakers, and fallbacks behave under failure",
        "5. Performance testing: latency and throughput hold at expected load, with headroom for peaks",
    ],
    "6. Security testing 7. Observability testing 8. Configuration & environment": [
        "6. Security testing: authentication, authorisation, and input validation are enforced, not assumed",
        "7. Observability testing: logs, metrics, and traces actually appear and carry correlation IDs",
        "8. Configuration & environment: one artifact runs everywhere, configured only from outside",
    ],
    "9. Quality & test coverage 10. Deployment readiness": [
        "9. Quality & test coverage: coverage is meaningful on the paths that carry risk, not just a percentage",
        "10. Deployment readiness: probes, resource limits, rollout strategy, and rollback are all in place",
    ],

    # ---- Module 9 ------------------------------------------------------
    "1. Create 2. Inject 3. Transmit 4. Extract 5. Continue (new span linked to the trace)": [
        "1. Create: the first service starts a trace and generates the trace and span identifiers",
        "2. Inject: those identifiers are written into outbound headers before the call leaves",
        "3. Transmit: the headers travel with the request over HTTP or alongside the message",
        "4. Extract: the receiving service reads the identifiers back out of the incoming request",
        "5. Continue: it opens a new span linked to the same trace, keeping the path connected end to end",
    ],
    "1. Be specific 2. Be actionable 3. Be timely": [
        "1. Be specific: say what broke and where, so nobody has to guess which service is involved",
        "2. Be actionable: every alert points at something a human can actually do right now",
        "3. Be timely: fire early enough to act, late enough to avoid noise from transient blips",
    ],
    "4. Be relevant 5. Be noise-free 6. Be reviewed": [
        "4. Be relevant: route to the team that owns the service, not to a channel everyone ignores",
        "5. Be noise-free: an alert that is routinely dismissed trains people to ignore the real one",
        "6. Be reviewed: prune and tune alerts regularly, because systems and thresholds drift",
    ],
    "1. Focus on outcomes 2. Route and escalate 3. Tune and test": [
        "1. Focus on outcomes: alert on user-visible symptoms rather than on every internal metric",
        "2. Route and escalate: send to the owning team first, with a defined path if nobody responds",
        "3. Tune and test: adjust thresholds against real incidents, and verify the alerts actually fire",
    ],
    "4. Deduplicate 5. Suppress intelligently 6. Continuously improve": [
        "4. Deduplicate: group related alerts so one failure produces one page, not fifty",
        "5. Suppress intelligently: silence downstream alerts during a known upstream outage or deployment",
        "6. Continuously improve: feed every noisy page back into the alert definitions",
    ],
    "1. Detect 2. Assess 3. Gather data 4. Analyze": [
        "1. Detect: an alert or a customer report signals that something is wrong",
        "2. Assess: judge severity, scope, and customer impact to set the response level",
        "3. Gather data: pull logs, metrics, and traces for the affected window and correlation IDs",
        "4. Analyze: form a hypothesis from the evidence rather than from the loudest guess",
    ],
    "5. Resolve 6. Verify 7. Document & improve": [
        "5. Resolve: apply the fix, rollback, or mitigation that restores service fastest",
        "6. Verify: confirm from metrics and traces that the symptom is genuinely gone",
        "7. Document & improve: record the timeline and cause, then fix what let it happen",
    ],

    # ---- Module 10 -----------------------------------------------------
    "1. Prepare app 2. Build image 3. Push image 4. Deploy 5. Expose 6. Access": [
        "1. Prepare app: externalise configuration, add health probes, and produce a runnable JAR",
        "2. Build image: layer the JAR into a container that runs as a non-root user",
        "3. Push image: publish to a registry with an immutable, versioned tag",
        "4. Deploy: create the Deployment so OpenShift schedules and supervises the pods",
        "5. Expose: add a Service for in-cluster traffic and a Route for external access",
        "6. Access: verify through the Route, then confirm probes and logs look healthy",
    ],
    "1. Application deployment 2. Configuration & secrets 3. Security": [
        "1. Application deployment: immutable image tags, declared resources, and a defined rollout strategy",
        "2. Configuration & secrets: ConfigMaps and Secrets injected at runtime, never baked into the image",
        "3. Security: non-root containers, least-privilege service accounts, and scanned images",
    ],
    "4. Networking 5. Storage & persistence": [
        "4. Networking: Services, Routes, and network policies that expose only what must be reachable",
        "5. Storage & persistence: persistent volumes for state, with backup and restore actually tested",
    ],
    "6. Observability 7. Resilience & scalability 8. CI/CD & release 9. Operations": [
        "6. Observability: logs, metrics, traces, and dashboards wired up before go-live",
        "7. Resilience & scalability: probes, replicas, autoscaling, and sensible limits under load",
        "8. CI/CD & release: an automated pipeline with quality gates, plus a rehearsed rollback",
        "9. Operations: runbooks, on-call ownership, and alerting that reaches the right team",
    ],

    # ---- Module 11 -----------------------------------------------------
    "1. Create short-lived branch 2. Develop 3. Pull request 4. Code review": [
        "1. Create short-lived branch: branch from trunk for hours or days, never weeks",
        "2. Develop: keep the change small and focused so it can be reviewed quickly",
        "3. Pull request: open early so CI and reviewers see the work while it is still small",
        "4. Code review: a second pair of eyes on correctness, security, and clarity",
    ],
    "5. Merge to trunk (multiple times a day) 6. Automate & deliver": [
        "5. Merge to trunk: integrate several times a day so conflicts stay small and trunk stays releasable",
        "6. Automate & deliver: every merge builds, tests, and can be promoted without manual steps",
    ],
    "1. Create branch 2. Make changes 3. Open PR 4. Code review 5. Approve 6. Merge": [
        "1. Create branch: isolate the change so trunk stays deployable while you work",
        "2. Make changes: commit in small logical steps that are easy to follow",
        "3. Open PR: describe intent and risk so a reviewer knows what to look for",
        "4. Code review: check correctness, security, tests, and readability",
        "5. Approve: record explicit sign-off, which doubles as the audit trail",
        "6. Merge: integrate once checks are green, then delete the branch",
    ],
    "1. Identify 2. Analyze 3. Assess 4. Report 5. Remediate": [
        "1. Identify: inventory every direct and transitive dependency in the build",
        "2. Analyze: match those components against known vulnerability and licence databases",
        "3. Assess: judge real exploitability and impact in your context, not just the raw score",
        "4. Report: produce an SBOM and findings that audit and security teams can consume",
        "5. Remediate: upgrade, patch, replace, or document an accepted risk with a named owner",
    ],
    "1. Scan 2. Detect 3. Alert 4. Remediate 5. Prevent": [
        "1. Scan: check commits, history, and build output for credential-shaped strings",
        "2. Detect: match against known patterns and entropy heuristics to find likely secrets",
        "3. Alert: notify the owning team immediately, because the exposure is already live",
        "4. Remediate: rotate the credential first, then remove it from history",
        "5. Prevent: add pre-commit hooks and pipeline gates so the next one never lands",
    ],
    "1. Create/Plan 2. Branch 3. Develop 4. Pull Request 5. Review & Feedback 6. Merge & Automate": [
        "1. Create/Plan: capture the work as an issue so intent and acceptance criteria are visible",
        "2. Branch: cut a short-lived branch from trunk for that single piece of work",
        "3. Develop: commit small, focused changes with tests alongside the code",
        "4. Pull Request: open it early and link the issue so reviewers have the context",
        "5. Review & Feedback: address comments and automated checks until the change is green",
        "6. Merge & Automate: merge to trunk and let the pipeline build, test, and deploy",
    ],
    "1. Source checkout 2. Dependency resolution 3. Compile & build 4. Unit test 5. Integration test": [
        "1. Source checkout: fetch the exact commit so the build is reproducible and traceable",
        "2. Dependency resolution: resolve pinned versions from an approved repository",
        "3. Compile & build: produce the artifact once, and promote that same artifact onwards",
        "4. Unit test: verify business logic in isolation, fast enough to run on every commit",
        "5. Integration test: exercise the service against real collaborators such as a database or broker",
    ],
    "6. Contract test 7. Security & quality gates 8. Package artifact 9. Build container image 10. Push & deploy": [
        "6. Contract test: prove the API still satisfies what consumers depend on before release",
        "7. Security & quality gates: fail the build on vulnerabilities, coverage drops, or code smells",
        "8. Package artifact: produce the versioned JAR that the rest of the pipeline promotes",
        "9. Build container image: layer that artifact into a scanned, non-root image",
        "10. Push & deploy: publish with an immutable tag, then roll out and smoke-test",
    ],
    "1. Source code 2. Dependency resolution 3. Build 4. Package (JAR/WAR or container image) 5. Store": [
        "1. Source code: the versioned commit that everything downstream is built from",
        "2. Dependency resolution: pull the declared libraries at their pinned versions",
        "3. Build: compile and test, failing fast before anything is packaged",
        "4. Package: produce a JAR, WAR, or container image as a single immutable unit",
        "5. Store: publish to a registry or repository so every environment pulls the same build",
    ],
    "1. Source code 2. Dockerfile 3. Build image 4. Image created 5. Push to registry": [
        "1. Source code: the application plus its build file, at a known commit",
        "2. Dockerfile: declares the base image, the layers, and the non-root user to run as",
        "3. Build image: assemble the layers, keeping dependencies and application code separate",
        "4. Image created: a self-contained, immutable artifact tagged with its version",
        "5. Push to registry: publish so OpenShift and every environment pull the identical image",
    ],

    # ---- Module 12 -----------------------------------------------------
    "1. Untrusted (external world) 2. MCP perimeter (gateway, WAF)": [
        "1. Untrusted (external world): anything outside your control -- assume every input here is hostile",
        "2. MCP perimeter (gateway, WAF): the first controlled hop, where traffic is authenticated and filtered",
    ],
    "3. MCP server zone 4. Backend services zone 5. Data zone": [
        "3. MCP server zone: where tools are exposed, each with an explicit scope and audit trail",
        "4. Backend services zone: the microservices behind the tools, reachable only through defined APIs",
        "5. Data zone: the stores themselves, the most restricted layer and never reachable directly",
    ],
    "1. Embedded (in-service) 2. Sidecar 3. Centralized gateway": [
        "1. Embedded (in-service): the MCP server runs inside the service -- simplest, but couples their lifecycles",
        "2. Sidecar: a separate container beside the service, sharing its pod but deployed independently",
        "3. Centralized gateway: one MCP server fronts many services, giving a single place for auth and audit",
    ],
    "4. Federated servers 5. Hybrid deployment": [
        "4. Federated servers: each domain runs its own MCP server, discovered through a shared registry",
        "5. Hybrid deployment: a gateway for external callers with embedded or sidecar servers internally",
    ],
    "1. Build & push container image 2. Create OpenShift resources (Deployment, Service, Route)": [
        "1. Build & push container image: package the MCP-enabled service and publish it with an immutable tag",
        "2. Create OpenShift resources: declare the Deployment, Service, and Route that run and expose it",
    ],
    "4. Deploy 5. Verify & test 6. Monitor & scale": [
        "4. Deploy: roll out to the cluster and let the probes confirm the pods are genuinely ready",
        "5. Verify & test: call each exposed tool and check the audit records land as expected",
        "6. Monitor & scale: watch latency, error rate, and tool usage, then size replicas to real demand",
    ],
}


def _key(text: str) -> str:
    return " ".join((text or "").split())


LOOKUP = {_key(k): v for k, v in EXPANSIONS.items()}


def expand(text: str) -> list[str] | None:
    """Replacement bullets for a collapsed list, or None to keep it unchanged."""
    return LOOKUP.get(_key(text))
