# Rule note: VAT evidence, accounting basis, and deduction

source_ids: bd_vat_invoice_basis, bd_vat_cash_basis, bd_vat_cash_basis_eligibility, bd_vat_input_conditions, bd_vat_invoice_requirements, bd_vat_non_deductible, bd_vat_eu_supply_timing, bd_vat_icp
workflow: all
tax_year: 2025, 2026
status: preparation_only
last_verified: "2026-10-02"
review_status: needs_review

The official pages below were checked on 2 October 2026. Human specialist review is still pending.

## Evidence and period

Inspect each sales/purchase invoice for its required identifier and party details, invoice and supply dates, country, taxable base, VAT amount/rate, business purpose, and any reverse-charge or credit-note treatment. Use a local evidence ID as the working reference; retain country and relevant tax facts, but do not transcribe full invoice identifiers, names, addresses, VAT numbers, or other identifying numbers into conversation ledgers or saved workpacks. Check duplicate invoices at the source and record the result without copying their full identifiers. Separate VAT from profit or bank receipts. A bank debit alone does not prove deductible VAT.

Under the ordinary invoice basis, output VAT follows the invoice date. An invoice generally must be issued by the fifteenth day after the supply month; a late issue cannot defer VAT beyond the period in which it should have been issued. Advances, non-invoiced consumer supplies, continuous supplies, and private use can have different timing: resolve before assigning a period.

The cash basis applies only where applicable to the taxpayer's activities or otherwise authorized. Output VAT then follows actual receipts; using a bank export does not itself establish permission to use this basis. Some listed sectors use it by default and may document their choice to use the invoice basis. Resolve eligibility instead of choosing whichever produces less VAT.

Input VAT under both ordinary invoice and cash bases uses received purchase invoices and their invoice dates. The invoice must have been received before deduction. Do not wait for payment merely because output VAT uses the cash basis.

For purchases from other EU countries (acquirer side, bd_vat_eu_supply_timing): intracommunautaire services received use the period in which the service was supplied to the taxpayer; do not blindly apply a domestic invoice-date rule. EU goods acquisitions use invoice dates, limited by the fifteenth day after the supply month. Continuous reverse-charged services longer than a year need an annual timing check.

For the taxpayer's own supplies to EU business customers (supplier side), the authority is bd_vat_icp, not the acquisitions page: intra-Community supplies of goods are reported in the period of the invoice date, intra-Community services in the period in which the taxpayer supplied the service, and the transfer of call-off stock (voorraad op afroep) in the period in which transport of the goods began. The same timing applies to rubric 3b and the opgaaf ICP, which the separate ICP workflow prepares.

## Deductible input VAT

Confirm actual delivery to the entrepreneur, business use for taxable activities, and an invoice satisfying the applicable requirements. Ordinary invoices identify supplier and customer, addresses, invoice date/unique number, supplier VAT identifier, description/scope and supply date, taxable bases, rates, and VAT. Simplified invoices and cross-border invoices have distinct requirements; do not reject or approve them using the ordinary checklist alone.

Input VAT attributable to private, exempt, or non-taxable activities is not ordinary deductible VAT. Taxable zero-rated and supplier reverse-charged sales can support deduction. Split evidenced mixed business/private or taxable/exempt use; unresolved allocations require review. Foreign VAT is not Dutch 5b input VAT merely because the cost is business-related.

Restaurant food/drink VAT for final consumption is generally not deductible, including business meals. Gifts and staff benefits can need a separate annual limitation review. Reverse-charged VAT appears in the payable rubric first; include it in 5b only to the extent deduction conditions are independently satisfied. A KOR participant normally cannot claim it.

Never reconstruct VAT by dividing every business expense by 1.21. Confirm the actual invoice/rate, supplier treatment, and entitlement. VAT deductibility and income-tax cost deductibility are separate judgments.

## Official sources

- bd_vat_invoice_basis: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/btw_aangifte_doen_en_betalen/bereken_het_bedrag/hoe_berekent_u_het_btw_bedrag/factuurstelsel
- bd_vat_cash_basis: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/btw_aangifte_doen_en_betalen/bereken_het_bedrag/hoe_berekent_u_het_btw_bedrag/kasstelsel/
- bd_vat_cash_basis_eligibility: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/btw_aangifte_doen_en_betalen/bereken_het_bedrag/hoe_berekent_u_het_btw_bedrag/kasstelsel/voor_wie_geldt_het_kasstelsel
- bd_vat_input_conditions: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/btw_aftrekken/welke_btw_is_aftrekbaar/welke_btw_mag_u_aftrekken
- bd_vat_invoice_requirements: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/administratie_bijhouden/facturen_maken/factuureisen/factuureisen
- bd_vat_non_deductible: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/btw_aftrekken/welke_btw_is_aftrekbaar/welke_btw_mag_u_niet_aftrekken
- bd_vat_eu_supply_timing: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/zakendoen_met_het_buitenland/goederen_en_diensten_afnemen_uit_andere_eu_landen/aangifte_doen/factuurdatum_of_leverdatum/aangifte_doen_factuurdatum_of_leverdatum
- bd_vat_icp: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/zakendoen_met_het_buitenland/goederen_en_diensten_naar_andere_eu_landen/opgaaf_icp/opgaaf_icp
