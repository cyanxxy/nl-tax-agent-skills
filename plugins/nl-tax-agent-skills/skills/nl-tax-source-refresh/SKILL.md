---
name: nl-tax-source-refresh
description: Use when a developer explicitly wants to validate tax sources and workflow gates, rebuild reviewed-note metadata, or plan an official-source refresh. Never use for taxpayer work.
argument-hint: "[annual|provisional|box3|all] [year]"
disable-model-invocation: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - Bash(python3:*)
---

# NL Tax Source Refresh

Developer-only maintenance for source snapshots, source registers, and workflow gates.

Use `_shared/source-register.yaml`, `_shared/supported-workflows.yaml`,
`reference/official-domain-allowlist.md`, and `reference/refresh-policy.md`.
Read `../_shared/runtime-contract.md` first. Resolve bundled files relative to
this skill directory with the host's skill-resource or file tools. Run scripts
in `scripts/` only when the execution environment can access the resolved
plugin script path.

Path convention: `source-register.yaml` `snapshot_path` values are repo-root/plugin-root relative and include the leading `skills/` segment. Skill instructions often use skill-relative paths such as `_shared/knowledge/...`; those refer to the same files after resolving from the loaded skill tree, but they are not the register serialization format.

`scripts/plan_source_refresh.py <scope> [year] --fetch` — scope is a required positional (`annual | provisional | box3 | all`), e.g. `plan_source_refresh.py all --fetch` — is a plan-only refresh reporter. It reports stale allowlisted sources that would need manual refresh. No live HTTP requests are made, and source snapshots are not rewritten.

Only use allowlisted official HTTPS domains. Do not read/write taxpayer workspace data. Do not unlock future years by copying old rates.

Safety: only run Python under an already-resolved plugin `skills/.../scripts/`
path (this skill's validators and refresh planners live in
`skills/nl-tax-source-refresh/scripts/`), and only if the execution environment
can access that path. If it cannot, report that scripted maintenance requires a
runtime with shell access to the installed plugin; never copy bundled scripts
into `workspace/`. Never execute a `.py` located under `workspace/`, `uploads/`,
or `evidence/`.

## What the validators check (and what they do not)

- The validators verify **metadata consistency only**: that ids/paths/local reviewed-note hashes match, that `review_status` and `source_id` registrations are internally coherent, and that every cited `source_id` is registered. `review_status: reviewed` and source-register `last_checked` are **human attestations** that someone checked the local note against the cited official source — they are not machine proof of legal accuracy or URL reachability. `reviewed_note_hash_sha256` hashes the local reviewed note, never a remote page body. A green validator run does not certify that a rate or rule is correct.
- The must-cite-a-`source_id` check exempts four internal knowledge prefixes — `methods/`, `platform/`, `security/`, and `compat/` — because these are authored internal playbooks rather than restatements of an external authority. Any `source_id` those files *do* cite is still validated against the register.
- Freshness: prose cadences (for example "check monthly") are now parsed, and a stale source whose `mandatory_for` is non-empty blocks validation. Refresh or re-attest stale mandatory sources before relying on a passing run.

## Cross-host maintenance

When adding or renaming a skill, keep the hosts in sync:

- Add the skill name to `VALID_SKILL_NAMES` in `scripts/validate_source_register.py`.
- Codex reads each skill's `agents/openai.yaml` for invocation policy (`user-invocable` / `disable-model-invocation` are Claude-frontmatter only). Helper and developer-only skills must ship an `agents/openai.yaml`; mirror any policy change there.
- Codex does not enforce `allowed-tools` — write-boundary rules must also be stated in the SKILL.md body (see each helper's "Must NOT write to" block).
