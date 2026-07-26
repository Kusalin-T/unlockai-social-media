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
→ Open PowerShell as **Administrator** (right-click → Run as administrator) and run the install
line again. If it still refuses:
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` then re-run `irm ... | iex`.

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
→ Delete the `unlockai-social-media` folder in Downloads and retry Step 2 with the archive
method. Confirm the 5 skill files exist (BOOTSTRAP Step 3) before moving on.

**No internet / very slow** → check WiFi first (the room's WiFi + password are on screen), then
retry. The whole repo is tiny (a few KB), so a slow download means the network, not the file.

---

## Windows-specific

**Mixed-up shell (a PowerShell command errors, or a bash command errors)**
→ Windows has two shells and their commands differ. `Invoke-WebRequest`/`Expand-Archive` are
**PowerShell**; `curl`/`tar` are **Git-Bash**. Detect which you're in (run `echo $PSVersionTable`
— PowerShell prints a table, Bash errors) and use the matching column in BOOTSTRAP Step 2. Don't
mix them.

**`Expand-Archive` / `Move-Item` fails ("already exists" / "in use")**
→ A leftover folder from a previous try. Delete `$HOME\Downloads\unlockai-social-media` and the
temp files (`$env:TEMP\unlockai.zip`, `$env:TEMP\unlockai-x`), then retry Step 2 method C.

**`cd $HOME\Downloads\unlockai-social-media` says "path not found"**
→ The download landed somewhere else, or the folder name differs. List `$HOME\Downloads` and look
for the real folder name (an archive download may leave `unlockai-social-media-master`). `cd` into
whatever actually exists, or re-run the Move-Item step to rename it.

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
→ Two options. **No-code (recommended for most):** Meta Business Suite → Inbox → **Automations**,
or **ManyChat** (free "Comment Growth Tool" template) — paste the keyword/reply/DM from your
`output/campaign-*.md`. **API path (self-hosted, advanced):** create your own Meta app, get an
access token — that's the visual guide's subject. Not sure? Use no-code; a helper can move you to
the API path if you want it.

**(API path) I created the app but `GET /{media}/comments` returns 0 even though the post has comments**
→ The app is still in **Development mode**. In Development, only role-holders' comments are
visible. Fix: **Publish** the app (left sidebar → Publish). This is the #1 API blocker.

**(API path) Publish is blocked — it wants a Privacy Policy URL**
→ App settings → Basic → **Privacy policy URL** must be a real reachable URL (Terms + Data-deletion
can be placeholders). See META-SETUP.md for a 2-minute hosted policy.

**(API path) "Do I need App Review / Advanced Access?" panic**
→ For your **own** account: **No.** Instagram-Login + "serves a business I own" = Standard Access,
no review. **Do NOT click "Become a Tech Provider"** — that's the review path you don't need.

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

Still stuck? DM **[@butabuilds](https://instagram.com/butabuilds)** — or ask the person running
the workshop.
