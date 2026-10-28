"""Command-line interface for the study planner."""

import argparse
from datetime import date
from pathlib import Path

from models import StudyTask, parse_due_date
from storage import load_tasks, save_tasks


DEFAULT_DATA_FILE = Path.home() / ".study-planner" / "tasks.json"


def build_parser():
    parser = argparse.ArgumentParser(description="Plan study tasks locally.")
    parser.add_argument(
        "--data-file",
        type=Path,
        default=DEFAULT_DATA_FILE,
        help=f"JSON storage path (default: {DEFAULT_DATA_FILE})",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    add_command = commands.add_parser("add", help="add a study task")
    add_command.add_argument("--title", required=True)
    add_command.add_argument("--course", required=True)
    add_command.add_argument("--due-date", required=True)
    add_command.add_argument(
        "--priority",
        choices=("low", "medium", "high"),
        default="medium",
    )

    list_command = commands.add_parser("list", help="list study tasks")
    list_command.add_argument(
        "--status",
        choices=("all", "pending", "completed"),
        default="all",
    )
    complete_command = commands.add_parser("complete", help="complete a task by ID")
    complete_command.add_argument("task_id", type=int)
    commands.add_parser("summary", help="summarize task progress")
    return parser


def run(args):
    tasks = load_tasks(args.data_file)

    if args.command == "add":
        task_id = max((task.task_id for task in tasks), default=0) + 1
        task = StudyTask(
            task_id=task_id,
            title=args.title.strip(),
            course=args.course.strip(),
            due_date=parse_due_date(args.due_date),
            priority=args.priority,
        )
        tasks.append(task)
        save_tasks(args.data_file, tasks)
        print(
            f"Added task #{task.task_id}: {task.title} ({task.course}) "
            f"[{task.priority}], due {task.due_date}."
        )
        return 0

    if args.command == "list":
        selected = [
            task
            for task in tasks
            if args.status == "all"
            or (args.status == "completed") == task.completed
        ]
        if not selected:
            print("No study tasks found.")
            return 0
        for task in selected:
            status = "completed" if task.completed else "pending"
            print(
                f"#{task.task_id} | {task.due_date} | {status} | "
                f"{task.priority} | {task.course} | {task.title}"
            )
        return 0

    if args.command == "complete":
        if args.task_id <= 0:
            raise ValueError("task ID must be positive")
        for index, task in enumerate(tasks):
            if task.task_id == args.task_id:
                if task.completed:
                    raise ValueError(f"task #{args.task_id} is already completed")
                completed_task = StudyTask(
                    task_id=task.task_id,
                    title=task.title,
                    course=task.course,
                    due_date=task.due_date,
                    priority=task.priority,
                    completed=True,
                )
                tasks[index] = completed_task
                save_tasks(args.data_file, tasks)
                print(
                    f"Completed task #{completed_task.task_id}: "
                    f"{completed_task.title}."
                )
                return 0
        raise ValueError(f"task #{args.task_id} was not found")

    if args.command == "summary":
        completed_count = sum(task.completed for task in tasks)
        pending_count = len(tasks) - completed_count
        overdue_count = sum(
            not task.completed and task.due_date < date.today() for task in tasks
        )
        print(f"Total tasks: {len(tasks)}")
        print(f"Pending: {pending_count}")
        print(f"Completed: {completed_count}")
        print(f"Overdue: {overdue_count}")
        return 0

    raise ValueError(f"unsupported command: {args.command}")


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run(args)
    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
