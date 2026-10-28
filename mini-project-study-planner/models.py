"""Validated task model for the study planner."""

from dataclasses import dataclass
from datetime import date


PRIORITIES = frozenset({"low", "medium", "high"})


def parse_due_date(value):
    """Parse a strict YYYY-MM-DD date."""
    try:
        parsed = date.fromisoformat(value)
    except (TypeError, ValueError) as error:
        raise ValueError("due date must be a valid YYYY-MM-DD date") from error
    if parsed.isoformat() != value:
        raise ValueError("due date must be a valid YYYY-MM-DD date")
    return parsed


@dataclass(frozen=True)
class StudyTask:
    task_id: int
    title: str
    course: str
    due_date: date
    priority: str = "medium"
    completed: bool = False

    def __post_init__(self):
        if isinstance(self.task_id, bool) or not isinstance(self.task_id, int):
            raise ValueError("task ID must be an integer")
        if self.task_id <= 0:
            raise ValueError("task ID must be positive")
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("title must not be blank")
        if not isinstance(self.course, str) or not self.course.strip():
            raise ValueError("course must not be blank")
        if type(self.due_date) is not date:
            raise ValueError("due date must be a date")
        if not isinstance(self.priority, str) or self.priority not in PRIORITIES:
            raise ValueError("priority must be low, medium, or high")
        if not isinstance(self.completed, bool):
            raise ValueError("completed must be a boolean")

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "course": self.course,
            "due_date": self.due_date.isoformat(),
            "priority": self.priority,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError("each task must be a JSON object")
        required_fields = {
            "task_id",
            "title",
            "course",
            "due_date",
            "priority",
            "completed",
        }
        if set(data) != required_fields:
            raise ValueError("task fields do not match the supported schema")
        return cls(
            task_id=data["task_id"],
            title=data["title"],
            course=data["course"],
            due_date=parse_due_date(data["due_date"]),
            priority=data["priority"],
            completed=data["completed"],
        )
