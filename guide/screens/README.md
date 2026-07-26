# Screenshots for the Instagram API visual guide

The guide (`guide/meta-setup.html`) loads the files in this folder automatically. The current
screens were recovered from the instructor's 26 July 2026 Meta walkthrough.

This is a **public repository**:

- Never add a screenshot containing a raw access token or App Secret.
- Remove personal email addresses, private account details, and business data. App IDs are public,
  but students do not need to copy them for this workshop.
- A missing image is safe: the guide shows a labeled placeholder instead.

| File | Status | What it shows |
|---|---|---|
| `01-usecase.png` | recovered | Current Meta app use-case picker |
| `02-tech-provider-trap.png` | recovered | The Tech Provider confirmation students should cancel |
| `03-instagram-api-setup.png` | recovered | Instagram Login setup + the three required permissions |
| `04-add-account.png` | recovered | Tester reminder and **Add account** button |
| token result | intentionally not captured | The guide uses a privacy-safe illustration instead |
| `06-optional-publish.png` | recovered | Publish screen for instructor troubleshooting only |

## Why there is no token screenshot

The token is revealed once and must stay private, so the public guide deliberately does not load a
token-result image. It uses a privacy-safe panel that tells students to copy the value directly.
Do not capture or expose App Secret either. The workshop bot needs only `IG_ACCESS_TOKEN` and
discovers `IG_USER_ID` automatically.

The full 17-image source set is stored privately outside this public repository, together with a
manifest and contact sheet.
