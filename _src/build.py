#!/usr/bin/env python3
"""Builds the Zero Work AI mini-site from _src/pages/*.html into static pages at the repo root.

    python3 _src/build.py                      → the real site (clean URLs: /faq/)
    python3 _src/build.py --preview --out DIR  → a copy whose links end in index.html (preview from files)

Every page shares one header, one footer and one <head> from this file. Page bodies live in
_src/pages/<slug>.html. Plain HTML on purpose: AI crawlers do not run JavaScript, so everything a
page says is in the HTML; motion is added on top by assets/site.js and never hides content
without it (the hidden-until-revealed states only apply under html.js).
"""
import json, os, re, sys, html, math
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

# path, slug, <title>, h1, meta description, lead, breadcrumb label, page-head visual
PAGES = [
    ("", "home", "Zero Work AI · סוכן תוכן בעברית לעסקים", None,
     "Zero Work AI (זירו וורק) היא אפליקציה ישראלית שמכינה לעסק תוכן לרשתות החברתיות לשבוע מראש, בעברית: פוסטים, קרוסלות, סטוריז וסרטונים. אתם מאשרים, וזה מתפרסם לכל הרשתות.",
     None, "ראשי", None),
    ("how-it-works/", "how-it-works", "איך Zero Work AI עובדת · מהשאלון ועד הפרסום", "איך זה עובד",
     "שלב אחרי שלב: שיחת היכרות, שאלון אפיון, חיבור הרשתות, תוכן לשבוע מראש, אישור ופרסום אוטומטי. כך עובד סוכן התוכן של Zero Work AI.",
     "מהשיחה הראשונה ועד שהתוכן עולה לרשתות: כל מה שקורה בדרך, ומה התפקיד שלכם בכל שלב.", "איך זה עובד", "week"),
    ("features/", "features", "היכולות של Zero Work AI · תוכן, עיצוב, וידאו ופרסום", "מה הסוכן עושה",
     "כל היכולות של Zero Work AI: תוכן שבועי אוטומטי, קרוסלות וסטוריז בעיצוב המותג, עריכת וידאו עם כתוביות בעברית, ניתוח מתחרים ופרסום לחמש רשתות.",
     "סוכן אחד שמתכנן, כותב, מעצב, עורך ומפרסם. אלה היכולות שלו, כל אחת עם הסבר מלא.", "יכולות", None),
    ("features/weekly-content/", "weekly-content", "תוכן שבועי אוטומטי לעסק · Zero Work AI", "תוכן שבועי אוטומטי",
     "Zero Work AI מכינה לעסק תוכן לשבוע שלם מראש: קרוסלות, פוסטים, סטוריז וסרטונים, בנושאים שנבחרים לפי העסק, הלקוחות שלו ומה שעובד עכשיו. אתם מאשרים פעם בשבוע.",
     "בוחרים פעם אחת כמה תכנים בשבוע ובאילו ימים. מאותו רגע, כל שבוע מחכה לכם שבוע מלא של תוכן לאישור.", "תוכן שבועי", "week"),
    ("features/design/", "design", "קרוסלות, פוסטים וסטוריז בעיצוב המותג · Zero Work AI", "קרוסלות, פוסטים וסטוריז",
     "עיצובים מוכנים בצבעי המותג, עם הלוגו והגופן של העסק: קרוסלות, פוסטים, סטוריז, הוכחות חברתיות מהמלצות לקוחות ותמונות AI. כל פרט ניתן לעריכה מהטלפון.",
     "כל תוכן יוצא מעוצב בצבעים, בלוגו ובגופן של העסק, ואפשר לשנות בו כל פרט לפני שהוא עולה.", "עיצוב", "slides"),
    ("features/video/", "video", "עריכת וידאו עם כתוביות בעברית · Zero Work AI", "עריכת וידאו וסרטונים קצרים",
     "מעלים סרטון גלם ומקבלים סרטון ערוך עם כתוביות בעברית, בי-רול ומוזיקה. שולחים קישור להרצאה או לפודקאסט ומקבלים קליפים קצרים מוכנים לפרסום.",
     "מצלמים בטלפון, ו-Zero Work AI הופכת את זה לסרטון ערוך שמוכן לרילס, לטיקטוק וליוטיוב.", "וידאו", "video"),
    ("features/competitors/", "competitors", "ניתוח מתחרים ודפוסים ויראליים · Zero Work AI", "ניתוח מתחרים",
     "Zero Work AI סורקת את המתחרים של העסק ואת התוכן שעובד בתחום, בארץ ובעולם, ומשתמשת בממצאים כדי לבחור נושאים ופתיחים לתוכן השבועי.",
     "הסוכן בודק מה עובד אצל אחרים בתחום שלכם, ומכניס את מה שלמד ישר לתוכן של השבוע.", "מתחרים", "radar"),
    ("features/publishing/", "publishing", "פרסום ותזמון לאינסטגרם, פייסבוק, טיקטוק, יוטיוב ולינקדאין · Zero Work AI", "פרסום לכל הרשתות",
     "Zero Work AI מפרסמת ומתזמנת תוכן לאינסטגרם, פייסבוק, טיקטוק, יוטיוב ולינקדאין, כולל תוכן שיצרתם בעצמכם. באפליקציה רואים מה מחכה לאישור, מה מתוזמן ומה פורסם.",
     "תוכן שאושר עולה לבד בזמן שנקבע, לכל הרשתות שחיברתם. אתם רק רואים שזה קרה.", "פרסום", "send"),
    ("features/brand/", "brand", "המותג והקול של העסק · Zero Work AI", "המותג והקול שלכם",
     "איך Zero Work AI לומדת את העסק: שאלון אפיון, צבעי מותג, לוגו, גופנים, הוראות כתיבה ותמונות רקע, ולמידה מהדירוגים שאתם נותנים לתוכן.",
     "כדי שהתוכן ישמע ויראה כמו העסק שלכם, הסוכן לומד אותו מכמה מקורות, וממשיך ללמוד מכל דירוג.", "מותג", "brand"),
    ("compare/", "compare", "Zero Work AI מול ChatGPT, Canva, כלי תזמון ומנהלת סושיאל", "מול האפשרויות האחרות",
     "השוואה עניינית: מה ההבדל בין Zero Work AI לבין עבודה עם ChatGPT ו-Canva, כלי תזמון, כלי כתיבה או מנהלת סושיאל, ומתי כל אפשרות מתאימה.",
     "יש כמה דרכים לנהל תוכן לעסק. כאן מוסבר מה כל אחת נותנת, מה נשאר עליכם, ומתי Zero Work AI היא הבחירה הנכונה.", "השוואות", None),
    ("faq/", "faq", "שאלות נפוצות על Zero Work AI", "שאלות נפוצות",
     "תשובות לשאלות הנפוצות על Zero Work AI: למי זה מתאים, אילו רשתות, האם התוכן בעברית, האם משהו מתפרסם בלי אישור, איך מתחילים ועוד.",
     "התשובות הקצרות לשאלות שאנחנו שומעים הכי הרבה.", "שאלות נפוצות", None),
    ("about/", "about", "אודות Zero Work AI (זירו וורק)", "אודות Zero Work AI",
     "Zero Work AI (זירו וורק) היא אפליקציה של חברת Zero Work LTD מאשדוד, שבונה סוכן תוכן בעברית לעסקים ישראליים. יותר מ-100 עסקים עובדים איתה היום.",
     "חברה ישראלית שבונה סוכן תוכן בעברית לעסקים קטנים ובינוניים.", "אודות", None),
    ("contact/", "contact", "צרו קשר · Zero Work AI", "דברו איתנו",
     "רוצים לשמוע איך Zero Work AI יכולה לנהל את התוכן של העסק שלכם? השאירו פרטים ונחזור אליכם, או התקשרו ל-050-9257065.",
     "השאירו פרטים ונחזור אליכם לשיחת היכרות קצרה, בלי התחייבות.", "צור קשר", None),
    ("privacy/", "privacy", "מדיניות פרטיות לאתר · Zero Work AI", "מדיניות פרטיות",
     "מדיניות הפרטיות של אתר Zero Work AI: איזה מידע נאסף בטופס יצירת הקשר, למה, איפה הוא נשמר ומה הזכויות שלכם. האתר אינו משתמש בעוגיות.",
     None, "מדיניות פרטיות", None),
    ("terms/", "terms", "תנאי שימוש באתר · Zero Work AI", "תנאי שימוש באתר", "תנאי השימוש באתר Zero Work AI.", None, "תנאי שימוש", None),
    ("accessibility/", "accessibility", "הצהרת נגישות · Zero Work AI", "הצהרת נגישות",
     "הצהרת הנגישות של אתר Zero Work AI: רמת הנגישות, מה הונגש, מגבלות ידועות ודרכים לפנות אלינו בנושא נגישות.",
     None, "הצהרת נגישות", None),
]

NAV = [("how-it-works/", "איך זה עובד"), ("features/", "יכולות"), ("compare/", "השוואות"), ("faq/", "שאלות נפוצות"), ("about/", "אודות")]

# href, visual, title, text, tile class
FEATURES = [
    ("features/weekly-content/", "week", "תוכן שבועי אוטומטי", "שבוע שלם של קרוסלות, פוסטים, סטוריז וסרטונים מחכה לאישור שלכם, בנושאים שנבחרו לפי העסק ולפי מה שעובד עכשיו.", "wide"),
    ("features/design/", "slides", "קרוסלות, פוסטים וסטוריז", "עיצובים בצבעי המותג, עם הלוגו והגופן שלכם. אפשר להחליף תמונה, צבע, טקסט ופריסה ישר מהטלפון.", ""),
    ("features/video/", "video", "עריכת וידאו", "מסרטון גלם לסרטון ערוך עם כתוביות בעברית, בי-רול ומוזיקה, ומהרצאה ארוכה לקליפים קצרים.", ""),
    ("features/competitors/", "radar", "ניתוח מתחרים", "הסוכן סורק את המתחרים ואת התוכן הוויראלי בתחום, בארץ ובעולם, ומכניס את מה שעובד לתוכן שלכם.", ""),
    ("features/publishing/", "send", "פרסום לכל הרשתות", "אינסטגרם, פייסבוק, טיקטוק, יוטיוב ולינקדאין, בזמנים שנקבעו. כולל תוכן שיצרתם בעצמכם.", ""),
    ("features/brand/", "brand", "המותג והקול שלכם", "שאלון אפיון, צבעים, לוגו, גופנים והוראות כתיבה, ולמידה מכל דירוג שאתם נותנים לתוכן.", "full"),
]

# The five networks, in their own colours (simple-icons paths, CC0).
NET_DIR = os.path.join(ROOT, "assets", "img", "net")
NETS = [("instagram", "Instagram", "אינסטגרם", "#E4405F"), ("facebook", "Facebook", "פייסבוק", "#0866FF"),
        ("tiktok", "TikTok", "טיקטוק", "#000000"), ("youtube", "YouTube", "יוטיוב", "#FF0000"), ("linkedin", "LinkedIn", "לינקדאין", "#0A66C2")]
NET_PATH = {k: re.search(r'<path d="([^"]+)"', open(os.path.join(NET_DIR, k + ".svg")).read()).group(1) for k, *_ in NETS}


def net_svg(key, color, size=None):
    s = f' width="{size}" height="{size}"' if size else ""
    return f'<svg viewBox="0 0 24 24"{s} aria-hidden="true" focusable="false"><path fill="{color}" d="{NET_PATH[key]}"/></svg>'


def rel(from_path, to_path):
    """Relative link from one page directory to another page (or asset)."""
    target = "../" * from_path.count("/") + to_path
    if PREVIEW and (to_path == "" or to_path.endswith("/")):
        target += "index.html"
    return target or "./"


def stores(p, small=False):
    cls = "foot-stores" if small else "stores"
    return (f'<div class="{cls}">'
            f'<a class="store" data-store="ios" href="{IOS}" rel="noopener"><img src="{rel(p, "assets/img/app-store-he.svg")}" width="156" height="54" alt="להורדה מה-App Store"></a>'
            f'<a class="store" data-store="android" href="{ANDROID}" rel="noopener"><img src="{rel(p, "assets/img/google-play-he.png")}" width="181" height="54" alt="כעת ב-Google Play"></a>'
            '</div>')


# ── small illustrations (decorative, aria-hidden) ──
def vis(kind, big=False):
    cls = "vis big" if big else "vis"
    if kind == "week":
        days = "".join(f"<i>{d}</i>" for d in "אבגדהוש")
        pattern = ["k", "s", "e", "p", "s", "v", "e",  "s", "k", "s", "e", "k", "e", "s",  "e", "p", "v", "s", "e", "e", "k"]
        cells = "".join(f'<b class="{c}" style="--i:{i}"></b>' for i, c in enumerate(pattern))
        inner = f'<div class="v-week">{days}{cells}</div>'
    elif kind == "slides":
        inner = '<div class="v-slides"><span></span><span></span><span>Aa</span></div>'
    elif kind == "video":
        bars = "".join(f'<i style="--i:{i}"></i>' for i in range(14))
        inner = f'<div class="v-video"><div class="cap"><span>ככה</span><span>מכינים</span><span>תוכן</span></div></div><div class="wave">{bars}</div>'
    elif kind == "radar":
        inner = '<div class="v-radar"><i></i><i></i><i></i></div>'
    elif kind == "send":
        inner = '<div class="v-send">' + "".join(f'<span style="--i:{i}">{net_svg(k, c)}</span>' for i, (k, _, _, c) in enumerate(NETS)) + "</div>"
    elif kind == "brand":
        inner = '<div class="v-brand"><div class="sw"><i></i><i></i><i></i><i></i><i></i></div><span class="aa">Aa</span><span class="stars">★★★★★</span></div>'
    return f'<div class="{cls}" aria-hidden="true">{inner}</div>'


def bento(p):
    tiles = "".join(
        f'<li class="tile rv {cl}" style="--d:{(i % 3) * 0.08:.2f}s">{vis(k)}<h3>{t}</h3><p>{d}</p>'
        f'<a class="more" href="{rel(p, h)}">עוד על {t}</a></li>'
        for i, (h, k, t, d, cl) in enumerate(FEATURES))
    return f'<ul class="bento">{tiles}</ul>'


def hub(p):
    """The signature: the logo's brain sending content along its circuits to the five networks."""
    cx = cy = 280
    angles = [-90, -18, 54, 126, 198]
    shapes = [
        '<rect x="-11" y="-11" width="22" height="22" rx="5" fill="url(#tA)"/>',
        '<rect x="-13" y="-8" width="18" height="18" rx="4" fill="#8B7CFF"/><rect x="-7" y="-11" width="18" height="18" rx="4" fill="url(#tA)" stroke="rgba(255,255,255,.5)"/>',
        '<rect x="-7" y="-12" width="14" height="24" rx="4" fill="url(#tB)"/>',
        '<rect x="-12" y="-9" width="24" height="18" rx="4" fill="url(#tA)"/><path d="M-3 -5 L5 0 L-3 5 Z" fill="#fff"/>',
        '<rect x="-11" y="-11" width="22" height="22" rx="5" fill="url(#tB)"/>',
    ]
    rails, flows, tiles, nodes = [], [], [], []
    dur = 3.2
    for i, a in enumerate(angles):
        r = math.radians(a)
        sx, sy = cx + 100 * math.cos(r), cy + 100 * math.sin(r)
        c = math.radians(a + 24)
        qx, qy = cx + 175 * math.cos(c), cy + 175 * math.sin(c)
        nx, ny = cx + 222 * math.cos(r), cy + 222 * math.sin(r)
        d = f"M{sx:.1f} {sy:.1f} Q{qx:.1f} {qy:.1f} {nx:.1f} {ny:.1f}"
        rails.append(f'<path class="rail" d="{d}"/>')
        flows.append(f'<path class="flow" d="{d}"/>')
        for k, extra in enumerate((0, dur / 2)):
            b = i * 0.64 + extra
            tiles.append(
                f'<g opacity="0">{shapes[(i + k) % len(shapes)]}'
                f'<animateMotion dur="{dur}s" begin="{b:.2f}s" repeatCount="indefinite" path="{d}"/>'
                f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.15;.8;1" dur="{dur}s" begin="{b:.2f}s" repeatCount="indefinite"/></g>')
        key, _, _, color = NETS[i]
        nodes.append(
            f'<g class="netn" style="--i:{i}">'
            f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="27" fill="none" stroke="#4DD6FF" stroke-width="2" opacity="0">'
            f'<animate attributeName="r" values="27;27;29;46" keyTimes="0;.68;.72;1" dur="{dur / 2}s" begin="{i * 0.64:.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0;.85;0" keyTimes="0;.68;.72;1" dur="{dur / 2}s" begin="{i * 0.64:.2f}s" repeatCount="indefinite"/></circle>'
            f'<circle class="net-bg" cx="{nx:.1f}" cy="{ny:.1f}" r="27"/>'
            f'<svg x="{nx - 13:.1f}" y="{ny - 13:.1f}" width="26" height="26" viewBox="0 0 24 24"><path fill="{color}" d="{NET_PATH[key]}"/></svg></g>')
    mark = rel(p, "assets/img/mark-white.png")
    return f'''<div class="hub fade" style="--d:.3s" aria-hidden="true">
<svg class="smil" viewBox="0 0 560 560" role="presentation">
  <defs>
    <linearGradient id="flowGrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4DD6FF"/><stop offset="1" stop-color="#8B7CFF"/></linearGradient>
    <linearGradient id="ringGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4DD6FF"/><stop offset=".5" stop-color="#2F6BFF"/><stop offset="1" stop-color="#8B7CFF"/></linearGradient>
    <linearGradient id="tA" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4DD6FF"/><stop offset="1" stop-color="#2F6BFF"/></linearGradient>
    <linearGradient id="tB" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8B7CFF"/><stop offset="1" stop-color="#4DD6FF"/></linearGradient>
    <radialGradient id="glow"><stop offset="0" stop-color="#2F6BFF" stop-opacity=".75"/><stop offset=".6" stop-color="#2F6BFF" stop-opacity=".12"/><stop offset="1" stop-color="#2F6BFF" stop-opacity="0"/></radialGradient>
  </defs>
  <circle class="halo" cx="280" cy="280" r="190" fill="url(#glow)"/>
  {"".join(rails)}{"".join(flows)}
  <circle class="ring" cx="280" cy="280" r="122"/>
  <path class="arc" d="M206 150 Q100 280 206 410"/><path class="arc" d="M354 150 Q460 280 354 410"/>
  <circle class="arc-dot" style="--i:0" cx="206" cy="150" r="7"/><circle class="arc-dot" style="--i:1" cx="206" cy="410" r="7"/>
  <circle class="arc-dot" style="--i:2" cx="354" cy="150" r="7"/><circle class="arc-dot" style="--i:3" cx="354" cy="410" r="7"/>
  <circle class="core" cx="280" cy="280" r="98"/>
  <image href="{mark}" x="212" y="223" width="136" height="114"/>
  {"".join(tiles)}
  {"".join(nodes)}
</svg>
</div>'''


def hero(p):
    words1, words2 = ["סוכן", "התוכן"], ["של", "העסק", "שלכם"]
    w1 = " ".join(f'<span class="w" style="--i:{i}">{w}</span>' for i, w in enumerate(words1))
    w2 = " ".join(f'<span class="w" style="--i:{i + 2}">{w}</span>' for i, w in enumerate(words2))
    return f'''<section class="wrap hero" aria-labelledby="hero-title">
  <div class="hero-copy">
    <h1 id="hero-title"><span class="line">{w1}</span><span class="line grad">{w2}</span></h1>
    <p class="lede fade" style="--d:.75s">Zero Work AI מכינה לעסק שלכם תוכן לרשתות החברתיות לשבוע מראש, בעברית ובסגנון של המותג. <b>אתם מאשרים פעם בשבוע</b>, וזה מתפרסם לבד באינסטגרם, בפייסבוק, בטיקטוק, ביוטיוב ובלינקדאין.</p>
    <div class="fade" style="--d:.95s">{stores(p)}</div>
    <div class="hero-actions fade" style="--d:1.1s"><a class="btn" href="{rel(p, "contact/")}">לשיחת היכרות</a><a class="btn ghost" href="{rel(p, "how-it-works/")}">איך זה עובד</a></div>
  </div>
  {hub(p)}
</section>
<div class="net-band"><div class="wrap"><p>מתפרסם לבד ל:</p><ul class="nets">{"".join(f'<li><span class="ni">{net_svg(k, c)}</span>{he}</li>' for k, _, he, c in NETS)}</ul></div></div>'''


def phone_story():
    rows = [("א׳", [("k", "קרוסלה"), ("s", "סטורי")]), ("ב׳", [("p", "פוסט")]), ("ג׳", [("s", "סטורי"), ("v", "וידאו")]),
            ("ד׳", [("k", "קרוסלה")]), ("ה׳", [("s", "סטורי"), ("p", "פוסט")]), ("ו׳", [("k", "קרוסלה")]), ("ש׳", [("s", "סטורי")])]
    n, s1 = 0, []
    for day, chips in rows:
        cs = []
        for c, label in chips:
            cs.append(f'<span class="chip {c}" style="--i:{n}">{label}</span>'); n += 1
        s1.append(f'<div class="day"><i>{day}</i>{"".join(cs)}</div>')
    posts = [("קרוסלה · יום א׳ 10:00", ["instagram", "facebook", "linkedin"]), ("פוסט · יום ב׳ 09:00", ["instagram", "facebook"]), ("סרטון · יום ג׳ 19:00", ["instagram", "tiktok", "youtube"]), ("קרוסלה · יום ד׳ 13:00", ["instagram", "linkedin"]), ("סטורי · יום ה׳ 12:00", ["instagram", "facebook"])]
    s3 = "".join(
        f'<div class="post"><span class="thumb"></span><span class="meta"><b>{t}</b><span>{"".join(net_svg(k, dict((a, d) for a, _, _, d in NETS)[k]) for k in ks)}</span></span><span class="done" style="--i:{i}">פורסם</span></div>'
        for i, (t, ks) in enumerate(posts))
    return f'''<div class="phone" data-step="1">
  <div class="screen">
    <div class="app-top"><b>השבוע שלכם</b><span>Zero Work AI</span></div>
    <div class="state s1">{"".join(s1)}<div class="gen">הסוכן מכין 11 תכנים לשבוע</div></div>
    <div class="state s2"><div class="slide"><small>קרוסלה · שקף 1 מתוך 6</small><strong>3 טעויות שעולות לכם בלקוחות</strong><small>Zero Work AI</small></div><div class="dots"><span></span><span></span><span></span><span></span></div><div class="approve"><span>עריכה</span><span class="yes">אישור</span></div><div class="toast">אושר ✓ יעלה ביום א׳ 10:00</div></div>
    <div class="state s3">{s3}</div>
  </div>
</div>
<p class="story-note">המחשה של מסכי האפליקציה</p>'''


def lead_form(p, fid):
    return f'''<form class="lead-form rv" id="{fid}" novalidate aria-describedby="{fid}-notice">
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


MOTION_BTN = ('<button class="motion-toggle" type="button" aria-pressed="false" aria-label="עצירת תנועה ואנימציות באתר">'
              '<svg class="pause" viewBox="0 0 16 16" aria-hidden="true"><rect x="3" y="2" width="3.5" height="12" rx="1" fill="currentColor"/><rect x="9.5" y="2" width="3.5" height="12" rx="1" fill="currentColor"/></svg>'
              '<svg class="play" viewBox="0 0 16 16" aria-hidden="true"><path d="M4 2.5v11l9-5.5z" fill="currentColor"/></svg>'
              '<span class="label">עצירת תנועה</span></button>')


def header(p, active):
    nav = "".join(f'<a href="{rel(p, href)}"{" aria-current=\"page\"" if href == active else ""}>{label}</a>' for href, label in NAV)
    brand = (f'<a class="brand" href="{rel(p, "")}" aria-label="Zero Work AI, לעמוד הראשי"><img class="mark" src="{rel(p, "assets/img/mark-white.png")}" width="40" height="34" alt="">'
             f'<img class="word" src="{rel(p, "assets/img/wordmark-white.png")}" width="146" height="14" alt=""></a>')
    return f'''<header class="site-header">
  <div class="wrap">
    {brand}
    <nav class="nav-desk" aria-label="ראשי">{nav}</nav>
    <div class="head-actions">{MOTION_BTN}<a class="btn small nav-desk" href="{rel(p, "contact/")}">דברו איתנו</a>
      <details class="menu"><summary>תפריט</summary><nav aria-label="ראשי (נייד)">{nav}<a href="{rel(p, "contact/")}">דברו איתנו</a></nav></details>
    </div>
  </div>
</header>'''


def footer(p):
    feats = "".join(f'<li><a href="{rel(p, h)}">{t}</a></li>' for h, _, t, _, _ in FEATURES)
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
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "Organization", "@id": SITE + "/#org", "name": "Zero Work AI", "alternateName": ["זירו וורק", "Zero Work"], "legalName": COMPANY,
         "url": SITE + "/", "logo": SITE + "/icon-192.png", "telephone": "+972-50-925-7065", "email": EMAIL,
         "address": {"@type": "PostalAddress", "streetAddress": "שדרות ירושלים 18", "addressLocality": "אשדוד", "addressCountry": "IL"},
         "areaServed": "IL", "sameAs": [IOS, ANDROID]},
        {"@type": "MobileApplication", "@id": SITE + "/#app", "name": "Zero Work AI", "operatingSystem": "iOS, Android",
         "applicationCategory": "BusinessApplication", "inLanguage": "he",
         "description": "סוכן תוכן בעברית לעסקים: מכין תוכן לרשתות החברתיות לשבוע מראש, אתם מאשרים, וזה מתפרסם לאינסטגרם, פייסבוק, טיקטוק, יוטיוב ולינקדאין.",
         "publisher": {"@id": SITE + "/#org"}, "installUrl": [IOS, ANDROID]},
        {"@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/", "name": "Zero Work AI", "inLanguage": "he", "publisher": {"@id": SITE + "/#org"}},
    ]}


def faq_jsonld(body):
    """FAQPage built from the visible <details> on the page, so the markup always matches the text."""
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


HEAD_SCRIPT = ("<script>(function(h){h.classList.remove('no-js');h.classList.add('js');var off=false;"
               "try{off=localStorage.getItem('zw-motion')==='off'}catch(e){}"
               "if(!off&&window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)off=true;"
               "h.classList.add(off?'motion-none':'motion')})(document.documentElement)</script>")


def render(page):
    p, slug, title, h1, desc, lead, crumb, pvis = page
    body = open(os.path.join(SRC, slug + ".html"), encoding="utf-8").read()
    repl = {
        "{{BENTO}}": bento(p), "{{STORES}}": stores(p), "{{FORM}}": lead_form(p, "lead-" + slug), "{{PHONE_STORY}}": phone_story(),
        "{{PHONE}}": PHONE, "{{EMAIL}}": EMAIL, "{{COMPANY}}": COMPANY, "{{COMPANY_ID}}": COMPANY_ID, "{{ADDRESS}}": ADDRESS,
        "{{IOS}}": IOS, "{{ANDROID}}": ANDROID, "{{TODAY_HE}}": date.today().strftime("%d.%m.%Y"),
    }
    for k, v in repl.items():
        body = body.replace(k, v)
    body = re.sub(r'\{\{LINK:([^}]*)\}\}', lambda m: rel(p, m.group(1)), body)
    body = re.sub(r'\{\{VIS:([a-z]+)\}\}', lambda m: vis(m.group(1), big=True), body)
    assert "{{" not in body, f"unresolved var in {slug}"

    url = SITE + "/" + p
    ld = [org_jsonld()] if slug == "home" else []
    if slug == "faq":
        ld.append(faq_jsonld(body))
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)

    if slug == "home":
        top = hero(p)
    else:
        side = f'<div class="rv" style="--d:.15s">{vis(pvis, big=True)}</div>' if pvis else ""
        top = (f'<section class="wrap page-head{"" if pvis else " solo"}"><div>{breadcrumbs(p, crumb)}<h1>{h1}</h1>'
               + (f'<p class="lede">{lead}</p>' if lead else "") + f"</div>{side}</section>")
    active = next((href for href, _ in NAV if href and p.startswith(href)), None)

    doc = f'''<!doctype html>
<html lang="he" dir="rtl" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
{HEAD_SCRIPT}
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#070F2B">
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
<link rel="preload" href="{rel(p, "assets/fonts/karantina-700-hebrew.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{rel(p, "assets/fonts/heebo-hebrew.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{rel(p, "assets/site.css")}">
{ld_html}
</head>
<body>
<a class="skip" href="#main">דלגו לתוכן הראשי</a>
<div class="aurora" aria-hidden="true"><span class="blob b1"></span><span class="blob b2"></span><span class="blob b3"></span></div>
{header(p, active)}
{top}
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
    page = ("", "404", "העמוד לא נמצא · Zero Work AI", "העמוד לא נמצא", "העמוד שחיפשתם לא נמצא.",
            "ייתכן שהקישור השתנה. אפשר לחזור לעמוד הראשי או לבחור עמוד מהתפריט.", "העמוד לא נמצא", None)
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
    urls = "\n".join(f"  <url><loc>{SITE}/{p}</loc><lastmod>{TODAY}</lastmod></url>" for p, *_ in PAGES)
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
    print(f"built {len(PAGES)} pages → {OUT}{' (preview links)' if PREVIEW else ''}")


if __name__ == "__main__":
    main()
