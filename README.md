# Zero Work AI — mini-site (app.zerowork-media.com)

Public Hebrew mini-site for Zero Work AI: what the product is, how it works, features, comparisons,
FAQ, contact form, and the legal pages (website privacy policy, terms, accessibility statement).
Built 2026-10-21 to be found and quoted by AI assistants (ChatGPT, Claude, Gemini, Perplexity) —
the research and plan behind it: app-hq `business/ai-visibility.md`.

**Kept separate from `zero-work-ai-app` on purpose:** every push to that repo's `main` ships a release
to all clients (Telegram + phones over the air). A change here never does.

## Editing

Pages are generated — never edit the HTML at the root by hand.

1. Edit a page body in `_src/pages/<slug>.html`, or the shared header/footer/form/`<head>` in `_src/build.py`.
2. `python3 _src/build.py` (writes every page + `sitemap.xml`).
3. Check locally: `python3 -m http.server 4810` → http://127.0.0.1:4810
4. Commit + push → GitHub Pages publishes in about a minute.

`python3 _src/build.py --preview --out <dir>` builds a copy whose links end in `index.html`, for previewing from files.

## Rules that keep it findable and legal

- **Plain HTML only.** AI crawlers do not run JavaScript; everything a page says must be in the HTML.
  `assets/site.js` adds motion on top (reveals, the scroll-driven phone, the stop button) and sends the form — the page reads completely without it.
- **Every page opens with a direct answer** (`<p class="answer">`) — the sentence an AI would quote.
- **Accessibility menu (side button, our own — no third-party plugin):** stop animations (this is the WCAG 2.2.2 pause mechanism — add any new looping element to the `.motion-paused` list in `site.css`), text size, high contrast, highlight links, readable font, reset, links to the statement. Choices live in `localStorage` (`zw-motion`, `zw-a11y`) and are applied by the head script before paint; the privacy policy mentions this. A widget is NOT legally required and never replaces the site being accessible itself (ISOC: icon optional; FTC fined accessiBe 2025).
- **Motion:** hidden-until-revealed states only under `html.js.motion`.
- **No cookies, pixels, analytics or third-party embeds.** The privacy policy says so; adding any of
  them means updating `/privacy/` first (and asking for consent for non-essential cookies).
- **Fonts are self-hosted** (Heebo for reading, Karantina for display; both OFL — `assets/fonts/`). Network icons: simple-icons (CC0), `assets/img/net/`.
- **Accessibility (ת"י 5568 / WCAG 2.1 AA):** contrast ≥4.5:1, visible focus, labelled fields, every
  loop stoppable, `prefers-reduced-motion` respected. Re-check with axe after any design change; update `/accessibility/` date.
- **`robots.txt` allows every crawler, including AI training bots** (Ori, 2026-10-21).
- FAQ JSON-LD is generated from the visible `<details>` on `/faq/`, so the two never disagree.

## The lead form

`assets/site.js` → Supabase edge function `site-lead` (project `jjbxsivcjhpuobpohpoz`, source in the
app repo `supabase/functions/site-lead/`) → Monday leads board `2102550949`, group `topics`,
`ref` = `טופס באתר`. Phone matched on the last 9 digits before anything is created (same rule as the
referral program). The Monday update records what the person wrote and their marketing consent.
If Monday fails the page tells the visitor to call, and the details are kept in `app_events`
(`site_lead.monday_fail`).

## Store links

- App Store: https://apps.apple.com/il/app/id6799529635 (keep `/il/`)
- Google Play: https://play.google.com/store/apps/details?id=com.zeroworkai.app

## Domain

`app.zerowork-media.com` — CNAME `app` in Cloudflare → `ai-agents-for-sale.github.io`, grey cloud
(DNS only). The custom domain is set on THIS repo only; setting one on the account's root site would
move the client app's address too.
