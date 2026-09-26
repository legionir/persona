# Persona Skills

هر پوشه یک **Agent Skill** است: `SKILL.md` هستهٔ عملیاتی (وقتی تسک مطابقت کرد خوانده می‌شود) و
`references/` متن کامل persona برای وقتی که به جزئیات قرارداد نیاز است.

نصب در Claude Code (پروژه):

```bash
# کل کتابخانه
cp -r skills/<name> .claude/skills/

# یا همهٔ skillها
for d in skills/*/; do cp -r "$d" .claude/skills/; done
```

بازتولید: `python3 scripts/build_skills.py` — اعتبارسنجی: `python3 scripts/validate_skills.py`

فهرست کامل و متادیتای ماشین‌خوان: [`index.json`](index.json)

| Skill | نوع | حوزه | منبع | خطوط SKILL.md |
|---|---|---|---|---|
| [`architecture-review-architecture-audit`](architecture-review-architecture-audit/SKILL.md) | ترکیبی | ترکیبی | `Architecture Review & Architecture Audit.md` | 135 |
| [`codebase-integrity-audit-protocol`](codebase-integrity-audit-protocol/SKILL.md) | ترکیبی | ترکیبی | `codebase-integrity-audit-protocol.md` | 71 |
| [`execution-plan-generator`](execution-plan-generator/SKILL.md) | ترکیبی | ترکیبی | `Execution Plan Generator.md` | 48 |
| [`forensic-codebase-review-audit`](forensic-codebase-review-audit/SKILL.md) | ترکیبی | ترکیبی | `Forensic Codebase Review & Audit.md` | 133 |
| [`production-readiness-reliability-audit`](production-readiness-reliability-audit/SKILL.md) | ترکیبی | ترکیبی | `Production Readiness & Reliability Audit.md` | 104 |
| [`accessibility-specialist`](accessibility-specialist/SKILL.md) | مجری | Design | `prompts/implementation/accessibility-specialist.md` | 236 |
| [`account-manager`](account-manager/SKILL.md) | ناظر | Support | `prompts/audit/account-manager.md` | 244 |
| [`agent-architect`](agent-architect/SKILL.md) | مجری | AI | `prompts/implementation/agent-architect.md` | 253 |
| [`agent-evaluator`](agent-evaluator/SKILL.md) | مجری | AI | `prompts/implementation/agent-evaluator.md` | 253 |
| [`agent-integration-engineer`](agent-integration-engineer/SKILL.md) | مجری | AI | `prompts/implementation/agent-integration-engineer.md` | 252 |
| [`agent-safety-engineer`](agent-safety-engineer/SKILL.md) | مجری | AI | `prompts/implementation/agent-safety-engineer.md` | 251 |
| [`agentic-prompt-specialist`](agentic-prompt-specialist/SKILL.md) | مجری | AI | `prompts/implementation/agentic-prompt-specialist.md` | 252 |
| [`agile-coach`](agile-coach/SKILL.md) | ناظر | Project | `prompts/audit/agile-coach.md` | 244 |
| [`ai-engineer`](ai-engineer/SKILL.md) | مجری | AI | `prompts/implementation/ai-engineer.md` | 249 |
| [`ai-engineer-lead`](ai-engineer-lead/SKILL.md) | ناظر | AI | `prompts/audit/ai-engineer-lead.md` | 266 |
| [`ai-ml-engineer`](ai-ml-engineer/SKILL.md) | مجری | AI | `prompts/implementation/ai-ml-engineer.md` | 248 |
| [`application-security-engineer`](application-security-engineer/SKILL.md) | مجری | Security | `prompts/implementation/application-security-engineer.md` | 248 |
| [`architecture-review-board`](architecture-review-board/SKILL.md) | ناظر | Architecture | `prompts/audit/architecture-review-board.md` | 262 |
| [`aso-specialist`](aso-specialist/SKILL.md) | مجری | Growth | `prompts/implementation/aso-specialist.md` | 235 |
| [`audit-specialist`](audit-specialist/SKILL.md) | ناظر | Audit | `prompts/audit/audit-specialist.md` | 257 |
| [`backend-developer`](backend-developer/SKILL.md) | مجری | Software | `prompts/implementation/backend-developer.md` | 236 |
| [`backup-administrator`](backup-administrator/SKILL.md) | مجری | Software | `prompts/implementation/backup-administrator.md` | 247 |
| [`beta-tester`](beta-tester/SKILL.md) | مجری | Support | `prompts/implementation/beta-tester.md` | 236 |
| [`bi-analyst`](bi-analyst/SKILL.md) | مجری | Analytics | `prompts/implementation/bi-analyst.md` | 237 |
| [`board-of-directors`](board-of-directors/SKILL.md) | ناظر | Business | `prompts/audit/board-of-directors.md` | 244 |
| [`build-engineer`](build-engineer/SKILL.md) | مجری | DevOps | `prompts/implementation/build-engineer.md` | 236 |
| [`business-analyst-ba`](business-analyst-ba/SKILL.md) | مجری | Analytics | `prompts/implementation/business-analyst-ba.md` | 247 |
| [`business-continuity-manager`](business-continuity-manager/SKILL.md) | ناظر | Project | `prompts/audit/business-continuity-manager.md` | 245 |
| [`business-development-manager`](business-development-manager/SKILL.md) | ناظر | Growth | `prompts/audit/business-development-manager.md` | 246 |
| [`cao`](cao/SKILL.md) | ناظر | Audit | `prompts/audit/cao.md` | 264 |
| [`change-manager`](change-manager/SKILL.md) | ناظر | Project | `prompts/audit/change-manager.md` | 257 |
| [`chief-design-officer`](chief-design-officer/SKILL.md) | ناظر | Design | `prompts/audit/chief-design-officer.md` | 264 |
| [`chief-privacy-officer`](chief-privacy-officer/SKILL.md) | ناظر | Compliance | `prompts/audit/chief-privacy-officer.md` | 262 |
| [`cio`](cio/SKILL.md) | ناظر | Business | `prompts/audit/cio.md` | 260 |
| [`ciso`](ciso/SKILL.md) | ناظر | Security | `prompts/audit/ciso.md` | 252 |
| [`cloud-architect`](cloud-architect/SKILL.md) | ناظر | Architecture | `prompts/audit/cloud-architect.md` | 246 |
| [`cloud-engineer`](cloud-engineer/SKILL.md) | مجری | DevOps | `prompts/implementation/cloud-engineer.md` | 235 |
| [`cloud-security-engineer`](cloud-security-engineer/SKILL.md) | مجری | Security | `prompts/implementation/cloud-security-engineer.md` | 251 |
| [`community-director`](community-director/SKILL.md) | ناظر | Growth | `prompts/audit/community-director.md` | 263 |
| [`community-manager`](community-manager/SKILL.md) | مجری | Support | `prompts/implementation/community-manager.md` | 235 |
| [`contract-manager`](contract-manager/SKILL.md) | ناظر | Compliance | `prompts/audit/contract-manager.md` | 245 |
| [`cto`](cto/SKILL.md) | ناظر | Business | `prompts/audit/cto.md` | 263 |
| [`customer-success-manager`](customer-success-manager/SKILL.md) | ناظر | Support | `prompts/audit/customer-success-manager.md` | 244 |
| [`customer-support-agent`](customer-support-agent/SKILL.md) | مجری | Support | `prompts/implementation/customer-support-agent.md` | 248 |
| [`cybersecurity-engineer`](cybersecurity-engineer/SKILL.md) | مجری | Security | `prompts/implementation/cybersecurity-engineer.md` | 247 |
| [`data-analyst`](data-analyst/SKILL.md) | مجری | Analytics | `prompts/implementation/data-analyst.md` | 248 |
| [`data-architect`](data-architect/SKILL.md) | ناظر | Architecture | `prompts/audit/data-architect.md` | 246 |
| [`data-engineer`](data-engineer/SKILL.md) | مجری | Data | `prompts/implementation/data-engineer.md` | 247 |
| [`data-governance-manager`](data-governance-manager/SKILL.md) | ناظر | Data | `prompts/audit/data-governance-manager.md` | 262 |
| [`data-scientist`](data-scientist/SKILL.md) | مجری | AI | `prompts/implementation/data-scientist.md` | 249 |
| [`database-administrator-dba`](database-administrator-dba/SKILL.md) | مجری | Data | `prompts/implementation/database-administrator-dba.md` | 247 |
| [`database-engineer`](database-engineer/SKILL.md) | مجری | Data | `prompts/implementation/database-engineer.md` | 238 |
| [`database-security-specialist`](database-security-specialist/SKILL.md) | مجری | Security | `prompts/implementation/database-security-specialist.md` | 251 |
| [`decommission-engineer`](decommission-engineer/SKILL.md) | مجری | Software | `prompts/implementation/decommission-engineer.md` | 271 |
| [`deployment-engineer`](deployment-engineer/SKILL.md) | مجری | Software | `prompts/implementation/deployment-engineer.md` | 247 |
| [`design-manager`](design-manager/SKILL.md) | ناظر | Design | `prompts/audit/design-manager.md` | 263 |
| [`design-system-designer`](design-system-designer/SKILL.md) | مجری | Design | `prompts/implementation/design-system-designer.md` | 248 |
| [`desktop-developer`](desktop-developer/SKILL.md) | مجری | Software | `prompts/implementation/desktop-developer.md` | 237 |
| [`development-manager`](development-manager/SKILL.md) | ناظر | Project | `prompts/audit/development-manager.md` | 263 |
| [`devops-engineer`](devops-engineer/SKILL.md) | مجری | DevOps | `prompts/implementation/devops-engineer.md` | 248 |
| [`devops-manager`](devops-manager/SKILL.md) | ناظر | DevOps | `prompts/audit/devops-manager.md` | 262 |
| [`devrel`](devrel/SKILL.md) | مجری | Software | `prompts/implementation/devrel.md` | 236 |
| [`devsecops-engineer`](devsecops-engineer/SKILL.md) | مجری | DevOps | `prompts/implementation/devsecops-engineer.md` | 248 |
| [`disaster-recovery-specialist`](disaster-recovery-specialist/SKILL.md) | مجری | Software | `prompts/implementation/disaster-recovery-specialist.md` | 248 |
| [`documentation-manager`](documentation-manager/SKILL.md) | ناظر | Documentation | `prompts/audit/documentation-manager.md` | 264 |
| [`documentation-specialist`](documentation-specialist/SKILL.md) | مجری | Documentation | `prompts/implementation/documentation-specialist.md` | 236 |
| [`domain-expert-sme`](domain-expert-sme/SKILL.md) | ناظر | Analytics | `prompts/audit/domain-expert-sme.md` | 245 |
| [`embedded-developer`](embedded-developer/SKILL.md) | مجری | Software | `prompts/implementation/embedded-developer.md` | 249 |
| [`embedded-systems-lead`](embedded-systems-lead/SKILL.md) | ناظر | Software | `prompts/audit/embedded-systems-lead.md` | 262 |
| [`end-of-life-manager`](end-of-life-manager/SKILL.md) | ناظر | Product | `prompts/audit/end-of-life-manager.md` | 257 |
| [`end-user`](end-user/SKILL.md) | مجری | Support | `prompts/implementation/end-user.md` | 236 |
| [`engineering-manager`](engineering-manager/SKILL.md) | ناظر | Project | `prompts/audit/engineering-manager.md` | 244 |
| [`enterprise-architect`](enterprise-architect/SKILL.md) | ناظر | Architecture | `prompts/audit/enterprise-architect.md` | 245 |
| [`external-auditor`](external-auditor/SKILL.md) | ناظر | Audit | `prompts/audit/external-auditor.md` | 245 |
| [`finance-manager`](finance-manager/SKILL.md) | ناظر | Project | `prompts/audit/finance-manager.md` | 245 |
| [`finops-specialist`](finops-specialist/SKILL.md) | ناظر | DevOps | `prompts/audit/finops-specialist.md` | 244 |
| [`firmware-engineer`](firmware-engineer/SKILL.md) | مجری | Software | `prompts/implementation/firmware-engineer.md` | 260 |
| [`founder`](founder/SKILL.md) | ناظر | Business | `prompts/audit/founder.md` | 247 |
| [`frontend-developer`](frontend-developer/SKILL.md) | مجری | Software | `prompts/implementation/frontend-developer.md` | 248 |
| [`full-stack-developer`](full-stack-developer/SKILL.md) | مجری | Software | `prompts/implementation/full-stack-developer.md` | 248 |
| [`game-developer`](game-developer/SKILL.md) | مجری | Software | `prompts/implementation/game-developer.md` | 236 |
| [`graphic-designer`](graphic-designer/SKILL.md) | مجری | Design | `prompts/implementation/graphic-designer.md` | 237 |
| [`growth-manager`](growth-manager/SKILL.md) | ناظر | Growth | `prompts/audit/growth-manager.md` | 244 |
| [`hr-people-manager`](hr-people-manager/SKILL.md) | ناظر | HR | `prompts/audit/hr-people-manager.md` | 245 |
| [`incident-manager`](incident-manager/SKILL.md) | ناظر | Project | `prompts/audit/incident-manager.md` | 257 |
| [`incident-response-engineer`](incident-response-engineer/SKILL.md) | مجری | Security | `prompts/implementation/incident-response-engineer.md` | 264 |
| [`infrastructure-engineer`](infrastructure-engineer/SKILL.md) | مجری | DevOps | `prompts/implementation/infrastructure-engineer.md` | 235 |
| [`infrastructure-manager`](infrastructure-manager/SKILL.md) | ناظر | DevOps | `prompts/audit/infrastructure-manager.md` | 263 |
| [`investor`](investor/SKILL.md) | ناظر | Business | `prompts/audit/investor.md` | 245 |
| [`iot-engineer`](iot-engineer/SKILL.md) | مجری | Software | `prompts/implementation/iot-engineer.md` | 248 |
| [`ip-copyright-specialist`](ip-copyright-specialist/SKILL.md) | ناظر | Compliance | `prompts/audit/ip-copyright-specialist.md` | 244 |
| [`legacy-modernization-engineer`](legacy-modernization-engineer/SKILL.md) | مجری | Software | `prompts/implementation/legacy-modernization-engineer.md` | 260 |
| [`legal-advisor`](legal-advisor/SKILL.md) | ناظر | Compliance | `prompts/audit/legal-advisor.md` | 245 |
| [`load-stress-tester`](load-stress-tester/SKILL.md) | مجری | Testing | `prompts/implementation/load-stress-tester.md` | 247 |
| [`localization-manager`](localization-manager/SKILL.md) | ناظر | Documentation | `prompts/audit/localization-manager.md` | 264 |
| [`localization-specialist`](localization-specialist/SKILL.md) | مجری | Documentation | `prompts/implementation/localization-specialist.md` | 236 |
| [`maintenance-engineer`](maintenance-engineer/SKILL.md) | مجری | Software | `prompts/implementation/maintenance-engineer.md` | 248 |
| [`marketing-specialist`](marketing-specialist/SKILL.md) | مجری | Growth | `prompts/implementation/marketing-specialist.md` | 247 |
| [`migration-specialist`](migration-specialist/SKILL.md) | مجری | Software | `prompts/implementation/migration-specialist.md` | 260 |
| [`mlops-engineer`](mlops-engineer/SKILL.md) | مجری | AI | `prompts/implementation/mlops-engineer.md` | 235 |
| [`mobile-developer`](mobile-developer/SKILL.md) | مجری | Software | `prompts/implementation/mobile-developer.md` | 237 |
| [`motion-designer`](motion-designer/SKILL.md) | مجری | Design | `prompts/implementation/motion-designer.md` | 237 |
| [`network-engineer`](network-engineer/SKILL.md) | مجری | DevOps | `prompts/implementation/network-engineer.md` | 236 |
| [`observability-engineer`](observability-engineer/SKILL.md) | مجری | DevOps | `prompts/implementation/observability-engineer.md` | 248 |
| [`on-call-engineer`](on-call-engineer/SKILL.md) | مجری | DevOps | `prompts/implementation/on-call-engineer.md` | 247 |
| [`operations-manager`](operations-manager/SKILL.md) | ناظر | Project | `prompts/audit/operations-manager.md` | 244 |
| [`partnership-manager`](partnership-manager/SKILL.md) | ناظر | Growth | `prompts/audit/partnership-manager.md` | 245 |
| [`penetration-tester`](penetration-tester/SKILL.md) | مجری | Security | `prompts/implementation/penetration-tester.md` | 260 |
| [`performance-engineer`](performance-engineer/SKILL.md) | مجری | Testing | `prompts/implementation/performance-engineer.md` | 248 |
| [`performance-engineering-lead`](performance-engineering-lead/SKILL.md) | ناظر | Testing | `prompts/audit/performance-engineering-lead.md` | 263 |
| [`platform-owner`](platform-owner/SKILL.md) | ناظر | Operations | `prompts/audit/platform-owner.md` | 262 |
| [`pmo`](pmo/SKILL.md) | ناظر | Project | `prompts/audit/pmo.md` | 246 |
| [`principal-engineer`](principal-engineer/SKILL.md) | ناظر | Software | `prompts/audit/principal-engineer.md` | 246 |
| [`privacy-compliance-officer`](privacy-compliance-officer/SKILL.md) | ناظر | Compliance | `prompts/audit/privacy-compliance-officer.md` | 245 |
| [`privacy-engineer`](privacy-engineer/SKILL.md) | مجری | Security | `prompts/implementation/privacy-engineer.md` | 248 |
| [`procurement-manager`](procurement-manager/SKILL.md) | ناظر | Growth | `prompts/audit/procurement-manager.md` | 263 |
| [`procurement-specialist`](procurement-specialist/SKILL.md) | مجری | Growth | `prompts/implementation/procurement-specialist.md` | 237 |
| [`product-analyst`](product-analyst/SKILL.md) | مجری | Analytics | `prompts/implementation/product-analyst.md` | 236 |
| [`product-analyst-lead`](product-analyst-lead/SKILL.md) | ناظر | Analytics | `prompts/audit/product-analyst-lead.md` | 264 |
| [`product-designer`](product-designer/SKILL.md) | مجری | Design | `prompts/implementation/product-designer.md` | 249 |
| [`product-manager-pm`](product-manager-pm/SKILL.md) | ناظر | Product | `prompts/audit/product-manager-pm.md` | 256 |
| [`product-marketing-manager`](product-marketing-manager/SKILL.md) | ناظر | Growth | `prompts/audit/product-marketing-manager.md` | 246 |
| [`product-owner-po`](product-owner-po/SKILL.md) | ناظر | Product | `prompts/audit/product-owner-po.md` | 246 |
| [`product-owner-release`](product-owner-release/SKILL.md) | ناظر | Product | `prompts/audit/product-owner-release.md` | 256 |
| [`product-visionary`](product-visionary/SKILL.md) | ناظر | Business | `prompts/audit/product-visionary.md` | 246 |
| [`program-manager`](program-manager/SKILL.md) | ناظر | Product | `prompts/audit/program-manager.md` | 245 |
| [`project-manager`](project-manager/SKILL.md) | ناظر | Project | `prompts/audit/project-manager.md` | 256 |
| [`project-sponsor`](project-sponsor/SKILL.md) | ناظر | Business | `prompts/audit/project-sponsor.md` | 233 |
| [`prompt-engineer`](prompt-engineer/SKILL.md) | مجری | AI | `prompts/implementation/prompt-engineer.md` | 249 |
| [`qa-engineer`](qa-engineer/SKILL.md) | مجری | Testing | `prompts/implementation/qa-engineer.md` | 249 |
| [`qa-lead`](qa-lead/SKILL.md) | ناظر | Project | `prompts/audit/qa-lead.md` | 256 |
| [`quality-manager`](quality-manager/SKILL.md) | ناظر | Project | `prompts/audit/quality-manager.md` | 246 |
| [`recruiter`](recruiter/SKILL.md) | مجری | HR | `prompts/implementation/recruiter.md` | 236 |
| [`recruitment-manager`](recruitment-manager/SKILL.md) | ناظر | HR | `prompts/audit/recruitment-manager.md` | 263 |
| [`refactoring-engineer`](refactoring-engineer/SKILL.md) | مجری | Software | `prompts/implementation/refactoring-engineer.md` | 248 |
| [`release-engineer`](release-engineer/SKILL.md) | مجری | DevOps | `prompts/implementation/release-engineer.md` | 236 |
| [`release-manager`](release-manager/SKILL.md) | ناظر | DevOps | `prompts/audit/release-manager.md` | 262 |
| [`risk-manager`](risk-manager/SKILL.md) | ناظر | Project | `prompts/audit/risk-manager.md` | 244 |
| [`sales-manager`](sales-manager/SKILL.md) | ناظر | Growth | `prompts/audit/sales-manager.md` | 244 |
| [`sales-representative`](sales-representative/SKILL.md) | مجری | Growth | `prompts/implementation/sales-representative.md` | 236 |
| [`scrum-master`](scrum-master/SKILL.md) | ناظر | Project | `prompts/audit/scrum-master.md` | 257 |
| [`scrum-product-team`](scrum-product-team/SKILL.md) | مجری | Support | `prompts/implementation/scrum-product-team.md` | 248 |
| [`security-architect`](security-architect/SKILL.md) | ناظر | Architecture | `prompts/audit/security-architect.md` | 258 |
| [`security-auditor`](security-auditor/SKILL.md) | مجری | Security | `prompts/implementation/security-auditor.md` | 253 |
| [`security-engineer`](security-engineer/SKILL.md) | مجری | Security | `prompts/implementation/security-engineer.md` | 236 |
| [`security-governance-manager`](security-governance-manager/SKILL.md) | ناظر | Security | `prompts/audit/security-governance-manager.md` | 262 |
| [`seo-specialist`](seo-specialist/SKILL.md) | مجری | Growth | `prompts/implementation/seo-specialist.md` | 235 |
| [`service-owner`](service-owner/SKILL.md) | ناظر | Operations | `prompts/audit/service-owner.md` | 262 |
| [`soc-analyst`](soc-analyst/SKILL.md) | مجری | Security | `prompts/implementation/soc-analyst.md` | 252 |
| [`software-architect`](software-architect/SKILL.md) | مجری | Architecture | `prompts/implementation/software-architect.md` | 248 |
| [`software-engineer`](software-engineer/SKILL.md) | مجری | Software | `prompts/implementation/software-engineer.md` | 261 |
| [`solution-architect`](solution-architect/SKILL.md) | ناظر | Architecture | `prompts/audit/solution-architect.md` | 257 |
| [`sre-site-reliability-engineer`](sre-site-reliability-engineer/SKILL.md) | مجری | DevOps | `prompts/implementation/sre-site-reliability-engineer.md` | 247 |
| [`staff-engineer`](staff-engineer/SKILL.md) | مجری | Software | `prompts/implementation/staff-engineer.md` | 248 |
| [`support-manager`](support-manager/SKILL.md) | ناظر | Support | `prompts/audit/support-manager.md` | 250 |
| [`system-administrator`](system-administrator/SKILL.md) | مجری | DevOps | `prompts/implementation/system-administrator.md` | 235 |
| [`system-architect`](system-architect/SKILL.md) | مجری | Architecture | `prompts/implementation/system-architect.md` | 237 |
| [`technical-evangelist`](technical-evangelist/SKILL.md) | مجری | Software | `prompts/implementation/technical-evangelist.md` | 236 |
| [`technical-lead-tech-lead`](technical-lead-tech-lead/SKILL.md) | ناظر | Software | `prompts/audit/technical-lead-tech-lead.md` | 257 |
| [`technical-project-manager`](technical-project-manager/SKILL.md) | ناظر | Project | `prompts/audit/technical-project-manager.md` | 256 |
| [`technical-recruiter`](technical-recruiter/SKILL.md) | مجری | HR | `prompts/implementation/technical-recruiter.md` | 236 |
| [`technical-support-engineer`](technical-support-engineer/SKILL.md) | مجری | Support | `prompts/implementation/technical-support-engineer.md` | 236 |
| [`technical-writer`](technical-writer/SKILL.md) | مجری | Documentation | `prompts/implementation/technical-writer.md` | 236 |
| [`test-automation-engineer`](test-automation-engineer/SKILL.md) | مجری | Testing | `prompts/implementation/test-automation-engineer.md` | 237 |
| [`test-engineer`](test-engineer/SKILL.md) | مجری | Testing | `prompts/implementation/test-engineer.md` | 236 |
| [`third-party-integration-specialist`](third-party-integration-specialist/SKILL.md) | مجری | Software | `prompts/implementation/third-party-integration-specialist.md` | 235 |
| [`tool-developer`](tool-developer/SKILL.md) | مجری | AI | `prompts/implementation/tool-developer.md` | 253 |
| [`translator`](translator/SKILL.md) | مجری | Documentation | `prompts/implementation/translator.md` | 224 |
| [`ui-designer`](ui-designer/SKILL.md) | مجری | Design | `prompts/implementation/ui-designer.md` | 237 |
| [`ui-ux-research-participants`](ui-ux-research-participants/SKILL.md) | مجری | Support | `prompts/implementation/ui-ux-research-participants.md` | 224 |
| [`ux-designer`](ux-designer/SKILL.md) | مجری | Design | `prompts/implementation/ux-designer.md` | 249 |
| [`ux-researcher`](ux-researcher/SKILL.md) | مجری | Analytics | `prompts/implementation/ux-researcher.md` | 249 |
| [`ux-writer-content-designer`](ux-writer-content-designer/SKILL.md) | مجری | Documentation | `prompts/implementation/ux-writer-content-designer.md` | 236 |
| [`vendor-manager`](vendor-manager/SKILL.md) | ناظر | Project | `prompts/audit/vendor-manager.md` | 244 |
| [`vulnerability-management-specialist`](vulnerability-management-specialist/SKILL.md) | مجری | Security | `prompts/implementation/vulnerability-management-specialist.md` | 252 |

_تعداد: 175 skill — ساخته‌شده در 2026-09-26 توسط `scripts/build_skills.py`_
