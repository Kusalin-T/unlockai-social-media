# UnlockAI: Social Media 🔓

Starter kit for doing real social media work with AI — from the **UnlockAI: Social Media** workshop.
ชุดเครื่องมือ AI สำหรับงาน social media จริง (ตัวช่วยตอบเป็นภาษาไทยให้เสมอ)

## What's inside

| Skill | Type | What it does |
|---|---|---|
| Brand Setup | `/brand` | AI interviews you and builds your brand file — **do this first** |
| Caption Writer | `/caption` | 3 on-brand caption options + hashtags (in Thai) |
| Content Ideas | `/ideas` | 10 content ideas/hooks from a single topic |
| Content Calendar | `/calendar` | A 7-day posting plan saved as a file |
| Comment-to-DM Campaign | `/autoreply` | Design a "comment KEYWORD → get it by DM" campaign — CTA, public reply, DM copy, ready to install |

> Everything the AI writes for you (captions, DMs, campaigns) comes out in **Thai** — the repo is in English, the output is Thai. (งานที่ได้เป็นภาษาไทย)

## Quick start — 2 steps

**Step 1 — install Claude Code once** (Mac/Windows) → follow [SETUP.md](SETUP.md) (~10 min).
Once `claude` opens, go to step 2.

**Step 2 — paste this one prompt** into Claude and press Enter. The AI downloads the toolkit itself (no manual download):

```
Set up my UnlockAI: Social Media workspace. Read and follow every step in https://raw.githubusercontent.com/Kusalin-T/unlockai-social-media/master/BOOTSTRAP.md — if anything breaks, read DEBUG.md in the same repo. Reply to me in Thai.
```

The AI downloads the repo, verifies the files, then tells you to reopen `claude` inside the folder.
In the workshop, type `/` to confirm the five commands appear, then wait for the next gate so the
room stays together.

Working through the kit on your own? Start with:

```
/brand
```
Answer the interview — it builds your brand file, and every other skill then writes in your brand voice automatically.

Then keep going — today's goal is `/autoreply`:
```
/caption a product launch next week
/ideas content for Songkran
/calendar
/autoreply
```

> Prefer to download it yourself instead of via the AI? See the manual steps at the bottom of [SETUP.md](SETUP.md).

## Folders

- `brand/` — your brand file (created by `/brand`)
- `output/` — work the AI writes for you (captions, posting plans, comment-to-DM campaigns)
- `workshop/` — the in-class exercises
- `windows/` — Windows-only notes + two helper scripts ([windows/README.md](windows/README.md))

## On Windows?

Everything above works as written in PowerShell. If anything looks off, there's a read-only
health check that tells you what's missing in one screen:

```powershell
powershell -ExecutionPolicy Bypass -File windows\check-setup.ps1
```

Windows-specific gotchas (use `py` not `python`, don't use `~` with `git`, why a re-run used to
nest the folder) are collected in **[windows/README.md](windows/README.md)**.

Stuck → DM [@butabuilds](https://instagram.com/butabuilds)
