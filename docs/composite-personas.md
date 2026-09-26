# Persona ترکیبی (Composite Persona) چطور بسازیم

> Personaهای ترکیبی همان master promptهای ریشهٔ مخزن هستند:
> `Forensic Codebase Review & Audit.md`، `Architecture Review & Architecture Audit.md`،
> `codebase-integrity-audit-protocol.md`، `Execution Plan Generator.md` و
> `Production Readiness & Reliability Audit.md`.
> تفاوتشان با personaهای `prompts/` در یک چیز است: **یک نقش نیستند، چند نقش را همزمان اجرا می‌کنند.**

---

## ۱. Persona ترکیبی چیست؟

| | Persona نقش (`prompts/**`) | Persona ترکیبی (ریشه) |
|---|---|---|
| هویت | یک عنوان شغلی، یک نوع (ناظر/مجری) | چند نقش به‌عنوان «عدسی» (lens) |
| قرارداد | ۲۹ بخش استاندارد Master | پروتکل آزاد، فازمحور |
| مأموریت | `PrimaryGoal` تک | مأموریت واحدِ مرکب (مثلاً «ممیزی forensic کدبیس») |
| خروجی | گزارش/کد مطابق قرارداد | گزارش چندبخشی با Coverage Matrix و Quality Gate |
| طول | ~۵۵۰ خط | ~۳۰۰ تا ~۸۰۰ خط |
| بازتولید | `generate_personas.py` | `compose_persona.py` (از بلوک + spec) |

قانون بنیادین: **ترکیبی ≠ چسباندن چند پرامپت.** اگر دو persona را پشت‌سرهم بچسبانی،
مدل یا یکی را dominate می‌کند یا در تناقض می‌افتد. Persona ترکیبی باید:

1. **یک مأموریت واحد** داشته باشد که بالاتر از همهٔ lensهاست.
2. هر lens را **مستقل** اعمال کند (هر یافته برچسب lens دارد).
3. برای تناقض‌ها **قانون پیشتازی (precedence)** داشته باشد.
4. **یک پروتکل مشترک** (فازها، شواهد، پوشش، قالب یافته، Quality Gate) داشته باشد.

---

## ۲. آناتومی یک Persona ترکیبی (۷ لایه)

```
# <Title> — Master Prompt (vN)          ← لایه ۰: عنوان + نسخه
## 1. INPUTS                            ← لایه ۱: ورودی‌های اجباری قبل از شروع
## 2. MISSION + Lens Table              ← لایه ۲: مأموریت واحد + جدول عدسی‌ها
## 3. PRIME DIRECTIVE — ZERO ASSUMPTIONS← لایه ۳: قواعد غیرقابل‌مذاکره (شواهد)
## 4. SCOPE / MISSING ARTIFACTS         ← لایه ۴: دامنه و پروتکل «چیزهای ناشناخته»
## 5. AUDIT PROTOCOL (Phases 0..N)      ← لایه ۵: ترتیب اجرا + ضدِ نمونه‌برداری
## 6. LENS SWEEP + PRECEDENCE           ← لایه ۶: اجرای مستقل lensها + حل تعارض
## 7. COVERAGE MATRIX                   ← لایه ۷: کنترل پوشش (ضدِ «کامل بررسی شد» دروغین)
## 8. FINDINGS (severity/confidence)    ← لایه ۸: قالب یافته + اولویت‌بندی
## 9. <Domain extras>                   ← لایه ۹: بخش‌های اختصاصی این ترکیبی
## 10. FINAL REPORT STRUCTURE           ← لایه ۱۰: ساختار گزارش
## 11. BEHAVIOURAL RULES + QUALITY GATE ← لایه ۱۱: رفتار و گیت نهایی
## Appendix C — Source Personas          ← ردیابی: از کدام personaها ساخته شده
```

---

## ۳. بلوک‌های آماده (`composites/blocks/`)

هر بلوک یک تکهٔ پروتکلِ آزمون‌شده است و در چند composite استفاده می‌شود:

| بلوک | محتوا | اجباری؟ |
|---|---|---|
| `00-header.md` | عنوان، راهنما، بلوک INPUTS، خلاصهٔ ترتیب اجرا | ✅ |
| `10-prime-directive.md` | مأموریت، جدول lensها، «هیچ حدسی»، استاندارد شواهد، ممنوعیت زبان | ✅ |
| `20-scope-artifacts.md` | چه چیزی شاهد است، دامنه، پروتکل artifactهای گم‌شده | ✅ |
| `30-protocol.md` | نردبان عمق، ضدِ نمونه‌برداری، فازها، پروتکل ادامه | ✅ |
| `40-lenses.md` | lens sweep، حل تعارض، `{{PRECEDENCE}}` | ✅ |
| `50-coverage.md` | ماتریس پوشش | ✅ |
| `60-findings.md` | راستی‌آزمایی، شدت، اطمینان، قالب یافته، تکراری‌سازی، اولویت | ✅ |
| `70-report.md` | ساختار گزارش نهایی | ✅ |
| `80-quality-gate.md` | قواعد رفتاری + Quality Gate + اصل حاکم | ✅ |

`{{EXTRA_SECTIONS}}`/`insert_before` محل درج بخش‌های اختصاصی spec است (پیش‌فرض: قبل از `80-quality-gate.md`).

**قاعدهٔ شماره‌گذاری:** بلوک‌ها شمارهٔ ثابت دارند تا تنها هم خوانا باشند؛ در composite نهایی
شماره‌ها از نو محاسبه می‌شوند (`## N.` و `### N.M`). به‌همین دلیل **هرگز در متن به شمارهٔ
بخش رجوع نکنید** — همیشه با نام (§«Final Quality Gate»، «Appendix B»).

---

## ۴. فرمت Spec (`composites/<slug>.json`)

```json
{
  "$schema": "composite-persona/v1",
  "slug": "production-readiness-reliability-audit",
  "title": "Production Readiness & Reliability Audit",
  "version": "v1",
  "language": "en",
  "output": "Production Readiness & Reliability Audit.md",
  "description": "<توضیح trigger برای skill — اختیاری>",
  "mission": "<مأموریت واحد، حداقل ۴۰ نویسه>",
  "order": "intake → discovery → … → gated report",
  "inputs": [{"name": "TARGET", "hint": "repository path / URL"}],
  "lenses": ["prompts/audit/release-manager.md", "…"],
  "lens_focus": {"Release Manager": "release gates, rollback, …"},
  "precedence": ["<قانون ۱>", "<قانون ۲>"],
  "blocks": ["00-header.md", "10-prime-directive.md", "…"],
  "insert_before": "80-quality-gate.md",
  "extra_sections": [{"title": "Readiness Gates", "body": "…"}]
}
```

اعتبارسنجی خودکار (`--check`) این‌ها را کنترل می‌کند:
عنوان/مأموریتِ غیرخالی، `inputs` دارای نام، **۲ تا ۱۲ lens** (هر کدام یک persona معتبر و بدون تکرار)،
وجود همهٔ بلوک‌ها، عدم تکرار بلوک، **پر بودن `precedence`**، و حل شدن همهٔ `{{PLACEHOLDER}}`ها.

### placeholderهای مجاز

`{{TITLE}}` `{{VERSION}}` `{{DATE}}` `{{MISSION}}` `{{INPUTS}}` `{{ORDER}}`
`{{LENS_TABLE}}` `{{LENS_COUNT}}` `{{PRECEDENCE}}` `{{EXTRA_SECTIONS}}`

---

## ۵. ساخت و بازتولید

```bash
# فهرست بلوک‌ها و specها
python3 scripts/compose_persona.py --list

# ساخت یک composite
python3 scripts/compose_persona.py --spec composites/production-readiness-reliability-audit.json

# ساخت همه + فقط اعتبارسنجی (بدون نوشتن)
python3 scripts/compose_persona.py --all
python3 scripts/compose_persona.py --all --check
```

خروجی پیش‌فرض در ریشهٔ مخزن نوشته می‌شود (`output` در spec)، مثل سایر master promptها.

---

## ۶. چک‌لیست کیفیت پیش از انتشار یک Composite

- [ ] مأموریت **یک** جملهٔ مرکب است و به هیچ lens واحدی نسبت داده نمی‌شود.
- [ ] ۲ تا ۱۲ lens، همه از `prompts/` و همه واقعاً لازم (نه تزئینی).
- [ ] هر lens در جدول یک «focus» مشخص و متمایز دارد.
- [ ] `precedence` حداقل یک قانون حل تعارض دارد (داده/امنیت > سرعت، بازیافت‌پذیری > قابلیت …).
- [ ] قواعد شواهد («هیچ حدس، هیچ ساخت، شاهد verbatim») موجود است.
- [ ] پروتکل فازمحور + پروتکل «ادامه در کدبیس بزرگ» موجود است.
- [ ] ماتریس پوشش اجباری است و «ادعای کامل‌بودن» به آن گره خورده.
- [ ] قالب یافته، شدت و اطمینان از هم جدا هستند.
- [ ] Quality Gate نهایی با چک‌باکس‌های قابل بررسی وجود دارد.
- [ ] هیچ ارجاع عددی به بخش‌ها نیست (فقط نام).
- [ ] Appendix منبعِ lensها ثبت شده (ردیابی به personaهای مبدأ).

---

## ۷. مثال: `Production Readiness & Reliability Audit`

سبک عملی:

```bash
python3 scripts/compose_persona.py --list
python3 scripts/compose_persona.py --spec composites/production-readiness-reliability-audit.json
```

نتیجه: یک master prompt با ۷ عدسی (Release Manager، QA Lead، Security Architect، SRE،
DevOps Engineer، Observability Engineer، DBA)، ۱۲ «گیت آمادگی» (Rollback/Restore/Migration/Deploy/…)
که هر کدام `PASS/FAIL/BLOCKED/NOT_APPLICABLE` می‌گیرند، و ۶ پاس تخصصی
(failure-mode، recovery، observability، data، release/ops، cost).

برای ساخت composite تازه:

1. `cp composites/production-readiness-reliability-audit.json composites/<slug>.json`
2. `title`/`mission`/`inputs`/`lenses`/`lens_focus`/`precedence`/`extra_sections` را بنویس.
3. `python3 scripts/compose_persona.py --spec composites/<slug>.json`
4. به skill تبدیلش کن: `python3 scripts/build_skills.py` (راهنما: [`persona-skills.md`](persona-skills.md))
