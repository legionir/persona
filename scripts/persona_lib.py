#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared helpers for persona tooling.

Used by:
  - scripts/compose_persona.py   (build a composite / ترکیبی persona from blocks + lenses)
  - scripts/build_skills.py      (turn personas into Agent Skills)
  - scripts/validate_skills.py   (validate the generated skills)

The library is intentionally dependency-free (stdlib only) and tolerant: persona
files come in two shapes and neither is guaranteed to be complete.

Two persona shapes are recognised:

  kind = "role"    ->  prompts/<audit|implementation>/<slug>.md
                       Persian, numbered sections 1..29, `# Persona — <Role>`.
  kind = "master"  ->  <Root>/*.md  (e.g. "Forensic Codebase Review & Audit.md")
                       English composite master prompt: free-form headings.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPTS = ROOT / "prompts"
SKILLS = ROOT / "skills"
COMPOSITES = ROOT / "composites"
BLOCKS = COMPOSITES / "blocks"

# Root-level markdown files that are NOT personas.
NON_PERSONA_MD = {"README.md"}

# Agent Skill frontmatter limits (see docs/persona-skills.md).
NAME_MAX = 64
DESC_MAX = 1024
SKILL_LINES_SOFT_MAX = 300

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
# `- **Key:** value` and the generated variant `- **Key:value` (no space/asterisks)
FIELD_RE = re.compile(r"^-\s+\*\*(.+?):\*\*\s*(.*)$|^-\s+\*\*([^:*]+?):\s*(.*)$")
STEP_RE = re.compile(r"^###\s+(STEP\s+\d+[^\n]*)$", re.M)


# ---------------------------------------------------------------------------
# markdown structure
# ---------------------------------------------------------------------------
@dataclass
class Section:
    level: int
    title: str
    body: str
    index: int = 0

    @property
    def flat_title(self) -> str:
        return self.title.strip()


@dataclass
class Doc:
    """A parsed markdown document: preamble + flat list of sections."""

    path: Path
    text: str
    preamble: str = ""
    sections: list[Section] = field(default_factory=list)

    def find(self, *patterns: str, regex: bool = False) -> Section | None:
        """First section whose title matches any pattern (substring or regex)."""
        for sec in self.sections:
            for pat in patterns:
                if (re.search(pat, sec.title, re.I) if regex else pat.lower() in sec.title.lower()):
                    return sec
        return None

    def find_at(self, *patterns: str, levels: tuple[int, ...] = (1, 2),
                regex: bool = False) -> Section | None:
        """First section at one of `levels` whose title matches any pattern."""
        for sec in self.sections:
            if sec.level not in levels:
                continue
            for pat in patterns:
                if (re.search(pat, sec.title, re.I) if regex else pat.lower() in sec.title.lower()):
                    return sec
        return None

    def find_all(self, *patterns: str, regex: bool = False) -> list[Section]:
        out = []
        for sec in self.sections:
            for pat in patterns:
                if (re.search(pat, sec.title, re.I) if regex else pat.lower() in sec.title.lower()):
                    out.append(sec)
                    break
        return out

    def section(self, title: str) -> Section | None:
        return self.find(title)


def split_sections(text: str, path: Path | None = None) -> Doc:
    """Split markdown into a preamble plus a flat list of heading-delimited sections.

    Sub-headings become their own Section (body stops at the next heading of any
    level), so callers can address `## 13. Procedure` and its `### STEP …` cards
    independently.
    """
    lines = text.splitlines()
    doc = Doc(path=path or Path("<memory>"), text=text)
    preamble: list[str] = []
    sections: list[Section] = []
    cur_title, cur_level, cur_lines = None, 0, []

    def flush() -> None:
        nonlocal cur_lines
        if cur_title is not None:
            body = "\n".join(cur_lines).strip("\n")
            sections.append(Section(level=cur_level, title=cur_title, body=body, index=len(sections)))

    for ln in lines:
        m = HEADING_RE.match(ln)
        if m:
            flush()
            if cur_title is None:
                doc.preamble = "\n".join(preamble).strip("\n")
            cur_level, cur_title, cur_lines = len(m.group(1)), m.group(2), []
        elif cur_title is None:
            preamble.append(ln)
        else:
            cur_lines.append(ln)
    flush()
    if cur_title is None:
        doc.preamble = "\n".join(preamble).strip("\n")
    doc.sections = sections
    return doc


def load_doc(path: Path) -> Doc:
    return split_sections(path.read_text(encoding="utf-8"), path)


def section_block(doc: Doc, *patterns: str, regex: bool = True) -> str:
    """Text of a section **plus** all of its sub-sections.

    Master prompts put most of their content under `###` children (e.g. "Part V —
    Final Report Structure" is nearly empty itself), so extraction has to walk the
    sub-tree, not just the section body. Top-level (`##`) matches win over deeper
    ones, so "Phase 7 — Report Emission" never shadows "Part V — Final Report
    Structure".
    """
    sec = None
    for levels in ((1, 2), (3, 4, 5, 6)):
        sec = doc.find_at(*patterns, levels=levels, regex=regex)
        if sec:
            break
    if not sec:
        return ""
    parts = [sec.body]
    for nxt in doc.sections[doc.sections.index(sec) + 1:]:
        if nxt.level <= sec.level:
            break
        parts.append(f"### {nxt.title}\n{nxt.body}".rstrip())
    return "\n\n".join(p for p in parts if p.strip())


# ---------------------------------------------------------------------------
# persona field extraction (Persian role files)
# ---------------------------------------------------------------------------
def fields_of(body: str) -> dict[str, str]:
    """Parse `- **Key:** value` bullets into a dict.

    Values may continue on following lines (until the next `- **Key:**` bullet);
    nested plain bullets (the list values of a key) are folded with `, ` separators.
    """
    out: dict[str, str] = {}
    cur: str | None = None
    for raw in body.splitlines():
        s = raw.strip()
        m = FIELD_RE.match(s) if s.startswith("-") else None
        if m:
            cur = (m.group(1) or m.group(3) or "").strip()
            value = (m.group(2) if m.group(1) else m.group(4) or "").strip()
            out[cur] = re.sub(r"^-\s+", "", value).strip()
        elif cur is not None:
            if not s or s == "---":
                continue
            s = re.sub(r"^-\s+", "", s)
            if s.startswith("**") and s.endswith(":**"):
                s = s[2:-3]
            out[cur] = (out[cur] + ", " + s).strip(", ") if out[cur] else s
    return out


def bullets_of(body: str, prefix: str = "- ") -> list[str]:
    out = []
    for raw in body.splitlines():
        s = raw.strip()
        if s.startswith(prefix):
            s = s[len(prefix):].strip()
            if s:
                out.append(s)
    return out


def numbered_of(body: str) -> list[str]:
    """First line of every `N. item` list entry (used to compress long reports)."""
    out = []
    for raw in body.splitlines():
        m = re.match(r"^\s*(\d+)\.\s+(.*)$", raw)
        if m:
            out.append(m.group(2).strip())
    return out


def checkbox_of(body: str) -> list[str]:
    return [re.sub(r"^- \[[ xX]\]\s*", "", ln.strip())
            for ln in body.splitlines() if ln.strip().startswith("- [")]


def bold_lead_lines(body: str, limit: int = 12) -> list[str]:
    """Lines that start with bold text (phase/protocol headers), compressed."""
    out = []
    for ln in body.splitlines():
        s = ln.strip()
        if s.startswith("**") and "—" in s or s.startswith("**Phase"):
            out.append(re.sub(r"\*\*", "", s).rstrip("."))
        if len(out) >= limit:
            break
    return out


def key_rules(text: str, limit: int = 10) -> list[str]:
    """The load-bearing rules of a section: blockquotes first, then substantial bullets."""
    out: list[str] = []
    for ln in text.splitlines():
        s = ln.strip()
        if s.startswith(">"):
            q = s.lstrip("> ").strip()
            if q:
                out.append(q)
    for b in bullets_of(text):
        if len(b) >= 60 or "**" in b:
            out.append(b)
    seen, uniq = set(), []
    for r in out:
        k = r.lower()[:60]
        if k not in seen:
            seen.add(k)
            uniq.append(r)
    return uniq[:limit]


def code_blocks(body: str) -> list[str]:
    """Contents of every fenced code block, in order."""
    out, cur, inside = [], [], False
    for ln in body.splitlines():
        if ln.strip().startswith("```"):
            if inside:
                out.append("\n".join(cur).strip("\n"))
                cur = []
            inside = not inside
            continue
        if inside:
            cur.append(ln)
    return out


# ---------------------------------------------------------------------------
# identity helpers
# ---------------------------------------------------------------------------
def detect_kind(text: str) -> str:
    return "role" if "# Persona — " in text else "master"


def slugify(text: str, max_len: int = NAME_MAX) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").lower()
    s = re.sub(r"-{2,}", "-", s)
    return (s[:max_len].strip("-") or "persona")


def today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def truncate(text: str, max_lines: int, note: str = "") -> str:
    lines = text.splitlines()
    if len(lines) <= max_lines:
        return text
    kept = "\n".join(lines[:max_lines]).rstrip()
    tail = note or f"… (+{len(lines) - max_lines} خط دیگر — متن کامل در `references/`)"
    return f"{kept}\n\n> {tail}"


def clip(text: str, max_chars: int) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= max_chars else text[: max_chars - 1].rstrip() + "…"


# ---------------------------------------------------------------------------
# role persona accessors
# ---------------------------------------------------------------------------
class RolePersona:
    """Structured view over a `prompts/**/<slug>.md` persona file."""

    def __init__(self, path: Path):
        self.path = path
        self.doc = load_doc(path)
        self.text = self.doc.text
        self.kind = detect_kind(self.text)
        self.slug = path.stem
        self.folder = path.parent.name
        self.f = {sec.title: fields_of(sec.body) for sec in self.doc.sections}

    def sec(self, *patterns: str) -> Section | None:
        return self.doc.find(*patterns)

    def fld(self, section_pattern: str, key: str, default: str = "") -> str:
        for sec in self.doc.sections:
            if re.search(section_pattern, sec.title, re.I):
                v = fields_of(sec.body).get(key)
                if v:
                    return v
        return default

    @property
    def title(self) -> str:
        m = re.search(r"^#\s*Persona\s*—\s*(.+)$", self.text, re.M)
        return m.group(1).strip() if m else self.slug

    @property
    def role_type(self) -> str:
        t = self.fld(r"^4\.", "Type") or self.fld(r"^1\.", "Type")
        return "SUPERVISOR" if "SUPERVISOR" in t.upper() else "EXECUTOR"

    @property
    def type_label(self) -> str:
        return "ناظر" if self.role_type == "SUPERVISOR" else "مجری"

    @property
    def domain(self) -> str:
        return self.fld(r"^1\.", "Domain") or self.fld(r"^1\.", "Group")

    @property
    def seniority(self) -> str:
        return self.fld(r"^1\.", "Seniority")

    @property
    def mission(self) -> str:
        return self.fld(r"^2\.", "PrimaryGoal")

    @property
    def steps(self) -> list[str]:
        return [h for h, _ in self.step_bodies()]

    def step_bodies(self) -> list[tuple[str, str]]:
        """(step header, step body) pairs from the Procedure section.

        Sections are split flat, so the `### STEP n` cards are siblings of
        `## 13. Procedure`; collect the run of STEP cards that follows it.
        """
        idx = None
        for i, sec in enumerate(self.doc.sections):
            if re.match(r"^\d+\.\s*Procedure", sec.title):
                idx = i
                break
        if idx is None:
            return []
        out: list[tuple[str, str]] = []
        for sec in self.doc.sections[idx + 1:]:
            if not re.match(r"^STEP\s+\d+", sec.title):
                break
            out.append((sec.title, sec.body))
        return out


class MasterPersona:
    """Structured view over a composite (ترکیبی) master prompt at repo root."""

    def __init__(self, path: Path):
        self.path = path
        self.doc = load_doc(path)
        self.text = self.doc.text
        self.kind = detect_kind(self.text)
        self.slug = slugify(path.stem)
        self.title = re.sub(r"^#\s*", "", self.text.splitlines()[0]).strip() if self.text else path.stem

    def sec(self, *patterns: str, regex: bool = False):
        return self.doc.find(*patterns, regex=regex)

    def first_paragraph(self) -> str:
        """The mission paragraph: prefer an explicit mission section, else the first
        substantial prose paragraph that is not a usage note."""
        skip = ("**how to use", "how to use", "**order of operations", "fill in the inputs")
        candidates = [self.doc.find(r"MISSION|Role and Mission|Role & Mission", regex=True)]
        candidates += self.doc.sections[:8]
        for sec in candidates:
            if not sec:
                continue
            for para in sec.body.split("\n\n"):
                p = para.strip()
                if len(p) < 80 or p.startswith(("|", "```", "-", ">", "#")):
                    continue
                if any(p.lower().startswith(s) for s in skip):
                    continue
                return p
        return ""

    def phase_lines(self) -> list[str]:
        """Ordered phase list: from `### Phase N — Title` headings and `**Phase N — …**` lines."""
        out: list[str] = []
        for sec in self.doc.sections:
            m = re.match(r"^(Phase\s+\S+|P\d+)\s*[—–-]\s*(.+)$", sec.title.strip())
            if m:
                out.append(f"{m.group(1)} — {m.group(2).strip()}")
        for sec in self.doc.sections:
            for ln in sec.body.splitlines():
                s = re.sub(r"\*\*", "", ln.strip())
                m = re.match(r"^(Phase\s+\S+|P\d+)\s*[—–-]\s*(.+)$", s)
                if m and len(s) < 400:
                    title = m.group(1).rstrip(".")
                    detail = clip(m.group(2).strip().rstrip("."), 130)
                    out.append(f"{title} — {detail}" if detail else title)
        seen, uniq = set(), []
        for line in out:
            key = line.split("—")[0].strip().lower()
            if key not in seen:
                seen.add(key)
                uniq.append(line)
        return uniq


# ---------------------------------------------------------------------------
# discovery
# ---------------------------------------------------------------------------
def master_personas() -> list[Path]:
    return sorted(p for p in ROOT.glob("*.md") if p.name not in NON_PERSONA_MD)


def role_personas() -> list[Path]:
    return sorted(p for p in PROMPTS.rglob("*.md") if p.name != "README.md")


# ---------------------------------------------------------------------------
# frontmatter
# ---------------------------------------------------------------------------
def yaml_scalar(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    s = str(value).replace("\\", "\\\\").replace('"', '\\"')
    s = s.replace("\n", " ")
    return f'"{s}"'


def frontmatter(data: dict) -> str:
    lines = ["---"]
    for k, v in data.items():
        if v is None:
            continue
        if isinstance(v, dict):
            lines.append(f"{k}:")
            for k2, v2 in v.items():
                if v2 is None:
                    continue
                lines.append(f"  {k2}: {yaml_scalar(v2)}")
        else:
            lines.append(f"{k}: {yaml_scalar(v)}")
    lines.append("---")
    return "\n".join(lines)


def frontmatter_problems(name: str, description: str) -> list[str]:
    problems = []
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name or ""):
        problems.append(f"name '{name}' must be lowercase letters/digits/hyphens")
    if not 1 <= len(name or "") <= NAME_MAX:
        problems.append(f"name length {len(name or '')} outside 1..{NAME_MAX}")
    if not description or not description.strip():
        problems.append("description is empty")
    elif len(description) > DESC_MAX:
        problems.append(f"description length {len(description)} > {DESC_MAX}")
    return problems


# ---------------------------------------------------------------------------
# personas.json (metadata index) accessors
# ---------------------------------------------------------------------------
def load_personas_index() -> dict[str, dict]:
    import json

    p = ROOT / "personas.json"
    if not p.exists():
        return {}
    return {r["id"]: r for r in json.loads(p.read_text(encoding="utf-8")).get("roles", [])}
