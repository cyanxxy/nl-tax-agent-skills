# NL Tax Agent Skills Non-Security Audit Repair Program

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver release 0.1.7 with every confirmed non-security audit issue fixed, an LLM-led Cowork workflow, and optional minimal Python checks.

**Architecture:** Execute three independently reviewable plans in order. The first corrects tax content and workflow contracts, the second reduces Python to four optional mechanical components, and the third finishes Claude/Cowork packaging, provenance, evals, documentation, and release verification.

**Tech Stack:** Claude Agent Skills Markdown/YAML, Python 3.10+ optional helpers, `unittest`, offline YAML eval fixtures, Claude plugin manifests and CLI validation.

## Global Constraints

- The LLM drives intake, interpretation, questions, tax reasoning, workpack assembly, and field-map preparation.
- Python is optional at runtime and never blocks a Cowork taxpayer workflow.
- Retained Python performs only inventory/hash, validation/rendering, source-pinned arithmetic, or developer consistency checks.
- The taxpayer alone opens, enters data in, reviews, signs, and submits through Mijn Belastingdienst.
- Preserve the public skill names and canonical workspace output paths.
- Do not edit `PRIVACY.md` or `SECURITY.md`.
- Do not fix or change any security/privacy finding enumerated in the approved design specification.
- Do not add unsupported formulas; unresolved official coverage becomes a visible manual-review boundary.
- Use failing tests or behavioral cases before every skill, data, script, or workflow behavior change.
- Target release version is exactly `0.1.7`.

---

### Task 1: Tax content and workflow contracts

**Plan:** `docs/superpowers/plans/2026-07-10-tax-workflow-corrections-plan.md`

**Produces:** Corrected official-source notes, annual/provisional workflows, entrepreneur boundaries, session state, field-map ownership, and tax behavioral cases.

- [ ] Execute every task in the tax/workflow plan.
- [ ] Confirm its focused and full tests pass before starting Task 2.

### Task 2: Optional Python tooling

**Plan:** `docs/superpowers/plans/2026-07-10-optional-python-tooling-plan.md`

**Consumes:** Tax formulas, accepted-row contracts, and workflow/manual-check contracts finalized by Task 1.

**Produces:** Four optional Python component groups, 14 retained scripts, removed heuristic roles, integrated Box 2 validation, and script/manual-check parity.

- [ ] Execute every task in the optional-Python plan.
- [ ] Confirm its focused and full tests pass before starting Task 3.

### Task 3: Cowork packaging, provenance, evals, and release

**Plan:** `docs/superpowers/plans/2026-07-10-cowork-release-consistency-plan.md`

**Consumes:** Final tax notes, workflows, Python inventory, fixtures, and output contracts.

**Produces:** Twelve unique Claude skills, current manifests/docs, reviewed-note provenance, complete eval coverage, release 0.1.7, and final independent review evidence.

- [ ] Execute every task in the Cowork/release plan.
- [ ] Run the complete acceptance gate and requirement-to-evidence audit.

### Task 4: Final scope guard

**Files:**
- Verify unchanged: `PRIVACY.md`
- Verify unchanged: `SECURITY.md`
- Verify: `docs/superpowers/specs/2026-07-10-non-security-audit-repair-design.md`

**Interfaces:**
- Consumes: all three reviewed plan results.
- Produces: proof that the implementation did not cross into the excluded security/privacy scope.

- [ ] **Step 1: Compare protected files with the program base**

Run:

```bash
PROGRAM_BASE=c912bb5
git diff --exit-code "$PROGRAM_BASE" -- PRIVACY.md SECURITY.md
```

Expected: exit 0 and no output.

- [ ] **Step 2: Verify every changed file maps to the approved non-security spec**

Run:

```bash
git diff --name-only c912bb5...HEAD
```

Expected: every path is covered by one of the three component plans or the spec/plan documents.

- [ ] **Step 3: Record completion evidence**

Append the exact test commands, exit codes, Claude inventory count, Plugin Eval result, independent-review verdicts, and remaining manual Cowork smoke item to the final task report. Do not mark the program complete from test counts alone.
