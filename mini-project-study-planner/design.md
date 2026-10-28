# Design: Study Planner

## Architecture

1. `models.py` defines the validated `StudyTask` record and JSON conversion.
2. `storage.py` loads and atomically saves a JSON list of tasks. A missing
   file means there are no tasks; malformed or unsupported data is reported
   and is never replaced with an empty list.
3. `cli.py` parses commands, applies task operations, and prints results.
4. `test_study_planner.py` covers model validation, persistence, and
   end-to-end CLI behavior using temporary files.

## Data model

| Field | Type | Rule |
|---|---|---|
| `task_id` | integer | Positive and unique |
| `title` | string | Must contain non-whitespace text |
| `course` | string | Must contain non-whitespace text |
| `due_date` | ISO date string | Valid date written as `YYYY-MM-DD` |
| `priority` | string | One of `low`, `medium`, or `high` |
| `completed` | boolean | `false` until completed |

Tasks are serialized as a JSON array, preserving insertion order. The next
task ID is one greater than the largest saved ID.

## Commands

- `add --title TITLE --course COURSE --due-date YYYY-MM-DD [--priority LEVEL]`
- `list [--status all|pending|completed]`
- `complete TASK_ID`
- `summary`

The global `--data-file PATH` option can be supplied before a command. If
omitted, the path is `~/.study-planner/tasks.json`. Invalid arguments and
storage errors produce a readable error and a nonzero exit status.

## Design review checklist

- Every command maps to a functional requirement.
- Persisted fields are validated on both load and creation.
- Updates use a temporary file in the destination directory before atomic
  replacement.
- Tests use temporary storage and do not touch a user's actual task list.
- No network, account, calendar, or notification feature is introduced.
