# Winst uit onderneming — Provisional 2026 Expected-Profit Forecast

source_ids: bd_provisional_request_2026, bd_provisional_change_2026
workflow: provisional_assessment
tax_year: 2026
status: active
review_status: reviewed
last_reviewed: "2026-07-11"

## Scope

This reference supports one preparation-only value in a request or change of a
2026 voorlopige aanslag: the taxpayer's reviewed full-year expected-profit
forecast for the portal section `Winst uit onderneming`.

## Output contract

- Field id: `onderneming.geschatte_winst`
- Meaning: the taxpayer's best current forecast of full-year 2026 business
  profit, entered in the `Winst uit onderneming` section.
- Provenance: retain an evidence id, a user-chat quote and timestamp, or a
  baseline reference; also record the forecast basis.
- Review: `manual_review_required: true`. The taxpayer reviews the value against
  current bookkeeping and the live portal before entry.

Do not substitute a generic other-income field for this business field.

## Questions

Ask for the expected full-year profit, the period covered by current
bookkeeping, known changes for the remaining months, and confirmation that the
result is the taxpayer's reviewed best estimate. If the user has no supportable
forecast, leave the field missing; never invent a zero.

## Exclusions

This forecast does not prepare or calculate:

- annual profit-and-loss or balance accounts
- zelfstandigenaftrek, startersaftrek, ondernemersaftrek, MKB-winstvrijstelling,
  KIA, or other annual deductions
- Zvw contributions
- cessation profit or another complex business event
- final tax, a final assessment, or a completed annual business return

Complex legal forms and events remain terminal manual review.
