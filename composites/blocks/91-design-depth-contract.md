## DESIGN DEPTH CONTRACT — A Philosophy of Software Design (binding)

This contract governs the **shape** of every change produced while applying this persona: where
module boundaries fall, how much each module hides, and how much a reader must hold in mind. The
Construction Contract (Clean Code + Code Complete) governs the *inside* of routines, names, data,
and tests; this contract governs the *seams between them*. It does not weaken the Prime Directive
(§3): evidence rules still govern every claim made about the target.

**Force of the rules.** Every unqualified rule below is `MUST`; `Prefer` is `SHOULD`; `Do not`,
`Avoid`, and `Never` are `MUST NOT` — unless the user explicitly overrides it, in which case the
conflict is stated rather than silently applied.

### 1. Complexity is the enemy

- Complexity is anything that makes software hard to understand or hard to change. Treat it as a defect class, not a style preference.
- Recognise its three symptoms: **change amplification** (one change forces edits in many places), **cognitive load** (too much must be known at once), and **unknown unknowns** (it is unclear what must be known, or where the relevant code lives).
- Hidden dependencies, information spread across many places, and temporal coupling that readers must reconstruct mentally are architectural warnings.
- Do not optimise for shorter files, fewer lines, or clever compactness when complexity rises. Measure by what the next reader must know.
- When a feature feels awkward, diagnose before patching: is the interface too wide, is the behaviour scattered, are details leaking that should be hidden, are there too many special cases, is a local fix raising global complexity?

### 2. Module depth

- A module's depth is the complexity it hides relative to the cost of its interface. Deep modules hide substantial complexity behind a small, strong interface; shallow modules expose nearly as much as they hide.
- Prefer a small interface with strong semantics over a large surface of minor helpers.
- Every module must carry its own weight — justify it by what it hides, not by what it contains.
- A module that only forwards work is too shallow.
- Do not create pass-through service classes, thin wrappers around libraries that simplify nothing, or helper modules that only rename obvious operations.
- Judge depth per change: a module that became shallower is a defect even if it became smaller.
- Function size is a symptom, not a metric: the Construction Contract's routine rules still apply, but never split a function only to hit a line count when the split forces readers to jump between fragments to follow one idea.

### 3. Information hiding

- Hide design decisions that are likely to change: internal data representations, incidental workflow steps, bookkeeping, and storage, protocol, framework, or file-format details.
- Keep callers from depending on implementation detail, performance hacks, or storage shape.
- Encapsulate messy edge conditions and normalisation logic behind the interface.
- Do not expose internal representation or state through module interfaces, and do not let callers coordinate object internals across modules.
- If a change to an implementation detail forces changes at call sites, information hiding failed — report that as the finding.

### 4. Interface design

- Design interfaces around what clients need to know, never around how the implementation works.
- Keep interfaces narrow but meaningful: few methods, strong semantic guarantees, limited required context.
- Do not require callers to stage operations in a fragile sequence; the interface must be usable without knowing the internal workflow.
- Eliminate arguments that exist only to expose internal implementation choices.
- Name methods after the abstraction they provide, not the mechanism they use.
- Treat as warnings: many configuration options, multiple setup methods required before use, and call-order traps.

### 5. Strategic over tactical programming

- Spend time reducing future complexity, not only making the current change pass.
- Reshape abstractions when recurring friction appears instead of accommodating it.
- Invest in decomposition that makes future changes local, and leave clearer structure behind after every substantial edit.
- Do not patch local symptoms while increasing global complexity, copy/paste to meet a deadline, expose one more internal detail instead of designing a boundary, or add flags and exceptions to dodge a better abstraction.
- A tactical patch that raises future difficulty is reported as a finding even when it works.

### 6. General-purpose vs special-purpose modules

- Prefer modules that capture a reusable concept at the right abstraction level.
- Do not overfit an interface to one narrow caller when a slightly more general concept is obvious.
- Do not generalise so far that the abstraction becomes vague. The best module is specific enough to be strong and general enough to be reusable within its domain.

### 7. Define away exceptions

- Design APIs that make misuse hard, and eliminate invalid or awkward states by changing the interface or the invariant — not only by adding checks.
- Use special/general decomposition when a few unusual cases clutter the main abstraction: keep the general case simple and isolate the rare behaviour.
- Do not pollute the main abstraction with every edge case, and do not scatter "special case" branches across many call sites.
- Keep the normal path obvious and the exceptional path isolated.
- Do not require every caller to repeat defensive ceremony, and do not hand callers half-valid objects they must tiptoe around.

### 8. Pull complexity downward

- Put complexity in one place rather than many, behind a simpler public contract.
- Prefer a slightly more complex implementation when it makes all callers simpler.
- Remove repeated reasoning burdens from call sites. Complexity pushed outward through flags, setup steps, and coupled operations is a design defect.

### 9. Temporal decomposition

- Do not structure modules primarily around execution order when the real structure is conceptual.
- Decompose around stable concepts and responsibilities; initialisation steps, processing phases, and cleanup stages must not force readers to reconstruct the design from time order alone.
- Keep call ordering simple and explicit where it matters.
- Do not scatter prepare/process/finalize stages without domain concepts, require secret temporal knowledge to use an API, or expose partial objects whose meaning depends on which phase has already run.

### 10. Combine or separate code

- Separate code only when the separation reduces complexity, hides a real design decision, or creates a stronger abstraction.
- Combine code when split pieces force readers to jump between shallow fragments to understand one idea.
- Keep related state, behaviour, and invariants together when separating them would create change amplification.
- Do not preserve a boundary merely because it already exists when it exposes almost as much complexity as it hides.
- Prefer one coherent deeper module over several tiny modules that require callers to coordinate details.
- Do not split by execution phase when the stable concept is not temporal, separate normal and special cases so far apart that their shared invariant is hidden, or add helper layers that distribute one design decision across many files.

### 11. Design alternatives and comments-first design

- For non-trivial design choices, compare at least two plausible designs before implementing the first one that works.
- Evaluate alternatives by interface simplicity, information hiding, special-case reduction, and future cognitive load.
- When an interface or abstraction is unclear, sketch the public contract and its explanatory comments before committing to an implementation.
- Revise the abstraction when the comment needed to explain it becomes complicated; never use comments to justify a confusing interface instead of changing the interface.
- Do not document implementation mechanics that callers should not need to know.

### 12. Consistency and obviousness

- Names reveal the abstraction a module provides, not the internal mechanism it uses.
- Keep names, argument order, error behaviour, and interface conventions consistent across related operations.
- Prefer obvious code: a reader should infer behaviour from local structure and names.
- Remove non-obvious behaviour unless it is hidden behind a clear contract.
- When code surprises a reader, treat that as complexity even if the code is short.

### 13. Performance, trends, and tests

- Do not sacrifice module depth or information hiding for performance without evidence that the trade-off matters.
- When performance matters, hide optimisation details behind stable interfaces so callers do not inherit the complexity; prefer measurements and targeted changes over broad speculative tuning.
- Do not adopt a trend, paradigm, pattern, or framework unless it reduces complexity in this codebase.
- Use tests to preserve behaviour while changing structure, but do not let test convenience force shallow or leaky interfaces.

### 14. Design review gate — for the change itself, not for the audit

Before presenting any change produced during this work, verify:

- [ ] Cognitive load went down, not up
- [ ] The touched modules are deeper (or at least not shallower) than before
- [ ] More complexity hides behind a stable interface
- [ ] Call sites handle fewer special cases than before
- [ ] An implementation detail was removed from the public surface
- [ ] No pass-through layer was added
- [ ] The interface describes the abstraction rather than the mechanism
- [ ] The change improves future changeability, not only present convenience

If any answer is no, revise the design before shipping.

---
