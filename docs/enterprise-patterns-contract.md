# قرارداد الگوهای سازمانی — استخراج از Patterns of Enterprise Application Architecture

این سند توضیح می‌دهد قواعد کتاب «Patterns of Enterprise Application Architecture» (Martin Fowler)
چگونه به **یک** قرارداد واحد تبدیل شده، کجا زندگی می‌کند، و چطور به personaها و skillها وصل می‌شود.

> خودِ قواعد اینجا تکرار **نشده‌اند**. منبع یگانه:
> [`composites/blocks/94-enterprise-patterns-contract.md`](../composites/blocks/94-enterprise-patterns-contract.md)
> (به انگلیسی، هم‌سبک با بقیهٔ بلوک‌ها). این سند فقط نقشهٔ استخراج و نحوهٔ اتصال است.

---

## ۱. نقشهٔ استخراج

| بخش بلوک ۹۴ | بخش کتاب |
|---|---|
| `Patterns, not invented architecture` | Purpose + Primary Directive + Architectural Baseline (Layering) |
| `Choose the business logic pattern deliberately` | Choosing the Business Logic Pattern (Transaction Script / Table Module / Domain Model) |
| `Application workflow` | Application Workflow Rules (Service Layer) |
| `Remote boundaries, facades, and DTOs` | Remote Facade + Data Transfer Object + Distribution Rules |
| `Persistence pattern choice` | Repository + Data Mapper + Row/Table Data Gateway + Active Record |
| `Unit of Work, Identity Map, and loading` | Identity, Caching, and Unit-of-Work Rules |
| `Object-relational mapping choices` | Object-Relational Mapping Pattern Index (۱۲ الگو) |
| `Transactions and offline concurrency` | Optimistic Offline Lock + Pessimistic Locking + Coarse-Grained/Implicit Lock + Transaction Boundaries |
| `Presentation responsibilities` | Presentation Layer Rules + Presentation Pattern Index |
| `Session and cross-cutting state` | Session State Rules |
| `Base patterns worth using deliberately` | Base Pattern Index (Gateway، Mapper، Special Case، Money، Plugin، …) |
| `Testing structure, not only behaviour` | Testing Rules |
| `Enterprise patterns review gate` | Review Checklist |

## ۲. چه چیزی عمداً نگرفتیم (تکرار با بلوک‌های موجود)

| محتوا | چرا نه | کجاست |
|---|---|---|
| مسئولیت لایه‌ها، جهت وابستگی، «هر لایه باید وجودش را توجیه کند» | لایه‌ها و جهت وابستگی در بلوک ۹۲ است؛ «ماژول عبوری» هم در بلوک ۹۱ | `92-clean-architecture-contract.md` §2 · `91-design-depth-contract.md` §2 |
| قواعد Repository (aggregate root، رابط دامنه‌محور، نبودِ generic CRUD) | بلوک DDD مالک آن است | `93-domain-model-contract.md` §10 |
| «domain logic نباید در controller/view باشد»، «ORM نباید مدل را تعیین کند» | بلوک ۹۲ الگوهای ممنوعش را دارد | `92-clean-architecture-contract.md` §11 |
| Value Object و immutability | بلوک DDD مالک آن است | `93-domain-model-contract.md` §7 |
| «تماس ریمی مثل متد محلی نیست» | بلوک ۹۲ آن را دارد | `92-clean-architecture-contract.md` §9 |
| کیفیت تست و لِوَل تست دامنه | بلوک ۹۰ و ۹۲ مالک آن‌ها هستند؛ ۹۴ فقط تست زیرساخت داده/تراکنش/مپینگ را اضافه می‌کند | `90-construction-contract.md` §11 · `92-clean-architecture-contract.md` §10 |
| قواعد همزمانی مشترک (state، immutability) | بلوک ۹۰ مالک آن است | `90-construction-contract.md` §13 |

نکتهٔ مهم: کتاب Fowler پیش‌تر در مخزن به‌صورت پراکنده دیده شده بود (مثل «repository» و «gateway»)،
پس این بلوک فقط چیزی را اضافه می‌کند که هیچ بلوکی نداشت: **انتخاب الگوی منطق کسب‌وکار**،
**الگوی persistence متناسب با پیچیدگی**، **Unit of Work / Identity Map / Lazy Load**،
**الگوهای ORM**، **قفل آفلاین و مرز تراکنش**، **الگوهای لایهٔ presentation** و **الگوهای پایه**.

## ۳. کجا وصل شده

| جایگاه | ۹۴ (الگوهای سازمانی) |
|---|---|
| `Software Design & Architecture Review.md` | ✅ |
| `Domain Model & Context Review.md` | ✅ |
| `Technical Debt & Modernization Audit.md` | ✅ |
| `Data & Database Integrity Audit.md` | ✅ |
| `API & Integration Contract Audit.md` | ✅ |

`Clean Code & Construction Review` عمداً آن را **نگرفت**: آن persona کیفیت ساخت محلی را می‌سنجد
و الگوهای ساختاری سازمانی خانهٔ personaهای طراحی/معماری و دامنه است.

## ۴. بازتولید

```bash
python3 scripts/compose_persona.py --all
python3 scripts/build_skills.py
python3 scripts/validate_skills.py
python3 scripts/validate_personas.py
```

## ۵. اضافه‌کردن قانون تازه

1. قانون را در `composites/blocks/94-enterprise-patterns-contract.md` بنویس (یک بار).
2. بلوک را به `blocks` compositeهای مرتبط اضافه کن.
3. بازتولید کن.
4. اگر قانون با بلوک دیگری هم‌پوشانی داشت، از بلوک دیگر **حذف**ش کن — منبع یگانه حفظ شود.
