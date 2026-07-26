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

---

## Step 1 — Work out the platform and the target folder

- Detect the OS you're running on (macOS / Windows / Linux).
- Target folder = the student's **Downloads** folder, subfolder `unlockai-social-media`:
  - macOS / Linux / Git-Bash: `~/Downloads/unlockai-social-media`
  - Windows PowerShell: `$HOME\Downloads\unlockai-social-media`
- If a folder already exists there from a previous try, delete it first so the download is clean.

Tell the student in Thai: "กำลังโหลดชุดเครื่องมือลงเครื่องให้นะครับ รอแป๊บ ⏳"

## Step 2 — Download the repo into that folder

Prefer **git** if it's installed; otherwise fall back to downloading the archive. Pick the
branch that matches the shell you actually have:

**A. If `git` is available (best):**
```
git clone https://github.com/Kusalin-T/unlockai-social-media.git <target folder>
```

**B. No git — macOS / Linux / Git-Bash (curl + tar):**
```
mkdir -p <target folder>
curl -fsSL https://codeload.github.com/Kusalin-T/unlockai-social-media/tar.gz/refs/heads/master -o /tmp/unlockai.tgz
tar -xzf /tmp/unlockai.tgz -C <target folder> --strip-components=1
```

**C. No git — Windows PowerShell (Invoke-WebRequest + Expand-Archive):**
```
New-Item -ItemType Directory -Force -Path "$HOME\Downloads" | Out-Null
Invoke-WebRequest -Uri "https://codeload.github.com/Kusalin-T/unlockai-social-media/zip/refs/heads/master" -OutFile "$env:TEMP\unlockai.zip"
Expand-Archive -Path "$env:TEMP\unlockai.zip" -DestinationPath "$env:TEMP\unlockai-x" -Force
Move-Item "$env:TEMP\unlockai-x\unlockai-social-media-master" "$HOME\Downloads\unlockai-social-media" -Force
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

If any are missing, delete the folder and retry Step 2 with the archive method. Do **not**
proceed until all 5 skills and both markdown files are present.

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

Then tell them: พอ Claude เปิดขึ้นมาใหม่ในโฟลเดอร์นี้ ให้พิมพ์ **`/brand`** เป็นคำสั่งแรก —
AI จะสัมภาษณ์แล้วสร้างไฟล์แบรนด์ให้ จากนั้นทุก skill จะเขียนงานในเสียงแบรนด์คุณอัตโนมัติ
เป้าหมายวันนี้คือ **`/autoreply`** = แคมเปญ "คอมเมนต์คำนี้ รับของทาง DM".

## Step 5 — Confirm success

Ask the student to reply once they see the 5 slash-commands (they can type `/` to see the list,
or `/help`). If they don't appear, go to DEBUG.md → "Skills don't show after relaunch".

---

### Notes for you, the agent
- The very first thing the student did — installing Claude Code — is the only truly manual step
  and is already done if you're reading this. Everything from here you do for them.
- On a fresh install you may see permission prompts for running commands or fetching URLs —
  that's normal; ask the student to approve them once.
- Keep each message short. One action at a time. Celebrate small wins ("โหลดเสร็จแล้ว ✅").
