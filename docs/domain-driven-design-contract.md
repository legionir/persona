# Domain Model Contract — extracted from Domain-Driven Design (Evans, Vernon ×2)

This document explains how the rules of the three books *Domain-Driven Design* (Eric Evans),
*Domain-Driven Design Distilled*, and *Implementing Domain-Driven Design* (Vaughn Vernon) were turned into
**one** single contract, where it lives, and how it is wired into the personas and the skills.

> The rules themselves are **not** repeated here. The single source:
> [`composites/blocks/93-domain-model-contract.md`](../composites/blocks/93-domain-model-contract.md)
> (in English, in the same style as the other blocks). This document is only the merge map and the wiring.
> The earlier contracts: [`docs/construction-contract.md`](construction-contract.md) (Clean Code + Code Complete) and
> [`docs/design-architecture-contract.md`](design-architecture-contract.md) (Ousterhout + Clean Architecture).
> Enterprise patterns (Fowler) and the pragmatic discipline (Hunt & Thomas):
> [`docs/enterprise-patterns-contract.md`](enterprise-patterns-contract.md) ·
> [`docs/pragmatic-programmer-contract.md`](pragmatic-programmer-contract.md).
> The refactoring contract (Refactoring.Guru): [`docs/refactoring-contract.md`](refactoring-contract.md).
> The frontend design-system contract: [`docs/frontend-design-system-contract.md`](frontend-design-system-contract.md).

---

## 1. Three books, one contract

The three books cover one subject with different emphases, so a single block with 15 sections was built:

| Source | Its contribution to the block |
|---|---|
| **DDD (Evans)** | Strategic (bounded context, context mapping, distillation, large-scale structure) and tactical (entity, value object, aggregate, domain service, specification, repository, factory, supple design) |
| **DDD Distilled (Vernon)** | Choice-making: subdomain classification, integration styles (RPC/REST/messaging), aggregate minimalism, event storming, and "DDD theatre" |
| **Implementing DDD (Vernon)** | Hands-on implementation: aggregate rules, domain events and event sourcing, transformation services, ACL and identity across contexts, package structure |

Every rule that appeared in more than one book was written **once** (the aggregate rules, for example, were nearly identical in all three books).

## 2. Merge map

| Block 93 section | Source |
|---|---|
| `The model serves the business meaning` | Primary Directive (all three) + What DDD Means in This Repository |
| `Ubiquitous language` | Ubiquitous Language (Evans + Distilled + IDDD) |
| `Bounded contexts` | Bounded Contexts (Evans) + Bounded Context Is Mandatory (IDDD) + Define Bounded Contexts Early (Distilled) |
| `Strategic design: subdomains and distillation` | Strategic Design + Distillation (Evans) + Start with Subdomains (Distilled) + Core Domain Protection (IDDD) |
| `Context mapping and integration` | Model Integrity Patterns + Context Mapping (Evans) + Context Relationship Rules + Integration Style Rules (Distilled) + Context Integration (IDDD) |
| `Entities` | Entities (Evans + Distilled + IDDD) |
| `Value objects` | Value Objects (Evans + Distilled + IDDD) |
| `Aggregates` | Aggregates (Evans) + Aggregate Minimalism (Distilled) + Aggregate Rules of Thumb (IDDD) |
| `Domain services and specifications` | Domain Services + Explicit Concepts and Specifications (Evans) + Domain and Transformation Service Rules (IDDD) |
| `Repositories and factories` | Repositories + Factories (Evans) + Repository Rules (IDDD) |
| `Domain events and eventual consistency` | Domain Event Rules + Event Sourcing (IDDD) + Domain Events (Distilled) |
| `Application layer, infrastructure, and translation` | Application Layer + Infrastructure + Translation at Boundaries (Evans) + Architecture and Infrastructure Rules (Distilled) |
| `Supple design` | Supple Design + Analysis and Model Patterns (Evans) |
| `Practicality: selective, serious DDD` | Adoption Fit (Distilled) + Practical Simplicity Rule (IDDD) + What DDD Does Not Mean (Evans) |
| `Domain model review gate` | Review Checklist (all three) |

## 3. What we deliberately left out (duplicating existing blocks)

This is the most important part: DDD overlaps Clean Architecture heavily, and block 92 already owns that overlap.

| Content | Why not | Where it lives |
|---|---|---|
| Layer responsibilities, dependency direction, use case as orchestration | Block 92 owns it | `92-clean-architecture-contract.md` §2-§3 |
| Root composition, port/adapter, hiding the implementation | Block 92 owns it | `92-clean-architecture-contract.md` §5 |
| "An entity must guard its invariants" (in general) | 92 has it; 93 only adds identity, lifecycle, and the ban on public setters | `92-clean-architecture-contract.md` §4 |
| Framework/database leakage into inner layers, god services, layer bypass | Block 92 owns the forbidden architecture patterns | `92-clean-architecture-contract.md` §11 |
| The SRP/OCP/LSP/ISP/DIP rules and the component cycle | Block 92 owns it | `92-clean-architecture-contract.md` §7 |
| Testing through the boundary, without framework/database/network | Block 92 owns the test level | `92-clean-architecture-contract.md` §10 |
| Good naming, types that make invalid values harder to represent | Block 90 owns it; 93 only adds "which domain the word comes from" and "every concept must have a name" | `90-construction-contract.md` §2 and §6 |
| Test quality (deterministic, isolated, one idea per test) | Block 90 owns it | `90-construction-contract.md` §11 |
| The duplication-removal rule and code combining/separating | Block 91 owns it | `91-design-depth-contract.md` §10 |
| Change-finding evidence + change plan | The shared block 95 | `95-change-findings.md` |

### The explicit boundary between 92 and 93

These two blocks are deliberately split this way:

- `92-clean-architecture-contract.md` → **which way the dependencies point and which layer owns which rule.**
- `93-domain-model-contract.md` → **what meaning the model carries: language, semantic boundaries, and the tactical building blocks.**

Wherever the two meet (application service, infrastructure, translation, test level), block 93
states only the domain-specific rule and refers the rest to 92 — for example, §12 says explicitly
"layer and use-case rules stay with the Architecture Boundaries contract".

## 4. Where it is wired in

| Location | 93 (domain model) |
|---|---|
| `Domain Model & Context Review.md` (new composite persona) | Yes |
| `Software Design & Architecture Review.md` | ✅ |
| `Technical Debt & Modernization Audit.md` | ✅ |
| `API & Integration Contract Audit.md` | ✅ |
| `Data & Database Integrity Audit.md` | ✅ |
| `Testing & Quality Assurance Audit.md` | ✅ |

`Clean Code & Construction Review` deliberately **does not** take 93: that persona measures local construction quality (naming, routines,
data, control flow, tests), and the domain model is the home of the new persona and of `Software Design & Architecture Review`.
The other composites can include it by adding `"93-domain-model-contract.md"` to the `blocks` of their own spec.

## 5. The new composite persona

`Domain Model & Context Review` (6 lenses: Staff Engineer, Principal Engineer, Software Architect,
Domain Expert/SME, Refactoring Engineer, Legacy Modernization Engineer) with two extra sections:

- **Bounded Context & Language Register** — one row per context: vocabulary, model elements, subdomain,
  the context-map relationship, the translation owner, and leakages.
- **Domain Modeling Passes** — 11 passes, each with its own ID prefix (`LNG-` language, `IMP-` implicit concepts,
  `CTX-` context, `MAP-` context mapping, `SUB-` subdomain, `ENT-` entity, `VAL-` value object,
  `AGG-` aggregate, `SVC-` service/specification/event, `REP-` repository/factory/translation,
  `THT-` DDD theatre).

## 6. Regeneration

```bash
python3 scripts/compose_persona.py --all
python3 scripts/build_skills.py
python3 scripts/validate_skills.py
python3 scripts/validate_personas.py
```

## 7. Adding a new rule

1. Write the rule in `composites/blocks/93-domain-model-contract.md` (once).
2. Add the block to the `blocks` of the related composites.
3. Regenerate.
4. If the rule overlaps another block, **remove** it from that other block — keep a single source.
