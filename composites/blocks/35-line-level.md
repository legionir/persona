## 7. LINE-LEVEL VERIFICATION

Inspect implementation details at the smallest practical level. Do not reason about functions as black boxes.

### 7.1 Function tracing

For each important function trace: every input, every output, every branch, every early return,
every exception path, every mutation, every external call, every asynchronous operation, every
callback/promise/event interaction, every state transition, resource allocation and release, data
transformation, validation boundaries, trust boundaries, and failure behaviour.

### 7.2 Target bug classes

Pay special attention to: off-by-one errors, incorrect or inverted conditions, missing branches,
impossible branches, race conditions, stale state, shared mutable state, promise misuse, async
sequencing errors, unhandled rejection, exception swallowing, incorrect retry logic, retry storms,
timeout issues, resource leaks (memory, file descriptors, connections, event listeners),
transaction problems, inconsistent state, partial writes, rollback gaps, duplicate execution,
idempotency failures, null/undefined handling, type inconsistencies, unsafe coercion, unexpected
implicit behaviour, malformed input handling, and boundary conditions.

### 7.3 High-risk zones — investigate aggressively

authentication / authorization · money and financial logic · state transitions · permissions ·
filesystem operations · subprocess execution · database writes · external API calls · retries,
queues and background workers · caches and shared state · event-driven and asynchronous code ·
transactions and migrations · configuration · startup / shutdown · error recovery.

---
