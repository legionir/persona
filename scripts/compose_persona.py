#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a composite (ترکیبی) persona from reusable blocks + role lenses.

A composite persona is a single master prompt that acts as several roles at once
(e.g. "Forensic Codebase Review & Audit"). It is assembled from three sources:

  1. composites/blocks/*.md  — reusable protocol blocks (prime directive, phases,
     coverage matrix, finding format, report structure, quality gate).
  2. composites/<slug>.json  — the composite spec: mission, inputs, lenses,
     precedence, block order, extra domain sections.
  3. prompts/**/*.md         — the lens personas whose mission/authority/focus are
     folded into the lens table (§5 of the generated prompt).

Placeholders available inside blocks / spec text:

  {{TITLE}} {{VERSION}} {{DATE}} {{MISSION}} {{INPUTS}} {{ORDER}}
  {{LENS_TABLE}} {{LENS_COUNT}} {{PRECEDENCE}} {{EXTRA_SECTIONS}}

Usage:
    python3 scripts/compose_persona.py --list
    python3 scripts/compose_persona.py --spec composites/<slug>.json
    python3 scripts/compose_persona.py --all
    python3 scripts/compose_persona.py --all --check      # validate only
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from persona_lib import (  # noqa: E402
    BLOCKS, COMPOSITES, ROOT, RolePersona, bullets_of, clip, fields_of,
    frontmatter_problems, load_doc, rel, slugify, today,
)

SCHEMA = "composite-persona/v1"
PLACEHOLDER_RE = re.compile(r"\{\{[A-Z_]+\}\}")
DEFAULT_INSERT_BEFORE = "80-quality-gate.md"


# ---------------------------------------------------------------------------
# spec loading / validation
# ---------------------------------------------------------------------------
def spec_files() -> list[Path]:
    return sorted(p for p in COMPOSITES.glob("*.json") if not p.name.startswith("_"))


def load_spec(path: Path) -> dict:
    spec = json.loads(path.read_text(encoding="utf-8"))
    spec["_path"] = path
    return spec


def lens_rows(spec: dict) -> tuple[list[dict], list[str]]:
    """Collect (role title, type, focus, path) for every lens of a composite."""
    problems: list[str] = []
    rows: list[dict] = []
    focus_map = spec.get("lens_focus") or {}
    seen: set[str] = set()
    for entry in spec.get("lenses", []):
        p = (ROOT / entry).resolve() if not Path(entry).is_absolute() else Path(entry)
        if not p.exists():
            problems.append(f"lens path not found: {entry}")
            continue
        rp = RolePersona(p)
        if rp.kind != "role":
            problems.append(f"lens is not a role persona: {entry}")
            continue
        if rp.slug in seen:
            problems.append(f"duplicate lens: {entry}")
            continue
        seen.add(rp.slug)
        focus = focus_map.get(rp.title) or focus_map.get(rp.slug)
        if not focus:
            primary = bullets_of(rp.doc.find("Responsibilities").body) if rp.doc.find("Responsibilities") else []
            focus = ", ".join(primary[:3]) or rp.mission
        rows.append({
            "title": rp.title,
            "type": rp.type_label,
            "focus": clip(focus, 160),
            "path": rel(p),
            "mission": rp.mission,
            "allowed": rp.fld(r"^5\.", "AllowedDecisions"),
        })
    return rows, problems


def validate_spec(spec: dict) -> list[str]:
    problems: list[str] = []
    title = (spec.get("title") or "").strip()
    if not title:
        problems.append("title is empty")
    slug = spec.get("slug") or slugify(title)
    if frontmatter_problems(slug, spec.get("description") or spec.get("mission") or "x" * 10):
        problems.extend(f"slug: {p}" for p in frontmatter_problems(slug, spec.get("description") or spec.get("mission") or "x" * 10))
    if not (spec.get("mission") or "").strip():
        problems.append("mission is empty")
    elif len(spec["mission"]) < 40:
        problems.append("mission is too short to steer a composite (<40 chars)")
    if not spec.get("inputs"):
        problems.append("inputs block is empty")
    else:
        for i, inp in enumerate(spec["inputs"]):
            if not inp.get("name"):
                problems.append(f"inputs[{i}] has no name")
    lenses = spec.get("lenses") or []
    if not 2 <= len(lenses) <= 12:
        problems.append(f"lenses must contain 2..12 personas (got {len(lenses)})")
    rows, lens_problems = lens_rows(spec)
    problems.extend(lens_problems)
    blocks = spec.get("blocks") or []
    if not blocks:
        problems.append("blocks list is empty")
    for b in blocks:
        if not (BLOCKS / b).exists():
            problems.append(f"block not found: {b}")
    if len(set(blocks)) != len(blocks):
        problems.append("duplicate block in spec")
    if not (spec.get("precedence") or []):
        problems.append("precedence list is empty (conflict resolution is mandatory)")
    out = spec.get("output") or f"{title}.md"
    if out == "README.md":
        problems.append("output must not overwrite README.md")
    if spec.get("description") and len(spec["description"]) > 1024:
        problems.append("description > 1024 chars")
    return problems


# ---------------------------------------------------------------------------
# rendering
# ---------------------------------------------------------------------------
def render_lens_table(rows: list[dict]) -> str:
    head = "| Lens | Type | Primary focus |\n|---|---|---|"
    body = "\n".join(f"| {r['title']} | {r['type']} | {r['focus']} |" for r in rows)
    return f"{head}\n{body}"


def render_inputs(inputs: list[dict]) -> str:
    width = max(len(i["name"]) for i in inputs) + 2
    return "\n".join(f"{i['name'].ljust(width)}<{i.get('hint', '')}>" for i in inputs)


def render_precedence(precedence: list[str]) -> str:
    return "\n".join(f"{i}. {clip(p, 240)}" for i, p in enumerate(precedence, 1))


def render_extra_sections(spec: dict) -> str:
    out = []
    for extra in spec.get("extra_sections") or []:
        out.append(f"## {extra['title']}\n\n{extra['body'].strip()}\n\n---")
    return "\n\n".join(out)


def render_source_appendix(rows: list[dict], spec: dict) -> str:
    lines = [
        "## Appendix C — Source Personas (lenses)",
        "",
        "This composite was assembled from the following persona prompts. Their mission,",
        "authority, and scope are folded into the Lens Sweep section; the full contracts stay",
        "the source of truth:",
        "",
        "| Lens | Source persona | Allowed decisions |",
        "|---|---|---|",
    ]
    for r in rows:
        lines.append(f"| {r['title']} | [`{r['path']}`]({r['path']}) | {r['allowed'] or '—'} |")
    lines += [
        "",
        f"Generated by `scripts/compose_persona.py` from `{rel(spec['_path'])}` on {today()}.",
        "",
    ]
    return "\n".join(lines)


def renumber(text: str) -> str:
    """Re-number headings after assembly.

    Blocks carry fixed numbers so they read well standalone; a composite re-uses a
    subset of blocks plus extra sections, so numbers are re-derived at the end:
    `## N. Title` and `### N.M Title`. Headings whose title starts with "Appendix"
    stay unnumbered. Cross-references inside blocks use section *names* (never
    numbers) precisely so that this renumbering is safe.
    """
    out, n, m, inside_fence = [], 0, 0, False
    for ln in text.splitlines():
        if ln.strip().startswith("```"):
            inside_fence = not inside_fence
        if not inside_fence and ln.startswith("## ") and not ln.startswith("### "):
            title = re.sub(r"^##\s+(?:\d+\.\s+)?", "", ln).strip()
            if title.lower().startswith("appendix"):
                out.append(f"## {title}")
                continue
            n += 1
            m = 0
            out.append(f"## {n}. {title}")
            continue
        if not inside_fence and ln.startswith("### "):
            title = re.sub(r"^###\s+(?:\d+\.\d+\s+)?", "", ln).strip()
            if title.lower().startswith("appendix"):
                out.append(f"### {title}")
                continue
            m += 1
            out.append(f"### {n}.{m} {title}")
            continue
        out.append(ln)
    return "\n".join(out)


def render(spec: dict) -> tuple[str, list[dict], list[str]]:
    problems: list[str] = []
    rows, lens_problems = lens_rows(spec)
    problems.extend(lens_problems)
    blocks = spec.get("blocks") or []
    missing = [b for b in blocks if not (BLOCKS / b).exists()]
    problems.extend(f"block not found: {b}" for b in missing)

    values = {
        "{{TITLE}}": spec.get("title", ""),
        "{{VERSION}}": spec.get("version", "v1"),
        "{{DATE}}": today(),
        "{{MISSION}}": (spec.get("mission") or "").strip(),
        "{{INPUTS}}": render_inputs(spec.get("inputs") or [{"name": "TARGET", "hint": "what to audit"}]),
        "{{ORDER}}": spec.get("order", "intake → discovery → deep review → synthesis → report"),
        "{{LENS_TABLE}}": render_lens_table(rows),
        "{{LENS_COUNT}}": str(len(rows)),
        "{{PRECEDENCE}}": render_precedence(spec.get("precedence") or []),
        "{{EXTRA_SECTIONS}}": render_extra_sections(spec),
    }

    insert_before = spec.get("insert_before", DEFAULT_INSERT_BEFORE)
    parts: list[str] = []
    extras = render_extra_sections(spec)
    for b in blocks:
        if (BLOCKS / b).exists() and b == insert_before and extras:
            parts.append(extras)
        parts.append((BLOCKS / b).read_text(encoding="utf-8"))
    if extras and insert_before not in blocks:
        parts.append(extras)
    parts.append(render_source_appendix(rows, spec))

    text = "\n".join(parts)
    for key, value in values.items():
        text = text.replace(key, value)
    leftover = sorted(set(PLACEHOLDER_RE.findall(text)))
    if leftover:
        problems.append(f"unresolved placeholders: {', '.join(leftover)}")
    text = renumber(text)
    return text, rows, problems


# ---------------------------------------------------------------------------
# cli
# ---------------------------------------------------------------------------
def list_all() -> None:
    print("Blocks (composites/blocks/):")
    for b in sorted(BLOCKS.glob("*.md")):
        first = b.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
        print(f"  {b.name:28} {first}")
    print("\nComposite specs:")
    if not spec_files():
        print("  (none)")
    for s in spec_files():
        spec = load_spec(s)
        rows, _ = lens_rows(spec)
        print(f"  {s.name:44} {spec.get('title')} — {len(rows)} lenses")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec", help="path to a composite spec JSON")
    ap.add_argument("--all", action="store_true", help="build every spec in composites/")
    ap.add_argument("--check", action="store_true", help="validate only, do not write")
    ap.add_argument("--list", action="store_true", help="list blocks and specs")
    ap.add_argument("--out-dir", default=str(ROOT), help="output directory (default: repo root)")
    args = ap.parse_args()

    if args.list:
        list_all()
        return 0

    specs = spec_files()
    if args.spec:
        p = Path(args.spec)
        if not p.is_absolute():
            p = ROOT / p
        specs = [p]
    elif not args.all:
        ap.error("use --spec <file>, --all, or --list")

    failures = 0
    out_dir = Path(args.out_dir)
    for sp in specs:
        try:
            spec = load_spec(sp)
        except (json.JSONDecodeError, OSError) as exc:
            print(f"[FAIL] {rel(sp)}: {exc}")
            failures += 1
            continue
        problems = validate_spec(spec)
        text, rows, render_problems = render(spec)
        problems.extend(render_problems)
        title = spec.get("title") or sp.stem
        if problems:
            failures += 1
            print(f"[FAIL] {title}")
            for pr in problems:
                print("   -", pr)
            continue
        if args.check:
            print(f"[OK]   {title} — {len(rows)} lenses, "
                  f"{len(spec.get('blocks', []))} blocks, {len(text.splitlines())} lines")
            continue
        out = out_dir / (spec.get("output") or f"{title}.md")
        out.write_text(text.rstrip() + "\n", encoding="utf-8")
        print(f"[OK]   {title}\n       -> {rel(out)} "
              f"({len(rows)} lenses, {len(spec.get('blocks', []))} blocks, "
              f"{len(text.splitlines())} lines)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
