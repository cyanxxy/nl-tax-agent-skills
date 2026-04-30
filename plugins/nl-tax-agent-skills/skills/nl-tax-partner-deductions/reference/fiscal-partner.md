# Rule note: Fiscal partner rules (fiscaal partnerschap)

source_id: bd_fisin_2025_partner
workflow: annual-return, provisional-assessment
tax_year: 2025, 2026
status: active
last_reviewed: "2026-04-30"
review_status: reviewed

## Rule

Fiscal partnership (fiscaal partnerschap) determines whether two people can allocate certain income and deduction items between them for income tax purposes. The rules are defined in the Wet inkomstenbelasting 2001, primarily article 5a and articles 1.2 and further.

These are reference notes for workpack preparation -- not final tax advice.

## Automatic fiscal partners

The following persons are automatically fiscal partners for the entire calendar year:

### Married couples (gehuwden)

- Spouses are automatically fiscal partners from the date of marriage through the end of the year.
- In the year of marriage: fiscal partnership applies for the full year (not just from the wedding date).
- Exception: if a request for divorce (verzoek tot echtscheiding) has been filed AND the spouses no longer live at the same address, they are no longer fiscal partners from the date of address separation.

### Registered partners (geregistreerd partnerschap)

- Registered partners have the same status as married couples for tax purposes.
- All rules that apply to married couples apply equally to registered partners.

## Optional fiscal partners (keuze-partnerschap)

Unmarried cohabitants may choose to be fiscal partners if they meet ALL of the following conditions:

### Required conditions

1. **Same address in the GBA (Basisregistratie Personen):** both persons must be registered at the same residential address in the municipal personal records database.
2. **Full-year requirement:** as a general rule, both persons must be registered at the same address for the entire calendar year. Part-year exceptions exist (see below).
3. **At least one additional criterion** from the following list:
   - They have a notarial cohabitation contract (notarieel samenlevingscontract)
   - They jointly own the home they live in (gezamenlijk eigendom van de woning)
   - One is designated as the other's pension partner (pensioenpartner)
   - They have a child together (or one partner has recognized the other's child)
   - They are both registered in the pension scheme of the other partner

### Part-year exceptions

In the following situations, the full-year same-address requirement may be relaxed:
- One partner moved to the Netherlands during the year (immigration)
- Both partners moved to the same address during the year and meet the additional criteria
- One partner died during the year (see special situations below)

### Choosing fiscal partnership

When conditions are met, the choice to be fiscal partners is made by both persons filing their tax returns accordingly. Both persons must make the same choice. If one files as fiscal partner and the other does not, the returns are inconsistent and the Belastingdienst will reject the incorrect filing.

## What fiscal partnership affects

### Allocatable items (gemeenschappelijk inkomen)

The following items can be allocated between fiscal partners in any proportion (0-100%):

#### Box 3 assets and debts

- The combined box 3 grondslag (assets minus debts, after heffingsvrij vermogen) can be split in any ratio between partners.
- Both partners each have their own heffingsvrij vermogen (EUR 57,000 for 2025).
- Optimal allocation often means splitting box 3 so that both partners use their heffingsvrij vermogen fully.

#### Eigen woning income (box 1)

- The net eigen woning result (eigenwoningforfait minus deductible mortgage interest and other eigen woning costs) is allocated as a unit.
- It must be allocated to one partner (not split partially) unless both partners are co-owners AND the mortgage is in both names, in which case the allocation follows ownership shares or the partners' chosen allocation.
- In practice for jointly owned homes: both partners can allocate their shares, and this is commonly treated as a single allocatable item.

#### Persoonsgebonden aftrek

- Alimentatie paid, excess zorgkosten, giften, and other personal deductions can be allocated freely between partners.
- The allocation can differ per deduction category.

### Items affected indirectly

#### Heffingskortingen

- The algemene heffingskorting and arbeidskorting are calculated per individual, but partner income affects the inkomensafhankelijke afbouw (income-dependent phase-out).
- The allocation of income items between partners can change each partner's total income, which in turn affects their heffingskorting amounts.
- The inkomensafhankelijke combinatiekorting requires the lower-earning partner to have at least a minimum level of arbeidsinkomen.

### Items that CANNOT be allocated

The following items are personal to the individual and cannot be allocated to the other partner:

- **Employment income (loon):** stays with the employee who earned it.
- **Pension income (pensioen):** stays with the recipient.
- **Social benefit income (uitkeringen):** stays with the recipient.
- **Arbeidskorting:** calculated based on individual employment income; cannot be transferred.
- **Ondernemersaftrek and MKB-winstvrijstelling:** personal to the entrepreneur.

## Special situations

### Partner died during the year (overlijden)

- If one partner dies during the calendar year, fiscal partnership applies for the FULL year (not just until the date of death).
- The surviving partner and the estate of the deceased file returns for the full year as fiscal partners.
- This is a mandatory rule, not a choice.
- Flag for human review: allocation choices for the year of death can be complex. Professional advice is recommended.

### Divorce or separation during the year (echtscheiding / scheiding)

- Married/registered partners: fiscal partnership ends when the divorce or dissolution is finalized AND the partners no longer live at the same address.
- In practice, this means fiscal partnership can end mid-year if both conditions are met.
- The year of divorce involves complex allocation rules: fiscal partnership applies for the portion of the year before the end conditions are met.
- **v1 scope note:** mid-year divorce is flagged as a complex situation. This skill does not generate allocation options for the partial-year period. Recommend professional advice.

### One partner is non-resident (buitenlandse partner)

- A non-resident partner can be a fiscal partner if they qualify as a "kwalificerend buitenlands belastingplichtige" (qualifying non-resident taxpayer).
- The qualifying non-resident must have at least 90% of worldwide income subject to Dutch taxation.
- If the non-resident partner does not qualify, fiscal partnership is generally not possible.
- **v1 scope note:** non-resident partner situations are flagged as potentially unsupported. The skill verifies the 90% criterion if data is available; otherwise it flags for human review.

### Married but separated (duurzaam gescheiden levend)

- Married couples who are permanently separated (duurzaam gescheiden levend) are no longer fiscal partners, even if the divorce has not been finalized.
- This requires actual permanent separation, not just temporary living apart.
- Evidence: separate addresses in GBA, absence of shared household.

## Verification checklist

When determining fiscal partnership, verify:

1. Civil status (married, registered partnership, unmarried)
2. If unmarried: GBA registration at the same address
3. If unmarried: duration of shared address registration (full year or exception applies)
4. If unmarried: at least one additional criterion met
5. If married/registered: check for divorce filing or permanent separation
6. If non-resident partner: check qualifying status
7. Both partners must make the same fiscal partnership choice in their returns

## Notes

- Fiscal partnership is an all-or-nothing choice per calendar year (with exceptions for part-year situations). Partners cannot be fiscal partners for some items and not others.
- The fiscal partnership choice is made annually. Being fiscal partners in one year does not automatically mean the same choice in the next year (for optional partners).
- For automatic partners (married/registered), there is no choice -- fiscal partnership is mandatory unless the exception conditions for separation or divorce apply.
