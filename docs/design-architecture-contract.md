# قرارداد طراحی و معماری — استخراج از A Philosophy of Software Design و Clean Architecture

این سند توضیح می‌دهد قواعد دو کتاب «A Philosophy of Software Design» (John Ousterhout) و
«Clean Architecture» (Robert C. Martin) چگونه به **دو** قرارداد واحد تبدیل شده‌اند، کجا زندگی
می‌کنند، و چطور به personaها و skillها وصل می‌شوند.

> خودِ قواعد اینجا تکرار **نشده‌اند**. منابع یگانه:
> [`composites/blocks/91-design-depth-contract.md`](../composites/blocks/91-design-depth-contract.md) (Ousterhout) و
> [`composites/blocks/92-clean-architecture-contract.md`](../composites/blocks/92-clean-architecture-contract.md) (Clean Architecture)،
> به انگلیسی و هم‌سبک با بقیهٔ بلوک‌ها. این سند فقط نقشهٔ استخراج و نحوهٔ اتصال است.
> قرارداد قبلی (Clean Code + Code Complete) در [`docs/construction-contract.md`](construction-contract.md) مستند شده است.
> یک کتاب دیگر («Domain-Driven Design») جداگانه مستند شده است:
> [`docs/domain-driven-design-contract.md`](domain-driven-design-contract.md).
> الگوهای سازمانی (Fowler) و انضباط پراگماتیک (Hunt & Thomas):
> [`docs/enterprise-patterns-contract.md`](enterprise-patterns-contract.md) ·
> [`docs/pragmatic-programmer-contract.md`](pragmatic-programmer-contract.md).
> قرارداد رفکتورینگ (Refactoring.Guru): [`docs/refactoring-contract.md`](refactoring-contract.md).

---

## ۱. چرا دو بلوک، نه یکی؟

این دو کتاب دو سؤال مختلف را جواب می‌دهند و برای دو composite متفاوت به کار می‌آیند:

| بلوک | سؤالی که جواب می‌دهد | کتاب |
|---|---|---|
| `91-design-depth-contract.md` | «این ماژول چقدر عمیق است و خواننده چقدر باید بداند؟» | A Philosophy of Software Design |
| `92-clean-architecture-contract.md` | «این قانون در کدام لایه است و وابستگی‌ها به کدام سمت اشاره می‌کنند؟» | Clean Architecture |

یکی‌کردنشان یک بلوک ~۲۵۰خطی می‌ساخت که هیچ composite‌ای به تمامش نیاز ندارد. تفکیک باعث می‌شود
هر composite فقط آن را include کند که موضوعش را دارد.

---

## ۲. نقشهٔ استخراج — Ousterhout → `91-design-depth-contract.md`

| بخش بلوک ۹۱ | بخش کتاب |
|---|---|
| `Complexity is the enemy` | Primary Directive + Symptoms of Complexity + Default Response |
| `Module depth` | Module Depth Rules + Avoid Shallow Modules + Function and Variable Rules |
| `Information hiding` | Information Hiding Rules |
| `Interface design` | Interface Design Rules |
| `Strategic over tactical programming` | Strategic Programming over Tactical Programming |
| `General-purpose vs special-purpose modules` | General-Purpose vs Special-Purpose Modules |
| `Define away exceptions` | Error Handling and Exception Elimination + Special-General Decomposition |
| `Pull complexity downward` | Pull Complexity Downward |
| `Temporal decomposition` | Temporal Decomposition Rules |
| `Combine or separate code` | Combine or Separate Code |
| `Design alternatives and comments-first design` | Design Alternatives and Comments-First Design |
| `Consistency and obviousness` | Naming, Consistency, and Obviousness |
| `Performance, trends, and tests` | Performance, Trends, and Tests |
| `Design review gate` | Review Checklist |

قواعد Code Generation و Testing کتاب هم در همین بلوک پخش شده‌اند (مثلًا «کدام مفهوم لایق مرز
ماژول است» → `Module depth`، «تست رفتار عمومی را حفظ می‌کند» → `Performance, trends, and tests`)
تا فهرست بلوک‌ها بی‌دلیل بزرگ نشود.

## ۳. نقشهٔ استخراج — Clean Architecture → `92-clean-architecture-contract.md`

| بخش بلوک ۹۲ | بخش کتاب |
|---|---|
| `The Dependency Rule` | Non-Negotiable Rules ۱ و ۱۰ + Architecture Heuristics (Dependency Direction) |
| `Layer responsibilities` | Required Layer Responsibilities (Domain / Application / Interface Adapters / Infrastructure) |
| `Use cases orchestrate` | Non-Negotiable Rules ۸ و ۹ + Code Generation Rules ۱ |
| `Entities guard invariants` | Non-Negotiable Rules ۲ و ۹ |
| `Ports, adapters, and wiring` | Code Generation Rules ۳–۶ + Use Explicit Boundaries |
| `Organise by use case` | Non-Negotiable Rule ۷ + Feature First Structure + Naming Rules |
| `Component rules` | Paradigm and Component Rules |
| `Boundary cost and deployment` | Boundary Cost, Deployment, and Operations + Architecture Economics |
| `Services, remote calls, and embedded details` | Services, Distribution, and Embedded Boundaries |
| `Testing through boundaries` | Testing Rules |
| `Forbidden patterns` | Forbidden Patterns |
| `Refactoring toward the rule` | Refactoring Rules |
| `Architecture economics` | Architecture Economics and Priority |
| `Architecture review gate` | Review Checklist |

### چه چیزی عمداً نگرفتیم (تکرار با بلوک‌های موجود)

| محتوا | چرا نه | کجاست |
|---|---|---|
| کامپوزیشن روت / جدا کردن ساخت از استفاده | همین قانون در قرارداد ساخت هست | `90-construction-contract.md` §Objects, modules, and boundaries |
| «کلاس خدا» و هم‌بستگی پایین | در قرارداد ساخت به‌صورت بو آمد؛ اینجا فقط شکل *معماری*اش (`*Service` مالک چند use case) | `90-construction-contract.md` §Objects, modules, and boundaries |
| نام‌گذاری معمولی (یک واژه per مفهوم) | Ousterhout فقط «نام، abstractions را نشان دهد نه مکانیزم» را اضافه می‌کند؛ بقیه تکرار بود | `90-construction-contract.md` §Naming |
| کیفیت تست (قطعی‌بودن، ایزوله‌بودن، یک ایده per تست) | در قرارداد ساخت هست؛ Clean Architecture لِوَل درست تست را می‌گوید | `90-construction-contract.md` §Tests |
| «ابهام/ناسازگاری معماری را پیدا کن» | فقط دامنهٔ نگاه است، قانون نیست | `55-specialized.md` §9.7 Architecture |
| طبقه‌بندی بدهی | در بلوک بدهی می‌ماند | `65-debt.md` |
| شدت/اطمینان/قالب یافته | بلوک Findings مالک آن است | `60-findings.md` |

### یک تضاد عمدی که مستند شد

قرارداد ساخت می‌گوید «تکرار را aggressive حذف کن»؛ Clean Architecture می‌گوید «تکراری را حذف نکن
که دو use case با بازیگران متفاوت را به هم ببندد». این تضاد در `92-clean-architecture-contract.md`
§Boundary cost صریح نوشته شده تا مدل مجبور به انتخاب آگاهانه شود، نه اینکه یک قانون دیگری را کپی کند.

---

## ۴. بلوک مشترک `95-change-findings.md`

وقتی persona ترکیبی «تغییر» پیشنهاد می‌دهد، یافته باید شواهد و پلن تغییر را داشته باشد. این قواعد
یک بار در [`composites/blocks/95-change-findings.md`](../composites/blocks/95-change-findings.md) نوشته شده
و توسط هر دو persona «تغییرمحور» include می‌شود:

- `Clean Code & Construction Review` — قبلاً این دو بخش را به‌عنوان `extra_sections` در spec خودش داشت.
- `Software Design & Architecture Review` — persona تازه.

قبل از این تغییر، همان متن در دو جا کپی شده بود؛ حالا در بلوک زندگی می‌کند و severity را به
روبيةٔ پایهٔ `60-findings.md` map می‌کند (روبیک severity را دوباره نمی‌نویسد).

---

## ۵. کجا وصل شده

| جایگاه | ۹۱ (عمق طراحی) | ۹۲ (مرزهای معماری) | ۹۵ (یافتهٔ تغییر) |
|---|---|---|---|
| `Software Design & Architecture Review.md` (persona ترکیبی تازه) | ✅ | ✅ | ✅ |
| `Clean Code & Construction Review.md` | ✅ | — | ✅ |
| `Technical Debt & Modernization Audit.md` | ✅ | ✅ | ✅ |
| `API & Integration Contract Audit.md` | — | ✅ | — |
| `Data & Database Integrity Audit.md` | — | ✅ | — |
| `Testing & Quality Assurance Audit.md` | — | ✅ | — |

بقیهٔ compositeها می‌توانند با اضافه‌کردن نام بلوک به `blocks` در spec خودشان include کنند.

---

## ۶. بازتولید

```bash
python3 scripts/compose_persona.py --all
python3 scripts/build_skills.py
python3 scripts/validate_skills.py
python3 scripts/validate_personas.py
```

## ۷. اضافه‌کردن قانون تازه

1. قانون را در بلوک مربوطه بنویس (یک بار).
2. بلوک را به `blocks` compositeهای مرتبط اضافه کن.
3. بازتولید کن.
4. اگر قانون با بلوک دیگری هم‌پوشانی داشت، از بلوک دیگر **حذف**ش کن — منبع یگانه حفظ شود.
