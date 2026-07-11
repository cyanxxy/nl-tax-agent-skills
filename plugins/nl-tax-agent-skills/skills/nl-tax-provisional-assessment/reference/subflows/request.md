## Request subflow

### Decision points

1. Does the taxpayer profile exist? If not, route back to intake.
2. Does the profile contain `provisional_2026_request`? If not, route to the correct subflow.
3. **Have they already received any 2026 voorlopige aanslag?** A later unsolicited VA based on earlier data may be issued, but is not guaranteed. If a 2026 beschikking or monthly amount actually exists, this is really a **change** (or **review**), not a request -- route to the change/review subflow with that beschikking as the baseline. Only continue as a request when no 2026 voorlopige aanslag exists yet.
4. Does the taxpayer have a fiscal partner? If yes, collect partner data and determine box 3 allocation.

### Data collection steps

1. **Employment income estimate** — gross annual salary, holiday allowance, bonuses expected in 2026
2. **Pension/benefit income estimate** — AOW, pension, WW, WIA, bijstand expected in 2026
3. **Other income estimate** — non-business rental, foreign, or other income expected in 2026
4. **Winst uit onderneming forecast** — if applicable, invoke or inline `nl-tax-winst`; record only the sourced, user-reviewed full-year forecast as `onderneming.geschatte_winst` with manual review. Never put business profit in a generic other-income field and never apply annual deductions, Zvw, cessation profit, or final tax.
5. **Own-home deduction estimate** — mortgage interest (hypotheekrente) for 2026, eigenwoningforfait based on WOZ-waarde
6. **Other deductions estimate** — alimentatie, lijfrentepremie, arbeidsongeschiktheidsverzekering, specific care costs, gifts. Treat zorgkosten thresholds and lijfrente limits as manual-review items unless exact reviewed sources and all required inputs are present.
7. **Box 2 estimate** — standard aanmerkelijk-belang estimates:
   - Estimated regular benefits, including dividends
   - Estimated disposal benefits from share sales
   - Estimated related costs and dividend withholding tax
   - Estimated fictitious regular benefit from BV lending, if applicable
   - Fiscal-partner Box 2 allocation, if applicable
   - Route valuation disputes, emigration, death, restructurings, treaty/nonresident issues, informal capital, non-arm's-length transfers, and corporate-tax-heavy DGA facts to manual review or unsupported
8. **Box 3 data** — assets and debts as of peildatum 1 January 2026:
   - Categorie I: Banktegoeden
   - Categorie II: Overige bezittingen
   - Categorie III: Schulden (excluding eigenwoningschuld)
   - Heffingsvrij vermogen deduction
   - FICTITIOUS METHOD ONLY

### Output generation

1. Generate `workspace/provisional/2026/provisional-pack.md` using the template
2. After the generation gate opens, invoke `nl-tax-field-mapper`; it alone writes and validates `workspace/provisional/2026/field-map.yaml` using `nl-tax-field-mapper/templates/field-map-template.yaml`, `nl-tax-field-mapper/reference/mapping-principles.md`, `nl-tax-field-mapper/reference/provisional-field-map.md`, and the optional `nl-tax-field-mapper/scripts/validate_field_map.py` check.
3. Update `workspace/shared/assumptions.md` with all assumptions made
4. Label all amounts as estimates

---
