# قرارداد پراگماتیک — استخراج از The Pragmatic Programmer

این سند توضیح می‌دهد قواعد کتاب «The Pragmatic Programmer» (Andrew Hunt و David Thomas) چگونه به
**یک** قرارداد واحد تبدیل شده، کجا زندگی می‌کند، و چطور به personaها و skillها وصل می‌شود.

> خودِ قواعد اینجا تکرار **نشده‌اند**. منبع یگانه:
> [`composites/blocks/95-pragmatic-contract.md`](../composites/blocks/95-pragmatic-contract.md)
> (به انگلیسی، هم‌سبک با بقیهٔ بلوک‌ها). این سند فقط نقشهٔ استخراج و نحوهٔ اتصال است.
> قرارداد رفکتورینگ (Refactoring.Guru): [`docs/refactoring-contract.md`](refactoring-contract.md).
> قرارداد سیستم طراحی فرانت‌اند: [`docs/frontend-design-system-contract.md`](frontend-design-system-contract.md).

---

## ۱. نقشهٔ استخراج

| بخش بلوک ۹۵ | بخش کتاب |
|---|---|
| `Be pragmatic, not dogmatic` | Primary Directive + Own the Result + Think Beyond the Local Edit + Broken Windows Rule |
| `DRY means duplicated knowledge, not duplicated text` | DRY Rules |
| `Orthogonality` | Orthogonality Rules |
| `Tracer bullets and incremental delivery` | Tracer Bullets + Prototyping Rules + Estimation and Increment Rules |
| `Automation and tooling` | Automation Rules + Tooling Rules + Basic Tool Rules |
| `Feedback loops` | Feedback Loop Rules |
| `Contracts, assumptions, and resources` | Design by Contract + Error Handling + Resource and Coupling Rules |
| `Communication is part of the work` | Naming and Communication Rules + Text and Data Rules + Project and Team Rules |
| `Pragmatic review gate` | Review Checklist |

## ۲. چه چیزی عمداً نگرفتیم (تکرار با بلوک‌های موجود)

| محتوا | چرا نه | کجاست |
|---|---|---|
| Boy Scout Rule («کد را تمیزتر واگذار کن») | بلوک ۹۰ مالک آن است؛ ۹۵ فقط «ناحیه بهتر شود نه فقط خطوط لمس‌شده» را اضافه می‌کند | `90-construction-contract.md` §1 |
| حذف تکراری کد و قاعدهٔ ترکیب/جدایی | بلوک ۹۰ و ۹۱ مالک آن‌ها هستند؛ ۹۵ تست *بین‌لایه‌ای* DRY را اضافه می‌کند (یک قانون = یک نمایندگی معتبر) | `90-construction-contract.md` §3 · `91-design-depth-contract.md` §10 |
| استثنای «تکراری را حذف نکن که دو use case را به هم ببندد» | بلوک ۹۲ مالک آن است و ۹۵ به آن ارجاع می‌دهد | `92-clean-architecture-contract.md` §8 |
| نام‌گذاری و مستندسازی | بلوک ۹۰ و ۹۳ مالک آن‌ها هستند | `90-construction-contract.md` §2 · §4 · `93-domain-model-contract.md` §2 |
| تفکیک assertion / validation / خطای دامنه | بلوک ۹۰ مالک آن است | `90-construction-contract.md` §9 |
| state مشترک و همزمانی | بلوک ۹۰ مالک آن است | `90-construction-contract.md` §13 |
| Law of Demeter / train wreck | بلوک ۹۰ مالک آن است | `90-construction-contract.md` §8 |
| بازگشت‌پذیری (reversibility) و DSL دامنه | بلوک ۹۲ (حفظ option) و ۹۳ (زبان دامنه) مالک آن‌ها هستند | `92-clean-architecture-contract.md` §13 · `93-domain-model-contract.md` §13 |
| کیفیت تست و تست بی‌ادعا | بلوک ۹۰ مالک آن است | `90-construction-contract.md` §11 |

## ۳. کجا وصل شده

| جایگاه | ۹۵ (پراگماتیک) |
|---|---|
| `Software Design & Architecture Review.md` | ✅ |
| `Clean Code & Construction Review.md` | ✅ |
| `Domain Model & Context Review.md` | ✅ |
| `Technical Debt & Modernization Audit.md` | ✅ |
| `Testing & Quality Assurance Audit.md` | ✅ |

`Data & Database Integrity Audit` و `API & Integration Contract Audit` عمداً آن را نگرفتند:
آن دو personaها موضوع narrowly مشخصی دارند (داده و قرارداد) و بلوک ۹۴ را گرفته‌اند که موضوعشان است.

## ۴. بازتولید

```bash
python3 scripts/compose_persona.py --all
python3 scripts/build_skills.py
python3 scripts/validate_skills.py
python3 scripts/validate_personas.py
```

## ۵. اضافه‌کردن قانون تازه

1. قانون را در `composites/blocks/95-pragmatic-contract.md` بنویس (یک بار).
2. بلوک را به `blocks` compositeهای مرتبط اضافه کن.
3. بازتولید کن.
4. اگر قانون با بلوک دیگری هم‌پوشانی داشت، از بلوک دیگر **حذف**ش کن — منبع یگانه حفظ شود.
