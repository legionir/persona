# Persona library — one entry point for the whole generation pipeline.
#
# The canonical order matters: personas come from the README table, metadata
# and composites are derived from the personas, and skills are derived from
# both. Running the targets out of order produces stale output.
#
#   make            regenerate everything and validate
#   make check      validate only, write nothing
#   make test       run the web test (needs: npm install)
#   make serve      serve the site at http://localhost:8000

PY      ?= python3
NODE    ?= node
PORT    ?= 8000

SCRIPTS := scripts

.DEFAULT_GOAL := all
.PHONY: all prompts metadata composites skills validate check test serve clean help

## all: regenerate every artifact from its source, then validate
all: prompts metadata composites skills validate test

## prompts: role prompts + README links, from the README role table
prompts:
	$(PY) $(SCRIPTS)/generate_personas.py

## metadata: personas.json (the API/search view of the 170 role personas)
metadata:
	$(PY) $(SCRIPTS)/build_metadata.py

## composites: the 15 spec-driven composite master prompts
composites:
	$(PY) $(SCRIPTS)/compose_persona.py --all

## skills: 189 Agent Skills + skills/index.json + skills/README.md
skills:
	$(PY) $(SCRIPTS)/build_skills.py

## validate: every structural check, without writing anything
validate:
	$(PY) $(SCRIPTS)/validate_personas.py
	$(PY) $(SCRIPTS)/validate_composites.py
	$(PY) $(SCRIPTS)/validate_skills.py
	$(PY) $(SCRIPTS)/compose_persona.py --all --check
	$(PY) $(SCRIPTS)/build_skills.py --check

## check: validate and test, without writing anything
check: validate test

## test: the index.html functional test (skips if jsdom is missing)
test:
	$(NODE) $(SCRIPTS)/test_web.js

## serve: local preview of the Persona Finder
serve:
	$(PY) -m http.server $(PORT) --bind 0.0.0.0

## clean: Python bytecode caches
clean:
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +
	find . -name '*.pyc' -delete

## help: list the targets
help:
	@grep -E '^## ' $(MAKEFILE_LIST) | sed 's/^## //'
