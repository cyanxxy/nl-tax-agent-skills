# Rule note: Voorlopige aanslag 2026 — refund payment timing

source_ids: bd_provisional_refund_timing_2026
workflow: provisional_assessment
tax_year: 2026
status: active
last_reviewed: "2026-07-16"
review_status: reviewed

## Rule

When a 2026 voorlopige aanslag results in a refund (teruggaaf), the Belastingdienst pays it out automatically across the year. These are reference notes for workpack preparation — not a payment guarantee; the Belastingdienst controls the actual payment runs.

## Refund payment schedule (teruggaaf)

- The amount on the voorlopige aanslag is a **yearly amount**, paid in **equal monthly termijnen**, automatically — the taxpayer does not need to do anything.
- The **first payment** arrives about **8 weeks** after the request.
- **Subsequent payments** fall on the **15th of each month**. If the 15th is a weekend or public holiday, payment moves to the next working day.
- If **fewer than 2 termijnen** remain in the calendar year, the assessment is paid **after year-end** — within about **1 week** of the date stated on the voorlopige aanslag.
- If the refund must be set off (verrekend) against an outstanding amount, payout can take longer.
- If the Belastingdienst lacks the taxpayer's rekeningnummer, it sends a letter and payment can take a few weeks longer (the account is checked against the taxpayer's name first).

### Worked example

Request on 1 May 2026 showing a EUR 7,000 refund: the first payment arrives around end of June, and the year amount is spread over 7 termijnen (June–December) = EUR 1,000 per month, with the last payment around 15 December.

## Changing a voorlopige aanslag mid-year

If the user changes the voorlopige aanslag during the year, the replacement
beschikking may re-spread a recalculated yearly refund over the remaining
termijnen. The portal preview is an estimate; the new beschikking controls the
actual amount and timing. The change subflow's rule still applies: prepare and verify the complete dataset; the change form requires all applicable categories, not only the changed item.

## Developer instruction

Use this only to set expectations in the provisional workpack (roughly when the
user may receive money). Do not present exact dates or amounts as guaranteed,
and do not convert a workpack estimate into a payment promise.

## Common failure

Do not promise a lump-sum refund for a mid-year request — a refund is paid in monthly termijnen across the remaining year, not all at once.
