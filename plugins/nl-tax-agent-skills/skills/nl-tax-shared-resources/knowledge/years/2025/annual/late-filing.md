# Rule note: Late-filing exposure for the 2025 annual return

source_ids: bd_annual_deadline_2025, bd_annual_extension_2025, bd_annual_extension_eligibility_2025, bd_verzuimboete, bd_belastingrente_overview, bd_belastingrente_ib, bd_invorderingsrente
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-07-16"
review_status: reviewed

## Rule

A taxpayer's potential exposure depends on whether an aangiftebrief was issued.
Do not merge the invited-return filing penalty with the separate no-letter
failure-to-request penalty. The workpack records facts and possible exposure;
the Belastingdienst determines fault, applicability, and the amount.

## Deadline

- If an invitation letter (aangiftebrief) exists, its date is the applicable deadline.
- With **no invitation**, use **14 July 2026** only for the
  `no_letter_but_mandatory` route described in `filing-flow.md`: EUR 58 or more
  to pay, or the separate asset/scheme test. A refund-only claim is not this
  mandatory route.
- If the no-letter result or asset/scheme test remains unresolved, do not invent
  a deadline and do not classify the return as late.
- Extension eligibility requires an invitation letter. With **no invitation**,
  extension is unavailable.
- As of **16 July 2026**, the ordinary online request window that ended on
  **1 May 2026** is closed; historically the request had to be made **before 1 May 2026**.
  If extension was already granted, verify the
  confirmation; the standard granted date is **1 September 2026** (4 months
  extra).
- If the invitation letter shows another date—a still-future date—the taxpayer may
  request extension by that date using the official form route. If that printed
  date has passed, do not present extension as available.

## Invited return: penalty for not filing by the aanmaning deadline

- Potential first-time exposure after the full escalation sequence: **EUR 469**.
- Potential repeated-filing exposure after the full escalation sequence: up to **EUR 6,709**.
- Escalation: missing the deadline does not trigger the boete immediately. The Belastingdienst first sends a **herinnering** (reminder), then an **aanmaning** (formal demand). After the aanmaning the taxpayer must file within **10 werkdagen** (working days) from the aanmaning date; only if the return is still not filed by then is the EUR 469 verzuimboete imposed. Requesting an aangifteformulier does not avoid the boete.
- Waiver: no boete is imposed if the taxpayer bears no fault for the late or missing filing ("geen enkele schuld"). This is decided by the Belastingdienst on the facts; the workpack never asserts the waiver applies.

## No letter but mandatory: separate failure-to-request regime

- Ask whether and when the taxpayer requested that an aangifte be issued. Do
  not apply the invited-return reminder/aanmaning sequence to this question.
- The official rule describes a request as late for income tax when it is not
  made within **6 months after the time the tax liability arose**. The official
  guidance also states that no failure-to-request penalty is imposed when the
  taxpayer requests the return within **2 weeks after that period**. Do not
  calculate those legal dates from assumptions; surface the 14 July 2026 filing
  guardrail and have the taxpayer verify correspondence and timing.
- Potential exposure for not requesting, or not requesting on time, is
  **EUR 3,354**. This is not the EUR 469 invited-return filing penalty and is not
  automatic. Keep it conditional and cite `bd_verzuimboete`.
- Keep intent/gross-negligence penalties separate. Do not characterize a missed
  request as intentional without an official determination.

## Belastingrente (tax interest)

- For income tax, belastingrente can apply when the Belastingdienst receives the
  return **on or after 1 May** following the tax year, or when it **deviates from
  the filed return when setting the assessment**. The second ground can apply
  even when the return was filed before 1 May. Therefore, "filed on time" means
  no late-filing penalty exposure; it is not a promise of zero belastingrente.
- For the 2025 return, the interest period normally starts on **1 July 2026**
  when tax is payable and an interest ground applies. It does **not** run until
  the aanslag is paid: the end is tied to the assessment rules, and for a return
  received on or after 1 May the period is capped at a maximum of 19 weeks after
  receipt when the assessment follows the return. Paying the aanslag faster
  does not reduce belastingrente already fixed on that assessment.
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
   - For `invited`, quote EUR 469 / up to EUR 6,709 only as potential
     exposure and record whether a **herinnering** and **aanmaning** were
     received and whether the **10 werkdagen** period expired.
   - For `no_letter_but_mandatory`, ask whether and when an aangifte was
     requested and quote EUR 3,354, the 6-month period, and 2-week grace only as
     potential official exposure. Do not substitute the invited-return
     escalation sequence.
   - Quote the belastingrente percentage applicable to the period after 1 July 2026.
   - List the recommended next steps: submit the prepared return as soon as
     possible, monitor the correspondence relevant to the route, and pay an
     eventual aanslag by its betaaltermijn to avoid invorderingsrente. State
     that any boete remains conditional and that belastingrente already set on
     the assessment is not reduced by paying faster.
3. If uitstel was granted, note the granted uitsteldatum and the rente warning (interest still accrues after 1 July 2026 if tax is owed).
4. If the return was filed on time, mark the section "Filing status: on time. No
   late-filing penalty exposure." Do not promise zero belastingrente: flag that
   it can still apply if the Belastingdienst deviates from the filed return, and
   can apply when a no-letter return is received on or after 1 May.

## Common failure

Do not pad the workpack with a rente calculation. The base rate is fixed but the daily accrual depends on the aanslag date, which is unknown at workpack-generation time. Quote the rate, state when it starts, and leave the arithmetic to the Belastingdienst.

Do not advise the user to skip filing because a boete might apply. Filing late is
materially better than not filing. On the invited route, if the return remains
missing through the herinnering, aanmaning, and 10-workday period, the
Belastingdienst may make an **estimated (ambtshalve) assessment** and impose a
verzuimboete; the estimate can differ from the true tax. A **vergrijpboete** is
separate: it applies only when the Belastingdienst establishes intent (opzet) or
gross negligence (grove schuld). It does not follow automatically, and the
initial estimated assessment is not a navorderingsaanslag.
