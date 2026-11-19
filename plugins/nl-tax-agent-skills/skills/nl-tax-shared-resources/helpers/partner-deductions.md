# Helper: Fiscal Partner, Deductions, and Neutral Allocation Scenarios

Internal read-only helper module for `nl-tax-annual-return` and
`nl-tax-provisional-assessment`. Returns fiscal-partner eligibility, sourced
deduction checks, neutral allocation scenarios, and open-question packets to
the owning workflow. Writes nothing.

## Boundaries

- **Only inside an owning workflow.** Apply only when `nl-tax-annual-return` or
  `nl-tax-provisional-assessment` is active. Never persist files, workpacks,
  field maps, or checklists.
- **The partners choose (HARD RULE).** Never rank, recommend, optimize, call
  "best" or "default", or automatically select an allocation. Label scenarios
  neutrally (`Scenario A`, `Scenario B`, or percentages), show traceable effects
  and uncertainty, and record a split only after explicit taxpayer choice (`U:`
  provenance).
- **Annual and provisional stay separate.** Use 2025 notes for annual 2025 and
  2026 provisional notes for provisional 2026. Provisional allocations are
  estimates that affect monthly cash flow and can be changed later or overridden
  in the annual return.
- **Human-only portal & no identifiers.** Follow
  `../nl-tax-shared-resources/runtime-contract.md`: never operate Mijn
  Belastingdienst or record BSN, IBAN, partner names, policy/
  contract/aanslag numbers, or credentials.

## Canonical knowledge sources (never paraphrase rates)

Load only the notes matching the active workflow (resolve relative to the active
owning skill directory):

- **All workflows (when partner rules apply):**
  - `../nl-tax-shared-resources/knowledge/partners/fiscal-partnership.md` (married/registered/unmarried conditions, start/end dates, allocatable vs personal items, death/divorce)
- **Annual 2025:**
  - `../nl-tax-shared-resources/knowledge/years/2025/annual/deductions.md` (persoonsgebonden aftrek categories, drempels, caps, cultural ANBI multiplier, lijfrente, AOV)
  - `../nl-tax-shared-resources/knowledge/years/2025/annual/box1-rates.md`, `own-home.md`, and `credits.md` (bracket rates, high-income deduction-rate cap, heffingskorting phase-outs)
- **Provisional 2026:**
  - `../nl-tax-shared-resources/knowledge/years/2026/provisional/rates-and-credits.md` and `own-home.md` (2026 provisional brackets, cap rate, credits)

Return every consulted `source_id` to the owning workflow for `Sources used` /
Appendix A `sources_loaded`.

## Step 1: Fiscal-partner legal eligibility

Distinguish legal partner status from allocation scenario comparison. Verify
from sourced facts only:

1. Civil status (married, registered partnership, unmarried, separated,
   divorced, widowed) and registered address history in the tax year and prior
   year. Do not assume marriage in-year automatically equals full-year
   partnership without checking address/marriage dates and whole-year choice.
2. For unmarried cohabitants: registered at the same address PLUS at least one
   official condition in `fiscal-partnership.md` (notarial cohabitation
   contract, joint child / recognition, pension partner, joint home ownership,
   qualifying samengesteld gezin, prior-year fiscal partnership, or qualifying
   parent-child rule).
3. **Route special situations to manual review:**
   - **Partner died during the year** (choice between until-death vs whole-year;
     may involve nabestaandenmachtiging / paper forms)
   - **Divorce or separation in-year** (married/registered ends only when BOTH a
     dissolution request is submitted AND registered addresses differ; whole-year
     choice must be asked, never assumed)
   - **Multiple possible partners**
   - **Nonresident partner / emigration / immigration** (resident workflows flag
     manual review; annual M/C belongs to `nl-tax-international-return`)
   - **Complex Box 2 allocation**

## Step 2: Deduction rules & household constraints

Use canonical thresholds, multipliers, caps, and phase-out tables from the
active year's knowledge notes — never guess or recall them:

- **Paid partneralimentatie:** allocatable between whole-year fiscal partners.
  Received partneralimentatie is personal Box 1 income (non-allocatable).
  Kinderalimentatie is not deductible.
- **Zorgkosten:** compute the drempel on **combined household drempelinkomen**,
  not per partner; only the excess above the combined drempel is allocatable.
- **Giften:** periodieke giften require a qualifying deed/written agreement
  (check canonical cap and older-agreement transition rule; record agreement
  date). Gewone giften use the combined household drempel and maximum from
  `deductions.md` (apply any canonical cultural ANBI multiplier before drempel
  and cap).
- **Lijfrentepremie & AOV:** personal to the paying partner; jaarruimte and
  reserveringsruimte depend on that partner's own pension gap (state as fact;
  never recommend who should pay).
- **Restant persoonsgebonden aftrek (carryforward):** record original partner
  and confirmed carryforward amount; eligible whole-year partners may allocate
  it in any 100%-total split.

## Step 3: Neutral scenario modeling & arithmetic invariants

- **Never assume highest marginal rate wins:** model multiple eligible splits
  (e.g., `Scenario A: 50/50`, `Scenario B: 100/0`, `Scenario C: 0/100`) because
  both the canonical high-income deduction-rate cap (`tariefsaanpassing`) and
  `algemene heffingskorting` phase-out (which depends on verzamelinkomen, unlike
  `arbeidskorting`) materially alter the combined result.
- **Own-home saldo & consistency:** full-year fiscal partners may allocate the
  net eigen woning saldo in any split totaling 100%, regardless of legal
  ownership share (ownership-share rules govern only when co-owners are not
  fiscal partners). Both partners must file the exact same allocation across
  their returns.
- **Provisional 2026 proportionality & uncertain partner status:** focus on the
  largest estimated items (mortgage interest and joint Box 3 grondslag —
  fictitious method only, never werkelijk rendement) using simple splits
  (`50/50`, `100/0`, `0/100`) with explicit uncertainty notes. If partner
  status is uncertain during 2026 (e.g., considering moving in together or
  possible separation), prepare the provisional assessment on the current
  situation and note that it can be changed later if circumstances change.
- **Explicit invariants (record `check_performed_by: checked_by_agent`):**
  1. Set real boolean `has_fiscal_partner` from reviewed facts (never defaulted).
  2. Set real boolean `allocatable` on EVERY row from `fiscal-partnership.md`
     (never inferred from a row label).
     - *Allocatable:* own-home saldo, Hillen deduction, Box 2 income, joint Box 3
       grondslag, paid partner alimony, zorgkosten excess, giften, prior-year
       persoonsgebonden aftrek remainder.
     - *Non-allocatable (personal):* employment/pension/benefit income, business
       profit, ROW, TBS, received alimony, lijfrente/AOV premiums, public
       transport deduction, negative personal deductions.
  3. Check every row: `taxpayer_pct` and `partner_pct` are finite numbers in
     `0..100` with `taxpayer_pct + partner_pct == 100`.
  4. Every non-allocatable row MUST be `100/0` or `0/100`.
  5. When `has_fiscal_partner` is `false`, `partner_pct` MUST be `0`.

## Question packet format

```yaml
- question_id: "partner.eligibility.cohabitation_conditions"
  workflow: "annual_2025"
  section: "partner.eligibility"
  prompt_for_user: "Are you registered at the same address as your partner, and do you have a notarial cohabitation contract, joint home, joint child, or pension-partner status?"
  acceptable_sources: ["user_chat"]
  evidence_hint: null
- question_id: "annual.deductions.giften.amount"
  workflow: "annual_2025"
  section: "deductions.giften"
  prompt_for_user: "What was the total ANBI-qualifying donation amount in 2025? You can provide one total or attach receipts."
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "donation receipts"
```
