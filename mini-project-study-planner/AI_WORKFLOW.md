# AI-assisted SDLC workflow: Study Planner

This project uses an AI coding assistant (GitHub Copilot, Windsurf, or
Ollama) as a collaborator through the software development lifecycle. Keep
the requirements as the source of truth: AI suggestions are proposals, and a
human reviews them before they are accepted.

## 1. Requirements analysis

**Prompt**

> Write concise, testable requirements for a single-user, offline Python CLI
> study planner. Include adding tasks with course, due date, and priority;
> listing with status filters; completing tasks by ID; a summary with
> overdue counts; local JSON persistence; validation; constraints; and
> out-of-scope features. Give each requirement a stable ID. Do not add a web
> service, account, calendar, or notification feature.

**Review gate:** Check that every requirement is testable and that the scope
is different from an expense tracker. The accepted requirements are in
`requirements.md`.

## 2. Design

**Prompt**

> Design the smallest Python-standard-library architecture that satisfies
> requirements.md. Define the task schema, CLI commands, local JSON format,
> validation, error behavior, and test plan. Ensure malformed saved data is
> reported rather than overwritten, IDs stay unique, and writes are atomic.
> Identify any requirement the design does not cover.

**Review gate:** Trace each requirement to a module and test. Reject proposed
features that are outside the approved requirements. The accepted design is
in `design.md`.

## 3. Implementation

**Prompt**

> Implement the approved design in models.py, storage.py, and cli.py using
> only the Python standard library. Validate all task fields both when
> created and when loaded from JSON. Preserve insertion order, assign the
> next ID safely, filter statuses correctly, and report errors without
> silently replacing corrupt data. Keep the implementation limited to the
> approved requirements.

**Review gate:** Compare the code to `requirements.md` and `design.md`.
Inspect input validation, status transitions, ID generation, data-loss
behavior, and atomic replacement before running the tests.

## 4. Test design and execution

**Prompt**

> Propose unittest cases for every requirement in requirements.md. Include
> blank fields, invalid dates and priorities, malformed JSON and schema,
> missing data files, duplicate IDs, status filtering, unknown completion
> IDs, overdue calculation, and an add/list/complete/summary CLI flow using
> temporary storage. Do not weaken assertions to make implementation pass.

**Review gate:** Confirm every case has an observable assertion and uses
temporary files. Run the checked-in suite from the repository root:

```powershell
py -3 -m unittest discover -s mini-project-study-planner -p test_study_planner.py -v
```

The suite is expected to pass all tests. Keep the actual test-run output with
the project submission; do not report an unrun test as passing.

## 5. Demonstration and acceptance

Run the CLI against a disposable file and compare the results with the
requirements:

```powershell
$demoFile = Join-Path $env:TEMP "study-planner-demo.json"
py -3 mini-project-study-planner\cli.py --data-file $demoFile add --title "Read chapter 4" --course Biology --due-date 2026-12-01 --priority high
py -3 mini-project-study-planner\cli.py --data-file $demoFile add --title "Solve exercises" --course Mathematics --due-date 2026-12-03
py -3 mini-project-study-planner\cli.py --data-file $demoFile list --status pending
py -3 mini-project-study-planner\cli.py --data-file $demoFile complete 1
py -3 mini-project-study-planner\cli.py --data-file $demoFile summary
Remove-Item $demoFile
```

Check that IDs are stable, the list filter works, task 1 becomes completed,
and summary counts agree. Review the final diff and test output before
committing or pushing. Never use real coursework data for a demo.

## 6. CI/CD

The repository's `.github/workflows/ci.yml` runs the Study Planner and
Practical 11 test suites on pushes and pull requests that touch either
project or the workflow.

**Prompt**

> Review the existing GitHub Actions workflow and requirements.md. Add the
> smallest CI change that runs the Study Planner test suite on relevant
> pushes and pull requests. Preserve the existing Practical 11 checks and
> pin the Python version consistently with the current workflow.

**Review gate:** Confirm path filters include this project and that both
existing and new test commands remain in the workflow. The local test run is
necessary but does not replace checking the remote Actions result after a
push.

## 7. Maintenance

When changing behavior, ask the assistant to identify affected requirements
and tests before editing. Review the proposed change, add or update focused
tests, run the suite above, and update this workflow or the design if the
approved behavior changes.
