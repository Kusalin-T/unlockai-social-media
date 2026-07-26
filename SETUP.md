# Setup — install Claude CLI

One time, lasts forever. Takes ~10 minutes.

## 1. Open a terminal

- **Mac**: press `⌘ + Space` → type `Terminal` → Enter
- **Windows**: press the Windows key → type `PowerShell` → Enter

## 2. Install Claude CLI

Copy this line, paste it into the terminal, press Enter:

**Mac:**
```
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows (PowerShell):**
```
irm https://claude.ai/install.ps1 | iex
```

Wait for "installed successfully", then **close the terminal and open a new one once**.

## 3. Open Claude and log in

First verify the install:
```
claude --version
```
Then open Claude:
```
claude
```
- First time it asks you to log in → follow the screen (use your Claude account)
- Asks to trust this folder → answer **Yes**
- You see the Claude Code screen = success ✅

## 4. Let the AI download the toolkit (paste one prompt)

Paste this into Claude and press Enter — you don't download anything yourself:

```
Set up my UnlockAI: Social Media workspace. Read and follow every step in https://raw.githubusercontent.com/Kusalin-T/unlockai-social-media/master/BOOTSTRAP.md — if anything breaks, read DEBUG.md in the same repo. Reply to me in Thai.
```

- If it asks permission to run a command / access the internet → click **Allow (Yes)**
- The AI downloads the repo into `Downloads/unlockai-social-media` and verifies the files
- When it's done it tells you to **reopen `claude` inside that folder** — do what it says, then
  type `/` and confirm the five workshop commands appear
- **In class:** stop there and wait for the next gate. **On your own:** start with `/brand`

If the AI replies and the download is complete = you're ready 🎉

---

## (Optional) Download it yourself — if you'd rather not go through the AI

**Mac — if you already have git:**
```
git clone https://github.com/Kusalin-T/unlockai-social-media.git ~/Downloads/unlockai-social-media
cd ~/Downloads/unlockai-social-media
claude
```
If that folder already exists, rename it first; never delete an existing workshop folder.

**Windows (PowerShell) — if you already have git:**

Copy the **whole block**. Don't put `~` in the `git` line: PowerShell doesn't expand `~` for `git`,
so you'd get a folder literally named `~` and the next `cd` would fail.
```
$targetFolder = Join-Path $HOME "Downloads\unlockai-social-media"
if (Test-Path -LiteralPath $targetFolder) {
  Move-Item -LiteralPath $targetFolder -Destination ("$targetFolder-backup-" + (Get-Date -Format 'yyyyMMdd-HHmmss'))
}
git clone https://github.com/Kusalin-T/unlockai-social-media.git "$targetFolder"
cd $targetFolder
claude
```

**Windows (PowerShell) — no git:**

Nothing to install — this uses only built-in PowerShell. Copy the **whole block**:
```
$ProgressPreference = 'SilentlyContinue'
$targetFolder = Join-Path $HOME "Downloads\unlockai-social-media"
$bootstrapTemp = Join-Path $env:TEMP ("unlockai-bootstrap-" + [guid]::NewGuid().ToString("N"))
$archivePath = Join-Path $bootstrapTemp "unlockai.zip"
$extractPath = Join-Path $bootstrapTemp "extract"
if (Test-Path -LiteralPath $targetFolder) {
  Move-Item -LiteralPath $targetFolder -Destination ("$targetFolder-backup-" + (Get-Date -Format 'yyyyMMdd-HHmmss'))
}
New-Item -ItemType Directory -Force -Path $extractPath | Out-Null
Invoke-WebRequest -Uri "https://codeload.github.com/Kusalin-T/unlockai-social-media/zip/refs/heads/master" -Headers @{"Cache-Control" = "no-cache"} -OutFile $archivePath
Expand-Archive -Path $archivePath -DestinationPath $extractPath
Move-Item -LiteralPath (Join-Path $extractPath "unlockai-social-media-master") -Destination $targetFolder
Remove-Item -LiteralPath $bootstrapTemp -Recurse -Force -ErrorAction SilentlyContinue
cd $targetFolder
claude
```

**No git (Mac):**
```
target_folder="$HOME/Downloads/unlockai-social-media"
if [ -e "$target_folder" ]; then
  mv "$target_folder" "${target_folder}-backup-$(date +%Y%m%d-%H%M%S)"
fi
bootstrap_dir=$(mktemp -d "${TMPDIR:-/tmp}/unlockai-bootstrap.XXXXXX")
mkdir -p "$target_folder"
curl -fsSL -H "Cache-Control: no-cache" https://codeload.github.com/Kusalin-T/unlockai-social-media/tar.gz/refs/heads/master -o "$bootstrap_dir/unlockai.tgz"
tar -xzf "$bootstrap_dir/unlockai.tgz" -C "$target_folder" --strip-components=1
cd "$target_folder" && claude
```
Then type `/` to confirm the five commands appear. In class, wait for the next gate; on your own,
start with `/brand`.

---

## Common problems

| Symptom | Fix |
|---|---|
| `command not found: claude` | Close the terminal, open a new one, try again |
| Windows complains about execution policy | In the same PowerShell window run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force`, then run the install line again |
| Login fails | Open the login link in Chrome instead of your default browser |
| Slow / stuck | Check your internet, type `/quit`, then reopen `claude` |
| Windows: a folder literally named `~` appeared | You used `~` in a `git` command. Remove it with `Remove-Item -LiteralPath '~' -Recurse -Force` and use the Windows blocks above |
| Windows: `A parameter cannot be found that matches parameter name 'fsSL'` | You pasted the **Mac** `curl` line into PowerShell, where `curl` is an alias for `Invoke-WebRequest`. Use the Windows block above |
| Windows: `python` opens the Microsoft Store | Use `py` instead (`py bot\run.py`) |

More detail — and the fixes the AI applies itself — are in [DEBUG.md](DEBUG.md).
Windows-only notes and ready-to-run scripts: [windows/README.md](windows/README.md).
