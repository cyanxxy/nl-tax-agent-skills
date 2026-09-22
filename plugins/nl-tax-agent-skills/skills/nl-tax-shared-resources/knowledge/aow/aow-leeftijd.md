# Rule note: AOW-leeftijd (Dutch state-pension age) for routing

source_ids: svb_aow_leeftijd, rijksoverheid_aow_leeftijd, bd_heffingskortingen_aow_2025_2026
workflow: all
tax_year: all
status: active
last_reviewed: "2026-07-16"
review_status: reviewed

## Rule

The AOW-leeftijd (Dutch state-pension age) determines whether a taxpayer is
below AOW age all year, reaches it during the tax year, or has it for the whole
tax year. That distinction informs which Box 1 rate material and credit review
applies. These are workpack-preparation notes, not an AOW entitlement
determination.

## AOW-leeftijd by year

- **2025: 67 years.**
- **2026: 67 years.**
- The AOW age does **not** rise in 2027 (it stays 67). It rises to **67 years and 3 months in 2028** and stays 67 years and 3 months through **2031**.
- The AOW age is fixed for everyone born **before 1 October 1964**; for later birth dates it is provisional and follows CBS life-expectancy figures, set at least 5 years in advance.
- A person's exact AOW date depends on their date of birth (the SVB publishes the personal date and pays AOW monthly, around the 23rd).

## How to use in the workpack

1. From the sourced date of birth and tax year, record exactly one reviewed
   `aow_by_tax_year.<tax_year>.status` value under `person` or `partner`:
   `below_all_year`, `reaches_during_year`, or `aow_all_year`.
2. **`aow_all_year`** → use the whole-year AOW-age material for that tax year
   and review ouderenkorting. Review alleenstaandeouderenkorting separately
   against entitlement to an AOW pension for a single person; family or
   single-parent status does not establish it.
3. **`reaches_during_year`** → record the same year's `transition_month` from
   the sourced date of birth. Use the applicable annual or provisional
   year-specific note's published month rate; do not use either whole-year
   table. Do not interpolate an affected credit. Review the credit result in
   the active workflow's official environment: the annual income-tax return
   for annual work or `Verzoek of wijziging voorlopige aanslag` for provisional
   work. Mark affected credits for manual portal review.
4. **`below_all_year`** → use the standard non-AOW material for that tax year.

Older scalar `aow_age_in_tax_year`, `aow_status_in_tax_year`, and
`aow_transition_month` fields may remain in an existing profile for resume
compatibility, but they are not authoritative when more than one tax year is
active. Normalize them into the applicable year entry before use.

## Developer instruction

The conversational intake agent records `person.aow_by_tax_year.<tax_year>`
and the partner equivalent from the sourced date of birth, tax year, and this
reviewed rule. Store the classification with `source: calculated` and
`calculated_from`; do not invent an assumption or ask for a second confirmation
of undisputed date arithmetic. Ask the user only when the date of birth is
missing or disputed. Never collect or store the AOW administration number or
BSN.

## Common failure

Do not reduce AOW handling to a boolean. A taxpayer who reaches AOW age during
the year has a distinct, month-dependent position. Also do not assume a fixed
age of 67 for future years — 67 applies only through 2027; for 2028-2031 the
AOW age is fixed at 67 years and 3 months, and beyond 2031 it is provisional.
For tax years 2025 and 2026 specifically it is 67.
