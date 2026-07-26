---
name: autoreply
description: Design a comment-to-DM campaign — "comment KEYWORD to get X" post CTA, public auto-reply under the comment, and the auto-DM that delivers the link/freebie. Use when user wants comment automation, keyword campaigns, or auto-DM funnels.
---

Build a **Comment-to-DM** campaign: someone comments a set keyword → the bot replies under the comment + auto-DMs them the item.
**Write all campaign copy (keyword, CTA, public reply, DM) in Thai.** Talk to the user in Thai.

## Steps

1. Read `brand/brand.md` first (if missing → invite them to run `/brand`).
2. Ask what you need (short, one round):
   - **What gets sent in the DM** (a link? a file? a discount code? product details?)
   - What the post/clip is about
   - The goal after the DM (buy? book? follow?)
3. Design the full campaign and save it to `output/campaign-<keyword>.md` (copy in Thai):

```markdown
# Campaign: <name> — keyword "<KEYWORD>"

## 1. Keyword
"<KEYWORD>" — short, easy to type, hard to misspell (e.g. "สนใจ", "ABC", "รับ")

## 2. CTA in the caption / end of the clip
"คอมเมนต์ '<KEYWORD>' เดี๋ยวส่ง <item> ให้ทาง DM เลย 📩"
(+ 2 more versions to choose from)

## 3. Public reply under the comment
3 rotating versions — short, on-brand, saying "DM sent, check your inbox"
(multiple versions keeps it from looking like spam)

## 4. DM message
- Greet + deliver the item immediately (link/file/code)
- One sentence to advance (the next CTA per the goal)
- Close with an invitation to keep chatting ("มีคำถามพิมพ์มาได้เลย")

## 5. Pre-launch checklist
- [ ] Automation is set up (see steps below)
- [ ] Self-test: comment the keyword from another account → get both reply + DM
- [ ] The link in the DM actually works
```

4. Append the **setup steps** at the end of the file (written for a non-technical person). The
   workshop's main path is the **API path** — the student gets their own Instagram key:
   - **Open the visual guide for them**: `open guide/meta-setup.html` (macOS) / `start guide\meta-setup.html` (Windows), and walk it screen-by-screen. Full written version + safety rules: **[META-SETUP.md](../../../META-SETUP.md)**.
   - It ends with the student holding **App ID + App Secret + access token**. Honor the safety rules: **never retry a DM send** (it may have already delivered), one reply per comment, skip the account's own comments.
   - **Fallback if they stall or time's short** → the no-code way: **Meta Business Suite** → Inbox → **Automations** → "Comment → Message", or **ManyChat** ("Comment Growth Tool" template) — paste the keyword, public reply, and DM text from this file. A working no-code bot beats a half-finished API one.
5. Reinforce two things:
   - One keyword per campaign/post — easy to measure, no collisions.
   - The first week, check the real DMs daily: how people reply, bring it back to the AI so it can sharpen the copy.

## Bonus — quick replies to ordinary comments

If the user pastes an ordinary comment/DM (not a campaign) for help replying → answer each in the brand voice: short, genuine, with a next step, and flag ⚠️ the ones the owner should answer personally (angry customer / drama / refund requests).
