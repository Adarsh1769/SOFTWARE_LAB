"""Tests for the Practical 9 DOT source verification."""

import unittest
from pathlib import Path

from verify_diagram import verify_source


DOT_SOURCE = Path(__file__).with_name("library_er.dot").read_text(
    encoding="utf-8"
)


class DiagramSourceTests(unittest.TestCase):
    def test_example_contains_all_entities_and_relationships(self):
        self.assertEqual(verify_source(DOT_SOURCE), [])

    def test_missing_entity_and_relationship_are_reported(self):
        incomplete = DOT_SOURCE.replace("AUTHOR -> BOOK_AUTHOR [label=", "AUTHOR -- BOOK_AUTHOR [label=")
        incomplete = incomplete.replace("    LOAN [label=<", "    ARCHIVE [label=<")
        issues = verify_source(incomplete)

        self.assertIn("Missing entity definition: LOAN", issues)
        self.assertIn("Missing relationship: AUTHOR to BOOK_AUTHOR", issues)


if __name__ == "__main__":
    unittest.main()
