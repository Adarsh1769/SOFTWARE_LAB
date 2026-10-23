"""Tests for the Practical 8 story completeness checker."""

import unittest
from pathlib import Path

from check_stories import evaluate


HERE = Path(__file__).resolve().parent
SRS = (HERE / "srs_excerpt.txt").read_text(encoding="utf-8")


class StoryCompletenessTests(unittest.TestCase):
    def test_draft_one_is_flagged_incomplete(self):
        stories = (HERE / "draft1_stories.md").read_text(encoding="utf-8")
        results = evaluate(SRS, stories)

        self.assertEqual(len(results), 4)
        self.assertFalse(all(
            result["covered"]
            and result["story_format"]
            and all(result["criteria"].values())
            for result in results
        ))
        self.assertFalse(results[0]["story_format"])
        self.assertFalse(results[1]["criteria"]["Then"])
        self.assertFalse(results[3]["covered"])

    def test_revised_stories_pass_every_completeness_check(self):
        stories = (HERE / "revised_stories.md").read_text(encoding="utf-8")
        results = evaluate(SRS, stories)

        self.assertEqual(len(results), 4)
        for result in results:
            self.assertTrue(result["covered"], result["id"])
            self.assertTrue(result["story_format"], result["id"])
            self.assertTrue(all(result["criteria"].values()), result["id"])


if __name__ == "__main__":
    unittest.main()
