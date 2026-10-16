#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Package the persona library in Claude Code's native layout.

Reads skills/ (built by build_skills.py) and produces:
    agents/<name>.md                  one subagent per role persona (190)
    .claude-plugin/plugin.json        plugin manifest (skills/ + agents/ auto-discovered)
    .claude-plugin/marketplace.json   makes the repo installable via /plugin marketplace add
    .claude/skills -> ../skills       project-level discovery (symlink)
    .claude/agents -> ../agents       project-level discovery (symlink)

SUPERVISOR personas get read-only tools; EXECUTOR personas inherit all tools.
Composites stay skills only (they are read-only audit procedures).

Usage: python3 scripts/build_claude_code.py [--check]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
AGENTS = ROOT / "agents"
READONLY_TOOLS = "Read, Grep, Glob"


def split_frontmatter(text: str) -> str:
    m = re.match(r"^---\n.*?\n---\n", text, re.S)
    return text[m.end():] if m else text


def agent_doc(entry: dict) -> str:
    name = entry["name"]
    body = split_frontmatter((ROOT / entry["skill"]).read_text(encoding="utf-8")).lstrip()
    # links were relative to skills/<name>/; subagents have no such anchor, use repo-root paths
    body = body.replace("](../../", "](")
    body = body.replace("`references/persona.md`", f"`skills/{name}/references/persona.md`")
    fm = ["---", f"name: {name}", f"description: {json.dumps(entry['description'], ensure_ascii=False)}"]
    if entry["type"] == "SUPERVISOR":
        fm.append(f"tools: {READONLY_TOOLS}")
    fm.append("---")
    preface = (
        f"You are the persona **{entry['title']}**. Operate strictly within the authority, scope, "
        f"evidence and quality-gate rules below. The full contract is in "
        f"`skills/{name}/references/persona.md` — read it when a detail is needed.\n\n"
    )
    return "\n".join(fm) + "\n\n" + preface + body


def write(path: Path, content: str, check: bool, stale: list[str]) -> None:
    if check:
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            stale.append(str(path.relative_to(ROOT)))
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def link(path: Path, target: str, check: bool, stale: list[str]) -> None:
    if check:
        if not (path.is_symlink() and os.readlink(path) == target):
            stale.append(str(path.relative_to(ROOT)))
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink() or path.exists():
        path.unlink()
    path.symlink_to(target)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    index = json.loads((SKILLS / "index.json").read_text(encoding="utf-8"))["skills"]
    roles = [e for e in index if e["type"] in ("SUPERVISOR", "EXECUTOR")]
    stale: list[str] = []

    for e in roles:
        write(AGENTS / f"{e['name']}.md", agent_doc(e), args.check, stale)
    wanted = {f"{e['name']}.md" for e in roles}
    for f in AGENTS.glob("*.md") if AGENTS.exists() else []:
        if f.name not in wanted:
            if args.check:
                stale.append(str(f.relative_to(ROOT)))
            else:
                f.unlink()

    meta = {
        "name": "persona",
        "version": "1.0.0",
        "description": f"{len(roles)} role personas as subagents and {len(index)} persona/audit skills",
        "license": "Apache-2.0",
        "keywords": ["persona", "audit", "agents", "skills"],
    }
    write(ROOT / ".claude-plugin/plugin.json", json.dumps(meta, indent=2) + "\n", args.check, stale)
    market = {
        "name": "persona",
        "owner": {"name": "legionir"},
        "plugins": [{**meta, "source": "./"}],
    }
    market["plugins"][0].pop("license")
    write(ROOT / ".claude-plugin/marketplace.json", json.dumps(market, indent=2) + "\n", args.check, stale)
    link(ROOT / ".claude/skills", "../skills", args.check, stale)
    link(ROOT / ".claude/agents", "../agents", args.check, stale)

    if args.check:
        if stale:
            print("stale:", *stale[:10], sep="\n  ")
            return 1
        print("ok")
        return 0
    print(f"agents: {len(roles)}  skills: {len(index)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
