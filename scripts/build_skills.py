#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Turn personas into Agent Skills (SKILL.md + references/).

A skill is the *loadable* form of a persona: a small `SKILL.md` that a model reads
when the task matches its description, plus the full persona as a reference file it
can pull only when needed (progressive disclosure).

Sources
  - prompts/audit/*.md, prompts/implementation/*.md  -> one skill per role persona
  - <root>/*.md (composite master prompts)           -> one skill per composite

Output layout (per skill):
    skills/<name>/SKILL.md              frontmatter + operating core (< ~300 lines)
    skills/<name>/references/persona.md verbatim source persona (full contract)
    skills/index.json                   machine-readable catalog
    skills/README.md                    human index

Usage:
    python3 scripts/build_skills.py                 # build every skill
    python3 scripts/build_skills.py --only audit-specialist
    python3 scripts/build_skills.py --source "prompts/audit/*.md"
    python3 scripts/build_skills.py --no-bundle     # SKILL.md only, no copies
    python3 scripts/build_skills.py --check         # validate, write nothing
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from persona_lib import (  # noqa: E402
    COMPOSITES, DESC_MAX, NAME_MAX, NON_PERSONA_MD, PROMPTS, ROOT, SKILLS,
    SKILL_LINES_SOFT_MAX,
    section_block,
    MasterPersona, RolePersona, bullets_of, checkbox_of, clip, code_blocks,
    fields_of, frontmatter, frontmatter_problems, load_doc, master_personas,
    key_rules, numbered_of, rel, role_personas, slugify, today, truncate,
)

STEP_BUDGET = 14          # max lines kept per procedure step
BODY_BUDGET = 18           # max lines kept per extracted section


# ---------------------------------------------------------------------------
# description generation (the skill trigger)
# ---------------------------------------------------------------------------
def role_description(rp: RolePersona) -> str:
    mission = clip(rp.mission or rp.title, 220)
    duties = clip(rp.fld(r"^3\.", "Primary") or "", 220)
    outcome = rp.fld(r"^2\.", "ExpectedOutcome") or r"Evidence-based output"
    allowed = clip(rp.fld(r"^5\.", "AllowedDecisions") or rp.fld(r"^14\.", "Decision Values"), 90)
    steps = len(rp.steps)
    duties_txt = duties or "this role's duties"
    desc = (
        f"Persona \"{rp.title}\" ({rp.type_label}) in the {rp.domain or '—'}: {mission}. "
        f"Use when the task needs {duties_txt} and the output must be "
        f"\"{outcome}\"; this skill enforces the domain, the authority ({allowed or '—'}), "
        f"the {steps} execution steps, and the final Quality Gate. "
        f"Use when you need {rp.title}-level judgment with evidence and a fixed scope."
    )
    return clip(desc, DESC_MAX)


def master_description(mp: MasterPersona, spec: dict | None) -> str:
    if spec and spec.get("description"):
        return clip(spec["description"], DESC_MAX)
    mission = clip(re.sub(r"\s+", " ", mp.first_paragraph()), 320)
    return clip(
        f"{mp.title} — composite master persona. {mission} "
        f"Use when you need a deep, structured, evidence-only run of this persona and a "
        f"generic checklist answer is not acceptable.",
        DESC_MAX,
    )


# ---------------------------------------------------------------------------
# SKILL.md — role personas
# ---------------------------------------------------------------------------
def role_skill_body(rp: RolePersona, bundle: bool = True) -> str:
    f = rp.f
    out: list[str] = [f"# {rp.title} — Persona Skill", ""]
    out.append(f"> Type: **{rp.type_label}** ({rp.role_type}) | Domain: {rp.domain or '—'} | "
               f"Level: {rp.seniority or '—'} | Source: [`{rel(rp.path)}`](../../{rel(rp.path)})")
    out.append("")

    # trigger
    outcome = rp.fld(r"^2\.", "ExpectedOutcome") or r"Evidence-based"
    success = clip(rp.fld(r"^2\.", "SuccessDefinition") or r"Sufficient evidence", 160)
    out.append(r"## When to Use (Trigger)")
    out.append(f"- When the task requires the judgement \"{rp.title}\" and the output **{outcome}** is needed.")
    out.append(r"- When the domain and authority must be settled before anything else; this persona does not decide without Evidence.")
    out.append(f"- When the output must be verifiable: {success}.")
    out.append("")

    def block(title: str, section_pattern: str, keys: list[str] | None = None,
              budget: int = BODY_BUDGET) -> None:
        """Render one persona section: either its named fields, or its bullets."""
        sec = rp.doc.find(section_pattern, regex=True)
        if not sec:
            return
        keys = keys or []
        vals = fields_of(sec.body)
        lines = [f"## {title}", ""]
        for k in keys:
            v = vals.get(k)
            if v:
                lines.append(f"- **{k}:** {clip(v, 400)}")
        if not any(line.startswith("- **") for line in lines):
            # field-less section (Quality Gates, Mandatory Rules, ...) -> bullets
            for b in bullets_of(sec.body)[:budget]:
                lines.append(f"- {clip(b, 240)}")
        if len(lines) > 2:
            out.extend(lines)
            out.append("")

    block(r"Mission and success criteria", r"^2\.", ["PrimaryGoal", "ExpectedOutcome", "SuccessDefinition", "FailureDefinition"])
    block(r"Authority and boundaries", r"^5\.", ["AllowedDecisions", "AllowedActions", "ForbiddenDecisions",
                                     "ForbiddenActions", "ProductionAuthority", "ApprovalRequiredFor",
                                     "CrossDomainRules"])
    block(r"Inputs", r"^7\.", ["Required", "Optional", "Prohibited", "Validation"])
    block(r"Preconditions", r"^8\.", ["Required", "Blocking", "Authorization"])
    block(r"Scope", r"^11\.", ["InScope", "OutOfScope", "AffectedAreas", "ScopeExpansionPolicy"])
    block(r"Tools", r"^15\.", ["Allowed", "Restricted", "Forbidden", "ApprovalRequired", "ReadOnly"])
    block(r"Evidence and verification", r"^16\.", ["Evidence", "Verification"])
    block(r"Risk", r"^19\.", ["Risks", "Mitigation", "Residual"])
    block("KPI", r"^28\.", ["Metrics", "Targets"])

    # procedure
    steps = rp.step_bodies()
    if steps:
        out.append(r"## Execution Steps (Procedure)")
        out.append("")
        for header, body in steps:
            vals = fields_of(body)
            out.append(f"### {header}")
            if vals.get("Objective"):
                out.append(f"- **Objective:** {clip(vals['Objective'], 240)}")
            if vals.get("Inputs"):
                out.append(f"- **Inputs:** {clip(vals['Inputs'], 200)}")
            if vals.get("Preconditions"):
                out.append(f"- **Preconditions:** {clip(vals['Preconditions'], 160)}")
            actions = fields_of(body).get("Actions", "")
            if actions:
                parts = [x.strip().rstrip(r",") for x in
                         re.split(r"\s+(?=\d+\.\s)|;\s*", actions) if x.strip()]
                if parts:
                    out.append("- **Actions:**")
                    for a in parts[:5]:
                        out.append(f"  - {clip(a, 220)}")
            if vals.get("ExitCriteria"):
                out.append(f"- **ExitCriteria:** {clip(vals['ExitCriteria'], 200)}")
            if vals.get("EscalationConditions"):
                out.append(f"- **Escalation:** {clip(vals['EscalationConditions'], 160)}")
            out.append("")

    block(r"Decision rules", r"^14\.", [r"Status Values (all Personas)", "Decision Values", "Rules"])
    block(r"Acceptance criteria (quality gate)", r"^21\.", budget=BODY_BUDGET)
    block(r"Non-negotiable rules", r"^29\.", budget=BODY_BUDGET)

    # type-specific report skeleton
    for title, pattern in ((r"Report structure / final output", r"^(Audit|Implementation) (Scope|Criteria|Procedure)"),
                           (r"Delivery, Escalation, and Execution Plan", r"^2[456]\.")):
        secs = rp.doc.find_all(pattern, regex=True)
        if not secs:
            continue
        out.append(f"## {title}")
        out.append("")
        for sec in secs[:6]:
            out.append(f"### {sec.flat_title}")
            out.append(truncate(sec.body.strip(), BODY_BUDGET).strip())
            out.append("")

    ref_link = "references/persona.md" if bundle else f"../../{rel(rp.path)}"
    ref_label = (r"Full prompt of this persona (29 sections of the Master contract)" if bundle
                 else r"Full prompt of this persona in the repository (not copied — `--no-bundle` mode)")
    out.append(r"## Full Reference (Progressive Disclosure)")
    out.append("")
    out.append(f"- [`{ref_link}`]({ref_link}) — {ref_label}. When you need finding-format details, "
               f"the state machine, traceability, or the execution plan, read this file.")
    out.append("")
    out.append("---")
    out.append("")
    out.append(f"_Generated by `scripts/build_skills.py` from `{rel(rp.path)}` — {today()}_")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# SKILL.md — composite / master personas
# ---------------------------------------------------------------------------
def master_skill_body(mp: MasterPersona, spec: dict | None, bundle: bool = True) -> str:
    doc = mp.doc
    out: list[str] = [f"# {mp.title} — Composite Persona Skill", ""]
    src = rel(mp.path)
    lenses = len((spec or {}).get("lenses", []))
    badge = f"> Type: **composite (Composite)** | lenses: {lenses or '—'} | Source: [`{src}`](../../{src})"
    out += [badge, ""]

    mission = re.sub(r"\s+", " ", mp.first_paragraph()).strip()
    out.append(r"## When to Use (Trigger)")
    if mission:
        out.append(f"- When the task's mission is: {clip(mission.split('. ')[0], 220).rstrip('.…')}.")
    out.append(r"- When the output must be structured, evidence-based, and verifiable — not a generic checklist.")
    out.append(r"- When you must know precisely what is missing, incorrect, or dangerous before deciding or acting.")
    out.append("")

    if mission:
        out += [r"## Mission", "", clip(mission, 900), ""]

    # inputs block
    inputs = section_block(doc, r"INPUTS", regex=True)
    blocks = code_blocks(inputs) or code_blocks(doc.preamble)
    if blocks:
        out += [r"## Required Inputs (fill in before starting)", "", "```"]
        out += blocks[0].splitlines()[:16] + ["```", ""]

    # non-negotiable rules (section + children)
    rules = section_block(doc, r"PRIME DIRECTIVE|CORE CONTRACT|ABSOLUTE RULES|non-negotiable", regex=True)
    rule_lines = key_rules(rules) or (bullets_of(rules) + numbered_of(rules))[:10]
    if rule_lines:
        out += [r"## Non-Negotiable Rules", ""]
        out += [f"- {clip(b, 240)}" for b in rule_lines] + [""]

    phases = mp.phase_lines()
    if phases:
        out += [r"## Execution Phases (in this order)", ""]
        out += [f"- {clip(p, 220)}" for p in phases[:16]] + [""]

    sev = section_block(doc, r"SEVERITY", regex=True)
    sev_rows = [ln for ln in sev.splitlines() if ln.strip().startswith("|")]
    sev_bullets = bullets_of(sev)[:8]
    if sev_rows or sev_bullets:
        out += [r"## Severity", ""]
        out += sev_rows[:9] if sev_rows else [f"- {clip(b, 220)}" for b in sev_bullets]
        out.append("")

    finding = section_block(doc, r"FINDING|Finding Record|Finding format", regex=True)
    tmpl = next((blk for blk in code_blocks(finding)
                 if sum(1 for ln in blk.splitlines() if "**" in ln and ":" in ln) >= 3), "")
    if tmpl:
        out += [r"## Finding Format (mandatory)", "", "````"]
        out += tmpl.splitlines()[:34] + ["````", ""]

    report = section_block(doc, r"REPORT STRUCTURE|Final Report|Report Emission", regex=True)
    items = numbered_of(report)[:20]
    if items:
        out += [r"## Final Report Structure", ""]
        out += [f"{i}. {clip(it, 200)}" for i, it in enumerate(items, 1)] + [""]

    gate = section_block(doc, r"QUALITY GATE|Pre-Flight|Final Gate", regex=True)
    boxes = checkbox_of(gate)[:20] or bullets_of(gate)[:14]
    if not boxes:
        boxes = [q.strip() for q in re.split(r"(?<=\?)\s+", gate) if "?" in q][:10]
    if boxes:
        out += [r"## Final Quality Gate (the final report must not be issued without passing it)", ""]
        out += [f"- [ ] {clip(b, 200)}" for b in boxes] + [""]

    principle_src = section_block(doc, r"CORE PRINCIPLE|PRINCIPLE|Final Objective|OBJECTIVE", regex=True)
    principle = []
    for ln in principle_src.splitlines():
        s = ln.strip()
        if not s.startswith(">"):
            continue
        s = s.lstrip(">").strip()
        if s.endswith("**"):
            s = s[:-2].rstrip()
        if s:
            principle.append(f"> {s}")
    if principle:
        out += [r"## Governing Principle", ""] + principle[-6:] + [""]

    ref_link = f"references/{mp.slug}.md" if bundle else f"../../{rel(mp.path)}"
    # map of the master prompt's sections, with the composite's own sections marked.
    # A table of contents only — never a copy of the content (progressive disclosure).
    extra_titles = [e.get("title", "") for e in (spec or {}).get("extra_sections", []) if e.get("title")]
    toc: list[str] = []
    for sec in doc.sections:
        if sec.level != 2:
            continue
        title = re.sub(r"^\d+\.\s*", "", sec.title).strip()
        if not title:
            continue
        own = any(title.startswith(x[:18]) for x in extra_titles)
        toc.append(f"- {'◆' if own else ''} {title}".replace("-  ", "- "))
    if toc:
        out += [r"## Master Prompt Map (in the reference — `◆` = section specific to this persona)", ""]
        out += toc + [""]

    out += [r"## Full Reference (Progressive Disclosure)", ""]
    out += [f"- [`{ref_link}`]({ref_link}) — the full master prompt text "
            f"({len(mp.text.splitlines())} lines). Open it only when you need protocol details, "
            f"the assessment scope, or the output formats.", ""]
    out += ["---", "", f"_Generated by `scripts/build_skills.py` from `{src}` — {today()}_"]
    return "\n".join(out)


# ---------------------------------------------------------------------------
# build
# ---------------------------------------------------------------------------
def composite_specs() -> dict[str, dict]:
    out = {}
    for p in sorted(COMPOSITES.glob("*.json")):
        try:
            spec = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if spec.get("output"):
            out[spec["output"]] = spec
    return out


def build_one(source: Path, bundle: bool = True) -> tuple[str, dict, list[str]]:
    problems: list[str] = []
    text = source.read_text(encoding="utf-8")
    specs = composite_specs()
    spec = specs.get(source.name)

    if "# Persona — " in text:
        rp = RolePersona(source)
        name = rp.slug
        title = rp.title
        description = role_description(rp)
        body = role_skill_body(rp, bundle=bundle)
        meta = {
            "version": "1",
            "type": rp.role_type,
            "typeLabel": rp.type_label,
            "domain": rp.domain,
            "seniority": rp.seniority,
            "source": rel(source),
            "language": "en",
        }
    else:
        mp = MasterPersona(source)
        name = mp.slug
        title = mp.title
        description = master_description(mp, spec)
        body = master_skill_body(mp, spec, bundle=bundle)
        meta = {
            "version": (spec or {}).get("version", "1"),
            "type": "COMPOSITE",
            "typeLabel": r"Composite",
            "lenses": len((spec or {}).get("lenses", [])) or None,
            "source": rel(source),
            "language": (spec or {}).get("language", "en"),
        }

    problems.extend(frontmatter_problems(name, description))
    lines = body.splitlines()
    if len(lines) > SKILL_LINES_SOFT_MAX:
        problems.append(f"SKILL.md is {len(lines)} lines (soft max {SKILL_LINES_SOFT_MAX}) — move detail into references/")

    dest = SKILLS / name
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True, exist_ok=True)
    ref_name = None
    if bundle:
        (dest / "references").mkdir(parents=True, exist_ok=True)
        ref_name = "persona.md" if "# Persona — " in text else f"{name}.md"
        (dest / "references" / ref_name).write_text(text, encoding="utf-8")
    skill_md = frontmatter({"name": name, "description": description, "metadata": meta}) + "\n\n" + body.rstrip() + "\n"
    (dest / "SKILL.md").write_text(skill_md, encoding="utf-8")
    return name, {"title": title, "description": description, "meta": meta,
                  "lines": len(skill_md.splitlines()), "source": rel(source),
                  "path": rel(dest / "SKILL.md"),
                  "reference": f"references/{ref_name}" if ref_name else None}, problems


def write_catalog(entries: dict[str, dict]) -> None:
    """Write skills/index.json.

    Skills that were not rebuilt in this run (e.g. `--only`) but still exist on
    disk are carried over, so a partial build never truncates the catalog.
    """
    merged = dict(entries)
    index = SKILLS / "index.json"
    if index.exists():
        try:
            for s in json.loads(index.read_text(encoding="utf-8")).get("skills", []):
                if s["name"] not in merged and (SKILLS / s["name"] / "SKILL.md").exists():
                    merged[s["name"]] = {
                        "title": s.get("title", s["name"]),
                        "description": s.get("description", ""),
                        "meta": {"type": s.get("type"), "typeLabel": s.get("typeLabel"),
                                 "domain": s.get("domain"),
                                 "lenses": s.get("lenses")},
                        "source": s.get("source", ""),
                        "path": s.get("skill", f"skills/{s['name']}/SKILL.md"),
                        "lines": len((SKILLS / s["name"] / "SKILL.md").read_text(encoding="utf-8").splitlines()),
                    }
        except (json.JSONDecodeError, OSError, KeyError):
            pass

    doc = {
        "$schema": "persona-skills/v1",
        "generated_at": f"{today()}T00:00:00Z",
        "source": {"generator": "scripts/build_skills.py",
                   "personas": "prompts/**/*.md + composite master prompts"},
        "totals": {"skills": len(merged),
                   "roles": sum(1 for e in merged.values()
                                if e["meta"].get("type") in ("SUPERVISOR", "EXECUTOR")),
                   "composites": sum(1 for e in merged.values()
                                     if e["meta"].get("type") == "COMPOSITE")},
        "skills": [
            {"name": n, "title": e["title"], "type": e["meta"].get("type"),
             "typeLabel": e["meta"].get("typeLabel"), "domain": e["meta"].get("domain"),
             "source": e["source"], "skill": e.get("path", f"skills/{n}/SKILL.md"),
             "description": e["description"],
             **({"lenses": e["meta"]["lenses"]}
                if e["meta"].get("lenses") else {})}
            for n, e in sorted(merged.items())
        ],
    }
    index.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_skills_readme(entries: dict[str, dict]) -> None:
    index = SKILLS / "index.json"
    if index.exists():
        try:
            for s in json.loads(index.read_text(encoding="utf-8")).get("skills", []):
                entries.setdefault(s["name"], {
                    "title": s.get("title", s["name"]),
                    "meta": {"type": s.get("type"), "typeLabel": s.get("typeLabel"),
                             "domain": s.get("domain")},
                    "source": s.get("source", ""),
                    "lines": len((SKILLS / s["name"] / "SKILL.md").read_text(encoding="utf-8").splitlines()),
                })
        except (json.JSONDecodeError, OSError, KeyError):
            pass
    rows = sorted(entries.items(), key=lambda kv: (kv[1]["meta"].get("type") != "COMPOSITE", kv[0]))
    lines = [
        "# Persona Skills",
        "",
        r"Each folder is one **Agent Skill**: `SKILL.md` is the operating core (read when the task matches) and",
        r"`references/` holds the full persona text for when contract details are needed.",
        "",
        r"Install in Claude Code (project):",
        "",
        "```bash",
        r"# The whole library",
        "cp -r skills/<name> .claude/skills/",
        "",
        r"# Or all skills",
        "for d in skills/*/; do cp -r \"$d\" .claude/skills/; done",
        "```",
        "",
        r"Regenerate: `python3 scripts/build_skills.py` — validate: `python3 scripts/validate_skills.py`",
        "",
        f"Full index and machine-readable metadata: [`index.json`](index.json)",
        "",
        r"| Skill | Type | Domain | Source | SKILL.md lines |",
        "|---|---|---|---|---|",
    ]
    for name, e in rows:
        domain = e["meta"].get("domain") or (r"Composite" if e["meta"].get("type") == "COMPOSITE" else "—")
        lines.append(f"| [`{name}`]({name}/SKILL.md) | {e['meta'].get('typeLabel', '—')} | "
                     f"{domain} | `{e['source']}` | {e['lines']} |")
    lines += ["", f"_Count: {len(entries)} skills — generated on {today()} by `scripts/build_skills.py`_", ""]
    (SKILLS / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", action="append", default=[], help="skill name(s) to build (repeatable)")
    ap.add_argument("--source", action="append", default=[], help="glob(s) relative to repo root (repeatable)")
    ap.add_argument("--no-bundle", action="store_true", help="do not copy the full persona into references/")
    ap.add_argument("--check", action="store_true", help="validate existing skills, write nothing")
    ap.add_argument("--out", default="skills", help="output directory (default: skills/)")
    args = ap.parse_args()

    global SKILLS
    SKILLS = (ROOT / args.out).resolve() if not Path(args.out).is_absolute() else Path(args.out)

    if args.check:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import validate_skills
        return validate_skills.main(["--out", str(SKILLS)])

    sources: list[Path] = []
    if args.source:
        for pat in args.source:
            sources.extend(sorted(p for p in ROOT.glob(pat) if p.name not in NON_PERSONA_MD))
    else:
        sources = role_personas() + master_personas()
    if args.only:
        wanted = set(args.only)
        sources = [s for s in sources if slugify(s.stem) in wanted or s.stem in wanted]
    if not sources:
        print("no sources matched")
        return 1

    entries: dict[str, dict] = {}
    failures = 0
    for src in sources:
        try:
            name, entry, problems = build_one(src, bundle=not args.no_bundle)
        except Exception as exc:  # noqa: BLE001
            print(f"[FAIL] {rel(src)}: {exc}")
            failures += 1
            continue
        entries[name] = entry
        if problems:
            failures += 1
            print(f"[WARN] {name}: " + "; ".join(problems))
        else:
            print(f"[OK]   {name:44} {entry['lines']:>4} lines  <- {entry['source']}")

    if not args.no_bundle and entries:
        write_catalog(entries)
        write_skills_readme(entries)
        print(f"\n{len(entries)} skills -> {rel(SKILLS)} "
              f"(index.json, README.md)")

    # full rebuild: drop skill directories whose persona no longer exists
    if not args.only and not args.source and not args.no_bundle:
        stale = [d for d in SKILLS.iterdir()
                 if d.is_dir() and d.name not in entries]
        for d in stale:
            shutil.rmtree(d)
            print(f"[prune] removed {rel(d)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
