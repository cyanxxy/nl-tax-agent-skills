---
name: nl-tax-source-refresh
description: Developer-only maintenance — validate Dutch tax source registers and supported-workflow gates, rebuild reviewed snapshot metadata, and plan official-source refreshes. Not a taxpayer workflow; never reads or writes workspace/uploads/evidence.
disable-model-invocation: true
allowed-tools:
  - Read
  - Grep
  - Write
  - Edit
  - Bash(python3:*)
---

# NL Tax Source Refresh

Developer-only maintenance for source snapshots, source registers, and workflow gates.

Use `_shared/source-register.yaml`, `_shared/supported-workflows.yaml`, `reference/official-domain-allowlist.md`, and `reference/refresh-policy.md`. Resolve bundled files with host file tools (`Read` first, `Glob` or `Grep` if a path is not obvious). Do not use Bash to discover or read plugin files: in Cowork, shell commands run in an isolated VM that may not see the plugin cache even when `Read` and `Glob` can. Run the scripts in `scripts/` to validate registers, build reviewed snapshot metadata, and plan source refreshes only when Bash can access the resolved plugin script path.

Path convention: `source-register.yaml` `snapshot_path` values are repo-root/plugin-root relative and include the leading `skills/` segment. Skill instructions often use skill-relative paths such as `_shared/knowledge/...`; those refer to the same files after resolving from the loaded skill tree, but they are not the register serialization format.

`scripts/fetch_sources.py --fetch` is a plan-only refresh reporter. It reports stale allowlisted sources that would need manual refresh. No live HTTP requests are made, and source snapshots are not rewritten.

Only use allowlisted official HTTPS domains. Do not read/write taxpayer workspace data. Do not unlock future years by copying old rates.

Safety: only run Python under an already-resolved plugin `skills/.../scripts/` path (this skill's validators and refresh planners live in `skills/nl-tax-source-refresh/scripts/`), and only if Bash can access that path. If Bash cannot see the plugin path, report that scripted maintenance requires Claude Code or another shell with plugin-cache access; never copy bundled scripts into `workspace/`. Never execute a `.py` located under `workspace/`, `uploads/`, or `evidence/`.

## What the validators check (and what they do not)

- The validators verify **metadata consistency only**: that ids/paths/hashes match, that `review_status` and `source_id` registrations are internally coherent, and that every cited `source_id` is registered. `review_status: reviewed` is a **human attestation** that someone checked the note against the cited official source — it is not machine proof of legal accuracy. A green validator run does not certify that a rate or rule is correct.
- The must-cite-a-`source_id` check exempts four internal knowledge prefixes — `methods/`, `platform/`, `security/`, and `compat/` — because these are authored internal playbooks rather than restatements of an external authority. Any `source_id` those files *do* cite is still validated against the register.
- Freshness: prose cadences (for example "check monthly") are now parsed, and a stale source whose `mandatory_for` is non-empty blocks validation. Refresh or re-attest stale mandatory sources before relying on a passing run.

## Cross-host maintenance

When adding or renaming a skill, keep the hosts in sync:

- Add the skill name to `VALID_SKILL_NAMES` in `scripts/validate_source_register.py`.
- Codex reads each skill's `agents/openai.yaml` for invocation policy (`user-invocable` / `disable-model-invocation` are Claude-frontmatter only). Helper and developer-only skills must ship an `agents/openai.yaml`; mirror any policy change there.
- Codex does not enforce `allowed-tools` — write-boundary rules must also be stated in the SKILL.md body (see each helper's "Must NOT write to" block).
