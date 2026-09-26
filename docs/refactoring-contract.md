# قرارداد رفکتورینگ — استخراج از Refactoring.Guru

این سند توضیح می‌دهد قواعد عمومیِ رفکتورینگ (مبتنی بر کاتالوگ
[Refactoring.Guru](https://refactoring.guru/refactoring) و بخش‌های
[what-is-refactoring](https://refactoring.guru/refactoring/what-is-refactoring)،
[technical-debt](https://refactoring.guru/refactoring/technical-debt)،
[when](https://refactoring.guru/refactoring/when)،
[how-to](https://refactoring.guru/refactoring/how-to)،
[smells](https://refactoring.guru/refactoring/smells) و
[catalog/techniques](https://refactoring.guru/refactoring/catalog)) چگونه به **یک** قرارداد واحد
تبدیل شده، کجا زندگی می‌کند، و چطور به personaها و skillها وصل می‌شود.

> خودِ قواعد اینجا تکرار **نشده‌اند**. منبع یگانه:
> [`composites/blocks/97-refactoring-contract.md`](../composites/blocks/97-refactoring-contract.md)
> (به انگلیسی، هم‌سبک با بقیهٔ بلوک‌ها). این سند فقط نقشهٔ استخراج و نحوهٔ اتصال است.

---

## ۱. چرا این بلوک لازم شد

مخزن از قبل «رفکتور در گام‌های کوچک» و «کد را تمیزتر واگذار کن» را داشت (در قرارداد ساخت)،
ولی سه چیز را نداشت:

1. **جداسازی رفکتور از کار feature/bug** و انضباط راستی‌آزمایی و **شرط توقف**.
2. **کاتالوگ بو با محرک → درمان → جایگزین → گزینهٔ پرهزینه** (یعنی از «بو» به «درمان»).
3. **قواعد استثنای بو** که جلوی رفکتورینگ مکانیکی و over-engineering را می‌گیرند.

این بلوک دقیقاً همان سه چیز است و بقیه را به بلوک مالک ارجاع می‌دهد.

## ۲. نقشهٔ استخراج

| بخش بلوک ۹۷ | بخش منبع |
|---|---|
| `Refactoring is controlled improvement` | Purpose + What Is Refactoring? |
| `Keep refactoring separate from other work` | Keep Refactoring and Adding New Features Separate |
| `Work in small steps` | Work in Small Steps |
| `Verify continuously` | Verify Continuously (شامل «تست شکسته را حذف نکن») |
| `Keep the result cleaner` | Keep the Result Cleaner + قاعدهٔ بازنویسی برنامه‌ریزی‌شده |
| `When to refactor` | When to Refactor: Rule of Three + While Adding a Feature + While Fixing a Bug + During Code Review |
| `Technical debt, operationally` | Technical Debt (فقط قواعد عملیاتی؛ طبقه‌بندی در `65-debt` می‌ماند) |
| `Smell detection: scan in this order` | Smells → شش دستهٔ Bloaters / OO Abusers / Change Preventers / Dispensables / Couplers / Library Gaps |
| `Diagnose, treat, verify, stop` | Diagnose → Treat → Verify → Stop (Do Not Refactor if...) |
| `Smell exception rules` | Smell Exception Rules (MAY/MUST NOT) |
| `Smell catalog: triggers and treatments` | Code Smells + Smell-to-Treatment Priority Map (۲۲ بو) |
| `Technique selection` | Techniques → شش خانواده (Composing Methods، Moving Features، Organizing Data، Simplifying Conditionals، Simplifying Method Calls، Dealing with Generalization) |
| `Technique execution safety` | Technique Execution Safety (Extraction/Inlining/Moving/Encapsulation/Conditional/Method Call/Data/Generalization) |
| `Decision anti-patterns` | Decision Anti-Patterns |
| `Refactoring workflow for agents` | Refactoring Workflow for Agents (Before/During/After) |
| `Refactoring review gate` | Review Checklist |

### چه چیزی عمداً فشرده شد

پلی‌بوک ۶۶ تکنیک (هر کدام با Symptom/Use/Avoid/Safe steps/Verify) به دو بخش خلاصه شد:
`Technique selection` (کدام تکنیک برای کدام بو) و `Technique execution safety` (قواعد ایمنی
مشترک همهٔ تکنیک‌ها). گام‌های کلی هر تکنیک تکرار نشدند چون بلوک باید سیاست اجرایی باشد،
نه آموزش گام‌به‌گام.

## ۳. چه چیزی عمداً نگرفتیم (تکرار با بلوک‌های موجود)

| محتوا | چرا نه | کجاست |
|---|---|---|
| «گام‌های کوچک و ایمن»، «اول کار کند بعد درست»، «بازطراحی بزرگ نکن»، «کد را تمیزتر واگذار کن» | بلوک ۹۰ مالک فرایند تغییر است | `90-construction-contract.md` §12 |
| فهرست تک‌خطیِ نشانه‌های پیچیدگی (نام گمراه‌کننده، کد مرده، coupling، …) | بلوک ۹۰ آن را از Clean Code/Code Complete دارد؛ ۹۷ فقط «محرک → درمان → استثنا» را اضافه می‌کند و در §11 صریحاً به آن ارجاع می‌دهد | `90-construction-contract.md` §10 |
| «هر گام behaviour-preserving»، «اول characterization test»، «rename قبل از restructure»، «verification + rollback per step» | بلوک ۹۶ مالک قواعد پلن تغییر است | `96-change-findings.md` §3 |
| طبقه‌بندی بدهی فنی (۱۳ کلاس) و قاعدهٔ بررسی repository-wide قبل از اعلام dead | بلوک ۶۵ مالک آن است؛ ۹۷ فقط قواعد عملیاتی (منشأ بدهی، بازپرداخت تدریجی، ممنوعیت پروژهٔ cleanup آینده) را دارد | `65-debt.md` |
| ORM، تراکنش، لایه‌بندی، aggregate و repository | بلوک‌های ۹۲/۹۳/۹۴ مالک آن‌ها هستند | `92-` · `93-` · `94-` |
| کیفیت تست و تست بی‌ادعا | بلوک ۹۰ و ۹۲ مالک آن‌ها هستند | `90-construction-contract.md` §11 · `92-` §10 |
| DRY و orthogonality | بلوک ۹۵ مالک آن‌ها هستند | `95-pragmatic-contract.md` |

## ۴. کجا وصل شده

| جایگاه | ۹۷ (رفکتورینگ) |
|---|---|
| `Clean Code & Construction Review.md` | ✅ |
| `Software Design & Architecture Review.md` | ✅ |
| `Technical Debt & Modernization Audit.md` | ✅ |
| `Domain Model & Context Review.md` | ✅ |
| `Testing & Quality Assurance Audit.md` | ✅ |

`Data & Database Integrity Audit` و `API & Integration Contract Audit` عمداً آن را نگرفتند:
موضوع narrowly مشخصی دارند (داده و قرارداد) و `94-` را گرفته‌اند.

## ۵. بازتولید

```bash
python3 scripts/compose_persona.py --all
python3 scripts/build_skills.py
python3 scripts/validate_skills.py
python3 scripts/validate_personas.py
```

## ۶. اضافه‌کردن قانون تازه

1. قانون را در `composites/blocks/97-refactoring-contract.md` بنویس (یک بار).
2. بلوک را به `blocks` compositeهای مرتبط اضافه کن.
3. بازتولید کن.
4. اگر قانون با بلوک دیگری هم‌پوشانی داشت، از بلوک دیگر **حذف**ش کن — منبع یگانه حفظ شود.
