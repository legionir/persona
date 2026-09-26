## REFACTORING CONTRACT — Refactoring.Guru (binding)

This contract governs **refactoring as a controlled discipline**: when it is justified, how it is
separated from other work, which technique treats which smell, and when to stop. The Construction
Contract already requires small behaviour-preserving steps, leaving the code cleaner, and no grand
redesign; it also lists the *signals* of rising complexity. This contract adds the operational
machinery on top: the smell catalog with triggers and treatments, the exception rules that prevent
mechanical over-refactoring, the verification and stop discipline, and the technique-selection and
safety rules. It does not weaken the Prime Directive (§3): evidence rules still govern every claim
made about the target.

**Force of the rules.** Every unqualified rule below is `MUST`; `Prefer` is `SHOULD`; `Do not`,
`Avoid`, and `Never` are `MUST NOT`; `MAY` is a permitted exception that must be justified — unless
the user explicitly overrides it, in which case the conflict is stated rather than silently applied.

### 1. Refactoring is controlled improvement, not cleanup

- Refactoring improves code structure without adding new functionality. Clean code is code that is obvious to other programmers, avoids duplicated knowledge and duplicated control flow, has a minimal number of moving parts, passes the relevant tests, and is cheaper to maintain than what it replaced.
- Every refactoring has: a specific smell, friction, or maintenance cost it addresses; a bounded transformation; a verification path; and no hidden feature change.
- Never treat refactoring as a vague cleanup pass. A refactoring without a named smell is not a refactoring.

### 2. Keep refactoring separate from other work

- Do not mix direct feature development and refactoring into one indistinguishable edit. Separate them at least by commit, patch section, or clearly labelled step.
- Any behaviour change is feature work or bug fixing — call it that, never refactoring.
- Refactor *before* feature work when dirty code blocks understanding or makes the feature awkward, and *after* it when the feature leaves new duplication, awkward names, or unnecessary structure.
- Preparatory refactoring stays separate from the feature behaviour it enables.

### 3. Work in small steps

- Apply refactoring as a sequence of small changes, keeping the program in working order after each meaningful step when practical.
- Run relevant tests after each risky structural change, and prefer several named transformations over one broad rewrite.
- Stop and reduce scope when a refactoring becomes too large to reason about locally. Refactoring is never cover for uncontrolled redesign.

### 4. Verify continuously

- Identify the relevant test, characterisation check, type check, or manual check *before* risky refactoring, and run all relevant existing tests after it.
- When tests fail, decide explicitly whether the refactoring changed behaviour or the tests were too coupled to implementation details. Fix refactoring mistakes before continuing.
- Replace or lift brittle low-level tests when they block behaviour-preserving structure changes. Never delete a failing test to make a refactoring appear successful.

### 5. Keep the result cleaner

- A refactoring succeeds only if the code becomes cleaner in the area touched. Do not perform a refactoring that leaves the code just as unclear, duplicated, or bloated.
- Pause and re-diagnose when a chain of small edits is not improving clarity.
- Consider a planned rewrite only when the code is extremely sloppy, tests exist or are added first, and enough time is explicitly allocated.

### 6. When to refactor

- **Rule of Three.** Implement a first occurrence directly; tolerate a second similar occurrence while the abstraction is still uncertain; on the third similar occurrence, consider refactoring. Never abstract coincidental similarity before the repeated responsibility is clear.
- **While adding a feature.** Refactor first when the existing code is too dirty to understand the change safely, reshape the local structure so the feature becomes straightforward, and use the request as a chance to pay down the specific debt that blocks it.
- **While fixing a bug.** Inspect the area around the bug for hidden complexity, duplication, and unclear ownership, and clean the structure that let the bug hide when the cleanup is small and local. Keep the bug fix as a separate behaviour change from the supporting refactor.
- **During code review.** Treat review as the last chance to catch smells before code becomes public: fix simple smells immediately when ownership allows, and estimate and isolate larger ones instead of smuggling them into the reviewed change.

### 7. Technical debt, operationally

- Debt is a cost that compounds by slowing future development. Never justify patches, kludges, missing tests, or unclear structure as harmless when they make later changes slower or riskier.
- Expose the source of debt when it comes from business pressure, missing tests, weak modularity, delayed refactoring, poor documentation, isolated branches, or inconsistent standards. Debt classification itself stays with the Technical Debt block.
- Prioritise debt that affects current change speed, correctness, or team understanding, and reduce it incrementally through ordinary feature and bug work.
- Do not defer all refactoring to a future cleanup project unless the current change cannot safely absorb it.

### 8. Smell detection: scan in this order

1. **Bloaters** — code grew too large to understand or change.
2. **Object-orientation abusers** — inheritance, type codes, or conditionals misusing the object model.
3. **Change preventers** — one change forces edits in too many places, or one class changes for unrelated reasons.
4. **Dispensables** — code exists without earning its maintenance cost.
5. **Couplers** — classes know too much about each other, or delegate so much that responsibility disappears.
6. **Library gaps** — external classes force duplicated workarounds.

For each smell: identify the symptom, identify why it makes change harder, choose the matching treatment, check whether the treatment creates worse coupling or unnecessary abstraction, and apply the smallest useful refactoring.

### 9. Diagnose, treat, verify, stop

Use this workflow for every non-trivial refactoring:

1. **Diagnose.** Name the visible symptom and the maintenance cost it creates; decide whether it is local, repeated, or architectural; and check whether the smell is real or only a style preference.
2. **Choose treatment.** Pick the catalog technique that directly addresses the smell, prefer a smaller technique before a larger structural move, note the expected cleaner end state before editing, and reject a treatment whose own tradeoff is worse than the smell.
3. **Verify behaviour.** Identify the existing check before moving code, run it after each risky step, and if behaviour changes, stop treating the change as refactoring and isolate the behaviour change.
4. **Decide the stop condition.** Stop when the named smell is gone or materially reduced; when the next improvement needs a different diagnosis; when the refactoring would cross ownership, public API, or feature scope without explicit approval; or when the code is cleaner enough for the requested change and further cleanup is speculative.

Do not continue refactoring just because another smell was discovered. Record the next smell separately unless it blocks the current change.

### 10. Smell exception rules

Do not treat smells mechanically. Confirm that the treatment improves clarity *for this codebase*, and leave a smell in place — with a reason — when it does not:

- A simple conditional may stay when replacing it with polymorphism would obscure a direct rule.
- Duplicate fragments may stay separate when the shared abstraction would be less obvious than the duplication, or when the fragments are only coincidentally similar and likely to diverge for different reasons.
- Comments may stay when they explain why, external constraints, or an algorithm that already resisted simpler structure.
- A small class may stay when it communicates a real extension point or boundary.
- Behaviour may stay separate from data when the design intentionally supports interchangeable behaviour.
- A long parameter list may stay temporarily when removing parameters would create stronger unwanted dependencies.
- Document or report intentional non-treatment whenever a visible smell is left in touched code.

### 11. Smell catalog: triggers and treatments

For each smell the entry gives the trigger, the preferred treatment, the fallback, and the risky option. The Construction Contract's complexity list names the signals; this catalog is the operational map from signal to treatment.

**Bloaters**

- **Long Method** — a method is long enough to need scrolling, comments, or mental bookkeeping (ten lines is a warning threshold, not a mechanical limit). Prefer `Extract Method`; fall back to `Replace Temp with Query`, `Introduce Parameter Object`, or `Preserve Whole Object` when locals block extraction; `Replace Method with Method Object` is risky. Extract a fragment that needs a comment to explain it, and extract loops, branches, and coherent phases. Never avoid extraction only because a call might cost performance.
- **Large Class** — too many fields, methods, responsibilities, or lines to understand as one concept. Prefer `Extract Class`; fall back to `Extract Subclass` for rare or variant behaviour, or `Extract Interface` for a client-facing subset; broad hierarchy extraction before responsibilities are stable is risky. Never split a class only because it is large when the extracted part has no stable responsibility.
- **Primitive Obsession** — primitives, strings, numbers, constants, or arrays standing in for meaningful concepts. Prefer `Replace Data Value with Object`, `Replace Magic Number with Symbolic Constant`, or `Replace Array with Object`; fall back to type-code refactorings when behaviour varies by code; replacing type code with subclasses or state/strategy before variation is stable is risky. Never wrap a primitive in a type that adds no name, validation, behaviour, or error prevention.
- **Long Parameter List** — more than three or four parameters, or callers must memorise argument order. Prefer `Replace Parameter with Method Call` or `Preserve Whole Object`; fall back to `Introduce Parameter Object`; removing parameters by creating hidden object dependencies is risky.
- **Data Clumps** — the same group of values appears in several fields, signatures, or calls. Prefer `Extract Class` or `Introduce Parameter Object`; fall back to `Preserve Whole Object`; passing a large owner object merely to avoid a parameter list is risky. Test whether the values still make sense if one member is removed; if not, model the group.

**Object-orientation abusers**

- **Switch Statements** — complex `switch` or repeated `if` chains branching on type, mode, or category. Prefer `Extract Method` plus `Move Method` to isolate the decision; fall back to type-code replacement; `Replace Conditional with Polymorphism` is risky when the conditional is simple or not based on stable variation. Suspect missing polymorphism when a new case forces edits at several switch sites, and use explicit methods instead when there are only a few simple parameter variations.
- **Temporary Field** — fields meaningful only in special circumstances, empty or invalid otherwise. Prefer `Extract Class` or `Replace Method with Method Object`; fall back to `Introduce Null Object` for absence checks; spreading optional half-state through more conditionals is risky. Never normalise half-initialised objects as ordinary design.
- **Refused Bequest** — a subclass inherits behaviour or data it does not use or cannot honour. Prefer `Push Down Method` or `Push Down Field`; fall back to `Replace Inheritance with Delegation`; preserving inheritance only to avoid changing callers is risky.
- **Alternative Classes with Different Interfaces** — two classes do the same job with different names or signatures. Prefer `Rename Method` plus signature alignment; fall back to `Extract Superclass`; merging classes across library or ownership boundaries is risky.

**Change preventers**

- **Divergent Change** — one class must change for many unrelated reasons. Prefer `Extract Class`; fall back to `Extract Superclass` or `Extract Subclass` for genuine shared behaviour; inheritance used to avoid clear responsibility splits is risky.
- **Shotgun Surgery** — one conceptual change forces many small edits across many classes. Prefer `Move Method` and `Move Field` to centralise ownership; fall back to `Inline Class` or `Extract Class`; adding forwarding layers without reducing edit sites is risky. Never leave knowledge scattered after the pattern is visible.
- **Parallel Inheritance Hierarchies** — adding a subclass in one hierarchy requires a matching subclass in another. Prefer moving methods and fields to collapse the mirrored variation; fall back to hierarchy collapse; adding the next paired subclass without redesigning ownership is risky.

**Dispensables**

- **Comments** — comments explain what unclear code does rather than why it exists. Prefer `Extract Variable`, `Extract Method`, or `Rename Method`; fall back to `Introduce Assertion` for hidden state assumptions; deleting comments before the code is self-explanatory is risky. Never use comments as deodorant for confusing structure.
- **Duplicate Code** — two fragments are identical or do the same job under slightly different wording. Prefer `Extract Method`; fall back to pull-up or `Extract Superclass` for sibling duplication, or `Extract Class` for a separate concept; merging coincidental similarity is risky. Remove accidental duplication even when the fragments are not textually identical.
- **Lazy Class** — a class no longer does enough to justify its maintenance cost. Prefer `Inline Class`; fall back to `Collapse Hierarchy`; keeping a class only because future work might need it is risky.
- **Data Class** — a class only stores data and exposes crude accessors while clients perform the behaviour. Prefer `Encapsulate Field` and `Encapsulate Collection`; fall back to `Move Method` and `Extract Method` to bring behaviour to the data; stopping after trivial accessors is risky.
- **Dead Code** — unused variables, parameters, fields, methods, classes, files, or unreachable branches. Prefer deletion after usage checks; fall back to `Inline Class`, `Collapse Hierarchy`, or `Remove Parameter`; deleting externally reachable API is risky. Never delete public, serialized, reflected, or plugin-facing code without checking external compatibility.
- **Speculative Generality** — abstractions, parameters, hooks, fields, or classes that exist only for imagined future needs. Prefer `Inline Method`, `Inline Class`, `Remove Parameter`, and field deletion; fall back to `Collapse Hierarchy`; removing framework extension points without checking users is risky.

**Couplers**

- **Feature Envy** — a method uses another object's data more than its own. Prefer `Move Method`; fall back to `Extract Method` before moving an envying fragment; moving behaviour that was deliberately separated for interchangeable strategy-like use is risky.
- **Inappropriate Intimacy** — classes rely on each other's internals or spend too much time together. Prefer `Move Method` and `Move Field`; fall back to `Hide Delegate` or `Replace Inheritance with Delegation`; widening visibility to preserve the intimacy is risky.
- **Message Chains** — client code navigates a chain of objects to reach data or behaviour. Prefer `Hide Delegate`; fall back to `Move Method` closer to the data; adding a middle man that merely forwards without reducing knowledge is risky. Never expose object-graph topology as a routine calling convention.
- **Middle Man** — a class mostly forwards calls and adds no policy, coordination, or protection. Prefer `Remove Middle Man`; fall back to `Inline Class`; removing a boundary that hides volatile structure or policy is risky.
- **Incomplete Library Class** — an external class lacks methods you need and cannot be changed. Prefer `Introduce Foreign Method` for a narrow missing operation; fall back to `Introduce Local Extension` for repeated substantial missing behaviour; broad library wrapping or forking is risky. Never scatter repeated library workarounds through the codebase.

### 12. Technique selection

Choose the technique by what it does, not by how modern it sounds:

- **Composing methods.** `Extract Method` for a fragment with a coherent purpose or one needing explanation; `Inline Method` when the body is clearer than the name; `Extract Variable` to name an expression; `Inline Temp` when a temp obscures a simple expression; `Replace Temp with Query` for a recomputable named value; `Split Temporary Variable` when one variable carries several meanings; `Remove Assignments to Parameters` for scratch parameters; `Replace Method with Method Object` when locals block extraction; `Substitute Algorithm` only after behaviour is protected.
- **Moving features.** `Move Method` when a method uses another class more than its own; `Move Field` when ownership is clearer elsewhere; `Extract Class` for separable responsibilities; `Inline Class` when a class no longer earns its existence; `Hide Delegate` when clients know too much about collaborators; `Remove Middle Man` when delegation hides nothing; `Introduce Foreign Method` for a narrow library gap; `Introduce Local Extension` for substantial missing behaviour.
- **Organizing data.** `Self Encapsulate Field` when access needs control; `Replace Data Value with Object` when a primitive needs meaning or validation; `Change Value to Reference` and `Change Reference to Value` for identity and lifecycle fit; `Replace Array with Object` when positions have names; `Duplicate Observed Data` when GUI-held domain data must move; change association direction only when both sides genuinely need navigation; `Replace Magic Number with Symbolic Constant` for meaningful literals; `Encapsulate Field` and `Encapsulate Collection` for exposed representation and mutable internals; type-code refactorings chosen by whether variation is stable, runtime, or constant data.
- **Simplifying conditionals.** `Decompose Conditional` for hard-to-read conditions; `Consolidate Conditional Expression` and `Consolidate Duplicate Conditional Fragments` only when checks are side-effect free and order is preserved; `Remove Control Flag` for flags that only direct flow; `Replace Nested Conditional with Guard Clauses` when special cases obscure the normal path; `Replace Conditional with Polymorphism` only for stable type or state variation; `Introduce Null Object` when null checks dominate; `Introduce Assertion` for hidden state assumptions.
- **Simplifying method calls.** `Rename Method` when the name hides behaviour; `Add Parameter` only when a field would be worse; `Remove Parameter` when unused; `Separate Query from Modifier` when a method both answers and mutates; `Parameterize Method` for value-only differences; `Replace Parameter with Explicit Methods` when a parameter selects behaviour; `Preserve Whole Object` for several values from one object; `Replace Parameter with Method Call` when the callee can obtain the data; `Introduce Parameter Object` for parameters that travel together; `Remove Setting Method` for post-construction immutability; `Hide Method` to shrink the interface; `Replace Constructor with Factory Method` when creation needs naming, selection, or caching; `Replace Error Code with Exception` and `Replace Exception with Test` chosen by whether the condition is exceptional or cheaply checkable.
- **Dealing with generalization.** Pull members up when sibling duplication is real and the superclass can honestly own it; push members down when the superclass contract is too broad; `Extract Subclass`, `Extract Superclass`, and `Extract Interface` only for real shared behaviour or a real client-facing subset; `Collapse Hierarchy` when the distinction is gone; `Form Template Method` when the skeleton and steps are stable; `Replace Inheritance with Delegation` for refused bequest or excess coupling; `Replace Delegation with Inheritance` only when the subtype relation is honest.

### 13. Technique execution safety

- **Extraction.** Identify every variable read, written, or returned by the fragment first. Leave variables local when they are declared and used only inside the fragment; pass prior values as parameters only when genuinely needed. Double-check any variable modified inside the fragment: if later code needs the changed value, return it explicitly or choose a safer refactoring. Name the extracted method after its purpose, not its mechanical steps, and never hide an important side effect behind a harmless-sounding name.
- **Inlining.** Confirm the method adds no useful name, abstraction, override point, or public contract, and check all callers — especially where dynamic dispatch, inheritance, or interfaces are involved. Before `Inline Class`, move all useful behaviour and data to the target and update every reference; delete the emptied class only when references, construction sites, tests, and documentation no longer require it.
- **Moving.** Inspect which class owns most of the data the method uses, extract the fragment first when only part of a method belongs elsewhere, and update all callers while preserving visibility intentionally — never widen access just to make a move compile. Migrate field reads and writes in a small sequence, and preserve construction, serialization, and persistence behaviour.
- **Encapsulation.** Add access methods and migrate direct readers and writers before making a field private, then review accessor callers: the behaviour may belong inside the owner. Prevent callers from mutating internal collections directly, exposing add and remove operations that preserve invariants instead of a settable collection. Never finish at trivial getters and setters that merely preserve public data under new names.
- **Conditionals.** Verify conditions are side-effect free before consolidating, move duplicate fragments only when execution order is preserved, identify the normal path before introducing guard clauses, and confirm stable type or state variation before introducing polymorphism.
- **Method calls.** Check whether the method should own or derive the data before adding a parameter; confirm a parameter is unused before removing it; split mutation from returned information before separating query from modifier; confirm a parameter selects behaviour rather than ordinary data before replacing it with explicit methods; and confirm grouped parameters form one concept before introducing a parameter object.
- **Data reorganisation.** Define the object's meaning, equality, validation, and allowed behaviour before replacing a primitive; decide whether identity, mutability, sharing, and lifecycle management are required before changing value or reference semantics; make value objects immutable before replacing references with values; use factory creation so callers receive the canonical object; and identify which side owns updates before changing association direction.
- **Generalization.** Confirm sibling duplication is real and the superclass contract can honestly own the member before pulling up; confirm the superclass no longer promises the member before pushing down; identify real shared behaviour or a real client-facing subset before extracting a superclass or interface; check substitutability and public type expectations before collapsing a hierarchy; and preserve delegated behaviour and forwarding paths deliberately when replacing inheritance with delegation.

### 14. Decision anti-patterns

- Do not apply a refactoring because its name sounds modern; apply it because it treats a diagnosed smell.
- Do not turn a simple conditional into polymorphism unless variation is stable, repeated, and owned by type or state.
- Do not create a parameter object from unrelated arguments just to shorten a signature.
- Do not introduce a superclass or interface from coincidental method names without a real client or shared behaviour.
- Do not replace duplication with an abstraction that has a worse name than the duplicated code.
- Do not stop at getters and setters when the real smell is behaviour living outside the data.
- Do not hide feature work inside a refactoring sequence.
- Do not preserve a forwarding class merely because deleting it requires caller updates.
- Do not use bidirectional association as a convenience shortcut when one side can receive the collaborator as a parameter or lookup.
- Do not delete speculative or dead-looking code until generated, reflected, serialized, plugin-facing, and public usages are checked.
- Do not add assertions for normal user input, expected absence, or recoverable errors, and do not use exceptions as routine tests when callers can cheaply check the condition first.
- Do not inline names that explain business intent even when the body is short, and do not move behaviour away from its data if that creates feature envy in the opposite direction.
- Do not continue cleanup after the diagnosed smell is fixed unless the next smell blocks the requested change.

### 15. Refactoring workflow for agents

**Before editing.** Identify the requested behaviour change or maintenance goal; scan the touched area for smells; name the primary smell, its cost, and the smallest useful refactoring; identify the expected cleaner end state and the stop condition; identify the tests or checks that prove behaviour is preserved; and decide whether the refactoring belongs before, after, or separate from the feature work.

**During editing.** Apply one named transformation at a time; keep the code runnable after each meaningful step; rename, extract, move, inline, or encapsulate before introducing larger design structures; re-run relevant tests after risky movement, public interface changes, or changed state flow; re-check whether the chosen technique is still the smallest treatment; and stop if the refactoring exposes a different, larger problem, reporting the new scope.

**After editing.** Confirm behaviour preservation; confirm the original smell is reduced or removed; confirm no broader feature change was hidden in the refactor; confirm no new smell was introduced — especially middle man, speculative generality, or inappropriate intimacy; confirm that any intentionally untreated smell has a reason; and report the technique used, the stop condition reached, and the validation performed.

### 16. Refactoring review gate — for the change itself, not for the audit

Before presenting any change produced during this work, verify:

- [ ] The change is labelled refactoring, feature, or bug fix, and that boundary is clear
- [ ] The code is cleaner in the touched area than before
- [ ] A named smell justified the transformation
- [ ] The smallest suitable technique was used
- [ ] All relevant tests pass, and no test was deleted or weakened to pass
- [ ] Any public interface change received compatibility handling or a transition path
- [ ] Duplication, bloat, coupling, or unclear control flow went down
- [ ] No speculative abstraction, needless polymorphism, or new bidirectional association was added
- [ ] Any remaining smell is explicitly deferred with a reason, not hidden

If any answer is no, revise before shipping.

---
