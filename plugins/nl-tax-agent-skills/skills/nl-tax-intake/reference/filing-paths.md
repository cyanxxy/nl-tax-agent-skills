# Filing Paths — Conversational Intent Guide

Use these distinctions to interpret what the user is trying to accomplish.
They are not a fixed questionnaire or decision tree: credit facts the user has
already supplied, ask only about a material ambiguity, and let the owning agent
choose the clearest conversational order.

## Annual Return 2025

- **Direction:** Backward-looking — what happened in 2025
- **Filing review:** Ask whether an invitation letter (aangiftebrief) exists. If it does, record
  `invited` and use its deadline. With no invitation, ask the taxpayer to
  complete the 2025 return personally in Mijn Belastingdienst without
  submitting. The assistant must not open or operate the authenticated portal.
  Record one of:
  `no_letter_but_mandatory` (EUR 58 or more to pay, or the separate
  income-dependent-scheme/assets test), `refund_claim_only` (EUR 19 or more
  back, with no mandatory test), or `filing_obligation_unresolved`. The first
  no-letter route carries the **14 July 2026** guardrail. These are review labels
  based on the official result, not an automated eligibility decision.
- **Asset/scheme question:** Filing can still be mandatory when the taxpayer has
  a right to an income-dependent scheme and relevant assets exceed EUR 37,395,
  or EUR 74,790 with a fiscal partner. Do not infer scheme entitlement or the
  relevant asset total.
- **What the user needs:** Relevant 2025 evidence (jaaropgaven, WOZ-beschikking,
  bank statements for applicable Box 3 dates, mortgage annual statement, and
  deduction evidence). Values may be supplied in chat when the user chooses not
  to upload a document.
- **Trigger phrases:** "aangifte doen", "belastingaangifte 2025", "file my taxes", "income tax return"

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

- **Annual = backward-looking:** What actually happened in 2025 (actuals, evidence-based)
- **Provisional = forward-looking:** What do you expect in 2026 (estimates, projection-based)

## When the User is Unsure

Ask: "Do you want to look back at what happened in 2025, or plan ahead for 2026?"

- If looking back at 2025 → Annual return 2025
- If planning ahead for 2026 → Voorlopige aanslag 2026 (then determine subflow: request, change, review, or stopzetten)
- If both → Record the chosen 2026 subflow, start with the annual return
  2025, and queue provisional 2026. After the completed annual workpack and
  field map validate, continue into the queued subflow without asking for a new
  activation phrase. Annual actuals may inform a later estimate only after the
  taxpayer reviews or states that provisional estimate; do not copy them
  automatically.
