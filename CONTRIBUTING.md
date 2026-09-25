# Contributing

This is the maintainer/contributor reference for **NL Tax Agent Skills**. For what the
plugin does, how to install it, and how to use it, see the [README](README.md).

The product is an agent-led plugin under `plugins/nl-tax-agent-skills/` — no
backend, web app, or filing automation. Reasoning lives in `SKILL.md` playbooks;
one Claude-only specialist reviewer provides bounded cross-checks without
owning the taxpayer conversation or canonical workflow state.
Taxpayer workflows need no Python: the installed plugin ships no scripts and
pre-approves no shell commands. The mechanical graders for evidence inventory,
field maps, and source-pinned arithmetic live under `tools/nl_tax_agent_skills/`
with the developer consistency and source-maintenance tools. None ask questions, select a workflow, classify an ambiguous tax fact, or decide
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
    nl-tax-shared-resources/
      knowledge-index.md            # topic → note map for every reviewed note
      source-register.yaml          # every cited source_id with metadata
      knowledge/                    # bundled source-cited rule notes
      templates/
    nl-tax-intake/                  # workflow router and taxpayer profile
    nl-tax-knowledge/               # read-only rule lookup from the reviewed notes
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

`.codex-plugin/plugin.json` exposes interface metadata for hosts that surface a catalog.
Do not add a portable Agent Plugins `plugin.json` at the plugin root: the Claude
directory portal then reads no manifest, README, or skills from the folder and
greys out Cowork and the Claude apps. Codex still reads `.codex-plugin/plugin.json`.
`test_plugin_root_has_no_portable_manifest` enforces this:

```json
{
  "name": "nl-tax-agent-skills",
  "version": "0.3.2",
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
portable skills request a built-in specialist subagent instead. Both plugin
manifests are versioned; both root marketplaces remain unversioned.

### Reviewer-agent coordination

The owning conversational skill remains the only writer, question asker,
router, and readiness authority. Its persisted status files are a resumability
ledger, not an execution engine: they record what the agent has established but
do not choose the next question or tax treatment. The packaged Claude reviewer
receives an exact workflow/year and bounded review question, then returns
findings to the owner. It can use available host tools for official-source
checks, while the owner retains the
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
```

Skills ship Markdown and YAML only. Do not add a `scripts/` folder or any other
executable code to the plugin package; `test_no_runtime_code.py` enforces this.

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
  - Edit(./workspace/**)
---
```

Pre-approve file writes only as `Edit(./workspace/**)` and never pre-approve `Bash`:
the Claude directory scan holds unscoped write grants and broad shell grants for
human review. Do not list `Write` at all: Claude Code never consults a
`Write(path)` rule (it warns at startup), and `Edit` rules already cover every
built-in tool that creates or changes files. `allowed-tools` is a pre-approval convenience, not a sandbox: on Claude Code it suppresses
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
`reference/`, `templates/`, `../nl-tax-shared-resources/`, and sibling `../nl-tax-*/` files
relative to the skill directory with `Read`. Write every bundled path in a `SKILL.md` or
`reference/` file in that skill-relative form, and name each file a skill needs, including
helper `SKILL.md` paths. The runtime contract forbids package-wide `Glob`/`Grep`; the only
permitted search is a narrow term search inside `../nl-tax-shared-resources/knowledge/`. Every
arithmetic and structural check is an agent checklist documented in the skill.

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
  snapshot_path: "skills/nl-tax-shared-resources/knowledge/years/2025/box3/box3-calc.md"
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
the source (with `mandatory_for` listing every skill that needs it), add a row to
`nl-tax-shared-resources/knowledge-index.md` (topic, key terms that occur in the note, and
the skill-relative path), then run the validators and the unit suite.
`test_knowledge_base_access.py` fails when a note is missing from the index or an index
key term does not occur in its note. Keep note headers on the uniform `source_ids:` and
`tax_year:` keys.
Every edit to a reviewed knowledge `.md` changes its `reviewed_note_hash_sha256` in the
mirrored repository-only metadata under
`tools/nl_tax_agent_skills/source_maintenance/metadata/`. Pick the path by what changed:

- **Substantive edit** (any rule, amount, percentage, threshold, date, condition,
  example, or cited source changes): run `build_snapshots.py`. It recomputes the hash and
  marks the note `review_status: needs_review`; only a human who compared the local note
  with the cited official source may change that status back to `reviewed`.
- **Maintainer-only edit** (a folder or path rename, a header-key rename such as
  `source_id:` → `source_ids:`, or whitespace): no rule text changes, so the existing
  attestation still holds. Show that the diff contains nothing else, for example by
  applying the same rename to `git show HEAD:<old path>` and comparing the result
  byte-for-byte with the new file. Then update `reviewed_note_hash_sha256` and
  `reviewed_note_hash_recorded_at` for every `source_id` the note backs, keeping
  `review_status: reviewed`. Do not run `build_snapshots.py` for this: it would demote
  the note and fail the gate. If any line of rule text changed, use the substantive path.

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
Taxpayer workflows need no Python because every runtime check is an
agent checklist. Run the following commands from the repo root.
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
  plugins/nl-tax-agent-skills/skills/nl-tax-shared-resources/source-register.yaml

python3 tools/nl_tax_agent_skills/source_maintenance/scripts/validate_knowledge_pack.py \
  plugins/nl-tax-agent-skills/skills/nl-tax-shared-resources/source-register.yaml

python3 tools/nl_tax_agent_skills/source_maintenance/scripts/validate_supported_workflows.py \
  tools/nl_tax_agent_skills/source_maintenance/supported-workflows.yaml \
  plugins/nl-tax-agent-skills/skills/nl-tax-shared-resources/source-register.yaml

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
  plugins/nl-tax-agent-skills/skills/nl-tax-shared-resources/source-register.yaml

# Rebuild reversible human-only runtime projections without reattesting sources
python3 tools/nl_tax_agent_skills/source_maintenance/scripts/build_runtime_projections.py

# Evidence inventory (repository grader)
python3 tools/nl_tax_agent_skills/evidence_indexer/index_evidence.py uploads/

# Field-map grading (repository tooling; runtime uses the agent checklist)
python3 tools/nl_tax_agent_skills/field_mapper/validate_field_map.py \
  workspace/annual/2025/field-map.yaml
python3 tools/nl_tax_agent_skills/field_mapper/render_field_map.py \
  workspace/annual/2025/field-map.yaml
```

---

## Release process

Both plugin manifests pin a fixed version (currently `0.3.2`):

```text
plugins/nl-tax-agent-skills/.claude-plugin/plugin.json   # "version": "0.3.2"
plugins/nl-tax-agent-skills/.codex-plugin/plugin.json    # "version": "0.3.2"
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
- **Sibling-path check (Cowork, then claude.ai chat).** Skills read each other and the
  knowledge pack through sibling paths such as `../nl-tax-shared-resources/`. Claude's
  docs only describe files inside a skill's own folder, and claude.ai chat copies just
  that folder into its sandbox, so verify on each surface before a directory review:
  1. Ask "What is the Box 3 heffingsvrij vermogen for 2025?". Expect EUR 57,684 per
     person with the tax year and a `bd_` source, read from
     `../nl-tax-shared-resources/knowledge-index.md` and the matching note.
  2. Ask "Help me prepare my 2025 Dutch income-tax workpack." Expect intake to load
     `../nl-tax-shared-resources/runtime-contract.md` and ask its first screening
     question, not to report a missing resource.
  3. A pass answers from the bundled notes. A fail is the agent reporting an incomplete
     install (the runtime contract's required behavior) or answering from memory without
     a source ID. Record the surface, app version, and result in the release notes, and
     do not list a surface as supported until it passes.
- Verify invocation-policy metadata in the target Claude Code and Codex builds.

Guard against a retroactive or duplicate tag before letting Claude create the
plugin release tag:

```bash
test "$(git tag --list 'nl-tax-agent-skills--v0.3.2')" = ""
claude plugin tag plugins/nl-tax-agent-skills
git tag --list 'nl-tax-agent-skills--v0.3.2'
```

### Publish the GitHub release

Pushing an annotated `vX.Y.Z` tag publishes the GitHub release through
`.github/workflows/release.yml`. The workflow fails unless the tag matches the
version in both plugin manifests and `CHANGELOG.md` has a `## [X.Y.Z]`
section. It runs the unit suite, attaches
`nl-tax-agent-skills-X.Y.Z-cowork.zip` (the tracked plugin files) and
`nl-tax-agent-skills-X.Y.Z-openai.zip` (the OpenAI bundle), uses the changelog
section as the notes, and takes the title from the tag message:

```bash
git tag -a v0.3.2 -m "v0.3.2 — <short release title>"
git push origin v0.3.2
```

A version bump is not a release until this tag is pushed.
