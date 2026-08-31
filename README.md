### AI Personas

> 🔍 **یافتن سریع Persona:** [`index.html`](index.html) را در مرورگر باز کن (یا `python3 -m http.server 8000` و سپس `http://localhost:8000/index.html`). این صفحه فایل [`personas.json`](personas.json) را می‌خواند و با جستجو/فیلتر (نوع، حوزه، دسته، سطح) فایل پرامپت هر نقش را نشان می‌دهد.
>
> 📦 **متادیتای API-ready:** [`personas.json`](personas.json) — بین ۱۷۰ نقش با فیلدهای `id`، `roleId`، `type`، `domain`، `category`، `seniority`، `mission`، `duties`، `supervisors`، `consumers`، `capabilities`، `path` و `facets` برای جستجو/دسته‌بندی. بازتولید: `python3 scripts/build_metadata.py`

| عنوان شغلی | توضیح وظایف | نقش (مجری/ناظر) | پرامپت |
|---|---|---|---|
| Founder / مؤسس | ایجاد ایده، تعیین جهت کلی کسب‌وکار و تصمیم‌های کلان | ناظر | [Audit](prompts/audit/founder.md) |
| Product Visionary | تعریف چشم‌انداز محصول و اینکه محصول قرار است چه مسئله‌ای را حل کند | ناظر | [Audit](prompts/audit/product-visionary.md) |
| Investor / سرمایه‌گذار | تأمین سرمایه و نظارت بر بازگشت سرمایه | ناظر | [Audit](prompts/audit/investor.md) |
| Board of Directors / هیئت‌مدیره | تصمیم‌گیری‌های استراتژیک و نظارت بر مدیریت پروژه/شرکت | ناظر | [Audit](prompts/audit/board-of-directors.md) |
| Project Sponsor | مالک حمایت مالی و سازمانی پروژه و رفع موانع کلان | ناظر | [Audit](prompts/audit/project-sponsor.md) |
| Business Analyst (BA) | استخراج نیازهای کسب‌وکار و تبدیل آن‌ها به نیازمندی‌های قابل اجرا | مجری | [Implementation](prompts/implementation/business-analyst-ba.md) |
| Domain Expert (SME) | ارائه دانش تخصصی حوزه‌ای که نرم‌افزار در آن استفاده می‌شود | ناظر | [Audit](prompts/audit/domain-expert-sme.md) |
| Product Manager (PM) | مدیریت محصول، اولویت‌بندی قابلیت‌ها و تصمیم‌گیری درباره Scope | ناظر | [Audit](prompts/audit/product-manager-pm.md) |
| Product Owner (PO) | مدیریت Product Backlog و تعیین اولویت نیازمندی‌ها | ناظر | [Audit](prompts/audit/product-owner-po.md) |
| Project Manager | مدیریت زمان، منابع، Scope، ریسک، هزینه و هماهنگی تیم | ناظر | [Audit](prompts/audit/project-manager.md) |
| Program Manager | مدیریت چند پروژه مرتبط با یکدیگر | ناظر | [Audit](prompts/audit/program-manager.md) |
| PMO | استانداردسازی و کنترل فرآیندهای مدیریت پروژه | ناظر | [Audit](prompts/audit/pmo.md) |
| Scrum Master | تسهیل فرآیند Agile/Scrum و رفع موانع تیم | ناظر | [Audit](prompts/audit/scrum-master.md) |
| Agile Coach | بهبود فرآیند Agile در سطح تیم یا سازمان | ناظر | [Audit](prompts/audit/agile-coach.md) |
| Technical Project Manager | مدیریت پروژه با تمرکز عمیق‌تر روی مسائل فنی | ناظر | [Audit](prompts/audit/technical-project-manager.md) |
| Solution Architect | طراحی راهکار کلان سیستم و انتخاب تکنولوژی‌ها | ناظر | [Audit](prompts/audit/solution-architect.md) |
| Software Architect | طراحی معماری نرم‌افزار، ماژول‌ها و ارتباطات آن‌ها | مجری | [Implementation](prompts/implementation/software-architect.md) |
| Enterprise Architect | هماهنگ‌کردن معماری نرم‌افزار با معماری کل سازمان | ناظر | [Audit](prompts/audit/enterprise-architect.md) |
| System Architect | طراحی معماری کل سیستم شامل نرم‌افزار، سخت‌افزار و زیرساخت | مجری | [Implementation](prompts/implementation/system-architect.md) |
| Technical Lead / Tech Lead | هدایت فنی تیم و تصمیم‌گیری درباره پیاده‌سازی | ناظر | [Audit](prompts/audit/technical-lead-tech-lead.md) |
| Development Manager | مدیریت تیم توسعه نرم‌افزار و منابع فنی | ناظر | [Audit](prompts/audit/development-manager.md) |
| Engineering Manager | مدیریت تیم مهندسی، افراد، ظرفیت و فرآیند توسعه | ناظر | [Audit](prompts/audit/engineering-manager.md) |
| Chief Technology Officer (CTO) | هدایت استراتژیک فناوری و تصمیم‌گیری‌های معماری کلان | ناظر | [Audit](prompts/audit/cto.md) |
| Staff Engineer | حل مسائل پیچیده فنی و هدایت معماری در مقیاس بزرگ | مجری | [Implementation](prompts/implementation/staff-engineer.md) |
| Principal Engineer | تصمیم‌گیری‌های فنی سطح سازمان و معماری‌های پیچیده | ناظر | [Audit](prompts/audit/principal-engineer.md) |
| Software Engineer | طراحی و پیاده‌سازی قابلیت‌های نرم‌افزار | مجری | [Implementation](prompts/implementation/software-engineer.md) |
| Backend Developer | توسعه API، Business Logic، سرویس‌ها و Backend | مجری | [Implementation](prompts/implementation/backend-developer.md) |
| Frontend Developer | توسعه رابط کاربری و منطق سمت Client | مجری | [Implementation](prompts/implementation/frontend-developer.md) |
| Full-Stack Developer | توسعه همزمان Frontend و Backend | مجری | [Implementation](prompts/implementation/full-stack-developer.md) |
| Mobile Developer | توسعه Android/iOS یا Cross-platform | مجری | [Implementation](prompts/implementation/mobile-developer.md) |
| Desktop Developer | توسعه نرم‌افزارهای Desktop | مجری | [Implementation](prompts/implementation/desktop-developer.md) |
| Game Developer | توسعه منطق، Gameplay و سیستم‌های بازی | مجری | [Implementation](prompts/implementation/game-developer.md) |
| Embedded Developer | توسعه نرم‌افزار برای دستگاه‌ها و سخت‌افزارهای Embedded | مجری | [Implementation](prompts/implementation/embedded-developer.md) |
| Firmware Engineer | توسعه Firmware و ارتباط مستقیم با سخت‌افزار | مجری | [Implementation](prompts/implementation/firmware-engineer.md) |
| IoT Engineer | توسعه سیستم‌های متصل به اینترنت و تجهیزات IoT | مجری | [Implementation](prompts/implementation/iot-engineer.md) |
| AI/ML Engineer | توسعه و Integration مدل‌های AI/ML | مجری | [Implementation](prompts/implementation/ai-ml-engineer.md) |
| Data Scientist | تحلیل داده و ساخت مدل‌های آماری/پیش‌بینی | مجری | [Implementation](prompts/implementation/data-scientist.md) |
| Data Engineer | ساخت Pipelineها و زیرساخت پردازش داده | مجری | [Implementation](prompts/implementation/data-engineer.md) |
| MLOps Engineer | Deployment، Monitoring و Lifecycle مدل‌های ML | مجری | [Implementation](prompts/implementation/mlops-engineer.md) |
| Prompt Engineer | طراحی Prompt و تعامل ساختاریافته با مدل‌های AI | مجری | [Implementation](prompts/implementation/prompt-engineer.md) |
| AI Engineer | طراحی سیستم‌های مبتنی بر LLM، Agent، RAG و AI Services | مجری | [Implementation](prompts/implementation/ai-engineer.md) |
| AI Engineer Lead | هدایت فنی تیم AI/Agent و Orchestration پروژه‌های Agent | ناظر | [Audit](prompts/audit/ai-engineer-lead.md) |
| Database Administrator (DBA) | مدیریت Database، Backup، Performance و Security | مجری | [Implementation](prompts/implementation/database-administrator-dba.md) |
| Database Engineer | طراحی Schema، Query، Index و معماری داده | مجری | [Implementation](prompts/implementation/database-engineer.md) |
| Data Architect | طراحی معماری کلان داده | ناظر | [Audit](prompts/audit/data-architect.md) |
| DevOps Engineer | CI/CD، Deployment، Automation و Infrastructure | مجری | [Implementation](prompts/implementation/devops-engineer.md) |
| SRE (Site Reliability Engineer) | تضمین Reliability، Availability و Performance سیستم | مجری | [Implementation](prompts/implementation/sre-site-reliability-engineer.md) |
| Cloud Engineer | طراحی و مدیریت زیرساخت Cloud | مجری | [Implementation](prompts/implementation/cloud-engineer.md) |
| Cloud Architect | طراحی معماری Cloud و انتخاب سرویس‌ها | ناظر | [Audit](prompts/audit/cloud-architect.md) |
| Infrastructure Engineer | مدیریت Server، Network، Storage و Infrastructure | مجری | [Implementation](prompts/implementation/infrastructure-engineer.md) |
| Network Engineer | طراحی و مدیریت Network | مجری | [Implementation](prompts/implementation/network-engineer.md) |
| System Administrator | مدیریت سیستم‌عامل‌ها، Serverها و سرویس‌های پایه | مجری | [Implementation](prompts/implementation/system-administrator.md) |
| Release Engineer | مدیریت فرآیند Build و Release نرم‌افزار | مجری | [Implementation](prompts/implementation/release-engineer.md) |
| Build Engineer | مدیریت Build، Package و Dependencyها | مجری | [Implementation](prompts/implementation/build-engineer.md) |
| QA Engineer | طراحی و اجرای تست‌های نرم‌افزار | مجری | [Implementation](prompts/implementation/qa-engineer.md) |
| QA Lead | مدیریت فرآیند و تیم QA | ناظر | [Audit](prompts/audit/qa-lead.md) |
| Test Engineer | اجرای تست‌های Functional و Technical | مجری | [Implementation](prompts/implementation/test-engineer.md) |
| Test Automation Engineer | ایجاد تست‌های خودکار | مجری | [Implementation](prompts/implementation/test-automation-engineer.md) |
| Performance Engineer | تست و بهینه‌سازی Performance | مجری | [Implementation](prompts/implementation/performance-engineer.md) |
| Load/Stress Tester | تست سیستم تحت Load و فشار بالا | مجری | [Implementation](prompts/implementation/load-stress-tester.md) |
| Security Engineer | پیاده‌سازی کنترل‌های امنیتی | مجری | [Implementation](prompts/implementation/security-engineer.md) |
| Application Security Engineer | بررسی امنیت خود Application | مجری | [Implementation](prompts/implementation/application-security-engineer.md) |
| Cybersecurity Engineer | حفاظت کلی سیستم‌ها و زیرساخت در برابر حملات | مجری | [Implementation](prompts/implementation/cybersecurity-engineer.md) |
| Penetration Tester | شناسایی آسیب‌پذیری با تست نفوذ مجاز | مجری | [Implementation](prompts/implementation/penetration-tester.md) |
| Security Architect | طراحی معماری امنیتی | ناظر | [Audit](prompts/audit/security-architect.md) |
| DevSecOps Engineer | ادغام Security در چرخه CI/CD | مجری | [Implementation](prompts/implementation/devsecops-engineer.md) |
| Privacy Engineer | طراحی سیستم مطابق الزامات Privacy و حفاظت داده | مجری | [Implementation](prompts/implementation/privacy-engineer.md) |
| UI Designer | طراحی ظاهر و اجزای رابط کاربری | مجری | [Implementation](prompts/implementation/ui-designer.md) |
| UX Designer | طراحی تجربه کاربر و جریان‌های تعامل | مجری | [Implementation](prompts/implementation/ux-designer.md) |
| Product Designer | ترکیب UX/UI و نیازهای محصول برای طراحی محصول | مجری | [Implementation](prompts/implementation/product-designer.md) |
| UX Researcher | تحقیق درباره رفتار و نیاز کاربران | مجری | [Implementation](prompts/implementation/ux-researcher.md) |
| UX Writer / Content Designer | طراحی متن‌ها و Microcopyهای داخل محصول | مجری | [Implementation](prompts/implementation/ux-writer-content-designer.md) |
| Design System Designer | ایجاد و نگهداری Design System | مجری | [Implementation](prompts/implementation/design-system-designer.md) |
| Graphic Designer | طراحی تصاویر، بنرها، Iconها و Assetهای گرافیکی | مجری | [Implementation](prompts/implementation/graphic-designer.md) |
| Motion Designer | طراحی Animation و Motion UI | مجری | [Implementation](prompts/implementation/motion-designer.md) |
| Accessibility Specialist | بررسی دسترسی‌پذیری محصول برای کاربران مختلف | مجری | [Implementation](prompts/implementation/accessibility-specialist.md) |
| Technical Writer | مستندسازی فنی، API، Installation و Developer Docs | مجری | [Implementation](prompts/implementation/technical-writer.md) |
| Documentation Specialist | تهیه مستندات کاربران و محصول | مجری | [Implementation](prompts/implementation/documentation-specialist.md) |
| Localization Specialist | ترجمه و بومی‌سازی محصول | مجری | [Implementation](prompts/implementation/localization-specialist.md) |
| Translator | ترجمه محتوا و مستندات | مجری | [Implementation](prompts/implementation/translator.md) |
| Legal Advisor | بررسی مسائل حقوقی پروژه و قراردادها | ناظر | [Audit](prompts/audit/legal-advisor.md) |
| IP / Copyright Specialist | مدیریت مالکیت فکری، License و Copyright | ناظر | [Audit](prompts/audit/ip-copyright-specialist.md) |
| Privacy / Compliance Officer | اطمینان از رعایت قوانین و مقررات | ناظر | [Audit](prompts/audit/privacy-compliance-officer.md) |
| Contract Manager | مدیریت قراردادها و تعهدات طرفین | ناظر | [Audit](prompts/audit/contract-manager.md) |
| Finance Manager | مدیریت بودجه، هزینه و مسائل مالی | ناظر | [Audit](prompts/audit/finance-manager.md) |
| Procurement Specialist | خرید سرویس، Hardware، Software و خدمات مورد نیاز | مجری | [Implementation](prompts/implementation/procurement-specialist.md) |
| HR / People Manager | جذب، مدیریت و توسعه نیروی انسانی | ناظر | [Audit](prompts/audit/hr-people-manager.md) |
| Recruiter | پیدا کردن و جذب اعضای تیم | مجری | [Implementation](prompts/implementation/recruiter.md) |
| Technical Recruiter | جذب نیروهای فنی | مجری | [Implementation](prompts/implementation/technical-recruiter.md) |
| Scrum Product Team | اجرای فرآیندهای توسعه Iterative | مجری | [Implementation](prompts/implementation/scrum-product-team.md) |
| UI/UX Research Participants | شرکت در تست و تحقیقات کاربری | مجری | [Implementation](prompts/implementation/ui-ux-research-participants.md) |
| Beta Tester | استفاده آزمایشی از محصول قبل از Release عمومی | مجری | [Implementation](prompts/implementation/beta-tester.md) |
| End User | استفاده واقعی از محصول و ارائه Feedback | مجری | [Implementation](prompts/implementation/end-user.md) |
| Customer Support Agent | پاسخ به مشکلات و درخواست‌های کاربران | مجری | [Implementation](prompts/implementation/customer-support-agent.md) |
| Technical Support Engineer | حل مشکلات فنی کاربران | مجری | [Implementation](prompts/implementation/technical-support-engineer.md) |
| Customer Success Manager | کمک به موفقیت مشتری در استفاده از محصول | ناظر | [Audit](prompts/audit/customer-success-manager.md) |
| Community Manager | مدیریت Community و ارتباط با کاربران | مجری | [Implementation](prompts/implementation/community-manager.md) |
| Product Marketing Manager | تعیین استراتژی بازاریابی محصول | ناظر | [Audit](prompts/audit/product-marketing-manager.md) |
| Marketing Specialist | اجرای کمپین‌ها و فعالیت‌های Marketing | مجری | [Implementation](prompts/implementation/marketing-specialist.md) |
| SEO Specialist | بهینه‌سازی محصول و محتوا برای Search Engine | مجری | [Implementation](prompts/implementation/seo-specialist.md) |
| ASO Specialist | بهینه‌سازی محصول برای App Storeها | مجری | [Implementation](prompts/implementation/aso-specialist.md) |
| Growth Manager | طراحی و اجرای استراتژی رشد محصول | ناظر | [Audit](prompts/audit/growth-manager.md) |
| Sales Manager | مدیریت فرآیند فروش | ناظر | [Audit](prompts/audit/sales-manager.md) |
| Sales Representative | فروش محصول/سرویس به مشتری | مجری | [Implementation](prompts/implementation/sales-representative.md) |
| Account Manager | مدیریت ارتباط با مشتریان کلیدی | ناظر | [Audit](prompts/audit/account-manager.md) |
| Business Development Manager | ایجاد Partnership و فرصت‌های تجاری | ناظر | [Audit](prompts/audit/business-development-manager.md) |
| Partnership Manager | مدیریت همکاری با شرکت‌ها و سرویس‌های دیگر | ناظر | [Audit](prompts/audit/partnership-manager.md) |
| Operations Manager | مدیریت عملیات جاری محصول پس از راه‌اندازی | ناظر | [Audit](prompts/audit/operations-manager.md) |
| DevRel | ارتباط با Developerها و جامعه فنی | مجری | [Implementation](prompts/implementation/devrel.md) |
| Technical Evangelist | معرفی تکنولوژی/محصول به جامعه فنی | مجری | [Implementation](prompts/implementation/technical-evangelist.md) |
| Incident Manager | مدیریت رخدادهای بحرانی Production | ناظر | [Audit](prompts/audit/incident-manager.md) |
| On-call Engineer | رسیدگی فوری به مشکلات Production | مجری | [Implementation](prompts/implementation/on-call-engineer.md) |
| Maintenance Engineer | نگهداری، Bug Fix و بهبود سیستم | مجری | [Implementation](prompts/implementation/maintenance-engineer.md) |
| Refactoring Engineer | بهبود ساختار و کیفیت کد موجود | مجری | [Implementation](prompts/implementation/refactoring-engineer.md) |
| Legacy Modernization Engineer | مهاجرت و نوسازی سیستم‌های قدیمی | مجری | [Implementation](prompts/implementation/legacy-modernization-engineer.md) |
| FinOps Specialist | کنترل و بهینه‌سازی هزینه زیرساخت Cloud | ناظر | [Audit](prompts/audit/finops-specialist.md) |
| Observability Engineer | Logging، Metrics، Tracing و Monitoring | مجری | [Implementation](prompts/implementation/observability-engineer.md) |
| Data Analyst | تحلیل رفتار کاربران و KPIهای محصول | مجری | [Implementation](prompts/implementation/data-analyst.md) |
| BI Analyst | ساخت گزارش‌ها و داشبوردهای مدیریتی | مجری | [Implementation](prompts/implementation/bi-analyst.md) |
| Product Analyst | تحلیل استفاده کاربران برای تصمیم‌های Product | مجری | [Implementation](prompts/implementation/product-analyst.md) |
| Product Analyst Lead | هدایت تیم تحلیل محصول و تصمیم‌گیری داده‌محور | ناظر | [Audit](prompts/audit/product-analyst-lead.md) |
| Risk Manager | شناسایی و مدیریت ریسک‌های پروژه | ناظر | [Audit](prompts/audit/risk-manager.md) |
| Change Manager | مدیریت تغییرات Scope، فرآیند و سازمان | ناظر | [Audit](prompts/audit/change-manager.md) |
| Quality Manager | کنترل کیفیت کل فرآیند تولید محصول | ناظر | [Audit](prompts/audit/quality-manager.md) |
| Audit Specialist | بررسی مستقل فرآیندها و خروجی‌ها | ناظر | [Audit](prompts/audit/audit-specialist.md) |
| External Auditor | ممیزی مستقل خارج از تیم | ناظر | [Audit](prompts/audit/external-auditor.md) |
| Vendor Manager | مدیریت شرکت‌ها و سرویس‌دهندگان خارجی | ناظر | [Audit](prompts/audit/vendor-manager.md) |
| Third-party Integration Specialist | Integration با سرویس‌ها و APIهای خارجی | مجری | [Implementation](prompts/implementation/third-party-integration-specialist.md) |
| Migration Specialist | انتقال داده و سیستم از محیط قبلی | مجری | [Implementation](prompts/implementation/migration-specialist.md) |
| Deployment Engineer | استقرار نسخه‌ها در محیط‌های مختلف | مجری | [Implementation](prompts/implementation/deployment-engineer.md) |
| Disaster Recovery Specialist | طراحی و تست بازیابی پس از Disaster | مجری | [Implementation](prompts/implementation/disaster-recovery-specialist.md) |
| Backup Administrator | مدیریت Backup و Restore | مجری | [Implementation](prompts/implementation/backup-administrator.md) |
| Business Continuity Manager | تضمین تداوم فعالیت کسب‌وکار | ناظر | [Audit](prompts/audit/business-continuity-manager.md) |
| Product Owner پس از Release | مدیریت Evolution محصول و Backlog آینده | ناظر | [Audit](prompts/audit/product-owner-release.md) |
| End-of-Life Manager | برنامه‌ریزی برای پایان عمر محصول | ناظر | [Audit](prompts/audit/end-of-life-manager.md) |
| Decommission Engineer | خاموش‌کردن امن سرویس‌ها و انتقال/حذف داده‌ها | مجری | [Implementation](prompts/implementation/decommission-engineer.md) |
| Agent Architect | طراحی معماری Agent، Orchestration و Workflow Management | مجری | [Implementation](prompts/implementation/agent-architect.md) |
| Agent Integration Engineer | پیاده‌سازی و Integration Agent‌ها در سیستم | مجری | [Implementation](prompts/implementation/agent-integration-engineer.md) |
| Tool Developer | ایجاد و maintenance Tools و API Wrapper برای Agent | مجری | [Implementation](prompts/implementation/tool-developer.md) |
| Agent Evaluator | بررسی رفتار Agent، Hallucination Detection و Safety Validation | مجری | [Implementation](prompts/implementation/agent-evaluator.md) |
| Agentic Prompt Specialist | طراحی Prompt مختص Agent و Few-Shot Examples | مجری | [Implementation](prompts/implementation/agentic-prompt-specialist.md) |
| Agent Safety Engineer | Implement Guardrail، Jailbreak Detection و Budget Control | مجری | [Implementation](prompts/implementation/agent-safety-engineer.md) |
| Chief Information Officer (CIO) | هدایت استراتژیک فناوری اطلاعات و IT Infrastructure | ناظر | [Audit](prompts/audit/cio.md) |
| Chief Audit Officer (CAO) | رهبری ممیزی و کنترل داخلی | ناظر | [Audit](prompts/audit/cao.md) |
| Chief Information Security Officer (CISO) | هدایت استراتژیک امنیت اطلاعات و حکمرانی امنیتی | ناظر | [Audit](prompts/audit/ciso.md) |
| Chief Privacy Officer | هدایت استراتژیک حریم خصوصی و انطباق داده | ناظر | [Audit](prompts/audit/chief-privacy-officer.md) |
| Chief Design Officer (CDO) | هدایت استراتژیک طراحی و تجربه کاربر | ناظر | [Audit](prompts/audit/chief-design-officer.md) |
| Community Director | هدایت استراتژیک جامعه و مشارکت اعضا | ناظر | [Audit](prompts/audit/community-director.md) |
| Design Manager | مدیریت تیم طراحی و کیفیت خروجی‌ها | ناظر | [Audit](prompts/audit/design-manager.md) |
| DevOps Manager | مدیریت تیم DevOps و فرایند تحویل | ناظر | [Audit](prompts/audit/devops-manager.md) |
| Documentation Manager | مدیریت تیم مستندسازی و کیفیت اسناد | ناظر | [Audit](prompts/audit/documentation-manager.md) |
| Embedded Systems Lead | هدایت تیم Embedded/IoT | ناظر | [Audit](prompts/audit/embedded-systems-lead.md) |
| Infrastructure Manager | مدیریت زیرساخت و عملیات | ناظر | [Audit](prompts/audit/infrastructure-manager.md) |
| Localization Manager | مدیریت تیم Localization و کیفیت ترجمه | ناظر | [Audit](prompts/audit/localization-manager.md) |
| Performance Engineering Lead | هدایت تیم بهینه‌سازی عملکرد | ناظر | [Audit](prompts/audit/performance-engineering-lead.md) |
| Procurement Manager | مدیریت خرید و تامین | ناظر | [Audit](prompts/audit/procurement-manager.md) |
| Recruitment Manager | مدیریت فرآیند جذب | ناظر | [Audit](prompts/audit/recruitment-manager.md) |
| Support Manager | مدیریت تیم پشتیبانی و رعایت SLA | ناظر | [Audit](prompts/audit/support-manager.md) |
| Architecture Review Board | بازبینی و تأیید تصمیم‌های معماری | ناظر | [Audit](prompts/audit/architecture-review-board.md) |
| Data Governance Manager | مدیریت حاکمیت داده | ناظر | [Audit](prompts/audit/data-governance-manager.md) |
| Security Governance Manager | مدیریت حاکمیت امنیت | ناظر | [Audit](prompts/audit/security-governance-manager.md) |
| Release Manager | مدیریت انتشار نسخه‌ها | ناظر | [Audit](prompts/audit/release-manager.md) |
| Service Owner | مالک سرویس | ناظر | [Audit](prompts/audit/service-owner.md) |
| Platform Owner | مالک پلتفرم | ناظر | [Audit](prompts/audit/platform-owner.md) |
| Cloud Security Engineer | امنیت سرویس‌های Cloud | مجری | [Implementation](prompts/implementation/cloud-security-engineer.md) |
| Database Security Specialist | امنیت پایگاه داده | مجری | [Implementation](prompts/implementation/database-security-specialist.md) |
| SOC Analyst | تحلیل و پاسخ اولیه به هشدارهای امنیتی | مجری | [Implementation](prompts/implementation/soc-analyst.md) |
| Incident Response Engineer | پاسخ به رخداد امنیتی | مجری | [Implementation](prompts/implementation/incident-response-engineer.md) |
| Vulnerability Management Specialist | مدیریت آسیب‌پذیری‌ها | مجری | [Implementation](prompts/implementation/vulnerability-management-specialist.md) |
| Security Auditor | ممیزی مستقل امنیت | مجری | [Implementation](prompts/implementation/security-auditor.md) |
