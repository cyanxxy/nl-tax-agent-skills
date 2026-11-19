---
type: llm
weight: 1
---
PASS only if the response satisfies these requirements:

- Computes 2025 eigenwoningforfait = EUR 400,000 * 0.35% = EUR 1,400 (confirming
  peildatum 1 January 2024).
- Includes BOTH mortgage interest (EUR 9,200) and periodic erfpacht (EUR 800) in
  `total_deductible_own_home_costs` = EUR 10,000, with Hillen deduction = EUR 0.
- Computes `box1_own_home_balance` = EUR 1,400 - EUR 10,000 = -EUR 8,600.
- Recognizes that Box 1 income exceeds the 2025 schijf 2 boundary (EUR 76,817),
  so tariefsaanpassing applies (49.50% minus 37.48% cap = 12.02%), and keeps
  tariefsaanpassing strictly SEPARATE from `box1_own_home_balance` and taxable
  Box 1 income (as a tax-benefit adjustment computed by the portal).
- Stays focused on verifying the eigen woning section (mentions checking VIA
  figures against the WOZ-beschikking / hypotheek jaaroverzicht) without forcing
  a full 14-phase survey or pretending this single section is a complete return
  workpack.
- Never attempts portal control and writes no file.
