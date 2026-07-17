# Human-only runtime projection: change-flow.md

projection_version: "1"
derived_from: skills/_shared/knowledge/years/2026/provisional/change-flow.md
derived_note_sha256: d67e793652e7dc4b27f0f3797cf2ae49ab285297682e59be1f2fd5d0f5100b54
source_ids: bd_provisional_change_2026

This is a mechanically reversible runtime projection, not an independently reviewed tax note. The cited reviewed snapshot remains the provenance authority. The only permitted body transformation is inserting `**Taxpayer:**` before portal-action imperatives.

## Rule

An existing voorlopige aanslag for 2026 is changed through the same "Voorlopige aanslag aanvragen of wijzigen" entry in Mijn Belastingdienst (request and change share one combined flow). Prepare and verify the complete dataset; the change form requires all applicable categories, not only the changed item.

## CRITICAL RULE -- Every field must be complete

A change requires all applicable categories, not only the changed item. The portal MAY offer to pre-fill figures from the taxpayer's most recent aangifte (the data from two years prior) when they opt in -- it does not carry forward the figures from the current voorlopige aanslag. Whether the form opens blank or pre-filled, the workpack must prepare, and the taxpayer must verify, the COMPLETE dataset:

- All income sources (employment, pension, benefits, other income, and the
  dedicated expected-business-profit forecast); include business profit in the
  Box 1 review rollup
- All deductions, including the separate own-home components using the WOZ
  peildatum of 1 January 2025
- All box 3 assets and qualifying debts after the official debt
  inclusion/exclusion screen

Official guidance states that all data must be present in the form, including data that does not change ("Houd er rekening mee dat u alle gegevens moet invullen. Ook de gegevens die niet wijzigen"), so the workpack must always cover the full dataset.

## Common reasons to change

- Salary increase or decrease
- New mortgage, mortgage change, or mortgage payoff
- Partner situation change (marriage, registered partnership, separation, divorce)
- Changed deductions (started or stopped alimony, new insurance premiums)
- Started or stopped self-employment
- Significant change in box 3 assets or debts
- Retirement or loss of employment

## Effect of a change

- A new beschikking (decision) is issued after the change is processed
- The replacement beschikking may adjust future payments or refunds for the
  remaining part of the year
- The Belastingdienst recalculates the assessment from the newly submitted complete dataset
- The portal preview may indicate a higher payment/lower refund or a lower
  payment/higher refund, but it is only an estimate
- Only the replacement beschikking determines the actual amount, treatment of
  earlier provisional amounts, and future payment/refund timing

## How to change

1. **Taxpayer:** Log in to Mijn Belastingdienst
2. **Taxpayer:** Open "Voorlopige aanslag aanvragen of wijzigen" for 2026 (request and change share one combined flow)
3. **Taxpayer:** Choose to change (wijzigen) the existing 2026 voorlopige aanslag; optionally accept the offer to pre-fill prior-year figures
4. **Taxpayer:** Prepare and verify the complete dataset: all applicable income, deductions, and box 3 categories, not only the changed item
5. **Taxpayer:** Review the portal's estimated summary and possible future monthly amount
6. **Taxpayer:** Sign and send (ondertekenen en verzenden)

## Developer instruction

When building a workpack for changing a voorlopige aanslag 2026:

1. Tell the user upfront: prepare and verify the complete dataset; the change form requires all applicable categories, not only the changed item
2. If previous workpack data is available, pre-populate the workpack as a starting point but have the user confirm every field (note that the portal itself may also offer to pre-fill prior-year figures)
3. Clearly show what changed between the old and new estimates
4. Present the delta: old monthly amount vs. new monthly amount
5. Remind the user that a new beschikking will be sent and that it, rather
   than the workpack delta, controls any payment/refund adjustment
6. For box 3 data, follow box3-provisional.md rules

## Common failure

Do not prepare only the changed fields. The Belastingdienst guidance requires all data to be filled in again, including unchanged data. Always ensure the workpack contains the full dataset.
