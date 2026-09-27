#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate the composite master prompts in prompts/composite/.

`compose_persona.py --all --check` covers the 15 spec-driven composites: it
re-renders them from `composites/blocks/` + `composites/<slug>.json` and fails
if the file on disk differs. The 4 hand-maintained composites have no spec and
are therefore invisible to that check.

This script covers all 19 and asserts the properties the pipeline itself does
not guarantee. The checks are deliberately narrow — they target exactly the
artefacts that were removed, not the English words that happen to appear in
legitimate prose:

  1. English only — no Arabic-script characters, no guillemets.
  2. Copy-paste ready — no fill-in placeholder left behind:
       - a heading that says "fill in" (the removed `## INPUTS (fill in ...)`)
       - a run of >= 2 consecutive `ALL_CAPS_NAME: <hint>` form fields
         (the removed `CODEBASE: / REPORT_LANGUAGE: / ...` blocks). A single
         such line is a legitimate finding-record field, so runs matter.
       - a `{PASTE THE FULL TASK DESCRIPTION...}` token
  3. No unrendered `{{TITLE}}`-style template markers.
  4. Substantive — long enough to be a master prompt, opens with an `# ` title
     that matches the file name, and carries a framing heading.

Usage:
    python3 scripts/validate_composites.py
    python3 scripts/validate_composites.py --dir prompts/composite
    python3 scripts/validate_composites.py --english-only     # subset 1
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from persona_lib import MASTERS, rel  # noqa: E402

# Arabic, Arabic Supplement, Arabic Extended-A, Arabic Presentation Forms
ARABIC_RE = re.compile(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]")
# Guillemets are the other leftover of the Persian origin.
GUILLEMET_RE = re.compile(r"[«»‹›]")

# `CODEBASE:   <repo URL, path, or "attached files">`
FORM_FIELD_RE = re.compile(r"^\s*[A-Z][A-Z0-9_ ]{2,}:\s*<[^>]*>\s*$")
FILL_IN_HEADING_RE = re.compile(r"^#+.*\bfill[\s-]?in\b.*$", re.M | re.I)
PLACEHOLDER_TOKEN_RE = re.compile(r"\{\{[A-Z_]+\}\}")
PASTE_TOKEN_RE = re.compile(r"\{PASTE\b")

# Framing headings — every composite states its mission or its purpose up front.
FRAMING_RE = re.compile(
    r"^#+\s*.*\b(Mission|Purpose|Role and Mission|How to use|Protocol)\b",
    re.M | re.I,
)

MIN_LINES = 40      # a master prompt shorter than this is a stub
MIN_CHARS = 2000
MIN_FORM_RUN = 2    # consecutive `NAME: <hint>` lines that mean a fill-in form


def line_no(text: str, idx: int) -> int:
    return text.count("\n", 0, idx) + 1


def form_field_runs(lines: list[str]) -> list[list[int]]:
    """Runs of consecutive fill-in form fields, with their 1-based line numbers."""
    runs: list[list[int]] = []
    current: list[int] = []
    for i, ln in enumerate(lines, start=1):
        if FORM_FIELD_RE.match(ln):
            current.append(i)
        elif current:
            runs.append(current)
            current = []
    if current:
        runs.append(current)
    return runs


def check_file(path: Path) -> list[str]:
    problems: list[str] = []
    text = path.read_text(encoding="utf-8")
    name = rel(path)
    lines = text.splitlines()

    # --- 1. English only -------------------------------------------------
    m = ARABIC_RE.search(text)
    if m:
        ln = line_no(text, m.start())
        problems.append(f"{name}:{ln}: non-Latin script "
                        f"({unicodedata.name(m.group(0), '?')}): "
                        f"{lines[ln - 1].strip()[:70]}")
    m = GUILLEMET_RE.search(text)
    if m:
        ln = line_no(text, m.start())
        problems.append(f"{name}:{ln}: guillemet '{m.group(0)}' "
                        f"left from the Persian source")

    # --- 2. copy-paste ready --------------------------------------------
    for m in FILL_IN_HEADING_RE.finditer(text):
        problems.append(f"{name}:{line_no(text, m.start())}: fill-in heading "
                        f"'{m.group(0).strip()}' — remove the placeholder")
    for run in form_field_runs(lines):
        if len(run) >= MIN_FORM_RUN:
            problems.append(
                f"{name}:{run[0]}-{run[-1]}: fill-in form block "
                f"({len(run)} fields) — remove the placeholder")
    m = PASTE_TOKEN_RE.search(text)
    if m:
        problems.append(f"{name}:{line_no(text, m.start())}: "
                        f"paste-the-task placeholder left in the prompt")

    # --- 3. no leftover template markers --------------------------------
    for m in PLACEHOLDER_TOKEN_RE.finditer(text):
        problems.append(f"{name}:{line_no(text, m.start())}: unrendered "
                        f"placeholder {m.group(0)}")

    # --- 4. substantive --------------------------------------------------
    if len(lines) < MIN_LINES:
        problems.append(f"{name}: only {len(lines)} lines — "
                        f"a master prompt needs >= {MIN_LINES}")
    if len(text) < MIN_CHARS:
        problems.append(f"{name}: only {len(text)} chars — "
                        f"a master prompt needs >= {MIN_CHARS}")
    if not lines or not lines[0].startswith("# "):
        problems.append(f"{name}: does not open with an '# ' title")
    else:
        title = lines[0][2:].strip()
        # The stem has no spaces, so compare on words: at least the first two
        # words of the file name must appear in the title. The title itself may
        # legitimately be longer (e.g. "... (v2, single file)").
        stem_words = [w for w in re.split(r"[-_]", path.stem.lower()) if w]
        title_norm = re.sub(r"[-_]", " ", title.lower())
        missing = [w for w in stem_words[:2] if w not in title_norm]
        if missing:
            problems.append(f"{name}: title '{title}' does not match "
                            f"the file name (missing: {', '.join(missing)})")
    if not FRAMING_RE.search(text):
        problems.append(f"{name}: no framing heading "
                        f"(Mission / Purpose / Protocol / How to use)")

    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dir", default=str(MASTERS),
                    help=f"composite directory (default: {rel(MASTERS)})")
    ap.add_argument("--english-only", action="store_true",
                    help="run only the Arabic-script / guillemet scan")
    args = ap.parse_args(argv)

    root = Path(args.dir)
    if not root.exists():
        print(f"no composite directory at {rel(root)}")
        return 1

    files = sorted(root.glob("*.md"))
    if not files:
        print(f"no composite master prompts in {rel(root)}")
        return 1

    problems: list[str] = []
    for f in files:
        text = f.read_text(encoding="utf-8")
        if args.english_only:
            m = ARABIC_RE.search(text) or GUILLEMET_RE.search(text)
            if m:
                ln = line_no(text, m.start())
                problems.append(f"{rel(f)}:{ln}: "
                                f"{unicodedata.name(m.group(0), m.group(0))}")
        else:
            problems.extend(check_file(f))

    print(f"Composite master prompts: {len(files)} in {rel(root)}")
    if problems:
        print(f"PROBLEMS: {len(problems)}")
        for pr in problems[:60]:
            print(" -", pr)
        return 1
    print("ALL CHECKS PASSED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
