# Agentic benchmark seed

This intentionally minimal workspace is copied for each conversational
benchmark scenario. Plugin Eval installs the plugin separately. The workspace
contains no taxpayer fixture, answer template, expected output, or case marker.

`verify-hard-contracts.sh` checks only the 0.4 file boundaries: under
`workspace/` only `workspace/nl-tax-annual-2025-workpack.md`,
`workspace/nl-tax-provisional-2026-workpack.md` and the identity-scoped VAT,
VAT-correction, ICP, OSS, international and annual 2026 workpack paths may
exist; there is no second `workspace/` tree or workpack copy; a workpack that
exists records `save_consent: given` and the workflow its file name encodes,
names no other workpack file (including another period, scheme or form of the
same kind), and a provisional workpack never collects werkelijk rendement. A
single-request benchmark run normally ends with no file at all, because saving
needs the user's consent. The script does not score tax reasoning, wording,
question order, or usefulness; those are reviewed with `agentic-rubric.json`.
