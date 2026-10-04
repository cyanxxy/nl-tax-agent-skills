# Rule note: KOR and VAT review boundaries

source_ids: bd_vat_kor, bd_vat_kor_effects, bd_vat_kor_conditions, bd_vat_kor_withdrawal, bd_vat_icp, bd_vat_private_use, bd_vat_logies_2026, law_wet_ob_1968
workflow: all
tax_year: 2025, 2026
status: preparation_only
last_verified: "2026-10-02"
review_status: needs_review

The official pages below were checked on 2 October 2026. Human specialist review is still pending.

## KOR screening

The Dutch KOR (kleineondernemersregeling) is a VAT exemption available subject to conditions. The business must be established in the Netherlands, and its turnover in the Netherlands (jaaromzet in Nederland) must be no more than EUR 20,000 both in the calendar year concerned and in the preceding calendar year (bd_vat_kor_conditions: the maximum applies to the calendar year of registration and to the calendar year before it). Turnover for this test is defined by Wet OB article 25 (law_wet_ob_1968) and the KOR conditions page, not by total business revenue: it counts supplies taxed with Dutch VAT (including the 0% rate and domestic reverse-charge supplies) and certain exempt turnover named on that page, and it leaves out, among other items, private-use VAT, sales of business assets used in the business, supplies taxed in another country and intra-Community acquisitions. Apply that definition from the source page rather than a paraphrase, and keep an unclear item as a human-review question. Turnover of all subnumbers of the same entrepreneur is added together.

Turnover below that ceiling does not mean the taxpayer automatically participates. Request the actual participation confirmation and effective dates, and ask for the prior calendar year's turnover in the Netherlands as well as the current year's. Never apply KOR retroactively from turnover alone or make an election for the user.

During participation the entrepreneur normally charges no VAT, makes no regular returns, and deducts no input VAT. Incidental returns can nevertheless be required, including foreign purchases subject to reverse charge. A return already issued must still be handled. Multiple activities/subnumbers of the same entrepreneur do not provide separate KOR turnover allowances.

Exceeding EUR 20,000 ends the exemption immediately: the entrepreneur must deregister at that moment, and the supply that causes the excess is itself already taxed with VAT (bd_vat_kor_withdrawal). After a threshold breach the entrepreneur is excluded from the KOR for the rest of that calendar year and for the following calendar year (Wet OB article 25a, paragraph 9; law_wet_ob_1968). Voluntary withdrawal (afmelden) is possible while turnover stays within the ceiling. The withdrawal page says it takes effect only from the first day of a filing period (aangiftetijdvak) and must be notified at least four weeks before the chosen date; Wet OB article 25a, paragraph 7 (law_wet_ob_1968), words the effective date as the first day of the next calendar quarter that starts at least four weeks after the notice is received. When those two descriptions could give different dates for a monthly filer, keep the effective date as a human-review question and use the date in the Belastingdienst confirmation. After a voluntary withdrawal, re-entry is barred for the rest of that calendar year and the following calendar year. The former three-year minimum participation period no longer applies from 1 January 2025; do not apply it. Joining/leaving may trigger revision of previous deductions. These transitions require specialist review; do not produce a complete ordinary-return map from incomplete participation facts.

EU-KOR exists from 1 January 2025 and is a separate scheme. Do not confuse Dutch KOR, EU-KOR, a sector exemption, the 0% rate, and reverse charge.

## Special cases and separate filings

EU business customer supplies may require opgaaf ICP in addition to VAT returns. The ICP totals reconcile to the relevant VAT 3b amount for the same period; goods and services can have different reporting periods. The VAT return does not fulfil ICP. Detect export, installation/distance supplies, EU consumer services, foreign establishment, OSS/IOSS, and special place-of-supply cases before routing.

Private use, gifts/staff benefits, investments and deduction revisions, vehicles, real estate, margin schemes, and cessation can require adjustments or separate rules. The VAT owner can invoke the bounded VAT-adjustments helper with the relevant sourced note and complete inputs; otherwise obtain confirmed adviser figures and keep the affected classification open. Property elections and disputed facts are never chosen by the helper. An unresolved adjustment prevents a ready label for the affected period, particularly the last return of the calendar year.

Confirm the actual activity's rate for each relevant year. For example, ordinary short-stay accommodation changed to 21% on 1 January 2026, including special advance-payment treatment; a prior-year 9% categorization must not be carried forward without review. Unfamiliar rate categories or combined supplies require review.

## Official sources

- bd_vat_kor: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/hoe_werkt_de_btw/kleineondernemersregeling/kleineondernemersregeling
- bd_vat_kor_effects: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/hoe_werkt_de_btw/kleineondernemersregeling/wat-betekent-meedoen-met-de-kleineondernemersregeling/wat-betekent-meedoen-met-de-kleineondernemersregeling
- bd_vat_kor_conditions: https://www.belastingdienst.nl/wps/wcm/connect/nl/btw/content/kor-voorwaarden
- bd_vat_kor_withdrawal: https://www.belastingdienst.nl/wps/wcm/connect/nl/btw/content/afmelden-kor
- bd_vat_icp: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/zakendoen_met_het_buitenland/goederen_en_diensten_naar_andere_eu_landen/opgaaf_icp/opgaaf_icp
- bd_vat_private_use: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/btw_aftrekken/privegebruik/
- bd_vat_logies_2026: https://www.belastingdienst.nl/wps/wcm/connect/nl/btw/content/btw-logies
- law_wet_ob_1968: https://wetten.overheid.nl/BWBR0002629/2026-01-01
