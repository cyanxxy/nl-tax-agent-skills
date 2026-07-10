# Optional Python Tooling Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reduce Python from 18 mixed-purpose scripts to 14 optional mechanical helpers grouped into four components, with the LLM owning all interpretation and workflow decisions.

**Architecture:** Delete heuristic summarizers/classifier and fold Box 2 validation into its calculator. Retained scripts consume explicit, already-classified inputs and mirror concise manual checks so Cowork works identically without Python.

**Tech Stack:** Python 3.10+, PyYAML as an optional/maintainer dependency, `unittest`, Markdown/YAML Agent Skills.

## Global Constraints

- Runtime Python is optional; no taxpayer is asked to install it.
- Retained scripts do not classify evidence, infer tax treatment, decide eligibility, generate workpacks, or optimize allocations.
- Preserve security/privacy behavior exactly, including broad Bash policy, YAML loader behavior, PII behavior, Markdown rendering behavior, path/symlink handling, and resource limits.
- Delete exactly four scripts: `summarize_box1_inputs.py`, `summarize_box2_inputs.py`, `validate_box2_inputs.py`, and `classify_box3_assets.py`.
- Retain 14 scripts grouped as inventory/hash, field-map checks, source-pinned arithmetic, and developer consistency.
- Each output records `checked_by_script` or `checked_by_agent` where a manual/script parity check is relevant.

---

### Task 1: Pin the 14-script and optional-runtime contract

**Files:**
- Create: `plugins/nl-tax-agent-skills/tests/test_optional_python_contracts.py`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-evidence-indexer/templates/evidence-index.yaml`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-field-mapper/templates/field-map-template.yaml`

**Interfaces:**
- Consumes: filesystem inventory under `skills/*/scripts/`.
- Produces: `EXPECTED_SCRIPT_GROUPS`, allowed check-trail values, and a regression test that Python remains optional.

- [ ] **Step 1: Write the failing inventory test**

```python
EXPECTED_SCRIPT_GROUPS = {
    "inventory_hash": {
        "nl-tax-evidence-indexer/scripts/index_evidence.py",
    },
    "field_map": {
        "nl-tax-field-mapper/scripts/validate_field_map.py",
        "nl-tax-field-mapper/scripts/render_field_map.py",
    },
    "arithmetic": {
        "nl-tax-box1-home/scripts/validate_own_home_inputs.py",
        "nl-tax-box2/scripts/calculate_box2_tax.py",
        "nl-tax-box3/scripts/compare_box3_annual_2025.py",
        "nl-tax-box3/scripts/summarize_box3_provisional_2026.py",
        "nl-tax-partner-deductions/scripts/validate_allocation.py",
    },
    "developer_consistency": {
        "nl-tax-source-refresh/scripts/build_snapshots.py",
        "nl-tax-source-refresh/scripts/plan_source_refresh.py",
        "nl-tax-source-refresh/scripts/validate_invocation_policy.py",
        "nl-tax-source-refresh/scripts/validate_knowledge_pack.py",
        "nl-tax-source-refresh/scripts/validate_source_register.py",
        "nl-tax-source-refresh/scripts/validate_supported_workflows.py",
    },
}

def test_exact_optional_python_inventory(self):
    actual = {
        str(path.relative_to(SKILLS_ROOT))
        for path in SKILLS_ROOT.glob("*/scripts/*.py")
    }
    expected = set().union(*EXPECTED_SCRIPT_GROUPS.values())
    self.assertEqual(actual, expected)
    self.assertEqual(len(actual), 14)
```

- [ ] **Step 2: Add failing absence and runtime-copy assertions**

```python
def test_retired_heuristics_have_no_runtime_references(self):
    retired = {
        "summarize_box1_inputs.py",
        "summarize_box2_inputs.py",
        "validate_box2_inputs.py",
        "classify_box3_assets.py",
        "fetch_sources.py",
    }
    shipped = "\n".join(
        path.read_text(encoding="utf-8")
        for path in SKILLS_ROOT.rglob("*")
        if path.is_file() and path.suffix in {".md", ".yaml", ".yml", ".py"}
    )
    for name in retired:
        self.assertNotIn(name, shipped)

def test_runtime_docs_make_python_optional(self):
    for relative in ("README.md", "skills/nl-tax-intake/SKILL.md"):
        text = (PLUGIN_ROOT / relative).read_text(encoding="utf-8").lower()
        self.assertIn("python is optional", text)
        self.assertIn("do not ask", text)
        self.assertIn("install python", text)
```

- [ ] **Step 3: Run RED and confirm the expected 18-versus-14 failure**

Run:

```bash
python3 -m unittest discover \
  -s plugins/nl-tax-agent-skills/tests \
  -p 'test_optional_python_contracts.py'
```

Expected: FAIL because four retired scripts and their references still exist.

- [ ] **Step 4: Add `check_performed_by` to the two shared output templates**

Use exactly:

```yaml
check_performed_by: "checked_by_agent"  # checked_by_agent | checked_by_script
```

Do not change any PII, path, YAML-loading, or rendering behavior.

- [ ] **Step 5: Re-run the focused test and retain the inventory failure for later tasks**

Expected: check-trail assertions pass; inventory/absence assertions remain RED.

### Task 2: Fold Box 2 validation into one optional calculator

**Files:**
- Modify: `plugins/nl-tax-agent-skills/tests/test_box2_helpers.py`
- Modify: `plugins/nl-tax-agent-skills/tests/test_review_fixes.py`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-box2/scripts/calculate_box2_tax.py`
- Delete: `plugins/nl-tax-agent-skills/skills/nl-tax-box2/scripts/validate_box2_inputs.py`
- Delete: `plugins/nl-tax-agent-skills/skills/nl-tax-box2/scripts/summarize_box2_inputs.py`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-box2/SKILL.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-box2/reference/box2-annual-2025.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-box2/reference/box2-provisional-2026.md`

**Interfaces:**
- Consumes: JSON mapping with explicit workflow, tax year, substantial-interest percentage, residency/standard-case booleans, and source-backed amounts.
- Produces: `calculate_from_payload(payload) -> {errors, warnings, normalized, result, check_performed_by}`; `result` is null whenever validation or a manual-review boundary blocks calculation.

- [ ] **Step 1: Replace separate-validator tests with failing integrated-entrypoint tests**

```python
def valid_annual_payload(**overrides):
    payload = {
        "workflow": "annual_2025",
        "tax_year": 2025,
        "substantial_interest_pct": "10",
        "resident_full_year": True,
        "standard_ab_case": True,
        "regular_benefits": "10000",
        "disposal_benefits": "0",
        "loss_setoff": "0",
    }
    payload.update(overrides)
    return payload

def test_payload_validation_cannot_be_bypassed(self):
    for patch in (
        {"substantial_interest_pct": ""},
        {"resident_full_year": "true"},
        {"standard_ab_case": False},
        {"workflow": "provisional_2026", "tax_year": 2025},
    ):
        output = self.mod.calculate_from_payload(valid_annual_payload(**patch))
        self.assertTrue(output["errors"])
        self.assertIsNone(output["result"])
```

- [ ] **Step 2: Add failing loss-setoff and unknown-key tests**

```python
def test_loss_setoff_blocks_until_reviewed(self):
    blocked = self.mod.calculate_from_payload(
        valid_annual_payload(loss_setoff="500")
    )
    self.assertIsNone(blocked["result"])
    reviewed = self.mod.calculate_from_payload(
        valid_annual_payload(
            loss_setoff="500",
            loss_setoff_reviewed=True,
            loss_setoff_source="2025 assessment loss statement",
        )
    )
    self.assertFalse(reviewed["errors"])
    self.assertIsNotNone(reviewed["result"])

def test_unknown_amount_key_is_rejected(self):
    output = self.mod.calculate_from_payload(
        valid_annual_payload(regluar_benefits="10000")
    )
    self.assertTrue(any("unknown" in item.lower() for item in output["errors"]))
```

- [ ] **Step 3: Run the Box 2 tests and verify RED**

```bash
python3 plugins/nl-tax-agent-skills/tests/test_box2_helpers.py
python3 plugins/nl-tax-agent-skills/tests/test_review_fixes.py
```

Expected: FAIL because the calculator bypasses the separate validator.

- [ ] **Step 4: Implement `validate_and_normalize_payload` inside the calculator**

The public flow is:

```python
def calculate_from_payload(payload):
    errors, warnings, normalized = validate_and_normalize_payload(payload)
    if errors or normalized.get("manual_review_required"):
        return {
            "errors": errors,
            "warnings": warnings,
            "normalized": normalized,
            "result": None,
            "check_performed_by": "checked_by_script",
        }
    return {
        "errors": [],
        "warnings": warnings,
        "normalized": normalized,
        "result": _calculate_validated(normalized),
        "check_performed_by": "checked_by_script",
    }
```

Require actual booleans; never infer workflow/year; reject unknown keys. Keep existing official annual/provisional rate arithmetic private in `_calculate_validated`.

- [ ] **Step 5: Delete the separate validator and summarizer, then update skill/reference calls**

The no-Python checklist must mirror the same required keys, manual boundaries, and rate ordering. It records `checked_by_agent`.

- [ ] **Step 6: Run focused and full regression tests**

```bash
python3 plugins/nl-tax-agent-skills/tests/test_box2_helpers.py
python3 plugins/nl-tax-agent-skills/tests/test_review_fixes.py
python3 -m unittest discover -s plugins/nl-tax-agent-skills/tests -p 'test_*.py'
```

Expected: PASS.

### Task 3: Replace Box 3 keyword classification with trusted-row arithmetic

**Files:**
- Modify: `plugins/nl-tax-agent-skills/tests/test_validators.py`
- Modify: `plugins/nl-tax-agent-skills/tests/test_review_fixes.py`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-box3/scripts/compare_box3_annual_2025.py`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-box3/scripts/summarize_box3_provisional_2026.py`
- Delete: `plugins/nl-tax-agent-skills/skills/nl-tax-box3/scripts/classify_box3_assets.py`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-box3/SKILL.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-box3/reference/box3-annual-2025.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-box3/reference/box3-provisional-2026.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-annual-return/templates/annual-return-pack.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-provisional-assessment/templates/provisional-pack.md`

**Interfaces:**
- Consumes: already-classified rows with `category`, `status`, `value`, and provenance.
- Produces: trusted totals, rejected rows with reasons, and source-pinned annual/provisional arithmetic. It never infers category from names or keywords.

- [ ] **Step 1: Replace classifier tests with a failing row-contract test**

```python
def test_only_accepted_rows_enter_trusted_totals(self):
    rows = [
        {"id": "a", "category": "banktegoeden", "status": "accepted", "value": 1000},
        {"id": "b", "category": "banktegoeden", "status": "manual_review", "value": 9000},
        {"id": "c", "category": "unknown", "status": "accepted", "value": 5000},
        {"id": "d", "category": "banktegoeden", "status": "accepted", "value": -100},
    ]
    output = self.mod.normalize_classified_rows(rows)
    self.assertEqual(output["trusted_totals"]["banktegoeden"], 1000)
    self.assertEqual({row["id"] for row in output["rejected_rows"]}, {"b", "c", "d"})
```

- [ ] **Step 2: Add a failing generic-loan workflow assertion**

The skill/reference test must require this shape before arithmetic:

```yaml
- description: "Loan to friend"
  category: "unknown"
  status: "manual_review"
  value: 10000
```

No Python keyword may convert it to a debt.

- [ ] **Step 3: Run RED**

```bash
python3 plugins/nl-tax-agent-skills/tests/test_validators.py
python3 plugins/nl-tax-agent-skills/tests/test_review_fixes.py
```

Expected: FAIL because existing calculators accept aggregate totals and the classifier still exists.

- [ ] **Step 4: Implement identical row normalization in the two method-specific modules**

Factor a small local helper only if it improves auditability. Accepted categories are explicit per method/year; accepted rows require `status == "accepted"` and a finite non-negative numeric value. Return rejected rows before calling the existing private formulas.

- [ ] **Step 5: Delete the classifier and rewrite skill/template contracts**

Templates contain separate accepted and rejected/manual-review tables. LLM instructions classify first; scripts only total accepted rows. Remove all runtime references to the deleted classifier.

- [ ] **Step 6: Verify annual/provisional method separation remains green**

```bash
python3 plugins/nl-tax-agent-skills/tests/test_validators.py
python3 plugins/nl-tax-agent-skills/tests/test_rate_parity.py
```

Expected: PASS with existing official golden arithmetic preserved.

### Task 4: Correct own-home arithmetic and retire the Box 1 summarizer

**Files:**
- Modify: `plugins/nl-tax-agent-skills/tests/test_box1_home.py`
- Modify: `plugins/nl-tax-agent-skills/tests/test_rate_parity.py`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-box1-home/scripts/validate_own_home_inputs.py`
- Delete: `plugins/nl-tax-agent-skills/skills/nl-tax-box1-home/scripts/summarize_box1_inputs.py`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-box1-home/SKILL.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-box1-home/reference/own-home-2025.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-box1-home/reference/box1-2025.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-box1-home/reference/box1-2026-provisional.md`

**Interfaces:**
- Consumes: explicit ordinary-home amounts already accepted by the LLM.
- Produces: total deductible own-home costs, `box1_balance_components`, own-home balance, Hillen result, and a separate rate-adjustment review value.

- [ ] **Step 1: Add the failing full-cost Hillen case**

```python
def test_hillen_uses_all_qualifying_costs(self):
    payload = self.valid_payload(
        eigenwoningforfait="4000",
        mortgage_interest="3500",
        qualifying_financing_costs="300",
        periodic_erfpacht_opstal_beklemming="300",
    )
    result = self.mod.validate(payload)
    self.assertEqual(result["total_deductible_own_home_costs"], "4100.00")
    self.assertEqual(result["hillen_deduction"], "0.00")
    self.assertEqual(result["box1_own_home_balance"], "-100.00")
```

- [ ] **Step 2: Add a failing separation assertion**

```python
self.assertEqual(result["box1_own_home_balance"], "-100.00")
self.assertNotIn("tariefsaanpassing", result["box1_balance_components"])
self.assertIn("tariefsaanpassing", result["review_adjustments"])
```

- [ ] **Step 3: Run RED, implement the four explicit derived values, and keep complex eligibility outside Python**

```bash
python3 plugins/nl-tax-agent-skills/tests/test_box1_home.py
```

Expected initially: FAIL because Hillen currently compares only mortgage interest.

- [ ] **Step 4: Delete the summarizer and make evidence completeness LLM-owned**

The Box 1 skill reads the evidence index directly. Only reviewed, successful, correct-year evidence closes a gap; Python is not used for this decision.

- [ ] **Step 5: Verify focused and parity tests**

```bash
python3 plugins/nl-tax-agent-skills/tests/test_box1_home.py
python3 plugins/nl-tax-agent-skills/tests/test_rate_parity.py
```

Expected: PASS.

### Task 5: Make partner allocation an explicit arithmetic check

**Files:**
- Modify: `plugins/nl-tax-agent-skills/tests/test_validators.py`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-partner-deductions/scripts/validate_allocation.py`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-partner-deductions/SKILL.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-partner-deductions/reference/fiscal-partner.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-partner-deductions/reference/deductions-2025.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-partner-deductions/reference/provisional-deductions-2026.md`

**Interfaces:**
- Consumes: wrapped payload with explicit real boolean partner status and explicit real boolean `allocatable` per row.
- Produces: arithmetic range/sum violations only; no keyword-based tax classification.

- [ ] **Step 1: Write failing boolean and no-inference tests**

```python
def test_partner_and_allocatable_require_real_booleans(self):
    for bad in ("false", "true", 0, 1, None):
        payload = {"has_fiscal_partner": bad, "items": []}
        errors = self.mod.validate(payload)
        self.assertTrue(errors)

def test_item_name_does_not_decide_allocatability(self):
    payload = {
        "has_fiscal_partner": True,
        "items": [{"name": "employment income", "allocatable": True,
                   "taxpayer_pct": 50, "partner_pct": 50}],
    }
    self.assertFalse(self.mod.validate(payload))
```

- [ ] **Step 2: Run RED**

```bash
python3 plugins/nl-tax-agent-skills/tests/test_validators.py
```

Expected: FAIL because string booleans/default partner and keyword inference are accepted.

- [ ] **Step 3: Remove `NON_ALLOCATABLE_KEYWORDS`, bare-list partner defaults, and truthiness casts**

Validate explicit types, then perform only percentage/range checks. Manual reference checks use the same invariants and record `checked_by_agent`.

- [ ] **Step 4: Re-run validators**

Expected: PASS.

### Task 6: Align evidence and field-map manual/script checks

**Files:**
- Modify: `plugins/nl-tax-agent-skills/tests/test_audit_followups.py`
- Modify: `plugins/nl-tax-agent-skills/tests/test_policy_and_field_maps.py`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-evidence-indexer/scripts/index_evidence.py`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-evidence-indexer/SKILL.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-evidence-indexer/reference/extraction-boundaries.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-evidence-indexer/templates/evidence-index.yaml`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-field-mapper/scripts/validate_field_map.py`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-field-mapper/scripts/render_field_map.py`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-field-mapper/SKILL.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-field-mapper/reference/mapping-principles.md`
- Modify: `plugins/nl-tax-agent-skills/skills/nl-tax-field-mapper/templates/field-map-template.yaml`

**Interfaces:**
- Consumes: user-selected evidence folder and completed field-map artifact.
- Produces: inventory/hash only for evidence; stable check IDs and check trail for field maps.

- [ ] **Step 1: Add failing evidence non-classification assertions**

```python
entry = self.mod.index_directory(str(folder))[0]
self.assertEqual(entry["evidence_type"], "")
self.assertIsNone(entry["tax_year"])
self.assertIsNone(entry["confidence"])
self.assertEqual(entry["extraction_status"], "indexed_only")
```

- [ ] **Step 2: Add failing field-map check-ID parity assertions**

Expose `CHECK_IDS` from the validator and list the same IDs in the manual checklist. Compare exact sets in the test. Include current metadata, workflow/year, structure, source, confidence/finite, reference coverage, missing/readiness, and provisional-method checks. Do not alter excluded PII/YAML/Markdown behavior.

- [ ] **Step 3: Run RED**

```bash
python3 plugins/nl-tax-agent-skills/tests/test_audit_followups.py
python3 plugins/nl-tax-agent-skills/tests/test_policy_and_field_maps.py
```

- [ ] **Step 4: Implement check trails and concise no-Python checklists**

Use only `checked_by_script` and `checked_by_agent`. Python absence permits a null hash and never blocks classification/workpack work by the LLM.

- [ ] **Step 5: Run focused tests**

Expected: PASS.

### Task 7: Finish inventory, documentation, and full regression verification

**Files:**
- Rename: `plugins/nl-tax-agent-skills/skills/nl-tax-source-refresh/scripts/fetch_sources.py` to `plugins/nl-tax-agent-skills/skills/nl-tax-source-refresh/scripts/plan_source_refresh.py`
- Modify: `plugins/nl-tax-agent-skills/README.md`
- Modify: `README.md`
- Modify: `CONTRIBUTING.md`
- Modify: `llm-agent-skill-plan.md`
- Modify: `evals/nl-tax-agent-skills/README.md`
- Modify: `.github/workflows/ci.yml`
- Verify unchanged: `PRIVACY.md`, `SECURITY.md`

**Interfaces:**
- Consumes: final 14-script tree and manual/script contracts.
- Produces: accurate optional-runtime documentation and Python 3.10/3.12 CI coverage.

- [ ] **Step 1: Rename the plan-only source reporter**

Rename `fetch_sources.py` to `plan_source_refresh.py` and update every current
skill, test, and documentation reference. Preserve its existing plan-only
behavior in this task; the Cowork/release plan later changes its provenance
vocabulary after final tax-note edits.

- [ ] **Step 2: Update documentation to name four conceptual components and Python 3.10+ as optional**

Historical changelog entries may retain retired script names as history. Current docs and skill/runtime references may not.

- [ ] **Step 3: Add a Python matrix to CI**

```yaml
strategy:
  matrix:
    python-version: ["3.10", "3.12"]
```

Use `${{ matrix.python-version }}` in `actions/setup-python` and run compilation plus both root/plugin test suites for each version.

- [ ] **Step 4: Run the inventory and absence checks**

```bash
python3 -m unittest discover \
  -s plugins/nl-tax-agent-skills/tests \
  -p 'test_optional_python_contracts.py'

rg -n 'summarize_box1_inputs|summarize_box2_inputs|classify_box3_assets|validate_box2_inputs|fetch_sources\.py' \
  plugins/nl-tax-agent-skills README.md CONTRIBUTING.md llm-agent-skill-plan.md \
  --glob '!CHANGELOG.md'
```

Expected: tests PASS; `rg` returns no current-runtime references.

- [ ] **Step 5: Run full regression and offline-eval checks**

```bash
python3 -m py_compile $(find plugins/nl-tax-agent-skills/skills plugins/nl-tax-agent-skills/tests -name '*.py' -print)
python3 -m unittest discover -s plugins/nl-tax-agent-skills/tests -p 'test_*.py'
(
  cd plugins/nl-tax-agent-skills
  python3 -m unittest discover -s tests -p 'test_*.py'
)
python3 evals/nl-tax-agent-skills/verify_offline_workspace.py --check-dataset
git diff --exit-code $(git merge-base main HEAD) HEAD -- PRIVACY.md SECURITY.md
```

Expected: all commands PASS with no privacy/security diff.
