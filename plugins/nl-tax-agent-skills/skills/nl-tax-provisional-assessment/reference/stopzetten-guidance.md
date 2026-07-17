# Stopzetten Guidance — When to Stop vs When to Change

## Contents

- Purpose
- Review table
- Monthly REFUND (teruggaaf) — stopzetten may be appropriate
- Monthly PAYMENT (betaling) — CHANGE, not stop
- Monthly PAYMENT (betaling) — amount is correct
- Edge case: user wants to stop because they will file early
- Manual checklist for stopzetten (for inclusion in workpack)
- Stopzetten checklist
- Safety notes

## Purpose

This document gives the conversational agent review prompts for discussing
whether stopzetten (stopping) a voorlopige aanslag is available or whether a
change is more appropriate. It is guidance for a taxpayer-specific review, not
an automated tax decision flow.

---

## Review table

Use this as an official-availability check and discuss the taxpayer's selected
goal; do not silently choose an action for them.

| Current situation         | User wants to...             | Official route to discuss |
|---------------------------|------------------------------|--------------------|
| Receives monthly refund   | Stop receiving refunds       | Stopzetten         |
| Receives monthly refund   | Reduce refund amount         | Change             |
| Pays monthly amount       | Stop because amount is wrong | Change (NOT stop)  |
| Pays monthly amount       | Reduce monthly payment       | Change             |
| Pays monthly amount       | Amount is correct            | No action needed   |
| Moving abroad             | Determine provisional route  | Residency review; not a categorical stopzetten reason |

---

## Monthly REFUND (teruggaaf) — stopzetten may be appropriate

### Current-date cutoff gate

Before preparing the stopzetten checklist, compare the current date to
2026-10-01. If the current date is on or after 2026-10-01, do not generate a
stopzetten checklist. Record that the cutoff has passed and explain that the
remaining handling is through review/change, if estimates are wrong, or through
a separate filing-status review and, when a return will be filed, annual
settlement.

### When the stop option warrants review

The taxpayer receives a monthly refund and wants to stop it. Review the
following reasons with the taxpayer; if only the amount should change or a
deduction applied for part of 2026, compare the full retroactive stop with the
change form before the taxpayer chooses:

- **Deductions no longer apply** — mortgage paid off, alimony ended, insurance premiums stopped
- **Situation changed significantly** — the basis for the refund is no longer valid
- **Want to avoid repayment** — the taxpayer realizes the refund is too high
  and does not want to receive money that a later notice or annual assessment
  may reclaim
- **Prevent further overpayment** — after reviewing whether the selected stop
  is retroactive or prospective, the taxpayer wants to prevent further excess
  refunds

### Process

> **HUMAN-ONLY PORTAL STEPS.** The taxpayer or an authorized human performs
> every step below on their own device. The assistant prepares guidance only
> and must not open or operate the portal, log in, click controls, confirm,
> send, or submit.

1. **Taxpayer:** Log in to Mijn Belastingdienst.
2. **Taxpayer:** Navigate to the existing voorlopige aanslag 2026.
3. **Taxpayer:** Select the option to stop (stopzetten) the monthly refunds.
4. **Taxpayer:** Confirm the request personally.
5. **Taxpayer:** Record the stated processing time (usually within 5 weeks, and always within 8 weeks).
6. **Taxpayer:** Complete stopzetten before 1 October 2026.

### Effect

- A refund based on **deductions** can only be stopped retroactively from
  **1 January 2026**.
- **IACK** can only be stopped retroactively from **1 January 2026**.
- **Algemene heffingskorting** can be stopped from the first day of a selected
  month; this is prospective from that selected/next payment month rather than the
  1 January rule for deductions/IACK.
- If deductions or IACK are stopped after the taxpayer already received money
  in 2026, that amount must be repaid. The Belastingdienst sends a **separate
  notice** for that repayment. Do not net it into an assumed future monthly
  amount.
- Usually the taxpayer hears within 5 weeks and always within 8 weeks. The
  official notice controls when payments stop and when any repayment is due.
- A later annual return can reconcile the position if the taxpayer has a filing
  obligation or otherwise files. Stopzetten itself does not make annual filing
  mandatory for everyone.

### Common reasons

| Reason                                | Action after stopzetten                        |
|---------------------------------------|------------------------------------------------|
| Mortgage paid off                     | Full stop is backdated to 1 January; consider change if part-year deduction should remain in the estimate |
| Alimony ended                         | Full stop is backdated to 1 January; consider change if part-year deduction should remain in the estimate |
| Income increased significantly        | Consider change instead to keep partial refund |
| Moving abroad                         | Residency review; not a categorical stopzetten reason |
| Want to avoid later repayment risk    | Review retroactive/prospective effect; later notice or filed annual return can reconcile amounts |

---

## Monthly PAYMENT (betaling) — CHANGE, not stop

### Why stopzetten is wrong for payment correction

If the taxpayer currently pays a monthly amount and the amount is wrong (too
high), the available correction path is to CHANGE the voorlopige aanslag, not
to stop it. Official stopzetten guidance applies to monthly refunds, not
monthly payment cases.

**Simply ceasing payments when tax is owed does NOT reduce the tax
obligation.** It can create arrears under the existing beschikking. The
taxpayer should use the official change route and follow the payment terms on
the current or replacement notice; do not predict a later annual lump sum as a
certainty.

### Payment cases cannot use stopzetten

The workpack must not provide a stopzetten checklist for a taxpayer who pays monthly. Route to the change flow so the full 2026 estimate can be recalculated.

### Better alternative: change the voorlopige aanslag

- Change the voorlopige aanslag to reflect the correct, lower income or higher deductions
- The Belastingdienst recalculates the monthly payment based on the new estimates
- A replacement beschikking may adjust future payments or refunds
- The actual amount and timing come from the portal calculation and the new
  beschikking, not the workpack estimate
- The taxpayer maintains a smooth payment schedule

### How to redirect

When a user who pays monthly wants to stop because the amount is wrong:

1. Explain that stopping will not reduce what they owe
2. Explain that simply ceasing payment can create arrears under the current
   beschikking and does not correct the estimate
3. Recommend changing the voorlopige aanslag instead
4. If the user agrees, transition to the change subflow and mutate progress before asking the next question:
   - set `active_workflow: provisional_2026_change`
   - set `provisional_2026.subflow: change`
   - copy the payment baseline into the `baseline` subsection
   - mark `stopzetten_direction` complete with `routed_to_change_payment_case`
   - reset `confirm` to `not_started`
5. If the user still asks to stop a monthly payment case, state that stopzetten is not available for payment cases and continue with the change flow

This state mutation prevents the next turn from re-entering the stopzetten prompt loop.

---

## Monthly PAYMENT (betaling) — amount is correct

If the taxpayer pays a monthly amount and the amount is correct, no action is needed. Confirm that the voorlopige aanslag appears to be aligned with their current situation and no changes are required.

---

## Edge case: user wants to stop because they will file early

Some taxpayers want to stop their voorlopige aanslag because they plan to file the annual return early and settle then. In this case:

- Explain that, when a 2026 annual return is filed, its assessment reconciles
  the provisional refunds or payments against the annual result
- Stopzetten is only an option if the taxpayer is receiving a monthly refund; payment cases must use the change flow
- If the taxpayer receives a monthly refund and wants to avoid further refunds in the interim, stopzetten can be appropriate until 1 October 2026
- Check the annual filing obligation separately. If the taxpayer must file, or
  otherwise files, the return can reconcile the provisional amounts;
  stopzetten does not make filing universally required.

---

## Manual checklist for stopzetten (for inclusion in workpack)

When stopzetten is the appropriate action, include this checklist:

```
## Stopzetten checklist

**HUMAN-ONLY PORTAL STEPS:** You, the taxpayer or an authorized human, perform
all portal steps below on your own device. The assistant must not operate the
portal or act on any control.

- [ ] I confirmed that stopping does not eliminate the tax obligation for 2026
- [ ] I identified whether I am stopping deductions, IACK, or the algemene heffingskorting
- [ ] For deductions or IACK: I confirmed the stop is retroactive to 1 January 2026
- [ ] For the algemene heffingskorting: I confirmed the selected first day of the month for prospective payment cessation
- [ ] If deductions or IACK have already been paid: I expect a separate repayment notice for the amount already received
- [ ] I checked the 2026 annual filing obligation separately; stopzetten does not decide it
- [ ] I confirmed that I am receiving a monthly refund; if I pay monthly, I use wijzigen instead
- [ ] I confirmed the current-date cutoff gate showed a date before 1 October 2026
- [ ] I logged in to Mijn Belastingdienst personally
- [ ] I navigated to my voorlopige aanslag 2026
- [ ] I selected the option to stop (stopzetten)
- [ ] I confirmed the request personally
- [ ] I kept the confirmation for my records
```

---

## Safety notes

- Do NOT calculate final tax consequences for the stopzetten subflow unless ALL assumptions are explicitly stated and confirmed by the user
- Stopzetten does not close the tax year. Annual filing is required only when
  the taxpayer has a filing obligation or otherwise chooses/qualifies to file;
  determine that separately.
- Stopzetten is for monthly refunds only; route monthly payment corrections to wijzigen
- If the user's situation is complex (multiple income sources, international elements, business income), recommend consulting a tax adviser before stopping
