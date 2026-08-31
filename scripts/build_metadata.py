#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate personas.json — machine-readable metadata (API-ready) for all personas.

The file is the data source for index.html (persona finder) and can be consumed
as a static API. It contains basic search/categorization info for every role:
id, role_id, type, domain/category/seniority, mission, duties, supervisors,
consumers, capabilities, file path and keyword facets.

Usage:
    python3 scripts/build_metadata.py
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from generate_personas import (  # noqa: E402
    ROOT, README, SPECS, GROUP_OF, GROUP_SPEC,
    TYPE_CAPS, CAPS_BY_GROUP, STEP_CAP, _step_kind,
    _slug, _steps, read_rows, load_details, spec_for,
    build_supervisor_map, load_master_registry, seniority_of,
    GROUP_DOMAIN, GROUP_CATEGORY,
)
from role_extras import SLUG_OVERRIDES  # noqa: E402

OUT = ROOT / "personas.json"

# ---------------------------------------------------------------------------
# Persian display labels
# ---------------------------------------------------------------------------
TYPE_LABEL_FA = {"SUPERVISOR": "ناظر", "EXECUTOR": "مجری"}

DOMAIN_LABEL_FA = {
    "Business": "کسب‌وکار", "Product": "محصول", "Project": "پروژه",
    "Analytics": "تحلیل", "Architecture": "معماری", "Software": "نرم‌افزار",
    "AI": "هوش مصنوعی", "Data": "داده", "DevOps": "DevOps", "Testing": "تست و کیفیت",
    "Security": "امنیت", "Compliance": "انطباق", "Design": "طراحی",
    "Documentation": "مستندسازی", "HR": "منابع انسانی", "Support": "پشتیبانی",
    "Growth": "رشد و بازاریابی", "Audit": "ممیزی", "Operations": "عملیات",
}

CATEGORY_LABEL_FA = {
    "Strategy": "استراتژی", "Management": "مدیریت", "Analysis": "تحلیل",
    "Architecture": "معماری", "Engineering": "مهندسی", "Data": "داده",
    "Infrastructure": "زیرساخت", "Testing": "تست", "Security": "امنیت",
    "Compliance": "انطباق", "Design": "طراحی", "Documentation": "مستندسازی",
    "Commercial": "تجاری", "Support": "پشتیبانی", "Operations": "عملیات",
    "Audit": "ممیزی",
}

SENIORITY_LABEL_FA = {
    "Junior": "جونیور", "Mid": "میانی", "Senior": "سینیور", "Staff": "Staff",
    "Principal": "Principal", "Lead": "Lead", "Manager": "مدیر",
    "Director": "مدیر ارشد", "Executive": "اجرایی", "Expert": "متخصص",
    "Specialist": "متخصص",
}


def group_label(group: str) -> str:
    spec = GROUP_SPEC.get(group)
    return spec[0] if spec else group


def capabilities_of(role_type: str, group: str, procedure: str) -> list[str]:
    caps = list(TYPE_CAPS[role_type])
    caps += CAPS_BY_GROUP.get(group, [])
    for step in _steps(procedure):
        caps += STEP_CAP.get(_step_kind(step), [])
    seen, out = set(), []
    for c in caps:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


def keywords_of(title: str, duties: str, mission: str) -> list[str]:
    raw = f"{title} {duties} {mission} {_slug(title)}"
    raw = raw.replace("\u200c", " ")
    tokens = re.split(r"[\s،,؛;/()\-–—|]+", raw)
    words = []
    seen = set()
    for tk in tokens:
        tk = tk.strip()
        if not tk:
            continue
        low = tk.lower()
        if low not in seen:
            seen.add(low)
            words.append(low)
    return words[:60]


def main() -> None:
    rows = read_rows()
    data_rows = [r for r in rows[1:]]
    details = load_details()
    _ms, _me = load_master_registry()
    sup_titles = {r[0] for r in data_rows if r[2] == "ناظر"}
    sup_map = build_supervisor_map(sup_titles)
    by_supervisor: dict[str, list[str]] = {}
    for exe_title, sups in sup_map.items():
        for s in sups:
            by_supervisor.setdefault(s, []).append(exe_title)

    roles = []
    sup_i = exe_i = 0
    for title, _duty, role_type in [(r[0], r[1], r[2]) for r in data_rows]:
        slug = SLUG_OVERRIDES.get(title, _slug(title))
        ptype = "SUPERVISOR" if role_type == "ناظر" else "EXECUTOR"
        spec = spec_for(slug)
        group = spec["domain"]
        persona = details.get(title, {})
        mission = persona.get("mission") or spec["mission"]
        duties = persona.get("duties") or _duty
        procedure = persona.get("procedure", "")
        if ptype == "SUPERVISOR":
            sup_i += 1
            role_id = f"SUP-{sup_i:03d}"
            supervisors, consumers = [], sorted(by_supervisor.get(title, []))
        else:
            exe_i += 1
            role_id = f"EXE-{exe_i:03d}"
            supervisors = sup_map.get(title, [])
            consumers = []
        domain = GROUP_DOMAIN.get(group, "Software")
        category = GROUP_CATEGORY.get(group, "Engineering")
        seniority = seniority_of(title)
        folder = "audit" if ptype == "SUPERVISOR" else "implementation"
        roles.append({
            "id": slug,
            "roleId": role_id,
            "title": title,
            "type": ptype,
            "typeLabel": TYPE_LABEL_FA[ptype],
            "group": group,
            "groupLabel": group_label(group),
            "domain": domain,
            "domainLabel": DOMAIN_LABEL_FA.get(domain, domain),
            "category": category,
            "categoryLabel": CATEGORY_LABEL_FA.get(category, category),
            "seniority": seniority,
            "seniorityLabel": SENIORITY_LABEL_FA.get(seniority, seniority),
            "mission": mission,
            "duties": duties,
            "supervisors": supervisors,
            "consumers": consumers,
            "capabilities": capabilities_of(ptype, group, procedure),
            "path": f"prompts/{folder}/{slug}.md",
            "file": f"{slug}.md",
            "keywords": keywords_of(title, duties, mission),
        })

    facets = {
        "types": [{"id": "SUPERVISOR", "label": "ناظر"},
                  {"id": "EXECUTOR", "label": "مجری"}],
        "groups": sorted({(r["group"], r["groupLabel"]) for r in roles}),
        "domains": sorted({(r["domain"], r["domainLabel"]) for r in roles}),
        "categories": sorted({(r["category"], r["categoryLabel"]) for r in roles}),
        "seniorities": sorted({(r["seniority"], r["seniorityLabel"]) for r in roles}),
    }

    doc = {
        "$schema": "personas-metadata/v1",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": {
            "schema": "Master Persona Schema & Generator Prompt.md",
            "readme": "README.md",
            "details": "details.md",
            "generator": "scripts/generate_personas.py",
            "metadata_builder": "scripts/build_metadata.py",
        },
        "totals": {
            "roles": len(roles),
            "supervisors": sum(1 for r in roles if r["type"] == "SUPERVISOR"),
            "executors": sum(1 for r in roles if r["type"] == "EXECUTOR"),
        },
        "facets": facets,
        "roles": roles,
    }
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"personas.json written: {len(roles)} roles "
          f"({doc['totals']['supervisors']} supervisors, {doc['totals']['executors']} executors)")
    print(f"size: {OUT.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
