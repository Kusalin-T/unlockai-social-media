"""
Instagram Graph API client (Instagram Login flow) — student edition.

A trimmed, dependency-free port of the content-automation client. Talks to
graph.instagram.com (NOT graph.facebook.com) for the account whose token you
generated in the visual guide (guide/meta-setup.html). Standard library only —
nothing to `pip install`.

Used by bot/run.py. You normally don't run this file directly.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

BASE = "https://graph.instagram.com"
DEFAULT_VERSION = "v21.0"

# Meta error code 190 = token bad/expired -> try one refresh.
_TOKEN_ERROR_CODES = {190}


class InstagramGraphError(Exception):
    """A Graph API call returned an error payload."""


class IGGraphClient:
    def __init__(self, access_token, user_id, version=DEFAULT_VERSION,
                 env_path=None, auto_refresh=True):
        self.token = access_token
        self.user_id = user_id
        self.version = version or DEFAULT_VERSION
        self.auto_refresh = auto_refresh
        self.env_path = Path(env_path) if env_path else None
        if not self.token or not self.user_id:
            raise ValueError(
                "IG_ACCESS_TOKEN and IG_USER_ID must be set in .env. "
                "See META-SETUP.md / the visual guide."
            )

    # ── low-level HTTP ─────────────────────────────────────────────────

    @staticmethod
    def _http_json(url, post_body=None):
        """GET (or POST, when post_body is given) and parse JSON. Reads the body
        on 4xx/5xx too — Graph puts its error JSON there."""
        req = urllib.request.Request(url, data=post_body,
                                     headers={"User-Agent": "unlockai-student-bot"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read()
        except urllib.error.HTTPError as e:
            body = e.read()
        except urllib.error.URLError as e:  # network/DNS/TLS
            raise InstagramGraphError(f"network error: {e.reason}") from e
        try:
            return json.loads(body)
        except json.JSONDecodeError as e:
            raise InstagramGraphError(f"non-JSON response: {body[:200]!r}") from e

    def _request(self, path, params=None, method="GET", _retried=False):
        params = dict(params or {})
        params["access_token"] = self.token
        encoded = urllib.parse.urlencode(params)
        if method == "POST":
            url = f"{BASE}/{self.version}/{path.lstrip('/')}"
            data = self._http_json(url, post_body=encoded.encode())
        else:
            url = f"{BASE}/{self.version}/{path.lstrip('/')}?" + encoded
            data = self._http_json(url)

        if isinstance(data, dict) and data.get("error"):
            err = data["error"]
            code = err.get("code")
            is_refresh = path.strip("/").startswith("refresh_access_token")
            if code in _TOKEN_ERROR_CODES and self.auto_refresh and not _retried and not is_refresh:
                self.refresh_token()
                return self._request(path, params, method=method, _retried=True)
            raise InstagramGraphError(
                f"{err.get('type', 'Error')} (code {code}): {err.get('message')}")
        return data

    # ── profile / media ────────────────────────────────────────────────

    def get_profile(self):
        """Account profile: user_id, username, account_type, media_count."""
        return self._request("me", {"fields": "user_id,username,account_type,media_count"})

    def get_media(self, limit=30):
        fields = "id,media_type,media_product_type,permalink,caption,timestamp,comments_count"
        resp = self._request(f"{self.user_id}/media", {"fields": fields, "limit": limit})
        return resp.get("data", [])

    def iter_media(self, page_size=50, max_items=200):
        """Paginate media newest-first (used to find an older attached post)."""
        fields = "id,permalink,comments_count"
        page = self._request(f"{self.user_id}/media", {"fields": fields, "limit": page_size})
        count = 0
        while True:
            for m in page.get("data", []):
                yield m
                count += 1
                if max_items and count >= max_items:
                    return
            nxt = page.get("paging", {}).get("next")
            if not nxt:
                return
            page = self._http_json(nxt)
            if page.get("error"):
                raise InstagramGraphError(str(page["error"]))

    # ── comments / messaging ───────────────────────────────────────────

    COMMENT_FIELDS = (
        "id,text,timestamp,username,parent_id,from{id,username},"
        "replies{id,text,timestamp,username,parent_id,from{id,username}}"
    )

    @staticmethod
    def _normalize(c):
        """The top-level `username` is only set for the account's OWN comments;
        every other commenter's handle arrives under `from{}`. Backfill it so we
        can skip our own comments and dedup correctly."""
        frm = c.get("from") or {}
        if not c.get("username") and frm.get("username"):
            c["username"] = frm["username"]
        if frm.get("id"):
            c["from_id"] = frm["id"]
        return c

    def iter_comments(self, media_id, page_size=50):
        """All comments on one post, flattening one level of replies (a reply can
        also carry the keyword). Yields normalized comment dicts."""
        page = self._request(f"{media_id}/comments",
                             {"fields": self.COMMENT_FIELDS, "limit": page_size})
        while True:
            for c in page.get("data", []):
                yield self._normalize(c)
                for r in c.get("replies", {}).get("data", []):
                    yield self._normalize(r)
            nxt = page.get("paging", {}).get("next")
            if not nxt:
                return
            page = self._http_json(nxt)
            if page.get("error"):
                raise InstagramGraphError(str(page["error"]))

    def reply_to_comment(self, comment_id, message):
        """Public threaded reply under a comment."""
        return self._request(f"{comment_id}/replies", {"message": message}, method="POST")

    def send_private_reply(self, comment_id, text):
        """DM the comment's author (Private Reply). One per comment, within 7 days.
        WARNING: not idempotent — never retry (see run.py)."""
        return self._request(
            f"{self.user_id}/messages",
            {"recipient": json.dumps({"comment_id": comment_id}),
             "message": json.dumps({"text": text})},
            method="POST")

    # ── token refresh ──────────────────────────────────────────────────

    def refresh_token(self):
        """Refresh the ~60-day token and persist it back to .env."""
        resp = self._request("refresh_access_token", {"grant_type": "ig_refresh_token"})
        new_token = resp.get("access_token")
        if not new_token:
            raise InstagramGraphError(f"refresh returned no token: {resp}")
        self.token = new_token
        if self.env_path:
            _update_env(self.env_path, "IG_ACCESS_TOKEN", new_token)
            _update_env(self.env_path, "IG_TOKEN_REFRESHED_AT", date.today().isoformat())
        return resp


def _update_env(env_path, key, value):
    """Set KEY=value in .env (replace in place or append), preserving other lines."""
    env_path = Path(env_path)
    lines = env_path.read_text(encoding="utf-8").splitlines() if env_path.exists() else []
    prefix = f"{key}="
    for i, line in enumerate(lines):
        if line.startswith(prefix):
            lines[i] = f"{key}={value}"
            break
    else:
        lines.append(f"{key}={value}")
    env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    try:
        env_path.chmod(0o600)
    except OSError:
        pass
