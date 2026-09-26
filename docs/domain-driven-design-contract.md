# قرارداد مدل دامنه — استخراج از Domain-Driven Design (Evans، Vernon ×2)

این سند توضیح می‌دهد قواعد سه کتاب «Domain-Driven Design» (Eric Evans)،
«Domain-Driven Design Distilled» و «Implementing Domain-Driven Design» (Vaughn Vernon) چگونه به
**یک** قرارداد واحد تبدیل شده‌اند، کجا زندگی می‌کنند، و چطور به personaها و skillها وصل می‌شوند.

> خودِ قواعد اینجا تکرار **نشده‌اند**. منبع یگانه:
> [`composites/blocks/93-domain-model-contract.md`](../composites/blocks/93-domain-model-contract.md)
> (به انگلیسی، هم‌سبک با بقیهٔ بلوک‌ها). این سند فقط نقشهٔ ادغام و نحوهٔ اتصال است.
> قراردادهای قبلی: [`docs/construction-contract.md`](construction-contract.md) (Clean Code + Code Complete) و
> [`docs/design-architecture-contract.md`](design-architecture-contract.md) (Ousterhout + Clean Architecture).

---

## ۱. سه کتاب، یک قرارداد

سه کتاب یک موضوع را با تمرکز متفاوت پوشش می‌دهند، پس یک بلوک با ۱۵ بخش ساخته شد:

| منبع | سهم آن در بلوک |
|---|---|
| **DDD (Evans)** | استراتژیک (بounded context، context mapping، distillation، large-scale structure) و تاکتیکی (entity، value object، aggregate، domain service، specification، repository، factory، supple design) |
| **DDD Distilled (Vernon)** | انتخاب‌محوری: طبقه‌بندی subdomain، سبک‌های یکپارچه‌سازی (RPC/REST/messaging)، حداقل‌گرایی aggregate، event storming و «DDD theatre» |
| **Implementing DDD (Vernon)** | پیاده‌سازی عملیاتی: قواعد تجمعی، domain event و event sourcing، transformation service، ACL و هویت بین contextها، ساختار package |

هر قانونی که در بیش از یک کتاب آمده بود **یک بار** نوشته شد (مثلًا قواعد aggregate در هر سه کتاب
تقریباً یکسان بودند).

## ۲. نقشهٔ ادغام

| بخش بلوک ۹۳ | منبع |
|---|---|
| `The model serves the business meaning` | Primary Directive (هر سه) + What DDD Means in This Repository |
| `Ubiquitous language` | Ubiquitous Language (Evans + Distilled + IDDD) |
| `Bounded contexts` | Bounded Contexts (Evans) + Bounded Context Is Mandatory (IDDD) + Define Bounded Contexts Early (Distilled) |
| `Strategic design: subdomains and distillation` | Strategic Design + Distillation (Evans) + Start with Subdomains (Distilled) + Core Domain Protection (IDDD) |
| `Context mapping and integration` | Model Integrity Patterns + Context Mapping (Evans) + Context Relationship Rules + Integration Style Rules (Distilled) + Context Integration (IDDD) |
| `Entities` | Entities (Evans + Distilled + IDDD) |
| `Value objects` | Value Objects (Evans + Distilled + IDDD) |
| `Aggregates` | Aggregates (Evans) + Aggregate Minimalism (Distilled) + Aggregate Rules of Thumb (IDDD) |
| `Domain services and specifications` | Domain Services + Explicit Concepts and Specifications (Evans) + Domain and Transformation Service Rules (IDDD) |
| `Repositories and factories` | Repositories + Factories (Evans) + Repository Rules (IDDD) |
| `Domain events and eventual consistency` | Domain Event Rules + Event Sourcing (IDDD) + Domain Events (Distilled) |
| `Application layer, infrastructure, and translation` | Application Layer + Infrastructure + Translation at Boundaries (Evans) + Architecture and Infrastructure Rules (Distilled) |
| `Supple design` | Supple Design + Analysis and Model Patterns (Evans) |
| `Practicality: selective, serious DDD` | Adoption Fit (Distilled) + Practical Simplicity Rule (IDDD) + What DDD Does Not Mean (Evans) |
| `Domain model review gate` | Review Checklist (هر سه) |

## ۳. چه چیزی عمداً نگرفتیم (تکرار با بلوک‌های موجود)

این مهم‌ترین بخش است: DDD با Clean Architecture هم‌پوشانی زیاد دارد و بلوک ۹۲ از قبل آن را دارد.

| محتوا | چرا نه | کجاست |
|---|---|---|
| مسئولیت لایه‌ها، جهت وابستگی، use case به‌عنوان ارکستراسیون | بلوک ۹۲ مالک آن است | `92-clean-architecture-contract.md` §2–§3 |
| کامپوزیشن روت، port/adapter، پنهان‌سازی پیاده‌سازی | بلوک ۹۲ مالک آن است | `92-clean-architecture-contract.md` §5 |
| «entity باید invariant را حفظ کند» (به‌صورت عمومی) | ۹۲ آن را دارد؛ ۹۳ فقط هویت، چرخهٔ عمر و ممنوعیت setter عمومی را اضافه می‌کند | `92-clean-architecture-contract.md` §4 |
| نشتی framework/database به لایه‌های درونی، god service، layer bypass | بلوک ۹۲ مالک الگوهای ممنوع معماری است | `92-clean-architecture-contract.md` §11 |
| قواعد SRP/OCP/LSP/ISP/DIP و چرخهٔ کامپوننت | بلوک ۹۲ مالک آن است | `92-clean-architecture-contract.md` §7 |
| تست از مسیر مرز، بدون framework/database/network | بلوک ۹۲ مالک لِوَل تست است | `92-clean-architecture-contract.md` §10 |
| نام‌گذاری خوب، تایپ‌هایی که مقدار نامعتبر سخت‌تر represent می‌شوند | بلوک ۹۰ مالک آن است؛ ۹۳ فقط «واژه از کدام دامنه بیاید» و «مفهوم باید نام داشته باشد» را اضافه می‌کند | `90-construction-contract.md` §2 و §6 |
| کیفیت تست (قطعی، ایزوله، یک ایده per تست) | بلوک ۹۰ مالک آن است | `90-construction-contract.md` §11 |
| قاعدهٔ حذف تکراری و ترکیب/جدایی کد | بلوک ۹۱ مالک آن است | `91-design-depth-contract.md` §10 |
| شواهد یافتهٔ تغییر + پلن تغییر | بلوک مشترک ۹۵ | `95-change-findings.md` |

### مرز مشخص بین ۹۲ و ۹۳

این دو بلوک عمداً چنین تقسیم شده‌اند:

- `92-clean-architecture-contract.md` → **وابستگی‌ها به کدام سمت اشاره می‌کنند و کدام لایه مالک کدام قانون است.**
- `93-domain-model-contract.md` → **مدل چه معنایی دارد: زبان، مرزهای معنایی، و بلوک‌های تاکتیکی.**

هر جا این دو به هم می‌رسند (application service، infrastructure، translation، لِوَل تست)، بلوک ۹۳
فقط قانون اختصاصی دامنه را می‌گوید و بقیه را به ۹۲ ارجاع می‌دهد — به‌عنوان مثال در §12 صریحاً
نوشته شده «layer and use-case rules stay with the Architecture Boundaries contract».

## ۴. کجا وصل شده

| جایگاه | ۹۳ (مدل دامنه) |
|---|---|
| `Domain Model & Context Review.md` (persona ترکیبی تازه) | ✅ |
| `Software Design & Architecture Review.md` | ✅ |
| `Technical Debt & Modernization Audit.md` | ✅ |
| `API & Integration Contract Audit.md` | ✅ |
| `Data & Database Integrity Audit.md` | ✅ |
| `Testing & Quality Assurance Audit.md` | ✅ |

`Clean Code & Construction Review` عمداً ۹۳ را **نگرفت**: آن persona کیفیت ساخت محلی (نام، روال،
داده، جریان کنترل، تست) را می‌سنجد و مدل دامنه خانهٔ شخصای تازه و `Software Design & Architecture Review` است.
بقیهٔ compositeها می‌توانند با اضافه‌کردن `"93-domain-model-contract.md"` به `blocks` در spec خودشان include کنند.

## ۵. persona ترکیبی تازه

`Domain Model & Context Review` (۶ عدسی: Staff Engineer، Principal Engineer، Software Architect،
Domain Expert/SME، Refactoring Engineer، Legacy Modernization Engineer) با دو بخش اختصاصی:

- **Bounded Context & Language Register** — یک ردیف per context: واژگان، اجزای مدل، subdomain،
  رابطهٔ context map، مالک translation و نشتی‌ها.
- **Domain Modeling Passes** — ۱۱ پاس با پیشوند ID جدا (`LNG-` زبان، `IMP-` مفهوم‌های ضمنی،
  `CTX-` context، `MAP-` context mapping، `SUB-` subdomain، `ENT-` entity، `VAL-` value object،
  `AGG-` aggregate، `SVC-` service/specification/event، `REP-` repository/factory/translation،
  `THT-` DDD theatre).

## ۶. بازتولید

```bash
python3 scripts/compose_persona.py --all
python3 scripts/build_skills.py
python3 scripts/validate_skills.py
python3 scripts/validate_personas.py
```

## ۷. اضافه‌کردن قانون تازه

1. قانون را در `composites/blocks/93-domain-model-contract.md` بنویس (یک بار).
2. بلوک را به `blocks` compositeهای مرتبط اضافه کن.
3. بازتولید کن.
4. اگر قانون با بلوک دیگری هم‌پوشانی داشت، از بلوک دیگر **حذف**ش کن — منبع یگانه حفظ شود.
