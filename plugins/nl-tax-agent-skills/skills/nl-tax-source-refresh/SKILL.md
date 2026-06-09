---
name: nl-tax-source-refresh
description: Developer-only maintenance — validate Dutch tax source registers and supported-workflow gates, rebuild reviewed snapshot metadata, and plan official-source refreshes. Not a taxpayer workflow; never reads or writes workspace/uploads/evidence.
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

## Cross-host maintenance

When adding or renaming a skill, keep the hosts in sync:

- Add the skill name to `VALID_SKILL_NAMES` in `scripts/validate_source_register.py`.
- Codex reads each skill's `agents/openai.yaml` for invocation policy (`user-invocable` / `disable-model-invocation` are Claude-frontmatter only). Helper and developer-only skills must ship an `agents/openai.yaml`; mirror any policy change there.
- Codex does not enforce `allowed-tools` — write-boundary rules must also be stated in the SKILL.md body (see each helper's "Must NOT write to" block).
