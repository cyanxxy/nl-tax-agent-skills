# LLM-Native Agent Skill Plan - NL Tax Skills

**Created:** 2026-04-30
**Purpose:** Redesign the current Dutch tax capability as a plugin that bundles LLM-native Agent Skills, not as a loose collection of static templates and scripts.
**Scope:** `plugins/nl-tax-agent-skills/` is the primary distributable plugin. The bundled skills support Dutch annual return 2025 and voorlopige aanslag 2026 workpack preparation.

---

## 1. Product Direction

The repository should ship a plugin that helps a person prepare a Dutch tax workpack through an LLM-guided workflow.

The plugin package is the release artifact:

```text
plugins/nl-tax-agent-skills/
  .claude-plugin/plugin.json
  .codex-plugin/plugin.json
  assets/
  skills/
```

Standalone `.claude/skills/` and `.agents/skills/` directories have been removed from the cleaned project. Skills live inside the plugin package.

The LLM should do the high-value work:

- ask targeted intake and follow-up questions;
- reason over the selected workflow;
- read and synthesize local source snapshots;
- interpret messy evidence summaries;
- identify missing facts, assumptions, blockers, and review questions;
- draft source-backed workpacks in plain language;
- map facts to manual-entry field maps;
- keep annual return and provisional assessment paths separate.

Scripts should stay small and deterministic:

- hash and list files;
- validate schemas and output contracts;
- run simple calculations;
- detect obvious invalid fields;
- report source-pack freshness and snapshot consistency.

The plugin is the product. Its bundled skills are the agent-facing workflow layer and must read like operating playbooks for an LLM agent.

---

## 2. Immediate Bug Fix Phase

Before the LLM redesign, fix the contract bugs found in review.

### 2.1 Annual output path

- [x] Change annual return skill output from `workspace/annual/2025/workpack.md` to `workspace/annual/2025/return-pack.md`.
- [x] Update field mapper references to read `return-pack.md`.
- [x] Update README references if needed.
- [ ] Add a validation check that annual and provisional outputs use their PRD paths.

### 2.2 Box 3 formula consistency

- [x] Fix `compare_box3_annual_2025.py` so debt weighting follows the local rule note formula.
- [x] Fix `summarize_box3_provisional_2026.py` the same way.
- [ ] Add examples or self-check cases where debts are present.
- [ ] Ensure annual 2025 can compare fictitious vs actual return, while provisional 2026 remains fictitious-only.

### 2.3 Source refresh path handling

- [x] Fix `fetch_sources.py` repo-root derivation.
- [x] Verify `fetch_sources.py all` reports existing snapshots correctly.
- [ ] Keep source refresh scoped to official source-register URLs only.

### 2.4 Snapshot metadata model

- [x] Replace one directory-level `_snapshot-metadata.yaml` file with metadata that can represent every source sharing a directory.
- [ ] Preferred option: create one metadata file per source, for example `_snapshot-metadata/<source_id>.yaml`.
- [x] Update `build_snapshots.py` and validators accordingly.
- [ ] Ensure every registered source can be checked independently.

### 2.5 Provisional output contract

- [x] Update provisional skill output matrix so request, change, review, and stopzetten match the PRD.
- [x] Change and review flows must produce the required field map and review questions.
- [ ] Change flow must always include the "enter all data again" reminder.
- [ ] Stopzetten payment scenario must route to change/review rather than produce normal stopzetten guidance.

### 2.6 Box 1 gap detection

- [x] Fix `summarize_box1_inputs.py` to pass `identify_gaps(box1_items)` into `format_gaps()`.
- [ ] Add a no-evidence smoke case proving missing evidence is reported.

---

## 3. LLM Skill Rewrite Phase

Rewrite each bundled `SKILL.md` as an LLM operating playbook inside `plugins/nl-tax-agent-skills/skills/`.

Each skill should include:

- when the skill should activate;
- what the model must ask first;
- what local files to read progressively;
- reasoning steps the model should follow;
- when to stop and ask the user;
- how to handle partial evidence;
- what output files to write;
- the final response format after writing outputs;
- a short worked example.

Avoid making `SKILL.md` only a file list. The model needs behavioral instructions.

### 3.1 `nl-tax-intake`

- [ ] Convert into a conversational workflow router.
- [ ] Add an interview script with minimal questions.
- [ ] Write explicit routing logic for:
  - annual_2025;
  - provisional_2026_request;
  - provisional_2026_change;
  - provisional_2026_review;
  - provisional_2026_stopzetten;
  - unsupported.
- [ ] Add example user prompts and selected workflows.
- [ ] Make output profile generation a model task using the template, not a static schema copy.

### 3.2 `nl-tax-evidence-indexer`

- [ ] Make the LLM responsible for classifying evidence after the script hashes files.
- [ ] Add instructions for summarizing what each document appears to prove.
- [ ] Add "low confidence" follow-up questions.
- [ ] Keep the script as file inventory plus hashing only.

### 3.3 `nl-tax-annual-return`

- [ ] Rewrite as a model-led workpack authoring flow.
- [ ] Instruct the model to synthesize evidence, assumptions, missing items, and source notes.
- [ ] Include annual box 3 fictitious plus actual-return comparison behavior.
- [ ] Include worked example from the simple resident fixture.
- [ ] Ensure final output always uses `return-pack.md`.

### 3.4 `nl-tax-provisional-assessment`

- [ ] Rewrite as four separate model paths inside the skill: request, change, review, stopzetten.
- [ ] Make the change/review path baseline + forecast + delta driven.
- [ ] Make the request path estimate driven.
- [ ] Make stopzetten guidance-first, with payment users redirected to change/review.
- [ ] Include hard wording that provisional 2026 never collects werkelijk rendement.

### 3.5 Domain helper skills

- [ ] Convert `nl-tax-box1-home`, `nl-tax-box3`, and `nl-tax-partner-deductions` into reasoning helpers.
- [ ] Each helper should explain what notes it contributes to the main workpack.
- [ ] Scripts remain calculators or validators only.
- [ ] Add explicit handoff language: "write notes to workspace/shared/*; do not write main workpacks."

### 3.6 Field mapper

- [ ] Make field mapping a model synthesis task using references and workpack facts.
- [ ] Keep `validate_field_map.py` as a guardrail.
- [ ] Add examples for annual and provisional field maps.
- [ ] Normalize workflow values to `annual_return` and `provisional_assessment`.

### 3.7 Submit companion

- [ ] Make it produce a tailored manual checklist from the selected workpack and field map.
- [ ] Keep it manual-only.
- [ ] Include blockers first, then checklist steps.

---

## 4. Prompt Eval Phase

The current fixtures describe scenarios but do not execute model behavior. Add prompt-based evals.

### 4.1 Eval harness

- [ ] Add `evals/prompts/` with one prompt file per scenario.
- [ ] Add `evals/expected/` with expected file paths and required phrases.
- [ ] Add a lightweight runner script that checks generated files for:
  - required sections;
  - forbidden phrases;
  - output path correctness;
  - annual/provisional separation;
  - field map workflow and tax year;
  - source IDs listed.

### 4.2 Minimum prompt evals

- [ ] Annual simple resident.
- [ ] Annual partner plus box 3 actual return.
- [ ] Provisional request with new mortgage.
- [ ] Provisional change with salary increase.
- [ ] Provisional stopzetten refund.
- [ ] Provisional stopzetten payment redirect.
- [ ] Out-of-scope resident or deceased-taxpayer case.

### 4.3 LLM behavior checks

Each eval should check that the model:

- asks only necessary follow-up questions;
- writes the correct workpack paths;
- lists assumptions and missing info;
- uses source IDs from the register;
- does not merge annual and provisional flows;
- labels provisional values as estimates;
- keeps werkelijk rendement out of provisional 2026.

---

## 5. Output Contract Phase

Create machine-checkable contracts for the main outputs.

- [ ] Add an annual workpack validator for `workspace/annual/2025/return-pack.md`.
- [ ] Add a provisional workpack validator for `workspace/provisional/2026/provisional-pack.md`.
- [ ] Add a shared assumptions/missing-info validator.
- [ ] Add source-ID validation against `_shared/source-register.yaml`.
- [ ] Ensure validators support partial drafts with clear warnings, but fail on contract violations.

---

## 6. Knowledge Pack Phase

The knowledge pack should support LLM retrieval and synthesis.

- [ ] Keep rule notes short and structured.
- [ ] Add `Developer instruction` and `Common failure` sections where missing.
- [ ] Add source IDs to every rule note.
- [ ] Split broad files if the model has to load too much unrelated content.
- [ ] Add examples to the most important files:
  - annual box 3 actual-vs-fictitious;
  - provisional box 3 fictitious-only;
  - provisional change baseline + forecast + delta;
  - stopzetten refund vs payment routing.

---

## 7. Acceptance Criteria

This redesign is complete when:

- [x] `plugins/nl-tax-agent-skills/` is the primary package and includes plugin manifests, assets, README, and bundled skills.
- [ ] Plugin skills are invoked with namespaced commands such as `/nl-tax-agent-skills:nl-tax-intake`.
- [x] Standalone `.claude/skills` and `.agents/skills` mirrors are removed.
- [ ] The six review findings above are fixed.
- [ ] Every `SKILL.md` reads as an LLM workflow playbook.
- [ ] Scripts are deterministic helpers, not the primary product logic.
- [ ] Prompt evals exercise the LLM behavior for all supported workflows.
- [ ] Annual output uses `workspace/annual/2025/return-pack.md`.
- [ ] Provisional output uses `workspace/provisional/2026/provisional-pack.md`.
- [ ] Field maps use `annual_return` or `provisional_assessment`.
- [ ] Source-refresh tools agree on snapshot presence and metadata.
- [ ] Provisional 2026 never asks for werkelijk rendement.
- [ ] Workpacks include sources used, missing information, assumptions, human review checklist, and not-submission-advice sections.

---

## 8. Execution Order

1. Fix the six concrete review findings.
2. Make `plugins/nl-tax-agent-skills/` the primary package and remove standalone skill-tree mirrors.
3. Normalize file paths and workflow names across bundled skills, README, fixtures, and validators.
4. Rewrite `nl-tax-intake`, `nl-tax-provisional-assessment`, and `nl-tax-annual-return` as LLM playbooks.
5. Rewrite helper skills and field mapper.
6. Add prompt eval harness.
7. Add output contract validators.
8. Run all validators and prompt evals.

Do not add a backend, web app, filing automation, or tax engine. The target is a plugin whose payload is a bundled Agent Skills suite.
