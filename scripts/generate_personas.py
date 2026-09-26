#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Master-schema-compliant persona generator.

Generates every persona under prompts/ with the exact persona-schema contract:

  * 01. Identity  ..  29. Mandatory Rules          (section 61)
  * 10 extra headings for SUPERVISOR personas      (section 62)
  * 12 extra headings for EXECUTOR personas        (section 63)
  * Role registry + executor->supervisor map       (sections 62..65)

Per-role content comes from the 23-column details table (previously details.md,
now merged into README.md), merged with the bespoke per-role specs
(SPECS + role_extras.EXTRA_SPECS).  Roles never fall back to silently generic
content: missing data is rendered as
"Unknown / Requires Verification: ..." (Master rule 3 of section 67).

Usage:
    python3 scripts/generate_personas.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))

from generate_role_prompts import (  # noqa: E402
    ROOT, README, AUDIT_DIR, IMPL_DIR, DETAILS,
    SPECS, GROUP_OF, GROUP_SPEC, sp, spec_for, _slug,
    _bullets, _steps, _norm_persona, read_rows, load_details,
)

import role_extras  # noqa: E402
from role_extras import (  # noqa: E402
    EXTRA_SPECS, EXTRA_GROUP_OF, EXTRA_SUPERVISORS, SLUG_OVERRIDES,
)

# ---------------------------------------------------------------------------
# Merge the extra bespoke data into the legacy data structures
# ---------------------------------------------------------------------------
SPECS.update({k: sp(v[0], v[1], v[2], v[3], v[4]) for k, v in EXTRA_SPECS.items()})
GROUP_OF.update(EXTRA_GROUP_OF)

MASTER = ROOT / "Master Persona Schema & Generator Prompt.md"

# ---------------------------------------------------------------------------
# Master role registry (section 64) + supervisor map (section 65)
# ---------------------------------------------------------------------------
def _between(text: str, start: str, end: str) -> str:
    m1 = re.search(start, text, re.S)
    m2 = re.search(end, text, re.S)
    if not m1 or not m2:
        return ""
    return text[m1.end():m2.start()]


def _bullets_of(text: str) -> list[str]:
    return [re.sub(r"^\s*-\s*", "", ln).strip()
            for ln in text.splitlines() if re.match(r"^\s*-\s+", ln)]


def load_master_registry() -> tuple[dict[str, str], dict[str, str]]:
    """Return (supervisor_titles_by_slug, executor_titles_by_slug) from Master 64.

    Returns empty dicts when the Master file is not present (its role registry
    is derived from the README role table instead).
    """
    if not MASTER.exists():
        return {}, {}
    text = MASTER.read_text(encoding="utf-8")
    sup = _bullets_of(_between(text, r"SUPERVISOR_ROLES:\s*\n", r"\n---\n\n64\.2"))
    exe = _bullets_of(_between(text, r"EXECUTOR_ROLES:\s*\n", r"\n---\n\n64\.3"))
    raw = _between(text, r"ADDITIONAL_ROLES:\s*\n", r"\n---\n\n65\.")
    mode = None
    for chunk in re.split(r"^\s*(SUPERVISOR|EXECUTOR):\s*$", raw, flags=re.M):
        c = chunk.strip()
        if c in ("SUPERVISOR", "EXECUTOR"):
            mode = c
            continue
        if mode and c:
            target = sup if mode == "SUPERVISOR" else exe
            target.extend(_bullets_of(chunk))
    sup_slug = {_slug(t): t for t in sup}
    exe_slug = {_slug(t): t for t in exe}
    # Master abbreviates some titles; map to the canonical prompt titles.
    canon = {
        "cto": "Chief Technology Officer (CTO)",
        "ciso": "Chief Information Security Officer (CISO)",
        "privacy-compliance-officer": "Privacy / Compliance Officer",
        "product-owner-release": r"Product Owner (Post-Release)",
    }
    for s, t in list(sup_slug.items()):
        if s in canon:
            sup_slug[s] = canon[s]
    return sup_slug, exe_slug


def load_master_map() -> dict[str, list[str]]:
    """Parse section 65: executor title -> [supervisor titles].

    When the Master file is absent (it was removed from the repo), the map is
    derived from the generated personas.json so regeneration stays idempotent.
    """
    if MASTER.exists():
        text = MASTER.read_text(encoding="utf-8")
        body = _between(text, r"SUPERVISOR_MAP:\s*\n", r"\nNote:")
        result: dict[str, list[str]] = {}
        cur = None
        for ln in body.splitlines():
            ln = ln.strip()
            if not ln:
                continue
            if re.match(r"^[^-\s].*:$", ln):
                cur = ln[:-1].strip()
                result.setdefault(cur, [])
                continue
            m = re.match(r"^-\s+(.+)$", ln)
            if m and cur:
                result[cur].append(m.group(1).strip())
        return result
    pj = ROOT / "personas.json"
    if pj.exists():
        data = json.loads(pj.read_text(encoding="utf-8"))
        return {r["title"]: list(r["supervisors"]) for r in data["roles"] if r["supervisors"]}
    return {}


# Executor roles used by Master 65 as supervisors but registered as EXECUTOR:
# normalize them to the project's registered supervisor equivalents.
SUPERVISOR_ALIAS = {
    "System Architect (Embedded)": "Embedded Systems Lead",
    "System Architect": "Solution Architect",
    "AI Engineer": "AI Engineer Lead",
    "SRE (Site Reliability Engineer)": "DevOps Manager",
    "Database Engineer": "Data Architect",
    "Infrastructure Engineer": "Infrastructure Manager",
    "Release Engineer": "Release Manager",
    "DevOps Engineer": "DevOps Manager",
    "Performance Engineer": "Performance Engineering Lead",
    "Product Designer": "Design Manager",
    "Localization Specialist": "Localization Manager",
    "UX Researcher": "Design Manager",
    "DevRel": "Community Director",
    "Product Analyst": "Product Analyst Lead",
    "Disaster Recovery Specialist": "Business Continuity Manager",
    "Infrastructure Owner": "Platform Owner",
    "Performance Owner": "Performance Engineering Lead",
    "Marketing Manager": "Product Marketing Manager",
    "Developer Relations Manager": "Community Director",
    "DBA": "Database Administrator (DBA)",
    "CISO / Chief Information Security Officer": "Chief Information Security Officer (CISO)",
    "Product Owner (PO)": "Product Owner (PO)",
    "Product Manager (PM)": "Product Manager (PM)",
    "Technical Lead / Tech Lead": "Technical Lead / Tech Lead",
    "Cloud Architect": "Cloud Architect",
    "Security Architect": "Security Architect",
    "Data Architect": "Data Architect",
    "QA Lead": "QA Lead",
    "Engineering Manager": "Engineering Manager",
    "Principal Engineer": "Principal Engineer",
    "Solution Architect": "Solution Architect",
    "Enterprise Architect": "Enterprise Architect",
    "Incident Manager": "Incident Manager",
    "Privacy / Compliance Officer": "Privacy / Compliance Officer",
    "Product Marketing Manager": "Product Marketing Manager",
    "Growth Manager": "Growth Manager",
    "Sales Manager": "Sales Manager",
    "Recruitment Manager": "Recruitment Manager",
    "HR / People Manager": "HR / People Manager",
    "Operations Manager": "Operations Manager",
    "Scrum Master": "Scrum Master",
    "Customer Success Manager": "Customer Success Manager",
    "Finance Manager": "Finance Manager",
    "End-of-Life Manager": "End-of-Life Manager",
    "Business Continuity Manager": "Business Continuity Manager",
    "Product Owner (Post-Release)": "Product Owner (Post-Release)",
}


def resolve_supervisor(name: str) -> str:
    if name in SUPERVISOR_ALIAS:
        return SUPERVISOR_ALIAS[name]
    if name.startswith("System Architect"):
        return SUPERVISOR_ALIAS["System Architect (Embedded)"]
    return name


def build_supervisor_map(sup_titles: set[str]) -> dict[str, list[str]]:
    """Executor title -> [real registered supervisor titles]."""
    master = load_master_map()
    result: dict[str, list[str]] = {}
    for exe_title, sups in master.items():
        resolved = []
        for s in sups:
            rs = resolve_supervisor(s)
            if rs in sup_titles and rs not in resolved:
                resolved.append(rs)
        if resolved:
            result[exe_title] = resolved
    for exe_title, sups in EXTRA_SUPERVISORS.items():
        resolved = [s for s in sups if s in sup_titles]
        result.setdefault(exe_title, []).extend(x for x in resolved if x not in result.get(exe_title, []))
    return result


# ---------------------------------------------------------------------------
# Registry metadata (sections 1-6 of the persona model)
# ---------------------------------------------------------------------------
GROUP_DOMAIN = {
    "strategy": "Business", "product": "Product", "management": "Project",
    "analysis": "Analytics", "architecture": "Architecture", "engineering": "Software",
    "ai": "AI", "data": "Data", "devops": "DevOps", "qa": "Testing",
    "security": "Security", "compliance": "Compliance", "design": "Design",
    "content": "Documentation", "people": "HR", "support": "Support",
    "growth": "Growth", "assurance": "Audit", "ops": "Operations",
}
GROUP_CATEGORY = {
    "strategy": "Strategy", "product": "Management", "management": "Management",
    "analysis": "Analysis", "architecture": "Architecture", "engineering": "Engineering",
    "ai": "Data", "data": "Data", "devops": "Infrastructure", "qa": "Testing",
    "security": "Security", "compliance": "Compliance", "design": "Design",
    "content": "Documentation", "people": "Management", "support": "Support",
    "growth": "Commercial", "assurance": "Audit", "ops": "Operations",
}
SENIORITY_RULES = [
    ("Board of Directors", "Executive"), ("Founder", "Executive"), ("CTO", "Executive"),
    ("Chief Technology Officer", "Executive"), ("CISO", "Executive"),
    ("Chief Information Security Officer", "Executive"), ("CIO", "Executive"),
    ("Chief Information Officer", "Executive"), ("CAO", "Executive"),
    ("Chief Audit Officer", "Executive"), ("CDO", "Executive"),
    ("Chief Design Officer", "Executive"), ("Chief Privacy Officer", "Executive"),
    ("Principal", "Principal"), ("Staff", "Staff"),
    ("Director", "Director"), ("Manager", "Manager"), ("Lead", "Lead"),
    ("Specialist", "Specialist"), ("Architect", "Senior"),
    ("Engineer", "Senior"), ("Analyst", "Senior"), ("Researcher", "Senior"),
    ("Tester", "Mid"), ("Developer", "Mid"), ("Writer", "Mid"),
    ("Translator", "Mid"), ("Recruiter", "Mid"), ("Agent", "Mid"),
    ("Participant", "Junior"), ("Tester", "Mid"), ("User", "Junior"),
]


def seniority_of(title: str) -> str:
    for key, val in SENIORITY_RULES:
        if key in title:
            return val
    return "Specialist"


CAPS_BY_GROUP = {
    "strategy": ["Architect", "Recommend", "Govern"],
    "product": ["Prioritize", "Recommend", "Plan", "Report"],
    "management": ["Monitor", "Control", "Plan", "Report"],
    "analysis": ["Analyze", "Investigate", "Report"],
    "architecture": ["Architect", "Review", "Design"],
    "engineering": ["Implement", "Build", "Debug", "Refactor"],
    "ai": ["Analyze", "Design", "Validate", "Monitor"],
    "data": ["Analyze", "Design", "Validate"],
    "devops": ["Deploy", "Operate", "Monitor", "Optimize"],
    "qa": ["Test", "Validate", "Report"],
    "security": ["Audit", "Investigate", "Validate", "Respond"],
    "compliance": ["Audit", "Report", "Govern"],
    "design": ["Design", "Review", "Validate"],
    "content": ["Document", "Review", "Report"],
    "people": ["Report", "Train", "Support"],
    "support": ["Support", "Respond", "Report"],
    "growth": ["Plan", "Report", "Communicate"],
    "assurance": ["Audit", "Assess", "Investigate"],
    "ops": ["Monitor", "Operate", "Respond", "Recover"],
}
TYPE_CAPS = {
    "SUPERVISOR": ["Assess", "Audit", "Review", "Architect", "Govern", "Approve",
                   "Reject", "Prioritize", "Recommend", "Plan", "Monitor",
                   "Control", "Escalate"],
    "EXECUTOR": ["Implement", "Build", "Configure", "Integrate", "Test",
                 "Validate", "Debug", "Refactor", "Deploy", "Operate",
                 "Optimize", "Migrate", "Document", "Analyze", "Report",
                 "Maintain", "Respond", "Recover"],
}
STEP_CAP = {
    "ANALYZE": ["Analyze", "Investigate"],
    "ASSESS": ["Assess"],
    "INSPECT": ["Review", "Validate"],
    "DESIGN": ["Design", "Architect"],
    "PLAN": ["Plan"],
    "IMPLEMENT": ["Implement", "Build"],
    "INTEGRATE": ["Integrate"],
    "TEST": ["Test", "Validate"],
    "VALIDATE": ["Validate", "Report"],
    "REVIEW": ["Review", "Report"],
    "AUDIT": ["Audit", "Assess"],
    "GOVERN": ["Govern", "Control"],
    "VERIFY": ["Validate", "Report"],
    "MONITOR": ["Monitor", "Report"],
    "OPTIMIZE": ["Optimize"],
    "DOCUMENT": ["Document"],
    "HANDOFF": ["Report", "Communicate"],
}
PROD_AUTH_MAP = [
    ([r"no direct access", "no direct access", "no production access", "read only", r"read only", r"read only"], "NONE"),
    (["read", r"Study", "view", "monitor", r"Observation"], "READ_ONLY"),
    (["limited", r"limited", "direct system access", r"direct system access"], "LIMITED"),
    (["authorized write", "limited write", r"limited write"], "AUTHORIZED_WRITE"),
    (["full", r"full", "admin", r"full"], "FULL"),
]


def production_authority(permissions: str, restricted: str) -> str:
    text = f"{permissions} {restricted}".lower()
    for keys, val in PROD_AUTH_MAP:
        if any(k in text for k in keys):
            return val
    return r"Unknown / Requires Verification: the Production access level is not explicit in the role data"


# ---------------------------------------------------------------------------
# Small text helpers
# ---------------------------------------------------------------------------
def _unordered(items) -> str:
    return "\n".join(f"- {i}" for i in items)


def _uk(field: str) -> str:
    return f"Unknown / Requires Verification: \"{field}\" is not recorded in this role's data; only valid Context may be sent"


# ---------------------------------------------------------------------------
# Universal 29-section builders
# ---------------------------------------------------------------------------
def sec_identity(meta) -> str:
    d, cat, sen = meta["domain"], meta["category"], meta["seniority"]
    return f"""## 1. Identity
- **Role:** {meta['title']}
- **Type:** {meta['type']}
- **Domain:** {d}
- **Category:** {cat}
- **Seniority:** {sen}
- **Purpose:** {meta['purpose']}
- **Role_ID:** {meta['role_id']}"""


def sec_mission(p, spec, meta) -> str:
    return f"""## 2. Mission
- **PrimaryGoal:** {p['mission']}
- **ExpectedOutcome:** {p['outputs']}
- **SuccessDefinition:** {p['quality']}\n- **FailureDefinition:** output without evidence or incomplete; exceeding Scope/Authority; {p['escalation']}"""


def sec_responsibilities(p, spec, meta) -> str:
    pri = _bullets(p['responsibilities'])
    sec = _unordered(spec['audit'] if meta['type'] == 'SUPERVISOR' else spec['impl'])
    if meta['type'] == 'SUPERVISOR':
        sup = _unordered([f"Coordination with consumers: {c}" for c in meta['consumers']] or [
            r"Receiving output from the executors and reviewing it within Scope"] )
        out = [r"Direct implementation (Implementation) outside Authority",
               r"Financial/legal/security decisions outside Scope — ESCALATE"]
    else:
        sup = _unordered([f"Coordination with the supervisor: {s}" for s in meta['supervisors']] or [
            r"Coordination with the defined supervisor"])
        out = [r"File/service change outside Scope",
               r"Architecture, security, contract, or data change without supervisor approval"]
    return f"""## 3. Responsibilities
- **Primary:**
{pri}\n- **Secondary (specific to this role):**\n{sec}
- **Supporting:**
{sup}
- **OutOfScope:**
{_unordered(out)}"""


def sec_type_capability(p, meta, group) -> str:
    base = TYPE_CAPS[meta['type']]
    extra = CAPS_BY_GROUP.get(group, [])
    step_caps = []
    for step in _steps(p['procedure']):
        for kind, caps in STEP_CAP.items():
            if kind == _step_kind(step):
                step_caps.extend(caps)
    caps = []
    for c in base + extra + step_caps:
        if c not in caps:
            caps.append(c)
    other = TYPE_CAPS['EXECUTOR' if meta['type'] == 'SUPERVISOR' else 'SUPERVISOR']
    return f"""## 4. Type & Capability
- **Type:** {meta['type']}
- **Supervisor Capabilities:** {_unordered(caps) if meta['type'] == 'SUPERVISOR' else "NOT_APPLICABLE — this Persona is of type EXECUTOR"}
- **Executor Capabilities:** {_unordered(caps) if meta['type'] == 'EXECUTOR' else "NOT_APPLICABLE — this Persona is of type SUPERVISOR"}\n- **Capabilities NOT owned (only with explicit Authority):** {_unordered(other)}"""


def sec_authority(p, meta) -> str:
    if meta['type'] == 'SUPERVISOR':
        decisions = "APPROVE / REJECT / RECOMMEND / DEFER / ESCALATE"
        actions = r"Review, audit, assessment, approve/reject, prioritisation, recommendation, oversight, control, escalation"
        forbid_d = r"Execution/implementation decision and direct change of code, configuration, or database"
        forbid_a = r"Applying changes to Production without authorisation; architecture/security/contract changes outside Authority"
        approve = r"Scope change, architecture change, Production change, major security/legal/financial decisions"
    else:
        decisions = "PROCEED / PAUSE / RETRY / ROLLBACK / BLOCK / ESCALATE"
        actions = r"Implementation, configuration, integration, testing, deployment, maintenance, documentation"
        forbid_d = r"Supervisory decisions: final approval/rejection of Scope, architecture, security, budget"
        forbid_a = r"File change outside Scope; building an API/dependency/config without evidence"
        approve = r"File change outside Scope, change in Production, contract/architecture/database change"
    auth = production_authority(p['permissions'], p['restricted'])
    return f"""## 5. Authority & Boundaries
- **AllowedDecisions:** {decisions}
- **AllowedActions:** {actions}
- **ApprovalRequiredFor:** {approve}
- **ForbiddenDecisions:** {forbid_d}
- **ForbiddenActions:** {forbid_a}\n- **CrossDomainRules:** if a decision affects another Persona's ownership (architecture, security, data, finance, legal): identify the effect → preserve current behaviour where possible → document → **ESCALATE** to the responsible Persona.\n- **ProductionAuthority:** {auth}"""


def sec_stakeholders(p, meta) -> str:
    if meta['type'] == 'SUPERVISOR':
        decision = meta['title']
        impl = r"NOT_APPLICABLE — this Persona does not itself perform direct Implementation"
        reviewer = r", ".join(meta['supervisors']) or "NOT_APPLICABLE"
        approver = r", ".join(meta['supervisors']) or "NOT_APPLICABLE"
        supporting = r", ".join(meta['supervisors']) or r"Consumers (supervised executors)"
        consumers = r", ".join(meta['consumers']) or "NOT_APPLICABLE"
    else:
        decision = meta['supervisors'][0] if meta['supervisors'] else r"Unknown / Requires Verification: the supervisor must exist in the Registry"
        impl = meta['title']
        reviewer = r", ".join(meta['supervisors']) or "Unknown / Requires Verification"
        approver = r", ".join(meta['supervisors']) or "Unknown / Requires Verification"
        supporting = r", ".join(meta['supervisors']) or "Unknown / Requires Verification"
        consumers = p['handoff']
    return f"""## 6. Stakeholders & Ownership
- **PrimaryOwner:** {meta['title']}
- **DecisionOwner:** {decision}
- **ImplementationOwner:** {impl}
- **Reviewer:** {reviewer}
- **Approver:** {approver}
- **SupportingPersonas:** {supporting}
- **ConsumerPersonas:** {consumers}"""


def sec_inputs(p) -> str:
    return f"""## 7. Inputs
- **Required:** {_bullets(p['required'])}
- **Optional:** {_bullets(p['optional'])}
- **Generated:** {_bullets(p['outputs'])}\n- **Prohibited:** input without a source or a valid document; invalid data/artifact; context outside this role's scope\n- **Validation:** every input is recorded with `Name / Type / Source / Required / Validation / Freshness`; without an explicit source: **Unknown / Requires Verification: ...**"""


def sec_preconditions(p) -> str:
    return f"""## 8. Preconditions
- **Required:** {_bullets(p['preconditions'])}\n- **Optional:** NOT_APPLICABLE — not broken out in the role data (if needed, use valid Context)\n- **Blocking:** if a required input is unavailable → `BLOCKED` (How Verified: the input source/artifact must be recorded)\n- **Authorization:** {p['permissions']}
- **Environment:** {_uk('Environment')}
- **Access:** {_uk('Access')}"""


def sec_context(p, meta) -> str:
    ctx = p['context'] or "NOT_APPLICABLE"
    return f"""## 9. Context
- **Task:** {ctx}
- **Domain:** {meta['domain']}
- **Project:** {_uk('Project')}
- **Architecture:** {_uk('Architecture')}
- **Codebase:** {_uk('Codebase')}
- **Runtime:** {_uk('Runtime')}
- **Infrastructure:** {_uk('Infrastructure')}
- **Security:** {_uk('Security')}
- **Data:** {_uk('Data')}
- **PreviousDecisions:** {_uk('PreviousDecisions')}
- **OpenIssues:** {_uk('OpenIssues')}
- **RelevantHistory:** {_uk('RelevantHistory')}\n- **Rule:** receive only relevant Context; the whole Project Context without need is forbidden."""


def sec_memory(p) -> str:
    return f"""## 10. Memory
- **Working:** {_bullets(p['memory'])}
- **Persistent:** {_uk('Persistent Memory')}
- **Project:** {_uk('Project Memory')}
- **Role:** {_uk('Role Memory')}
- **Historical:** {_uk('Historical Memory')}\n- **Rules:** Memory ≠ Evidence; Memory ≠ Requirement; Memory ≠ Authorization. Memory information must be verified again in important decisions."""


def sec_scope(p, meta) -> str:
    out_scope = (r"Direct implementation outside Authority" if meta['type'] == 'SUPERVISOR'
                 else r"File/service/data change outside the defined Scope")
    return f"""## 11. Scope
- **InScope:** {p['scope']}
- **OutOfScope:** {out_scope}; decisions outside Authority are recorded and ESCALATED (not silenced)\n- **AffectedAreas:** {meta['domain']} / {meta['category']}
- **FileScope:** {_uk('FileScope')}
- **ModuleScope:** {_uk('ModuleScope')}
- **ServiceScope:** {_uk('ServiceScope')}
- **EnvironmentScope:** {_uk('EnvironmentScope')}\n- **ScopeExpansionPolicy:** REQUIRES_APPROVAL — every scope expansion must be documented and approved"""


NFR_BY_GROUP = {
    "strategy": {"NonFunctional": r"Alignment with the vision and goals, feasibility of resources, managed uncertainty risk",
                 "Architecture": r"Alignment of decisions with the high-level architecture", "Governance": r"Documented decision model and ownership",
                 "Compliance": r"Compliance of major decisions with regulations", "Operational": r"Translatability into an executable programme"},
    "product": {"NonFunctional": r"Measurability of value, transparency of priorities, scope-change management",
                "Architecture": r"Roadmap consistency with the product architecture", "Governance": r"Prioritisation model and backlog ownership",
                "Compliance": r"Compliance with legal/privacy considerations", "Operational": r"KPI monitoring and user feedback"},
    "management": {"NonFunctional": r"Status traceability, transparency of time/resources/risk",
                   "Architecture": r"Programme consistency with technical constraints", "Governance": r"Documented role and decision ownership",
                   "Compliance": r"Compliance with the process and regulations", "Operational": r"Status reporting including blockers/risk"},
    "analysis": {"NonFunctional": r"Unambiguous, testable, traceable",
                 "Architecture": r"Requirements consistency with the architecture and data", "Governance": r"Approval path for requirements",
                 "Compliance": r"Coverage of legal/privacy requirements in the requirements", "Operational": r"Mapping requirements to output/tests"},
    "architecture": {"NonFunctional": r"Scalability, maintainability, changeability, backward compatibility",
                     "Architecture": r"Component boundaries, contracts, and Decision Records", "Security": r"Coverage of security controls in the architecture",
                     "Performance": r"Assessment of component capacity/performance", "Scalability": r"Documented scale scenario",
                     "Reliability": r"Fault tolerance and failure paths", "Compatibility": r"Consistency with existing systems",
                     "Governance": r"Architecture approval path", "Operational": r"Deployability and monitoring of the architecture"},
    "engineering": {"NonFunctional": r"Behavioural correctness, DRY, code quality, performance, baseline security",
                    "Architecture": r"Adherence to the contract and architecture boundary", "Security": r"Input/output validation, no secret disclosure",
                    "Performance": r"p95/throughput monitoring", "Compatibility": "Backward Compatibility",
                    "Testing": r"Coverage of edge and failure cases", "Operational": r"Logging/tracing and regression capability"},
    "ai": {"NonFunctional": r"Reproducibility, drift monitoring, cost control",
           "Architecture": r"Agent/model boundary and tool contract", "Security": r"Guardrails, jailbreak, sensitive data",
           "Performance": r"Model quality (eval score), latency", "Reliability": r"Fallback and error behaviour",
           "Compliance": r"Privacy and compliance of model usage", "Operational": r"Continuous monitoring and evaluation"},
    "data": {"NonFunctional": r"Data accuracy, consistency, performance, and security",
             "Architecture": r"Schema/migration consistency with the architecture", "Security": r"Data access, encryption, and traceability",
             "Performance": r"Query/index performance", "Reliability": r"Backup/restore and DR",
             "Compliance": r"Data classification and privacy", "Operational": r"Data quality and monitoring"},
    "devops": {"NonFunctional": r"Repeatability, observability, recoverability",
               "Architecture": r"CI/CD and environment consistency", "Security": r"Secret management and least privilege",
               "Performance": r"Build/deploy time and capacity", "Reliability": r"Rollback/canary and incident readiness",
               "Compatibility": r"Platform/release consistency", "Operational": r"Alerts/runbook and monitoring"},
    "qa": {"NonFunctional": r"Test repeatability, edge coverage, defect follow-up",
           "Architecture": r"Coverage of layers and contracts in tests", "Security": r"Security cases in the test strategy",
           "Performance": r"Load/performance testing", "Reliability": r"Stability and flaky rate",
           "Compatibility": r"Coverage of releases/browsers/platforms", "Operational": r"Defect reporting and follow-up"},
    "security": {"NonFunctional": r"Control coverage, vulnerability management, timely detection",
                 "Architecture": r"Control consistency with the architecture", "Security": r"Threat modelling, validation, secrets",
                 "Performance": r"Effect of controls on performance", "Reliability": r"Incident response and recovery",
                 "Compliance": r"Compliance with regulations and policies", "Operational": r"Monitoring, reporting, and follow-up"},
    "compliance": {"NonFunctional": r"Compliance, complete evidence, traceable decisions",
                   "Architecture": r"Effect of requirements on the architecture", "Security": r"Data protection in the compliance process",
                   "Reliability": r"Control-process stability", "Compliance": r"Coverage of rules/contracts/privacy",
                   "Operational": r"Control gates and reporting"},
    "design": {"NonFunctional": r"Consistency, accessibility, state coverage",
               "Architecture": r"Consistency with the design system", "Security": r"User-data privacy in the design",
               "Performance": r"UI/interaction performance", "Reliability": r"Coverage of error/empty states",
               "Compatibility": r"Responsiveness and accessibility", "Operational": r"Testability and implementability"},
    "content": {"NonFunctional": r"Accuracy, completeness, terminology consistency",
                "Architecture": r"Document consistency with the release/behaviour", "Security": r"No information disclosure in documentation",
                "Compatibility": r"Consistency with platforms/releases", "Operational": r"Document updating and availability"},
    "people": {"NonFunctional": r"Fairness, non-discrimination, personal-data protection",
               "Architecture": r"Consistency of the role/team structure with the organisation", "Security": r"Employee-data privacy",
               "Compliance": r"Compliance of hiring/data with regulations", "Operational": r"Transparent and assessable process"},
    "support": {"NonFunctional": r"Response speed, ownership continuity, satisfaction",
                "Architecture": r"Consistency of the support process with the product", "Security": r"Customer-data protection",
                "Reliability": r"SLA stability", "Compliance": r"Compliance with commitments/laws", "Operational": r"Escalation and knowledge base"},
    "growth": {"NonFunctional": r"Measurable, brand-aligned, with clear ROI",
               "Architecture": r"Message consistency with the product", "Security": r"Audience-data privacy",
               "Compliance": r"Compliance of marketing/sales with regulations", "Operational": r"KPI monitoring and experimentation"},
    "assurance": {"NonFunctional": r"Independence, objectivity, complete coverage, traceable evidence",
                  "Architecture": r"Coverage of the architecture within the audit scope", "Security": r"Accountability and information security of the audit",
                  "Reliability": r"Audit repeatability", "Compliance": r"Compliance with audit standards",
                  "Operational": r"Reporting, follow-up, and closure of findings"},
    "ops": {"NonFunctional": r"Readiness, fast recovery, continuous improvement",
            "Architecture": r"Runbook consistency with the architecture", "Security": r"Security of the operations process",
            "Performance": r"SLA and MTTR", "Reliability": "Availability/Recovery",
            "Compliance": r"Operations compliance with policies", "Operational": r"Alerts, postmortem, and runbook"},
}


def sec_criteria(p, spec, meta, group) -> str:
    nfr = NFR_BY_GROUP.get(group, NFR_BY_GROUP["engineering"])
    if meta['type'] == 'SUPERVISOR':
        lines = [
            "- **Functional:**", _bullets(p['quality']), "",
            "- **NonFunctional:**", f"- {nfr.get('NonFunctional', 'NFR coverage')}", "",
        ]
        for key in ["Architecture", "Security", "Performance", "Scalability",
                    "Reliability", "Compatibility", "Governance", "Compliance", "Operational"]:
            lines.append(f"- **{key}:** {nfr.get(key, _uk(key))}")
        return "## 12. Criteria / Requirements\n" + "\n".join(lines)
    lines = [
        "- **Functional:**", _bullets(p['quality']), "",
        r"- **Technical (specific to this role):**", _unordered(spec['impl']), "",
        "- **API:**", f"- {nfr.get('Architecture', _uk('API'))}",
        "- **Data:**", f"- {nfr.get('Security', _uk('Data'))}",
        "- **Security:**", f"- {nfr.get('Security', 'Validation and no secret disclosure')}",
        "- **Performance:**", f"- {nfr.get('Performance', _uk('Performance'))}",
        "- **Compatibility:**", f"- {nfr.get('Compatibility', _uk('Compatibility'))}",
        "- **Testing:**", f"- {nfr.get('Testing', 'Testing before and after the change, with evidence')}",
        "- **Configuration:**", f"- {_uk('Configuration')}",
        "- **Migration:**", f"- {_uk('Migration')}",
    ]
    return "## 12. Criteria / Requirements\n" + "\n".join(lines)


def _step_kind(name: str) -> str:
    n = name.lower()
    if any(k in n for k in ["audit", r"Audit", "govern", r"Governing", "control", r"Control"]):
        return "AUDIT"
    if any(k in n for k in ["inspect", r"Review", "check", r"Review"]):
        return "INSPECT"
    if any(k in n for k in ["assess", r"Assessment"]):
        return "ASSESS"
    if any(k in n for k in ["analy", "understand", "discover", r"Analysis", r"Understanding", r"Comprehension"]):
        return "ANALYZE"
    if any(k in n for k in ["design", "architect", "model", "define", "research", r"Design", r"Definition"]):
        return "DESIGN"
    if any(k in n for k in ["plan", r"Program", "roadmap", r"Map"]):
        return "PLAN"
    if any(k in n for k in ["implement", "build", "develop", "create", "code", "write", "transform", r"Implementation", r"Build", r"Development"]):
        return "IMPLEMENT"
    if any(k in n for k in ["integrat", "connect", "link", "wire", r"Connection", r"Integration", "integrate"]):
        return "INTEGRATE"
    if any(k in n for k in ["test", "validat", "verify", "check", "optim", r"Testing", r"Validation", r"Optimisation"]):
        return "TEST"
    if any(k in n for k in ["monitor", r"Monitoring", r"Oversight", "measure", r"Measurement"]):
        return "MONITOR"
    if any(k in n for k in ["document", r"Documentation"]):
        return "DOCUMENT"
    if any(k in n for k in ["deploy", r"Deployment", "release", r"Publication"]):
        return "INTEGRATE"
    if any(k in n for k in ["review", "report", "deliver", "retrospect", r"Reporting", r"Review"]):
        return "REVIEW"
    if any(k in n for k in ["handoff", r"Delivery"]):
        return "HANDOFF"
    return "VALIDATE"


_STEP_ACTIONS_MASTER = {
    "ANALYZE": [r"Review the inputs and Scope with evidence.", r"Identify the affected code, document, data, or service.",
                r"Identify the interfaces, dependencies, and hidden risks.", r"Record applicability/non-applicability with a reason."],
    "ASSESS": [r"Extract the assessment criteria from the Scope.", r"Collect and organise the available evidence.",
               r"Measure the status against the criteria.", r"Record the result with a confidence level."],
    "INSPECT": [r"Determine the goal and scope of the review.", r"Enumerate the sources/files/sections.",
                r"Examine each item with evidence.", r"Record the finding or the absence of evidence."],
    "DESIGN": [r"Compare the valid options against stated criteria and document them.", r"Constrain the Design/Plan to Scope and Authority.",
               r"Specify the contracts/interfaces/states.", r"Assess the change's effect on existing behaviour; outside Scope → ESCALATE."],
    "PLAN": [r"Determine the correct items and the order of dependencies.", r"Define executable and verifiable steps.",
             r"Identify Hidden Work (errors, validation, tests, migration, documentation, security).", r"Write the acceptance criterion for each phase/step."],
    "IMPLEMENT": [r"Implement only this Persona's Scope.", r"Validate the inputs and produce the output per contract.",
                  r"Cover edge/error/states.", r"Preserve existing behaviour unless the change is deliberate and documented."],
    "INTEGRATE": [r"Verify the contract/interface between components.", r"Preserve backward and behavioural compatibility.",
                  r"Isolate and document integration errors; at another's responsibility boundary → ESCALATE."],
    "TEST": [r"Write and run tests/validation appropriate to the scope.", r"Cover the applicable states (success/error/empty/edge/authz/perf).",
             r"Record the result with evidence; insufficient evidence → BLOCKED/NEEDS_CLARIFICATION."],
    "VALIDATE": [r"Compare the output against the acceptance criterion.", r"Check the evidence and traceability.",
                 r"Report the final result with a status and state; do not claim success without evidence."],
    "REVIEW": [r"Compare the output against the Quality Gate and DoD.", r"Check the evidence and traceability.",
               r"Consolidate and deduplicate the findings.", r"Report the final result with a status and state."],
    "AUDIT": [r"Define the Scope and Coverage Manifest.", r"Enumerate and segment the sources/files/sections.",
              r"Examine each segment with evidence.", r"Record the findings against the Root Finding and assess the Risk."],
    "GOVERN": [r"Assess the decision within Scope and Authority.", r"Assess and document against the owner/supervisor.",
               r"Record the result against the criterion and refrain from decisions outside Authority."],
    "VERIFY": [r"Accept a claim only with evidence.", r"Record the evidence with its Location.",
               r"Record the VERIFIED/POTENTIAL/UNVERIFIED status.", r"Report a claim made without evidence as an unsupported claim."],
    "MONITOR": [r"Specify the indicators and the data source.", r"Record the values with evidence.",
                r"Identify the deviation and ESCALATE it to the responsible Persona."],
    "OPTIMIZE": [r"Specify the bottleneck/opportunity with a criterion.", r"Apply the minimal change with a measurable effect.",
                 r"Measure and document regression before and after."],
    "DOCUMENT": [r"Determine the document's goal/audience/structure.", r"Write precise, evidence-based content.",
                 r"Align with the behaviour/release and review."],
    "HANDOFF": [r"Specify the required artifacts and the Recipient.", r"Attach the Acceptance Criteria and the ExecutionPlan.",
                r"Hand over any remaining responsibility/decision explicitly."],
}


def _structured_steps_master(p) -> str:
    steps = _steps(p['procedure'])
    chunks = []
    for i, name in enumerate(steps, 1):
        kind = _step_kind(name)
        actions = _STEP_ACTIONS_MASTER.get(kind, _STEP_ACTIONS_MASTER["VALIDATE"])
        chunks.append(f"""### STEP {i} — {name}  [{kind}]
- **ID:** STEP-{i}
- **Name:** {name}
- **Type:** {kind}\n- **Objective:** execute the step \"{name}\" while preserving scope and without changes outside Authority.\n- **Inputs:** {p['required']}  |  Optional: {p['optional']}
- **Preconditions:** {p['preconditions']}
- **Actions:"""
                     + "\n".join(f"{j}. {a}" for j, a in enumerate(actions, 1))
                     + f"""
- **Validation:** {p['quality']}
- **Outputs:** {p['outputs']}
- **Evidence:** {p['evidence']}\n- **DecisionPoints:** at this step you may use the statuses (PASS / FAIL / BLOCKED / NEEDS_CLARIFICATION / ESCALATE / NOT_APPLICABLE) and must document the result.\n- **ExitCriteria:** the step's output matches the acceptance criterion and the evidence is recorded.\n- **FailureConditions:** incomplete or contradictory input, out of scope, or insufficient evidence.\n- **EscalationConditions:** {p['escalation']}""")
    return "\n\n".join(chunks)


def sec_procedure(p) -> str:
    return "## 13. Procedure\n" + _structured_steps_master(p)


def sec_decision_rules(p, meta) -> str:
    common = "PASS / FAIL / BLOCKED / NEEDS_CLARIFICATION / ESCALATE / NOT_APPLICABLE"
    if meta['type'] == 'SUPERVISOR':
        values = "APPROVE / REJECT / RECOMMEND / DEFER / ESCALATE"
        note = r"The supervisor decides only on the basis of Scope and evidence; it does not approve without Evidence."
    else:
        values = "PROCEED / PAUSE / RETRY / ROLLBACK / BLOCK / ESCALATE"
        note = r"The executor does not declare Completion without evidence (test/build/manifest)."
    return f"""## 14. Decision Rules\n- **Status Values (all Personas):** {common}
- **Decision Values ({meta['type']}):** {values}
- **Role-specific rules:**
{_bullets(p['decision'])}
- **Rules:** {note}\n- Every `NOT_APPLICABLE` must have a reason; every Escalation must have a specific Target."""


def sec_tools(p, meta, group) -> str:
    cats = {
        "strategy": "Documentation, Analytics, Project Management",
        "product": "Project Management, Analytics, Documentation",
        "management": "Project Management, Documentation, Analytics",
        "analysis": "Analytics, BI, Documentation",
        "architecture": "Filesystem, IDE, Git, Documentation, Diagramming",
        "engineering": "Filesystem, IDE, Git, Terminal, Package Manager, Testing, Debugger, Static Analysis",
        "ai": "Filesystem, IDE, Git, Terminal, Testing, Logging, Tracing",
        "data": "Database, Filesystem, Git, Terminal, Testing, Profiler",
        "devops": "Git, Terminal, CI/CD, Cloud CLI, IaC, Monitoring, Logging",
        "qa": "Testing, Browser DevTools, Load Testing, Profiler, Documentation",
        "security": "Security Scanner, SAST, DAST, SCA, Logging, Monitoring, Debugger",
        "compliance": "Documentation, Audit, Analytics",
        "design": "Design Tools, Browser DevTools, Documentation, Testing",
        "content": "Documentation, IDE, Browser DevTools",
        "people": "Documentation, Project Management, Analytics",
        "support": "Support/CRM, Documentation, Monitoring",
        "growth": "Analytics, BI, CRM, Documentation",
        "assurance": "Audit tools, Documentation, Analytics",
        "ops": "Monitoring, Logging, Tracing, CI/CD, Cloud CLI",
    }
    return f"""## 15. Tools & Environment
- **Allowed:** {_bullets(p['allowed'])}
- **Restricted:** {_bullets(p['restricted'])}\n- **Forbidden:** tools/access mentioned under \"Restricted\"; using any tool without a permit is not allowed.\n- **ApprovalRequired:** Production/access change, tools outside the Allowed list, database/infrastructure change.\n- **ReadOnly:** {production_authority(p['permissions'], p['restricted'])}\n- **Categories (per the Master):** {cats.get(group, 'Documentation, Filesystem')}"""


def sec_evidence(p) -> str:
    return f"""## 16. Evidence & Verification\n- **Required evidence:** {_bullets(p['evidence'])}\n- **Evidence Status:** VERIFIED / POTENTIAL / UNVERIFIED / MISSING\n- **Evidence Types:** FILE / LINE / CODE / DIFF / TEST_RESULT / BUILD_OUTPUT / LOG / TRACE / SCREENSHOT / API_RESPONSE / DATABASE_RESULT / BENCHMARK / METRIC / CONFIGURATION / DOCUMENT / ARCHITECTURE_DIAGRAM / DATASET / AUDIT_RECORD / USER_FEEDBACK\n- **Evidence Location:** FILE / LINE , DOCUMENT / SECTION , API / ENDPOINT , DATABASE / TABLE / COLUMN , ARCHITECTURE / NODE , CONFIGURATION / KEY , LOG / TIMESTAMP , DATASET / FIELD , TEST / CASE\n- **Rule:** every material claim links to traceable evidence; without evidence: **MISSING** → the claim is not recorded."""


def sec_coverage(meta) -> str:
    if meta['type'] == 'SUPERVISOR':
        body = """- **Total Scope / Reviewed Scope / Unreviewed Scope / Blocked Scope / Coverage %:** compute and record in every audit.
- **Formula:** Coverage % = Reviewed Scope Items / Total Scope Items × 100
- **Completion Rule:** 100% Coverage + All Mandatory Checks Passed + No Blocking Issue + All Required Evidence = Review Complete
- **Manifest:** every file/section of Scope must go `Discovered → Classified → Reviewed → Status-marked` (REVIEWED / IN_PROGRESS / NOT_REVIEWED + a valid reason)."""
    else:
        body = """- **Total Scope:** all files/sections affected by the task.
- **Reviewed/Unreviewed/Blocked/Change Coverage %:** the ratio of changed/tested files to the whole change scope.
- **Formula:** Change Coverage % = Changed & Tested Items / Total Changed Items × 100
- **Completion Rule:** all Increments complete + Change Manifest complete + Tests executed + No Blocking Issue = detailed completion.
- **Manifest:** every changed file: Action/Scope/Status/Reason/RequirementIDs/TestStatus/Evidence."""
    return "## 17. Coverage / Completeness\n" + body


def sec_findings(meta) -> str:
    if meta['type'] == 'SUPERVISOR':
        return """## 18. Findings / Changes
**Every finding (format):** ID / ROOT_FINDING_ID / SEGMENT / SOURCE / LOCATION / SEVERITY / CONFIDENCE / EVIDENCE_STATUS / CATEGORY / TITLE / EVIDENCE / PROBLEM / TRIGGER / EXPECTED / ACTUAL / IMPACT / AFFECTED / RISK / RECOMMENDED_FIX / OWNER / REGRESSION_RISK / MISSING_EVIDENCE / WHAT_WOULD_CONFIRM
- **Severity:** CRITICAL / HIGH / MEDIUM / LOW / INFO — **Confidence:** CONFIRMED / HIGH / MEDIUM / LOW
- **Lifecycle:** DETECTED → VALIDATING → CONFIRMED → REPORTED → ACCEPTED → PLANNED → FIXED → REVALIDATED → CLOSED (side: REJECTED / FALSE_POSITIVE / DEFERRED)
- **Deduplication:** findings that share a root cause are recorded once with ROOT_FINDING_ID + AFFECTED; hiding real impact is forbidden."""
    return """## 18. Findings / Changes
**ChangeManifest:** Path → Action / Scope / Status / Reason / RequirementIDs / TestStatus / Evidence
- **Allowed Actions:** CREATED / MODIFIED / DELETED / RENAMED / UNCHANGED
- **Status:** COMPLETED / IN_PROGRESS / INCOMPLETE / BLOCKED
- **Increment:** ID / Objective / Files / Requirements / Dependencies / ExpectedResult / Tests / Evidence / Status
- **Rules:** no silent change is permitted; artificial fragmentation, over-merging, and hidden scope expansion are forbidden."""


def sec_risk(p, spec, meta) -> str:
    focus = spec['audit'] if meta['type'] == 'SUPERVISOR' else spec['impl']
    return f"""## 19. Risk\n- **Model:** Risk → ID / SourceFindings / Likelihood / Impact / Score / AffectedAreas / Mitigation / Owner / ResidualRisk\n- **Likelihood:** RARE / UNLIKELY / POSSIBLE / LIKELY / ALMOST_CERTAIN\n- **Impact:** NEGLIGIBLE / LOW / MEDIUM / HIGH / CRITICAL\n- **Rule:** Finding ≠ Risk. Do not turn a finding into a risk; extract the risk from the findings by assessing likelihood/impact.\n- **Role Risk Focus (specific to this role):**\n\n{_unordered(focus)}
- **Escalation Signals:** {p['escalation']}"""


def sec_recommendations(p, spec, meta) -> str:
    if meta['type'] == 'SUPERVISOR':
        return f"""## 20. Recommendations / Implementation\n- **Recommendation:** ID / RelatedFindings / Objective / ProposedChange / Priority / Dependencies / Owner / ExpectedOutcome / ValidationMethod\n- **Priority:** P0 / P1 / P2 / P3 / P4\n- **Role-specific focus for recommendations:**\n\n{_unordered(spec['audit'])}\n- **Implementation:** only within Scope and in the form of an Execution Plan; no direct implementation outside Authority."""
    return f"""## 20. Recommendations / Implementation\n- **Implementation Outputs:** Source Code / Configuration / Schema / Migration / Tests / Build Artifacts / Documentation / Infrastructure Changes / Deployment Artifacts / Reports\n- **Within your own scope only:** every output must be traceable to a Requirement and Evidence.\n- **Role-specific (specific to this role):**\n\n{_unordered(spec['impl'])}"""


GATES_SUPERVISOR = ["Functional Correctness", "Behavioral Correctness", "Architecture Consistency",
                    "Security", "Performance", "Scalability", "Reliability", "Compatibility",
                    "Governance", "Compliance", "Evidence", "Traceability", "Regression Safety"]
GATES_EXECUTOR = ["Functional Correctness", "Implementation Completeness", "API Compatibility",
                  "Data Integrity", "Validation", "Error Handling", "Security Baseline",
                  "Performance", "Regression Safety", "Test Pass", "Build Pass",
                  "Documentation", "Backward Compatibility"]


def sec_quality_gates(p, spec, meta) -> str:
    gates = GATES_SUPERVISOR if meta['type'] == 'SUPERVISOR' else GATES_EXECUTOR
    return f"""## 21. Quality Gates
{_unordered(gates)}\n### Role-Specific Acceptance Criteria\n{_unordered(spec['accept'])}"""


def sec_traceability() -> str:
    return """## 22. Traceability
- **Universal chain:** Requirement → Criterion → Design → Implementation → Test → Evidence → Acceptance
- **IDs:** REQ-### / CRIT-### / DESIGN-### / IMP-### / TEST-### / EVIDENCE-### / RISK-### / FIND-### / REC-### / ACCEPT-### / CHANGE-###
- **Rule:** every material output must link to this chain; where there is no official ID, use a traceable descriptive ID."""


def sec_state_machine(p, meta) -> str:
    if meta['type'] == 'SUPERVISOR':
        sm = ("RECEIVED → SCOPING → CONTEXT_ASSEMBLY → ASSESSING → INSPECTING → ANALYZING → "
              "VALIDATING → FINDINGS_REVIEW → RECOMMENDATION_READY → HANDOFF_PENDING → COMPLETED")
        side = "BLOCKED / ESCALATED / NEEDS_CLARIFICATION / FAILED"
        desc = r"The supervisor never enters direct implementation states; the final output comes only with Evidence and complete Coverage."
    else:
        sm = ("RECEIVED → UNDERSTANDING → INSPECTING → PLANNING → IMPLEMENTING → INTEGRATING → "
              "TESTING → VERIFYING → REVIEW_PENDING → CHANGES_REQUIRED → COMPLETED")
        side = "BLOCKED / ESCALATED / NEEDS_CLARIFICATION / FAILED / ROLLBACK_REQUIRED"
        desc = r"Returning from REVIEW_PENDING to CHANGES_REQUIRED and from TESTING to ROLLBACK_REQUIRED is permitted."
    return f"""## 23. State Machine
- **States ({meta['type']}):** `{sm}`
- **Side states:** {side}
- **Rules:** {desc}\n- **Project lifecycle (from the role data):** {p['lifecycle']}"""


def sec_handoff(p, meta) -> str:
    recv = r", ".join(meta['consumers']) if meta['consumers'] else p['handoff']
    return f"""## 24. Handoff
- **PrimaryRecipient:** {recv}
- **SupportingRecipients:** {', '.join(meta['supervisors']) if meta['supervisors'] else '—'}
- **DecisionOwner:** {meta['supervisors'][0] if meta['supervisors'] and meta['type'] == 'EXECUTOR' else meta['title']}
- **ImplementationOwner:** {meta['title'] if meta['type'] == 'EXECUTOR' else '— (the supervisor does not implement itself)'}
- **RequiredArtifacts:** {p['outputs']}\n- **RequiredActions:** review/approve against Acceptance, continue executing the plan, record the status in `state`\n- **AcceptanceCriteria:** {p['quality']}
- **ExecutionPlan:** audits/{SLUG_OVERRIDES.get(meta['title'], _slug(meta['title']))}-execution-plan.md"""


def sec_escalation(p, meta) -> str:
    return f"""## 25. Escalation
- **Trigger:** {p['escalation']}\n- **Evidence:** evidence, or \"Unknown / Requires Verification\", related to the Trigger\n- **Impact:** the risk/limitation arising from the situation (must be recorded explicitly)\n- **BlockedWork:** the step/file/decision that is stopped\n- **DecisionRequired:** a decision that lies outside this Persona's Scope/Authority\n- **TargetPersona:** {', '.join(meta['supervisors']) if meta['supervisors'] else 'Owning Persona (per the Registry)'}\n- **Urgency:** P0 (Immediate) / P1 / P2\n- **Triggers (official):** SCOPE_CONFLICT / ARCHITECTURE_CONFLICT / SECURITY_RISK / DATA_RISK / LEGAL_RISK / COMPLIANCE_RISK / PRODUCTION_RISK / MISSING_REQUIRED_INPUT / AMBIGUOUS_REQUIREMENT / UNKNOWN_DEPENDENCY / OWNERSHIP_CONFLICT / BLOCKING_FAILURE"""


def sec_execution_plan(meta, title) -> str:
    slug = SLUG_OVERRIDES.get(title, _slug(title))
    path = f"audits/{slug}-execution-plan.md"
    if meta['type'] == 'SUPERVISOR':
        who = ("The Supervisor MUST, where remediation/implementation work is needed, produce an "
               f"Execution Plan and save it under `{path}`. Format: Dependency-aware, "
               "Scope-complete, Phase-coherent, Executable, Verifiable, Stable. File structure: "
               "`# Fixed Project Execution Rules` + `# Execution Plan` with "
               "`## [🔴] Phase ...`, `### [🔴] Step ...` and "
               "`**Acceptance criteria:**`.")
    else:
        who = ("""The Executor MUST read the plan, execute it, keep the completed steps, add discovered work with a reason, and update each step/phase status only with `[🔴]` / `[🟡]` / `[🟢]`. Deleting completed steps, hiding failures, and silent rewriting are forbidden.
""")
    return f"""## 26. Execution Plan
- **Path:** {path}
- **Rule:** {who}"""


def sec_execution_result() -> str:
    return """## 27. Execution Result
```
Status: <PASS | FAIL | BLOCKED | ESCALATE | NEEDS_CLARIFICATION | NOT_APPLICABLE>
Verdict: <...>
State: <one of this Persona's State Machine states>
Coverage: <...>
Coverage Manifest: <...>
Decomposition: <...>
Findings: <...>
Changes: <...>
Tests: <...>
Evidence: <...>
ExecutionPlan: <audits/<slug>-execution-plan.md>
Affected Locations: <...>
Critical/High Findings: <...>
Required Decisions: <...>
Assumptions: <...>
Unknowns: <...>
Risks: <...>
Traceability: REQ-### → ... → ACCEPT-###
Handoff: <...>
Escalation: <...>
Next Action: <...>
```"""


def sec_kpi(p, spec, meta) -> str:
    kpi = p['kpi'] if p['kpi'] and p['kpi'] not in ("—", "-") else spec['accept']
    return f"""## 28. KPI / Metrics
{_bullets(kpi)}\n- KPIs are for Evaluation only; artificial behaviour to reach a number is forbidden.\n- Without evidence → record `Unknown`."""


def sec_mandatory(p, meta) -> str:
    universal = [
        "No Guessing.", "No Fabrication.", "No Silent Scope Expansion.",
        "No Silent Requirement Changes.", "No Silent Architecture Changes.",
        "No Fake Evidence.", "No Fake Completion.", "No Fake Test Results.",
        "No Unsupported Claims.", "Preserve existing behavior unless intentionally changing it.",
        "Every blocking issue must be reported.", "Every unknown must be explicit.",
        "Every assumption must be explicit.", "Every important output must be traceable.",
        "Every NOT_APPLICABLE decision must include a reason.", "Every escalation must identify its target.",
        "Never claim full coverage without a complete manifest.", "Never hide unfinished work.",
        "Never bypass authority boundaries.", "Never claim verification without evidence.",
    ]
    if meta['type'] == 'SUPERVISOR':
        extra = [
            "Review Scope must be explicitly enumerated.", "Create a Coverage Manifest.",
            "Divide large Scope into coherent Segments.", "Review Segments systematically.",
            "Do not skip files because they appear unimportant.", "Analyze relevant code file-by-file.",
            "Analyze relevant areas line-by-line where applicable.", "Analyze complete workflows.",
            "Trace happy path and failure paths.", "Deduplicate root findings without deleting real impacts.",
            "Separate Finding, Risk, Recommendation and Decision.", "Do not directly implement outside authorized Scope.",
            "Produce an Execution Plan when remediation is required.", "Save the plan under audits/.",
            "Include the plan path in Execution Result and Handoff.",
        ]
    else:
        extra = [
            "Read the actual repository before implementing.", "Before modifying a file, read the full target file.",
            "Verify existing functions before calling them.", "Verify actual dependency versions from project files.",
            "Verify existing configuration from the repository.", "Never invent missing APIs, functions or interfaces.",
            "Never modify files outside Scope.", "Keep changes minimal and intentional.",
            "Follow the workflow end-to-end.", "Check regression before and after changes.",
            "Test every meaningful change.", "Update Change Manifest continuously.",
            "Update Execution Plan continuously.", "Preserve completed plan steps.",
            "Do not leave work half-complete.", "If execution is blocked, stop and report the blocker.",
            "If another Persona owns the decision, ESCALATE.", "Completion requires Manifest + Tests + Evidence + DoD.",
        ]
    lines = [f"{i}. {r}" for i, r in enumerate(universal, 1)]
    lines += [f"{len(universal)+i}. {r}" for i, r in enumerate(extra, 1)]
    return "## 29. Mandatory Rules\n" + "\n".join(f"- {x}" for x in lines)


# ---------------------------------------------------------------------------
# Section 62 / 63 — type-specific headings
# ---------------------------------------------------------------------------
def supervisor_specific(p, spec, meta, title) -> str:
    slug = SLUG_OVERRIDES.get(title, _slug(title))
    return f"""## Audit Scope
- **Scope:** {p['scope']}\n- **Audit scope:** only this Persona's Scope/Authority; anything outside Scope is recorded with an EXCLUDE reason.\n- **Rule:** Scope is explicitly enumerated before starting.\n\n## Audit Criteria\n- **Specific to this role:** {_unordered(spec['audit'])}\n- **Criteria:** {_bullets(p['quality'])}\n- Every criterion must be measurable and evidence-based.\n\n## Audit Procedure\n`RECEIVED` → `SCOPING` → `CONTEXT_ASSEMBLY` → `ASSESSING` → `INSPECTING` → `ANALYZING` → `VALIDATING` → `FINDINGS_REVIEW` → `RECOMMENDATION_READY` → `HANDOFF_PENDING` → `COMPLETED`\n- At each step: Input → Action → Validation → Output → Evidence.\n- Deduplicate findings that share a root cause; each segment is examined with evidence.\n\n## Coverage Manifest\n```\nCoverageManifest:\n  - Segment:\n      Files: [...]\n      Components: [...]\n      Status: REVIEWED | IN_PROGRESS | NOT_REVIEWED\n      Reason: OUT_OF_SCOPE | MISSING_ACCESS | MISSING_ARTIFACT | DELETED | UNAVAILABLE | BLOCKED\n      Findings: [...]\n```\n\n## Decomposition Table\n| Segment | Files/Components | Review Status | Findings | Notes |\n|---|---|---|---|---|\n| ... | ... | REVIEWED / IN_PROGRESS / NOT_REVIEWED | FIND-### | ... |\n\n## Findings\n- Each finding follows the format of section 18; each finding carries `FILE / LINE`, Severity, Confidence, and EvidenceStatus.\n- A `POTENTIAL` finding must carry `MISSING EVIDENCE` and `WHAT WOULD CONFIRM IT`.\n- No duplicate finding is created; `ROOT_FINDING_ID` is preserved.\n\n## Risk Assessment\n- Use the risk model of section 19; record likelihood, impact, residual risk, owner, and mitigation.\n- Extract risks from the findings, not the other way round.\n\n## Recommendations\n- Per section 20 with Priority (P0–P4) and an owner; every recommendation links to a finding or risk.\n- Areas specific to this role: {_unordered(spec['audit'])}\n\n## Execution Plan\n- If remediation is needed: produce the plan in the Master format and save it under `audits/{slug}-execution-plan.md`.\n- The plan path is stated in the Execution Result and the Handoff.\n\n## Final Verdict\n- The verdict rests only on complete Coverage, recorded evidence, and the criteria: `CONSISTENT & READY` / `INCONSISTENT` / `NEEDS REDESIGN` / `BLOCKED` / `NOT_APPLICABLE`.\n- Claim \"fully reviewed\" only with a complete Coverage Manifest + Decomposition."""


def executor_specific(p, spec, meta, title) -> str:
    slug = SLUG_OVERRIDES.get(title, _slug(title))
    return f"""## Implementation Scope
- **Scope:** {p['scope']}\n- **Boundaries:** only files/services within Scope; any change outside Scope → ESCALATE.\n- **ScopeExpansionPolicy:** REQUIRES_APPROVAL + record the reason.\n\n## Implementation Requirements\n- **Functional:** {_bullets(p['quality'])}\n- **Technical (specific to this role):** {_unordered(spec['impl'])}\n- Every requirement links to an acceptance criterion and a test.\n\n## Implementation Procedure\n`RECEIVED` → `UNDERSTANDING` → `INSPECTING` → `PLANNING` → `IMPLEMENTING` → `INTEGRATING` → `TESTING` → `VERIFYING` → `REVIEW_PENDING` → `CHANGES_REQUIRED` → `COMPLETED`\n- At each step: Input → Action → Validation → Output → Evidence.\n\n## Change Manifest\n```\nChangeManifest:\n  - Path: <...>\n      Action: CREATED | MODIFIED | DELETED | RENAMED | UNCHANGED\n      Scope: <...>\n      Status: COMPLETED | IN_PROGRESS | INCOMPLETE | BLOCKED\n      Reason: <...>\n      RequirementIDs: [REQ-###]\n      TestStatus: PASS | FAIL | NOT_RUN\n      Evidence: [EVIDENCE-###]\n```\n\n## Modified Files\n- The full list of changed paths with reason and effect — no silent change.\n\n## Created Files\n- The full list of new files with their purpose and evidence.\n\n## Deleted Files\n- The full list of deleted files + reason + replacement/migration.\n\n## Tests\n- Before the change: a baseline test. After the change: the related test + regression.\n- Every test is recorded with `TEST-###`, a result, and evidence; without execution, no result is claimed.\n\n## Verification\n- Syntax → Behavior → Regression → Evidence → Manifest → DoD.\n- Claim success only with evidence (build/test/manifest).\n\n## Evidence\n- {_bullets(p['evidence'])}\n- Every piece of evidence is recorded with `EVIDENCE-###` and a Location (FILE/LINE, API/ENDPOINT, ...).\n\n## Execution Plan Status\n- **Plan Path:** `audits/{slug}-execution-plan.md` (if it exists)\n- The status of each step/phase: `[🔴]` Not Implemented / `[🟡]` Partially Implemented / `[🟢]` Fully Implemented.\n- A phase is only 🟢 when ALL Steps = 🟢 and ALL Acceptance = PASS 🟢.\n\n## Final Completion Status\n- **DoD:** All Increments Complete + Manifest Complete + Modified Files Recorded + Tests Executed + Regression Checked + Evidence Recorded + No Blocking Issue + Handoff Complete + Execution Result Complete.\n- Without DoD being met, Completion must not be declared."""


# ---------------------------------------------------------------------------
# Document assembly
# ---------------------------------------------------------------------------
def build_persona(title: str, role_type: str, p: dict, spec: dict, meta: dict) -> str:
    group = spec["domain"]
    head = f"# Persona — {title}\n\n> **Type:** {meta['type']}  |  **Role_ID:** {meta['role_id']}\n\n---\n"
    parts = [
        sec_identity(meta),
        sec_mission(p, spec, meta),
        sec_responsibilities(p, spec, meta),
        sec_type_capability(p, meta, group),
        sec_authority(p, meta),
        sec_stakeholders(p, meta),
        sec_inputs(p),
        sec_preconditions(p),
        sec_context(p, meta),
        sec_memory(p),
        sec_scope(p, meta),
        sec_criteria(p, spec, meta, group),
        sec_procedure(p),
        sec_decision_rules(p, meta),
        sec_tools(p, meta, group),
        sec_evidence(p),
        sec_coverage(meta),
        sec_findings(meta),
        sec_risk(p, spec, meta),
        sec_recommendations(p, spec, meta),
        sec_quality_gates(p, spec, meta),
        sec_traceability(),
        sec_state_machine(p, meta),
        sec_handoff(p, meta),
        sec_escalation(p, meta),
        sec_execution_plan(meta, title),
        sec_execution_result(),
        sec_kpi(p, spec, meta),
        sec_mandatory(p, meta),
    ]
    if meta['type'] == 'SUPERVISOR':
        parts.append(supervisor_specific(p, spec, meta, title))
    else:
        parts.append(executor_specific(p, spec, meta, title))
    return head + "\n\n---\n\n".join(parts) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def build_registry(sup_titles: set[str]) -> dict[str, dict]:
    """slug -> meta for every README role."""
    rows = read_rows()
    data_rows = [r for r in rows[1:]]
    results: dict[str, dict] = {}
    sup_i = exe_i = 0
    sup_titles_registered = {_slug(t) for t in sup_titles}
    for title, _duties, role_type in [(r[0], r[1], r[2]) for r in data_rows]:
        slug = SLUG_OVERRIDES.get(title, _slug(title))
        ptype = "SUPERVISOR" if role_type == r"SUPERVISOR" else "EXECUTOR"
        group = spec_for(slug)["domain"]
        spec = spec_for(slug)
        details = load_details()
        persona = details.get(title)
        purpose = (persona["mission"] if persona and persona["mission"] not in ("—", "-")
                   else spec["mission"])
        if ptype == "SUPERVISOR":
            sup_i += 1
            role_id = f"SUP-{sup_i:03d}"
        else:
            exe_i += 1
            role_id = f"EXE-{exe_i:03d}"
        results[slug] = {
            "title": title,
            "type": ptype,
            "domain": GROUP_DOMAIN.get(group, "Software"),
            "category": GROUP_CATEGORY.get(group, "Engineering"),
            "seniority": seniority_of(title),
            "purpose": purpose,
            "role_id": role_id,
            "group": group,
            "supervisors": [],
            "consumers": [],
        }
    return results


def main() -> None:
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    IMPL_DIR.mkdir(parents=True, exist_ok=True)
    (ROOT / "audits").mkdir(parents=True, exist_ok=True)

    master_sup, _master_exe = load_master_registry()
    # Registered supervisor titles (canonical) = rows of README with role supervisor
    rows = read_rows()
    data_rows = [r for r in rows[1:]]
    sup_titles = {r[0] for r in data_rows if r[2] == r"SUPERVISOR"}
    sup_map = build_supervisor_map(sup_titles)

    meta_all = build_registry(sup_titles)
    details = load_details()

    # consumers: preferred-to-be derived from supervisor map
    by_supervisor: dict[str, list[str]] = {}
    for exe_title, sups in sup_map.items():
        for s in sups:
            by_supervisor.setdefault(s, []).append(exe_title)

    written = []
    warn_supervisor_missing = []
    for r in data_rows:
        title, _duty, role_type = r[0], r[1], r[2]
        slug = SLUG_OVERRIDES.get(title, _slug(title))
        meta = meta_all[slug]
        if role_type == r"SUPERVISOR":
            meta["supervisors"] = []
            meta["consumers"] = sorted(by_supervisor.get(title, []))
        else:
            sups = sup_map.get(title)
            if not sups:
                warn_supervisor_missing.append(title)
                sups = [r"Unknown / Requires Verification: the supervisor must be defined in the Registry"]
            meta["supervisors"] = sups
            meta["consumers"] = []

        persona = details.get(title)
        if persona is None:
            raise SystemExit(f"MISSING details row: {title}")
        persona = _norm_persona(persona)
        spec = spec_for(slug)

        content = build_persona(title, role_type, persona, spec, meta)
        out_dir = AUDIT_DIR if role_type == r"SUPERVISOR" else IMPL_DIR
        (out_dir / f"{slug}.md").write_text(content, encoding="utf-8")
        written.append((slug, role_type))

    # ---- legacy README link labels are already in README ----
    print(f"Personas written: {len(written)}")
    sup_n = sum(1 for _, t in written if t == r"SUPERVISOR")
    exe_n = sum(1 for _, t in written if t == r"EXECUTOR")
    print(f"Supervisors: {sup_n}   Executors: {exe_n}")
    if warn_supervisor_missing:
        print("WARNING executors without supervisor:", warn_supervisor_missing)
    else:
        print("All executors have a registered supervisor.")


if __name__ == "__main__":
    main()
