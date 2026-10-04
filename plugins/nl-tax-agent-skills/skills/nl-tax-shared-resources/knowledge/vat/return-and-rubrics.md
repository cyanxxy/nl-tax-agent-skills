# Rule note: VAT return preparation and rubric mapping

source_ids: bd_vat_return_walkthrough, bd_vat_rubric_structure, bd_vat_return_obligation, bd_vat_return_deadlines, bd_vat_rounding, bd_vat_domestic_reverse_charge, bd_vat_eu_acquisitions, bd_vat_non_eu_services, bd_vat_icp, bd_zakelijk_login_machtigen
workflow: all
tax_year: 2025, 2026
status: preparation_only
last_verified: "2026-10-02"
review_status: needs_review

The official pages below were checked on 2 October 2026. Human specialist review is still pending. These notes support bounded preparation of a btw-aangifte (VAT return for omzetbelasting) for an entrepreneur established in the Netherlands; they do not establish final tax liability or authorize filing.

## Period, obligation, and deadline

Establish VAT registration, the actual assigned period, and any invitation or portal notice. A ready or received return must be submitted even where no tax is payable. A true nil return requires no reportable turnover, input VAT, reverse charge, acquisitions, or adjustments; a zero net result alone is insufficient. KOR and exclusively exempt activities need separate screening.

For Dutch resident entrepreneurs, quarterly return and payment deadlines are: Q4 2025, 31 January 2026; Q1 2026, 30 April 2026; Q2 2026, 31 July 2026; Q3 2026, 31 October 2026; Q4 2026, 31 January 2027. Monthly deadlines fall at the end of the following month. Annual 2025 and 2026 deadlines are 31 March 2026 and 31 March 2027. Verify the user's assigned period and official deadline. Foreign-established entrepreneur deadlines are different.

The current public deadline table starts at December/Q4 2025. For an earlier
2025 period, obtain the assigned historical deadline from the taxpayer's
notice or filing record instead of treating this current table as evidence.

## Supported entries

The official Stichting en Vereniging Loket corroborates the common rubric structure and ordinary 1a/1b/1e labels. Use that source for form structure only; its sector-specific conditions, such as a sports-canteen rate in 1c, do not establish a ZZP taxpayer's eligibility.

| Rubric | Prepared amount and condition |
| --- | --- |
| 1a | Domestic net sales and output VAT at an already confirmed 21% rate. |
| 1b | Domestic net sales and output VAT at an already confirmed 9% rate. The plugin does not decide an unfamiliar activity's rate. |
| 1d | An evidenced private-use adjustment from the bounded VAT-adjustments helper or confirmed adviser amount; unresolved classification/inputs stay blocked. |
| 1e | 'Leveringen/diensten belast met 0% of niet bij u belast': confirmed domestic supplies and services taxed at 0% or not taxed with the supplier, including domestic reverse charge to a Dutch business customer; net amount only. Exports (3a), supplies to or services in other EU member states (3b) and exempt supplies never go here. |
| 2a | Confirmed domestic purchases subject to reverse charge: taxable base and Dutch VAT payable by the recipient. |
| 3b | 'Leveringen naar/diensten in landen binnen de EU': net amount of confirmed intra-Community supplies of goods and services to business customers in other EU member states, the amount that the opgaaf ICP specifies (bd_vat_icp); no VAT column. Reconcile it with the separate ICP workflow; never place it in 1e. |
| 4a | Confirmed ordinary services from a non-EU supplier where Dutch reverse charge applies: base and self-assessed VAT. |
| 4b | Confirmed ordinary services from an EU supplier where Dutch reverse charge applies: base and self-assessed VAT. EU goods acquisitions require separate review. |
| 5a | Output/self-assessed VAT from rubrics 1–4; the online form calculates this. |
| 5b | Evidenced deductible input VAT, including deductible VAT self-assessed in 2a/4a/4b. Deduction is conditional, never automatic. |

Keep the calculated payable/refundable result separate from entered fields: 5a minus 5b. The current public resident walkthrough does not establish a universal 5c or 5g identifier for that result. Match the actual form's displayed total label; do not fabricate a numbered total field or reuse a historical form layout.

Detect outgoing cross-border supplies, export, EU customer transactions/ICP, foreign registration, OSS/IOSS, unusual rates, and import goods. Explain the missing review and retain evidence; do not mark the complete return ready until those classifications and separate obligations are resolved. Do not treat all overseas services as automatically subject to Dutch reverse charge.

## Rounding and handoff

Keep administration and reconciliation totals in cents and aggregate each rubric before rounding. Invoice VAT uses ordinary cent rounding with a consistent method. The current common-rubric guide requires all return amounts, including bases, in whole euros and permits rounding in the taxpayer's favour. The separate VAT rounding page confirms this for VAT amounts.

The sources do not prescribe a separate floor/ceiling algorithm for every base or negative adjustment. Show the cents totals and whole-euro entry amounts; document the user/adviser-confirmed base rounding method. If that method or a whole-euro base remains unresolved, keep the entry blocked until an adviser supplies or confirms it. Sum actual VAT independently from the administration; never recompute VAT from the rounded entry bases. Preserve minus signs for negative entries.

Draft preparation ends with an evidence-linked field map and a review of its
blockers. A manual-entry checklist with amounts remains unavailable until
human source-content review clears. The taxpayer controls login,
verification, transmission, payment, and saving the official confirmation.
Payment details must come from the actual return/notice rather than a
remembered bank account.

## Authorization for someone helping with business tax (machtigen)

A ZZP'er or eenmanszaak logs in to Mijn Belastingdienst Zakelijk with DigiD and can authorize a helper through DigiD Machtigen, stating clearly which business-tax matters the authorization covers. An intermediary such as a bookkeeper or adviser logs in with eHerkenning, which for an eenmanszaak needs a DigiD machtiging and for another business needs a ketenmachtiging (bd_zakelijk_login_machtigen). An authorization covers only the matters it names, so a machtiging for income tax alone does not cover the VAT return. When someone other than the taxpayer will review or file, the plugin only reminds the human to check that the right authorization exists; it never arranges an authorization and never asks for, accepts, stores or processes credentials.

## Official sources

- bd_vat_return_walkthrough: https://www.belastingdienst.nl/wps/wcm/connect/nl/btw/content/ik-moet-btw-aangifte-doen-hoe-vul-ik-die-in
- bd_vat_rubric_structure: https://stichtingenvereniging.belastingdienst.nl/aangifte/aangifte-omzetbelasting/invullen-rubrieken/
- bd_vat_return_obligation: https://www.belastingdienst.nl/wps/wcm/connect/nl/btw/content/moet-ik-altijd-btw-aangifte-doen
- bd_vat_return_deadlines: https://www.belastingdienst.nl/wps/wcm/connect/nl/btw/content/uiterste-aangifte-en-betaaldatums
- bd_vat_rounding: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/administratie_bijhouden/facturen_maken/btw-bedrag_afronden
- bd_vat_domestic_reverse_charge: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/btw_aftrekken/welke_btw_is_aftrekbaar/verlegde_btw_aftrekken
- bd_vat_eu_acquisitions: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/zakendoen_met_het_buitenland/goederen_en_diensten_afnemen_uit_andere_eu_landen/aangifte_doen/aangifte-doen-van-goederen-en-diensten-uit-andere-eu-landen
- bd_vat_non_eu_services: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/zakendoen_met_het_buitenland/zakendoen_buiten_de_eu/aangifte_doen_als_u_zakendoet_buiten_de_eu/aangifte_doen_als_u_diensten_afneemt_van_leveranciers_uit_niet_eu_landen
- bd_vat_icp: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/zakendoen_met_het_buitenland/goederen_en_diensten_naar_andere_eu_landen/opgaaf_icp/opgaaf_icp
- bd_zakelijk_login_machtigen: https://www.belastingdienst.nl/wps/wcm/connect/nl/home/content/hulp-inloggen-belastingdienst-zakelijk

## Extended preparation links

For private-use/pro-rata/revision/BUA/margin arithmetic the owning VAT skill
loads `../nl-tax-vat-adjustments/SKILL.md` and the relevant separately sourced
adjustment note. The helper can calculate a bounded line after classification
and inputs are confirmed; this general rubric note does not supply those
formulas. ICP/OSS uses separate owners, source notes and workpacks. These
extensions remain draft until source and applicable schema review/activation.
