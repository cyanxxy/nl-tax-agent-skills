## Winst uit onderneming forecast

[Repeat or reference the sourced `onderneming.geschatte_winst` forecast above.
If not applicable, state that explicitly. Preserve manual review and do not
include annual deduction or final-tax calculations.]

Definition confirmed with the taxpayer before the amount was recorded: the winst
expected as ondernemer in 2026, **before** the ondernemersaftrek and **before**
the MKB-winstvrijstelling, excluding the btw payable and the btw reclaimable,
with a minus sign for an expected loss. It is the only business figure the 2026
form asks for; the Belastingdienst applies the ondernemersaftrek and the
MKB-winstvrijstelling itself. Every 2026 business figure is read from
`../nl-tax-shared-resources/knowledge/years/2026/provisional/winst-provisional-2026.md`.

### Rollover check

| Item | Value | Src |
|------|-------|-----|
| 2026 voorlopige aanslag extended automatically or opened pre-filled | [yes / no / unknown] | [F/U/?] |
| Year whose figures the current 2026 voorlopige aanslag rests on | [year / unknown] | [F/U/?] |
| Profit estimate the current 2026 voorlopige aanslag uses | EUR [amount / unknown] (from-baseline) | [F/U/B/?] |
| Still the taxpayer's own best estimate for 2026 | [yes / no / unknown] | [F/U/?] |
| Reasoning still uses an earlier year's zelfstandigenaftrek | [yes / no / unknown] | [F/U/?] |
| Finding | [carried-over zelfstandigenaftrek above the 2026 amount in `winst-provisional-2026.md` / no rollover issue found / unresolved] | C:review |

A carried-over zelfstandigenaftrek above the 2026 amount overstates the
deduction, so too little is paid through the year and the difference is owed
when the final 2026 assessment is made up. Leave an unanswered row as `?` and
list it under Missing information; never assume and never enter a zero. A change
made to the voorlopige aanslag 2025 after the cut-off date stated in
`winst-provisional-2026.md` is not carried into 2026 automatically.

### Zvw companion -- separate voorlopige aanslag Zorgverzekeringswet

[Required whenever there is winst uit onderneming or income from work performed
outside employment. Otherwise state "N/A -- no winst uit onderneming or income
from work outside employment reported."]

| Item | Value | Src |
|------|-------|-----|
| Voorlopige aanslag Zorgverzekeringswet 2026 received | [yes / no / unknown] | [F/U/?] |
| Income estimate that voorlopige aanslag Zvw uses | EUR [amount / unknown] (from-baseline) | [F/U/B/?] |
| Still matches the taxpayer's own 2026 expectation | [yes / no / unknown] | [F/U/?] |
| Handling | separate aanslag, separate change route -- manual review | C:review |

You (the taxpayer) receive two aanslagen: one for the inkomstenbelasting/premie
volksverzekeringen and a separate one for the bijdrage Zorgverzekeringswet. At
this stage there can be two voorlopige aanslagen, with separate change routes.
Whether a change to the income-tax voorlopige aanslag is coupled to the Zvw
assessment is not established in the reviewed sources. You therefore check the
Zvw assessment separately, and this workpack records what you find.

- [ ] You (the taxpayer) also check your voorlopige aanslag Zorgverzekeringswet
  2026 in Mijn Belastingdienst and change it through its own route if its
  estimate is no longer right.

The Zvw base is the belastbare winst -- a different figure from
`onderneming.geschatte_winst`, which is taken before the ondernemersaftrek and
the MKB-winstvrijstelling. The bijdrage is not deductible and is never
subtracted from the profit estimate. This section reports the Zvw alongside the
income-tax dataset and never inside it: no bijdrage amount, no Zvw row in the
income-tax form, and no Zvw instalment, deadline, payment, or refund timing.
Percentages and the maximumbijdrage-inkomen are read from
`../nl-tax-shared-resources/knowledge/years/2026/provisional/zvw-provisional-2026.md`; the
Belastingdienst calculates the bijdrage.

The income-tax field map contains no Zvw field or value: no Zvw `field_id`,
label, note, amount, baseline, estimate, or manual-entry row.

### Estimated tax credits

| Credit area                           | Handling | Src |
|---------------------------------------|----------|-----|
| Algemene heffingskorting              | [portal estimate / source-backed estimate / manual review] | [C/F/U/A/?] |
| Arbeidskorting                        | [portal estimate / source-backed estimate / manual review] | [C/F/U/A/?] |
| IACK                                  | [manual review unless exact reviewed sources and required facts are present] | [F/U/A/?] |
| Ouderenkorting                        | [manual review unless exact reviewed sources and required facts are present] | [F/U/A/?] |
| Alleenstaandeouderenkorting           | [manual review of entitlement to an AOW pension for a single person; never infer from single-parent status or children] | [F/U/A/?] |
| Jonggehandicaptenkorting              | [manual review unless exact reviewed sources and required facts are present] | [F/U/A/?] |

Do not show calculated credit amounts unless exact reviewed sources are registered and all required taxpayer facts are available.
