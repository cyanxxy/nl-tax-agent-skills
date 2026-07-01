# NL Tax Agent Skills — Plugin Package

This directory is the product package for **NL Tax Agent Skills**: a skills-only Agent
Skills plugin that prepares Dutch individual income-tax workpacks and manual Mijn
Belastingdienst entry guidance (annual 2025 and voorlopige aanslag 2026).

> **Not tax advice.** This plugin prepares local workpacks and manual-entry
> guidance only. It never logs in, signs, or submits anything, and its output is
> not official advice or a final calculation — the taxpayer reviews everything
> and enters it manually in Mijn Belastingdienst.

> **Install, usage, workflows, architecture, and privacy live in the repository
> docs** at <https://github.com/cyanxxy/nl-tax-agent-skills> (`README.md`,
> `CONTRIBUTING.md`, `PRIVACY.md`). This file only orients you inside the
> package. Licensed under Apache-2.0 — see the bundled [`LICENSE`](LICENSE)
> file (also declared in both plugin manifests).

In the development repository, the repository root additionally holds the
marketplace manifests that point at this package: `.claude-plugin/marketplace.json`
(Claude) and `.agents/plugins/marketplace.json` (repo-scoped Codex). Neither
ships inside this package.

## Package contents

```text
nl-tax-agent-skills/
  .claude-plugin/plugin.json    # Claude Code plugin manifest
  .codex-plugin/plugin.json     # Codex plugin manifest
  LICENSE                       # Apache-2.0 license text
  assets/                       # icon.png, logo.png
  commands/                     # Claude Code slash-command wrappers (one per user skill)
  skills/
    _shared/                    # source-register.yaml, supported-workflows.yaml, knowledge/, templates/, eval-fixtures/
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
  tests/                        # unit tests (validators, box helpers, eval verifier, field-map policy)
```

## Skill inventory

| Skill | Type | Main responsibility |
|---|---|---|
| `nl-tax-intake` | user entry | Screen scope, select a supported workflow, create `workspace/taxpayer/profile.yaml` |
| `nl-tax-evidence-indexer` | user entry | Index local evidence files, compute hashes, produce review questions |
| `nl-tax-annual-return` | user entry | Prepare the annual 2025 return workpack and field map |
| `nl-tax-provisional-assessment` | user entry | Prepare 2026 request, change, review, or stopzetten packages |
| `nl-tax-field-mapper` | user entry | Convert workpack findings into manual-entry field maps |
| `nl-tax-submit-companion` | manual-only | Create a manual checklist for official submission |
| `nl-tax-box1-home` | background | Summarize box 1 and own-home notes into `workspace/shared/` |
| `nl-tax-box2` | background | Prepare Box 2 substantial-interest notes into `workspace/shared/` |
| `nl-tax-box3` | background | Classify assets and produce source-backed box 3 notes (no method mixing) |
| `nl-tax-partner-deductions` | background | Produce fiscal-partner and allocation notes |
| `nl-tax-source-refresh` | developer | Validate source registers, knowledge snapshots, and supported workflows |

Only the annual and provisional workflow skills write main workpacks; helper skills write
shared notes only.

## Scope

The plugin intentionally has **no** backend service, web app, browser automation,
signing, filing, Digipoort transport, or autonomous submission. It helps the
taxpayer collect information, review it, and follow step-by-step guidance while filling the
official forms manually.

It must not prepare 2027 annual or provisional workpacks from 2025/2026 values — future tax
years become active only after exact official source snapshots are added and all validators
pass.
