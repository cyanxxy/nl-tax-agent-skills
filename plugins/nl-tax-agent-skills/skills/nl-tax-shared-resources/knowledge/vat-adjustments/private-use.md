# Rule note: VAT business/private use beyond cars

source_ids: bd_vat_private_use, bd_vat_mixed_investment_allocation, bd_vat_movable_private_use, bd_vat_computer_private_use, bd_vat_free_services
workflow: all
tax_year: 2025, 2026
status: preparation_only
last_verified: "2026-10-02"
review_status: needs_review

Draft source summary, requiring human tax-content review.

## Cost/asset treatment

Determine VAT allocation independently of IB allocation. Record an existing
documented allocation; never make the taxpayer's election. Distinguish ordinary
consumed purchases, movable capital goods, property, cars, withdrawals of stock,
and free services. Deduction for taxable business use is not a general permission
to deduct private or exempt expenditure.

For ordinary mixed business/private services and consumed goods, accept an
evidenced business/private split and deductible-VAT classification. Supported
arithmetic is eligible invoice VAT × business-use fraction × taxable fraction
of that business use. Keep both fractions' denominators explicit. If the
taxable fraction already describes all use, do not multiply the business share
again. Reconcile any earlier deduction against this final eligible amount.

For a movable capital good wholly allocated to the VAT business with purchase
VAT deducted, annual private-use cost base includes one fifth of acquisition
cost excluding VAT in first-use year and four following years. Time-apportion
that component for first-year/last-year availability (bd_vat_movable_private_use:
"tijdsevenredig"); add relevant annual use,
repair and maintenance costs excluding VAT on which VAT was deducted. Multiply
each rate-separated component by evidenced private-use fraction and its VAT
rate. After the window, only relevant ongoing costs remain. If purchase VAT
on the private part was excluded initially, do not add an acquisition private-
use charge on that excluded part. Cars and property follow their separate notes.

Before applying that ordinary purchase basis, ask whether financial lease or
huurkoop applies and compare documented acquisition/production cost with the
taxable acquisition/manufacturing base. If the cost is lower, the cited source
requires that taxable base instead. An unestablished lease classification or
taxable base blocks that component; do not automatically reuse purchase cost.

For confirmed taxable free services to the proprietor/family, the cost base can
include materials, staff labour and other costs without previously deducted
VAT. Do not use only claimed input VAT as the free-service output-tax base.
For a confirmed stock withdrawal use the documented source treatment of the
goods and applicable valuation; uncertain valuation/classification stays a
specific question. Staff/relationship gifts require BUA screening instead of
automatically stacking a private-use charge.

The helper can return an evidenced split or cost-based draft calculation;
missing allocation, cost base, rate, use evidence, or prior deduction blocks
only that affected line. Preserve unrounded components and distinct input/
output effects for the owner and mapper.

## Official sources

- bd_vat_private_use: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/btw_aftrekken/privegebruik/
- bd_vat_mixed_investment_allocation: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/btw_aftrekken/privegebruik/gemengd_gebruik/investeringsgoederen/investeringsgoederen
- bd_vat_movable_private_use: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/btw_aftrekken/privegebruik/gemengd_gebruik/investeringsgoederen/roerende_investeringsgoederen/
- bd_vat_computer_private_use: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/btw_aftrekken/privegebruik/gemengd_gebruik/investeringsgoederen/roerende_investeringsgoederen/voorbeeld_computer_geheel_bedrijfsvermogen
- bd_vat_free_services: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/btw_berekenen_aan_uw_klanten/waarover_btw_berekenen/diensten/btw_betalen_over_gratis_diensten
