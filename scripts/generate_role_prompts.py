#!/usr/bin/env python3
"""Generate role-specific prompt files for every job title in README.md.

Each role has its own hand-authored spec (mission + role-specific targets +
role-specific acceptance criteria). The prompts are NOT generic templates with
only the title swapped — the content is bespoke per role.

!! DO NOT RUN THIS FILE DIRECTLY !!
===================================

This module is a *library*: `scripts/generate_personas.py` imports `SPECS`,
`DETAILS`, `_slug`, `read_rows`, `load_details`, ... from it.

Its own `main()` writes prompts with the legacy `_slug()` naming
(`chief-technology-officer-cto.md`), while the canonical pipeline uses
`SLUG_OVERRIDES` from `role_extras.py` (`cto.md`). Running it directly creates
duplicate files beside the canonical ones and rewrites the README link cells,
which breaks `validate_personas.py`.

The canonical entry point is:

    python3 scripts/generate_personas.py          # or: make prompts

`main()` below refuses to run unless `--i-know` is passed.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
AUDIT_DIR = ROOT / "prompts" / "audit"
IMPL_DIR = ROOT / "prompts" / "implementation"
AUDITS_DIR = ROOT / "audits"
DETAILS = ROOT / "details.md"


DETAIL_COLS = 23  # legacy details.md layout (kept for backward compat)
MAIN_COLS = 28    # width of the merged main role table in README.md


DETAIL_KEYS = [
    "mission", "responsibilities", "scope", "required", "optional",
    "context", "preconditions", "procedure", "decision", "allowed",
    "restricted", "outputs", "quality", "evidence", "handoff",
    "escalation", "permissions", "lifecycle", "memory", "kpi", "duties",
]



# --------------------------------------------------------------------------
# Per-role bespoke spec.
# Each spec defines:
#   domain   -> coarse functional area (for organization only)
#   mission  -> what this role is actually trying to achieve
#   audit    -> specific things this observer role must verify
#   impl     -> specific things this executor role must deliver/plan
#   accept   -> role-specific acceptance criteria
# --------------------------------------------------------------------------

def sp(domain, mission, audit, impl, accept):
    return {"domain": domain, "mission": mission,
            "audit": audit, "impl": impl, "accept": accept}


SPECS = {
    # ----------------------------- founder -----------------------------
    "founder": sp(
        "strategy",
        r"Are overall business direction and the goals of major decision-making defined clearly and actionably?",
        [
            r"Clarity and consistency between vision, mission, and short-term goals",
            r"Ability to translate top-level direction into executable priorities",
            r"Clarity of the decision boundary and accountability",
            r"Alignment of major decisions with resources and team capacity",
        ],
        [
            r"Defining vision/mission and measurable objectives",
            r"Setting non-goals and boundaries deliberately not pursued",
            r"Defining the decision model for major issues (who, when)",
            r"Mapping top-level goals to traceable KPIs",
        ],
        [
            r"Every major decision ties to one objective and one KPI",
            r"Vision/mission are free of contradiction with the non-goals",
            r"The decision function is documented (owner, criteria, timing)",
        ],
    ),
    "product-visionary": sp(
        "strategy",
        r"Does the product vision genuinely solve the user/market problem and is it actionable?",
        [
            r"Accuracy of the problem being solved (problem statement)",
            r"Differentiation of the vision from competitors and alternatives",
            r"Clarity of the value proposition for the target user",
            r"Alignment of the vision with technical/market feasibility",
        ],
        [
            r"Documenting the problem statement and target user",
            r"Defining the value proposition and key differentiators",
            r"Defining the boundary of the conditions in which the product has value",
            r"Mapping the vision to specific features (feature assumptions)",
        ],
        [
            r"The problem statement is unambiguous and evidence-backed",
            r"The value proposition is stated in one measurable sentence",
            r"Every proposed feature ties to a hypothesis or success criterion",
        ],
    ),
    "investor": sp(
        "strategy",
        r"Is the investment accompanied by acceptable risk and a measurable return path?",
        [
            r"Validity of the financial model and revenue assumptions",
            r"Coverage of investment risks (market, technology, execution)",
            r"Clarity of funding milestones and capital consumption",
            r"Ability to return capital (ROI) and exit within the stated horizon",
        ],
        [
            r"Defining the financial structure, burn rate, and runway",
            r"Defining investment milestones and funding gates",
            r"Modelling revenue/cost scenarios and break-even",
            r"Defining exit criteria and conditions for raising more capital",
        ],
        [
            r"The financial model has explicit assumptions and base/best/worst scenarios",
            r"Every milestone has a progress indicator and a funding condition",
            r"Risks are documented with probability/impact and a reduction plan",
        ],
    ),
    "board-of-directors": sp(
        "strategy",
        r"Does the board properly oversee strategy, governance, and corporate performance?",
        [
            r"Sufficiency of management reporting for board decision-making",
            r"Alignment of board decisions with regulations and stakeholder interests",
            r"Transparency of conflicts of interest and member independence",
            r"Monitoring performance against the strategic plan",
        ],
        [
            r"Defining the governance framework and board/CEO authorities",
            r"Defining periodic management reporting (financial, risk, strategy)",
            r"Implementing the conflict-of-interest resolution and voting mechanism",
            r"Implementing board/management performance evaluation",
        ],
        [
            r"Authorities and decision boundaries are written down",
            r"Management reporting covers at least strategy, finance, risk, and execution",
            r"The conflict-of-interest and voting mechanism is defined and recorded",
        ],
    ),
    "project-sponsor": sp(
        "strategy",
        r"Does the project sponsor remove obstacles financially and organisationally, and is their support durable and traceable?",
        [
            r"Clarity of the sponsor's supportive role (financial, political, organisational)",
            r"Effectiveness in removing major obstacles at the right time",
            r"Alignment of support with project scope and interests",
            r"How major changes and budget control are handled",
        ],
        [
            r"Defining the project charter and the sponsor's scope of support",
            r"Defining the process for major decisions and scope change",
            r"Defining the sponsor's communication channel with the team/stakeholders",
            r"Defining indicators for monitoring support and obstacle removal",
        ],
        [
            r"The project charter has a sponsor and clearly stated authority limits",
            r"The approve/reject process for major changes is documented",
            r"Every major obstacle removed ties to a stakeholder, date, and outcome",
        ],
    ),

    # --------------------------- analysis / BA -------------------------
    "business-analyst-ba": sp(
        "analysis",
        r"Have business needs been converted into precise, testable, unambiguous requirements?",
        [
            r"Complete requirement coverage and unambiguous acceptance criteria",
            r"Business flows are validated and measurable",
            r"Stakeholder mapping and engagement",
            r"Alignment with existing processes/systems (as-is/to-be)",
        ],
        [
            r"Extracting functional, non-functional, and data requirements",
            r"Writing user stories with acceptance criteria and edge cases",
            r"Drawing as-is and to-be and gap analysis",
            r"Defining the requirement-to-output/test traceability matrix",
        ],
        [
            r"Every requirement has unambiguous acceptance criteria",
            r"The gap analysis includes the effect on process and data",
            r"The requirement-to-acceptance/test traceability matrix is complete",
        ],
    ),
    "domain-expert-sme": sp(
        "analysis",
        r"Is domain expertise correctly reflected in the product/requirements and correctly interpreted?",
        [
            r"Correctness of domain concepts (values, terms, rules)",
            r"Accuracy of business rules and domain edges",
            r"The effect of misinterpreting the domain on implementation",
            r"Sufficiency of domain documentation for the implementation team",
        ],
        [
            r"Defining the domain glossary/terms and business rules",
            r"Identifying domain depth (core/support/generic)",
            r"Defining domain scenarios and edges with experts",
            r"Mapping domain concepts to the data model/logic",
        ],
        [
            r"Every domain concept has one definition/glossary entry",
            r"Every business rule has a positive and negative scenario",
            r"Domain interpretations have been carried into code/data without semantic error",
        ],
    ),

    # ----------------------------- product -----------------------------
    "product-manager-pm": sp(
        "product",
        r"Is the product aligned with strategy and is feature prioritisation based on real value?",
        [
            r"Alignment of the roadmap with product and market goals",
            r"Prioritisation logic (value/risk/effort)",
            r"Defining and monitoring KPIs and learning from feedback",
            r"Clarity of scope and management of product change",
        ],
        [
            r"Defining the product roadmap with phases and go/no-go conditions",
            r"Prioritising features with weighted shortest job first or RICE",
            r"Defining product KPIs and the data sources for measuring them",
            r"Managing scope change with the product decision model",
        ],
        [
            r"Every roadmap feature has a value/risk/effort criterion",
            r"KPIs have an equation, a data source, and a target",
            r"Scope changes are recorded with their effect on the roadmap",
        ],
    ),
    "product-owner-po": sp(
        "product",
        r"Does the product backlog contain ready, prioritised, testable items?",
        [
            r"Backlog quality (complete, decomposed, prioritised)",
            r"Clarity of the definition of ready and definition of done",
            r"Alignment of acceptance criteria with user expectation",
            r"Coverage of non-technical/technical stories and dependencies",
        ],
        [
            r"Defining and maintaining the product backlog and refinement",
            r"Writing acceptance criteria and the definition of ready",
            r"Prioritising and labelling value/effort/dependency",
            r"Mapping the backlog to sprint goals and outputs",
        ],
        [
            r"Every item has measurable acceptance criteria and a definition of ready",
            r"The backlog is consistent in priority and dependency",
            r"The sprint goal has a traceable link to the selected items",
        ],
    ),
    "program-manager": sp(
        "product",
        r"Are several related projects progressing in alignment, without interference, under shared management?",
        [
            r"Alignment of project goals with programme goals",
            r"Managing dependencies and interference between projects",
            r"Allocating shared resources and managing capacity",
            r"Integrated programme reporting against risk/interval",
        ],
        [
            r"Defining the programme structure and mapping projects to goals",
            r"Mapping and managing cross-project dependencies",
            r"Defining the shared-risk/resource and change mechanism",
            r"Defining programme reporting (status/blocker/dependency)",
        ],
        [
            r"Every project ties to one programme goal",
            r"Cross dependencies are recorded with owner/date/status",
            r"Programme reporting includes dependencies, risks, and deviations",
        ],
    ),
    "product-owner-release": sp(
        "product",
        r"Is the product properly evolved after release and is the future backlog aligned with user reality?",
        [
            r"Quality and priority of the backlog after release",
            r"Alignment of evolution with received user feedback",
            r"Preparing next-release requirements and data alignment",
            r"Defining the review cycle for the value of released features",
        ],
        [
            r"Defining the post-release feedback collection mechanism",
            r"Re-prioritising the backlog with real usage data",
            r"Defining the released-feature review cycle (KPI/retention)",
            r"Defining the link between releases and the future backlog",
        ],
        [
            r"Every released feature has a feedback source and a decision",
            r"The future backlog is updated on the basis of data and priority",
            r"The feature evaluation cycle has a stated date and output",
        ],
    ),
    "end-of-life-manager": sp(
        "product",
        r"Is the product/phase end-of-life managed with minimal harm to customer and team?",
        [
            r"Documenting the reasons for ending support and its scope",
            r"Migration message and path for the customer",
            r"Coverage of data, contract, and support in the transition period",
            r"Planning and communications for stakeholders",
        ],
        [
            r"Defining the EOL matrix (date, phases, remaining support)",
            r"Defining the migration/replacement path for users",
            r"Defining end-of-life communications and documents",
            r"Implementing data/contract maintenance through the transition period",
        ],
        [
            r"The EOL matrix contains the dates and remaining services",
            r"The migration path for users is executable and documented",
            r"EOL communications include timing, audience, message, and channel",
        ],
    ),

    # ----------------------------- management --------------------------
    "project-manager": sp(
        "management",
        r"Is the project progressing within time, resources, risk, and cost limits with team coordination?",
        [
            r"Alignment of the schedule with dependencies and real capacity",
            r"Scope coverage and control, avoiding scope creep",
            r"Quality of the risk plan and obstacle management",
            r"Transparency of status and reporting to stakeholders",
        ],
        [
            r"Defining the WBS, schedule, and critical path",
            r"Defining budget/resources and the variance control mechanism",
            r"Defining risks/issues and the blocker-removal mechanism",
            r"Defining phase gates and periodic status reporting",
        ],
        [
            r"Every step has a stated owner, time, and dependency",
            r"Scope control is documented with change control",
            r"Status reporting includes progress, variance, risk, and blockers",
        ],
    ),
    "technical-project-manager": sp(
        "management",
        r"Is the technical project managed with a balance between technical requirements and time/resources?",
        [
            r"Clarity of technical decisions and their effect on time/resources",
            r"Sound reasoning in technical estimate/risk",
            r"Coordination between the technical team and non-technical stakeholders",
            r"Coverage of technical dependencies and infrastructure readiness",
        ],
        [
            r"Defining the sequence of technical work on the basis of dependencies",
            r"Estimating technical effort/risk and the risk-reduction plan",
            r"Defining the technical readiness criterion (technical definition of ready)",
            r"Coordination between engineering/DevOps/QA teams with checkpoints",
        ],
        [
            r"Every technical task has a documented dependency and estimate/risk",
            r"The technical risk plan has an owner, time, and effect",
            r"Technical gates are defined with a verifiable output",
        ],
    ),
    "pmo": sp(
        "management",
        r"Are project management processes standardised, measurable, and repeatable?",
        [
            r"Sufficiency and currency of PM standards",
            r"Alignment of reports and templates across the organisation",
            r"Implementation of the control framework and gates",
            r"Quality of planning data and PPM reporting",
        ],
        [
            r"Defining the PM documentation/reporting standard and templates",
            r"Defining phase gates and stage-gate processes",
            r"Implementing PMO indicators (variance, delivery, risk)",
            r"Defining training/guidance and compliance audit",
        ],
        [
            r"PM templates and reports exist as standard in the repository",
            r"Each phase's gates have defined inputs and outputs",
            r"PMO indicators are defined and extractable",
        ],
    ),
    "scrum-master": sp(
        "management",
        r"Is Scrum facilitated correctly and are team obstacles removed or clarified in time?",
        [
            r"Correct execution of Scrum events (planning/review/retro/standup)",
            r"Effectiveness of impediment removal and obstacle recording/tracking",
            r"Quality of facilitation and team collaboration",
            r"Alignment with Agile principles (self-organisation, feedback, improvement)",
        ],
        [
            r"Defining the event cadence and each meeting's template",
            r"Defining the impediment record/track/resolve process",
            r"Defining team health indicators (velocity, commit, retros)",
            r"Defining improvement behaviour integrated with Scrum development",
        ],
        [
            r"Every event has a stated goal, output, and time",
            r"Team obstacles have a status, owner, and date",
            r"The retro has an action item and feeds the next retro",
        ],
    ),
    "agile-coach": sp(
        "management",
        r"Is the Agile process genuinely maturing at team or organisation level?",
        [
            r"How well Agile values/principles are honoured in practice",
            r"The impact of coaching on team behaviour",
            r"Quality of training/documentation and adoption",
            r"Monitoring improvement (cycle time, handoff, blockages)",
        ],
        [
            r"Defining the Agile maturity model (measurement points)",
            r"Defining the coaching cycle: assess → observe → give feedback → act",
            r"Defining meeting, retro, and Lean patterns and techniques",
            r"Defining improvement indicators (cycle time/throughput/blockage)",
        ],
        [
            r"Maturity assessment is recorded with evidence and a stated scale",
            r"The coaching plan has a goal, action, and review",
            r"Improvement indicators are measured from real data (cycle time)",
        ],
    ),
    "engineering-manager": sp(
        "management",
        r"Is the engineering team properly managed in terms of people, capacity, and development process?",
        [
            r"Alignment of capacity with workload and priorities",
            r"Quality of people growth/feedback and career paths",
            r"Health of the development process (review, merge, on-call)",
            r"Engagement in technical decisions aligned with architecture",
        ],
        [
            r"Defining the capacity model and work assignment",
            r"Defining the feedback/coaching and growth cycle",
            r"Defining engineering health indicators (DORA, PR, on-call)",
            r"Defining technical coordination with tech leads and decision records",
        ],
        [
            r"Each person's/team's capacity against workload is transparent",
            r"The feedback/coaching cycle has a schedule and an output",
            r"Development health indicators are defined and reported",
        ],
    ),
    "operations-manager": sp(
        "management",
        r"Are ongoing product operations after launch stable, efficient, and monitorable?",
        [
            r"Coverage of operational processes (team, SLA, runbooks)",
            r"Effectiveness of escalation and incident management",
            r"Operational cost and resources are optimised",
            r"Quality of operational reporting and continuous improvement",
        ],
        [
            r"Defining runbooks and day-to-day operational processes",
            r"Defining the SLA and escalation matrix",
            r"Defining operational indicators (uptime/MTTR/cost)",
            r"Defining the improvement cycle and process review",
        ],
        [
            r"Runbooks have steps, owners, and timings",
            r"SLA and escalation are available with audience, timing, and threshold",
            r"Operational indicators are reportable and comparable",
        ],
    ),
    "risk-manager": sp(
        "management",
        r"Are project risks identified, assessed, and managed with an effective reduction plan?",
        [
            r"Completeness of risk identification (technical, financial, schedule, organisational)",
            r"Accuracy of probability/impact scoring",
            r"Effectiveness of reduction and response plans",
            r"Currency of and reporting on risk throughout the project",
        ],
        [
            r"Defining the risk identify/assess/score framework",
            r"Defining the response, reduction, and risk owner",
            r"Defining risk monitoring/review at project gates",
            r"Defining risk recording and reporting",
        ],
        [
            r"Risk records include probability, impact, response, and owner",
            r"The reduction plan has an action, time, and effectiveness criterion",
            r"Risks are updated at periodic reviews",
        ],
    ),
    "change-manager": sp(
        "management",
        r"Are scope, process, and organisational changes applied with control and risk reduction?",
        [
            r"Clarity and completeness of the change request",
            r"Assessing the change's effect on scope, budget, schedule, and team",
            r"Adherence to the approval process and change board",
            r"Sufficiency of communications/training and change adoption",
        ],
        [
            r"Defining the change request form and flow",
            r"Defining impact/risk assessment and the decision proposal",
            r"Defining the change approve/execute/review gate",
            r"Defining the communications/training plan and adoption monitoring",
        ],
        [
            r"Every change has a request, impact, decision, date, and owner",
            r"The approval process includes a board or decision-maker role",
            r"Approved changes are monitored with periodic adoption/impact reporting",
        ],
    ),
    "incident-manager": sp(
        "management",
        r"Are production crises managed and improved quickly and with minimal damage?",
        [
            r"Clarity of the severity definition and escalation path",
            r"Effectiveness of the IC team and immediate actions",
            r"Quality of communication during an incident",
            r"Quality of the post-mortem and action follow-up",
        ],
        [
            r"Defining incident classification and the escalation matrix",
            r"Defining the incident commander/communication structure",
            r"Defining the detect/mitigate/recover flow",
            r"Defining the blameless post-mortem process and actions",
        ],
        [
            r"Every severity has a response, time, and owner",
            r"The incident log has times, location, and actions",
            r"The post-mortem has a root cause, action, owner, and deadline",
        ],
    ),
    "vendor-manager": sp(
        "management",
        r"Is the relationship with suppliers/service providers managed effectively and assessably?",
        [
            r"Quality of contract/SLA and alignment with requirements",
            r"Assessment of supplier performance and risk",
            r"Management of vendor cost and relationship/strategy",
            r"Vendor offboarding and exit approach",
        ],
        [
            r"Defining vendor selection/assessment criteria",
            r"Defining the SLA, performance reporting, and periodic review",
            r"Defining the relationship structure, risk, and contract",
            r"Defining exit/transition and dependency reduction",
        ],
        [
            r"Every vendor has an SLA, assessment criterion, and owner",
            r"Periodic reviews are recorded with performance evidence",
            r"An exit/replacement plan exists for critical vendors",
        ],
    ),
    "business-continuity-manager": sp(
        "management",
        r"Is business continuity guaranteed in a crisis and have its EQP been tested?",
        [
            r"Coverage of crisis scenarios in the BCP",
            r"Continuity of critical services/processes in the scenario",
            r"Quality of documentation/communications and roles",
            r"Realism of BCP tests and of RTO/RPO",
        ],
        [
            r"Defining the BIA and critical service/process",
            r"Defining RTO/RPO and continuity scenarios",
            r"Defining the test/exercise plan and assessment",
            r"Defining crisis roles, responsibilities, and communication channels",
        ],
        [
            r"The BIA has a critical service and RTO/RPO",
            r"Every crisis scenario has a gap/free exercise and a result",
            r"Crisis roles and channels are written down and accessible",
        ],
    ),
    "qa-lead": sp(
        "management",
        r"Are the QA process and team properly managed and aligned with output quality?",
        [
            r"Coverage of the test strategy and team readiness",
            r"Quality of methodology, tooling, and the coverage matrix",
            r"Alignment of QA expectations with product goals",
            r"First pass on defects/reports and trend",
        ],
        [
            r"Defining the test strategy, level, and scale",
            r"Defining the coverage matrix and risk-based testing",
            r"Defining the defect/review/quality-metric cycle",
            r"Defining QA team growth and capacity assessment",
        ],
        [
            r"The test strategy includes scope, risk, and standard",
            r"Coverage/defect trend is reportable",
            r"Defect triage and prioritisation follow a stated process",
        ],
    ),

    # ------------------------------ devops -----------------------------
    "devops-engineer": sp(
        "devops",
        r"Is the build/test/deploy cycle and infrastructure stable, automated, and safe?",
        [
            r"Repeatability and stability of the pipeline",
            r"Coverage of failure/rollback in deployment",
            r"Security and secret management in the pipeline",
            r"Alignment with environments and configuration",
        ],
        [
            r"Defining CI/CD (jobs, env, gates, caching)",
            r"Defining IaC and secret/configuration management",
            r"Defining rollback, canary, and blue-green",
            r"Defining monitoring/alerting for the pipeline",
        ],
        [
            r"The pipeline is green in CI and ignores no error",
            r"Deployment has a rollback and is under external control",
            r"Secrets are not hardcoded in code and are on secure paths",
        ],
    ),
    "sre-site-reliability-engineer": sp(
        "devops",
        r"Are service reliability, availability, and performance maintained at the SLA level?",
        [
            r"Clarity of SLO/SLI and reliability coverage",
            r"Quality of the error budget and release decisions",
            r"Coverage of monitoring/alerting and runbook detail",
            r"Effectiveness of reliability improvement (blameless/MTTR)",
        ],
        [
            r"Defining SLOs/SLIs and the error budget",
            r"Defining monitoring, alerting, and incident flow",
            r"Defining capacity, baseline, and performance",
            r"Defining the improvement cycle and postmortem",
        ],
        [
            r"Every SLO has an SLI and an error budget",
            r"Every alert/runbook has a response, step, and owner",
            r"MTTR/availability and improvement actions are reportable",
        ],
    ),
    "cloud-engineer": sp(
        "devops",
        r"Is the cloud infrastructure secure, scalable, observable, and cost-effective?",
        [
            r"Cloud architecture, security, and scale pattern",
            r"Cost management and resource optimisation",
            r"Cleanup/drift and environment isolation",
            r"Backup/HA/disaster coverage in the cloud",
        ],
        [
            r"Defining environments, accounts, IAM, and landing zone",
            r"Implementing IaC and drift management",
            r"Optimising cost/scale and right-sizing",
            r"Implementing backup/DR/HA for critical services",
        ],
        [
            r"Cloud environments are isolated and use least privilege",
            r"Critical resources have backup/DR/HA",
            r"Cost is traceable by destination/vendor report",
        ],
    ),
    "cloud-architect": sp(
        "architecture",
        r"Is the cloud architecture consistent with needs, security, and best practices, and extensible?",
        [
            r"Selecting services and architecture suited to the workload",
            r"Managing security, identity, and network in the cloud",
            r"Scalability, recoverability, and cost",
            r"Consistency with the multi-cloud/on-prem strategy",
        ],
        [
            r"Selecting architecture (serverless/containers/VMs) and decisions",
            r"Defining network, IAM, security, and observability in the cloud",
            r"Defining scale, availability, and cost",
            r"Defining architecture decisions and trade-offs",
        ],
        [
            r"The cloud architecture has a review/decision record",
            r"Network, identity, and security are established with minimum permission",
            r"Scale, recovery, and cost are defined assessably",
        ],
    ),
    "infrastructure-engineer": sp(
        "devops",
        r"Is the infrastructure (server/network/storage) stable, secure, and scalable?",
        [
            r"Alignment of infrastructure with requirements and SLA",
            r"Managing infrastructure security, patching, and monitoring",
            r"Managing capacity and scale",
            r"Infrastructure backup/HA/disaster coverage",
        ],
        [
            r"Defining the provisioning/configuration standard",
            r"Implementing monitoring, patching, security, and hardening",
            r"Capacity planning and auto-scaling",
            r"Defining infrastructure backup/HA/DR and testing",
        ],
        [
            r"Critical infrastructure has HA, backup, and DR",
            r"Patching, monitoring, and security are run to plan and trend",
            r"Capacity is monitored with load evidence and criteria",
        ],
    ),
    "network-engineer": sp(
        "devops",
        r"Is the network designed/managed securely, stably, and with minimal disruption?",
        [
            r"Alignment of network design with needs and scale",
            r"Managing security, segmentation, firewall, IPS/IDS",
            r"Sufficiency of network monitoring and troubleshooting",
            r"DR/HA coverage and connectivity management",
        ],
        [
            r"Defining topology, VLAN, subnet, and routing",
            r"Defining perimeter security, firewall, and ACL",
            r"Defining network monitoring/alerting and runbook",
            r"Defining redundancy/HA and capacity planning",
        ],
        [
            r"The network architecture has redundancy and documentation",
            r"Security rules (ACL/firewall) are defined and traceable",
            r"Network alert/change reports are current",
        ],
    ),
    "system-administrator": sp(
        "devops",
        r"Are operating systems, servers, and base services kept stable, secure, and current?",
        [
            r"Stability of base services and time available",
            r"Security of user, permissions, patching, and files",
            r"Quality of automation and config management",
            r"Backup/restore and DR coverage",
        ],
        [
            r"Defining the server hardening and user standard",
            r"Defining automation (scripts/ansible) and config",
            r"Defining base monitoring, logging, and alerting",
            r"Defining backup/restore and testing",
        ],
        [
            r"Critical servers are covered by hardening and patching",
            r"The backup/restore and test procedure has been run and results captured",
            r"Base monitoring/logging is active and alerts are configured",
        ],
    ),

    # -------------------------------- qa --------------------------------
    "qa-engineer": sp(
        "qa",
        r"Are tests designed/executed with quality, coverage, and on a risk basis?",
        [
            r"Coverage of functional, regression, and edge",
            r"Quality of test cases and acceptance mapping",
            r"Stability and executability of tests",
            r"Documenting defects with evidence",
        ],
        [
            r"Designing the test plan, master test, and automation",
            r"Writing test cases with steps, expected results, and evidence",
            r"Defining the regression suite for releases",
            r"Defining the defect lifecycle and report",
        ],
        [
            r"Every requirement links to a test case and evidence",
            r"The regression suite is stable and executable in CI",
            r"Defects have severity, evidence, and flow",
        ],
    ),
    "test-engineer": sp(
        "qa",
        r"Are functional/technical tests executed precisely and on the basis of real scenarios?",
        [
            r"Quality of functional/technical test execution",
            r"Coverage of data scenarios and edge cases",
            r"Accuracy of reporting and evidence",
            r"Consistency with SLA/regression",
        ],
        [
            r"Preparing test data and environment setup",
            r"Executing functional/technical and regression tests",
            r"Documenting results and evidence",
            r"Coordinating with dev/PM for triage",
        ],
        [
            r"Every test record includes result, evidence, and date",
            r"Errors are reported with reproduction and evidence",
            r"Tests are repeatable with a documented environment",
        ],
    ),
    "test-automation-engineer": sp(
        "qa",
        r"Are automated tests stable, fast, and maintainable?",
        [
            r"Framework quality and flakiness",
            r"Coverage of automated suites in CI",
            r"Maintainability (selectors, data, isolation)",
            r"Execution speed and stability",
        ],
        [
            r"Selecting the framework and structure (page objects)",
            r"Writing maintained, data-isolated tests",
            r"Connecting to CI and reporting",
            r"Managing flaky tests and automatic regression",
        ],
        [
            r"Suites run in CI with reporting",
            r"Flaky tests have an owner and recorded issue",
            r"Automated tests can run in any environment",
        ],
    ),
    "performance-engineer": sp(
        "qa",
        r"Is performance testing, analysis, and optimisation carried out with reliable evidence?",
        [
            r"Clarity of performance and load goals",
            r"Quality of test criteria and absence of bias",
            r"Effectiveness of optimisation recommendations",
            r"Coverage of bottlenecks and capacity",
        ],
        [
            r"Defining workload, durations, sizes, and baseline",
            r"Running load, stress, and spike tests",
            r"Analysing bottlenecks and recommending optimisations",
            r"Performance reporting and comparison",
        ],
        [
            r"Performance goals are measurable against a baseline",
            r"Tests are reproducible with recorded config/values",
            r"Recommendations are reported with evidence and effect",
        ],
    ),
    "load-stress-tester": sp(
        "qa",
        r"Is system behaviour under load/high pressure stable and as expected?",
        [
            r"Realism of the load/stress scenario",
            r"Monitoring resources, collapse, and recovery",
            r"Coverage of capacity limits and endpoints",
            r"Accuracy of reporting and conclusions",
        ],
        [
            r"Defining the load model (RPS/users/consumption)",
            r"Running load, soak, and spike tests",
            r"Monitoring metrics and identifying failures",
            r"Capacity reporting and recommendations",
        ],
        [
            r"Load scenarios have goals, magnitude, and duration",
            r"The report includes metrics, errors, and thresholds",
            r"Recommendations are backed by capacity evidence",
        ],
    ),

    # ------------------------------ security ----------------------------
    "security-engineer": sp(
        "security",
        r"Are security controls properly implemented, configured, and monitored?",
        [
            r"Coverage of in-scope security controls",
            r"Managing vulnerabilities, patching, and permissions",
            r"Security of data, secrets, and config",
            r"Alignment with compliance",
        ],
        [
            r"Defining the control matrix and threat model",
            r"Implementing CIS hardening and patching",
            r"Managing secrets, permissions, and audit",
            r"Defining security tests, scanners, and triage",
        ],
        [
            r"Critical controls have implementation, testing, and reporting",
            r"Vulnerabilities have severity, owner, and deadline",
            r"Secrets and permissions comply with policy",
        ],
    ),
    "application-security-engineer": sp(
        "security",
        r"Is the application's own security (code, input, response content) guaranteed?",
        [
            r"OWASP-like coverage in code/API",
            r"Security of input, parameters, and authentication",
            r"Managing trust and data exposure",
            r"Security of race conditions, errors, and debug",
        ],
        [
            r"Implementing input validation and output encoding",
            r"Security of session, authz, CSRF, XSS, and SQLi",
            r"Secure error/exception handling and non-disclosing logs",
            r"Defining security code review and tests",
        ],
        [
            r"Inputs and outputs are validated and encoded",
            r"Authentication and authorisation are established with least privilege",
            r"Errors, logs, and exceptions do not disclose internals",
        ],
    ),
    "cybersecurity-engineer": sp(
        "security",
        r"Are systems and infrastructure protected against general attacks?",
        [
            r"Coverage of defence layers (endpoint/network/identity)",
            r"Monitoring, detection, and response (SIEM/EDR)",
            r"Managing threats, vulnerabilities, and remediation",
            r"Incident readiness and blockers",
        ],
        [
            r"Defining defence in depth and control layers",
            r"Implementing monitoring and threat detection",
            r"Managing incident response and playbooks",
            r"Defining baseline, hardening, and patching",
        ],
        [
            r"Layered defence and core controls are defined",
            r"Detection, response, and recovery have a runbook",
            r"Patching, hardening, and remediation are recorded against SLA",
        ],
    ),
    "penetration-tester": sp(
        "security",
        r"Are exploitable vulnerabilities identified/reported safely and with evidence?",
        [
            r"Legality of the test scope and authority",
            r"Quality of identification, exploitation, and evidence",
            r"Accuracy of severity and reproducibility",
            r"Safety of the test (no damage)",
        ],
        [
            r"Defining scope, rules, and authorisation",
            r"Running reconnaissance, testing, and exploitation",
            r"Documenting evidence, severity, and reproduction",
            r"Defining the report and cooperation with remediation",
        ],
        [
            r"Testing is carried out only within the authorised scope",
            r"Every finding has evidence, reproduction, and severity",
            r"The report includes explanation and a remediation path",
        ],
    ),
    "security-architect": sp(
        "architecture",
        r"Is the security architecture aligned with requirements, threats, and best practices?",
        [
            r"Coverage of controls and the model in the architecture",
            "safety/privacy/zero-trust",
            r"Managing trust boundaries and data flows",
            r"Consistency with compliance",
        ],
        [
            r"Designing the threat model and trust boundaries",
            r"Defining the security architecture and zero trust",
            r"Selecting controls, encryption, and identity",
            r"Defining security acceptance and review",
        ],
        [
            r"The architecture has trust boundaries and a threat model",
            r"Data, identity, and encryption comply with policy",
            r"Controls are defined with an acceptance criterion",
        ],
    ),
    "devsecops-engineer": sp(
        "devops",
        r"Is security integrated into the CI/CD cycle automatically and traceably?",
        [
            r"Security gates exist in CI",
            r"Coverage of scanning, risk, and dependencies",
            r"Managing secrets in the pipeline",
            r"Traceability and consistency of release security",
        ],
        [
            r"Defining security checks in the pipeline",
            r"Implementing SAST, DAST, and dependency scanning",
            r"Managing secrets and security gates",
            r"Defining reporting and compliance",
        ],
        [
            r"The pipeline has security gates",
            r"Scan findings have triage, owner, and disposition",
            r"Secrets are managed safely in CI",
        ],
    ),
    "privacy-engineer": sp(
        "security",
        r"Is the product designed so that personal and private data are protected?",
        [
            r"Mapping personal data and destinations",
            r"Adherence to principles (data minimisation, consent)",
            r"Security of processing, storage, and recovery",
            r"Coverage of user rights (delete, rectify)",
        ],
        [
            r"Defining the data inventory and retention",
            r"Implementing consent, minimisation, and access control",
            r"Implementing anonymisation and encryption",
            r"Implementing the delete/export process",
        ],
        [
            r"Personal data have maximum protection and SIEM coverage",
            r"The consent/user-rights mechanism is executable",
            r"Data recovery/deletion follows policy",
        ],
    ),
    "privacy-compliance-officer": sp(
        "compliance",
        r"Is compliance with privacy laws and regulations guaranteed with documentation and evidence?",
        [
            r"Map of applicable regulations",
            r"Coverage of consent, rights, and records",
            r"Quality of audit and controls",
            r"Accountability and the data programme process",
        ],
        [
            r"Defining the compliance framework and gaps",
            r"Implementing controls, documentation, and evidence",
            r"Defining the data request response process",
            r"Defining audit, reporting, and remediation",
        ],
        [
            r"Regulatory requirements are mapped to gaps and controls",
            r"The data-subject request process has an SLA",
            r"Audit evidence and reports exist",
        ],
    ),

    # ------------------------------- design -----------------------------
    "ui-designer": sp(
        "design",
        r"Does the user interface have quality in appearance, hierarchy, and consistency with the design system?",
        [
            r"Visual consistency with the existing design system",
            r"Hierarchy, balance, and space",
            r"Coverage of states (hover/focus/disabled/loading)",
            r"Consistency of responsive and a11y principles",
        ],
        [
            r"Extracting design tokens and UI patterns",
            r"Designing states, responsiveness, and grid",
            r"Respecting contrast, focus, and semantics",
            r"Using reusable components and tokens",
        ],
        [
            r"Every page is designed with the project's tokens, not hardcoded values",
            r"Key states are covered in the design",
            r"Contrast and accessibility are respected in the design",
        ],
    ),
    "ux-designer": sp(
        "design",
        r"Is the user experience properly designed in terms of path, friction, and discoverability?",
        [
            r"Clarity and efficiency of user paths",
            r"Feedback, error, dead-end, and recovery",
            r"Predictability and terminology consistency",
            r"Coverage of accessibility, keyboard, and stability",
        ],
        [
            r"Defining user flows and journeys",
            r"Designing feedback, error, and undo policies",
            r"Designing IA, navigation, and terminology",
            r"Evaluating with a11y and task completion",
        ],
        [
            r"Every path has entry points, exits, and error points",
            r"Destructive actions have confirmation and recovery",
            r"The glossary and terminology are consistent across the whole product",
        ],
    ),
    "product-designer": sp(
        "design",
        r"Does the product design strike a balance between UX/UI and product needs?",
        [
            r"Alignment of the design with product goals and constraints",
            r"Clarity and prioritisation of elements",
            r"Consistency with the product process and feedback",
            r"Implementability and scalability",
        ],
        [
            r"Defining the design problem, constraints, and scope",
            r"Combining UX flow with UI design and tokens",
            r"Coordinating with PM/tech and ensuring feasibility",
            r"Defining the feedback loop and iteration",
        ],
        [
            r"The design has a valid user path and constraints",
            r"The design is consistent with the design system/prototype",
            r"The design has been reviewed with the team and documented",
        ],
    ),
    "ux-researcher": sp(
        "analysis",
        r"Is user behaviour/need research and analysis carried out with valid methods?",
        [
            r"Validity of method and sampling",
            r"Coverage of bias and neutrality",
            r"Presence of evidence and traceable interpretation",
            r"Linkage of findings to the product decision",
        ],
        [
            r"Defining the research plan, objectives, and method",
            r"Running interviews, surveys, and usability studies",
            r"Analysing qualitative and quantitative evidence",
            r"Reporting insight with recommendations and stakeholders",
        ],
        [
            r"The research plan includes goal, method, and sampling",
            r"The analysis is evidence-based and free of bias",
            r"Recommendations link to the product decision",
        ],
    ),
    "ux-writer-content-designer": sp(
        "content",
        r"Are UI copy and microcopy clear, consistent, and aligned with the user?",
        [
            r"Clarity and consistency of language and terminology",
            r"Clear feedback, errors, and buttons",
            r"Consistency with tone of voice and a11y",
            r"Coverage of states and context",
        ],
        [
            r"Defining the voice, tone, and word guide",
            r"Writing copy for error, empty, success, and CTA",
            r"Reviewing UI copy consistency everywhere",
            r"Evaluating clarity, action, and impact",
        ],
        [
            r"Every text has a goal, audience, and action",
            r"Errors and feedback are clear and actionable",
            r"Product-wide terminology is consistent",
        ],
    ),
    "design-system-designer": sp(
        "design",
        r"Is the design system coherent, scalable, and maintainable?",
        [
            r"Completeness of tokens, components, and states",
            r"Consistency of docs and adoption",
            r"Maintainability and versioning",
            r"Consistency of a11y and responsive behaviour",
        ],
        [
            r"Defining tokens (colour, typography, spacing, radius)",
            r"Defining the component library and its states and variants",
            r"Defining docs, usage, and versioning",
            r"Defining governance and contribution for the design system",
        ],
        [
            r"Every component has states, variants, and docs",
            r"Tokens are central and free of hardcoding",
            r"Design-system version and changes are documented",
        ],
    ),
    "graphic-designer": sp(
        "design",
        r"Are graphic assets (icon/banner/image) consistent with brand identity?",
        [
            r"Consistency of style, colour, and scale",
            r"Quality of assets and format output",
            r"Compliance with brand rules and accessibility",
            r"Consistency with the design system",
        ],
        [
            r"Defining style, assets, and brand",
            r"Designing icons, illustrations, and banners at scale and format",
            r"Producing assets to naming and export standards",
            r"Assessing consistency and performance",
        ],
        [
            r"Assets are consistent in style and scale",
            r"Format and export match the standard",
            r"Assets are tied to scenario and brand and free of conflict",
        ],
    ),
    "motion-designer": sp(
        "design",
        r"Does animation/motion have quality, clarity, and consistency, and does it serve the UX?",
        [
            r"Whether animation serves the UX",
            r"Consistency of duration and easing",
            r"Reducing clutter, performance cost, and a11y cost",
            r"Consistency with the design system",
        ],
        [
            r"Defining motion principles, duration, and easing",
            r"Designing transitions, feedback, and hover",
            r"Respecting reduced-motion and performance",
            r"Defining a checklist for motion",
        ],
        [
            r"Every animation has a goal, duration, and easing",
            r"Motion respects reduced-motion",
            r"Motion is aligned with the design system",
        ],
    ),
    "accessibility-specialist": sp(
        "design",
        r"Is the product usable for all users in terms of accessibility and standards?",
        [
            r"WCAG coverage (contrast, keyboard, semantics)",
            r"Contrast, alternative content, and focus",
            r"Coverage of screen readers and forms",
            r"Readiness for disability use cases",
        ],
        [
            r"Defining a11y acceptance and checklist",
            r"Respecting semantic HTML, ARIA, alt, and labels",
            "manage focus/modal/keyboard",
            r"Compiling a11y tests and reviews",
        ],
        [
            r"Every page/component has labels, alt text, and semantics",
            r"Keyboard, focus, and modal behaviour are correct",
            r"Contrast and a11y are covered by checklists",
        ],
    ),

    # ------------------------------- content ----------------------------
    "technical-writer": sp(
        "content",
        r"Is the technical documentation precise, actionable, and appropriate to its audience?",
        [
            r"Technical accuracy and scenario coverage",
            r"Clarity of structure and executability (tutorials)",
            r"Consistency with release and system behaviour",
            r"Coverage of troubleshooting and FAQ",
        ],
        [
            r"Defining the docs structure (API, install, guide)",
            r"Documenting endpoints, params, and examples",
            r"Reviewing technical validity and version",
            r"Defining errors and troubleshooting",
        ],
        [
            r"Every doc has a goal, audience, and precise steps",
            r"Tutorials are executable from start to end",
            r"Docs are current with the release and behaviour",
        ],
    ),
    "documentation-specialist": sp(
        "content",
        r"Is the product documentation clear, complete, and coherent for the end user?",
        [
            r"Information is complete and usable",
            r"Consistency of structure, terminology, and language",
            r"Coverage of scenarios, steps, and challenges",
            r"Maintenance and periodic review",
        ],
        [
            r"Defining the docs structure and style guide",
            r"Authoring user guides, FAQs, and quickstarts",
            r"Reviewing accuracy and documentation UX",
            r"Managing maintenance and availability",
        ],
        [
            r"Every doc has a stated path, step, and outcome",
            r"Terminology and structure are consistent across all docs",
            r"Docs exist in the right release alongside the product",
        ],
    ),
    "localization-specialist": sp(
        "content",
        r"Is localisation, culture/language, and the local experience handled correctly?",
        [
            r"Translation quality and cultural fit",
            r"Consistency of strings, dates, numbers, and formats",
            r"Coverage of RTL/LTR and critical UI",
            r"Managing locale and glossary",
        ],
        [
            r"Defining locale, glossary, and style",
            r"Translating and localising strings and formats",
            r"Preparing RTL/LTR and adjustments",
            r"Testing the localised version and QA",
        ],
        [
            r"Content is consistent with locale and glossary",
            r"Local formats render correctly",
            r"Locale cases are covered by tests",
        ],
    ),
    "translator": sp(
        "content",
        r"Is content/documentation translation accurate, fluent, and technically correct?",
        [
            r"Semantic and terminological accuracy",
            r"Consistency of glossary and tone",
            r"Accuracy of technical terms, code, and names",
            r"Anticipating and covering source releases",
        ],
        [
            r"Defining glossary and tone per language",
            r"Translating source and terminology consistently",
            r"Contextual review and QA",
            r"Maintaining version and translation updates",
        ],
        [
            r"Translation is consistent with glossary and tone",
            r"Names, code, and technical terms are preserved in translation",
            r"Translation updates sync with the source release",
        ],
    ),

    # --------------------------- audit / compliance ---------------------
    "audit-specialist": sp(
        "assurance",
        r"Are processes and outputs audited independently, precisely, and on an evidence basis?",
        [
            r"Independence and completeness of audit coverage",
            r"Traceability of evidence",
            r"Compliance with standards and criteria",
            r"Quality of reporting and follow-up",
        ],
        [
            r"Defining audit scope, criteria, and reporting",
            r"Collecting evidence and testing controls",
            r"Recording findings with severity and evidence",
            r"Follow-up and remediation sequence",
        ],
        [
            r"Every finding has evidence, severity, and a recommendation",
            r"The audit report is documented with scope and criteria",
            r"Corrective actions have an owner and deadline",
        ],
    ),
    "external-auditor": sp(
        "assurance",
        r"Is the independent audit conducted impartially and with clear evidence from outside?",
        [
            r"Impartiality and audit independence",
            r"Complete coverage of scope and evidence",
            r"Compliance with regulations and standards",
            r"Quality of the report and trust in it",
        ],
        [
            r"Defining scope and criteria in the audit engagement",
            r"Collecting evidence and testing independently",
            r"Reporting findings with conclusions",
            r"Defining follow-up, accountability, and confirmation",
        ],
        [
            r"The audit is free of conflict and based on scope",
            r"Findings relate to evidence and standards",
            r"The report includes the conclusion and compliance state",
        ],
    ),
    "quality-manager": sp(
        "management",
        r"Is the quality of the whole product delivery process guaranteed by criteria and controls?",
        [
            r"Coverage of quality gates in the process",
            r"Quality of metrics (defect, coverage, rework)",
            r"Managing the quality plan and improvement",
            r"Consistency with standards",
        ],
        [
            r"Defining the quality policy, gates, and metrics",
            r"Defining inspections, reviews, and gates",
            r"Defining root-cause analysis and continuous improvement",
            r"Quality reporting and follow-up",
        ],
        [
            r"Every gate has a pass/fail criterion",
            r"Quality metrics are reported with data and trend",
            r"Improvement actions have an owner and effect",
        ],
    ),

    # ------------------------------- legal ------------------------------
    "legal-advisor": sp(
        "compliance",
        r"Are legal/contract matters and risks managed with precise advice?",
        [
            r"Coverage of contractual and legal risks",
            r"Clarity of responsibility, obligation, and ownership",
            r"Compliance with laws and constraints",
            r"Quality of evidence and documentation",
        ],
        [
            r"Defining contract and terms review",
            r"Identifying legal, liability, and IP risks",
            r"Defining legal points in the process (consent, DPA)",
            r"Defining follow-up and archiving",
        ],
        [
            r"Every contract has documented risk, terms, and responsibility",
            r"Legal matters are recorded with documentation and follow-up",
            r"Documentation, signatures, and archiving comply with policy",
        ],
    ),
    "ip-copyright-specialist": sp(
        "compliance",
        r"Are intellectual property, licences, and copyright managed correctly?",
        [
            r"Coverage of IP, licence, and copyright",
            r"Detecting infringement and risk",
            r"Managing third-party and open source",
            r"Documentation and rights tracking",
        ],
        [
            r"Defining the IP inventory and licence policy",
            r"Reviewing open source and licence compliance",
            r"Defining registration, maintenance, and renewal",
            r"Defining the claims response process",
        ],
        [
            r"Every asset is recorded with IP status and licence",
            r"The open-source/licence database is current",
            r"Legal actions and claims are documented",
        ],
    ),
    "contract-manager": sp(
        "compliance",
        r"Are contracts and obligations controlled by a precise management cycle and without negligence?",
        [
            r"Coverage of contract content and terms",
            r"Managing schedules and renewals",
            r"Consistency with SLA and obligations",
            r"Traceability and reporting",
        ],
        [
            r"Defining the contract workflow and approval",
            r"Defining calendaring, reminders, and renewal",
            r"Defining obligation tracking",
            r"Defining archiving and reporting",
        ],
        [
            r"Every contract has a date, status, and owner",
            r"Renewal reminders are configured with timing",
            r"Obligations are traceable against SLA",
        ],
    ),

    # --------------------------- finance etc ----------------------------
    "finance-manager": sp(
        "management",
        r"Are budget/cost and project financial health managed transparently?",
        [
            r"Coverage of budget and cash flow",
            r"Alignment of cost with scope and value",
            r"Accurate financial reporting and forecasting",
            "management of spending and risks",
        ],
        [
            r"Defining budget, forecast, and cost model",
            r"Reporting cost, variance, and forecast",
            r"Budget gate control and approvals",
            r"Defining financial criteria and ROI",
        ],
        [
            r"Financial reporting includes budget, actual, and forecast",
            r"Cost decisions are recorded with approval",
            r"Financial variance and risk are traceable",
        ],
    ),
    "finops-specialist": sp(
        "devops",
        r"Is cloud infrastructure cost controlled, optimised, and explainable?",
        [
            r"Cost visibility and allocation",
            r"Correct allocation and showback",
            r"Optimisation and right-sizing",
            r"Commitment to cost of value",
        ],
        [
            r"Defining cost tags and allocation",
            r"Cost monitoring and alerting process",
            r"Managing optimisation (right-sizing, scheduling)",
            r"Defining cloud financial reporting and decisions",
        ],
        [
            r"Costs are separable by tag and owner",
            r"Budget and cost alerts are configured",
            r"Optimisation actions are recorded with cost reduction and effect",
        ],
    ),
    "procurement-specialist": sp(
        "growth",
        r"Is equipment/service/software procurement carried out correctly, fairly, and cost-effectively?",
        [
            r"Consistency of source, quality, and price",
            r"Alignment of procurement with need and budget",
            r"Managing contract and supplier",
            r"Supporting growth and stability",
        ],
        [
            r"Defining purchase needs, requirements, and specifications",
            r"Requesting, comparing, and negotiating with vendors",
            r"Managing order, contract, and settlement",
            r"Defining vendor and quality assessment",
        ],
        [
            r"Every purchase has a requirement, price, owner, and date",
            r"Vendor comparison uses stated criteria",
            r"Contract, delivery, and availability are documented",
        ],
    ),

    # ------------------------------- people ------------------------------
    "hr-people-manager": sp(
        "people",
        r"Are people recruited, developed, and retained with quality and consistency?",
        [
            r"Alignment of the people strategy with team goals",
            r"In the recruit, assess, and develop process",
            r"Coverage of fairness, impartiality, and privacy",
            r"Effectiveness of programmes and retention",
        ],
        [
            r"Defining role, skill, classification, and path",
            r"Designing the hire, onboarding, and assessment process",
            r"Defining growth, performance management, and retention",
            r"Managing policy, privacy, and data processing",
        ],
        [
            r"The people process has criteria, steps, and owners",
            r"Assessment and feedback are evidence-based and free of bias",
            r"Employee data is managed according to privacy policy",
        ],
    ),
    "recruiter": sp(
        "people",
        r"Are team members recruited with quality, speed, and fairness?",
        [
            r"Quality of the pipeline and candidate experience",
            r"Coverage of team and skill requirements",
            r"Fairness and absence of bias",
            r"Consistency with time and cost",
        ],
        [
            r"Defining job description, sourcing, and shortlist",
            r"Interviewing, assessing, and scoring against criteria",
            r"Improving the pipeline and candidate experience",
            r"Managing data, privacy, and legal matters",
        ],
        [
            r"Every candidate is assessed against stated criteria",
            r"The pipeline has phases, owners, and dates",
            r"The candidate experience is recorded with feedback",
        ],
    ),
    "technical-recruiter": sp(
        "people",
        r"Is technical hiring done with skill assessment and technical fit?",
        [
            r"Quality of technical requirements and assessment",
            r"Fit with the stack and architecture",
            r"Coverage of technical screening and fairness",
            r"Consistency with level, experience, and growth",
        ],
        [
            r"Defining skills, technical tests, and rubric",
            r"Participating in technical screening and assessment",
            r"Coordinating with the team and lead",
            r"Managing candidate data and feedback",
        ],
        [
            r"Every assignment is measured against rubrics, skills, and stack",
            r"The technical test has criteria, timing, and no bias",
            r"Technical feedback to the candidate is documented",
        ],
    ),

    # ---------------------------- support/community ---------------------
    "customer-support-agent": sp(
        "support",
        r"Are user issues and requests answered with quality and within a reasonable time?",
        [
            r"Accuracy and completeness of the response",
            r"Speed and SLA compliance",
            r"Coverage of escalation and ownership",
            r"User experience and feedback",
        ],
        [
            r"Defining flow, scripts, and base FAQ",
            r"Responding, diagnosing, escalating, and resolving issues",
            r"Recording the ticket and documentation/outcome",
            r"Reporting quality and survey results",
        ],
        [
            r"Every ticket has a status, owner, and documentation",
            r"Response and resolution SLAs are met",
            r"User feedback is recorded with action",
        ],
    ),
    "technical-support-engineer": sp(
        "support",
        r"Are users' technical problems resolved through correct diagnosis and fix?",
        [
            r"Accuracy of diagnosis and fix",
            r"Coverage of logs, evidence, and tests",
            r"Consistency with release and environment",
            r"Documentation and improvement",
        ],
        [
            r"Defining initial diagnosis and log collection",
            r"Fix, recommendation, and workaround",
            r"Recording and reviewing the fix and escalating",
            r"Feeding docs and the knowledge base",
        ],
        [
            r"Every technical ticket has a diagnosis, action, and outcome",
            r"Evidence and logs are recorded with analysis",
            r"Actions and fixes are documented and improved",
        ],
    ),
    "customer-success-manager": sp(
        "support",
        r"Is customer success facilitated through onboarding, usage, and retention?",
        [
            r"Account health, usage, and retention",
            r"Sufficiency of onboarding and value creation",
            r"Managing churn, risk, and expansion",
            r"Alignment with product and team",
        ],
        [
            r"Defining the health score and onboarding",
            r"Monitoring adoption, usage, and churn signals",
            r"Defining QBR, growth signals, and retention",
            r"Coordinating with product and tech for feedback",
        ],
        [
            r"Every account has a health score, owner, and action",
            r"Churn signals have an alert and a related action",
            r"Onboarding and renewal outcomes are recorded with evidence",
        ],
    ),
    "community-manager": sp(
        "support",
        r"Is the user community managed with content, engagement, and health?",
        [
            r"Coverage of community growth and engagement",
            r"Managing content, rules, and safety",
            r"Consistency with brand and literacy",
            r"Feedback to the product",
        ],
        [
            r"Defining community strategy, rules, and roles",
            r"Producing and publishing content and activation",
            r"Managing moderation and feedback",
            r"Reporting engagement and improvement",
        ],
        [
            r"Every community channel is specified with rules and moderators",
            r"Engagement reporting is recorded with real data",
            r"Feedback reaches the product and team with effect",
        ],
    ),

    # ------------------------------ marketing ---------------------------
    "product-marketing-manager": sp(
        "growth",
        r"Is the product marketing strategy aligned with product/market and measurable?",
        [
            r"Clarity of positioning, message, and audience",
            r"Coherence with the product stage",
            r"Measurability and KPI alignment",
            r"Managing launch, campaign, and market",
        ],
        [
            r"Defining category, positioning, and persona",
            r"Defining message, copy, offer, and channel",
            r"Defining the launch plan, KPI, and gating",
            r"Coordinating with content, growth, and sales",
        ],
        [
            r"Positioning and message are documented and unambiguous",
            r"The launch plan has steps, owners, and KPIs",
            r"KPIs are tracked with data and decisions",
        ],
    ),
    "marketing-specialist": sp(
        "growth",
        r"Are campaigns and marketing activities executed effectively and measurably?",
        [
            r"Campaign quality and effect",
            r"Coverage of channel, audience, and copy",
            r"Optimisation and ROI",
            r"Message consistency with brand and audience",
        ],
        [
            r"Defining campaign objective, audience, and copy",
            r"Executing channel execution",
            r"Monitoring performance and A/B tests",
            r"Reporting inspiration, learning, and iteration",
        ],
        [
            r"Every campaign has an objective, criteria, and budget",
            r"Message and channel are consistent with brand and audience",
            r"Results are tracked with data and recommendations",
        ],
    ),
    "seo-specialist": sp(
        "growth",
        r"Is content/architecture optimisation for search engines done correctly?",
        [
            r"Coverage of technical SEO and content",
            r"Quality of keyword, topic, and intent",
            r"Consistency with site, brand, and experience",
            r"Monitoring and reporting rank and traffic",
        ],
        [
            r"Defining keyword/topic model and site structure",
            r"Optimising on-page, technical, and structured data",
            r"Link model and internal linking",
            r"Reporting rank, organic traffic, and conversion",
        ],
        [
            r"Every page is optimised for intent, keyword, and on-page factors",
            r"Correcting technical SEO (crawl, index, speed)",
            r"Organic reporting includes data and decisions",
        ],
    ),
    "aso-specialist": sp(
        "growth",
        r"Is App Store / Google Play optimisation effective and measurable?",
        [
            r"Coverage of metadata, keywords, and imagery",
            r"Consistency with platform and trend",
            r"Improving conversion and category",
            r"Monitoring installs, rank, and reviews",
        ],
        [
            r"Defining keywords, title, subtitle, and screenshots",
            r"Optimising metadata and creative",
            r"Managing reviews, replies, and conversion",
            r"Reporting A/B tests and installs",
        ],
        [
            r"Metadata is current with keyword intent and platform",
            r"Creatives and assets have imagery and A/B testing",
            r"Install, rank, and review reporting is data-backed",
        ],
    ),
    "growth-manager": sp(
        "growth",
        r"Is the product growth strategy effective through experimentation, funnel, and retention?",
        [
            r"Clarity of north-star metric, funnel, and retention",
            r"Coverage of experiments and prioritisation",
            r"Consistency with product and audience",
            r"Measurement and learning capability",
        ],
        [
            r"Defining north-star, funnel, and KPI",
            r"Defining the experiment backlog and prioritisation",
            r"Implementing activation, retention, and acquisition",
            r"Defining the feedback loop and grading",
        ],
        [
            r"Every experiment has a hypothesis, criterion, and gate",
            r"Growth KPIs are monitored with data",
            r"Experiments are documented with results and recommendations",
        ],
    ),

    # -------------------------------- sales -----------------------------
    "sales-manager": sp(
        "growth",
        r"Is the sales process managed with pipeline coverage, negotiation, and closing?",
        [
            r"Quality of pipeline, prospecting, and forecast",
            r"Alignment of the process with product and audience",
            r"Transparency of deals, stage, and risk",
            r"Consistency with team and brand",
        ],
        [
            r"Defining the sales pipeline, stages, and process",
            r"Defining prospecting, qualification, and decision",
            r"Defining forecast, commit, and review",
            r"Defining coordination with marketing and product",
        ],
        [
            r"Every deal has a stage, value, owner, and risk",
            r"Forecast is recorded with data, probability, and time",
            r"Process and contract are consistent with the team and documented",
        ],
    ),
    "sales-representative": sp(
        "growth",
        r"Is customer engagement and selling done with quality, transparency, and need alignment?",
        [
            r"Quality of communication and need discovery",
            r"Coverage of objections and pushback",
            r"Transparency of offer, price, and stage",
            r"Retention and conversion (CRM)",
        ],
        [
            r"Defining target, qualification, and discovery",
            r"Presenting, demoing, and answering objections",
            r"Defining offer, proposal, and agreement",
            r"Updating CRM and following up",
        ],
        [
            r"Every lead/account has a stage, status, and owner",
            r"Presentations and meetings are documented with the need",
            r"Agreements and contracts are recorded with documentation and follow-up",
        ],
    ),

    # --------------------- biz dev / partnerships --------------------
    "account-manager": sp(
        "support",
        r"Is key-customer relationship management done with need understanding, coordination, and relationship retention?",
        [
            r"Quality of relationship and survey",
            r"Usage, satisfaction, and opportunity",
            r"Coverage of escalation and renewal",
            r"Alignment with product and team",
        ],
        [
            r"Defining the account plan, value, and contact",
            r"Monitoring usage, satisfaction, and consistency",
            r"Managing renewal, upsell, and escalation",
            r"Coordinating with product, support, and customer success",
        ],
        [
            r"Every account has a plan, owner, contact, and status",
            r"Hostility and satisfaction are monitored with evidence",
            r"Renewal and risk have an action and an owner",
        ],
    ),
    "business-development-manager": sp(
        "growth",
        r"Are commercial opportunities correctly identified and pursued through partnership and market?",
        [
            r"Quality of opportunity and platform identification",
            r"Follow-up and value proposition",
            r"Consistency with strategy and market",
            r"Partnership effect and ROI",
        ],
        [
            r"Defining market, partner, and opportunity discovery",
            r"Defining touchpoints, follow-up, and contract",
            r"Consistency with product and strategy",
            r"Reporting pipeline, momentum, and value",
        ],
        [
            r"Every opportunity has a value, stage, and owner",
            r"Follow-ups have a status and date",
            r"Partnership reporting includes ROI and definitions",
        ],
    ),
    "partnership-manager": sp(
        "growth",
        r"Is collaboration with companies/services developed and managed correctly?",
        [
            r"Alignment with strategy and mutual value",
            r"Coverage of channel, service, and contract",
            r"Managing ROI, incentives, and content",
            r"Quality of relationship and follow-up",
        ],
        [
            r"Defining partner profile and value",
            r"Defining programme, incentive, catalogue, and process",
            r"Managing co-marketing, integration, and contract",
            r"Reporting performance and ROI",
        ],
        [
            r"Partners are documented with value, channel, and contract",
            r"Partnership actions have a date and status",
            r"Performance reporting includes data and decisions",
        ],
    ),

    # --------------------------- devrel / evangelist --------------------
    "devrel": sp(
        "engineering",
        r"Is developer and technical-community engagement effective through content, education, and feedback?",
        [
            r"Quality of content, education, and events",
            r"Coverage of developer persona and journey",
            r"Attracting feedback and adoption",
            r"Consistency with brand and available resources",
        ],
        [
            r"Defining developer persona and content plan",
            r"Writing docs, tutorials, and workshops",
            r"Participating in community and events",
            r"Collecting feedback and community growth",
        ],
        [
            r"Developer content is consistent with release and behaviour",
            r"Community and events have engagement and feedback",
            r"Feedback is shared with product and engineering",
        ],
    ),
    "technical-evangelist": sp(
        "engineering",
        r"Is technology/product introduction to the technical community done accurately, positively, and with educational impact?",
        [
            r"Technical accuracy and absence of misdirection",
            r"Quality of demo, content, and response",
            r"Effect on adoption",
            r"Consistency with brand and strategy",
        ],
        [
            r"Defining audience, case, and demo",
            r"Producing content, presentations, and workshops",
            r"Answering questions and objections",
            r"Capturing feedback and reporting adoption",
        ],
        [
            r"Technical claims are consistent with release and evidence",
            r"Presentations and demos have a stated audience and time",
            r"Feedback and adoption criteria are reported",
        ],
    ),

    # ------------------------------ engineering -------------------------
    "software-architect": sp(
        "architecture",
        r"Is the software architecture sound in modularity, boundaries, and maintainability?",
        [
            r"Separation of modules and boundaries",
            r"Alignment with requirements and scale",
            r"Quality of inter-module contracts",
            r"Maintainability and testability",
        ],
        [
            r"Defining layers, boundaries, and packaging",
            r"Defining contracts, interfaces, and events",
            r"Defining the approach to data, technique, and refactoring",
            r"Defining assessment and decision records",
        ],
        [
            r"The architecture has layers and boundaries without reverse dependency",
            r"Contracts are defined with input, output, and error",
            r"Decisions are documented with trade-offs",
        ],
    ),
    "software-engineer": sp(
        "engineering",
        r"Are features designed and implemented with quality, tests, and contracts?",
        [
            r"Correct, readable, maintainable code",
            r"Alignment with architecture and contract",
            r"Coverage of edge, failure, and validation",
            r"Testing, reporting, and consistency",
        ],
        [
            r"Defining behaviour, input, output, and contract",
            r"Implementing domain, interface, and core",
            r"Managing validation, errors, and edge cases",
            r"Writing tests, review, and release",
        ],
        [
            r"Code matches the expected behaviour and contract",
            r"Edge and failure cases are tested with documented behaviour",
            r"Tests are green and merge quality is maintained",
        ],
    ),
    "backend-developer": sp(
        "engineering",
        r"Is the backend (API, logic, service) developed with correctness, security, and efficiency?",
        [
            r"Quality of API, business logic, and persistence",
            r"Security of authentication, authorisation, and validation",
            r"Performance, transaction, and concurrency",
            r"Coverage of error, retry, and observability",
        ],
        [
            r"Defining API contracts, validation, and status",
            r"Implementing business, service, and data access",
            r"Managing transactions and optimistic locking",
            r"Testing, logging, tracing, and session upgrade",
        ],
        [
            r"The API is consistent with its contract, errors, and response codes",
            r"Validation and authorisation are implemented",
            r"Logic is covered with transactions and tests",
        ],
    ),
    "frontend-developer": sp(
        "engineering",
        r"Are the UI and client logic developed with quality, responsiveness, and accessibility?",
        [
            r"Quality of the UI state, render, and responsiveness",
            r"Coverage of state management and data fetching",
            "a11y/responsive/animation",
            r"DRY and use of components",
        ],
        [
            r"Defining component, state, and data flow",
            r"Implementing UI with semantics and accessibility",
            r"Managing loading, empty, error, and optimistic states",
            r"Component, regression, and performance testing",
        ],
        [
            r"The UI covers its states (load, empty, error, disabled)",
            r"Semantics, focus, keyboard, and responsive behaviour are respected",
            r"Components are reusable and free of duplicate versions",
        ],
    ),
    "full-stack-developer": sp(
        "engineering",
        r"Is simultaneous frontend/backend development done with consistency and quality?",
        [
            r"Alignment of the API contract with the UI",
            r"Quality of the end-to-end flow",
            r"Coverage of auth, state, data, and session",
            r"Quality of architecture and DRY",
        ],
        [
            r"Defining contract, data flow, and end-to-end",
            r"Implementing backend and frontend to agreement",
            r"Managing auth, session, and optimisation",
            r"Integration/E2E testing and documentation",
        ],
        [
            r"Contracts between frontend and backend are free of mismatch",
            r"The end-to-end flow is covered with state and session",
            r"Integration and E2E tests are green and reproducible",
        ],
    ),
    "mobile-developer": sp(
        "engineering",
        r"Is the mobile application developed with quality, stability, and platform compliance?",
        [
            r"Correctness of native/cross-platform consistency",
            r"Quality of state, deep links, media, and offline",
            r"Coverage of app lifecycle, permissions, and notifications",
            r"Performance, battery, and flow",
        ],
        [
            r"Defining navigation, state, and persistence",
            r"Implementing UI and platform compliance",
            r"Managing offline, network, permissions, and notifications",
            r"Device testing, signing, and release",
        ],
        [
            r"The navigation, deep-link, and state flow is stable",
            r"Offline, error, and retry flows are covered",
            r"Tests run across multiple devices and versions",
        ],
    ),
    "desktop-developer": sp(
        "engineering",
        r"Is the desktop software developed with quality, OS compliance, and a desktop experience?",
        [
            r"Consistency with multiple OS versions",
            r"Quality of UI, processing, files, and window management",
            r"Coverage of async, updates, and security",
            r"Robustness and performance",
        ],
        [
            r"Defining architecture, state, and data",
            r"Implementing UI and system integration",
            r"Managing file, update, contact, and context",
            r"Multi-platform, performance, and signature testing",
        ],
        [
            r"The software is consistent with OS defaults",
            r"Release, update, and signing are covered",
            r"Platform obstacles and errors are managed with tests",
        ],
    ),
    "game-developer": sp(
        "engineering",
        r"Is the game developed with logic, gameplay, stable systems, and an enjoyable experience?",
        [
            r"Stability of loop, gameplay, and state",
            r"Performance, frame rate, and platform",
            r"System, startup, and shutdown review",
            r"Quality of UX, audio, and visuals",
        ],
        [
            r"Defining the gameplay loop and state machine",
            r"Implementing mechanics, events, and entities",
            r"Managing performance, memory, input, and device",
            r"Gameplay, performance, and feedback testing",
        ],
        [
            r"Gameplay with goals and a tested loop is stable",
            r"Loading, quality, and bug fixing are covered",
            r"A performance criterion (fps, memory) is established",
        ],
    ),
    "embedded-developer": sp(
        "engineering",
        r"Is embedded-device software developed with resource constraints and stability?",
        [
            r"Consistency with hardware constraints",
            r"Stability, real-time, interruption, and startup",
            r"Connectivity, communication, and protocol",
            r"Security and on-board testing",
        ],
        [
            r"Defining target, memory, power, and protocol",
            r"Implementing low-level, OS, and device code",
            r"Managing interrupts, timing, and watchdog",
            r"Device, hardware-in-the-loop, and safety testing",
        ],
        [
            r"The system is stable at high times and low resources",
            r"Connectivity and error handling are preserved by protocol",
            r"Tests run on hardware and best patterns",
        ],
    ),
    "firmware-engineer": sp(
        "engineering",
        r"Is firmware developed at low level with hardware communication, stable and upgradeable?",
        [
            r"Consistency with device and HAL",
            r"Security, upgradeability, and durability",
            r"Stability, timing, and degrees",
            r"Hardware documentation and testing",
        ],
        [
            r"Defining device, register, and memory map",
            r"Implementing driver, protocol, and startup",
            r"Managing boot, update, and watchdog",
            r"Hardware, OTA, and safety testing",
        ],
        [
            r"Firmware runs successfully on device/simulator",
            r"Update, OTA, and rollback are defined",
            r"Hardware tests and logs are evidence-backed",
        ],
    ),
    "iot-engineer": sp(
        "engineering",
        r"Are IoT systems (device/data/connectivity) developed securely, scalably, and monitorably?",
        [
            r"Security of device, network, and data",
            r"Connectivity, MQTT, and scale",
            r"Monitoring, footprint, and reliability",
            r"Consistency with cloud data and pipelines",
        ],
        [
            r"Defining device, edge, connectivity, and protocol",
            r"Implementing ingestion, telemetry, and control",
            r"Managing auth, replay, OTA, and device identity",
            r"Authoring monitoring, alerts, and device tests",
        ],
        [
            r"Devices connect with identity, security, and OTA",
            r"Telemetry and status are visible and monitored with alerts",
            r"Scale and latency are managed in real time",
        ],
    ),
    "maintenance-engineer": sp(
        "engineering",
        r"Is maintenance, bug fixing, and system improvement carried out without destroying stability?",
        [
            r"Coverage of regression and stability after change",
            r"Quality of fix, tests, and recommendation",
            r"Documentation and release",
            r"Managing priority appropriately",
        ],
        [
            r"Defining triage, reproduction, and root cause",
            r"Applying the fix with tests and regression",
            r"Managing release, hotfix, and backport",
            r"The observability of known issues",
        ],
        [
            r"Bugs are fixed with root cause and a test",
            r"Regression stays green after the fix",
            r"Changes and releases are documented with release reporting",
        ],
    ),
    "refactoring-engineer": sp(
        "engineering",
        r"Is code structure/quality improvement carried out without behaviour change and with reduced risk?",
        [
            r"Preserving behaviour while refactoring",
            r"Quality of changes and phases",
            r"Coverage of regression",
            r"Ordering and retiring debt",
        ],
        [
            r"Defining refactor bounds, master, and tests",
            r"Incremental questions and refactoring",
            r"Increasing readability and maintainability",
            r"Test safety and CI cycles",
        ],
        [
            r"A test suite exists before refactoring",
            r"Refactoring applies changes in small sections",
            r"Behaviour (output) is unchanged after refactoring",
        ],
    ),
    "legacy-modernization-engineer": sp(
        "engineering",
        r"Is legacy system migration/modernisation carried out with risk control and continuity preserved?",
        [
            r"Full understanding of the legacy system",
            r"Coverage of migration and backward compatibility",
            r"Reducing cutover risk",
            r"Rollback capability",
        ],
        [
            r"Defining the modern target, strangler, and steps",
            r"The legacy-to-new mapping plan",
            r"Implementing migration steps and tests",
            r"Managing cutover, rollback, and parallel run",
        ],
        [
            r"Every migration step has mapping, tests, and rollback",
            r"Legacy services are gradually replaced by the new ones",
            r"Cutover has rollback and monitoring",
        ],
    ),
    "third-party-integration-specialist": sp(
        "engineering",
        r"Is connection to external services/APIs done securely, with hardening and tests?",
        [
            r"Understanding API, resources, and limits",
            r"Managing auth, rate, and error",
            r"Hardening, retry, and fallback",
            r"Integration and mock testing",
        ],
        [
            r"Defining contract, auth, and timeout",
            r"Implementing integration with validation",
            r"Managing rate, retry, circuit breaker, and fallback",
            r"Integration, mock, and secrets testing",
        ],
        [
            r"Third-party integrations are consistent with auth and limits",
            r"Error, retry, and fallback are tested",
            r"Secrets and keys are in a secure location and not hardcoded",
        ],
    ),
    "migration-specialist": sp(
        "engineering",
        r"Is data/system migration from the previous environment done accurately, securely, and on schedule?",
        [
            r"Complete coverage of data and mapping",
            r"Accuracy, repeatability, and recovery",
            r"Security, compliance, and data retention",
            r"Rollback capability and action",
        ],
        [
            r"Defining source, target, mapping, and validation",
            r"Implementing migration with a dry run",
            r"Managing cutover, backup, and rollback",
            r"Data validation and resume testing",
        ],
        [
            r"Data mapping to the target is complete and error-free",
            r"Data is validated at the destination",
            r"Interruptions and errors are managed with resume and rollback",
        ],
    ),
    "deployment-engineer": sp(
        "engineering",
        r"Is release deployment across environments done with stability, security, and reversibility?",
        [
            r"Quality of pipeline and deployment",
            r"Coverage of environment, secret, and version",
            r"Rollback and monitoring capability",
            r"Consistency with environment and fit",
        ],
        [
            r"Defining the deploy strategy (env, artifact)",
            r"Executing deploy and rollback",
            r"Managing config, secrets, and environment types",
            r"Defining post-deploy checks and alerts",
        ],
        [
            r"Deployment carries a version image and integrity",
            r"Failure and rollback are driven by alerts and canary",
            r"Config and secrets for each environment are accessible and secure",
        ],
    ),
    "disaster-recovery-specialist": sp(
        "engineering",
        r"Is disaster recovery carried out with RTO/RPO targets and valid testing?",
        [
            r"Coverage of scenario and recovery",
            r"Accuracy of backup, recovery, and timing",
            r"Verifying tests and rehearsals",
            r"Documentation and runbook",
        ],
        [
            r"Defining RTO, RPO, source, and backup",
            r"Designing DR, pipeline, and replication",
            r"Testing failure and criteria",
            r"Defining runbook, communication, and recovery",
        ],
        [
            r"Every DR scenario has an RTO, RPO, source, and recovery",
            r"Backup and recovery have been tested",
            r"The runbook documents role, timing, and method",
        ],
    ),
    "backup-administrator": sp(
        "engineering",
        r"Are backup and restore managed with accuracy, timing, and regular testing?",
        [
            r"Coverage of data and backup retention",
            r"Accuracy, completeness, and restore",
            r"Tests, rehearsals, and alerts",
            r"Safety and continuity",
        ],
        [
            r"Defining scope, schedule, and retention",
            r"Managing backup jobs and monitoring",
            r"Testing restore and fixing errors",
            r"Defining alerts, alarms, and reporting",
        ],
        [
            r"Backup files follow the schedule and retention",
            r"Restore tests succeed",
            r"Backup failure comes with an alert and investigation",
        ],
    ),
    "on-call-engineer": sp(
        "devops",
        r"Is immediate response to production issues carried out with speed, documentation, and improvement?",
        [
            r"Clarity of the on-call procedure",
            r"Speed and accuracy of response",
            r"Algorithm, escalation, and handoff",
            r"Stability and shift coverage",
        ],
        [
            r"Defining the on-call rotation and runbook",
            r"Responding to alerts and incidents",
            r"Recording action, communication, and handoff",
            r"Assessing and supporting improvement",
        ],
        [
            r"Every alert and incident has a recorded response and outcome",
            r"The runbook and escalation path are available",
            r"Networks are free of overlap and sized to estimated coverage",
        ],
    ),
    "decommission-engineer": sp(
        "engineering",
        r"Is safe decommissioning of services and migration/deletion of data done without harming users and with security respected?",
        [
            r"Completeness and safety of the data deletion/migration process",
            r"Coverage of the exit period (drain, alert, backup)",
            r"Compliance and retention respected in data deletion",
            r"Recoverability when needed (rollback, backup)",
        ],
        [
            r"Defining the inventory of services and data and their dependencies",
            r"Planning drain, throttling, and deactivation",
            r"Implementing migration, archiving, and safe data deletion",
            r"Testing shutdown, rollback, and reporting",
        ],
        [
            r"No critical service or data is decommissioned without backup or migration",
            r"The exit period is documented with alerts, classification, and backup",
            r"Data deletion is carried out and reported per retention and compliance",
        ],
    ),
    "staff-engineer": sp(
        "engineering",
        r"Are complex problems solved and architecture led at large scale?",
        [
            r"Quality and accuracy of decisions and trade-offs",
            r"Coverage of goals and the technical path",
            r"Impact and technical leadership",
            r"Alignment with culture and constraints",
        ],
        [
            r"Defining the technical strategy and roadmap",
            r"Complex analysis and architecture at scale",
            r"Mentoring and code/risk",
            r"Defining system, integration, and decision records",
        ],
        [
            r"Decisions are recorded with evidence and trade-offs",
            r"Solutions are justified against architecture criteria (scale, performance)",
            r"Delay and debt are documented with risk and posture",
        ],
    ),
    "principal-engineer": sp(
        "engineering",
        r"Are enterprise technical decisions and complex architectures led effectively with adoption and impact?",
        [
            r"Quality of the enterprise technical viewpoint",
            r"Consistency with execution and experience",
            r"Managing complexity and trade-offs",
            r"Effect on solutions and the team",
        ],
        [
            r"Defining enterprise architecture and standards",
            r"Solving several complex problems and cross-technical gaps",
            r"Ability to define RFCs and decisions",
            r"Guiding and enabling the team",
        ],
        [
            r"Enterprise decisions are recorded with RFCs and evidence",
            r"Complex architecture is justified with scale and scenario",
            r"Decisions in the organisation are implementable and assessable",
        ],
    ),
    "technical-lead-tech-lead": sp(
        "engineering",
        r"Is team technical leadership and implementation decision-making done with quality and coordination?",
        [
            r"Clarity of role and technical decision",
            r"Quality of code policy and mentoring",
            r"Quality coverage (tests, review)",
            r"Coordination with stakeholders",
        ],
        [
            r"Defining decision, review, and coding standards",
            r"Leading the team in technical and architectural verification",
            r"Managing risk, technical debt, and quality",
            r"Mentoring and reporting",
        ],
        [
            r"Technical decisions are documented and assessable",
            r"Review, code quality, and tests are in place",
            r"Technical risk, debt, and variance are reported with status",
        ],
    ),

    # ------------------------------ ai / data ---------------------------
    "ai-ml-engineer": sp(
        "ai",
        r"Are AI/ML models developed and integrated with correctness, reproducibility, and monitoring?",
        [
            r"Quality of model, data, and pipeline",
            r"Coverage of train, eval, deploy, and monitor",
            r"Reproducibility and versioning",
            "Safety/Privacy/Cost",
        ],
        [
            r"Defining features, dataset, and metric",
            r"Implementing training, eval, and inference",
            r"Managing model and data versioning",
            r"Implementing monitor, drift, and guardrail",
        ],
        [
            r"The pipeline is reproducible with dataset, version, and eval",
            r"The deployed model has monitor, drift detection, and fallback",
            r"Data, bias, and privacy are managed with tests and reporting",
        ],
    ),
    "data-scientist": sp(
        "ai",
        r"Is data analysis and statistical/predictive model building done with precise criteria and hypothesis?",
        [
            r"Quality of data, EDA, and datasets",
            r"Coverage of model, validation, and metric",
            r"Reproducibility and interpretation",
            r"Prediction, stability, and bias",
        ],
        [
            r"Defining problem, data, and evaluation",
            r"Performing EDA, feature engineering, model, and validation",
            r"Measuring metrics with cross-validation",
            r"Reporting insight, risk, and deploy readiness",
        ],
        [
            r"Results are reproducible with metric and cross-validation",
            r"Hypothesis, data, and limitations are documented",
            r"Findings are reported with evidence and confidence level",
        ],
    ),
    "data-engineer": sp(
        "data",
        r"Are data processing pipelines and infrastructure built with correctness, scale, and monitoring?",
        [
            r"Quality and reliability of the pipeline",
            r"Coverage of data quality and capability",
            r"Scale, cost, and latency",
            r"Consistency with source and contracts",
        ],
        [
            r"Defining sources, schema, and transforms",
            r"Implementing pipeline with retries and backfill",
            r"Managing data quality, errors, and power",
            r"Defining monitor, alert, and cost",
        ],
        [
            r"The pipeline is stable with schema, tests, and error handling",
            r"Backfill, retry, and duplicates are covered",
            r"Data quality and management are reported with alerts",
        ],
    ),
    "mlops-engineer": sp(
        "ai",
        r"Are ML model deployment, monitoring, and lifecycle carried out with stability and control?",
        [
            r"Coverage of the ML lifecycle and versioning",
            r"Quality of deployment and monitoring",
            r"Reproducibility, risk, and fallback",
            r"Monitoring, price, and speed",
        ],
        [
            r"Defining the pipeline (train, eval, deploy)",
            r"Managing the model registry and versioning",
            r"Monitoring drift, performance, and alerts",
            r"Defining rollback, canary, and cost",
        ],
        [
            r"Every model has registry, version, and evidence",
            r"Drift and performance monitoring and alerts are configured",
            r"Deployment and recovery have rollback and fallback",
        ],
    ),
    "prompt-engineer": sp(
        "ai",
        r"Is prompt design and structured interaction with models done with precision and evaluation?",
        [
            r"Quality of prompt, content, and meaning",
            r"Coverage of evaluation and qualities",
            r"Safety and reduction of hallucination",
            r"Consistency with task and context",
        ],
        [
            r"Defining task, context, few-shot, and reference",
            r"Designing prompts and variables",
            r"Measuring quality, safety, and evaluation",
            r"Repeating prompt experiments and keeping versions",
        ],
        [
            r"Responses are evaluated against criteria",
            r"Signs of harm and hallucination are managed",
            r"Prompt versions are tracked with results and versions",
        ],
    ),
    "ai-engineer": sp(
        "ai",
        r"Are LLM/agent/RAG/AI-service systems designed and developed correctly and safely?",
        [
            r"Quality of the LLM/agent architecture",
            r"Coverage of RAG, retrieval, and eval",
            "Safety/hallucination/guardrail",
            r"Action, tools, latency, and cost",
        ],
        [
            r"Defining the architecture (agent, flow, retrieval)",
            r"Implementing RAG, agents, tools, and eval",
            r"Defining guardrail, fallback, and observability",
            r"Measuring cost, latency, and quality",
        ],
        [
            r"The system is reproducible with retrieval, eval, and fallback",
            r"Guardrails against harm and hallucination are implemented",
            r"Performance and cost are observable and optimised",
        ],
    ),
    "observability-engineer": sp(
        "devops",
        r"Are logging/metrics/tracing/monitoring complete with detection and improvement capability?",
        [
            r"Coverage of observability (logs, metrics, traces)",
            r"Quality of alerts and dashboards",
            "Correlation/troubleshooting",
            r"Monitoring SLO and performance",
        ],
        [
            r"Defining instrumented code, log, metric, and trace",
            r"Implementing metrics, dashboards, and alerts",
            r"Managing correlation and context",
            r"Defining SLO, error budget, and accumulation",
        ],
        [
            r"Critical services have logs, metrics, and traces",
            r"Alerts and dashboards relate to the SLO",
            r"Monitoring findings are documented with improvement actions",
        ],
    ),
    "data-analyst": sp(
        "analysis",
        r"Is user-behaviour and KPI analysis carried out with accurate data and actionable insight?",
        [
            r"Quality of data, metrics, and accuracy",
            r"Coverage of funnels, segments, and insights",
            r"Consistency with product and A/B tests",
            r"Actionability of insight",
        ],
        [
            r"Defining the metric, data, and schema source",
            r"Analysing behaviour, funnel, and segment",
            r"Reporting analysis and recommendations",
            r"Linking with product and engineering",
        ],
        [
            r"Every KPI has a definition, source, numerator, and denominator",
            r"Analysis is open about sample, data, and limitations",
            r"Recommendations have action, owner, and impact",
        ],
    ),
    "bi-analyst": sp(
        "analysis",
        r"Are management reports and dashboards accurate, understandable, and useful?",
        [
            r"Quality of the data model and richness",
            r"Accuracy, coverage, and filtering of dashboards",
            r"Comprehension, action, and response for management",
            r"Data freshness, access, and security",
        ],
        [
            r"Defining the data model and reporting requirements",
            r"Building dashboards with KPIs, filters, and gates",
            r"Managing data freshness and access",
            r"Assessing usage and improvement",
        ],
        [
            r"Every dashboard is documented with data source, KPI, and filter",
            r"Data is consistent in definition and timezone",
            r"Data access and security are respected",
        ],
    ),
    "product-analyst": sp(
        "analysis",
        r"Is usage analysis for product decisions carried out with data and experimentation?",
        [
            r"Clarity of metric and product objective",
            r"Running funnels, experiments, and segments",
            r"Adding insight to the product decision",
            r"Accuracy and reliability",
        ],
        [
            r"Defining product metrics and funnels",
            r"Running analysis and experiment evaluation",
            r"Reporting recommendations and trade-offs",
            r"Coordinating with PM, design, and engineering",
        ],
        [
            r"Analysis is documented with metric, calculation, and limitations",
            r"Experiments are evaluated against criteria and significance",
            r"Recommendations link to product and feature decisions",
        ],
    ),

    # ----------------------------- database -----------------------------
    "database-administrator-dba": sp(
        "data",
        r"Is the database managed for stability, security, backup, and performance?",
        [
            r"Stability, performance, and overload",
            r"Security, access, and permissions",
            r"Backup, recovery, and DR",
            r"Fit with schema, index, and query",
        ],
        [
            r"Defining access, SSL, and audit",
            r"Managing backup, restore, and DR",
            r"Monitoring performance, waits, and locks",
            r"Reviewing query, index, and storage",
        ],
        [
            r"User access follows least privilege",
            r"Backup files are tested against schedule and recovery",
            r"Monitoring and alerts (CPU, locks, storage) are active",
        ],
    ),
    "database-engineer": sp(
        "data",
        r"Are schema, queries, indexes, and data architecture designed with correctness, performance, and scale?",
        [
            r"Quality of schema, intersection, and standard",
            r"Query, index, and load performance",
            r"Data integrity and transactions",
            r"Consistency with contract and scale",
        ],
        [
            r"Defining schema, migration, and null constraints",
            r"Designing query, index, and types",
            r"Managing transactions and consistency",
            r"Testing performance and data quality",
        ],
        [
            r"The schema is documented with constraints, indexes, and migrations",
            r"Query and index derive from an appropriate execution plan",
            r"Integrity and consistency are tested with evidence",
        ],
    ),
    "data-architect": sp(
        "architecture",
        r"Is the high-level data architecture (scale, standard, governance) sound and extensible?",
        [
            r"Consistency with requirements and scale",
            r"Managing model, text, and lifecycle",
            r"Access, governance, and quality",
            r"Extensibility and maintainability",
        ],
        [
            r"Defining the data model, layers, and standards",
            r"Defining data governance, catalog, and lineage",
            r"Selecting storage and processing",
            r"Managing quality, security, and compliance",
        ],
        [
            r"The architecture has layers, standards, and mapping",
            r"Catalog, lineage, and governance exist",
            r"Scalability, quality, and security are assessed",
        ],
    ),

    # ----------------------------- ops/infra ---------------------------
    "system-architect": sp(
        "architecture",
        r"Is the overall system architecture (software, hardware, infrastructure) coherent and executable?",
        [
            r"Coverage of the complete system and components",
            r"Consistency of software, hardware, and infrastructure",
            r"Scale, resilience, and security",
            r"Executability and changeability",
        ],
        [
            r"Defining the system view, components, and interface",
            r"Designing deployment, infrastructure, and hardware",
            r"Managing optimisation and failure reduction",
            r"Defining decisions and artifacts",
        ],
        [
            r"The system architecture has a map, boundaries, and tones",
            r"Critical components have redundancy and scale",
            r"Decisions are documented with trade-offs and review",
        ],
    ),
    "solution-architect": sp(
        "architecture",
        r"Is the high-level system solution designed with technology selection and need fit?",
        [
            r"Coverage of functional, non-functional, and constraints",
            r"Technology selection logic",
            r"Managing cost, complexity, and risk",
            r"Executability and changeability",
        ],
        [
            r"Defining solution options and criteria",
            r"Selecting technology, contract, and integration",
            r"Managing cost, complexity, and trade-offs",
            r"Defining the architecture decision and rollout",
        ],
        [
            r"The solution includes options, selection, and justification",
            r"Technology is selected by criteria (fit, cost, lock-in)",
            r"The solution is converted into an implementable plan",
        ],
    ),
    "enterprise-architect": sp(
        "architecture",
        r"Is the software architecture aligned with the overall enterprise architecture?",
        [
            r"Consistency with enterprise architecture and standards",
            r"Alignment with strategy and governance",
            r"Managing integration and data",
            r"Appropriateness, review, and responsibility",
        ],
        [
            r"Defining enterprise architecture and policy",
            r"Mapping solutions to domains",
            r"Managing interoperability and compliance",
            r"Defining review, governance, and change",
        ],
        [
            r"Solutions map to enterprise standards and strategy",
            r"Data, service, and integration align with enterprise architecture",
            r"Decisions are documented with governance and compliance",
        ],
    ),
    "release-engineer": sp(
        "devops",
        r"Is the build and release process managed with stability, security, and reversibility?",
        [
            r"Quality of pipeline, version, and artifact",
            r"Coverage of rollback and canary",
            r"Security, audit, and reproducibility",
            r"Consistency with the environment",
        ],
        [
            r"Defining versioning, artifacts, and signing",
            r"Implementing the release pipeline and gates",
            r"Managing rollout, rollback, and canary",
            r"Defining changelog and release notes",
        ],
        [
            r"Every release has a version, artifact, and checksum",
            r"Rollback and canary are defined and tested",
            r"Release notes and audit are traceable",
        ],
    ),
    "build-engineer": sp(
        "devops",
        r"Are build, packaging, and dependencies managed with stability and reproducibility?",
        [
            r"Quality of build, config, and caching",
            r"Coverage of dependencies and vulnerabilities",
            r"Reproducibility and artifacts",
            r"Consistency with speed and size",
        ],
        [
            r"Defining build scripts, Docker, and CI",
            r"Managing dependencies, locks, and security",
            r"Implementing caching and parallel execution",
            r"Producing artifacts that can be tested",
        ],
        [
            r"The build is free of hardcoding and reproducible",
            r"Dependencies are secured by lock files and scanning",
            r"Artifacts and errors are visible in CI",
        ],
    ),

    # --------------------------- misc roles ----------------------------
    "scrum-product-team": sp(
        "support",
        r"Are iterative development processes run coherently with roles and Scrum work?",
        [
            r"Code and iteration output with focus",
            r"Coverage of sprint items and definition",
            r"Team collaboration and delivery quality",
            r"Consistency with the sprint goal",
        ],
        [
            r"Defining the sprint goal and backlog selection",
            r"Running daily, refinement, review, and retro",
            r"Managing blocked items, issues, and ownership",
            r"Defining the definition of done and sprint acceptance",
        ],
        [
            r"Every sprint has a goal and related items",
            r"Outputs are checked against DoD and acceptance",
            r"Retros and issues are recorded for improvement",
        ],
    ),
    "ui-ux-research-participants": sp(
        "support",
        r"Is participation in testing/user research done with honest, usable feedback?",
        [
            r"Quality and honesty of feedback",
            r"Coverage of scenario and cause",
            r"Consistency with the test goal",
            r"Desired and definable data",
        ],
        [
            r"Familiarity with the study scenario and goal",
            r"Executing tasks and stating behaviour/problem",
            r"Recording feedback and observations",
            r"Feedback with suggestion and initiative",
        ],
        [
            r"Feedback links to each task and screen",
            r"Observations are recorded with findings, quotes, and documents",
            r"Consistency with privacy and discussion",
        ],
    ),
    "beta-tester": sp(
        "support",
        r"Is experimental use of the product before release done with precise, safe reporting?",
        [
            r"Coverage of use cases and scenarios",
            r"Reporting bugs, feedback, and information",
            r"Security and configuration",
            r"Consistency with the beta goal",
        ],
        [
            r"Receiving access, exploration, and use",
            r"Executing flows and recording issues",
            r"Findings with information (build, step, evidence)",
            r"Feedback to the team and quality preservation",
        ],
        [
            r"Issues are reported with severity, steps, and evidence",
            r"The feedback and documentation guide is specified",
            r"Non-disclosable information does not leak",
        ],
    ),
    "end-user": sp(
        "support",
        r"Is real use of the product carried out with practical feedback and effective impact?",
        [
            r"Use in a real scenario",
            r"Reporting problem and expectation",
            r"Reaction to UX and performance",
            r"Useful and safe feedback",
        ],
        [
            r"Setting goals and day-to-day use",
            r"Recording problems, friction, and efficiency",
            r"Reporting to the team and the path",
            r"Security, information, and compliance",
        ],
        [
            r"Feedback covers behaviour, document, and file",
            r"Problems are reported with severity and reproduction",
            r"Personal and sensitive information is not disclosed",
        ],
    ),
}


# --------------------------------------------------------------------------
# Fallback group specs (only used if a slug isn't explicitly in SPECS above).
# These are still functional, but every real role currently has a bespoke spec.
# --------------------------------------------------------------------------

GROUP_SPEC = {
    "strategy": (r"Strategy and top-level direction",
        [r"Alignment with vision and top-level goals", r"Transparency and feasibility of decisions",
         r"Allocation and effect of resources", r"Managing risk and uncertainty"],
        [r"Defining objective, non-goal, and KPI", r"Defining the decision model",
         r"Decomposing the goal into outputs", r"Defining the success criteria"],
        [r"Goals are measurable and tied to KPIs", r"Non-goals are documented",
         r"Decisions are recorded with owner and rationale"]),
    "product": (r"Product process / backlog",
        [r"Completeness of the backlog and scope", r"Prioritisation by value and risk",
         r"Clarity of acceptance and definition of done", r"Consistency of the user path"],
        [r"Extracting requirements and user stories", r"Prioritisation by criteria",
         r"Defining the definition of done and acceptance", r"Detecting hidden work and mapping scope"],
        [r"Every item has acceptance criteria and a definition of done", r"Priority is set by criteria",
         r"Requirements appear in the phases without scope loss"]),
    "management": (r"Process / team management",
        [r"Alignment of the plan with time, resources, and risk", r"Scope coverage",
         r"Transparency of role and decision", r"Status traceability"],
        [r"Defining WBS, phases, and owners", r"Defining time, cost, and quality criteria",
         r"Reporting structure", r"Change management"],
        [r"Every step has an owner, time, and dependency", r"Changes are controlled",
         r"Status reporting includes risk and blockers"]),
    "analysis": (r"Analysis / requirements",
        [r"Requirements are complete and unambiguous", r"Acceptance criteria are testable",
         r"Consistency with technical and data reality", r"Traceability of every requirement to its output"],
        [r"Extracting functional, non-functional, data, and UI requirements", r"Converting to acceptance criteria",
         r"Identifying ambiguity and assumptions", r"Defining in and out of scope"],
        [r"Requirements are unambiguous and evidence-backed", r"Acceptance criteria are testable",
         r"No requirement is left without traceability"]),
    "architecture": (r"Architecture",
        [r"Consistency with requirements and scale", r"Change readiness and maintainability",
         r"Consistency of components and contracts", r"Coverage of security, performance, and reliability"],
        [r"Defining component boundaries and contracts", r"Selecting and justifying technology",
         r"Defining decision records", r"Managing backward compatibility"],
        [r"The architecture is documented with boundaries and contracts", r"Decisions are recorded with trade-offs",
         r"Critical components are assessed for scale and security"]),
    "engineering": (r"Engineering / implementation",
        [r"Correct behaviour and maintainability", r"Alignment with architecture and contract",
         r"Coverage of tests, errors, and edge cases", r"Quality of code, DRY, security, and performance"],
        [r"Defining contract, input, and output", r"Implementing the core with validation",
         r"Coverage of edge and failure cases", r"Writing tests and preserving compatibility"],
        [r"Code matches the contract and behaviour", r"Tests cover edge cases",
         r"Code changes meet the standard and introduce no regression"]),
    "ai": (r"AI / data science",
        [r"Quality of model, data, and pipeline", r"Reproducibility and versioning",
         r"Monitoring, drift, and consistency", "Safety/Privacy/Cost"],
        [r"Defining features, data, and metrics", r"Designing the pipeline",
         r"Managing versioning and reproducibility", r"Monitoring and safety"],
        [r"Results are reproducible against metrics", r"The model has monitoring and guardrails",
         r"Bias and privacy risk is made safe"]),
    "data": (r"Data / database",
        [r"Correctness of schema, query, and index", r"Data integrity and quality",
         r"Performance and scale", r"Security, backup, and access"],
        [r"Defining schema and migration", r"Optimising query and index",
         r"Implementing validation and cleanup", r"Defining backup, restore, and DR"],
        [r"The schema has constraints and indexes", r"Data assets have tests",
         r"Backup and restore are tested"]),
    "devops": (r"DevOps / infrastructure",
        [r"Repeatability of CI/CD", r"Coverage of failure and rollback",
         r"Security of secrets and least privilege", r"Monitoring and incidents"],
        [r"Defining the pipeline", r"Managing config and secrets",
         r"Designing rollback and canary", r"Defining monitoring and runbook"],
        [r"The pipeline is green and reproducible", r"Deployment has rollback and secure secrets",
         r"Alerts and runbooks are available"]),
    "qa": (r"Testing / quality",
        [r"Coverage of test cases against requirements", r"Coverage of edge and error cases",
         r"Stability and reproducibility", r"Defect follow-up"],
        [r"Test strategy", "Test Data/Fixture",
         r"Coverage of functional, edge, and regression", r"Automation and reporting"],
        [r"Requirements link to tests", r"Tests are reproducible",
         r"Defects are managed with severity and evidence"]),
    "security": (r"Security",
        [r"Coverage of controls", r"Managing vulnerabilities and gaps",
         r"Access, secrets, and data", r"Compliance consistency"],
        ["Threat modeling", "Input validation/authz",
         r"Managing secrets and permissions", "Security tests/scan"],
        [r"Controls have tests and reporting", r"Secrets and permissions comply with policy",
         r"Vulnerabilities have owners and deadlines"]),
    "compliance": (r"Compliance / legal",
        [r"Compliance with laws and policy", r"Coverage of contract, IP, and privacy",
         r"Managing legal risk", r"Documentation and traceability"],
        [r"Identifying requirements", r"Defining contract, IP, and licence",
         r"Traceability and evidence", r"Control gate"],
        [r"Requirements are mapped to gaps and controls", r"Evidence and reports exist",
         r"Decisions are documented with an approval path"]),
    "design": (r"Design / UX / UI",
        [r"Consistency with the design system", r"Coverage of states",
         r"Accessibility and responsiveness", r"Quality of interaction"],
        [r"Extracting the design system and tokens", r"Designing states and responsive behaviour",
         r"Respecting accessibility", "DRY/Reusable components"],
        [r"The design uses tokens and states", r"Accessibility and responsiveness are respected",
         r"Reusable components are consistent"]),
    "content": (r"Content / documentation",
        [r"Accuracy, completeness, and usability", r"Consistency of terminology and structure",
         r"Consistency with release and behaviour", r"Coverage of scenarios and errors"],
        [r"Defining the style guide and structure", r"Producing and reviewing content",
         r"Checking accuracy", r"Coverage of API, install, and error"],
        [r"Docs have a goal, audience, and steps", r"Terminology is consistent",
         r"Docs are consistent with the release"]),
    "people": ("People/HR",
        [r"Alignment with team goals", r"Quality of hiring and assessment",
         r"Fairness, absence of bias, and privacy", r"Effectiveness and retention"],
        [r"Defining role, skill, and criteria", r"Designing the process", r"Managing growth and assessment",
         r"Protecting personal data"],
        [r"The process has criteria and steps", r"Assessment is free of bias",
         r"Data is managed according to privacy policy"]),
    "support": (r"Support / customer",
        [r"Accuracy and speed of response", r"Coverage of problems and errors",
         r"Escalation and ownership", r"Feedback and satisfaction"],
        [r"Defining the response and escalation flow", r"Recording and resolving the issue",
         r"Defining quality criteria", r"Collecting feedback"],
        [r"Every request has a status and owner", r"The SLA is met",
         r"Feedback is recorded with action"]),
    "growth": (r"Growth / marketing / sales",
        [r"Alignment with the goal", r"Measurable KPIs",
         r"Consistency of message and brand", r"Effect and ROI"],
        [r"Defining persona, message, and offer", r"Channel and campaign",
         r"KPI and tooling", r"Sales and negotiation process"],
        [r"Steps have goals and KPIs", r"The message is consistent with the audience",
         r"Results are tracked with data"]),
    "assurance": (r"Audit / assurance",
        [r"Independence and objectivity", r"Complete coverage",
         r"Evidence and traceability", r"Quality of reporting and follow-up"],
        [r"Risk and control matrix", r"Sampling method and evidence",
         r"Determining severity and evidence", r"Reporting and follow-up"],
        [r"Every finding has severity, evidence, and action", r"Scope and criteria are documented",
         r"Actions have owners and deadlines"]),
    "ops": (r"Operations / readiness",
        [r"Consistency with the runbook", r"Coverage of reliability and incidents",
         r"Speed and recovery", r"Continuous improvement"],
        [r"Defining the runbook and alerts", r"Responding to incidents",
         r"Managing recovery", "Postmortem/improvement"],
        [r"Alerts and runbooks have roles", r"Recovery is documented with timings",
         r"The postmortem has actions and owners"]),
}


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def _slug(title: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", title)
    if not words:
        return re.sub(r"\s+", "-", title).strip("-").lower()
    s = "-".join(w.lower() for w in words)
    return re.sub(r"-+", "-", s).strip("-")


def _lines(items) -> str:
    return "\n".join(f"- {x}" for x in items)


def spec_for(slug: str) -> dict:
    """Return bespoke spec, falling back to its group spec if absent."""
    if slug in SPECS:
        s = SPECS[slug]
        if s["mission"]:
            return s
    # fallback by group mapping
    group = GROUP_OF.get(slug, "engineering")
    mission, audit, impl, accept = GROUP_SPEC[group]
    return sp(group, mission, audit, impl, accept)


# Map every REAL slug to a group (only needed for fallback handling).
GROUP_OF = {
    "founder": "strategy", "product-visionary": "strategy", "investor": "strategy",
    "board-of-directors": "strategy", "project-sponsor": "strategy",
    "business-analyst-ba": "analysis", "domain-expert-sme": "analysis",
    "product-manager-pm": "product", "product-owner-po": "product",
    "project-manager": "management", "program-manager": "product",
    "pmo": "management", "scrum-master": "management", "agile-coach": "management",
    "technical-project-manager": "management", "solution-architect": "architecture",
    "software-architect": "architecture", "enterprise-architect": "architecture",
    "system-architect": "architecture", "technical-lead-tech-lead": "engineering",
    "engineering-manager": "management", "staff-engineer": "engineering",
    "principal-engineer": "engineering", "software-engineer": "engineering",
    "backend-developer": "engineering", "frontend-developer": "engineering",
    "full-stack-developer": "engineering", "mobile-developer": "engineering",
    "desktop-developer": "engineering", "game-developer": "engineering",
    "embedded-developer": "engineering", "firmware-engineer": "engineering",
    "iot-engineer": "engineering", "ai-ml-engineer": "ai",
    "data-scientist": "ai", "data-engineer": "data", "mlops-engineer": "ai",
    "prompt-engineer": "ai", "ai-engineer": "ai",
    "database-administrator-dba": "data", "database-engineer": "data",
    "data-architect": "architecture", "devops-engineer": "devops",
    "sre-site-reliability-engineer": "devops", "cloud-engineer": "devops",
    "cloud-architect": "architecture", "infrastructure-engineer": "devops",
    "network-engineer": "devops", "system-administrator": "devops",
    "release-engineer": "devops", "build-engineer": "devops",
    "qa-engineer": "qa", "qa-lead": "management", "test-engineer": "qa",
    "test-automation-engineer": "qa", "performance-engineer": "qa",
    "load-stress-tester": "qa", "security-engineer": "security",
    "application-security-engineer": "security", "cybersecurity-engineer": "security",
    "penetration-tester": "security", "security-architect": "architecture",
    "devsecops-engineer": "devops", "privacy-engineer": "security",
    "ui-designer": "design", "ux-designer": "design", "product-designer": "design",
    "ux-researcher": "analysis", "ux-writer-content-designer": "content",
    "design-system-designer": "design", "graphic-designer": "design",
    "motion-designer": "design", "accessibility-specialist": "design",
    "technical-writer": "content", "documentation-specialist": "content",
    "localization-specialist": "content", "translator": "content",
    "legal-advisor": "compliance", "ip-copyright-specialist": "compliance",
    "privacy-compliance-officer": "compliance", "contract-manager": "compliance",
    "finance-manager": "management", "procurement-specialist": "growth",
    "hr-people-manager": "people", "recruiter": "people",
    "technical-recruiter": "people", "scrum-product-team": "support",
    "ui-ux-research-participants": "support", "beta-tester": "support",
    "end-user": "support", "customer-support-agent": "support",
    "technical-support-engineer": "support", "customer-success-manager": "support",
    "community-manager": "support", "product-marketing-manager": "growth",
    "marketing-specialist": "growth", "seo-specialist": "growth",
    "aso-specialist": "growth", "growth-manager": "growth",
    "sales-manager": "growth", "sales-representative": "growth",
    "account-manager": "support", "business-development-manager": "growth",
    "partnership-manager": "growth", "operations-manager": "management",
    "devrel": "engineering", "technical-evangelist": "engineering",
    "incident-manager": "management", "on-call-engineer": "devops",
    "maintenance-engineer": "engineering", "refactoring-engineer": "engineering",
    "legacy-modernization-engineer": "engineering", "finops-specialist": "devops",
    "observability-engineer": "engineering", "data-analyst": "analysis",
    "bi-analyst": "analysis", "product-analyst": "analysis",
    "risk-manager": "management", "change-manager": "management",
    "quality-manager": "management", "audit-specialist": "assurance",
    "external-auditor": "assurance", "vendor-manager": "management",
    "third-party-integration-specialist": "engineering",
    "migration-specialist": "engineering", "deployment-engineer": "engineering",
    "disaster-recovery-specialist": "engineering",
    "backup-administrator": "engineering", "business-continuity-manager": "management",
    "product-owner-release": "product", "end-of-life-manager": "product",
    "decommission-engineer": "engineering",
}


# --------------------------------------------------------------------------
# Prompt builders (structure stays stable; body comes from bespoke spec)
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Executable Role Contract primitives
# --------------------------------------------------------------------------

DECISION_STATES = [
    "PASS", "FAIL", "BLOCKED", "NEEDS_CLARIFICATION",
    "ESCALATE", "NOT_APPLICABLE",
]

STATE_MACHINE = [
    "RECEIVED", "ANALYZING", "READY", "IMPLEMENTING", "INTEGRATING",
    "TESTING", "REVIEW_PENDING", "CHANGES_REQUIRED", "VERIFIED", "COMPLETED",
    "BLOCKED", "ESCALATED", "FAILED",
]

KPI_METRICS = {
    "strategy": ["Decision-to-outcome alignment %", "Metricable objective coverage", "Risk-adjusted ROI"],
    "product": ["Feature value realization", "Backlog health index", "Scope-change rate"],
    "management": ["Escalation response time", "Blocker resolution time", "Plan variance (time/cost/quality)"],
    "analysis": ["Requirement ambiguity rate", "Acceptance-criterion coverage", "Traceability completeness %"],
    "architecture": ["Architecture review pass rate", "Change impact coverage", "Technical debt / NFR compliance"],
    "engineering": ["Defect escape rate", "Test coverage %", "Regression rate", "Build/review cycle time", "p95 latency / throughput"],
    "ai": ["Model quality (accuracy / eval score)", "Reproducibility rate", "Drift / alarm count", "Cost per request"],
    "data": ["Data quality pass rate", "Pipeline success rate", "Backup / restore success", "Query cost / latency"],
    "devops": ["Deploy success rate", "Rollback frequency", "Provisioning change failure rate", "Mean time to detect/recover"],
    "qa": ["Defect escape rate", "Test coverage %", "Flaky test rate", "Automation coverage %"],
    "security": ["Control coverage %", "Critical-finding to fix time", "Vulnerability reduction", "Policy compliance %"],
    "compliance": ["Compliance score", "Evidence completeness", "License/IP issues closed", "Regulatory finding closure"],
    "design": ["Design-system deviation count", "State coverage %", "A11y pass rate", "Component reuse rate"],
    "content": ["Doc accuracy %", "Terminology consistency", "Search/read success", "Docs freshness"],
    "people": ["Time-to-hire", "Hiring quality score", "Retention rate", "Fairness / bias checks"],
    "support": ["First-response SLA", "Resolution rate", "CSAT", "Escalation correctness"],
    "growth": ["Conversion / CAC / LTV", "Organic & paid acquisition", "Campaign ROI", "Experiment decision rate"],
    "assurance": ["Finding accuracy", "Evidence completeness", "Independent coverage", "Audit closure rate"],
    "ops": ["Availability / MTTR", "Runbook coverage", "Incident recurrence", "Recovery readiness"],
}

ROLE_SPECIAL_BLOCKS = {
    "frontend-developer": """## State Model (UI) — identifying applicable states
Assess the following states purely on the basis of the feature's logic; **not all of them are required**:
- Initial, Loading, Success/Ready, Empty, Error, Retrying, Disabled, Submitting,
  Success-after-submit, Submission-error, Unauthorized (401), Forbidden (403),
  Offline, Partial, Stale
- For each state report `APPLICABLE / NOT_APPLICABLE`; if applicable, define its entry/exit conditions and behaviour.
- If a feature is genuinely without an empty/error/loading path, record it as `NOT_APPLICABLE`; do not inflate the feature artificially just to cover a state.""",
    "backend-developer": """## Transaction & Concurrency Policy
- **Assess first, then decide**: introduce a transaction or concurrency control (such as optimistic locking) only where data integrity or business rules require it.
- **Do not create an unnecessary transaction boundary**: define the transaction around a single logical unit of change with a stated consistency; avoid long or unjustified transactions.
- Where needed, document the `Concurrency` controls (such as version / CAS) and the `Retry` behaviour.
- Record every transaction decision with its reason and its effect on data and performance.

## Security Baseline (Backend) — minimum controls
These items are within your scope and must be respected:
- Authentication, Authorization, Input Validation, Output Validation
- Injection Protection, Sensitive Data Handling, Secret Handling, Rate Limiting
- Error Disclosure (no disclosure of internal details), Logging, Auditability, Dependency Security
- If there is a security architecture decision, a complex control design, or a critical vulnerability, **do not keep it**; explicitly ESCALATE it to the Security Engineer / Application Security Engineer.""",
}


def _extra_role_blocks(slug: str) -> str:
    return ROLE_SPECIAL_BLOCKS.get(slug, "")


def _kpi_list(group: str) -> str:
    items = KPI_METRICS.get(group, KPI_METRICS["engineering"])
    return "\n".join(f"- {x}" for x in items)


def _norm_text(value: str) -> str:
    value = value.replace(r",", ", ").replace("\u3001", ", ").replace("\u200c", "")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def _norm_persona(persona: dict) -> dict:
    return {k: _norm_text(v) for k, v in persona.items()}


def _bullets(value: str) -> str:
    parts = [x.strip() for x in re.split(r"[,\u060c]", value) if x.strip()]
    if not parts:
        return "- —"
    return "\n".join(f"- {x}" for x in parts)


def _steps(value: str) -> str:
    parts = [x.strip() for x in re.split(r"\u2192", value) if x.strip()]
    if not parts:
        return ["—"]
    return parts


def _decisions(value: str) -> str:
    parts = [x.strip() for x in re.split(r"[,\u060c/]", value) if x.strip()]
    if not parts:
        return ["—"]
    return parts


def _step_kind(name: str) -> str:
    n = name.lower()
    if any(k in n for k in ["analy", "understand", "discover", "assess", "review input"]):
        return "ANALYZE"
    if any(k in n for k in ["design", "plan", "architect", "model", "define", "research"]):
        return "DESIGN"
    if any(k in n for k in ["implement", "build", "develop", "create", "code", "write", "transform"]):
        return "IMPLEMENT"
    if any(k in n for k in ["integrat", "connect", "link", "wire", "deploy"]):
        return "INTEGRATE"
    if any(k in n for k in ["test", "validat", "verify", "check", "optim"]):
        return "TEST"
    if any(k in n for k in ["review", "report", "deliver", "retrospect", "monitor", "measure"]):
        return "REVIEW"
    return "GENERIC"


_STEP_ACTIONS = {
    "ANALYZE": [
        r"Review the scope of work and the required inputs.",
        r"Identify the affected code, document, data, or service.",
        r"Identify the interfaces, dependencies, and hidden risks.",
        r"Determine the applicability or non-applicability of each item.",
    ],
    "DESIGN": [
        r"Compare the valid options against stated criteria and document them.",
        r"Constrain the design/plan to this persona's scope and authority boundary.",
        r"Identify the contracts, tokens, protocols, and relationships.",
        r"Assess the change's effect on existing behaviour; escalate changes outside scope.",
    ],
    "IMPLEMENT": [
        r"Implement only this persona's scope; avoid touching another persona's ownership.",
        r"Validate the inputs and produce the output according to contract.",
        r"Cover edge cases, error paths, and related states.",
        r"Preserve existing behaviour unless the change is deliberate and documented.",
    ],
    "INTEGRATE": [
        r"Verify the contract/interface between components (without interfering with others' ownership).",
        r"Preserve backward and behavioural compatibility.",
        r"Isolate and document integration errors, and escalate where the responsibility boundary belongs to another persona.",
    ],
    "TEST": [
        r"Write and run tests/validation appropriate to the scope.",
        r"Cover the applicable states (success/failure/empty/edge/authz/perf).",
        r"Record the test result with evidence; report insufficient evidence as `BLOCKED`/`NEEDS_CLARIFICATION`.",
    ],
    "REVIEW": [
        r"Compare the output against the Quality Gate and Definition of Done.",
        r"Check the evidence and traceability.",
        r"Report the final result with a status and a State Machine state.",
    ],
    "GENERIC": [
        r"Review and prepare the input, then produce and document the output according to the step.",
        r"If the input is incomplete or beyond scope, behave according to the decision rules.",
    ],
}


def _structured_steps(p: dict, group: str, slug: str) -> str:
    steps = _steps(p["procedure"])
    lines = []
    for i, name in enumerate(steps, 1):
        kind = _step_kind(name)
        actions = _STEP_ACTIONS[kind]
        lines.append(f"### STEP {i} — {name}  [{kind}]")
        lines.append("")
        lines.append(f"**Objective:** execute the step \"{name}\" while preserving scope and without changes outside your authority.")
        lines.append("")
        lines.append(f"**Inputs:** {p['required']}  |  Optional: {p['optional']}  |  Context: {p['context']}  |  Preconditions: {p['preconditions']}")
        lines.append("")
        lines.append("**Actions:**")
        for j, a in enumerate(actions, 1):
            lines.append(f"{j}. {a}")
        lines.append("")
        lines.append("**Validation:**")
        lines.append(f"- {p['quality']}")
        lines.append(r"- Inputs are present and valid; no unresolved conflict or incompatibility remains.")
        lines.append("")
        lines.append(f"**Outputs:** {p['outputs']}")
        lines.append("")
        lines.append(f"**Evidence:** {p['evidence']}")
        lines.append("")
        lines.append(r"**Exit Criteria:** the step's output matches the acceptance criterion and the evidence is recorded.")
        lines.append("")
        lines.append(r"**Failure Conditions:** incomplete or contradictory input, out of scope, or insufficient evidence.")
        lines.append("")
        lines.append(f"**Escalation Conditions:** {p['escalation']}")
        lines.append("")
    return "\n".join(lines).strip()


def _authority_rules(role_type: str) -> str:
    return """## Authority & Boundaries
- You may decide only within **this scope and authority level**. Do not decide outside it.
- If a decision affects another persona's ownership (for example architecture, database, security, design, CI/CD):
  1) identify the conflict/impact;
  2) preserve current behaviour where possible;
  3) document the impact;
  4) **ESCALATE** to the responsible persona — do not stay silent and do not decide unilaterally."""


def _traceability() -> str:
    return """## Traceability
Connect every output to this chain:
`Requirement → Design → Implementation → Test → Evidence → Acceptance`
Identification pattern:
- `REQ-###` (requirement)
- `DESIGN-###` (related design)
- `IMP-###` (implementation / component / file)
- `TEST-###` (test / validation)
- `EVIDENCE-###` (log, screenshot, report, evidence)
- `ACCEPT-###` (acceptance / quality gate)
If no formal identifier exists, create a descriptive, traceable one and record it in `Execution Result`."""


def _state_machine_block() -> str:
    return (
        """## State Machine
Steps move through these states (the orchestrator uses `status` to know where the persona is):
`RECEIVED` → `ANALYZING` → `READY` → `IMPLEMENTING` → `INTEGRATING` → `TESTING` → `REVIEW_PENDING` → `CHANGES_REQUIRED` → `VERIFIED` → `COMPLETED`
Plus the side states: `BLOCKED`, `ESCALATED`, `FAILED`
- At start: `RECEIVED`; after successful analysis: `READY`; after final approval: `COMPLETED`.
- If changes are requested: return to `CHANGES_REQUIRED`; if blocked: `BLOCKED`/`ESCALATED`.
- Never invent a state on your own; use exactly this set."""
    )


def _decision_block_body(p: dict) -> str:
    parts = _decisions(p["decision"])
    return """## Decision Rules

This Persona's decision rules:
""" + "\n".join(f"- {x}" for x in parts) + f"""\n- At each step, choose the status only from the set below: `{", ".join(DECISION_STATES)}`\n- `PASS` = complete, valid output with evidence; `FAIL` = erroneous or incomplete output.\n- `BLOCKED` = external obstacle or missing input; `NEEDS_CLARIFICATION` = ambiguity needing confirmation (not necessarily an error).\n- `ESCALATE` = a decision beyond scope or a significant danger; `NOT_APPLICABLE` = the step is meaningless for this item (with a reason)."""


def _execution_result_block() -> str:
    return """## Execution Result (machine-processable by the orchestrator)
Give the final output in this format (the same structure can later be converted to JSON):
```
Status: PASS | FAIL | BLOCKED | ESCALATE | NEEDS_CLARIFICATION | NOT_APPLICABLE
State:  <one of the State Machine states>
ExecutionPlan: <path to the plan file in audits/ and the phases/steps updated in this run | N/A if no plan exists>
PlanStatus: <🔴 / 🟡 / 🟢 for each changed step/phase>
Completed Steps: [...]
Modified Files: [...]
Created Files: [...]
Tests: [...]
Evidence: [...]
Issues: [...]
Assumptions: [...]
Unknowns: [...]
Risks: [...]
Required Decisions: [...]
Traceability: REQ-### → ... → ACCEPT-###
Handoff: [...]
Next Action: [...]
```"""


def _ready_done_block(quality: str) -> str:
    return f"""### Definition of Ready / Done / Quality Gates\n**Definition of Ready (before starting):**\n- Required inputs are present and valid (`{quality}`).\n- The assigned scope is clear and no blocking conflict or ambiguity remains.\n- This persona's preconditions are satisfied.\n\n**Definition of Done (after completion):**\n- Every step of the Procedure has been executed in full.\n- Outputs and evidence are recorded; the acceptance criterion `{quality}` is met.\n- Related tests/validation are green; no blocking issues.\n- `Handoff` and `Execution Result` are complete.\n\n**Quality Gates:**\n- Functional / behavioural correctness\n- Integration & backward compatibility\n- Quality/Perf/Security criteria relevant to this persona\n- Evidence & traceability\n- Regression safety"""


def _kpi_block(group: str) -> str:
    return """## KPI / Performance Metrics (measurable)
""" + _kpi_list(group) + """
- These KPIs are for **performance evaluation**; you must not behave artificially to reach a number.
- In the final report, record each KPI only with real evidence, and if there is no data, write `Unknown`."""


def audit_result_block() -> str:
    return """## Execution Result (machine-readable by the Orchestrator)
Give the audit results in the following format:
```
Status: PASS | FAIL | BLOCKED | ESCALATE | NEEDS_CLARIFICATION | NOT_APPLICABLE
Verdict: <Consistent & ready / Inconsistent / Needs redesign ...>
State: <one of the State Machine states>
Coverage: [item | evidence source | status]
Coverage Manifest: [Segment | Files/Components | Review Status (DONE/IN_PROGRESS/NOT_REVIEWED+Reason)]
Decomposition: [Segment | Files/Components | Findings]
Findings: [ID | File/Line | Severity | Confidence | EvidenceStatus | Summary]
ExecutionPlan: <path of the saved execution-plan file under audits/, e.g. audits/<slug>-execution-plan.md>
Affected Locations: [...]
Critical/High Findings: [...]
Required Decisions: [...]
Traceability: REQ-### → ... → ACCEPT-###
Handoff: [...]
Next Action: [...]
Also record: Assumptions / Unknowns / Risks if any.
```

"""
def audit_final_structure() -> str:
    return """## Final Audit Output
1. **Executive summary**: overall state, the most important risks, readiness.
2. **Coverage Manifest**: the full list of in-scope sections/files and the review status of each (reviewed / in progress / not reviewed + reason). No section may remain "not reviewed" without a reason.
3. **Decomposition Table**: `Segment | Files/Components | Review status | Findings | Note`.
4. **Coverage table** (item | evidence source | PASS/FAIL/NOT_APPLICABLE status).
5. **Findings** in the format below and after deduplication; every finding carries `FILE / LINE`.
6. **Final verdict** + action priority (SEVERITY → CONFIDENCE → EVIDENCE_STATUS).
7. **Execution plan**: the path of the file saved in `audits/` and a summary of the phases and coverage status.

Some findings may be `NOT_APPLICABLE`; record the reason for not-applicable instead of manufacturing an artificial finding.
A claim of "fully reviewed" is permitted only when the Coverage Manifest and Decomposition Table cover the entire scope and no file or section has been dropped without a reason."""


def _codebase_analysis_rules() -> str:
    return """## Code and Codebase Analysis Rules (mandatory for supervisors)
### a) No guessing or speculation
- Record no claim without direct evidence. Every finding must reference a `FILE / LINE` or a specific source (file, component, document, log, test output).
- If something is merely "possible/speculative", mark it explicitly as `POTENTIAL` or `ASSUMPTION` and state `MISSING EVIDENCE` and `WHAT WOULD CONFIRM IT`; never present speculation as fact.
- If you do not know, write "Unknown / Requires Verification: ..."; fabricating information or filling a gap with an assumption is forbidden.

### b) File-by-file and line-by-line review
- Review the code **file by file** and **line by line**; superficial review, a general summary, or random sampling in place of full coverage is forbidden.
- For each file record at least: the file path, the file's role/responsibility, its inputs/outputs, its dependencies, and the lines or regions with findings.
- Every finding reference must include `FILE` and, where possible, `LINE`; a finding without a valid line/file reference is not valid.
- Analyse workflows **step by step and in execution order**: the happy path, error paths, branches, retry/rollback, boundary conditions, and state transitions — not just the known points.

### c) Complete and precise finding documentation
- Record every finding in full using the standard "finding format"; leave no finding incomplete or with a partial reference.
- Deduplicate findings, but deleting or ignoring any real finding is not permitted.
- The final report must be independently reproducible on its own; any reader must be able to reach the same line/file/evidence from it.

### d) Safety on large projects and extensive codebases
- Split the whole scope into **smaller, related, reviewable segments** (for example by module/service/layer/folder) and work through each in order without skipping.
- Produce a **Coverage Manifest** that lists every in-scope file/section and shows the status of each (reviewed / in progress / not reviewed + reason).
- Preserve consistency: drop no file or piece of code, ignore no section because it is "large" or "seems unimportant", and do not become careless or indifferent to the code.
- If the scope exceeds what one step can hold, document it in several **Batches** and in each batch report precisely the coverage done and remaining; never claim full coverage of unreviewed work.
- A "not reviewed" status is acceptable only with a valid reason (such as out of scope, deleted file, no access/authorisation) and must be listed in the report."""


def _impl_codebase_rules() -> str:
    return """## Implementation and Codebase Change Rules (mandatory for executors)
### a) No guessing, speculation, or invention
- Never invent an API, file, function, dependency, version, data schema, config, or business rule from memory; read all of them from the codebase, the contracts, and the real documentation.
- If something is needed but unavailable, write explicitly "Unknown / Requires Verification: ..."; if an assumption is unavoidable, mark it "Assumption: ..." and record it in `Execution Result`.
- Never silently convert an assumption into a requirement or a certain behaviour.

### b) File-by-file and line-by-line change
- Before any change, read the whole target file and understand the current behaviour; apply the change minimally, purposefully, and without unnecessary rewriting.
- Record every modified/created file with its full path in `Modified Files`/`Created Files`; do not touch files outside the scope.
- Follow the workflow from input to output (happy path, error paths, branches, retry/rollback, boundary conditions, state transitions) so your change does not break the chain or backward compatibility.

### c) Complete change documentation
- Record every change with its "reason + effect"; no change may be silent.
- Fill in `Execution Result` completely (Modified/Created Files, Tests, Evidence, Assumptions, Unknowns, Risks) and never declare a change without evidence as "done".

### d) Task decomposition and full coverage on large codebases
- Split the task into small, related, testable increments and perform them in order without skipping.
- Maintain a **Change/Completion Manifest** listing every in-scope file/section with its status (done / in progress / incomplete + reason).
- Leave no requirement or file incomplete without a reason; claim "done" only when the Manifest and Definition of Done are complete.
- If the scope exceeds what one step can hold, do it in several **Batches** and in each batch report precisely the coverage done and remaining."""


def _execution_plan_impl_block() -> str:
    return """## Executing According to the Execution Plan and Updating It
- If an execution plan exists for this task (a Markdown file in the `audits/` folder, usually `audits/<slug>-execution-plan.md`), treat it as the **primary reference for execution** and carry the task out phase by phase and step by step exactly according to it; do not reinterpret the plan unilaterally.
- Update the status of every step and phase in that same file as you execute, using only these three statuses: `[🔴]` not done, `[🟡]` partial, `[🟢]` complete.
- Mark a phase `[🟢]` only when **all of its steps** are `[🟢]` and the phase's acceptance criterion is met; never dress up "most steps done" as "complete".
- Do not delete completed steps; do not silently rewrite requirements; do not delete failed or hard work just because it is difficult.
- If newly required work is discovered, add it to the appropriate phase and write down why; if the architecture or a dependency changed, update the plan explicitly.
- If no plan exists, record that explicitly as `Unknown` and proceed according to this prompt's Structured Procedure; do not claim alignment with a plan that does not exist."""


def _audit_execution_plan_block(slug: str) -> str:
    return f"""## Producing and Saving the Execution Plan (mandatory for supervisors)\nAs a supervisor, in addition to the audit report you must produce a precise, dependency-aware **execution plan** and save it as a **file** at `audits/` so the executor can carry it out and update it phase by phase.\n\n### Method and source\n- Follow the full \"Execution Plan Generator\" instructions in `prompts/composite/Execution Plan Generator.md`; treat it as part of this audit's scope and respect all of its rules (1 to 19).\n- Before producing the plan, analyse the task deeply: functional/non-functional/architecture/data/API/UI/security/performance/test/migration/compatibility requirements, existing system constraints, risks, unknowns, and the required sequence.\n- Build the dependency graph and derive the true priority from it (blocking prerequisites → architecture/infrastructure → core logic → contracts/interfaces → integration → secondary features → optimization → testing/hardening → documentation and delivery); never place an apparently important feature ahead of a blocking technical prerequisite.\n- Identify Hidden Work (validation, auth, error handling, migration, tests, documentation, backward compatibility, and so on) and delete nothing merely because it was \"not explicitly mentioned\".\n\n### Phase and step design rules\n- Each phase is a complete, coherent unit of engineering work, not a category label; the steps inside a phase must be completable in a single execution stage.\n- Do neither **artificial Fragmentation** (a separate phase for every tiny move) nor **Over-Merging** (merging unrelated/high-risk work into one giant phase); keep the balance between \"meaningful enough\" and \"executable and verifiable enough\".\n- Each phase must leave the project in a stable, consistent, verifiable state (tests green, migration complete, contracts compatible, no deliberate breakage).\n- Each step must be one specific implementation responsibility (what, where, what behaviour, what dependency, what must be preserved, expected result) — not a vague sentence like \"improve the system\".\n- The plan must define *what* must be achieved and give the executor reasonable freedom in *how*.\n- Each phase must have an objective, measurable acceptance criterion; \"it works\" is not a criterion.\n\n### No guessing in the plan\n- Invent no requirement/API/file/architecture/technology/schema/dependency/existing behaviour or business rule; write \"Unknown / Requires Verification: ...\" and \"Assumption: ...\" explicitly and never silently convert an assumption into a requirement.\n\n### Anti Scope Loss and Quality Gate\n- Before finalising, run a **Scope Audit** confirming that every requirement of the original task is represented somewhere in the plan (implementation, integration, testing, error handling, config, migration, documentation, verification).\n- Review the plan through the lens of a senior architect, senior developer, QA, TPM, security, DevOps, and requirements analyst, and fix every issue (missing requirement, wrong order, hidden/circular dependency, Fragmentation/Over-Merging, missing testing/validation/error handling/migration, security gap, unmeasurable criterion, vague step, unsupported assumption, Scope Creep) before delivery.\n\n### Execution status system\n- Every phase and step must carry the status `[🔴]` (not done) / `[🟡]` (partial) / `[🟢]` (complete); the plan starts entirely `[🔴]`.\n- The plan is a living document: the executor updates statuses while executing, adds newly required work with a reason, and applies architecture/dependency changes explicitly; without deleting completed steps.\n\n### Output and storage location (mandatory)\n- Produce the plan exactly in the \"Final Plan Format\" structure: the section `# Fixed Project Execution Rules` (at least the rules equivalent to items 17) and the section `# Execution Plan` with the phases, steps, and each phase's acceptance criterion.\n- Save the plan as a Markdown file in the `audits/` folder; suggested name pattern: `audits/{slug}-execution-plan.md` (if there is a clash or several versions, add a date/version suffix).\n- Record the plan file path in `Execution Result` (the `ExecutionPlan` field) and in `Handoff` so the executor can find and follow it."""


def audit_prompt(title: str, persona: dict, slug: str) -> str:
    s = spec_for(slug)
    p = persona
    group = s["domain"]
    special = _extra_role_blocks(slug)
    return f"""# Prompt System — Audit of \"{title}\"\n\n## 1) Identity\n- **Role:** {title} (supervisor)\n- **Mission:** {p['mission']}\n- **Authority:** {p['scope']}  |  Access: {p['permissions']}\n\n## 2) Responsibilities and Boundaries\n{_bullets(p['responsibilities'])}
{_authority_rules('audit')}\n\n## 3) Inputs and Preconditions\n- Required: {p['required']}
- Optional: {p['optional']}
- Context: {p['context']}
- Preconditions: {p['preconditions']}\n\n## 4) Audit Process (Structured Procedure)\n{_structured_steps(p, group, slug)}

{_decision_block_body(p)}\n\n## 5) Tools\n- Allowed: {p['allowed']}
- Restricted / Forbidden: {p['restricted']}\n\n## 6) Validation\n{_ready_done_block(p['quality'])}\n\n## 7) Evidence & Traceability\n- Required evidence: {p['evidence']}
{_traceability()}\n\n## 8) Output and Handoff\n- Audit output: {p['outputs']}
- Handoff: {p['handoff']}
- Escalation: {p['escalation']}\n\n## 9) Memory\n- {p['memory']}

{_state_machine_block()}

{_kpi_block(group)}

{special}\n\n## Audit Rules (mandatory)\n- Every finding must refer to a specific **file/component/data/document**; without a valid reference it is not valid.\n- If real rendering/execution is not possible, mark the finding `POTENTIAL`; tool availability is a state you determine, not an assumption.\n- Record findings that share a root cause as one **Root Finding** with `Affected`; do not create duplicate findings.\n- Where evidence is insufficient, write: \"there is not enough evidence to prove this item\".\n- Record `NOT_APPLICABLE` with a reason; never drop a step from the audit without a reason.\n\n\n{_codebase_analysis_rules()}\n\n## Finding Format\n```\nID:\nSEGMENT: <the decomposition section the finding belongs to>\nFILE / LINE: <file path | line number(s)>\nSEVERITY: CRITICAL / HIGH / MEDIUM / LOW / INFO\nCONFIDENCE: CONFIRMED / HIGH / MEDIUM / LOW\nEVIDENCE_STATUS: VERIFIED / POTENTIAL / UNVERIFIED\nCATEGORY:\nTITLE:\nLOCATION:\nEVIDENCE:\nPROBLEM:\nTRIGGER / WHERE IT APPEARS:\nEXPECTED vs ACTUAL:\nIMPACT:\nRECOMMENDED FIX:\nREGRESSION RISK:\n```\nFor `POTENTIAL`/`UNVERIFIED`, add `MISSING EVIDENCE` and `WHAT WOULD CONFIRM IT`.\n\n\n{_audit_execution_plan_block(slug)}

{audit_final_structure()}

{audit_result_block()}\n\n## Audit Acceptance Criteria \"{title}\"
{_lines(s['accept'])}\n- Each finding carries a separate SEVERITY / CONFIDENCE / EVIDENCE_STATUS.\n- Coverage, the State Machine, and the Execution Result are complete and free of duplicate findings.\n- The final verdict rests only on documented findings.\n- The execution plan has been produced per the \"Execution Plan Generator\" and saved as a file under `audits/`; its path is recorded in `ExecutionPlan`.\n- The plan is free of scope loss, artificial fragmentation, and over-merging, and every phase has a measurable acceptance criterion.\n\n"""


def impl_prompt(title: str, persona: dict, slug: str) -> str:
    s = spec_for(slug)
    p = persona
    group = s["domain"]
    special = _extra_role_blocks(slug)
    return f"""# Prompt System — Execution/Implementation of \"{title}\"\n\n## 1) Identity\n- **Role:** {title} (executor/execution)\n- **Mission:** {p['mission']}\n- **Authority:** {p['scope']}  |  Access: {p['permissions']}\n\n## 2) Responsibilities and Boundaries\n{_bullets(p['responsibilities'])}
{_authority_rules('impl')}\n\n## 3) Inputs and Preconditions\n- Required: {p['required']}
- Optional: {p['optional']}
- Context: {p['context']}
- Preconditions: {p['preconditions']}\n\n## 4) Execution Process (Structured Procedure)\n{_structured_steps(p, group, slug)}

{_decision_block_body(p)}\n\n## 5) Tools\n- Allowed: {p['allowed']}
- Restricted / Forbidden: {p['restricted']}\n\n## 6) Validation\n{_ready_done_block(p['quality'])}\n\n## 7) Evidence & Traceability\n- Required evidence: {p['evidence']}
{_traceability()}\n\n## 8) Output and Handoff\n- Outputs: {p['outputs']}
- Handoff: {p['handoff']}
- Escalation: {p['escalation']}\n\n## 9) Memory\n- {p['memory']}

{_state_machine_block()}

{_kpi_block(group)}

{special}\n\n## Implementation Focus Areas Specific to This Role\n{_lines(s['impl'])}\n\n## Execution Rules (mandatory)\n- Execute the task according to the Structured Procedure and preserve the dependencies.\n- Every output must satisfy the acceptance criterion; without approval and evidence, do not claim completion.\n- If the necessary information is absent, write \"Unknown / Requires Verification: ...\" or \"Assumption: ...\".\n- Do not artificially split the work into smaller pieces, and do not merge risky or unrelated work into a single step.\n- Use only the defined Decision States; record `NOT_APPLICABLE` with a reason.\n- Preserve existing behaviour unless you are deliberately changing it; document every change.\n\n\n{_impl_codebase_rules()}

{_execution_plan_impl_block()}

{_execution_result_block()}\n\n## Execution Acceptance Criteria \"{title}\"
{_lines(s['accept'])}\n- The output matches the Quality Gate and every step is documented.\n- The State Machine, Decision Status, and Execution Result are complete.\n- The review/handoff to the identified stakeholder is recorded with evidence.\n- If an execution plan exists under `audits/`, the task has been executed exactly according to it and the step/phase statuses have been updated in that same file (🔴/🟡/🟢).\n\n"""

# --------------------------------------------------------------------------
# README handling
# --------------------------------------------------------------------------

def read_rows() -> list[dict]:
    """Return the rows of the FIRST (quick overview) table in README.md.

    The merged README contains several tables (quick overview, 23-column
    details, category tables); only the first contiguous table block is the
    role registry consumed by the generators.
    """
    data: list[dict] = []
    started = False
    for ln in README.read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if s.startswith("|"):
            started = True
            cells = [c.strip() for c in s.split("|")]
            if cells and cells[0] == "":
                cells = cells[1:]
            if cells and cells[-1] == "":
                cells = cells[:-1]
            if len(cells) < 3:
                continue
            data.append(cells)
        elif started:
            break
    return [r for r in data if not all(set(c) <= set("-: ") for c in r)]


def rewrite_readme(links: dict[str, str]) -> None:
    """Refresh the prompt links of the FIRST (merged main) table in README.md.

    Only the first contiguous table block is rewritten — its 8th column holds
    the prompt link; every other line (domain-grouping tables, mapping, stats,
    prose) passes through untouched.
    """
    out: list[str] = []
    in_table = False
    for ln in README.read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if s.startswith("|"):
            in_table = True
            cells = [c.strip() for c in s.split("|")]
            if cells and cells[0] == "":
                cells = cells[1:]
            if cells and cells[-1] == "":
                cells = cells[:-1]
            if cells and cells[0] == r"Job Title":
                out.append(ln)
                continue
            if cells and all(set(c) <= set("-: ") for c in cells):
                out.append("|" + "---|" * MAIN_COLS)
                continue
            if len(cells) < MAIN_COLS:
                out.append(ln)
                continue
            cells[7] = links.get(cells[0], "")
            out.append("| " + " | ".join(cells) + " |")
            continue
        if in_table:
            in_table = False
        out.append(ln)
    README.write_text("\n".join(out) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def load_details() -> dict[str, dict]:
    """Return title -> persona dict (the 23-column detail data per role).

    Reads details.md when present (legacy layout, 23 columns, detail data
    starting at column 3); otherwise reads the merged 28-column main table in
    README.md, where the detail columns (mission..kpi) start at column 8.
    """
    result: dict[str, dict] = {}
    if DETAILS.exists():
        iterable = DETAILS.read_text(encoding="utf-8").splitlines()[2:]
        width, base = DETAIL_COLS, 3
    else:
        iterable = [
            ln for ln in README.read_text(encoding="utf-8").splitlines()
            if ln.strip().startswith("|")
        ]
        # only keep the first contiguous table block (the merged main table)
        first: list[str] = []
        for ln in iterable:
            if ln.strip().startswith("|"):
                first.append(ln)
            elif first:
                break
        iterable = first
        width, base = MAIN_COLS, 8
    for ln in iterable:
        s = ln.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if cells and cells[0] == "":
            cells = cells[1:]
        if cells and cells[-1] == "":
            cells = cells[:-1]
        if len(cells) != width:
            continue
        if cells[0] == r"Job Title" or all(set(c) <= set("-: ") for c in cells):
            continue
        title = cells[0]
        result[title] = {
            "duties": cells[1],
            "mission": cells[base + 0],
            "responsibilities": cells[base + 1],
            "scope": cells[base + 2],
            "required": cells[base + 3],
            "optional": cells[base + 4],
            "context": cells[base + 5],
            "preconditions": cells[base + 6],
            "procedure": cells[base + 7],
            "decision": cells[base + 8],
            "allowed": cells[base + 9],
            "restricted": cells[base + 10],
            "outputs": cells[base + 11],
            "quality": cells[base + 12],
            "evidence": cells[base + 13],
            "handoff": cells[base + 14],
            "escalation": cells[base + 15],
            "permissions": cells[base + 16],
            "lifecycle": cells[base + 17],
            "memory": cells[base + 18],
            "kpi": cells[base + 19],
        }
    return result


def main(argv: list[str] | None = None) -> None:
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--i-know" not in argv:
        raise SystemExit(
            "REFUSED: this generator uses the legacy _slug() naming and will\n"
            "create duplicate prompts beside the canonical SLUG_OVERRIDES ones\n"
            "and rewrite the README link cells.\n\n"
            "Use the canonical pipeline instead:\n"
            "    python3 scripts/generate_personas.py        # or: make prompts\n\n"
            "If you really want the legacy output, re-run with --i-know."
        )
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    IMPL_DIR.mkdir(parents=True, exist_ok=True)
    AUDITS_DIR.mkdir(parents=True, exist_ok=True)

    rows = read_rows()
    header = rows[0]
    data_rows = [r for r in rows if r[0] != header[0]]
    print(f"Role rows found: {len(data_rows)}")

    details = load_details()
    print(f"Detail rows found: {len(details)}")

    links: dict[str, str] = {}
    missing_spec = []
    missing_detail = []
    for r in data_rows:
        title, duties, role_type = r[0], r[1], r[2]
        slug = _slug(title)
        spec = spec_for(slug)
        if spec["mission"]:
            pass
        else:
            missing_spec.append(slug)

        persona = details.get(title)
        if persona is None:
            missing_detail.append(title)
            persona = {
                "duties": duties,
                "mission": spec["mission"],
                "responsibilities": duties,
                "scope": "—",
                "required": "—",
                "optional": "—",
                "context": "—",
                "preconditions": "—",
                "procedure": "—",
                "decision": "—",
                "allowed": "—",
                "restricted": "—",
                "outputs": "—",
                "quality": "—",
                "evidence": "—",
                "handoff": "—",
                "escalation": "—",
                "permissions": "—",
                "lifecycle": "—",
                "memory": "—",
                "kpi": "—",
            }

        persona = _norm_persona(persona)

        if role_type == r"SUPERVISOR":
            rel = f"prompts/audit/{slug}.md"
            path = ROOT / rel
            path.write_text(audit_prompt(title, persona, slug), encoding="utf-8")
            label = "Audit"
        else:
            rel = f"prompts/implementation/{slug}.md"
            path = ROOT / rel
            path.write_text(impl_prompt(title, persona, slug), encoding="utf-8")
            label = "Implementation"
        links[title] = f"[{label}]({rel})"

    rewrite_readme(links)
    print(f"Audit prompts:     {len(list(AUDIT_DIR.glob('*.md')))}")
    print(f"Implementation:    {len(list(IMPL_DIR.glob('*.md')))}")
    if missing_spec:
        print("WARNING fallback specs used for:", missing_spec)
    else:
        print("All roles use a bespoke specification.")


if __name__ == "__main__":
    main()
