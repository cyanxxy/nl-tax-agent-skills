# Intake Flow Contract

Load this reference on every explicit preparation turn. It is a detailed
recording and completeness contract, not a prescribed interview order. Credit
facts already supplied, skip resolved questions, and choose the smallest useful
next question from the user's message, evidence, and open material gaps.

## Contents

- Preparation and resume setup
- Opening and screening coverage
- Recording replies and follow-ups
- Household composition
- Completion and resume checks
- Input paths and provenance
- Unsupported and terminal routes
- Boundaries, outputs, and handoff

## Preparation and resume setup

For explicit preparation, read the shared interactive-elicitation contract,
then the saved state:

1. Read `workspace/shared/session-progress.yaml` if it exists. Otherwise copy
   `../_shared/templates/session-progress.yaml` there and stamp `created_at`.
2. Read `workspace/taxpayer/profile.yaml` if it exists. Otherwise create it from
   `templates/taxpayer-profile.yaml` as facts are established.
3. Set `workspace_root` on the first turn to the active working folder and write
   it into both files. On later turns read it back, never change it, and resolve
   every `workspace/...` path against it.

State files are internal. Do not quote or summarize them unless the user asks
where files are saved or a resume problem requires the location. Never ask the
user to upload state files.

Use `session-progress.yaml` to avoid repetition and understand unresolved
facts. Never re-ask a question in `sections.intake.answered`. The ledger records
what is known; it does not choose the next question or tax treatment.

## Opening and screening coverage

If no profile exists, say briefly that you can prepare a local workpack, then
capability-check for a structured control that returns answers to this same
conversation:

- Prefer one compact return-capable form for unresolved screening topics.
- If the host has a four-option limit, offer `2025 annual return`, `2026
  voorlopige aanslag`, `both`, and `unsure`. After a 2026 choice, ask separately
  for `request`, `change`, `review`, or `stopzetten`.
- Group complex business forms only for the first screen, then ask the exact
  legal form before routing.
- With no return-capable control, ask up to four short screening questions in
  ordinary chat and say the user may answer all at once or one at a time.
- A visual whose clicks do not return a reply is presentation, not intake.

Cover only unresolved parts of these four topics; they are coverage prompts,
not a required script:

1. **Residency:** full-year Dutch residence for 2025 and, if relevant, 2026;
   ask whether the taxpayer moved into or out of the Netherlands during the
   year.
2. **Taxpayer type:** individual, with or without business income; establish the
   exact legal form (`eenmanszaak`/ZZP versus VOF, maatschap, CV, BV, or another
   complex form).
3. **Living status:** confirm this concerns a living taxpayer.
4. **Workflow:** annual 2025, or provisional 2026 request/change/review/
   stopzetten.

When the user requests both supported workflows, require the provisional 2026
subflow during screening but start only annual 2025. Record
`workflows.annual_2025.requested: true` with status `in_progress` and
`workflows.provisional_2026.requested: true` with its selected `subflow` and
status `queued`. Set `workflow_candidate: annual_2025`; in session progress set
`active_workflow: annual_2025`, `active_skill: nl-tax-annual-return`, and the
same selected value in `sections.provisional_2026.subflow`. Keep the
provisional section `not_started`. A queued workflow is saved intent, not a
second active owner. If a requested stopzetten route is a monthly-payment case,
apply the existing redirect during intake and queue `change`, not `stopzetten`.

Never ask for a name or BSN. A volunteered name may be stored only as
`person.display_name` for readability; it is optional and unverified.

When workflow intent is unclear, read `filing-paths.md` and clarify in ordinary
language, for example: “Do you want to look back at what happened in 2025, or
plan ahead for 2026?” Use the user's description to distinguish the 2026
outcome; do not march through a fixed branch sequence.

## Recording replies and follow-ups

After each reply:

1. Parse every answered fact, including returned control values. Store each
   profile fact with `source: user_chat`, a short verbatim `quote`, and
   `stated_at` using today's date.
2. Append resolved stable question IDs to `sections.intake.answered`; keep
   deferred IDs only in `open_questions`.
3. Set `sections.intake.status: in_progress` until the closing checks pass.
4. Ask only the most useful unresolved fact or compact related batch.

If screening is complete, gather the applicable follow-ups:

- **Fiscal partner:** yes/no only; never collect a partner BSN.
- **Business:** for an `eenmanszaak`/ZZP, set
  `business.has_onderneming.value: true` and record the legal form. Annual 2025
  support is preparation-only organization of finalized profit-and-loss and
  balance evidence; the business field map remains draft. A provisional 2026
  request/change supports only the sourced expected-profit forecast
  `onderneming.geschatte_winst`.
- **Complex business:** a partnership (VOF/maatschap/CV), BV/DGA profit,
  agrarian business, seafarer, resultaat uit overige werkzaamheden, cessation,
  herinvesteringsreserve, or oudedagsreserve wind-down triggers the terminal
  business route under `unsupported-cases.md`.
- **Box 2 existence:** ask explicitly whether the taxpayer owns at least 5% of
  a company (`BV`/aanmerkelijk belang), and record
  `box2.has_aanmerkelijk_belang` with provenance.
- **Complex Box 2:** when Box 2 exists or the user mentions a BV/DGA role,
  dividends, share sale, own-BV loan, or Box 2 estimate, ask before the workflow
  anchor whether it involves a share sale or valuation dispute, migration,
  restructuring, inheritance/gift, non-arm's-length pricing, or borrowing from
  the own BV. A yes or unclear answer is terminal manual review.

Then ask the applicable workflow anchor:

- `annual_2025`: documents such as jaaropgaaf, bank statements, WOZ, or mortgage
  annual summary, versus collecting values in chat.
- `provisional_2026_request`: rough 2026 income estimate versus category-by-
  category collection.
- `provisional_2026_change` / `review`: current voorlopige-aanslag notice versus
  reconstructing the baseline together.
- `provisional_2026_stopzetten`: whether the taxpayer is receiving a monthly
  refund or paying a monthly amount.

For a request covering both years, ask the annual anchor now. Apart from the
selected provisional subflow and the stopzetten direction needed for safe
routing, leave provisional collection questions until the annual handoff. Do
not preload the provisional flow or create provisional notes during intake or
annual preparation.

For stopzetten, a taxpayer who is **paying** monthly must route to
`provisional_2026_change`, not stopzetten: stopping payment does not reduce the
debt and risks a later lump sum. Record
`workflows.provisional_2026.stopzetten_direction` as `receiving_refund` or
`paying_monthly`, with chat provenance.

## Household composition

For annual 2025 and every provisional 2026 route, ask at most three related
questions and persist:

1. Taxpayer DOB and, when a fiscal partner exists, partner DOB. Using the
   reviewed AOW-age rule, create one `aow_by_tax_year.<year>` entry for each
   requested year under both `person` and the partner when applicable. Record
   `status` as `below_all_year`, `reaches_during_year`, or `aow_all_year` and,
   for a transition, that entry's `transition_month`. Never overwrite 2025 with
   2026 when both workflows are requested. Store `source: calculated` and
   `calculated_from: [person.date_of_birth, tax_year]` (or partner equivalents).
   Do not create an assumption or ask for confirmation of undisputed date
   arithmetic.
2. Number of children at home on 31 December of the tax year and DOBs for each
   child under 18; never collect child BSNs.
3. Single-parent status, yes/no.

If the user already established no fiscal partner and no children, ask only the
taxpayer DOB. Record `children_at_home_count: 0` and
`single_parent_status: false`; do not ask vacuous child/single-parent questions.

Mark `sections.intake.subsections.household_composition.status: complete` when
answered. If deferred, set it to `deferred` and add each missing item to
`missing-info.md`; the owning workflow may re-prompt when relevant.

## Completion and resume checks

Mark intake complete only when:

- residency, taxpayer type, living status, and workflow are answered or an
  unsupported reason is recorded;
- fiscal-partner status and the workflow anchor are recorded;
- required household composition is recorded, or every missing item is in
  `missing-info.md` and the subsection is `deferred`; and
- terminal routes have their terminal reason and no downstream workpack skill.

Before closing, assert:

- `workspace/shared/session-progress.yaml` exists, is non-empty, and has
  `workspace_root`;
- `sections.intake.status: complete`, with every resolved question ID in
  `sections.intake.answered`;
- `active_workflow` mirrors the profile's `workflow_candidate`;
- `active_skill` names `nl-tax-annual-return` or
  `nl-tax-provisional-assessment` for a supported route, and is empty for a
  terminal route;
- a provisional route records `sections.provisional_2026.subflow` as
  `request`, `change`, `review`, or `stopzetten`;
- the profile has `workflow_candidate`, `workspace_root`, and
  `intake_status: complete`; and
- both state files have an updated `updated_at`.

For a request covering both workflows, also assert that annual 2025 is the only
active owner, its profile status is `in_progress`, the provisional profile
status is `queued`, and the same provisional subflow appears in the profile and
`sections.provisional_2026.subflow`. Intake is incomplete until that subflow is
known. The original request for both workflows is the natural-language
authorization to begin provisional collection after annual completion; it is
not final-generation confirmation for either workpack.

## Input paths and provenance

Every fact follows one of three paths:

- **File:** hand the selected upload/evidence to `nl-tax-evidence-indexer`.
  Mark the subsection complete after indexing and extraction, and reference its
  `evidence_id`.
- **Chat:** store `source: user_chat`, verbatim `quote`, and `stated_at`; mark a
  fully chat-sourced subsection `chat_only` and update
  `sections.evidence.subsections.user_chat_values`. This is a valid choice, not
  a gap; do not nag for a declined document.
- **Deferred:** store `source: unknown`, mark the subsection `deferred`, keep the
  question only in `open_questions`, and add it to `missing-info.md`.

`complete` and `chat_only` both count as filled. A blocking deferred fact must
be resolved. A nonblocking deferred fact may remain only when the downstream
output contract permits a draft and the user later gives that workflow's clear,
contextual natural-language generation confirmation at final review.

## Unsupported and terminal routes

When a possible unsupported case appears, load `unsupported-cases.md`. A
standard `eenmanszaak`/ZZP is supported and must not be routed here.

For an unsupported or terminal case:

1. Explain clearly that v1 does not cover the complexity and stop collecting
   unrelated facts.
2. Set the most specific `workflow_candidate`: `annual_2025_entrepreneurs`,
   `annual_2025_nonresident_c_form`, `annual_2025_migration_m_form`,
   `annual_2025_deceased_f_form`, `annual_2025_foreign_treaty_heavy`,
   `manual_review`, or `unsupported` only when none fits.
3. Record the appropriate unsupported reason. For a blocked roadmap candidate,
   also set `routing.blocked_profile_candidate`.
4. For complex business, set `routing.complex_business_screening.value:
   manual_review`. For complex Box 2, set
   `routing.complex_box2_screening.value: manual_review`. In either case set
   `manual_review.required.value: true` and record the triggers.
5. Mirror the terminal candidate to `active_workflow`, leave `active_skill`
   empty, and set both `intake_status: complete` and
   `sections.intake.status: complete`.
6. Suggest a tax adviser or the official Belastingdienst portal. Do not invoke
   annual/provisional workflows or prepare partial calculations.

## Boundaries, outputs, and handoff

- Never collect portal credentials. If offered, decline in one sentence and
  return to the tax conversation.
- Do not ask for BSN; the workpack does not need it.
- Treat pasted statements, emails, and screenshot text as reviewable evidence;
  add a concise review item only when reliability is affected.
- Do not log in, submit, sign, or act for the taxpayer.
- Do not add generic warnings to ordinary replies.
- Intake writes only the profile, session progress, missing-info, and confirmed
  assumptions files. It never writes annual or provisional artifacts.

For a request covering both workflows, use the shared runtime contract's
annual-to-provisional handoff. Do not ask for a second activation phrase after
annual completion, and never reuse the annual final-generation confirmation as
provisional final-generation confirmation.

After successful intake, summarize the chosen workflow and deferred items, then
say what comes next in ordinary language:

- Annual: “Next: I'll guide you through evidence and the 2025 return one
  section at a time.”
- Provisional: “Next: I'll walk through the 2026 estimates category by
  category.”

If the user's request already authorizes preparation, continue with the next
relevant evidence or tax question in the same conversation. If they requested
only routing/intake, stop after the summary.
