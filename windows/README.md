# Windows notes

Everything Windows-specific in one place: two ready-to-run scripts, and the traps found while
testing the workshop end-to-end on a clean Windows 11 machine.

Tested on **Windows 11 (10.0.26200)**, **Windows PowerShell 5.1** (what Windows ships — not
PowerShell 7), execution policy `RemoteSigned`, Python 3.13 via `py`, Claude Code 2.1.220.
Nothing here needs administrator rights.

---

## Scripts

Run these from inside the workshop folder.

| Script | What it does |
|---|---|
| `windows\check-setup.ps1` | Read-only health check: Windows/PowerShell version, `claude`, `py`, `git`, the workspace, and all five skills. Prints one line per check. |
| `windows\get-workspace.ps1` | Downloads (or safely re-downloads) the workspace — no git needed. Renames any existing folder to a timestamped backup instead of deleting it. |

```powershell
powershell -ExecutionPolicy Bypass -File windows\check-setup.ps1
powershell -ExecutionPolicy Bypass -File windows\get-workspace.ps1
```

`get-workspace.ps1` is safe to run repeatedly — that's the whole point of it.

> **Why `-ExecutionPolicy Bypass`?** The default policy (`RemoteSigned`) blocks *scripts that carry
> an internet mark*. Files downloaded with `Invoke-WebRequest` and unpacked with `Expand-Archive`
> don't get that mark, so `.\windows\check-setup.ps1` normally just works. But if the student
> downloaded the ZIP through **a browser** and extracted it with File Explorer, the mark *is*
> carried through and the script is blocked. `-ExecutionPolicy Bypass` sidesteps both cases without
> changing any machine setting. To clear the mark instead:
> `Get-ChildItem windows\*.ps1 | Unblock-File`

---

## Traps found in testing

### 1. `Move-Item -Force` silently nests the folder on a re-run

The single worst one, because it looks like it worked.

```powershell
# WRONG — what the old instructions did
Move-Item "$env:TEMP\unlockai-x\unlockai-social-media-master" "$HOME\Downloads\unlockai-social-media" -Force
```

On Windows, `Move-Item -Force` onto a path that already exists as a **folder** does not replace it —
it moves the source *inside* it, and reports success. First run: fine. Second run: you silently get
`unlockai-social-media\unlockai-social-media-master`, and the student's `/` menu shows no skills
because Claude is started one level too high. Third run: a raw `Cannot create a file when that file
already exists` error.

**Fix:** guarantee the destination doesn't exist first, by backing it up.

```powershell
if (Test-Path -LiteralPath $targetFolder) {
  Move-Item -LiteralPath $targetFolder -Destination ("$targetFolder-backup-" + (Get-Date -Format 'yyyyMMdd-HHmmss'))
}
Move-Item -LiteralPath $extracted -Destination $targetFolder
```

`check-setup.ps1` detects the nested folder if a student already has one.

### 2. Never delete a student's workspace

`Downloads\unlockai-social-media` holds `brand\brand.md`, everything in `output\`, `.env` with
their token, and `bot\campaign.json`. Rename to `...-backup-<timestamp>`; never `Remove-Item`.
Recovering a brand file mid-workshop costs more time than the re-download ever saves.

### 3. `~` is not a home directory for `git` in PowerShell

```powershell
git clone https://github.com/... ~/Downloads/unlockai-social-media   # WRONG
```

PowerShell does **not** expand `~` when passing arguments to a native program, so `git` takes it
literally and creates a real folder named `~`. The very next line, `cd ~/Downloads/...`, *does*
expand it — so the student lands somewhere that doesn't exist and gets "path not found" while the
files sit in `C:\Users\<name>\~\Downloads\...`.

Use `$HOME` or `Join-Path`:

```powershell
$targetFolder = Join-Path $HOME "Downloads\unlockai-social-media"
git clone https://github.com/Kusalin-T/unlockai-social-media.git "$targetFolder"
```

To remove a stray one, `-LiteralPath` is required — otherwise PowerShell expands the `~` and you
delete your home directory's contents instead:

```powershell
Remove-Item -LiteralPath '~' -Recurse -Force
```

### 4. `curl` in PowerShell is not curl

`curl` is an **alias for `Invoke-WebRequest`** in Windows PowerShell 5.1. A student who pastes the
Mac line gets:

```
A parameter cannot be found that matches parameter name 'fsSL'.
```

— not "command not found", which is why it reads as a broken repo rather than a wrong-shell
mistake. (PowerShell 7 drops the alias and calls the real `curl.exe`, so the same paste behaves
differently again.) `tar` *does* exist natively on Windows 10+, so a half-Mac recipe can even
partly work, which makes it more confusing. Always use the PowerShell block.

### 5. Python file I/O defaults to cp1252, not UTF-8

Every file this bot touches contains Thai. `Path.read_text()` / `open()` without an explicit
encoding uses the Windows ANSI codepage (`cp1252` here, `cp874` on Thai-locale machines), so:

```
UnicodeDecodeError: 'charmap' codec can't decode byte 0x81 in position 176
```

...the moment `py bot\run.py` reads a `campaign.json` that `/autoreply` just wrote. It hit
`campaign.json`, `state.json` and `contacts.csv`. Every read and write in `bot/` now passes
`encoding="utf-8"` explicitly, and `bot/test_bot.py` has Thai round-trip tests that fail on Windows
if anyone drops it again.

Check with:

```powershell
py -c "import locale; print(locale.getpreferredencoding(False))"   # cp1252 / cp874, not utf-8
```

### 6. `py`, not `python`

Windows ships an **App execution alias** stub at `python.exe` that opens the Microsoft Store instead
of running anything — it isn't a missing command, so the error message is unhelpful (often no output
at all). Use the launcher `py` everywhere: `py bot\run.py`, `py --version`.

```powershell
(Get-Command python).Source   # a path under WindowsApps = it's the Store stub
```

Also: installing Python does not update PATH in terminals that are already open. Always open a new
one before retrying. Same for Claude Code itself.

### 7. Paths with spaces

Real user folders are `C:\Users\Kusalin Thanyakulsajja\...`. Quote every path passed to a native
program (`git clone ... "$targetFolder"`), and prefer `-LiteralPath` over `-Path` for cmdlets —
`-Path` also treats `[` and `]` as wildcards, which breaks on some user names. The whole test pass
for this kit was run from a directory with spaces in it for exactly this reason.

### 8. Stale temp files

The old instructions reused fixed temp paths (`$env:TEMP\unlockai.zip`, `$env:TEMP\unlockai-x`), so
a half-extracted folder from a failed attempt got silently reused on the next try. Use a unique
temp directory per run and delete it afterwards — `get-workspace.ps1` does both, in a `finally`
block so it cleans up even when the download fails.

---

## Things that turned out fine

Checked, working, no change needed — recorded so nobody re-tests them:

- `cd $HOME\Downloads\unlockai-social-media` **unquoted** works even when the path has spaces.
- `start guide\meta-setup.html` opens the visual guide correctly from the workspace folder.
- The visual guide's five screenshots all load offline; only the Google Fonts link needs internet,
  and the page degrades gracefully without it.
- All five skills are picked up from `.claude\skills\` — the `SKILL.md` files are BOM-free, which
  matters because a UTF-8 BOM breaks frontmatter parsing.
- Execution policy only blocks *scripts*, never commands pasted into the terminal — so the
  copy-paste blocks in SETUP.md work under the default `RemoteSigned`.

## Known residual risk

- **OneDrive folder redirection.** If Downloads is redirected to OneDrive, `$HOME\Downloads` is a
  *different, new* folder from the one File Explorer shows. The setup still works, but the student
  may not find the folder where they expect. Use the absolute path the assistant prints.
- **PowerShell 7** is not installed on a default Windows 11 machine. Everything here is written for
  5.1 and also verified on 7, but 5.1 is what to assume in the room.
