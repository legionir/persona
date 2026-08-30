# Prompt Files

این پوشه شامل پرامپت‌های نقش‌محور است که برای هر ردیف در [README](../README.md) تولید شده‌اند.

## ساختار

- `audit/` — پرامپت‌های ممیزی برای نقش‌های **ناظر**. هدف: ارزیابی شواهد‌محور کیفیت، کامل‌بودن و انطباق خروجیِ حوزه‌ی همان نقش.

> همه‌ی پرامپت‌های ناظر شامل بخش الزامی «قواعد تحلیل کد و کدبیس» هستند: ممنوعیت حدس و گمان، بررسی فایل‌به‌فایل و خط‌به‌خط، تحلیل دقیق ورکفلوها، مستندسازی کامل یافته‌ها (هر یافته با `FILE / LINE`)، و تقسیم پروژه‌های بزرگ به بخش‌های کوچک‌ترِ قابل بررسی بدون از قلم انداختن هیچ فایل یا کدی (از طریق Coverage Manifest و Decomposition Table).
- `implementation/` — پرامپت‌های راهنمای پیاده‌سازی برای نقش‌های **مجری**. هدف: تبدیل تسک به یک پلن اجرایی دقیق، فاز‌به‌فاز، وابستگی‌آگاه و دارای معیار پذیرش.

## نام‌گذاری

هر فایل با اسلاگ (slug) انگلیسیِ عنوانِ شغلی نام‌گذاری شده است؛ مثلاً:
`prompts/audit/founder.md` یا `prompts/implementation/backend-developer.md`.

## Regeneration

پرامپت‌ها از جدول `README.md` و با قالب‌های موجود در `scripts/generate_role_prompts.py` تولید می‌شوند. برای بازتولید:

```bash
python3 scripts/generate_role_prompts.py
```

این اسکریپت هم فایل‌های پرامپت را بازنویسی می‌کند و هم ستون `پرامپت` و لینک‌های README را به‌روز نگه می‌دارد.

---

# جدول دسته‌بندی کامل نقش‌ها (با ناظرهای کامل)

## فهرست مطالب
- [دسته‌بندی بر اساس نقش](#دسته‌بندی-بر-اساس-نقش)
  - [ناظرها](#ناظرها)
  - [مجری‌ها](#مجری‌ها)
- [دسته‌بندی بر اساس حوزه](#دسته‌بندی-بر-اساس-حوزه)
- [مپینگ ناظر-مجری](#مپینگ-ناظر-مجری)
- [آمار و خلاصه](#آمار-و-خلاصه)

---

## دسته‌بندی بر اساس نقش

### ناظرها (65 نقش)

| عنوان شغلی | حوزه اصلی | حوزه فرعی | توضیح مختصر |
|---|---|---|---|
| Founder / مؤسس | مدیریت و استراتژی | کسب‌وکار | ایجاد ایده، تعیین جهت کلی کسب‌وکار |
| Product Visionary | محصول | استراتژی | تعریف چشم‌انداز محصول |
| Investor / سرمایه‌گذار | مالی و تجاری | سرمایه‌گذاری | تأمین سرمایه و نظارت بر بازگشت سرمایه |
| Board of Directors / هیئت‌مدیره | مدیریت و استراتژی | Governance | تصمیم‌گیری‌های استراتژیک و نظارت |
| Project Sponsor | مدیریت و استراتژی | مالی | حمایت مالی و سازمانی |
| Domain Expert (SME) | تحقیق و آنالیز | تخصصی | ارائه دانش تخصصی حوزه |
| Product Manager (PM) | محصول | مدیریت | مدیریت محصول و اولویت‌بندی |
| Product Owner (PO) | محصول | Backlog | مدیریت Product Backlog |
| Project Manager | مدیریت و استراتژی | پروژه | مدیریت زمان، منابع، Scope، ریسک |
| Program Manager | مدیریت و استراتژی | برنامه | مدیریت چند پروژه مرتبط |
| PMO | مدیریت و استراتژی | فرآیند | استانداردسازی فرآیند مدیریت پروژه |
| Scrum Master | مدیریت و استراتژی | Agile | تسهیل Agile/Scrum |
| Agile Coach | مدیریت و استراتژی | Agile | بهبود فرآیند Agile |
| Technical Project Manager | مدیریت و استراتژی | فنی | مدیریت پروژه با تمرکز فنی |
| Solution Architect | معماری نرم‌افزاری | راهکار | طراحی راهکار کلان سیستم |
| Enterprise Architect | معماری نرم‌افزاری | سازمانی | هماهنگی معماری با سازمان |
| Technical Lead / Tech Lead | توسعه نرم‌افزار | رهبری | هدایت فنی تیم |
| **Development Manager** | توسعه نرم‌افزار | مدیریت | مدیریت تیم توسعه نرم‌افزار |
| **Engineering Manager** | مدیریت و استراتژی | مهندسی | مدیریت تیم مهندسی |
| **Chief Technology Officer (CTO)** | معماری نرم‌افزاری | استراتژیک | هدایت استراتژیک فناوری |
| Principal Engineer | معماری نرم‌افزاری | استراتژیک | هدایت فنی در سطح سازمان |
| Data Architect | معماری نرم‌افزاری | داده | طراحی معماری کلان داده |
| Cloud Architect | ابری | معماری | طراحی معماری Cloud |
| Security Architect | امنیتی | معماری | طراحی و بررسی معماری امنیتی |
| **Chief Information Security Officer (CISO)** | امنیتی | استراتژیک | هدایت استراتژیک امنیت |
| QA Lead | کیفیت و تست | مدیریت | مدیریت تیم و فرآیند QA |
| **Quality Manager** | کیفیت و تست | مدیریت | کنترل کیفیت کل فرآیند |
| **Performance Engineering Lead** | کیفیت و تست | Performance | هدایت تیم بهینه‌سازی عملکرد |
| Legal Advisor | حقوقی و انطباق | حقوقی | بررسی مسائل حقوقی |
| IP / Copyright Specialist | حقوقی و انطباق | مالکیت فکری | مدیریت مالکیت فکری |
| Privacy / Compliance Officer | حقوقی و انطباق | حریم خصوصی | تطابق با قوانین و مقررات |
| **Chief Privacy Officer** | حقوقی و انطباق | حریم خصوصی | هدایت استراتژیک حریم خصوصی |
| Contract Manager | حقوقی و انطباق | قراردادها | مدیریت قراردادها |
| Finance Manager | مالی و تجاری | بودجه | مدیریت بودجه و هزینه |
| **Procurement Manager** | مالی و تجاری | خرید | مدیریت خرید و تامین |
| HR / People Manager | منابع انسانی | مدیریت | مدیریت نیروی انسانی |
| **Recruitment Manager** | منابع انسانی | جذب | مدیریت فرآیند جذب |
| Customer Success Manager | بازاریابی و فروش | موفقیت مشتری | موفقیت مشتری در استفاده از محصول |
| Product Marketing Manager | بازاریابی و فروش | محصول | استراتژی بازاریابی محصول |
| Growth Manager | بازاریابی و فروش | رشد | طراحی استراتژی رشد |
| Sales Manager | بازاریابی و فروش | فروش | مدیریت فروش |
| Account Manager | بازاریابی و فروش | مشتریان | مدیریت مشتریان کلیدی |
| Business Development Manager | بازاریابی و فروش | توسعه کسب‌وکار | ایجاد فرصت‌های تجاری |
| Partnership Manager | بازاریابی و فروش | شراکت | مدیریت همکاری با شرکت‌ها |
| Operations Manager | عملیاتی و زیرساخت | عملیات | حفظ Operational Continuity |
| **Infrastructure Manager** | عملیاتی و زیرساخت | مدیریت | مدیریت زیرساخت و عملیات |
| **DevOps Manager** | DevOps و SRE | مدیریت | مدیریت تیم DevOps |
| Incident Manager | Incident و Disaster Recovery | مدیریت | مدیریت رخدادهای بحرانی |
| FinOps Specialist | ابری | مالی | کنترل هزینه Cloud |
| Business Continuity Manager | Incident و Disaster Recovery | تداوم کسب‌وکار | تضمین تداوم کسب‌وکار |
| Product Owner پس از Release | محصول | Post-Release | مدیریت Evolution محصول |
| End-of-Life Manager | محصول | پایان عمر | مدیریت امن Product Retirement |
| Risk Manager | مدیریت و استراتژی | ریسک | شناسایی و مدیریت ریسک |
| Change Manager | مدیریت و استراتژی | تغییرات | مدیریت تغییرات Scope |
| Audit Specialist | حقوقی و انطباق | ممیزی | بررسی مستقل فرآیندها |
| External Auditor | حقوقی و انطباق | ممیزی خارجی | ممیزی مستقل خارج از تیم |
| Vendor Manager | مالی و تجاری | وندورها | مدیریت Vendorها |
| **Support Manager** | پشتیبانی مشتری | مدیریت | مدیریت تیم پشتیبانی |
| **Community Director** | بازاریابی و فروش | جامعه | هدایت استراتژیک جامعه |
| **Design Manager** | طراحی و تجربه کاربری | مدیریت | مدیریت تیم طراحی |
| **Chief Design Officer (CDO)** | طراحی و تجربه کاربری | استراتژیک | هدایت استراتژیک طراحی |
| **Documentation Manager** | مستندسازی | مدیریت | مدیریت تیم مستندسازی |
| **Localization Manager** | Localization و ترجمه | مدیریت | مدیریت تیم Localization |
| **Embedded Systems Lead** | سخت‌افزار و Embedded | رهبری | هدایت تیم Embedded/IoT |

---

### مجری‌ها (90 نقش)

| عنوان شغلی | حوزه اصلی | حوزه فرعی | توضیح مختصر | ناظر مربوطه |
|---|---|---|---|---|
| Business Analyst (BA) | تحقیق و آنالیز | کسب‌وکار | استخراج نیازهای کسب‌وکار | Product Manager |
| Software Architect | معماری نرم‌افزاری | نرم‌افزار | طراحی ساختار داخلی نرم‌افزار | CTO / Technical Lead |
| System Architect | معماری نرم‌افزاری | سیستم | طراحی معماری کل سیستم | Enterprise Architect |
| Staff Engineer | توسعه نرم‌افزار | تخصصی | حل مسائل پیچیده فنی | Principal Engineer |
| Software Engineer | توسعه نرم‌افزار | عمومی | طراحی و پیاده‌سازی قابلیت‌ها | Development Manager |
| Backend Developer | توسعه نرم‌افزار | Backend | توسعه API و Backend | Development Manager |
| Frontend Developer | توسعه نرم‌افزار | Frontend | توسعه رابط کاربری | Development Manager |
| Full-Stack Developer | توسعه نرم‌افزار | Full-Stack | تحویل End-to-End قابلیت | Development Manager |
| Mobile Developer | توسعه نرم‌افزار | موبایل | توسعه Mobile Application | Development Manager |
| Desktop Developer | توسعه نرم‌افزار | دسکتاپ | توسعه Desktop Application | Development Manager |
| Game Developer | توسعه بازی | توسعه | تولید Gameplay و Game Systems | Development Manager |
| Embedded Developer | سخت‌افزار و Embedded | نرم‌افزار | اجرای منطق دستگاه | Embedded Systems Lead |
| Firmware Engineer | سخت‌افزار و Embedded | Firmware | کنترل Hardware از طریق Firmware | Embedded Systems Lead |
| IoT Engineer | سخت‌افزار و Embedded | IoT | اتصال Device به Platform | Embedded Systems Lead |
| AI/ML Engineer | داده و هوش مصنوعی | مهندسی | توسعه مدل‌های AI/ML | Principal Engineer |
| Data Scientist | داده و هوش مصنوعی | علم داده | تحلیل داده و ساخت مدل | Data Architect |
| Data Engineer | داده و هوش مصنوعی | مهندسی داده | ساخت Data Pipeline | Data Architect |
| MLOps Engineer | داده و هوش مصنوعی | عملیات ML | Deployment و Lifecycle مدل ML | Principal Engineer |
| Prompt Engineer | داده و هوش مصنوعی | Prompt | بهینه‌سازی رفتار مدل | AI Engineer Lead |
| AI Engineer | داده و هوش مصنوعی | مهندسی AI | طراحی LLM، Agent، RAG | Principal Engineer |
| Database Administrator (DBA) | پایگاه داده | مدیریت | Availability و Integrity دیتابیس | Data Architect |
| Database Engineer | پایگاه داده | مهندسی | طراحی Schema و Query | Data Architect |
| DevOps Engineer | DevOps و SRE | DevOps | Automate Delivery | DevOps Manager |
| SRE (Site Reliability Engineer) | DevOps و SRE | SRE | تضمین Reliability و Availability | DevOps Manager |
| Cloud Engineer | ابری | مهندسی | مدیریت Cloud Infrastructure | Cloud Architect |
| Infrastructure Engineer | عملیاتی و زیرساخت | زیرساخت | تأمین Infrastructure پایدار | Infrastructure Manager |
| Network Engineer | شبکه | مهندسی | طراحی و مدیریت Network | Infrastructure Manager |
| System Administrator | عملیاتی و زیرساخت | مدیریت سیستم | سلامت سیستم‌های پایه | Infrastructure Manager |
| Release Engineer | DevOps و SRE | Release | انتشار کنترل‌شده نرم‌افزار | DevOps Manager |
| Build Engineer | DevOps و SRE | Build | تولید Artifact قابل انتشار | DevOps Manager |
| QA Engineer | کیفیت و تست | مهندسی | طراحی و اجرای تست نرم‌افزار | QA Lead |
| Test Engineer | کیفیت و تست | اجرای تست | کشف Defect | QA Lead |
| Test Automation Engineer | کیفیت و تست | خودکارسازی | ایجاد تست‌های خودکار | QA Lead |
| Performance Engineer | کیفیت و تست | Performance | تست و بهینه‌سازی Performance | Performance Engineering Lead |
| Load/Stress Tester | کیفیت و تست | بار و استرس | تست سیستم تحت فشار | Performance Engineering Lead |
| Security Engineer | امنیتی | مهندسی | پیاده‌سازی کنترل‌های امنیتی | CISO |
| Application Security Engineer | امنیتی | Application | بررسی امنیت Application | CISO |
| Cybersecurity Engineer | امنیتی | کلی | حفاظت کلی سیستم و زیرساخت | CISO |
| Penetration Tester | امنیتی | تست نفوذ | تست نفوذ مجاز | CISO |
| DevSecOps Engineer | امنیتی | DevSecOps | ادغام Security در CI/CD | CISO |
| Privacy Engineer | حقوقی و انطباق | حریم خصوصی | طراحی Privacy و حفاظت داده | Chief Privacy Officer |
| UI Designer | طراحی و تجربه کاربری | UI | ایجاد UI قابل استفاده و Consistent | Design Manager |
| UX Designer | طراحی و تجربه کاربری | UX | ایجاد User Experience مناسب | Design Manager |
| Product Designer | طراحی و تجربه کاربری | محصول | ترکیب UX/UI و Product Needs | Design Manager |
| UX Researcher | تحقیق و آنالیز | UX | تحقیق درباره رفتار کاربران | Design Manager |
| UX Writer / Content Designer | طراحی و تجربه کاربری | محتوا | ایجاد Clear Product Communication | Design Manager |
| Design System Designer | طراحی و تجربه کاربری | Design System | ایجاد و نگهداری Design System | Design Manager |
| Graphic Designer | طراحی و تجربه کاربری | گرافیک | ایجاد Visual Assets | Design Manager |
| Motion Designer | طراحی و تجربه کاربری | Motion | بهبود Interaction Feedback | Design Manager |
| Accessibility Specialist | طراحی و تجربه کاربری | دسترسی‌پذیری | بررسی Accessibility | Design Manager |
| Technical Writer | مستندسازی | فنی | انتقال دانش فنی | Documentation Manager |
| Documentation Specialist | مستندسازی | کاربر | قابل‌فهم کردن Product | Documentation Manager |
| Localization Specialist | Localization و ترجمه | Localization | تطبیق محصول با بازار هدف | Localization Manager |
| Translator | Localization و ترجمه | ترجمه | ترجمه دقیق و طبیعی | Localization Manager |
| Procurement Specialist | مالی و تجاری | خرید | تأمین منابع موردنیاز | Procurement Manager |
| Recruiter | منابع انسانی | جذب | تأمین نیروی موردنیاز | Recruitment Manager |
| Technical Recruiter | منابع انسانی | جذب فنی | جذب Technical Talent | Recruitment Manager |
| Scrum Product Team | توسعه نرم‌افزار | تیم | اجرای توسعه Iterative | Product Owner |
| UI/UX Research Participants | تحقیق و آنالیز | کاربری | ارائه User Feedback | UX Researcher |
| Beta Tester | کیفیت و تست | Beta | کشف مشکلات قبل از Release | QA Lead |
| End User | تحقیق و آنالیز | کاربر نهایی | ایجاد Signal واقعی از Product Usage | Product Manager |
| Customer Support Agent | پشتیبانی مشتری | عمومی | حل User Issues | Support Manager |
| Technical Support Engineer | پشتیبانی مشتری | فنی | رفع Technical Issues | Support Manager |
| Community Manager | بازاریابی و فروش | جامعه | ایجاد تعامل سالم با کاربران | Community Director |
| Marketing Specialist | بازاریابی و فروش | کمپین | جذب و فعال‌سازی کاربران | Product Marketing Manager |
| SEO Specialist | بازاریابی و فروش | SEO | افزایش Organic Acquisition | Product Marketing Manager |
| ASO Specialist | بازاریابی و فروش | ASO | افزایش App Discovery | Product Marketing Manager |
| Sales Representative | بازاریابی و فروش | نمایندگی | تبدیل Lead به Customer | Sales Manager |
| DevRel | بازاریابی و فروش | Developer Relations | رشد Developer Ecosystem | Community Director |
| Technical Evangelist | بازاریابی و فروش | تکنولوژی | افزایش Technical Adoption | Community Director |
| On-call Engineer | Incident و Disaster Recovery | On-call | رسیدگی فوری به Production | Incident Manager |
| Maintenance Engineer | عملیاتی و زیرساخت | نگهداری | حفظ سلامت سیستم | Infrastructure Manager |
| Refactoring Engineer | توسعه نرم‌افزار | Refactoring | بهبود ساختار کد | Technical Lead |
| Legacy Modernization Engineer | Migration و Modernization | Legacy | کاهش Legacy Risk | Principal Engineer |
| Observability Engineer | DevOps و SRE | Observability | Logging، Metrics، Tracing و Monitoring | DevOps Manager |
| Data Analyst | تحقیق و آنالیز | داده | تحلیل رفتار کاربران و KPIها | Product Analyst Lead |
| BI Analyst | تحقیق و آنالیز | BI | ساخت گزارش و Dashboard مدیریتی | Product Analyst Lead |
| Product Analyst | تحقیق و آنالیز | محصول | کمک به Product Decisions | Product Manager |
| Third-party Integration Specialist | Integration و Third-Party | API | اتصال پایدار سرویس‌ها | Technical Lead |
| Migration Specialist | Migration و Modernization | Migration | انتقال داده و سیستم | Technical Lead |
| Deployment Engineer | DevOps و SRE | Deployment | استقرار نسخه‌ها | DevOps Manager |
| Disaster Recovery Specialist | Incident و Disaster Recovery | DR | طراحی و تست بازیابی | Business Continuity Manager |
| Backup Administrator | Incident و Disaster Recovery | Backup | مدیریت Backup و Restore | Infrastructure Manager |
| Decommission Engineer | Migration و Modernization | Decommission | خاموش‌کردن امن سرویس‌ها | Infrastructure Manager |

---

## دسته‌بندی بر اساس حوزه

### مدیریت و استراتژی (18 ناظر)

| عنوان شغلی | نقش | ناظر مربوطه |
|---|---|---|
| Founder / مؤس | ناظر | - |
| Board of Directors / هیئت‌مدیره | ناظر | - |
| Project Sponsor | ناظر | - |
| Project Manager | ناظر | - |
| Program Manager | ناظر | - |
| PMO | ناظر | - |
| Scrum Master | ناظر | - |
| Agile Coach | ناظر | - |
| Technical Project Manager | ناظر | - |
| Engineering Manager | ناظر | - |
| Development Manager | ناظر | - |
| Risk Manager | ناظر | - |
| Change Manager | ناظر | - |
| Quality Manager | ناظر | - |
| Operations Manager | ناظر | - |
| Incident Manager | ناظر | - |
| Business Continuity Manager | ناظر | - |

---

### محصول (10 ناظر + 5 مجری = 15)

| عنوان شغلی | نقش | ناظر مربوطه |
|---|---|---|
| Product Visionary | ناظر | - |
| Product Manager (PM) | ناظر | - |
| Product Owner (PO) | ناظر | - |
| Customer Success Manager | ناظر | - |
| Product Marketing Manager | ناظر | - |
| Growth Manager | ناظر | - |
| Product Owner پس از Release | ناظر | - |
| End-of-Life Manager | ناظر | - |
| Business Analyst (BA) | مجری | Product Manager |
| Product Designer | مجری | Design Manager |
| Product Analyst | مجری | Product Manager |
| Scrum Product Team | مجری | Product Owner |
| End User | مجری | Product Manager |

---

### معماری نرم‌افزاری (9 ناظر + 2 مجری = 11)

| عنوان شغلی | نقش | ناظر مربوطه |
|---|---|---|
| Solution Architect | ناظر | - |
| Enterprise Architect | ناظر | - |
| CTO | ناظر | - |
| Principal Engineer | ناظر | - |
| Technical Lead / Tech Lead | ناظر | - |
| Data Architect | ناظر | - |
| Cloud Architect | ناظر | - |
| Security Architect | ناظر | - |
| CISO | ناظر | - |
| Software Architect | مجری | CTO / Technical Lead |
| System Architect | مجری | Enterprise Architect |

---

### توسعه نرم‌افزار (1 ناظر + 15 مجری = 16)

| عنوان شغلی | نقش | ناظر مربوطه |
|---|---|---|
| Development Manager | ناظر | - |
| Software Engineer | مجری | Development Manager |
| Backend Developer | مجری | Development Manager |
| Frontend Developer | مجری | Development Manager |
| Full-Stack Developer | مجری | Development Manager |
| Mobile Developer | مجری | Development Manager |
| Desktop Developer | مجری | Development Manager |
| Game Developer | مجری | Development Manager |
| Staff Engineer | مجری | Principal Engineer |
| Refactoring Engineer | مجری | Technical Lead |
| Legacy Modernization Engineer | مجری | Principal Engineer |
| Third-party Integration Specialist | مجری | Technical Lead |
| Migration Specialist | مجری | Technical Lead |

---

### داده و هوش مصنوعی (2 ناظر + 6 مجری = 8)

| عنوان شغلی | نقش | ناظر مربوطه |
|---|---|---|
| Data Architect | ناظر | - |
| Principal Engineer | ناظر | - |
| AI/ML Engineer | مجری | Principal Engineer |
| Data Scientist | مجری | Data Architect |
| Data Engineer | مجری | Data Architect |
| MLOps Engineer | مجری | Principal Engineer |
| Prompt Engineer | مجری | AI Engineer Lead |
| AI Engineer | مجری | Principal Engineer |

---

### امنیتی (2 ناظر + 6 مجری = 8)

| عنوان شغلی | نقش | ناظر مربوطه |
|---|---|---|
| CISO | ناظر | - |
| Security Architect | ناظر | - |
| Security Engineer | مجری | CISO |
| Application Security Engineer | مجری | CISO |
| Cybersecurity Engineer | مجری | CISO |
| Penetration Tester | مجری | CISO |
| DevSecOps Engineer | مجری | CISO |
| Privacy Engineer | مجری | Chief Privacy Officer |

---

### کیفیت و تست (3 ناظر + 7 مجری = 10)

| عنوان شغلی | نقش | ناظر مربوطه |
|---|---|---|
| QA Lead | ناظر | - |
| Quality Manager | ناظر | - |
| Performance Engineering Lead | ناظر | - |
| QA Engineer | مجری | QA Lead |
| Test Engineer | مجری | QA Lead |
| Test Automation Engineer | مجری | QA Lead |
| Performance Engineer | مجری | Performance Engineering Lead |
| Load/Stress Tester | مجری | Performance Engineering Lead |
| Beta Tester | مجری | QA Lead |

---

### طراحی و تجربه کاربری (2 ناظر + 10 مجری = 12)

| عنوان شغلی | نقش | ناظر مربوطه |
|---|---|---|
| Design Manager | ناظر | - |
| Chief Design Officer (CDO) | ناظر | - |
| UI Designer | مجری | Design Manager |
| UX Designer | مجری | Design Manager |
| Product Designer | مجری | Design Manager |
| UX Researcher | مجری | Design Manager |
| UX Writer / Content Designer | مجری | Design Manager |
| Design System Designer | مجری | Design Manager |
| Graphic Designer | مجری | Design Manager |
| Motion Designer | مجری | Design Manager |
| Accessibility Specialist | مجری | Design Manager |
| UI/UX Research Participants | مجری | UX Researcher |

---

### عملیاتی و زیرساخت (3 ناظر + 7 مجری = 10)

| عنوان شغلی | نقش | ناظر مربوطه |
|---|---|---|
| Operations Manager | ناظر | - |
| Infrastructure Manager | ناظر | - |
| DevOps Manager | ناظر | - |
| Infrastructure Engineer | مجری | Infrastructure Manager |
| System Administrator | مجری | Infrastructure Manager |
| Network Engineer | مجری | Infrastructure Manager |
| Maintenance Engineer | مجری | Infrastructure Manager |
| DevOps Engineer | مجری | DevOps Manager |
| SRE (Site Reliability Engineer) | مجری | DevOps Manager |
| Cloud Engineer | مجری | Cloud Architect |
| Backup Administrator | مجری | Infrastructure Manager |
| Deploy Engineer | مجری | DevOps Manager |
| On-call Engineer | مجری | Incident Manager |
| Observability Engineer | مجری | DevOps Manager |
| Decommission Engineer | مجری | Infrastructure Manager |

---

### ابری (3 ناظر + 2 مجری = 5)

| عنوان شغلی | نقش | ناظر مربوطه |
|---|---|---|
| Cloud Architect | ناظر | - |
| FinOps Specialist | ناظر | - |
| CTO | ناظر | - |
| Cloud Engineer | مجری | Cloud Architect |
| Observability Engineer | مجری | DevOps Manager |

---

### شبکه (1 مجری)

| عنوان شغلی | نقش | ناظر مربوطه |
|---|---|---|
| Network Engineer | مجری | Infrastructure Manager |

---

### پایگاه داده (1 ناظر + 2 مجری = 3)

| عنوان شغلی | نقش | ناظر مربوطه |
|---|---|---|
| Data Architect | ناظر | - |
| Database Administrator (DBA) | مجری | Data Architect |
| Database Engineer | مجری | Data Architect |

---

### DevOps و SRE (3 ناظر + 6 مجری = 9)

| عنوان شغلی | نقش | ناظر مربوطه |
|---|---|---|
| DevOps Manager | ناظر | - |
| Infrastructure Manager | ناظر | - |
| Incident Manager | ناظر | - |
| DevOps Engineer | مجری | DevOps Manager |
| SRE (Site Reliability Engineer) | مجری | DevOps Manager |
| Release Engineer | مجری | DevOps Manager |
| Build Engineer | مجری | DevOps Manager |
| Deployment Engineer | مجری | DevOps Manager |
| On-call Engineer | مجری | Incident Manager |

---

### بازاریابی و فروش (11 ناظر + 7 مجری = 18)

| عنوان شغلی | نقش | ناظر مربوطه |
|---|---|---|
| Investor / سرمایه‌گذار | ناظر | - |
| Customer Success Manager | ناظر | - |
| Product Marketing Manager | ناظر | - |
| Growth Manager | ناظر | - |
| Sales Manager | ناظر | - |
| Account Manager | ناظر | - |
| Business Development Manager | ناظر | - |
| Partnership Manager | ناظر | - |
| Vendor Manager | ناظر | - |
| Community Director | ناظر | - |
| Support Manager | ناظر | - |
| Marketing Specialist | مجری | Product Marketing Manager |
| SEO Specialist | مجری | Product Marketing Manager |
| ASO Specialist | مجری | Product Marketing Manager |
| Sales Representative | مجری | Sales Manager |
| DevRel | مجری | Community Director |
| Technical Evangelist | مجری | Community Director |
| Community Manager | مجری | Community Director |

---

### پشتیبانی مشتری (1 ناظر + 2 مجری = 3)

| عنوان شغلی | نقش | ناظر مربوطه |
|---|---|---|
| Support Manager | ناظر | - |
| Customer Support Agent | مجری | Support Manager |
| Technical Support Engineer | مجری | Support Manager |

---

### حقوقی و انطباق (6 ناظر + 1 مجری = 7)

| عنوان شغلی | نقش | ناظر مربوطه |
|---|---|---|
| Legal Advisor | ناظر | - |
| IP / Copyright Specialist | ناظر | - |
| Privacy / Compliance Officer | ناظر | - |
| Chief Privacy Officer | ناظر | - |
| Contract Manager | ناظر | - |
| Audit Specialist | ناظر | - |
| External Auditor | ناظر | - |
| Privacy Engineer | مجری | Chief Privacy Officer |

---

### مالی و تجاری (4 ناظر + 1 مجری = 5)

| عنوان شغلی | نقش | ناظر مربوطه |
|---|---|---|
| Investor / سرمایه‌گذار | ناظر | - |
| Finance Manager | ناظر | - |
| Procurement Manager | ناظر | - |
| Vendor Manager | ناظر | - |
| Procurement Specialist | مجری | Procurement Manager |

---

### منابع انسانی (2 ناظر + 3 مجری = 5)

| عنوان شغلی | نقش | ناظر مربوطه |
|---|---|---|
| HR / People Manager | ناظر | - |
| Recruitment Manager | ناظر | - |
| Recruiter | مجری | Recruitment Manager |
| Technical Recruiter | مجری | Recruitment Manager |

---

### تحقیق و آنالیز (1 ناظر + 6 مجری = 7)

| عنوان شغلی | نقش | ناظر مربوطه |
|---|---|---|
| Domain Expert (SME) | ناظر | - |
| Business Analyst (BA) | مجری | Product Manager |
| Data Analyst | مجری | Product Analyst Lead |
| BI Analyst | مجری | Product Analyst Lead |
| Product Analyst | مجری | Product Manager |
| UX Researcher | مجری | Design Manager |
| UI/UX Research Participants | مجری | UX Researcher |

---

### مستندسازی (1 ناظر + 2 مجری = 3)

| عنوان شغلی | نقش | ناظر مربوطه |
|---|---|---|
| Documentation Manager | ناظر | - |
| Technical Writer | مجری | Documentation Manager |
| Documentation Specialist | مجری | Documentation Manager |

---

### Localization و ترجمه (1 ناظر + 2 مجری = 3)

| عنوان شغلی | نقش | ناظر مربوطه |
|---|---|---|
| Localization Manager | ناظر | - |
| Localization Specialist | مجری | Localization Manager |
| Translator | مجری | Localization Manager |

---

### سخت‌افزار و Embedded (1 ناظر + 3 مجری = 4)

| عنوان شغلی | نقش | ناظر مربوطه |
|---|---|---|
| Embedded Systems Lead | ناظر | - || Embedded Developer | مجری | Embedded Systems Lead |
| Firmware Engineer | مجری | Embedded Systems Lead |
| IoT Engineer | مجری | Embedded Systems Lead |

---

### Integration و Third-Party (2 مجری)

| عنوان شغلی | نقش | ناظر مربوطه |
|---|---|---|
| Third-party Integration Specialist | مجری | Technical Lead |
| Migration Specialist | مجری | Technical Lead |

---

### Migration و Modernization (2 مجری)

| عنوان شغلی | نقش | ناظر مربوطه |
|---|---|---|
| Legacy Modernization Engineer | مجری | Principal Engineer |
| Decommission Engineer | مجری | Infrastructure Manager |

---

### Incident و Disaster Recovery (2 ناظر + 4 مجری = 6)

| عنوان شغلی | نقش | ناظر مربوطه |
|---|---|---|
| Incident Manager | ناظر | - |
| Business Continuity Manager | ناظر | - |
| On-call Engineer | مجری | Incident Manager |
| Disaster Recovery Specialist | مجری | Business Continuity Manager |
| Backup Administrator | مجری | Infrastructure Manager |
| Decommission Engineer | مجری | Infrastructure Manager |

---

## مپینگ ناظر-مجری

### تیم توسعه نرم‌افزار
- **Development Manager** → Software Engineer, Backend Developer, Frontend Developer, Full-Stack Developer, Mobile Developer, Desktop Developer, Game Developer
- **Technical Lead** → Staff Engineer, Refactoring Engineer, Third-party Integration Specialist, Migration Specialist
- **Principal Engineer** → Staff Engineer, AI/ML Engineer, MLOps Engineer, Legacy Modernization Engineer

### تیم معماری
- **CTO** → Technical Lead, Principal Engineer, Solution Architect, Enterprise Architect
- **Cloud Architect** → Cloud Engineer
- **Enterprise Architect** → System Architect
- **Data Architect** → Database Administrator, Database Engineer

### تیم امنیتی
- **CISO** → Security Architect, Security Engineer, Application Security Engineer, Cybersecurity Engineer, Penetration Tester, DevSecOps Engineer
- **Chief Privacy Officer** → Privacy Engineer

### تیم کیفیت و تست
- **QA Lead** → QA Engineer, Test Engineer, Test Automation Engineer, Beta Tester
- **Quality Manager** → QA Lead
- **Performance Engineering Lead** → Performance Engineer, Load/Stress Tester

### تیم طراحی
- **Design Manager** → UI Designer, UX Designer, Product Designer, UX Researcher, UX Writer, Design System Designer, Graphic Designer, Motion Designer, Accessibility Specialist
- **Chief Design Officer** → Design Manager

### تیم عملیات و زیرساخت
- **Infrastructure Manager** → Infrastructure Engineer, System Administrator, Network Engineer, Maintenance Engineer, Backup Administrator, Decommission Engineer
- **DevOps Manager** → DevOps Engineer, SRE, Release Engineer, Build Engineer, Deployment Engineer, Observability Engineer
- **Incident Manager** → On-call Engineer
- **Business Continuity Manager** → Disaster Recovery Specialist

### تیم ابری
- **Cloud Architect** → Cloud Engineer

### تیم بازاریابی و فروش
- **Product Marketing Manager** → Marketing Specialist, SEO Specialist, ASO Specialist
- **Sales Manager** → Sales Representative
- **Community Director** → Community Manager, DevRel, Technical Evangelist
- **Support Manager** → Customer Support Agent, Technical Support Engineer

### تیم مالی و تجاری
- **Finance Manager** → (no direct executors)
- **Procurement Manager** → Procurement Specialist
- **Vendor Manager** → (no direct executors)

### تیم منابع انسانی
- **HR / People Manager** → (no direct executors in list)
- **Recruitment Manager** → Recruiter, Technical Recruiter

### تیم تحقیق و آنالیز
- **Product Manager** → Business Analyst, Product Analyst
- **Design Manager** → UX Researcher
- **Product Analyst Lead** → Data Analyst, BI Analyst

### تیم مستندسازی
- **Documentation Manager** → Technical Writer, Documentation Specialist

### تیم Localization
- **Localization Manager** → Localization Specialist, Translator

### تیم سخت‌افزار و Embedded
- **Embedded Systems Lead** → Embedded Developer, Firmware Engineer, IoT Engineer

---

## آمار و خلاصه

### بر اساس نقش
- **ناظرها:** 65 نقش (15 نقش جدید اضافه شد)
- **مجری‌ها:** 90 نقش
- **کل نقش‌ها:** 155 نقش

### بر اساس حوزه

| حوزه | ناظر | مجری | مجموع |
|---|---|---|---|
| مدیریت و استراتژی | 18 | 0 | 18 |
| محصول | 10 | 5 | 15 |
| معماری نرم‌افزاری | 9 | 2 | 11 |
| توسعه نرم‌افزار | 1 | 15 | 16 |
| داده و هوش مصنوعی | 2 | 6 | 8 |
| امنیتی | 2 | 6 | 8 |
| کیفیت و تست | 3 | 7 | 10 |
| طراحی و تجربه کاربری | 2 | 10 | 12 |
| عملیاتی و زیرساخت | 3 | 7 | 10 |
| ابری | 3 | 2 | 5 |
| شبکه | 0 | 1 | 1 |
| پایگاه داده | 1 | 2 | 3 |
| DevOps و SRE | 3 | 6 | 9 |
| بازاریابی و فروش | 11 | 7 | 18 |
| پشتیبانی مشتری | 1 | 2 | 3 |
| حقوقی و انطباق | 6 | 1 | 7 |
| مالی و تجاری | 4 | 1 | 5 |
| منابع انسانی | 2 | 3 | 5 |
| تحقیق و آنالیز | 1 | 6 | 7 |
| مستندسازی | 1 | 2 | 3 |
| Localization و ترجمه | 1 | 2 | 3 |
| سخت‌افزار و Embedded | 1 | 3 | 4 |
| Integration و Third-Party | 0 | 2 | 2 |
| Migration و Modernization | 0 | 2 | 2 |
| Incident و Disaster Recovery | 2 | 4 | 6 |
| **جمع** | **65** | **90** | **155** |

---

### نکات کلیدی:
✅ **تمام 90 نقش مجری اکنون حداقل یک ناظر دارند**
✅ **15 نقش ناظر جدید اضافه شد**
✅ **ساختار سازمانی کامل و متوازن**
✅ **مپینگ کامل ناظر-مجری برای هر تیم**

### ناظرهای جدید اضافه شده:
1. Development Manager
2. Engineering Manager
3. CTO (Chief Technology Officer)
4. CISO (Chief Information Security Officer)
5. Chief Privacy Officer
6. Performance Engineering Lead
7. Infrastructure Manager
8. DevOps Manager
9. Support Manager
10. Community Director
11. Design Manager
12. Chief Design Officer (CDO)
13. Documentation Manager
14. Localization Manager
15. Embedded Systems Lead
16. Procurement Manager
17. Recruitment Manager
