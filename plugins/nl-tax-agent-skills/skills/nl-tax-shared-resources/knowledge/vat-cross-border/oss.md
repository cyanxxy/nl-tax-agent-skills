# Rule note: OSS Union, non-Union and IOSS preparation

source_ids: bd_oss_reporting, bd_oss_non_union, bd_oss_non_union_reporting, bd_oss_distance_threshold, bd_ioss_scope, eu_oss_scope, eu_oss_registration, eu_oss_declare_pay, eu_ioss_explanatory_notes, eu_ioss_customs_addendum_2026, eu_vat_directive_oss_currency
workflow: all
tax_year: 2025, 2026
status: preparation_only
last_verified: "2026-10-02"
review_status: needs_review

Public guidance was checked on 2 October 2026. Human tax-content review is
still required. Keep the schemes and years separate. The July 2026 revised
Commission guides include changes taking effect in 2027; those later rules
must not be applied to a 2025/2026 period. The 2026 customs addendum below is
applicable to the stated 2026 IOSS transactions, not 2025 supplies.

## Select an established scheme

OSS is the eenloketsysteem; the Belastingdienst calls the Union scheme the
Unieregeling, the non-Union scheme the niet-Unieregeling and IOSS the
Invoerregeling, and the return a btw-melding. OSS is optional, but once a scheme is used its covered supplies in all
relevant member states must be reported through it. OSS is additional to
domestic VAT obligations. Union reporting can cover intracommunity distance
sales and eligible B2C services; services in an EU state where the supplier
has a business/fixed establishment go through that state's domestic return.
Ordinary domestic goods sales are not distance sales; deemed-supplier cases
require separate review. Non-Union covers B2C services by a supplier with
neither its business nor a fixed establishment in the EU. IOSS covers
qualifying imported distance-sale consignments of intrinsic value no higher
than EUR 150, excluding excise goods. Goods already held in an EU warehouse
are not IOSS imports. Source: eu_oss_scope.

A Netherlands-established ZZP cannot choose non-Union merely because its
customer or supplier is outside the EU. Non-Union can be prepared for a
non-EU-established supplier whose registration identifies the Netherlands;
services may include Netherlands consumption. Source: bd_oss_non_union.

Confirm the actual member state of identification, registered scheme,
effective date and any intermediary appointment using the taxpayer's
confirmation. Union identification follows establishment rules; non-Union
identification can be chosen subject to eligibility. Non-EU IOSS intermediary
requirements and any applicable exception need confirmed evidence rather
than an assumption. Keep registration identifiers in the human's records.
The plugin does not enroll, deregister, change schemes or retroactively infer
participation. Source: eu_oss_registration.

## Destination and threshold screening

The combined annual EUR 10,000 threshold concerns qualifying cross-border
digital/TBE services and intracommunity distance sales, excluding VAT.
Confirm both current and preceding calendar-year amounts and any effective
election for destination taxation. It is not a per-country allowance, and
does not cover every B2C service or IOSS imports. Overseas fixed
establishments require review before applying the domestic threshold.
Exceeding it changes treatment; a small turnover figure alone proves neither
Dutch VAT nor OSS enrollment. Source: bd_oss_distance_threshold.

Northern Ireland (country code XI) is treated as part of the EU VAT area for
goods only, under the Windsor Framework; for services Northern Ireland is not
an EU country. Intra-Community distance sales of goods from the Netherlands
to consumers in Northern Ireland can therefore belong in the Union scheme
with consumption state XI. B2C services to Northern Ireland consumers are
never Union-scheme EU supplies, and United Kingdom code GB is never an OSS
consumption state. The OSS sources registered for this note do not state the
Union-scheme XI reporting treatment or how these sales count toward the
EUR 10,000 threshold. Do not drop these sales and do not relabel them as GB.
Keep every XI row under specialist review and record the named human-review
question: "Has an adviser or the Belastingdienst confirmed that these
Northern Ireland goods sales are Union-scheme distance sales reported under
code XI, and how they count toward the EUR 10,000 threshold?"

Record consumption country, supply type, dispatch country/service
establishment where relevant, date and taxable base. A country code alone
does not prove place of supply. Each country/category/rate row needs dated
evidence of the applicable rate and human/adviser confirmation for that
specific product/service and period. The plugin has no destination rate
catalogue and never selects a remembered rate. Keep exemptions and
zero-rated supplies separate; they are excluded from OSS current-supply rows.
Source for return exclusions: eu_oss_declare_pay.

## Period, currency and records

Union and non-Union use calendar quarters; IOSS uses calendar months.
Active registration requires a return even without covered supplies. The
return and payment are due by the end of the following month; returns cannot
be filed before the period ends. In the Netherlands reporting/payment is in
euros. When conversion is needed, use the ECB reference rate published for
the last day of the tax period (the quarter for Union and non-Union, the
month for IOSS). Preserve currency, dated rate, direction and converted
values; no remembered spot rate. Maintain related OSS/IOSS records for ten
years after the supply year. Source: bd_oss_reporting.

If the ECB published no reference rate on the last day of the tax period
(for example because it falls on a weekend or a TARGET holiday), use the
rate of the next day on which the ECB publishes. Never use an earlier date,
a bank rate or a remembered rate. Record which publication date applied.
Source: eu_vat_directive_oss_currency (Directive 2006/112/EC, articles 366(2)
for non-Union, 369h(2) for Union and 369u(2) for IOSS).

Non-Union likewise uses quarterly euro reporting, including nil periods,
and the same ECB conversion rule. A filed return is not filed again to correct
it; corrections go into the next declaration, within three years of the
date on which the original return had to be submitted (its due date), not
the date on which it was actually filed. After that window or ended participation, the human
needs the consumption state's correction route. Source:
bd_oss_non_union_reporting.

Do not deduct input VAT in OSS/IOSS. Keep domestic input VAT or foreign
refund obligations as separate review material. Dutch VAT whole-euro
rounding is not an OSS rule; preserve cents and obtain actual-form precision
confirmation. No bank account or unique payment reference is generated or
stored; the human obtains the genuine payment instructions from their
current declaration. Source for no input-tax deduction: bd_oss_reporting.

## Corrections and country balances

For a filed 2025/2026 return, corrections identify the original tax period,
consumption state and signed VAT adjustment in a later return. A later credit
note corrects the original supply period. Do not put that adjustment in both
current turnover and prior-period corrections. Current-supply totals cannot
be negative; a negative correction section can be. For each consumption
state, balance equals current VAT plus its own prior-period corrections.
A negative state's balance cannot offset another state's positive balance.
Calculate payable as the sum of positive country balances and show negative
balances separately for the relevant state's refund review. Keep original
declared totals, prior corrections already made, target corrected totals
and the remaining delta explicit to avoid reporting the same correction
twice. Source: eu_oss_declare_pay.

## IOSS and the 2026 customs change

For 2025/2026 IOSS, VAT on the supply is collected when the order payment is
accepted, rather than the later shipping/import date. Use the relevant
payment-acceptance record to allocate the reporting month. Source:
eu_ioss_explanatory_notes, section 4.2.9; this source's historical customs-duty
discussion does not establish 2026 customs treatment.

Confirm intrinsic consignment value and separately identified transport/
insurance charges. An order/consignment exceeding the scheme's limit,
excise goods or an unresolved marketplace/deemed-supplier role needs separate
review. IOSS cannot simultaneously be used for a supply exempt under KOR or
EU-KOR; do not terminate an exemption for the user. Source: bd_ioss_scope.

From 1 July 2026 the temporary EUR 3 customs duty is due at customs
declaration acceptance. It is not automatically part of the IOSS sale's VAT
base, but if charged to the customer at sale it becomes consideration and
is included. Obtain the sale/payment date, whether the duty was passed on
at sale, and a confirmed taxable-base breakdown. The plugin does not
calculate customs liabilities. Import VAT under non-IOSS routes has a
different base and is not an IOSS return amount. The addendum's announced
handling fee is prospective; do not treat a future proposal as already
charged or as a confirmed filing rule. Source:
eu_ioss_customs_addendum_2026, only when relevant to 2026.

## Official sources

- bd_oss_reporting: https://www.belastingdienst.nl/wps/wcm/connect/nl/btw/content/btw-melden-eenloketsysteem
- bd_oss_non_union: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/internationaal/btw_voor_buitenlandse_ondernemers/e_commerce_en_diensten/ik_lever_diensten_-_de_niet-unieregeling/
- bd_oss_non_union_reporting: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/internationaal/btw_voor_buitenlandse_ondernemers/e_commerce_en_diensten/ik_lever_diensten_-_de_niet-unieregeling/niet-unieregeling_btw_melden_en_betalen/
- bd_oss_distance_threshold: https://www.belastingdienst.nl/wps/wcm/connect/nl/btw/content/btw-diensten-particulieren
- bd_ioss_scope: https://www.belastingdienst.nl/wps/wcm/connect/nl/btw/content/btw-goederen-importeren-leveren
- eu_oss_scope: https://vat-one-stop-shop.ec.europa.eu/one-stop-shop_en
- eu_oss_registration: https://vat-one-stop-shop.ec.europa.eu/one-stop-shop/register-oss_en
- eu_oss_declare_pay: https://vat-one-stop-shop.ec.europa.eu/one-stop-shop/declare-and-pay-oss_en
- eu_ioss_explanatory_notes: https://vat-one-stop-shop.ec.europa.eu/document/download/3372e2f2-d5ec-46ea-a2ac-97bc4f5ec634_en?filename=vatecommerceexplanatory_notes_28102020_en.pdf
- eu_ioss_customs_addendum_2026: https://vat-one-stop-shop.ec.europa.eu/document/download/3086db0e-7b4a-4202-9f38-d32bd774f5a8_en?filename=20260821_VAT+guidelines-3+EUR+Customs+duty_revised.pdf
- eu_vat_directive_oss_currency: https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32006L0112
