# Cowork Packaging and Release Consistency Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Package the corrected plugin as a truthful Cowork-first 0.1.7 release with 12 unique skills, progressive disclosure, reviewed-note provenance, complete behavioral-eval parity, consistent documentation, and strict Claude validation.

**Architecture:** Remove legacy command collisions while preserving public skill names. Finalize all tax notes before rebuilding local-note hashes once; then update evals, docs, assets, manifests, CI, and release evidence as one consistency pass.

**Tech Stack:** Claude/Codex JSON manifests, Agent Skills Markdown/YAML, Python `unittest`, GitHub Actions, Claude CLI, Plugin Eval.

## Global Constraints

- Execute after the optional-Python and tax/workflow plans are green.
- Leave `PRIVACY.md`, `SECURITY.md`, security code behavior, and security fixture content unchanged.
- Preserve all 12 public skill names and canonical output paths.
- Python is optional in Cowork; optional helpers require Python 3.10+.
- `last_checked` means human review of an official source; local hashes cover synthesized rule notes, not remote page bodies.
- Marketplaces remain unversioned; nested Claude/Codex manifests finish at `0.1.7`.
- Do not create retroactive Git tags.
- Rebuild reviewed-note hashes exactly once after every knowledge-note edit is final.

---

### Task 1: Add release, discovery, and provenance RED tests

**Files:**
- Create: `plugins/nl-tax-agent-skills/tests/test_release_017_packaging.py`
- Create: `plugins/nl-tax-agent-skills/tests/test_skill_discovery_and_loading.py`
- Create: `plugins/nl-tax-agent-skills/tests/test_source_provenance.py`
- Modify: `plugins/nl-tax-agent-skills/tests/test_fixture_schema.py`
- Modify: `plugins/nl-tax-agent-skills/tests/test_eval_verifier.py`

**Interfaces:**
- Consumes: repository/plugin manifests, skill frontmatter/bodies, source metadata, docs/assets, fixture/dataset/benchmark files.
- Produces: release invariants that remain RED until later tasks complete.

- [ ] **Step 1: Write the failing packaging test**

```python
class Release017PackagingTests(unittest.TestCase):
    def test_no_legacy_commands(self):
        self.assertFalse((PLUGIN / "commands").exists())

    def test_exactly_12_unique_skills(self):
        names = [frontmatter(path)["name"] for path in SKILLS.glob("*/SKILL.md")]
        self.assertEqual(len(names), 12)
        self.assertEqual(len(set(names)), 12)

    def test_manifest_versions_and_metadata(self):
        claude = load_json(PLUGIN / ".claude-plugin/plugin.json")
        codex = load_json(PLUGIN / ".codex-plugin/plugin.json")
        self.assertEqual(claude["version"], "0.1.7")
        self.assertEqual(codex["version"], "0.1.7")
        self.assertEqual(claude["displayName"], "NL Tax Agent Skills")
        self.assertEqual(claude["homepage"], REPOSITORY_URL)
        self.assertEqual(claude["repository"], REPOSITORY_URL)
```

Also assert seven exact `argument-hint` values, one retained icon, no `logo.png` or Cowork screenshot, Python 3.10 wording, no current 0.1.2 example, and future tag-check instructions.

- [ ] **Step 2: Write the failing discovery/progressive-loading test**

```python
def test_public_triggers_require_preparation_intent(self):
    intake = frontmatter(SKILLS / "nl-tax-intake/SKILL.md")["description"].lower()
    evidence = frontmatter(SKILLS / "nl-tax-evidence-indexer/SKILL.md")["description"].lower()
    self.assertIn("explicitly wants", intake)
    self.assertIn("informational", intake)
    self.assertIn("explicitly wants", evidence)
    self.assertNotIn("mentions belastingaangifte", intake)

def test_large_output_files_load_only_at_generation(self):
    for skill_name, template in (
        ("nl-tax-annual-return", "annual-return-pack.md"),
        ("nl-tax-provisional-assessment", "provisional-pack.md"),
    ):
        text = read_skill(skill_name)
        self.assertIn(f"load `{template}` only after", text.lower())
```

Add assertions for phase/subflow files and explicit sibling mapper paths.

- [ ] **Step 3: Write the failing provenance test**

```python
def test_metadata_hashes_reviewed_notes(self):
    for metadata_path in SKILLS.glob("_shared/knowledge/**/_snapshot-metadata.yaml"):
        metadata = load_yaml(metadata_path)
        self.assertEqual(metadata["metadata_version"], "1.1")
        for item in metadata["sources"].values():
            self.assertIn("reviewed_note_hash_sha256", item)
            self.assertIn("reviewed_note_hash_recorded_at", item)
            self.assertNotIn("content_hash_sha256", item)
            self.assertNotIn("snapshot_created_at", item)
```

Also assert the note hash matches its local file, `last_checked` is documented as human review, reachability is explicit, and legal attribution names Wet IB 3.112 and AWR 52.

- [ ] **Step 4: Add failing eval set-equality assertions**

Require equality among shipped fixture paths, dataset fixture paths, dataset IDs, `benchmark_default_cases`, and benchmark `datasetCaseId` values.

- [ ] **Step 5: Run RED suites**

```bash
for pattern in \
  test_release_017_packaging.py \
  test_skill_discovery_and_loading.py \
  test_source_provenance.py; do
  python3 -m unittest discover -s plugins/nl-tax-agent-skills/tests -p "$pattern"
done
```

Expected: FAIL on command collisions, metadata 0.1.6, stale assets/docs, eager loading, old provenance keys, and incomplete eval parity.

### Task 2: Remove command collisions and migrate invocation metadata

**Files:**
- Delete: all seven files under `plugins/nl-tax-agent-skills/commands/`.
- Modify: seven corresponding `SKILL.md` frontmatter blocks.
- Modify: `plugins/nl-tax-agent-skills/tests/test_policy_and_field_maps.py`
- Modify: `.github/workflows/ci.yml`
- Modify: `CONTRIBUTING.md`

**Interfaces:**
- Consumes: legacy command `argument-hint` values.
- Produces: skills-only discovery with unchanged namespaced skill names.

- [ ] **Step 1: Add these exact frontmatter values before deleting wrappers**

```yaml
nl-tax-annual-return: "[2025] [confirm]"
nl-tax-evidence-indexer: "[path-to-upload-folder]"
nl-tax-field-mapper: "[annual|provisional] [year]"
nl-tax-intake: "[annual|request|change|review|stopzetten]"
nl-tax-provisional-assessment: "[2026] [request|change|review|stopzetten|confirm]"
nl-tax-source-refresh: "[annual|provisional|box3|all] [year]"
nl-tax-submit-companion: "[annual|provisional] [2025|2026]"
```

- [ ] **Step 2: Delete wrappers and replace wrapper tests**

Replace command-body assertions with exact no-directory, unique-name, and argument-hint assertions.

- [ ] **Step 3: Change CI/package checks**

Use:

```bash
test ! -e plugins/nl-tax-agent-skills/commands
```

- [ ] **Step 4: Run focused tests and Claude inventory**

```bash
python3 -m unittest discover -s plugins/nl-tax-agent-skills/tests -p 'test_release_017_packaging.py'
claude --plugin-dir plugins/nl-tax-agent-skills plugin details nl-tax-agent-skills
```

Expected: command/skill assertions PASS and inventory shows `Skills (12)`; later version/assets assertions remain RED.

### Task 3: Make skill triggering and loading Cowork-first

**Files:**
- Modify: all 12 `plugins/nl-tax-agent-skills/skills/*/SKILL.md` files.
- Shorten: `plugins/nl-tax-agent-skills/skills/nl-tax-annual-return/reference/annual-flow.md`
- Create: annual `reference/phases/*.md` phase files listed below.
- Shorten: provisional `reference/provisional-flow.md`
- Create: provisional `reference/subflows/*.md` files listed below.

**Interfaces:**
- Consumes: finalized workflow text from the tax/workflow plan.
- Produces: intent-specific metadata and phase/subflow references loaded only when relevant.

- [ ] **Step 1: Tighten public descriptions**

Public descriptions use the form “Use when the user explicitly wants to prepare, organize, review, index, map, or create a manual checklist.” Intake explicitly excludes informational questions. Evidence indexing requires indexing/organization intent rather than a document-name mention.

Background descriptions stay concise and distinguish annual/provisional method or section. `nl-tax-submit-companion` keeps its name but uses “Manual-entry checklist” as its title/copy.

- [ ] **Step 2: Split the annual flow without changing order or requirements**

Keep `annual-flow.md` as a short index/common contract and create:

```text
reference/phases/01-preflight.md
reference/phases/01-5-filing-status.md
reference/phases/02-income.md
reference/phases/02a-winst.md
reference/phases/03-own-home.md
reference/phases/03a-box2.md
reference/phases/04-box3.md
reference/phases/05-deductions.md
reference/phases/05-5-credits.md
reference/phases/06-partner.md
reference/phases/07-field-map.md
reference/phases/08-missing-info.md
reference/phases/09-review-questions.md
reference/phases/10-assembly.md
```

Each phase file is linked directly from the SKILL/index; no deeper reference chain is introduced.

- [ ] **Step 3: Split provisional subflows**

Create:

```text
reference/subflows/request.md
reference/subflows/change.md
reference/subflows/review.md
reference/subflows/stopzetten.md
```

The skill loads the common index and exactly one active subflow. Output contracts/templates load only after the generation gate.

- [ ] **Step 4: Replace every ambiguous cross-skill mapping path**

Use these explicit sibling paths:

```text
nl-tax-field-mapper/templates/field-map-template.yaml
nl-tax-field-mapper/reference/mapping-principles.md
nl-tax-field-mapper/reference/annual-field-map.md
nl-tax-field-mapper/reference/provisional-field-map.md
nl-tax-field-mapper/scripts/validate_field_map.py
```

- [ ] **Step 5: Run discovery/loading tests**

```bash
python3 -m unittest discover \
  -s plugins/nl-tax-agent-skills/tests \
  -p 'test_skill_discovery_and_loading.py'
```

Expected: PASS.

### Task 4: Correct reviewed-note provenance and legal attribution

**Files:**
- Modify: all 13 `skills/_shared/knowledge/**/_snapshot-metadata.yaml` files.
- Modify: source-refresh builder/validators/reporter and references.
- Modify: `skills/nl-tax-source-refresh/scripts/plan_source_refresh.py`.
- Modify: `skills/_shared/source-register.yaml`
- Modify: `skills/_shared/README.md`
- Modify: two existing generic law notes.
- Create: `skills/_shared/knowledge/laws/algemene-wet-inzake-rijksbelastingen.md`

**Interfaces:**
- Consumes: final knowledge notes after all tax edits.
- Produces: metadata schema 1.1 whose hashes unambiguously cover local reviewed notes.

- [ ] **Step 1: Change code/tests to the new keys while preserving review status**

Use exactly:

```python
metadata = {
    "metadata_version": "1.1",
    "reviewed_note_hash_sha256": compute_sha256(abs_snapshot),
    "reviewed_note_hash_recorded_at": now,
}
```

Keep `snapshot_path` in the source register for compatibility but document it as the reviewed-note path.

- [ ] **Step 2: Separate review from reachability in the reporter**

The plan-only reporter emits:

```python
record = {
    "url_reachability": "not_checked",
    "reachability_checked_at": None,
    "last_retrieved_at": None,
    "last_human_reviewed": str(source["last_checked"]),
    "reviewed_note_path": source["snapshot_path"],
    "reviewed_note_hash_sha256": compute_sha256(abs_snapshot),
}
```

It never implies that it fetched or archived a remote page. The optional-Python
plan already renamed this internal maintenance command; no compatibility shim
exists.

- [ ] **Step 3: Correct legal attribution**

Remove direct-eigenwoningforfait attribution from the Uitvoeringsbesluit note and cite Wet IB 2001 article 3.112. Remove general-retention attribution from the Uitvoeringsregeling note. Add an AWR article 52 note/source and include it where business retention is cited.

- [ ] **Step 4: Rebuild hashes once**

```bash
python3 plugins/nl-tax-agent-skills/skills/nl-tax-source-refresh/scripts/build_snapshots.py \
  plugins/nl-tax-agent-skills/skills/_shared/source-register.yaml
```

Review every changed note against its official URL, then set `review_status: reviewed`; the builder may not promote it automatically.

- [ ] **Step 5: Run provenance and source validators**

```bash
python3 -m unittest discover -s plugins/nl-tax-agent-skills/tests -p 'test_source_provenance.py'
python3 plugins/nl-tax-agent-skills/skills/nl-tax-source-refresh/scripts/validate_source_register.py \
  plugins/nl-tax-agent-skills/skills/_shared/source-register.yaml
python3 plugins/nl-tax-agent-skills/skills/nl-tax-source-refresh/scripts/validate_knowledge_pack.py \
  plugins/nl-tax-agent-skills/skills/_shared/source-register.yaml
```

Expected: PASS with zero missing/stale/hash errors.

### Task 5: Make fixture, dataset, default, and benchmark coverage identical

**Files:**
- Modify: `evals/nl-tax-agent-skills/offline-dataset.yaml`
- Modify: `evals/nl-tax-agent-skills/plugin-eval-benchmark.json`
- Modify: `evals/nl-tax-agent-skills/verify_offline_workspace.py`
- Modify: `evals/nl-tax-agent-skills/README.md`
- Create: `evals/claude/cowork-casual-tax-question/prompt.md`
- Create: `evals/claude/cowork-casual-tax-question/graders/criteria.md`
- Create: `evals/claude/cowork-explicit-annual-preparation/prompt.md`
- Create: `evals/claude/cowork-explicit-annual-preparation/graders/criteria.md`
- Create: `evals/claude/cowork-annual-entrepreneur-boundary/prompt.md`
- Create: `evals/claude/cowork-annual-entrepreneur-boundary/graders/criteria.md`
- Create: `evals/claude/cowork-provisional-entrepreneur-profit/prompt.md`
- Create: `evals/claude/cowork-provisional-entrepreneur-profit/graders/criteria.md`
- Create: `evals/claude/cowork-corrected-tax-rules/prompt.md`
- Create: `evals/claude/cowork-corrected-tax-rules/graders/criteria.md`
- Modify locally: `CLAUDE.md` (gitignored developer guide; runtime wording only)
- Modify: `plugins/nl-tax-agent-skills/tests/test_fixture_schema.py`
- Modify: `plugins/nl-tax-agent-skills/tests/test_eval_verifier.py`

**Interfaces:**
- Consumes: every shipped fixture, including new non-security cases from the tax/workflow plan.
- Produces: exact set equality and one benchmark scenario per dataset case.

- [ ] **Step 1: Add currently omitted shipped fixtures to the dataset**

Include `provisional/stopzetten-payment-redirect.yaml` and `security/source-staleness.yaml` without changing their content.

- [ ] **Step 2: Add `datasetCaseId` to every benchmark scenario**

Example:

```json
{
  "id": "annual-simple-resident",
  "datasetCaseId": "annual_simple_resident",
  "title": "Annual 2025 simple resident"
}
```

- [ ] **Step 3: Expand benchmark/default sets to exact dataset equality**

Add scenarios for every dataset case, including casual informational tax, explicit preparation, winst resume, annual entrepreneur preparation-only, provisional entrepreneur profit, corrected tax behavior, and stale-source semantics.

- [ ] **Step 4: Remove starter-template benchmark copy**

Replace generic notes/setup questions with actual NL tax task descriptions and verification expectations.

- [ ] **Step 5: Add first-party Claude behavior cases**

Use the native `prompt.md` plus `graders/criteria.md` format produced by
`claude plugin eval init --bare`. Grade only non-security behavior: casual
questions do not start intake, explicit preparation does, annual entrepreneurs
stay preparation-only, provisional profit uses the Winst section, and corrected
healthcare/credit/deadline claims are retrieved from the bundled notes.

- [ ] **Step 6: Run parity, offline, and Claude checks**

```bash
python3 plugins/nl-tax-agent-skills/tests/test_fixture_schema.py
python3 plugins/nl-tax-agent-skills/tests/test_eval_verifier.py
python3 evals/nl-tax-agent-skills/verify_offline_workspace.py --check-dataset
claude plugin eval plugins/nl-tax-agent-skills \
  --case 'cowork-*' \
  --runs 1 \
  --threshold 0.8 \
  --output-dir evals/results/0.1.7
```

Expected: PASS with exact case-set equality.

### Task 6: Align docs, assets, manifests, CI, and 0.1.7 release state

**Files:**
- Modify: `README.md`
- Modify: `plugins/nl-tax-agent-skills/README.md`
- Modify: `CONTRIBUTING.md`
- Modify: `CHANGELOG.md`
- Modify: `llm-agent-skill-plan.md`
- Modify: `skills/_shared/knowledge/platform/claude-skills.md`
- Modify: `skills/_shared/README.md`
- Modify: `evals/nl-tax-agent-skills/README.md`
- Modify: nested Claude/Codex manifests and root marketplace descriptions.
- Modify: `.github/workflows/ci.yml`
- Delete: `plugins/nl-tax-agent-skills/assets/logo.png`
- Delete: `plugins/nl-tax-agent-skills/assets/cowork-annual-return.png`
- Retain: `plugins/nl-tax-agent-skills/assets/icon.png`
- Verify unchanged: `PRIVACY.md`, `SECURITY.md`

**Interfaces:**
- Consumes: final behavior, script inventory, source schema, and eval set.
- Produces: consistent public release documentation and version 0.1.7 metadata.

- [ ] **Step 1: Rewrite Cowork-first quickstart and runtime wording**

Lead with a natural-language request such as:

```text
Help me prepare my 2025 Dutch income-tax workpack. I have my year statement and mortgage summary.
```

Move namespaced invocation to an advanced section. Correct the provisional command, remove command-precedence wording, describe local and remote Cowork sessions, state Python is optional, and distinguish first-party Claude validation from the unverified Cowork UI smoke gate.

- [ ] **Step 2: Fix contributor/history docs**

Remove `commands/`, add winst and phase/subflow layout, use one icon, replace stale 0.1.2 current examples, document Python 3.10+ optional helpers, mark `llm-agent-skill-plan.md` historical, and add a current 0.1.7 status matrix.

Use this future tag guard without creating retroactive tags:

```bash
test "$(git tag --list 'nl-tax-agent-skills--v0.1.7')" = ""
claude plugin tag plugins/nl-tax-agent-skills
git tag --list 'nl-tax-agent-skills--v0.1.7'
```

Update the ignored local `CLAUDE.md` only where it incorrectly describes Cowork
as always local/no-code or forbids scripts as a primary rule. Leave its
security/privacy sections unchanged. Because this file is not shipped or
tracked, the tracked README/contributor/platform notes remain the normative
source.

- [ ] **Step 3: Update assets and manifests**

Add to Claude manifest:

```json
"displayName": "NL Tax Agent Skills",
"homepage": "https://github.com/cyanxxy/nl-tax-agent-skills",
"repository": "https://github.com/cyanxxy/nl-tax-agent-skills"
```

Set both nested versions to `0.1.7`. Point Codex `composerIcon` and `logo` to `./assets/icon.png`. Delete the duplicate/stale images and update references.

- [ ] **Step 4: Add the Python 3.10/3.12 CI matrix**

```yaml
strategy:
  matrix:
    python-version: ["3.10", "3.12"]
```

Run compilation, validators, root tests, plugin-cwd tests, and offline dataset checks on the matrix. Python remains a maintainer/optional-helper dependency, never a taxpayer prerequisite.

- [ ] **Step 5: Add the 0.1.7 changelog entry**

List all non-security tax/workflow fixes, 12-skill discovery, optional Python reduction, progressive disclosure, provenance schema, eval parity, assets/manifests, and Cowork docs. State explicitly that security/privacy behavior and `PRIVACY.md`/`SECURITY.md` did not change.

- [ ] **Step 6: Run packaging tests**

```bash
python3 -m unittest discover -s plugins/nl-tax-agent-skills/tests -p 'test_release_017_packaging.py'
python3 -m unittest discover -s plugins/nl-tax-agent-skills/tests -p 'test_skill_discovery_and_loading.py'
```

Expected: PASS.

### Task 7: Execute the final release verification and review

**Files:**
- Verify: entire plugin/repository release surface.
- Verify unchanged: `PRIVACY.md`, `SECURITY.md`.

**Interfaces:**
- Consumes: Tasks 1–6 plus completed prior component plans.
- Produces: strict validation output, 12-skill runtime inventory, Plugin Eval evidence, package guards, and independent review approval.

- [ ] **Step 1: Validate JSON, source/workflow contracts, and Python**

```bash
python3 -m json.tool plugins/nl-tax-agent-skills/.codex-plugin/plugin.json >/dev/null
python3 -m json.tool plugins/nl-tax-agent-skills/.claude-plugin/plugin.json >/dev/null
python3 -m json.tool .claude-plugin/marketplace.json >/dev/null
python3 -m json.tool .agents/plugins/marketplace.json >/dev/null

python3 plugins/nl-tax-agent-skills/skills/nl-tax-source-refresh/scripts/validate_source_register.py \
  plugins/nl-tax-agent-skills/skills/_shared/source-register.yaml
python3 plugins/nl-tax-agent-skills/skills/nl-tax-source-refresh/scripts/validate_knowledge_pack.py \
  plugins/nl-tax-agent-skills/skills/_shared/source-register.yaml
python3 plugins/nl-tax-agent-skills/skills/nl-tax-source-refresh/scripts/validate_supported_workflows.py \
  plugins/nl-tax-agent-skills/skills/_shared/supported-workflows.yaml \
  plugins/nl-tax-agent-skills/skills/_shared/source-register.yaml
python3 plugins/nl-tax-agent-skills/skills/nl-tax-source-refresh/scripts/validate_invocation_policy.py \
  plugins/nl-tax-agent-skills/skills
python3 -m py_compile $(find plugins/nl-tax-agent-skills/skills plugins/nl-tax-agent-skills/tests -name '*.py' -print)
```

- [ ] **Step 2: Run full tests and offline dataset**

```bash
python3 -m unittest discover -s plugins/nl-tax-agent-skills/tests -p 'test_*.py'
(
  cd plugins/nl-tax-agent-skills
  python3 -m unittest discover -s tests -p 'test_*.py'
)
python3 evals/nl-tax-agent-skills/verify_offline_workspace.py --check-dataset
```

- [ ] **Step 3: Run strict Claude validation and inventory**

```bash
claude plugin validate plugins/nl-tax-agent-skills --strict
claude plugin validate . --strict
claude --plugin-dir plugins/nl-tax-agent-skills plugin details nl-tax-agent-skills
```

Expected inventory contains exactly `Skills (12)`.

- [ ] **Step 4: Run Plugin Eval analysis/benchmark**

```bash
PLUGIN_EVAL_JS="$(find "${CODEX_HOME:-$HOME/.codex}/plugins/cache" \
  -path '*/plugin-eval/*/scripts/plugin-eval.js' -type f -print | head -n 1)"
test -n "$PLUGIN_EVAL_JS"
node "$PLUGIN_EVAL_JS" analyze plugins/nl-tax-agent-skills --format markdown \
  > evals/nl-tax-agent-skills/plugin-eval-analysis-0.1.7.md
node "$PLUGIN_EVAL_JS" benchmark plugins/nl-tax-agent-skills \
  --config evals/nl-tax-agent-skills/plugin-eval-benchmark.json \
  --format markdown \
  > evals/nl-tax-agent-skills/plugin-eval-benchmark-0.1.7.md
```

Run the native Claude suite again with `--runs 3` and retain its aggregate JSON
under `evals/results/0.1.7/`. Summarize model/version, case scores, and any
documented Cowork UI gap in `evals/nl-tax-agent-skills/claude-eval-0.1.7.md`.

- [ ] **Step 5: Run package guards**

```bash
test ! -e plugins/nl-tax-agent-skills/commands
test "$(find plugins/nl-tax-agent-skills/skills -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l | tr -d ' ')" = "12"
test ! -e plugins/nl-tax-agent-skills/assets/logo.png
test ! -e plugins/nl-tax-agent-skills/assets/cowork-annual-return.png
test -e plugins/nl-tax-agent-skills/assets/icon.png

git ls-files plugins/nl-tax-agent-skills | \
  rg '(^|/)(commands|__pycache__)/|cowork-annual-return\.png$|logo\.png$|\.pyc$' && exit 1 || true

rg -n 'content_hash_sha256|Python 3\.8|currently `0\.1\.2`|commands/.*wrapper|skill takes precedence' \
  README.md CONTRIBUTING.md plugins/nl-tax-agent-skills evals/nl-tax-agent-skills \
  --glob '!CHANGELOG.md'

git diff --exit-code $(git merge-base main HEAD) HEAD -- PRIVACY.md SECURITY.md
git diff --check
```

Also run:

```bash
rg -n -i 'always.*local vm|cowork.*no-code|scripts.*not supported' CLAUDE.md
```

Expected: no stale runtime/no-code claim in the local guide.

Expected: asset/source scans return no current stale references; privacy/security diff is empty.

- [ ] **Step 6: Dispatch two independent read-only reviews**

Reviewer A maps every specification item to a file/test/runtime artifact. Reviewer B receives only the final plugin and realistic requests, then checks Cowork-oriented triggering, Python-free flow, corrected tax boundaries, and output ownership. Fix every Critical/Important non-security finding and re-run its covering tests.
