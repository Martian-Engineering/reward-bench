import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError

from scripts.run_jev import choose, main, payload, select_rows


class JevPilotTests(unittest.TestCase):
    def test_selection_is_seeded_and_balanced_by_subset(self):
        rows = [{"id": index, "subset": "chat" if index < 10 else "hard"} for index in range(20)]
        first = select_rows(rows, ("chat", "hard"), 3, 100)
        second = select_rows(list(reversed(rows)), ("chat", "hard"), 3, 100)
        self.assertEqual(first, second)
        self.assertEqual([row["subset"] for row in first], ["chat"] * 3 + ["hard"] * 3)

    def test_request_contains_both_answers_and_validates_choice(self):
        request_payload = payload("Name a color", "Blue", "Triangle", "jev-test")
        self.assertEqual(request_payload["state"]["observation"], "User request:\nName a color")
        self.assertEqual(
            request_payload["questions"]["better_response"]["criteria"],
            {"A": "Blue", "B": "Triangle"},
        )
        response = io.BytesIO(
            json.dumps({"answers": {"better_response": {"choice": "A"}}, "usage": {"input_tokens": 20}}).encode()
        )
        with patch("urllib.request.urlopen", return_value=response) as urlopen:
            choice, input_tokens, _, _ = choose(request_payload, "https://example.test", "test-key")
        self.assertEqual((choice, input_tokens), ("A", 20))
        sent = json.loads(urlopen.call_args.args[0].data)
        self.assertEqual(sent, request_payload)

    def test_authentication_error_exits_nonzero_and_preserves_partial_result(self):
        row = {"id": 1, "subset": "chat", "prompt": "Name a color", "chosen": "Blue", "rejected": "Triangle"}
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "pilot.jsonl"
            with (
                patch.dict(os.environ, {"TYPESAFE_API_KEY": "test-key"}),
                patch("sys.argv", ["run_jev.py", "--subsets", "chat", "--per-subset", "1", "--output", str(output)]),
                patch("scripts.run_jev.fetch_rows", return_value=[row]),
                patch("scripts.run_jev.choose", side_effect=HTTPError("https://example.test", 401, "", {}, None)),
            ):
                with self.assertRaises(SystemExit) as exit_error:
                    main()
            self.assertEqual(exit_error.exception.code, 1)
            records = [json.loads(line) for line in output.read_text().splitlines()]
            self.assertEqual(records[1]["orders"], [{"expected": "A", "error": "HTTPError"}])


if __name__ == "__main__":
    unittest.main()
