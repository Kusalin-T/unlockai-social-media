# BOOTSTRAP — agent-followed setup

**You are the AI assistant running on the student's laptop.** The student pasted a short
prompt asking you to set up their *UnlockAI: Social Media* workspace. Follow the steps below
exactly, top to bottom. **Talk to the student in Thai, short and encouraging** — they are a
creator / business owner, not a programmer. Do the technical parts yourself; only ask them to
press a key or approve a permission when you truly need it.

If anything fails, open **DEBUG.md** in the same repo
(`https://raw.githubusercontent.com/Kusalin-T/unlockai-social-media/master/DEBUG.md`),
find the matching symptom, apply the fix, then continue where you left off.

Repo (public, no login needed): `https://github.com/Kusalin-T/unlockai-social-media`
Default branch: `master`

**Golden rule: never let the student watch a raw error.** If any command fails, don't paste the
stack trace at them — read the failure yourself, match it in DEBUG.md, fix it, and only tell them
the plain next step. One thing at a time. If you're ever stuck after two tries, tell them in Thai:
"ยกมือเรียกทีมงานได้เลยครับ ตรงนี้เดี๋ยวช่วยจัดให้" (raise your hand — a helper will sort this out).

---

## Step 0 — Preflight (do this first, it prevents most breakage)

Before downloading anything, confirm the ground is solid. Run these and read the results:

1. **Which shell am I in?** On Windows you may be in PowerShell (commands like `Invoke-WebRequest`)
   or Git-Bash (commands like `curl`/`tar`). Detect it and use the matching column in Step 2 —
   do not mix them. If unsure, run `echo $PSVersionTable` (PowerShell prints a table; Bash errors).
2. **Can I reach the internet?** Check that `https://codeload.github.com` is reachable
   (a HEAD request or a tiny curl/Invoke-WebRequest). If not → DEBUG.md → "No internet".
3. **Do I have a home Downloads folder?** If `~/Downloads` (mac/Linux) or `$HOME\Downloads`
   (Windows) doesn't exist, create it. Never write to a system folder.
4. **Report platform in one line to the student, in Thai** (e.g. "เครื่อง Windows พร้อมแล้วครับ")
   so they — and any helper walking by — know what you detected.

Only once all four pass, continue.

## Step 1 — Work out the platform and the target folder

- Detect the OS you're running on (macOS / Windows / Linux).
- Target folder = the student's **Downloads** folder, subfolder `unlockai-social-media`:
  - macOS / Linux / Git-Bash: `~/Downloads/unlockai-social-media`
  - Windows PowerShell: `$HOME\Downloads\unlockai-social-media`
- **Never delete an existing workspace.** If the target already exists, rename it beside the
  target to `unlockai-social-media-backup-YYYYMMDD-HHMMSS`, tell the student where the backup is,
  and only then continue with a clean target folder.

Tell the student (in Thai) that you're downloading the toolkit onto their computer — one moment. ⏳

## Step 2 — Download the repo into that folder

Prefer **git** if it's installed; otherwise fall back to downloading the archive. Pick the
branch that matches the shell you actually have:

**A. If `git` is available (best):**

macOS / Linux / Git-Bash:
```
git clone https://github.com/Kusalin-T/unlockai-social-media.git "$HOME/Downloads/unlockai-social-media"
```

Windows PowerShell:
```
git clone https://github.com/Kusalin-T/unlockai-social-media.git "$HOME\Downloads\unlockai-social-media"
```

**B. No git — macOS / Linux / Git-Bash (curl + tar):**
```
target_folder="$HOME/Downloads/unlockai-social-media"
bootstrap_dir=$(mktemp -d "${TMPDIR:-/tmp}/unlockai-bootstrap.XXXXXX")
mkdir -p "$target_folder"
curl -fsSL -H "Cache-Control: no-cache" https://codeload.github.com/Kusalin-T/unlockai-social-media/tar.gz/refs/heads/master -o "$bootstrap_dir/unlockai.tgz"
tar -xzf "$bootstrap_dir/unlockai.tgz" -C "$target_folder" --strip-components=1
```

**C. No git — Windows PowerShell (Invoke-WebRequest + Expand-Archive):**
```
$targetFolder = Join-Path $HOME "Downloads\unlockai-social-media"
$bootstrapTemp = Join-Path $env:TEMP ("unlockai-bootstrap-" + [guid]::NewGuid().ToString("N"))
$archivePath = Join-Path $bootstrapTemp "unlockai.zip"
$extractPath = Join-Path $bootstrapTemp "extract"
New-Item -ItemType Directory -Force -Path $extractPath | Out-Null
Invoke-WebRequest -Uri "https://codeload.github.com/Kusalin-T/unlockai-social-media/zip/refs/heads/master" -Headers @{"Cache-Control" = "no-cache"} -OutFile $archivePath
Expand-Archive -Path $archivePath -DestinationPath $extractPath
Move-Item (Join-Path $extractPath "unlockai-social-media-master") $targetFolder
```

If a command asks for a GitHub username/password, the repo is public — you do **not** need to log
in; use the archive method (B or C) instead. See DEBUG.md → "git asks for a username".

## Step 3 — Verify the download

Confirm these exist inside the target folder:
- `.claude/skills/brand/SKILL.md`
- `.claude/skills/caption/SKILL.md`
- `.claude/skills/ideas/SKILL.md`
- `.claude/skills/calendar/SKILL.md`
- `.claude/skills/autoreply/SKILL.md`
- `README.md`, `CLAUDE.md`

If any are missing, rename the partial folder to a timestamped backup and retry Step 2 with the
archive method. Do **not** delete it, and do **not** proceed until all 5 skills and both markdown
files are present.

## Step 4 — Hand off (the student must relaunch inside the folder)

The 5 skills (`/brand`, `/caption`, `/ideas`, `/calendar`, `/autoreply`) only switch on when
Claude Code is **started inside this folder** — you cannot activate them from the current
session because it started somewhere else. So finish by telling the student **in Thai**,
clearly, with the exact commands for their OS. Print the real absolute path you used.

macOS / Linux:
```
cd ~/Downloads/unlockai-social-media
claude
```
Windows PowerShell:
```
cd $HOME\Downloads\unlockai-social-media
claude
```

Then tell them (in Thai): once Claude reopens inside this folder, type **`/`** and confirm the five
workshop skills appear. **In class, stop there and wait for the instructor's next gate** so the room
stays together. If they are doing the kit on their own, start with **`/brand`**; it interviews them
and builds the brand file used by the other content skills. Today's workshop goal is
**`/autoreply`** = a "comment KEYWORD → get it by DM" campaign.

## Step 5 — Confirm success

Ask the student to reply once they see the 5 slash-commands (they can type `/` to see the list,
or `/help`). If they don't appear, go to DEBUG.md → "Skills don't show after relaunch".

---

### Notes for you, the agent
- The very first thing the student did — installing Claude Code — is the only truly manual step
  and is already done if you're reading this. Everything from here you do for them.
- On a fresh install you may see permission prompts for running commands or fetching URLs —
  that's normal; ask the student to approve them once.
- Keep each message short. One action at a time. Celebrate small wins ("Downloaded ✅") — in Thai.
