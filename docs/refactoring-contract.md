# Refactoring Contract — extracted from Refactoring.Guru

This document explains how the general rules of refactoring (based on the
[Refactoring.Guru](https://refactoring.guru/refactoring) catalogue and its
[what-is-refactoring](https://refactoring.guru/refactoring/what-is-refactoring),
[technical-debt](https://refactoring.guru/refactoring/technical-debt),
[when](https://refactoring.guru/refactoring/when),
[how-to](https://refactoring.guru/refactoring/how-to),
[smells](https://refactoring.guru/refactoring/smells), and
[catalog/techniques](https://refactoring.guru/refactoring/catalog) sections) were turned into **one** single
contract, where it lives, and how it is wired into the personas and the skills.

> The rules themselves are **not** repeated here. The single source:
> [`composites/blocks/97-refactoring-contract.md`](../composites/blocks/97-refactoring-contract.md)
> (in English, in the same style as the other blocks). This document is only the extraction map and the wiring.
> The frontend design-system contract: [`docs/frontend-design-system-contract.md`](frontend-design-system-contract.md).

---

## 1. Why this block was needed

The repository already had "refactor in small steps" and "leave the code cleaner" (in the construction contract),
but it lacked three things:

1. **Separating refactoring from feature/bug work** plus the discipline of verifying and the **stop condition**.
2. **A smell catalogue with trigger → treatment → replacement → the expensive option** (that is, from "smell" to "treatment").
3. **Smell exception rules** that prevent mechanical refactoring and over-engineering.

This block is exactly those three things, and it refers everything else to the owning block.

## 2. Extraction map

| Block 97 section | Source section |
|---|---|
| `Refactoring is controlled improvement` | Purpose + What Is Refactoring? |
| `Keep refactoring separate from other work` | Keep Refactoring and Adding New Features Separate |
| `Work in small steps` | Work in Small Steps |
| `Verify continuously` | Verify Continuously (including "do not delete a broken test") |
| `Keep the result cleaner` | Keep the Result Cleaner + the planned-rewrite rule |
| `When to refactor` | When to Refactor: Rule of Three + While Adding a Feature + While Fixing a Bug + During Code Review |
| `Technical debt, operationally` | Technical Debt (operational rules only; classification stays in `65-debt`) |
| `Smell detection: scan in this order` | Smells → the six categories Bloaters / OO Abusers / Change Preventers / Dispensables / Couplers / Library Gaps |
| `Diagnose, treat, verify, stop` | Diagnose → Treat → Verify → Stop (Do Not Refactor if...) |
| `Smell exception rules` | Smell Exception Rules (MAY/MUST NOT) |
| `Smell catalog: triggers and treatments` | Code Smells + Smell-to-Treatment Priority Map (22 smells) |
| `Technique selection` | Techniques → the six families (Composing Methods, Moving Features, Organizing Data, Simplifying Conditionals, Simplifying Method Calls, Dealing with Generalization) |
| `Technique execution safety` | Technique Execution Safety (Extraction/Inlining/Moving/Encapsulation/Conditional/Method Call/Data/Generalization) |
| `Decision anti-patterns` | Decision Anti-Patterns |
| `Refactoring workflow for agents` | Refactoring Workflow for Agents (Before/During/After) |
| `Refactoring review gate` | Review Checklist |

### What was deliberately compressed

The playbook of 66 techniques (each with Symptom/Use/Avoid/Safe steps/Verify) was compressed into two sections:
`Technique selection` (which technique for which smell) and `Technique execution safety` (the safety rules
shared by all techniques). The generic steps of each technique were not repeated, because the block must be an execution policy,
not a step-by-step tutorial.

## 3. What we deliberately left out (duplicating existing blocks)

| Content | Why not | Where it lives |
|---|---|---|
| "Small, safe steps", "make it work then make it right", "do not do a big redesign", "leave the code cleaner" | Block 90 owns the change process | `90-construction-contract.md` §12 |
| The one-line list of complexity signals (misleading name, dead code, coupling, …) | Block 90 has it from Clean Code/Code Complete; 97 only adds "trigger → treatment → exception" and refers to it explicitly in §11 | `90-construction-contract.md` §10 |
| "Every step behaviour-preserving", "characterization test first", "rename before restructure", "verification + rollback per step" | Block 96 owns the change-plan rules | `96-change-findings.md` §3 |
| Technical-debt classification (13 classes) and the repository-wide check before declaring something dead | Block 65 owns it; 97 has only the operational rules (debt origin, gradual repayment, the ban on a future cleanup project) | `65-debt.md` |
| ORM, transactions, layering, aggregates, and repositories | Blocks 92/93/94 own them | `92-` · `93-` · `94-` |
| Test quality and assertion-free tests | Blocks 90 and 92 own them | `90-construction-contract.md` §11 · `92-` §10 |
| DRY and orthogonality | Block 95 owns them | `95-pragmatic-contract.md` |

## 4. Where it is wired in

| Location | 97 (refactoring) |
|---|---|
| `Clean Code & Construction Review.md` | ✅ |
| `Software Design & Architecture Review.md` | ✅ |
| `Technical Debt & Modernization Audit.md` | ✅ |
| `Domain Model & Context Review.md` | ✅ |
| `Testing & Quality Assurance Audit.md` | ✅ |

`Data & Database Integrity Audit` and `API & Integration Contract Audit` deliberately do not take it:
they have a narrowly defined subject (data and contracts) and take `94-`.

## 5. Regeneration

```bash
python3 scripts/compose_persona.py --all
python3 scripts/build_skills.py
python3 scripts/validate_skills.py
python3 scripts/validate_personas.py
```

## 6. Adding a new rule

1. Write the rule in `composites/blocks/97-refactoring-contract.md` (once).
2. Add the block to the `blocks` of the related composites.
3. Regenerate.
4. If the rule overlaps another block, **remove** it from that other block — keep a single source.
