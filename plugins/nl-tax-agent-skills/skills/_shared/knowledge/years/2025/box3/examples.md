# Rule note: Box 3 worked examples -- fictitious vs actual return 2025

source_ids: bd_box3_2025_calc, bd_box3_2025_actual_return
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-05-15"
review_status: reviewed

## Rule

These worked examples illustrate the box 3 calculation methods for tax year 2025. They demonstrate both the fictitious return (forfaitair rendement) and the actual return (werkelijk rendement) approaches and their comparison.

Use these constants for 2025 annual return examples:

- Banktegoeden: 1.37%
- Beleggingen en andere bezittingen: 5.88%
- Schulden: 2.70%
- Box 3 tax rate: 36%
- Heffingsvrij vermogen: EUR 57,684 per person
- Drempel schulden: EUR 3,800 per person (EUR 7,600 combined for fiscal partners)

---

## Example 1: Savings only, single taxpayer

### Facts

- Taxpayer: single, no fiscal partner
- Savings account on 1 January 2025: EUR 150,000
- No investments and no debts
- Actual interest received in 2025: EUR 1,200

### Fictitious return calculation

| Step | Description | Amount |
|------|-------------|--------|
| 1 | Belastbaar rendement: EUR 150,000 x 1.37% | EUR 2,055 |
| 2 | Rendementsgrondslag | EUR 150,000 |
| 3 | Grondslag sparen en beleggen: EUR 150,000 - EUR 57,684 | EUR 92,316 |
| 4 | Aandeel in rendementsgrondslag: EUR 92,316 / EUR 150,000 | 61.54% |
| 5 | Box 3 income: EUR 2,055 x 61.54% | EUR 1,264 |
| 6 | Box 3 tax: EUR 1,264 x 36% | EUR 455 |

### Actual return calculation

| Description | Amount |
|-------------|--------|
| Interest received | EUR 1,200 |
| Total actual return for tax comparison | EUR 1,200 |
| Box 3 tax at 36% | EUR 432 |

### Comparison

| Method | Box 3 income | Box 3 tax |
|--------|-------------|-----------|
| Fictitious return | EUR 1,264 | EUR 455 |
| Actual return | EUR 1,200 | EUR 432 |

**Result:** The actual-return method is lower in this example. The official filing environment makes the binding comparison.

---

## Example 2: Mixed portfolio, actual return lower

### Facts

- Taxpayer: single, no fiscal partner
- Savings account on 1 January 2025: EUR 150,000
- Investments and second home on 1 January 2025: EUR 275,000
- Box 3 debt on 1 January 2025: EUR 100,000
- Actual return in 2025:
  - Interest on savings: EUR 1,000
  - Dividends received: EUR 2,500
  - Value decrease on investments and second home: EUR -15,000
  - Interest paid on box 3 debt: EUR -700
  - Custody and transaction costs: not deducted

### Fictitious return calculation

| Step | Description | Amount |
|------|-------------|--------|
| 1 | Aftrekbare schulden: EUR 100,000 - EUR 3,800 | EUR 96,200 |
| 2 | Bank return: EUR 150,000 x 1.37% | EUR 2,055 |
| 3 | Other-assets return: EUR 275,000 x 5.88% | EUR 16,170 |
| 4 | Debt return: EUR 96,200 x 2.70% | EUR -2,597 |
| 5 | Belastbaar rendement | EUR 15,628 |
| 6 | Rendementsgrondslag: EUR 425,000 - EUR 96,200 | EUR 328,800 |
| 7 | Grondslag sparen en beleggen: EUR 328,800 - EUR 57,684 | EUR 271,116 |
| 8 | Aandeel in rendementsgrondslag: EUR 271,116 / EUR 328,800 | 82.45% |
| 9 | Box 3 income: EUR 15,628 x 82.45% | EUR 12,885 |
| 10 | Box 3 tax: EUR 12,885 x 36% | EUR 4,638 |

### Actual return calculation

| Description | Amount |
|-------------|--------|
| Interest received | EUR 1,000 |
| Dividends received | EUR 2,500 |
| Value changes | EUR -15,000 |
| Interest paid on box 3 debt | EUR -700 |
| Total actual return | EUR -12,200 |
| Total actual return for tax comparison | EUR 0 |
| Box 3 tax at 36% | EUR 0 |

### Comparison

| Method | Box 3 income | Box 3 tax |
|--------|-------------|-----------|
| Fictitious return | EUR 12,885 | EUR 4,638 |
| Actual return | EUR 0 | EUR 0 |

**Result:** The actual-return method is lower in this example. Negative actual return is set to EUR 0 for the comparison and is not carried to another year.

---

## Example 3: Fiscal partners, savings only

### Facts

- Two fiscal partners
- Combined savings on 1 January 2025: EUR 150,000
- No investments and no debts
- Combined heffingsvrij vermogen: EUR 115,368
- The partners allocate the grondslag sparen en beleggen 50/50

### Combined fictitious return calculation

| Step | Description | Amount |
|------|-------------|--------|
| 1 | Belastbaar rendement: EUR 150,000 x 1.37% | EUR 2,055 |
| 2 | Rendementsgrondslag | EUR 150,000 |
| 3 | Grondslag sparen en beleggen: EUR 150,000 - EUR 115,368 | EUR 34,632 |
| 4 | Each partner's allocated grondslag | EUR 17,316 |
| 5 | Each partner's aandeel: EUR 17,316 / EUR 150,000 | 11.54% |
| 6 | Box 3 income per partner: EUR 2,055 x 11.54% | EUR 237 |
| 7 | Box 3 tax per partner: EUR 237 x 36% | EUR 85 |

## Developer instruction

When generating box 3 examples or performing calculations in the workpack:

1. Always show the official calculation chain: belastbaar rendement, rendementsgrondslag, grondslag sparen en beleggen, aandeel in rendementsgrondslag, box 3 income, and tax.
2. For actual return comparisons, show both methods side by side with a clear recommendation note.
3. For fiscal partners, compute allocation scenarios for the grondslag sparen en beleggen.
4. Present monetary outputs in whole euros and truncate the aandeel percentage toward zero to two decimal places, matching the official examples.
5. Do not deduct custody fees, transaction costs, management fees, maintenance costs, or adviser fees from actual return.

## Common failure

Do not subtract the full debt amount. First subtract the debt threshold and use only aftrekbare schulden in the return and rendementsgrondslag calculations.

Do not apply the heffingsvrij vermogen before calculating the belastbaar rendement. The heffingsvrij vermogen is only deducted to determine the grondslag sparen en beleggen.
