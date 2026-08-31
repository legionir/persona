#!/usr/bin/env python3
"""Normalize the 23-column details table embedded in README.md.

The details table (previously a separate details.md file) now lives inside
README.md as its own 23-column table; this script normalizes it in place.

Changes:
1. Rebuilds the table with leading/trailing pipes + header separator row.
2. Harmonizes the "SRE" title with README's "SRE (Site Reliability Engineer)".
3. Applies a controlled vocabulary to the tooling / permissions / lifecycle /
   restricted-tools columns and normalizes list separators everywhere.

Run:
    python3 scripts/normalize_details.py
"""

from __future__ import annotations

import re
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"

N_COLS = 23

# ---------------------------------------------------------------------------
# Title harmonization
# ---------------------------------------------------------------------------

TITLE_ALIASES = {
    "SRE": "SRE (Site Reliability Engineer)",
}


def readme_title_of(title: str) -> str | None:
    """Return the canonical README title for a details row title."""
    for ln in README.read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.split("|")]
        if cells and cells[0] == "":
            cells = cells[1:]
        if cells and cells[-1] == "":
            cells = cells[:-1]
        if len(cells) >= 4:
            cell_title = cells[0]
            if cell_title == title:
                return cell_title
    return None


# ---------------------------------------------------------------------------
# Allowed tools — canonical vocabulary
# ---------------------------------------------------------------------------

TOOL_ALIASES = {
    # documentation / reporting
    "Docs": "Documentation",
    "Docs Tools": "Documentation Tools",
    "Documentation Tools": "Documentation Tools",
    "Docs, Git": "Documentation, Git",
    "Documentation, Diagramming": "Documentation, Diagramming",
    "Documentation, Diagramming Tools": "Documentation, Diagramming",
    # IDE / code
    "IDE, Git, Diagram Tools": "IDE, Git, Diagram Tools",
    "IDE, Git, Terminal, Tests": "IDE, Git, Terminal, Tests",
    "IDE, Git, DB Tools": "IDE, Git, DB Tools",
    "IDE, Git, DB, Terminal": "IDE, Git, DB, Terminal",
    "IDE, SDK, Emulator": "IDE, SDK, Emulator",
    "IDE, Build Tools": "IDE, Build Tools",
    "IDE, Debugger, Serial Tools": "IDE, Debugger, Serial Tools",
    "IDE, Git, CI/CD": "IDE, Git, CI/CD",
    "IDE, Git, Profilers": "IDE, Git, Profilers",
    "IDE, API Tools, Git": "IDE, API Tools, Git",
    "IDE, MQTT Tools, Cloud Tools": "IDE, MQTT Tools, Cloud Tools",
    "Git, IDE, CI/CD": "IDE, Git, CI/CD",
    "Git, CI/CD, Containers, Cloud": "Git, CI/CD, Containers, Cloud",
    "Git, CI/CD, PM Tools": "Git, CI/CD, Project Management Tools",
    "CI/CD, Git": "CI/CD, Git",
    "Build Tools, CI": "Build Tools, CI",
    "Migration Tools, Git, DB": "Migration Tools, Git, DB",
    "Migration Tools, DB": "Migration Tools, DB",
    "Automation Frameworks, CI": "Automation Frameworks, CI",
    "Agile Tools, Git, CI": "Agile Tools, Git, CI",
    "Test Tools, CI": "Test Tools, CI",
    "Security Tools, Git": "Security Tools, Git",
    "CI/CD, Security Scanners": "CI/CD, Security Scanners",
    "CI/CD, Containers, Monitoring": "CI/CD, Containers, Monitoring",
    "CI/CD, Cloud, Monitoring": "CI/CD, Cloud, Monitoring",
    "CI/CD, Security Tools": "CI/CD, Security Scanners",
    "CI/CD, Monitoring": "CI/CD, Monitoring",
    "CI/CD": "CI/CD",
    "CI/CD, Git": "CI/CD, Git",
    "CI": "CI/CD",
    "CD": "CI/CD",
    # project / pm
    "PM Tools, Reports": "Project Management Tools, Reports",
    "PM Tools, Audit Tools": "Project Management Tools, Audit Tools",
    "PM, HR Tools": "Project Management, HR Tools",
    "PM, Analytics": "Project Management, Analytics",
    "Project Management, Documentation": "Project Management, Documentation",
    "Project Management Tools": "Project Management Tools",
    "Portfolio Tools": "Portfolio Tools",
    "Scrum Tools": "Scrum Tools",
    "Analytics, Roadmap Tools": "Analytics, Roadmap Tools",
    "Analytics, Workshop Tools": "Analytics, Workshop Tools",
    "Analytics, Backlog Tools": "Analytics, Backlog Tools",
    "Analytics, Experiment Tools": "Analytics, Experiment Tools",
    # architecture
    "Architecture Tools": "Architecture Tools",
    "Architecture Tools, Documentation": "Architecture Tools, Documentation",
    "Architecture Repository": "Architecture Repository",
    "Architecture/Analytics": "Architecture Tools, Analytics",
    "Architecture/Cost Tools": "Architecture Tools, Cost Tools",
    "Modeling Tools": "Modeling Tools",
    "Modeling, Security Tools": "Modeling Tools, Security Tools",
    # design
    "Design Tools": "Design Tools",
    "UX Tools": "Design Tools",
    "Motion Tools": "Design Tools",
    "Research Tools": "Research Tools",
    "Accessibility Tools": "Accessibility Tools",
    # data / db
    "DB Tools, Monitoring": "DB Tools, Monitoring",
    "SQL, DB Tools": "SQL, DB Tools",
    "SQL, BI, Analytics": "SQL, BI, Analytics",
    "SQL, Python, Pipeline Tools": "SQL, Python, Pipeline Tools",
    "Data Mapping, Audit Tools": "Data Mapping, Audit Tools",
    "Analytics, SQL": "Analytics, SQL",
    "BI Tools, SQL": "BI Tools, SQL",
    "Analytics": "Analytics",
    # ai / ml
    "Python, ML Frameworks": "Python, ML Frameworks",
    "Python, Notebooks, Statistics": "Python, Notebooks, Statistics",
    "LLM Tools, Evaluation": "LLM Tools, Evaluation",
    "LLM, Vector DB, IDE, Git": "LLM, Vector DB, IDE, Git",
    # security
    "SAST, DAST, SCA, Code Analysis": "SAST, DAST, SCA, Code Analysis",
    "SIEM, Security Tools": "SIEM, Security Tools",
    "Approved Pentest Tools": "Approved Pentest Tools",
    "Security Tools, Analysis": "Security Tools, Analysis",
    # infra
    "Terminal, Monitoring, IaC": "Terminal, Monitoring, Infrastructure as Code",
    "Terminal, Monitoring": "Terminal, Monitoring",
    "Cloud CLI, IaC": "Cloud CLI, Infrastructure as Code",
    "Infrastructure, Cloud, DB, Monitoring": "Infrastructure, Cloud, DB, Monitoring",
    "Network Tools": "Network Tools",
    "Ops Tools, Monitoring": "Ops Tools, Monitoring",
    "Observability Tools": "Observability Tools",
    "Monitoring, Logs, Terminal": "Monitoring, Logs, Terminal",
    # qa
    "Test Tools": "Test Tools",
    "Test Management Tools": "Test Management Tools",
    "Profilers, Load Tools": "Profilers, Load Tools",
    "Load Testing Tools": "Load Testing Tools",
    "QA/Audit Tools": "QA/Audit Tools",
    "Test Interface": "Test Interface",
    "Testing Interface": "Test Interface",
    "Beta Tools": "Beta Tools",
    # support / people
    "Support Tools, Knowledge Base": "Support Tools, Knowledge Base",
    "Logs, Terminal, Diagnostics": "Logs, Terminal, Diagnostics",
    "Community Tools": "Community Tools",
    "CRM, Analytics": "CRM, Analytics",
    "CRM, Communication": "CRM, Communication",
    "CRM, Research": "CRM, Research",
    "CRM, Project Tools": "CRM, Project Management Tools",
    "Recruitment Tools": "Recruitment Tools",
    "ATS, Technical Tests": "ATS, Technical Tests",
    "HR Tools": "HR Tools",
    "Procurement Tools": "Procurement Tools",
    "Contract Tools": "Contract Tools",
    # growth/marketing
    "Marketing Tools": "Marketing Tools",
    "SEO Tools, Analytics": "SEO Tools, Analytics",
    "ASO Tools": "ASO Tools",
    "CRM": "CRM",
    "Presentation, Demo Tools": "Presentation, Demo Tools",
    "Docs, Community Tools": "Documentation, Community Tools",
    # finance/ops
    "Financial Reports": "Financial Reports",
    "Financial Tools": "Financial Tools",
    "Billing/Analytics": "Billing, Analytics",
    "Risk Tools": "Risk Tools",
    "Risk/Planning Tools": "Risk Tools, Planning Tools",
    "Vendor/Contract Tools": "Vendor, Contract Tools",
    "Business Intelligence, Reports": "Business Intelligence, Reports",
    "BI, Reports": "Business Intelligence, Reports",
    "Legal Research": "Legal Research",
    "License Tools": "License Tools",
    "Incident Tools, Monitoring": "Incident Tools, Monitoring",
    "Backup, DR Tools": "Backup, DR Tools",
    "Backup Tools": "Backup Tools",
    "Research, Analytics": "Research, Analytics",
    "Domain References": "Domain References",
    "Product Interface": "Product Interface",
}

TOOL_NOUN_ALIASES = {
    "Docs": "Documentation",
    "IaC": "Infrastructure as Code",
    "PM": "Project Management",
    "BI": "Business Intelligence",
}


def normalize_tools(value: str) -> str:
    # NOTE: do NOT split on '/' so tokens like CI/CD and AI/ML stay intact.
    parts = [p.strip() for p in re.split(r"[,،、]", value)]
    parts = [p for p in parts if p]
    out = []
    for p in parts:
        canonical = TOOL_ALIASES.get(p)
        if canonical:
            # canonical might itself be a list
            out.extend([x.strip() for x in re.split(r",", canonical) if x.strip()])
        else:
            p2 = p
            for k, v in TOOL_NOUN_ALIASES.items():
                if p2 == k or re.fullmatch(re.escape(k) + r".*", p2):
                    p2 = v + p2[len(k):]
            out.append(p2)
    # drop duplicates preserving order
    seen = OrderedDict.fromkeys(out)
    return ", ".join(seen)


# ---------------------------------------------------------------------------
# Restricted / Forbidden tools — controlled vocabulary
# ---------------------------------------------------------------------------

RESTRICTED_CANON = OrderedDict([
    ("production-secrets", "Production (no credentials/secrets exposure)"),
    ("production-data", "Production (no data access/export without authorization)"),
    ("production-destructive", "Production (no destructive change without approval)"),
    ("production-no-approval", "Production (no unapproved change)"),
    ("production-cred", "Production (no credentials/secrets)"),
    ("production-hardware", "Production (no direct hardware changes)"),
    ("production-direct-write", "Production (no direct write)"),
    ("production-read", "Production (read-only)"),
    ("destructive-ops", "Destructive operations (no approval)"),
    ("destructive-commands", "Destructive commands (no approval)"),
    ("unauth-data", "Unauthorized data access"),
    ("out-of-scope", "Out-of-scope targets"),
    ("bypass-gates", "Security gates (no bypass)"),
    ("evidence-alter", "Audit evidence (no modification)"),
    ("scope-tool", "Approved tools only (read-only scope)"),
    ("admin-destructive", "Admin/destructive actions (no approval)"),
])


def _classify_restricted(value: str) -> str:
    v = value.lower()
    if "secret" in v or "credential" in v:
        return "production-secrets"
    if "data access" in v or "data mutation" in v or "user data" in v or "data without" in v or "data modification" in v or "exploitation" in v or "unauthorized data" in v or "unauthorized user" in v:
        return "production-data"
    if "destructive production" in v or "production destructive" in v or "destructive tests" in v or "production tests" in v:
        return "production-destructive"
    if "flash operations" in v or "destructive commands" in v or "destructive actions" in v or "destructive operations" in v or "unsafe flash" in v:
        return "destructive-ops"
    if "destructive" in v:
        return "destructive-ops"
    if "bypass security" in v or "bypass" in v:
        return "bypass-gates"
    if "out-of-scope" in v or "out of scope" in v or "unsafe production" in v:
        return "out-of-scope"
    if "evidence" in v or "audited evidence" in v:
        return "evidence-alter"
    if "unauthorized production" in v or "unapproved production" in v or "unapproved changes" in v or "unapproved destructive" in v or "manual unapproved" in v or "direct unapproved" in v:
        return "production-no-approval"
    if "production credentials" in v or "production secrets" in v:
        return "production-secrets"
    if "production hardware" in v:
        return "production-hardware"
    if "admin" in v or "infrastructure" in v:
        return "admin-destructive"
    # fall back to production-level restriction family
    return "production-direct-write"


def normalize_restricted(value: str) -> str:
    # some cells are conceptual (e.g. one restriction) but may be comma lists
    parts = [p.strip() for p in re.split(r"[،、/]", value)]
    parts = [p for p in parts if p]
    keys = [_classify_restricted(p) for p in parts]
    # dedupe preserving order
    seen = []
    for k in keys:
        if k not in seen:
            seen.append(k)
    result = [RESTRICTED_CANON[k] for k in seen]
    return ", ".join(result)


# ---------------------------------------------------------------------------
# Permissions — controlled vocabulary
# ---------------------------------------------------------------------------

PERM_ALIASES = {
    # generic access levels
    "Strategic": "Strategic",
    "Program": "Program",
    "Management": "Management",
    "Governance": "Governance",
    "Advisory": "Advisory",
    "Project": "Project",
    "Process": "Process",
    "Product": "Product",
    "Business": "Business",
    "Financial": "Financial",
    "Financial/Cloud": "Finance & Cloud",
    # code / repo
    "Repository": "Repository",
    "Backend Repository": "Repository (Backend)",
    "Frontend Repository": "Repository (Frontend)",
    "Mobile Repository": "Repository (Mobile)",
    "Test Repository": "Repository (Test)",
    "Security/Test": "Security & Test",
    "Test/Performance": "Test & Performance",
    "Design Workspace": "Design Workspace",
    # design / content
    "Design": "Design",
    "Design Workspace": "Design",
    "Content": "Content",
    "Documentation": "Documentation",
    "Research": "Research",
    "Analytics": "Analytics",
    "BI": "Business Intelligence",
    # data / AI
    "Data Workspace": "Data",
    "Data Platform": "Data",
    "Database": "Database",
    "AI Environment": "AI/ML",
    "ML Environment": "AI/ML",
    "ML Infrastructure": "AI/ML (Infra)",
    # infra / ops
    "Infrastructure": "Infrastructure",
    "Cloud": "Cloud",
    "Network": "Network",
    "Server": "Server",
    "Production Monitoring": "Observability",
    "Production": "Production",
    "Operations": "Operations",
    "Incident Management": "Incident",
    "CI/CD": "CI/CD",
    "Release": "Release",
    "System": "System",
    "Device": "Device",
    "IoT": "IoT",
    "Integration": "Integration",
    # quality / security
    "QA": "QA",
    "Test": "Test",
    "Test Environment": "Test",
    "Security": "Security",
    "Security Architecture": "Security",
    # people / support
    "Recruitment": "Recruitment",
    "HR": "HR",
    "Team": "Team",
    "Support": "Support",
    "CRM": "CRM",
    "Community": "Community",
    "Marketing": "Marketing",
    "Store": "Store",
    "Website": "Website",
    "Procurement": "Procurement",
    "Commercial": "Commercial",
    "User": "User",
    "Beta": "Beta",
    "Limited": "Limited",
    # restricted variants
    "Restricted": "Restricted",
    "Restricted Production": "Restricted",
    "Production Restricted": "Restricted",
    "Restricted Data": "Restricted",
    "Restricted/Destructive": "Restricted",
    "Read-only": "Read-only",
    "Read-heavy": "Read-only",
}


def normalize_permissions(value: str) -> str:
    # NOTE: do NOT split on '/' so tokens like CI/CD and Security/Test stay intact.
    parts = [p.strip() for p in re.split(r"[،、]", value)]
    parts = [p for p in parts if p]
    out = []
    for p in parts:
        p = p.strip()
        if p in ("Advisory", "Restricted", "Read-only"):
            out.append(PERM_ALIASES.get(p, p))
            continue
        out.append(PERM_ALIASES.get(p, p))
    seen = list(OrderedDict.fromkeys(out))
    return ", ".join(seen)


# ---------------------------------------------------------------------------
# Lifecycle — controlled vocabulary per state token
# ---------------------------------------------------------------------------

LIFECYCLE_ALIASES = {
    # planning / creation
    "Planning": "Planning", "Draft": "Draft", "Discovery": "Discovery",
    "Analysis": "Analysis", "Assessment": "Assessment", "Prospecting": "Prospecting",
    "Sourcing": "Sourcing", "Requested": "Requested", "Hypothesis": "Hypothesis",
    "Assigned": "Assigned", "Approved": "Approved", "Ready": "Ready",
    "Active": "Active", "Running": "Running", "Live": "Live", "Auditing": "Auditing",
    "Monitoring": "Monitoring", "Maintenance": "Maintenance", "Incident": "Incident",
    "Open": "Open", "Investigating": "Investigating", "Blocked": "Blocked",
    "At Risk": "At Risk", "Review": "Review", "Retest": "Retest",
    "Testing": "Testing", "Test": "Testing", "Evaluation": "Evaluation",
    "Execution": "Execution", "Executing": "Executing", "Implement": "Implement",
    "Implementing": "Implementing", "Implementation": "Implementing",
    "Development": "Development", "Development,": "Development", "Fixing": "Fixing",
    "Verification": "Verification", "Verified": "Verified", "Sign-off": "Sign-off",
    "Passed": "Passed", "Failed": "Failed", "Screening": "Screening",
    "Sprint": "Sprint", "Backlog": "Backlog", "Training": "Training",
    "Building": "Building", "Deploy": "Deploying", "Deploying": "Deploying",
    "Preparation": "Preparing", "Preparing": "Preparing", "Released": "Released",
    "Published": "Published", "Approved": "Approved", "Completed": "Completed",
    "Done": "Completed", "Closed": "Closed", "Cancelled": "Cancelled",
    "Paused": "Paused", "Suspended": "Suspended", "Withdrawn": "Withdrawn",
    "Terminated": "Terminated", "Deprecated": "Deprecated", "Retired": "Retired",
    "Retiring": "Retiring", "Renewed": "Renewed", "Expired": "Expired",
    "Resolved": "Resolved", "Mitigated": "Mitigated", "Recovery": "Recovery",
    "Rolled Back": "Rolled Back", "Rollback": "Rolled Back", "Ready": "Ready",
    "Optimization": "Optimization", "Refactoring": "Refactoring",
    "Migration": "Migration", "Cutover": "Cutover", "Validation": "Validation",
    "Instrumenting": "Instrumenting", "Reporting": "Reporting", "Audit": "Auditing",
    "Optimize": "Optimization", "Playtest": "Playtest", "Flashing": "Flashing",
    "Patch": "Patch", "Patch,": "Patch", "On-call": "On-call", "Oncall": "On-call",
    "Busy": "Busy", "Available": "Available", "Negotiation": "Negotiation",
    "Recruit": "Recruitment", "Launching": "Launch", "Launch": "Launch",
    "Coaching": "Coaching", "Assessment,": "Assessment", "Retest": "Retest",
    "Signoff": "Sign-off", "Sign-off,": "Sign-off",
}

# tokens that just become themselves (pass-through) are already in alias set;
# ANY token not listed gets title-normalized as a noun.
PROPER_NOUNS = {
    "Active", "Planning", "Draft", "Review", "Approved", "Ready", "Blocked",
    "Paused", "Cancelled", "Completed", "Closed", "At Risk", "Suspended",
    "Withdrawn", "Terated", "Deprecated", "Expired", "Renewed", "Resolved",
    "Mitigated", "Rolled Back", "Retired", "Retiring", "Recovery", "Live",
    "Open", "Investigating", "Running", "Failed", "Passed", "Done", "Monitoring",
    "Maintenance", "Incident", "Auditing", "Testing", "Development", "Deploying",
    "Released", "Published", "Screening", "Assessment", "Analysis", "Discovery",
    "Prospecting", "Sourcing", "Requested", "Hypothesis", "Negotiation",
    "Onboarding", "At Risk", "Capacity", "Optimization", "Refactoring",
    "Migration", "Cutover", "Validation", "Instrumenting", "Reporting",
    "Evaluation", "Training", "Building", "Preparing", "Verified", "Verification",
}


def _norm_state_token(tok: str) -> str:
    tok = tok.strip()
    if tok in LIFECYCLE_ALIASES and LIFECYCLE_ALIASES[tok] != tok:
        return LIFECYCLE_ALIASES[tok]
    if tok in (set(LIFECYCLE_ALIASES) - {"Development,", "Patch,", "Assessment,", "Sign-off,"}):
        return LIFECYCLE_ALIASES[tok]
    return tok


def normalize_lifecycle(value: str) -> str:
    # normalize separators and stray full-stop / comma fragments
    value = value.replace("、", ",").replace("،", ",")
    tokens = [t.strip() for t in value.split(",")]
    tokens = [t for t in tokens if t]
    out = []
    for t in tokens:
        t = t.strip()
        norm = _norm_state_token(t)
        if norm and norm not in out:
            out.append(norm)
    # Pass-through single tokens if no alias matched
    if not out:
        return value
    return ", ".join(out)


# ---------------------------------------------------------------------------
# Generic cell normalization
# ---------------------------------------------------------------------------

def normalize_list_separator(value: str) -> str:
    """Normalize Persian/Chinese separators to ASCII commas + space."""
    value = value.replace("،", ", ").replace("、", ", ").replace("،", ", ")
    value = re.sub(r"\s*,\s*", ", ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def clean(value: str) -> str:
    value = value.strip()
    value = re.sub(r"\s+", " ", value)
    return value


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

HEADER = (
    "عنوان شغلی| توضیح وظایف| نقش| مأموریت اصلی (Mission)| مسئولیت‌ها (Responsibilities)| "
    "محدوده اختیار (Scope)| ورودی‌های الزامی (Required Inputs)| ورودی‌های اختیاری (Optional Inputs)| "
    "Context موردنیاز| پیش‌شرط‌ها (Preconditions)| گام‌های اجرایی (Procedure)| "
    "تصمیم‌ها و قوانین (Decision Rules)| ابزارهای مجاز (Allowed Tools)| "
    "ابزارهای ممنوع/محدود (Restricted/Forbidden Tools)| خروجی‌ها (Outputs)| "
    "معیار پذیرش خروجی (Quality Gate)| شواهد موردنیاز (Evidence)| تحویل به (Handoff)| "
    "شرایط Escalation| سطح دسترسی (Permissions)| وضعیت‌های Lifecycle| "
    "حافظه موردنیاز (Memory)| KPI / معیار عملکرد"
)


HEADER_CELLS = [c.strip() for c in HEADER.split("|")]


def _cells(s: str) -> list[str]:
    s = s.strip()
    if not s.startswith("|"):
        return []
    cells = [c.strip() for c in s.strip("|").split("|")]
    if cells and cells[0] == "":
        cells = cells[1:]
    if cells and cells[-1] == "":
        cells = cells[:-1]
    return cells


def parse_rows() -> list[list[str]]:
    rows: list[list[str]] = []
    for ln in README.read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if not s.startswith("|"):
            continue
        cells = _cells(s)
        # strip markdown header + any separator row
        if cells == HEADER_CELLS:
            continue
        if all(re.fullmatch(r":?-{2,}:?", c) or c in ("---", "--") for c in cells):
            continue
        if len(cells) == N_COLS:
            rows.append(cells)
        # rows with a different column count belong to other README tables
    return rows


def transform(row: list[str]) -> list[str]:
    r = [clean(x) for x in row]

    # 1. harmonize title with README
    title = r[0]
    for alias, canonical in TITLE_ALIASES.items():
        if title == alias:
            title = canonical
    readme_title = readme_title_of(title)
    if readme_title and title != readme_title:
        title = readme_title
    r[0] = title

    # 2. tooling / lifecycle / permissions / restricted controlled vocab
    r[12] = normalize_tools(r[12])
    r[13] = normalize_restricted(r[13])
    r[19] = normalize_permissions(r[19])
    r[20] = normalize_lifecycle(r[20])

    # 3. normal list separators on remaining mostly-list cells
    for idx in (4, 5, 6, 7, 8, 14, 17, 18, 22):
        r[idx] = normalize_list_separator(r[idx])

    # 4. remove whitespace-only duplicates artifacts
    r[12] = normalize_list_separator(r[12])
    r[13] = normalize_list_separator(r[13])
    r[19] = normalize_list_separator(r[19])
    r[20] = normalize_list_separator(r[20])
    return r


def esc(value: str) -> str:
    # escape pipes just in case, preserve RTL text
    return value.replace("|", "\\|")


def main() -> None:
    rows = parse_rows()
    print(f"Parsed rows: {len(rows)}")
    transformed = [transform(r) for r in rows]

    table: list[str] = []
    table.append("| " + " | ".join(esc(c) for c in HEADER_CELLS) + " |")
    table.append("|" + "---|" * N_COLS)
    for r in transformed:
        table.append("| " + " | ".join(esc(c) for c in r) + " |")

    # Replace the 23-column details table inside README.md in-place.
    lines = README.read_text(encoding="utf-8").splitlines()
    start = next(i for i, ln in enumerate(lines) if _cells(ln) == HEADER_CELLS)
    end = start + 1
    while end < len(lines) and lines[end].strip().startswith("|"):
        end += 1
    README.write_text("\n".join(lines[:start] + table + lines[end:]) + "\n", encoding="utf-8")
    print(f"Wrote {len(table)} lines into README.md")

    # verify roundtrip
    re_rows = parse_rows()
    print(f"Round-trip data rows: {len(re_rows)}")
    print("SRE title row:", next(r[0] for r in re_rows if "SRE" in r[0]))


if __name__ == "__main__":
    main()
