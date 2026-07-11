## Stopzetten subflow

### Decision points

1. Does the taxpayer profile exist and contain `provisional_2026_stopzetten`?
2. Is the user receiving a monthly refund (teruggaaf) or paying a monthly amount (betaling)?
   - **Refund → stopzetten may be appropriate until 1 October 2026**
   - **Payment + amount is wrong → REDIRECT to change subflow**
   - **Payment + amount is correct → no action needed**
3. Why does the user want to stop?
   - Deductions no longer apply → stopzetten appropriate
   - Situation changed → review whether change or stopzetten is better
   - Wants to avoid repayment risk → stopzetten appropriate
   - Will file early and settle then → explain that the annual return handles this; stopzetten is only available if the user receives a monthly refund

### Data collection steps

1. **Current voorlopige aanslag type** — receiving refund or making payments
2. **Current monthly amount** — how much per month
3. **Reason for wanting to stop** — to determine correct routing
4. **If redirecting to change:** collect all estimates as per the change subflow

### Output generation

1. Generate `workspace/provisional/2026/provisional-pack.md` with stopzetten context
2. Update `workspace/shared/assumptions.md`
3. If stopzetten is appropriate: include manual checklist for the Mijn Belastingdienst stopzetten process
4. If redirecting a payment case to change, mutate progress before the next question: set `active_workflow: provisional_2026_change`; set `provisional_2026.subflow: change`; write the known monthly amount and any stated beschikking details with provenance to `workspace/provisional/2026/notes/baseline.yaml`; mark the `baseline` subsection `in_progress`; mark `stopzetten_direction` as `complete` with `answered: ["routed_to_change_payment_case"]`; reset `confirm` to `not_started`; then stop using this file and load only `reference/subflows/change.md`.
5. Do NOT calculate final tax consequences unless all assumptions are explicit and confirmed

---
