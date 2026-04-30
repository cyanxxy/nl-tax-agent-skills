# Rule note: Stopping a voorlopige aanslag 2026 (stopzetten)

source_id: bd_provisional_stopzetten_2026
workflow: provisional_assessment
tax_year: 2026
status: active
last_reviewed: "2026-04-30"
review_status: reviewed

## Rule

Stopzetten means stopping the monthly payments or refunds of a voorlopige aanslag. This is primarily relevant when the taxpayer RECEIVES a monthly refund (teruggaaf) and wants to stop it. Stopping does not mean the taxpayer no longer owes tax -- it defers the settlement to the annual return.

## When stopzetten is appropriate

### Receiving a monthly refund (teruggaaf)

Stopzetten is the correct action when:

- The deductions that justified the refund no longer apply (e.g., mortgage paid off, alimony ended)
- The taxpayer wants to avoid receiving money that will need to be repaid later
- The taxpayer's situation has changed and the refund is no longer justified
- The taxpayer prefers to settle everything at annual return time

### Paying a monthly amount (betaling)

If the taxpayer currently PAYS a monthly amount and the amount is wrong:

- The correct path is usually to CHANGE the voorlopige aanslag (see change-flow.md), not to stop it
- Stopping payments when tax is owed can result in a large bill at annual return time
- Only consider stopping if the taxpayer has strong reasons and understands the consequence

## How to stop

1. Log in to Mijn Belastingdienst with DigiD
2. Navigate to the existing voorlopige aanslag 2026
3. Select the option to stop (stopzetten) the monthly payments or refunds
4. Confirm the request

## Effect of stopzetten

- Monthly payments or refunds stop after processing
- No further amounts are collected or paid out for the remainder of the year
- The final settlement happens when the annual return for 2026 is filed (in 2027)
- Any tax owed or overpaid is reconciled at that time
- Interest may apply on underpayments at annual return time

## Warning

Stopping a voorlopige aanslag does NOT mean:

- That no tax is owed for 2026
- That the Belastingdienst will not collect what is due
- That the annual return is not required

It only means that monthly payments/refunds are paused. The full tax obligation is determined and settled when the annual return is filed.

## Developer instruction

When a user asks about stopping their voorlopige aanslag:

1. First determine whether the user is receiving a refund or making payments
2. If receiving a refund: stopping is straightforward -- explain that refunds will cease and settlement happens at annual return
3. If making payments: strongly recommend CHANGING the voorlopige aanslag instead of stopping it
   - Explain the risk of a large lump-sum bill at annual return time
   - Only proceed with stopzetten if the user explicitly confirms after understanding the risk
4. In all cases, warn that stopping does not eliminate the tax obligation
5. Direct the user to the Mijn Belastingdienst portal for the actual action

## Common failure

Do not conflate stopzetten with "cancelling" the tax obligation. Stopzetten only stops the monthly cash flow. The underlying tax liability remains and will be settled at annual return time. Never suggest that stopping a voorlopige aanslag means the taxpayer no longer owes anything.
