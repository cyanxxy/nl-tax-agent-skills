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

### 6.4 Allocation recommendations

- Identify each partner's marginal rate and affected credits
- Present allocation scenarios rather than choosing one automatically
- Consider the 2025 tariefsaanpassing/deduction-rate cap for listed deductions (37.48% cap)
- Consider the phase-out of heffingskortingen
- Present at least the default and one optimized allocation for review
- Include any prior-year personal-deduction remainder for eligible whole-year fiscal partners; keep every scenario traceable and require taxpayer review in the official filing environment.

---
