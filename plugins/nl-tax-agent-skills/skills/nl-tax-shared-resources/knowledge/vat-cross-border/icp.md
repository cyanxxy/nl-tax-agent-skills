# Rule note: ICP preparation, period and reconciliation

source_ids: bd_vat_icp, bd_icp_periods, bd_icp_explanation_2025, bd_icp_explanation_2026, bd_icp_vat_id_checks
workflow: all
tax_year: 2025, 2026
status: preparation_only
last_verified: "2026-10-02"
review_status: needs_review

The official pages and current year-specific explanations below were checked
on 2 October 2026. Human tax-content review is required before review-ready
output. Use only the explanation for the declaration's year. The 2025 document
currently linked by the Belastingdienst was revised in June 2026; an older
search result is not its replacement.

## Scope and period

The opgaaf ICP (opgaaf intracommunautaire prestaties) specifies
intracommunautaire goods and services supplied to business customers
reporting VAT in another EU country. It is additional to the Dutch VAT return
(btw-aangifte). Own-goods movements and call-off stock (voorraad op afroep)
may also require ICP; they need their own classification and records.
Ordinary consumer sales are not automatically ICP. Services exempt or
zero-rated in the customer's country are excluded. No supplies in a period
normally means no ICP declaration, unlike an active OSS scheme's nil-return
obligation. An outstanding correction or official filing notice still needs
human follow-up. Source: bd_vat_icp. The register keeps the bd_vat_icp
snapshot with the domestic VAT notes in
`knowledge/vat/kor-and-special-cases.md`; it is still a source of this note.

Period timing for the taxpayer's own supplies: intracommunautaire goods
supplies go in the period of the invoice date; intracommunautaire services go
in the period in which the service was supplied; a call-off stock transfer
goes in the period in which the transport of the goods began. Source:
bd_vat_icp. The acquisition-side timing page (bd_vat_eu_supply_timing, about
goods and services bought from other EU countries) is not authority for ICP
supplies; route other unresolved timing questions to specialist review.

The year-specific explanations also exclude these services from the ICP:
services supplied under OSS (the eenloketsysteem); services connected with
immovable property, such as letting and maintenance; passenger transport;
services giving admission to cultural, artistic, sporting, scientific,
entertainment or educational events; restaurant and catering services; and
the short-term hire of a means of transport for a continuous period of at
most 30 days, or at most 90 days for a ship. Keep such services out of ICP
rows and out of the ICP side of the btw-aangifte rubric 3b reconciliation.
Sources: bd_icp_explanation_2025 and bd_icp_explanation_2026, selected by year.

A supply of a new or nearly new means of transport (nieuw vervoermiddel)
from the Netherlands to a private person or a non-taxable legal person in
another EU country is an intracommunautaire levering, but it cannot be
entered in the ICP because the customer has no VAT ID. The human sends a copy
of the sales invoice with a covering letter to the Belastingdienst/Central
Liaison Office instead. The ICP explanations do not name the btw-aangifte
rubric for this supply, so its btw-aangifte rubric is a named
specialist-review item (new means of transport rubric review); do not place
it in a btw-aangifte rubric from this note. If the btw-aangifte rubric 3b
total compared with the ICP includes such a supply, record the difference it
causes against the ICP rubric 3 total under that specialist-review item, not
as an explained or closed difference. Sources: bd_icp_explanation_2025 and bd_icp_explanation_2026, selected by
year.

Goods can be reported monthly; quarterly reporting requires goods not to
exceed EUR 50,000 in that quarter and each of the preceding four quarters.
Annual reporting requires a permit. Services can be reported monthly or
quarterly, or annually with a permit. Goods and services may have separate
frequencies; a combined declaration follows goods rules. If the goods
threshold is crossed in the first, second or third month, the transition
respectively uses three monthly declarations, a first-two-month declaration
plus the final month, or a full-quarter declaration followed by monthly
reporting. Do not relabel the two-month period as one month. After four
consecutive quarters below the threshold, quarterly reporting can resume in
the fifth quarter if it also remains below the threshold. Source:
bd_icp_periods.

For a Netherlands-established entrepreneur the year-specific explanations
give filing deadlines at the end of the following month, including 31 January
following an annual ICP period. Foreign-established ICP deadlines differ.
Confirm establishment and exact assignment; ordinary annual VAT deadlines
do not establish annual ICP deadlines. Sources: bd_icp_explanation_2025,
bd_icp_explanation_2026, selected by year.

## Customer verification and data minimization

A real declaration needs the actual customer's VAT ID, not an alias. The
taxpayer or authorized human checks the actual ID in the European Commission's
VAT verification service, confirms the customer's business details as
available, and preserves the result in their own administration. Invalid IDs
or conflicting details require follow-up; service unavailability is not a
successful check. The Belastingdienst notes that Germany's name/address
check is unavailable, while a valid ID there can establish business status.
Source: bd_icp_vat_id_checks.

The plugin retains a stable customer alias, country and the human's dated
verification result with provenance. It does not store actual VAT IDs,
personal names/addresses or verification request identifiers. An alias-only
workpack is never a self-contained filing dataset. Missing actual-ID
verification blocks the affected row; even when verified, the human retrieves
and enters the genuine ID from their administration separately. The plugin
must state that limitation beside its draft banner and map.

## Current supplies, credit notes and correction errors

The year-specific explanations separate ordinary ICP goods/services in ICP
rubric 3a from simplified triangular supplies in ICP rubric 3b. Do not confuse
these ICP form rubrics with the btw-aangifte rubrics: btw-aangifte rubric 3a
covers supplies to countries outside the EU, and btw-aangifte rubric 3b covers
supplies to and services in other EU countries. Goods use invoice timing;
services use the supply period rather than invoice timing. Northern Ireland's
XI treatment covers goods, not services. The ICP rubric 3 total (ICP 3a plus
ICP 3b) over all ICP declarations for the same dates must equal btw-aangifte
rubric 3b for that coverage, even when filing frequencies differ; own-goods
transfers appear in both. Sources: bd_icp_explanation_2025 and
bd_icp_explanation_2026, selected by year.

An error in an earlier declaration uses ICP correction rubric 2a (ordinary
goods/services) or ICP rubric 2b (simplified triangulation), in the next
opgaaf ICP. No OSS-style three-year window or consumption-state route applies
to ICP corrections. Record original period, customer alias, original declared
amount, corrected amount and signed difference. An incorrect customer ID needs reversal under the old identity
and a matching positive row under the correct identity; actual IDs remain
with the human. Credit notes for cancellations or price reductions belong
in current ICP rubric 3, not automatically in the error-correction section.
Sources: bd_vat_icp for correcting in the next opgaaf ICP, and
bd_icp_explanation_2025 and bd_icp_explanation_2026, selected by year.

The workpack records raw cents, any human-confirmed form rounding, and each
explained difference. These sources do not establish a universal favorable
rounding algorithm for ICP; do not import Dutch VAT or OSS rounding rules.
Simplified triangulation, own-goods transfers, call-off stock, fiscal units,
nonstandard two-month transitions and foreign-established declarations stay
under specialist review until their specific classification and form coverage
are supplied. Preserve their figures without silently treating them as
ordinary ZZP services or declaring the complete period ready.

## Official sources

- bd_vat_icp: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/zakendoen_met_het_buitenland/goederen_en_diensten_naar_andere_eu_landen/opgaaf_icp/opgaaf_icp
- bd_icp_periods: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/zakendoen_met_het_buitenland/goederen_en_diensten_naar_andere_eu_landen/opgaaf_icp/tijdvak_opgaaf_icp/
- bd_icp_explanation_2025: https://download.belastingdienst.nl/belastingdienst/docs/toelichting-digitale-opgaaf-intracomm-pres-ob1291t53fd.pdf
- bd_icp_explanation_2026: https://download.belastingdienst.nl/belastingdienst/docs/toelichting-digitale-opgaaf-intracomm-pres-ob1291t62fd.pdf
- bd_icp_vat_id_checks: https://www.belastingdienst.nl/wps/wcm/connect/nl/btw/content/btw-id-controleren
