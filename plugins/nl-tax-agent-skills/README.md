# NL Tax Agent Skills — Plugin Package

This directory is the product package for **NL Tax Agent Skills**: a
Cowork-first, cross-platform, agent-led plugin for Claude, ChatGPT Work, and
Codex that prepares Dutch individual income-tax workpacks and manual Mijn
Belastingdienst entry guidance (annual 2025 and voorlopige aanslag 2026). It
ships portable Agent Skills plus one optional Claude Cowork specialist reviewer;
Codex and ChatGPT Work can use their built-in subagents under
the same single-writer contract.

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

## Claude Cowork, ChatGPT Work, and Codex quickstart

After installing the plugin, attach or select the relevant documents and ask:

```text
Help me prepare my 2025 Dutch income-tax workpack. I have my year statement and mortgage summary.
```

The LLM agent runs intake, asks for missing facts, loads only the needed rule notes,
and drafts the review artifacts. For a provisional workflow, ask naturally to request,
change, review, or stopzetten a 2026 voorlopige aanslag. A direct advanced invocation is
`/nl-tax-agent-skills:nl-tax-provisional-assessment 2026 request` (replace `request` with
the desired subflow).

A user may request annual 2025 and one provisional 2026 subflow together in
natural language. The agent keeps annual as the sole active owner until its
complete workpack and field map validate, then continues into the recorded 2026
subflow without a new activation phrase. The two workflows keep independent
status, source, confirmation, and artifact ledgers.

For finite-choice intake questions, the skills prefer a native question control
or compact form when the host can return selections to the same conversation.
If it cannot, the agent asks the same short question batch in chat; the workflow
never depends on an interactive UI.
In Claude Cowork, the preferred path is Claude's native interactive inputs when
offered; a custom HTML visual is not used as the answer-submission mechanism.

Tasks may use local or cloud execution environments, so file availability and
shell tooling depend on the active surface. Work web/mobile uses uploaded or
project files; desktop tasks can also use a selected local folder. Python is
optional; the agent follows the manual check path whenever a helper cannot run.

## Package contents

```text
nl-tax-agent-skills/
  .claude-plugin/plugin.json    # Claude Code plugin manifest
  .codex-plugin/plugin.json     # Codex plugin manifest
  LICENSE                       # Apache-2.0 license text
  assets/                       # icon.png
  agents/
    nl-tax-specialist-reviewer.md # optional Claude Cowork section reviewer
  skills/
    _shared/                    # source-register.yaml, knowledge/, templates/
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
```

Unit tests, structural fixtures, source metadata, the workflow-support gate,
and source-maintenance tooling live outside this installed package under
repository-level `tests/`, `evals/`, and `tools/`.

### Optional script prerequisites

Python is optional at runtime. Do not ask the taxpayer to install Python: the
agent applies the same explicit checks from the bundled knowledge and skill
instructions. The bundled scripts are best-effort mechanical accelerators, not
the primary mechanism. Runtime scripts cover evidence inventory/hash, field-map
checks, and source-pinned arithmetic checks. Repository-only validators and
source-maintenance tooling are not installed. On hosts without Python, the
agent-driven manual checks in each `SKILL.md` apply.

## Skill inventory

| Skill | Type | Main responsibility |
|---|---|---|
| `nl-tax-intake` | user entry | Screen scope, select a supported workflow, create `workspace/taxpayer/profile.yaml` |
| `nl-tax-evidence-indexer` | user entry | Index local evidence files, compute hashes, produce review questions |
| `nl-tax-annual-return` | user entry | Prepare the annual 2025 workpack and invoke the mapper for its field map (incl. the belastbare winst for a straightforward eenmanszaak) |
| `nl-tax-provisional-assessment` | user entry | Prepare 2026 request, change, review, or stopzetten packages |
| `nl-tax-field-mapper` | user entry | Convert workpack findings into manual-entry field maps |
| `nl-tax-submit-companion` | explicit user entry | Create a human-only manual-entry checklist when the user asks naturally or accepts the mapper's immediate offer |
| `nl-tax-box1-home` | background | Return sourced Box 1 and own-home facts/questions to the owning workflow |
| `nl-tax-box2` | background | Return standard Box 2 facts/questions to the owning workflow |
| `nl-tax-box3` | background | Return trusted-row, method-specific Box 3 facts without method mixing |
| `nl-tax-winst` | background | Return annual-2025 business findings, incl. the ordered belastbare-winst chain for a straightforward eenmanszaak, or one sourced provisional-2026 expected-profit forecast |
| `nl-tax-partner-deductions` | background | Return fiscal-partner, deduction, and allocation facts/questions |

The `skills/_shared/` directory is packaged as the hidden
`nl-tax-shared-resources` internal skill so OpenAI plugin ingestion can validate
the shared runtime contract and resources. It is not a taxpayer workflow and
cannot be invoked implicitly.

Only the annual and provisional workflow skills write main workpacks. Intake
creates taxpayer/session state, the field mapper alone writes canonical field
maps, and background helpers write no artifacts. A host may use specialist
subagents to cross-check already-collected, independent sections, but the main
conversational agent remains the only writer, question asker, workflow router,
and readiness authority. Subagents never create a second taxpayer workflow.
Persisted statuses are a resumability and completeness ledger, not a state
machine that chooses questions or tax treatment.

The annual workflow uses a coverage checklist (intake gate, evidence review,
Box 1/own home, optional winst, Box 2, Box 3, partner allocations, field
mapping, and final review). The agent may change the conversational order when
the taxpayer's facts make another order clearer; the checklist prevents
omissions rather than scripting an interview.
Its reviewed 2025 deduction guidance includes the specific-healthcare-cost
threshold and increase, the EUR 925 limited-mobility transport forfait, the
narrow legacy DUO prestatiebeurs study-cost exception, and
jaarruimte/reserveringsruimte. The agent uses the official Belastingdienst
Hulpmiddel Lijfrentepremie for lijfrente limits and retains its result; no local
universal pension-room calculator replaces the official tool.
The provisional workflow has four separate subflows: request, change, review, and
stopzetten. `nl-tax-winst` determines the annual-2025 belastbare winst uit
onderneming for a straightforward eenmanszaak from a finalized profit-and-loss
statement and balance, and supports the single bounded provisional field
`onderneming.geschatte_winst`. Every other IB business form is recognised and
routed to manual review; it never computes a stakingswinst, a reserve movement,
a terbeschikkingstellingsresultaat, a medegerechtigde loss cap, or a per-vennoot
winstaandeel, and it is not a provisional tax engine or final-tax calculator.

The package passes manifest and discovery checks, including host-specific
validation when the relevant CLI capability is installed. Those checks do not
replace fresh-task smoke tests in Work web, Work desktop, Codex, and Claude.

On hosts with scheduled tasks, users can request deadline reminders,
missing-document check-ins, source-freshness reports, or resumed draft reviews.
These continue from the saved conversation ledger; they do not introduce a
fixed questionnaire or Python-owned tax workflow.

## Scope

The plugin intentionally has **no** backend service, web app, browser/Chrome or
computer-use portal control, signing, filing, Digipoort transport, or autonomous submission. It helps the
taxpayer collect information, review it, and follow source-traceable guidance
while filling the official forms manually.

The taxpayer or an authorized human performs every authenticated portal action
on their own device. Host permissions, browser tools, screen interaction, and
user consent do not override that boundary. Public read-only research on
official sources is still allowed.

It must not prepare 2027 annual or provisional workpacks from 2025/2026 values — future tax
years become active only after exact official source snapshots are added and all validators
pass.
