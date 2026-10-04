# VAT intent and scope

Apply this branch to ordinary VAT return/correction intent before any income-
tax screening. Explicit ICP or OSS/IOSS preparation uses
`reference/extended-routing.md` and its separate owner instead. Credit facts
already given.
Ask only the unresolved essentials: Netherlands-established eenmanszaak/ZZP,
return versus correction, tax year, exact assigned period, invoicing or cash
system, and KOR/exemption status. Confirm the assigned period from the user's
notice, accounting record, or explicit statement; do not derive frequency from
turnover. Period tokens are `Q1`–`Q4`, `M01`–`M12`, or `Y` for 2025/2026;
`Y` means only an annual assigned filing period. A whole-year suppletie by a
monthly or quarterly filer is not prepared by these skills; route each
corrected period separately and leave the whole-year option to human review.
An unclear legal form or establishment stays unresolved; other legal forms
and foreign establishment require manual review.

VAT status never proves eligibility for income-tax entrepreneur reliefs. Do
not collect dates of birth, partner details, BSN, VAT registration numbers,
bank details, or credentials. The taxpayer performs every authenticated action
in Mijn Belastingdienst Zakelijk personally.

For an attached VAT workpack, check Appendix A: `nl-tax-workpack`, version
`2.x`, year, period, and workflow `vat_<year>_<period>` or
`vat_correction_<year>_<period>`. A mismatch is an ordinary source document.
Once year and period are established, check only the matching fixed path:
`workspace/nl-tax-vat-<year>-<period>-workpack.md` or
`workspace/nl-tax-vat-correction-<year>-<period>-workpack.md`. For a found file,
read only `updated_at` and ask once whether to continue before using its facts.
Never search for every period's workpack. Resume confirmed facts without
re-screening; an attached copy needs separate consent to keep saving.

Route return preparation to `../nl-tax-vat-return/SKILL.md` and corrections to
`../nl-tax-vat-correction/SKILL.md`. A correction requires original filed
figures and revised complete figures; a current unfiled return belongs to the
return workflow. The owner checks special-case scope and source-review status.
The VAT owner invokes `../nl-tax-vat-adjustments/SKILL.md` for complete bounded
car/private-use, pro-rata, property/revision, BUA and margin arithmetic.
Classification uncertainty stays specific; these topics are not blanket
unsupported cases. Separate ICP obligations route to `../nl-tax-icp/SKILL.md`
and confirmed OSS/IOSS scheme work to `../nl-tax-oss/SKILL.md`, one owner at a
time with separate identity, file, consent and source ledger. Domestic VAT
preparation can continue while an affected cross-border position stays open.
KOR screening is supported, but it never starts a KOR application or assumes
that no filing invitation needs a response.

When income tax and VAT are both requested, use one owner at a time, retaining
the other request as conversational intent. Follow the user's stated order;
if none is stated, start the explicit VAT period, then the income-tax request.
Save consent applies separately to each workflow. Do not copy income-tax
profit into VAT turnover or transfer amounts between periods automatically.

When a deadline is mentioned, the owner consults the VAT deadline note and
confirms the actual assigned deadline. Intake never changes the assigned
period, grants extension, opens the portal, or computes penalties.
