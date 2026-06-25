---
name: nl-tax-annual-return
description: Prepare a 2025 Dutch annual income-tax (aangifte IB) workpack for manual Mijn Belastingdienst entry. Use after intake routes to annual_2025 — walks box 1, own home, box 2, box 3, deductions, partner allocation, and credits.
allowed-tools:
  - Read
  - Grep
  - Write
  - Edit
  - Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/nl-tax-field-mapper/scripts/*.py:*)
---

# NL Tax Annual Return

Prepare local guidance for manually filling the 2025 annual income-tax form. The workpack is a preparation document for Mijn Belastingdienst; it does not file, submit, sign, or give official tax advice.

This skill is conversational. Do not assume the user has pre-staged a complete folder. Walk the user through the workflow defined in [`reference/annual-flow.md`](reference/annual-flow.md), persist progress after every turn, and generate the workpack only after the explicit confirmation phrase below.

## Path resolution

Bundled paths (`reference/`, `templates/`, `_shared/`) are relative to this skill's own directory; `_shared/` is `../_shared/`. Resolve bundled files with host file tools (`Read` first, `Glob` or `Grep` if a path is not obvious). Do not use Bash to discover or read plugin files: in Cowork, shell commands run in an isolated VM that may not see the plugin cache even when `Read` and `Glob` can. If the host has already expanded `${CLAUDE_PLUGIN_ROOT}` or `${CLAUDE_SKILL_DIR}`, those absolute paths are fine for file tools; otherwise search within the loaded plugin/skill tree and resolve relative to this skill directory. Resolve every `workspace/...` path against `workspace_root` from `session-progress.yaml` (or `profile.yaml`); never create a second `workspace/` tree.

Safety: only run Python under an already-resolved plugin `skills/.../scripts/` path (this skill runs the bundled `nl-tax-field-mapper/scripts/validate_field_map.py`), and only if Bash can access that path. If Bash cannot see the plugin path, perform the equivalent validation manually against `nl-tax-field-mapper/reference/mapping-principles.md` (read it with the file tools); never copy bundled scripts into `workspace/`. Never execute a `.py` located under `workspace/`, `uploads/`, or `evidence/`.

## Read first (mandatory every turn)

Before the first user-facing reply on each turn, load these files. Append every loaded `source_id` (from `_shared/source-register.yaml`) to `sections … sources_loaded` in `session-progress.yaml`; only those IDs may appear in the workpack's "Sources used" section.

Always:

1. `reference/annual-flow.md` — the 10 numbered phases this skill follows
2. `reference/annual-output-contract.md` — the structural and safety rules for the workpack
3. `templates/annual-return-pack.md` — the workpack template
4. `workspace/taxpayer/profile.yaml`
5. `workspace/shared/session-progress.yaml`
6. `workspace/taxpayer/evidence-index.yaml` if it exists

Before generating any workpack content (Phase 2 onward in `annual-flow.md`), load the 2025 rate sheets. These are canonical for every numeric line the workpack will reference — do not paraphrase rates from memory.

- `_shared/knowledge/years/2025/annual/box1-rates.md`
- `_shared/knowledge/years/2025/annual/credits.md`
- `_shared/knowledge/years/2025/annual/own-home.md`
- `_shared/knowledge/years/2025/annual/deductions.md`
- `_shared/knowledge/years/2025/annual/late-filing.md`
- `_shared/knowledge/years/2025/annual/filing-flow.md`
- `_shared/knowledge/years/2025/annual/evidence-checklist.md`
- `_shared/knowledge/years/2025/box3/fictitious.md`
- `_shared/knowledge/years/2025/box3/actual-return.md`
- `_shared/knowledge/years/2025/box2/box2-rates.md` (only when the case has an aanmerkelijk belang — `box2.has_aanmerkelijk_belang: yes`)
- `_shared/knowledge/years/2025/box2/box2-income-guidance.md` (same condition)
- `_shared/knowledge/years/2025/box2/fisin-aanmerkelijk-belang.md` (same condition)
- `_shared/knowledge/own-home/eigenwoningforfait.md`
- `_shared/knowledge/own-home/hypotheekrenteaftrek.md`
- `_shared/knowledge/partners/fiscal-partnership.md`

If a rate sheet fails to load, stop and tell the user — do not fabricate a rate.

Confirm `workflow_candidate: annual_2025`. If the profile is missing or the workflow is unsupported, hand control back to `nl-tax-intake`.

## Resume guard

`session-progress.yaml` is the resume contract. Before doing any work:

- If `session-progress.yaml` is missing or empty, reconstruct it from `profile.yaml` and `_shared/templates/session-progress.yaml` before proceeding.
- If `profile.yaml` shows `intake_status: complete`, never restart intake — continue the annual workflow from recorded progress.
- Skip any subsection already marked `complete`, `chat_only`, or `deferred` in `session-progress.yaml`.

## Workflow

`reference/annual-flow.md` is authoritative. It defines 10 phases (Pre-flight → Income → Own home → Box 2 → Box 3 → Deductions → Partner → Field map → Missing info → Review questions → Assembly). Follow them in order, and within each phase apply the conversational contract below.

### Conversational contract

For every phase:

1. Read `workspace/shared/session-progress.yaml` and skip subsections already marked `complete`, `chat_only`, or `deferred`.
2. Check existing evidence and notes before asking the user anything.
3. Ask for gaps in groups of **at most 3 closely related questions**, with one exception: when the questions all come from a **single artifact** (one mortgage statement, one WOZ-beschikking, one jaaropgaaf), ask up to **6 questions** in a single batch. The canonical case is eigen woning with tijdelijke twee woningen, which needs the move date, both addresses, both WOZ-waarden, both mortgage statements, and the vacancy/listing status.
4. Accept either a file or a chat answer for each value (see "Evidence handoff" below).
5. Record every value under `workspace/annual/2025/notes/<section>.yaml` with `source` (`file`, `user_chat`, `assumption`, or `unknown`) and either `evidence_id` or `quote` plus `stated_at`.
6. If the user cannot answer, record `source: unknown`, add the item to `workspace/shared/missing-info.md`, and continue.
7. Update `workspace/shared/session-progress.yaml`: move answered question ids into `answered`, leave open ones in `open_questions`, set subsection `status` accordingly, and append any new `source_id` to `sources_loaded`.

Never silently treat missing values as zero. Use assumptions only after the user explicitly accepts them.

### Evidence handoff

For every value the user could provide:

- **User uploads a file** (to `uploads/` or `evidence/`) → invoke `nl-tax-evidence-indexer`, then read the resulting `evidence-index.yaml` and reference values by `evidence_id`. The subsection is `complete` once the file is indexed and the value extracted.
- **User states the value in chat only** → record the value with `source: user_chat`, set the subsection's `status: chat_only`, and continue. This is an explicit choice, not a gap. Do not nag for a file the user has declined to upload.
- **User says they will provide later** → record `source: unknown`, set `status: deferred`, add the item to `missing-info.md`, and continue.

A subsection in `chat_only` counts as filled for the generation gate, but the workpack's Human Review checklist must list every `U:` line for spot-checking before filing.

### Helper delegation

The box and partner phases use the background helper contracts. Prefer a direct Skill/Task invocation when the host provides one. If no Skill/Task tool exists, inline the helper's SKILL.md instructions in this workflow and write the helper-owned `workspace/shared/` files yourself. This fallback is allowed for annual and provisional owning workflows, but the ownership boundary does not change: helpers own only their named `workspace/shared/` artifacts, and this skill owns `workspace/annual/**`.

In each phase, invoke or inline the matching helper, let it append its question packet under `workspace/shared/`, ask the user those questions, record the answers, then re-invoke/re-run the helper contract to fold them into its notes:

- **Box 1 / own home** → `nl-tax-box1-home` (writes `workspace/shared/box1-home-notes.md` and `workspace/shared/box1-home-open-questions.yaml`)
- **Box 2** → `nl-tax-box2` (writes `workspace/shared/box2-notes.md` and `workspace/shared/box2-open-questions.yaml`). Only when the case has a real Box 2 position (`box2.has_aanmerkelijk_belang: yes`): load the three box 2 rate sheets listed above first, and — because the helper cannot update annual progress — this skill MUST append `bd_box2_rates_2025_2026`, `bd_box2_income_ab_guidance`, and `bd_fisin_aanmerkelijk_belang_2025` to `session-progress.yaml` → `sources_loaded`, so the workpack's Sources Used section matches the Box 2 facts it cites.
- **Box 3** → `nl-tax-box3` (writes `workspace/shared/box3-notes.md`, `workspace/shared/box3-open-questions.yaml`, and `workspace/shared/box3-review-questions.md`; annual collects fictitious **and** werkelijk rendement for the comparison)
- **Partner / deductions** → `nl-tax-partner-deductions` (writes `workspace/shared/allocation-options.md`, `workspace/shared/partner-deductions-open-questions.yaml`, and `workspace/shared/partner-deduction-review-questions.md`)

Read `workspace/shared/box2-notes.md` and `workspace/shared/box2-open-questions.yaml` back before assembling the Box 2 section. Read the sibling helpers' named notes/open-question artifacts back before assembling their sections. The helpers never write to `workspace/annual/**`; this skill owns that tree.

## Sections in the workpack

The output contract requires 19 sections in order. Don't confuse "sections the user is asked about" with "sections the workpack emits". The emitted workpack sections are:

1. Scope
2. Unsupported-case checks
3. Sources used
4. Taxpayer profile summary
5. Evidence summary
6. Filing status and late-filing exposure
7. Income notes
8. Own-home notes
9. Box 2 notes
10. Box 3 notes
11. Deductions notes
12. Credits screening
13. Fiscal partner notes
14. Field map summary
15. Missing information
16. Assumptions
17. User-stated values index
18. Human review checklist
19. Not submission advice

**User-facing question groups (you ask the user about these):**

1. Filing status (on-time, uitstel, or late — drives late-filing exposure)
2. Box 1 employment / pension / benefit / other income
3. Own home — WOZ, mortgage interest, mortgage type, tariefsaanpassing, Hillenregeling, two-homes if applicable
4. Box 2 — substantial-interest status and standard fields, or "not applicable"
5. Box 3 peildatum (1 January 2025) values; box 3 actual-return data for the comparison
6. Deductions — alimentatie, zorgkosten, giften, lijfrentepremie, other
7. Credits screening — IACK, ouderenkorting, alleenstaande-ouderenkorting, jonggehandicaptenkorting triggers based on household composition (already in `profile.yaml`)
8. Fiscal partner status and allocation choices
9. Final review and confirmation

Match this list to `reference/annual-output-contract.md`. If anything diverges, the contract wins.

## Workpack generation gate

Do not write `workspace/annual/2025/return-pack.md` until **all** of:

1. Every annual subsection in `session-progress.yaml` is `complete`, `chat_only`, or `deferred`.
2. The user has typed one of these confirmation phrases verbatim in chat:
   - `generate the workpack`
   - `genereer de workpack`
   - `klaar voor workpack`

   Or the user has run `/nl-tax-agent-skills:nl-tax-annual-return confirm`. Anything else (including "looks good", "yes", "ok let's do it") is **not** confirmation — ask explicitly: "Type 'generate the workpack' when you want me to assemble it."

When the gate is satisfied:

- Assemble `workspace/annual/2025/notes/*.yaml` into `templates/annual-return-pack.md`.
- Preserve source provenance for every numeric line using the `Src` codes from the template.
- Run the self-check in `reference/annual-output-contract.md` § "Workpack self-check"; report every check yes/no in your end-of-turn message. If any structural, content, cross-contamination, or safety check fails, do not write the file — fix the gap or ask the user, and re-run.
- Set the workpack's top-of-file STATUS banner deterministically from `session-progress.yaml`: if any annual subsection is `deferred` or `unknown`, the banner reads `DRAFT`; otherwise it reads `COMPLETE DRAFT FOR REVIEW`. In both cases the banner always says "not for filing". Treat a mismatch between the banner and `session-progress.yaml` as a blocking self-check item.
- Write `workspace/annual/2025/field-map.yaml`. Optionally record the same readiness state as a **top-level** `readiness` key in `field-map.yaml` (`draft` or `review_ready` — the values `validate_field_map.py` accepts).
- After writing `field-map.yaml`, run `nl-tax-field-mapper/scripts/validate_field_map.py` against it and treat validation failure as a blocking self-check item; the field-map MUST conform to the `nl-tax-field-mapper` schema (`templates/field-map-template.yaml` + `reference/annual-field-map.md`) and use `field_id`s from that reference.

## Output files

Write incrementally:

- `workspace/annual/2025/notes/<section>.yaml`
- `workspace/shared/session-progress.yaml`
- `workspace/shared/missing-info.md`
- `workspace/shared/assumptions.md`

Write only after the generation gate:

- `workspace/annual/2025/return-pack.md`
- `workspace/annual/2025/field-map.yaml`

Do not write `workspace/provisional/**`.

## Safety

- Do not log in, submit, sign, automate forms, or collect BSN.
- Do not present output as official advice or a final calculation.

## Worked example

> Profile shows `annual_2025`, a single resident, one employer, an eigen woning, no Box 2. In Phase 2 (Income) the agent reads `evidence-index.yaml`, sees an indexed jaaropgaaf, references gross income by `evidence_id`, and asks only for the one missing loonheffing figure. In Phase 3 it invokes `nl-tax-box1-home` for the own-home line, asks the WOZ + mortgage-interest questions the helper returned, then re-invokes it. Box 3 invokes `nl-tax-box3`, collecting both fictitious and werkelijk-rendement data for the comparison. Nothing is written to `return-pack.md` until the user types `generate the workpack`; then the agent runs the output-contract self-check, writes `return-pack.md` + `field-map.yaml`, and reports each check yes/no.

## End-of-turn report

After each turn, tell the user in 2-4 sentences which tax topic was covered, whether values came from uploaded/indexed files or chat, and what comes next. Do not mention internal status names or file-maintenance details.
