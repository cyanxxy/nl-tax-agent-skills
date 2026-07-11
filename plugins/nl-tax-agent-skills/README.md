# NL Tax Agent Skills — Plugin Package

This directory is the product package for **NL Tax Agent Skills**: a Cowork-first,
skills-only Agent Skills plugin that prepares Dutch individual income-tax workpacks and
manual Mijn Belastingdienst entry guidance (annual 2025 and voorlopige aanslag 2026).

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

## Cowork quickstart

After installing the plugin, attach or select the relevant documents and ask:

```text
Help me prepare my 2025 Dutch income-tax workpack. I have my year statement and mortgage summary.
```

The LLM agent runs intake, asks for missing facts, loads only the needed rule notes,
and drafts the review artifacts. For a provisional workflow, ask naturally to request,
change, review, or stopzetten a 2026 voorlopige aanslag. A direct advanced invocation is
`/nl-tax-agent-skills:nl-tax-provisional-assessment 2026 request` (replace `request` with
the desired subflow).

Cowork tasks may use local or remote execution environments, so file availability and
shell tooling depend on the active session. Python is optional; the agent follows the
manual check path whenever a helper cannot run.

## Package contents

```text
nl-tax-agent-skills/
  .claude-plugin/plugin.json    # Claude Code plugin manifest
  .codex-plugin/plugin.json     # Codex plugin manifest
  LICENSE                       # Apache-2.0 license text
  assets/                       # icon.png
  skills/
    _shared/                    # source-register.yaml, supported-workflows.yaml, knowledge/, templates/, eval-fixtures/
    nl-tax-intake/                  # workflow router and taxpayer profile
    nl-tax-evidence-indexer/        # local evidence cataloging
    nl-tax-annual-return/           # annual 2025 workpack
    nl-tax-provisional-assessment/  # provisional 2026 workpack and review flows
    nl-tax-box1-home/               # background helper
    nl-tax-box2/                    # background helper
    nl-tax-box3/                    # background helper
    nl-tax-winst/                   # background helper (winst uit onderneming)
    nl-tax-partner-deductions/      # background helper
    nl-tax-field-mapper/            # manual-entry field maps
    nl-tax-submit-companion/        # manual submission checklist
    nl-tax-source-refresh/          # developer-only source maintenance
  tests/                        # unit tests (validators, box helpers, eval verifier, field-map policy)
```

The test suite runs standalone from this package (`python3 -m unittest discover -s tests -p 'test_*.py'`); repo-only checks skip themselves. Scenario eval fixtures ship in `skills/_shared/eval-fixtures/`; the offline eval harness that runs benchmark cases against them lives at repo level under `evals/nl-tax-agent-skills/` and is deliberately not shipped in this package.

### Optional script prerequisites

Python is optional at runtime. Do not ask the taxpayer to install Python: the
agent applies the same explicit checks from the bundled knowledge and skill
instructions. The bundled scripts are best-effort mechanical accelerators, not
the primary mechanism. They form four conceptual components: evidence
inventory/hash, field-map checks, source-pinned arithmetic checks, and
developer consistency/source maintenance. When a maintainer chooses to run
them, they need Python 3.10+ and — for the validators and register tooling —
PyYAML (`python3 -m pip install pyyaml`). On hosts without Python or PyYAML,
the agent-driven manual checks in each `SKILL.md` apply.

## Skill inventory

| Skill | Type | Main responsibility |
|---|---|---|
| `nl-tax-intake` | user entry | Screen scope, select a supported workflow, create `workspace/taxpayer/profile.yaml` |
| `nl-tax-evidence-indexer` | user entry | Index local evidence files, compute hashes, produce review questions |
| `nl-tax-annual-return` | user entry | Prepare the annual 2025 workpack and invoke the mapper for its field map (incl. preparation-only winst) |
| `nl-tax-provisional-assessment` | user entry | Prepare 2026 request, change, review, or stopzetten packages |
| `nl-tax-field-mapper` | user entry | Convert workpack findings into manual-entry field maps |
| `nl-tax-submit-companion` | manual-only | Create a manual checklist for official submission |
| `nl-tax-box1-home` | background | Return sourced Box 1 and own-home facts/questions to the owning workflow |
| `nl-tax-box2` | background | Return standard Box 2 facts/questions to the owning workflow |
| `nl-tax-box3` | background | Return trusted-row, method-specific Box 3 facts without method mixing |
| `nl-tax-winst` | background | Return annual-2025 preparation facts or one sourced provisional-2026 expected-profit forecast |
| `nl-tax-partner-deductions` | background | Return fiscal-partner, deduction, and allocation facts/questions |
| `nl-tax-source-refresh` | developer | Validate source registers, knowledge snapshots, and supported workflows |

Only the annual and provisional workflow skills write main workpacks. Intake
creates taxpayer/session state, the field mapper alone writes canonical field
maps, and background helpers write no artifacts.

The annual workflow is phase-based (intake gate, evidence review, Box 1/own home,
optional winst, Box 2, Box 3, partner allocations, field mapping, and final review).
The provisional workflow has four separate subflows: request, change, review, and
stopzetten. `nl-tax-winst` supports straightforward annual-2025 preparation and
the single bounded provisional field `onderneming.geschatte_winst`; it is not a
provisional tax engine or final business-tax calculator.

The package passes manifest and discovery checks, including first-party Claude validation
when the CLI capability is installed. Those checks do not replace a human Cowork UI smoke
test after install/update in a fresh task.

## Scope

The plugin intentionally has **no** backend service, web app, browser automation,
signing, filing, Digipoort transport, or autonomous submission. It helps the
taxpayer collect information, review it, and follow step-by-step guidance while filling the
official forms manually.

It must not prepare 2027 annual or provisional workpacks from 2025/2026 values — future tax
years become active only after exact official source snapshots are added and all validators
pass.
