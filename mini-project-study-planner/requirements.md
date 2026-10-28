# Requirements: Study Planner

## Goal

Build a local command-line study planner that helps one student organize
coursework by due date and priority. The application stores tasks in a JSON
file and works without a network connection.

## Functional requirements

- **REQ-01 - Add a task:** Create a task with a non-empty title and course, a
  valid due date in `YYYY-MM-DD` format, and a priority of `low`, `medium`, or
  `high`. Assign each task a unique positive integer ID.
- **REQ-02 - List tasks:** Show tasks in insertion order. Support filtering
  for all, pending, or completed tasks.
- **REQ-03 - Complete a task:** Mark a pending task complete by ID. Report an
  error if the ID is invalid or unknown.
- **REQ-04 - Summarize tasks:** Show total, pending, completed, and overdue
  task counts. A pending task is overdue when its due date is before the
  current local date.
- **REQ-05 - Persist tasks:** Store tasks locally as JSON and reload them on
  later commands. Use an atomic file replacement when saving.
- **REQ-06 - Validate data:** Reject invalid input and malformed or
  unsupported stored data with a clear error. Never silently discard saved
  tasks.

## Constraints

- Use Python's standard library only.
- Make the storage path configurable with `--data-file`.
- Default to `~/.study-planner/tasks.json`, outside the source tree.
- Keep the app single-user, offline, and command-line based.

## Out of scope

- Accounts, cloud sync, calendar integrations, notifications, collaboration,
  and automatic AI-generated study plans.
