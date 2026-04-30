# Rule note: Uitvoeringsregeling inkomstenbelasting 2001 -- structural reference

source_id: law_uitvoeringsregeling_ib_2001
workflow: all
tax_year: all
status: active
last_reviewed: "2026-04-30"
review_status: reviewed

## Rule

The Uitvoeringsregeling inkomstenbelasting 2001 is the ministerial regulation implementing the Wet IB 2001. It contains detailed operational rules that give effect to the provisions of the parent law.

## Scope of the regulation

The Uitvoeringsregeling specifies detailed rules for:

- **Income categorization** -- how specific types of income are classified and which box they belong to
- **Deduction requirements** -- conditions that must be met for deductions to be claimed
- **Evidence standards** -- what documentation a taxpayer must retain to substantiate claims
- **Administrative procedures** -- how certain elections and notifications must be made

## Relevance to this project

### Evidence checklist validation

The regulation defines what evidence is required to support specific deduction claims. The evidence-indexer skill uses these requirements to validate whether a taxpayer's documentation is complete.

### Deduction eligibility checks

Detailed conditions for claiming deductions (e.g., specific care costs, gifts, own-home interest) are specified in this regulation. Skills that calculate or validate deductions must reference these conditions.

### Documentation requirements

The regulation specifies retention periods and formats for supporting documentation. This informs the evidence-indexer skill's completeness checks.

## Developer instruction

When building deduction validation or evidence checks:

1. Consult the topic-specific knowledge files that incorporate rules from this regulation
2. Do not reference this regulation directly for specific thresholds or conditions -- those are extracted into topic-specific files
3. When a user asks "what evidence do I need?", the answer ultimately traces back to this regulation via the evidence-checklist knowledge file
4. If a deduction rule appears ambiguous, note the ambiguity and flag for human review rather than guessing

## Common failure

Do not treat this file as the source for specific deduction rules or thresholds. Detailed operational rules from this regulation are incorporated into topic-specific knowledge files (e.g., evidence-checklist, own-home rules). Always use those downstream files for implementation.
