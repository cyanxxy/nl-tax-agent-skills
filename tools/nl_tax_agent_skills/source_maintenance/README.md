# NL Tax Source Maintenance

These are repository-only developer tools for validating the source register,
reviewed-note metadata, workflow gates, and cross-host invocation metadata.
They are deliberately outside `plugins/nl-tax-agent-skills/` and are not
installed in Claude, Cowork, ChatGPT Work, or Codex.

The canonical runtime data remains under:

- `plugins/nl-tax-agent-skills/skills/_shared/source-register.yaml`
- `plugins/nl-tax-agent-skills/skills/_shared/knowledge/`

Reviewed-note hashes live in repository-only mirrored directories under
`tools/nl_tax_agent_skills/source_maintenance/metadata/`. They are release
validation data and are deliberately excluded from installed plugin context.
The active/blocked workflow validation gate is likewise repository-only at
`tools/nl_tax_agent_skills/source_maintenance/supported-workflows.yaml`; runtime
skills carry the supported routes and boundaries they actually execute.

Run scripts from the repository root. For example:

```bash
python3 tools/nl_tax_agent_skills/source_maintenance/scripts/validate_source_register.py \
  plugins/nl-tax-agent-skills/skills/_shared/source-register.yaml
python3 tools/nl_tax_agent_skills/source_maintenance/scripts/validate_knowledge_pack.py \
  plugins/nl-tax-agent-skills/skills/_shared/source-register.yaml
python3 tools/nl_tax_agent_skills/source_maintenance/scripts/plan_source_refresh.py all
python3 tools/nl_tax_agent_skills/source_maintenance/scripts/build_runtime_projections.py
```

`plan_source_refresh.py <annual|provisional|box3|all> [year] --fetch` remains a
plan-only report. It makes no live HTTP request and rewrites no reviewed note.
See `reference/refresh-policy.md` and
`reference/official-domain-allowlist.md` for maintainer policy.

`build_runtime_projections.py` preserves the reviewed request/change/stopzetten
notes byte-for-byte and regenerates the three installed human-only projections.
Each projection records the raw note hash and source ids, and inserts only a
mechanically reversible `**Taxpayer:**` prefix before portal imperatives. It
does not review, reattest, or modify a source snapshot.

## What the validators check (and what they do not)

- The validators verify **metadata consistency only**: that ids/paths/local reviewed-note hashes match, that `review_status` and `source_id` registrations are internally coherent, and that every cited `source_id` is registered. `review_status: reviewed` and source-register `last_checked` are **human attestations** that someone checked the local note against the cited official source — they are not machine proof of legal accuracy or URL reachability. `reviewed_note_hash_sha256` hashes the local reviewed note, never a remote page body. A green validator run does not certify that a rate or rule is correct.
- The must-cite-a-`source_id` check exempts the internal `methods/` and
  `security/` prefixes because they contain runtime conversation or product-scope
  guidance rather than tax-rule restatements. Maintainer-only platform,
  future-compatibility, and rule-authoring notes live under
  `docs/maintainers/source-notes/` and do not ship in the plugin.
- Freshness: prose cadences (for example "check monthly") are now parsed, and a stale source whose `mandatory_for` is non-empty blocks validation. Refresh or re-attest stale mandatory sources before relying on a passing run.

## Cross-host maintenance

When adding or renaming a skill, keep the hosts in sync:

- Add the skill name to `VALID_SKILL_NAMES` in
  `scripts/validate_source_register.py`.
- Codex reads each skill's `agents/openai.yaml` for invocation policy (`user-invocable` / `disable-model-invocation` are Claude-frontmatter only). Helper and developer-only skills must ship an `agents/openai.yaml`; mirror any policy change there.
- Codex does not enforce Claude-only frontmatter; runtime write boundaries must
  stay in each installed `SKILL.md` body.
