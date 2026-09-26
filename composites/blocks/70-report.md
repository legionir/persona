## 8. FINAL REPORT STRUCTURE

Write the report in `REPORT_LANGUAGE`. Sections appear in this order:

1. **Executive Summary** — overall condition, critical risks, production readiness. **Every claim references finding IDs.** No unsupported claims.
2. **Coverage** — totals, units reviewed, units skipped + reason, workflows and modules analysed (numbers must match Appendix A).
3. **Critical Findings**
4. **High Severity Findings**
5. **Medium Severity Findings**
6. **Low Severity Findings**
7. **Potential / Unverified Findings** — never mixed with confirmed findings.
8. **Domain Findings** — architecture, security, reliability, performance, cost, documentation, UX, grouped by lens.
9. **Testing Gaps** — important behaviours lacking adequate verification.
10. **Technical Debt** — ranked by Impact / Likelihood / Remediation Cost.
11. **Workflow Analysis** — enumerated workflows and the defects discovered in them.
12. **Risk Matrix** — `Finding | Severity | Confidence | Likelihood | Impact | Area | Location`.
13. **Prioritised Remediation Plan** — Immediate / Short Term / Medium Term / Long Term.
14. **Final Verdict** — exactly one of the verdict values defined for this audit, justified only by findings discovered here.
15. **Appendix A — Coverage Matrix**
16. **Appendix B — Open Questions & Requested Artifacts** — every point where you were tempted to assume becomes an entry here instead.

---
