# Agentic benchmark seed

This intentionally minimal workspace is copied for each conversational
benchmark scenario. Plugin Eval installs the plugin separately. The workspace
contains no taxpayer fixture, answer template, expected output, or case marker.

`verify-hard-contracts.sh` checks only cross-scenario artifact invariants. It
does not score tax reasoning, wording, question order, or usefulness; those are
reviewed with `agentic-rubric.json`.
