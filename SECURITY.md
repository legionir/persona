# Security Policy

## What this repository is

This repository is a library of **AI persona prompts** and **Agent Skills**. It contains
no application code, no credentials, and no network services. The files are static
Markdown, JSON, Python generators, and one HTML page.

## Reporting a vulnerability

If you find a security problem — for example a prompt that instructs an agent to
exfiltrate data, ignore a permission boundary, or run a destructive command — please
report it privately rather than opening a public issue.

- Open an issue titled `security` and ask for a private follow-up, **or**
- contact the maintainers through GitHub.

Please include:

- the affected file path (`prompts/…`, `skills/…`, `composites/…`)
- the exact text that is unsafe
- what an agent following it could do

## What counts as a security issue here

| Yes | No |
|---|---|
| A prompt that tells the agent to bypass a permission check | A prompt that is merely strict or verbose |
| A prompt that instructs running a destructive command against real data | A prompt that forbids destructive commands (all of them do) |
| A generator script that writes outside the repository | A generator that rewrites generated files |
| A committed credential or secret | A missing feature |

Every composite master prompt is explicitly **read-only and non-destructive**: it must
never modify source, configuration, or data, and never run destructive commands,
migrations against real data, or calls to external services with real credentials. If
you find one that does not say this, that is a bug.

## Response

There is no formal SLA. Reports are acknowledged as time allows, and fixes ship through
the normal pipeline — `make all` then `make check` — so a corrected prompt reaches every
derived artifact at once.
