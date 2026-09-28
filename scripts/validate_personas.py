#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate that every persona under prompts/ follows the Master contract.

Checks:
  1. Every file has exactly sections 1..29 in order (section 61 of the Master).
  2. SUPERVISOR files additionally contain the 10 headings of section 62.
  3. EXECUTOR files additionally contain the 12 headings of section 63.
  4. Every file matches a README row and no README row is orphaned.
  5. Canonical supervisor registry equals README, prompt, and metadata relationships.
  6. Every executor has at least one registered supervisor.
  7. No legacy headers / legacy state machines remain.

Usage:
    python3 scripts/validate_personas.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPTS = ROOT / "prompts"
README = ROOT / "README.md"
MAIN_COLS = 28    # width of the merged main role table

SUP_HEADINGS = [
    "## Audit Scope", "## Audit Criteria", "## Audit Procedure", "## Coverage Manifest",
    "## Decomposition Table", "## Findings", "## Risk Assessment", "## Recommendations",
    "## Execution Plan", "## Final Verdict",
]
EXE_HEADINGS = [
    "## Implementation Scope", "## Implementation Requirements", "## Implementation Procedure",
    "## Change Manifest", "## Modified Files", "## Created Files", "## Deleted Files", "## Tests",
    "## Verification", "## Evidence", "## Execution Plan Status", "## Final Completion Status",
]


def read_rows(path: Path) -> list[tuple[str, str, str, str]]:
    rows = []
    for ln in path.read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 3:
            continue
        title = cells[0]
        if title == r"Job Title" or set(title) <= set("-: "):
            continue
        # the merged main table carries the prompt link in one of its cells;
        # scan for it instead of assuming a fixed column index. The `prompts/`
        # prefix is required so that links elsewhere in the README (e.g. the
        # composite-persona / skills sections) are not mistaken for role rows.
        for c in cells:
            m = re.search(r"prompts/(audit|implementation)/([\w\-]+)\.md", c)
            if m:
                rows.append((title, cells[2], m.group(1), m.group(2)))
                break
    return rows


def read_main_table(path: Path) -> list[list[str]]:
    """Read only the first contiguous Markdown table (the 28-column role table)."""
    rows: list[list[str]] = []
    started = False
    for line in path.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if text.startswith("|"):
            started = True
            cells = [c.strip() for c in text.split("|")]
            if cells and cells[0] == "": cells = cells[1:]
            if cells and cells[-1] == "": cells = cells[:-1]
            if len(cells) == MAIN_COLS and not all(set(c) <= set("-: ") for c in cells):
                rows.append(cells)
        elif started:
            break
    return rows


def validate_supervisor_parity(problems: list[str], rows: list[tuple[str, str, str, str]]) -> None:
    registry_path = ROOT / "data" / "supervisor-map.json"
    try:
        data = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        problems.append(f"cannot read canonical supervisor registry: {exc}")
        return
    main_rows = read_main_table(README)
    if not main_rows or main_rows[0][0] != "Job Title":
        problems.append("main README role table is missing or malformed")
        return
    role_rows = [r for r in main_rows[1:] if r[2] in ("SUPERVISOR", "EXECUTOR")]
    expected_ids = {r[0]: f"EXE-{i:03d}" for i, r in enumerate([x for x in role_rows if x[2] == "EXECUTOR"], 1)}
    canonical: dict[str, list[str]] = {}
    for item in data.get("roles", []):
        title, supervisors = item.get("title"), item.get("supervisors")
        if title in canonical or title not in expected_ids:
            problems.append(f"supervisor registry has duplicate/unknown executor: {title!r}")
            continue
        if item.get("roleId") != expected_ids[title]:
            problems.append(f"supervisor registry roleId mismatch for {title}: {item.get('roleId')!r}")
        if not isinstance(supervisors, list) or any(not isinstance(x, str) for x in supervisors):
            problems.append(f"supervisor registry entry for {title} must contain a string array")
            continue
        if len(supervisors) != len(set(supervisors)):
            problems.append(f"supervisor registry entry for {title} contains duplicates")
        canonical[title] = supervisors
    if set(canonical) != set(expected_ids):
        problems.append(f"supervisor registry coverage mismatch: expected {len(expected_ids)}, got {len(canonical)}")
    registered = {r[0] for r in role_rows if r[2] == "SUPERVISOR"}
    for title, sups in canonical.items():
        for sup in sups:
            if sup not in registered:
                problems.append(f"canonical supervisor for {title} is not a registered SUPERVISOR: {sup}")
    for cells in role_rows:
        title, role_type = cells[0], cells[2]
        if role_type != "EXECUTOR":
            continue
        expected = canonical.get(title)
        if expected is None:
            continue
        readme_sups = [x.strip() for x in cells[6].split(",") if x.strip()]
        if readme_sups != expected:
            problems.append(f"README supervisor mismatch for {title}: {readme_sups!r} != {expected!r}")
        slug_match = next((r[3] for r in rows if r[0] == title), None)
        if not slug_match:
            continue
        prompt = ROOT / "prompts" / "implementation" / f"{slug_match}.md"
        try:
            text = prompt.read_text(encoding="utf-8")
        except OSError:
            continue
        section = re.search(r"## 6\. Stakeholders & Ownership\n(.*?)(?:\n\n## 7\.)", text, re.S)
        if not section:
            problems.append(f"{prompt.relative_to(ROOT)}: missing ownership section")
            continue
        fields = {m.group(1): m.group(2).strip() for m in re.finditer(r"^- \*\*([^:]+):\*\* (.*)$", section.group(1), re.M)}
        expected_join = ", ".join(expected)
        for field in ("Reviewer", "Approver", "SupportingPersonas"):
            if fields.get(field) != (expected_join or "Unknown / Requires Verification"):
                problems.append(f"{prompt.relative_to(ROOT)}: {field} differs from canonical supervisor map")
        expected_owner = expected[0] if expected else "Unknown / Requires Verification: the supervisor must exist in the Registry"
        if fields.get("DecisionOwner") != expected_owner:
            problems.append(f"{prompt.relative_to(ROOT)}: DecisionOwner differs from canonical supervisor map")
    metadata_path = ROOT / "personas.json"
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        meta_roles = {r.get("title"): r for r in metadata.get("roles", []) if r.get("type") == "EXECUTOR"}
        for title, sups in canonical.items():
            row = meta_roles.get(title)
            if row is None or row.get("supervisors") != sups:
                problems.append(f"personas.json supervisor mismatch for {title}")
    except (OSError, json.JSONDecodeError) as exc:
        problems.append(f"cannot read personas.json for supervisor parity: {exc}")


def main() -> int:
    problems: list[str] = []
    files = sorted(
        p for p in PROMPTS.rglob("*.md")
        if p.name != "README.md" and (PROMPTS / "composite") not in p.parents
    )
    rows = read_rows(README)
    readme_slugs = {(d, s) for _, _, d, s in rows}
    file_slugs = {(p.parent.name, p.stem) for p in files}

    # Every supervisor named in the README "Supervisor" column must itself be a
    # row registered as a SUPERVISOR. Generation resolves supervisors from the
    # Master map + EXTRA_SUPERVISORS, so a bad name here does not break the
    # build -- it only makes the table lie to the reader, which is worse.
    registered = {r[0] for r in rows if r[1] == r"SUPERVISOR"}
    for ln in README.read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) != MAIN_COLS:
            continue
        title, _duty, role_type = cells[0], cells[1], cells[2]
        if title == r"Job Title" or set(title) <= set("-: "):
            continue
        if role_type != r"EXECUTOR":
            continue
        for sup in cells[6].split(","):
            sup = sup.strip()
            if sup and sup not in registered:
                problems.append(
                    f"README row '{title}' names unregistered supervisor '{sup}'")

    for p in files:
        text = p.read_text(encoding="utf-8")
        rel = str(p.relative_to(ROOT))
        if "# Persona — " not in text:
            problems.append(f"{rel}: missing '# Persona — <Role>' title")
        if r"Prompt System" in text:
            problems.append(f"{rel}: legacy header found")
        nums = re.findall(r"^## (\d+)\. ", text, re.M)
        expected = [str(i) for i in range(1, 30)]
        if nums != expected:
            problems.append(f"{rel}: sections missing/out of order: {nums[:6]}")
            continue
        type_text = re.search(r"## 4\. Type & Capability\n(.*?)\n\n---", text, re.S)
        is_sup = bool(type_text and "SUPERVISOR" in type_text.group(1) and "EXECUTOR" not in type_text.group(1))
        wanted = SUP_HEADINGS if is_sup else EXE_HEADINGS
        missing = [h for h in wanted if h not in text]
        if missing:
            problems.append(f"{rel}: missing type-specific headings {missing}")
        if is_sup and "IMPLEMENTING" in text.split("## 23. State Machine")[1][:400]:
            problems.append(f"{rel}: supervisor uses executor state machine")
        if not is_sup and "RECOMMENDATION_READY" in text.split("## 23. State Machine")[1][:400]:
            problems.append(f"{rel}: executor uses supervisor state machine")
        if "GENERIC" in text:
            problems.append(f"{rel}: forbidden GENERIC step type")

    orphan_files = file_slugs - readme_slugs
    orphan_rows = readme_slugs - file_slugs
    for d, s in sorted(orphan_files):
        problems.append(f"orphan file without README row: prompts/{d}/{s}.md")
    for d, s in sorted(orphan_rows):
        problems.append(f"README row without file: {d}/{s}")

    validate_supervisor_parity(problems, rows)

    # supervisor mapping sanity
    sup_files = {p.stem for p in (PROMPTS / "audit").glob("*.md")}
    impl_files = {p.stem for p in (PROMPTS / "implementation").glob("*.md")}
    for p in (PROMPTS / "implementation").glob("*.md"):
        text = p.read_text(encoding="utf-8")
        sec6 = re.search(r"## 6\. Stakeholders & Ownership\n(.*?)\n\n## 7\.", text, re.S)
        if not sec6 or "Unknown / Requires Verification" in sec6.group(1).split("Reviewer:")[1][:200]:
            problems.append(f"implementation/{p.stem}: no registered supervisor")

    print(f"Persona files: {len(files)} (supervisor {len(sup_files)}, executor {len(impl_files)})")
    print(f"README role rows: {len(rows)}")
    if problems:
        print(f"PROBLEMS: {len(problems)}")
        for pr in problems[:40]:
            print(" -", pr)
        return 1
    print("ALL CHECKS PASSED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
