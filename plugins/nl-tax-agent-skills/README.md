# NL Tax Agent Skills Plugin

Plugin package for preparing Dutch individual income-tax information packs and manual form-entry guidance through LLM-native Agent Skills and Claude Code slash-command wrappers.

This directory is the product package. The skills are bundled inside the plugin under `skills/`; flat command wrappers live under `commands/` for Claude Code slash-command compatibility.

The repository root contains marketplace manifests that point at this nested plugin package:

```text
.claude-plugin/marketplace.json       # Claude marketplace
.agents/plugins/marketplace.json      # repo-scoped Codex marketplace
```

The package is licensed under Apache-2.0; see the repository root `LICENSE`.

## Package Contents

```text
nl-tax-agent-skills/
  .claude-plugin/plugin.json    # Claude Code plugin manifest
  .codex-plugin/plugin.json     # Codex plugin manifest
  assets/
    icon.png
    logo.png
  commands/                     # Claude Code slash-command wrappers
    nl-tax-intake.md
    nl-tax-evidence-indexer.md
    nl-tax-annual-return.md
    nl-tax-provisional-assessment.md
    nl-tax-field-mapper.md
    nl-tax-submit-companion.md
    nl-tax-source-refresh.md
  skills/                       # Bundled Agent Skills
    _shared/                    # Source pack, workflow gate, templates, fixtures
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
    nl-tax-box2/                    # background helper
    nl-tax-box3/                    # background helper
    nl-tax-partner-deductions/      # background helper
    nl-tax-field-mapper/            # manual-entry field maps
    nl-tax-submit-companion/        # manual submission checklist
    nl-tax-source-refresh/          # developer-only source maintenance
  tests/                        # unit tests (validators, box1/box2 helpers, eval verifier, field-map policy)
```

The bundled skills cover:

- annual income-tax return workpack for tax year 2025;
- voorlopige aanslag 2026 request, change, review, and stopzetten guidance;
- source-refresh gated 2027 annual/provisional workflows, blocked until official 2027 sources are registered and validated;
- evidence indexing with untrusted-content handling;
- box 1, box 2, box 3, partner/deduction, field-map, source-refresh, and manual submission companion workflows.

The plugin intentionally does not include a backend service, web app, browser automation, DigiD collection, signing, filing, Digipoort transport, or autonomous submission. It helps the taxpayer collect information, review it, and follow step-by-step guidance while filling the official forms manually.

The plugin must not prepare 2027 annual or provisional workpacks from 2025/2026 values. Future tax years become active only after exact official source snapshots are added and all validators pass.

## Skill Inventory

| Skill | Type | Main responsibility |
|---|---|---|
| `nl-tax-intake` | User entry point | Screen scope, select a supported workflow, and create `workspace/taxpayer/profile.yaml`. |
| `nl-tax-evidence-indexer` | User entry point | Index local evidence files, compute hashes, and produce evidence review questions. |
| `nl-tax-annual-return` | User entry point | Prepare the annual 2025 return workpack and field map. |
| `nl-tax-provisional-assessment` | User entry point | Prepare 2026 request, change, review, or stopzetten packages. |
| `nl-tax-field-mapper` | User entry point | Convert workpack findings into manual-entry field maps. |
| `nl-tax-submit-companion` | Manual-only | Create a manual checklist for official submission. |
| `nl-tax-box1-home` | Background helper | Summarize box 1 and own-home notes into `workspace/shared/`. |
| `nl-tax-box2` | Background helper | Prepare Box 2 substantial-interest notes into `workspace/shared/`. |
| `nl-tax-box3` | Background helper | Classify assets and produce source-backed box 3 notes. |
| `nl-tax-partner-deductions` | Background helper | Produce fiscal-partner and allocation notes. |
| `nl-tax-source-refresh` | Developer-only | Validate source registers, knowledge snapshots, and supported workflows. |

Only the annual and provisional workflow skills write main workpacks. Helper skills write shared notes only.

## Claude Code

Install through the repository marketplace at `https://github.com/cyanxxy/nl-tax-agent-skills` by running these slash commands inside Claude Code:

```text
/plugin marketplace add cyanxxy/nl-tax-agent-skills
/plugin install nl-tax-agent-skills@nl-tax-agent-skills-marketplace
```

Load the plugin directly during local development:

```bash
claude --plugin-dir ./plugins/nl-tax-agent-skills
```

Plugin skills and command wrappers are namespaced. In current Claude Code, plugin skills are directly slash-invokable; if a command wrapper and skill share the same name, the skill takes precedence. Examples:

```text
/nl-tax-agent-skills:nl-tax-intake annual
/nl-tax-agent-skills:nl-tax-provisional-assessment 2026 change
/nl-tax-agent-skills:nl-tax-field-mapper annual 2025
```

## Claude Cowork

This repository is open source and hosted on `github.com`. Cowork supports two install paths, with different repo-visibility rules.

**Personal install (public GitHub repo).** In Claude Desktop, switch to the **Cowork** tab, click **Customize** in the left sidebar, then click **Browse plugins**. Select the **Personal** tab, click **+**, choose **Add marketplace from GitHub**, and enter:

```text
https://github.com/cyanxxy/nl-tax-agent-skills
```

Cowork syncs the marketplace and surfaces `nl-tax-agent-skills`. Click **Install** on the plugin entry. Public GitHub repos are accepted for personal marketplaces, so no fork or ZIP upload is needed.

**Team or Enterprise organization install.** Cowork's organization marketplace flow accepts only **private or internal** GitHub repositories on `github.com` — public repos are blocked at the org level. Fork or mirror this plugin into a private or internal GitHub repository on `github.com` under your organization. Then in Claude Desktop go to **Organization settings > Plugins**, click **Add plugin**, choose **GitHub** as the source, and enter `your-org/your-fork` in `owner/repo` format. Set the plugin to one of **Available for install**, **Installed by default**, **Not available**, or **Required**.

**Community marketplace.** Open-source plugins can be submitted to the Anthropic community marketplace at [clau.de/plugin-directory-submission](https://clau.de/plugin-directory-submission). Once accepted, Cowork users install it from the in-product catalog without adding a marketplace or forking.

**Optional ZIP fallback.** If the GitHub-marketplace path is unavailable in a given Cowork build, package the plugin directory and upload it through the same **Browse plugins** modal:

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

## Codex

For Codex discovery from the repository root, use the tracked repo-scoped marketplace at:

```text
.agents/plugins/marketplace.json
```

That marketplace points to the nested plugin package at `plugins/nl-tax-agent-skills/`. The plugin package itself keeps the required Codex manifest at:

```text
plugins/nl-tax-agent-skills/.codex-plugin/plugin.json
```

Only `.agents/plugins/marketplace.json` is tracked under `.agents/`; other assistant state in `.agents/` remains ignored.

Codex users invoke the bundled skills after discovery. The plugin also includes `commands/`, but those files are Claude Code slash-command wrappers and should not be treated as the Codex command surface unless a target Codex host explicitly documents support for command files.

## Update Behavior

Both plugin manifests pin a fixed `version` (currently `0.1.1`):

```text
.claude-plugin/plugin.json   # "version": "0.1.1"
.codex-plugin/plugin.json    # "version": "0.1.1"
```

Bump **both** for every release so Claude Code, Cowork, and Codex installs pin to semver. Only the marketplace files (`.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`) omit a version; for those GitHub-synced marketplaces Claude can fall back to the git commit SHA, so a pushed commit is still picked up by the Cowork marketplace **Update** button or by `/plugin update` in Claude Code.

## Release Checks

- The release artifact must contain only this plugin package, the repository README, the license, the Claude marketplace, and the repo-scoped Codex marketplace.
- Do not include `.git/`, `.claude/`, `.codex/`, `__MACOSX/`, `__pycache__/`, local workspaces, uploads, evidence files, compiled Python files, or local `.agents/` state other than `.agents/plugins/marketplace.json`.
- Run source-register, knowledge-pack, and supported-workflows validation before release.
- Test manual-only skills in the target Claude Code version before release. If `disable-model-invocation: true` is not respected for plugin skills, use permission rules to deny unsafe skills or move manual-only skills to standalone project/user skills.

Run these checks from the repository root:

```bash
python3 -m json.tool plugins/nl-tax-agent-skills/.codex-plugin/plugin.json >/dev/null
python3 -m json.tool plugins/nl-tax-agent-skills/.claude-plugin/plugin.json >/dev/null
python3 -m json.tool .claude-plugin/marketplace.json >/dev/null
python3 -m json.tool .agents/plugins/marketplace.json >/dev/null
test -d plugins/nl-tax-agent-skills/commands

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

## Privacy Boundary

Real taxpayer data belongs only in ignored local workspace paths such as `workspace/`, `uploads/`, and `evidence/`. Do not add real taxpayer files, DigiD credentials, BSNs, IBANs, screenshots, PDFs, or spreadsheets to this plugin package.

## Source Model

Taxpayer-facing skills must use the bundled local source pack under:

```text
plugins/nl-tax-agent-skills/skills/_shared/knowledge/
```

Only the developer-only `nl-tax-source-refresh` skill may refresh official source snapshots.

Workflow/year support is controlled by:

```text
plugins/nl-tax-agent-skills/skills/_shared/supported-workflows.yaml
```

The source register is the canonical list of official sources:

```text
plugins/nl-tax-agent-skills/skills/_shared/source-register.yaml
```
