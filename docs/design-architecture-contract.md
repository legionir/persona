# Design and Architecture Contract — extracted from A Philosophy of Software Design and Clean Architecture

This document explains how the rules of the two books *A Philosophy of Software Design* (John Ousterhout) and
*Clean Architecture* (Robert C. Martin) were turned into **two** single contracts, where they live,
and how they are wired into the personas and the skills.

> The rules themselves are **not** repeated here. The single sources:
> [`composites/blocks/91-design-depth-contract.md`](../composites/blocks/91-design-depth-contract.md) (Ousterhout) and
> [`composites/blocks/92-clean-architecture-contract.md`](../composites/blocks/92-clean-architecture-contract.md) (Clean Architecture),
> in English and in the same style as the other blocks. This document is only the extraction map and the wiring.
> The earlier contract (Clean Code + Code Complete) is documented in [`docs/construction-contract.md`](construction-contract.md).
> One further book (*Domain-Driven Design*) is documented separately:
> [`docs/domain-driven-design-contract.md`](domain-driven-design-contract.md).
> Enterprise patterns (Fowler) and the pragmatic discipline (Hunt & Thomas):
> [`docs/enterprise-patterns-contract.md`](enterprise-patterns-contract.md) ·
> [`docs/pragmatic-programmer-contract.md`](pragmatic-programmer-contract.md).
> The refactoring contract (Refactoring.Guru): [`docs/refactoring-contract.md`](refactoring-contract.md).
> The frontend design-system contract: [`docs/frontend-design-system-contract.md`](frontend-design-system-contract.md).

---

## 1. Why two blocks, not one?

These two books answer two different questions and serve two different composites:

| Block | The question it answers | Book |
|---|---|---|
| `91-design-depth-contract.md` | "How deep is this module, and how much must the reader know?" | A Philosophy of Software Design |
| `92-clean-architecture-contract.md` | "Which layer does this rule belong to, and which way do the dependencies point?" | Clean Architecture |

Merging them would produce a ~250-line block that no composite needs in full. Keeping them apart means
each composite includes only the one that matches its subject.

---

## 2. Extraction map — Ousterhout → `91-design-depth-contract.md`

| Block 91 section | Book section |
|---|---|
| `Complexity is the enemy` | Primary Directive + Symptoms of Complexity + Default Response |
| `Module depth` | Module Depth Rules + Avoid Shallow Modules + Function and Variable Rules |
| `Information hiding` | Information Hiding Rules |
| `Interface design` | Interface Design Rules |
| `Strategic over tactical programming` | Strategic Programming over Tactical Programming |
| `General-purpose vs special-purpose modules` | General-Purpose vs Special-Purpose Modules |
| `Define away exceptions` | Error Handling and Exception Elimination + Special-General Decomposition |
| `Pull complexity downward` | Pull Complexity Downward |
| `Temporal decomposition` | Temporal Decomposition Rules |
| `Combine or separate code` | Combine or Separate Code |
| `Design alternatives and comments-first design` | Design Alternatives and Comments-First Design |
| `Consistency and obviousness` | Naming, Consistency, and Obviousness |
| `Performance, trends, and tests` | Performance, Trends, and Tests |
| `Design review gate` | Review Checklist |

The book's Code Generation and Testing rules were also distributed into this block (for example "which concept deserves a module
boundary" → `Module depth`, "the test preserves public behaviour" → `Performance, trends, and tests`)
so the block list does not grow for no reason.

## 3. Extraction map — Clean Architecture → `92-clean-architecture-contract.md`

| Block 92 section | Book section |
|---|---|
| `The Dependency Rule` | Non-Negotiable Rules 1 and 10 + Architecture Heuristics (Dependency Direction) |
| `Layer responsibilities` | Required Layer Responsibilities (Domain / Application / Interface Adapters / Infrastructure) |
| `Use cases orchestrate` | Non-Negotiable Rules 8 and 9 + Code Generation Rules 1 |
| `Entities guard invariants` | Non-Negotiable Rules 2 and 9 |
| `Ports, adapters, and wiring` | Code Generation Rules 3-6 + Use Explicit Boundaries |
| `Organise by use case` | Non-Negotiable Rule 7 + Feature First Structure + Naming Rules |
| `Component rules` | Paradigm and Component Rules |
| `Boundary cost and deployment` | Boundary Cost, Deployment, and Operations + Architecture Economics |
| `Services, remote calls, and embedded details` | Services, Distribution, and Embedded Boundaries |
| `Testing through boundaries` | Testing Rules |
| `Forbidden patterns` | Forbidden Patterns |
| `Refactoring toward the rule` | Refactoring Rules |
| `Architecture economics` | Architecture Economics and Priority |
| `Architecture review gate` | Review Checklist |

### What we deliberately left out (duplicating existing blocks)

| Content | Why not | Where it lives |
|---|---|---|
| Root composition / separating construction from use | Already in the construction contract | `90-construction-contract.md` §Objects, modules, and boundaries |
| "God class" and low coupling | It appears as a smell in the construction contract; here only its *architectural* shape (`*Service` owning several use cases) | `90-construction-contract.md` §Objects, modules, and boundaries |
| Ordinary naming (one word per concept) | Ousterhout only adds "a name should reveal abstractions, not the mechanism"; the rest was duplication | `90-construction-contract.md` §Naming |
| Test quality (deterministic, isolated, one idea per test) | In the construction contract; Clean Architecture contributes the right test level | `90-construction-contract.md` §Tests |
| "Find architectural ambiguity/inconsistency" | A field of view, not a rule | `55-specialized.md` §9.7 Architecture |
| Debt classification | Stays in the debt block | `65-debt.md` |
| Severity/confidence/finding format | The Findings block owns it | `60-findings.md` |

### One deliberate contradiction, documented

The construction contract says "remove duplication aggressively"; Clean Architecture says "do not remove duplication
that would fuse two use cases with different actors". That contradiction is stated explicitly in `92-clean-architecture-contract.md`
§Boundary cost so that the model is forced into a conscious choice instead of copying another rule.

---

## 4. The shared `95-change-findings.md` block

When a composite persona proposes a change, the finding must carry the evidence and the change plan. These rules
are written once in [`composites/blocks/95-change-findings.md`](../composites/blocks/95-change-findings.md)
and included by both change-oriented personas:

- `Clean Code & Construction Review` — previously carried these two sections as `extra_sections` in its own spec.
- `Software Design & Architecture Review` — a new persona.

Before this change the same text was copied in two places; now it lives in the block and maps severity onto the
base rubric of `60-findings.md` (it does not rewrite the severity rubric).

---

## 5. Where it is wired in

| Location | 91 (design depth) | 92 (architecture boundaries) | 95 (change finding) |
|---|---|---|---|
| `Software Design & Architecture Review.md` (new composite persona) | Yes | Yes | Yes |
| `Clean Code & Construction Review.md` | ✅ | — | ✅ |
| `Technical Debt & Modernization Audit.md` | ✅ | ✅ | ✅ |
| `API & Integration Contract Audit.md` | — | ✅ | — |
| `Data & Database Integrity Audit.md` | — | ✅ | — |
| `Testing & Quality Assurance Audit.md` | — | ✅ | — |

The other composites can include a block by adding its name to `blocks` in their own spec.

---

## 6. Regeneration

```bash
python3 scripts/compose_persona.py --all
python3 scripts/build_skills.py
python3 scripts/validate_skills.py
python3 scripts/validate_personas.py
```

## 7. Adding a new rule

1. Write the rule in the relevant block (once).
2. Add the block to the `blocks` of the related composites.
3. Regenerate.
4. If the rule overlaps another block, **remove** it from that other block — keep a single source.
