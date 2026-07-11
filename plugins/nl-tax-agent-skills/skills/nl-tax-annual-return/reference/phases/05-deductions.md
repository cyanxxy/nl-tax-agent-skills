## Phase 5 — Deductions compilation

Compile all deductible items from evidence and user-provided data.

### 5.1 Alimentatie

- Check for partneralimentatie payments (deductible)
- Verify: kinderalimentatie is NOT deductible -- flag if the user attempts to claim it
- Evidence: court order or divorce agreement, plus bank statements showing payments
- Record: total annual amount, evidence_id, assumption_id if amount is estimated

### 5.2 Specifieke zorgkosten (medical expenses)

- Inventory potentially qualifying medical expenses. Reimbursed costs,
  premiums, and the statutory excess are excluded. **Wheelchair: not deductible**; scooters and home modifications are also not deductible
  healthcare costs for 2025.
- Apply the zorgkosten drempel and any multiplier only if the complete reviewed
  2025 table and all inputs are present; otherwise record **threshold: manual review** and do not calculate a deductible result.
- Drempelinkomen = combined income of both partners before persoonsgebonden aftrek
- Only the amount above the drempel is deductible
- Note the multiplier for certain specific zorgkosten categories
- Evidence: receipts, insurance reimbursement statements

### 5.3 Giften (charitable donations)

- Distinguish between periodieke giften (no threshold; **EUR 1.5 million** 2025
  cap subject to the reviewed **transition** rule) and gewone giften (with
  threshold and cap).
- Periodieke giften: verify the notarial deed or written agreement for 5+ years,
  record its date, and route uncertain transition-rule facts to manual review.
- Gewone giften: threshold 1% of drempelinkomen (min EUR 60), cap 10% of drempelinkomen
- Cultural ANBI multiplier: 1.25x up to EUR 1,250 additional
- Verify ANBI registration of recipient organizations
- Evidence: receipts, bank statements, ANBI registration confirmation

### 5.4 Lijfrentepremie (annuity premium)

- Collect premiums paid for lijfrente products
- Calculate jaarruimte and reserveringsruimte only if the exact reviewed 2025 source rules and required inputs are present; otherwise flag the limit and deductible amount for manual review
- Required inputs normally include employment income, pension accrual (factor A), and unused jaarruimte of prior years
- Evidence: annual statement from lijfrente provider, factor A statement from employer

### 5.5 Other deductions

- A qualifying private AOV premium belongs to the **private income-provision category**, **not ordinary business costs**. Inventory the policy and annual
  insurer statement; ambiguous policy types and exact deductibility are manual
  review. Do not reduce business profit by the AOV premium.
- Studiekosten / scholingsuitgaven: collect only as a manual-review item unless a reviewed official source is added
- Restant persoonsgebonden aftrek from prior years; eligible whole-year fiscal partners may allocate this prior-year personal-deduction remainder, subject to traceable scenarios and taxpayer review
- Any other qualifying deductions from the profile or evidence

### 5.6 Deduction summary

- Total persoonsgebonden aftrek
- Note the allocation order: box 1 first, then box 3, then box 2
- If fiscal partners: note allocation options and model scenarios; do not assume the highest marginal-rate partner is always best. Partner allocation of these deductions is finalized in Phase 6 via `nl-tax-partner-deductions`.

---
