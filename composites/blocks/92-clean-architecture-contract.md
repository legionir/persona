## ARCHITECTURE BOUNDARIES CONTRACT — Clean Architecture (binding)

This contract governs the **direction and ownership of dependencies** in every change produced
while applying this persona: which layer owns a rule, which layer may know about a detail, and
where adapters, ports, and wiring belong. The Construction Contract (Clean Code + Code Complete)
already requires hiding implementation behind narrow local adapters and separating construction
from use at an explicit composition area; this contract decides **which way those dependencies
point** and **which layer owns which rule**. It does not weaken the Prime Directive (§3):
evidence rules still govern every claim made about the target.

**Force of the rules.** Every unqualified rule below is `MUST`; `Prefer` is `SHOULD`; `Do not`,
`Avoid`, and `Never` are `MUST NOT` — unless the user explicitly overrides it, in which case the
conflict is stated rather than silently applied.

### 1. The Dependency Rule

- Source code dependencies point inward, toward higher-level policy. Inner layers never import, name, or depend on outer layers.
- Business rules must not depend on frameworks, web handlers, database drivers, UI libraries, queues, external services, or other details.
- Outer layers may depend on inner layers, never the reverse: controllers depend on use cases; gateways implement interfaces owned by the use case or domain layer; presenters implement output boundaries owned by inner layers.
- Before placing any dependency, verify the direction: does this import point inward, is a high-level policy depending on a low-level detail, is a framework or vendor type reaching a core layer, is an adapter bypassing its boundary?

### 2. Layer responsibilities

- **Domain** — entities, enterprise business rules, domain invariants, core business rules. Plain objects, functions, or modules; no specific modelling style is mandated. Must be framework-free, persistence-ignorant, and delivery-agnostic. Must not import web libraries, database access types, or external service clients; perform I/O; or read configuration directly.
- **Application** — use cases, input and output models, ports and boundaries, orchestration. Must depend on domain abstractions, define the interfaces it needs from the outside, and coordinate workflows explicitly. Must not contain controller logic, database access details, or framework response types.
- **Interface adapters** — controllers, presenters, view models, gateway adapters, and mappers between external and internal models. Must translate external formats into internal models and depend inward. Must not move business policy out of the use case or domain layer, or bypass use cases to call gateways directly without justification.
- **Infrastructure** — framework bootstrap, object-graph and component wiring, database access, external service integration, message bus clients, filesystem and network implementations. Must remain replaceable, implement interfaces owned by inner layers, and stay at the outermost edge. Must not define business rules, dictate domain shapes, or leak vendor types inward.
- Place code in the highest-level place that matches its responsibility: business policy, orchestration, translation, or infrastructure.

### 3. Use cases orchestrate

- A use case represents one application action and coordinates entities and gateways.
- A use case must not contain delivery concerns, database concerns, or presentation formatting concerns.
- For every non-trivial feature, define the use case first: the input, the output, the required ports, and the orchestration in one place.

### 4. Entities guard invariants

- Critical domain rules and invariants belong in entities or equivalent domain objects, which protect their own consistency.
- Do not leave core rules in controllers, jobs, handlers, or database scripts.
- Pass plain data into use cases through request models or arguments; business rules must not read web requests, environment variables, framework context, or database rows directly.

### 5. Ports, adapters, and wiring

- Inner layers own the interfaces they need; outer layers implement them. Never define a gateway interface in infrastructure and consume it from core policy.
- Create ports for volatile dependencies: gateways, mailers, payment providers, message publishers, storage providers, clocks, ID generators, transaction runners.
- Object construction belongs at the composition root; never instantiate infrastructure inside a use case or entity.
- Avoid shared "common" packages that create sideways coupling between unrelated policy.
- When in doubt, introduce a boundary sooner; a partial boundary is acceptable when it preserves a future extraction path.

### 6. Organise by use case

- Prefer feature and use-case oriented structure over generic technical buckets; the structure should reveal the application's intent.
- Do not let generic controller, service, or gateway folders obscure use-case ownership.
- Name modules and packages after business capabilities or use cases, use cases after action verbs, ports after the role they play for the use case, and adapters after the external detail they adapt.
- If a class is named `Service`, justify why it is not a use case, adapter, or domain object.

### 7. Component rules

- Apply SRP by separating code that changes for different actors or reasons; OCP by protecting stable policy from volatile extension details; LSP by keeping implementations substitutable; ISP by keeping interfaces focused on what each client actually needs; DIP by pointing source dependencies toward stable policy and abstractions.
- Group components by cohesion and release pressure; do not group unrelated policy merely because it shares a technical layer.
- Avoid component cycles; break them before they harden into deployment or test bottlenecks.
- Stable components must not depend on unstable details, and abstract components must have a concrete reason to exist.

### 8. Boundary cost and deployment

- A boundary may be a source boundary, deployment boundary, process boundary, service boundary, or partial boundary. Choose the lightest one that preserves the needed independence.
- Use partial boundaries when a full runtime split is too expensive but future separation is valuable.
- Do not overbuild boundaries whose cost exceeds the option value they preserve; choose boundaries by volatility, policy importance, substitution value, testability, and cost.
- Keep development, deployment, operation, and maintenance concerns visible without letting them own business policy.
- The Construction Contract requires eliminating duplication; this rule qualifies it — do not eliminate duplication when the shared code would couple use cases that change for different actors.
- Make architectural boundaries enforceable through package structure, tests, dependency rules, or build constraints.

### 9. Services, remote calls, and embedded details

- A service is not automatically an architectural boundary; source dependencies and data ownership still decide coupling.
- Treat remote calls as I/O boundaries, never as local method calls.
- Keep service listeners humble: translate external messages into use case calls and return through output boundaries.
- Keep embedded and hardware details behind interfaces so policy can be tested without the target device.

### 10. Testing through boundaries

- Prioritise tests for entities, use cases, and boundary contracts; they must run without the real framework, the real database, and the network — fast and deterministically.
- Test adapters separately for mapping correctness, gateway behaviour, controller translation, and presenter formatting.
- Do not use slow integration tests as a substitute for testing business rules.
- Test through supported boundaries: prefer use cases with fakes or mocks for ports, and use integration tests only where an architectural seam meets a real detail.
- Do not reach for private internals when a public use case boundary exists.

### 11. Forbidden patterns

- **Framework leakage** — domain entities annotated with database or web framework metadata where avoidable; use cases depending on `Request`, `Response`, controller base classes, framework sessions, or middleware; the application layer importing serializer or database base classes.
- **Database leakage** — use cases returning table rows or database-bound entities; domain rules embedded in gateway implementations; domain objects shaped primarily around persistence convenience.
- **Controller-centric logic** — controllers containing branching business rules or validation that belongs to business policy; controllers calling gateways directly instead of use cases.
- **God services** — large `*Service` classes that create, fetch, validate, persist, publish, and present everything; services owning unrelated use cases; application services used as dumping grounds.
- **Layer bypass** — controllers bypassing use cases to call gateways; presenters reading directly from databases; infrastructure code imported by domain code.
- **Direction violations** — gateway interfaces defined in infrastructure and consumed by core policy; entities importing adapters; use cases depending on concrete implementations.
- **Utility dumping grounds** — generic utility, shared, base, or core folders used as architecture escape hatches; abstractions with no clear ownership.

### 12. Refactoring toward the rule

- Move business rules inward: extract domain logic from controllers, handlers, views, gateways, and jobs.
- Introduce boundaries around details: external services, database access, message buses, filesystem operations, and clocks.
- Replace concrete dependencies with ports owned by inner layers.
- Separate translation from policy: request parsing, data mapping, serialisation, and presentation formatting belong outside core business rules.
- Break up god services by use case, and rewrite tests to target use cases and entities directly where possible.
- Refactor incrementally: prefer safe boundary extraction over large rewrites, and preserve behaviour while direction improves.

### 13. Architecture economics

- Treat architecture as the way to keep future change cost proportional to the scope of the change.
- Do not sacrifice important architectural work merely because urgent feature work is louder.
- Preserve options around frameworks, databases, delivery mechanisms, and deployment topology until evidence justifies commitment.
- Revisit architecture when change shape, team ownership, deployment needs, or operational constraints reveal rising cost.

### 14. Architecture review gate — for the change itself, not for the audit

Before presenting any change produced during this work, verify:

- [ ] Business rules are independent from frameworks, delivery, and persistence
- [ ] Source dependencies point inward at every new import
- [ ] The use case owns its input and output models, and no framework or database type crossed inward
- [ ] Controllers and presenters only translate
- [ ] Entities guard their invariants; no core rule lives in a controller, job, handler, or database script
- [ ] Ports are owned by inner layers and implemented at the edge; wiring happens at the composition root
- [ ] Core tests run without the web framework, the database, and the network
- [ ] The project structure reflects use cases, not generic technical buckets

If any answer is no, revise the design before shipping.

---
