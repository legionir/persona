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

### بلوک‌های عمق (اختیاری — برای ممیزی‌های forensic)

این بلوک‌ها از نقطهٔ قوتِ `Forensic Codebase Review & Audit.md` استخراج شده‌اند و هر جا بخواهی
ممیزی «فایل‌به‌فایل و خط‌به‌خط» واقعی باشد (نه خلاصهٔ سطحی) اضافه‌شان کن:

| بلوک | محتوا |
|---|---|
| `25-file-by-file.md` | ۲۸ موردی که برای **هر فایل** باید تعیین شود (side effects، state mutation، resource، dead code، …) |
| `35-line-level.md` | ردیابی توابع، کلاس‌های باگ هدف، نواطق پرخطر (auth، پول، migration، concurrency، …) |
| `45-cross-file.md` | تحلیل بین‌فایلی + بازسازی ورکفلو (موفق/شکست) + جریان داده |
| `55-specialized.md` | ۱۲ دامنهٔ ممیزی تخصصی (security، error، concurrency، DB، API، testing، architecture، config، deps، perf، observability، build/deploy) |
| `65-debt.md` | بدهی فنی (۱۳ کلاس) + کد مرده و مشکوک + قاعدهٔ بررسی repository-wide قبل از اعلام dead |
| `90-construction-contract.md` | قرارداد ساخت کد: ادغام یگانهٔ Clean Code + Code Complete (نام‌گذاری، روال، کامنت، داده، جریان کنترل، خطا، بوها، تست، رفکتور، همزمانی، گیت بازبینی) |
| `91-design-depth-contract.md` | قرارداد عمق طراحی: ادغام یگانهٔ A Philosophy of Software Design (پیچیدگی، عمق ماژول، پنهان‌سازی اطلاعات، رابط، استراتژیک در مقابل تاکتیکی، حذف استثناها، کشیدن پیچیدگی به پایین، تجزیهٔ زمانی، ترکیب/جدایی، طراحی comments-first) |
| `92-clean-architecture-contract.md` | قرارداد مرزهای معماری: ادغام یگانهٔ Clean Architecture (قانون وابستگی، مسئولیت لایه‌ها، use case و entity، port و adapter، ساختار بر پایهٔ use case، قواعد کامپوننت، هزینهٔ مرز، تست از مسیر مرز، الگوهای ممنوع) |
| `93-domain-model-contract.md` | قرارداد مدل دامنه: ادغام یگانهٔ DDD (زبان مشترک، bounded context و context map، subdomain و distillation، entity/value object/aggregate، domain service و specification، repository/factory، domain event و event sourcing، ترجمه در مرزها، DDD انتخاب‌محور) |
| `94-enterprise-patterns-contract.md` | قرارداد الگوهای سازمانی: ادغام یگانهٔ PoEAA (انتخاب الگوی منطق کسب‌وکار، الگوی persistence، Unit of Work/Identity Map/Lazy Load، الگوهای ORM، قفل آفلاین و مرز تراکنش، الگوهای presentation، الگوهای پایه) |
| `95-pragmatic-contract.md` | قرارداد پراگماتیک: ادغام یگانهٔ The Pragmatic Programmer (DRY یعنی دانش نه متن، orthogonality، tracer bullet، خودکارسازی، حلقهٔ بازخورد، قرارداد و منابع، ارتباطات) |
| `96-change-findings.md` | شواهد الزامی برای هر یافتهٔ «تغییر» + قواعد پلن تغییر (severity را به روبیک پایهٔ Findings map می‌کند، دوباره نمی‌نویسد) |
| `97-refactoring-contract.md` | قرارداد رفکتورینگ: ادغام یگانهٔ Refactoring.Guru (جداسازی از کار feature/bug، گام‌های کوچک، راستی‌آزمایی و شرط توقف، قاعدهٔ سه، شش دستهٔ بو با محرک→درمان→جایگزین، قواعد استثنای بو، انتخاب و ایمنی تکنیک، آنتی‌الگوهای تصمیم، ورکفلو agent) |

ترتیب پیشنهادی یک ممیزی forensic کامل:

```
00 → 10 → 20 → 30 → 40 → 25 → 35 → 45 → 55 → [65] → 50 → 60 → [extra] → 80
```

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
- [ ] اگر موضوع ممیزی به کیفیت ساخت کد مربوط است، بلوک `90-construction-contract.md` include شده
      (و بلوک دیگری قواعد مشابه را کپی نمی‌کند).
- [ ] اگر موضوع ممیزی به کیفیت ساخت کد مربوط است، بلوک `90-construction-contract.md` include شده
      (و بلوک دیگری قواعد مشابه را کپی نمی‌کند).
- [ ] اگر موضوع ممیزی به طراحی/معماری مربوط است، بلوک‌های `91-` و/یا `92-` include شده‌اند.
- [ ] اگر موضوع ممیزی به مدل دامنه مربوط است، بلوک `93-domain-model-contract.md` include شده
      (و قواعد لایه/وابرسی که در `92-` هستند دوباره نوشته نشده‌اند).
- [ ] اگر خروجی composite «تغییر» پیشنهاد می‌دهد، بلوک `96-change-findings.md` include شده است
      (به‌جای نوشتن دوبارهٔ شواهد یافته در `extra_sections`).
- [ ] اگر composite تغییر ساختاری/رفکتورینگ پیشنهاد می‌دهد، بلوک `97-refactoring-contract.md` include شده
      (و فرایند تغییر و قواعد پلن از `90-`/`96-` تکرار نشده‌اند).

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

## ۷. فهرست Compositeهای مخزن

| Composite | عدسی‌ها | تمرکز |
|---|---|---|
| `forensic-codebase-review-audit` | — | ممیزی forensic کدبیس (فایل‌به‌فایل، خط‌به‌خط، بدون حدس) |
| `clean-code-construction-review` | ۶ | کیفیت ساخت کد بر اساس قرارداد Clean Code + Code Complete |
| `software-design-architecture-review` | ۶ | عمق طراحی و جهت وابستگی‌ها بر اساس Philosophy of Software Design + Clean Architecture |
| `domain-model-context-review` | ۶ | زبان مشترک، bounded context و مدل دامنه بر اساس DDD (Evans / Vernon) |
| `architecture-review-architecture-audit` | — | بازبینی معماری با Tier/Size و سنجش ۰–۱۰۰ |
| `codebase-integrity-audit-protocol` | — | یکپارچگی و ورکفلو، فازبه‌فاز و قابل ادامه (P0–P10) |
| `execution-plan-generator` | — | تبدیل تسک بزرگ به پلن اجرایی فازبه‌فاز |
| `production-readiness-reliability-audit` | ۷ | آمادگی production: Rollback/Restore/Migration/Observability/SLO |
| `forensic-security-threat-audit` | ۸ | سطح حمله و مرزهای اعتماد؛ exploitable vs theoretical |
| `data-database-integrity-audit` | ۶ | ثبات داده، migration، تراکنش، backup/restore |
| `api-integration-contract-audit` | ۶ | قرارداد API و یکپارچه‌سازی؛ drift مستندات ↔ پیاده‌سازی |
| `ai-agent-system-audit-hardening` | ۶ | سیستم‌های LLM/Agent: ابزارها، مجوزها، eval، مسیرهای ناامن |
| `performance-scalability-audit` | ۶ | گلوگاه‌ها، سقف منابع، رفتار در ۱۰x و ۱۰۰x |
| `technical-debt-modernization-audit` | ۶ | بدهی فنی بر اساس هزینهٔ تغییر؛ مسیر مهاجرت تدریجی |
| `testing-quality-assurance-audit` | ۶ | آنچه سوئیت واقعاً اثبات می‌کند؛ تست‌های بی‌ادعا و شکاف پوشش |
| `incident-forensic-review-postmortem` | ۶ | بازسازی تایم‌لاین، زنجیرهٔ علّی، شکاف detection و recovery |
| `cloud-infrastructure-audit` | ۷ | IaC و drift، exposure، IAM، secrets، blast radius، هزینه |
| `privacy-compliance-audit` | ۶ | جریان دادهٔ شخصی، کنترل↔شاهد، حقوق داده‌دار، اشتراک با ثالث |

## ۸. ساخت Composite تازه

1. `cp composites/production-readiness-reliability-audit.json composites/<slug>.json`
2. `title`/`mission`/`inputs`/`lenses`/`lens_focus`/`precedence`/`extra_sections` را بنویس.
3. در `blocks` ترتیب را انتخاب کن (برای ممیزی forensic بلوک‌های `25/35/45/55` را هم بیاور).
4. `python3 scripts/compose_persona.py --spec composites/<slug>.json`
5. به skill تبدیلش کن: `python3 scripts/build_skills.py` (راهنما: [`persona-skills.md`](persona-skills.md))
