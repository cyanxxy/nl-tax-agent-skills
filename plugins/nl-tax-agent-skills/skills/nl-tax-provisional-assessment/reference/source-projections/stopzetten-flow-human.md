# Human-only runtime projection: stopzetten-flow.md

projection_version: "1"
derived_from: skills/_shared/knowledge/years/2026/provisional/stopzetten-flow.md
derived_note_sha256: e6b1cc970721a14a3a8f7ace8ef8c8d518fb33ba8b2d1086dc22352aaee4f729
source_ids: bd_provisional_stopzetten_2026

This is a mechanically reversible runtime projection, not an independently reviewed tax note. The cited reviewed snapshot remains the provenance authority. The only permitted body transformation is inserting `**Taxpayer:**` before portal-action imperatives.

## Rule

Stopzetten is available for a voorlopige aanslag where the taxpayer RECEIVES a
monthly refund (teruggaaf) and wants to stop all or an eligible part of that
refund. If the taxpayer pays a monthly amount, they cannot use stopzetten; they
must change the voorlopige aanslag instead. Stopping a refund does not cancel
the underlying 2026 tax position.

## When stopzetten is appropriate

Moving abroad requires a residency review and is **not a categorical stopzetten reason**. Route migration or international-residency facts to the unsupported residency/migration path; do not generate stopzetten guidance solely because the taxpayer is moving abroad.

### Current-date cutoff gate

Before offering a stopzetten checklist, compare the current date to 2026-10-01.
If the current date is on or after 2026-10-01, do not generate a stopzetten
checklist. Record that the cutoff has passed and route the user to review/change
if estimates are wrong, or to a separate filing-status review and annual
settlement only when a return will be filed.

### Receiving a monthly refund (teruggaaf)

Stopzetten can be available for review when:

- The deductions that justified the refund no longer apply (e.g., mortgage paid off, alimony ended)
- The taxpayer wants to avoid receiving money that will need to be repaid later
- The taxpayer's situation has changed and the refund is no longer justified
- The taxpayer understands whether the selected stop has a retroactive or
  prospective effect and wants to prevent further overpayment

If a deduction applied for part of 2026 and the taxpayer wants that part-year
amount retained in the provisional estimate, discuss the change form as an
alternative to a full deductions stop that is backdated to 1 January. The
agent presents both effects and records the taxpayer's choice; it does not make
the choice automatically.

### Paying a monthly amount (betaling)

If the taxpayer currently PAYS a monthly amount and the amount is wrong:

- The correct path is to CHANGE the voorlopige aanslag (see change-flow.md), not to stop it
- Official stopzetten guidance does not allow stopping a monthly payment case
- Simply ceasing payments can create arrears under the current beschikking; it
  does not correct the estimate

## How to stop

1. **Taxpayer:** Log in to Mijn Belastingdienst
2. **Taxpayer:** Navigate to the existing voorlopige aanslag 2026
3. **Taxpayer:** Select the option to stop (stopzetten) the monthly refund
4. **Taxpayer:** Confirm the request
5. Stopzetten can be done until 1 October 2026

## Effect of stopzetten

First identify what is being stopped; the effects are not interchangeable:

- **Deductions / the refund based on deductions:** stopzetten works
  retroactively from **1 January 2026**.
- **Inkomensafhankelijke combinatiekorting (IACK):** stopzetten also works
  retroactively from **1 January 2026**.
- **Algemene heffingskorting:** this can be stopped from the first day of a
  selected month. Treat the effect as prospective from that selected/next
  payment month, not as the 1 January retroactive rule used for deductions and
  IACK.
- When deductions or IACK are stopped after payments have already been made,
  the taxpayer must repay the amount already received in 2026. The
  Belastingdienst sends a **separate notice** about that repayment; do not fold
  it into a guessed next monthly amount.
- The Belastingdienst usually responds within 5 weeks and always within 8
  weeks. Actual payment cessation and any repayment timing are controlled by
  that notice, not by the workpack estimate.
- If the taxpayer must file a 2026 annual return, or later chooses/qualifies to
  file one, the annual result can reconcile the provisional amounts. Stopping
  a refund does **not by itself** establish that every taxpayer must file an
  annual return.

## Warning

Stopping a voorlopige aanslag does NOT mean:

- That no tax is owed for 2026
- That the Belastingdienst will not collect what is due
- That prior 2026 payments disappear; deductions/IACK may create a separate
  repayment notice because the stop is backdated to 1 January 2026

It changes the selected provisional refund stream. Whether a 2026 annual
return must be filed is a separate filing-obligation question; do not state
that stopzetten itself makes filing universally required.

## Developer instruction

When a user asks about stopping their voorlopige aanslag:

1. First determine whether the user is receiving a refund or making payments
2. If receiving a refund: first apply the current-date cutoff gate, then ask
   whether the refund is based on deductions, IACK, or the general credit.
   Explain the correct 1 January retroactive or monthly prospective effect,
   and keep any prior-payment repayment separate from future cash flow
3. If making payments: route to CHANGING the voorlopige aanslag; do not offer stopzetten
   - Explain that simply ceasing payment can create arrears under the current
     beschikking and does not correct the estimate
   - Mutate session state before the next question: set `active_workflow: provisional_2026_change`, set `provisional_2026.subflow: change`, copy the payment baseline into the `baseline` subsection, mark `stopzetten_direction` complete with `routed_to_change_payment_case`, and reset `confirm` to `not_started`
4. Warn that stopping a refund does not eliminate the tax obligation and does
   not by itself decide the taxpayer's annual filing obligation
5. Direct the user to the Mijn Belastingdienst portal for the actual action only when the cutoff gate is before 2026-10-01

## Common failure

Do not conflate stopzetten with "cancelling" the tax obligation. Never apply
the general-credit monthly rule to deductions or IACK, and never hide the
separate repayment of amounts already received. Do not say every taxpayer must
file solely because a provisional refund was stopped.

Do not leave a payment case in `provisional_2026_stopzetten` after redirecting it. Copy the payment baseline into the change subflow so the change flow can continue from the same beschikking without re-asking the stopzetten direction question.
