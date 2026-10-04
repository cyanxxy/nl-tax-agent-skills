# Rule note: Margin goods, individual/global methods and reconciliation

source_ids: bd_vat_margin_goods, bd_vat_margin_calculation, bd_vat_margin_return, bd_vat_margin_method, bd_vat_margin_losses, bd_vat_margin_year_balance, bd_vat_margin_next_year
workflow: all
tax_year: 2025, 2026
status: preparation_only
last_verified: "2026-10-02"
review_status: needs_review

Draft source summary; human tax-content review is required.

## Eligibility and existing method

Confirm reseller status, goods and supplier eligibility, absence of earlier
deduction, and existing method. Buying an ordinary business asset without VAT
does not alone make all its sale proceeds reseller margin sales. Art/antiques/
collectibles, imports and special items can require distinct treatment.
Margin invoices do not separately show deductible VAT.

The global method is mandatory for the cited categories: vehicles, clothing,
furniture, books/periodicals, photo/film/video equipment, image/sound media,
musical instruments, domestic/electrical/electronic equipment, pets, art,
antiques/collectibles, and their used parts/accessories. Other goods ordinarily
use the individual method. A permitted switch needs the established treatment;
do not choose whichever produces the smaller amount. Auctioneers/agents acting
on commission cannot simply use globalisation. Preserve a source-confirmed
method switch or special classification as a distinct fact.

## Bounded arithmetic

Individual method: for each eligible item, gross margin = sale price minus
linked purchase price. Sum positive margins only; losses on individual items
do not offset positive items. Split purchase of a bundle among items using
documented expected-sales-value proportions. Group by applicable VAT rate.
VAT = positive gross margin × r/(1+r); net margin = gross margin − VAT.
`r` is a confirmed decimal fraction from the VAT-rate note, never an invented
rate. Do not treat VAT on repairs as an extra margin-goods purchase price
without the applicable repair treatment.

Global method: for each rate pool, gross margin = period eligible margin-sales
receipts minus eligible margin purchases in that same period, not merely cost
of items sold. Deduct a documented unused negative same-year prior-period
margin of that pool. A remaining positive amount uses r/(1+r); a nonpositive
amount creates no negative VAT/refund for that period and remains a separately
tracked loss. Never offset normal VAT turnover or another rate pool's positive
margin. Do not reuse a loss already consumed.

For global annual reconciliation, sum positive and negative period margins
per rate pool. Calculate VAT on max(annual margin,0) and compare with VAT
already accounted for in that year. An established difference may support
a repayment request; it is not permission to put a negative margin in ordinary
turnover. VAT already paid in a year whose annual balance (jaarsaldo) is lower
or negative is reclaimed by a written repayment request (a letter) that the
taxpayer sends to the tax office (bd_vat_margin_year_balance).

A negative annual balance can be offset against a positive annual balance of
the next year, not against next year's first quarter or another single period,
and only after the Belastingdienst has determined (vastgesteld) that negative
balance at the taxpayer's request (bd_vat_margin_next_year). The taxpayer asks
for that determination by sending a letter to the tax office at the same time
as the VAT return for the first filing period of the following year. Without
that determination, the negative balance can never be offset against a future
positive annual balance. When the next year's annual balance is also negative,
it is added to the earlier negative balance and the taxpayer must ask again for
the combined negative balance to be determined. When a negative balance cannot
be fully offset against the next year's positive balance, the taxpayer must ask
for the remaining negative amount to be determined, again with the return for
the first filing period of the following year.

When the owner prepares the final period of a year with a negative annual
balance, or the first filing period of the next year, return both human-only
steps (the repayment request and the vaststelling request) as dated open
questions, naming the first-period return as the deadline for the vaststelling
request. Use a carried-forward negative balance in a cross-year calculation
only with documentary evidence of the Belastingdienst determination. Never
draft, send, or automate either request; the taxpayer or an authorized human
sends every letter.

For a margin-sale return, the left rubric-1 column uses the net margin and
the right uses margin VAT, added to ordinary amounts in the corresponding
rate bucket. Keep gross selling receipts separately for scheme thresholds;
KOR turnover is not merely the profit margin. When goods/method/rate/unused
loss or balance evidence is uncertain, block that line and continue established
arithmetic for other pools.

## Official sources

- bd_vat_margin_goods: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/bijzondere_regelingen/margeregeling/wat_zijn_margegoederen/
- bd_vat_margin_calculation: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/bijzondere_regelingen/margeregeling/margegoederen/btw_berekenen_bij_margegoederen
- bd_vat_margin_return: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/bijzondere_regelingen/margeregeling/margeregeling_aangifte_doen/aangifte_doen_bij_handel_in_margegoederen
- bd_vat_margin_method: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/bijzondere_regelingen/margeregeling/administratie_bijhouden_bij_handel_in_margegoederen/administratie_bijhouden_bij_handel_in_margegoederen
- bd_vat_margin_losses: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/bijzondere_regelingen/margeregeling/margeregeling_aangifte_doen/negatieve_winstmarge_verrekenen/negatieve_winstmarge_verrekenen
- bd_vat_margin_year_balance: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/bijzondere_regelingen/margeregeling/margeregeling_aangifte_doen/negatieve_winstmarge_verrekenen/vaststellen_van_het_jaarsaldo
- bd_vat_margin_next_year: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/bijzondere_regelingen/margeregeling/margeregeling_aangifte_doen/negatieve_winstmarge_verrekenen/negatief_jaarsaldo_verrekenen_met_een_positief_jaarsaldo_in_het_volgende_jaar
