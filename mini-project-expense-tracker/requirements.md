# Requirements: Personal Expense Tracker

## Goal

Build a small command-line application that lets one person record and review
personal expenses stored locally as JSON.

## Functional requirements

- **REQ-01 - Record expenses:** Add an expense with a positive amount, a
  non-empty category, a non-empty description, and an expense date.
- **REQ-02 - Default date:** If the user does not provide a date, use the
  current local date. Accept explicitly provided dates in `YYYY-MM-DD` format.
- **REQ-03 - List expenses:** Show saved expenses in insertion order with
  amount, category, description, and date.
- **REQ-04 - Summarize expenses:** Show the total amount and totals grouped by
  category.
- **REQ-05 - Persist data:** Save expenses to a local JSON file and reload
  them on the next command.
- **REQ-06 - Validate data:** Reject invalid amounts, blank text fields,
  malformed dates, and malformed or unsupported stored data with a clear
  error. Do not silently discard data.

## Constraints

- Use Python's standard library only.
- Use decimal arithmetic for money and display exactly two decimal places.
- Do not require a network connection or external service.
- Keep the storage path configurable; default to a file in the user's home
  directory rather than creating data in the source tree.

## Out of scope

- User accounts, cloud synchronization, budgets, currencies, and bank
  integrations.
