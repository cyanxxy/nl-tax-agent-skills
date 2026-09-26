# Provisional Output Contract — Required Sections and Validation Rules

## Contents

- Purpose
- Where the workpack lives
- Required sections
- Status banner and readiness
- Amount labeling rules
- Winst uit onderneming forecast rule
- Voorlopige aanslag Zorgverzekeringswet -- REQUIRED companion item
- Rollover-trap check -- REQUIRED
- Box 3 validation rule — CRITICAL
- Box 2 validation rule
- Field map requirements
- Change subflow validation rules
- Review subflow validation rules
- Stopzetten validation rules
- Sources used section — REQUIRED
- Not submission advice section — REQUIRED
- Appendix A — Resume record
- Validation checklist

## Purpose

This document defines the mandatory sections, labeling requirements, and validation rules for every provisional assessment workpack, whether it is shown in the conversation or saved. A workpack that violates any rule in this contract is invalid and must not be delivered.

---

## Where the workpack lives

- By default the workpack exists only in the conversation, shown as Markdown
  or on a host surface that creates no file. Presentation never writes:
  creating a downloadable file counts as saving. In chat, render only filled
  sections, with no template fill notes, no bracketed instructions, and no
  Appendix A or Appendix B YAML (the field map appears as its summary table).
- The only file this workflow may write is
  `workspace/nl-tax-provisional-2026-workpack.md`, and only while save consent
  is active in this conversation (a fresh yes, a found file the user confirmed
  resuming, or an attached copy the user agreed to keep saving). Appendix A
  `save_consent` records that decision; it never authorizes a write. Update it
  in place; never create a copy, versioned or dated variant, or second
  `workspace/` tree. A file at that path that the user did not resume is
  replaced only after the replace-or-keep question in the runtime contract,
  never merged into.
- Never write `workspace/nl-tax-annual-2025-workpack.md` or any path other than
  the provisional workpack.
- Section owners inside the one file: this skill writes every section except
  `Field map summary` and `Appendix B — Field map` (written by
  `nl-tax-field-mapper`), the mapper's own gap rows in `Open questions` and
  `Missing information` with their Q-IDs in Appendix A (also written by
  `nl-tax-field-mapper`), and `Manual-entry checklist` (written by
  `nl-tax-submit-companion`). The first save writes everything established so
  far from the facts and provenance recorded in the conversation, and
  otherwise seeds those sections with their template placeholders. An unsaved
  field map is not state: for that save, and at every regeneration,
  `nl-tax-field-mapper` rebuilds the map from the recorded facts and re-runs
  every FM-* check before writing `Field map summary` and Appendix B; a
  checklist already shown is carried over only when each of its values matches
  the rebuilt map, otherwise with the stale line below. After that, this skill
  never edits those sections except to add the stale line.
- Stale outputs: when a sourced fact changes after generation,
  `generation_confirmed` returns to `false`, and this skill adds the line
  `STALE — predates the change to <fact> (<YYYY-MM-DD>); regenerate before
  use.` at the top of `Field map summary`, of Appendix B (above the `yaml`
  block), and of a requested `Manual-entry checklist`, and shows it in the
  conversation. A stale marker is valid only while `generation_confirmed` is
  `false`; regeneration re-runs the mapper, which replaces the stale summary
  and Appendix B.
- For request and change, once mapping has run `Field map summary` is the
  checked surface, in the saved file and in the conversation: every
  `manual_entry` field in Appendix B appears in it with the same value, and
  every `missing_fields` entry appears as a `MISSING - enter manually` row with
  its Q-ID.
- When consent is active and the host has no writable working folder, deliver
  the same workpack through the host's normal file or document output. When the
  working folder may not outlast the session, save there and also deliver a
  download at pauses and at generation. A download at generation is produced
  after mapping, so it includes the map.

---

## Required sections

Every provisional workpack follows `templates/provisional-workpack.md` and
contains these top-level sections in this order:

| Section                     | Required for subflow(s)                   |
|-----------------------------|-------------------------------------------|
| Title + STATUS banner       | all                                       |
| How to use this file        | all                                       |
| Contents                    | all                                       |
| Subflow identifier          | all                                       |
| Scope                       | all                                       |
| Unsupported-case checks     | all                                       |
| Taxpayer profile summary    | all                                       |
| Documents and sources       | all                                       |
| Sources used                | all                                       |
| Existing baseline           | all (may be "No existing baseline" for request) |
| Current-year estimates      | request, change                           |
| Delta summary               | change                                    |
| Review questions            | review                                    |
| Stopzetten outcome          | stopzetten; change reached through the stopzetten payment redirect |
| Income estimate             | request, change                           |
| Winst uit onderneming forecast | request, change                        |
| Own-home estimate           | request, change                           |
| Box 2 provisional estimate  | request, change                           |
| Box 3 provisional estimate  | request, change                           |
| Deductions estimate         | request, change                           |
| Change subflow — full re-entry reminder | change                        |
| Open questions              | all                                       |
| Missing information         | all                                       |
| Assumptions                 | all                                       |
| User-stated values index    | all                                       |
| Field map summary           | request, change (field mapper)            |
| Manual-entry checklist      | all ("not requested" until asked)         |
| Human review checklist      | all                                       |
| Not submission advice       | all                                       |
| Appendix A — Resume record  | all                                       |
| Appendix B — Field map      | all (`not yet mapped` until mapping; review and stopzetten never map) |

Sections not applicable to the current subflow must be explicitly marked as "N/A — not applicable for [subflow]" rather than omitted.

`Taxpayer profile summary` holds residency, taxpayer type, 2026 AOW status
and transition month (taxpayer and partner), fiscal partner, household,
Box 2 screening, and business screening, each with provenance, and no BSN,
IBAN, or names. `Documents and sources` holds one row per document or chat
value used: `ev_NNN`, document as the user named it, type, tax year, owner,
location, values taken, and status (`extracted` / `needs review`); no file
hashes and no copied content beyond the short quote needed for provenance.
A chat value's row is named `chat YYYY-MM-DD` with type `user_chat`; no row
records a full BSN, IBAN, policy, contract, or aanslag number.
`Open questions` uses the columns Q-ID, section, question, blocking, and status;
`Missing information` uses M-ID, description, workpack row, linked Q-ID, and how
to resolve; `Assumptions` lists only assumptions the user explicitly accepted,
each with its A-ID and the `U:` quote and date of that acceptance.

---

## Status banner and readiness

The workpack opens with a STATUS banner derived from the section rollup in
`reference/provisional-flow.md`:

- `STATUS: DRAFT — N open section(s) — not for filing` while any applicable
  section is not `complete` or `chat_only`, a blocking open question remains,
  or a workflow-specific manual-review blocker forces a draft.
- `STATUS: COMPLETE DRAFT FOR REVIEW — not for filing` only when every
  applicable section is `complete` or `chat_only` and nothing forces a draft.

Appendix A `readiness` (`draft` / `review_ready`) and the field-map
`readiness` come from the same rollup. This skill is the single readiness
authority; a validator may reject an impossible `review_ready` but never
promotes `draft`.

---

## Amount labeling rules

Every monetary amount in the workpack MUST be labeled with one of:

- **estimate** — a forward-looking projection provided by the taxpayer for 2026
- **from-baseline** — a value carried from an existing voorlopige aanslag or prior-year data

Do NOT present any amount without a label. Unlabeled amounts create ambiguity about whether they are actuals, estimates, or inherited values.

Box 2 provisional amounts MUST also be labeled this way. This applies to estimated regular benefits, estimated disposal benefits, estimated costs, estimated dividend withholding tax, estimated fictitious regular benefit from BV lending, and partner allocation values.

## Winst uit onderneming forecast rule

For an eenmanszaak/ZZP, the workpack may contain one sourced, user-reviewed
full-year forecast in the portal section `Winst uit onderneming`:
`onderneming.geschatte_winst`. It MUST carry provenance, an estimate or
from-baseline label, and manual review. Do not use the generic Box 1
other-income field as a business-profit substitute.

`../nl-tax-shared-resources/knowledge/years/2026/provisional/winst-provisional-2026.md` is
canonical for this field and for every 2026 business figure named anywhere in
this contract. Read each figure there; never restate one from memory.

**Confirmed field semantics -- REQUIRED.** The workpack MUST record the estimate
on exactly these terms, and the agent MUST state them to the taxpayer before the
amount is recorded:

- the winst the taxpayer expects to earn as ondernemer in 2026;
- taken **before** the ondernemersaftrek and **before** the
  MKB-winstvrijstelling -- an estimate already reduced by either one is too low;
- excluding the btw payable and the btw reclaimable;
- an expected loss entered as a negative amount, with a minus sign;
- one business figure, and only one.

The provisional workpack MUST NOT prepare annual profit-and-loss or balance
accounts, zelfstandigenaftrek, startersaftrek, ondernemersaftrek,
MKB-winstvrijstelling, KIA, a bijdrage Zvw amount, cessation profit, or final
tax. The 2026 form has no amount field for any of them. Complex forms and events
route to terminal manual review.

When a forecast applies, it MUST also appear as its own row in the change
delta and in the Box 1 income-before-own-home rollup. A workpack that records
`onderneming.geschatte_winst` but drops it from those review totals is invalid.

### Examples

- "Employment income: EUR 45,000 (estimate)" — correct
- "Employment income: EUR 45,000 (from-baseline)" — correct
- "Employment income: EUR 45,000" — INVALID, missing label

---

## Voorlopige aanslag Zorgverzekeringswet -- REQUIRED companion item

`../nl-tax-shared-resources/knowledge/years/2026/provisional/zvw-provisional-2026.md` is canonical
for the 2026 percentage, the maximumbijdrage-inkomen, and every other figure in
this section. Read them there; never restate one from memory, and never multiply
the percentage by the ceiling.

Where the taxpayer has winst uit onderneming or income from work performed
outside employment, the workpack MUST raise the inkomensafhankelijke bijdrage
Zorgverzekeringswet without waiting to be asked, and MUST record:

- that such a taxpayer receives **two** aanslagen -- one for the
  inkomstenbelasting/premie volksverzekeringen and a separate one for the
  bijdrage Zvw -- and may hold a separate **voorlopige aanslag
  Zorgverzekeringswet 2026** alongside the income-tax one;
- that the voorlopige aanslag Zvw has its **own change route**. No reviewed
  source establishes whether a change to the income-tax voorlopige aanslag is
  coupled to the Zvw assessment, so the taxpayer must check the Zvw assessment
  separately and the workpack records what they find;
- the answer to the direct question "Have you (the taxpayer) received a
  voorlopige aanslag Zorgverzekeringswet for 2026, and what income estimate does
  it use?", with provenance -- or an open row in Missing information when the
  taxpayer does not know. Never assume there is none and never enter a zero;
- a human-subject action line, for example: "You (the taxpayer) also check your
  voorlopige aanslag Zorgverzekeringswet 2026 in Mijn Belastingdienst and change
  it separately if its estimate is no longer right.";
- that the Zvw base is the belastbare winst, a different figure from
  `onderneming.geschatte_winst`, which is taken before the ondernemersaftrek and
  the MKB-winstvrijstelling;
- that the bijdrage Zvw is not deductible and is never subtracted from the
  profit estimate.

The Zvw is reported **alongside** the income-tax dataset and is never merged into
it. The workpack MUST NOT compute a bijdrage Zvw amount, MUST NOT emit a field,
portal instruction, or checklist row that has the taxpayer entering a Zvw amount
in the income-tax voorlopige-aanslag form, and MUST NOT state Zvw instalment,
deadline, payment, or refund timing. Those, and any exception regime, are
manual-review items; the Belastingdienst calculates the bijdrage.

The income-tax field map (Appendix B and the Field map summary) MUST contain no
Zvw field or value whatsoever: no Zvw `field_id`, label, note, amount, baseline,
estimate, or manual-entry row. The separate assessment belongs only in the
workpack companion section and the human review action.

---

## Rollover-trap check -- REQUIRED

A voorlopige aanslag 2026 that the Belastingdienst extended automatically, or
that opened pre-filled from an earlier return, rests on an earlier year's
figures. No reviewed source states that a carried-over business estimate is
recalculated for the new year's ondernemersaftrek, and the zelfstandigenaftrek
has fallen sharply between the two years -- both amounts are in
`winst-provisional-2026.md`. A 2026 calculation still resting on the older,
higher zelfstandigenaftrek overstates the deduction, so the taxpayer pays too
little through the year and owes the difference when the final 2026 assessment
is made up.

For every taxpayer whose 2026 voorlopige aanslag was extended automatically or
opened pre-filled, the workpack MUST record the answers to:

1. Which year's figures does the current voorlopige aanslag 2026 rest on?
2. What profit estimate does it use, and is that still the taxpayer's own best
   estimate for 2026?
3. Does the taxpayer's own reasoning about the amount still use a
   zelfstandigenaftrek from an earlier year?

Flag any calculation that still rests on a zelfstandigenaftrek above the 2026
amount in `winst-provisional-2026.md`, and put the finding in words the taxpayer
can act on. An unanswered question stays an open row in Missing information;
never fill the gap with an assumption and never enter a zero.

A change made to the voorlopige aanslag 2025 after the cut-off date stated in
`winst-provisional-2026.md` is not carried into 2026 automatically. Where the
taxpayer made such a late correction, re-derive the 2026 estimate from their own
current forecast rather than assuming it followed.

---

## Box 3 validation rule — CRITICAL

**Box 3 MUST use the fictitious return method (forfaitair rendement) only.**

### FAIL conditions

The workpack MUST be rejected if any of the following are true:

- Werkelijk rendement is referenced as a data input
- Werkelijk rendement is requested from the user
- Werkelijk rendement is used in any calculation
- The workpack offers any method choice for box 3
- Box 3 calculation uses any method other than the three-category fictitious return

If the user asks about werkelijk rendement, answer in the conversation with:
"Werkelijk rendement may become relevant when filing the annual 2026 return in
2027." Do not add that exchange to the workpack as an input or option.

### Required box 3 structure

The box 3 section MUST follow this structure:

1. Categorie I: Banktegoeden — amount as of 1 January 2026
2. Categorie II: Overige bezittingen — amount as of 1 January 2026
3. Categorie III: qualifying Box 3 schulden — amount as of 1 January 2026,
   after the official inclusion/exclusion screen. A generic non-own-home debt
   is not accepted automatically; unresolved debts remain manual-review rows
   outside the totals
4. Aftrekbare schulden after the debt threshold
5. Belastbaar rendement
6. Rendementsgrondslag
7. Grondslag sparen en beleggen
8. Aandeel in rendementsgrondslag
9. Box 3 income
10. Box 3 tax at the rate from `box3-provisional.md`

The official 2026 page says 3 decimals in its general step but shows 2 decimals
in worked examples. If a review estimate displays the aandeel, the workpack
MUST identify the convention used and state that the live portal calculation
and resulting beschikking are authoritative; it must not claim either display
rule is the binding portal algorithm.

### Required box 3 note

Every workpack with a box 3 section MUST include:

> Werkelijk rendement is not part of provisional 2026.

No additional werkelijk-rendement input instructions, fields, calculations, or method-choice wording may be added.

---

## Box 2 validation rule

Standard Box 2 provisional preparation is supported for `provisional_2026` request and change flows.

The workpack and field map may include:

- `box2.geschatte_reguliere_voordelen`
- `box2.geschatte_vervreemdingsvoordelen`
- `box2.geschatte_kosten`
- `box2.geschatte_ingehouden_dividendbelasting`
- `box2.geschat_fictief_regulier_voordeel_bv_lening`
- `partner.verdeling_box2_inkomen`

Every Box 2 amount must be labeled as estimate or from-baseline. Route valuation disputes, emigration, death, restructurings, treaty/nonresident issues, informal capital, non-arm's-length transfers, and corporate-tax-heavy DGA facts to manual review or unsupported.

---

## Field map requirements

For request and change, the canonical field map is the one fenced `yaml` block
in `Appendix B — Field map`, with the human-readable table in `Field map
summary`. `nl-tax-field-mapper` alone authors both, following its own template,
provisional field reference, mapping principles, and rule data; `field_id`s
come from its provisional reference and `workflow` is `provisional_assessment`.
In the field map, `source.evidence_id` points to a `Documents and sources`
row, `source.profile_path` to a row `Key` in `Taxpayer profile summary`, and
`missing_fields[].open_question_id` to `Open questions`.

The mapper shows the `Field map summary` table in the conversation and
performs every check on the YAML it composes; the YAML is never printed in chat
and is written only into a saved workpack. The mapper adds its own rows to
`Open questions` and `Missing information` for mapping gaps, continuing the
Q001/M001 numbering, so every `missing_fields[].open_question_id` resolves. The taxpayer's review before manual
entry is the final check. Review and stopzetten produce no field map.

---

## Change subflow validation rules

### Full re-entry reminder — REQUIRED

Every change-subflow workpack MUST include this reminder:

> Prepare and verify the complete dataset; the change form requires all applicable categories, not only the changed item.

The reminder must appear:
- In the workpack body (not just in footnotes or appendices)
- Before the field map summary section

The portal may offer to pre-fill figures from the most recent annual return, but
it does not carry forward the current voorlopige-aanslag figures. Whether the
form opens blank or pre-filled, the workpack covers every applicable category.
Never claim that omitted values default to zero.

### Delta summary — REQUIRED

The change subflow MUST complete the `Delta summary` section of the workpack, following `reference/delta-rules.md`, containing:

- Baseline values (from existing voorlopige aanslag)
- Current estimate values (from user input)
- Delta per category (difference between baseline and current estimate)
- A non-binding possible direction for future payment/refund, or `uncertain`,
  plus the live-portal/replacement-beschikking caveat
- A separate expected-business-profit row when applicable
- Separate own-home component rows for eigenwoningforfait, total deductible
  own-home costs, any Hillen deduction, and `box1_own_home_balance`

A change-subflow workpack without a completed Delta summary section is invalid.

---

## Review subflow validation rules

The review subflow MUST complete the `Review questions` section of the
workpack: the category review table (each category `unchanged`, `changed`, or
`unknown`), the recommended action summary, and the change-subflow trigger.
Every `unknown` category has a question under `Open questions`. A review that
finds material changes recommends the change subflow, which collects the
complete dataset again; the review itself produces no field map.

---

## Stopzetten validation rules

Moving abroad requires residency review and is **not a categorical stopzetten reason**. A workpack must route migration facts to the unsupported residency/migration path rather than producing a stopzetten outcome solely from the move.

For review/change context, an **unsolicited** VA from earlier data **may be issued**, but it is **not guaranteed**; do not present a later VA as automatic.

### Current-date cutoff gate -- REQUIRED

Before writing stopzetten instructions, compare the current date to 2026-10-01.
If the current date is on or after 2026-10-01, the workpack MUST NOT include a
stopzetten checklist. It must state that the 2026 stopzetten cutoff has passed
and route the user to review/change or to a separate filing-status review and,
when a return will be filed, annual settlement.

### Structured stopzetten body -- REQUIRED

Every stopzetten-subflow workpack MUST include a `Stopzetten outcome` section in
the body. For a refund case before the cutoff, it MUST include:

- current cash-flow direction: monthly refund
- current-date cutoff result
- the selected refund component and expected effect of stopping: deductions,
  IACK, or algemene heffingskorting
- a separate annual-filing-status note; stopzetten itself does not create a
  universal filing obligation
- manual checklist for the official stopzetten process

For non-stopzetten outcomes, the same section must explicitly state the route
chosen and must not include a refund-stop checklist.

### Payment user routing — REQUIRED

If the user currently PAYS a monthly amount and the amount is incorrect:

- The workpack MUST redirect to the change subflow
- The workpack MUST NOT provide stopzetten guidance for payment correction
- The workpack MUST explain that stopping payments does not reduce the tax obligation and can create arrears under the current beschikking
- Record the redirect before continuing: the subflow becomes change (in the conversation and, when saved, in the `Subflow` heading and Appendix A `workflow: provisional_2026_change`); the payment baseline goes into `Existing baseline, if any` with provenance and `baseline` is `in_progress`; `stopzetten_direction` is `complete` with the route `change VA (payment case)` recorded in `Stopzetten outcome`; `confirm` returns to `not_started` and `generation_confirmed` to `false`. This avoids returning to stopzetten on the next turn.

### Refund user guidance — REQUIRED

If the user currently RECEIVES a monthly refund:

- The workpack MUST include a manual checklist for the official Mijn Belastingdienst stopzetten process
- For deductions and IACK, it MUST state that the stop is retroactive to
  1 January 2026 and show already-received amounts as a possible repayment
  controlled by a separate Belastingdienst notice
- For the algemene heffingskorting, it MUST record the chosen first day of the
  month and describe the payment effect as prospective from that selected/next
  payment month
- It MUST keep annual filing conditional on the taxpayer's separate filing
  obligation or choice/eligibility to file

---

## Sources used section — REQUIRED

Every workpack MUST list exactly the `source_id` values consulted for
provisional 2026, one per line, and that list MUST equal Appendix A
`sources_loaded`. Do not copy IDs from the annual workflow; the same ID may
appear in both workpacks only when it was independently consulted for both.
This provides traceability and allows a check against the knowledge base.

### Example

```
## Sources used
- bd_box3_2026_provisional
- bd_provisional_request_2026
- bd_provisional_rates_2026
```

---

## Not submission advice section -- REQUIRED

Every workpack MUST include the following section immediately before the
appendices:

> This workpack is a preparation aid. You, the taxpayer or an authorized human,
> must review the figures and perform all portal entry, signing, sending, or
> changes yourself. The assistant must not access or operate Mijn
> Belastingdienst.

A workpack without this section is invalid.
Do not expand it into generic credential boilerplate.

---

## Appendix A — Resume record

`Appendix A — Resume record` is one fenced `yaml` block with
`workpack_format: nl-tax-workpack`, `workpack_version: "2.0"`,
`plugin_version: "0.4.0"`, `workflow: provisional_2026_<subflow>`,
`tax_year: 2026`, `created_at`, `updated_at`, `save_consent`, `readiness`,
`generation_confirmed`, `queued_workflow: null`, `sections`, and
`sources_loaded`. `save_consent` defaults to `not_given` in the template and is
`given` in the written file; it is a record, never an authorization to write. `sections` uses the provisional keys from
`reference/provisional-flow.md` that apply to the subflow, each as
`{status, open}` where `open` lists the open question IDs for that section.
Facts never live in the resume record; they live in the readable sections with
provenance.

---

## Validation checklist

Before delivering any workpack, verify (`check_performed_by: checked_by_agent`):

- [ ] All required sections are present in order for the applicable subflow
- [ ] STATUS banner, Appendix A `readiness`, and any field-map `readiness` come from the same rollup
- [ ] Taxpayer profile summary and Documents and sources contain no BSN, IBAN, policy, contract, or aanslag number, file hash, or copied document content
- [ ] User-stated values index lists every `U:` chat-stated value for spot-checking
- [ ] Every `F:` code points to a Documents and sources row
- [ ] All amounts are labeled (estimate or from-baseline)
- [ ] Box 2 amounts are labeled estimate or from-baseline, when applicable
- [ ] Box 3 uses fictitious method only, with only the required explanatory note for werkelijk rendement
- [ ] Candidate Box 3 debts passed the official inclusion/exclusion screen; unresolved debts remain manual-review rows outside accepted totals
- [ ] Any displayed Box 3 aandeel records the estimate's rounding convention and defers to the live portal/beschikking
- [ ] AOW status is `below_all_year`, `reaches_during_year`, or `aow_all_year`; a transition-year month and manual portal result replace a whole-year table estimate
- [ ] Expected business profit, when applicable, is included in the Box 1 rollup and change delta
- [ ] `onderneming.geschatte_winst` is recorded and explained as the winst before
  ondernemersaftrek and before MKB-winstvrijstelling, excluding btw, with a minus
  sign for an expected loss, and the definition was stated to the taxpayer before
  the amount was recorded
- [ ] The separate voorlopige aanslag Zorgverzekeringswet is raised as a
  companion item with its own change route, no bijdrage amount is computed, and
  no Zvw row enters the income-tax dataset
- [ ] The rollover-trap check was performed when the 2026 voorlopige aanslag was
  extended automatically or opened pre-filled, and any zelfstandigenaftrek above
  the 2026 amount was flagged
- [ ] Own-home review shows the 1 January 2025 WOZ peildatum and all components of `box1_own_home_balance`
- [ ] IACK, ouderenkorting, alleenstaandeouderenkorting, jonggehandicaptenkorting, zorgkosten thresholds, and lijfrente limits are manual-review items unless exact reviewed sources and required inputs are registered
- [ ] Partner allocation scenarios are traceable and none is ranked or selected; the split is recorded only after both partners choose it
- [ ] Change subflow includes the full re-entry reminder
- [ ] Change subflow includes a completed Delta summary section
- [ ] Review subflow includes a completed Review questions section
- [ ] Stopzetten subflow includes a structured `Stopzetten outcome` body
- [ ] Stopzetten cutoff was evaluated against the current date before any checklist was included
- [ ] Stopzetten routes payment users to change subflow
- [ ] Stopzetten distinguishes retroactive deductions/IACK from the prospective monthly algemene-heffingskorting stop, keeps prior repayment in a separate notice, and treats annual filing as a separate question
- [ ] Sources used lists exactly the provisional 2026 source IDs and equals Appendix A `sources_loaded`
- [ ] Not submission advice section is present before the appendices
- [ ] Open questions, Missing information, and Assumptions sections are present; Assumptions holds only user-accepted assumptions
- [ ] Human review checklist is present
- [ ] Nothing was written except `workspace/nl-tax-provisional-2026-workpack.md`, and only while save consent was active in this conversation
- [ ] A missing baseline field is `unknown` with a non-blocking note in the Delta summary, not an assumption or a Missing information row
