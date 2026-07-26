# Workshop Exercises — follow along in class

## ✅ Block 1 — machine ready
- [ ] Terminal opens
- [ ] Claude CLI installed + `claude` opens and you're logged in (see SETUP.md)
- [ ] Paste the **bootstrap prompt** (SETUP.md step 4) → the AI downloads the repo for you
- [ ] Reopen `claude` inside the `Downloads/unlockai-social-media` folder, type `/`, and see all 5 commands
- [ ] Say one line to the AI and get a reply

## ✅ Block 2 — get your Instagram key (Meta app)
The main event. Follow the **visual guide** — the assistant opens it, or run `open guide/meta-setup.html` (Mac) / `start guide\meta-setup.html` (Windows).
- [ ] Create your own Meta app → choose **Manage messaging & content on Instagram**
- [ ] **Don't** click "Become a Tech Provider"
- [ ] Add the required Instagram permissions → add your professional Instagram account
- [ ] Generate and copy your **access token** — do not reveal the App Secret; this bot does not need it
- [ ] Stuck on a screen? Raise your hand — a helper will jump in
> Short on time or blocked? The no-code fallback (Business Suite / ManyChat) is at the bottom of META-SETUP.md.

## ✅ Block 3 — Comment-to-DM, live
- [ ] Run `/autoreply` → design a "comment <KEYWORD> to get <item>" campaign → get `output/campaign-<keyword>.md`
- [ ] Give the access token to the assistant → it saves it to `.env` and writes `bot/campaign.json`
- [ ] **Dry-run** the bot: `python bot/run.py` (Windows: `py bot\run.py`) — shows what it would send, sends nothing
- [ ] Have the person next to you comment your keyword from **their** account (you can't self-test from your own)
- [ ] **Go live**: `python bot/run.py --live` → they get a public reply + a DM 🎉

## ✅ Block 4 — explore the rest of your toolkit
- [ ] Run `/brand`, answer the interview, and open `brand/brand.md`
- [ ] Pick one: `/caption`, `/ideas`, or `/calendar`
- [ ] Ask the agent to improve today's campaign using the new brand file

## 🏠 Homework (if you don't finish in class, keep going at home)
- [ ] `/ideas` for a topic you want to push this month
- [ ] `/calendar` to plan next week
- [ ] Run a second `/autoreply` campaign on another post
- [ ] Stuck → DM @butabuilds
