# Stopzetten Guidance — When to Stop vs When to Change

## Purpose

This document provides the decision logic for determining whether stopzetten (stopping) a voorlopige aanslag is the correct action, or whether changing it is more appropriate. Incorrect routing can lead to unexpected large tax bills for the taxpayer.

---

## Decision matrix

| Current situation         | User wants to...             | Correct action     |
|---------------------------|------------------------------|--------------------|
| Receives monthly refund   | Stop receiving refunds       | Stopzetten         |
| Receives monthly refund   | Reduce refund amount         | Change             |
| Pays monthly amount       | Stop because amount is wrong | Change (NOT stop)  |
| Pays monthly amount       | Reduce monthly payment       | Change             |
| Pays monthly amount       | Amount is correct            | No action needed   |

---

## Monthly REFUND (teruggaaf) — stopzetten may be appropriate

### When stopzetten is the right action

The taxpayer receives a monthly refund and wants to stop it. This is appropriate when:

- **Deductions no longer apply** — mortgage paid off, alimony ended, insurance premiums stopped
- **Situation changed significantly** — the basis for the refund is no longer valid
- **Want to avoid repayment** — the taxpayer realizes the refund is too high and does not want to receive money that will need to be repaid when the annual return is filed
- **Preference for settlement at annual return** — the taxpayer prefers to handle everything at annual return time rather than receiving monthly refunds

### Process

1. Log in to Mijn Belastingdienst using DigiD
2. Navigate to the existing voorlopige aanslag 2026
3. Select the option to stop (stopzetten) the monthly refunds
4. Confirm the request
5. Processing time: typically within a few weeks

### Effect

- Monthly refunds stop after processing
- No further amounts are paid out for the remainder of the year
- The final settlement happens when the annual return for 2026 is filed (in 2027)
- Any tax owed or overpaid is reconciled at annual return time
- If the taxpayer received more refund than entitled to, the excess must be repaid at annual return time

### Common reasons

| Reason                                | Action after stopzetten                        |
|---------------------------------------|------------------------------------------------|
| Mortgage paid off                     | Refunds stop; settlement at annual return      |
| Alimony ended                         | Refunds stop; settlement at annual return      |
| Income increased significantly        | Consider change instead to keep partial refund |
| Moving abroad                         | Stopzetten; consult adviser for tax residency  |
| Want to avoid year-end repayment risk | Refunds stop; final amount determined at annual return |

---

## Monthly PAYMENT (betaling) — CHANGE, not stop

### Why stopzetten is wrong for payment correction

If the taxpayer currently pays a monthly amount and the amount is wrong (too high), the correct path is to CHANGE the voorlopige aanslag, not to stop it.

**Stopping payments when tax is owed does NOT reduce the tax obligation.** It only defers the payment to annual return time, where the full amount becomes due as a lump sum — potentially with interest.

### What happens if the user stops payments anyway

- Monthly payments stop
- The tax obligation for 2026 does NOT change
- When the annual return for 2026 is filed (in 2027), the Belastingdienst calculates the total tax owed
- The amount previously collected through monthly payments is subtracted
- The remaining balance is due as a single payment
- This balance may be large and unexpected
- Interest (invorderingsrente) may apply on the unpaid amount

### Better alternative: change the voorlopige aanslag

- Change the voorlopige aanslag to reflect the correct, lower income or higher deductions
- The Belastingdienst recalculates the monthly payment based on the new estimates
- Monthly payments decrease to the correct level
- No lump-sum surprise at annual return time
- The taxpayer maintains a smooth payment schedule

### How to redirect

When a user who pays monthly wants to stop because the amount is wrong:

1. Explain that stopping will not reduce what they owe
2. Explain the risk of a large lump-sum bill at annual return time
3. Recommend changing the voorlopige aanslag instead
4. If the user agrees, transition to the change subflow
5. If the user insists on stopping despite understanding the risk, document their decision in the assumptions section but still recommend change

---

## Monthly PAYMENT (betaling) — amount is correct

If the taxpayer pays a monthly amount and the amount is correct, no action is needed. Confirm that the voorlopige aanslag appears to be aligned with their current situation and no changes are required.

---

## Edge case: user wants to stop because they will file early

Some taxpayers want to stop their voorlopige aanslag because they plan to file the annual return early and settle then. In this case:

- Explain that the annual return process handles the settlement automatically
- When the annual return for 2026 is filed, the Belastingdienst reconciles the provisional payments/refunds against the final tax amount
- Stopping the voorlopige aanslag is optional in this case — the annual return will settle the difference regardless
- If the taxpayer wants to stop to avoid further payments/refunds in the interim, stopzetten is acceptable
- Make sure the taxpayer understands that filing the annual return is required regardless of whether the voorlopige aanslag is stopped

---

## Manual checklist for stopzetten (for inclusion in workpack)

When stopzetten is the appropriate action, include this checklist:

```
## Stopzetten checklist

- [ ] Confirm you understand that stopping does not eliminate the tax obligation for 2026
- [ ] Confirm you understand that settlement occurs when the annual return for 2026 is filed
- [ ] If you received refunds that were too high, you may need to repay the excess at annual return time
- [ ] Log in to Mijn Belastingdienst using your DigiD
- [ ] Navigate to your voorlopige aanslag 2026
- [ ] Select the option to stop (stopzetten)
- [ ] Confirm the request
- [ ] Keep the confirmation for your records
```

---

## Safety notes

- Do NOT calculate final tax consequences for the stopzetten subflow unless ALL assumptions are explicitly stated and confirmed by the user
- Stopzetten does not mean the tax year is closed — the annual return is still required
- If the user's situation is complex (multiple income sources, international elements, business income), recommend consulting a tax adviser before stopping
- Do not share DigiD credentials with this tool
