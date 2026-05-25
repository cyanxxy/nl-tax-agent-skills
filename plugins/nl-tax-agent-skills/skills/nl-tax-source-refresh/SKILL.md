---
name: nl-tax-source-refresh
description: Use when validating Dutch tax source snapshots.
disable-model-invocation: true
allowed-tools:
  - Read
  - Grep
  - Write
  - Edit
  - Bash(python3 *.py:*)
---

# NL Tax Source Refresh

Developer-only maintenance for source snapshots, source registers, and workflow gates.

Use `_shared/source-register.yaml`, `_shared/supported-workflows.yaml`, `reference/official-domain-allowlist.md`, and `reference/refresh-policy.md`. Run the scripts in `scripts/` to validate registers, build reviewed snapshot metadata, and plan source refreshes.

`scripts/fetch_sources.py --fetch` is a dry-run refresh planner. It reports stale allowlisted sources that would need manual refresh. No live HTTP requests are made, and source snapshots are not rewritten.

Only use allowlisted official HTTPS domains. Do not read/write taxpayer workspace data. Do not unlock future years by copying old rates.
