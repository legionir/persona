# How to Build a Composite Persona

> Composite personas are the master prompts in `prompts/composite/`:
> `Forensic Codebase Review & Audit.md`, `Architecture Review & Architecture Audit.md`,
> `codebase-integrity-audit-protocol.md`, `Execution Plan Generator.md`, and
> `Production Readiness & Reliability Audit.md`.
> They differ from the role personas in `prompts/audit/` and `prompts/implementation/` in one respect: **they are not a single role — they run several roles at the same time.**

---

## 1. What is a composite persona?

| | Role persona (`prompts/**`) | Composite persona (root) |
|---|---|---|
| Identity | One job title, one type (supervisor/executor) | Several roles acting as *lenses* |
| Contract | The 29 standard Master sections | A free-form, phase-oriented protocol |
| Mission | A single `PrimaryGoal` | One compound mission (for example "forensic codebase audit") |
| Output | A report/code per the contract | A multi-part report with a Coverage Matrix and a Quality Gate |
| Length | ~550 lines | ~300 to ~800 lines |
| Regeneration | `generate_personas.py` | `compose_persona.py` (from block + spec) |

The foundational rule: **a composite is not two prompts glued together.** If you concatenate two personas, the model either lets one dominate the other or lands in contradiction. A composite persona must:

1. Have **one single mission** that ranks above every lens.
2. Apply each lens **independently** (every finding carries a lens label).
3. Have a **precedence rule** for resolving contradictions.
4. Have **one shared protocol** (phases, evidence, coverage, finding format, Quality Gate).

---

## 2. Anatomy of a composite persona (11 layers)

```
# <Title> — Master Prompt (vN)          <- layer 0: title + version
## 1. MISSION + Lens Table              <- layer 1: the single mission + the lens table
## 2. PRIME DIRECTIVE — ZERO ASSUMPTIONS<- layer 2: non-negotiable rules (evidence)
## 3. SCOPE, INPUTS, MISSING ARTIFACTS  <- layer 3: scope and the "unknown things" protocol
## 4. AUDIT PROTOCOL (Phases 0..N)      <- layer 4: execution order + anti-sampling
## 5. LENS SWEEP AND PRECEDENCE         <- layer 5: independent lens runs + conflict resolution
## 6. FILE-BY-FILE / LINE-LEVEL / ...   <- layer 6: depth blocks (optional, forensic audits)
## N. COVERAGE CONTROL — AUDIT MATRIX   <- layer N: coverage control (against a false "fully reviewed")
## N. FINDINGS (severity/confidence)    <- layer N: finding format + prioritisation
## N. <Domain extras>                   <- layer N: the sections specific to this composite
## N. BEHAVIOURAL RULES + QUALITY GATE  <- layer N: behaviour and the final gate
## N. CORE PRINCIPLE                    <- layer N: the governing principle
## Appendix C — Source Personas          <- traceability: which personas it was assembled from
```

---

## 3. Ready-made blocks (`composites/blocks/`)

Each block is one tested slice of protocol and is reused across several composites:

| Block | Contents | Required? |
|---|---|---|
| `00-header.md` | Title, how-to-use note, summary of the order of operations | Yes |
| `10-prime-directive.md` | Mission, the lens table, "no guessing", the evidence standard, the language ban | Yes |
| `20-scope-artifacts.md` | What counts as evidence, scope, the missing-artifact protocol | Yes |
| `30-protocol.md` | The depth ladder, anti-sampling, phases, the continuation protocol | Yes |
| `40-lenses.md` | The lens sweep, conflict resolution, `{{PRECEDENCE}}` | Yes |
| `50-coverage.md` | The coverage matrix | Yes |
| `60-findings.md` | Validation, severity, confidence, finding format, de-duplication, prioritisation | Yes |
| `70-report.md` | The final report structure | Yes |
| `80-quality-gate.md` | Behavioural rules + Quality Gate + the governing principle | Yes |

### Depth blocks (optional — for forensic audits)

These blocks were extracted from the strength of `prompts/composite/Forensic Codebase Review & Audit.md`; add them wherever the audit must be genuinely file-by-file and line-by-line rather than a shallow summary:

| Block | Contents |
|---|---|
| `25-file-by-file.md` | The 28 things that must be established for **every file** (side effects, state mutation, resources, dead code, …) |
| `35-line-level.md` | Function tracing, the target bug classes, the high-risk zones (auth, money, migration, concurrency, …) |
| `45-cross-file.md` | Cross-file analysis + workflow reconstruction (success/failure) + data flow |
| `55-specialized.md` | The 12 specialised audit domains (security, error, concurrency, DB, API, testing, architecture, config, deps, perf, observability, build/deploy) |
| `65-debt.md` | Technical debt (13 classes) + dead and suspicious code + the rule to check repository-wide before declaring something dead |
| `90-construction-contract.md` | The code construction contract: single merge of Clean Code + Code Complete (naming, routines, comments, data, control flow, errors, smells, tests, refactoring, concurrency, the review gate) |
| `91-design-depth-contract.md` | The design-depth contract: single merge of A Philosophy of Software Design (complexity, module depth, information hiding, interfaces, strategic versus tactical, eliminating exceptions, pulling complexity downward, temporal decomposition, combining/separating, comments-first design) |
| `92-clean-architecture-contract.md` | The architecture-boundaries contract: single merge of Clean Architecture (the dependency rule, layer responsibilities, use cases and entities, ports and adapters, use-case-based structure, component rules, boundary cost, testing through the boundary, forbidden patterns) |
| `93-domain-model-contract.md` | The domain-model contract: single merge of DDD (ubiquitous language, bounded context and context map, subdomains and distillation, entity/value object/aggregate, domain service and specification, repository/factory, domain event and event sourcing, translation at the boundaries, choice-making DDD) |
| `94-enterprise-patterns-contract.md` | The enterprise-patterns contract: single merge of PoEAA (business-logic pattern choice, the persistence pattern, Unit of Work/Identity Map/Lazy Load, ORM patterns, offline locking and the transaction boundary, presentation patterns, base patterns) |
| `95-pragmatic-contract.md` | The pragmatic contract: single merge of The Pragmatic Programmer (DRY means knowledge not text, orthogonality, tracer bullets, automation, the feedback loop, contracts and resources, communication) |
| `96-change-findings.md` | The evidence required for every change finding + the change-plan rules (it maps severity onto the base Findings rubric instead of rewriting it) |
| `97-refactoring-contract.md` | The refactoring contract: single merge of Refactoring.Guru (separating refactoring from feature/bug work, small steps, verification and the stop condition, the rule of three, the six smell categories with trigger → treatment → replacement, smell exception rules, technique selection and safety, decision anti-patterns, the agent workflow) |
| `98-frontend-design-system-contract.md` | The frontend design-system contract: single merge of the Doctrine of Visual & Interaction Consistency (tokens, one concept = one component, a uniform prop API, shell and template, state coverage, forms, tables, typography, colour, iconography, motion, responsiveness, accessibility, theming, naming, mechanical enforcement) |

Suggested order for a full forensic audit:

```
00 → 10 → 20 → 30 → 40 → 25 → 35 → 45 → 55 → [65] → 50 → 60 → [extra] → 80
```

`{{EXTRA_SECTIONS}}`/`insert_before` is where the spec's own extra sections are inserted (default: before `80-quality-gate.md`).

**Numbering rule:** blocks carry fixed numbers so each stands alone; in the final composite the numbers are recomputed (`## N.` and `### N.M`). For that reason **never refer to a section by its number** — always by name (§"Final Quality Gate", "Appendix B").

---

## 4. Spec format (`composites/<slug>.json`)

```json
{
  "$schema": "composite-persona/v1",
  "slug": "production-readiness-reliability-audit",
  "title": "Production Readiness & Reliability Audit",
  "version": "v1",
  "language": "en",
  "output": "Production Readiness & Reliability Audit.md",
  "description": "<trigger description for the skill — optional>",
  "mission": "<the single mission, at least 40 characters>",
  "order": "intake → discovery → … → gated report",
  "inputs": [{"name": "TARGET", "hint": "repository path / URL"}],
  "lenses": ["prompts/audit/release-manager.md", "…"],
  "lens_focus": {"Release Manager": "release gates, rollback, …"},
  "precedence": ["<rule 1>", "<rule 2>"],
  "blocks": ["00-header.md", "10-prime-directive.md", "…"],
  "insert_before": "80-quality-gate.md",
  "extra_sections": [{"title": "Readiness Gates", "body": "…"}]
}
```

The automatic validation (`--check`) checks all of this: a non-empty title/mission, `inputs` entries that have a name, **2 to 12 lenses** (each one a valid, non-duplicated persona), the presence of every block, no duplicated block, a non-empty `precedence`, and that every `{{PLACEHOLDER}}` resolves.

## 4.1 Eight-auditor codebase matrix

For integrated codebase reviews, [`docs/eight-auditor-matrix.md`](eight-auditor-matrix.md) is the canonical scope and separation matrix for Security, Architecture, Code Quality, Performance, Reliability, Testing, Dependency, and DevOps. The [Codebase Integrity Audit Protocol](../prompts/composite/codebase-integrity-audit-protocol.md) applies it through an evidence-based applicability gate, supports changed-file CI runs, and consolidates cross-auditor findings before final severity calibration. Update the matrix first when scope ownership changes.

### Allowed placeholders

`{{TITLE}}` `{{VERSION}}` `{{MISSION}}` `{{INPUTS}}` `{{ORDER}}`
`{{LENS_TABLE}}` `{{LENS_COUNT}}` `{{PRECEDENCE}}` `{{EXTRA_SECTIONS}}`

---

## 5. Decisions for the four hand-maintained composites

The following operating decisions apply to the four hand-maintained protocols in `prompts/composite/` and are recorded for this revision in [`composite-persona-decisions.md`](composite-persona-decisions.md):

- Coverage is budgeted explicitly and reported with counts; sampling or unread in-scope material prevents a full-verification verdict.
- Tool execution is opt-in: inspect side effects first, require explicit authorization, use a disposable isolated workspace, record exact commands/network use, and label unrun commands `NOT RUN`.
- Execution plans separate repository implementation evidence from plan progress; new plan steps begin `UNASSESSED` / `NOT STARTED` unless evidence supports another state.
- Binary assets and unchanged context-only files are inventoried and counted in distinct, non-overlapping classes; neither is silently counted as deeply reviewed.

## 6. Build and regeneration

```bash
# list the blocks and specs
python3 scripts/compose_persona.py --list

# build one composite
python3 scripts/compose_persona.py --spec composites/production-readiness-reliability-audit.json

# build everything, validate only (write nothing)
python3 scripts/compose_persona.py --all
python3 scripts/compose_persona.py --all --check
```

The default output is written to `prompts/composite/` (`output` in the spec names the file; `--out-dir` overrides the directory), alongside the other master prompts.

---

## 7. Quality checklist before publishing a composite

- [ ] The mission is **one** compound sentence and is not attributable to any single lens.
- [ ] 2 to 12 lenses, all from `prompts/`, all genuinely needed (not decorative).
- [ ] Each lens has a distinct, specific `focus` in the table.
- [ ] `precedence` has at least one conflict-resolution rule (data/security over speed, recoverability over capability …).
- [ ] The evidence rules ("no guessing, no inventing, verbatim evidence") are present.
- [ ] The phase-oriented protocol and the "continue on a large codebase" protocol are present.
- [ ] The coverage matrix is mandatory and the "it is complete" claim is tied to it.
- [ ] Finding format, severity, and confidence are separate from each other.
- [ ] The final Quality Gate exists with checkable checkboxes.
- [ ] No numeric references to sections (names only).
- [ ] The source of the lenses is recorded in an appendix (traceability back to the origin personas).
- [ ] If the audit subject touches code-construction quality, the `90-construction-contract.md` block is included
      (and no other block copies similar rules).
- [ ] If the audit subject touches code-construction quality, the `90-construction-contract.md` block is included
      (and no other block copies similar rules).
- [ ] If the audit subject touches design/architecture, the `91-` and/or `92-` blocks are included.
- [ ] If the audit subject touches the domain model, the `93-domain-model-contract.md` block is included
      (and the layer/oversight rules that live in `92-` are not written again).
- [ ] If the composite proposes changes, the `96-change-findings.md` block is included
      (instead of rewriting the finding evidence in `extra_sections`).
- [ ] If the composite proposes structural change/refactoring, the `97-refactoring-contract.md` block is included
      (and the change process and plan rules are not repeated from `90-`/`96-`).
- [ ] If the composite audits frontend/UI, the `98-frontend-design-system-contract.md` block is included
      (and the presentation/domain split from `94-` and the smell catalogue from `97-` are not repeated).

---

## 8. Example: `Production Readiness & Reliability Audit`

Practical style:

```bash
python3 scripts/compose_persona.py --list
python3 scripts/compose_persona.py --spec composites/production-readiness-reliability-audit.json
```

Result: a master prompt with 7 lenses (Release Manager, QA Lead, Security Architect, SRE,
DevOps Engineer, Observability Engineer, DBA), 12 "readiness gates" (Rollback/Restore/Migration/Deploy/…)
each of which takes `PASS/FAIL/BLOCKED/NOT_APPLICABLE`, and 6 specialised passes
(failure-mode, recovery, observability, data, release/ops, cost).

## 9. The repository's composite catalogue

| Composite | Lenses | Focus |
|---|---|---|
| `forensic-codebase-review-audit` | — | Forensic codebase review (file by file, line by line, no guessing) |
| `clean-code-construction-review` | 6 | Code-construction quality per the Clean Code + Code Complete contract |
| `software-design-architecture-review` | 6 | Design depth and dependency direction per Philosophy of Software Design + Clean Architecture |
| `domain-model-context-review` | 6 | Ubiquitous language, bounded context, and the domain model per DDD (Evans / Vernon) |
| `frontend-design-system-review` | 6 | Tokens, the component library, shell/template, and state coverage in the frontend |
| `architecture-review-architecture-audit` | — | Architecture review with Tier/Size classification and a 0-100 score |
| `codebase-integrity-audit-protocol` | — | Consistency and workflow, phase by phase and resumable (P0-P10) |
| `execution-plan-generator` | — | Turning a large task into a phased execution plan |
| `production-readiness-reliability-audit` | 7 | Production readiness: Rollback/Restore/Migration/Observability/SLO |
| `forensic-security-threat-audit` | 8 | Attack surface and trust boundaries; exploitable versus theoretical |
| `data-database-integrity-audit` | 6 | Data consistency, migration, transactions, backup/restore |
| `api-integration-contract-audit` | 6 | API contract and integration; documentation-implementation drift |
| `ai-agent-system-audit-hardening` | 6 | LLM/Agent systems: tools, permissions, evals, unsafe paths |
| `performance-scalability-audit` | 6 | Bottlenecks, resource ceilings, behaviour at 10x and 100x |
| `technical-debt-modernization-audit` | 6 | Technical debt by cost of change; a gradual migration path |
| `testing-quality-assurance-audit` | 6 | What the suite actually proves; assertion-free tests and coverage gaps |
| `incident-forensic-review-postmortem` | 6 | Timeline reconstruction, the causal chain, detection and recovery gaps |
| `cloud-infrastructure-audit` | 7 | IaC and drift, exposure, IAM, secrets, blast radius, cost |
| `privacy-compliance-audit` | 6 | Personal-data flow, control-evidence, data-subject rights, third-party sharing |

## 10. Building a new composite

1. `cp composites/production-readiness-reliability-audit.json composites/<slug>.json`
2. Write `title`/`mission`/`inputs`/`lenses`/`lens_focus`/`precedence`/`extra_sections`.
3. Choose the order in `blocks` (for a forensic audit, bring the `25/35/45/55` blocks too).
4. `python3 scripts/compose_persona.py --spec composites/<slug>.json`
5. Convert it into a skill: `python3 scripts/build_skills.py` (guide: [`persona-skills.md`](persona-skills.md))
