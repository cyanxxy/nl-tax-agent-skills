# Rule note: VAT correction and suppletie preparation

source_ids: bd_vat_corrections, bd_vat_suppletie_explanation, bd_vat_return_deadlines
workflow: all
tax_year: 2025, 2026
status: preparation_only
last_verified: "2026-10-02"
review_status: needs_review

The official pages below were checked on 2 October 2026. Human specialist review is still pending.

## Determine the correction

Collect the original filed return(s), period, corrected full totals per rubric, discovery date, and supporting evidence. Calculate the net VAT difference separately from changes to individual sales/input rubrics. A previously prepared workpack does not establish what was actually filed.

For a net VAT correction of EUR 1,000 or less, the ordinary route is to adjust the corresponding rubrics of the next (eerstvolgende) VAT return after discovery: add or subtract the amount in the rubric where it normally belongs, for example adding EUR 100 to 5b. Do not choose a later return than the next one, and do not enter the net difference into an invented single correction field. Document original period, each rubric change, and resulting net effect so the next period remains reconcilable.

For a correction exceeding EUR 1,000, prepare a suppletie (Suppletie btw, correctie btw-aangifte). Correct promptly and within eight weeks of discovering the error. The eight-week requirement was introduced on 1 January 2025; do not assume year-end accounts or the five-year correction window permit waiting. Record the discovery-date evidence and escalate immediately if the deadline is near or passed. Even correction within eight weeks does not promise immunity if the tax authority discovers the error first.

## When the original period's deadline has not yet passed

If the original return was filed but that period's official filing and payment deadline (the deadline table in return-and-rubrics.md, source bd_vat_return_deadlines, or the taxpayer's own notice) has not yet passed, the suppletie explanation directs use of the Suppletie btw form. Any additional VAT is then paid before that period's final payment date using that period's own payment reference (betalingskenmerk) from the genuine return or notice; no naheffingsaanslag is awaited in this case. The explanation does not say whether a correction of EUR 1,000 or less made while the original deadline is still open may instead go into the next return; keep that point as a named human-review question. Source: bd_vat_suppletie_explanation.

## Suppletie is corrected totals, not rubric deltas

Use corrected full totals for the corrected period in every rubric, including those that did not change. The period entered on the form begins on the first day and ends on the last day of a month. Enter the earlier declared net VAT total in the form's separate field "Totaalbedrag eerdere btw-aangifte over dit tijdvak". The form then shows the corrected end total (Eindtotaal) and the additional payable or refundable difference (Totaal te betalen or terug te vragen). Keep all three concepts explicit: originally declared total, corrected total, and net change.

The official current explanation permits correcting one period (month, quarter or year) or, when errors are found only later, such as when the annual accounts are prepared, a complete calendar or financial year with the correct figures for the whole year. These skills prepare one correction per originally assigned and filed period. The whole-year suppletie option may be mentioned to the taxpayer as an official option, but these skills do not prepare it: a whole-year suppletie by a monthly or quarterly filer is a human-review route and is never prepared under the `Y` period token, which means only an annual assigned filing period. Ordinary corrections can be made through the fifth year following the relevant year, including after cessation. This is a correction window, not a substitute for prompt filing.

## After a suppletie

Once the original period's deadline has passed, a suppletie showing additional VAT due results in a naheffingsaanslag, usually within eight weeks: wait for it and pay using its own payment details. A suppletie showing less VAT results in a teruggaafbeschikking, usually within eight weeks. Do not reuse ordinary-return payment instructions or an unrelated payment reference.

If an already filed suppletie is wrong, do not file a new one: wait for the resulting naheffingsaanslag or teruggaafbeschikking and lodge an objection (bezwaar) within six weeks of its date. Exception: if that suppletie produced no payment and no refund, no decision is sent, and a corrected suppletie must be submitted instead. The human prepares and lodges any objection.

## Cases where the suppletie form is not used

The Suppletie btw form is not used for (a) a refund of an intra-Community acquisition already declared in both the Netherlands and another EU member state, or (b) a margin-scheme refund through annual globalisation (jaarglobalisatie). Both are requested by letter to the taxpayer's tax office, and a refund of EUR 1,000 or less in these cases may not be offset in the next return. A suppletie that changes rubric 3b must be followed by a letter giving the 3b change to Belastingdienst/Central Liaison Office; a change to rubric 3b only uses that letter alone and no suppletie. These letters are prepared and sent by the human. ICP-only changes and other special schemes require separate review. Source: bd_vat_suppletie_explanation.

These skills prepare the evidence, route, rubric reconciliation, and handoff. They do not transmit a correction, conduct a dispute, calculate penalties, or guarantee interest relief.

## Official sources

- bd_vat_corrections: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/btw_aangifte_doen_en_betalen/aangifte_corrigeren/aangifte_corrigeren
- bd_vat_suppletie_explanation: https://download.belastingdienst.nl/belastingdienst/docs/toelichting_suppletie_btw_ob1431t21pl.pdf
- bd_vat_return_deadlines: https://www.belastingdienst.nl/wps/wcm/connect/nl/btw/content/uiterste-aangifte-en-betaaldatums
