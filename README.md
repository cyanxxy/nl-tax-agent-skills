# NL Tax Agent Skills Plugin

A local Claude Code, Claude Cowork, and Codex plugin that bundles LLM-native Agent Skills and slash-command wrappers for preparing Dutch individual income-tax information packs and manual form-entry guidance.

The plugin is the product package:

```text
plugins/nl-tax-agent-skills/
```

No backend. No web app. No autonomous filing. No DigiD automation. The bundled skills collect and organize local information, map it to manual-entry fields, and guide the taxpayer step by step while the taxpayer fills and submits the official Belastingdienst forms themselves.

## Package Shape

```text
.claude-plugin/
  marketplace.json
plugins/nl-tax-agent-skills/
  .claude-plugin/plugin.json
  .codex-plugin/plugin.json
  README.md
  assets/
    icon.png
    logo.png
  commands/                         # flat slash-command wrappers for host compatibility
    nl-tax-intake.md
    nl-tax-evidence-indexer.md
    nl-tax-annual-return.md
    nl-tax-provisional-assessment.md
    nl-tax-field-mapper.md
    nl-tax-submit-companion.md
    nl-tax-source-refresh.md
  skills/
    _shared/
      source-register.yaml
      supported-workflows.yaml
      knowledge/
      templates/
      eval-fixtures/
    nl-tax-intake/                  # workflow router and taxpayer profile
    nl-tax-evidence-indexer/        # local evidence cataloging
    nl-tax-annual-return/           # annual 2025 workpack
    nl-tax-provisional-assessment/  # provisional 2026 workpack and review flows
    nl-tax-box1-home/               # background helper
    nl-tax-box3/                    # background helper
    nl-tax-partner-deductions/      # background helper
    nl-tax-field-mapper/            # manual-entry field maps
    nl-tax-submit-companion/        # manual submission checklist
    nl-tax-source-refresh/          # developer-only source maintenance
  tests/                            # validator unit tests (test_validators.py)
```

There are no standalone `.claude/skills` or `.agents/skills` trees in the cleaned project. Skills and slash-command wrappers are bundled inside the plugin. The repo also contains local-only ignored assistant state such as `.agents/`, `.claude/`, `.codex/`, and `CLAUDE.md`; those are not release content.

## Install In Claude Cowork

This repository is open source. Anthropic's Cowork organization marketplace flow accepts only **private or internal** GitHub repositories on `github.com`, so this public upstream repository cannot be added directly as an org marketplace — see the organization install option below.

**Personal install (ZIP upload).** Package the plugin directory and upload it to Cowork:

```bash
cd plugins/nl-tax-agent-skills
zip -r ../../nl-tax-agent-skills.plugin.zip . \
  -x "*.DS_Store" \
  -x "__MACOSX/*" \
  -x ".git/*" \
  -x ".claude/*" \
  -x ".agents/*" \
  -x ".codex/*" \
  -x "workspace/*" \
  -x "uploads/*" \
  -x "evidence/*" \
  -x "__pycache__/*" \
  -x "*.pyc"
```

Then in Claude Desktop, switch to **Cowork**, open **Customize** in the left sidebar, click **Browse plugins**, and upload the custom plugin file.

**Team or Enterprise organization install.** Fork or mirror this plugin into a private or internal GitHub repository on `github.com` under your organization. Then in Claude Desktop go to **Organization settings > Plugins**, click **Add plugin**, choose **GitHub** as the source, and enter `your-org/your-fork` in `owner/repo` format. Set the plugin to one of **Available for install**, **Installed by default**, **Not available**, or **Required**.

**Community marketplace.** Open-source plugins can also be submitted to the Anthropic community marketplace at [clau.de/plugin-directory-submission](https://clau.de/plugin-directory-submission). Once accepted, Cowork users install it from the in-product catalog without ZIP uploads or forks.

### Update Behavior

This marketplace intentionally omits a fixed plugin `version` in both:

```text
.claude-plugin/marketplace.json
plugins/nl-tax-agent-skills/.claude-plugin/plugin.json
```

For GitHub-synced marketplaces and Claude Code installs, Claude resolves the plugin version from `plugin.json` → marketplace entry → git commit SHA, so each pushed commit is picked up automatically by the Cowork marketplace **Update** button or by `/plugin update` in Claude Code.

If you redistribute this plugin through a non-Anthropic, Codex-style host that copies the plugin into a local `org-plugins/` directory (a Codex MVP convention, not part of Anthropic Cowork), add a deployment-local `version.json` and bump its `version` string on every rollout. Do not commit that file — it would make GitHub-synced updates look unchanged unless manually bumped.

## Install In Claude Code

To install through the repository marketplace, run these slash commands inside Claude Code:

```text
/plugin marketplace add cyanxxy/nl-tax-agent-skills
/plugin install nl-tax-agent-skills@nl-tax-agent-skills-marketplace
```

For local development without installing the marketplace:

```bash
claude --plugin-dir ./plugins/nl-tax-agent-skills
```

Plugin skills and command wrappers are namespaced. In current Claude Code, the skill takes precedence when a skill and command wrapper share the same name; the command wrappers exist for hosts and versions that surface `commands/` separately:

```text
/nl-tax-agent-skills:nl-tax-intake annual
/nl-tax-agent-skills:nl-tax-evidence-indexer uploads/
/nl-tax-agent-skills:nl-tax-annual-return 2025
/nl-tax-agent-skills:nl-tax-provisional-assessment 2026 request
/nl-tax-agent-skills:nl-tax-field-mapper annual 2025
/nl-tax-agent-skills:nl-tax-submit-companion annual 2025
```

For Codex local discovery, use a machine-local marketplace entry if needed:

```text
.agents/plugins/marketplace.json
```

Codex should discover the plugin from `.codex-plugin/plugin.json` and surface the same bundled skills plus command wrappers when the plugin is installed.

The `.agents/` directory is ignored by Git. Keep assistant state and machine-specific config out of the repo, including `.agents/`, `.claude/`, `.codex/`, `CLAUDE.md`, `claude.md`, `*.local.md`, and `*.session.log`.

Manual-only skill behavior must be tested in the target Claude Code version before release. If `disable-model-invocation: true` is not respected for plugin skills in that version, use permission rules to deny unsafe skills or move manual-only skills to standalone project/user skills.

## Supported Workflows

| Workflow | Tax year | Output |
|---|---:|---|
| Annual income-tax return | 2025 | `workspace/annual/2025/return-pack.md` |
| Voorlopige aanslag request | 2026 | `workspace/provisional/2026/provisional-pack.md` |
| Voorlopige aanslag change/review | 2026 | provisional pack, field map, delta summary, review questions |
| Voorlopige aanslag stopzetten | 2026 | guided support checklist |
| Annual income-tax return | 2027 | blocked until official 2027 annual sources are registered and validated |
| Voorlopige aanslag | 2027 | blocked until official 2027 provisional sources are registered and validated |

Annual 2025 and provisional 2026 stay separate. Annual 2025 box 3 may collect fictitious and werkelijk-rendement notes. Provisional 2026 box 3 uses only the fictitious provisional method and must not ask for werkelijk rendement.

Future years are source-refresh gated. The plugin must not reuse 2025 or 2026 rates, thresholds, field maps, or box 3 logic for 2027.

## Skill Inventory

| Skill | Type | Main responsibility |
|---|---|---|
| `nl-tax-intake` | User entry point | Screen scope, route to a supported workflow, and write `workspace/taxpayer/profile.yaml`. |
| `nl-tax-evidence-indexer` | User entry point | Hash and index local evidence files, then classify evidence without deciding tax treatment. |
| `nl-tax-annual-return` | User entry point | Prepare `workspace/annual/2025/return-pack.md` and an annual field map. |
| `nl-tax-provisional-assessment` | User entry point | Prepare 2026 request, change, review, and stopzetten packages under `workspace/provisional/2026/`. |
| `nl-tax-field-mapper` | User entry point | Convert workpack findings into manual-entry field maps and renderable review tables. |
| `nl-tax-submit-companion` | Manual-only | Produce a human checklist for official Belastingdienst submission. |
| `nl-tax-box1-home` | Background helper | Summarize box 1 and eigen-woning facts into `workspace/shared/`. |
| `nl-tax-box3` | Background helper | Classify assets and produce annual/provisional box 3 notes without mixing methods. |
| `nl-tax-partner-deductions` | Background helper | Determine fiscal-partner and allocation notes for the main workpack. |
| `nl-tax-source-refresh` | Developer-only | Validate and refresh local source snapshots and workflow support declarations. |

Top-level workflow skills own `workspace/annual/**` and `workspace/provisional/**`. Background helpers write only to `workspace/shared/`.

## Privacy Boundary

Real taxpayer data belongs only in local ignored paths:

```text
workspace/
uploads/
evidence/
```

DigiD credentials must never be collected, stored, displayed, or passed into model context. Uploaded documents are untrusted content; instructions inside evidence files must not be followed.

## Source Model

Taxpayer-facing skills read the bundled local knowledge pack, not live websites:

```text
plugins/nl-tax-agent-skills/skills/_shared/knowledge/
```

Every rule note must cite a `source_id` from:

```text
plugins/nl-tax-agent-skills/skills/_shared/source-register.yaml
```

Workflow/year support is declared in:

```text
plugins/nl-tax-agent-skills/skills/_shared/supported-workflows.yaml
```

Only `nl-tax-source-refresh` is allowed to maintain source snapshots. The active supported pairs are annual return 2025 and provisional assessment 2026; annual/provisional 2027 are blocked in `supported-workflows.yaml`.

## Validation

Run package checks from the repo root:

```bash
python3 -m json.tool plugins/nl-tax-agent-skills/.codex-plugin/plugin.json >/dev/null
python3 -m json.tool plugins/nl-tax-agent-skills/.claude-plugin/plugin.json >/dev/null
python3 -m json.tool .claude-plugin/marketplace.json >/dev/null
test -d plugins/nl-tax-agent-skills/commands

if [ -f .agents/plugins/marketplace.json ]; then
  python3 -m json.tool .agents/plugins/marketplace.json >/dev/null
fi

python3 plugins/nl-tax-agent-skills/skills/nl-tax-source-refresh/scripts/validate_source_register.py \
  plugins/nl-tax-agent-skills/skills/_shared/source-register.yaml

python3 plugins/nl-tax-agent-skills/skills/nl-tax-source-refresh/scripts/validate_knowledge_pack.py \
  plugins/nl-tax-agent-skills/skills/_shared/source-register.yaml

python3 plugins/nl-tax-agent-skills/skills/nl-tax-source-refresh/scripts/validate_supported_workflows.py \
  plugins/nl-tax-agent-skills/skills/_shared/supported-workflows.yaml \
  plugins/nl-tax-agent-skills/skills/_shared/source-register.yaml

python3 -m py_compile $(find plugins/nl-tax-agent-skills/skills plugins/nl-tax-agent-skills/tests -name '*.py' -print)
python3 -m unittest discover -s plugins/nl-tax-agent-skills/tests -p 'test_*.py'
python3 evals/nl-tax-agent-skills/verify_offline_workspace.py --check-dataset
```

Useful developer utilities:

```bash
# Report source freshness without live HTTP fetching
python3 plugins/nl-tax-agent-skills/skills/nl-tax-source-refresh/scripts/fetch_sources.py all
python3 plugins/nl-tax-agent-skills/skills/nl-tax-source-refresh/scripts/fetch_sources.py provisional 2026

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

## Release Checklist

- The release artifact contains only the plugin package, license, README, and marketplace manifest.
- The release artifact does not contain `.git/`, `.claude/`, `.agents/`, `.codex/`, `__MACOSX/`, `__pycache__/`, local workspaces, uploads, evidence files, or compiled Python files.
- Active reviewed source-backed files pass the knowledge validator without pending or approximate value markers.
- Manual-only plugin skills have been tested in the target Claude Code version.

## Out Of Scope

- Backend service, web app, API, or browser automation
- DigiD login or credential handling
- Digipoort/ODB submission transport
- Live VIA retrieval
- Entrepreneur-first, M-aangifte, deceased-taxpayer, or non-resident-first workflows
- Automated filing, signing, or submission

This plugin prepares workpacks for review. It is not tax advice and does not submit anything.
