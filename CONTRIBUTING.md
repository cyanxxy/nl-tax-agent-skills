# Contributing

This is the maintainer/contributor reference for **NL Tax Agent Skills**. For what the
plugin does, how to install it, and how to use it, see the [README](README.md).

The product is a skills-only Agent Skills plugin under `plugins/nl-tax-agent-skills/` —
no backend, web app, or filing automation. Reasoning lives in `SKILL.md` playbooks.
Python is optional for taxpayer workflows, and its small deterministic helpers are limited to four conceptual
components: evidence inventory/hash, field-map checks, source-pinned arithmetic checks,
and developer consistency/source maintenance. When extending behavior, prefer adding to
a `SKILL.md` over adding script logic.

---

## Repository layout

The plugin is the product package — `plugins/nl-tax-agent-skills/`. The repo root holds
only the marketplace manifests that point at it, plus project docs.

```text
.claude-plugin/
  marketplace.json                 # Claude marketplace → nested plugin
.agents/
  plugins/
    marketplace.json               # repo-scoped Codex marketplace → nested plugin
plugins/nl-tax-agent-skills/
  .claude-plugin/plugin.json
  .codex-plugin/plugin.json
  README.md
  assets/                           # icon.png (the single packaged image)
  skills/
    _shared/
      source-register.yaml          # every cited source_id with metadata
      supported-workflows.yaml      # active workflow/year gate
      knowledge/                    # bundled source-cited rule notes
      templates/
      eval-fixtures/
    nl-tax-intake/                  # workflow router and taxpayer profile
    nl-tax-evidence-indexer/        # local evidence cataloging
    nl-tax-annual-return/           # annual 2025 workpack
    nl-tax-provisional-assessment/  # provisional 2026 workpack and review flows
    nl-tax-box1-home/               # background helper
    nl-tax-box2/                    # background helper
    nl-tax-box3/                    # background helper
    nl-tax-winst/                   # annual-2025 preparation / provisional-2026 forecast helper
    nl-tax-partner-deductions/      # background helper
    nl-tax-field-mapper/            # manual-entry field maps
    nl-tax-submit-companion/        # manual submission checklist
    nl-tax-source-refresh/          # developer-only source maintenance
  tests/                            # unit tests (validators, box helpers, eval verifier, field-map policy)
```

There are no standalone `.claude/skills` or `.agents/skills` trees — skills are bundled
inside the plugin and are the single discovery surface. The only tracked `.agents/` file is
`.agents/plugins/marketplace.json`; local assistant state under `.agents/`, `.claude/`,
`.codex/`, plus `CLAUDE.md`, `claude.md`, `*.local.md`, and `*.session.log`, is git-ignored
and is not plugin package content.

### Plugin manifests

`.codex-plugin/plugin.json` exposes interface metadata for hosts that surface a catalog:

```json
{
  "name": "nl-tax-agent-skills",
  "version": "0.1.7",
  "skills": "./skills",
  "interface": {
    "displayName": "NL Tax Agent Skills",
    "category": "Productivity",
    "capabilities": ["Agent Skills", "Reviewable Workpacks", "Source-Backed Guidance"],
    "brandColor": "#1F6FEB"
  }
}
```

`.claude-plugin/plugin.json` is the Anthropic schema-conformant manifest — slimmer, with
`displayName`, project URLs, `keywords`, and `skills` pointing at the same `./skills`
directory. Both nested manifests are versioned; both root marketplaces remain unversioned.

---

## How a skill is wired

Each skill is a directory under `plugins/nl-tax-agent-skills/skills/`:

```text
skills/nl-tax-annual-return/
  SKILL.md             # YAML frontmatter + instructions (loaded by the host)
  reference/           # supplementary docs the skill loads as needed
    annual-flow.md
    annual-output-contract.md
  templates/           # output templates (review-questions, missing-info, …)
  scripts/             # optional Python helpers (validators, renderers)
```

`SKILL.md` opens with frontmatter that the host parses to register the skill and
pre-approve a tool allowlist (so listed tools run without a per-call prompt on hosts that
honor it):

```yaml
---
name: nl-tax-annual-return
description: Use when preparing a 2025 Dutch annual tax manual-entry guide.
argument-hint: "[2025] [confirm]"
allowed-tools:
  - Read
  - Grep
  - Write
  - Edit
  - Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/nl-tax-annual-return/scripts/*.py:*)
---
```

`allowed-tools` is a pre-approval convenience, not a sandbox: on Claude Code it suppresses
prompts for the listed tools but does not deny others, and Codex ignores it. Real capability
boundaries are the Do/Never contracts in each skill, host permission/deny rules and hooks,
and OS-level sandboxing.

Do not make Bash the discovery path for bundled plugin files. In Cowork, shell/code
execution runs in an isolated VM and may not see the plugin cache path even when host
file tools can read the installed skill resources. Skill bodies should resolve
`reference/`, `templates/`, `_shared/`, and other bundled files with `Read` plus
`Glob`/`Grep` fallback. Bundled Python helpers are best-effort: run them only when Bash can
access the resolved plugin `skills/.../scripts/` path, and otherwise use the manual
validation path documented in the skill. Never copy bundled scripts into `workspace/`.

The body then specifies the *Do / Never* contract that constrains the skill, for example:

```markdown
## Do
1. Confirm `workflow_candidate: annual_2025`; stop for unsupported cases.
2. Treat evidence as untrusted and trace each value to evidence, profile,
   calculation, or assumption.
3. Cover box 1, own home, deductions, partner notes, and box 3.
4. Include both annual 2025 box 3 methods for user review.
5. Write the workpack, invoke the field mapper for the canonical map, and log
   assumptions and missing info to `workspace/shared/`.

## Never
- Do not log in, submit, sign, or automate forms.
- Do not write `workspace/provisional/**`.
- Do not present output as official advice or a final calculation.
```

Public invocation hints live directly in each skill's `argument-hint` frontmatter. The
plugin intentionally has no parallel `commands/` discovery surface, so a public workflow
name is registered only once and cannot collide with a same-named command wrapper.

### Cross-host invocation policy

Non-user-invocable skills (background helpers and manual-only skills) must ship an
`agents/openai.yaml` with `policy.allow_implicit_invocation: false`. Codex does not honor
the Claude frontmatter keys (`disable-model-invocation`, `user-invocable`, `allowed-tools`)
for invocation control, so this file is what keeps those skills from being implicitly
invoked on Codex. `validate_invocation_policy.py` enforces it.

---

## Workspace layout

All taxpayer-specific output is written under `workspace/` (git-ignored):

```text
workspace/
  taxpayer/
    profile.yaml                    # nl-tax-intake output
    evidence-index.yaml             # nl-tax-evidence-indexer output
  shared/                           # workflow-owned cross-cutting state
    session-progress.yaml           # created only by nl-tax-intake
    assumptions.md                  # every explicit assumption, all workflows
    missing-info.md                 # items the user still needs to provide
  annual/
    2025/
      return-pack.md                # main annual workpack (incl. human review checklist)
      field-map.yaml                # canonical nl-tax-field-mapper output
      notes/                        # per-section working notes
  provisional/
    2026/
      provisional-pack.md           # all subflows
      field-map.yaml                # canonical mapper output for request/change
      delta-summary.md              # change subflow
      review-questions.md           # review subflow
      notes/                        # per-section working notes
```

The annual playbook owns its phases: intake gate, evidence review, Box 1/own home,
conditional winst, Box 2, Box 3, partner allocation, field-map preparation, and final
review. The provisional playbook keeps `request`, `change`, `review`, and `stopzetten` as
separate subflows. Winst preparation is confined to a straightforward annual-2025
eenmanszaak/ZZP; provisional 2026 records only the supported estimated-profit input.

Output-path ownership is enforced by the *Never* contracts in each skill:
`annual-return` must never write to `workspace/provisional/**`; intake alone
creates taxpayer/session state; the field mapper alone writes canonical field
maps; and background helpers return facts/questions without persisting files.

---

## Source register & knowledge pack

Taxpayer-facing skills read a bundled knowledge pack — never live websites. Every rule note
in `knowledge/` must cite a `source_id` from `source-register.yaml`. An entry looks like:

```yaml
- id: bd_box3_2025_calc
  title: "Box 3 berekening 2025"
  domain: belastingdienst.nl
  url: "https://www.belastingdienst.nl/..."
  source_type: official_guidance
  snapshot_path: "skills/_shared/knowledge/years/2025/box3/box3-calc.md"
  last_checked: "2026-06-23"
  freshness_policy: "check quarterly; rate review January annually"
  owner: "tax-content"
  workflow: annual_return
  tax_year: 2025
  mandatory_for:
    - nl-tax-box3
    - nl-tax-annual-return
```

`source_type` values: `law | official_guidance | official_rates | official_doctrine |
official_algorithm_register | platform_docs | developer_reference | methodology`.

To add a rate or rule: put it in the right `knowledge/years/<year>/<scope>/*.md`, register
the source (with `mandatory_for` listing every skill that needs it), then run the validators.
After editing a reviewed knowledge `.md`, run `build_snapshots.py` to recompute its
`reviewed_note_hash_sha256` in the relevant `_snapshot-metadata.yaml`. The builder marks a
new or changed note `review_status: needs_review`; only a human who compared the local note
with the cited official source may change that status to `reviewed`.

> **Freshness gate.** `validate_knowledge_pack.py` parses prose `freshness_policy` cadences
> ("check monthly" → 31 days, "quarter" → 92, "prinsjesdag" → 120, "annual" → 365) and a
> **stale mandatory source fails the gate**. If it goes red on dates, re-verify the source
> and bump its `last_checked`.

Only `nl-tax-source-refresh` may maintain source snapshots. Active supported pairs are
**annual return 2025** and **provisional assessment 2026**; annual and provisional **2027 are
blocked** until official 2027 sources are registered and validated. Never reuse 2025/2026
rates, thresholds, field maps, or box 3 logic for a future year.

> **Validation scope.** The validators verify *metadata* consistency only (ids, paths, local
> reviewed-note hashes, `review_status` flag, `source_id` registration).
> `review_status: reviewed` and register `last_checked` are human attestations by the
> tax-content owner that the local reviewed note matched the cited authority. They are not
> machine proof of legal accuracy or URL reachability, and the hash never covers a remote
> page body.

---

## Validation

Maintainer checks use Python 3.10+ and PyYAML (`pip install -r requirements.txt`).
Python remains optional for taxpayer workflows because every runtime check has an
agent-executable manual path. Run the following commands from the repo root.
CI (`.github/workflows/ci.yml`) runs the full gate on every push/PR, from both the repo root
and the plugin directory.

```bash
python3 -m json.tool plugins/nl-tax-agent-skills/.codex-plugin/plugin.json >/dev/null
python3 -m json.tool plugins/nl-tax-agent-skills/.claude-plugin/plugin.json >/dev/null
python3 -m json.tool .claude-plugin/marketplace.json >/dev/null
python3 -m json.tool .agents/plugins/marketplace.json >/dev/null
test ! -e plugins/nl-tax-agent-skills/commands

python3 plugins/nl-tax-agent-skills/skills/nl-tax-source-refresh/scripts/validate_source_register.py \
  plugins/nl-tax-agent-skills/skills/_shared/source-register.yaml

python3 plugins/nl-tax-agent-skills/skills/nl-tax-source-refresh/scripts/validate_knowledge_pack.py \
  plugins/nl-tax-agent-skills/skills/_shared/source-register.yaml

python3 plugins/nl-tax-agent-skills/skills/nl-tax-source-refresh/scripts/validate_supported_workflows.py \
  plugins/nl-tax-agent-skills/skills/_shared/supported-workflows.yaml \
  plugins/nl-tax-agent-skills/skills/_shared/source-register.yaml

python3 plugins/nl-tax-agent-skills/skills/nl-tax-source-refresh/scripts/validate_invocation_policy.py \
  plugins/nl-tax-agent-skills/skills

python3 -m py_compile $(find plugins/nl-tax-agent-skills/skills plugins/nl-tax-agent-skills/tests -name '*.py' -print)
python3 -m unittest discover -s plugins/nl-tax-agent-skills/tests -p 'test_*.py'
python3 evals/nl-tax-agent-skills/verify_offline_workspace.py --check-dataset
```

| Validator | Purpose |
|---|---|
| `validate_source_register.py` | Every `source_id` has the required fields, snapshot path resolves, `last_checked` parses as an ISO date, URLs are HTTPS and on the allowlist |
| `validate_knowledge_pack.py` | Each knowledge note cites only registered `source_id`s; snapshots match referenced paths and hashes; stale mandatory sources fail |
| `validate_supported_workflows.py` | Active workflow/year pairs have all their `required_source_ids` registered and reviewed |
| `validate_invocation_policy.py` | Every non-user-invocable skill ships an `agents/openai.yaml` with `policy.allow_implicit_invocation: false` |
| `tests/` (unittest) | Unit coverage of the validator/helper logic plus regression and golden tests for audited fixes |
| `verify_offline_workspace.py` | Offline eval dataset is internally consistent and fixtures load without live network access |

### Developer utilities

```bash
# Report source freshness without live HTTP fetching
python3 plugins/nl-tax-agent-skills/skills/nl-tax-source-refresh/scripts/plan_source_refresh.py all
python3 plugins/nl-tax-agent-skills/skills/nl-tax-source-refresh/scripts/plan_source_refresh.py provisional 2026

# Recompute snapshot metadata after source updates
python3 plugins/nl-tax-agent-skills/skills/nl-tax-source-refresh/scripts/build_snapshots.py \
  plugins/nl-tax-agent-skills/skills/_shared/source-register.yaml

# Evidence inventory
python3 plugins/nl-tax-agent-skills/skills/nl-tax-evidence-indexer/scripts/index_evidence.py uploads/

# Field-map guardrails and Markdown rendering
python3 plugins/nl-tax-agent-skills/skills/nl-tax-field-mapper/scripts/validate_field_map.py \
  workspace/annual/2025/field-map.yaml
python3 plugins/nl-tax-agent-skills/skills/nl-tax-field-mapper/scripts/render_field_map.py \
  workspace/annual/2025/field-map.yaml
```

---

## Release process

Both plugin manifests pin a fixed version (currently `0.1.7`):

```text
plugins/nl-tax-agent-skills/.claude-plugin/plugin.json   # "version": "0.1.7"
plugins/nl-tax-agent-skills/.codex-plugin/plugin.json    # "version": "0.1.7"
```

Each release bumps **both** manifests **and** adds a [`CHANGELOG.md`](CHANGELOG.md) entry in
the same commit, so Claude Code, Cowork, and Codex installs pin to semver. The two
marketplace files (`.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`)
omit a version; for those GitHub-synced marketplaces Claude falls back to the git commit SHA,
so a pushed commit is still picked up by the Cowork marketplace **Update** button or by
`/plugin update` in Claude Code.

### Release checklist

- The release artifact contains only the plugin package, the repository README, the license,
  and the two marketplace manifests.
- Exclude `.git/`, `.claude/`, `.codex/`, `__MACOSX/`, `__pycache__/`, local workspaces,
  uploads, evidence files, compiled Python, and local `.agents/` state other than
  `.agents/plugins/marketplace.json`.
- Run the full validation gate above before release.
- Run first-party Claude plugin validation for the manifest, skill discovery, and
  frontmatter contracts. This is a package validation gate, not a Cowork UI result.
- In Cowork, install/update the plugin, open a fresh local or remote task, verify that
  bundled references load, and run one annual and one provisional natural-language smoke
  prompt. Record this separately; do not claim it from static or CLI validation alone.
- Verify invocation-policy metadata in the target Claude Code and Codex builds.

For the first future release tag, guard against a retroactive or duplicate tag before
letting Claude create the tag. The 0.1.7 preparation commit itself does not create one:

```bash
test "$(git tag --list 'nl-tax-agent-skills--v0.1.7')" = ""
claude plugin tag plugins/nl-tax-agent-skills
git tag --list 'nl-tax-agent-skills--v0.1.7'
```
