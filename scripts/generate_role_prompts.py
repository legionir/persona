#!/usr/bin/env python3
"""
Generate one prompt file for every job role listed in README.md.

Rules:
  - Roles marked "ناظر"  -> an Audit prompt  (prompts/audit/<slug>.md)
  - Roles marked "مجری"  -> an Implementation prompt (prompts/implementation/<slug>.md)

The script also adds a "پرامپت" column to the README table and links each row
to its generated file.

Run:
    python3 scripts/generate_role_prompts.py
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"

AUDIT_DIR = ROOT / "prompts" / "audit"
IMPL_DIR = ROOT / "prompts" / "implementation"


# --------------------------------------------------------------------------- #
# Role grouping
# --------------------------------------------------------------------------- #

ROLE_GROUPS = {
    # strategy / leadership
    "founder": "strategy",
    "product-visionary": "strategy",
    "investor": "strategy",
    "board-of-directors": "strategy",
    "project-sponsor": "strategy",
    "product-manager-pm": "product",
    "product-owner-po": "product",
    "program-manager": "product",
    "scrum-master": "product",
    "agile-coach": "product",
    "product-owner-release": "product",
    "end-of-life-manager": "product",
    # project / process management
    "project-manager": "management",
    "technical-project-manager": "management",
    "pmo": "management",
    "engineering-manager": "management",
    "operations-manager": "management",
    "risk-manager": "management",
    "change-manager": "management",
    "incident-manager": "management",
    "vendor-manager": "management",
    "business-continuity-manager": "management",
    "qa-lead": "management",
    "customer-success-manager": "management",
    "account-manager": "management",
    "partnership-manager": "management",
    "product-marketing-manager": "management",
    "growth-manager": "management",
    "sales-manager": "management",
    "finance-manager": "management",
    "hr-people-manager": "management",
    "quality-manager": "management",
    # analysis / requirements
    "business-analyst-ba": "analysis",
    "domain-expert-sme": "analysis",
    "data-analyst": "analysis",
    "bi-analyst": "analysis",
    "product-analyst": "analysis",
    "ux-researcher": "analysis",
    # architecture
    "solution-architect": "architecture",
    "software-architect": "architecture",
    "enterprise-architect": "architecture",
    "system-architect": "architecture",
    "cloud-architect": "architecture",
    "data-architect": "architecture",
    "security-architect": "architecture",
    # software engineering
    "software-engineer": "engineering",
    "backend-developer": "engineering",
    "frontend-developer": "engineering",
    "full-stack-developer": "engineering",
    "mobile-developer": "engineering",
    "desktop-developer": "engineering",
    "game-developer": "engineering",
    "embedded-developer": "engineering",
    "firmware-engineer": "engineering",
    "iot-engineer": "engineering",
    "technical-lead-tech-lead": "engineering",
    "staff-engineer": "engineering",
    "principal-engineer": "engineering",
    "maintenance-engineer": "engineering",
    "refactoring-engineer": "engineering",
    "legacy-modernization-engineer": "engineering",
    "third-party-integration-specialist": "engineering",
    "migration-specialist": "engineering",
    "deployment-engineer": "engineering",
    "release-engineer": "engineering",
    "build-engineer": "engineering",
    "devrel": "engineering",
    "technical-evangelist": "engineering",
    # ai / data
    "ai-ml-engineer": "ai",
    "data-scientist": "ai",
    "data-engineer": "ai",
    "mlops-engineer": "ai",
    "prompt-engineer": "ai",
    "ai-engineer": "ai",
    "observability-engineer": "ai",
    # databases
    "database-administrator-dba": "data",
    "database-engineer": "data",
    # devops / infra
    "devops-engineer": "devops",
    "sre-site-reliability-engineer": "devops",
    "cloud-engineer": "devops",
    "infrastructure-engineer": "devops",
    "network-engineer": "devops",
    "system-administrator": "devops",
    "finops-specialist": "devops",
    "disaster-recovery-specialist": "devops",
    "backup-administrator": "devops",
    "decommission-engineer": "devops",
    # qa
    "qa-engineer": "qa",
    "test-engineer": "qa",
    "test-automation-engineer": "qa",
    "performance-engineer": "qa",
    "load-stress-tester": "qa",
    # security / privacy / legal
    "security-engineer": "security",
    "application-security-engineer": "security",
    "cybersecurity-engineer": "security",
    "penetration-tester": "security",
    "devsecops-engineer": "security",
    "privacy-engineer": "security",
    "privacy-compliance-officer": "security",
    "legal-advisor": "compliance",
    "ip-copyright-specialist": "compliance",
    "contract-manager": "compliance",
    # design
    "ui-designer": "design",
    "ux-designer": "design",
    "product-designer": "design",
    "ux-writer-content-designer": "design",
    "design-system-designer": "design",
    "graphic-designer": "design",
    "motion-designer": "design",
    "accessibility-specialist": "design",
    # content / docs
    "technical-writer": "content",
    "documentation-specialist": "content",
    "localization-specialist": "content",
    "translator": "content",
    # people / support
    "recruiter": "people",
    "technical-recruiter": "people",
    "customer-support-agent": "support",
    "technical-support-engineer": "support",
    "community-manager": "support",
    "scrum-product-team": "support",
    "ui-ux-research-participants": "support",
    "beta-tester": "support",
    "end-user": "support",
    # marketing / sales
    "marketing-specialist": "growth",
    "seo-specialist": "growth",
    "aso-specialist": "growth",
    "sales-representative": "growth",
    "business-development-manager": "growth",
    "procurement-specialist": "growth",
    # audit / assurance
    "audit-specialist": "assurance",
    "external-auditor": "assurance",
    "on-call-engineer": "ops",
}

GROUPS: dict[str, dict[str, list[str]]] = {
    "strategy": {
        "audit_focus": [
            "هم‌راستایی چشم‌انداز و تصمیم‌ها با اهداف کلان کسب‌وکار/محصول",
            "وضوح، قابل‌اندازه‌گیری و عدم تناقض در اهداف و Directionها",
            "تصمیم‌های کلان و تخصیص منابع (هزینه، سرمایه، پرسنل)",
            "مدیریت ریسک و ابهامات سطح استراتژیک",
            "پیامدهای تصمیم روی تیم، محصول، مشتری و بازار",
        ],
        "impl_checklist": [
            "تعریف Objective/Criteria قابل‌سنجش به‌همراه Non-Goals صریح",
            "تجزیه اهداف به خروجی‌ها و محدوده‌های کاری قابل اجرا",
            "شناسایی وابستگی‌ها (مالی، منابع، سازمانی، فنی)",
            "تعیین اولویت و مدل تصمیم‌گیری در شرایط عدم قطعیت",
            "تعیین نحوه اندازه‌گیری موفقیت (KPI / Success Criteria)",
        ],
    },
    "product": {
        "audit_focus": [
            "کامل و سازگار بودن Backlog و نیازمندی‌ها با Scope",
            "اولویت‌بندی بر اساس ارزش، ریسک و وابستگی‌ها",
            "وضوح Acceptance Criteria و Definition of Done برای هر Item",
            "سازگاری مسیر کاربری با هدف محصول و مدل ذهنی کاربر",
            "پوشش تدریجی (Progressive Disclosure) و کاهش اصطکاک",
        ],
        "impl_checklist": [
            "استخراج نیازمندی‌ها و User Storyها با Acceptance Criteria",
            "اولویت‌بندی با منطق Value / Risk / Effort / Dependency",
            "تعریف Definition of Done و معیارهای پذیرش قابل آزمایش",
            "تشخیص Hidden Work (validation، error handling،، integration)",
            "نگاشت نیازمندی به فاز/گام برای جلوگیری از Scope Loss",
        ],
    },
    "management": {
        "audit_focus": [
            "انطباق برنامه با زمان، منابع، ریسک و بودجه",
            "پوشش کامل Scope و عدم حذف پنهان نیازمندی‌ها",
            "شفافیت نقش‌ها، مسئولیت‌ها و نقاط تصمیم‌گیری",
            "قابلیت ردیابی خروجی‌ها و وضعیت (progress/blocker)",
            "کنترل کیفیت فرآیند و یکپارچگی بین تیم‌ها",
        ],
        "impl_checklist": [
            "تعریف WBS / فازها با وابستگی صریح و مسئول مشخص",
            "تعیین معیارهای زمان، هزینه، کیفیت و ریسک",
            "ساختار گزارش‌دهی و Update وضعیت (🔴/🟡/🟢)",
            "مدیریت تغییرات Scope و تأیید تغییرات",
            "تعریف Checkpoint و خروجی قابل تأیید برای هر مرحله",
        ],
    },
    "analysis": {
        "audit_focus": [
            "کامل و بدون ابهام بودن نیازها و مفروضات",
            "قابل آزمون بودن نیازمندی‌ها و معیارهای پذیرش",
            "سازگاری با واقعیت فنی، داده و فرآیند موجود",
            "پشتیبانی از تصمیم با شواهد (داده/مصاحبه/منطق)",
            "ردیابی هر نیاز به یک تحویل‌دادی مشخص",
        ],
        "impl_checklist": [
            "استخراج Functional / Non-functional / Data / API / UI نیازمندی‌ها",
            "تبدیل نیازها به Acceptance Criteria و Scenarioهای آزمون‌پذیر",
            "شناسایی نکات مبهم و برچسب «Unknown / Requires Verification»",
            "تعریف مرز دامنه (In/Out of Scope) برای جلوگیری از Scope Creep",
            "ارتباط نیازمندی‌ها با فازهای پیاده‌سازی و تست",
        ],
    },
    "architecture": {
        "audit_focus": [
            "انطباق معماری با نیازمندی‌ها، مقیاس و محدودیت‌ها",
            "آمادگی برای تغییر، قابلیت آزمون و نگهداشت‌پذیری",
            "سازگاری اجزا، قراردادهای بین‌سیستمی و Backward Compatibility",
            "مدیریت ریسک فنی و وابستگی‌های تکنولوژی",
            "پوشش Security / Performance / Reliability / Operability",
        ],
        "impl_checklist": [
            "تعیین مرز اجزا، مسئولیت‌ها و Contractهای بین‌آنها",
            "انتخاب/توجیه تکنولوژی با مقایسه گزینه‌ها",
            "تعریف Decision Records برای تصمیم‌های معماری",
            "مدیریت Backward Compatibility و مهاجرت تدریجی",
            "تعیین معیارهای انتهایی (NFR) و مسیر ارزیابی معماری",
        ],
    },
    "engineering": {
        "audit_focus": [
            "ادرست بودن و قابلیت نگهداشت پیاده‌سازی",
            "انطباق با معماری، قراردادها و الگوهای موجود",
            "پوشش تست، خطاها، لبه‌ها و Backward Compatibility",
            "کیفیت کد (DRY، خوانایی، تست‌پذیری، نام‌گذاری)",
            "Performance و Security در سطح پیاده‌سازی",
        ],
        "impl_checklist": [
            "تفکیک منطق دامنه از لایه‌های ورودی/خروجی/زیرساخت",
            "تعریف API/Core با Validation و Error Handling",
            "پیاده‌سازی Edge Cases و مسیرهای Failure",
            "نوشتن تست (Unit/Integration) و اجرای آنها",
            "حفظ Backward Compatibility و مهاجرت داده در صورت نیاز",
        ],
    },
    "ai": {
        "audit_focus": [
            "درستی مدل/Pipeline و کیفیت داده و فرآیند آموزش",
            "دقت، فراخوانی، قابلیت بازتولید و مدیریت Drift",
            "ارزیابی مدل در برابر معیارها/Data distribution",
            "مسائل امنیت، حریم خصوصی و کنترل مدل (Guardrails)",
            "Monitor/Deployment/Lifecycle و قابل توضیح بودن نتایج",
        ],
        "impl_checklist": [
            "تعریف ویژگی‌ها، داده (آموزش/اعتبارسنجی/تست) و Eval Metricها",
            "طراحی Pipeline (preprocess/train/evaluate/deploy)",
            "مدیریت Versioning مدل/داده و بازتولیدپذیری",
            "تعریف Monitoring، Alert و Slope/Drift",
            "در نظر گرفتن Safety، Bias، Privacy و Fallback/Mock",
        ],
    },
    "data": {
        "audit_focus": [
            "صحت Schema، Query، Index و یکپارچگی داده",
            "پوشش داده‌های لبه، تکرار و کیفیت داده",
            "Performance و مقیاس‌پذیری Query/Pipeline",
            "امنیت، Backup، Restore و کنترل دسترسی داده",
            "سازگاری با قراردادهای داده و Backward Compatibility",
        ],
        "impl_checklist": [
            "طراحی Schema/Normalization و مدیریت Migration",
            "بهینه‌سازی Query/Index با بررسی Execution Plan",
            "پیاده‌سازی Validation و Cleanup داده",
            "تعریف Backup/Restore و Disaster Recovery",
            "حفظ سازگاری بین مدل داده و Code Contracts",
        ],
    },
    "devops": {
        "audit_focus": [
            "قابل اعتماد بودن CI/CD، Deployment و Infrastructure as Code",
            "پوشش Failure، Retry و Rollback",
            "امنیت، جاسازی Secret و Least Privilege",
            "Monitor/Observability و پاسخ به Incident",
            "سازگاری با محیط‌های Dev/Test/Prod و Reversibility",
        ],
        "impl_checklist": [
            "تعریف Pipeline (build/test/deploy) با بازخورد سریع",
            "مدیریت Configuration و Secret به‌صورت ایمن",
            "طراحی Rollback، Canary و Degraded Mode",
            "تعریف Monitoring/Alerting و Runbook",
            "پیاده‌سازی حقوق دسترسی و مدل های Risk",
        ],
    },
    "qa": {
        "audit_focus": [
            "پوشش Test Cases در برابر نیازمندی‌ها",
            "پوشش لبه‌ها، خطاها و مسیرهای Failure",
            "پایداری و قابل بازتولید بودن تست‌ها",
            "پیگیری نقص‌ها و اولویت‌بندی آنها",
            "گزارش کیفیت بر اساس شواهد",
        ],
        "impl_checklist": [
            "طراحی استراتژی تست (Unit/Integration/E2E/Performance)",
            "تعریف Test Data و Fixtureها",
            "پوشش Functional/Edge/Error/Regression/Compatibility",
            "اتوماسیون و مسیر Debug در صورت شکست",
            "ارتباط Test Cases با Acceptance Criteria",
        ],
    },
    "security": {
        "audit_focus": [
            "پوشش کنترل‌های امنیتی در کل چرخه (SDLC/CI/CD)",
            "مدیریت آسیب‌پذیری‌ها، پرچم‌داربودن Findings و اولویت",
            "کنترل دسترسی، احراز هویت و داده حساس",
            "امنیت Configuration, Secret و Dependencies",
            "مدیریت Compliance/Privacy و مستندسازی شواهد",
        ],
        "impl_checklist": [
            "اجرای Threat Modeling و تعریف Trust Boundaries",
            "پیاده‌سازی Input Validation و Authorization",
            "مدیریت امن Secret/Permission و Least Privilege",
            "افزودن Security Tests و Dependency Scanners",
            "تعریف معیارهای Security Acceptance",
        ],
    },
    "compliance": {
        "audit_focus": [
            "انطباق با قوانین و مقررات و سیاست‌ها",
            "پوشش حقوقی قراردادها و مالکیت معنوی",
            "مدیریت Risk حقوقی و عدم قطعیت",
            "مستندسازی شواهد و قابلیت ردیابی تصمیم‌ها",
        ],
        "impl_checklist": [
            "شناسایی الزامات قانونی/مقرراتی اعمال‌شونده",
            "تعریف الزامات قراردادها، License و IP",
            "تضمین قابلیت ردیابی و شواهد",
            "تعریف مسیر تأیید و فرآیند برخورد با انحراف",
            "تعیین گیت کنترل قبل از Release/انتشار",
        ],
    },
    "design": {
        "audit_focus": [
            "یکپارچگی بصری با Design System موجود",
            "پوشش حالت‌ها (Default/Loading/Empty/Error/Disabled/Hover/Focus/Active)",
            "دسترس‌پذیری (Contrast، Keyboard، ARIA، Semantics)",
            "واکنش‌گرایی و رفتار در Breakpointهای مختلف",
            "کیفیت تعامل، Feedback و فاصله‌گذاری",
        ],
        "impl_checklist": [
            "استخراج Design System موجود (رنگ/تایپو/Spacing/Radius/Shadow)",
            "تعریف طراحی حالت‌ها و Responsive رفتار",
            "رعایت A11y (Contrast، Alt، Label، Focus، Keyboard)",
            "تکرارنکردن الگوها (DRY) و استفاده از Reusable Components",
            "تعریف مقیاس تایپوگرافی، spacing و سایر توکن‌ها",
        ],
    },
    "content": {
        "audit_focus": [
            "دقت، کامل بودن و قابلیت استفاده از مستندات",
            "یکدستی اصطلاحات و ساختار",
            "همسان‌سازی با محصول، نسخه و Behavior واقعی",
            "پوشش سناریوها/خطاها/مراحل راه‌اندازی",
            "کیفیت ترجمه/بومی‌سازی و دقت فنی",
        ],
        "impl_checklist": [
            "تعریف ساختار محتوایی و Style Guide",
            "طراحی ساختار مرجع/موضوع/گام‌ها و بارگذاری مثال",
            "بررسی دقت فنی و یکدستی اصطلاحات",
            "تعریف معیارهای تناسب برای مخاطب",
            "پوشش موارد API/Installation/Error/FAQ",
        ],
    },
    "people": {
        "audit_focus": [
            "انطباق فرآیند جذب/توسعه با نیازهای تیم",
            "شفافیت معیارها و رفع سوگیری",
            "تجربه کاندیدا و حفظ داده‌ها/حریم خصوصی",
            "پوشش نقش‌ها و مهارت‌های موردنیاز",
        ],
        "impl_checklist": [
            "تعریف نقش، مهارت‌ها و معیار ارزیابی",
            "طراحی فرآیند و برخورد با Edge Cases",
            "نگاشت کاندیدا به تیم و گپ مهارتی",
            "مستندسازی و حفاظت از داده شخصی",
        ],
    },
    "support": {
        "audit_focus": [
            "وضوح مسیر حل مشکل و پاسخ به کاربر",
            "پوشش مشکلات رایج، خطاها و مکانیزم دسترسی",
            "کیفیت پاسخ و زمان بازخورد",
            "بازیابی از خطا و راه ادامه‌کار",
            "جمع‌آوری Feedback و قابلیت ردیابی",
        ],
        "impl_checklist": [
            "تعریف سناریوهای کاربر/خطا و پاسخ مناسب",
            "طراحی جریان کمک، ارجاع و بسته‌شدن درخواست",
            "تعریف معیار کیفیت پاسخ و زمان پاسخ",
            "جمع‌بندی بازخورد قابل‌اندازه‌گیری",
            "طراحی مسیر پیشنهاد و بهبود تدریجی",
        ],
    },
    "growth": {
        "audit_focus": [
            "هم‌راستایی استراتژی Marketing/Sales با محصول و مخاطب",
            "قابل‌اندازه‌گیری بودن اهداف و KPIها",
            "یکدستی پیام، اصطلاحات و شناسه برند",
            "مدیریت ریسک کمپین/مذاکره و بازگشت سرمایه",
            "کیفیت کپی و قابلیت سنجش فرآیند فروش",
        ],
        "impl_checklist": [
            "تعریف Persona، Message و Value Proposition",
            "تعیین کانال‌ها، محتوا و Campaign Plan",
            "انتخاب KPI و ابزار سنجش",
            "طراحی فرآیند فروش/مذاکره/قرارداد",
            "تعریف Owner و Timebox هر فعالیت",
        ],
    },
    "assurance": {
        "audit_focus": [
            "استقلال، عینیت و پوشش کامل ممیزی",
            "مستندسازی شواهد و قابلیت ردیابی",
            "انطباق با معیارهای پذیرش و الزامات مرجع",
            "دقت باورهای استنتاج و برخورد منصفانه",
            "کیفیت خروجی و پیگیری اصلاحات",
        ],
        "impl_checklist": [
            "تهیه ماتریس Risk/Control و معیارهای پذیرش ممیزی",
            "روش نمونه‌گیری و جمع‌آوری شواهد",
            "پیاده‌سازی مسیر رستگاری کنترل و گزارش",
            "تعیین Severity/Confidence/Evidence Status",
            "نگه‌داشتن شیوه Deduplication و قابلیت تکرار گزارش",
        ],
    },
    "ops": {
        "audit_focus": [
            "سواد آمادگی/پاسخ به Incident",
            "پوشش Runbook، Alert و ابزار تشخیص ریشه‌ای",
            "مدیریت فشار کاری و ارتباط در بحران",
            "مرور Blameless و بهبود مستمر",
        ],
        "impl_checklist": [
            "تعریف تشخیص و طبقه‌بندی Incident",
            "تهیه Runbook و مراحل اسکویل",
            "تعریف خطا/بازیابی و بررسی Postmortem",
            "نگهداری ثبات Monitoring و آلرت‌ها",
        ],
    },
}

DEFAULT_GROUP = "engineering"


def group_for(slug: str) -> str:
    return ROLE_GROUPS.get(slug, DEFAULT_GROUP)


# --------------------------------------------------------------------------- #
# Markdown helpers
# --------------------------------------------------------------------------- #

def _slugify(title: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", title)
    if not words:
        return re.sub(r"\s+", "-", title).strip("-").lower()
    slug = "-".join(w.lower() for w in words)
    slug = re.sub(r"[^a-z0-9-]+", "", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


def _lines(items: list[str]) -> str:
    return "\n".join(f"- {x}" for x in items)


def _bullets_or_fallback(items: list[str] | None, fallback: list[str]) -> list[str]:
    return items if items else fallback


# --------------------------------------------------------------------------- #
# Prompt templates
# --------------------------------------------------------------------------- #

def audit_prompt(role: str, duties: str, group: str, slug: str) -> str:
    g = GROUPS.get(group, GROUPS[DEFAULT_GROUP])
    focus = g["audit_focus"]
    return f"""# سیستم پرامپت — ممیزی «{role}»

## نقش
تو به‌عنوان «{role}» و در قالب یک **ناظر مستقل و متخصص** عمل می‌کنی. وظیفه‌ی تو اجرا نیست؛ تو کیفیت، کامل‌بودن، صحت و انطباق را ارزیابی می‌کنی و بر اساس شواهد واقعی، حکم/پیشنهاد می‌دهی.

هدف نهایی: تعیین اینکه خروجی/کارِ حوزه‌ی تعریف‌شده برای این نقش، در چه سطحی است و چه مواردی نیاز به اصلاح، تأیید یا عدم تأیید دارد.

## مسئولیت‌های اصلی (بر اساس README)
- {duties}

## قانون طلایی (در تمام گام‌ها معتبر)
- هیچ نتیجه‌گیری‌ای صرفاً بر اساس حدس یا «معمولاً این‌طور است» مجاز نیست؛ هر یافته باید به یک **فایل/کامپوننت/داده/خروجی/سند مشخص** ارجاع داشته باشد.
- اگر فقط کد/سند/مدارک در دسترس است و امکان اجرا، رندر یا مشاهده‌ی واقعی خروجی وجود ندارد، این محدودیت صریحاً اعلام شود و یافته‌های وابسته را `POTENTIAL` علامت بزن، نه قطعی.
- اگر ابزار اجرا/رندر/مرورگر/تست در دسترس است، از آن برای cross-check یافته‌های Static استفاده کن؛ در غیر این صورت صرفاً بر اساس کد/مدارک کار کن و هرگز واقعیت را بدون شواهد قطعی ثبت نکن.
- هر ادعای «همه‌ی موارد بررسی شد» باید با فهرست واقعی موارد بررسی‌شده همراه باشد.
- اگر حجم کار اجازه‌ی اتمام یک گام را در یک پاسخ نمی‌دهد، پیشرفت را صریح گزارش کن و ادامه بده.
- هر گام فقط وقتی «تمام» تلقی می‌شود که معیار پذیرش آن گام برآورده شده باشد.
- اگر شواهد کافی نیست: «شواهد کافی برای اثبات این مورد وجود ندارد.» و از عبارت حدسی استفاده نکن.

## دامنه‌ی ممیزی
- {role} — {duties}

{_lines(focus)}

## روش کار (گام‌ها)
### گام ۱ — کشف و جمع‌آوری
- فهرست کامل ورودی‌ها/خروجی‌های مرتبط با این نقش را استخراج کن.
- منبع هر قطعه شواهد (فایل/مسیر/خط/خروجی) را ثبت کن.

### گام ۲ — ارزیابی هر مورد
- هر مورد را نسبت به معیارهای پذیرش، الزامات و الگوهای موجود ارزیابی کن.
- برای هر حالت مرتبط با دامنه، نتیجه را ثبت کن (در UI: Default/Loading/Empty/Error/Disabled/Focus/Hover؛ در سایر دامنه‌ها: موفق/شکست/خالی/لبه/ناسازگاری/بازگشت‌ناپذیر).

### گام ۳ — Deduplication (اجباری)
- یافته‌های با «ریشه‌ی یکسان» را به‌صورت یک **Root Finding** با فهرست `Affected` گروه‌بندی کن.
- هرگز برای هر محل تکرار، finding مستقل نساز.

### گام ۴ — گزارش نهایی
- اولویت‌بندی: مسائل breaking/انطباق‌شکن > دسترس‌پذیری/امنیت/ریسک > UX/کارایی بحرانی > DRY/Reusability > جزئیات ظاهری > موارد سلیقه‌ای.
- مرتب‌سازی: ابتدا **SEVERITY**، سپس **CONFIDENCE**، سپس **EVIDENCE_STATUS**.

## قالب هر Finding
```
ID:
SEVERITY: CRITICAL / HIGH / MEDIUM / LOW / INFO
CONFIDENCE: CONFIRMED / HIGH / MEDIUM / LOW
EVIDENCE_STATUS: VERIFIED / POTENTIAL / UNVERIFIED
CATEGORY:
TITLE:
LOCATION: file : line / component / datum
EVIDENCE:
PROBLEM:
TRIGGER / WHERE IT APPEARS:
EXPECTED vs ACTUAL:
IMPACT:
RECOMMENDED FIX:
REGRESSION RISK:
```
برای `POTENTIAL`/`UNVERIFIED` دو خط اضافه ثبت کن: `MISSING EVIDENCE` و `WHAT WOULD CONFIRM IT`.

## خروجی نهایی
1. **خلاصه اجرایی**: وضعیت کلی، مهم‌ترین ریسک‌ها، آمادگی برای ادامه/انتشار.
2. **جدول پوشش (Coverage)**: مورد | منبع | وضعیت (بررسی‌شده / رد‌شده + دلیل).
3. **یافته‌ها** با قالب بالا و پس از Deduplication.
4. **جدول Master Findings** با ستون‌های: `TITLE | LOCATION | EVIDENCE | PROBLEM | TRIGGER | EXPECTED vs ACTUAL | IMPACT | RECOMMENDED FIX | REGRESSION RISK | STATUS`؛ مقدار STATUS فقط `pending` / `partial` / `fixed`.

## معیارهای پذیرش ممیزی
- هر finding دارای SEVERITY / CONFIDENCE / EVIDENCE_STATUS جدا باشد.
- هیچ یافته‌ی تکراری (بدون Deduplication) باقی نمانده باشد.
- تمام موارد بررسی‌شده با ارجاع قابل ردیابی ثبت شده باشند.
- حکم نهایی صرفاً بر اساس یافته‌های مستند باشد.
- اگر مورد غیرقابل تأیید است، صراحتاً `UNVERIFIED` با دلیل ثبت شده باشد.
"""


def impl_prompt(role: str, duties: str, group: str, slug: str) -> str:
    g = GROUPS.get(group, GROUPS[DEFAULT_GROUP])
    checklist = g["impl_checklist"]
    return f"""# سیستم پرامپت — راهنمای پیاده‌سازی «{role}»

## نقش
تو به‌عنوان «{role}» و در قالب یک **Senior Implementation Planner / Orchestrator** عمل می‌کنی. وظیفه‌ی تو این است که یک تسک بزرگ و چندمرحله‌ای را به یک **پلن اجرایی دقیق، وابستگی‌آگاه و قابل ردیابی** تبدیل کنی تا یک agent پیاده‌ساز بتواند بدون بازتفسیر تسک، آن را فاز‌به‌فاز اجرا کند.

## مسئولیت‌های اصلی (بر اساس README)
- {duties}

## دامنه‌ی پیاده‌سازی
- {role} — {duties}

{_lines(checklist)}

## اصول طراحی پلن (الزامی)
- **قبل از پلان‌ریزی تحلیل کن**: Functional، Non-functional، Architectural، Dependencies، Data/API/UI، Security، Performance، Testing، Migration و ریسک‌ها.
- **وابستگی را مقدم بدار**: اگر B به A وابسته است، A قبل از B. اجزای مستقل را در یک فاز عملی، بدون کاهش کیفیت، گروه‌بندی کن.
- **هر فاز یک واحد کار کامل است**، نه یک دسته‌بندی: باید Cohesive، قابل اجرا در یک stage، باثبات (Stable Intermediate State) و دارای معیار پذیرش قابل سنجش باشد.
- **شکنش مصنوعی ممنوع**: تنها برای عملیات ریز، فاز جدا نساز؛ فازها باید کمترین تعدادِ منطقیِ کامل باشند.
- **Over-merge ممنوع**: کارهای پرریسک و نامرتبط (مثلاً مهاجرت دیتابیس، احراز هویت، پرداخت، بازطراحی UI، بهینه‌سازی) را در یک فاز غول‌پیکر ادغام نکن.
- **Do Not Guess**: اگر اطلاعات لازم نیست، با «Unknown / Requires Verification: ...» یا «Assumption: ...» مشخص کن؛ هرگز API/فایل/اسکیمای موجود را که نمی‌دانی اختراع نکن.
- **Hidden Work را پیدا کن**: هر نیاز اصلی ممکن است نیاز به validation، auth، error handling، schema، serialization، test، doc، integration و backward compatibility هم داشته باشد؛ این‌ها را حذف نکن.
- **No Scope Loss**: قبل از نهایی‌کردن، ممیزی Scope انجام بده؛ هر نیاز از تسک اصلی باید در جای مشخصی از پلن باشد.

## ساختار خروجی (قالب الزامی)
```markdown
# قوانین ثابت انجام پروژه
[قواعد دائمی که agent باید در همه‌ی فازها رعایت کند.]

# پلن اجرایی

## [🔴] فاز ۱: عنوان فاز
توضیح دقیق و کوتاه درباره هدف، Scope و خروجی مورد انتظار.

### [🔴] گام ۱: عنوان گام
توضیح دقیق implementation responsibility.

### [🔴] گام ۲: عنوان گام
توضیح دقیق implementation responsibility.

**معیار پذیرش:**
- ...
---
```
تا زمانی که کل Scope پوشش داده شده ادامه بده.

## سیستم وضعیت
- `🔴` — Not Implemented
- `🟡` — Partially Implemented
- `🟢` — Fully Implemented

یک فاز فقط وقتی `🟢` می‌شود که **همه‌ی گام‌ها 🟢** و **تمام معیارهای پذیرش** محقق باشند. هرگز به‌خاطر «اکثر گام‌ها کامل بود» فاز را `🟢` نزن.

## قواعد دائمی (در متن خروجی درج شود)
- هیچ الزامی را حذف نکن؛ در صورت نیاز، دلیل را صریح بنویس.
- اطلاعات ناقص را حدس نزن.
- کار ناقص را «کامل» علامت نزن.
- عملکرد موجود را حفظ کن مگر عمداً در حال تغییر آن هستی.
- هر فاز تکمیل‌شده را راستی‌آزمایی کن.
- بعد از هر مرحله، وضعیت را به‌روز کن.
- پلن را با پیاده‌سازی واقعی همگام نگه دار.
- Scope اضافه وارد نکن.
- شکنش مصنوعی و Over-merge انجام نده.
- برای پیاده‌سازی استاندارد production-quality عمل کن.
- بدون تأیید، ادعای اتمام نکن.

## معیارهای پذیرش پلن
- تمام نیازمندی‌های تسک به‌صورت ردیابی‌پذیر در فازها بازنمایی شده باشند.
- ترتیب فازها با گراف وابستگی سازگار باشد.
- هر فاز دارای معیار پذیرش قابل سنجش باشد.
- هیچ گام مبهم مثل «بهتر کردن سیستم / افزودن قابلیت لازم» وجود نداشته باشد.
- هر مرحله، وضعیت دقیقِ 🔴/🟡/🟢 و معیار Definition of Done داشته باشد.
"""


# --------------------------------------------------------------------------- #
# README rewrite
# --------------------------------------------------------------------------- #

def read_rows() -> list[dict]:
    lines = README.read_text(encoding="utf-8").splitlines()
    rows: list[dict] = []
    for ln in lines:
        s = ln.strip()
        if not s or s.startswith("#") or not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.split("|")]
        if cells and cells[0] == "":
            cells = cells[1:]
        if cells and cells[-1] == "":
            cells = cells[:-1]
        if len(cells) < 3:
            continue
        rows.append({"cells": cells, "raw": ln})
    # drop separator rows
    rows = [r for r in rows if not all(set(c) <= set("-: ") for c in r["cells"])]
    return rows


def rewrite_readme(links: dict[str, str]) -> None:
    raw = README.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    skip_sep = False
    for ln in raw:
        s = ln.strip()
        # keep title/heading and everything before table
        if s.startswith("#") or not s.startswith("|"):
            out.append(ln)
            continue
        cells = [c.strip() for c in s.split("|")]
        if cells and cells[0] == "":
            stem = [c.strip() for c in cells[1:]]
        else:
            stem = cells
        stem = [c for c in stem if c != ""]
        if all(set(c) <= set("-: ") for c in stem):
            # separator row -> add extra separator column
            out.append("|---|---|---|---|")
            continue
        if len(stem) < 3:
            out.append(ln)
            continue
        title = stem[0]
        role = stem[2] if len(stem) > 2 else ""
        link = links.get(title, "")
        if role == "نقش (مجری/ناظر)":
            out.append("| عنوان شغلی | توضیح وظایف | نقش (مجری/ناظر) | پرامپت |")
        else:
            out.append(f"| {stem[0]} | {stem[1]} | {role} | {link} |")
    README.write_text("\n".join(out) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def main() -> None:
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    IMPL_DIR.mkdir(parents=True, exist_ok=True)

    rows = read_rows()
    data_rows = [r for r in rows if r["cells"][0] != "عنوان شغلی"]
    print(f"Role rows found: {len(data_rows)}")

    links: dict[str, str] = {}

    for r in data_rows:
        cells = r["cells"]
        title = cells[0]
        duties = cells[1]
        role_type = cells[2]
        slug = _slugify(title)
        group = group_for(slug)

        if role_type == "ناظر":
            relative = f"prompts/audit/{slug}.md"
            path = ROOT / relative
            path.write_text(audit_prompt(title, duties, group, slug), encoding="utf-8")
            label = "Audit"
        else:
            relative = f"prompts/implementation/{slug}.md"
            path = ROOT / relative
            path.write_text(impl_prompt(title, duties, group, slug), encoding="utf-8")
            label = "Implementation"

        links[title] = f"[{label}]({relative})"

    rewrite_readme(links)

    audit_count = sum(1 for _ in AUDIT_DIR.glob("*.md"))
    impl_count = sum(1 for _ in IMPL_DIR.glob("*.md"))
    print(f"Audit prompts:     {audit_count}")
    print(f"Implementation:    {impl_count}")
    print("README updated with پرامپت column.")


if __name__ == "__main__":
    main()
