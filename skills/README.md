# Persona Skills

Each folder is one **Agent Skill**: `SKILL.md` is the operating core (read when the task matches) and
`references/` holds the full persona text for when contract details are needed.

Install in Claude Code (project):

```bash
# The whole library
cp -r skills/<name> .claude/skills/

# Or all skills
for d in skills/*/; do cp -r "$d" .claude/skills/; done
```

Regenerate: `python3 scripts/build_skills.py` — validate: `python3 scripts/validate_skills.py`

Full index and machine-readable metadata: [`index.json`](index.json)

| Skill | Type | Domain | Source | SKILL.md lines |
|---|---|---|---|---|
| [`ai-agent-system-audit-hardening`](ai-agent-system-audit-hardening/SKILL.md) | Composite | Composite | `prompts/composite/AI Agent System Audit & Hardening.md` | 112 |
| [`api-integration-contract-audit`](api-integration-contract-audit/SKILL.md) | Composite | Composite | `prompts/composite/API & Integration Contract Audit.md` | 115 |
| [`architecture-review-architecture-audit`](architecture-review-architecture-audit/SKILL.md) | Composite | Composite | `prompts/composite/Architecture Review & Architecture Audit.md` | 136 |
| [`clean-code-construction-review`](clean-code-construction-review/SKILL.md) | Composite | Composite | `prompts/composite/Clean Code & Construction Review.md` | 116 |
| [`cloud-infrastructure-audit`](cloud-infrastructure-audit/SKILL.md) | Composite | Composite | `prompts/composite/Cloud & Infrastructure Audit.md` | 112 |
| [`codebase-integrity-audit-protocol`](codebase-integrity-audit-protocol/SKILL.md) | Composite | Composite | `prompts/composite/codebase-integrity-audit-protocol.md` | 119 |
| [`data-database-integrity-audit`](data-database-integrity-audit/SKILL.md) | Composite | Composite | `prompts/composite/Data & Database Integrity Audit.md` | 115 |
| [`domain-model-context-review`](domain-model-context-review/SKILL.md) | Composite | Composite | `prompts/composite/Domain Model & Context Review.md` | 120 |
| [`execution-plan-generator`](execution-plan-generator/SKILL.md) | Composite | Composite | `prompts/composite/Execution Plan Generator.md` | 73 |
| [`forensic-codebase-review-audit`](forensic-codebase-review-audit/SKILL.md) | Composite | Composite | `prompts/composite/Forensic Codebase Review & Audit.md` | 144 |
| [`forensic-security-threat-audit`](forensic-security-threat-audit/SKILL.md) | Composite | Composite | `prompts/composite/Forensic Security & Threat Audit.md` | 112 |
| [`frontend-design-system-review`](frontend-design-system-review/SKILL.md) | Composite | Composite | `prompts/composite/Frontend & Design System Review.md` | 117 |
| [`incident-forensic-review-postmortem`](incident-forensic-review-postmortem/SKILL.md) | Composite | Composite | `prompts/composite/Incident Forensic Review & Postmortem.md` | 112 |
| [`performance-scalability-audit`](performance-scalability-audit/SKILL.md) | Composite | Composite | `prompts/composite/Performance & Scalability Audit.md` | 112 |
| [`privacy-compliance-audit`](privacy-compliance-audit/SKILL.md) | Composite | Composite | `prompts/composite/Privacy & Compliance Audit.md` | 112 |
| [`production-readiness-reliability-audit`](production-readiness-reliability-audit/SKILL.md) | Composite | Composite | `prompts/composite/Production Readiness & Reliability Audit.md` | 108 |
| [`software-design-architecture-review`](software-design-architecture-review/SKILL.md) | Composite | Composite | `prompts/composite/Software Design & Architecture Review.md` | 122 |
| [`technical-debt-modernization-audit`](technical-debt-modernization-audit/SKILL.md) | Composite | Composite | `prompts/composite/Technical Debt & Modernization Audit.md` | 121 |
| [`testing-quality-assurance-audit`](testing-quality-assurance-audit/SKILL.md) | Composite | Composite | `prompts/composite/Testing & Quality Assurance Audit.md` | 117 |
| [`accessibility-specialist`](accessibility-specialist/SKILL.md) | EXECUTOR | Design | `prompts/implementation/accessibility-specialist.md` | 237 |
| [`account-manager`](account-manager/SKILL.md) | SUPERVISOR | Support | `prompts/audit/account-manager.md` | 244 |
| [`agent-architect`](agent-architect/SKILL.md) | EXECUTOR | AI | `prompts/implementation/agent-architect.md` | 254 |
| [`agent-evaluator`](agent-evaluator/SKILL.md) | EXECUTOR | AI | `prompts/implementation/agent-evaluator.md` | 254 |
| [`agent-integration-engineer`](agent-integration-engineer/SKILL.md) | EXECUTOR | AI | `prompts/implementation/agent-integration-engineer.md` | 253 |
| [`agent-safety-engineer`](agent-safety-engineer/SKILL.md) | EXECUTOR | AI | `prompts/implementation/agent-safety-engineer.md` | 252 |
| [`agentic-prompt-specialist`](agentic-prompt-specialist/SKILL.md) | EXECUTOR | AI | `prompts/implementation/agentic-prompt-specialist.md` | 253 |
| [`agile-coach`](agile-coach/SKILL.md) | SUPERVISOR | Project | `prompts/audit/agile-coach.md` | 244 |
| [`ai-engineer`](ai-engineer/SKILL.md) | EXECUTOR | AI | `prompts/implementation/ai-engineer.md` | 250 |
| [`ai-engineer-lead`](ai-engineer-lead/SKILL.md) | SUPERVISOR | AI | `prompts/audit/ai-engineer-lead.md` | 267 |
| [`ai-ml-engineer`](ai-ml-engineer/SKILL.md) | EXECUTOR | AI | `prompts/implementation/ai-ml-engineer.md` | 249 |
| [`ai-safety-alignment-engineer`](ai-safety-alignment-engineer/SKILL.md) | EXECUTOR | AI | `prompts/implementation/ai-safety-alignment-engineer.md` | 238 |
| [`analytics-engineer`](analytics-engineer/SKILL.md) | EXECUTOR | Data | `prompts/implementation/analytics-engineer.md` | 238 |
| [`application-security-engineer`](application-security-engineer/SKILL.md) | EXECUTOR | Security | `prompts/implementation/application-security-engineer.md` | 249 |
| [`architecture-review-board`](architecture-review-board/SKILL.md) | SUPERVISOR | Architecture | `prompts/audit/architecture-review-board.md` | 262 |
| [`aso-specialist`](aso-specialist/SKILL.md) | EXECUTOR | Growth | `prompts/implementation/aso-specialist.md` | 236 |
| [`audit-specialist`](audit-specialist/SKILL.md) | SUPERVISOR | Audit | `prompts/audit/audit-specialist.md` | 257 |
| [`backend-developer`](backend-developer/SKILL.md) | EXECUTOR | Software | `prompts/implementation/backend-developer.md` | 237 |
| [`backup-administrator`](backup-administrator/SKILL.md) | EXECUTOR | Software | `prompts/implementation/backup-administrator.md` | 248 |
| [`beta-tester`](beta-tester/SKILL.md) | EXECUTOR | Support | `prompts/implementation/beta-tester.md` | 237 |
| [`bi-analyst`](bi-analyst/SKILL.md) | EXECUTOR | Analytics | `prompts/implementation/bi-analyst.md` | 238 |
| [`board-of-directors`](board-of-directors/SKILL.md) | SUPERVISOR | Business | `prompts/audit/board-of-directors.md` | 244 |
| [`brand-designer`](brand-designer/SKILL.md) | EXECUTOR | Design | `prompts/implementation/brand-designer.md` | 238 |
| [`build-engineer`](build-engineer/SKILL.md) | EXECUTOR | DevOps | `prompts/implementation/build-engineer.md` | 237 |
| [`business-analyst-ba`](business-analyst-ba/SKILL.md) | EXECUTOR | Analytics | `prompts/implementation/business-analyst-ba.md` | 248 |
| [`business-continuity-manager`](business-continuity-manager/SKILL.md) | SUPERVISOR | Project | `prompts/audit/business-continuity-manager.md` | 245 |
| [`business-development-manager`](business-development-manager/SKILL.md) | SUPERVISOR | Growth | `prompts/audit/business-development-manager.md` | 246 |
| [`cao`](cao/SKILL.md) | SUPERVISOR | Audit | `prompts/audit/cao.md` | 264 |
| [`change-manager`](change-manager/SKILL.md) | SUPERVISOR | Project | `prompts/audit/change-manager.md` | 257 |
| [`chaos-engineer`](chaos-engineer/SKILL.md) | EXECUTOR | DevOps | `prompts/implementation/chaos-engineer.md` | 238 |
| [`chief-design-officer`](chief-design-officer/SKILL.md) | SUPERVISOR | Design | `prompts/audit/chief-design-officer.md` | 264 |
| [`chief-privacy-officer`](chief-privacy-officer/SKILL.md) | SUPERVISOR | Compliance | `prompts/audit/chief-privacy-officer.md` | 262 |
| [`cio`](cio/SKILL.md) | SUPERVISOR | Business | `prompts/audit/cio.md` | 261 |
| [`ciso`](ciso/SKILL.md) | SUPERVISOR | Security | `prompts/audit/ciso.md` | 264 |
| [`cloud-architect`](cloud-architect/SKILL.md) | SUPERVISOR | Architecture | `prompts/audit/cloud-architect.md` | 246 |
| [`cloud-engineer`](cloud-engineer/SKILL.md) | EXECUTOR | DevOps | `prompts/implementation/cloud-engineer.md` | 236 |
| [`cloud-security-engineer`](cloud-security-engineer/SKILL.md) | EXECUTOR | Security | `prompts/implementation/cloud-security-engineer.md` | 252 |
| [`community-director`](community-director/SKILL.md) | SUPERVISOR | Growth | `prompts/audit/community-director.md` | 263 |
| [`community-manager`](community-manager/SKILL.md) | EXECUTOR | Support | `prompts/implementation/community-manager.md` | 236 |
| [`compliance-evidence-analyst`](compliance-evidence-analyst/SKILL.md) | EXECUTOR | Compliance | `prompts/implementation/compliance-evidence-analyst.md` | 238 |
| [`content-strategist`](content-strategist/SKILL.md) | EXECUTOR | Documentation | `prompts/implementation/content-strategist.md` | 238 |
| [`contract-manager`](contract-manager/SKILL.md) | SUPERVISOR | Compliance | `prompts/audit/contract-manager.md` | 245 |
| [`cryptography-engineer`](cryptography-engineer/SKILL.md) | EXECUTOR | Security | `prompts/implementation/cryptography-engineer.md` | 238 |
| [`cto`](cto/SKILL.md) | SUPERVISOR | Business | `prompts/audit/cto.md` | 264 |
| [`customer-success-manager`](customer-success-manager/SKILL.md) | SUPERVISOR | Support | `prompts/audit/customer-success-manager.md` | 244 |
| [`customer-support-agent`](customer-support-agent/SKILL.md) | EXECUTOR | Support | `prompts/implementation/customer-support-agent.md` | 249 |
| [`cybersecurity-engineer`](cybersecurity-engineer/SKILL.md) | EXECUTOR | Security | `prompts/implementation/cybersecurity-engineer.md` | 248 |
| [`data-analyst`](data-analyst/SKILL.md) | EXECUTOR | Analytics | `prompts/implementation/data-analyst.md` | 249 |
| [`data-architect`](data-architect/SKILL.md) | SUPERVISOR | Architecture | `prompts/audit/data-architect.md` | 246 |
| [`data-engineer`](data-engineer/SKILL.md) | EXECUTOR | Data | `prompts/implementation/data-engineer.md` | 248 |
| [`data-governance-manager`](data-governance-manager/SKILL.md) | SUPERVISOR | Data | `prompts/audit/data-governance-manager.md` | 262 |
| [`data-scientist`](data-scientist/SKILL.md) | EXECUTOR | AI | `prompts/implementation/data-scientist.md` | 250 |
| [`data-steward`](data-steward/SKILL.md) | EXECUTOR | Data | `prompts/implementation/data-steward.md` | 238 |
| [`database-administrator-dba`](database-administrator-dba/SKILL.md) | EXECUTOR | Data | `prompts/implementation/database-administrator-dba.md` | 248 |
| [`database-engineer`](database-engineer/SKILL.md) | EXECUTOR | Data | `prompts/implementation/database-engineer.md` | 239 |
| [`database-security-specialist`](database-security-specialist/SKILL.md) | EXECUTOR | Security | `prompts/implementation/database-security-specialist.md` | 252 |
| [`decommission-engineer`](decommission-engineer/SKILL.md) | EXECUTOR | Software | `prompts/implementation/decommission-engineer.md` | 272 |
| [`deployment-engineer`](deployment-engineer/SKILL.md) | EXECUTOR | Software | `prompts/implementation/deployment-engineer.md` | 248 |
| [`design-manager`](design-manager/SKILL.md) | SUPERVISOR | Design | `prompts/audit/design-manager.md` | 263 |
| [`design-system-designer`](design-system-designer/SKILL.md) | EXECUTOR | Design | `prompts/implementation/design-system-designer.md` | 249 |
| [`designops-engineer`](designops-engineer/SKILL.md) | EXECUTOR | Design | `prompts/implementation/designops-engineer.md` | 238 |
| [`desktop-developer`](desktop-developer/SKILL.md) | EXECUTOR | Software | `prompts/implementation/desktop-developer.md` | 238 |
| [`development-manager`](development-manager/SKILL.md) | SUPERVISOR | Project | `prompts/audit/development-manager.md` | 263 |
| [`devops-engineer`](devops-engineer/SKILL.md) | EXECUTOR | DevOps | `prompts/implementation/devops-engineer.md` | 249 |
| [`devops-manager`](devops-manager/SKILL.md) | SUPERVISOR | DevOps | `prompts/audit/devops-manager.md` | 262 |
| [`devrel`](devrel/SKILL.md) | EXECUTOR | Software | `prompts/implementation/devrel.md` | 237 |
| [`devsecops-engineer`](devsecops-engineer/SKILL.md) | EXECUTOR | DevOps | `prompts/implementation/devsecops-engineer.md` | 249 |
| [`disaster-recovery-specialist`](disaster-recovery-specialist/SKILL.md) | EXECUTOR | Software | `prompts/implementation/disaster-recovery-specialist.md` | 249 |
| [`documentation-manager`](documentation-manager/SKILL.md) | SUPERVISOR | Documentation | `prompts/audit/documentation-manager.md` | 264 |
| [`documentation-specialist`](documentation-specialist/SKILL.md) | EXECUTOR | Documentation | `prompts/implementation/documentation-specialist.md` | 237 |
| [`domain-expert-sme`](domain-expert-sme/SKILL.md) | SUPERVISOR | Analytics | `prompts/audit/domain-expert-sme.md` | 245 |
| [`embedded-developer`](embedded-developer/SKILL.md) | EXECUTOR | Software | `prompts/implementation/embedded-developer.md` | 250 |
| [`embedded-systems-lead`](embedded-systems-lead/SKILL.md) | SUPERVISOR | Software | `prompts/audit/embedded-systems-lead.md` | 263 |
| [`end-of-life-manager`](end-of-life-manager/SKILL.md) | SUPERVISOR | Product | `prompts/audit/end-of-life-manager.md` | 257 |
| [`end-user`](end-user/SKILL.md) | EXECUTOR | Support | `prompts/implementation/end-user.md` | 237 |
| [`engineering-manager`](engineering-manager/SKILL.md) | SUPERVISOR | Project | `prompts/audit/engineering-manager.md` | 244 |
| [`enterprise-architect`](enterprise-architect/SKILL.md) | SUPERVISOR | Architecture | `prompts/audit/enterprise-architect.md` | 245 |
| [`external-auditor`](external-auditor/SKILL.md) | SUPERVISOR | Audit | `prompts/audit/external-auditor.md` | 245 |
| [`finance-manager`](finance-manager/SKILL.md) | SUPERVISOR | Project | `prompts/audit/finance-manager.md` | 245 |
| [`fine-tuning-engineer`](fine-tuning-engineer/SKILL.md) | EXECUTOR | AI | `prompts/implementation/fine-tuning-engineer.md` | 238 |
| [`finops-specialist`](finops-specialist/SKILL.md) | SUPERVISOR | DevOps | `prompts/audit/finops-specialist.md` | 244 |
| [`firmware-engineer`](firmware-engineer/SKILL.md) | EXECUTOR | Software | `prompts/implementation/firmware-engineer.md` | 261 |
| [`founder`](founder/SKILL.md) | SUPERVISOR | Business | `prompts/audit/founder.md` | 248 |
| [`frontend-developer`](frontend-developer/SKILL.md) | EXECUTOR | Software | `prompts/implementation/frontend-developer.md` | 249 |
| [`full-stack-developer`](full-stack-developer/SKILL.md) | EXECUTOR | Software | `prompts/implementation/full-stack-developer.md` | 249 |
| [`game-designer`](game-designer/SKILL.md) | EXECUTOR | Design | `prompts/implementation/game-designer.md` | 238 |
| [`game-developer`](game-developer/SKILL.md) | EXECUTOR | Software | `prompts/implementation/game-developer.md` | 237 |
| [`graphic-designer`](graphic-designer/SKILL.md) | EXECUTOR | Design | `prompts/implementation/graphic-designer.md` | 238 |
| [`growth-manager`](growth-manager/SKILL.md) | SUPERVISOR | Growth | `prompts/audit/growth-manager.md` | 244 |
| [`hr-people-manager`](hr-people-manager/SKILL.md) | SUPERVISOR | HR | `prompts/audit/hr-people-manager.md` | 245 |
| [`iam-identity-engineer`](iam-identity-engineer/SKILL.md) | EXECUTOR | Security | `prompts/implementation/iam-identity-engineer.md` | 238 |
| [`incident-commander`](incident-commander/SKILL.md) | SUPERVISOR | Operations | `prompts/audit/incident-commander.md` | 248 |
| [`incident-manager`](incident-manager/SKILL.md) | SUPERVISOR | Project | `prompts/audit/incident-manager.md` | 257 |
| [`incident-response-engineer`](incident-response-engineer/SKILL.md) | EXECUTOR | Security | `prompts/implementation/incident-response-engineer.md` | 265 |
| [`infrastructure-engineer`](infrastructure-engineer/SKILL.md) | EXECUTOR | DevOps | `prompts/implementation/infrastructure-engineer.md` | 236 |
| [`infrastructure-manager`](infrastructure-manager/SKILL.md) | SUPERVISOR | DevOps | `prompts/audit/infrastructure-manager.md` | 263 |
| [`investor`](investor/SKILL.md) | SUPERVISOR | Business | `prompts/audit/investor.md` | 245 |
| [`iot-engineer`](iot-engineer/SKILL.md) | EXECUTOR | Software | `prompts/implementation/iot-engineer.md` | 249 |
| [`ip-copyright-specialist`](ip-copyright-specialist/SKILL.md) | SUPERVISOR | Compliance | `prompts/audit/ip-copyright-specialist.md` | 244 |
| [`kyc-aml-specialist`](kyc-aml-specialist/SKILL.md) | EXECUTOR | Compliance | `prompts/implementation/kyc-aml-specialist.md` | 238 |
| [`legacy-modernization-engineer`](legacy-modernization-engineer/SKILL.md) | EXECUTOR | Software | `prompts/implementation/legacy-modernization-engineer.md` | 261 |
| [`legal-advisor`](legal-advisor/SKILL.md) | SUPERVISOR | Compliance | `prompts/audit/legal-advisor.md` | 245 |
| [`load-stress-tester`](load-stress-tester/SKILL.md) | EXECUTOR | Testing | `prompts/implementation/load-stress-tester.md` | 248 |
| [`localization-manager`](localization-manager/SKILL.md) | SUPERVISOR | Documentation | `prompts/audit/localization-manager.md` | 264 |
| [`localization-specialist`](localization-specialist/SKILL.md) | EXECUTOR | Documentation | `prompts/implementation/localization-specialist.md` | 237 |
| [`maintenance-engineer`](maintenance-engineer/SKILL.md) | EXECUTOR | Software | `prompts/implementation/maintenance-engineer.md` | 249 |
| [`marketing-specialist`](marketing-specialist/SKILL.md) | EXECUTOR | Growth | `prompts/implementation/marketing-specialist.md` | 248 |
| [`migration-specialist`](migration-specialist/SKILL.md) | EXECUTOR | Software | `prompts/implementation/migration-specialist.md` | 261 |
| [`mlops-engineer`](mlops-engineer/SKILL.md) | EXECUTOR | AI | `prompts/implementation/mlops-engineer.md` | 236 |
| [`mobile-developer`](mobile-developer/SKILL.md) | EXECUTOR | Software | `prompts/implementation/mobile-developer.md` | 238 |
| [`motion-designer`](motion-designer/SKILL.md) | EXECUTOR | Design | `prompts/implementation/motion-designer.md` | 238 |
| [`network-engineer`](network-engineer/SKILL.md) | EXECUTOR | DevOps | `prompts/implementation/network-engineer.md` | 237 |
| [`observability-engineer`](observability-engineer/SKILL.md) | EXECUTOR | DevOps | `prompts/implementation/observability-engineer.md` | 249 |
| [`on-call-engineer`](on-call-engineer/SKILL.md) | EXECUTOR | DevOps | `prompts/implementation/on-call-engineer.md` | 248 |
| [`operations-manager`](operations-manager/SKILL.md) | SUPERVISOR | Project | `prompts/audit/operations-manager.md` | 244 |
| [`partnership-manager`](partnership-manager/SKILL.md) | SUPERVISOR | Growth | `prompts/audit/partnership-manager.md` | 245 |
| [`payments-billing-engineer`](payments-billing-engineer/SKILL.md) | EXECUTOR | Software | `prompts/implementation/payments-billing-engineer.md` | 238 |
| [`penetration-tester`](penetration-tester/SKILL.md) | EXECUTOR | Security | `prompts/implementation/penetration-tester.md` | 261 |
| [`performance-engineer`](performance-engineer/SKILL.md) | EXECUTOR | Testing | `prompts/implementation/performance-engineer.md` | 249 |
| [`performance-engineering-lead`](performance-engineering-lead/SKILL.md) | SUPERVISOR | Testing | `prompts/audit/performance-engineering-lead.md` | 263 |
| [`platform-engineer`](platform-engineer/SKILL.md) | EXECUTOR | DevOps | `prompts/implementation/platform-engineer.md` | 238 |
| [`platform-owner`](platform-owner/SKILL.md) | SUPERVISOR | Operations | `prompts/audit/platform-owner.md` | 262 |
| [`pmo`](pmo/SKILL.md) | SUPERVISOR | Project | `prompts/audit/pmo.md` | 246 |
| [`principal-engineer`](principal-engineer/SKILL.md) | SUPERVISOR | Software | `prompts/audit/principal-engineer.md` | 246 |
| [`privacy-compliance-officer`](privacy-compliance-officer/SKILL.md) | SUPERVISOR | Compliance | `prompts/audit/privacy-compliance-officer.md` | 245 |
| [`privacy-engineer`](privacy-engineer/SKILL.md) | EXECUTOR | Security | `prompts/implementation/privacy-engineer.md` | 249 |
| [`procurement-manager`](procurement-manager/SKILL.md) | SUPERVISOR | Growth | `prompts/audit/procurement-manager.md` | 264 |
| [`procurement-specialist`](procurement-specialist/SKILL.md) | EXECUTOR | Growth | `prompts/implementation/procurement-specialist.md` | 238 |
| [`product-analyst`](product-analyst/SKILL.md) | EXECUTOR | Analytics | `prompts/implementation/product-analyst.md` | 237 |
| [`product-analyst-lead`](product-analyst-lead/SKILL.md) | SUPERVISOR | Analytics | `prompts/audit/product-analyst-lead.md` | 264 |
| [`product-designer`](product-designer/SKILL.md) | EXECUTOR | Design | `prompts/implementation/product-designer.md` | 250 |
| [`product-manager-pm`](product-manager-pm/SKILL.md) | SUPERVISOR | Product | `prompts/audit/product-manager-pm.md` | 256 |
| [`product-marketing-manager`](product-marketing-manager/SKILL.md) | SUPERVISOR | Growth | `prompts/audit/product-marketing-manager.md` | 246 |
| [`product-owner-po`](product-owner-po/SKILL.md) | SUPERVISOR | Product | `prompts/audit/product-owner-po.md` | 246 |
| [`product-owner-post-release`](product-owner-post-release/SKILL.md) | SUPERVISOR | Software | `prompts/audit/product-owner-post-release.md` | 256 |
| [`product-visionary`](product-visionary/SKILL.md) | SUPERVISOR | Business | `prompts/audit/product-visionary.md` | 247 |
| [`program-manager`](program-manager/SKILL.md) | SUPERVISOR | Product | `prompts/audit/program-manager.md` | 245 |
| [`project-manager`](project-manager/SKILL.md) | SUPERVISOR | Project | `prompts/audit/project-manager.md` | 256 |
| [`project-sponsor`](project-sponsor/SKILL.md) | SUPERVISOR | Business | `prompts/audit/project-sponsor.md` | 233 |
| [`prompt-engineer`](prompt-engineer/SKILL.md) | EXECUTOR | AI | `prompts/implementation/prompt-engineer.md` | 250 |
| [`qa-engineer`](qa-engineer/SKILL.md) | EXECUTOR | Testing | `prompts/implementation/qa-engineer.md` | 250 |
| [`qa-lead`](qa-lead/SKILL.md) | SUPERVISOR | Project | `prompts/audit/qa-lead.md` | 256 |
| [`quality-manager`](quality-manager/SKILL.md) | SUPERVISOR | Project | `prompts/audit/quality-manager.md` | 246 |
| [`rag-retrieval-engineer`](rag-retrieval-engineer/SKILL.md) | EXECUTOR | AI | `prompts/implementation/rag-retrieval-engineer.md` | 238 |
| [`recruiter`](recruiter/SKILL.md) | EXECUTOR | HR | `prompts/implementation/recruiter.md` | 237 |
| [`recruitment-manager`](recruitment-manager/SKILL.md) | SUPERVISOR | HR | `prompts/audit/recruitment-manager.md` | 264 |
| [`refactoring-engineer`](refactoring-engineer/SKILL.md) | EXECUTOR | Software | `prompts/implementation/refactoring-engineer.md` | 249 |
| [`release-engineer`](release-engineer/SKILL.md) | EXECUTOR | DevOps | `prompts/implementation/release-engineer.md` | 237 |
| [`release-manager`](release-manager/SKILL.md) | SUPERVISOR | DevOps | `prompts/audit/release-manager.md` | 262 |
| [`revenue-operations-analyst`](revenue-operations-analyst/SKILL.md) | EXECUTOR | Growth | `prompts/implementation/revenue-operations-analyst.md` | 238 |
| [`risk-manager`](risk-manager/SKILL.md) | SUPERVISOR | Project | `prompts/audit/risk-manager.md` | 244 |
| [`sales-manager`](sales-manager/SKILL.md) | SUPERVISOR | Growth | `prompts/audit/sales-manager.md` | 244 |
| [`sales-representative`](sales-representative/SKILL.md) | EXECUTOR | Growth | `prompts/implementation/sales-representative.md` | 237 |
| [`scrum-master`](scrum-master/SKILL.md) | SUPERVISOR | Project | `prompts/audit/scrum-master.md` | 257 |
| [`scrum-product-team`](scrum-product-team/SKILL.md) | EXECUTOR | Support | `prompts/implementation/scrum-product-team.md` | 249 |
| [`search-relevance-engineer`](search-relevance-engineer/SKILL.md) | EXECUTOR | Software | `prompts/implementation/search-relevance-engineer.md` | 238 |
| [`security-architect`](security-architect/SKILL.md) | SUPERVISOR | Architecture | `prompts/audit/security-architect.md` | 258 |
| [`security-auditor`](security-auditor/SKILL.md) | EXECUTOR | Security | `prompts/implementation/security-auditor.md` | 254 |
| [`security-engineer`](security-engineer/SKILL.md) | EXECUTOR | Security | `prompts/implementation/security-engineer.md` | 237 |
| [`security-governance-manager`](security-governance-manager/SKILL.md) | SUPERVISOR | Security | `prompts/audit/security-governance-manager.md` | 262 |
| [`seo-specialist`](seo-specialist/SKILL.md) | EXECUTOR | Growth | `prompts/implementation/seo-specialist.md` | 236 |
| [`service-owner`](service-owner/SKILL.md) | SUPERVISOR | Operations | `prompts/audit/service-owner.md` | 262 |
| [`soc-analyst`](soc-analyst/SKILL.md) | EXECUTOR | Security | `prompts/implementation/soc-analyst.md` | 253 |
| [`soc2-iso27001-readiness-specialist`](soc2-iso27001-readiness-specialist/SKILL.md) | EXECUTOR | Compliance | `prompts/implementation/soc2-iso27001-readiness-specialist.md` | 238 |
| [`software-architect`](software-architect/SKILL.md) | EXECUTOR | Architecture | `prompts/implementation/software-architect.md` | 249 |
| [`software-engineer`](software-engineer/SKILL.md) | EXECUTOR | Software | `prompts/implementation/software-engineer.md` | 262 |
| [`solution-architect`](solution-architect/SKILL.md) | SUPERVISOR | Architecture | `prompts/audit/solution-architect.md` | 257 |
| [`sre-site-reliability-engineer`](sre-site-reliability-engineer/SKILL.md) | EXECUTOR | DevOps | `prompts/implementation/sre-site-reliability-engineer.md` | 248 |
| [`staff-engineer`](staff-engineer/SKILL.md) | EXECUTOR | Software | `prompts/implementation/staff-engineer.md` | 249 |
| [`support-manager`](support-manager/SKILL.md) | SUPERVISOR | Support | `prompts/audit/support-manager.md` | 250 |
| [`system-administrator`](system-administrator/SKILL.md) | EXECUTOR | DevOps | `prompts/implementation/system-administrator.md` | 236 |
| [`system-architect`](system-architect/SKILL.md) | EXECUTOR | Architecture | `prompts/implementation/system-architect.md` | 238 |
| [`technical-evangelist`](technical-evangelist/SKILL.md) | EXECUTOR | Software | `prompts/implementation/technical-evangelist.md` | 237 |
| [`technical-lead-tech-lead`](technical-lead-tech-lead/SKILL.md) | SUPERVISOR | Software | `prompts/audit/technical-lead-tech-lead.md` | 257 |
| [`technical-project-manager`](technical-project-manager/SKILL.md) | SUPERVISOR | Project | `prompts/audit/technical-project-manager.md` | 256 |
| [`technical-recruiter`](technical-recruiter/SKILL.md) | EXECUTOR | HR | `prompts/implementation/technical-recruiter.md` | 237 |
| [`technical-support-engineer`](technical-support-engineer/SKILL.md) | EXECUTOR | Support | `prompts/implementation/technical-support-engineer.md` | 237 |
| [`technical-writer`](technical-writer/SKILL.md) | EXECUTOR | Documentation | `prompts/implementation/technical-writer.md` | 237 |
| [`test-automation-engineer`](test-automation-engineer/SKILL.md) | EXECUTOR | Testing | `prompts/implementation/test-automation-engineer.md` | 238 |
| [`test-engineer`](test-engineer/SKILL.md) | EXECUTOR | Testing | `prompts/implementation/test-engineer.md` | 237 |
| [`third-party-integration-specialist`](third-party-integration-specialist/SKILL.md) | EXECUTOR | Software | `prompts/implementation/third-party-integration-specialist.md` | 236 |
| [`tool-developer`](tool-developer/SKILL.md) | EXECUTOR | AI | `prompts/implementation/tool-developer.md` | 254 |
| [`translator`](translator/SKILL.md) | EXECUTOR | Documentation | `prompts/implementation/translator.md` | 225 |
| [`ui-designer`](ui-designer/SKILL.md) | EXECUTOR | Design | `prompts/implementation/ui-designer.md` | 238 |
| [`ui-ux-research-participants`](ui-ux-research-participants/SKILL.md) | EXECUTOR | Support | `prompts/implementation/ui-ux-research-participants.md` | 225 |
| [`ux-designer`](ux-designer/SKILL.md) | EXECUTOR | Design | `prompts/implementation/ux-designer.md` | 250 |
| [`ux-researcher`](ux-researcher/SKILL.md) | EXECUTOR | Analytics | `prompts/implementation/ux-researcher.md` | 250 |
| [`ux-writer-content-designer`](ux-writer-content-designer/SKILL.md) | EXECUTOR | Documentation | `prompts/implementation/ux-writer-content-designer.md` | 237 |
| [`vendor-manager`](vendor-manager/SKILL.md) | SUPERVISOR | Project | `prompts/audit/vendor-manager.md` | 244 |
| [`vulnerability-management-specialist`](vulnerability-management-specialist/SKILL.md) | EXECUTOR | Security | `prompts/implementation/vulnerability-management-specialist.md` | 253 |

_Count: 209 skills — generated on 2026-09-27 by `scripts/build_skills.py`_
