## PRAGMATIC CONTRACT — The Pragmatic Programmer (binding)

This contract governs **how the work is done**: duplicated knowledge, coupling between concerns,
feedback speed, automation, and the discipline of leaving code easier to change. The Construction
Contract governs the *inside* of routines, names, data, and tests; the Design Depth and Architecture
Boundaries contracts govern *structure*; this contract governs *working habits that show up in the
code*. It does not weaken the Prime Directive (§3): evidence rules still govern every claim made
about the target.

**Force of the rules.** Every unqualified rule below is `MUST`; `Prefer` is `SHOULD`; `Do not`,
`Avoid`, and `Never` are `MUST NOT` — unless the user explicitly overrides it, in which case the
conflict is stated rather than silently applied.

### 1. Be pragmatic, not dogmatic

- When uncertain, choose the option that reduces knowledge duplication, keeps concerns independent, shortens feedback loops, leaves the system easier to change, and makes intent clearer to future maintainers.
- Do not follow style or process rituals that do not improve outcomes, and do not blame tooling, framework defaults, or «existing style» for avoidable bad design.
- Take responsibility for the quality and changeability of the code you touch, and surface trade-offs, risks, and uncertainty explicitly.
- Every change affects future maintainability: a small quick fix that multiplies future cost is a bad bargain. The Boy Scout Rule from the Construction Contract applies — this adds that the *area* should be better, not only the touched lines.
- Watch for entropy: do not normalize local decay, fix small quality problems before they signal that nobody cares, and never leave a «temporary» hack with no cleanup plan.

### 2. DRY means duplicated knowledge, not duplicated text

- A business rule has one authoritative representation. Validation for the same concept is not scattered, status semantics and calculations are not copied across layers, and configuration and schema meaning is not repeated inconsistently.
- Do not encode the same rule in UI, API, service, and database trigger with no owner; do not copy/paste with minor edits for «just this one case»; do not keep one concept with several partially aligned implementations.
- The Construction Contract requires eliminating duplicated *code* and the Design Depth contract governs *combining and separating* it; this adds the cross-layer test: if the same *rule* is expressed twice in different vocabularies, one of them is wrong and neither owns the rule.
- Where two use cases genuinely change for different actors, the Architecture Boundaries contract's exception applies — duplicating is cheaper than coupling them.

### 3. Orthogonality

- Keep components independent so one change does not force unrelated changes elsewhere, and minimize hidden coupling through globals, ambient context, or shared mutable state.
- Avoid overlapping responsibilities between modules, and separate policy from mechanism, data from presentation, and orchestration from computation.
- Do not let one module know too much about the internals of others, and do not let a shared utility module create sideways coupling everywhere.
- Orthogonality is measured by blast radius: a change that requires edits in many unrelated places is the finding, regardless of how clean each file looks.

### 4. Tracer bullets and incremental delivery

- Prefer a thin end-to-end slice over a pile of isolated pieces: validate architecture, integration, and assumptions early with something real enough to prove the path.
- Refine from working feedback instead of predicting everything up front; do not build many layers before anything runs end to end, and do not wait for perfect certainty before integrating.
- Use prototypes to learn, not to pretend you are done. State explicitly what a prototype proves and what it does not, and never let experimental shortcuts silently become production defaults.
- Break work into pieces that can be reasoned about, tested, and corrected, and make risk visible early rather than reporting large hidden progress.

### 5. Automation and tooling

- Automate repetitive, error-prone, or easy-to-forget tasks, and prefer repeatable scripts over tribal-knowledge commands.
- Build, test, lint, format, package, and deploy steps must be reproducible and aligned between local automation and the project's shared pipeline.
- Do not hand-do tasks that should be scripted, and do not write documentation that describes what a script should do instead of having the script.
- Use code generators to remove duplicated mechanical work, but keep the source specification authoritative; never rely on generated code, tools, or specifications you do not understand.
- Keep editor, formatter, lint, tests, and local scripts aligned with team standards, and improve the toolchain when repeated friction appears.

### 6. Feedback loops

- Shorten the time between change and feedback, run relevant tests early and often, and prefer a cheap early signal over a late expensive surprise.
- Use automated checks where they reduce real risk, and make failure visible fast.
- When debugging, do not guess: reproduce, observe, isolate, explain, fix, and verify. An unexplained fix is an open defect.

### 7. Contracts, assumptions, and resources

- Make assumptions explicit in code rather than in comments, and keep contracts close to the abstraction they protect. Assertions, validation, and domain errors are already separated by the Construction Contract; this adds that the distinction must survive to the caller.
- Detect errors close to their source, never discard useful error context, and let callers distinguish retryable, recoverable, and permanent failures where relevant.
- Finish what you start: release every resource you acquire, preferably in the opposite order from acquisition, and keep resource ownership local and explicit.
- Avoid temporal coupling — make ordering requirements explicit or remove them. Reveal only necessary information between modules, and use metaprogramming only when it reduces duplication without hiding behaviour.
- Understand algorithmic growth before writing or accepting performance-sensitive code.

### 8. Communication is part of the work

- Code is communication first: use names that reflect domain meaning and developer intent, and prefer clarity over cleverness. Naming rules stay with the Construction Contract and the Domain Model contract.
- Write comments and documents where they convey decision rationale, contracts, or non-obvious behaviour — not where they narrate the code.
- Treat docs, commit messages, scripts, and tests as engineering artifacts that must communicate intent, and favor inspectable plain text for long-lived automation, configuration, and integration.
- Be skeptical of methods, diagrams, and ceremonies that do not improve the work.

### 9. Pragmatic review gate — for the change itself, not for the audit

Before presenting any change produced during this work, verify:

- [ ] Duplicated knowledge was reduced, not just duplicated lines
- [ ] Responsibilities are more orthogonal after the change, with no new hidden coupling
- [ ] Feedback is faster or unchanged, with no new manual step
- [ ] Something repetitive was automated if it was hurting reliability
- [ ] Contracts and assumptions are explicit in code
- [ ] The code is easier to communicate about than before
- [ ] No prototype shortcut became a silent production default
- [ ] At least one small broken window in the touched area was fixed

If any answer is no, revise before shipping.

---
