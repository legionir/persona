# Contributing

Thanks for helping improve the persona library. Everything here is generated, so the
most useful thing you can do is change a **source** and let the pipeline do the rest.

## The one rule: never edit a generated file

These are derived. Editing them by hand is lost the next time anyone runs `make all`,
and CI fails the build if they drift:

| Generated | Rebuilt by | From |
|---|---|---|
| `prompts/audit/*.md`, `prompts/implementation/*.md` | `scripts/generate_personas.py` | the role table in `README.md` |
| `prompts/composite/*.md` (15 of them) | `scripts/compose_persona.py` | `composites/blocks/` + `composites/*.json` |
| `personas.json` | `scripts/build_metadata.py` | `README.md` + `prompts/composite/` |
| `skills/**` | `scripts/build_skills.py` | `prompts/**` |

Edit the source instead:

- **A role is wrong** → fix its row in the `README.md` role table (mission, duties, details), then `make prompts`.
- **A composite is wrong** → fix `composites/<slug>.json` or `composites/blocks/*.md`, then `make composites`.
- **A skill's shape is wrong** → fix `scripts/build_skills.py`, then `make skills`.

The four hand-maintained composites in `prompts/composite/` (`Architecture Review &
Architecture Audit.md`, `Forensic Codebase Review & Audit.md`, `Execution Plan
Generator.md`, `codebase-integrity-audit-protocol.md`) have no spec and are edited
directly — they are the exception.

## Before you open a pull request

```bash
make all      # regenerate everything from source
make check    # validate structure, composites, skills, and the web page
```

`make check` runs five gates:

| Gate | What it guarantees |
|---|---|
| `validate_personas.py` | 190 prompts match the README table, slugs and links agree |
| `validate_composites.py` | all 19 master prompts are English-only, copy-paste ready, and substantive |
| `validate_skills.py` | 218 skills have valid frontmatter, resolvable links, and a reference copy identical to its source |
| `compose_persona.py --all --check` | the 24 spec-driven composites re-render byte-for-byte |
| `build_skills.py --check` | the skills on disk match what the builder would produce |
| `scripts/test_web.js` | `index.html` renders all 218 personas, filters, sorts, and searches |

The web test needs `npm install` first (it is the only Node dependency in the repo;
the site itself has none).

## Content rules

- **English only.** No Persian text, no Persian headings. CI scans for it.
- **Copy-paste ready.** A master prompt must run when pasted into an AI session with
  repository access. No `fill in` blocks, no `<PLACEHOLDER>` fields.
- **No duplication.** Shared protocol lives in `composites/blocks/` and is included by
  spec; role rules are never copied into another role's prompt.
- **Progressive disclosure.** `SKILL.md` stays under the soft line budget and points at
  `references/` for the full contract.

## Adding a new role

1. Add a row to the role table in `README.md` (title, duties, type, group, and the
   detail columns).
2. Run `make prompts`.
3. Add its spec to `scripts/generate_role_prompts.py` if the generic one is not enough.

## Adding a new composite

See [`docs/composite-personas.md`](docs/composite-personas.md) — it walks through the
blocks, the spec format, and the quality checklist.

## Reporting a bug

Open an issue with the persona name and what you expected. If a prompt contradicts
itself, quote both sections — the block/spec split is the usual cause.
