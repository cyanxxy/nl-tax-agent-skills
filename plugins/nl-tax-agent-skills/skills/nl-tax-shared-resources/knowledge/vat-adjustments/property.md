# Rule note: Property VAT classification and bounded adjustment support

source_ids: bd_vat_property_delivery, bd_vat_property_delivery_option, bd_vat_property_rent_option, bd_vat_property_private_use
workflow: all
tax_year: 2025, 2026
status: preparation_only
last_verified: "2026-10-02"
review_status: needs_review

Draft source summary; human tax-content review is required.

## Sales and rental classification

Property supplies are normally exempt, with mandatory taxable delivery of a
building before/on/within two years of first use, building land and new-building
completion. Confirm first-use dates and legal new-building/building-land status;
ordinary expenditure value alone proves neither. Business-transfer and limited-
rights cases require their own classification.

For an otherwise exempt sale, an option for taxable delivery is joint and must
be documented before delivery. The purchaser generally needs at least 90%
deductible use, or 70% for the specified sectors in the cited option source.
KOR by either side prevents that option. A qualifying use percentage is not
proof of an option. Do not choose it, prepare an election, or assume a building
included in a business transfer can use the ordinary option.

Rental generally requires its own exemption/exception classification. A
taxable rental option needs a VAT-business tenant, documented election and
qualifying deductible use: at least 90%, or 70% for employers' organisations,
property agents, travel agencies, occupational-health services, postal
businesses and public radio/television organisations. Residential-use space
cannot use the option; KOR prevents it. Check each independent portion and
written tenant declaration. Short-term accommodation/parking/other statutory
exceptions need the relevant separate treatment. A fact change may invalidate
an earlier option and cause invoice/deduction corrections.

## Private use and revision

For property acquired from 2011, do not deduct VAT for private use simply
because the whole property is VAT business property. Use the evidenced taxable
business-use allocation on acquisition and ongoing costs. A wholly VAT-business-
allocated property's later private-use change can revise acquisition deduction
over its ten-year window. A private allocation initially excluded from VAT
business property does not later create extra acquisition deduction merely
because business use grows. Historical pre-2011 treatment needs specialist
classification.

After treatment is established, calculate invoice VAT × accepted deductible-use
fraction and full initial entitlement reconciliation; use `revision.md` for
later years/disposal. Keep property VAT, investment-service VAT, rent/output
VAT, and any transfer-tax question separate. Missing election or property
classification blocks that position, not unrelated confirmed calculations.

## Official sources

- bd_vat_property_delivery: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/onroerende_zaken/levering_onroerende_zaak/levering_van_een_onroerende_zaak
- bd_vat_property_delivery_option: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/onroerende_zaken/levering_onroerende_zaak/belaste_levering/voorwaarde_voor_belaste_levering
- bd_vat_property_rent_option: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/onroerende_zaken/verhuur_onroerende_zaak/belaste_verhuur/voorwaarden_belaste_verhuur/
- bd_vat_property_private_use: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/btw_aftrekken/privegebruik/gemengd_gebruik/investeringsgoederen/onroerende-zaken
