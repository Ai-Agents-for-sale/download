#!/usr/bin/env python3
"""Builds the Zero Work AI mini-site from _src/pages/*.html into static pages at the repo root.

    python3 _src/build.py            → the real site (clean URLs: /faq/)
    python3 _src/build.py --preview  → links end in index.html (for previewing from files)

Every page shares one header, one footer and one <head> from this file, so a link,
a phone number or the legal footer is changed here once. Page bodies live in
_src/pages/<slug>.html. Plain HTML on purpose: AI crawlers do not run JavaScript,
so everything a page says must be in the HTML itself.
"""
import json, os, sys, html
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_src", "pages")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else ROOT
PREVIEW = "--preview" in sys.argv
SITE = "https://app.zerowork-media.com"
TODAY = date.today().isoformat()

IOS = "https://apps.apple.com/il/app/id6799529635"
ANDROID = "https://play.google.com/store/apps/details?id=com.zeroworkai.app"
PHONE = "050-9257065"
EMAIL = "aiagentsforsale@gmail.com"
COMPANY = "Zero Work LTD"
COMPANY_ID = "517268801"
ADDRESS = "שדרות ירושלים 18, אשדוד"

# path, slug, title (<title>), h1, description, lead, breadcrumb label, in sitemap
PAGES = [
    ("", "home", "Zero Work AI · סוכן תוכן בעברית לעסקים", None,
     "Zero Work AI (זירו וורק) היא אפליקציה ישראלית שמכינה לעסק תוכן לרשתות החברתיות לשבוע מראש, בעברית: פוסטים, קרוסלות, סטוריז וסרטונים. אתם מאשרים, וזה מתפרסם לכל הרשתות.",
     None, "ראשי"),
    ("how-it-works/", "how-it-works", "איך Zero Work AI עובדת · מהשאלון ועד הפרסום", "איך זה עובד",
     "שלב אחרי שלב: שיחת היכרות, שאלון אפיון, חיבור הרשתות, תוכן לשבוע מראש, אישור ופרסום אוטומטי. כך עובד סוכן התוכן של Zero Work AI.",
     "מהשיחה הראשונה ועד שהתוכן עולה לרשתות, כל מה שקורה בדרך ומה התפקיד שלכם בכל שלב.", "איך זה עובד"),
    ("features/", "features", "היכולות של Zero Work AI · תוכן, עיצוב, וידאו ופרסום", "מה הסוכן עושה",
     "כל היכולות של Zero Work AI: תוכן שבועי אוטומטי, קרוסלות וסטוריז בעיצוב המותג, עריכת וידאו עם כתוביות בעברית, ניתוח מתחרים ופרסום לחמש רשתות.",
     "סוכן אחד שמתכנן, כותב, מעצב, עורך ומפרסם. אלה היכולות שלו, כל אחת עם הסבר מלא.", "יכולות"),
    ("features/weekly-content/", "weekly-content", "תוכן שבועי אוטומטי לעסק · Zero Work AI", "תוכן שבועי אוטומטי",
     "Zero Work AI מכינה לעסק תוכן לשבוע שלם מראש: קרוסלות, פוסטים, סטוריז וסרטונים, בנושאים שנבחרים לפי העסק, הלקוחות שלו ומה שעובד עכשיו. אתם מאשרים פעם בשבוע.",
     "בוחרים פעם אחת כמה תכנים בשבוע ובאילו ימים. מאותו רגע, כל שבוע מחכה לכם שבוע מלא של תוכן לאישור.", "תוכן שבועי"),
    ("features/design/", "design", "קרוסלות, פוסטים וסטוריז בעיצוב המותג · Zero Work AI", "קרוסלות, פוסטים וסטוריז",
     "עיצובים מוכנים בצבעי המותג, עם הלוגו והגופן של העסק: קרוסלות, פוסטים, סטוריז, הוכחות חברתיות מהמלצות לקוחות ותמונות AI. כל פרט ניתן לעריכה מהטלפון.",
     "כל תוכן יוצא מעוצב בצבעים, בלוגו ובגופן של העסק, ואפשר לשנות בו כל פרט לפני שהוא עולה.", "עיצוב"),
    ("features/video/", "video", "עריכת וידאו עם כתוביות בעברית · Zero Work AI", "עריכת וידאו וסרטונים קצרים",
     "מעלים סרטון גלם ומקבלים סרטון ערוך עם כתוביות בעברית, בי-רול ומוזיקה. שולחים קישור להרצאה או לפודקאסט ומקבלים קליפים קצרים מוכנים לפרסום.",
     "מצלמים בטלפון, ו-Zero Work AI הופכת את זה לסרטון ערוך שמוכן לרילס, לטיקטוק וליוטיוב.", "וידאו"),
    ("features/competitors/", "competitors", "ניתוח מתחרים ודפוסים ויראליים · Zero Work AI", "ניתוח מתחרים ודפוסים ויראליים",
     "Zero Work AI סורקת את המתחרים של העסק ואת התוכן שעובד בתחום, בארץ ובעולם, ומשתמשת בממצאים כדי לבחור נושאים ופתיחים לתוכן השבועי.",
     "הסוכן בודק מה עובד אצל אחרים בתחום שלכם, ומכניס את מה שלמד ישר לתוכן של השבוע.", "מתחרים"),
    ("features/publishing/", "publishing", "פרסום ותזמון לאינסטגרם, פייסבוק, טיקטוק, יוטיוב ולינקדאין · Zero Work AI", "פרסום ותזמון לכל הרשתות",
     "Zero Work AI מפרסמת ומתזמנת תוכן לאינסטגרם, פייסבוק, טיקטוק, יוטיוב ולינקדאין, כולל תוכן שיצרתם בעצמכם. באפליקציה רואים מה מחכה לאישור, מה מתוזמן ומה פורסם.",
     "תוכן שאושר עולה לבד בזמן שנקבע, לכל הרשתות שחיברתם. אתם רק רואים שזה קרה.", "פרסום"),
    ("features/brand/", "brand", "המותג והקול של העסק · Zero Work AI", "המותג והקול של העסק",
     "איך Zero Work AI לומדת את העסק: שאלון אפיון, צבעי מותג, לוגו, גופנים, הוראות כתיבה ותמונות רקע, ולמידה מהדירוגים שאתם נותנים לתוכן.",
     "כדי שהתוכן ישמע ויראה כמו העסק שלכם, הסוכן לומד אותו מכמה מקורות, וממשיך ללמוד מכל דירוג.", "מותג"),
    ("compare/", "compare", "Zero Work AI מול ChatGPT, Canva, כלי תזמון ומנהלת סושיאל", "Zero Work AI מול האפשרויות האחרות",
     "השוואה עניינית: מה ההבדל בין Zero Work AI לבין עבודה עם ChatGPT ו-Canva, כלי תזמון, כלי כתיבה או מנהלת סושיאל, ומתי כל אפשרות מתאימה.",
     "יש כמה דרכים לנהל תוכן לעסק. כאן מוסבר מה כל אחת נותנת, מה נשאר עליכם, ומתי Zero Work AI היא הבחירה הנכונה.", "השוואות"),
    ("faq/", "faq", "שאלות נפוצות על Zero Work AI", "שאלות נפוצות",
     "תשובות לשאלות הנפוצות על Zero Work AI: למי זה מתאים, אילו רשתות, האם התוכן בעברית, האם משהו מתפרסם בלי אישור, איך מתחילים ועוד.",
     "התשובות הקצרות לשאלות שאנחנו שומעים הכי הרבה.", "שאלות נפוצות"),
    ("about/", "about", "אודות Zero Work AI (זירו וורק)", "אודות Zero Work AI",
     "Zero Work AI (זירו וורק) היא אפליקציה של חברת Zero Work LTD מאשדוד, שבונה סוכן תוכן בעברית לעסקים ישראליים. יותר מ-100 עסקים עובדים איתה היום.",
     "חברה ישראלית שבונה סוכן תוכן בעברית לעסקים קטנים ובינוניים.", "אודות"),
    ("contact/", "contact", "צרו קשר · Zero Work AI", "דברו איתנו",
     "רוצים לשמוע איך Zero Work AI יכולה לנהל את התוכן של העסק שלכם? השאירו פרטים ונחזור אליכם, או התקשרו ל-050-9257065.",
     "השאירו פרטים ונחזור אליכם לשיחת היכרות קצרה, בלי התחייבות.", "צור קשר"),
    ("privacy/", "privacy", "מדיניות פרטיות לאתר · Zero Work AI", "מדיניות פרטיות",
     "מדיניות הפרטיות של אתר Zero Work AI: איזה מידע נאסף בטופס יצירת הקשר, למה, איפה הוא נשמר ומה הזכויות שלכם. האתר אינו משתמש בעוגיות.",
     None, "מדיניות פרטיות"),
    ("terms/", "terms", "תנאי שימוש באתר · Zero Work AI", "תנאי שימוש באתר",
     "תנאי השימוש באתר Zero Work AI.", None, "תנאי שימוש"),
    ("accessibility/", "accessibility", "הצהרת נגישות · Zero Work AI", "הצהרת נגישות",
     "הצהרת הנגישות של אתר Zero Work AI: רמת הנגישות, מה הונגש, מגבלות ידועות ודרכים לפנות אלינו בנושא נגישות.",
     None, "הצהרת נגישות"),
]

NAV = [("how-it-works/", "איך זה עובד"), ("features/", "יכולות"), ("compare/", "השוואות"), ("faq/", "שאלות נפוצות"), ("about/", "אודות")]

FEATURES = [
    ("features/weekly-content/", "calendar", "תוכן שבועי אוטומטי", "שבוע שלם של קרוסלות, פוסטים, סטוריז וסרטונים מחכה לאישור שלכם, בנושאים שנבחרו לפי העסק ולפי מה שעובד עכשיו."),
    ("features/design/", "layers", "קרוסלות, פוסטים וסטוריז", "עיצובים בצבעי המותג, עם הלוגו והגופן שלכם. אפשר להחליף תמונה, צבע, טקסט ופריסה ישר מהטלפון."),
    ("features/video/", "video", "עריכת וידאו", "מסרטון גלם לסרטון ערוך עם כתוביות בעברית, בי-רול ומוזיקה, ומהרצאה ארוכה לקליפים קצרים."),
    ("features/competitors/", "radar", "ניתוח מתחרים", "הסוכן סורק את המתחרים ואת התוכן הוויראלי בתחום, בארץ ובעולם, ומכניס את מה שעובד לתוכן שלכם."),
    ("features/publishing/", "send", "פרסום לכל הרשתות", "אינסטגרם, פייסבוק, טיקטוק, יוטיוב ולינקדאין, בזמנים שנקבעו. כולל תוכן שיצרתם בעצמכם."),
    ("features/brand/", "palette", "המותג והקול שלכם", "שאלון אפיון, צבעים, לוגו, גופנים והוראות כתיבה, ולמידה מכל דירוג שאתם נותנים לתוכן."),
]

ICONS = {
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "layers": '<path d="M12 3l9 5-9 5-9-5 9-5z"/><path d="M3 13l9 5 9-5"/>',
    "video": '<rect x="3" y="6" width="13" height="12" rx="2.5"/><path d="M16 10l5-3v10l-5-3"/>',
    "radar": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5M11 7v4l2.5 2.5"/>',
    "send": '<path d="M21 3L10 14"/><path d="M21 3l-7 18-4-7-7-4 18-7z"/>',
    "palette": '<path d="M12 3a9 9 0 1 0 0 18c1.1 0 2-.8 2-1.9 0-.6-.3-1-.6-1.4-.3-.4-.5-.8-.5-1.3 0-1.1.9-2 2-2H17a4 4 0 0 0 4-4C21 6 17 3 12 3z"/><circle cx="7.5" cy="11" r="1"/><circle cx="10" cy="7" r="1"/><circle cx="15" cy="7.5" r="1"/>',
}


def icon(name):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' + ICONS[name] + '</svg>')


def rel(from_path, to_path):
    """Relative link from one page directory to another page (or asset)."""
    depth = from_path.count("/")
    up = "../" * depth
    target = up + to_path
    if PREVIEW and (to_path == "" or to_path.endswith("/")):
        target += "index.html"
    return target or "./"


def stores(p, small=False):
    cls = "foot-stores" if small else "stores"
    return (f'<div class="{cls}">'
            f'<a class="store" data-store="ios" href="{IOS}" rel="noopener"><img src="{rel(p, "assets/img/app-store-he.svg")}" width="161" height="56" alt="להורדה מה-App Store"></a>'
            f'<a class="store" data-store="android" href="{ANDROID}" rel="noopener"><img src="{rel(p, "assets/img/google-play-he.png")}" width="188" height="56" alt="כעת ב-Google Play"></a>'
            '</div>')


def lead_form(p, fid):
    return f'''<form class="lead-form" id="{fid}" novalidate aria-describedby="{fid}-notice">
  <div class="field">
    <label for="{fid}-name">שם מלא <span class="req" aria-hidden="true">*</span></label>
    <input id="{fid}-name" name="name" type="text" autocomplete="name" required aria-required="true" aria-describedby="{fid}-name-error" maxlength="80">
    <span class="error" id="{fid}-name-error" hidden></span>
  </div>
  <div class="field">
    <label for="{fid}-phone">טלפון <span class="req" aria-hidden="true">*</span></label>
    <input id="{fid}-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" dir="ltr" required aria-required="true" aria-describedby="{fid}-phone-error" maxlength="20">
    <span class="error" id="{fid}-phone-error" hidden></span>
  </div>
  <div class="field">
    <label for="{fid}-business">שם העסק או התחום</label>
    <input id="{fid}-business" name="business" type="text" autocomplete="organization" maxlength="120">
  </div>
  <div class="field">
    <label for="{fid}-message">רוצים להוסיף משהו?</label>
    <textarea id="{fid}-message" name="message" maxlength="1000"></textarea>
  </div>
  <div class="hp" aria-hidden="true"><label for="{fid}-website">אתר</label><input id="{fid}-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
  <label class="check" for="{fid}-consent">
    <input id="{fid}-consent" name="marketing_consent" type="checkbox">
    <span>אני מסכים/ה לקבל מ-{COMPANY} דברי פרסומת ועדכונים בוואטסאפ, ב-SMS ובדוא"ל. אפשר לבטל בכל עת בהשבת "הסר" או בפנייה ל-{EMAIL}. (לא חובה, ולא נדרש כדי שנחזור אליכם.)</span>
  </label>
  <p class="form-notice" id="{fid}-notice">שדות המסומנים ב-<span aria-hidden="true">*</span><span class="sr-only">כוכבית</span> הם חובה למשלוח הטופס. מסירת הפרטים אינה חובה לפי חוק והיא תלויה ברצונכם, אבל בלי שם וטלפון לא נוכל לחזור אליכם. בלחיצה על "שליחה" אתם מבקשים שנחזור אליכם בטלפון או בוואטסאפ בעניין הפנייה. האחראית על המידע: {COMPANY}, ח.פ. {COMPANY_ID}, {ADDRESS}, טלפון {PHONE}, {EMAIL}. הפרטים ישמשו למענה לפנייה ולהצגת השירות. הם עוברים דרך שרתי Supabase (באוסטרליה) ונשמרים במערכת ניהול הלקוחות Monday.com (שרתים מחוץ לישראל), ולא יימסרו לאף גורם אחר לצורכי שיווק. אתם זכאים לעיין במידע עליכם ולבקש לתקן או למחוק אותו, בפנייה לטלפון או לדוא"ל שלמעלה. פירוט מלא ב<a href="{rel(p, "privacy/")}">מדיניות הפרטיות</a>.</p>
  <button class="btn" type="submit">שליחה</button>
  <p class="form-status" role="status" tabindex="-1" hidden></p>
</form>'''


def header(p, active):
    nav = "".join(
        f'<a href="{rel(p, href)}"{" aria-current=\"page\"" if href == active else ""}>{label}</a>' for href, label in NAV)
    return f'''<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{rel(p, "")}" aria-label="Zero Work AI, לעמוד הראשי"><img class="mark" src="{rel(p, "assets/img/mark-white.png")}" width="40" height="34" alt=""><img class="word" src="{rel(p, "assets/img/wordmark-white.png")}" width="146" height="14" alt=""></a>
    <nav class="nav-desk" aria-label="ראשי">{nav}<a class="btn light" href="{rel(p, "contact/")}">דברו איתנו</a></nav>
    <details class="menu"><summary>תפריט</summary><nav aria-label="ראשי (נייד)">{nav}<a href="{rel(p, "contact/")}">דברו איתנו</a></nav></details>
  </div>
</header>'''


def footer(p):
    feats = "".join(f'<li><a href="{rel(p, h)}">{t}</a></li>' for h, _, t, _ in FEATURES)
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-about">
        <a class="brand" href="{rel(p, "")}" aria-label="Zero Work AI, לעמוד הראשי"><img class="mark" src="{rel(p, "assets/img/mark-white.png")}" width="40" height="34" alt=""><img class="word" src="{rel(p, "assets/img/wordmark-white.png")}" width="146" height="14" alt=""></a>
        <p>Zero Work AI (זירו וורק) היא סוכן תוכן בעברית לעסקים: מכינה תוכן לשבוע מראש, אתם מאשרים, וזה מתפרסם לכל הרשתות.</p>
        {stores(p, small=True)}
      </div>
      <div><h2>יכולות</h2><ul>{feats}</ul></div>
      <div><h2>המוצר והחברה</h2><ul>
        <li><a href="{rel(p, "how-it-works/")}">איך זה עובד</a></li>
        <li><a href="{rel(p, "compare/")}">השוואות</a></li>
        <li><a href="{rel(p, "faq/")}">שאלות נפוצות</a></li>
        <li><a href="{rel(p, "about/")}">אודות</a></li>
        <li><a href="{rel(p, "contact/")}">צור קשר</a></li>
        <li><a href="https://ai-agents-for-sale.github.io/zero-work-ai-app/support/" rel="noopener">תמיכה ללקוחות</a></li>
      </ul></div>
      <div><h2>מידע משפטי</h2><ul>
        <li><a href="{rel(p, "privacy/")}">מדיניות פרטיות</a></li>
        <li><a href="{rel(p, "terms/")}">תנאי שימוש באתר</a></li>
        <li><a href="{rel(p, "accessibility/")}">הצהרת נגישות</a></li>
        <li><a href="https://ai-agents-for-sale.github.io/zero-work-ai-app/legal/terms.html" rel="noopener">תנאי השירות באפליקציה</a></li>
      </ul></div>
    </div>
    <div class="foot-legal">
      <span>© {date.today().year} {COMPANY} · ח.פ. {COMPANY_ID} · {ADDRESS}</span>
      <span>טלפון <a href="tel:+972509257065" dir="ltr">{PHONE}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></span>
      <span>App Store הוא סימן מסחר של Apple Inc. ‏Google Play והלוגו של Google Play הם סימני מסחר של Google LLC.</span>
    </div>
  </div>
</footer>'''


def org_jsonld():
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization", "@id": SITE + "/#org",
                "name": "Zero Work AI", "alternateName": ["זירו וורק", "Zero Work"], "legalName": COMPANY,
                "url": SITE + "/", "logo": SITE + "/icon-192.png",
                "telephone": "+972-50-925-7065", "email": EMAIL,
                "address": {"@type": "PostalAddress", "streetAddress": "שדרות ירושלים 18", "addressLocality": "אשדוד", "addressCountry": "IL"},
                "areaServed": "IL",
                "sameAs": [IOS, ANDROID],
            },
            {
                "@type": "MobileApplication", "@id": SITE + "/#app",
                "name": "Zero Work AI", "operatingSystem": "iOS, Android",
                "applicationCategory": "BusinessApplication", "inLanguage": "he",
                "description": "סוכן תוכן בעברית לעסקים: מכין תוכן לרשתות החברתיות לשבוע מראש, אתם מאשרים, וזה מתפרסם לאינסטגרם, פייסבוק, טיקטוק, יוטיוב ולינקדאין.",
                "publisher": {"@id": SITE + "/#org"},
                "installUrl": [IOS, ANDROID],
            },
            {"@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/", "name": "Zero Work AI", "inLanguage": "he", "publisher": {"@id": SITE + "/#org"}},
        ],
    }


def faq_jsonld(body):
    """FAQPage built from the visible <details> on the page, so the markup always matches the text."""
    import re
    qa = re.findall(r'<details>\s*<summary>(.*?)</summary>\s*<div class="a">(.*?)</div>\s*</details>', body, re.S)
    strip = lambda s: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in qa]}


def breadcrumbs(p, label):
    if p == "":
        return ""
    parts = [("", "ראשי")]
    if p.startswith("features/") and p != "features/":
        parts.append(("features/", "יכולות"))
    items = "".join(f'<li><a href="{rel(p, h)}">{t}</a></li>' for h, t in parts)
    return f'<nav class="crumbs" aria-label="פירורי לחם"><ol>{items}<li aria-current="page">{label}</li></ol></nav>'


def hero(p):
    return f'''<div class="wrap hero">
  <div class="hero-copy">
    <h1>סוכן התוכן<br><span class="soft">של העסק שלכם</span></h1>
    <p class="lead">Zero Work AI מכינה לעסק שלכם תוכן לרשתות החברתיות לשבוע מראש, בעברית ובסגנון של המותג. <b>אתם מאשרים פעם בשבוע</b>, וזה מתפרסם לבד באינסטגרם, בפייסבוק, בטיקטוק, ביוטיוב ובלינקדאין.</p>
    {stores(p)}
    <div class="hero-actions"><a class="btn light" href="{rel(p, "contact/")}">לשיחת היכרות</a><a class="btn ghost" href="{rel(p, "how-it-works/")}">איך זה עובד</a></div>
  </div>
  <div class="visual" aria-hidden="true">
    <svg viewBox="0 0 400 400"><path d="M118 52 Q 8 200 118 348"/><path d="M282 52 Q 392 200 282 348"/><line x1="63" y1="200" x2="337" y2="200"/><circle cx="118" cy="52" r="8"/><circle cx="118" cy="348" r="8"/><circle cx="282" cy="52" r="8"/><circle cx="282" cy="348" r="8"/><circle cx="63" cy="200" r="9"/><circle cx="337" cy="200" r="9"/></svg>
    <div class="tile"><img src="{rel(p, "assets/img/app-icon.jpg")}" width="440" height="440" alt=""></div>
  </div>
</div>'''


def render(page):
    p, slug, title, h1, desc, lead, crumb = page
    body = open(os.path.join(SRC, slug + ".html"), encoding="utf-8").read()
    # tiny template vars inside page bodies
    feature_cards = "".join(
        f'<li class="card"><span class="ic">{icon(ic)}</span><h3>{t}</h3><p>{d}</p><a class="more" href="{rel(p, h)}">עוד על {t}<span class="sr-only"> </span></a></li>'
        for h, ic, t, d in FEATURES)
    repl = {
        "{{FEATURE_CARDS}}": f'<ul class="cards">{feature_cards}</ul>',
        "{{STORES}}": stores(p),
        "{{FORM}}": lead_form(p, "lead-" + slug),
        "{{PHONE}}": PHONE, "{{EMAIL}}": EMAIL, "{{COMPANY}}": COMPANY, "{{COMPANY_ID}}": COMPANY_ID, "{{ADDRESS}}": ADDRESS,
        "{{IOS}}": IOS, "{{ANDROID}}": ANDROID, "{{TODAY_HE}}": date.today().strftime("%d.%m.%Y"),
    }
    for k, v in repl.items():
        body = body.replace(k, v)
    import re
    body = re.sub(r'\{\{LINK:([^}]*)\}\}', lambda m: rel(p, m.group(1)), body)
    assert "{{" not in body, f"unresolved var in {slug}"

    url = SITE + "/" + p
    ld = [org_jsonld()] if slug == "home" else []
    if slug == "faq":
        ld.append(faq_jsonld(body))
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)

    top = hero(p) if slug == "home" else (
        f'<div class="wrap page-head">{breadcrumbs(p, crumb)}<h1>{h1}</h1>' + (f'<p class="lead">{lead}</p>' if lead else "") + "</div>")
    active = next((href for href, _ in NAV if p.startswith(href) and href), None)

    doc = f'''<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#14246B">
<meta property="og:type" content="website">
<meta property="og:locale" content="he_IL">
<meta property="og:site_name" content="Zero Work AI">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og.png">
<meta property="og:image:width" content="1024">
<meta property="og:image:height" content="500">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="{rel(p, "icon-192.png")}">
<link rel="apple-touch-icon" href="{rel(p, "icon-180.png")}">
<link rel="preload" href="{rel(p, "assets/fonts/heebo-hebrew.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{rel(p, "assets/site.css")}">
{ld_html}
</head>
<body>
<a class="skip" href="#main">דלגו לתוכן הראשי</a>
<div class="dark">
{header(p, active)}
{top}
</div>
<main id="main" tabindex="-1">
{body}
</main>
{footer(p)}
<script src="{rel(p, "assets/site.js")}" defer></script>
</body>
</html>
'''
    out_dir = os.path.join(OUT, p)
    os.makedirs(out_dir, exist_ok=True)
    open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(doc)


def render_404():
    """GitHub Pages serves /404.html for any missing path, at that path — so every link in it must be root-absolute."""
    import re
    page = ("", "404", "העמוד לא נמצא · Zero Work AI", "העמוד לא נמצא", "העמוד שחיפשתם לא נמצא.",
            "ייתכן שהקישור השתנה. אפשר לחזור לעמוד הראשי או לבחור עמוד מהתפריט.", "העמוד לא נמצא")
    render(page)
    path = os.path.join(OUT, "index.html")
    doc = open(path, encoding="utf-8").read()
    doc = re.sub(r'(href|src)="(?!https?:|mailto:|tel:|#|/)', r'\1="/', doc)
    doc = doc.replace('<link rel="canonical" href="' + SITE + '/">', '<meta name="robots" content="noindex">')
    open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(doc)


def main():
    render_404()          # first, because it borrows the root index.html slot…
    for page in PAGES:    # …which the real home page then overwrites
        render(page)
    # 404 page reuses the layout with a tiny body
    urls = "\n".join(f"  <url><loc>{SITE}/{p}</loc><lastmod>{TODAY}</lastmod></url>" for p, *_ in PAGES)
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
    print(f"built {len(PAGES)} pages → {OUT}{' (preview links)' if PREVIEW else ''}")


if __name__ == "__main__":
    main()
