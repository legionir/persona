# قرارداد سیستم طراحی فرانت‌اند — استخراج از Doctrine of Visual & Interaction Consistency

این سند توضیح می‌دهد قواعد «Unified Design System Doctrine» چگونه به **یک** قرارداد واحد تبدیل
شده، کجا زندگی می‌کند، و چطور به personaها و skillها وصل می‌شود.

> خودِ قواعد اینجا تکرار **نشده‌اند**. منبع یگانه:
> [`composites/blocks/98-frontend-design-system-contract.md`](../composites/blocks/98-frontend-design-system-contract.md)
> (به انگلیسی، هم‌سبک با بقیهٔ بلوک‌ها). این سند فقط نقشهٔ استخراج و نحوهٔ اتصال است.

---

## ۱. چرا این بلوک لازم شد

تا این لحظه هیچ بلوکی دربارهٔ **لایهٔ نمایش** حرف نمی‌زد، جز دو مورد پراکنده:

- `94-enterprise-patterns-contract.md` §9 می‌گوید «کد presentation ورودی/رندر/ترنسپورت را handling
  می‌کند و قانون کسب‌وکار در view نباید باشد» — یعنی *جداسازی مسئولیت*.
- `97-refactoring-contract.md` §11 بوهای «Duplicate Code» و «Speculative Generality» را دارد —
  یعنی *درمان تکرار*.

اما چیزی که مخزن نداشت: **سیستم بصریِ درونِ لایهٔ presentation** — توکن‌ها، کتابخانهٔ مشترک
کامپوننت، shell و template صفحه، پوشش stateها، و اینکه بی‌نظمی بصری یک **defect** است نه سلیقه.

## ۲. نقشهٔ استخراج

| بخش بلوک ۹۸ | بخش سند منبع |
|---|---|
| `Visual inconsistency is a defect` | Purpose + Primary Directive + Final Instruction |
| `Design tokens are the single source of visual truth` | The Single Source of Truth: Design Tokens (۹ قانون) |
| `One concept, one component` | Component Library: One Concept, One Component (۷ قانون) |
| `Layout and page shell consistency` | Layout & Page Shell Consistency |
| `State consistency` | State Consistency (۷ state) |
| `Forms and inputs` | Forms & Input Consistency |
| `Tables, lists, and collections` | Tables, Lists & Collections Consistency |
| `Typography hierarchy` | Typography Hierarchy |
| `Colour usage discipline` | Color Usage Discipline |
| `Iconography, motion, and responsiveness` | Iconography + Motion & Animation Consistency + Responsive & Breakpoint Consistency |
| `Accessibility and theming consistency` | Accessibility Consistency + Theming Consistency |
| `Naming and file structure` | Naming & File Structure Conventions |
| `Enforce it mechanically` | Anti-Duplication Enforcement |
| `Pre-build checklist` | Mandatory Pre-Build Checklist |
| `Frontend review gate` | Review Checklist |

### چه چیزی عمداً نگرفتیم

| محتوا | چرا نه | کجاست |
|---|---|---|
| «قانون کسب‌وکار در view/controller نباشد»، «مدل presentation می‌تواند با مدل دامنه فرق کند»، الگوهای MVC/Page Controller/Front Controller/Template View | بلوک ۹۴ مالک جداسازی presentation از domain و انتخاب الگوی presentation است | `94-enterprise-patterns-contract.md` §9 |
| «کامپوننت تکراری = بوِ Duplicate Code»، مسیر Extract/Inline برای حذف آن | بلوک ۹۷ مالک کاتالوگ بو و درمان است؛ ۹۸ فقط می‌گوید کدام مفهوم باید یکی شود | `97-refactoring-contract.md` §11 |
| نام‌گذاری دامنهٔ کسب‌وکار (ubiquitous language) | بلوک ۹۳ مالک آن است؛ ۹۸ نام‌گذاری *کامپوننت و فایل* را اضافه می‌کند و صریحاً به ۹۳ ارجاع می‌دهد | `93-domain-model-contract.md` §2 |
| «کد باید قابل درک برای خوانندهٔ بعدی باشد» / obviousness | بلوک ۹۱ و ۹۵ مالک آن‌ها هستند | `91-` §12 · `95-` §8 |
| کیفیّت تست و تست بی‌ادعا | بلوک ۹۰ و ۹۲ مالک آن‌ها هستند؛ «visual regression testing» در ۹۸ فقط به‌عنوان **مکانیزم اجبار** آمده، نه به‌عنوان راهنمای تست | `90-` §11 · `92-` §10 |
| قواعد نوشتن کد (روال، کامنت، داده) | بلوک ۹۰ | `90-construction-contract.md` |

## ۳. کجا وصل شد

| جایگاه | ۹۸ (سیستم طراحی فرانت‌اند) |
|---|---|
| `Frontend & Design System Review.md` (persona ترکیبی تازه) | ✅ |
| `Software Design & Architecture Review.md` | ✅ |

بقیهٔ compositeها می‌توانند با اضافه‌کردن `"98-frontend-design-system-contract.md"` به `blocks` در
spec خودشان include کنند.

## ۴. persona ترکیبی تازه

`Frontend & Design System Review` (۶ عدسی: Frontend Developer، Design System Designer،
UI Designer، Accessibility Specialist، Mobile Developer، Full-Stack Developer) با دو بخش اختصاصی:

- **Design System Register** — یک ردیف per توکن/کامپوننت/template: مکان canonical، variantها،
  stateهای پوشش‌داده‌شده، تعداد استفاده، پیاده‌سازی‌های موازی، و token bypassها.
- **Frontend Consistency Passes** — ۱۲ پاس با پیشوند ID جدا (`TKN-` توکن، `CMP-` تکرار کامپوننت،
  `API-` prop API، `SHL-` shell/template، `STT-` پوشش state، `FRM-` فرم، `TBL-` جدول/لیست،
  `TYG-` تایپوگرافی/رنگ/آیکون/موشن، `RSP-` ریسپانسیو/دسترس‌پذیری/تم، `NAM-` نام‌گذاری/ساختار،
  `ENF-` اجبار مکانیکی، `DRF-` drift).

## ۵. بازتولید

```bash
python3 scripts/compose_persona.py --all
python3 scripts/build_skills.py
python3 scripts/validate_skills.py
python3 scripts/validate_personas.py
```

## ۶. اضافه‌کردن قانون تازه

1. قانون را در `composites/blocks/98-frontend-design-system-contract.md` بنویس (یک بار).
2. بلوک را به `blocks` compositeهای مرتبط اضافه کن.
3. بازتولید کن.
4. اگر قانون با بلوک دیگری هم‌پوشانی داشت، از بلوک دیگر **حذف**ش کن — منبع یگانه حفظ شود.
