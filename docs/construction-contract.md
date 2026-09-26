# قرارداد ساخت (Construction Contract) — استخراج از Clean Code و Code Complete

این سند توضیح می‌دهد قواعد دو کتاب «Clean Code» (Robert C. Martin) و «Code Complete»
(Steve McConnell) چگونه به **یک** قرارداد واحد و بدون تکرار تبدیل شده‌اند، کجا زندگی می‌کنند،
و چطور به personaها و skillها وصل می‌شوند.

> خودِ قواعد اینجا تکرار **نشده‌اند**. تنها منبع قواعد:
> [`composites/blocks/90-construction-contract.md`](../composites/blocks/90-construction-contract.md)
> (به انگلیسی، هم‌سبک با بقیهٔ بلوک‌های master prompt). این سند فقط نقشهٔ ادغام و نحوهٔ اتصال است.
> دو کتاب دیگر («A Philosophy of Software Design» و «Clean Architecture») جداگانه مستند شده‌اند:
> [`docs/design-architecture-contract.md`](design-architecture-contract.md).
> الگوهای سازمانی (Fowler) و انضباط پراگماتیک (Hunt & Thomas):
> [`docs/enterprise-patterns-contract.md`](enterprise-patterns-contract.md) ·
> [`docs/pragmatic-programmer-contract.md`](pragmatic-programmer-contract.md).
> قرارداد رفکتورینگ (Refactoring.Guru): [`docs/refactoring-contract.md`](refactoring-contract.md). شواهد الزامی برای یافته‌های
> «تغییر» هم در بلوک مشترک `95-change-findings.md` زندگی می‌کند.

---

## ۱. چرا یک بلوک، نه ۱۷۰ کپی؟

معماری مخزن این است: پرامپت personaها **تولیدشده** هستند (`scripts/generate_personas.py` از دادهٔ README)
و قرارداد مشترکِ ممیزی‌ها در **بلوک‌های قابل استفادهٔ مجدد** زندگی می‌کند (`composites/blocks/`).
اگر قواعد ساخت را داخل ۱۷۰ فایل persona کپی می‌کردیم:

- هر اصلاح قانون باید ۱۷۰ بار تکرار می‌شد (و ناهم‌خوان می‌شد)؛
- بازتولید personaها محتوای دستی را پاک می‌کرد؛
- حجم مخزن و کانتکست مدل بی‌دلیل دوبرابر می‌شد.

پس قانون طلایی این تغییر: **یک منبع، چند ارجاع.** قواعد یک جا نوشته می‌شوند و compositeهای
مرتبط آن بلوک را include می‌کنند؛ skillها هم از طریق `references/` به همان متن واحد اشاره می‌کنند.

---

## ۲. نقشهٔ ادغام (کدام بخش‌ها یکی شدند)

دو سند اصلی در بسیاری از نقاط یک چیز را با واژهٔ دیگری می‌گفتند. ادغام به این شکل انجام شد:

| بخش قرارداد | از Clean Code | از Code Complete | تصمیم ادغام |
|---|---|---|---|
| `Priority` | Priority and behavior، Implementation preferences | Primary Directive، Construction Prerequisites | هر دو یک چیز می‌گفتند: «خوانندهٔ بعدی مهم‌تر از باهوشی است» → یک بخش |
| `Naming` | Naming rules | Variable and Data Rules (بخش نام‌ها) | یکی شد؛ قواعد «یک واژه per مفهوم» و «بدون encoding» فقط یک بار |
| `Routines` | Function rules | Routine Design Rules | یکی شد؛ anti-patternهای مشترک یک بار |
| `Comments` | Comment rules | Comment Rules | یکی شد؛ فهرست «کامنت خوب» یک بار |
| `Formatting and structure` | Formatting and structure | Coding Standards Rules، Statement Rules (بخش چیدمان) | یکی شد |
| `Data and types` | Objects, modules, and data structures (بخش داده) | Variable Rules، Data Type Rules | یکی شد؛ «مقدار جادویی/واحد/دامنه» یک بار |
| `Control flow` | Function rules (بخش جریان کنترل) | Control Flow Rules، Statement/Conditional/Loop Rules | یکی شد |
| `Objects, modules, and boundaries` | Objects and data structures، Boundaries | Class and Module Design، Boundaries | یکی شد؛ «god class» و «train wreck» یک بار |
| `Errors and defensive programming` | Error handling | Defensive Programming، Error Handling، Preconditions/Postconditions | یکی شد؛ تفکیک assertion/validation/domain-error یک بار |
| `Complexity and smells` | Smells to detect and eliminate | Complexity Management، Forbidden Patterns، Review Rules | یکی شد؛ فهرست بوها یک بار (طبقه‌بندی بدهی در بلوک `65-debt` مانده) |
| `Tests` | Tests، TDD and clean test rules | Testing Rules | یکی شد؛ «تست = کد تولید» یک بار |
| `Refactoring and change process` | Refactoring rules، Emergent design، Change Process | Incremental Construction، Quality/Refactoring | یکی شد؛ چک‌لیست فرایند تغییر یک بار |
| `Concurrency` | Concurrency and async work | — (فقط در Code Complete نبود) | از Clean Code آمد، بدون تغییر معنایی |
| `Construction review gate` | Review checklist | Review Checklist | دو چک‌لیست تقریباً یکسان بودند → **یکی** شد |

### چه چیزی عمداً حذف شد (برای جلوگیری از تکرار با بلوک‌های موجود)

| محتوا | چرا نگرفتیم | کجاست |
|---|---|---|
| طبقه‌بندی بدهی فنی (accidental/architectural/testing/…) و قاعدهٔ «dead را repository-wide بررسی کن» | در قرارداد ساخت فقط به‌عنوان «بو» نام برده شد، بدون توضیح مجدد | `composites/blocks/65-debt.md` |
| شکاف تست (چه چیزی تست نشده) | قرارداد ساخت فقط *کیفیت نوشتن تست* را می‌گوید؛ «چه چیزی کم است» در پاس تخصصی می‌ماند | `composites/blocks/55-specialized.md` (§9.6) |
| قواعد شواهد و «هیچ حدس» | مبحث متفاوتی است: ادعا دربارهٔ کدبیس، نه کیفیت کد | `composites/blocks/10-prime-directive.md` |
| Quality Gate نهایی ممیزی | گیت ما برای *خودِ تغییر* است، نه برای پوشش ممیزی | `composites/blocks/80-quality-gate.md` |

---

## ۳. کجا وصل شده

| جایگاه | وضعیت |
|---|---|
| `composites/blocks/90-construction-contract.md` | ✅ منبع واحد قواعد |
| `Clean Code & Construction Review.md` (persona ترکیبی تازه) | ✅ کل قرارداد + عدسی‌های Staff/Principal/Architect/Refactoring/Test-Automation/Docs |
| `Technical Debt & Modernization Audit.md` | ✅ بلوک اضافه شد (بدهی ↔ قواعد ساخت) |
| `Testing & Quality Assurance Audit.md` | ✅ بلوک اضافه شد (کیفیت تست) |
| `skills/clean-code-construction-review/`, `skills/technical-debt-modernization-audit/`, `skills/testing-quality-assurance-audit/` | ✅ خودکار بازتولید شدند؛ `SKILL.md` فقط **نقشهٔ بخش‌ها** را دارد و قواعد را کپی نمی‌کند |

سایر compositeها می‌توانند با اضافه‌کردن `"90-construction-contract.md"` به `blocks` در spec خود
این قرارداد را include کنند (پیش‌فرض include نشدهند تا محتوا تکراری نشود).

### چطور در skillها تکراری نشده

در `SKILL.md`ها فقط **فهرست بخش‌های master prompt** می‌آید (با نشان `◆` برای بخش‌های اختصاصی)،
مثلاً:

```
## نقشهٔ master prompt (در مرجع — ◆ = بخش اختصاصی این persona)
- PRIME DIRECTIVE — ZERO ASSUMPTIONS
- CONSTRUCTION CONTRACT — Clean Code + Code Complete (binding)
- ◆ Construction Findings — required evidence
```

خودِ قواعد فقط در `references/<persona>.md` هستند. این همان progressive disclosure است:
مدل اول نقشه را می‌بیند و فقط وقتی به قواعد نیاز دارد مرجع را باز می‌کند.

---

## ۴. بازتولید

```bash
python3 scripts/compose_persona.py --all          # ساخت master promptها از بلوک + spec
python3 scripts/build_skills.py                   # بازتولید skillها
python3 scripts/validate_skills.py                # اعتبارسنجی
python3 scripts/validate_personas.py              # اعتبارسنجی personaهای نقش
```

## ۵. اضافه‌کردن قانون تازه به قرارداد

1. قانون را در `composites/blocks/90-construction-contract.md` بنویس (یک بار).
2. اگر persona ترکیبی تازه‌ای باید آن را داشته باشد، بلوک را به `blocks` specش اضافه کن.
3. `python3 scripts/compose_persona.py --all && python3 scripts/build_skills.py`
4. اگر قانون با بلوک دیگری هم‌پوشانی داشت، از بلوک دیگر **حذف**ش کن (نه اینجا کپی) — منبع یگانه حفظ شود.
