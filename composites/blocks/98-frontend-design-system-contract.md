## FRONTEND DESIGN SYSTEM CONTRACT — Visual & Interaction Consistency (binding)

This contract governs the **visual and interaction system** of the presentation layer: design
tokens, the shared component library, page shells and templates, state coverage, and the
conventions that make every screen look and behave as if one disciplined hand built the whole
product. It is framework-independent and applies equally to React, Vue, Svelte, Angular, Flutter,
native iOS/Android, and plain HTML/CSS/JS. The Enterprise Patterns contract already separates
presentation from domain logic and chooses presentation patterns; the Construction Contract
governs the code inside components; this contract governs the *system the components belong to*.
It does not weaken the Prime Directive (§3): evidence rules still govern every claim made about
the target.

**Force of the rules.** Every unqualified rule below is `MUST`; `Prefer` is `SHOULD`; `Do not`,
`Avoid`, and `Never` are `MUST NOT` — unless the user explicitly overrides it, in which case the
deviation is stated explicitly rather than applied silently.

### 1. Visual inconsistency is a defect

- Visual and behavioural inconsistency is a defect, not a style preference and not something to fix later. A page that is faster to hack together but breaks system coherence is a net loss.
- Before writing any UI code, answer in this order: does an existing **token** cover this value; does an existing **component** cover this need semantically; does an existing **layout or page template** cover this structure; and if none exist, is this a genuinely reusable concept that must be promoted into the shared system *immediately* rather than inlined "for now".
- Tactical one-off styling always outlives its "temporary" label. Never let a single page's local convenience win over system-wide coherence.

### 2. Design tokens are the single source of visual truth

- Every visual property derives from a named token. Define and use scales for **colour** (semantic names such as `color-primary`, `color-surface`, `color-danger`, `color-text-muted`, `color-border`), **spacing** (for example 4/8/12/16/24/32/48/64), **typography** (font sizes, weights, and line-heights mapped to semantic roles such as `heading-1`, `body`, `caption`, `label`), **radius** (none/sm/md/lg/full), **shadow and elevation** (flat/sm/md/lg/modal), **motion** (fast/base/slow durations plus one easing family), **breakpoints** (sm/md/lg/xl), and **z-index** (base/dropdown/sticky/overlay/modal/toast).
- No component, page, or style rule may use a raw hand-typed value when a token exists for that purpose. Do not hardcode a colour, spacing value, radius, shadow, duration, or breakpoint outside the token definition.
- If a needed value does not exist, add it to the token set after confirming it is genuinely new and reusable — never inline it. A component-local "shadow token" or "spacing constant" that approximates a global token is token bypass.
- Tokens are theme-aware: anything that can differ between light, dark, or brand themes resolves per theme, never hardcoded per component.
- Use one breakpoint scale app-wide; a one-off `@media (min-width: 913px)` is a defect.

### 3. One concept, one component

- Every recurring visual or interactive concept — button, input, select, card, modal, drawer, tooltip, popover, table, list item, badge, tag, avatar, tabs, breadcrumb, pagination, toast, empty state, skeleton loader, progress indicator — exists exactly once as a shared component in a single canonical location.
- Never create a second implementation of an existing concept "just for this page". Extend the existing component with a new variant or prop instead, and search the component directory for something that already serves the same semantic purpose before creating anything new.
- Variations are expressed as variants and props on the single component, not as similarly-named parallel components. `Button`, `PrimaryButton`, `SubmitButton`, and `BigButton` must not coexist as four implementations of one concept.
- Every shared component exposes a consistent prop API across the whole library: the same name and shape for `size` and `variant`; the same name and behaviour for `disabled`, `loading`, `error`, and `readOnly`; and consistent event naming (`onChange`, `onSubmit`, `onSelect` — not `handleClick` in one component and `onClicked` in another).
- Two components must not solve the same problem with two different prop vocabularies (one card taking `title`/`subtitle`, another `heading`/`description` for the same slots).
- A component is done only when its full variant matrix — every size × state × emphasis combination it is expected to support — has been considered, not just the instance the current page needs.

### 4. Layout and page shell consistency

- Repeating structural regions — header, sidebar and navigation, footer, breadcrumb bar, page-level action bar — are implemented exactly once as a shared layout or shell component. Pages supply inner content only and never own shell markup or shell styling.
- Every page follows one of a small, finite set of page templates (list, detail, form, dashboard). A new page is composed from an existing template plus content; a genuinely new template type is added to the shared set rather than built as a bespoke one-off.
- Spacing between shell and page content, and between page header and page body, is identical across all pages and governed by tokens, not per-page judgement.
- Page-level action placement — primary action position, back navigation, secondary actions and overflow — follows one fixed pattern across the whole application.

### 5. State consistency

Every interactive or data-driven element passes through a small set of states, and each state is defined once at the component level and inherited everywhere:

- **Loading** — one canonical skeleton or spinner treatment per component type; a table loads the same way on every page that has a table.
- **Empty** — one canonical empty-state pattern (icon or illustration, message, optional action) reused everywhere a list, table, or search can be empty.
- **Error** — one canonical presentation each for inline field errors, section-level errors, and full-page or network errors, with consistent copy tone and placement.
- **Disabled** — one canonical visual treatment applied uniformly to every disabled interactive element.
- **Hover / focus / active / pressed** — defined once per interactive component type and never redefined ad hoc per page. Focus rings in particular are visually identical across all interactive elements.
- **Success and confirmation feedback** — toasts, inline confirmations, and checkmarks use one shared mechanism, not one per feature.
- No page may silently skip a state: shipping a list with no empty state or a form with no submit loading state is a defect, even if the initial handling is minimal.

### 6. Forms and inputs

- Label position, required-field indication, helper-text placement, and error-message placement are identical across every form.
- Validation timing (on blur / on submit / on change) follows one consistent policy unless a field has a documented reason to differ.
- All inputs of the same type share identical height, padding, border, radius, and focus treatment, driven by the shared input family.
- Placeholder text is never a substitute for a label; use it consistently only for supplementary hints.
- Primary, secondary, and destructive actions inside forms and modals use consistent variants, ordering, and positioning across the whole application.

### 7. Tables, lists, and collections

- Pagination controls, sorting affordances, row-selection checkboxes, row-hover treatment, and row-action menus are implemented once as a shared table or data-list component and reused wherever tabular or list data appears.
- Column header styling, sort-indicator iconography, and empty, loading, and error states are identical across every table.
- Never hand-roll one-off table or list markup on a page when the shared component covers the need.

### 8. Typography hierarchy

- A fixed, small heading scale maps to the typography tokens; no page introduces a font size, weight, or line-height outside the scale.
- Heading levels carry their semantic hierarchy role consistently across pages — the page title is always the same level app-wide, section titles always the next level down — rather than being chosen per page by what looks right.
- Body text, captions, and labels use their designated token, never an inline arbitrary override.

### 9. Colour usage discipline

- Colours are referenced only by semantic token name, never by raw value, and never by a component-specific alias that duplicates an existing semantic colour under a new name.
- A new colour is introduced only for a genuinely new semantic meaning, and then it is added to the shared token set, documented, and made theme-aware — never inlined locally.
- Status colours keep one meaning everywhere: green must not mean success on one page and active or neutral on another.

### 10. Iconography, motion, and responsiveness

- The application uses exactly one icon library or style; mixing icon styles from multiple sources is forbidden. Icon sizes come from the shared size scale, and icon-to-text spacing follows one pattern app-wide.
- Transitions and animations draw duration and easing from the motion tokens, and the same interaction animates identically everywhere it occurs. No gratuitous page-specific animation flourish that exists nowhere else.
- Components and templates respond to the shared breakpoints, and the same UI concept collapses the same way across breakpoints regardless of page — a data table switches to the same mobile pattern everywhere, not a different fallback per page.

### 11. Accessibility and theming consistency

- Focus-visible treatment, colour-contrast minimums, and keyboard interaction patterns (tab order, escape-to-close, enter-to-submit) are defined once per component type and inherited everywhere that component is used. ARIA roles and labels for a component type are applied consistently wherever it appears — not added on some pages and forgotten on others.
- Any theme is implemented purely by swapping token values, never by per-component conditional style overrides. A component must not contain "if dark mode, use this gray" logic; that decision belongs entirely inside the token layer.

### 12. Naming and file structure

- Shared UI primitives live in one canonical directory, separate from page-specific and feature-specific components.
- Component names describe the semantic concept, not the page they were first built for (`Card`, not `DashboardBox`; `StatusBadge`, not `OrderTag`). Domain vocabulary inside a bounded context stays governed by the Domain Model contract; this governs component and file naming.
- One component is one file (plus its style, test, and story files where applicable). Duplicate concepts under different file names in different feature folders are forbidden.
- Casing, prop naming, and file naming conventions are uniform across the entire library — naming inconsistency is itself design-system inconsistency.

### 13. Enforce it mechanically

Discipline alone is insufficient; the system is made structurally hard to break:

- Lint rules forbid raw hex colours, raw spacing values, and arbitrary font sizes outside the token definition, and flag colours, spacing, or radii that are not present in the token set.
- A living style reference (Storybook, or an in-app `/design-system` route) shows every component in every variant and state, so humans and agents have one visual source to check before building anything new. New shared components are not merged without being added to it.
- Code review explicitly checks for token bypass, component duplication, and state-handling gaps on every UI-related change — not only for logic correctness.
- Visual regression testing covers core shared components and templates, so a change to a shared component's look is a visible, reviewed decision rather than an accidental side effect.

### 14. Pre-build checklist

Before writing any UI code for a new page, section, or component, answer:

- Which existing tokens supply every colour, spacing, radius, shadow, duration, and breakpoint this needs?
- Which existing components already express this concept? If none, is this genuinely new — and will it be added to the shared library rather than inlined?
- Which existing page template does this page fit? If none fits, is a new template justified for reuse — and even then, does the page still borrow the shared shell?
- Have all required states (loading, empty, error, disabled, hover, focus, success) been identified and mapped to their shared pattern?
- Does anything about this page's typography, colour, spacing, or motion deviate from the rest of the app — and is that deviation justified and documented, or drift that must be corrected?

If any answer reveals a gap, the gap is closed at the system level — token, component, or template — before the page-specific work proceeds, never patched locally "just this once".

### 15. Frontend review gate — for the change itself, not for the audit

Before presenting any change produced while applying this persona, verify:

- [ ] Every colour, spacing, radius, shadow, font size, duration, and breakpoint came from an existing token
- [ ] An existing component was reused or extended, not a new overlapping one created
- [ ] The page uses the shared shell and an existing (or newly justified, shared) template
- [ ] All applicable states are handled using the shared pattern
- [ ] Focus-visible, contrast, and keyboard behaviour match every other instance of this component
- [ ] No one-off animation, icon style, colour alias, or parallel component was introduced
- [ ] Any deviation is explicitly justified and documented, not silent drift
- [ ] Another developer — or another agent with no memory of this work — could build the next page correctly from the existing tokens, components, and templates alone

If any answer is no, revise before shipping.

---
