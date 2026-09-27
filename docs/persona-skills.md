# How to Turn a Persona into a Skill

> A skill is the *loadable* shape of a persona: a small `SKILL.md` that the model reads when a task
> matches, plus the full persona text as a reference (progressive disclosure).

---

## 1. Why a skill? (and why it is not just a prompt copy)

A persona prompt is 500 to 800 lines long. If you put all of it into the context every time,
it costs money, dilutes attention, and in practice never becomes "active". A skill solves the problem
with two layers:

| Layer | File | Size | When it is read |
|---|---|---|---|
| Trigger | `SKILL.md` (frontmatter) | ~300 characters | The model decides from `description` whether the skill is needed |
| Operational core | `SKILL.md` (body) | ~100-300 lines | When the skill is invoked |
| Full reference | `references/<persona>.md` | The entire prompt | Only when the contract details are needed |

So converting to a skill means **distilling the operational core while keeping the full text as a reference**, not a raw copy.

---

## 2. Output anatomy

```
skills/
├── README.md                 # the English catalogue of every skill
├── index.json                # machine-readable metadata (like personas.json)
├── backend-developer/
│   ├── SKILL.md              # frontmatter + operational core
│   └── references/persona.md # the full persona text (for role personas)
├── forensic-codebase-review-audit/
│   ├── SKILL.md
│   └── references/forensic-codebase-review-audit.md   # the full master prompt
└── …
```

### Frontmatter

```yaml
---
name: "backend-developer"                 # lowercase letters/digits/hyphen, <= 64 chars, = the folder name
description: "Persona \"Backend Developer\" (EXECUTOR) …"   # <= 1024 chars; this is the skill trigger
metadata:
  version: "1"
  type: "EXECUTOR"          # or SUPERVISOR / COMPOSITE
  typeLabel: "EXECUTOR"
  domain: "Software"
  seniority: "Mid"
  source: "prompts/implementation/backend-developer.md"
  language: "en"
---
```

### The `SKILL.md` body for a role persona

`Trigger` → mission and success criteria → authority and boundaries → inputs → preconditions → scope →
tools → evidence → risks → KPIs → execution steps → decision rules → Quality Gate → absolute rules →
report/output structure → handoff and escalation → the pointer to `references/`.

### The `SKILL.md` body for a composite persona

`Trigger` (from the mission) → required inputs → non-negotiable rules → execution phases →
the severity table → the finding format → the report structure → the Quality Gate → the governing principle → the pointer to `references/`.

---

## 3. Commands

```bash
# build every skill (170 role personas + the composites)
python3 scripts/build_skills.py

# only a few
python3 scripts/build_skills.py --only backend-developer --only audit-specialist

# only a subset (a glob relative to the root)
python3 scripts/build_skills.py --source "prompts/audit/*.md"

# without copying the full text (SKILL.md only, lighter)
python3 scripts/build_skills.py --no-bundle

# validate without writing anything
python3 scripts/validate_skills.py
python3 scripts/build_skills.py --check
```

Orphaned structures (skills whose persona was deleted) are pruned automatically on a full run.

---

## 4. Validation (`validate_skills.py`)

| Check | Why |
|---|---|
| frontmatter and `name` are present | Without them the skill does not load |
| `name` equals the folder name, `^[a-z0-9-]+$`, <= 64 | The Agent Skills contract |
| `description` is non-empty and <= 1024 | The trigger; longer means ineffective |
| The internal `SKILL.md` links resolve | A broken pointer is a lost reference |
| `SKILL.md` is <= 300 lines (soft) | Otherwise progressive disclosure becomes meaningless |
| `index.json` matches the folders | Do not build a lying catalogue |

Successful output: `ALL CHECKS PASSED.`

---

## 5. Install and use

### Claude Code (project)

```bash
mkdir -p .claude/skills
cp -r skills/backend-developer .claude/skills/
# or all of them:
for d in skills/*/; do cp -r "$d" .claude/skills/; done
```

Then you only have to write the task ("run a forensic audit on this repo"); the model decides from
`description` which skill to invoke.

### Claude.ai / API

Import the contents of the skill folder into the skill environment (or send the request with the contents of `SKILL.md` +
`references/`). For the API, each skill is a `container` with its own files.

### An important note for supervisor personas

Supervisor personas are read-only; the skill text says so too. If you want it enforced strictly,
restrict write permission in the environment settings (a skill on its own does not create a tool restriction).

---

## 6. The golden rule for writing a good `description`

The description is a trigger, not an introduction. Three components are required:

1. **Who/what** — "Persona \"Backend Developer\" (EXECUTOR) in the Software domain".
2. **What it does** — "Backend implementation … output: Backend Code, Tests, API Docs".
3. **When** — "Use when …".

Good: "… Rollback/Restore/Migration … before release, for production readiness."
Bad: "A very complete, professional persona for backend development." (no trigger at all)

Limits: `name` <= 64 characters, `description` <= 1024 characters.

---

## 7. Troubleshooting

| Problem | Solution |
|---|---|
| The skill is never invoked | Rewrite `description` around "when"; use the task's own keywords |
| The model does not know the contract details | Point explicitly at `references/…md` in `SKILL.md` (it is always at the end of the file) |
| `SKILL.md` grew past 300 lines | Move the detail into `references/` (the script warns you) |
| `validate_skills.py` reports a broken link | Run the script again; the links are derived from the reference file names |
| I built a new composite but it has no skill | `python3 scripts/build_skills.py` (it walks `prompts/` and `prompts/composite/`) |

---

## 8. The full workflow (role → composite → skill)

```bash
# 1) the role personas (whenever README/generator changes)
python3 scripts/generate_personas.py
python3 scripts/build_metadata.py

# 2) build / rebuild the composite
python3 scripts/compose_persona.py --all

# 3) turn every persona into a skill
python3 scripts/build_skills.py

# 4) validate
python3 scripts/validate_personas.py
python3 scripts/validate_skills.py
```
