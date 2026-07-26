# Workshop Exercises — follow along in class

## ✅ Block 1 — machine ready
- [ ] Terminal opens
- [ ] Claude CLI installed + `claude` opens and you're logged in (see SETUP.md)
- [ ] Paste the **bootstrap prompt** (SETUP.md step 4) → the AI downloads the repo for you
- [ ] Reopen `claude` inside the `Downloads/unlockai-social-media` folder, type `/`, and see all 5 commands
- [ ] Say one line to the AI and get a reply

## ✅ Block 2 — your brand
- [ ] Run `/brand`, answer the interview to the end
- [ ] Open `brand/brand.md` — tweak it until it feels right
- [ ] Run `/caption` for your first post — pick 1 of 3

## ✅ Block 3 — get your Instagram key (Meta app)
The main event. Follow the **visual guide** — the assistant opens it, or run `open guide/meta-setup.html` (Mac) / `start guide\meta-setup.html` (Windows).
- [ ] Create your own Meta app (developers.facebook.com) — **don't** click "Become a Tech Provider"
- [ ] Add Instagram → "API setup with Instagram login"
- [ ] Copy your **App ID** + **App Secret**, generate your **access token**
- [ ] Add a Privacy Policy URL → **Publish** the app (this is what makes it work on real followers)
- [ ] Stuck on a screen? Raise your hand — a helper will jump in
> Short on time or blocked? The no-code fallback (Business Suite / ManyChat) is at the bottom of META-SETUP.md.

## ✅ Block 4 — Comment-to-DM, live
- [ ] Run `/autoreply` → design a "comment <KEYWORD> to get <item>" campaign → get `output/campaign-<keyword>.md`
- [ ] Give your keys to the assistant → it saves them to `.env` and writes `bot/campaign.json`
- [ ] **Dry-run** the bot: `python bot/run.py` (Windows: `py bot\run.py`) — shows what it would send, sends nothing
- [ ] Have the person next to you comment your keyword from **their** account (you can't self-test from your own)
- [ ] **Go live**: `python bot/run.py --live` → they get a public reply + a DM 🎉

## 🏠 Homework (if you don't finish in class, keep going at home)
- [ ] `/ideas` for a topic you want to push this month
- [ ] `/calendar` to plan next week
- [ ] Run a second `/autoreply` campaign on another post
- [ ] Stuck → DM @butabuilds
