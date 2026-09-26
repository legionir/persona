#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate generated Agent Skills under skills/.

Checks, per skill directory:
  1. SKILL.md exists and starts with YAML frontmatter (--- ... ---).
  2. `name` is lowercase-hyphen, <= 64 chars, and equals the directory name.
  3. `description` is non-empty and <= 1024 chars (it is the skill's trigger).
  4. Every local markdown link inside SKILL.md resolves to a real file.
  5. SKILL.md stays under the soft line budget (progressive disclosure).
  6. skills/index.json lists exactly the directories that exist.

Usage:
    python3 scripts/validate_skills.py
    python3 scripts/validate_skills.py --out skills
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from persona_lib import DESC_MAX, NAME_MAX, ROOT, SKILL_LINES_SOFT_MAX, rel  # noqa: E402

FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
KEY_RE = re.compile(r"^([a-zA-Z_]+):\s*(.*)$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    m = FM_RE.match(text)
    if not m:
        return {}, text
    data: dict = {}
    current: str | None = None
    for ln in m.group(1).splitlines():
        km = KEY_RE.match(ln)
        if km and not ln.startswith(" "):
            current = km.group(1)
            data[current] = km.group(2).strip().strip('"')
        elif ln.startswith("  ") and current:
            k2, _, v2 = ln.strip().partition(":")
            if k2:
                data.setdefault(current, {})
                if isinstance(data[current], dict):
                    data[current][k2.strip()] = v2.strip().strip('"')
    return data, text[m.end():]


def check_skill(skill_dir: Path) -> list[str]:
    problems: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"{rel(skill_dir)}: SKILL.md missing"]
    text = skill_md.read_text(encoding="utf-8")
    data, body = parse_frontmatter(text)
    if not data:
        problems.append(f"{rel(skill_dir)}: no YAML frontmatter")

    name = data.get("name", "")
    if name != skill_dir.name:
        problems.append(f"{rel(skill_dir)}: name '{name}' != directory '{skill_dir.name}'")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        problems.append(f"{rel(skill_dir)}: name must be lowercase letters/digits/hyphens")
    if len(name) > NAME_MAX:
        problems.append(f"{rel(skill_dir)}: name longer than {NAME_MAX} chars")

    desc = data.get("description", "")
    if not desc.strip():
        problems.append(f"{rel(skill_dir)}: empty description (the skill would never trigger)")
    if len(desc) > DESC_MAX:
        problems.append(f"{rel(skill_dir)}: description {len(desc)} chars > {DESC_MAX}")
    if desc.count('"') % 2:
        problems.append(f"{rel(skill_dir)}: unbalanced quotes in description")

    for target in LINK_RE.findall(body):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        clean = target.split("#")[0]
        if not clean:
            continue
        if not (skill_dir / clean).resolve().exists():
            problems.append(f"{rel(skill_dir)}: broken link -> {target}")

    lines = len(text.splitlines())
    if lines > SKILL_LINES_SOFT_MAX:
        problems.append(f"{rel(skill_dir)}: SKILL.md {lines} lines > soft max {SKILL_LINES_SOFT_MAX}")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=str(ROOT / "skills"))
    args = ap.parse_args(argv)
    root = Path(args.out)
    if not root.exists():
        print(f"no skills directory at {rel(root)} — run scripts/build_skills.py first")
        return 1

    dirs = sorted(p for p in root.iterdir() if p.is_dir())
    problems: list[str] = []
    for d in dirs:
        problems.extend(check_skill(d))

    index = root / "index.json"
    if index.exists():
        doc = json.loads(index.read_text(encoding="utf-8"))
        listed = {s["name"] for s in doc.get("skills", [])}
        present = {d.name for d in dirs}
        for missing in sorted(present - listed):
            problems.append(f"index.json: missing entry for {missing}")
        for extra in sorted(listed - present):
            problems.append(f"index.json: stale entry for {extra}")
    else:
        problems.append("index.json missing")

    print(f"Skills: {len(dirs)}")
    if problems:
        print(f"PROBLEMS: {len(problems)}")
        for pr in problems[:60]:
            print(" -", pr)
        return 1
    print("ALL CHECKS PASSED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
