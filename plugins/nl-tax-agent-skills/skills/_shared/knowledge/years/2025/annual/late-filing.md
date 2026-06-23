# Rule note: Late-filing exposure for the 2025 annual return

source_ids: bd_annual_deadline_2025, bd_annual_extension_2025, bd_verzuimboete, bd_belastingrente_overview, bd_belastingrente_ib, bd_invorderingsrente
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-06-23"
review_status: reviewed

## Rule

A taxpayer who has not filed the 2025 aangifte inkomstenbelasting by the deadline shown in their personal aangiftebrief (or by the granted uitsteldatum) faces two financial consequences: a verzuimboete (administrative penalty for filing late) and, when the eventual aanslag shows tax owed, belastingrente (statutory interest). Both are imposed by the Belastingdienst; this skill does not calculate or impose them. The workpack must surface the exposure so the taxpayer can act before the boete or rente grows.

## Deadline

- The general/default deadline for the 2025 return was **1 May 2026**, but the binding date is the one on the taxpayer's personal aangiftebrief. The exact date is the one shown on the taxpayer's aangiftebrief or in Mijn Belastingdienst — always prefer the personal notice over the default.
- An uitstel granted before 1 May 2026 extends the deadline by **4 months**, to **1 September 2026**.
- The taxpayer can request uitstel for up to 4 months after the original deadline as long as the request is filed before that deadline.

## Verzuimboete (penalty for late filing)

- First time the taxpayer files late: **EUR 469**.
- Repeated late filing: the penalty rises to a maximum of **EUR 6,709**.
- Escalation: missing the deadline does not trigger the boete immediately. The Belastingdienst first sends a **herinnering** (reminder), then an **aanmaning** (formal demand). After the aanmaning the taxpayer must file within **10 werkdagen** (working days) from the aanmaning date; only if the return is still not filed by then is the EUR 469 verzuimboete imposed. Requesting an aangifteformulier does not avoid the boete.
- Waiver: no boete is imposed if the taxpayer bears no fault for the late or missing filing ("geen enkele schuld"). This is decided by the Belastingdienst on the facts; the workpack never asserts the waiver applies.

## Belastingrente (tax interest)

- Belastingrente starts running on **1 July following the tax year** for taxpayers who have not filed in time and end up owing tax. For the 2025 return, interest accrues from **1 July 2026**. It does **not** run until the aanslag is paid: belastingrente ends at a fixed point tied to the dagtekening of the aanslag — the end of the 6-week betaaltermijn after the dagtekening of the aanslag — and for an aangifte received on or after 1 May it is capped at a maximum of 19 weeks after receipt of the aangifte. Paying the aanslag faster does not reduce belastingrente, because the end date is already fixed when the aanslag is issued.
- Applicable percentages for inkomstenbelasting:
  - **From 1 January 2026: 5%**
  - 1 January 2025 to 31 December 2025: 6.5%
  - 1 January 2024 to 31 December 2024: 7.5%
- If the Belastingdienst grants uitstel, belastingrente is still due over the period the aanslag is outstanding.
- **Invorderingsrente** is a separate regime from belastingrente. It applies only when the aanslag is paid **after** its betaaltermijn (due date), running from the end of the betaaltermijn until the date of payment. Paying the aanslag by its betaaltermijn avoids invorderingsrente entirely.
- The workpack reports the rate that applies during the period interest will accrue. It does not compute a final rente amount; the Belastingdienst calculates that on the aanslag.

## Developer instruction

When building the workpack for box 1 / overall filing status:

1. Read the filing status from the intake notes or ask the user explicitly: did they file before the deadline, did they get uitstel, or is the return still outstanding?
2. If the return is outstanding and the deadline has passed:
   - Include a "Filing status and late-filing exposure" section at the top of the workpack, before income notes.
   - Quote the verzuimboete amounts above without computing a final figure (the actual amount is set by the Belastingdienst).
   - Quote the belastingrente percentage applicable to the period after 1 July 2026.
   - List the recommended next steps: submit the prepared return as soon as possible, expect the verzuimboete, monitor for the aanslag and pay the aanslag by its betaaltermijn to avoid invorderingsrente. Note that belastingrente is already fixed on the aanslag and is not reduced by paying faster.
3. If uitstel was granted, note the granted uitsteldatum and the rente warning (interest still accrues after 1 July 2026 if tax is owed).
4. If the return was filed on time, mark the section "Filing status: on time. No late-filing exposure" and continue.

## Common failure

Do not pad the workpack with a rente calculation. The base rate is fixed but the daily accrual depends on the aanslag date, which is unknown at workpack-generation time. Quote the rate, state when it starts, and leave the arithmetic to the Belastingdienst.

Do not advise the user to skip filing because the boete already applies. Filing late is materially better than not filing. For a non-filer the Belastingdienst makes an **estimated (ambtshalve) assessment** plus a verzuimboete, and the estimate is often higher than the true tax. A **vergrijpboete** is separate: it applies only when the Belastingdienst establishes intent (opzet) or gross negligence (grove schuld) — it does not follow automatically, and the initial estimated assessment is not a navorderingsaanslag.
