# Unsupported Cases — Out of Scope for v1

The following taxpayer situations are not supported in version 1 of the Dutch tax skill. When any of these cases is detected during intake, the skill must:

1. Clearly inform the user that their situation is not covered in v1
2. Set `workflow_candidate: unsupported` in the taxpayer profile
3. Suggest they consult a tax adviser or use the official Belastingdienst portal (mijn.belastingdienst.nl)
4. Not attempt to generate a workpack or proceed with calculations

---

## 1. Part-Year Dutch Resident (Buitenlandse Belastingplicht)

- **Description:** The taxpayer was a Dutch resident for only part of the tax year (e.g., emigrated or immigrated during 2025)
- **Why unsupported:** Requires pro-rata calculations, split-year treatment, and potentially two country returns
- **Advice:** Use the Belastingdienst portal or consult a tax adviser experienced in migration cases

## 2. Non-Resident Taxpayer (C-biljet / Kwalificerende Buitenlandse Belastingplichtige)

- **Description:** The taxpayer lives outside the Netherlands but has Dutch-source income (e.g., Dutch employment, Dutch property, Dutch pension)
- **Why unsupported:** Requires C-biljet filing, qualification rules for deductions, and potential treaty application
- **Advice:** Use the Belastingdienst portal for non-residents or consult an international tax adviser

## 3. Deceased Taxpayer (F-biljet)

- **Description:** The tax return is being filed for a person who passed away during or before the tax year
- **Why unsupported:** Requires F-biljet, estate considerations, and often involves executor/heir authorization
- **Advice:** Contact the Belastingdienst directly or consult a tax adviser or notaris

## 4. IB-Onderneming as Primary Income

- **Description:** The taxpayer's primary income is from an unincorporated business (eenmanszaak, vof, maatschap) and the core workflow involves zelfstandigenaftrek, startersaftrek, MKB-winstvrijstelling, or FOR
- **Why unsupported:** Requires detailed profit calculations, entrepreneurial deductions, and business-specific tax treatment that goes beyond v1 scope
- **Advice:** Use accounting software (e.g., Exact, Moneybird) with tax filing integration, or consult a boekhouder/belastingadviseur
- **Note:** Employed individuals who have a small side business may still be in scope if employment is the primary income source — assess on a case-by-case basis

## 5. M-Aangifte (Migration Return)

- **Description:** A special return filed in the year of immigration to or emigration from the Netherlands
- **Why unsupported:** Combines elements of resident and non-resident filing, requires complex allocation rules
- **Advice:** Consult a tax adviser experienced in international/migration tax matters

## 6. Box 2 Substantial Interest as Primary Workflow

- **Description:** The taxpayer's primary concern is Box 2 income from a substantial interest (aanmerkelijk belang) in a BV or other entity — dividends, share sales, deemed dispositions
- **Why unsupported:** Requires corporate-personal tax interaction, valuation of shares, and complex Box 2 rules
- **Advice:** Consult a tax adviser, especially one experienced with DGA (directeur-grootaandeelhouder) matters
- **Note:** If the taxpayer has a small Box 2 position alongside primary Box 1 employment income, the case may still be in scope — assess on a case-by-case basis

## 7. Multiple Nationalities with Tax Treaty Complications

- **Description:** The taxpayer holds multiple nationalities and the applicable tax treaty creates complications regarding residence determination, tie-breaker rules, or income allocation
- **Why unsupported:** Requires treaty interpretation, tie-breaker analysis, and potential competent authority procedures
- **Advice:** Consult an international tax adviser

## 8. Foreign Pension with Treaty Override

- **Description:** The taxpayer receives a foreign pension where a tax treaty allocates taxation rights differently from standard Dutch rules, potentially requiring exemption or credit methods
- **Why unsupported:** Requires treaty-by-treaty analysis, voorkoming dubbele belasting calculations, and potentially foreign tax credit computations
- **Advice:** Consult a tax adviser experienced in cross-border pension taxation

---

## General Guidance for Unsupported Cases

When informing the user that their case is unsupported, use language like:

> "Your situation involves [specific complexity] which is not yet covered by this tool. I recommend consulting a registered tax adviser (belastingadviseur) or using the official Belastingdienst portal at mijn.belastingdienst.nl for accurate filing."

Do not attempt partial calculations or provide tax advice for unsupported cases, as incomplete guidance could lead to incorrect filings.
