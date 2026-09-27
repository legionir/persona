#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate personas.json — machine-readable metadata (API-ready) for all personas.

The file is the data source for index.html (persona finder) and can be consumed
as a static API. It contains basic search/categorization info for every role:
id, role_id, type, domain/category/seniority, mission, duties, supervisors,
consumers, capabilities, file path and keyword facets.

It also carries a `composites` array with the 19 composite master prompts from
`prompts/composite/`, so a consumer of this one file sees the whole library
instead of only the 170 roles. A composite has no group / domain / seniority —
it runs several roles at once — so those fields are null by design.

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
from persona_lib import (  # noqa: E402
    COMPOSITES, MASTERS, MasterPersona, clip, master_description,
    master_personas,
)
from role_extras import SLUG_OVERRIDES  # noqa: E402

OUT = ROOT / "personas.json"

# ---------------------------------------------------------------------------
# Persian display labels
# ---------------------------------------------------------------------------
TYPE_LABEL_FA = {"SUPERVISOR": r"SUPERVISOR", "EXECUTOR": r"EXECUTOR",
                 "COMPOSITE": r"Composite"}

DOMAIN_LABEL_FA = {
    "Business": r"Business", "Product": r"Product", "Project": r"Project",
    "Analytics": r"Analysis", "Architecture": r"Architecture", "Software": r"Software",
    "AI": r"AI", "Data": r"Data", "DevOps": "DevOps", "Testing": r"Testing & Quality",
    "Security": r"Security", "Compliance": r"Compliance", "Design": r"Design",
    "Documentation": r"Documentation", "HR": r"Human Resources", "Support": r"Support",
    "Growth": r"Growth & Marketing", "Audit": r"Audit", "Operations": r"Operations",
}

CATEGORY_LABEL_FA = {
    "Strategy": r"Strategy", "Management": r"Management", "Analysis": r"Analysis",
    "Architecture": r"Architecture", "Engineering": r"Engineering", "Data": r"Data",
    "Infrastructure": r"Infrastructure", "Testing": r"Testing", "Security": r"Security",
    "Compliance": r"Compliance", "Design": r"Design", "Documentation": r"Documentation",
    "Commercial": r"Commercial", "Support": r"Support", "Operations": r"Operations",
    "Audit": r"Audit",
}

SENIORITY_LABEL_FA = {
    "Junior": r"Junior", "Mid": r"Mid", "Senior": r"Senior", "Staff": "Staff",
    "Principal": "Principal", "Lead": "Lead", "Manager": r"Manager",
    "Director": r"Senior Manager", "Executive": r"Executive", "Expert": r"Specialist",
    "Specialist": r"Specialist",
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
    tokens = re.split(r"[\s,;/()\-–—|]+", raw)
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


# The placeholder a spec uses for its own lens list; a composite without one is
# hand-maintained, so its lens count is unknown rather than zero.
def spec_for_master(path: Path) -> tuple[dict | None, str | None]:
    """The composite spec that produced this master prompt, if there is one."""
    slug = MasterPersona(path).slug
    for spec_path in sorted(COMPOSITES.glob("*.json")):
        try:
            spec = json.loads(spec_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if spec.get("output") == path.name or spec.get("slug") == slug:
            return spec, f"composites/{spec_path.name}"
    return None, None


def composite_keywords(mp: MasterPersona, spec: dict | None) -> list[str]:
    """Search terms for a composite: its title, slug, spec mission and lens titles."""
    raw = [mp.title, mp.slug]
    if spec:
        raw.append(spec.get("mission", ""))
        raw += spec.get("lenses", [])
        raw += [e.get("title", "") for e in spec.get("extra_sections", [])]
    return keywords_of(" ".join(raw), "", "")


MASTER_SUFFIX_RE = re.compile(r"\s*—\s*Master Prompt\s*(\(v\d+\))?\s*$", re.I)


def composite_title(mp: MasterPersona) -> str:
    """The master prompt's own title, without the '— Master Prompt (v1)' tag.

    The tag is in the file so a human reading the prompt knows what it is; the
    catalogue title is the bare name, as in the README table.
    """
    return MASTER_SUFFIX_RE.sub("", mp.title).strip() or mp.title


def build_composites() -> list[dict]:
    out = []
    for path in master_personas():
        mp = MasterPersona(path)
        spec, spec_path = spec_for_master(path)
        out.append({
            "id": mp.slug,
            "title": composite_title(mp),
            "type": "COMPOSITE",
            "typeLabel": TYPE_LABEL_FA["COMPOSITE"],
            "group": None,
            "groupLabel": None,
            "domain": None,
            "domainLabel": None,
            "category": None,
            "categoryLabel": None,
            "seniority": None,
            "seniorityLabel": None,
            "mission": clip(mp.first_paragraph(), 320) or master_description(mp, spec),
            "description": master_description(mp, spec),
            "lenses": len(spec.get("lenses", [])) if spec else None,
            "spec": spec_path,
            "generated": bool(spec),
            "supervisors": [],
            "consumers": [],
            "capabilities": [],
            "path": f"prompts/composite/{path.name}",
            "file": path.name,
            "skill": f"skills/{mp.slug}/SKILL.md",
            "keywords": composite_keywords(mp, spec),
        })
    return out


def main() -> None:
    rows = read_rows()
    data_rows = [r for r in rows[1:]]
    details = load_details()
    _ms, _me = load_master_registry()
    sup_titles = {r[0] for r in data_rows if r[2] == r"SUPERVISOR"}
    sup_map = build_supervisor_map(sup_titles)
    by_supervisor: dict[str, list[str]] = {}
    for exe_title, sups in sup_map.items():
        for s in sups:
            by_supervisor.setdefault(s, []).append(exe_title)

    roles = []
    sup_i = exe_i = 0
    for title, _duty, role_type in [(r[0], r[1], r[2]) for r in data_rows]:
        slug = SLUG_OVERRIDES.get(title, _slug(title))
        ptype = "SUPERVISOR" if role_type == r"SUPERVISOR" else "EXECUTOR"
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
        "types": [{"id": "SUPERVISOR", "label": r"SUPERVISOR"},
                  {"id": "EXECUTOR", "label": r"EXECUTOR"},
                  {"id": "COMPOSITE", "label": r"Composite"}],
        "groups": sorted({(r["group"], r["groupLabel"]) for r in roles}),
        "domains": sorted({(r["domain"], r["domainLabel"]) for r in roles}),
        "categories": sorted({(r["category"], r["categoryLabel"]) for r in roles}),
        "seniorities": sorted({(r["seniority"], r["seniorityLabel"]) for r in roles}),
    }

    composites = build_composites()
    # No wall-clock stamp on purpose: these files are committed artifacts, and a
    # build timestamp makes every regeneration produce a diff, which breaks the
    # CI drift gate and hides real drift in noise. Provenance comes from git.
    doc = {
        "$schema": "personas-metadata/v1",
        "source": {
            "schema": r"README.md (full role table) + prompts/composite/*.md",
            "readme": "README.md",
            "details": r"README.md (full role table)",
            "generator": "scripts/generate_personas.py",
            "metadata_builder": "scripts/build_metadata.py",
            "composites": "prompts/composite/*.md (+ composites/*.json for the 15 spec-driven ones)",
        },
        "totals": {
            "roles": len(roles),
            "supervisors": sum(1 for r in roles if r["type"] == "SUPERVISOR"),
            "executors": sum(1 for r in roles if r["type"] == "EXECUTOR"),
            "composites": len(composites),
            "personas": len(roles) + len(composites),
        },
        "facets": facets,
        "roles": roles,
        "composites": composites,
    }
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"personas.json written: {len(roles)} roles "
          f"({doc['totals']['supervisors']} supervisors, {doc['totals']['executors']} executors) "
          f"+ {len(composites)} composites")
    print(f"size: {OUT.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
