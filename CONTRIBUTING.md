# Contributing

This is the maintainer/contributor reference for **NL Tax Agent Skills**. For what the
plugin does, how to install it, and how to use it, see the [README](README.md).

The product is an agent-led plugin under `plugins/nl-tax-agent-skills/` — no
backend, web app, or filing automation. Reasoning lives in `SKILL.md` playbooks;
one Claude-only specialist reviewer provides bounded cross-checks without
owning the taxpayer conversation or canonical workflow state.
Python is optional for taxpayer workflows. The installed mechanical helpers
cover evidence inventory/hash, field-map checks, and source-pinned arithmetic;
developer consistency and source-maintenance tools stay repository-only. None
ask questions, select a workflow, classify an ambiguous tax fact, or decide
readiness. When extending behavior, prefer agent guidance in a `SKILL.md` over
adding script-owned workflow logic.

---

## Repository layout

The plugin is the product package — `plugins/nl-tax-agent-skills/`. Repository-level
tests, evaluations, submission tooling, marketplace manifests, and project docs stay
outside that distributable directory.

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
  agents/
    nl-tax-specialist-reviewer.md   # Claude Cowork specialist reviewer
  skills/
    _shared/
      source-register.yaml          # every cited source_id with metadata
      knowledge/                    # bundled source-cited rule notes
      templates/
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
tests/
  nl_tax_agent_skills/              # repository-only unit and regression tests
evals/nl-tax-agent-skills/fixtures/ # repository-only structural scenarios
tools/nl_tax_agent_skills/
  source_maintenance/               # validators, metadata, workflow gate, planner
```

There are no standalone `.claude/skills` or `.agents/skills` trees — portable
skills are bundled inside the plugin and are the workflow discovery surface.
The plugin-level `agents/` directory is a Claude component, not local assistant
state; it contains only a specialist reviewer and is deliberately excluded from
the OpenAI submission bundle. The only tracked root `.agents/` file is
`.agents/plugins/marketplace.json`; local assistant state under `.agents/`, `.claude/`,
`.codex/`, plus `CLAUDE.md`, `claude.md`, `*.local.md`, and `*.session.log`, is git-ignored
and is not plugin package content.

### Plugin manifests

`.codex-plugin/plugin.json` exposes interface metadata for hosts that surface a catalog:

```json
{
  "name": "nl-tax-agent-skills",
  "version": "0.1.12",
  "skills": "./skills",
  "interface": {
    "displayName": "NL Tax Agent Skills",
    "category": "Productivity",
    "capabilities": ["Agent Skills", "Reviewable Workpacks", "Source-Backed Guidance"],
    "brandColor": "#1F6FEB"
  }
}
```

`.claude-plugin/plugin.json` is the Anthropic schema-conformant manifest. Claude
auto-discovers the plugin-root `agents/` directory; no duplicate manifest key is
needed. Codex plugin components do not include custom agents;
Codex custom-agent TOML belongs in user or project `.codex/agents/`, so the
portable skills request a built-in specialist subagent instead. Both nested
manifests are versioned; both root marketplaces remain unversioned.

### Reviewer-agent coordination

The owning conversational skill remains the only writer, question asker,
router, and readiness authority. Its persisted status files are a resumability
ledger, not an execution engine: they record what the agent has established but
do not choose the next question or tax treatment. The packaged Claude reviewer
receives an exact workflow/year and bounded review question, then returns
findings to the owner. It can use available host tools for official-source
checks and optional mechanical validators, while the owner retains the
conversation, canonical state, and readiness decision. Never build a parallel
Python workflow engine.

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

The authenticated-tax-portal boundary does not depend on those host controls.
Even if Cowork or another host exposes Chrome, browser control, computer use,
screen interaction, or connectors, a tax skill must never open or operate Mijn
Belastingdienst, log in, enter or change values, click controls, sign, send,
submit, retrieve private portal data, or handle credentials/sessions. Public,
read-only official-source research remains allowed. Generated portal guidance
must use an explicit human subject such as `Taxpayer:`.

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

Non-user-invocable background helpers and skills explicitly carrying
`disable-model-invocation: true` must ship an `agents/openai.yaml` with
`policy.allow_implicit_invocation: false`. Codex does not honor
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
When one request covers annual 2025 and provisional 2026, intake records both
but activates annual only. A complete validated annual map atomically hands
ownership to the selected provisional subflow; drafts and failed validation do
not hand off. `sources_loaded_by_workflow` keeps independent annual and
provisional source ledgers, while top-level `sources_loaded` mirrors only the
currently active workflow for backward compatibility.

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

Runtime `source_type` values are `law | official_guidance | official_rates |
official_doctrine | official_algorithm_register`. Platform, future-compatibility,
and authoring-method research lives under `docs/maintainers/source-notes/`
rather than in the taxpayer source register.

To add a rate or rule: put it in the right `knowledge/years/<year>/<scope>/*.md`, register
the source (with `mandatory_for` listing every skill that needs it), then run the validators.
After editing a reviewed knowledge `.md`, run `build_snapshots.py` to recompute its
`reviewed_note_hash_sha256` in the mirrored repository-only metadata under
`tools/nl_tax_agent_skills/source_maintenance/metadata/`. The builder marks a
new or changed note `review_status: needs_review`; only a human who compared the local note
with the cited official source may change that status to `reviewed`.

The reviewed provisional request/change/stopzetten snapshots are preserved
byte-for-byte. After a human reattests any of those notes, rebuild their
human-subject runtime projections with `build_runtime_projections.py`. The
projection builder inserts only the reversible `**Taxpayer:**` subject, records
the complete source-note hash and source ids, and never changes review status.

> **Freshness gate.** `validate_knowledge_pack.py` parses prose `freshness_policy` cadences
> ("check monthly" → 31 days, "quarter" → 92, "prinsjesdag" → 120, "annual" → 365) and a
> **stale mandatory source fails the gate**. If it goes red on dates, re-verify the source
> and bump its `last_checked`.

Only the repository source-maintenance tools may maintain source snapshots. Active supported pairs are
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

python3 submission/openai/build_bundle.py
python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py \
  dist/openai/nl-tax-agent-skills

python3 tools/nl_tax_agent_skills/source_maintenance/scripts/validate_source_register.py \
  plugins/nl-tax-agent-skills/skills/_shared/source-register.yaml

python3 tools/nl_tax_agent_skills/source_maintenance/scripts/validate_knowledge_pack.py \
  plugins/nl-tax-agent-skills/skills/_shared/source-register.yaml

python3 tools/nl_tax_agent_skills/source_maintenance/scripts/validate_supported_workflows.py \
  tools/nl_tax_agent_skills/source_maintenance/supported-workflows.yaml \
  plugins/nl-tax-agent-skills/skills/_shared/source-register.yaml

python3 tools/nl_tax_agent_skills/source_maintenance/scripts/validate_invocation_policy.py \
  plugins/nl-tax-agent-skills/skills

python3 tools/nl_tax_agent_skills/source_maintenance/scripts/build_runtime_projections.py

python3 -m compileall -q plugins/nl-tax-agent-skills/skills tools/nl_tax_agent_skills tests/nl_tax_agent_skills
python3 -m unittest discover -s tests/nl_tax_agent_skills -p 'test_*.py'
python3 evals/nl-tax-agent-skills/verify_offline_workspace.py --check-dataset
```

For an OpenAI Plugin Directory release, also review
`submission/openai/README.md`, run its fresh-task smoke-test matrix, and submit
the exact five positive and three negative reviewer cases in
`submission/openai/test-cases.yaml`. Repository validation cannot replace
publisher verification, Apps Management permission, genuine product
screenshots, or a Work web/desktop smoke test.

| Validator | Purpose |
|---|---|
| OpenAI plugin validator | Codex manifest, skill metadata, asset containment, invocation metadata, and ingestion shape |
| `validate_source_register.py` | Every `source_id` has the required fields, snapshot path resolves, `last_checked` parses as an ISO date, URLs are HTTPS and on the allowlist |
| `validate_knowledge_pack.py` | Each knowledge note cites only registered `source_id`s; snapshots match referenced paths and hashes; stale mandatory sources fail |
| `validate_supported_workflows.py` | Active workflow/year pairs have all their `required_source_ids` registered and reviewed |
| `validate_invocation_policy.py` | Every non-user-invocable skill ships an `agents/openai.yaml` with `policy.allow_implicit_invocation: false` |
| `tests/nl_tax_agent_skills/` (unittest) | Repository-only unit coverage of validator/helper logic plus regression and golden tests; it is excluded from the installed plugin |
| `verify_offline_workspace.py` | Structural contract library is internally consistent; it is not the live conversational grader |

### Developer utilities

```bash
# Report source freshness without live HTTP fetching
python3 tools/nl_tax_agent_skills/source_maintenance/scripts/plan_source_refresh.py all
python3 tools/nl_tax_agent_skills/source_maintenance/scripts/plan_source_refresh.py provisional 2026

# Recompute snapshot metadata after source updates
python3 tools/nl_tax_agent_skills/source_maintenance/scripts/build_snapshots.py \
  plugins/nl-tax-agent-skills/skills/_shared/source-register.yaml

# Rebuild reversible human-only runtime projections without reattesting sources
python3 tools/nl_tax_agent_skills/source_maintenance/scripts/build_runtime_projections.py

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

Both plugin manifests pin a fixed version (currently `0.1.12`):

```text
plugins/nl-tax-agent-skills/.claude-plugin/plugin.json   # "version": "0.1.12"
plugins/nl-tax-agent-skills/.codex-plugin/plugin.json    # "version": "0.1.12"
```

Each release bumps **both** manifests **and** adds a [`CHANGELOG.md`](CHANGELOG.md) entry in
the same commit, so Claude Code, Cowork, and Codex installs pin to semver. The two
marketplace files (`.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`)
omit a version; for those GitHub-synced marketplaces Claude falls back to the git commit SHA,
so a pushed commit is still picked up by the Cowork marketplace **Update** button or by
`/plugin update` in Claude Code.

### Release checklist

- The release artifact contains only the plugin package, its README and
  license, and the Claude/Codex plugin manifests.
- Exclude `.git/`, `.claude/`, `.codex/`, `.plugin-eval/`, `__MACOSX/`,
  `__pycache__/`, local workspaces, uploads, evidence files, compiled Python,
  and local `.agents/` state other than `.agents/plugins/marketplace.json`.
- Run the full validation gate above before release.
- Run first-party Claude plugin validation for the manifest, skill discovery, and
  frontmatter contracts. This is a package validation gate, not a Cowork UI result.
- In Cowork, install/update the plugin, open a fresh local or remote task, verify that
  bundled references load, and run one annual and one provisional natural-language smoke
  prompt. Record this separately; do not claim it from static or CLI validation alone.
- Verify invocation-policy metadata in the target Claude Code and Codex builds.

Guard against a retroactive or duplicate tag before letting Claude create the
plugin release tag:

```bash
test "$(git tag --list 'nl-tax-agent-skills--v0.1.12')" = ""
claude plugin tag plugins/nl-tax-agent-skills
git tag --list 'nl-tax-agent-skills--v0.1.12'
```
