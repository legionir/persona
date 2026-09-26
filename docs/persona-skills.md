# Persona را چطور به Skill تبدیل کنیم

> Skill = شکلِ «قابل بارگذاری» یک persona: یک `SKILL.md` کوچک که مدل وقتی تسک مطابقت
> کرد می‌خواند، به‌علاوهٔ متن کامل persona به‌عنوان مرجع (progressive disclosure).

---

## ۱. چرا Skill؟ (و چرا فقط کپیٔ پرامپت نیست)

پرامپت persona بین ۵۰۰ تا ۸۰۰ خط است. اگر همهٔ آن را همیشه در کانتکست بگذاری:
هزینه می‌برد، توجه را رقیق می‌کند و عملاً هیچ‌وقت «فعال» نمی‌شود. Skill این مشکل را با
دو لایه حل می‌کند:

| لایه | فایل | اندازه | چه وقت خوانده می‌شود |
|---|---|---|---|
| Trigger | `SKILL.md` (frontmatter) | ~۳۰۰ نویسه | مدل از description تصمیم می‌گیرد skill لازم است یا نه |
| هستهٔ عملیاتی | `SKILL.md` (body) | ~۱۰۰–۳۰۰ خط | وقتی skill صدا زده شد |
| مرجع کامل | `references/<persona>.md` | کل پرامپت | فقط وقتی به جزئیات قرارداد نیاز شد |

پس تبدیل به skill یعنی **تقطیرِ هستهٔ عملیاتی + نگه‌داشتن متن کامل به‌عنوان مرجع**، نه کپی خام.

---

## ۲. آناتومی خروجی

```
skills/
├── README.md                 # فهرست فارسی همهٔ skillها
├── index.json                # متادیتای ماشین‌خوان (شبهٔ personas.json)
├── backend-developer/
│   ├── SKILL.md              # frontmatter + هستهٔ عملیاتی
│   └── references/persona.md # متن کامل persona (برای personaهای نقش)
├── forensic-codebase-review-audit/
│   ├── SKILL.md
│   └── references/forensic-codebase-review-audit.md   # master prompt کامل
└── …
```

### Frontmatter

```yaml
---
name: "backend-developer"                 # حروف کوچک/عدد/خط تیره، ≤ ۶۴ نویسه، = نام پوشه
description: "Persona «Backend Developer» (مجری) …"   # ≤ ۱۰۲۴ نویسه؛ ترایگر skill است
metadata:
  version: "1"
  type: "EXECUTOR"          # یا SUPERVISOR / COMPOSITE
  typeLabel: "مجری"
  domain: "Software"
  seniority: "Mid"
  source: "prompts/implementation/backend-developer.md"
  language: "fa"
---
```

### بدنهٔ `SKILL.md` برای persona نقش

`Trigger` → مأموریت و معیار موفقیت → اختیار و مرزها → ورودی‌ها → پیش‌شرط‌ها → دامنه →
ابزارها → شواهد → ریسک → KPI → گام‌های اجرایی → قواعد تصمیم → Quality Gate → قواعد مطلق →
ساختار گزارش/خروجی → تحویل و Escalation → رجوع به `references/`.

### بدنهٔ `SKILL.md` برای persona ترکیبی

`Trigger` (از مأموریت) → ورودی‌های اجباری → قواعد غیرقابل‌مذاکره → فازهای اجرا →
جدول شدت → قالب یافته → ساختار گزارش → Quality Gate → اصل حاکم → رجوع به `references/`.

---

## ۳. دستورات

```bash
# ساخت همهٔ skillها (۱۷۰ persona نقش + ۵ composite)
python3 scripts/build_skills.py

# فقط چندتا
python3 scripts/build_skills.py --only backend-developer --only audit-specialist

# فقط یک زیرمجموعه (glob نسبت به ریشه)
python3 scripts/build_skills.py --source "prompts/audit/*.md"

# بدون کپیٔ متن کامل (فقط SKILL.md، سبک‌تر)
python3 scripts/build_skills.py --no-bundle

# اعتبارسنجی بدون نوشتن چیزی
python3 scripts/validate_skills.py
python3 scripts/build_skills.py --check
```

ساختارهای بی‌ریشه (skillهایی که personaشان حذف شده) در اجرای کامل خودکار prune می‌شوند.

---

## ۴. اعتبارسنجی (`validate_skills.py`)

| بررسی | چرا |
|---|---|
| وجود frontmatter و `name` | بدون آن skill بارگذاری نمی‌شود |
| `name` = نام پوشه، `^[a-z0-9-]+$`، ≤۶۴ | قرارداد Agent Skills |
| `description` غیرخالی و ≤۱۰۲۴ | ترایگر؛ بلندتر = بی‌اثر |
| لینک‌های داخلی `SKILL.md` سالم باشند | رجوع شکسته = مرجع گم‌شده |
| `SKILL.md` ≤ ۳۰۰ خط (نرم) | وگرّنه progressive disclosure بی‌معنا می‌شود |
| `index.json` هم‌خوان با پوشه‌ها | کاتالوگ دروغین نساز |

خروجی موفق: `ALL CHECKS PASSED.`

---

## ۵. نصب و استفاده

### Claude Code (پروژه)

```bash
mkdir -p .claude/skills
cp -r skills/backend-developer .claude/skills/
# یا همه:
for d in skills/*/; do cp -r "$d" .claude/skills/; done
```

سپس کافی است تسک را بنویسی («یک ممیزی forensic روی این ریپو بگیر»)؛ مدل از روی
`description` تصمیم می‌گیرد کدام skill را صدا بزند.

### Claude.ai / API

محتوای پوشهٔ skill را در محیط skill وارد کن (یا درخواست را با محتوای `SKILL.md` +
`references/` بفرست). برای API، هر skill یک `container` با فایل‌های خودش است.

### نکتهٔ مهم برای personaهای «ناظر»

personaهای ناظر read-only هستند؛ در متن skill هم گفته شده. اگر می‌خواهی سخت‌گیرانه اجرا شود،
در تنظیمات محیط اجازهٔ نوشتن را محدود کن (skill به‌تنهایی محدودیت ابزار ایجاد نمی‌کند).

---

## ۶. قاعدهٔ طلایی نوشتن `description` خوب

description ترایگر است، نه معرفی. سه جزء لازم است:

1. **چه کسی/چه چیزی** — «Persona «Backend Developer» (مجری) در حوزه Software».
2. **چه کاری** — «پیادهسازی Backend … خروجی: Backend Code, Tests, API Docs».
3. **چه وقت** — «استفاده کن وقتی … / Use when …».

خوب ✅: «… Rollback/Restore/Migration … قبل از انتشار، برای آمادگی production.»
بد ❌: «یک persona بسیار کامل و حرفه‌ای برای توسعهٔ بک‌اند.» (هیچ تریگری ندارد)

محدودیت‌ها: `name` ≤ ۶۴ نویسه، `description` ≤ ۱۰۲۴ نویسه.

---

## ۷. عیب‌یابی

| مشکل | راه‌حل |
|---|---|
| skill صدا زده نمی‌شود | `description` را با «چه وقت» بازنویسی کن؛ از کلمات کلیدی تسک استفاده کن |
| مدل جزئیات قرارداد را نمی‌داند | در `SKILL.md` صراحتاً به `references/…md` رجوع بده (همیشه آخر فایل هست) |
| `SKILL.md` بیش از ۳۰۰ خط شد | جزئیات را به `references/` منتقل کن (اسکریپت هشدار می‌دهد) |
| `validate_skills.py` خطای broken link داد | اسکریپت را دوباره اجرا کن؛ لینک‌ها از نام فایل مرجع ساخته می‌شوند |
| composite تازه ساخته‌ام ولی skill ندارد | `python3 scripts/build_skills.py` (ریشهٔ مخزن را می‌گردد) |

---

## ۸. گردش کار کامل (نقش → ترکیبی → skill)

```bash
# ۱) personaهای نقش (در صورت تغییر README/generator)
python3 scripts/generate_personas.py
python3 scripts/build_metadata.py

# ۲) ساخت/بازساخت composite
python3 scripts/compose_persona.py --all

# ۳) تبدیل همهٔ personaها به skill
python3 scripts/build_skills.py

# ۴) اعتبارسنجی
python3 scripts/validate_personas.py
python3 scripts/validate_skills.py
```
