# DEBUG — when setup gets stuck

For the **AI assistant**: find the matching symptom, apply the fix, then return to BOOTSTRAP.md
and continue. For a **human helper** in the room: same table, plain steps. Talk to the student
in Thai.

---

## Installing / launching Claude Code

**`claude: command not found` (or `'claude' is not recognized` on Windows)**
→ Close the terminal completely and open a **new** one, then type `claude` again. The installer
adds `claude` to PATH only for new terminals.
→ Still nothing? Re-run the installer:
- macOS: `curl -fsSL https://claude.ai/install.sh | bash`
- Windows PowerShell: `irm https://claude.ai/install.ps1 | iex`

**Windows blocks the install script (execution policy / "running scripts is disabled")**
→ In the same PowerShell window run:
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force`
then re-run `irm https://claude.ai/install.ps1 | iex`. This changes policy only for the current
PowerShell process; administrator mode is not required.

**Login link won't open / login fails**
→ Copy the login URL and open it in **Google Chrome** instead of the default browser. Finish
login there, come back to the terminal.

**"Trust this folder?" prompt** → answer **Yes** (it's your own workshop folder).

---

## During bootstrap (download step)

**Permission prompt to run a command or fetch a URL**
→ This is normal on a fresh install. Approve it (accept / "yes"). It's just the assistant asking
before touching the machine or the internet.

**`git: command not found`**
→ You don't need git. Use the archive method: BOOTSTRAP.md Step 2 method **B** (macOS/Linux) or
**C** (Windows). The assistant should switch to that automatically.

**git asks for a GitHub username / password**
→ The repo is **public**, so login is never required. This only happens when git has cached
credentials that are getting in the way. Use the archive method (BOOTSTRAP Step 2 B or C) — it
needs no account at all.

**Download seems to work but the folder is empty / partial**
→ Never delete an existing workspace. Rename the partial `unlockai-social-media` folder beside
it to `unlockai-social-media-backup-YYYYMMDD-HHMMSS`, then retry Step 2 with the archive method.
Confirm the 5 skill files exist (BOOTSTRAP Step 3) before moving on.

**No internet / very slow** → check WiFi first (the room's WiFi + password are on screen), then
retry. The whole repo is tiny (a few KB), so a slow download means the network, not the file.

---

## Windows-specific

> Windows-only notes, every snippet as a ready-to-run script, and the full list of Windows traps
> found in testing: **[windows/README.md](windows/README.md)**.

**Mixed-up shell (a PowerShell command errors, or a bash command errors)**
→ Windows has two shells and their commands differ. `Invoke-WebRequest`/`Expand-Archive` are
**PowerShell**; the `curl … | tar -xz` form is **Git-Bash / macOS**. Detect which you're in (run
`echo $PSVersionTable` — PowerShell prints a table, Bash errors) and use the matching column in
BOOTSTRAP Step 2. Don't mix them.

**`A parameter cannot be found that matches parameter name 'fsSL'`**
→ The student pasted the **Mac** `curl` line into **Windows PowerShell**, where `curl` is an
*alias for `Invoke-WebRequest`* — so it fails on the flags instead of saying "command not found",
which is why it looks so confusing. Use BOOTSTRAP Step 2 method **C**.

**Which PowerShell do students have — 5.1 or 7?**
→ Windows 11 ships **5.1** ("Windows PowerShell", blue icon). PowerShell 7 ("PowerShell", black
icon) is a separate install and most students won't have it. Everything in this kit is written and
tested to work on **5.1**, so nobody needs to install anything. Check with `$PSVersionTable.PSVersion`.

**A folder literally named `~` appeared (e.g. `C:\Users\you\~\Downloads\…`)**
→ PowerShell does **not** expand `~` when passing arguments to `git`, so
`git clone … ~/Downloads/x` creates a real folder called `~`. Then `cd ~/Downloads/x` (which *does*
expand) reports "path not found" — same machine, two different places. Use `$HOME` / `Join-Path`
as in SETUP.md. Remove the stray folder with `Remove-Item -LiteralPath '~' -Recurse -Force` —
`-LiteralPath` matters, or PowerShell expands the `~` again and you delete the wrong thing.

**`Expand-Archive` / `Move-Item` fails ("already exists" / "in use")**
→ First close any Explorer or terminal window currently inside the folder. If the target exists,
rename it to a timestamped backup; never delete it. Retry BOOTSTRAP Step 2 method C — it creates
a new uniquely named temporary folder each time, so stale ZIP and extraction files cannot collide.

**There is an `unlockai-social-media-master` folder *inside* `unlockai-social-media`**
→ An older version of these instructions used `Move-Item -Force`, which moves the source *inside*
an existing folder instead of replacing it — and reports success, so nothing looked wrong at the
time. Rerun BOOTSTRAP Step 2 method C (it backs the folder up first), then copy any of the
student's work across from the backup.

**`cd $HOME\Downloads\unlockai-social-media` says "path not found"**
→ The download landed somewhere else, or the folder name differs. List `$HOME\Downloads` and look
for the real folder name (an archive download may leave `unlockai-social-media-master`). `cd` into
whatever actually exists, or re-run the Move-Item step to rename it.
→ Check the `~` trap above — a `git clone` with `~` puts it in a folder literally named `~`.
→ If File Explorer shows Downloads under **OneDrive**, the folder was redirected and
`$HOME\Downloads` is a *different, new* folder. Use the absolute path the assistant printed.

**Antivirus / SmartScreen warning on the installer** → this is the Windows install of Claude Code
itself, from the official `claude.ai` script. Allow it / "More info → Run anyway". If the machine
is locked down, the student needs their own admin password (that's on the pre-work checklist).

---

## After relaunch (skills / workspace)

**Skills don't show after relaunch (`/brand` isn't there)**
→ Almost always: Claude Code was started in the **wrong folder**. In the Claude session type a
message asking "what folder are you running in?" — it must end in `unlockai-social-media`.
→ Fix: quit (`/quit` or Ctrl+C twice), then in the terminal:
`cd ~/Downloads/unlockai-social-media` (Windows: `cd $HOME\Downloads\unlockai-social-media`),
then `claude` again. Type `/` to see the 5 commands.

**`/brand` runs but later skills say "no brand file"**
→ Run `/brand` to the end first — it creates `brand/brand.md`, which every other skill reads.
Then try `/caption`, `/ideas`, `/calendar`, `/autoreply` again.

**Assistant is replying in the wrong language** → it should default to Thai; just tell it
"ตอบเป็นภาษาไทย" (reply in Thai) and it will switch.

---

## Comment-to-DM automation (the `/autoreply` goal)

**Full picture + a click-through visual guide live in [META-SETUP.md](META-SETUP.md).** Open the
visual walkthrough with `open guide/meta-setup.html` (macOS) / `start guide\meta-setup.html`
(Windows). The most common blockers, and how to clear them:

**Which path do I even use?**
→ Today's main path is the **API path**: create your own Meta app and get your own access token —
that's the visual guide (`guide/meta-setup.html`). **If it stalls or time runs short, fall back to
no-code:** Meta Business Suite → Inbox → **Automations**, or **ManyChat** (free "Comment Growth
Tool" template) — paste the keyword/reply/DM from your `output/campaign-*.md`. A working no-code
bot beats a half-finished API one.

**(API path) I created the app but `GET /{media}/comments` returns 0 even though the post has comments**
→ Check the simple own-account path first: the Instagram account is Professional, it was added as
an Instagram Tester/connected account, the token belongs to that same account, and the token has
`instagram_business_manage_comments`. The workshop bot polls; it does not need a webhook.

**(API path) "Do I need App Review / Advanced Access?" panic**
→ For your **own** account: **No.** Instagram-Login + "serves a business I own" = Standard Access,
no review. **Do NOT click "Become a Tech Provider"** — that's the review path you don't need.

**(API path) Meta asks for App ID or App Secret**
→ Leave the App Secret hidden. The workshop bot uses only `IG_ACCESS_TOKEN`; it discovers
`IG_USER_ID` automatically. Never paste App Secret into Claude, a slide, or a repository.

**(API path) Meta says Publish is required**
→ The dashboard explicitly requires Published state for **webhooks**; this workshop bot does not
use webhooks. If Meta blocks token generation or the own-account dry-run anyway, raise a hand so
the instructor can inspect the exact requirement. Do not click "Become a Tech Provider" and do
not invent a fake Privacy Policy URL.

**(API path) The DM sends look like they failed but people got the message (and some got 5 copies)**
→ **Never retry a private-reply send.** That endpoint can deliver the DM while returning an error;
retrying re-sends. Send exactly once, mark the comment done, move on — no retry loop, ever.

**(API path) My token stopped working after ~2 months**
→ Long-lived tokens last ~60 days. Refresh via `graph.instagram.com/refresh_access_token` before
expiry. (Renaming your IG username does NOT break the token — it binds to the numeric id.)

**Test it the right way** → have the person next to you comment the keyword under your post from
*their* account. You should get both a public reply and an auto-DM. You **cannot** self-test from
your own account (own comments are skipped and you can't DM yourself). The DM lands in the
recipient's **Requests** folder if they don't follow you.

---

## Running the bot (`bot/run.py`)

**`python: command not found` / `'python' is not recognized` (Windows)**
→ Try `py bot\run.py` instead of `python`. Still nothing? Install Python from python.org (tick
**"Add Python to PATH"** during install), then **open a new terminal** — PATH only refreshes in
new terminals — and retry.

**(Windows) `python` opens the Microsoft Store, or returns silently doing nothing**
→ That's Windows' "App execution alias" stub, not a real Python. Use **`py`** for everything:
`py bot\run.py`, `py --version`. To confirm, run `(Get-Command python).Source` — a path under
`WindowsApps` means it's the stub. (It can be turned off in Settings → Apps → Advanced app
settings → App execution aliases, but `py` is faster and needs no admin rights.)

**(Windows) `UnicodeDecodeError` / `charmap codec can't decode byte …` when running the bot**
→ An older copy of the kit. The bot used to read `campaign.json` with Windows' default encoding
(cp1252 on Thai/Western machines) instead of UTF-8, so any Thai text crashed it on the first run.
Update `bot/run.py` and `bot/ig_client.py` to the current version — every file read/write there now
passes `encoding="utf-8"`. Verify with `py -m unittest discover -s bot -p "test_*.py"`.

**`python3: command not found` (macOS)**
→ Check with `python3 --version`. If it is missing, install the current Python 3 from python.org,
open a new Terminal, then run `python3 bot/run.py`. Do not assume every Mac includes Python.

**`IG_ACCESS_TOKEN is missing from .env`**
→ Finish the visual guide and let the assistant save the token, or paste it into the repo's
`.env` file as `IG_ACCESS_TOKEN=...`. The bot discovers and saves `IG_USER_ID` automatically.

**`No campaign file` / missing field**
→ Run `/autoreply` (the assistant writes `bot/campaign.json`), or copy `bot/campaign.example.json`
to `bot/campaign.json` and fill in the post URL, keyword, reply, and DM text.

**Dry-run says `matched=0`** → no unhandled comment contains your keyword yet. Have a **second
account** comment the exact keyword, then run again. (Already-answered comments are remembered in
`bot/state.json`, so they never fire twice.)

**"Refusing to send live — unfilled `<<placeholder>>`"** → your `dm_text`/`public_reply` still has
a `<<...>>` token. Put the real link/text in `bot/campaign.json`, then re-run.

**Comments come back empty even though the post has comments** → check the connected/tester
account and token permissions in the Meta section above.

---

Still stuck? DM **[@butabuilds](https://instagram.com/butabuilds)** — or ask the person running
the workshop.
