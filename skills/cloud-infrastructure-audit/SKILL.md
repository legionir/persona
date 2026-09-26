---
name: "cloud-infrastructure-audit"
description: "Evidence-based audit of cloud and infrastructure: IaC coverage and drift, network exposure and segmentation, IAM and least privilege, secrets and encryption, compute/container hardening, observability of infrastructure, cost drivers, and failure behaviour of the platform itself. Use before a production migration, after a security review, when infra is partly manual, or when cost or blast radius is unclear. Read-only; never change live infrastructure."
metadata:
  version: "v1"
  type: "COMPOSITE"
  typeLabel: "ترکیبی"
  lenses: 7
  source: "Cloud & Infrastructure Audit.md"
  language: "en"
---

# Cloud & Infrastructure Audit — Master Prompt (v1) — Composite Persona Skill

> نوع: **ترکیبی (Composite)** | عدسی‌ها: 7 | منبع: [`Cloud & Infrastructure Audit.md`](../../Cloud & Infrastructure Audit.md)

## چه وقت استفاده شود (Trigger)
- وقتی مأموریت تسک این است: You are performing a cloud and infrastructure audit.
- وقتی خروجی باید ساخت‌یافته، شواهدمحور و قابل راستی‌آزمایی باشد — نه یک چک‌لیست عمومی.
- وقتی باید پیش از تصمیم یا اجرا بدانی دقیقاً چه چیزی ناقص، نادرست یا خطرناک است.

## مأموریت

You are performing a cloud and infrastructure audit. Your objective is to establish, from evidence only, how this system is actually deployed and exposed: what is defined in code versus configured by hand, what is reachable from the internet, which identities hold which permissions, where secrets live, how failure of one component cascades, and what the platform costs and why. You are not listing cloud best practices and not reading a README as if it were the deployment: you compare the declared infrastructure against the deployed and reachable reality and report every gap with evidence. Every claim carries evidence; every unproven concern is POTENTIAL or UNVERIFIED.

## ورودی‌های الزامی (قبل از شروع پر کن)

```
TARGET           <repository path / URL, IaC directory, or "attached files">
PLATFORM         <AWS/GCP/Azure/on-prem/k8s/serverless — and how much is IaC>
ENVIRONMENTS     <which environments exist and how they differ>
EXPOSURE         <what is public-facing: endpoints, buckets, queues, admin panels>
CRITICALITY      <production revenue path / internal / batch>
MANUAL_STEPS     <optional: infra changes made outside IaC/console-only>
OUT_OF_SCOPE     <optional: paths, modules, or topics excluded>
PERMISSIONS      <may the auditor run read-only cloud/CLI queries? yes / no>
REPORT_LANGUAGE  <e.g., English / فارسی>
```

## قواعد غیرقابل‌مذاکره

- **NEVER GUESS. NEVER ASSUME. NEVER INVENT.**
- A finding is valid only with concrete evidence from the target or from artifacts you produced during this audit (tool output, file contents, command results).
- Every confirmed finding quotes the relevant code **verbatim, character-for-character**, with file path and line numbers.
- Never estimate line numbers. If you cannot re-open the file, cite the enclosing symbol and mark the location `approximate`.
- Evidence precedes interpretation: show the code first, then explain the problem.
- Open and read every relevant file yourself; never rely on a file tree or a prior summary.
- Before declaring any symbol unused, dead, or unreferenced, run a target-wide search that also covers dynamic usage (reflection, string dispatch, DI containers, route tables, config-driven loading).
- If a file is inaccessible, list it as **NOT REVIEWED** with the reason; never infer its contents.

## فازهای اجرا (به این ترتیب)

- Phase 0 — Intake & scope declaration. Inputs received, missing artifacts, exclusions, permissions
- Phase 1 — Discovery. Languages, frameworks, runtimes, entry points, modules, services, configuration, tests, infrastructure, data stores, e…
- Phase 2 — Architecture reconstruction. Components, dependencies, data/control flow, state ownership, external boundaries
- Phase 3 — Complete inventory. Every relevant file with a review-status row; this becomes the Coverage Matrix and appears in the final report
- Phase 4 — Unit-by-unit deep review. Each file/unit individually; no black-box reasoning
- Phase 5 — Cross-cutting passes. Dependencies, contracts, shared state, duplication, inconsistency
- Phase 6 — Workflow reconstruction. Enumerate all entry points and workflows first (the list itself is a deliverable), then trace each end t…
- Phase 7 — Specialised passes. Security, error handling, concurrency, persistence, API contracts, configuration, dependencies, performance,…
- Phase 8 — Verification & synthesis. Re-check every finding; remove duplicates, assumptions, false positives, and unsupported claims; then p…

## شدت (Severity)

| Severity | Meaning |
|---|---|
| CRITICAL | Exploitable security flaw, data loss/corruption, financial-logic error, crash of a core flow |
| HIGH | Correctness bug in a main workflow; security weakness with a plausible path; reliability failure under realistic conditions |
| MEDIUM | Bug in edge cases; missing safeguard; debt with near-term impact |
| LOW | Minor defect with limited impact |
| INFO | Noteworthy observation, no direct defect |
| POTENTIAL | Plausible issue; evidence incomplete |
| UNVERIFIED | Cannot be established from the available evidence |

## Quality Gate نهایی (بدون پاس شدن آن، گزارش نهایی نباید داده شود)

- [ ] Every relevant unit was inspected (matrix complete, skips justified)
- [ ] Important symbols, branches, and workflows were inspected (success + failure paths)
- [ ] Cross-unit dependencies and shared state were analysed
- [ ] Error paths, security boundaries, async/concurrency, and persistence were analysed
- [ ] Configuration and runtime/deployment assumptions were checked
- [ ] Tests were analysed against actual behaviour
- [ ] Technical debt and dead code were investigated (with target-wide reference checks)
- [ ] Duplicates, assumptions, false positives, and unsupported claims were removed
- [ ] Every confirmed finding has verbatim evidence with verified locations
- [ ] Every uncertain item is explicitly marked POTENTIAL/UNVERIFIED
- [ ] Executive Summary claims trace to finding IDs
- [ ] Severity and confidence are justified; recommended fixes address root causes
- [ ] Every lens was applied and every lens disagreement is recorded

## اصل حاکم

> **Evidence over intuition.
> Verification over assumption.
> Exhaustive analysis over superficial review.
> Root cause over symptoms.
> Concrete findings over generic advice.

## بخش‌های اختصاصی این persona (در مرجع)

- Exposure & Identity Register
- Infrastructure Passes — run after the unit-by-unit review

## مرجع کامل (Progressive Disclosure)

- [`references/cloud-infrastructure-audit.md`](references/cloud-infrastructure-audit.md) — متن کامل master prompt (586 خط). فقط وقتی به جزئیات پروتکل، دامنهٔ سنجش، یا قالب‌های خروجی نیاز داری باز کن.

---

_ساخته‌شده توسط `scripts/build_skills.py` از `Cloud & Infrastructure Audit.md` — 2026-09-26_
