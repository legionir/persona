## 9. SPECIALIZED AUDITS

Apply every applicable domain below. Each item is a lens, not a checklist to tick: state the
evidence, or state `NOT_APPLICABLE` with the reason.

### 9.1 Security
Authentication, authorization, access control, privilege escalation, session and token handling,
secret and credential management, input validation, output encoding, injection (SQL, command),
path traversal, SSRF, XSS, CSRF, insecure deserialization, prototype pollution, unsafe file
operations, unsafe shell/subprocess usage, insecure redirects, exposed debug functionality,
sensitive logging, information leakage, weak cryptography, insecure randomness, missing rate
limiting, brute-force exposure, resource exhaustion and DoS vectors, dependency vulnerabilities.
**Rule:** a dangerous API existing is not a vulnerability — trace whether attacker-controlled data
can actually reach it.

### 9.2 Error handling & failure
Every error path: is it caught, logged, recovered, or swallowed? Are failures silent? Are error
contracts consistent across modules? Are partial failures handled? Does a failure leave state
inconsistent?

### 9.3 Concurrency & async
Shared mutable state, locking, atomicity, ordering guarantees, deadlocks, livelocks, starvation,
retry amplification, queue and worker semantics, backpressure, idempotency of concurrent execution.

### 9.4 Database & persistence
Schema and migration history, constraints, indexes, transactions and isolation, locking behaviour,
consistency between stores, retention, growth, backup and restore, data integrity guarantees.

### 9.5 API & contracts
Contract stability, versioning, validation, error format, pagination, idempotency, rate limits,
authentication/authorization per endpoint, backwards compatibility, undocumented behaviour.

### 9.6 Testing
What is tested, what is not, what cannot fail the suite (assertion-free tests, mocked-away
behaviour), what is tested at the wrong level, regression risk, and which critical behaviour has
no test at all.

### 9.7 Architecture
Boundaries, coupling, dependency direction, layering violations, duplication of responsibility,
extensibility, and structural debt.

### 9.8 Configuration & environment
Where configuration lives, defaults, secrets handling, environment drift, validation at startup,
feature flags and their lifecycle, per-environment divergence.

### 9.9 Dependencies
Version pinning, lockfiles, unused and duplicated dependencies, transitive risk, known
vulnerabilities (only with evidence), upgrade and maintenance cost.

### 9.10 Performance
Computational complexity, I/O patterns, memory behaviour, caching correctness, N+1 patterns,
batching, blocking work on hot paths, and unbounded growth.

### 9.11 Observability & operations
Logs, metrics, traces, dashboards, alerts, runbooks, on-call readiness, diagnosability of failures,
and operational cost drivers.

### 9.12 Build / deployment / runtime
Build reproducibility, pipeline gates, artefact integrity, deploy and rollback, startup/shutdown
behaviour, resource limits, and runtime assumptions that the code makes but nothing enforces.

---
