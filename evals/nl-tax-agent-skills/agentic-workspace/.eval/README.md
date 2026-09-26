# Agentic benchmark seed

This intentionally minimal workspace is copied for each conversational
benchmark scenario. Plugin Eval installs the plugin separately. The workspace
contains no taxpayer fixture, answer template, expected output, or case marker.

`verify-hard-contracts.sh` checks only the 0.4 file boundaries: under
`workspace/` nothing but `workspace/nl-tax-annual-2025-workpack.md` and
`workspace/nl-tax-provisional-2026-workpack.md` may exist; there is no second
`workspace/` tree or workpack copy; a workpack that exists records
`save_consent: given` and its own workflow, never names the other workflow's
file, and a provisional workpack never collects werkelijk rendement. A
single-request benchmark run normally ends with no file at all, because saving
needs the user's consent. The script does not score tax reasoning, wording,
question order, or usefulness; those are reviewed with `agentic-rubric.json`.
