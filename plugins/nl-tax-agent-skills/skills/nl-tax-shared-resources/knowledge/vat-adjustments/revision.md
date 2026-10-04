# Rule note: VAT revision of capital goods and investment services

source_ids: bd_vat_capital_revision, bd_vat_investment_services, bd_vat_investment_services_regulation, bd_vat_kor_revision, bd_vat_property_revision, bd_vat_deduction_policy, bd_vat_deduction_policy_amendment_2026, law_uitvoeringsbeschikking_ob_1968
workflow: all
tax_year: 2025, 2026
status: preparation_only
last_verified: "2026-10-02"
review_status: needs_review

Draft source summary; human tax-content review is required.

## First use and later years

Collect item VAT invoiced, deduction already claimed net of prior changes,
documented VAT asset allocation, acquisition and first-use dates, first-use-year
final deductible fraction, current-year fraction and any disposal. Movable
capital goods are followed for five bookyears including first-use year;
property for ten. First-use and first-use-year-end reconciliation uses the full
eligible invoiced VAT, not one fifth/tenth. Delta is full final entitlement
minus net deduction already claimed; no later-year tolerance is silently
applied at these initial reconciliation stages.

For an ordinary later year inside the window, use annual share = eligible
invoiced VAT / window years. Preliminary delta = annual share × (current final
deductible fraction − original first-use-year final fraction). Herziening is
required when the absolute fraction difference exceeds 10% of the original
fraction, not ten percentage points. Equality is within tolerance. Original
fraction zero and later entitlement above zero therefore requires checking
revision, subject to VAT business allocation and eligibility. Do not substitute
last year's use for the original baseline. Positive adjustment adds input VAT
in 5b; a repayment may be declared as extra VAT under rubric 1. Establish the
correct subrubric with the source and mapper rather than inventing one.

For a confirmed disposal (doorlevering) inside the window, split the bookyear
of delivery at the delivery date (deduction decree Stcrt. 2020, 63000,
paragraph 4.2.8, and Uitvoeringsbeschikking omzetbelasting 1968 articles 13
and 13a):

- From the start of that bookyear to the delivery date is an ordinary later-year
  revision for the shift in taxable and exempt use during that part of the year.
  It is declared in the return for the final filing period of that bookyear
  (art. 13, second and third paragraphs). The cited sources do not give a worked
  formula for this part. This note uses annual share × elapsed fraction of the
  bookyear × (actual deductible fraction in that part − original first-use-year
  fraction), subject to the 10% tolerance, so that together with the one-time
  remainder each part of the window is revised exactly once. Name the
  elapsed-fraction pro-rating as a source-content review point in the return
  packet.
- From the delivery date to the end of the window (the remaining fractional
  bookyears) is revised once, in the return for the filing period in which the
  delivery takes place (art. 13a, second paragraph). The taxpayer is deemed to
  use the item until the end of the window only for taxable activities when the
  delivery is taxed or is a supply for which no VAT is due but the right to
  deduct is kept under article 15, second paragraph, of the Wet OB 1968, and
  only for activities without a right to deduction when the delivery is
  otherwise exempt. Remainder = eligible invoiced VAT × remaining
  fractional bookyears / window years × (deemed fraction − original fraction).
- Never apply a full-year annual share in the year of delivery, and never
  include the period after delivery in an annual revision as well. Art. 13a
  refers only to art. 13, second and third paragraphs, and not to the fourth
  paragraph with the 10% tolerance; no cited source states outright whether the
  tolerance applies to the one-time remainder, so return any wish to apply it
  there as a human-review question rather than applying it.

Classification of a business transfer (article 37d of the Wet OB 1968),
new-building reconstruction, or the disposal-date fraction needs review when
not established.

## Investment services from 2026

The effective legal amendment includes a qualifying service's remuneration
of at least EUR 30,000 excluding VAT, not only amounts above it. It covers
multi-year-benefit services to property, including renovation/maintenance,
associated demolition and incorporated installations. Apply the threshold to
the actual service; do not divide by invoice, supplier instalment, or property
unit merely to fall below it. A service below the threshold still has ordinary
first-use/year-end deduction reconciliation.

For a VvE service, the 2026 amendment tests the threshold at the association,
not against an individual member's contribution. Establish whether the VvE
acquired the service as an entrepreneur, whether the member-deduction approval
applies, and the documented contribution/deduction share. Missing facts block
that VvE line; do not silently treat the member's share as a separate service.
The amendment (Stcrt. 2026, 29217) took effect on 25 August 2026. Its VvE
acquisition condition (the association did not acquire the goods or services as
an entrepreneur) is described by the decree as a clarification that also covers
existing situations, so it may be applied to an open 2025 or 2026 period.
Testing the EUR 30,000 threshold at association level applies only to
investment services under the regime for services first used on or after
1 January 2026.

The new five-bookyear schedule starts with first use on/after 1 January 2026.
An invoice or contract begun in 2025 may qualify when actual first use is in
2026. Mere temporary/incidental use is not necessarily first durable use.
First-use-year reconciliation uses full VAT; the following four years use one
fifth. Keep every service schedule separate from the property's ten-year
acquisition schedule. Works creating a new building or an asserted longer
economic-life/EU-law treatment require a specific classification decision.
Do not apply the new five-year service regime to a service first used in 2025.

## KOR and source conflict checks

For revision caused by starting/stopping KOR, the additional exemption is
aggregate revision around the EUR 500 boundary in the bookyear for investments first used in
earlier years. It is not a per-asset allowance or an exemption for first-use
full-VAT reconciliation. Uitvoeringsbeschikking omzetbelasting 1968 article 13,
fourth paragraph (version in force from 1 April 2026), and the public KOR
guidance omit KOR-caused revision only when the total revision amount in that
bookyear is less than EUR 500 ("minder is dan € 500"). The 2020 deduction
decree, paragraph 3.4.4, says "not more than EUR 500". At exactly EUR 500 the
regulation text requires the revision. Whether the decree wording can be relied
on at exactly EUR 500 is a human-review question: return it as one and do not
silently omit the revision. Establish participation dates and aggregate
coverage before using any exemption.

The property guidance's later-year example says 80% current use but calculates
70%. Return that inconsistency if relying on the example. The formula in this
note and the capital-revision source supply consistent arithmetic; do not copy
the conflicting example amount as an authoritative result.

## Canonical repository parity data

```yaml
vat_adjustment_policy:
  movable_revision_years: 5
  property_revision_years: 10
  service_revision_years: 5
  revision_tolerance_fraction: '0.10'
  investment_service_threshold_ex_vat: '30000'
  investment_service_effective_year: 2026
  kor_revision_aggregate_boundary: '500'
  kor_revision_omitted_only_below_boundary: true
  kor_revision_equality_requires_source_review: true
```

## Official sources

- bd_vat_capital_revision: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/btw_aftrekken/belaste_en_vrijgestelde_omzet/inschatting_van_het_gebruik2/herziening_aftrek_bij_investeringsgoederen2/herziening_aftrek_bij_investeringsgoederen
- bd_vat_investment_services: https://www.belastingdienst.nl/wps/wcm/connect/nl/btw/content/btw-aftrek-investeringsdiensten
- bd_vat_investment_services_regulation: https://zoek.officielebekendmakingen.nl/stcrt-2024-41523.html
- bd_vat_kor_revision: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/hoe_werkt_de_btw/kleineondernemersregeling/wat-betekent-meedoen-met-de-kleineondernemersregeling/moet-ik-mijn-btw-aftrek-herzien-vanwege-de-kleineondernemersregeling
- bd_vat_property_revision: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/onroerende_zaken/herziening_btw/
- bd_vat_deduction_policy: https://zoek.officielebekendmakingen.nl/stcrt-2020-63000.html
- bd_vat_deduction_policy_amendment_2026: https://zoek.officielebekendmakingen.nl/stcrt-2026-29217.html
- law_uitvoeringsbeschikking_ob_1968: https://wetten.overheid.nl/BWBR0002634/
