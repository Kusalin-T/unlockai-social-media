# The bot — turn comments into DMs

This runs the actual comment→DM automation using the Instagram key you made in the
visual guide (`guide/meta-setup.html`). It's plain Python, **standard library only** — nothing to
install beyond Python itself.

## What you need first
1. Finished the visual guide → your `IG_ACCESS_TOKEN` + `IG_USER_ID` are saved in the repo's
   `.env` file (the assistant does this for you).
2. A campaign file → `bot/campaign.json` (copy `bot/campaign.example.json` and fill it in, or just
   run `/autoreply` and the assistant writes it).

## Run it
Always dry-run first — it shows what it *would* do and sends nothing:
```
python bot/run.py
```
When it looks right, send for real:
```
python bot/run.py --live
```
On **Windows**, if `python` isn't found, use `py`:
```
py bot\run.py
py bot\run.py --live
```

## How to test (the right way)
Have the person next to you comment your keyword under your post from **their** account, then run
`python bot/run.py --live`. You can't test from your own account — the bot skips your own comments,
and you can't DM yourself.

## The safety rules it follows (don't remove these)
- **Never retries a DM send.** Instagram's private-reply API can deliver the message even when it
  reports an error, so a retry would DM the person twice. One attempt per comment, ever.
- **Claims each comment before sending** (in `state.json`) so an interruption can't re-send.
- **Skips your own comments**, only replies **within 7 days** of the comment, and (by default) DMs
  each person **once** per campaign.
- Every send is logged to `bot/contacts.csv`.

## Files (created as you go, not committed)
- `campaign.json` — your campaign copy
- `state.json` — which comments were already handled (this is what prevents double-DMs)
- `contacts.csv` — a log of everyone the bot replied to

Stuck? See [../DEBUG.md](../DEBUG.md) → "Comment-to-DM automation", or [../META-SETUP.md](../META-SETUP.md).
