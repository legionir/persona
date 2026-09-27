# Pragmatic Contract — extracted from The Pragmatic Programmer

This document explains how the rules of the book *The Pragmatic Programmer* (Andrew Hunt and David Thomas) were turned into
**one** single contract, where it lives, and how it is wired into the personas and the skills.

> The rules themselves are **not** repeated here. The single source:
> [`composites/blocks/95-pragmatic-contract.md`](../composites/blocks/95-pragmatic-contract.md)
> (in English, in the same style as the other blocks). This document is only the extraction map and the wiring.
> The refactoring contract (Refactoring.Guru): [`docs/refactoring-contract.md`](refactoring-contract.md).
> The frontend design-system contract: [`docs/frontend-design-system-contract.md`](frontend-design-system-contract.md).

---

## 1. Extraction map

| Block 95 section | Book section |
|---|---|
| `Be pragmatic, not dogmatic` | Primary Directive + Own the Result + Think Beyond the Local Edit + Broken Windows Rule |
| `DRY means duplicated knowledge, not duplicated text` | DRY Rules |
| `Orthogonality` | Orthogonality Rules |
| `Tracer bullets and incremental delivery` | Tracer Bullets + Prototyping Rules + Estimation and Increment Rules |
| `Automation and tooling` | Automation Rules + Tooling Rules + Basic Tool Rules |
| `Feedback loops` | Feedback Loop Rules |
| `Contracts, assumptions, and resources` | Design by Contract + Error Handling + Resource and Coupling Rules |
| `Communication is part of the work` | Naming and Communication Rules + Text and Data Rules + Project and Team Rules |
| `Pragmatic review gate` | Review Checklist |

## 2. What we deliberately left out (duplicating existing blocks)

| Content | Why not | Where it lives |
|---|---|---|
| The Boy Scout Rule ("leave the code cleaner than you found it") | Block 90 owns it; 95 only adds "make the area better, not just the touched lines" | `90-construction-contract.md` §1 |
| Removing code duplication and the combining/separating rule | Blocks 90 and 91 own them; 95 adds the *cross-layer* DRY test (one rule = one authoritative representation) | `90-construction-contract.md` §3 · `91-design-depth-contract.md` §10 |
| The exception "do not remove duplication that would fuse two use cases" | Block 92 owns it and 95 refers to it | `92-clean-architecture-contract.md` §8 |
| Naming and documentation | Blocks 90 and 93 own them | `90-construction-contract.md` §2 · §4 · `93-domain-model-contract.md` §2 |
| The assertion / validation / domain-error split | Block 90 owns it | `90-construction-contract.md` §9 |
| Shared state and concurrency | Block 90 owns it | `90-construction-contract.md` §13 |
| Law of Demeter / train wreck | Block 90 owns it | `90-construction-contract.md` §8 |
| Reversibility and a domain DSL | Blocks 92 (keeping options open) and 93 (domain language) own them | `92-clean-architecture-contract.md` §13 · `93-domain-model-contract.md` §13 |
| Test quality and assertion-free tests | Block 90 owns it | `90-construction-contract.md` §11 |

## 3. Where it is wired in

| Location | 95 (pragmatic) |
|---|---|
| `Software Design & Architecture Review.md` | ✅ |
| `Clean Code & Construction Review.md` | ✅ |
| `Domain Model & Context Review.md` | ✅ |
| `Technical Debt & Modernization Audit.md` | ✅ |
| `Testing & Quality Assurance Audit.md` | ✅ |

`Data & Database Integrity Audit` and `API & Integration Contract Audit` deliberately do not take it:
those two personas have a narrowly defined subject (data and contracts) and take block 94, which matches their subject.

## 4. Regeneration

```bash
python3 scripts/compose_persona.py --all
python3 scripts/build_skills.py
python3 scripts/validate_skills.py
python3 scripts/validate_personas.py
```

## 5. Adding a new rule

1. Write the rule in `composites/blocks/95-pragmatic-contract.md` (once).
2. Add the block to the `blocks` of the related composites.
3. Regenerate.
4. If the rule overlaps another block, **remove** it from that other block — keep a single source.
