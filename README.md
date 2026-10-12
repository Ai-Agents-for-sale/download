# Zero Work AI — download page

Public landing page that sends people to the app stores:
https://app.zerowork-media.com/

- App Store: https://apps.apple.com/il/app/id6799529635 (keep `/il/`)
- Google Play: https://play.google.com/store/apps/details?id=com.zeroworkai.app

Static GitHub Pages site (branch `main`, root). Kept separate from `zero-work-ai-app` on purpose:
every push to that repo's `main` ships a release to all clients (Telegram + phones over the air),
and a change to this page should never do that.

`index.html` is self-contained (logo, icon and store badges are embedded). `og.png` is the
link preview (same image as the Google Play feature graphic).
