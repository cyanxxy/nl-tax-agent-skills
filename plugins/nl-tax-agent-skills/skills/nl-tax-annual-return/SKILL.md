---
name: nl-tax-annual-return
description: Use when the user explicitly wants to prepare or review a 2025 Dutch annual income-tax workpack for manual entry, including standard business preparation and Boxes 1–3.
argument-hint: "[2025] [confirm]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - AskUserQuestion
  - Bash(python3:*)
---

# NL Tax Annual Return

Prepare local guidance for manually filling the 2025 annual income-tax form. The workpack is a preparation document for Mijn Belastingdienst; it does not file, submit, sign, or give official tax advice.

This skill is conversational. Do not assume the user has pre-staged a complete folder. Walk the user through the workflow defined in [`reference/annual-flow.md`](reference/annual-flow.md), persist progress after every turn, and generate the workpack only after the explicit confirmation phrase below.

## Path resolution

Read `../_shared/runtime-contract.md` first. Bundled paths (`reference/`,
`templates/`, `_shared/`) are relative to this skill's own directory;
`_shared/` is `../_shared/`. Use the host's skill-resource or file tools to
resolve them, and do not depend on shell visibility or vendor-specific
environment variables. Resolve every `workspace/...` path against
`workspace_root` from `session-progress.yaml` (or `profile.yaml`); never create
a second `workspace/` tree.

Field-map resources are sibling-skill paths, never local `templates/` or
`reference/` paths: `nl-tax-field-mapper/templates/field-map-template.yaml`,
`nl-tax-field-mapper/reference/mapping-principles.md`,
`nl-tax-field-mapper/reference/annual-field-map.md`, and
`nl-tax-field-mapper/scripts/validate_field_map.py`. The field mapper owns use
of those resources and the canonical map artifact.

## Read first

Two different read cadences apply. Record every loaded knowledge file's `source_id` (from `_shared/source-register.yaml`) in the top-level `sources_loaded` list in `session-progress.yaml` — add each ID once, the first time its file is loaded; never append duplicates. Only those IDs may appear in the workpack's "Sources used" section.

**Workspace state — re-read before the first user-facing reply on every turn** (it may have changed since the last turn):

1. `workspace/taxpayer/profile.yaml`
2. `workspace/shared/session-progress.yaml`
3. `workspace/taxpayer/evidence-index.yaml` if it exists

**Bundled workflow references — load progressively.** Load
`reference/annual-flow.md` when this skill becomes active. Then load exactly
one active phase file immediately before performing that phase; re-read the
active file only when resuming from disk or when its exact wording is needed.
Do not preload later phases:

1. `reference/phases/01-preflight.md`
2. `reference/phases/01-5-filing-status.md`
3. `reference/phases/02-income.md`
4. `reference/phases/02a-winst.md`
5. `reference/phases/03-own-home.md`
6. `reference/phases/03a-box2.md`
7. `reference/phases/04-box3.md`
8. `reference/phases/05-deductions.md`
9. `reference/phases/05-5-credits.md`
10. `reference/phases/06-partner.md`
11. `reference/phases/07-field-map.md`
12. `reference/phases/08-missing-info.md`
13. `reference/phases/09-review-questions.md`
14. `reference/phases/10-assembly.md`

Do not load `reference/annual-output-contract.md` or
`templates/annual-return-pack.md` during collection. Load `annual-return-pack.md` only after
the workpack generation gate opens, together
with `annual-output-contract.md` for the final self-check.

Load knowledge only for the active phase and only when the case needs it:

- Filing status: `_shared/knowledge/years/2025/annual/filing-flow.md`; add
  `_shared/knowledge/years/2025/annual/late-filing.md` only for
  granted-extension/outstanding or late-exposure branches.
- Income: `_shared/knowledge/years/2025/annual/box1-rates.md`.
- Business: only the entrepreneur files actually needed when
  `business.has_onderneming.value` is true.
- Own home: `_shared/knowledge/years/2025/annual/own-home.md`,
  `_shared/knowledge/own-home/eigenwoningforfait.md`, and
  `_shared/knowledge/own-home/hypotheekrenteaftrek.md`; add Box 1/deduction rates only when the
  top-rate adjustment is applicable.
- Box 2: only the three Box 2 files when an aanmerkelijk belang exists.
- Box 3: `_shared/knowledge/years/2025/box3/fictitious.md` and
  `_shared/knowledge/years/2025/box3/actual-return.md`.
- Deductions: `_shared/knowledge/years/2025/annual/deductions.md`.
- Credits: `_shared/knowledge/years/2025/annual/credits.md` and
  `_shared/knowledge/aow/aow-leeftijd.md` when AOW screening
  needs the reviewed age rule.
- Partner allocation: `_shared/knowledge/partners/fiscal-partnership.md`.
- Evidence checklist:
  `_shared/knowledge/years/2025/annual/evidence-checklist.md`, only when the
  user chooses document-based collection.

Do not load or stale-check a source for an inapplicable branch. If a required
active-phase source fails to load, stop that phase and tell the user; never
fabricate a rate.

**Source-pack staleness check (warn, don't block):** the first time knowledge files are loaded in a session, compare each loaded source's `last_checked` in `_shared/source-register.yaml` against its `freshness_policy` cadence and today's date. If any source required by this workflow is past its cadence, tell the user once, in one sentence, that the source pack may be stale (name the stale `source_id`s) and that the values should be double-checked in Mijn Belastingdienst before filing. Staleness never blocks workpack generation; list the stale `source_id`s in the workpack's Human review checklist instead.

Confirm `workflow_candidate: annual_2025`. If the profile is missing or the workflow is unsupported, hand control back to `nl-tax-intake`.

## Resume guard

`session-progress.yaml` is the resume contract. Before doing any work:

- If `session-progress.yaml` is missing or empty, require intake to create it:
  return control to `nl-tax-intake` and do not create annual artifacts.
- For a pre-1.4 state, migrate it in place as defined by the shared
  elicitation contract: add both missing winst subsections without changing
  existing answers, then set version 1.4. Mark annual winst `complete` with a
  stable answered `not applicable` entry only when profile facts establish
  there is no business.
- If `profile.yaml` shows `intake_status: complete`, never restart intake — continue the annual workflow from recorded progress.
- Skip subsections marked `complete` or `chat_only`. A `deferred` subsection
  remains open: do not nag during the same pass, but reopen it when the user
  supplies the fact, asks to resume missing items, or reaches final missing-info
  review.

## Workflow

`reference/annual-flow.md` is the authoritative ordered index. Follow its 14
directly linked phases in order, loading exactly one active phase at a time,
and within each phase apply the conversational contract below.

### Conversational contract

For every phase:

1. Read `workspace/shared/session-progress.yaml`; skip `complete` and `chat_only` subsections. Preserve deferred questions as open and revisit them only when the user resumes them or during final missing-info review.
2. Check existing evidence and notes before asking the user anything.
3. Ask for gaps in groups of **at most 3 closely related questions**, with one exception: when the questions all come from a **single artifact** (one mortgage statement, one WOZ-beschikking, one jaaropgaaf), ask up to **6 questions** in a single batch. The canonical case is eigen woning with tijdelijke twee woningen, which needs the move date, both addresses, both WOZ-waarden, both mortgage statements, and the vacancy/listing status.
4. Accept either a file or a chat answer for each value (see "Evidence handoff" below).
5. Record every value under `workspace/annual/2025/notes/<section>.yaml` with `source` (`file`, `user_chat`, `calculated`, `assumption`, or `unknown`) and the matching provenance.
6. If the user cannot answer, record `source: unknown`, keep the question ID in `open_questions` rather than `answered`, add the item to `workspace/shared/missing-info.md`, and continue.
7. Update `workspace/shared/session-progress.yaml`: put only resolved question IDs in `answered`, leave deferred ones in `open_questions`, set subsection and workflow rollup statuses, update the shared user-chat evidence ledger, and append only actually loaded `source_id`s to `sources_loaded`.

Never silently treat missing values as zero. Use assumptions only after the user explicitly accepts them.

### Evidence handoff

For every value the user could provide:

- **User uploads a file** (to `uploads/` or `evidence/`) → invoke `nl-tax-evidence-indexer`, then read the resulting `evidence-index.yaml` and reference values by `evidence_id`. The subsection is `complete` once the file is indexed and the value extracted.
- **User states the value in chat only** → record the value with `source: user_chat`, set the subsection's `status: chat_only` when all required facts are supplied, update `sections.evidence.subsections.user_chat_values`, and continue. This is an explicit choice, not a gap. Do not nag for a file the user has declined to upload.
- **User says they will provide later** → record `source: unknown`, set `status: deferred`, keep the question in `open_questions`, add the item to `missing-info.md`, and continue.

A subsection in `chat_only` counts as filled for the generation gate, but the workpack's Human Review checklist must list every `U:` line for spot-checking before filing.

### Helper delegation

The box and partner phases use background helper contracts. Prefer direct
Skill/Task invocation when the host provides it; otherwise inline the helper's
instructions. In both modes the helper returns structured facts and open
questions in its response and writes nothing. This owning workflow must
persist the returned facts and open questions in the matching
`workspace/annual/2025/notes/<section>.yaml`, update session state, ask the user,
and re-run the helper with the newly sourced answers.
Keep this delegation invisible to the user; continue the tax conversation in
one voice and never announce helper or skill activation.

- **Box 1 / own home** → `nl-tax-box1-home`
- **Winst uit onderneming** → `nl-tax-winst` when
  `business.has_onderneming.value` is true. Load the entrepreneur sources
  actually consulted and append their returned source IDs to `sources_loaded`.
  Require finalized profit-and-loss and balance evidence, organize facts and
  questions only, and keep the annual field map draft with a business-section
  schema-review blocker. Never derive final taxable business profit or claim a
  complete business return.
- **Box 2** → `nl-tax-box2` when
  `box2.has_aanmerkelijk_belang.value` is true. Load the Box 2 sources listed
  above and append their returned source IDs to `sources_loaded`.
- **Box 3** → `nl-tax-box3` (annual collects fictitious and werkelijk
  rendement for comparison).
- **Partner / deductions** → `nl-tax-partner-deductions`.

Historical `workspace/shared/*-notes.md`, `*-open-questions.yaml`, and helper
review files remain readable for resume compatibility only. They must not be
updated or created in a new run. Fold any useful legacy content into the
workflow-owned annual notes before continuing. This skill owns session state,
annual notes, and the annual workpack; helpers own no persisted artifact.

## Sections in the workpack

The output contract requires 20 sections in order. Don't confuse "sections the user is asked about" with "sections the workpack emits". The emitted workpack sections are:

1. Scope
2. Unsupported-case checks
3. Sources used
4. Taxpayer profile summary
5. Evidence summary
6. Filing status and late-filing exposure
7. Income notes
8. Winst uit onderneming notes
9. Own-home notes
10. Box 2 notes
11. Box 3 notes
12. Deductions notes
13. Credits screening
14. Fiscal partner notes
15. Field map summary
16. Missing information
17. Assumptions
18. User-stated values index
19. Human review checklist
20. Not submission advice

**User-facing question groups (you ask the user about these):**

1. Filing status (on-time, uitstel, or late — drives late-filing exposure)
2. Box 1 employment / pension / benefit / other income
3. Winst uit onderneming — preparation-only review of finalized profit-and-loss, balance, status, hours, investments, and candidate-deduction evidence (eenmanszaak / ZZP), or "not applicable"
4. Own home — WOZ, mortgage interest, mortgage type, tariefsaanpassing, Hillenregeling, two-homes if applicable
5. Box 2 — substantial-interest status and standard fields, or "not applicable"
6. Box 3 peildatum (1 January 2025) values; box 3 actual-return data for the comparison
7. Deductions — alimentatie, zorgkosten, giften, lijfrentepremie, other
8. Credits screening — IACK, ouderenkorting, alleenstaande-ouderenkorting, jonggehandicaptenkorting triggers based on household composition (already in `profile.yaml`)
9. Fiscal partner status and allocation choices
10. Final review and confirmation

Match this list to `reference/annual-output-contract.md`. If anything diverges, the contract wins.

## Workpack generation gate

Do not write `workspace/annual/2025/return-pack.md` until **all** of:

1. Every annual subsection in `session-progress.yaml` is `complete`, `chat_only`, or `deferred`.
2. No blocking deferred item remains. Nonblocking deferred items may produce a
   `DRAFT` only after the explicit confirmation below.
3. The user has typed one of these confirmation phrases verbatim in chat:
   - `generate the workpack`
   - `genereer de workpack`
   - `klaar voor workpack`

   Or the user has run `/nl-tax-agent-skills:nl-tax-annual-return confirm`. Anything else (including "looks good", "yes", "ok let's do it") is **not** confirmation — ask explicitly: "Type 'generate the workpack' when you want me to assemble it."

When the gate is satisfied:

- Load `reference/annual-output-contract.md` and
  `templates/annual-return-pack.md` now; neither belongs in collection context.
- Assemble `workspace/annual/2025/notes/*.yaml` into `templates/annual-return-pack.md`.
- Preserve source provenance for every numeric line using the `Src` codes from the template.
- Run the self-check in `reference/annual-output-contract.md` § "Workpack self-check"; report every check yes/no in your end-of-turn message. If any structural, content, cross-contamination, or safety check fails, do not write the file — fix the gap or ask the user, and re-run.
- Set the workpack's top-of-file STATUS banner deterministically from `session-progress.yaml`: if any annual subsection is `deferred`, or contains a `source: unknown` / open blocking item, the banner reads `DRAFT`; otherwise it reads `COMPLETE DRAFT FOR REVIEW`. In both cases the banner always says "not for filing". Treat a mismatch between the banner and `session-progress.yaml` as a blocking self-check item.
- Use only the two resolved resources named above. Do not probe speculative template names or add Git/repository checks to the workpack self-check.
- Before invoking the mapper, recompute and persist the annual rollup from the
  subsections. Set `sections.annual_2025.status: complete` only when every
  applicable subsection is `complete` or `chat_only`; otherwise set it to
  `in_progress`. Keep `active_skill: nl-tax-annual-return` through validation.
- After the confirmed workpack is written and the rollup is current, invoke `nl-tax-field-mapper`. Pass
  it the workpack and workflow context; it alone writes and validates
  `workspace/annual/2025/field-map.yaml` using
  `nl-tax-field-mapper/templates/field-map-template.yaml`,
  `nl-tax-field-mapper/reference/mapping-principles.md`,
  `nl-tax-field-mapper/reference/annual-field-map.md`, and
  `nl-tax-field-mapper/scripts/validate_field_map.py`. The mapper derives its
  `readiness` from this same session rollup; optional script output cannot
  promote a draft. Treat a structural/provenance validation failure or a
  readiness mismatch as blocking before presenting the manual-entry map.
- After successful mapping, clear `active_skill` only when the persisted annual
  rollup is `complete`. Otherwise keep `active_skill: nl-tax-annual-return` so
  later chat answers resume the draft. A deferred question must remain open and
  must not also be listed as answered.
- If any sourced fact changes after a workpack was generated, reset the
  `confirm` subsection to `not_started`. Recompute affected calculations and
  require a fresh exact generation phrase before overwriting the canonical
  workpack and field map.

## Output files

Write incrementally:

- `workspace/annual/2025/notes/<section>.yaml`
- `workspace/shared/session-progress.yaml`
- `workspace/shared/missing-info.md` (seed from `_shared/templates/missing-info.md` on first write)
- `workspace/shared/assumptions.md` (seed from `_shared/templates/assumptions.md` on first write)

Write only after the generation gate:

- `workspace/annual/2025/return-pack.md`

The invoked field mapper separately produces the unchanged public artifact
`workspace/annual/2025/field-map.yaml`; this workflow does not write it.

Do not write `workspace/provisional/**`.

## Safety

- Do not log in, submit, sign, automate forms, or collect BSN.
- Do not present output as official advice or a final calculation.

## Worked example

> Profile shows `annual_2025`, a single resident, one employer, an eigen woning, no Box 2. In Phase 2 (Income) the agent reads `evidence-index.yaml`, sees an indexed jaaropgaaf, references gross income by `evidence_id`, and asks only for the one missing loonheffing figure. In Phase 3 it invokes `nl-tax-box1-home` for the own-home line, persists the returned WOZ + mortgage-interest questions in annual notes, asks them, then re-invokes it. Box 3 invokes `nl-tax-box3`, collecting both fictitious and werkelijk-rendement data for the comparison. Nothing is written to `return-pack.md` until the user types `generate the workpack`; then the agent runs the output-contract self-check, writes `return-pack.md`, and invokes `nl-tax-field-mapper` to produce the canonical `field-map.yaml`.

## End-of-turn report

After each turn, tell the user in 2-4 sentences which tax topic was covered, whether values came from uploaded/indexed files or chat, and what comes next. Do not mention internal status names or file-maintenance details.
