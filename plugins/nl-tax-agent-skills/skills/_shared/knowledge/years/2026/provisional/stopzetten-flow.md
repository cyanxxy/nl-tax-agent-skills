# Rule note: Stopping a voorlopige aanslag 2026 (stopzetten)

source_id: bd_provisional_stopzetten_2026
workflow: provisional_assessment
tax_year: 2026
status: active
last_reviewed: "2026-07-11"
review_status: reviewed

## Rule

Stopzetten is available for a voorlopige aanslag where the taxpayer RECEIVES a monthly refund (teruggaaf) and wants to stop that refund. If the taxpayer pays a monthly amount, they cannot use stopzetten; they must change the voorlopige aanslag instead. Stopping a refund does not mean the taxpayer no longer owes tax -- final settlement happens through the annual return.

## When stopzetten is appropriate

Moving abroad requires a residency review and is **not a categorical stopzetten reason**. Route migration or international-residency facts to the unsupported residency/migration path; do not generate stopzetten guidance solely because the taxpayer is moving abroad.

### Current-date cutoff gate

Before offering a stopzetten checklist, compare the current date to 2026-10-01.
If the current date is on or after 2026-10-01, do not generate a stopzetten
checklist. Record that the cutoff has passed and route the user to review/change
if estimates are wrong, or to annual-return settlement if no provisional change
is available.

### Receiving a monthly refund (teruggaaf)

Stopzetten is the correct action when:

- The deductions that justified the refund no longer apply (e.g., mortgage paid off, alimony ended)
- The taxpayer wants to avoid receiving money that will need to be repaid later
- The taxpayer's situation has changed and the refund is no longer justified
- The taxpayer prefers to settle everything at annual return time

### Paying a monthly amount (betaling)

If the taxpayer currently PAYS a monthly amount and the amount is wrong:

- The correct path is to CHANGE the voorlopige aanslag (see change-flow.md), not to stop it
- Official stopzetten guidance does not allow stopping a monthly payment case
- Stopping payments when tax is owed can result in a large bill at annual return time

## How to stop

1. Log in to Mijn Belastingdienst
2. Navigate to the existing voorlopige aanslag 2026
3. Select the option to stop (stopzetten) the monthly refund
4. Confirm the request
5. Stopzetten can be done until 1 October 2026

## Effect of stopzetten

- Monthly refunds stop after processing
- No further refund amounts are paid out for the remainder of the year
- The final settlement happens when the annual return for 2026 is filed (in 2027)
- Any tax owed or overpaid is reconciled at that time
- Interest may apply on underpayments at annual return time

## Warning

Stopping a voorlopige aanslag does NOT mean:

- That no tax is owed for 2026
- That the Belastingdienst will not collect what is due
- That the annual return is not required

It only means that monthly refunds are stopped. The full tax obligation is determined and settled when the annual return is filed.

## Developer instruction

When a user asks about stopping their voorlopige aanslag:

1. First determine whether the user is receiving a refund or making payments
2. If receiving a refund: first apply the current-date cutoff gate, then explain that refunds will cease and settlement happens at annual return
3. If making payments: route to CHANGING the voorlopige aanslag; do not offer stopzetten
   - Explain the risk of a large lump-sum bill at annual return time
   - Mutate session state before the next question: set `active_workflow: provisional_2026_change`, set `provisional_2026.subflow: change`, copy the payment baseline into the `baseline` subsection, mark `stopzetten_direction` complete with `routed_to_change_payment_case`, and reset `confirm` to `not_started`
4. Warn that stopping a refund does not eliminate the tax obligation
5. Direct the user to the Mijn Belastingdienst portal for the actual action only when the cutoff gate is before 2026-10-01

## Common failure

Do not conflate stopzetten with "cancelling" the tax obligation. Stopzetten only stops the monthly cash flow. The underlying tax liability remains and will be settled at annual return time. Never suggest that stopping a voorlopige aanslag means the taxpayer no longer owes anything.

Do not leave a payment case in `provisional_2026_stopzetten` after redirecting it. Copy the payment baseline into the change subflow so the change flow can continue from the same beschikking without re-asking the stopzetten direction question.
