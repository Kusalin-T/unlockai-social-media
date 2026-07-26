# Meta / Instagram setup — the guardrailed walkthrough

This is the "connect Instagram so comments turn into DMs" step. There's a **visual click-through**
version of the API path — open it during setup:
- macOS: `open guide/meta-setup.html`
- Windows: `start guide\meta-setup.html`

For the **AI assistant**: read this before helping with the Meta step. Talk to the student in Thai,
one action at a time, and never let them stare at a raw error — match it in [DEBUG.md](DEBUG.md)
and give the plain next step. If a step needs a human, tell them to raise their hand.

---

## The workshop path: the API (get your own key)

Today's main event is **Path A below** — the student creates their own Meta app and gets one
**Instagram access token**. It's the powerful version, and it's the breakage-prone one, so go
slowly, one screen at a time, and lean on the visual guide. **If a student gets stuck or you're
running out of time, fall back to the no-code path at the bottom** — a working no-code bot beats
a half-finished API one.

> **Do not ask the student for App Secret.** The workshop bot does not use it. Treat it like a
> password and leave it hidden in Meta.

---

## Path A — API (the workshop path): create your own app + get the keys

Follow the **visual guide** (`guide/meta-setup.html`) screen-by-screen — open it now. The written
version:

1. **Create the app** — `developers.facebook.com` → **Create App** → choose
   **Manage messaging & content on Instagram**. Fill in the app details and connect the student's
   own business portfolio if Meta asks.
2. **Don't click "Become a Tech Provider."** That starts verification/App Review for serving
   accounts owned by other businesses. The workshop uses the student's own account with Standard
   Access.
3. **Open the Instagram use case** → **API setup with Instagram login** → add all required
   permissions (`instagram_business_basic`, `instagram_business_manage_comments`, and
   `instagram_business_manage_messages`).
4. **Add the Instagram account as a tester** if Meta asks → accept the tester invite inside
   Instagram → return to Meta and click **Add account**. The Instagram account must be
   **Professional** (Business or Creator).
5. **Generate the access token** (the workshop's "API key") and copy it once. It lasts roughly
   60 days; the bot refreshes it when Meta allows. Never photograph or paste the raw token into
   a public chat, slide, or repository.
6. **Hand only the access token to the assistant** — it stores `IG_ACCESS_TOKEN` in a private,
   gitignored `.env` file on the laptop. The bot discovers and saves `IG_USER_ID` automatically.
7. **Run the bot** — `bot/run.py` does the actual comment→DM with that token (see
   [bot/README.md](bot/README.md)). Always **dry-run first** (`python bot/run.py`), then
   `python bot/run.py --live` once a real comment from a second account exists. Windows: `py bot\run.py`.

### About Publish, Privacy Policy, and App Review

The workshop bot **polls an Instagram account the student owns**. It does not use webhooks and it
does not serve accounts owned by other businesses. That is the Standard Access case.

- Meta's dashboard says **Published state is required for webhooks**. This bot does not configure
  webhooks.
- Do not send students into **Become a Tech Provider** or App Review during the workshop.
- If Meta explicitly blocks token generation or the own-account dry-run behind a Publish
  requirement, raise a hand. A helper can add the required app details and decide whether to
  publish. Do not improvise a fake Privacy Policy URL.

### Safety rules the assistant must honor (Path A)
- **Never retry a private-reply DM send.** The endpoint can deliver the DM *while returning an
  error* — retrying re-sends and spams the person. One comment → send exactly once → mark done.
- **One private reply per comment**, text ≤ 1000 chars, within 7 days of the comment. Long lead
  magnets go as a **tappable link**, not inline.
- **Skip own-account comments** (don't reply to yourself → loops).
- Space sends ~2s; back off on rate-limit error codes.

---

## Fallback — no-code (Business Suite / ManyChat)

If the API path stalls or time's short, get a working bot the no-code way — no keys, no publishing:

1. Log in to `business.facebook.com` with the account the Instagram is connected to.
2. Make sure the **Instagram** account is linked in the same Business Suite.
3. **Inbox → Automations** → find a **"Comment → Message"** / reply-to-comment automation → paste
   the keyword, public reply, and DM text from your `output/campaign-*.md`.
4. **No automation menu?** (features differ by account/country) → use **ManyChat** (free): connect
   Instagram → **Comment Growth Tool** template → paste the same three pieces.

You can always come back and do the API path later.

---

## Testing (both paths)
Have the person next to you comment the keyword under your post from **their** account → you should
get a public reply **and** an auto-DM to them. You **can't** self-test from your own account. The
DM lands in their **Requests** folder if they don't follow you — that's normal.
