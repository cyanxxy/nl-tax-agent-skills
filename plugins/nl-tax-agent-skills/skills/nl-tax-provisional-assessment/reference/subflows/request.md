## Request subflow

### Conversational review checkpoints

1. Does the taxpayer profile exist? If not, route back to intake.
2. Does the profile contain `provisional_2026_request`? If not, route to the correct subflow.
3. **Have they already received any 2026 voorlopige aanslag?** A later unsolicited VA based on earlier data may be issued, but is not guaranteed. If a 2026 beschikking or monthly amount actually exists, this is really a **change** (or **review**), not a request -- route to the change/review subflow with that beschikking as the baseline. Only continue as a request when no 2026 voorlopige aanslag exists yet.
4. Does the taxpayer have a fiscal partner? If yes, collect partner data and determine box 3 allocation.

### Data collection steps

1. **Employment income estimate** — gross annual salary, holiday allowance, bonuses expected in 2026
2. **Pension/benefit income estimate** — AOW, pension, WW, WIA, bijstand expected in 2026
3. **Other income estimate** — non-business rental, foreign, or other income expected in 2026
4. **Winst uit onderneming forecast** — if applicable, invoke or inline `nl-tax-winst`; record only the sourced, user-reviewed full-year forecast as `onderneming.geschatte_winst` with manual review. Include it in the Box 1 income-before-own-home rollup. Never put business profit in a generic other-income field and never apply annual deductions, a bijdrage Zvw amount, cessation profit, or final tax.
   - **State the definition before recording the amount.** Tell the taxpayer, in the conversation, what the single figure means: the winst they expect to earn as ondernemer in 2026, taken **before** the ondernemersaftrek and **before** the MKB-winstvrijstelling, excluding the btw payable and the btw reclaimable, with a minus sign for an expected loss. Record the amount only after the taxpayer has confirmed it on those terms.
   - Read that definition, the invulhulp item list, and every 2026 business figure from `_shared/knowledge/years/2026/provisional/winst-provisional-2026.md`; never restate one from memory. Walk the taxpayer through the invulhulp items, and record anything they cannot answer as an open question -- never assume an item is nil and never enter a zero. Do not build or request a balans or a winst-en-verliesrekening; the 2026 form has neither.
5. **Voorlopige aanslag Zorgverzekeringswet** -- whenever there is winst uit onderneming or income from work performed outside employment, raise the separate bijdrage Zvw without waiting to be asked, using `_shared/knowledge/years/2026/provisional/zvw-provisional-2026.md` for every figure. Tell the taxpayer there are two separate aanslagen with separate change routes. No reviewed source establishes whether a change to the income-tax voorlopige aanslag is coupled to the Zvw assessment, so the taxpayer must check the Zvw assessment separately and record what they find. Ask: "Have you (the taxpayer) received a voorlopige aanslag Zorgverzekeringswet for 2026, and what income estimate does it use?" Record the answer with provenance, or an open question when the taxpayer does not know. Report it alongside the income-tax dataset: never compute a bijdrage amount, never merge it into the income-tax figures, never subtract it from the profit estimate, and never add a Zvw field, value, label, note, or row to the income-tax field map.
6. **Own-home estimate** — use the own-home WOZ value with peildatum 1 January 2025 and preserve eigenwoningforfait, mortgage interest, qualifying financing costs, periodic erfpacht/opstal/beklemming, total deductible own-home costs, any Hillen deduction, and `box1_own_home_balance` as separate review components
7. **Other deductions estimate** — alimentatie, lijfrentepremie, arbeidsongeschiktheidsverzekering, specific care costs, gifts. Treat zorgkosten thresholds and lijfrente limits as manual-review items unless exact reviewed sources and all required inputs are present.
8. **Box 2 estimate** — standard aanmerkelijk-belang estimates:
   - Estimated regular benefits, including dividends
   - Estimated disposal benefits from share sales
   - Estimated related costs and dividend withholding tax
   - Estimated fictitious regular benefit from BV lending, if applicable
   - Fiscal-partner Box 2 allocation, if applicable
   - Route valuation disputes, emigration, death, restructurings, treaty/nonresident issues, informal capital, non-arm's-length transfers, and corporate-tax-heavy DGA facts to manual review or unsupported
9. **Box 3 data** — assets and candidate debts as of peildatum 1 January 2026:
   - Categorie I: Banktegoeden
   - Categorie II: Overige bezittingen
   - Categorie III: qualifying Box 3 schulden after the official inclusion/exclusion screen; unresolved debts remain manual-review rows outside accepted totals
   - Heffingsvrij vermogen deduction
   - FICTITIOUS METHOD ONLY

### Output generation

1. Generate `workspace/provisional/2026/provisional-pack.md` using the template
2. After the generation gate opens, invoke `nl-tax-field-mapper`; it alone writes and validates `workspace/provisional/2026/field-map.yaml` using `nl-tax-field-mapper/templates/field-map-template.yaml`, `nl-tax-field-mapper/reference/mapping-principles.md`, `nl-tax-field-mapper/reference/provisional-field-map.md`, and the agent checklist with `nl-tax-field-mapper/reference/field-map-rules.yaml`.
3. Update `workspace/shared/assumptions.md` with all assumptions made
4. Label all amounts as estimates
5. If `person.aow_by_tax_year.2026.status` is `reaches_during_year`, record the transition
   month and use the live portal result for the affected rates/credits; do not
   select either whole-year table

---
