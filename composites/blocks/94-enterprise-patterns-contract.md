## ENTERPRISE PATTERNS CONTRACT — Patterns of Enterprise Application Architecture (binding)

This contract governs **structural responsibility in enterprise software**: where business logic
is allowed to live, how persistence and transactions are owned, how remote boundaries are shaped,
and which well-understood pattern fits the actual complexity. The Architecture Boundaries contract
governs *dependency direction and layer ownership*; the Domain Model contract governs *what the
model means*; this contract governs *which structural pattern earns its cost here*. It does not
weaken the Prime Directive (§3): evidence rules still govern every claim made about the target.

**Force of the rules.** Every unqualified rule below is `MUST`; `Prefer` is `SHOULD`; `Do not`,
`Avoid`, and `Never` are `MUST NOT` — unless the user explicitly overrides it, in which case the
conflict is stated rather than silently applied.

### 1. Patterns, not invented architecture

- Enterprise software is not improved by inventing structure from scratch for every feature. Prefer a small number of well-understood patterns applied deliberately.
- Make these responsibilities explicit and give each exactly one owner: presentation and transport, application workflow, domain logic, data source interaction, transaction management, concurrency control, integration boundaries.
- Layering is the default organizing principle — presentation/delivery, application coordination, domain logic, data source and integration access. Layer responsibilities and dependency direction stay with the Architecture Boundaries contract; this adds only that **each layer must earn its existence** by reducing coupling or clarifying responsibility.
- Do not let one class or layer own all of those responsibilities, and reject fashionable complexity and accidental coupling alike.

### 2. Choose the business logic pattern deliberately

Pick the pattern that matches the real complexity, and say which one the code uses:

- **Transaction Script** — when logic is simple and each request or use case is mostly independent. Keep scripts short and use-case focused; escalate when duplication, lifecycle, or invariant complexity grows. Do not let it become the dumping ground for all business logic.
- **Table Module** — when logic is naturally organized around tabular data sets and calculations are set-oriented. Keep behaviour centred on the table abstraction, and isolate tabular logic from presentation and transport. Do not fake entities when the real model is tabular.
- **Domain Model** — when domain complexity is significant and rules, invariants, and lifecycles matter. Rich logic belongs in model objects, application coordination stays separate from domain decisions, and anemic models are not acceptable in behaviour-rich domains.

The Domain Model contract already governs *how* to build a domain model; this governs *whether* one is justified. Do not default to a domain model everywhere regardless of complexity, and do not leave complex rules trapped in transaction scripts.

### 3. Application workflow

- Application services define application operations, orchestrate use cases, and own transaction boundaries; they expose an application-oriented API, never UI mechanics. Orchestration and use-case rules stay with the Architecture Boundaries and Domain Model contracts.
- Do not let the service layer absorb domain logic by default, and do not let controllers duplicate its orchestration.
- Place use-case coordination in the service layer, domain decisions in the model, and persistence behind repositories, mappers, or gateways — in that order.

### 4. Remote boundaries, facades, and DTOs

- Expose coarse-grained remote operations; a remote facade translates between the remote contract and the internal model and keeps transport concerns at the boundary.
- DTOs are transport structures, not domain models. Keep mapping explicit, batch values where serialization cost is real, and never move business behaviour into a DTO.
- Do not distribute objects or services remotely by default. Separate local object design from remote contract design, and budget explicitly for latency, serialization, versioning, and partial failure.
- Chatty remote interfaces, local-method-call semantics assumed over a network, and domain internals leaked through remote endpoints are defects.

### 5. Persistence pattern choice

Choose the persistence pattern that matches the domain, and keep the choice visible:

- **Repository** — a collection-like interface over domain object access, speaking in domain terms and shaped by use cases or aggregates rather than table shape. Repository rules stay with the Domain Model contract; implementations hide query, mapping, and storage detail.
- **Data Mapper** — when the domain model must stay decoupled from database structure and object-relational mismatch is real. Mapping code belongs outside the domain objects, and domain objects must not know SQL, record formats, or mapping mechanics.
- **Row Data Gateway** — when behaviour is simple and record-oriented. **Table Data Gateway** — when operations are naturally table-oriented and one table interface can clearly centralize access.
- **Active Record** — only when domain logic is simple and persistence coupling is acceptable. Never default to it for complex domains.
- Do not use one generic CRUD abstraction for all domain and data access, expose persistence models directly to callers, or let ORM convenience dictate aggregates, services, and DTOs.

### 6. Unit of Work, Identity Map, and loading

- Make transactional write coordination explicit through a Unit of Work: commit work as one logical unit, keep its scope understandable, and name its owner.
- Preserve one in-memory representation per identity per scope where needed, so duplicate instances cannot fight each other inside one logical unit of work.
- Use Lazy Load deliberately, not everywhere: know where it may trigger remote or database chatter, and avoid lazy-loading surprises in loops and serialization paths.
- Do not allow invisible N+1 behaviour, hidden auto-persistence with surprising write timing, or ad-hoc saves from random callers.

### 7. Object-relational mapping choices

When in-memory objects and relational tables disagree, choose an explicit mapping strategy instead of an accidental one:

- **Identity Field** for stable database identity; **Foreign Key Mapping** for object references that map to relational keys, without hiding expensive joins behind innocent traversal.
- **Association Table Mapping** for many-to-many relationships; **Dependent Mapping** for children with no independent identity outside their owner; **Embedded Value** for a small value object living inside the owning row.
- **Serialized LOB** only when the value is never queried inside and serialization versioning is controlled.
- **Single Table Inheritance** when one table with nullable columns is simpler than joins; **Class Table Inheritance** when normalized subtype data is worth the join cost; **Concrete Table Inheritance** when each concrete type can own its table without excessive duplication.
- **Inheritance Mappers** to keep inheritance persistence decisions out of domain logic; **Metadata Mapping** only when the rules are regular enough to centralize safely; **Query Object** when query construction needs a composable object model instead of scattered SQL strings.
- Whatever the choice, mapping stays outside the domain model and stays testable.

### 8. Transactions and offline concurrency

- Transaction boundaries must be explicit in application workflow, short, and owned by one identifiable place. Do not bury transaction ownership in helper classes, span transactions across remote calls, or treat a long-running workflow as one immediate transaction.
- **Optimistic Offline Lock** when conflicts are possible but uncommon: detect conflicting concurrent updates, fail safely and explicitly, and make conflict resolution or merge semantics intentional.
- **Pessimistic Locking** only when contention is expected and its cost is justified.
- **Coarse-Grained Lock** when related objects must be locked together to preserve a user-level edit; **Implicit Lock** only when acquisition is reliably hidden without making concurrency undiagnosable.
- Keep concurrency and loading assumptions visible to maintainers.

### 9. Presentation responsibilities

- Presentation code handles input, rendering, and transport concerns. Business rules must not live in controllers or views, and formatting, pagination, and UI interaction state belong outside domain logic.
- Presentation models may differ from domain models; keep routing concerns out of business logic.
- Choose pragmatically: **Model View Controller** to separate model, view, and controller; **Page Controller** when each page or action is handled independently; **Front Controller** when centralized handling, authentication, or dispatch is valuable.
- For views: **Template View** when templates clearly express the response, **Transform View** when transforming data is clearer than embedding logic, **Two Step View** when shared structure should be separated from page-specific content, and **Application Controller** when flow and navigation need a dedicated coordinator.

### 10. Session and cross-cutting state

- Choose session state deliberately: **Client Session State** only when client storage is acceptable and integrity and security implications are handled; **Server Session State** when server-managed data is needed and scaling and cleanup costs are explicit; **Database Session State** when durability or server-farm sharing outweighs database load.
- Treat shared mutable state as expensive regardless of where it lives, and keep its ownership and lifetime explicit.

### 11. Base patterns worth using deliberately

- **Gateway** to isolate access to an external resource or subsystem; **Mapper** to move data between objects or layers while keeping both sides independent; **Separated Interface** so clients depend on an interface owned away from implementation details.
- **Special Case** to replace repeated null or exceptional handling with a named object — a null check repeated across callers is a missing concept, not a defensive habit.
- **Money** for currency amounts so rounding, currency, and arithmetic rules stay explicit; **Value Object** for small values where equality by value and immutability simplify code (value-object rules stay with the Domain Model contract).
- **Plugin** when implementations must be selected or extended without changing core code; **Service Stub** to test or run without a real remote service; **Record Set** when tabular data is the natural interchange shape and object behaviour is not needed.
- **Layer Supertype** only when shared layer behaviour is real and stable; **Registry** sparingly for well-known objects, and never as a global hidden dependency.

### 12. Testing structure, not only behaviour

- Test domain logic independently from presentation and persistence whenever possible; the Domain Model and Architecture Boundaries contracts already fix the *level* of domain tests.
- Test repositories, mappers, and gateways separately as data-access infrastructure, and test DTO and remote-facade mapping at the boundaries.
- Test service and application workflows for transaction and orchestration behaviour, and test concurrency behaviour where optimistic or pessimistic locking matters.

### 13. Enterprise patterns review gate — for the change itself, not for the audit

Before presenting any change produced during this work, verify:

- [ ] The business logic pattern matches the actual complexity, and the code says which one it is
- [ ] Presentation, workflow, domain logic, and persistence responsibilities are distinct
- [ ] Transaction ownership is explicit and the boundary is short
- [ ] Repositories and gateways are shaped by use cases or aggregates, not by raw tables
- [ ] Mapping and ORM decisions are isolated from domain logic
- [ ] Remote boundaries are coarse-grained, translated explicitly, and budgeted for failure
- [ ] Loading and locking assumptions are visible, with no invisible N+1
- [ ] No generic repository overreach, controller-centric design, or layering theatre

If any answer is no, revise the design before shipping.

---
