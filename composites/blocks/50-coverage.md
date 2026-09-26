## 6. COVERAGE CONTROL — AUDIT MATRIX

Maintain a coverage matrix throughout and **include it in the final report** (Appendix A).
For every relevant unit track:

| Unit | Reviewed? | Key symbols | Branches | Dependencies | Error paths | Security | Performance | Tests | Workflows | Findings |
|---|---|---|---|---|---|---|---|---|---|---|

Rules:

- Do not declare the audit complete until every relevant unit is either reviewed or has an
  explicit skip reason.
- Every skipped unit requires a stated reason (generated, vendored, out of scope, inaccessible).
- Coverage claims in the report must match this matrix exactly.

---
