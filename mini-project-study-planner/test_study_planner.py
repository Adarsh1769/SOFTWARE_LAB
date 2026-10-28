"""Tests for study task validation, persistence, and CLI behavior."""

import contextlib
import io
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from cli import main
from models import StudyTask, parse_due_date
from storage import load_tasks, save_tasks


class StudyTaskModelTests(unittest.TestCase):
    def test_due_date_parser_requires_strict_iso_date(self):
        self.assertEqual(parse_due_date("2026-10-28"), date(2026, 10, 28))
        for invalid_date in ("2026-02-30", "20261028", "2026-W44-3"):
            with self.subTest(invalid_date=invalid_date):
                with self.assertRaisesRegex(ValueError, "YYYY-MM-DD"):
                    parse_due_date(invalid_date)

    def test_task_rejects_invalid_fields(self):
        valid = {
            "task_id": 1,
            "title": "Read chapter",
            "course": "Biology",
            "due_date": date(2026, 10, 28),
        }
        invalid_fields = (
            {"task_id": 0},
            {"task_id": True},
            {"title": "  "},
            {"course": " "},
            {"priority": "urgent"},
            {"priority": []},
            {"completed": 1},
        )
        for field in invalid_fields:
            with self.subTest(field=field), self.assertRaises(ValueError):
                StudyTask(**(valid | field))


class StudyTaskStorageTests(unittest.TestCase):
    def test_save_and_load_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "tasks.json"
            original = [
                StudyTask(1, "Read chapter", "Biology", date(2026, 10, 28), "high")
            ]
            save_tasks(path, original)
            self.assertEqual(load_tasks(path), original)

    def test_missing_file_is_empty_but_corrupt_data_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"
            self.assertEqual(load_tasks(path), [])
            path.write_text("{bad json", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "could not read"):
                load_tasks(path)
            path.write_text(json.dumps([{"task_id": 1}]), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "supported schema"):
                load_tasks(path)

    def test_duplicate_task_ids_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"
            task = StudyTask(1, "Read chapter", "Biology", date(2026, 10, 28))
            save_tasks(path, [task, task])
            with self.assertRaisesRegex(ValueError, "unique"):
                load_tasks(path)


class StudyPlannerCliTests(unittest.TestCase):
    def test_add_filter_complete_and_summary_flow(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(
                    main(
                        [
                            "--data-file",
                            str(path),
                            "add",
                            "--title",
                            "Read chapter",
                            "--course",
                            "Biology",
                            "--due-date",
                            "2026-10-28",
                            "--priority",
                            "high",
                        ]
                    ),
                    0,
                )
                main(["--data-file", str(path), "list", "--status", "pending"])
                main(["--data-file", str(path), "complete", "1"])
                main(["--data-file", str(path), "list", "--status", "completed"])
                main(["--data-file", str(path), "summary"])

            result = output.getvalue()
            self.assertIn("Added task #1", result)
            self.assertIn(
                "#1 | 2026-10-28 | pending | high | Biology | Read chapter",
                result,
            )
            self.assertIn("Completed task #1", result)
            self.assertIn(
                "#1 | 2026-10-28 | completed | high | Biology | Read chapter",
                result,
            )
            self.assertIn("Total tasks: 1\nPending: 0\nCompleted: 1\nOverdue: 0", result)

    def test_unknown_completion_id_returns_readable_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"
            with contextlib.redirect_stderr(io.StringIO()) as errors:
                with self.assertRaises(SystemExit) as exit_info:
                    main(["--data-file", str(path), "complete", "9"])
            self.assertEqual(exit_info.exception.code, 2)
            self.assertIn("task #9 was not found", errors.getvalue())

    def test_summary_counts_overdue_pending_tasks(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"
            save_tasks(
                path,
                [
                    StudyTask(1, "Past task", "History", date(2000, 1, 1)),
                    StudyTask(
                        2,
                        "Finished task",
                        "History",
                        date(2000, 1, 1),
                        completed=True,
                    ),
                ],
            )
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                main(["--data-file", str(path), "summary"])
            self.assertIn("Overdue: 1", output.getvalue())


if __name__ == "__main__":
    unittest.main()
