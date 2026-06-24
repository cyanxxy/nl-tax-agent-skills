# Unsupported Cases — Out of Scope for v1

The following taxpayer situations are not supported in version 1 of the Dutch tax skill. When any of these cases is detected during intake, the skill must:

1. Clearly inform the user that their situation is not covered in v1
2. Set the most specific terminal profile candidate named below, or `workflow_candidate: unsupported` only when no specific candidate fits
3. Set `intake_status: complete` so a resumed annual/provisional guard does not restart intake
4. Suggest they consult a tax adviser or use the official Belastingdienst portal (mijn.belastingdienst.nl)
5. Not attempt to generate a workpack or proceed with calculations

---

## 1. Part-Year Dutch Resident (Buitenlandse Belastingplicht)

- **Description:** The taxpayer was a Dutch resident for only part of the tax year (e.g., emigrated or immigrated during 2025)
- **Profile candidate:** `annual_2025_migration_m_form`
- **Why unsupported:** Requires pro-rata calculations, split-year treatment, and potentially two country returns
- **Advice:** Use the Belastingdienst portal or consult a tax adviser experienced in migration cases

## 2. Non-Resident Taxpayer (C-biljet / Kwalificerende Buitenlandse Belastingplichtige)

- **Description:** The taxpayer lives outside the Netherlands but has Dutch-source income (e.g., Dutch employment, Dutch property, Dutch pension)
- **Profile candidate:** `annual_2025_nonresident_c_form`
- **Why unsupported:** Requires C-biljet filing, qualification rules for deductions, and potential treaty application
- **Advice:** Use the Belastingdienst portal for non-residents or consult an international tax adviser

## 3. Deceased Taxpayer (F-biljet)

- **Description:** The tax return is being filed for a person who passed away during or before the tax year
- **Profile candidate:** `annual_2025_deceased_f_form`
- **Why unsupported:** Requires F-biljet, estate considerations, and often involves executor/heir authorization
- **Advice:** Contact the Belastingdienst directly or consult a tax adviser or notaris

## 4. IB-Onderneming as Primary Income

- **Description:** The taxpayer's primary income is from an unincorporated business (eenmanszaak, vof, maatschap) and the core workflow involves zelfstandigenaftrek, startersaftrek, MKB-winstvrijstelling, or FOR
- **Profile candidate:** `annual_2025_entrepreneurs`
- **Why unsupported:** Requires detailed profit calculations, entrepreneurial deductions, and business-specific tax treatment that goes beyond v1 scope
- **Advice:** Use accounting software (e.g., Exact, Moneybird) with tax filing integration, or consult a boekhouder/belastingadviseur
- **Note:** Employed individuals who have a small side business may still be in scope if employment is the primary income source — assess on a case-by-case basis

## 5. M-Aangifte (Migration Return)

- **Description:** A special return filed in the year of immigration to or emigration from the Netherlands
- **Profile candidate:** `annual_2025_migration_m_form`
- **Why unsupported:** Combines elements of resident and non-resident filing, requires complex allocation rules
- **Advice:** Consult a tax adviser experienced in international/migration tax matters

## 6. Complex Box 2 Substantial-Interest Cases

- **Supported standard preparation:** A full-year resident individual in an active `annual_2025` or `provisional_2026` workflow may include standard Box 2 preparation for an aanmerkelijk belang, including regular benefits such as dividends, disposal benefits such as share-sale profit, dividend withholding tax credit, loss carry-forward fields, and fiscal-partner Box 2 allocation.
- **Profile candidate:** `manual_review`
- **Manual review / unsupported boundary:** Route the case to manual review or unsupported when Box 2 involves valuation disputes, immigration or emigration, death, restructurings, treaty or nonresident issues, informal capital, non-arm's-length transfers, or corporate-tax-heavy DGA questions.
- **Advice:** For complex Box 2 cases, consult a tax adviser, especially one experienced with DGA (directeur-grootaandeelhouder) and corporate-tax interaction.

## 7. Multiple Nationalities with Tax Treaty Complications

- **Description:** The taxpayer holds multiple nationalities and the applicable tax treaty creates complications regarding residence determination, tie-breaker rules, or income allocation
- **Profile candidate:** `annual_2025_foreign_treaty_heavy`
- **Why unsupported:** Requires treaty interpretation, tie-breaker analysis, and potential competent authority procedures
- **Advice:** Consult an international tax adviser

## 8. Foreign Pension with Treaty Override

- **Description:** The taxpayer receives a foreign pension where a tax treaty allocates taxation rights differently from standard Dutch rules, potentially requiring exemption or credit methods
- **Profile candidate:** `annual_2025_foreign_treaty_heavy`
- **Why unsupported:** Requires treaty-by-treaty analysis, voorkoming dubbele belasting calculations, and potentially foreign tax credit computations
- **Advice:** Consult a tax adviser experienced in cross-border pension taxation

---

## General Guidance for Unsupported Cases

When informing the user that their case is unsupported, use language like:

> "Your situation involves [specific complexity] which is not yet covered by this tool. I recommend consulting a registered tax adviser (belastingadviseur) or using the official Belastingdienst portal at mijn.belastingdienst.nl for accurate filing."

Do not attempt partial calculations or provide tax advice for unsupported cases, as incomplete guidance could lead to incorrect filings.
