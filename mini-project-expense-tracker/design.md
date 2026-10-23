# Design: Personal Expense Tracker

## Architecture

The application is split into three small modules:

1. `models.py` defines and validates an `Expense` record and its JSON shape.
2. `storage.py` loads and saves the JSON list, writing updates atomically so
   an interrupted save does not leave a partially written data file.
3. `cli.py` parses commands, calls the model/storage layer, and presents
   errors and results to the user.

The CLI accepts an optional `--data-file` path. If omitted, it uses
`~/.expense-tracker/expenses.json`.

## Data model

Each expense contains:

| Field | Type | Rule |
|---|---|---|
| `amount` | decimal string in JSON | Must be finite and greater than zero |
| `category` | string | Must contain non-whitespace text |
| `description` | string | Must contain non-whitespace text |
| `date` | ISO date string | Must be a valid `YYYY-MM-DD` date |

Amounts are encoded as strings in JSON to avoid binary floating-point
rounding errors.

## Commands

- `add --amount AMOUNT --category CATEGORY --description TEXT [--date DATE]`
- `list`
- `summary`

Errors go to the command-line parser as a readable message and return a
nonzero exit status. Corrupt saved data is reported; it is not overwritten
with an empty list.

## AI-assisted design review prompt

> Review requirements.md and propose a minimal Python standard-library
> architecture for a CLI expense tracker. Define validated data fields,
> commands, persistence format, error behavior, and test cases. Preserve
> decimal money precision and do not add features outside the requirements.
