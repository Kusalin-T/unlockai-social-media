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

Today's main event is **Path A below** — the student creates their own Meta app and gets their
own **App ID + App Secret + access token**. It's the powerful version, and it's the breakage-prone
one, so go slowly, one screen at a time, and lean on the visual guide. **If a student gets stuck
or you're running out of time, fall back to the no-code path at the bottom** — a working no-code
bot beats a half-finished API one.

---

## Path A — API (the workshop path): create your own app + get the keys

Follow the **visual guide** (`guide/meta-setup.html`) screen-by-screen — open it now. The written
version:

1. **Create the app** — `developers.facebook.com` → **Create App** → **Other** → **Business**.
2. **Don't click "Become a Tech Provider."** That starts App Review, which own-account use does
   **not** need.
3. **Add Instagram** → **API setup with Instagram login** (this path needs **no Facebook Page**).
4. **Copy your secret key** — App settings → Basic → **App ID** + **App Secret** (treat the secret
   like a password).
5. **Add your Instagram as a Tester** → accept in the IG app (Settings → Apps and websites → Tester
   invites). Your IG must be a **Professional** account (Business or Creator).
6. **Generate your access token** (the "API key"). It lasts ~60 days; refresh before expiry via
   `graph.instagram.com/refresh_access_token`.
7. **Privacy Policy URL** — App settings → Basic → a real reachable URL (needed to publish). No
   policy? The assistant can deploy a 2-minute static one.
8. **Publish** the app (left sidebar → Publish). **Critical:** while unpublished, the API sees
   **zero** comments from normal followers — this is the #1 "why isn't it working".
9. **Hand the three values to the assistant** — it stores `App ID`, `App Secret`, `Access token`
   in a private `.env` on the machine; they never leave the computer.

### Safety rules the assistant must honor (Path B)
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
