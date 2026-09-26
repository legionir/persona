## DOMAIN MODEL CONTRACT — Domain-Driven Design (binding)

This contract governs **what the model means**: the language the code speaks, the boundaries inside
which that language is valid, and the tactical building blocks that carry behaviour and invariants.
The Architecture Boundaries contract governs *dependency direction and layer ownership*; the
Construction Contract governs the *inside* of routines, names, data, and tests. Where the three
meet — application services, infrastructure, translation, test level — this contract adds only the
domain-specific rule and defers to the others for the rest. It does not weaken the Prime Directive
(§3): evidence rules still govern every claim made about the target.

**Force of the rules.** Every unqualified rule below is `MUST`; `Prefer` is `SHOULD`; `Do not`,
`Avoid`, and `Never` are `MUST NOT` — unless the user explicitly overrides it, in which case the
conflict is stated rather than silently applied.

### 1. The model serves the business meaning

- When uncertain, prefer the option that makes the domain model clearer.
- Do not optimise primarily for fewer files, generic reuse, CRUD convenience, object-relational mapping convenience, delivery-layer convenience, framework conventions, or short-term speed at the cost of model clarity.
- DDD here does not mean ceremony: layers for their own sake, renaming service classes to sound sophisticated, wrapping CRUD in verbose abstractions, entities with only fields and setters, turning every concept into an aggregate, or over-engineering simple subdomains.
- DDD here does mean code built around business concepts, rules expressed in domain language, explicit context boundaries, invariants protected by the model, deliberate identity/value/lifecycle/consistency choices, explicit translation across boundaries, and aggressive simplification outside the core domain.
- Treat the model as discovered, not invented from technical structure. Awkward code, contradictory language, and repeated conditionals are signals to model more deeply, not to patch.

### 2. Ubiquitous language

- Use the exact business terms used by domain experts inside a bounded context — in code, tests, commands, events, repositories, and packages.
- One concept has one name inside a context; one name never carries two meanings inside a context.
- Operation names express the domain action; module and package names use the same vocabulary as the domain.
- Rename code when domain understanding improves. Never keep a bad name because it already exists in the database.
- Do not import a term from another context without translation, and do not use a technical placeholder where a precise domain term exists.
- The Construction Contract governs *how well* a name reveals intent; this governs *which vocabulary* the name comes from. Hiding domain complexity behind `type`, `status`, or `metadata` fields is a language defect, not a storage choice.

### 3. Bounded contexts

- Every substantial domain area belongs to a clearly identified bounded context, and a model is valid only inside its own context.
- Package, module, or namespace ownership makes the context explicit; the same term may legitimately mean different things in different contexts.
- Do not import another context's concepts as if they were native, and do not share model classes across contexts by default.
- A shared model across contexts is forbidden unless it is intentionally governed as a shared kernel with ownership and tests.
- Prefer context-specific contracts, identifiers, published language, or an anticorruption layer over shared classes.
- Do not build one giant company-wide domain model or a `shared/domain` package that erases boundaries.

### 4. Strategic design: subdomains and distillation

- Classify major areas as core domain, supporting subdomain, or generic subdomain, and put the most modelling care into the core domain.
- Do not over-model commodity concerns; keep supporting and generic subdomains simpler unless their complexity proves real.
- Make the core domain easy to find in code, and protect it from foreign models, vendor schemas, and generic abstractions.
- Choose refactoring targets by strategic importance, not by local messiness.
- Do not spend equal modelling effort on every subsystem, and do not let technical mechanisms dominate the core model.

### 5. Context mapping and integration

- Every interaction between contexts has an explicit, named relationship: Partnership, Shared Kernel, Customer/Supplier, Conformist, Anticorruption Layer, Open Host Service, Published Language, or Separate Ways.
- Translation is mandatory at context boundaries, and ownership of that translation is explicit in code.
- Foreign terms must not silently invade the local language, and an upstream API must not define downstream domain vocabulary.
- Do not call every integration an anticorruption layer when no translation exists, and do not keep context mapping as documentation that the code structure ignores.
- Choose integration style deliberately: RPC only when request/response coupling, latency, versioning, and failure semantics are acceptable; REST resources as application-facing representations rather than leaked aggregate internals; messaging when asynchronous coordination fits the business and consumers can handle lag, duplicates, and ordering limits.
- Treat a ball of mud as a context to contain and translate around, not a model to spread.

### 6. Entities

- Use an entity when identity, lifecycle, or continuity beyond current attributes matters, or when a rule depends on *which one* rather than only *what value*.
- Entities have explicit, stable identity, and they protect their own valid state transitions.
- Expose intention-revealing behaviour, not arbitrary state changes; hide direct state changes behind methods that encode domain meaning.
- Do not use public setters for every field, let application services or UI code decide which transitions are valid, or keep entities as passive persistence shells in behaviour-rich domains.

### 7. Value objects

- Use a value object when a concept is defined by its attributes, carries validation, has behaviour, or would hide meaning if passed as a primitive.
- Value objects are immutable by default, construct themselves valid, and compare by value rather than identity.
- Validation and side-effect-free operations live next to the concept, and the object is named after the domain concept rather than the primitive representation.
- Replace primitive obsession aggressively where the concept matters: the same validation repeated across handlers is the signal that a value object is missing.
- The Construction Contract already requires types that make invalid values hard to represent; this adds that the concept must also be *named in the domain language*.
- Do not let an invalid value exist temporarily without an explicit model for incompleteness.

### 8. Aggregates

- An aggregate is a consistency boundary, not an object graph: design it around invariants that must hold immediately.
- Keep aggregates as small as possible. Only the aggregate root may be referenced from outside, and every invariant-changing operation goes through the root.
- Internal members stay encapsulated; reference other aggregates by identity unless stronger consistency is truly required.
- Align transactional boundaries with invariants: one transaction usually modifies one aggregate, and cross-aggregate coordination is usually eventual rather than transactional.
- Do not size aggregates for object-relational mapping convenience or screen navigation, expose internal collections for arbitrary external change, or stretch transactions across many aggregates because references make it easy.

### 9. Domain services and specifications

- Use a domain service only for a domain-significant operation that does not naturally belong to one entity or value object, and name it in the ubiquitous language.
- If behaviour clearly belongs on an entity or value object, keep it there; do not thin out entities to feed services.
- Use specifications for named, combinable business rules that answer whether something satisfies a criterion, and keep them in domain language rather than query language.
- Extract repeated conditionals and boolean flags into named concepts — a specification is a domain rule, not a persistence query builder.
- Do not create a single `*Service` holding every rule for a model area, or a "domain service" that is only a wrapper around a repository or an external client.

### 10. Repositories and factories

- Repositories exist for aggregate roots, not for every table; their interfaces are defined by the domain or application code that uses them.
- Repositories reconstitute and persist aggregates and return domain objects or domain-oriented results — never persistence records, and never a universal query utility.
- Prefer focused, intent-revealing repository methods over generic CRUD when domain intent matters, and keep reconstitution paths separate from creation paths when that protects invariants.
- Factories create valid objects and encode domain creation rules; clients, endpoints, and mappers must not stitch aggregates together or build invalid objects to fix later.
- Use a constructor directly when creation is simple and intention-revealing, and do not add a factory only to hide a trivial constructor.

### 11. Domain events and eventual consistency

- Publish domain events for meaningful business facts; name them in the past tense and keep payloads meaningful and local to the model.
- Use events to coordinate across aggregates or contexts when immediate consistency is not required; do not publish trivial noise for every field change.
- Use event sourcing only when the sequence of events is genuinely the right persistence model for the aggregate: keep streams consistent with aggregate identity and versioning, rebuild state deterministically, and version events with upcasting when their meaning evolves.
- Do not choose event sourcing merely because domain events exist, use events to compensate for a missing aggregate design, or let events carry framework request objects or persistence artifacts.

### 12. Application layer, infrastructure, and translation

- Application services coordinate: load aggregates, invoke domain behaviour, persist results, publish events. They must not own the domain's core decisions — layer and use-case rules stay with the Architecture Boundaries contract.
- Infrastructure is subordinate to the model: object-relational mappings, serializers, transport formats, caches, and framework types stay out of the domain model, and persistence shape never defines domain shape.
- Translation is mandatory at context boundaries and between domain objects and transport or persistence representations; an anticorruption layer preserves the local model instead of mirroring the foreign one.
- Do not pass external API models deep into the domain, reuse one representation as delivery input, persistence record, domain object, and integration message, or adopt vendor status codes as native domain terminology.

### 13. Supple design

- Interfaces reveal intention in domain language; prefer side-effect-free functions for calculations and queries, and make assertions and invariants explicit in the model.
- Shape objects around conceptual contours, keep related concepts together when they change together, and look for cohesive concepts hidden inside long methods, conditionals, or parameter groups.
- Combine specifications with AND, OR, or NOT only while each component's meaning stays readable.
- Do not express invariants only in comments or in UI/application validation, and do not use declarative frameworks that obscure rather than clarify business rules.

### 14. Practicality: selective, serious DDD

- Use the least expensive pattern that honestly models the problem, and strengthen the model when invariants, lifecycle, and language complexity rise.
- Do not apply full tactical DDD to simple CRUD, generic subdomains, or problems whose complexity is mainly technical — and do not dismiss modelling where the domain is genuinely complex.
- Reject DDD theatre: renaming CRUD layers, adding repositories, factories, and services without domain need, and over-modelling simple supporting subdomains.
- Track modelling debt when code and language are known to be imperfect but intentionally deferred.

### 15. Domain model review gate — for the change itself, not for the audit

Before presenting any change produced during this work, verify:

- [ ] The bounded context of every touched concept is explicit
- [ ] The code speaks the context's ubiquitous language, with one term per concept
- [ ] Important concepts are modelled explicitly, not hidden behind flags, statuses, or metadata
- [ ] Value objects replace primitives that carry meaning, validation, or units
- [ ] Entities protect their own transitions; no public setters in behaviour-rich domains
- [ ] Aggregates are small, centred on immediate invariants, and referenced by identity
- [ ] Repositories are aggregate-oriented; factories create only valid objects
- [ ] Application services orchestrate; the domain model still carries the decisions
- [ ] Foreign models are translated explicitly at every boundary crossed
- [ ] Modelling effort matches strategic importance, with no ceremony where the domain is simple

If any answer is no, revise the design before shipping.

---
