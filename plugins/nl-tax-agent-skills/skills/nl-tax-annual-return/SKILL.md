---
name: nl-tax-annual-return
description: Prepare a 2025 Dutch annual income-tax (aangifte IB) workpack for manual Mijn Belastingdienst entry. Use after intake routes to annual_2025 — walks box 1, winst uit onderneming (eenmanszaak / ZZP), own home, box 2, box 3, deductions, partner allocation, and credits.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - Bash(python3:*)
---

# NL Tax Annual Return

Prepare local guidance for manually filling the 2025 annual income-tax form. The workpack is a preparation document for Mijn Belastingdienst; it does not file, submit, sign, or give official tax advice.

This skill is conversational. Do not assume the user has pre-staged a complete folder. Walk the user through the workflow defined in [`reference/annual-flow.md`](reference/annual-flow.md), persist progress after every turn, and generate the workpack only after the explicit confirmation phrase below.

## Path resolution

Bundled paths (`reference/`, `templates/`, `_shared/`) are relative to this skill's own directory; `_shared/` is `../_shared/`. Resolve bundled files with host file tools (`Read` first, `Glob` or `Grep` if a path is not obvious). Do not use Bash to discover or read plugin files: in Cowork, shell commands run in an isolated VM that may not see the plugin cache even when `Read` and `Glob` can. If the host has already expanded `${CLAUDE_PLUGIN_ROOT}` or `${CLAUDE_SKILL_DIR}`, those absolute paths are fine for file tools; otherwise search within the loaded plugin/skill tree and resolve relative to this skill directory. Resolve every `workspace/...` path against `workspace_root` from `session-progress.yaml` (or `profile.yaml`); never create a second `workspace/` tree.

Safety: only run Python under an already-resolved plugin `skills/.../scripts/` path (this skill runs the bundled `nl-tax-field-mapper/scripts/validate_field_map.py`), and only if Bash can access that path. When a script takes a workspace file as an argument (e.g. the field-map validator), the same shell must also see the workspace path — translate `workspace_root` to the path the shell actually mounts (in Cowork the working folder, not the host path) before invoking, and if script and workspace file are not co-visible from one shell, use the manual fallback instead. If Bash cannot see the plugin path, perform the equivalent validation manually against `nl-tax-field-mapper/reference/mapping-principles.md` (read it with the file tools); never copy bundled scripts into `workspace/`. Never execute a `.py` located under `workspace/`, `uploads/`, or `evidence/`.

## Read first

Two different read cadences apply. Record every loaded knowledge file's `source_id` (from `_shared/source-register.yaml`) in the top-level `sources_loaded` list in `session-progress.yaml` — add each ID once, the first time its file is loaded; never append duplicates. Only those IDs may appear in the workpack's "Sources used" section.

**Workspace state — re-read before the first user-facing reply on every turn** (it may have changed since the last turn):

1. `workspace/taxpayer/profile.yaml`
2. `workspace/shared/session-progress.yaml`
3. `workspace/taxpayer/evidence-index.yaml` if it exists

**Bundled references — load once when this skill becomes active**, and re-read them only when resuming a session from disk or when a self-check needs the exact wording (they do not change mid-conversation; keeping them loaded in context satisfies this rule):

1. `reference/annual-flow.md` — the 14 numbered phases this skill follows
2. `reference/annual-output-contract.md` — the structural and safety rules for the workpack
3. `templates/annual-return-pack.md` — the workpack template

Before generating content for a phase (Phase 2 onward in `annual-flow.md`), load the 2025 rate sheets that phase relies on — each sheet once, when its phase first needs it, re-read on resume. These are canonical for every numeric line the workpack will reference — do not paraphrase rates from memory or from an earlier paraphrase.

- `_shared/knowledge/years/2025/annual/box1-rates.md`
- `_shared/knowledge/years/2025/annual/credits.md`
- `_shared/knowledge/years/2025/annual/own-home.md`
- `_shared/knowledge/years/2025/annual/deductions.md`
- `_shared/knowledge/years/2025/annual/late-filing.md`
- `_shared/knowledge/years/2025/annual/filing-flow.md`
- `_shared/knowledge/years/2025/annual/evidence-checklist.md`
- `_shared/knowledge/years/2025/entrepreneur/ondernemer-criteria.md` (only when the case has winst uit onderneming — `business.has_onderneming` value `true` in the profile)
- `_shared/knowledge/years/2025/entrepreneur/ondernemersaftrek.md` (same condition)
- `_shared/knowledge/years/2025/entrepreneur/mkb-winstvrijstelling.md` (same condition)
- `_shared/knowledge/years/2025/entrepreneur/investeringsaftrek.md` (same condition)
- `_shared/knowledge/years/2025/entrepreneur/winst-en-kosten.md` (same condition)
- `_shared/knowledge/years/2025/entrepreneur/entrepreneur-aangifte.md` (same condition)
- `_shared/knowledge/years/2025/box3/fictitious.md`
- `_shared/knowledge/years/2025/box3/actual-return.md`
- `_shared/knowledge/years/2025/box2/box2-rates.md` (only when the case has an aanmerkelijk belang — `box2.has_aanmerkelijk_belang` value `true` in the profile)
- `_shared/knowledge/years/2025/box2/box2-income-guidance.md` (same condition)
- `_shared/knowledge/years/2025/box2/fisin-aanmerkelijk-belang.md` (same condition)
- `_shared/knowledge/own-home/eigenwoningforfait.md`
- `_shared/knowledge/own-home/hypotheekrenteaftrek.md`
- `_shared/knowledge/partners/fiscal-partnership.md`

If a rate sheet fails to load, stop and tell the user — do not fabricate a rate.

**Source-pack staleness check (warn, don't block):** the first time knowledge files are loaded in a session, compare each loaded source's `last_checked` in `_shared/source-register.yaml` against its `freshness_policy` cadence and today's date. If any source required by this workflow is past its cadence, tell the user once, in one sentence, that the source pack may be stale (name the stale `source_id`s) and that the values should be double-checked in Mijn Belastingdienst before filing. Staleness never blocks workpack generation; list the stale `source_id`s in the workpack's Human review checklist instead.

Confirm `workflow_candidate: annual_2025`. If the profile is missing or the workflow is unsupported, hand control back to `nl-tax-intake`.

## Resume guard

`session-progress.yaml` is the resume contract. Before doing any work:

- If `session-progress.yaml` is missing or empty, reconstruct it from `profile.yaml` and `_shared/templates/session-progress.yaml` before proceeding.
- If `profile.yaml` shows `intake_status: complete`, never restart intake — continue the annual workflow from recorded progress.
- Skip any subsection already marked `complete`, `chat_only`, or `deferred` in `session-progress.yaml`.

## Workflow

`reference/annual-flow.md` is authoritative. It defines 14 phases (Pre-flight → Filing status → Income → Winst uit onderneming → Own home → Box 2 → Box 3 → Deductions → Credits screening → Partner → Field map → Missing info → Review questions → Assembly; numbered 1, 1.5, 2, 2A, 3, 3A, 4, 5, 5.5, 6, 7, 8, 9, 10 there). Follow them in order, and within each phase apply the conversational contract below.

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
- **Winst uit onderneming** → `nl-tax-winst` (writes `workspace/shared/winst-notes.md`, `workspace/shared/winst-open-questions.yaml`, and `workspace/shared/winst-review-questions.md`). Only when the case has winst uit onderneming (`business.has_onderneming` value `true`): load the six entrepreneur rate sheets listed above first, and — because helpers never update `session-progress.yaml` (this skill owns session state) — this skill MUST append `bd_ondernemer_criteria_2025`, `bd_ondernemerscheck_2025`, `bd_urencriterium_2025`, `bd_ondernemersaftrek_2025`, `bd_zelfstandigenaftrek_2025`, `bd_startersaftrek_ao_2025`, `bd_startersaftrek_2025`, `bd_meewerkaftrek_2025`, `bd_stakingsaftrek_2025`, `bd_so_aftrek_2025`, `bd_mkb_winstvrijstelling_2025`, `bd_kia_2025`, `bd_eia_2025`, `bd_eia_mia_vamil_2025`, `bd_zakelijke_kosten_2025`, `bd_beperkt_aftrekbare_kosten_2025`, `bd_werkruimte_2025`, `bd_privevervoermiddel_2025`, `bd_oudedagsreserve_2025`, `bd_administratie_bewaren_2025`, `bd_aangifte_ondernemers_2025`, `bd_ondernemer_cijfers_aangifte_2025`, and `bd_ondernemer_voorbereiden_2025` to `session-progress.yaml` → `sources_loaded` as their notes are loaded, so the workpack's Sources Used section matches the winst facts it cites.
- **Box 2** → `nl-tax-box2` (writes `workspace/shared/box2-notes.md`, `workspace/shared/box2-open-questions.yaml`, and `workspace/shared/box2-review-questions.md`). Only when the case has a real Box 2 position (`box2.has_aanmerkelijk_belang` value `true`): load the three box 2 rate sheets listed above first, and — because helpers never update `session-progress.yaml` (this skill owns session state) — this skill MUST append `bd_box2_rates_2025_2026`, `bd_box2_income_ab_guidance`, and `bd_fisin_aanmerkelijk_belang_2025` to `session-progress.yaml` → `sources_loaded`, so the workpack's Sources Used section matches the Box 2 facts it cites.
- **Box 3** → `nl-tax-box3` (writes `workspace/shared/box3-notes.md`, `workspace/shared/box3-open-questions.yaml`, and `workspace/shared/box3-review-questions.md`; annual collects fictitious **and** werkelijk rendement for the comparison)
- **Partner / deductions** → `nl-tax-partner-deductions` (writes `workspace/shared/allocation-options.md`, `workspace/shared/partner-deductions-open-questions.yaml`, and `workspace/shared/partner-deduction-review-questions.md`)

Read `workspace/shared/box2-notes.md`, `workspace/shared/box2-open-questions.yaml`, and `workspace/shared/box2-review-questions.md` back before assembling the Box 2 section (the review questions feed the Human review checklist). Read `workspace/shared/winst-notes.md`, `workspace/shared/winst-open-questions.yaml`, and `workspace/shared/winst-review-questions.md` back before assembling the Winst uit onderneming section. Read the sibling helpers' named notes/open-question artifacts back before assembling their sections. The helpers never write to `workspace/annual/**`; this skill owns that tree.

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
3. Winst uit onderneming — ondernemer status, urencriterium, winst, ondernemersaftrek, MKB-winstvrijstelling, investeringsaftrek (only when the taxpayer has an eenmanszaak / ZZP), or "not applicable"
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
- `workspace/shared/missing-info.md` (seed from `_shared/templates/missing-info.md` on first write)
- `workspace/shared/assumptions.md` (seed from `_shared/templates/assumptions.md` on first write)

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
