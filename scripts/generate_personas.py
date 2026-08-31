#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Master-schema-compliant persona generator.

Generates every persona under prompts/ with the exact contract of
"Master Persona Schema & Generator Prompt.md":

  * 01. Identity  ..  29. Mandatory Rules          (section 61)
  * 10 extra headings for SUPERVISOR personas      (section 62)
  * 12 extra headings for EXECUTOR personas        (section 63)
  * Role registry + executor->supervisor map       (sections 62..65)

Per-role content comes from details.md (bespoke per role), merged with the
bespoke per-role specs (SPECS + role_extras.EXTRA_SPECS).  Roles never fall
back to silently generic content: missing data is rendered as
"Unknown / Requires Verification: ..." (Master rule 3 of section 67).

Usage:
    python3 scripts/generate_personas.py
"""

from __future__ import annotations

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
    """Return (supervisor_titles_by_slug, executor_titles_by_slug) from Master 64."""
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
        "product-owner-release": "Product Owner پس از Release",
    }
    for s, t in list(sup_slug.items()):
        if s in canon:
            sup_slug[s] = canon[s]
    return sup_slug, exe_slug


def load_master_map() -> dict[str, list[str]]:
    """Parse section 65: executor title -> [supervisor titles]."""
    text = MASTER.read_text(encoding="utf-8")
    body = _between(text, r"SUPERVISOR_MAP:\s*\n", r"\n«توجه:")
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
    "Product Owner پس از Release": "Product Owner پس از Release",
    "Product Owner پس از Release": "Product Owner پس از Release",
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
    (["بدون دسترسی", "no direct access", "no production access", "read only", "فقط مشاهده", "فقط مطالعه"], "NONE"),
    (["read", "مطالعه", "view", "monitor", "مشاهده"], "READ_ONLY"),
    (["limited", "محدود", "direct system access", "دسترسی مستقیم"], "LIMITED"),
    (["authorized write", "limited write", "نوشتن محدود"], "AUTHORIZED_WRITE"),
    (["full", "کامل", "admin", "مدیریت کامل"], "FULL"),
]


def production_authority(permissions: str, restricted: str) -> str:
    text = f"{permissions} {restricted}".lower()
    for keys, val in PROD_AUTH_MAP:
        if any(k in text for k in keys):
            return val
    return "Unknown / Requires Verification: سطح دسترسی Production در دادهٔ نقش صریح نیست"


# ---------------------------------------------------------------------------
# Small text helpers
# ---------------------------------------------------------------------------
def _unordered(items) -> str:
    return "\n".join(f"- {i}" for i in items)


def _uk(field: str) -> str:
    return f"Unknown / Requires Verification: «{field}» در دادهٔ این نقش ثبت نشده؛ فقط Context معتبر باید ارسال شود"


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
- **SuccessDefinition:** {p['quality']}
- **FailureDefinition:** خروجی بدون Evidence یا ناقص؛ عبور از Scope/Authority؛ {p['escalation']}"""


def sec_responsibilities(p, spec, meta) -> str:
    pri = _bullets(p['responsibilities'])
    sec = _unordered(spec['audit'] if meta['type'] == 'SUPERVISOR' else spec['impl'])
    if meta['type'] == 'SUPERVISOR':
        sup = _unordered([f"هماهنگی با مصرف‌کننده‌ها: {c}" for c in meta['consumers']] or [
            "دریافت خروجی از مجری‌ها و بررسی آن در Scope"] )
        out = ["پیاده‌سازی مستقیم (Implementation) خارج از Authority",
               "تصمیم‌های مالی/حقوقی/امنیتی خارج از Scope — ESCALATE"]
    else:
        sup = _unordered([f"هماهنگی با ناظر: {s}" for s in meta['supervisors']] or [
            "هماهنگی با ناظر/مالک تعریف‌شده"])
        out = ["تغییر فایل/سرویس خارج از Scope",
               "تغییر معماری، امنیت، قرارداد یا داده بدون تأیید ناظر"]
    return f"""## 3. Responsibilities
- **Primary:**
{pri}
- **Secondary (مختص این نقش):**
{sec}
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
- **Supervisor Capabilities:** {_unordered(caps) if meta['type'] == 'SUPERVISOR' else "NOT_APPLICABLE — این Persona نوع EXECUTOR است"}
- **Executor Capabilities:** {_unordered(caps) if meta['type'] == 'EXECUTOR' else "NOT_APPLICABLE — این Persona نوع SUPERVISOR است"}
- **Capabilities NOT owned (فقط در صورت Authority صریح):** {_unordered(other)}"""


def sec_authority(p, meta) -> str:
    if meta['type'] == 'SUPERVISOR':
        decisions = "APPROVE / REJECT / RECOMMEND / DEFER / ESCALATE"
        actions = "بررسی، ممیزی، ارزیابی، تأیید/رد، اولویت‌بندی، توصیه، نظارت، کنترل، اسکالیشن"
        forbid_d = "تصمیم اجرایی/پیاده‌سازی و تغییر مستقیم کد، پیکربندی یا دیتابیس"
        forbid_a = "اعمال تغییر در Production بدون مجوز؛ تغییر معماری/امنیت/قرارداد خارج از Authority"
        approve = "تغییر Scope، تغییر معماری، تغییر Production، تصمیم‌های امنیتی/حقوقی/مالی کلان"
    else:
        decisions = "PROCEED / PAUSE / RETRY / ROLLBACK / BLOCK / ESCALATE"
        actions = "پیاده‌سازی، پیکربندی، یکپارچه‌سازی، تست، استقرار، نگهداری، مستندسازی"
        forbid_d = "تصمیم ناظرانه: تأیید/رد نهایی Scope، معماری، امنیت، بودجه"
        forbid_a = "تغییر فایل خارج از Scope؛ ساخت API/وابستگی/کانفیگ بدون شواهد"
        approve = "تغییر فایل خارج از Scope، تغییر در Production، تغییر قرارداد/معماری/دیتابیس"
    auth = production_authority(p['permissions'], p['restricted'])
    return f"""## 5. Authority & Boundaries
- **AllowedDecisions:** {decisions}
- **AllowedActions:** {actions}
- **ApprovalRequiredFor:** {approve}
- **ForbiddenDecisions:** {forbid_d}
- **ForbiddenActions:** {forbid_a}
- **CrossDomainRules:** اگر تصمیم روی مالکیت Persona دیگر اثر دارد (معماری، امنیت، داده، مالی، حقوقی): شناسایی اثر → حفظ رفتار فعلی در صورت امکان → مستندسازی → **ESCALATE** به Persona مسئول.
- **ProductionAuthority:** {auth}"""


def sec_stakeholders(p, meta) -> str:
    if meta['type'] == 'SUPERVISOR':
        decision = meta['title']
        impl = "NOT_APPLICABLE — این Persona خود Implementation مستقیم انجام نمی‌دهد"
        reviewer = "، ".join(meta['supervisors']) or "NOT_APPLICABLE"
        approver = "، ".join(meta['supervisors']) or "NOT_APPLICABLE"
        supporting = "، ".join(meta['supervisors']) or "مصرف‌کننده‌ها (مجری‌های تحت نظارت)"
        consumers = "، ".join(meta['consumers']) or "NOT_APPLICABLE"
    else:
        decision = meta['supervisors'][0] if meta['supervisors'] else "Unknown / Requires Verification: ناظر باید در Registry باشد"
        impl = meta['title']
        reviewer = "، ".join(meta['supervisors']) or "Unknown / Requires Verification"
        approver = "، ".join(meta['supervisors']) or "Unknown / Requires Verification"
        supporting = "، ".join(meta['supervisors']) or "Unknown / Requires Verification"
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
- **Generated:** {_bullets(p['outputs'])}
- **Prohibited:** ورودی بدون منبع یا سند معتبر؛ داده/آرتیفکت نامعتبر؛ Context خارج از Scope این نقش
- **Validation:** هر ورودی باید با `Name / Type / Source / Required / Validation / Freshness` ثبت شود؛ در نبود منبع صریح: **Unknown / Requires Verification: ...**"""


def sec_preconditions(p) -> str:
    return f"""## 8. Preconditions
- **Required:** {_bullets(p['preconditions'])}
- **Optional:** NOT_APPLICABLE — در دادهٔ نقش تفکیک نشده (در صورت نیاز، از Context معتبر استفاده کن)
- **Blocking:** اگر ورودی الزامی در دسترس نباشد → `BLOCKED` (How Verified: منبع/آرتیفکت ورودی باید ثبت شود)
- **Authorization:** {p['permissions']}
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
- **RelevantHistory:** {_uk('RelevantHistory')}
- **Rule:** فقط Context مرتبط را دریافت کن؛ کل Project Context بدون نیاز ممنوع."""


def sec_memory(p) -> str:
    return f"""## 10. Memory
- **Working:** {_bullets(p['memory'])}
- **Persistent:** {_uk('Persistent Memory')}
- **Project:** {_uk('Project Memory')}
- **Role:** {_uk('Role Memory')}
- **Historical:** {_uk('Historical Memory')}
- **Rules:** Memory ≠ Evidence؛ Memory ≠ Requirement؛ Memory ≠ Authorization. اطلاعات Memory در تصمیم‌های مهم باید دوباره Verify شود."""


def sec_scope(p, meta) -> str:
    out_scope = ("پیاده‌سازی مستقیم خارج از Authority" if meta['type'] == 'SUPERVISOR'
                 else "تغییر فایل/سرویس/داده خارج از Scope تعیین‌شده")
    return f"""## 11. Scope
- **InScope:** {p['scope']}
- **OutOfScope:** {out_scope}؛ تصمیم‌های خارج از Authority ثبت و ESCALATE می‌شوند (نه سکوت)
- **AffectedAreas:** {meta['domain']} / {meta['category']}
- **FileScope:** {_uk('FileScope')}
- **ModuleScope:** {_uk('ModuleScope')}
- **ServiceScope:** {_uk('ServiceScope')}
- **EnvironmentScope:** {_uk('EnvironmentScope')}
- **ScopeExpansionPolicy:** REQUIRES_APPROVAL — هر توسعهٔ Scope باید مستند و تأیید شود"""


NFR_BY_GROUP = {
    "strategy": {"NonFunctional": "سازگاری با چشم‌انداز و اهداف، امکان‌سنجی منابع، ریسک عدم قطعیت مدیریت‌شده",
                 "Architecture": "همسویی تصمیم‌ها با معماری کلان", "Governance": "مدل تصمیم و مالکیت مستند",
                 "Compliance": "انطباق تصمیم‌های کلان با مقررات", "Operational": "قابلیت ترجمه به برنامهٔ اجرایی"},
    "product": {"NonFunctional": "قابلیت سنجش ارزش، شفافیت اولویت‌ها، مدیریت تغییر Scope",
                "Architecture": "سازگاری Roadmap با معماری محصول", "Governance": "مدل اولویت‌بندی و مالکیت Backlog",
                "Compliance": "انطباق با ملاحظات قانونی/حریم", "Operational": "پایش KPI و بازخورد کاربر"},
    "management": {"NonFunctional": "قابلیت ردیابی وضعیت، شفافیت زمان/منابع/ریسک",
                   "Architecture": "سازگاری برنامه با محدودیت‌های فنی", "Governance": "نقش و مالکیت تصمیم مستند",
                   "Compliance": "انطباق با فرایند و مقررات", "Operational": "گزارش وضعیت شامل بلوکر/ریسک"},
    "analysis": {"NonFunctional": "بدون ابهام، قابل آزمون، قابل ردیابی",
                 "Architecture": "سازگاری نیازها با معماری و داده", "Governance": "مسیر تأیید نیازمندی‌ها",
                 "Compliance": "پوشش الزامات قانونی/حریم در نیازها", "Operational": "نگاشت نیاز به خروجی/تست"},
    "architecture": {"NonFunctional": "مقیاس‌پذیری، نگهداشت، تغییرپذیری، Backward Compatibility",
                     "Architecture": "مرز اجزا، قراردادها و Decision Records", "Security": "پوشش کنترل‌های امنیتی در معماری",
                     "Performance": "ارزیابی ظرفیت/کارایی اجزا", "Scalability": "سناریوی مقیاس مستند",
                     "Reliability": "Fault Tolerance و مسیرهای شکست", "Compatibility": "سازگاری با سامانه‌های موجود",
                     "Governance": "مسیر تأیید معماری", "Operational": "قابلیت استقرار و پایش معماری"},
    "engineering": {"NonFunctional": "صحت رفتار، DRY، کیفیت کد، کارایی، امنیت پایه",
                    "Architecture": "رعایت قرارداد و مرز معماری", "Security": "اعتبارسنجی ورودی/خروجی، عدم افشای Secret",
                    "Performance": "پایش p95/Throughput", "Compatibility": "Backward Compatibility",
                    "Testing": "پوشش Edge/Failure", "Operational": "Logging/Tracing و قابلیت رگرسیون"},
    "ai": {"NonFunctional": "بازتولیدپذیری، پایش Drift، کنترل هزینه",
           "Architecture": "مرز Agent/مدل و قرارداد ابزار", "Security": "Guardrail، Jailbreak، دادهٔ حساس",
           "Performance": "کیفیت مدل (Eval Score)، Latency", "Reliability": "Fallback و رفتار خطا",
           "Compliance": "حریم خصوصی و انطباق استفاده از مدل", "Operational": "پایش و Evaluation پیوسته"},
    "data": {"NonFunctional": "دقت، یکپارچگی، کارایی و امنیت داده",
             "Architecture": "سازگاری Schema/Migration با معماری", "Security": "دسترسی، رمزنگاری و ردیابی داده",
             "Performance": "کارایی Query/Index", "Reliability": "Backup/Restore و DR",
             "Compliance": "طبقه‌بندی داده و حریم خصوصی", "Operational": "کیفیت و پایش داده"},
    "devops": {"NonFunctional": "تکرارپذیری، مشاهده‌پذیری، بازیابی‌پذیری",
               "Architecture": "سازگاری CI/CD و محیط‌ها", "Security": "مدیریت Secret و Least Privilege",
               "Performance": "زمان Build/Deploy و ظرفیت", "Reliability": "Rollback/Canary و آمادگی حادثه",
               "Compatibility": "سازگاری پلتفرم/نسخه‌ها", "Operational": "Alert/Runbook و پایش"},
    "qa": {"NonFunctional": "تکرارپذیری تست، پوشش Edge، پیگیری Defect",
           "Architecture": "پوشش لایه‌ها و قراردادها در تست", "Security": "کیس‌های امنیتی در استراتژی تست",
           "Performance": "تست بار/کارایی", "Reliability": "پایداری و Flaky Rate",
           "Compatibility": "پوشش نسخه‌ها/مرورگرها/پلتفرم‌ها", "Operational": "گزارش و پیگیری Defect"},
    "security": {"NonFunctional": "پوشش کنترل‌ها، مدیریت آسیب‌پذیری، کشف به‌موقع",
                 "Architecture": "انطباق کنترل‌ها با معماری", "Security": "Threat Modeling، اعتبارسنجی، Secret",
                 "Performance": "اثر کنترل‌ها بر کارایی", "Reliability": "پاسخ و بازیابی حادثه",
                 "Compliance": "انطباق با مقررات و سیاست‌ها", "Operational": "پایش، گزارش و پیگیری"},
    "compliance": {"NonFunctional": "انطباق، شواهد کامل، ردیابی تصمیم",
                   "Architecture": "تأثیر الزامات بر معماری", "Security": "حفاظت داده در فرایند انطباق",
                   "Reliability": "ثبات فرایند کنترل", "Compliance": "پوشش قوانین/قرارداد/حریم",
                   "Operational": "گیت‌های کنترل و گزارش‌دهی"},
    "design": {"NonFunctional": "یکدستی، دسترس‌پذیری، پوشش Stateها",
               "Architecture": "سازگاری با Design System", "Security": "حریم دادهٔ کاربری در طراحی",
               "Performance": "کارایی UI/تعامل", "Reliability": "پوشش حالت‌های خطا/خالی",
               "Compatibility": "ریسپانسیو و دسترس‌پذیری", "Operational": "قابلیت تست و پیاده‌سازی"},
    "content": {"NonFunctional": "دقت، کامل بودن، یکدستی اصطلاحات",
                "Architecture": "سازگاری اسناد با نسخه/رفتار", "Security": "عدم افشای اطلاعات در مستندات",
                "Compatibility": "سازگاری با پلتفرم/نسخه‌ها", "Operational": "به‌روزرسانی و دسترسی اسناد"},
    "people": {"NonFunctional": "عدالت، عدم تبعیض، حفاظت دادهٔ شخصی",
               "Architecture": "سازگاری ساختار نقش/تیم با سازمان", "Security": "حریم دادهٔ افراد",
               "Compliance": "انطباق استخدام/داده با مقررات", "Operational": "فرایند شفاف و قابل ارزیابی"},
    "support": {"NonFunctional": "سرعت پاسخ، پیوستگی مالکیت، رضایت",
                "Architecture": "سازگاری فرایند پشتیبانی با محصول", "Security": "حفاظت دادهٔ مشتری",
                "Reliability": "ثبات SLA", "Compliance": "مطابقت با تعهدات/قوانین", "Operational": "اسکالیشن و دانش‌نامه"},
    "growth": {"NonFunctional": "قابل اندازه‌گیری، هم‌راستا با برند، ROI شفاف",
               "Architecture": "سازگاری پیام با محصول", "Security": "حریم دادهٔ مخاطب",
               "Compliance": "انطباق بازاریابی/فروش با مقررات", "Operational": "پایش KPI و آزمایش"},
    "assurance": {"NonFunctional": "استقلال، عینیت، پوشش کامل، شواهد ردیابی‌شده",
                  "Architecture": "پوشش معماری در محدودهٔ ممیزی", "Security": "مسئولیت‌پذیری و امنیت اطلاعات ممیزی",
                  "Reliability": "تکرارپذیری ممیزی", "Compliance": "انطباق با استانداردهای ممیزی",
                  "Operational": "گزارش، پیگیری و بسته‌شدن یافته‌ها"},
    "ops": {"NonFunctional": "آمادگی، بازیابی سریع، بهبود مستمر",
            "Architecture": "سازگاری Runbook با معماری", "Security": "امنیت فرایند عملیات",
            "Performance": "SLA و MTTR", "Reliability": "Availability/Recovery",
            "Compliance": "انطباق عملیات با سیاست‌ها", "Operational": "Alert، Postmortem و Runbook"},
}


def sec_criteria(p, spec, meta, group) -> str:
    nfr = NFR_BY_GROUP.get(group, NFR_BY_GROUP["engineering"])
    if meta['type'] == 'SUPERVISOR':
        lines = [
            "- **Functional:**", _bullets(p['quality']), "",
            "- **NonFunctional:**", f"- {nfr.get('NonFunctional', 'پوشش NFR')}", "",
        ]
        for key in ["Architecture", "Security", "Performance", "Scalability",
                    "Reliability", "Compatibility", "Governance", "Compliance", "Operational"]:
            lines.append(f"- **{key}:** {nfr.get(key, _uk(key))}")
        return "## 12. Criteria / Requirements\n" + "\n".join(lines)
    lines = [
        "- **Functional:**", _bullets(p['quality']), "",
        "- **Technical (مختص این نقش):**", _unordered(spec['impl']), "",
        "- **API:**", f"- {nfr.get('Architecture', _uk('API'))}",
        "- **Data:**", f"- {nfr.get('Security', _uk('Data'))}",
        "- **Security:**", f"- {nfr.get('Security', 'اعتبارسنجی و عدم افشای Secret')}",
        "- **Performance:**", f"- {nfr.get('Performance', _uk('Performance'))}",
        "- **Compatibility:**", f"- {nfr.get('Compatibility', _uk('Compatibility'))}",
        "- **Testing:**", f"- {nfr.get('Testing', 'تست قبل و بعد از تغییر با شواهد')}",
        "- **Configuration:**", f"- {_uk('Configuration')}",
        "- **Migration:**", f"- {_uk('Migration')}",
    ]
    return "## 12. Criteria / Requirements\n" + "\n".join(lines)


def _step_kind(name: str) -> str:
    n = name.lower()
    if any(k in n for k in ["audit", "ممیزی", "govern", "حاکم", "control", "کنترل"]):
        return "AUDIT"
    if any(k in n for k in ["inspect", "بازبینی", "check", "بررسی"]):
        return "INSPECT"
    if any(k in n for k in ["assess", "ارزیابی"]):
        return "ASSESS"
    if any(k in n for k in ["analy", "understand", "discover", "تحلیل", "فهم", "درک"]):
        return "ANALYZE"
    if any(k in n for k in ["design", "architect", "model", "define", "research", "طراحی", "تعریف"]):
        return "DESIGN"
    if any(k in n for k in ["plan", "برنامه", "roadmap", "نقشه"]):
        return "PLAN"
    if any(k in n for k in ["implement", "build", "develop", "create", "code", "write", "transform", "پیاده", "ساخت", "توسعه"]):
        return "IMPLEMENT"
    if any(k in n for k in ["integrat", "connect", "link", "wire", "اتصال", "یکپارچه", "integrate"]):
        return "INTEGRATE"
    if any(k in n for k in ["test", "validat", "verify", "check", "optim", "تست", "اعتبار", "بهینه"]):
        return "TEST"
    if any(k in n for k in ["monitor", "پایش", "نظارت", "measure", "سنجش"]):
        return "MONITOR"
    if any(k in n for k in ["document", "مستند"]):
        return "DOCUMENT"
    if any(k in n for k in ["deploy", "استقرار", "release", "انتشار"]):
        return "INTEGRATE"
    if any(k in n for k in ["review", "report", "deliver", "retrospect", "گزارش", "مرور"]):
        return "REVIEW"
    if any(k in n for k in ["handoff", "تحویل"]):
        return "HANDOFF"
    return "VALIDATE"


_STEP_ACTIONS_MASTER = {
    "ANALYZE": ["ورودی‌ها و Scope را با شواهد بررسی کن.", "کد/سند/داده/سرویس متأثر را شناسایی کن.",
                "رابط‌ها، وابستگی‌ها و ریسک‌های پنهان را مشخص کن.", "شمول/عدم شمول را با دلیل ثبت کن."],
    "ASSESS": ["معیارهای ارزیابی را از Scope استخراج کن.", "شواهد موجود را جمع و مرتب کن.",
               "وضعیت را در برابر معیارها بسنج.", "نتیجه را با سطح اطمینان ثبت کن."],
    "INSPECT": ["هدف و محدودهٔ بررسی را تعیین کن.", "منابع/فایل‌ها/بخش‌ها را enumerate کن.",
                "هر مورد را با شواهد بررسی کن.", "یافته/غیاب شواهد را ثبت کن."],
    "DESIGN": ["گزینه‌های معتبر را با معیار مشخص مقایسه و مستند کن.", "Design/Plan را با Scope و Authority محدود کن.",
               "قراردادها/رابط‌ها/Stateها را مشخص کن.", "اثر تغییر روی رفتار موجود را ارزیابی کن؛ خارج از Scope → ESCALATE."],
    "PLAN": ["موارد درست و ترتیب وابستگی‌ها را تعیین کن.", "گام‌های قابل اجرا و قابل راستی‌آزمایی تعریف کن.",
             "Hidden Work (خطا، اعتبارسنجی، تست، مهاجرت، مستندسازی، امنیت) را شناسایی کن.", "معیار پذیرش هر فاز/گام را بنویس."],
    "IMPLEMENT": ["فقط Scope همین Persona را پیاده‌سازی کن.", "ورودی‌ها را Validate و خروجی را مطابق قرارداد تولید کن.",
                  "Edge/Error/Stateها را پوشش بده.", "رفتار موجود را حفظ کن مگر تغییر عمدی مستند."],
    "INTEGRATE": ["قرارداد/رابط بین اجزا را راستی‌آزمایی کن.", "Backward و سازگاری رفتاری را حفظ کن.",
                  "خطاهای Integration را جدا/مستند کن؛ در مرز مسئولیت دیگر → ESCALATE."],
    "TEST": ["تست/validation متناسب با Scope بنویس و اجرا کن.", "حالت‌های Applicable (موفق/خطا/خالی/edge/authz/perf) را پوشش بده.",
             "نتیجه را با شواهد ثبت کن؛ شاهد ناکافی → BLOCKED/NEEDS_CLARIFICATION."],
    "VALIDATE": ["خروجی را با معیار پذیرش مقایسه کن.", "شواهد و ردیابی را کنترل کن.",
                 "نتیجه را با Status و State ثبت کن؛ بدون شواهد ادعای موفقیت نکن."],
    "REVIEW": ["خروجی را با Quality Gate و DoD مقایسه کن.", "شواهد و ردیابی را کنترل کن.",
               "یافته‌ها را یکپارچه و Deduplicate کن.", "نتیجهٔ نهایی را با Status و State گزارش کن."],
    "AUDIT": ["Scope و Coverage Manifest تعریف کن.", "منابع/فایل‌ها/بخش‌ها را enumerate و segment کن.",
              "هر Segment را با شواهد بررسی کن.", "یافته‌ها را با Root Finding ثبت و Risk را ارزیابی کن."],
    "GOVERN": ["تصمیم را در Scope و Authority ارزیابی کن.", "با مالک/ناظر سنجیده و مستند کن.",
               "Result را با معیار ثبت کن و از تصمیم خارج از Authority خودداری کن."],
    "VERIFY": ["ادعا را فقط با شاهد بپذیر.", "شاهد/Evidence را با Location ثبت کن.",
               "وضعیت VERIFIED/POTENTIAL/UNVERIFIED را ثبت کن.", "ادعای بدون شاهد را «ادعای پشتیبانی‌نشده» گزارش کن."],
    "MONITOR": ["شاخص‌ها و منبع داده را مشخص کن.", "مقادیر را با شواهد ثبت کن.",
                "انحراف/report را شناسایی و به Persona مسئول ESCALATE کن."],
    "OPTIMIZE": ["گلوگاه/فرصت را با معیار مشخص کن.", "تغییر حداقلی با اثر قابل اندازه‌گیری اعمال کن.",
                 "Regression را قبل/بعد بسنج و مستند کن."],
    "DOCUMENT": ["هدف/مخاطب/ساختار سند را تعیین کن.", "محتوای دقیق مبتنی بر شواهد بنویس.",
                 "با رفتار/نسخه تطبیق بده و بازبینی کن."],
    "HANDOFF": ["آرتیفکت‌های لازم و Recipient را مشخص کن.", "Acceptance Criteria و ExecutionPlan را ضمیمه کن.",
                "مسئولیت/تصمیم باقی‌مانده را صریح تحویل بده."],
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
- **Type:** {kind}
- **Objective:** اجرای گام «{name}» با حفظ Scope و بدون تغییر خارج از Authority.
- **Inputs:** {p['required']}  |  Optional: {p['optional']}
- **Preconditions:** {p['preconditions']}
- **Actions:"""
                     + "\n".join(f"{j}. {a}" for j, a in enumerate(actions, 1))
                     + f"""
- **Validation:** {p['quality']}
- **Outputs:** {p['outputs']}
- **Evidence:** {p['evidence']}
- **DecisionPoints:** در این گام از Status مجاز استفاده کن (PASS / FAIL / BLOCKED / NEEDS_CLARIFICATION / ESCALATE / NOT_APPLICABLE) و نتیجه را مستند کن.
- **ExitCriteria:** خروجی گام با معیار پذیرش مطابقت دارد و شواهد ثبت شده‌اند.
- **FailureConditions:** ورودی ناقص/متناقض، خارج از Scope، یا شواهد ناکافی.
- **EscalationConditions:** {p['escalation']}""")
    return "\n\n".join(chunks)


def sec_procedure(p) -> str:
    return "## 13. Procedure\n" + _structured_steps_master(p)


def sec_decision_rules(p, meta) -> str:
    common = "PASS / FAIL / BLOCKED / NEEDS_CLARIFICATION / ESCALATE / NOT_APPLICABLE"
    if meta['type'] == 'SUPERVISOR':
        values = "APPROVE / REJECT / RECOMMEND / DEFER / ESCALATE"
        note = "ناظر فقط بر اساس Scope و شواهد تصمیم می‌گیرد؛ بدون Evidence تأیید نمی‌کند."
    else:
        values = "PROCEED / PAUSE / RETRY / ROLLBACK / BLOCK / ESCALATE"
        note = "مجری بدون شواهد (تست/Build/مانیفست) Completion اعلام نمی‌کند."
    return f"""## 14. Decision Rules
- **Status Values (همهٔ Persona):** {common}
- **Decision Values ({meta['type']}):** {values}
- **Role-specific rules:**
{_bullets(p['decision'])}
- **Rules:** {note}
- هر `NOT_APPLICABLE` باید دلیل داشته باشد؛ هر Escalation باید Target مشخص داشته باشد."""


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
- **Restricted:** {_bullets(p['restricted'])}
- **Forbidden:** ابزار/دسترسی‌ای که در «Restricted» ذکر شده؛ هر ابزار بدون مدرک اجازهٔ استفاده.
- **ApprovalRequired:** Production/تغییر دسترسی، ابزار خارج از لیست Allowed، تغییر دیتابیس/زیرساخت.
- **ReadOnly:** {production_authority(p['permissions'], p['restricted'])}
- **Categories (مطابق Master):** {cats.get(group, 'Documentation, Filesystem')}"""


def sec_evidence(p) -> str:
    return f"""## 16. Evidence & Verification
- **Evidence لازم:** {_bullets(p['evidence'])}
- **Evidence Status:** VERIFIED / POTENTIAL / UNVERIFIED / MISSING
- **Evidence Types:** FILE / LINE / CODE / DIFF / TEST_RESULT / BUILD_OUTPUT / LOG / TRACE / SCREENSHOT / API_RESPONSE / DATABASE_RESULT / BENCHMARK / METRIC / CONFIGURATION / DOCUMENT / ARCHITECTURE_DIAGRAM / DATASET / AUDIT_RECORD / USER_FEEDBACK
- **Evidence Location:** FILE / LINE ، DOCUMENT / SECTION ، API / ENDPOINT ، DATABASE / TABLE / COLUMN ، ARCHITECTURE / NODE ، CONFIGURATION / KEY ، LOG / TIMESTAMP ، DATASET / FIELD ، TEST / CASE
- **Rule:** هر ادعای مهم به Evidence قابل ردیابی متصل است؛ بدون Evidence: **MISSING** → ادعا ثبت نمی‌شود."""


def sec_coverage(meta) -> str:
    if meta['type'] == 'SUPERVISOR':
        body = """- **Total Scope / Reviewed Scope / Unreviewed Scope / Blocked Scope / Coverage %:** در هر ممیزی محاسبه و ثبت کن.
- **Formula:** Coverage % = Reviewed Scope Items / Total Scope Items × 100
- **Completion Rule:** 100% Coverage + All Mandatory Checks Passed + No Blocking Issue + All Required Evidence = Review Complete
- **Manifest:** هر فایل/بخش Scope باید `Discovered → Classified → Reviewed → Status-marked` شود (REVIEWED / IN_PROGRESS / NOT_REVIEWED + دلیل معتبر)."""
    else:
        body = """- **Total Scope:** همهٔ فایل‌ها/بخش‌های متأثر از تسک.
- **Reviewed/Unreviewed/Blocked/Change Coverage %:** نسبت فایل‌های تغییر/تست‌شده به کل Scope تغییر.
- **Formula:** Change Coverage % = Changed & Tested Items / Total Changed Items × 100
- **Completion Rule:** تمام Incrementها کامل + Change Manifest کامل + Tests اجراشده + No Blocking Issue = Detailed completion.
- **Manifest:** هر فایل تغییر: Action/Scope/Status/Reason/RequirementIDs/TestStatus/Evidence."""
    return "## 17. Coverage / Completeness\n" + body


def sec_findings(meta) -> str:
    if meta['type'] == 'SUPERVISOR':
        return """## 18. Findings / Changes
**هر Finding (قالب):** ID / ROOT_FINDING_ID / SEGMENT / SOURCE / LOCATION / SEVERITY / CONFIDENCE / EVIDENCE_STATUS / CATEGORY / TITLE / EVIDENCE / PROBLEM / TRIGGER / EXPECTED / ACTUAL / IMPACT / AFFECTED / RISK / RECOMMENDED_FIX / OWNER / REGRESSION_RISK / MISSING_EVIDENCE / WHAT_WOULD_CONFIRM
- **Severity:** CRITICAL / HIGH / MEDIUM / LOW / INFO — **Confidence:** CONFIRMED / HIGH / MEDIUM / LOW
- **Lifecycle:** DETECTED → VALIDATING → CONFIRMED → REPORTED → ACCEPTED → PLANNED → FIXED → REVALIDATED → CLOSED (side: REJECTED / FALSE_POSITIVE / DEFERRED)
- **Deduplication:** یافته‌های هم‌ریشه با ROOT_FINDING_ID + AFFECTED یک‌بار ثبت می‌شوند؛ حذف Impact واقعی ممنوع است."""
    return """## 18. Findings / Changes
**ChangeManifest:** Path → Action / Scope / Status / Reason / RequirementIDs / TestStatus / Evidence
- **Allowed Actions:** CREATED / MODIFIED / DELETED / RENAMED / UNCHANGED
- **Status:** COMPLETED / IN_PROGRESS / INCOMPLETE / BLOCKED
- **Increment:** ID / Objective / Files / Requirements / Dependencies / ExpectedResult / Tests / Evidence / Status
- **Rules:** هیچ تغییر Silent مجاز نیست؛ Fragmentation مصنوعی، Over-Merging و Scope Expansion پنهان ممنوع."""


def sec_risk(p, spec, meta) -> str:
    focus = spec['audit'] if meta['type'] == 'SUPERVISOR' else spec['impl']
    return f"""## 19. Risk
- **Model:** Risk → ID / SourceFindings / Likelihood / Impact / Score / AffectedAreas / Mitigation / Owner / ResidualRisk
- **Likelihood:** RARE / UNLIKELY / POSSIBLE / LIKELY / ALMOST_CERTAIN
- **Impact:** NEGLIGIBLE / LOW / MEDIUM / HIGH / CRITICAL
- **Rule:** Finding ≠ Risk. یافته را به Risk تبدیل نکن؛ ریسک را از یافته‌ها با ارزیابی احتمال/اثر استخراج کن.
- **Role Risk Focus (مختص این نقش):**
{_unordered(focus)}
- **Escalation Signals:** {p['escalation']}"""


def sec_recommendations(p, spec, meta) -> str:
    if meta['type'] == 'SUPERVISOR':
        return f"""## 20. Recommendations / Implementation
- **Recommendation:** ID / RelatedFindings / Objective / ProposedChange / Priority / Dependencies / Owner / ExpectedOutcome / ValidationMethod
- **Priority:** P0 / P1 / P2 / P3 / P4
- **Role-specific focus برای Recommendation:**
{_unordered(spec['audit'])}
- **Implementation:** فقط در Scope و به‌صورت Execution Plan؛ هیچ پیاده‌سازی مستقیم خارج از Authority."""
    return f"""## 20. Recommendations / Implementation
- **Implementation Outputs:** Source Code / Configuration / Schema / Migration / Tests / Build Artifacts / Documentation / Infrastructure Changes / Deployment Artifacts / Reports
- **فقط در Scope خود:** هر خروجی باید با Requirement و Evidence ردیابی شود.
- **Role-specific (مختص این نقش):**
{_unordered(spec['impl'])}"""


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
{_unordered(gates)}
### Role-Specific Acceptance Criteria (مختص این نقش)
{_unordered(spec['accept'])}"""


def sec_traceability() -> str:
    return """## 22. Traceability
- **Universal chain:** Requirement → Criterion → Design → Implementation → Test → Evidence → Acceptance
- **IDs:** REQ-### / CRIT-### / DESIGN-### / IMP-### / TEST-### / EVIDENCE-### / RISK-### / FIND-### / REC-### / ACCEPT-### / CHANGE-###
- **Rule:** هر خروجی مهم باید به این زنجیره متصل باشد؛ شناسهٔ رسمی نبود → شناسهٔ توصیفی قابل ردیابی."""


def sec_state_machine(p, meta) -> str:
    if meta['type'] == 'SUPERVISOR':
        sm = ("RECEIVED → SCOPING → CONTEXT_ASSEMBLY → ASSESSING → INSPECTING → ANALYZING → "
              "VALIDATING → FINDINGS_REVIEW → RECOMMENDATION_READY → HANDOFF_PENDING → COMPLETED")
        side = "BLOCKED / ESCALATED / NEEDS_CLARIFICATION / FAILED"
        desc = "ناظر هرگز وارد狀態‌های Implementation مستقیم نمی‌شود؛ خروجی نهایی فقط با Evidence و Coverage کامل."
    else:
        sm = ("RECEIVED → UNDERSTANDING → INSPECTING → PLANNING → IMPLEMENTING → INTEGRATING → "
              "TESTING → VERIFYING → REVIEW_PENDING → CHANGES_REQUIRED → COMPLETED")
        side = "BLOCKED / ESCALATED / NEEDS_CLARIFICATION / FAILED / ROLLBACK_REQUIRED"
        desc = "برگشت از REVIEW_PENDING به CHANGES_REQUIRED و از TESTING به ROLLBACK_REQUIRED مجاز است."
    return f"""## 23. State Machine
- **States ({meta['type']}):** `{sm}`
- **Side states:** {side}
- **Rules:** {desc}
- **Project lifecycle (از دادهٔ نقش):** {p['lifecycle']}"""


def sec_handoff(p, meta) -> str:
    recv = "، ".join(meta['consumers']) if meta['consumers'] else p['handoff']
    return f"""## 24. Handoff
- **PrimaryRecipient:** {recv}
- **SupportingRecipients:** {', '.join(meta['supervisors']) if meta['supervisors'] else '—'}
- **DecisionOwner:** {meta['supervisors'][0] if meta['supervisors'] and meta['type'] == 'EXECUTOR' else meta['title']}
- **ImplementationOwner:** {meta['title'] if meta['type'] == 'EXECUTOR' else '— (ناظر خودش پیاده‌سازی نمی‌کند)'}
- **RequiredArtifacts:** {p['outputs']}
- **RequiredActions:** بازبینی/تأیید بر اساس Acceptance، تداوم اجرای پلن، ثبت وضعیت در `state`
- **AcceptanceCriteria:** {p['quality']}
- **ExecutionPlan:** audits/{SLUG_OVERRIDES.get(meta['title'], _slug(meta['title']))}-execution-plan.md"""


def sec_escalation(p, meta) -> str:
    return f"""## 25. Escalation
- **Trigger:** {p['escalation']}
- **Evidence:** شواهد یا «Unknown / Requires Verification» مرتبط با Trigger
- **Impact:** ریسک/محدودیت ناشی از وضعیت (باید صریح ثبت شود)
- **BlockedWork:** گام/فایل/تصمیم متوقف‌شده
- **DecisionRequired:** تصمیمی که خارج از Scope/Authority این Persona است
- **TargetPersona:** {', '.join(meta['supervisors']) if meta['supervisors'] else 'Persona مالک (طبق Registry)'}
- **Urgency:** P0 (Immediate) / P1 / P2
- **Triggers (رسمی):** SCOPE_CONFLICT / ARCHITECTURE_CONFLICT / SECURITY_RISK / DATA_RISK / LEGAL_RISK / COMPLIANCE_RISK / PRODUCTION_RISK / MISSING_REQUIRED_INPUT / AMBIGUOUS_REQUIREMENT / UNKNOWN_DEPENDENCY / OWNERSHIP_CONFLICT / BLOCKING_FAILURE"""


def sec_execution_plan(meta, title) -> str:
    slug = SLUG_OVERRIDES.get(title, _slug(title))
    path = f"audits/{slug}-execution-plan.md"
    if meta['type'] == 'SUPERVISOR':
        who = ("Supervisor MUST در صورت نیاز به کار remediation/implementation یک Execution Plan تولید کند و آن را "
               f"در `{path}` ذخیره کند. قالب: Dependency-aware، Scope-complete، Phase-coherent، Executable، Verifiable، Stable. "
               "ساختار فایل: `# قوانین ثابت انجام پروژه` + `# پلن اجرایی` با `## [🔴] فاز ...`، `### [🔴] گام ...` و `### معیار پذیرش`.")
    else:
        who = ("Executor MUST پلن را بخواند، اجرا کند، گام‌های انجام‌شده را حفظ کند، کار کشف‌شده را با دلیل اضافه کند و "
               "وضعیت هر گام/فاز را فقط با `[🔴]` / `[🟡]` / `[🟢]` به‌روزرسانی کند. حذف گام‌های انجام‌شده، پنهان‌کردن شکست و "
               "بازنویسی بی‌صدا ممنوع.")
    return f"""## 26. Execution Plan
- **Path:** {path}
- **Rule:** {who}"""


def sec_execution_result() -> str:
    return """## 27. Execution Result
```
Status: <PASS | FAIL | BLOCKED | ESCALATE | NEEDS_CLARIFICATION | NOT_APPLICABLE>
Verdict: <...>
State: <یکی از State Machine این Persona>
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
{_bullets(kpi)}
- KPI فقط برای Evaluation است؛ رفتار مصنوعی برای رسیدن به عدد ممنوع.
- بدون Evidence → `Unknown` ثبت کن."""


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
- **Scope:** {p['scope']}
- **محدودهٔ ممیزی:** فقط Scope/Authority همین Persona؛ هر بخش خارج از Scope با دلیل EXCLUDE ثبت می‌شود.
- **Rule:** Scope قبل از شروع صریحاً enumerate شود.

## Audit Criteria
- **مختص این نقش:** {_unordered(spec['audit'])}
- **معیارها:** {_bullets(p['quality'])}
- هر معیار باید قابل سنجش و مبتنی بر شواهد باشد.

## Audit Procedure
`RECEIVED` → `SCOPING` → `CONTEXT_ASSEMBLY` → `ASSESSING` → `INSPECTING` → `ANALYZING` → `VALIDATING` → `FINDINGS_REVIEW` → `RECOMMENDATION_READY` → `HANDOFF_PENDING` → `COMPLETED`
- در هر گام: Input → Action → Validation → Output → Evidence.
- یافته‌های هم‌ریشه Deduplicate و هر Segment با شواهد بررسی می‌شود.

## Coverage Manifest
```
CoverageManifest:
  - Segment:
      Files: [...]
      Components: [...]
      Status: REVIEWED | IN_PROGRESS | NOT_REVIEWED
      Reason: OUT_OF_SCOPE | MISSING_ACCESS | MISSING_ARTIFACT | DELETED | UNAVAILABLE | BLOCKED
      Findings: [...]
```

## Decomposition Table
| Segment | Files/Components | Review Status | Findings | Notes |
|---|---|---|---|---|
| ... | ... | REVIEWED / IN_PROGRESS / NOT_REVIEWED | FIND-### | ... |

## Findings
- هر یافته طبق قالب بخش ۱۸؛ هر یافته دارای `FILE / LINE`، Severity، Confidence و EvidenceStatus.
- یافتهٔ `POTENTIAL` باید `MISSING EVIDENCE` و `WHAT WOULD CONFIRM IT` داشته باشد.
- یافتهٔ تکراری ساخته نمی‌شود؛ `ROOT_FINDING_ID` حفظ می‌شود.

## Risk Assessment
- از مدل Risk بخش ۱۹ استفاده کن؛ احتمال/اثر/ریسک باقی‌مانده/مالک/کاهش را ثبت کن.
- ریسک‌ها را از یافته‌ها استخراج کن، نه برعکس.

## Recommendations
- طبق بخش ۲۰ با Priority (P0–P4) و مالک؛ هر Recommendation به Find/Risk متصل است.
- محورهای خاص این نقش: {_unordered(spec['audit'])}

## Execution Plan
- اگر remediation لازم است: پلن با قالب Master تولید و در `audits/{slug}-execution-plan.md` ذخیره شود.
- مسیر پلن در Execution Result و Handoff درج شود.

## Final Verdict
- Verdict فقط بر اساس Coverage کامل، شواهد ثبت‌شده و معیارها: `CONSISTENT & READY` / `INCONSISTENT` / `NEEDS REDESIGN` / `BLOCKED` / `NOT_APPLICABLE`.
- ادعای «بررسی کامل» فقط با Coverage Manifest + Decomposition کامل."""


def executor_specific(p, spec, meta, title) -> str:
    slug = SLUG_OVERRIDES.get(title, _slug(title))
    return f"""## Implementation Scope
- **Scope:** {p['scope']}
- **Boundaries:** فقط فایل‌ها/سرویس‌های در Scope؛ هر تغییر خارج از Scope → ESCALATE.
- **ScopeExpansionPolicy:** REQUIRES_APPROVAL + ثبت دلیل.

## Implementation Requirements
- **Functional:** {_bullets(p['quality'])}
- **Technical (مختص این نقش):** {_unordered(spec['impl'])}
- هر requirement به Accept و Test متصل است.

## Implementation Procedure
`RECEIVED` → `UNDERSTANDING` → `INSPECTING` → `PLANNING` → `IMPLEMENTING` → `INTEGRATING` → `TESTING` → `VERIFYING` → `REVIEW_PENDING` → `CHANGES_REQUIRED` → `COMPLETED`
- در هر گام: Input → Action → Validation → Output → Evidence.

## Change Manifest
```
ChangeManifest:
  - Path: <...>
      Action: CREATED | MODIFIED | DELETED | RENAMED | UNCHANGED
      Scope: <...>
      Status: COMPLETED | IN_PROGRESS | INCOMPLETE | BLOCKED
      Reason: <...>
      RequirementIDs: [REQ-###]
      TestStatus: PASS | FAIL | NOT_RUN
      Evidence: [EVIDENCE-###]
```

## Modified Files
- فهرست کامل مسیرهای تغییر‌یافته با دلیل و Effect — هیچ تغییر خاموشی.

## Created Files
- فهرست کامل فایل‌های جدید با هدف و Evidence.

## Deleted Files
- فهرست کامل فایل‌های حذف‌شده + دلیل + جایگزین/مهاجرت.

## Tests
- قبل از تغییر: تست Baseline. بعد از تغییر: تست مرتبط + Regression.
- هر تست با `TEST-###`، نتیجه و شواهد ثبت شود؛ بدون اجرا، نتیجه‌ای ادعا نشود.

## Verification
- Syntax → Behavior → Regression → Evidence → Manifest → DoD.
- ادعای موفقیت فقط با شواهد (Build/Test/Manifest).

## Evidence
- {_bullets(p['evidence'])}
- هر شاهد با `EVIDENCE-###` و Location ثبت شود (FILE/LINE، API/ENDPOINT، ...).

## Execution Plan Status
- **Plan Path:** `audits/{slug}-execution-plan.md` (اگر وجود دارد)
- وضعیت هر گام/فاز: `[🔴]` Not Implemented / `[🟡]` Partially Implemented / `[🟢]` Fully Implemented.
- فاز فقط با ALL Steps = 🟢 و ALL Acceptance = PASS 🟢 می‌شود.

## Final Completion Status
- **DoD:** All Increments Complete + Manifest Complete + Modified Files Recorded + Tests Executed + Regression Checked + Evidence Recorded + No Blocking Issue + Handoff Complete + Execution Result Complete.
- بدون تحقق DoD، Completion اعلام نشود."""


# ---------------------------------------------------------------------------
# Document assembly
# ---------------------------------------------------------------------------
def build_persona(title: str, role_type: str, p: dict, spec: dict, meta: dict) -> str:
    group = spec["domain"]
    head = f"# Persona — {title}\n\n> **نوع:** {meta['type']}  |  **Role_ID:** {meta['role_id']}\n\n---\n"
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
        ptype = "SUPERVISOR" if role_type == "ناظر" else "EXECUTOR"
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
    # Registered supervisor titles (canonical) = rows of README with role ناظر
    rows = read_rows()
    data_rows = [r for r in rows[1:]]
    sup_titles = {r[0] for r in data_rows if r[2] == "ناظر"}
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
        if role_type == "ناظر":
            meta["supervisors"] = []
            meta["consumers"] = sorted(by_supervisor.get(title, []))
        else:
            sups = sup_map.get(title)
            if not sups:
                warn_supervisor_missing.append(title)
                sups = ["Unknown / Requires Verification: supervisor باید در Registry تعریف شود"]
            meta["supervisors"] = sups
            meta["consumers"] = []

        persona = details.get(title)
        if persona is None:
            raise SystemExit(f"MISSING details row: {title}")
        persona = _norm_persona(persona)
        spec = spec_for(slug)

        content = build_persona(title, role_type, persona, spec, meta)
        out_dir = AUDIT_DIR if role_type == "ناظر" else IMPL_DIR
        (out_dir / f"{slug}.md").write_text(content, encoding="utf-8")
        written.append((slug, role_type))

    # ---- legacy README link labels are already in README ----
    print(f"Personas written: {len(written)}")
    sup_n = sum(1 for _, t in written if t == "ناظر")
    exe_n = sum(1 for _, t in written if t == "مجری")
    print(f"Supervisors: {sup_n}   Executors: {exe_n}")
    if warn_supervisor_missing:
        print("WARNING executors without supervisor:", warn_supervisor_missing)
    else:
        print("All executors have a registered supervisor.")


if __name__ == "__main__":
    main()
