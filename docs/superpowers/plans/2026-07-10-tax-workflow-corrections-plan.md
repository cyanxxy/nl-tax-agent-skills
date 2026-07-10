# Tax and Workflow Corrections Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Correct every audited non-security tax claim and make annual/provisional workflow state, entrepreneur scope, helper ownership, and field-map readiness truthful.

**Architecture:** Canonical official-source notes define each supported rule; workflows and templates consume those notes without duplicating contrary logic. The LLM owns judgment and persistence, the field mapper is the sole map writer, and unsupported calculations remain visible manual-review items.

**Tech Stack:** Agent Skills Markdown/YAML, Python `unittest` contract tests, offline YAML fixtures, existing optional arithmetic helpers.

## Global Constraints

- Execute before `2026-07-10-optional-python-tooling-plan.md`; this plan defines
  the final formulas and workflow contracts that optional checks must mirror.
- Do not edit Python security/privacy behavior or `PRIVACY.md`/`SECURITY.md`.
- Use only reviewed 2025 annual and 2026 provisional official sources.
- No missing formula is reconstructed from memory.
- Annual entrepreneur support is preparation-only for the business section.
- Provisional entrepreneur support is a sourced expected-profit forecast in `Winst uit onderneming`, not generic other income.
- The field mapper alone writes `field-map.yaml`; orchestrators invoke it.
- Helpers return facts/questions; the owning workflow persists them.
- Every changed claim has a failing test first and an explicit `source_id`.

---

### Task 1: Create the official tax-policy contract suite

**Files:**
- Create: `plugins/nl-tax-agent-skills/tests/test_tax_content_repairs.py`
- Read: `plugins/nl-tax-agent-skills/skills/_shared/source-register.yaml`

**Interfaces:**
- Consumes: canonical knowledge note and every consuming workflow/template path.
- Produces: reusable `assert_claim` helpers that require a registered official source, correct year, required wording, and forbidden wording.

- [ ] **Step 1: Write the contract helper and healthcare RED tests**

```python
from pathlib import Path
import unittest
import yaml

PLUGIN = Path(__file__).resolve().parents[1]
SKILLS = PLUGIN / "skills"

class TaxContentRepairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        register = yaml.safe_load(
            (SKILLS / "_shared/source-register.yaml").read_text(encoding="utf-8")
        )
        cls.sources = {item["id"]: item for item in register["sources"]}

    def assert_official_source(self, source_id, year):
        source = self.sources[source_id]
        self.assertTrue(source["url"].startswith("https://"))
        self.assertEqual(source.get("tax_year"), year)

    def assert_text_contract(self, relative, required=(), forbidden=()):
        text = (SKILLS / relative).read_text(encoding="utf-8").lower()
        for token in required:
            self.assertIn(token.lower(), text)
        for token in forbidden:
            self.assertNotIn(token.lower(), text)

    def test_healthcare_exclusions_and_manual_threshold(self):
        self.assert_official_source("bd_zorgkosten_overzicht_2025", 2025)
        for relative in (
            "_shared/knowledge/years/2025/annual/deductions.md",
            "nl-tax-annual-return/reference/annual-flow.md",
            "nl-tax-annual-return/templates/annual-return-pack.md",
        ):
            self.assert_text_contract(
                relative,
                required=("wheelchair: not deductible", "threshold: manual review"),
                forbidden=("wheelchairs and mobility aids are deductible",),
            )
```

- [ ] **Step 2: Add one test method for each audited claim**

Use explicit methods named:

```text
test_own_home_balance_excludes_tariefsaanpassing
test_hillen_uses_all_qualifying_costs
test_company_car_boundary_and_first_admission
test_stock_options_use_tradability_or_election
test_akw_is_not_taxable_box1_income
test_zw_wazo_arbeidskorting_is_conditional
test_iack_is_younger_than_12_on_january_1
test_elderly_single_credit_uses_aow_single_person_entitlement
test_upo_is_not_payment_or_withholding_evidence
test_periodic_gift_cap_and_transition
test_aov_is_not_an_ordinary_business_cost
test_prior_year_remainder_can_be_allocated_for_eligible_partners
test_no_universal_higher_earner_optimization
test_invitation_deadline_and_conditional_14_july
test_unsolicited_va_is_possible_not_automatic
test_complete_change_dataset_without_zero_default_claim
test_moving_abroad_routes_to_residency_review
test_annual_box3_explains_both_methods_and_records_actual_complete_or_deferred
```

Each method checks both the canonical note and every consumer listed in later tasks.

- [ ] **Step 3: Run RED**

```bash
python3 -m unittest discover \
  -s plugins/nl-tax-agent-skills/tests \
  -p 'test_tax_content_repairs.py'
```

Expected: multiple failures containing the currently incorrect claims.

### Task 2: Correct healthcare, gifts, AOV, benefits, credits, and Box 1 edge notes

**Files:**
- Modify: `plugins/nl-tax-agent-skills/skills/_shared/knowledge/years/2025/annual/deductions.md`
- Modify: `plugins/nl-tax-agent-skills/skills/_shared/knowledge/years/2025/annual/credits.md`
- Modify: `plugins/nl-tax-agent-skills/skills/_shared/knowledge/years/2025/annual/evidence-checklist.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-box1-home/reference/box1-2025.md`
- Modify: `plugins/nl-tax-agent-skills/skills/_shared/knowledge/years/2025/annual/box1-rates.md`
- Modify: `plugins/nl-tax-agent-skills/skills/_shared/knowledge/years/2025/entrepreneur/winst-en-kosten.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-annual-return/reference/annual-flow.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-annual-return/templates/annual-return-pack.md`

**Interfaces:**
- Consumes: registered Belastingdienst sources for 2025 deductions, credits, benefits, company cars, and equity compensation.
- Produces: one canonical factual statement per topic and matching workpack prompts/review boundaries.

- [ ] **Step 1: Correct healthcare and deduction rules minimally**

The notes and flow must say:

```markdown
- Wheelchairs, scooters, and home modifications are not deductible healthcare costs for 2025.
- Reimbursed costs, premiums, and the statutory excess are not included.
- The workpack inventories potentially qualifying evidence; threshold and multiplier calculations remain manual review until the complete reviewed table and inputs are present.
- Periodic gifts are capped at EUR 1.5 million, subject to the reviewed transition rule.
- Qualifying periodic AOV premiums belong to the private income-provision category, not ordinary business costs; ambiguous policy types remain manual review.
```

- [ ] **Step 2: Correct benefits and credit screens**

Use this decision shape:

```yaml
akw_child_benefit:
  taxable_box1_income: false
zw_wazo_arbeidskorting:
  outcome: "conditional_on_employment_relationship"
iack_child_test:
  reference_date: "2025-01-01"
  condition: "younger_than_12"
elderly_single_credit:
  condition: "entitled_to_aow_single_person_benefit"
upo:
  use: "accrual_or_projection_context_only"
```

Templates must request a payment-year pension statement for taxable pension/withholding amounts.

- [ ] **Step 3: Correct company-car and stock-option wording**

Use “500 private kilometres or fewer.” Do not show a company-car rate until first-admission/regime facts are confirmed. Describe tradability as the default stock-option tax point, with immediate-tradability/election cases requiring review.

- [ ] **Step 4: Run the focused policy suite**

Before running, resolve the annual Box 3 instruction conflict. Annual 2025
always explains the fictitious and actual-return methods and offers
actual-return evidence collection. When the taxpayer declines or lacks those
facts, record the actual-return subsection as deferred/manual review rather than
silently omitting it or claiming that both methods were completed.

```bash
python3 -m unittest discover \
  -s plugins/nl-tax-agent-skills/tests \
  -p 'test_tax_content_repairs.py'
```

Expected: Task 2 topics PASS; later own-home/partner/deadline topics remain RED.

### Task 3: Align own-home workflow output with corrected arithmetic

**Files:**
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-annual-return/reference/annual-flow.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-annual-return/reference/annual-output-contract.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-annual-return/templates/annual-return-pack.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-box1-home/reference/own-home-2025.md`
- Modify: `plugins/nl-tax-agent-skills/skills/_shared/knowledge/years/2025/annual/own-home.md`
- Modify: `plugins/nl-tax-agent-skills/skills/_shared/knowledge/own-home/eigenwoningforfait.md`
- Modify: `plugins/nl-tax-agent-skills/skills/_shared/knowledge/own-home/hypotheekrenteaftrek.md`
- Modify: `plugins/nl-tax-agent-skills/skills/_shared/knowledge/years/2026/provisional/own-home.md`

**Interfaces:**
- Consumes: optional helper fields `total_deductible_own_home_costs`, `box1_own_home_balance`, `hillen_deduction`, and separate `tariefsaanpassing` review adjustment.
- Produces: a workpack that never adds the rate adjustment into taxable Box 1 income.

- [ ] **Step 1: Add/adjust RED text assertions in `test_tax_content_repairs.py`**

Assert every consumer contains the equivalent of:

```text
box1_own_home_balance = eigenwoningforfait - total_deductible_own_home_costs - hillen_deduction
tariefsaanpassing = separate tax-benefit adjustment; never part of box1_own_home_balance
```

- [ ] **Step 2: Rewrite the own-home tables and formulas**

Itemize mortgage interest, qualifying financing costs, and periodic erfpacht/opstal/beklemming. Use their sum for Hillen. Keep the adjustment in a separate review table.

- [ ] **Step 3: Narrow multi-home behavior**

One ordinary main residence may receive a review estimate. Two homes, sale/purchase overlap, temporary double-home deductions, divorce use, and other complex cases collect facts and route to manual review.

- [ ] **Step 4: Run policy plus existing own-home tests**

```bash
python3 -m unittest discover -s plugins/nl-tax-agent-skills/tests -p 'test_tax_content_repairs.py'
python3 plugins/nl-tax-agent-skills/tests/test_box1_home.py
python3 plugins/nl-tax-agent-skills/tests/test_rate_parity.py
```

Expected: PASS.

### Task 4: Correct partner, deadline, EVA, change, and stopzetten behavior

**Files:**
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-partner-deductions/reference/deductions-2025.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-intake/reference/filing-paths.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-submit-companion/reference/annual-submit-steps.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-submit-companion/SKILL.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-submit-companion/reference/provisional-submit-steps.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-provisional-assessment/SKILL.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-provisional-assessment/reference/provisional-flow.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-provisional-assessment/reference/provisional-output-contract.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-provisional-assessment/reference/delta-rules.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-provisional-assessment/reference/stopzetten-guidance.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-provisional-assessment/templates/provisional-pack.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-provisional-assessment/templates/delta-summary.md`
- Modify: `plugins/nl-tax-agent-skills/skills/_shared/knowledge/years/2026/provisional/change-flow.md`
- Modify: `plugins/nl-tax-agent-skills/skills/_shared/knowledge/years/2026/provisional/refund-payment-timing.md`
- Modify: `plugins/nl-tax-agent-skills/skills/_shared/knowledge/years/2026/provisional/review-flow.md`
- Modify: `plugins/nl-tax-agent-skills/skills/_shared/knowledge/years/2026/provisional/vva-eva-baseline-delta.md`

**Interfaces:**
- Consumes: invitation status/date, current VA existence/type, complete current estimates, and residency facts.
- Produces: qualified deadline/change guidance without universal zero-default, automatic-EVA, migration-stop, or higher-earner claims.

- [ ] **Step 1: Change partner allocation guidance**

Eligible whole-year partners may allocate the prior-year personal-deduction remainder. Present traceable scenarios and require taxpayer review; remove every universal higher-earner recommendation.

- [ ] **Step 2: Make deadline routing explicit**

```text
if invitation letter exists -> use its deadline
else if taxpayer discovers tax is due -> apply reviewed voluntary-filing guardrail, including conditional 14 July wording
else -> do not invent a filing deadline
```

- [ ] **Step 3: Remove the zero-default claim repository-wide**

Replace it with: “Prepare and verify the complete dataset; the change form requires all applicable categories, not only the changed item.”

- [ ] **Step 4: Correct EVA and migration wording**

A later unsolicited VA may be issued from earlier data; it is not guaranteed. Moving abroad routes to the unsupported residency/migration path rather than categorical stopzetten guidance.

- [ ] **Step 5: Run RED/GREEN proof**

```bash
python3 -m unittest discover -s plugins/nl-tax-agent-skills/tests -p 'test_tax_content_repairs.py'
rg -n -i 'omitted data defaults to zero|automatically produces the next|allocate.*higher earner' \
  plugins/nl-tax-agent-skills/skills
```

Expected: tests PASS; `rg` returns no prohibited current claim.

### Task 5: Repair session state and one-writer ownership

**Files:**
- Modify: `plugins/nl-tax-agent-skills/tests/test_intake_contracts.py`
- Modify: `plugins/nl-tax-agent-skills/tests/test_policy_and_field_maps.py`
- Modify: `plugins/nl-tax-agent-skills/skills/_shared/templates/session-progress.yaml`
- Modify: `plugins/nl-tax-agent-skills/skills/_shared/knowledge/methods/interactive-elicitation.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-annual-return/SKILL.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-provisional-assessment/SKILL.md`
- Modify: all five helper `SKILL.md` files.
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-field-mapper/SKILL.md`

**Interfaces:**
- Consumes: profile, session state, helper-returned facts/questions, and workpack.
- Produces: schema 1.4 with `annual_2025.winst` and `provisional_2026.winst_forecast`; one canonical writer per final artifact.

- [ ] **Step 1: Add failing session schema tests**

```python
def test_session_tracks_annual_and_provisional_winst(self):
    state = load_yaml("skills/_shared/templates/session-progress.yaml")
    self.assertEqual(state["session_progress_version"], "1.4")
    self.assertIn("winst", state["sections"]["annual_2025"]["subsections"])
    self.assertIn("winst_forecast", state["sections"]["provisional_2026"]["subsections"])

def test_unfinished_winst_blocks_annual_review_readiness(self):
    state = completed_annual_state()
    state["sections"]["annual_2025"]["subsections"]["winst"]["status"] = "in_progress"
    self.assertEqual(readiness(state), "draft")
```

- [ ] **Step 2: Add failing ownership tests**

Assert the annual/provisional skills own workpack/session artifacts but do not claim to write field maps; `nl-tax-field-mapper` alone claims both canonical map paths; helpers claim no final persisted artifact.

- [ ] **Step 3: Run RED**

```bash
python3 plugins/nl-tax-agent-skills/tests/test_intake_contracts.py
python3 plugins/nl-tax-agent-skills/tests/test_policy_and_field_maps.py
```

- [ ] **Step 4: Implement schema 1.4 and legacy resume migration**

No-business cases mark winst/winst_forecast not applicable using the existing terminal status convention. Existing shared helper notes remain readable only for resume compatibility; new helper results are persisted by the owning workflow.

- [ ] **Step 5: Make the field mapper the sole map writer**

Annual/provisional orchestration invokes the mapper after workpack confirmation.
Replace every local-looking mapper path with the exact sibling paths
`nl-tax-field-mapper/templates/field-map-template.yaml`,
`nl-tax-field-mapper/reference/mapping-principles.md`,
`nl-tax-field-mapper/reference/annual-field-map.md`,
`nl-tax-field-mapper/reference/provisional-field-map.md`, and
`nl-tax-field-mapper/scripts/validate_field_map.py`.

- [ ] **Step 6: Re-run focused tests**

Expected: PASS.

### Task 6: Narrow annual entrepreneur support and add the provisional forecast

**Files:**
- Modify: `plugins/nl-tax-agent-skills/tests/test_entrepreneur_unlock.py`
- Modify: `plugins/nl-tax-agent-skills/tests/test_policy_and_field_maps.py`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-winst/SKILL.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-winst/reference/winst-2025.md`
- Create: `plugins/nl-tax-agent-skills/skills/nl-tax-winst/reference/winst-2026-provisional.md`
- Modify: annual skill, flow, output contract, and template.
- Modify: provisional skill, flow, output contract, and template.
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-intake/reference/unsupported-cases.md`
- Modify: `plugins/nl-tax-agent-skills/skills/_shared/supported-workflows.yaml`
- Modify: annual/provisional field-map references.
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-field-mapper/scripts/validate_field_map.py`

**Interfaces:**
- Consumes: finalized P&L/balance evidence for annual preparation or a sourced expected-profit forecast for provisional.
- Produces: annual preparation/manual-review business section and provisional `onderneming.geschatte_winst`; never a generic-other-income substitution.

- [ ] **Step 1: Rewrite entrepreneur tests to RED against the current overclaim**

Required assertions:

```python
self.assertIn("profit-and-loss", annual_contract.lower())
self.assertIn("balance", annual_contract.lower())
self.assertIn("preparation-only", annual_contract.lower())
self.assertNotIn("calculate final taxable business profit", annual_contract.lower())
self.assertIn("`onderneming.geschatte_winst`", provisional_reference)
self.assertNotIn("`box1.geschat_overig_inkomen`", provisional_business_section)
```

The validator must accept only the provisional expected-profit business field while continuing to reject annual entrepreneur deductions in a provisional map.

- [ ] **Step 2: Run RED**

```bash
python3 plugins/nl-tax-agent-skills/tests/test_entrepreneur_unlock.py
python3 plugins/nl-tax-agent-skills/tests/test_policy_and_field_maps.py
```

- [ ] **Step 3: Rewrite the winst helper as a fact/question contract**

Annual: organize official P&L and balance categories, hours, investments, and deduction evidence; never determine final taxable profit or claim a complete business return. Complex forms/events remain terminal review.

Provisional: collect a user-reviewed expected-profit forecast for `Winst uit onderneming`; do not calculate business accounts, annual deductions, Zvw, cessation profit, or final tax.

- [ ] **Step 4: Change field-map readiness**

Annual entrepreneur maps remain `draft` with a business-section blocker until a complete reviewed zakelijke schema exists. Provisional maps may include `onderneming.geschatte_winst` with provenance and manual review.

- [ ] **Step 5: Re-run entrepreneur and field-map tests**

Expected: PASS.

### Task 7: Add non-security behavioral fixtures and offline cases

**Files:**
- Modify: `plugins/nl-tax-agent-skills/skills/_shared/eval-fixtures/annual/entrepreneur-zzp.yaml`
- Create: `plugins/nl-tax-agent-skills/skills/_shared/eval-fixtures/provisional/entrepreneur-profit.yaml`
- Create: `plugins/nl-tax-agent-skills/skills/_shared/eval-fixtures/annual/evidence-status.yaml`
- Modify: `plugins/nl-tax-agent-skills/skills/_shared/eval-fixtures/annual/simple-resident.yaml`
- Modify: `evals/nl-tax-agent-skills/offline-dataset.yaml`
- Modify: `plugins/nl-tax-agent-skills/tests/test_fixture_schema.py`
- Modify: `plugins/nl-tax-agent-skills/tests/test_eval_verifier.py`

**Interfaces:**
- Consumes: final schema 1.4 and workflow/output contracts.
- Produces: fixture-backed cases for annual entrepreneur preparation-only, provisional expected profit, and evidence completeness.

- [ ] **Step 1: Add failing fixture expectations**

Annual entrepreneur expected state includes `field_map_readiness: draft` and a business manual-review blocker. Provisional expected state includes `onderneming.geschatte_winst` and forbids annual deductions/Zvw/final tax. Evidence-status expected state counts only the reviewed/current-year item.

- [ ] **Step 2: Add every fixture to the offline dataset in the same patch**

Use case IDs:

```text
annual_entrepreneur_zzp
provisional_entrepreneur_profit
annual_evidence_status
```

- [ ] **Step 3: Run fixture and dataset RED/GREEN**

```bash
python3 plugins/nl-tax-agent-skills/tests/test_fixture_schema.py
python3 plugins/nl-tax-agent-skills/tests/test_eval_verifier.py
python3 evals/nl-tax-agent-skills/verify_offline_workspace.py --check-dataset
```

Expected: PASS.

### Task 8: Run the complete tax/workflow gate

**Files:**
- Verify: all files changed by Tasks 1–7.
- Verify unchanged: `PRIVACY.md`, `SECURITY.md`.

**Interfaces:**
- Consumes: corrected tax/workflow tree.
- Produces: green test evidence before packaging/provenance hashes are finalized.

- [ ] **Step 1: Run focused suites**

```bash
python3 -m unittest discover -s plugins/nl-tax-agent-skills/tests -p 'test_tax_content_repairs.py'
python3 plugins/nl-tax-agent-skills/tests/test_box1_home.py
python3 plugins/nl-tax-agent-skills/tests/test_box2_helpers.py
python3 plugins/nl-tax-agent-skills/tests/test_entrepreneur_unlock.py
python3 plugins/nl-tax-agent-skills/tests/test_intake_contracts.py
python3 plugins/nl-tax-agent-skills/tests/test_policy_and_field_maps.py
python3 plugins/nl-tax-agent-skills/tests/test_validators.py
```

- [ ] **Step 2: Run full root/plugin suites and validators**

```bash
python3 -m unittest discover -s plugins/nl-tax-agent-skills/tests -p 'test_*.py'
(
  cd plugins/nl-tax-agent-skills
  python3 -m unittest discover -s tests -p 'test_*.py'
)
python3 evals/nl-tax-agent-skills/verify_offline_workspace.py --check-dataset
```

- [ ] **Step 3: Prove excluded files remain untouched**

```bash
git diff --exit-code $(git merge-base main HEAD) HEAD -- PRIVACY.md SECURITY.md
```

Expected: all commands PASS with no privacy/security diff.
