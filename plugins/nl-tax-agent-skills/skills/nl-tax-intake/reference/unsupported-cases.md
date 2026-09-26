# Unsupported Cases

The situations below are outside this plugin's preparation scope. When intake
detects one of them, except under section 4:

1. Tell the user clearly, in chat, which part of their situation is not
   covered.
2. Use the most specific route label named below, or `unsupported` only when
   no specific label fits.
3. Suggest a registered tax adviser, or that the taxpayer files personally
   through Mijn Belastingdienst (mijn.belastingdienst.nl).
4. Prepare no workpack and no calculation, and write no file. The outcome lives
   only in the conversation.

---

## 1. Part-Year Dutch Resident (Buitenlandse Belastingplicht)

- **Description:** The taxpayer was a Dutch resident for only part of the tax year (e.g., emigrated or immigrated during 2025)
- **Route label:** `annual_2025_migration_m_form`
- **Why unsupported:** Requires pro-rata calculations, split-year treatment, and potentially two country returns
- **Advice:** The taxpayer files through Mijn Belastingdienst personally or consults a tax adviser experienced in migration cases

## 2. Non-Resident Taxpayer (C-biljet / Kwalificerende Buitenlandse Belastingplichtige)

- **Description:** The taxpayer lives outside the Netherlands but has Dutch-source income (e.g., Dutch employment, Dutch property, Dutch pension)
- **Route label:** `annual_2025_nonresident_c_form`
- **Why unsupported:** Requires C-biljet filing, qualification rules for deductions, and potential treaty application
- **Advice:** The taxpayer uses the Belastingdienst route for non-residents personally or consults an international tax adviser

## 3. Deceased Taxpayer (F-biljet)

- **Description:** The tax return is being filed for a person who passed away during or before the tax year
- **Route label:** `annual_2025_deceased_f_form`
- **Why unsupported:** Requires F-biljet, estate considerations, and often involves executor/heir authorization
- **Advice:** The heirs or executor contact the Belastingdienst directly or consult a tax adviser or notaris

## 4. Complex Business Forms (Winst uit onderneming)

This section is the one place in this file where recognising the case does **not**
end the preparation. Only the named computations below are terminal; everything
else about the business is prepared, so do not apply the numbered stop rules at
the top of this file to a business case before checking the lists here.

- **Supported preparation:** A full-year resident individual with an **eenmanszaak** uses `annual_2025` for the complete business section: the reviewed zakelijke schema (winst-en-verliesrekening rubrieken, both balans columns, the entrepreneur questions, and the priveonttrekkingen en -stortingen), and the ordered profit chain from winst uit onderneming through the investeringsaftrek, the ondernemersaftrek and the MKB-winstvrijstelling to the belastbare winst uit onderneming that feeds the box 1 income total. The business field map can reach `readiness: review_ready`. An IB-ondernemer also receives a **second, separate aanslag** for the inkomensafhankelijke bijdrage Zorgverzekeringswet alongside the aanslag inkomstenbelasting; prepare both from the same return. Amounts, percentages and hour counts stay in `../nl-tax-shared-resources/knowledge/years/2025/entrepreneur/`; never restate them here. A `provisional_2026_request` or `provisional_2026_change` may carry only the sourced, user-reviewed expected-profit forecast in `onderneming.geschatte_winst`.
- **Resultaat uit overige werkzaamheden is a supported prepared path, not a dead end.** A freelancer who is not an ondernemer voor de inkomstenbelasting keeps `business.has_onderneming` false and has the ROW result prepared from `../nl-tax-shared-resources/knowledge/years/2025/entrepreneur/row-en-dba-2025.md`, which also carries the bron-van-inkomen pre-screen that runs before any category question and the explain-only Wet DBA account. Ondernemersaftrek, MKB-winstvrijstelling and investeringsaftrek never apply to a ROW result; the bijdrage Zvw does. Do not route a ROW case to a terminal label, and do not judge the arbeidsrelatie or draft a modelovereenkomst for the taxpayer.
- **Every other IB business form is recognised and routed, not dead-ended.** A vof, maatschap, man-vrouwfirma, cv, medegerechtigdheid, an agrarische onderneming, a zeevarende, a staking, a herinvesteringsreserve, an oudedagsreserve wind-down, or terbeschikkingstelling is named, its effect on the ondernemer tests and on the deductions is explained, its facts are collected with provenance, and the parts of the return it does not block are still prepared.
- **Active route:** keep `annual_2025` so the annual workflow can prepare the
  unaffected sections. `annual_2025_entrepreneurs` is only the roadmap marker
  for the blocked business computation, handed to the annual workflow; it is
  never a terminal route.
- **Terminal manual review -- the computations that stay out of scope:** the profit-share computation of a samenwerkingsverband (VOF, maatschap, man-vrouwfirma, CV), including the winstaandeel, the KIA apportionment and the per-participant figures; the loss caps applying to a medegerechtigde or a profit-sharing geldverstrekker; DGA / BV winst and its corporate-tax interaction; agrarische ondernemingen (landbouwvrijstelling); zeevarenden (zeescheepvaart); the stakingswinst computation, the doorschuiffaciliteiten and the stakingslijfrente; any herinvesteringsreserve or kostenegalisatiereserve movement; the oudedagsreserve wind-down computation; and terbeschikkingstelling of assets to a connected company or enterprise. Collect the facts so far, name the figure that could not be computed and why, and hand that figure to professional review without producing a partial calculation.
- **How to route it:** keep `annual_2025` active in every case in this section.
  Hand the annual workflow the business-screening outcome `manual_review` with
  its triggers, plus the roadmap marker `annual_2025_entrepreneurs` when the
  blocked computation is the business section itself (partnership profit share,
  medegerechtigdheid, DGA/BV winst, agrarisch or zeevarende). A supported
  eenmanszaak with one blocked item needs no marker. The annual workflow keeps
  the business field map `draft` and the blocked figure `?` while it prepares
  the unaffected sections. Do **not** follow the terminal steps at the top of
  this file and do not suppress the workpack.
- **Why the boundary:** these figures need taxpayer-specific balance-sheet history, a per-participant allocation, or a formal request that no reviewed source settles. The Belastingdienst itself describes the stakingswinst computation as very complicated and advises taking advice.
- **Advice:** For the blocked computations, the taxpayer uses accounting software (e.g., Exact, Moneybird) with tax-filing integration, or consults a boekhouder / belastingadviseur.

## 5. M-Aangifte (Migration Return)

- **Description:** A special return filed in the year of immigration to or emigration from the Netherlands
- **Route label:** `annual_2025_migration_m_form`
- **Why unsupported:** Combines elements of resident and non-resident filing, requires complex allocation rules
- **Advice:** Consult a tax adviser experienced in international/migration tax matters

## 6. Complex Box 2 Substantial-Interest Cases

- **Supported standard preparation:** A full-year resident individual in an active `annual_2025` or `provisional_2026` workflow may include standard Box 2 preparation for an aanmerkelijk belang, including regular benefits such as dividends, disposal benefits such as share-sale profit, dividend withholding tax credit, loss carry-forward fields, and fiscal-partner Box 2 allocation.
- **Route label:** `manual_review`
- **Manual review / unsupported boundary:** Route the case to manual review or unsupported when Box 2 involves valuation disputes, immigration or emigration, death, restructurings, treaty or nonresident issues, informal capital, non-arm's-length transfers, or corporate-tax-heavy DGA questions.
- **Advice:** For complex Box 2 cases, consult a tax adviser, especially one experienced with DGA (directeur-grootaandeelhouder) and corporate-tax interaction.

## 7. Multiple Nationalities with Tax Treaty Complications

- **Description:** The taxpayer holds multiple nationalities and the applicable tax treaty creates complications regarding residence determination, tie-breaker rules, or income allocation
- **Route label:** `annual_2025_foreign_treaty_heavy`
- **Why unsupported:** Requires treaty interpretation, tie-breaker analysis, and potential competent authority procedures
- **Advice:** Consult an international tax adviser

## 8. Foreign Pension with Treaty Override

- **Description:** The taxpayer receives a foreign pension where a tax treaty allocates taxation rights differently from standard Dutch rules, potentially requiring exemption or credit methods
- **Route label:** `annual_2025_foreign_treaty_heavy`
- **Why unsupported:** Requires treaty-by-treaty analysis, voorkoming dubbele belasting calculations, and potentially foreign tax credit computations
- **Advice:** Consult a tax adviser experienced in cross-border pension taxation

---

## General Guidance for Unsupported Cases

When telling the user that their case is unsupported, use language like:

> "Your situation involves [specific complexity], which this tool does not cover. I recommend a registered tax adviser (belastingadviseur), or you can file it yourself in Mijn Belastingdienst."

Add a short list of the facts already screened and the specific trigger, so the
user can take it to an adviser. Do not attempt partial calculations or give tax
advice for unsupported cases: incomplete guidance could lead to incorrect
filings.
