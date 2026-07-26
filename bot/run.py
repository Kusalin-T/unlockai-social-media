"""
Comment -> DM bot (student edition).

Polls ONE of your Instagram posts, finds comments containing your keyword, and
sends each commenter a public reply + a private-reply DM with your link. Uses
the access token you generated in the visual guide. Standard library only.

Reads:
  ../.env          IG_ACCESS_TOKEN (the assistant saves this for you)
  campaign.json    your keyword / reply / DM copy + the post URL

Run it:
  python bot/run.py            # DRY RUN — shows what it *would* send, sends nothing
  python bot/run.py --live     # actually send replies + DMs
  (Windows: use `py bot\\run.py` if `python` isn't found)

Safety built in: it dedups by comment id (state.json), skips your own comments,
only replies within Instagram's 7-day window, and NEVER retries a DM send (that
API can deliver the message even when it reports an error, so retrying would
double-DM someone). It claims each comment BEFORE sending so an interruption
can't cause a re-send. Every send is logged to contacts.csv.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ig_client import IGGraphClient, InstagramGraphError

BOT_DIR = Path(__file__).parent
REPO_ROOT = BOT_DIR.parent
ENV_PATH = REPO_ROOT / ".env"
CAMPAIGN_PATH = BOT_DIR / "campaign.json"
STATE_PATH = BOT_DIR / "state.json"
CONTACTS_PATH = BOT_DIR / "contacts.csv"

PRIVATE_REPLY_WINDOW = timedelta(days=7)
SEND_PAUSE_SECS = 2.0
DEEP_LOOKUP_LIMIT = 200

_SHORTCODE_RE = re.compile(r"instagram\.com/(?:p|reel|tv)/([A-Za-z0-9_-]+)")
_THAI_RE = re.compile("[฀-๿]")
CONTACTS_COLUMNS = ["responded_at", "permalink", "comment_id", "username",
                    "from_id", "comment_text", "dm_status", "public_reply_status"]


# ── tiny .env reader (so there's nothing to pip install) ────────────────

def load_env(path: Path) -> dict:
    env = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def save_env_value(path: Path, key: str, value: str) -> None:
    """Set one value without replacing the student's other local settings."""
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    prefix = f"{key}="
    for i, line in enumerate(lines):
        if line.startswith(prefix):
            lines[i] = f"{key}={value}"
            break
    else:
        lines.append(f"{key}={value}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    # POSIX-only; on Windows this just clears the read-only bit. The file is
    # gitignored either way.
    try:
        path.chmod(0o600)
    except OSError:
        pass


# ── config ──────────────────────────────────────────────────────────────

def load_campaign(path: Path) -> dict:
    if not path.exists():
        sys.exit(f"No campaign file at {path}.\n"
                 f"Copy campaign.example.json to campaign.json and fill it in "
                 f"(or ask the assistant / run /autoreply).")
    c = json.loads(path.read_text(encoding="utf-8"))
    for field in ("post_url", "keywords", "public_reply", "dm_text"):
        if not c.get(field):
            sys.exit(f"campaign.json is missing '{field}'.")
    if isinstance(c["keywords"], str):
        c["keywords"] = [c["keywords"]]
    c.setdefault("match", "word")
    c.setdefault("once_per_user", True)
    c.setdefault("lang", "auto")
    return c


def normalize_shortcode(entry: str) -> str:
    m = _SHORTCODE_RE.search(entry or "")
    return m.group(1) if m else (entry or "").strip().strip("/")


def keyword_hits(text: str, keywords, match: str) -> bool:
    """Case-insensitive. 'word' = latin keywords on word boundaries (so "AI"
    doesn't fire on "air"), Thai matches as substring. 'contains' = anywhere.
    'exact' = whole trimmed comment equals a keyword."""
    lowered = (text or "").lower()
    for kw in keywords:
        k = kw.lower()
        if match == "exact":
            if lowered.strip() == k:
                return True
        elif match == "contains":
            if k in lowered:
                return True
        elif k.isascii():
            if re.search(rf"(?<![a-z0-9]){re.escape(k)}(?![a-z0-9])", lowered):
                return True
        elif k in lowered:
            return True
    return False


# ── state / contacts ────────────────────────────────────────────────────

def load_state(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"replied": {}, "user_campaign": []}


def save_state(path: Path, state: dict) -> None:
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(path)


def append_contact(path: Path, row: dict) -> None:
    new_file = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CONTACTS_COLUMNS)
        if new_file:
            writer.writeheader()
        writer.writerow(row)


# ── the run ──────────────────────────────────────────────────────────────

def find_post(client: IGGraphClient, code: str):
    """Locate the target post by shortcode: recent media first, then deeper."""
    if code == "*":
        return None  # wildcard: handled by scanning all recent posts
    for m in client.get_media(limit=50):
        if normalize_shortcode(m.get("permalink") or "") == code:
            return m
    for m in client.iter_media(max_items=DEEP_LOOKUP_LIMIT):
        if normalize_shortcode(m.get("permalink") or "") == code:
            return m
    return None


def main() -> None:
    ap = argparse.ArgumentParser(description="Comment -> DM bot (student edition)")
    ap.add_argument("--live", action="store_true",
                    help="actually send replies/DMs (default: dry-run)")
    args = ap.parse_args()

    env = load_env(ENV_PATH)
    token = env.get("IG_ACCESS_TOKEN")
    user_id = env.get("IG_USER_ID")
    if not token:
        sys.exit("IG_ACCESS_TOKEN is missing from .env.\n"
                 "Finish the visual guide (guide/meta-setup.html), then let the "
                 "assistant save your access token and run this again.")

    campaign = load_campaign(CAMPAIGN_PATH)

    # Safety: never send copy that still has an unfilled <<placeholder>>.
    if args.live:
        for t in (campaign["public_reply"], campaign["dm_text"]):
            if "<<" in t:
                sys.exit("Refusing to send live — your copy still has an unfilled "
                         "<<placeholder>>. Fill in the real link/text in campaign.json first.")

    # The token can identify its own account. Students should not have to hunt
    # through Meta's UI for a second numeric value.
    client = IGGraphClient(access_token=token, user_id=user_id or "me", env_path=ENV_PATH)

    try:
        profile = client.get_profile()
    except InstagramGraphError as e:
        sys.exit(f"Couldn't reach your account: {e}\n"
                 "If it mentions the token, generate a fresh one in the guide.")
    if not user_id:
        user_id = str(profile.get("user_id") or profile.get("id") or "")
        if not user_id:
            sys.exit("The token worked, but Instagram did not return an account ID. "
                     "Ask a workshop helper to check the token permissions.")
        client.user_id = user_id
        save_env_value(ENV_PATH, "IG_USER_ID", user_id)
        print("Saved IG_USER_ID automatically.")
    own_username = (profile.get("username") or "").lower()
    mode = "LIVE" if args.live else "DRY-RUN"
    print(f"Comment->DM bot [{mode}] — @{own_username} ({profile.get('account_type')})")

    code = normalize_shortcode(campaign["post_url"])
    posts = []
    if code == "*":
        posts = [m for m in client.get_media(limit=25) if m.get("comments_count")]
    else:
        post = find_post(client, code)
        if not post:
            sys.exit(f"Couldn't find the post {campaign['post_url']} on your account. "
                     f"Check the URL in campaign.json.")
        posts = [post]

    state = load_state(STATE_PATH)
    now = datetime.now(timezone.utc)
    scanned = matched = sent = failed = 0

    for post in posts:
        if not post.get("comments_count"):
            continue
        try:
            comments = list(client.iter_comments(post["id"]))
        except InstagramGraphError as e:
            print(f"  x couldn't read comments on {post.get('permalink','')}: {e}")
            failed += 1
            continue

        for c in comments:
            scanned += 1
            cid = c["id"]
            text = c.get("text") or ""
            username = (c.get("username") or "").lower()
            if cid in state["replied"]:
                continue
            # Skip our own comments (and authorless ones — our own reply comments
            # can surface with no username and would otherwise self-trigger).
            if not username or username == own_username:
                state["replied"][cid] = f"skipped:own {now.isoformat()}"
                save_state(STATE_PATH, state)
                continue
            # Outside Instagram's 7-day private-reply window? Leave it.
            try:
                created = datetime.strptime(c.get("timestamp", ""), "%Y-%m-%dT%H:%M:%S%z")
            except ValueError:
                created = now
            if now - created > PRIVATE_REPLY_WINDOW:
                continue
            if not keyword_hits(text, campaign["keywords"], campaign["match"]):
                continue
            matched += 1

            user_key = username
            if campaign["once_per_user"] and username and user_key in state["user_campaign"]:
                state["replied"][cid] = f"skipped:already {now.isoformat()}"
                save_state(STATE_PATH, state)
                continue

            preview = text.replace("\n", " ")[:60]
            if not args.live:
                print(f"  [dry-run] would DM @{username}: “{preview}”")
                continue

            # Claim BEFORE sending, and NEVER retry the send. The private-reply
            # API is not idempotent and can deliver the DM while returning an
            # error — retrying would double-DM. Attempt exactly once, ever.
            state["replied"][cid] = now.isoformat()
            if username:
                state["user_campaign"].append(user_key)
            save_state(STATE_PATH, state)

            dm_status, pub_status = "sent", "sent"
            try:
                client.send_private_reply(cid, campaign["dm_text"])
            except InstagramGraphError as e:
                dm_status = f"error: {e}"
                print(f"  x DM to @{username} reported an error (NOT retried, may "
                      f"have delivered): {e}")
            time.sleep(SEND_PAUSE_SECS)

            if campaign["public_reply"]:
                try:
                    client.reply_to_comment(cid, campaign["public_reply"])
                except InstagramGraphError as e:
                    pub_status = f"error: {e}"
                time.sleep(SEND_PAUSE_SECS)

            append_contact(CONTACTS_PATH, {
                "responded_at": now.isoformat(),
                "permalink": post.get("permalink", ""),
                "comment_id": cid, "username": username,
                "from_id": c.get("from_id", ""), "comment_text": preview,
                "dm_status": dm_status, "public_reply_status": pub_status,
            })
            ok = dm_status == "sent"
            sent += 1 if ok else 0
            failed += 0 if ok else 1
            print(f"  {'v' if ok else 'x'} @{username} (DM {dm_status}, reply {pub_status})")

    tail = "" if args.live else "  (dry-run — nothing sent)"
    print(f"Done. scanned={scanned} matched={matched} sent={sent} failed={failed}{tail}")
    if not args.live and matched:
        print("Looks right? Run again with --live to actually send.")


if __name__ == "__main__":
    main()
