## 10. TECHNICAL DEBT, DEAD CODE, SUSPICIOUS CODE

### 10.1 Technical debt

Find debt explicitly. Classify into: accidental complexity, intentional shortcuts, duplicated
logic, obsolete code, temporary workarounds, architectural debt, testing debt, documentation debt,
security debt, operational debt, dependency debt, performance debt, maintainability debt.

For each debt item state: what it is, where it exists, why it matters, current impact, future risk,
suggested remediation, and estimated complexity.

### 10.2 Dead / unused / suspicious code

Search for: unused imports, variables, functions and classes, unreachable branches, obsolete
feature flags, dead configuration, duplicated implementations, shadowed variables, suspicious
fallback logic, commented-out production logic, stale TODOs and FIXMEs, temporary hacks, debug
code, and development-only behaviour leaking into production.

**Rule:** do not mark code as dead merely because it is not referenced locally. Verify
repository-wide references and dynamic usage (reflection, string dispatch, DI containers,
route/config-driven loading) before claiming it.

---
