# Eight-Auditor Codebase Review Matrix

This matrix defines eight complementary audit workstreams for a repository review. It is the source of truth for skill scope, applicability, and ownership boundaries. The auditor labels describe review lanes, not necessarily eight separate runtime agents: one auditor may execute several applicable lanes, but must keep their findings attributable to the lane and skill that produced them.

**Run order:** discover the project stack → applicability gate each skill → review only applicable skills → verify findings → aggregate duplicates and calibrate severity. In CI incremental mode, deep review is limited to changed files; unchanged files may be inspected only as supporting context and must not silently expand the review scope. See the [Codebase Integrity Audit Protocol](../prompts/composite/codebase-integrity-audit-protocol.md).

## Applicability and finding rules

- Mark each skill `APPLICABLE`, `NOT_APPLICABLE` (with stack evidence), or `UNKNOWN` (with the missing evidence). Do not execute a skill marked `NOT_APPLICABLE`; do not treat `UNKNOWN` as a pass.
- Applicability is decided from observed project evidence—languages, frameworks, manifests, entry points, deployment files, and runtime topology—not from a directory name or assumption.
- A finding belongs to one primary auditor/skill. Additional auditors may be recorded as contributors when they independently identify the same root cause.
- Merge findings only when the underlying root cause and triggering behavior are the same. Same-file or same-line location alone is not enough to deduplicate distinct defects.
- Calibrate severity once for each aggregate finding from demonstrated impact. Do not add severities together; retain the strongest severity justified by evidence and record the rationale.
- Keep each skill within its boundary below. A cross-boundary concern is linked to the owning lane rather than reported twice.

---

## 1. Security Auditor

| Skill | Review scope |
|---|---|
| Secret & Credential Detection | Hard-coded API keys, passwords, private keys, or other credentials in source, configuration, logs, and tests. Never reproduce secret values in findings. |
| Injection Security | SQL, NoSQL, LDAP, template, and header injection; trace attacker-controlled sources to sinks. |
| Command/Code Execution Security | Unsafe `eval`, shell execution, and dynamic loading reached with user-controlled input. |
| Authentication Security | Login flows, brute-force protection, MFA, and authentication bypass. |
| Authorization & Access Control | Role/permission checks, privilege escalation, and incomplete ownership checks. |
| Session & Token Security | JWTs, session cookies, expiry, fixation, and tokens that are not revoked. |
| Input Validation & Sanitization | Boundary/schema/type validation and trust boundaries between layers. |
| Output Encoding | XSS and encoding appropriate to the output context. |
| File & Path Security | Path traversal, unsafe uploads, symlinks, and archive extraction. |
| SSRF & Network Security | Server-side requests to internal/metadata addresses and redirect abuse. |
| Web Security | CORS, CSRF, security headers, cookie flags, and clickjacking. |
| Cryptography Security | Weak algorithms, hard-coded cryptographic keys, unsafe randomness, and password hashing. |
| Dependency Security | Whether the project's actually used packages have known vulnerabilities (CVE/advisory status only). |
| **Boundary — dependency findings** | Do not assess general dependency-graph health here; unresolved imports, cycles, unused/missing packages, version compatibility, and license compliance belong to the Dependency Auditor. Installation/build/CI supply-chain controls belong to DevOps. |
| Security Configuration | Debug mode enabled, permissive CORS, and insecure production settings. |
| Data Exposure & Privacy | PII/credentials in responses or logs, and stack-trace disclosure. |
| Unsafe Deserialization | Unsafe JSON/object deserialization and prototype pollution. |
| Security Error Handling | Fail-open behavior or error detail disclosure that directly leaks information or bypasses a security control. |
| **Boundary — error handling** | Only direct security leakage/bypass belongs here. General error quality belongs to Code Quality; recovery and graceful degradation belong to Reliability. |
| Security Logging & Monitoring | Missing security audit trails and secrets written to logs. |

## 2. Architecture Auditor

| Skill | Review scope |
|---|---|
| Project Structure Analysis | Identify modules, applications, libraries, and actual project boundaries. |
| Module Boundary Analysis | Public/private boundaries and leakage of internal implementation. |
| Dependency Direction | Whether actual design dependencies follow the intended direction. |
| **Boundary — dependency direction** | Assess whether the design is correct or violated. The extracted, technical direction of edges in the actual import graph belongs to Dependency. |
| Coupling Analysis | Excessive fan-in/fan-out, cross-directory coupling, and central dependencies. |
| Cohesion Analysis | Whether a module has one coherent responsibility or mixes concerns. |
| Circular Dependency Analysis | Whether a cycle violates layering or design. |
| **Boundary — cycles** | Assess design consequences only. Technical cycle detection and resolution in the import graph belong to Dependency. |
| Layering Analysis | Layer bypasses in patterns such as controller/service/repository. |
| Responsibility Analysis | God modules/classes and business logic placed in UI/controllers. |
| Abstraction Analysis | Excessive or insufficient abstraction and implementation leakage. |
| Interface & Contract Analysis | Inter-module contracts, DTOs, and agreement between contract and implementation. |
| Architecture Consistency | Consistency of architectural patterns across project areas. |
| Entrypoint & Composition Analysis | Bootstrap, CLI, workers, and composition roots. |
| Shared/Common Module Analysis | `utils`/`common` modules turning into dependency dumping grounds. |
| Architecture Drift Detection | Difference between intended and observed architecture. |
| Complexity & Hotspot Analysis | Highly coupled modules with high ripple-effect risk. |

## 3. Code Quality Auditor

| Skill | Review scope |
|---|---|
| Code Smell Detection | Long methods, god objects, deep nesting, and feature envy. |
| Complexity Analysis | Structural complexity, nesting, and function/class size. |
| Function Quality | Length, parameter count, side effects, and testability. |
| Class/Module Quality | Size, responsibility, public surface, and coupling. |
| Duplication Analysis | Repeated logic (not superficial similarity), especially validation/mapping. |
| Dead Code Analysis | Declarations without references and unused imports/exports. |
| Naming & Readability | Ambiguous, inconsistent, or misleading terminology. |
| Error Handling Quality | Empty catches and `null` returns where the contract is unclear. |
| **Boundary — errors** | Assess code quality/readability only. Security violations belong to Security; runtime recovery belongs to Reliability. |
| Async/Promise Quality | Missing `await`, fire-and-forget, and callback/promise mixing as maintainability concerns. |
| **Boundary — async** | Assess maintainability only. Races/safety belong to Reliability; throughput/latency belongs to Performance. |
| Type Safety | `any`, unsafe casts, and nullable ambiguity. |
| API/Function Contract Quality | Ambiguous inputs/outputs and inconsistent return shapes. |
| Maintainability Patterns | Local reasoning, appropriate dependency injection, and separation of concerns. |
| Debug/Temporary Code | Leftover `console.log`, commented-out code, and development flags. |
| Comment & TODO Quality | Important TODOs and stale or contradictory comments. |
| Consistency Analysis | Consistency of error, naming, async, and import patterns. |

## 4. Performance Auditor

| Skill | Review scope |
|---|---|
| Algorithmic Complexity | Nested loops, N²/N³ behavior, and unsuitable data structures. |
| CPU Hotspots | Expensive synchronous work, costly regexes, and repeated cryptography. |
| Memory Usage Patterns | Large collections, cloning, and unbounded caches. |
| I/O Efficiency | Whole-file reads, synchronous I/O, and missing batching. |
| Database Performance | Queries in loops, N+1 access, and over-fetching. |
| Network Performance | Repeated/sequential requests, oversized payloads, and absent caching. |
| Async/Concurrency Efficiency | Parallelizable work run sequentially and event-loop blocking. |
| **Boundary — async/concurrency** | Assess throughput and latency only. Race safety belongs to Reliability; async-code maintainability belongs to Code Quality. |
| Caching | Missing suitable caches, invalidation defects, and cache stampedes. |
| Resource Lifecycle | Connection/socket leaks insofar as they harm performance. |
| Frontend Performance | Unnecessary rendering, large bundles, and slow startup. |
| Startup/Initialization Performance | Unnecessary eager loading and full filesystem scans at startup. |
| Scalability Patterns | Local state incompatible with horizontal scaling and global locks. |
| Serialization/Parsing Costs | Repeated JSON parsing/stringification inside loops. |
| Performance Anti-Patterns | Busy loops, continuous polling, and uncontrolled retries. |

## 5. Reliability Auditor

| Skill | Review scope |
|---|---|
| Error Handling & Recovery | Whether failures are actually recovered from or degraded gracefully. |
| **Boundary — errors** | Assess system stability after failure. Direct security leakage/bypass belongs to Security; code-quality issues belong to Code Quality. |
| Exception Safety | Partial operations, inconsistent state after exceptions, and incomplete cleanup. |
| Timeout Analysis | Missing timeouts on HTTP, database, socket, and queue operations. |
| Retry & Backoff | Retries without backoff/jitter and retries of non-idempotent operations. |
| Circuit Breaking | External dependencies whose failures cascade. |
| Resource Leak Detection | Connection/timer/listener/worker leaks from a system-stability perspective. |
| Concurrency Safety | Race conditions, shared mutable state, and lost updates. |
| **Boundary — concurrency** | Assess correctness and safety only. Throughput belongs to Performance; async readability belongs to Code Quality. |
| State Consistency | Incomplete transitions, invalid state, and partial failure. |
| Transaction Reliability | Atomicity, transaction scope, and incomplete rollback. |
| Failure Isolation | Whether a component failure takes down the whole process. |
| Graceful Shutdown | SIGTERM/SIGINT handling, closing pools/queues, and completing in-flight work. |
| Startup/Recovery | Behavior after crash/restart and state recovery. |
| Idempotency | Duplicate events for job/webhook/payment-like operations. |
| Queue/Job Reliability | Stuck jobs, duplicate processing, dead-letter handling, and visibility timeouts. |
| External Dependency Resilience | Behavior when an external database/API/queue is slow or unavailable. |
| Data Integrity | Partial writes, validation before persistence, and corruption. |
| Health Checks & Recovery Signals | Health/readiness/liveness and detection of degraded states. |

## 6. Testing Auditor

| Skill | Review scope |
|---|---|
| Test Inventory | Locate test files, suites, runners, fixtures, and mocks. |
| Test Coverage Analysis | Coverage of critical code, not merely a raw percentage. |
| Unit Test Quality | Isolation, single responsibility, and determinism. |
| Integration Test Quality | Real coverage of database/API/filesystem/queue boundaries. |
| E2E Test Quality | Important user/system flows, authentication, and failure paths. |
| Test Completeness | Important modules/functions without tests. |
| Edge Case Analysis | Null/empty/boundary/malformed/duplicate/large input and concurrency. |
| Error Path Testing | Whether failure paths are tested, not only happy paths. |
| Regression Protection | Tests that protect important fixes against regressions. |
| Mocking/Stubbing Quality | Over-mocking and mocks that bypass the real contract. |
| Test Isolation | Shared state, global mutation, and order dependency. |
| Determinism & Flakiness | Reliance on random/time/network and test races. |
| Testability Analysis | Dependency injection, side-effect isolation, and unit-test difficulty. |
| Assertion Quality | Weak assertions such as truthiness-only checks. |
| Security Testing | Whether auth-bypass/injection scenarios are tested. |
| **Boundary — security tests** | Assess only whether scenarios are tested. Actual vulnerability status belongs to Security. |
| Performance Testing | Whether benchmarks exist for latency-sensitive paths. |
| **Boundary — performance tests** | Assess only whether a path is tested. Actual slowness belongs to Performance. |

## 7. Dependency Auditor

| Skill | Review scope |
|---|---|
| Source Dependency Analysis | Internal `import`/`require`/`export-from` relationships and graph construction. |
| External Package Analysis | Packages actually used versus packages merely declared. |
| Dependency Resolution | Aliases, relative paths, package exports, and workspace resolution. |
| Unresolved Dependency Detection | Imports whose destinations do not exist. |
| Circular Dependency Analysis | Technical cycle detection/resolution in the extracted graph. |
| **Boundary — cycles** | Technical graph correctness only. Whether a cycle violates design belongs to Architecture. |
| Dependency Direction | Actual direction of edges in the graph extracted from code. |
| **Boundary — direction** | Record technical reality only. Whether that direction matches intended design belongs to Architecture. |
| Unused Dependency Analysis | Declared dependency with no provable usage. |
| Missing Dependency Analysis | Runtime dependency required by code but absent from the manifest. |
| Duplicate/Redundant Dependency Analysis | Multiple packages serving similar roles and multiple versions. |
| Version & Compatibility Analysis | Version ranges and mismatches across package-manager files. |
| Runtime vs Build Dependency Analysis | `dependencies`/`devDependencies`/peer/optional distinctions. |
| Type-only Dependency Analysis | Type-only imports and their effect on the runtime graph. |
| Re-export & Barrel Analysis | Barrel files, `export *`, and hidden dependencies. |
| Dynamic Dependency Analysis | Dynamic import/require and plugin loading not statically resolvable. |
| Package Boundary Analysis | Internal workspace/package boundaries and cross-package leakage. |
| Dependency Risk Analysis | Highly central, unfamiliar, or deeply chained dependencies. |
| **License Compliance Analysis (new)** | Identify the license for each direct and transitive dependency and compare its documented obligations/compatibility with the project's declared license and distribution/use model. Cite manifests, lockfiles, package metadata, and policy evidence. Mark unknown or conflicting license metadata as `UNKNOWN`; do not make a legal determination or infer a license from package popularity. |

## 8. DevOps Auditor

| Skill | Review scope |
|---|---|
| Build System Analysis | Build scripts, compiler flags, and dev/production build differences. |
| CI/CD Analysis | Pipeline stages, test/lint gates, and branch/release workflows. |
| Docker/Container Analysis | Dockerfiles, image size, multi-stage builds, root user, and health checks. |
| Environment & Configuration Management | `.env`, configuration precedence, and environment drift. |
| Deployment Analysis | Startup commands, migration order, and rollback. |
| Process & Runtime Management | Process manager, worker count, and log rotation. |
| Infrastructure as Code | Docker Compose/Kubernetes/Terraform compatibility when present. |
| Secrets in DevOps | Credentials in CI logs/workflows and Docker layers. |
| Release Management | Versioning, artifact tagging, and migration compatibility. |
| Health & Readiness Operations | Health checks and readiness/liveness probes. |
| Logging & Observability Configuration | Log levels, structured logging, and correlation IDs. |
| Backup & Recovery Configuration | Backup scripts, restore procedures, and retention. |
| Dependency/Artifact Reproducibility | Lockfiles, pinned versions, and deterministic builds. |
| Supply Chain Security | Security of the install/build/CI chain and unsigned artifacts. |
| **Boundary — supply chain** | Assess install/build/CI/artifact provenance only. Vulnerabilities in package code belong to Security; technical dependency-graph health belongs to Dependency. |
| Resource & Scaling Configuration | CPU/memory limits, replicas, and statelessness. |
| Operational Documentation | Runbooks, required environment variables, and troubleshooting. |

---

## Loadable audit skills in this repository

These are independently invokable Agent Skills, mapped to the eight auditor lanes. The first seven are existing domain audit composites; `devops-audit` is the dedicated DevOps audit added alongside this matrix. `license-compliance-analysis` is a standalone subskill of the Dependency Auditor.

| Auditor lane | Loadable skill | Purpose / scope |
|---|---|---|
| Security | [`forensic-security-threat-audit`](../skills/forensic-security-threat-audit/SKILL.md) | Security controls and evidence-based attack-path analysis. |
| Architecture | [`software-design-architecture-review`](../skills/software-design-architecture-review/SKILL.md) | Architecture boundaries, design direction, layering, and drift. |
| Code Quality | [`clean-code-construction-review`](../skills/clean-code-construction-review/SKILL.md) | Construction quality, maintainability, smells, and type/readability concerns. |
| Performance | [`performance-scalability-audit`](../skills/performance-scalability-audit/SKILL.md) | Throughput, latency, resource behavior, and scalability. |
| Reliability | [`production-readiness-reliability-audit`](../skills/production-readiness-reliability-audit/SKILL.md) | Failure handling, recovery, state consistency, and operational readiness. |
| Testing | [`testing-quality-assurance-audit`](../skills/testing-quality-assurance-audit/SKILL.md) | Test coverage, quality, isolation, determinism, and gaps. |
| Dependency | [`supply-chain-dependency-audit`](../skills/supply-chain-dependency-audit/SKILL.md) | Dependency graph, package inventory, provenance, and supply-chain risk. |
| Dependency (subskill) | [`license-compliance-analysis`](../skills/license-compliance-analysis/SKILL.md) | Direct/transitive/vendored dependency license evidence and compliance-risk triage. |
| DevOps | [`devops-audit`](../skills/devops-audit/SKILL.md) | Build, CI/CD, configuration, deployment, runtime, release, reproducibility, recovery, and operations. |

Each skill is also listed in `skills/index.json` and `skills/README.md`. These are executable domain skills, not nine new role personas; the loadable audit composites run from their own focused scope, while the eight-lane matrix remains the shared ownership contract.

## Ownership at a glance

| Concern | Primary owner | Other lane's non-overlapping role |
|---|---|---|
| Package vulnerability vs graph health vs install/build chain | Security / Dependency / DevOps respectively | Preserve the stated boundary; share evidence by reference. |
| Design direction vs observed import edges | Architecture / Dependency respectively | Architecture evaluates intent; Dependency reports graph facts. |
| Error quality vs recovery vs security leakage | Code Quality / Reliability / Security respectively | Split only when distinct root causes or impacts are evidenced. |
| Async maintainability vs race safety vs throughput | Code Quality / Reliability / Performance respectively | Do not duplicate a single issue under all three labels. |
| Test existence vs actual defect | Testing vs owning domain auditor | Testing reports coverage; the owning auditor establishes the defect. |
