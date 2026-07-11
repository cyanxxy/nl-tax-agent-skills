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
- Load the reviewed 2025 drempel and increase rules from `deductions.md`. Ask for
  full-year partner status, drempelinkomen, AOW age on 1 January 2025, and a
  category-level expense breakdown before calculating. If an input is missing,
  name it and leave the result for review rather than guessing.
- Drempelinkomen = boxes 1, 2, and 3 before persoonsgebonden aftrek; combine it
  only for full-year fiscal partners or an elected full-year partnership
- Only the amount above the drempel is deductible
- Note the multiplier for certain specific zorgkosten categories
- Screen for the EUR 925 mobility forfait by asking whether the person can walk
  more than 100 metres independently, what evidence supports that fact, and
  which reimbursements were received or available
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
- For jaarruimte 2025, gather the requested 2024 income and pension-accrual/UPO
  inputs and use the official Belastingdienst Hulpmiddel Lijfrentepremie
- For reserveringsruimte, gather 2015-2024 unused-jaarruimte and actual-payment
  history; apply the official tool result and the EUR 42,108 2025 cap
- Evidence: provider annual statement, UPO/factor-A evidence, historical room
  and payment records, and saved official-tool result

### 5.5 Other deductions

- A qualifying private AOV premium belongs to the **private income-provision category**, **not ordinary business costs**. Inventory the policy and annual
  insurer statement; ambiguous policy types and exact deductibility are manual
  review. Do not reduce business profit by the AOV premium.
- Studiekosten: ordinary expenses are not deductible. Screen only for the narrow
  pre-1 July 2015 prestatiebeurs exception, requiring a final DUO notice that
  the grant was not converted into a gift after the diploma period expired
- Restant persoonsgebonden aftrek from prior years; eligible whole-year fiscal partners may allocate this prior-year personal-deduction remainder, subject to traceable scenarios and taxpayer review
- Any other qualifying deductions from the profile or evidence

### 5.6 Deduction summary

- Total persoonsgebonden aftrek
- Note the allocation order: box 1 first, then box 3, then box 2
- If fiscal partners: note allocation options and model scenarios; do not assume the highest marginal-rate partner is always best. Partner allocation of these deductions is finalized in Phase 6 via `nl-tax-partner-deductions`.

---
