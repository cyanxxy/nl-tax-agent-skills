# Filing Paths — Conversational Intent Guide

Use these distinctions to interpret what the user is trying to accomplish.
They are not a fixed questionnaire or decision tree: credit facts the user has
already supplied, ask only about a material ambiguity, and let the owning agent
choose the clearest conversational order.

## Annual Return 2025

- **Direction:** Backward-looking — what happened in 2025
- **Filing review:** The annual workflow asks whether an invitation letter
  (aangiftebrief) exists. If it does, the label is `invited` and its deadline
  applies. With no invitation, the taxpayer completes the 2025 return
  personally in Mijn Belastingdienst without submitting; the assistant never
  opens or operates the authenticated portal. The official result gives one of
  these labels: `no_letter_but_mandatory` (EUR 58 or more to pay, or the
  separate income-dependent-scheme/assets test), `refund_claim_only` (EUR 19 or
  more back, with no mandatory test), or `filing_obligation_unresolved`. The
  first no-letter route carries the **14 July 2026** guardrail. These are
  review labels based on the official result, not an automated eligibility
  decision.
- **Asset/scheme question:** Filing can still be mandatory when the taxpayer has
  a right to an income-dependent scheme and relevant assets exceed EUR 37,395,
  or EUR 74,790 with a fiscal partner. Do not infer scheme entitlement or the
  relevant asset total.
- **What the user needs:** Relevant 2025 evidence (jaaropgaven, WOZ-beschikking,
  bank statements for applicable Box 3 dates, mortgage annual statement, and
  deduction evidence). For an IB-ondernemer, also the business evidence: the
  finalized winst-en-verliesrekening, the balans with both the opening and the
  closing column, the urenadministratie, and the investeringsfacturen for
  bedrijfsmiddelen bought in the year. The user may give values in chat
  instead of sharing a document.
- **Trigger phrases:** "aangifte doen", "belastingaangifte 2025", "file my taxes", "income tax return"

## Annual Return 2026

- **Direction:** Actual 2026 income, assets and deductions; year-to-date
  evidence stays distinct from forecasts until final annual evidence exists.
- **Owner:** `../nl-tax-annual-return-2026/SKILL.md`. A separate actual-return
  draft, not the provisional 2026 estimate workflow.
- **Boundary:** Source/form review and outstanding year-end evidence keep
  preparation draft; no opening date, deadline or final annual portal
  inventory is assumed. Resident 2025 helper/rate contracts do not apply.

## Migration / Nonresident Annual 2025 or 2026

- **Direction:** Establish residence intervals and the migration or full-year
  nonresident form, then prepare evidence with international classification
  questions. Use `reference/extended-routing.md` and its international owner.
- **Boundary:** 2025 M/C preparation is available; 2026 is precollection until
  its final annual form is reviewed. Neither route is automatically terminal.
  A voorlopige aanslag 2026 for a migrant or nonresident is not this route: it
  follows the terminal provisional boundary in section 1 of
  `reference/unsupported-cases.md`.

## ICP / OSS / IOSS

- **Direction:** Separate cross-border declarations. The ICP rubric 3 total
  (ICP rubric 3a goods and services plus ICP rubric 3b simplified
  triangulation) must reconcile to btw-aangifte rubric 3b for the same
  coverage.
  OSS uses an already established Union/non-Union/IOSS registration, scheme
  and period, with verified consumption-country rates.
- **Owner:** `reference/extended-routing.md` names the separate ICP/OSS owners.
  A domestic VAT return never substitutes for either declaration.

## Voorlopige Aanslag 2026 — Request

- **Direction:** Forward-looking — what do you expect in 2026
- **Timing:** Can be requested any time during 2026
- **What the user needs:** Estimates for 2026 income, deductions, and credits
- **Trigger phrases:** "voorlopige aanslag aanvragen", "request provisional assessment", "monthly refund"

## Voorlopige Aanslag 2026 — Change

- **Direction:** Forward-looking — updated expectations for 2026
- **Prerequisite:** User already has a voorlopige aanslag for 2026
- **What the user needs:** Updated estimates that differ from the original request
- **Trigger phrases:** "voorlopige aanslag wijzigen", "change my provisional", "update my monthly payment"

## Voorlopige Aanslag 2026 — Review

- **Direction:** Forward-looking — verify current voorlopige aanslag is still correct
- **Prerequisite:** User already has a voorlopige aanslag for 2026
- **What the user needs:** Current voorlopige aanslag details and actual/expected 2026 figures
- **Trigger phrases:** "klopt mijn voorlopige aanslag", "check my provisional", "is my monthly amount correct"

## Voorlopige Aanslag 2026 — Stopzetten

- **Direction:** Forward-looking — stop monthly refunds; payment corrections go through wijzigen
- **Prerequisite:** User already has a voorlopige aanslag for 2026
- **What the user needs:** Confirmation that they want to stop; understanding of consequences
- **Trigger phrases:** "voorlopige aanslag stopzetten", "stop my provisional", "stop monthly refund"

## Key Distinction

- **VAT = transaction and period based:** a `btw-aangifte`/`omzetbelasting`
  for an assigned monthly, quarterly, or annual period. Use
  `reference/vat-routing.md` for return or correction intent. A "ZZP return"
  may mean income tax or VAT; resolve that ambiguity before the annual flow.

- **Annual = actuals:** What happened in the requested 2025 or 2026 year.
  Annual 2026 collected before year-end remains an actual-evidence draft.
- **Provisional = forward-looking:** What do you expect in 2026 (estimates, projection-based)

## When the User is Unsure

For ambiguous 2026 income-tax intent, ask whether the user wants actual
annual-return evidence preparation or a provisional estimate. When the user is
choosing between the resident annual return 2025 and the voorlopige aanslag
2026, ask: "Do you want to look back at what happened in 2025, or plan
ahead for 2026?" Do not turn explicit annual 2026 intent into provisional.

- If looking back at 2025 → Annual return 2025
- If planning ahead for 2026 → Voorlopige aanslag 2026 (then determine subflow: request, change, review, or stopzetten)
- If both → Settle the 2026 subflow, start with the annual return 2025, and
  queue provisional 2026. After the annual workpack is generated and mapped,
  continue into the queued subflow without asking for a new activation phrase.
  Annual actuals may inform a later estimate only after the taxpayer reviews or
  states that provisional estimate; never copy them automatically.
