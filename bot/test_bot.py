"""Small, dependency-free safety tests for the workshop bot."""

from __future__ import annotations

import json
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock
from urllib.parse import parse_qs

sys.path.insert(0, str(Path(__file__).parent))
from ig_client import IGGraphClient
from run import keyword_hits, normalize_shortcode, save_env_value


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
                env_path.read_text(),
                "KEEP=this\nIG_ACCESS_TOKEN=new\n",
            )
            if hasattr(stat, "S_IMODE"):
                self.assertEqual(stat.S_IMODE(env_path.stat().st_mode), 0o600)


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
