# گزارش انطباق: «Master Persona Schema & Generator Prompt» با فایل‌های `prompts/`

**تاریخ تحلیل:** 2026-08-31
**منبع مقایسه:**
- استاندارد: `Master Persona Schema & Generator Prompt.md` (۲۸۳۲ خط)
- فایل‌های تولیدشده: `prompts/audit/` (۶۸ فایل) و `prompts/implementation/` (۹۰ فایل) = **۱۵۸ فایل**
- جدول منبع: `README.md` (۱۴۴ ردیف = ۵۴ ناظر + ۹۰ مجری) و `prompts/README.md` (ادعای ۶۵ ناظر + ۹۰ مجری = ۱۵۵)
- ژنراتور: `scripts/generate_role_prompts.py` (۴۴۸۸ سطر، + `normalize_details.py`)

---

## ۰) خلاصه اجرایی

| موضوع | استاندارد (Master) | فایل‌های prompt |
|---|---|---|
| تعداد کل نقش‌ها | ۱۴۶ نقش (۴۸ ناظر + ۸۴ مجری + ۱۴ نقش تکمیلی بخش ۶۴.۳) | ۱۵۸ فایل (۶۸ ممیزی + ۹۰ اجرا) |
| ناظرها | ۴۸ + ۸ تکمیلی = ۵۶ | ۶۸ فایل |
| مجری‌ها | ۸۴ + ۶ تکمیلی = ۹۰ | ۹۰ فایل |
| ساختار الزامی هر Persona | ۲۹ سکشن (§۱ و §۶۱) + ۱۰ سکشن ویژه ناظر (§۶۲) + ۱۲ سکشن ویژه مجری (§۶۳) | ~۱۷ هدینگ در ۱۴۸ فایل و ۷ هدینگ در ۱۰ فایل |

**نتیجه‌گیری اصلی:**
1. **۱۲ نقش از Master در `prompts/` وجود ندارند** — همه از بخش ۶۴.۳ (Additional Required Roles).
2. **۲۴ فایل/نقش در `prompts/` وجود دارند که در Role Registry استاندارد نیستند** (۱۸ ممیزی + ۶ اجرا).
3. **ساختار هیچ‌کدام از ۱۵۸ فایل با §۶۱–۶۳ استاندارد مطابقت ندارد.** ژنراتور قالب کاملاً متفاوتی استفاده می‌کند؛ حتی ۱۴۸ فایل با قالب «بلند» و ۱۰ فایل با قالب «کوتاه» تولید شده‌اند (دو ساختار ناهمگون داخل خود `prompts/`).
4. خود Master در §۶۵ مپینگ، ناسازگاری داخلی دارد (نقش‌هایی که در Registry نیستند و نقش‌های مجری که به‌عنوان ناظر استفاده شده‌اند) — این‌ها هم باید اصلاح شوند.

---

## ۱) نقش‌هایی که در Master وجود دارند ولی در `prompts/` وجود ندارند

همهٔ ۱۲ نقش جاافتاده از **بخش ۶۴.۳ «Additional Required Roles»** هستند (بخش‌های ۶۴.۱ و ۶۴.۲ کامل پوشش داده شده‌اند).

### ناظرهای جاافتاده (۶ نقش)

| نقش | چرا مهم است |
|---|---|
| `Architecture Review Board` | مرجع تصمیم/تأیید معماری در §۶۵ (برای Solution/Enterprise/System Architect) |
| `Data Governance Manager` | ناظر Data Engineer و نگهبان حاکمیت داده |
| `Security Governance Manager` | ناظر Cybersecurity Engineer، SOC Analyst، Vulnerability Management، Security Auditor |
| `Release Manager` | ناظر Release Engineer / Deployment Engineer |
| `Service Owner` | ناظر SRE |
| `Platform Owner` | ناظر سکو/پلتفرم (در Mapping §۶۵ به‌عنوان ناظر Infrastructure Engineer استفاده می‌شود) |

### مجری‌های جاافتاده (۶ نقش)

| نقش | ناظر تعیین‌شده در §۶۵ |
|---|---|
| `Cloud Security Engineer` | Security Architect ،Cloud Architect ،CISO |
| `Database Security Specialist` | Security Architect ،Data Architect |
| `SOC Analyst` | CISO ،Security Governance Manager |
| `Incident Response Engineer` | Incident Manager ،CISO |
| `Vulnerability Management Specialist` | Security Governance Manager ،CISO |
| `Security Auditor` | Security Governance Manager ،CISO |

> بنابراین کل زنجیرهٔ امنیتی-حاکمیتی (§۶۴.۳) در فایل‌های Prompt غایب است؛ در حالی که §۶۵ صریحاً به این نقش‌ها ارجاع می‌دهد.

---

## ۲) نقش‌های اضافی (در `prompts/` موجودند، ولی در Role Registry Master نیستند)

### ناظرهای اضافی (۱۸ فایل در `prompts/audit/`)

| فایل | عنوان README | نکته |
|---|---|---|
| `ai-engineer-lead.md` | AI Engineer Lead | در Master فقط «AI Engineer» (مجری) داریم |
| `cao.md` | Chief Audit Officer (CAO) | اصلاً در Master نیست |
| `cio.md` | Chief Information Officer (CIO) | اصلاً در Master نیست |
| `chief-design-officer.md` | Chief Design Officer (CDO) | نه در ۶۴.۱، نه ۶۴.۳ |
| `chief-privacy-officer.md` | Chief Privacy Officer | فقط «Privacy / Compliance Officer» در Master است |
| `community-director.md` | Community Director | ثبت‌نشده در Master |
| `design-manager.md` | Design Manager | ثبت‌نشده |
| `development-manager.md` | Development Manager | Master فقط «Engineering Manager» دارد |
| `devops-manager.md` | DevOps Manager | ثبت‌نشده |
| `documentation-manager.md` | Documentation Manager | ثبت‌نشده |
| `embedded-systems-lead.md` | Embedded Systems Lead | ثبت‌نشده |
| `infrastructure-manager.md` | Infrastructure Manager | ثبت‌نشده |
| `localization-manager.md` | Localization Manager | ثبت‌نشده |
| `performance-engineering-lead.md` | Performance Engineering Lead | ثبت‌نشده |
| `procurement-manager.md` | Procurement Manager | در §۶۵ به‌عنوان ناظر Procurement Specialist آمده ولی در Registry نیست |
| `product-analyst-lead.md` | Product Analyst Lead | Master فقط «Product Analyst» (مجری) دارد ولی در §۶۵ به‌عنوان ناظر Data Analyst/BI Analyst استفاده می‌شود |
| `recruitment-manager.md` | Recruitment Manager | ثبت‌نشده |
| `support-manager.md` | Support Manager | ثبت‌نشده |

> `cto.md` و `ciso.md` در ظاهر «اضافی» به‌نظر می‌رسند ولی در واقع همان نقش‌های بخش ۶۴.۳ هستند (با عنوان کوتاه CTO/CISO به‌جای «CTO / Chief Technology Officer»). پس باید به‌عنوان «مطبق با نام» اصلاح شوند، نه حذف.

### مجری‌های اضافی (۶ فایل در `prompts/implementation/`)

| فایل | عنوان README |
|---|---|
| `agent-architect.md` | Agent Architect |
| `agent-evaluator.md` | Agent Evaluator |
| `agent-integration-engineer.md` | Agent Integration Engineer |
| `agent-safety-engineer.md` | Agent Safety Engineer |
| `agentic-prompt-specialist.md` | Agentic Prompt Specialist |
| `tool-developer.md` | Tool Developer |

> این ۶ نقش در Master ثبت نشده‌اند؛ یعنی یک «Agent/Tooling» خوشهٔ کامل در استاندارد غایب است (در حالی که فایل و ردیف README دارند).

### ناسازگاری منبع (READMEها) — خودش یک «اضافه/کسر» است

| منبع | ناظر | مجری | جمع |
|---|---|---|---|
| Master §۶۴ | ۵۶ | ۹۰ | ۱۴۶ |
| `README.md` (ریشه) | ۵۴ | ۹۰ | ۱۴۴ |
| `prompts/README.md` | ۶۵ (ادعا) | ۹۰ | ۱۵۵ |
| فایل‌های واقعی | ۶۸ | ۹۰ | ۱۵۸ |

- ۱۴ فایل `audit/` در `README.md` ریشه لینک ندارند (CIO, CAO, CISO, CDO, Chief Privacy Officer, Community Director, Design Manager, DevOps Manager, Documentation Manager, Embedded Systems Lead, Infrastructure Manager, Localization Manager, Performance Engineering Lead, Procurement Manager, Recruitment Manager, Support Manager).
- ۷ فایل در جدول ۶۵تایی `prompts/README.md` نیستند (AI Engineer Lead, CAO, CIO, CTO, CISO, CDO, Product Analyst Lead).
- یعنی حتی READMEهای خود مخزن با فایل‌ها هم‌سو نیستند.

---

## ۳) ساختار هر نقش چه تفاوتی با Master دارد؟

### ۳.۱ دو قالب متفاوت داخل خود `prompts/`

**قالب A (۱۴۸ فایل — خروجی `generate_role_prompts.py`):**

```
# سیستم پرامپت — ممیزی/اجرا «عنوان»
## ۱) Identity                    ← نقش/مأموریت/اختیار/دسترسی
## ۲) مسئولیت و مرز
##    مرز اختیار و مسئولیت (Authority & Boundaries)   ← پاراگراف ثابت
## ۳) ورودی‌ها و پیش‌شرط‌ها
## ۴) فرآیند ممیزی/اجرا (Structured Procedure)        ← STEP 1..N
## Decision Rules (قواعد تصمیم)
## ۵) ابزار
## ۶) Validation                   ← DoR / DoD / Quality Gates
## ۷) Evidence & Traceability
## ۸) خروجی و تحویل                ← خروجی‌ها / Handoff / Escalation
## ۹) Memory
## State Machine                   ← یک ماشین واحد برای هر دو نوع
## KPI / معیار عملکرد              ← بر اساس گروه (نه نقش)
[ناظر]  قواعد ممیزی / قواعد تحلیل کد و کدبیس / قالب هر یافته /
        تولید پلن اجرایی / خروجی نهایی ممیزی / Execution Result / معیارهای پذیرش
[مجری]  محورهای پیاده‌سازی / قواعد اجرا / قواعد تغییر کدبیس /
        اجرا مطابق پلن / Execution Result / معیارهای پذیرش
```

**قالب B (۱۰ فایل — کوتاه‌تر و متفاوت):**
`ai-engineer-lead.md`، `cao.md`، `cio.md`، `product-analyst-lead.md`، `agent-architect.md`، `agent-evaluator.md`، `agent-integration-engineer.md`، `agent-safety-engineer.md`، `agentic-prompt-specialist.md`، `tool-developer.md`

```
# سیستم پرامپت — ممیزی/اجرا «عنوان»
## ۱) Identity
## ۲) مسئولیت و مرز
## ۳) ورودی‌ها و پیش‌شرط‌ها
## ۴) فرآیند ... (Structured Procedure)     ← STEP بدون الگوی جامع
## ۵) ابزار
## ۶) Validation
## ۷) خروجی و تحویل
## Execution Result
```

مثال (CIO): فیلد `Status: APPROVED | NEEDS_REVISION | ESCALATED | BLOCKED` دارد که نه با DECISION_STATES ژنراتور هم‌خوان است و نه با Master. این ۱۰ فایل: فاقد Decision Rules، State Machine، KPI، Memory، Traceability، قواعد ناظر/مجری، Evidence Status و معیارهای پذیرش هستند.

### ۳.۲ مقایسه سکشن‌به‌سکشن با §۶۱ (۲۹ سکشن الزامی)

| # | سکشن Master | وضعیت در فایل‌ها | تفاوت اصلی |
|---|---|---|---|
| 1 | Identity | ⚠️ ناقص | فقط `نقش / مأموریت / اختیار / دسترسی`؛ فاقد `Role / Type / Domain / Category / Seniority / Purpose / Role_ID` |
| 2 | Mission | ❌ غایب | به‌صورت یک خط داخل Identity؛ فاقد `PrimaryGoal / ExpectedOutcome / SuccessDefinition / FailureDefinition` |
| 3 | Responsibilities | ⚠️ ناقص | بولت تخت؛ فاقد تقسیم `Primary / Secondary / Supporting / OutOfScope` |
| 4 | Type & Capability | ❌ غایب | نوع فقط در پرانتز؛ هیچ‌جا `SUPERVISOR / EXECUTOR / HYBRID` و لیست Capabilities نیست |
| 5 | Authority & Boundaries | ⚠️ ناقص | یک پاراگراف ثابت و عمومی؛ فاقد `AllowedDecisions / AllowedActions / ApprovalRequiredFor / ForbiddenDecisions / ForbiddenActions / CrossDomainRules / ProductionAuthority` |
| 6 | Stakeholders & Ownership | ❌ غایب | هیچ مالک/ناظر/داور/مصرف‌کننده‌ای تعریف نشده ⇒ قانون «هر Executor باید Supervisor معتبر داشته باشد» (§۸، §۶۵) عملاً در خود فایل‌ها تضمین نمی‌شود |
| 7 | Inputs | ⚠️ ناقص | فقط Required/Optional؛ فاقد `Generated / Prohibited` و ساختار `Name/Type/Source/Required/Validation/Freshness` |
| 8 | Preconditions | ⚠️ ناقص | یک خط؛ فاقد `Required/Optional/Blocking/Authorization/Environment/Access` و `How Verified` |
| 9 | Context | ⚠️ ناقص | یک خط؛ فاقد ۱۱ کلید `Project/Task/Domain/Architecture/Codebase/Runtime/Infrastructure/Security/Data/PreviousDecisions/OpenIssues/RelevantHistory` |
| 10 | Memory | ⚠️ ناقص | یک بولت؛ فاقد `Working/Persistent/Project/Role/Historical` و قاعده `Memory ≠ Evidence` |
| 11 | Scope | ❌ غایب | فقط رشتهٔ «اختیار» در Identity؛ فاقد `InScope/OutOfScope/AffectedAreas/FileScope/ModuleScope/ServiceScope/EnvironmentScope/ScopeExpansionPolicy` |
| 12 | Criteria / Requirements | ❌ غایب | سکشن مجزا ندارد (فقط Quality Gates عمومی + Acceptance در انتها)؛ فاقد ۱۱ بعد Criteria ناظر و ۱۱ بعد Requirements مجری |
| 13 | Procedure | ⚠️ ناقص | STEP دارد اما فیلد `ID/Name/Type/Objective/Inputs/Preconditions/Actions/Validation/Outputs/Evidence/DecisionPoints/ExitCriteria/FailureConditions/EscalationConditions` را طبق §۱۵ ندارد؛ نوع گام‌ها (`GENERIC`، `AUDIT`) خارج از لیست مجاز §۱۵ است؛ الگوی §۱۶/§۱۷ (RECEIVED→SCOPING→… و RECEIVED→UNDERSTANDING→…) اجرا نمی‌شود |
| 14 | Decision Rules | ⚠️ ناقص | فقط ۶ Status عمومی دارد؛ فاقد Decision Values ناظر (`APPROVE/REJECT/RECOMMEND/DEFER/ESCALATE`) و مجری (`PROCEED/PAUSE/RETRY/ROLLBACK/BLOCK/ESCALATE`)؛ به‌جایش بولت‌های آزاد از `details.md` |
| 15 | Tools & Environment | ⚠️ ناقص | فقط Allowed/Restricted؛ فاقد `Forbidden/ApprovalRequired/ReadOnly` و دسته‌های ابزار §۱۹ |
| 16 | Evidence & Verification | ⚠️ ناقص | فقط «شواهد لازم + زنجیره ردیابی»؛ فاقد `Evidence Status (VERIFIED/POTENTIAL/UNVERIFIED/MISSING)` و `Evidence Types` و `Generic Evidence Location` |
| 17 | Coverage / Completeness | ⚠️ ناقص | فقط برای ناظر به‌صورت prose؛ فاقد فرمول Coverage% و Completion Rule؛ برای مجری اصلاً ندارد |
| 18 | Findings / Changes | ⚠️ ناقص | قالب یافتهٔ ناظر نزدیک است اما `ROOT_FINDING_ID / AFFECTED` و Lifecycle §۳۲ را ندارد؛ مجری `Change Manifest / Modified Files / Created Files / Deleted Files` را به‌صورت سکشن مستقل ندارد (فقط توضیح prose) |
| 19 | Risk | ❌ غایب | هیچ سکشن Risk با `Likelihood/Impact/Score/Mitigation/Owner/ResidualRisk` در هیچ قالب وجود ندارد؛ فقط «Escalation Conditions» خطی |
| 20 | Recommendations / Implementation | ⚠️ ناقص | ناظر: فقط «اولویت اقدامات» در حکم نهایی؛ مجری: «محورهای پیاده‌سازی»؛ بدون ساختار `ID/RelatedFindings/Objective/ProposedChange/Priority/Dependencies/Owner/ExpectedOutcome/ValidationMethod` |
| 21 | Quality Gates | ⚠️ ناقص | گیت‌های عمومی و ثابت؛ نه ۱۳ گیت ناظر §۳۷ و نه ۱۳ گیت مجری §۳۸ |
| 22 | Traceability | ⚠️ ناقص | زنجیرهٔ `REQ→…→ACCEPT` هست ولی شناسه‌های `CRIT/RISK/FIND/REC/CHANGE` را ندارد |
| 23 | State Machine | ❌ نادرست | **یک** ماشین واحد `RECEIVED→ANALYZING→READY→IMPLEMENTING→INTEGRATING→TESTING→REVIEW_PENDING→CHANGES_REQUIRED→VERIFIED→COMPLETED + BLOCKED/ESCALATED/FAILED` برای **هر دو نوع**؛ ناظر هم IMPLEMENTING/TESTING دارد (خلاف اصل §۲ و §۱۶)؛ ماشین مجزای ناظر (§۴۲) و حالت `ROLLBACK_REQUIRED` ندارد |
| 24 | Handoff | ⚠️ ناقص | یک خط؛ فاقد `PrimaryRecipient/SupportingRecipients/DecisionOwner/ImplementationOwner/RequiredArtifacts/RequiredActions/AcceptanceCriteria/ExecutionPlan` |
| 25 | Escalation | ⚠️ ناقص | یک خط؛ فاقد `Trigger/Evidence/Impact/BlockedWork/DecisionRequired/TargetPersona/Urgency` و ۱۳ Trigger §۴۴ |
| 26 | Execution Plan | ⚠️ ناقص | ناظر: «تولید پلن + ذخیره در audits/» ✔؛ مجری: «اجرا و به‌روزرسانی پلن» ✔؛ اما پلن در خود Persona سکشن مستقل ندارد و به فایل `Execution Plan Generator.md` ارجاع می‌دهد که **در مخزن وجود ندارد**؛ پوشهٔ `audits/` هم وجود ندارد |
| 27 | Execution Result | ⚠️ ناقص | دو قالب متفاوت (ناظر/مجری) با فیلدهای پراکنده؛ با «Universal Format» §۵۶ یکسان نیست (مثلاً مجری `Verdict/Decomposition/Coverage` ندارد، ناظر `PlanStatus/Completed Steps` ندارد) |
| 28 | KPI | ⚠️ ناقص | KPI بر اساس **گروه** (۱۸ گروه) تولید می‌شود و ستون KPI خود `details.md` **دیده نمی‌شود** (`_kpi_list(group)` در ژنراتور)؛ پس KPI ویژهٔ نقش از بین می‌رود |
| 29 | Mandatory Rules | ⚠️ ناقص | «قواعد ممیزی/اجرا» و «قواعد کدبیس» دارد اما نه **۲۰ قاعدهٔ §۵۸**، نه **۱۵ قاعدهٔ §۵۹** و نه **۱۸ قاعدهٔ §۶۰** به‌صورت شماره‌دار و کامل |

### ۳.۳ سکشن‌های ویژهٔ ناظر (§۶۲ — MUST)

| سکشن الزامی | در فایل‌های audit |
|---|---|
| Audit Scope | ❌ ندارد |
| Audit Criteria | ❌ ندارد (فقط Acceptance در انتها) |
| Audit Procedure | ⚠️ به‌صورت «فرآیند ممیزی» ولی با الگوی STEP غیراستاندارد |
| Coverage Manifest | ⚠️ فقط داخل prose «خروجی نهایی ممیزی» |
| Decomposition Table | ⚠️ فقط داخل prose |
| Findings | ⚠️ فقط «قالب هر یافته» (بدون Lifecycle/Deduplication Complete) |
| Risk Assessment | ❌ ندارد |
| Recommendations | ❌ ندارد |
| Execution Plan | ⚠️ دارد (تولید پلن + audits/) |
| Final Verdict | ⚠️ فقط «حکم نهایی» داخل prose |

### ۳.۴ سکشن‌های ویژهٔ مجری (§۶۳ — MUST)

| سکشن الزامی | در فایل‌های implementation |
|---|---|
| Implementation Scope | ❌ ندارد |
| Implementation Requirements | ❌ ندارد |
| Implementation Procedure | ⚠️ دارد ولی غیراستاندارد |
| Change Manifest | ❌ به‌صورت سکشن مستقل ندارد (فقط توضیح در قواعد کدبیس) |
| Modified Files | ❌ ندارد (فقط داخل Execution Result) |
| Created Files | ❌ ندارد |
| Deleted Files | ❌ ندارد |
| Tests | ❌ ندارد |
| Verification | ❌ ندارد |
| Evidence | ⚠️ داخل «Evidence & Traceability» |
| Execution Plan Status | ⚠️ داخل «اجرا مطابق پلن» |
| Final Completion Status | ❌ ندارد |

### ۳.۵ سایر تفاوت‌های قراردادی

1. **قالب هدینگ‌ها:** Master می‌گوید `# Persona — <Role>` و `## 1. Identity` … `## 29. Mandatory Rules`؛ فایل‌ها هدینگ فارسی «# سیستم پرامپت — ممیزی/اجرا «…»» و شماره‌های ۱–۹ فارسی دارند و بقیهٔ هدینگ‌ها بدون شماره‌اند.
2. **نوع Persona:** Master سه مقدار `SUPERVISOR / EXECUTOR / HYBRID`؛ فایل‌ها `(ناظر) / (مجری)` و هیچ‌کدام HYBRID ندارند.
3. **منبع داده:** ژنراتور از `README.md` (۱۴۴ ردیف) + `details.md` (۲۳ ستون) می‌خواند؛ دادهٔ لازم برای `Type/Domain/Category/Seniority/Purpose/Role_ID` اصلاً در `details.md` وجود ندارد؛ `kpi` و `lifecycle` جزو داده هست ولی در قالب استفاده نمی‌شوند.
4. **SPECS:** فقط تعدادی نقش SPEC اختصاصی دارند؛ بقیه با `GROUP_OF → GROUP_SPEC` (۱۸ گروه) fallback می‌شوند — یعنی محتوای «مختص نقش» برای خیلی از نقش‌ها در واقع گروهی است.
5. **ROLE_SPECIAL_BLOCKS:** فقط `frontend-developer` (State Model) و `backend-developer` (Transaction/Security) بلاک ویژه دارند.
6. **State Machine واحد** برای ممیزی و اجرا ⇒ ناظرها هم مجبور به مسیر IMPLEMENTING/TESTING می‌شوند که با نقش Governance ناسازگار است.
7. **عدم وجود نظارت در فایل:** سکشن Stakeholders غایب است و هیچ فایلی نمی‌گوید «ناظر تو کیست»؛ بنابراین Orchestrator نمی‌تواند §۸/§۶۵ را از روی خود Persona اجرا کند.
8. ارجاع به `Execution Plan Generator.md` و پوشهٔ `audits/` که وجود ندارند (لینک شکسته).

---

## ۴) چطور همهٔ این تفاوت‌ها را برطرف کنیم

### ۴.۱ تصمیم پایه: Master مرجع است، نه فایل‌ها

Master را به‌عنوان «منبع حقیقت» نگه دار و Generator را با آن هم‌سو کن. گزینهٔ جایگزین (بازنویسی Master مطابق قالب فعلی) توصیه نمی‌شود، چون §۱–۶۸ دقیقاً همان قرارداد عملیاتی Orchestrator است و فایل‌ها فقط خروجی آن هستند.

### ۴.۲ گام‌های اجرایی پیشنهادی (مرتب)

**گام ۱ — دادهٔ Registry را در ژنراتور تثبیت کن**
- در `scripts/generate_role_prompts.py` یک ماژول دادهٔ `ROLE_REGISTRY` (انطباق §۶۴.۱–۶۴.۳) و `SUPERVISOR_MAP` (انطباق §۶۵) بساز: `{role_id, title, type, domain, category, seniority, supervisors}`.
- از `SPECS/GROUP_OF/GROUP_SPEC` به‌عنوان محتوای «role-specific» نگه دار، ولی انتخاب نقش/نوع/ناظر از Registry انجام شود، نه از ستون «نقش» README.

**گام ۲ — خروجی را با §۶۱ هم‌راستا کن (تغییر قالب ژنراتور)**
- عنوان فایل: `# Persona — <Role>`.
- ۲۹ سکشن با شمارهٔ انگلیسی دقیق §۶۱ (`## 1. Identity` … `## 29. Mandatory Rules`) تولید شود.
- برای ناظر، ۱۰ سکشن §۶۲ و برای مجری ۱۲ سکشن §۶۳ **به‌عنوان هدینگ مستقل** اضافه شود (نه فقط در prose).
- یک تابع `universal_block(section_no, role_data)` بساز تا تکه‌های مشترک (Evidence Status/Types، Risk، Traceability IDs، Handoff، Escalation، Execution Result، Mandatory Rules) یک‌بار تعریف و در همهٔ فایل‌ها رندر شوند.

**گام ۳ — شکاف‌های داده را پر کن**
- به `details.md` (یا registry) ستون‌های `Type (SUPERVISOR/EXECUTOR/HYBRID)`، `Domain`، `Category`، `Seniority`، `Purpose`، `Role_ID` اضافه کن.
- برای هر نقش، دادهٔ `Criteria/Requirements`، `Scope (In/Out/File/Module/Service/Environment + Expansion)`، `Stakeholders (از SUPERVISOR_MAP)`، `Risk`، `Findings/Changes` را به‌صورت ساخت‌یافته اضافه کن (می‌تواند در registry یا یک فایل `role_data/*.yaml`).
- KPI: به‌جای `_kpi_list(group)` از `persona['kpi']` استفاده کن و در نبود داده `Unknown` بنویس.

**گام ۴ — Procedure و State Machine را دوگانه کن**
- ناظر: گام‌ها طبق §۱۶ و ماشین §۴۲-nاظر؛ نوع گام فقط از §۱۵ (حذف `GENERIC`, افزودن `AUDIT/GOVERN/VERIFY/MONITOR/DOCUMENT`).
- مجری: گام‌ها طبق §۱۷ و ماشین §۴۲-مجری + `ROLLBACK_REQUIRED`.
- `_step_kind` را با لیست مجاز §۱۵ بازنویسی کن.

**گام ۵ — Decision Rules و Mandatory Rules را کامل کن**
- Common statuses + Decision Values ناظر/مجری §۱۸ را دقیق درج کن.
- لیست‌های شماره‌دار §۵۸ (۲۰)، §۵۹ (۱۵)، §۶۰ (۱۸) را به‌صورت ثابت در قالب قرار بده (با قواعد عام که در هر دو قالب وجود دارد ادغام کن).

**گام ۶ — ۱۲ نقش جاافتاده را اضافه کن**
- ردیف‌های §۶۴.۳ را به `README.md` و `prompts/README.md` و `details.md` و registry اضافه کن:
  - ناظر: `Architecture Review Board`, `Data Governance Manager`, `Security Governance Manager`, `Release Manager`, `Service Owner`, `Platform Owner`
  - مجری: `Cloud Security Engineer`, `Database Security Specialist`, `SOC Analyst`, `Incident Response Engineer`, `Vulnerability Management Specialist`, `Security Auditor`
- برای هر کدام SPEC اختصاصی بنویس (یا گروه در `GROUP_OF`).
- `CTO`/`CISO` را رسماً با نام کامل Master («CTO / Chief Technology Officer», «CISO / Chief Information Security Officer») عنون‌دهی کن.

**گام ۷ — ۲۴ نقش اضافی را تصمیم‌گیری کن**
- **پیشنهاد:** این نقش‌ها را به Master اضافه کن (آن‌ها در عمل مأموریت واقعی و Mapping دارند):
  - به §۶۴.۱/۶۴.۳ ناظر: `AI Engineer Lead`, `CAO`, `CIO`, `CDO`, `Chief Privacy Officer`, `Community Director`, `Design Manager`, `Development Manager`, `DevOps Manager`, `Documentation Manager`, `Embedded Systems Lead`, `Infrastructure Manager`, `Localization Manager`, `Performance Engineering Lead`, `Procurement Manager`, `Product Analyst Lead`, `Recruitment Manager`, `Support Manager`
  - به §۶۴.۲/۶۴.۳ مجری: `Agent Architect`, `Agent Evaluator`, `Agent Integration Engineer`, `Agent Safety Engineer`, `Agentic Prompt Specialist`, `Tool Developer`
- اگر برخی واقعاً اضافهٔ ناخواسته‌اند، فایل‌ها + ردیف READMEها را حذف/ادغام کن (مثلاً `Development Manager` → `Engineering Manager`).
- در هر دو حالت، مپینگ §۶۵ را هم‌زمان به‌روزرسانی کن.

**گام ۸ — ۱۰ فایل «قالب کوتاه» را با ژنراتور جدید بازتولید کن**
- `cio`, `cao`, `ai-engineer-lead`, `product-analyst-lead`, `agent-*`, `tool-developer` باید دقیقاً همان ساختار ۲۹+ویژه را بگیرند و Statusهای غیرمجاز (`APPROVED | NEEDS_REVISION | …`) حذف شوند.

**گام ۹ — ناسازگاری‌های داخلی Master را برطرف کن**
- نقش‌هایی که در §۶۵ ارجاع شده‌اند ولی در Registry نیستند را یا ثبت کن یا Map کن: `Infrastructure Owner`, `Performance Owner`, `Procurement Manager`, `Marketing Manager`, `Developer Relations Manager`, `DBA` (→ `Database Administrator (DBA)`).
- ۱۴ نقش ثبت‌شدهٔ مجری را که در §۶۵ به‌عنوان ناظر استفاده شده‌اند (System Architect, AI Engineer, SRE, Database Engineer, Infrastructure Engineer, Release Engineer, DevOps Engineer, Performance Engineer, Product Designer, Localization Specialist, UX Researcher, DevRel, Product Analyst, Disaster Recovery Specialist) را یا به ناظر ارتقا بده و در ۶۴.۱ ثبت کن، یا Mapping را به نقش ناظر نزدیک تغییر بده (مطابق «توجه» §۶۵).

**گام ۱۰ — مستندات و لینک‌ها را هم‌سو کن**
- فایل `Execution Plan Generator.md` (مرجع §۴۵–۵۲) را به مخزن اضافه کن، یا ارجاع فایل‌ها را به «Master Persona Schema & Generator Prompt.md» تغییر بده.
- پوشهٔ `audits/` را در ژنراتور create کن (الان `mkdir` هست؟ در `main()` هست ولی با `git` track نشده؛ با `.gitkeep` اضافه کن).
- آمار READMEها را با شمارش واقعی فایل‌ها یکی کن (بعد از گام ۶–۸): همهٔ فایل‌ها در README ریشه لینک شوند و جدول `prompts/README.md` با همان مجموعه برابر باشد.

**گام ۱۱ — Validation خودکار اضافه کن**
یک اسکریپت `scripts/validate_personas.py` (یا بخشی از همان ژنراتور) که بعد از تولید چک کند:
- [ ] هر فایل ۲۹ هدینگ §۶۱ را دارد و ترتیب درست است.
- [ ] ناظرها ۱۰ هدینگ §۶۲ و مجری‌ها ۱۲ هدینگ §۶۳ را دارند.
- [ ] هر Executor در `SUPERVISOR_MAP` ناظر معتبر (ثبت‌شده در Registry) دارد.
- [ ] هر ردیف README → فایل، و هر فایل → Registry (بدون یتیم).
- [ ] هیچ فایلی `State Machine` مجری را برای ناظر استفاده نکرده باشد.
- [ ] هیچ `Status/GENERIC` خارج از مقادیر مجاز وجود نداشته باشد.
- [ ] KPI هر نقش از دادهٔ همان نقش باشد (یا `Unknown`).
- [ ] `ExecutionPlan Generator.md` و `audits/` موجود باشند.

### ۴.۳ برآورد بازهٔ کار

| بخش | کار |
|---|---|
| گام ۱–۵ (قالب جدید) | بزرگ‌ترین بخش: ~۱ روز توسعهٔ ژنراتور + بازتولید ۱۵۸ فایل |
| گام ۶–۷ (Registry) | ~نیم روز (داده + SPECs) |
| گام ۸ (۱۰ فایل) | خودکار بعد از گام ۲–۴ |
| گام ۹–۱۱ | ~نیم روز (مستندات + validation) |

---

## پیوست: شمارش دقیق (برای بازتولیدپذیری)

- Master: 48 ناظر (۶۴.۱) + 84 مجری (۶۴.۲) + 8/6 تکمیلی (۶۴.۳) = **146**
- فایل‌ها: 68 audit + 90 implementation = **158**
- پوشش کامل: 48/48 ناظر ۶۴.۱ ✓ ، 84/84 مجری ۶۴.۲ ✓ ، 2/14 تکمیلی ✓ (CTO, CISO)
- Missing: 12/14 تکمیلی
- Extra: 18 audit + 6 implementation = **24**
- فایل‌های با قالب کوتاه: **10**

---

## ۵) وضعیت پس از اصلاح (2026-08-31)

✅ **انجام شد:**

1. **۱۲ نقش جاافتاده §۶۴.۳ اضافه شدند** (۶ ناظر: Architecture Review Board، Data Governance Manager، Security Governance Manager، Release Manager، Service Owner، Platform Owner — ۶ مجری: Cloud Security Engineer، Database Security Specialist، SOC Analyst، Incident Response Engineer، Vulnerability Management Specialist، Security Auditor). ردیف‌های README ریشه + `details.md` + SPEC تخصصی + Registry دریافت کردند.
2. **۱۴ ناظر موجود بدون ردیف** (CISO، Chief Privacy Officer، CDO، Community Director، Design Manager، DevOps Manager، Documentation Manager، Embedded Systems Lead، Infrastructure Manager، Localization Manager، Performance Engineering Lead، Procurement Manager، Recruitment Manager، Support Manager) به README و `details.md` اضافه و معتبر شدند.
3. **۱۰ نقش قبلی بدون دادهٔ تخصصی** (Development Manager، CTO، AI Engineer Lead، Product Analyst Lead، CIO، CAO و ۵ نقش Agent/Tool) ردیف‌های تخصصی `details.md` + SPEC دریافت کردند.
4. **همهٔ ۱۷۰ فایل با ساختار استاندارد بازتولید شدند:** `# Persona — <Role>` + «## 1. Identity … ## 29. Mandatory Rules» + ۱۰ هدینگ §۶۲ برای ناظر / ۱۲ هدینگ §۶۳ برای مجری؛ محتوای هر سکشن از دادهٔ همان نقش (`details.md` + SPEC مخصوص نقش) ساخته می‌شود.
5. **نقاط ضعف قبلی رفع شد:** Risk دارای سکشن کامل، Stakeholders & Ownership با ناظر واقعی (مطابق §۶۵ + نقش‌های Agent)، State Machine مجزا برای ناظر/مجری (§۴۲)، Decision Values ناظر/مجری (§۱۸)، KPI سرانهٔ نقش از `details.md`، Traceability کامل با ۱۱ شناسه، Mandatory Rules شماره‌دار §۵۸+§۵۹/§۶۰، Execution Plan با مسیر `audits/<slug>-execution-plan.md`، و حذف نوع گام `GENERIC`.
6. **ژنراتور جدید:** `scripts/generate_personas.py` (استاندارد-محور، با Registry/Mapping از خود فایل Master) + `scripts/role_extras.py` (۳۸ SPEC تخصصی + supervisor map) + `scripts/validate_personas.py` (چک ۲۹+۱۰/۱۲ سکشن، بدون orphan، ناظر معتبر برای هر مجری).
7. **README ریشه:** ۱۷۰ ردیف (۷۴ ناظر + ۹۶ مجری) — همهٔ فایل‌ها لینک دارند. **prompts/README:** جدول‌ها و آمار همگام شد (۷۴/۹۶/۱۷۰) + بخش‌های مپینگ Agent/امنیتی/انتشار اضافه شد.

**تعداد نهایی:** ۱۷۰ فایل = ۷۴ ممیزی + ۹۶ اجرا — `python3 scripts/validate_personas.py` → ALL CHECKS PASSED.

**باقی‌مانده (اختیاری):** ~~افزودن ۲۴ نقش «اضافی» به Master~~ ✅ **انجام شد.**

## ۶) تکمیل هم‌مرجع‌سازی + متادیتا و جستجوگر (2026-08-31)

1. **Master §۶۴.۳ به‌روزرسانی شد:** ۱۸ ناظر (CIO، CAO، Chief Privacy Officer، CDO، AI Engineer Lead، Product Analyst Lead، Development Manager، DevOps Manager، Infrastructure Manager، Support Manager، Community Director، Design Manager، Documentation Manager، Localization Manager، Performance Engineering Lead، Procurement Manager، Recruitment Manager، Embedded Systems Lead) و ۶ مجری Agent/Tooling (Agent Architect، Agent Integration Engineer، Tool Developer، Agent Evaluator، Agentic Prompt Specialist، Agent Safety Engineer) به ADDITIONAL_ROLES اضافه شدند؛ Registry Master اکنون **۷۴ ناظر + ۹۶ مجری = ۱۷۰ نقش** — دقیقاً برابر فایل‌های prompt.
2. **Master §۶۵ هم‌راستا شد:** نگاشت‌های Agent/Tooling اضافه شد؛ ارجاع‌های قبلی به نقش‌های مجری به‌عنوان ناظر با نقش‌های ثبت‌شده جایگزین شدند (AI Engineer → AI Engineer Lead، Product Analyst → Product Analyst Lead، Infrastructure Owner → Platform Owner، Performance Owner → Performance Engineering Lead، Marketing Manager → Product Marketing Manager، Developer Relations Manager → Community Director، DBA → Database Administrator (DBA)).
3. **متادیتای API-ready:** `personas.json` (تولید با `scripts/build_metadata.py`) — ۱۷۰ رکورد با `id/roleId/type/title/mission/duties/domain/category/seniority/supervisors/consumers/capabilities/path/keywords` + `facets` برای فیلتر و `totals`؛ قابل مصرف به‌عنوان API استاتیک.
4. **جستجوگر:** `index.html` — `personas.json` را با fetch می‌خواند؛ جستجوی فارسی/انگلیسی، فیلتر نوع/گروه/حوزه/دسته/سطح، مرتب‌سازی، کارت با لینک مستقیم فایل و GitHub؛ بدون وابستگی خارجی.
5. ژنراتور و اعتبارسنجی پس از تغییرات Master دوباره اجرا شدند: **170 فایل، ALL CHECKS PASSED**؛ خروجی persona بدون تغییر ماند (فقط Master، متادیتا و جستجوگر اضافه شدند).
