# Construction Contract — extracted from Clean Code and Code Complete

This document explains how the rules of the two books *Clean Code* (Robert C. Martin) and *Code Complete*
(Steve McConnell) were turned into **one** contract with no duplication, where that contract lives,
and how it is wired into the personas and the skills.

> The rules themselves are **not** repeated here. The only source of the rules:
> [`composites/blocks/90-construction-contract.md`](../composites/blocks/90-construction-contract.md)
> (in English, in the same style as the other master-prompt blocks). This document is only the merge map and the wiring.
> Two further books (*A Philosophy of Software Design* and *Clean Architecture*) are documented separately:
> [`docs/design-architecture-contract.md`](design-architecture-contract.md).
> Enterprise patterns (Fowler) and the pragmatic discipline (Hunt & Thomas):
> [`docs/enterprise-patterns-contract.md`](enterprise-patterns-contract.md) ·
> [`docs/pragmatic-programmer-contract.md`](pragmatic-programmer-contract.md).
> The refactoring contract (Refactoring.Guru): [`docs/refactoring-contract.md`](refactoring-contract.md).
> The frontend design-system contract: [`docs/frontend-design-system-contract.md`](frontend-design-system-contract.md). The evidence required for
> change findings lives in the shared `95-change-findings.md` block.

---

## 1. Why one block, not 170 copies?

The repository architecture is this: the persona prompts are **generated** (`scripts/generate_personas.py` from the README data)
and the shared audit contract lives in **reusable blocks** (`composites/blocks/`).
If we had copied the construction rules inside 170 persona files:

- every rule fix would have to be repeated 170 times (and would drift apart);
- regenerating the personas would wipe out manual edits;
- the repository size and the model context would double for no reason.

So the golden rule of this change: **one source, many references.** The rules are written once and the related composites
include that block; the skills point at the same single text through `references/`.

---

## 2. Merge map (which sections became one)

The two source documents said the same thing with different words in many places. The merge was done like this:

| Contract section | From Clean Code | From Code Complete | Merge decision |
|---|---|---|---|
| `Priority` | Priority and behavior, Implementation preferences | Primary Directive, Construction Prerequisites | Both said the same thing: "the next reader matters more than cleverness" → one section |
| `Naming` | Naming rules | Variable and Data Rules (the naming part) | Merged; the "one word per concept" and "no encoding" rules appear once |
| `Routines` | Function rules | Routine Design Rules | Merged; the shared anti-patterns appear once |
| `Comments` | Comment rules | Comment Rules | Merged; the "good comment" list appears once |
| `Formatting and structure` | Formatting and structure | Coding Standards Rules, Statement Rules (the layout part) | Merged |
| `Data and types` | Objects, modules, and data structures (the data part) | Variable Rules, Data Type Rules | Merged; "magic value/unit/domain" appears once |
| `Control flow` | Function rules (the control-flow part) | Control Flow Rules, Statement/Conditional/Loop Rules | Merged |
| `Objects, modules, and boundaries` | Objects and data structures, Boundaries | Class and Module Design, Boundaries | Merged; "god class" and "train wreck" appear once |
| `Errors and defensive programming` | Error handling | Defensive Programming, Error Handling, Preconditions/Postconditions | Merged; the assertion/validation/domain-error split appears once |
| `Complexity and smells` | Smells to detect and eliminate | Complexity Management, Forbidden Patterns, Review Rules | Merged; the smell list appears once (debt classification stays in the `65-debt` block) |
| `Tests` | Tests, TDD and clean test rules | Testing Rules | Merged; "tests are production code" appears once |
| `Refactoring and change process` | Refactoring rules, Emergent design, Change Process | Incremental Construction, Quality/Refactoring | Merged; the change-process checklist appears once |
| `Concurrency` | Concurrency and async work | — (absent from Code Complete) | Came from Clean Code, with no change of meaning |
| `Construction review gate` | Review checklist | Review Checklist | The two checklists were nearly identical → merged into **one** |

### What was deliberately dropped (to avoid duplicating existing blocks)

| Content | Why we left it out | Where it lives |
|---|---|---|
| Technical-debt classification (accidental/architectural/testing/…) and the "check repository-wide before declaring dead" rule | Mentioned in the construction contract only as a *smell*, without restating it | `composites/blocks/65-debt.md` |
| Test gaps (what is not tested) | The construction contract only covers *how well tests are written*; "what is missing" stays in the specialised pass | `composites/blocks/55-specialized.md` (§9.6) |
| The evidence rules and "no guessing" | A different subject: claims about the codebase, not code quality | `composites/blocks/10-prime-directive.md` |
| The audit's final Quality Gate | Our gate is for *the change itself*, not for audit coverage | `composites/blocks/80-quality-gate.md` |

---

## 3. Where it is wired in

| Location | Status |
|---|---|
| `composites/blocks/90-construction-contract.md` | The single source of the rules |
| `Clean Code & Construction Review.md` (new composite persona) | The whole contract + the Staff/Principal/Architect/Refactoring/Test-Automation/Docs lenses |
| `Technical Debt & Modernization Audit.md` | Block added (debt ↔ construction rules) |
| `Testing & Quality Assurance Audit.md` | Block added (test quality) |
| `skills/clean-code-construction-review/`, `skills/technical-debt-modernization-audit/`, `skills/testing-quality-assurance-audit/` | Regenerated automatically; `SKILL.md` carries only the **section map** and does not copy the rules |

The other composites can include this contract by adding `"90-construction-contract.md"` to the `blocks` of their own spec
(they are not included by default, so no duplicated content appears).

### How duplication was avoided in the skills

In the `SKILL.md` files only the **list of the master prompt's sections** appears (marked with `◆` for the persona-specific ones),
for example:

```
## Master prompt map (in the reference — ◆ = section specific to this persona)
- PRIME DIRECTIVE — ZERO ASSUMPTIONS
- CONSTRUCTION CONTRACT — Clean Code + Code Complete (binding)
- ◆ Construction Findings — required evidence
```

The rules themselves live only in `references/<persona>.md`. That is progressive disclosure:
the model sees the map first and opens the reference only when it needs the rules.

---

## 4. Regeneration

```bash
python3 scripts/compose_persona.py --all          # build the master prompts from block + spec
python3 scripts/build_skills.py                   # regenerate the skills
python3 scripts/validate_skills.py                # validate
python3 scripts/validate_personas.py              # validate the role personas
```

## 5. Adding a new rule to the contract

1. Write the rule in `composites/blocks/90-construction-contract.md` (once).
2. If a new composite persona should have it, add the block to that spec's `blocks`.
3. `python3 scripts/compose_persona.py --all && python3 scripts/build_skills.py`
4. If the rule overlaps another block, **remove** it from that other block (do not copy it here) — keep a single source.
