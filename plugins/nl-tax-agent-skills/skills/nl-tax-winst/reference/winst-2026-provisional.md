# Winst uit onderneming -- Provisional 2026 Expected-Profit Forecast

source_ids: bd_provisional_request_2026, bd_provisional_change_2026
workflow: provisional_assessment
tax_year: 2026
status: active
review_status: reviewed
last_reviewed: "2026-08-15"

## Scope

This reference supports one preparation-only value in a request or change of a
2026 voorlopige aanslag: the taxpayer's reviewed full-year expected-profit
forecast for the portal section `Winst uit onderneming`.

Two reviewed knowledge notes are canonical here and own every figure:

- `_shared/knowledge/years/2026/provisional/winst-provisional-2026.md` -- the
  meaning of the single business field, what the form does and does not contain,
  the items the invulhulp says the estimate must take into account, and the
  rollover trap on a carried-forward estimate.
- `_shared/knowledge/years/2026/provisional/zvw-provisional-2026.md` -- the
  bijdrage Zorgverzekeringswet and the separate voorlopige aanslag Zvw.

Read both there and never restate a figure from memory. Do not load annual
entrepreneur material, annual rates, or an annual profit chain for this flow.

## Output contract

- Field id: `onderneming.geschatte_winst`
- Meaning: the taxpayer's best current forecast of full-year 2026 business
  profit, entered in the `Winst uit onderneming` section.
- Position in the chain: the winst **before** the ondernemersaftrek and **before**
  the mkb-winstvrijstelling. Never reduce the estimate by those items first --
  the Belastingdienst applies them itself when it calculates the aanslag, so a
  pre-reduced estimate is too low and gets reduced twice.
- Btw: the estimate excludes the btw the taxpayer has to pay over and the btw
  they can reclaim.
- Sign: an expected loss is entered as a negative amount, with a minus sign.
- Count: one business figure, and only one. The form carries no balans, no
  winst-en-verliesrekening, and no amount field for a deduction or an exemption.
- Provenance: retain an evidence id, a user-chat quote and timestamp, or a
  baseline reference; also record the forecast basis.
- Review: `manual_review_required: true`. The taxpayer reviews the value against
  current bookkeeping and the live portal before entry.

Do not substitute a generic other-income field for this business field, and do
not add a second business field to the dataset.

## Questions

Ask for the expected full-year profit, the period covered by current
bookkeeping, known changes for the remaining months, and confirmation that the
result is the taxpayer's reviewed best estimate. Then ask about each item the
invulhulp lists that plausibly applies to this taxpayer, reading that list from
`winst-provisional-2026.md`. If the user has no supportable forecast, leave the
field missing; never invent a zero, and never assume an item is nil because the
taxpayer did not mention it.

The form also puts eligibility questions to the taxpayer around the
ondernemersaftrek, including whether they are a medegerechtigde or a
geldverstrekker. Answer those from facts the taxpayer confirms, never from an
inference.

## The separate voorlopige aanslag Zvw

Raise this with the taxpayer without waiting to be asked. It is the point in this
flow with the most practical value for an ondernemer.

- An ondernemer, and anyone with income from work outside employment, pays the
  inkomensafhankelijke bijdrage Zorgverzekeringswet themselves and receives a
  **separate voorlopige aanslag Zorgverzekeringswet** alongside the voorlopige
  aanslag inkomstenbelasting. Two assessments, not one.
- It has its **own change route**. No reviewed source establishes whether an
  income-tax change is coupled to the Zvw assessment, so the taxpayer checks the
  Zvw assessment separately and records what they find.
- The Zvw base is a different figure from the one on this form: the
  bijdrage-inkomen is the belastbare winst, while `onderneming.geschatte_winst`
  is the winst before the ondernemersaftrek and the mkb-winstvrijstelling. Never
  present the income-tax estimate as the Zvw base, and do not compute the
  belastbare winst in this flow.
- Read the percentage and the maximumbijdrage-inkomen from
  `zvw-provisional-2026.md`. Do not print a maximum bijdrage amount and do not
  predict what the aanslag will say.
- Return the Zvw only as a companion note and separate human check. Never return
  a Zvw field or value for the income-tax field map: no Zvw `field_id`, label,
  note, amount, baseline, estimate, or manual-entry row.
- Payment terms and timing for the voorlopige aanslag Zvw are not established in
  the reviewed sources. Ask the taxpayer to read the dates printed on their own
  voorlopige aanslag Zvw, and route any timing question to manual review.
- **You (the taxpayer)** open, check, and change each aanslag yourself. This
  plugin never opens or operates the portal.

## Exclusions

This forecast does not prepare or calculate:

- annual profit-and-loss or balance accounts
- zelfstandigenaftrek, startersaftrek, ondernemersaftrek, MKB-winstvrijstelling,
  KIA, or other annual deductions
- Zvw contributions: the separate voorlopige aanslag Zvw is raised with the
  taxpayer and never sized here
- cessation profit or another complex business event
- final tax, a final assessment, or a completed annual business return

Complex legal forms and events remain terminal manual review. Where the taxpayer
asks for one of the items above, say which return owns it and keep this dataset
to the single field.
