"""Small, dependency-free safety tests for the workshop bot."""

from __future__ import annotations

import json
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock
from urllib.parse import parse_qs

sys.path.insert(0, str(Path(__file__).parent))
from ig_client import IGGraphClient
from run import (append_contact, keyword_hits, load_campaign, load_env,
                 load_state, normalize_shortcode, save_env_value, save_state)

# Thai + emoji: exactly what /autoreply writes into campaign.json and what a
# real commenter types. These crash on Windows unless every file open is UTF-8.
THAI_SAMPLE = "สนใจครับ 📩"


class CampaignHelpersTest(unittest.TestCase):
    def test_latin_keyword_uses_word_boundaries(self) -> None:
        self.assertTrue(keyword_hits("Send me AI please", ["AI"], "word"))
        self.assertFalse(keyword_hits("fresh air", ["AI"], "word"))

    def test_thai_keyword_matches_as_substring(self) -> None:
        self.assertTrue(keyword_hits("ขอรายละเอียดหน่อยครับ", ["รายละเอียด"], "word"))

    def test_shortcode_accepts_url_or_raw_value(self) -> None:
        self.assertEqual(normalize_shortcode("https://instagram.com/reel/ABC_123/"), "ABC_123")
        self.assertEqual(normalize_shortcode("ABC_123"), "ABC_123")


class SecretStorageTest(unittest.TestCase):
    def test_env_update_preserves_other_values_and_is_private(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            env_path = Path(temp_dir) / ".env"
            env_path.write_text("KEEP=this\nIG_ACCESS_TOKEN=old\n")

            save_env_value(env_path, "IG_ACCESS_TOKEN", "new")

            self.assertEqual(
                env_path.read_text(encoding="utf-8"),
                "KEEP=this\nIG_ACCESS_TOKEN=new\n",
            )
            # chmod is POSIX-only. On Windows it just clears the read-only bit,
            # so st_mode comes back 0o666 and asserting 0o600 always fails.
            if os.name == "posix":
                self.assertEqual(stat.S_IMODE(env_path.stat().st_mode), 0o600)


class WindowsEncodingTest(unittest.TestCase):
    """Every file the bot touches holds Thai. Python's default encoding on
    Windows is cp1252/cp874, so an open() without encoding='utf-8' raises
    UnicodeDecodeError/UnicodeEncodeError and the bot dies on the first run."""

    def test_campaign_with_thai_loads(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "campaign.json"
            path.write_text(json.dumps({
                "post_url": "https://instagram.com/reel/ABC_123/",
                "keywords": ["สนใจ"],
                "public_reply": THAI_SAMPLE,
                "dm_text": "ลิงก์ครับ 🔓",
            }, ensure_ascii=False), encoding="utf-8")

            campaign = load_campaign(path)

            self.assertEqual(campaign["keywords"], ["สนใจ"])
            self.assertEqual(campaign["public_reply"], THAI_SAMPLE)

    def test_state_round_trips_thai(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "state.json"

            save_state(path, {"replied": {"c1": THAI_SAMPLE}, "user_campaign": []})

            self.assertEqual(load_state(path)["replied"]["c1"], THAI_SAMPLE)

    def test_contacts_log_accepts_thai_comment(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "contacts.csv"

            append_contact(path, {
                "responded_at": "2026-07-26T10:00:00+00:00",
                "permalink": "https://instagram.com/reel/ABC_123/",
                "comment_id": "c1", "username": "somchai", "from_id": "42",
                "comment_text": THAI_SAMPLE,
                "dm_status": "sent", "public_reply_status": "sent",
            })

            self.assertIn(THAI_SAMPLE, path.read_text(encoding="utf-8"))

    def test_env_reads_utf8_written_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / ".env"
            path.write_text("IG_ACCESS_TOKEN=abc\n# หมายเหตุ\n", encoding="utf-8")

            save_env_value(path, "IG_USER_ID", "1784")

            env = load_env(path)
            self.assertEqual(env["IG_ACCESS_TOKEN"], "abc")
            self.assertEqual(env["IG_USER_ID"], "1784")


class InstagramRequestShapeTest(unittest.TestCase):
    def test_private_reply_uses_comment_id_and_sends_once(self) -> None:
        client = IGGraphClient("token", "1784", auto_refresh=False)
        client._http_json = Mock(return_value={"recipient_id": "person", "message_id": "message"})

        client.send_private_reply("comment-1", "hello")

        self.assertEqual(client._http_json.call_count, 1)
        url = client._http_json.call_args.args[0]
        body = client._http_json.call_args.kwargs["post_body"]
        self.assertIn("/1784/messages", url)
        params = parse_qs(body.decode())
        self.assertEqual(json.loads(params["recipient"][0]), {"comment_id": "comment-1"})
        self.assertEqual(json.loads(params["message"][0]), {"text": "hello"})

    def test_profile_can_be_discovered_from_me(self) -> None:
        client = IGGraphClient("token", "me", auto_refresh=False)
        client._http_json = Mock(
            return_value={
                "user_id": "1784",
                "username": "workshop",
                "account_type": "BUSINESS",
            }
        )

        profile = client.get_profile()

        self.assertEqual(profile["user_id"], "1784")
        url = client._http_json.call_args.args[0]
        self.assertIn("/me?", url)
        self.assertIn("user_id%2Cusername%2Caccount_type%2Cmedia_count", url)


if __name__ == "__main__":
    unittest.main()
