## Phase 6 — Partner handling

If the taxpayer has a fiscal partner, compile the partner section.

Delegate fiscal-partner determination and allocation modelling to
`nl-tax-partner-deductions` under the Helper delegation contract in `SKILL.md`.
Persist the returned facts and open questions in the matching annual notes, ask
the user, and re-invoke the helper with newly sourced answers. The helper
writes nothing; this skill owns `workspace/annual/**` and session state.

### 6.1 Partner status confirmation

- Confirm fiscal partner status on 31 December 2025 (or qualifying part-year partnership)
- Married, registered partnership, or cohabiting with qualifying conditions
- Ask whether the taxpayers want to file together online or submit separate
  returns. Joint filing is permitted for qualifying fiscal partners; it is not
  mandatory. If filing together, both partners review and sign. If filing
  separately, each signs the own return.

### 6.2 Allocatable items

List all items that can be freely allocated between partners:
- Eigen woning result (`box1_own_home_balance`, after all qualifying deductible own-home costs and Hillen)
- Box 2 income from aanmerkelijk belang, when full-year fiscal partner allocation applies
- Box 3 grondslag (assets minus debts)
- Persoonsgebonden aftrek components (alimentatie, zorgkosten, giften, etc.)

### 6.3 Non-allocatable items

List items that are personal and cannot be allocated:
- Arbeidskorting (based on individual arbeidsinkomen)
- Ondernemersaftrek (personal to the ondernemer)
- MKB-winstvrijstelling (personal to the ondernemer)

### 6.4 Allocation comparison scenarios

- Identify each partner's marginal rate and affected credits
- Present allocation scenarios rather than choosing one automatically
- Consider the 2025 tariefsaanpassing/deduction-rate cap for listed deductions (37.48% cap)
- Consider the phase-out of heffingskortingen
- Present at least two clearly labeled comparison scenarios when material,
  showing both partners' percentages, estimated individual and combined
  effects, difference versus Scenario A, assumptions, uncertainty, and sources
- Do not call a scenario default, recommended, optimized, best, or optimal;
  never rank or automatically select one
- Record `Taxpayer-selected allocation: [not selected / user-confirmed split]`
  with `U:` provenance, and leave it unresolved until the taxpayer chooses
- Include any prior-year personal-deduction remainder for eligible whole-year fiscal partners; keep every scenario traceable and require taxpayer review in the official filing environment.
- Never select an allocation for the taxpayer or merely because the returns are filed separately.
  Where allocation is legally available (for example whole-year fiscal
  partners), cross-check the chosen shared entries across both returns: they
  must remain consistent, corresponding percentages must agree, and each
  allocatable item must total no more than 100%. Keep a part-year election or
  separation case as manual review rather than assuming allocation is allowed.

---
