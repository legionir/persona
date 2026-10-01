# Decisions for the hand-maintained composite prompts

**Recorded:** 2026-09-28  
**Scope:** the four hand-maintained prompts in `prompts/composite/`; generated composite prompts remain governed by their specs and shared blocks.

These decisions were approved as part of the corrective package before validation. They define prompt contracts; they do not claim that a target repository has been runtime-tested.

## D-CP-01 — Coverage budgets and verdicts

- **Architecture Review & Architecture Audit:** inventory 100% of declared scope; deep-review all mandatory surfaces and high-risk units; deep-review at least 20% (round up) of remaining units, or all if five or fewer remain. Record selections and excluded/unread counts. Any in-scope unread, partially read, or sampled unit forces `PARTIALLY VERIFIED` (coverage-limited).
- **Forensic Codebase Review & Audit:** `FULL` mode requires a complete declared-scope inventory and deep review of every in-scope source/configuration/test file; no sampling. `INCREMENTAL` mode covers all changed and justified affected paths, with changed/affected coverage separated from `CONTEXT_ONLY`. Any required unread item forces `PARTIALLY VERIFIED`.
- Report measured coverage and constraints; do not infer completeness from the number of files inspected or from sampling.

## D-CP-02 — Safe execution of tools

All four default to read-only inspection. Before running scripts, installing dependencies, or invoking tests/builds/linters/other commands, inspect likely side effects. Execution requires explicit user authorization and a disposable isolated workspace; report the exact command and network use. Do not touch the original checkout, production systems, credentials, or perform destructive operations. Unexecuted commands are `NOT RUN`, never `PASS`.

## D-CP-03 — Execution-plan baseline states

A new plan initializes plan progress as `NOT STARTED`, while implementation state is `UNASSESSED` unless current evidence justifies another defined state. These are separate fields: plan progress never implies the repository lacks prior implementation. Any assessed implementation state cites revision, concrete evidence, and date; update plan progress only as the planned responsibility is executed and reviewed.

## D-CP-04 — Binary and context-only inventory

The integrity-audit protocol includes binary assets in total/in-scope and T4 inventory counts by default, but treats them as inventory-only unless deep content review is requested and completed. `CONTEXT_ONLY` files are separately inventoried and counted; they do not contribute to deep-reviewed coverage or standalone findings. Counts and status categories must be disjoint and consistent across manifests, state, phase reports, and final report.

## Verification boundary

These rules were checked statically in the four source prompts. They are not a claim that any project audited by those prompts has passed the defined coverage, authorization, or runtime gates.
