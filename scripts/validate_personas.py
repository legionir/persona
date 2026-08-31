#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate that every persona under prompts/ follows the Master contract.

Checks:
  1. Every file has exactly sections 1..29 in order (section 61 of the Master).
  2. SUPERVISOR files additionally contain the 10 headings of section 62.
  3. EXECUTOR files additionally contain the 12 headings of section 63.
  4. Every file matches a README row and no README row is orphaned.
  5. Every executor has at least one registered supervisor.
  6. No legacy headers / legacy state machines remain.

Usage:
    python3 scripts/validate_personas.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPTS = ROOT / "prompts"
README = ROOT / "README.md"

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
        if title == "عنوان شغلی" or set(title) <= set("-: "):
            continue
        # the merged main table carries the prompt link in one of its cells;
        # scan for it instead of assuming a fixed column index
        for c in cells:
            m = re.search(r"(audit|implementation)/([\w\-]+)\.md", c)
            if m:
                rows.append((title, cells[2], m.group(1), m.group(2)))
                break
    return rows


def main() -> int:
    problems: list[str] = []
    files = sorted(p for p in PROMPTS.rglob("*.md") if p.name != "README.md")
    rows = read_rows(README)
    readme_slugs = {(d, s) for _, _, d, s in rows}
    file_slugs = {(p.parent.name, p.stem) for p in files}

    for p in files:
        text = p.read_text(encoding="utf-8")
        rel = str(p.relative_to(ROOT))
        if "# Persona — " not in text:
            problems.append(f"{rel}: missing '# Persona — <Role>' title")
        if "سیستم پرامپت" in text:
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
