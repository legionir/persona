# Frontend Design System Contract — extracted from the Doctrine of Visual & Interaction Consistency

This document explains how the rules of the *Unified Design System Doctrine* were turned into **one** single
contract, where it lives, and how it is wired into the personas and the skills.

> The rules themselves are **not** repeated here. The single source:
> [`composites/blocks/98-frontend-design-system-contract.md`](../composites/blocks/98-frontend-design-system-contract.md)
> (in English, in the same style as the other blocks). This document is only the extraction map and the wiring.

---

## 1. Why this block was needed

Until now no block spoke about the **presentation layer**, except two scattered mentions:

- `94-enterprise-patterns-contract.md` §9 says "presentation code handles input/render/transport
  and business rules must not live in the view" — that is *separation of responsibilities*.
- `97-refactoring-contract.md` §11 has the "Duplicate Code" and "Speculative Generality" smells —
  that is *treating duplication*.

But what the repository lacked was this: **the visual system inside the presentation layer** — tokens, a shared
component library, page shell and template, state coverage, and the principle that visual inconsistency is a **defect**, not a matter of taste.

## 2. Extraction map

| Block 98 section | Source document section |
|---|---|
| `Visual inconsistency is a defect` | Purpose + Primary Directive + Final Instruction |
| `Design tokens are the single source of visual truth` | The Single Source of Truth: Design Tokens (9 rules) |
| `One concept, one component` | Component Library: One Concept, One Component (7 rules) |
| `Layout and page shell consistency` | Layout & Page Shell Consistency |
| `State consistency` | State Consistency (7 states) |
| `Forms and inputs` | Forms & Input Consistency |
| `Tables, lists, and collections` | Tables, Lists & Collections Consistency |
| `Typography hierarchy` | Typography Hierarchy |
| `Colour usage discipline` | Color Usage Discipline |
| `Iconography, motion, and responsiveness` | Iconography + Motion & Animation Consistency + Responsive & Breakpoint Consistency |
| `Accessibility and theming consistency` | Accessibility Consistency + Theming Consistency |
| `Naming and file structure` | Naming & File Structure Conventions |
| `Enforce it mechanically` | Anti-Duplication Enforcement |
| `Pre-build checklist` | Mandatory Pre-Build Checklist |
| `Frontend review gate` | Review Checklist |

### What we deliberately left out

| Content | Why not | Where it lives |
|---|---|---|
| "No business rules in the view/controller", "the presentation model may differ from the domain model", the MVC/Page Controller/Front Controller/Template View patterns | Block 94 owns the presentation/domain split and the presentation-pattern choice | `94-enterprise-patterns-contract.md` §9 |
| "A duplicated component is the Duplicate Code smell", the Extract/Inline path to remove it | Block 97 owns the smell catalogue and its treatments; 98 only says which concept must become one | `97-refactoring-contract.md` §11 |
| Business-domain naming (ubiquitous language) | Block 93 owns it; 98 adds *component and file* naming and refers explicitly to 93 | `93-domain-model-contract.md` §2 |
| "The code must be understandable to the next reader" / obviousness | Blocks 91 and 95 own them | `91-` §12 · `95-` §8 |
| Test quality and assertion-free tests | Blocks 90 and 92 own them; "visual regression testing" appears in 98 only as an **enforcement mechanism**, not as a testing guide | `90-` §11 · `92-` §10 |
| Code-writing rules (routines, comments, data) | Block 90 | `90-construction-contract.md` |

## 3. Where it is wired in

| Location | 98 (frontend design system) |
|---|---|
| `Frontend & Design System Review.md` (new composite persona) | Yes |
| `Software Design & Architecture Review.md` | ✅ |

The other composites can include it by adding `"98-frontend-design-system-contract.md"` to the `blocks` in
their own spec.

## 4. The new composite persona

`Frontend & Design System Review` (6 lenses: Frontend Developer, Design System Designer,
UI Designer, Accessibility Specialist, Mobile Developer, Full-Stack Developer) with two extra sections:

- **Design System Register** — one row per token/component/template: the canonical location, the variants,
  the covered states, the usage count, parallel implementations, and token bypasses.
- **Frontend Consistency Passes** — 12 passes, each with its own ID prefix (`TKN-` token, `CMP-` component duplication,
  `API-` prop API, `SHL-` shell/template, `STT-` state coverage, `FRM-` forms, `TBL-` tables/lists,
  `TYG-` typography/colour/icon/motion, `RSP-` responsiveness/accessibility/theme, `NAM-` naming/structure,
  `ENF-` mechanical enforcement, `DRF-` drift).

## 5. Regeneration

```bash
python3 scripts/compose_persona.py --all
python3 scripts/build_skills.py
python3 scripts/validate_skills.py
python3 scripts/validate_personas.py
```

## 6. Adding a new rule

1. Write the rule in `composites/blocks/98-frontend-design-system-contract.md` (once).
2. Add the block to the `blocks` of the related composites.
3. Regenerate.
4. If the rule overlaps another block, **remove** it from that other block — keep a single source.
