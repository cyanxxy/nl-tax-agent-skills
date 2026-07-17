# Voorlopige Aanslag Review Questions -- 2026

## Workflow: provisional_2026_review
## Created: [timestamp]

## Purpose

Use this file to compare the current 2026 voorlopige aanslag baseline with the taxpayer's current 2026 situation. It is a review aid: if material changes are found, route to the change subflow and prepare a complete change workpack.

## Baseline summary

| Baseline field | Baseline value | Src |
|----------------|----------------|-----|
| Beschikking date | [date] | [F/U/?] |
| Monthly amount | [EUR X refund/payment] | [F/U/?] |
| Source type | [EVA / VVA / beschikking / user input] | [F/U/?] |

## Category review

| Category | Baseline field | Current 2026 estimate | Change status | Evidence / quote | Recommended action |
|----------|----------------|-----------------------|---------------|------------------|--------------------|
| Employment income | [baseline row] | [current estimate or unchanged] | [unchanged / changed / unknown] | [F/U/?] | [no action / ask follow-up / change subflow] |
| Pension and benefits | [baseline row] | [current estimate or unchanged] | [unchanged / changed / unknown] | [F/U/?] | [no action / ask follow-up / change subflow] |
| AOW status and transition month | [below_all_year / reaches_during_year / aow_all_year] | [reviewed state and month/N/A] | [unchanged / changed / unknown] | [F/U/calculated/?] | [manual portal review for transition / ask follow-up / change subflow] |
| Expected business profit (`onderneming.geschatte_winst`) | [baseline row/N/A] | [current estimate or unchanged] | [unchanged / changed / unknown / N/A] | [F/U/?] | [no action / ask follow-up / change subflow / manual review] |
| Other income | [baseline row] | [current estimate or unchanged] | [unchanged / changed / unknown] | [F/U/?] | [no action / ask follow-up / change subflow] |
| Own-home WOZ / eigenwoningforfait | [WOZ peildatum 1 January 2025 and baseline EWF] | [current estimate or unchanged] | [unchanged / changed / unknown] | [F/U/?] | [no action / ask follow-up / change subflow] |
| Own-home deductible costs / Hillen / `box1_own_home_balance` | [baseline components] | [current components or unchanged] | [unchanged / changed / unknown] | [F/U/?] | [no action / ask follow-up / change subflow / manual review] |
| Deductions | [baseline row] | [current estimate or unchanged] | [unchanged / changed / unknown] | [F/U/?] | [no action / ask follow-up / change subflow] |
| Box 2 | [baseline row] | [current estimate or not applicable] | [unchanged / changed / unknown / not applicable] | [F/U/?] | [no action / ask follow-up / change subflow / manual review] |
| Box 3 peildatum assets | [baseline row] | [current estimate or unchanged at 1 January 2026] | [unchanged / changed / unknown] | [F/U/?] | [no action / ask follow-up / change subflow] |
| Box 3 qualifying debts | [accepted baseline rows] | [accepted current rows after inclusion/exclusion screen] | [unchanged / changed / unknown] | [F/U/?] | [no action / ask follow-up / change subflow / manual review] |
| Alleenstaandeouderenkorting | [baseline credit/N/A] | [entitlement to an AOW pension for a single person / unresolved] | [unchanged / changed / unknown / N/A] | [F/U/?] | [manual review; never infer from single-parent status] |
| Partner allocation | [baseline row] | [current estimate or unchanged] | [unchanged / changed / unknown / not applicable] | [F/U/?] | [no action / ask follow-up / change subflow] |

## Open questions

| Question ID | Category | Question | Why it matters | Status |
|-------------|----------|----------|----------------|--------|
| RQ-001 | [category] | [question] | [impact on VA] | [open / answered / deferred] |

## Recommended action summary

| Recommended action | Applies? | Reason |
|--------------------|----------|--------|
| No action | [yes/no] | [reason] |
| Continue review | [yes/no] | [remaining unknowns] |
| Change subflow | [yes/no] | [changed categories] |
| Manual review | [yes/no] | [complex or unsupported facts] |

## Change-subflow trigger

If a reviewed category is marked `changed` and may materially affect the
portal estimate, discuss `provisional_2026_change`. A change workpack must
collect the complete dataset again; do not prepare only the changed rows. The
live portal and replacement beschikking, not this review table, determine the
actual future payment/refund amount and timing.
