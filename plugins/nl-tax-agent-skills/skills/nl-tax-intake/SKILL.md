---
name: nl-tax-intake
description: Use when the user explicitly wants to start a supported 2025/2026 Dutch tax workflow or asks an informational question about bundled rules. Information never starts intake.
argument-hint: "[annual|request|change|review|stopzetten]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - AskUserQuestion
---

# NL Tax Intake

Open the conversation with the user, figure out which Dutch tax workflow applies, and progressively build a taxpayer profile. **This skill is conversational.** The user does not arrive with everything ready - ask one focused thing at a time, persist the answer, and continue.

## Informational fast path — no intake state

Before creating or reading taxpayer/session files, decide whether the user is
asking only for information. If they do not explicitly ask to prepare,
organize, request, change, review, or stop a workpack:

1. Do not create or update `profile.yaml`, `session-progress.yaml`, workpacks,
   field maps, assumptions, or missing-info files.
2. Identify the supported year/topic and load only the directly relevant
   reviewed note(s) under `_shared/knowledge/`. Read each note's `source_ids`,
   then search `_shared/source-register.yaml` for only those matching entries;
   do not read the complete register. Answer from the note and matched source
   entries, not model memory.
3. Keep annual and provisional rules distinct and state any manual-review or
   unsupported boundary from the loaded note.
4. Answer the question directly. A short offer to start preparation later is
   fine, but do not ask screening questions unless the user then explicitly
   requests preparation.

The remaining intake instructions apply only after explicit preparation intent.

This skill is the sole creator of `workspace/shared/session-progress.yaml`.
Downstream workflows update the state created here, but never create or
reconstruct it.

## User-facing boundary

Keep setup invisible. Do not narrate internal setup steps such as skill selection, rule or template loading, path resolution, local state-file creation, YAML updates, or policy loading. Create and update local files silently. Do not proactively recite generic warnings. The first user-facing reply should say only that you prepare a local workpack and then present the screening questions, preferably through a return-capable structured-input control. If the workflow is already clear and the user has documents ready, ask them to upload the relevant tax files; do not ask them to upload workspace or state files.

Python is optional at runtime. Do not ask the taxpayer to install Python. The
agent owns intake and applies the documented checks directly; optional scripts
may only accelerate mechanical checks when the host already supports them.

## When to use

- User wants to file a Dutch income tax return
- User wants to request, change, review, or stop a voorlopige aanslag
- User asks an informational question about a bundled annual-2025 or
  provisional-2026 rule; use the fast path and create no state
- First contact for any Dutch tax preparation task

## Read first (every turn)

Bundled paths below are relative to this skill's own directory: `templates/`
is a subfolder, and `_shared/` is the plugin-shared folder at `../_shared/`.
Read `../_shared/runtime-contract.md` first. Resolve bundled files relative to
this skill directory with the host's skill-resource or file tools. Do not
depend on shell visibility or vendor-specific environment variables.

For explicit preparation only, before responding to the user, read:

1. `_shared/knowledge/methods/interactive-elicitation.md` - the conversational contract this skill follows.
2. `reference/filing-paths.md` - intent-based workflow disambiguation and the request / change / review / stopzetten decision tree. Use it whenever the user is unsure which workflow they want, or does not recognize the jargon in screening question 4.
3. `workspace/shared/session-progress.yaml` if it exists. If it does not, copy `_shared/templates/session-progress.yaml` to that path and stamp `created_at`.
4. `workspace/taxpayer/profile.yaml` if it exists. Otherwise prepare to create it from `templates/taxpayer-profile.yaml`.

Items 3-4 are internal rules. Do not quote or summarize them to the user unless
the user offers credentials, asks for login/submission help, or a specific
uploaded item needs review.

Use `session-progress.yaml` to decide what to ask next. Never re-ask a question already in `sections.intake.answered`.

## Workspace location

All `workspace/...` paths must resolve to one working folder that stays
constant across every turn and every resumed session. On the first turn, set
`workspace_root` to the absolute path of that folder and write it into both
`workspace/shared/session-progress.yaml` and `workspace/taxpayer/profile.yaml`.
On every later turn, read `workspace_root` back and resolve all `workspace/...`
paths against it. Once set, never change it and never create a second
`workspace/` tree. See the **Workspace root** section of
`_shared/knowledge/methods/interactive-elicitation.md` for the full contract.

Do not volunteer the folder path in the opening message. State the storage
location only when the user asks where files are saved or when a later resume
problem requires it. A later session relies entirely on finding `profile.yaml`
and `session-progress.yaml`; if the host is pointed somewhere else, the resume
guard cannot fire and intake will wrongly restart.

## What this skill produces

Across one or more turns of conversation:

1. `workspace/taxpayer/profile.yaml` - incrementally filled as the user answers
2. `workspace/shared/session-progress.yaml` - updated every turn
3. `workspace/shared/missing-info.md` - items the user could not yet provide
4. `workspace/shared/assumptions.md` - confirmed assumptions, if any

## Conversation flow

### Turn 1 - open warmly, then ask the first screening batch

If `workspace/taxpayer/profile.yaml` does not exist, briefly explain what you'll
do (prepare a local workpack), then capability-check for a structured-input
control that returns answers to this same conversation:

- **Return-capable control available:** prefer one compact form for the four
  screening topics below. A richer form may use separate controls for
  individual filing and business legal form. Use native selects, radios, or the
  host's multiple-choice question tool; label every control. The submitted
  values must return as a user reply before anything is recorded.
- **Claude chat or Cowork:** first try Claude's native interactive inputs. Do
  not build a custom HTML visual for Cowork intake because visual clicks may not
  return a follow-up reply. `AskUserQuestion` is a documented Claude Code tool,
  not a guaranteed Cowork API; if Cowork presents no native input, use chat.
- **Claude Code:** use `AskUserQuestion` when available and apply the bounded
  choice split below.
- **Codex:** use a native input control or inline form only when submission
  creates a follow-up message in this same task.
- **Control has a four-option limit:** use `2025 annual return`, `2026
  voorlopige aanslag`, `both`, and `unsure` for the workflow question. If the
  user chooses 2026, ask a second four-choice control for `request`, `change`,
  `review`, or `stopzetten`. Group complex business forms only for the first
  screen, then ask the exact legal form before routing.
- **No return-capable control:** ask up to **four short screening questions** in
  one ordinary chat message. Do not use a display-only visual. In particular,
  a custom visual whose clicks cannot create a follow-up reply is presentation,
  not intake.

Use these screening topics and distinctions in either presentation:

1. **Residency** - Were you a Dutch resident for the *full* of 2025 (and, if relevant, 2026)? Did you move to or from the Netherlands at any point during the year? (A mid-year move usually means an M-aangifte, which v1 does not cover -- see `reference/unsupported-cases.md` #1/#5.)
2. **Taxpayer type** - Are you filing as an individual? Do you have income from your own business, and if so what legal form (eenmanszaak / ZZP, or a VOF / maatschap / BV)? (An eenmanszaak / ZZP is supported; partnerships and BVs route to a specialist.)
3. **Living status** - Is this for a living taxpayer?
4. **Workflow** - What do you want help with: the annual 2025 return, or a 2026 voorlopige aanslag (request / change / review / stopzetten)?

In the chat fallback, tell the user they can answer all at once or one at a
time. Never ask for names or BSN. If the user volunteers a name, you may store
it in `person.display_name` as a plain label for readability; it is never
required and never verified.

**If the user is unsure about question 4** (the voorlopige-aanslag terms are jargon most people do not use, and many confuse *voorlopige aanslag* with *voorlopige teruggaaf* or just say "I get/pay money monthly"): do NOT repeat the jargon list. Read `reference/filing-paths.md` and disambiguate by intent -- ask "Do you want to look back at what happened in 2025, or plan ahead for 2026?" -- then narrow the 2026 case using the request / change / review / stopzetten decision tree in that file.

### Turn 2+ - record, then continue

After each user reply:

1. Parse out everything the user answered, including values returned by a
   structured-input control. For each value, record it in
   `workspace/taxpayer/profile.yaml` with `source: user_chat`, a short verbatim
   `quote`, and `stated_at` (today's date).
2. Append the answered `question_id`s to `sections.intake.answered` in `session-progress.yaml`.
3. Update `sections.intake.status` to `in_progress`.
4. Decide the next thing to ask:
   - If any of the four screening answers are still missing, ask only those.
   - If the case is unsupported or terminal manual review (see below), say so clearly, close intake as terminal, and stop.
   - If the workflow is identified, ask a short batch of follow-ups:
     - **Fiscal partner?** Yes / no. If yes, do NOT collect partner BSN - only whether a partner exists.
     - **Winst uit onderneming + business-form screen:** If the user reports income from an **eenmanszaak / ZZP**, set `business.has_onderneming.value: true` and record the legal form. For `annual_2025`, continue only to preparation-only organization of finalized profit-and-loss and balance evidence; the business field map remains draft. For a `provisional_2026_request` or `provisional_2026_change`, continue only to the sourced expected-profit forecast `onderneming.geschatte_winst`. If the form is a **partnership (VOF / maatschap / CV), a BV / DGA-winst, an agrarische onderneming, or the taxpayer is a zeevarende**, if the income looks like **resultaat uit overige werkzaamheden**, or if the case involves staking/cessation, herinvesteringsreserve, or oudedagsreserve wind-down: record `routing.complex_business_screening.value: manual_review`, set `manual_review.required.value: true`, record the trigger(s), use the most specific blocked candidate or `manual_review`, complete intake, mirror the terminal candidate into `active_workflow`, leave `active_skill` empty, and stop.
     - **Box 2 existence + early complex Box 2 screen:** Ask one explicit yes/no rather than waiting for the user to volunteer jargon: "Do you own 5% or more of a company (a BV / aanmerkelijk belang)?" Record the yes/no answer in `box2.has_aanmerkelijk_belang` with provenance. If yes -- or if the user mentions a BV, DGA role, aanmerkelijk belang, dividends, a share sale, an own BV loan, or a Box 2 estimate -- ask before the workflow-specific anchor: "Does the Box 2 situation involve a share sale or valuation dispute, emigration/immigration, restructuring, inheritance or gift, non-arm's-length pricing, or borrowing from your own BV?" If yes or unclear, record `routing.complex_box2_screening.value: manual_review`, set `manual_review.required.value: true`, record the trigger(s), set `workflow_candidate: manual_review`, set `intake_status: complete`, set `sections.intake.status: complete`, set `active_workflow: manual_review`, leave `active_skill` empty, and stop. `manual_review` is terminal: do not call annual/provisional workflows and do not leave it as an unknown workflow candidate.
     - **Workflow-specific anchor:**
       - `annual_2025` -> "Do you already have any documents (jaaropgaaf, bankafschriften, WOZ, mortgage jaaroverzicht), or shall we collect amounts step by step in chat?"
       - `provisional_2026_request` -> "Do you have a rough estimate of your 2026 income, or do you want me to ask category by category?"
       - `provisional_2026_change` / `review` -> "Do you have your current voorlopige aanslag beschikking handy, or shall we reconstruct the baseline together?"
       - `provisional_2026_stopzetten` -> "Are you currently RECEIVING a monthly refund (teruggaaf) or PAYING a monthly amount?"

     **Stopzetten routing consequence (apply at intake, where the answer is first captured):** if the user is PAYING a monthly amount (not receiving a refund), do NOT set `workflow_candidate: provisional_2026_stopzetten`. Stopzetten only applies to a refund; stopping payments does not reduce the debt and risks a lump-sum bill at annual time. Explain this and set `workflow_candidate: provisional_2026_change` instead. Record the refund-vs-paying direction either way in `profile.yaml` → `workflows.provisional_2026.stopzetten_direction` (value `receiving_refund` or `paying_monthly`, with `source`/`quote`/`stated_at` provenance) so the downstream skill has it.

### Household composition (before closing intake)

If the workflow is `annual_2025` or any `provisional_2026_*` flow, also collect household composition. The annual workpack's credits screening (IACK, ouderenkorting, alleenstaande-ouderenkorting, jonggehandicaptenkorting) depends on these facts. Ask in a single batch of **at most 3 questions**, persisting each answer to `profile.yaml` -> `person`, `partner`, and `household`:

1. **Date of birth** of the taxpayer (and of the fiscal partner if one exists). Persist to `person.date_of_birth` and `partner.partner_date_of_birth`. Using the reviewed AOW-age rule for the tax year, derive `aow_age_in_tax_year` deterministically from the DOB. Store it with `source: calculated` and `calculated_from: [person.date_of_birth, tax_year]` (or the partner equivalents). Do not create an assumption or ask the user to confirm the calculation; ask only if the DOB itself is missing or disputed.
2. **Children at home on 31 December of the tax year**: count and, for any child under 18, their date of birth (DOBs only -- never BSN). Persist to `household.children_at_home_count` and `household.children`.
3. **Single-parent status**: yes / no. Persist to `household.single_parent_status`.

Short-circuit: if the user has already stated they have **no fiscal partner and no children**, you only need the taxpayer's date of birth (for AOW-age derivation). Skip the children-DOB and single-parent questions -- they are vacuously answered (`children_at_home_count: 0`, `single_parent_status: false`). Only ask the children/single-parent questions when a partner or any child has been mentioned.

Mark `sections.intake.subsections.household_composition.status: complete` in `session-progress.yaml` once these are answered. If the user defers, mark `status: deferred` and add the items to `missing-info.md` -- the annual workflow will re-prompt in Phase 1.7.

### Closing the intake section

Mark `sections.intake.status: complete` only when:

- Residency, taxpayer type, living status, and workflow are all answered or recorded as `unsupported_reason`.
- Fiscal-partner status is recorded.
- The workflow-specific anchor question is answered.
- Household composition (DOB taxpayer + partner if applicable, children at home, single-parent status) is recorded for `annual_2025` and provisional flows -- or each missing item is in `missing-info.md` and the corresponding subsection is `deferred`.
- For terminal routes (`manual_review`, `unsupported`, or a blocked `annual_2025_*` profile candidate), the terminal reason is recorded and no annual/provisional workpack skill is selected.

Before closing intake, assert the resume contract holds. A resuming agent
relies entirely on these files; if they are not populated it will wrongly
restart intake:

- `workspace/shared/session-progress.yaml` exists, is non-empty, and has `workspace_root` set.
- `sections.intake.status` is `complete` and every answered `question_id` is in `sections.intake.answered`.
- `session-progress.yaml` is self-describing: set `active_workflow` to the chosen `workflow_candidate`, set `active_skill` to the skill that runs next (e.g. `nl-tax-annual-return` or `nl-tax-provisional-assessment`), and for a provisional flow set `sections.provisional_2026.subflow` to `request`/`change`/`review`/`stopzetten`. For terminal routes, set `active_workflow` to the terminal candidate and leave `active_skill` empty. `workflow_candidate` in `profile.yaml` remains the source of truth; these fields mirror it so the resume file is not stale.
- `workspace/taxpayer/profile.yaml` has `workflow_candidate` set, `workspace_root` set, and `intake_status: complete`.
- `updated_at` is stamped on both files.

Once complete, write a one-paragraph summary back to the user and describe the next tax topic without naming or narrating a skill handoff:

- `annual_2025` -> "Next: I'll guide you through evidence and the 2025 return one section at a time."
- `provisional_2026_*` -> "Next: I'll walk through the 2026 estimates category by category."

Do NOT auto-invoke the next skill. Wait for the user to continue.

## Three paths for every input

For every fact you record, the user may take one of three paths:

- **Upload a file** to `uploads/` or `evidence/` - hand off to the `nl-tax-evidence-indexer` skill. The corresponding subsection in `session-progress.yaml` becomes `complete` once the file is indexed and the value extracted.
- **State the value in chat only** - record it with `source: user_chat`, a verbatim `quote`, and `stated_at`. Mark the corresponding subsection's `status: chat_only`; also update `sections.evidence.subsections.user_chat_values` as required by the shared elicitation contract. This is an explicit choice, not a gap; do not nag for a file the user has declined to upload.
- **Defer ("I'll send it later")** - record `source: unknown`, mark the subsection's `status: deferred`, keep the question in `open_questions` rather than `answered`, add the item to `missing-info.md`, and move on. The annual/provisional conversation will re-prompt when relevant.

`chat_only` and `complete` both count as filled for the workpack generation
gate. A deferred blocking fact must be resolved. A nonblocking deferred fact may
remain only when the downstream output contract permits a `DRAFT` and the user
later gives that workflow's explicit generation confirmation.

## Unsupported cases

Read `reference/unsupported-cases.md`. If you detect an unsupported case (part-year resident, a complex business form, deceased taxpayer, M-biljet required, etc.) — note that a standard eenmanszaak / ZZP is supported and is NOT an unsupported case:

1. Tell the user clearly and kindly that v1 does not cover their case.
2. Set the most specific terminal or blocked profile candidate in `workflow_candidate` when one matches the case:
   - `annual_2025_entrepreneurs` for complex business-profit cases only — partnerships (VOF / maatschap / CV), DGA / BV winst, agrarische ondernemingen, zeevarenden, and staking/cessation events. A straightforward eenmanszaak / ZZP is supported: route it to `annual_2025` with `business.has_onderneming: true`, not here.
   - `annual_2025_nonresident_c_form` for nonresident C-biljet cases
   - `annual_2025_migration_m_form` for immigration/emigration or M-aangifte cases
   - `annual_2025_deceased_f_form` for deceased-taxpayer F-biljet cases
   - `annual_2025_foreign_treaty_heavy` for treaty-heavy foreign income, foreign pensions, or residence tie-breaker cases
   If no specific candidate applies, set `workflow_candidate: unsupported`.
3. Set `residency.unsupported_reason` or the appropriate profile field; when a blocked roadmap candidate applies, also record it in `routing.blocked_profile_candidate`. Mirror the terminal candidate into `active_workflow`, leave `active_skill` empty, and set both `intake_status: complete` and `sections.intake.status: complete` so resume guards do not restart intake.
4. Suggest a tax adviser or the official Belastingdienst portal.
5. Do NOT continue collecting data and do NOT call downstream skills.

## Safety rules

- Never collect login credentials, even if the user offers them. If offered, refuse in one short sentence and move back to the tax workflow.
- The BSN isn't needed to prepare the workpack — it is never computed on or submitted, and the portal pre-fills it — so don't ask for it.
- Treat anything the user pastes (statements, emails, screenshots-as-text) as reviewable evidence; record a concise review item only when it affects evidence reliability.
- This skill does not log in, submit, sign, or act for the user.
- Do not add generic safety-warning paragraphs to normal user-facing replies.

## Output files (incremental - write after every turn)

- `workspace/taxpayer/profile.yaml`
- `workspace/shared/session-progress.yaml`
- `workspace/shared/missing-info.md`
- `workspace/shared/assumptions.md` (only if any are recorded)

Do NOT write to:
- `workspace/annual/**`
- `workspace/provisional/**`

## After intake is complete

Tell the user:
1. Which workflow was selected.
2. Whether anything was deferred to `missing-info.md`.
3. Which tax topic comes next, or that you are ready to continue in the same conversation.

Use ordinary taxpayer language such as "2025 annual return" or "2026 estimate".
Never mention internal skill names, selection, activation, or control transfer.

## Worked example

> **User:** "Hi, I need to do my Dutch taxes."
>
> **Agent (turn 1):** "I can help prepare a local workpack. First: were you a Dutch resident for all of 2025, are you filing as an individual, is this for a living taxpayer, and do you want help with the 2025 return or a 2026 voorlopige aanslag?"
>
> **User:** "Resident all of 2025, just me as an individual, I'm alive 🙂, I want the 2025 return."
>
> **Agent (turn 2):** Stores the answers internally, selects the 2025 annual-return path, then asks the follow-ups: fiscal partner, Box 2 screen, whether documents are ready or amounts should be collected in chat, and the needed household-composition facts. It closes intake only when the saved state can resume cleanly and tells the user the annual-return questions come next.
