# Enterprise Patterns Contract — extracted from Patterns of Enterprise Application Architecture

This document explains how the rules of the book *Patterns of Enterprise Application Architecture* (Martin Fowler)
were turned into **one** single contract, where it lives, and how it is wired into the personas and the skills.

> The rules themselves are **not** repeated here. The single source:
> [`composites/blocks/94-enterprise-patterns-contract.md`](../composites/blocks/94-enterprise-patterns-contract.md)
> (in English, in the same style as the other blocks). This document is only the extraction map and the wiring.
> The refactoring contract (Refactoring.Guru): [`docs/refactoring-contract.md`](refactoring-contract.md).
> The frontend design-system contract: [`docs/frontend-design-system-contract.md`](frontend-design-system-contract.md).

---

## 1. Extraction map

| Block 94 section | Book section |
|---|---|
| `Patterns, not invented architecture` | Purpose + Primary Directive + Architectural Baseline (Layering) |
| `Choose the business logic pattern deliberately` | Choosing the Business Logic Pattern (Transaction Script / Table Module / Domain Model) |
| `Application workflow` | Application Workflow Rules (Service Layer) |
| `Remote boundaries, facades, and DTOs` | Remote Facade + Data Transfer Object + Distribution Rules |
| `Persistence pattern choice` | Repository + Data Mapper + Row/Table Data Gateway + Active Record |
| `Unit of Work, Identity Map, and loading` | Identity, Caching, and Unit-of-Work Rules |
| `Object-relational mapping choices` | Object-Relational Mapping Pattern Index (12 patterns) |
| `Transactions and offline concurrency` | Optimistic Offline Lock + Pessimistic Locking + Coarse-Grained/Implicit Lock + Transaction Boundaries |
| `Presentation responsibilities` | Presentation Layer Rules + Presentation Pattern Index |
| `Session and cross-cutting state` | Session State Rules |
| `Base patterns worth using deliberately` | Base Pattern Index (Gateway, Mapper, Special Case, Money, Plugin, …) |
| `Testing structure, not only behaviour` | Testing Rules |
| `Enterprise patterns review gate` | Review Checklist |

## 2. What we deliberately left out (duplicating existing blocks)

| Content | Why not | Where it lives |
|---|---|---|
| Layer responsibilities, dependency direction, "every layer must justify its existence" | Layers and dependency direction are in block 92; the "pass-through module" is in block 91 | `92-clean-architecture-contract.md` §2 · `91-design-depth-contract.md` §2 |
| Repository rules (aggregate root, domain-facing interface, no generic CRUD) | The DDD block owns it | `93-domain-model-contract.md` §10 |
| "Domain logic must not live in the controller/view", "the ORM must not dictate the model" | Block 92 owns its forbidden patterns | `92-clean-architecture-contract.md` §11 |
| Value objects and immutability | The DDD block owns it | `93-domain-model-contract.md` §7 |
| "A remote call is not a local method call" | Block 92 has it | `92-clean-architecture-contract.md` §9 |
| Test quality and the domain test level | Blocks 90 and 92 own them; 94 only adds tests for the data/transaction/mapping infrastructure | `90-construction-contract.md` §11 · `92-clean-architecture-contract.md` §10 |
| Shared concurrency rules (state, immutability) | Block 90 owns it | `90-construction-contract.md` §13 |

Important note: Fowler's book had previously appeared in the repository only in scattered form (as "repository" and "gateway"),
so this block adds only what no block had: **business-logic pattern choice**,
**the persistence pattern that matches the complexity**, **Unit of Work / Identity Map / Lazy Load**,
**the ORM patterns**, **offline locking and the transaction boundary**, **the presentation-layer patterns**, and **the base patterns**.

## 3. Where it is wired in

| Location | 94 (enterprise patterns) |
|---|---|
| `Software Design & Architecture Review.md` | ✅ |
| `Domain Model & Context Review.md` | ✅ |
| `Technical Debt & Modernization Audit.md` | ✅ |
| `Data & Database Integrity Audit.md` | ✅ |
| `API & Integration Contract Audit.md` | ✅ |

`Clean Code & Construction Review` deliberately **does not** take it: that persona measures local construction quality,
and enterprise structural patterns are the home of the design/architecture and domain personas.

## 4. Regeneration

```bash
python3 scripts/compose_persona.py --all
python3 scripts/build_skills.py
python3 scripts/validate_skills.py
python3 scripts/validate_personas.py
```

## 5. Adding a new rule

1. Write the rule in `composites/blocks/94-enterprise-patterns-contract.md` (once).
2. Add the block to the `blocks` of the related composites.
3. Regenerate.
4. If the rule overlaps another block, **remove** it from that other block — keep a single source.
