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

**Wrong language** → tell the assistant "ตอบภาษาไทยนะ" — it defaults to Thai but will match
whatever language you use.

---

## Comment-to-DM automation (the `/autoreply` goal)

**`/autoreply` gives me the campaign text — now where do I actually turn the automation on?**
→ The skill saves a file in `output/` with the keyword, the public reply, and the DM text, plus
install steps at the bottom. Set it up in **Meta Business Suite → Inbox → Automations** (look for
a "Comment → Message" / reply-to-comment automation) and paste in the text from that file.

**Business Suite doesn't show a comment→DM automation** (features differ by account/country)
→ Use **ManyChat** (free): connect your Instagram, pick the "Comment Growth Tool" template, and
paste the same keyword / reply / DM text. The `/autoreply` file already explains this fallback.

**Test it the right way** → have the person next to you comment the keyword under your post from
*their* account. You should get both a public reply under the comment **and** an auto-DM. Testing
from your own account often won't trigger it.

---

Still stuck? DM **[@butabuilds](https://instagram.com/butabuilds)** — or ask the person running
the workshop.
