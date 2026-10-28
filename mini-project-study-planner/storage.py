"""JSON persistence for study tasks."""

import json
import os
import tempfile
from pathlib import Path

from models import StudyTask


def load_tasks(path):
    """Load tasks, returning an empty list only when the file is absent."""
    file_path = Path(path)
    if not file_path.exists():
        return []
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(
            f"could not read task data from {file_path}: {error}"
        ) from error
    if not isinstance(data, list):
        raise ValueError(f"task data in {file_path} must be a JSON list")
    try:
        tasks = [StudyTask.from_dict(item) for item in data]
        task_ids = [task.task_id for task in tasks]
        if len(task_ids) != len(set(task_ids)):
            raise ValueError("task IDs must be unique")
        return tasks
    except ValueError as error:
        raise ValueError(f"invalid task data in {file_path}: {error}") from error


def save_tasks(path, tasks):
    """Atomically write all tasks to a JSON file."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=file_path.parent,
            prefix=f".{file_path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            json.dump([task.to_dict() for task in tasks], temporary_file, indent=2)
            temporary_file.write("\n")
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        temporary_path.replace(file_path)
    except OSError:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raise
