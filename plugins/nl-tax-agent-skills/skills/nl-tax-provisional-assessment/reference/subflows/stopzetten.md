## Stopzetten subflow

### Conversational review checkpoints

1. Does the taxpayer profile exist and contain `provisional_2026_stopzetten`?
2. Is the user receiving a monthly refund (teruggaaf) or paying a monthly amount (betaling)?
   - **Refund → stopzetten may be appropriate until 1 October 2026**
   - **Payment + amount is wrong → REDIRECT to change subflow**
   - **Payment + amount is correct → no action needed**
3. Why does the user want to stop?
   - Deductions no longer apply → compare a full stop backdated to 1 January
     with a change when a part-year deduction should remain in the estimate;
     let the taxpayer choose after reviewing both effects
   - Situation changed → review whether change or stopzetten is better
   - Wants to avoid repayment risk → stopzetten appropriate
   - Will file early and settle then → check the filing obligation separately;
     if a return is filed it can reconcile the provisional amounts, but
     stopzetten is only available if the user receives a monthly refund
4. Which part is being stopped?
   - **Deductions or IACK** → the official effect is retroactive to 1 January
     2026; separately explain repayment of amounts already received and the
     separate Belastingdienst notice
   - **Algemene heffingskorting** → record the selected first day of the month;
     the payment effect is prospective from that selected/next payment month

### Data collection steps

1. **Current voorlopige aanslag type** — receiving refund or making payments
2. **Current monthly amount** — how much per month
3. **Reason for wanting to stop** — to determine correct routing
4. **Refund component and prior payments** — deductions, IACK, or algemene
   heffingskorting; record the amount already received without netting it into
   a future-payment guess
5. **Annual filing status** — required / not required / unresolved / plans to
   file; never infer a universal filing duty from stopzetten
6. **If redirecting to change:** collect all estimates as per the change subflow

### Output generation

1. Generate `workspace/provisional/2026/provisional-pack.md` with stopzetten context
2. Update `workspace/shared/assumptions.md`
3. If stopzetten is appropriate: include manual checklist for the Mijn Belastingdienst stopzetten process
   and explain the selected component's retroactive or prospective effect;
   show any repayment of prior 2026 deductions/IACK payments as a separate
   notice item
4. If redirecting a payment case to change, mutate progress before the next question: set `active_workflow: provisional_2026_change`; set `provisional_2026.subflow: change`; write the known monthly amount and any stated beschikking details with provenance to `workspace/provisional/2026/notes/baseline.yaml`; mark the `baseline` subsection `in_progress`; mark `stopzetten_direction` as `complete` with `answered: ["routed_to_change_payment_case"]`; reset `confirm` to `not_started`; then stop using this file and load only `reference/subflows/change.md`.
5. Do NOT calculate final tax consequences unless all assumptions are explicit and confirmed

---
