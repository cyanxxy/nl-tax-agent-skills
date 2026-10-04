#!/usr/bin/env python3
"""Validate source-backed workflow support declarations.

Usage:
    python3 validate_supported_workflows.py \
      <path-to-supported-workflows.yaml> <path-to-source-register.yaml>

Checks:
    - Active workflows have source IDs, knowledge dirs, and source-register
      coverage for the exact workflow/year or required shared all-year
      sources. Their output_paths list exactly the one consented workpack file
      for that workflow and year (0.4 design, R3), for example
      workspace/nl-tax-annual-2025-workpack.md.
    - Blocked future workflows cannot produce workpacks and write nothing
      (allowed_output: conversation_only).
    - Terminal routing entries (manual_review / unsupported) never prepare a
      workpack and write nothing (allowed_output: conversation_only).
    - Source-register workflow/year pairs are declared as active before they
      can be treated as supported.
"""

import os
import sys
from datetime import date


VALID_WORKFLOWS = {"annual_return", "provisional_assessment", "vat_return", "vat_correction", "icp_declaration", "oss_return", "international_return"}
# The workflow gate itself must carry a valid, reasonably fresh attestation —
# it decides what the plugin is allowed to prepare.
LAST_REVIEWED_MAX_AGE_DAYS = 365
BLOCKED_STATUSES = {"blocked_pending_official_sources"}
TERMINAL_STATUSES = {"terminal_manual_review", "terminal_unsupported"}

WORKFLOW_SKILLS = {
    "annual_return": "nl-tax-annual-return",
    "provisional_assessment": "nl-tax-provisional-assessment",
    "vat_return": "nl-tax-vat-return",
    "vat_correction": "nl-tax-vat-correction",
    "icp_declaration": "nl-tax-icp",
    "oss_return": "nl-tax-oss",
    "international_return": "nl-tax-international-return",
}

COMMON_WORKFLOW_HELPER_SKILLS = {
    "nl-tax-intake",
    "nl-tax-field-mapper",
    "nl-tax-submit-companion",
}

# 0.4 design (R1/R3): terminal and blocked workflows write nothing; their only
# output is the conversation. Active workflows write exactly one consented
# workpack file per workflow and tax year, at a fixed path.
CONVERSATION_ONLY_OUTPUT = "conversation_only"
WORKPACK_SLUGS = {
    "annual_return": "annual",
    "provisional_assessment": "provisional",
    "vat_return": "vat",
    "vat_correction": "vat-correction",
}


def expected_workpack_path(workflow, tax_year):
    """Return the one workpack path an active workflow/year may write."""
    if workflow == "icp_declaration":
        return f"workspace/nl-tax-icp-{int(tax_year)}-{{period}}-workpack.md"
    if workflow == "oss_return":
        return f"workspace/nl-tax-oss-{{scheme}}-{int(tax_year)}-{{period}}-workpack.md"
    if workflow == "international_return":
        return f"workspace/nl-tax-international-{int(tax_year)}-{{return_form}}-workpack.md"
    slug = WORKPACK_SLUGS.get(workflow)
    if slug is None:
        return None
    period = "-{period}" if workflow in {"vat_return", "vat_correction"} else ""
    return f"workspace/nl-tax-{slug}-{int(tax_year)}{period}-workpack.md"

KNOWLEDGE_SKILL_HINTS = (
    ("box1", "nl-tax-box1-home"),
    ("own-home", "nl-tax-box1-home"),
    ("box2", "nl-tax-box2"),
    ("box3", "nl-tax-box3"),
    ("entrepreneur", "nl-tax-winst"),
    ("winst", "nl-tax-winst"),
    ("partner", "nl-tax-partner-deductions"),
)


def load_yaml_or_json(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    try:
        import yaml
    except ImportError:
        raise SystemExit(
            "PyYAML is required to run this validator "
            "(python3 -m pip install pyyaml)."
        )
    try:
        return yaml.safe_load(content)
    except yaml.YAMLError as exc:
        raise SystemExit(f"Error: invalid YAML in {path}: {exc}")


def find_plugin_root(reference_path):
    """Find the plugin root that workflow knowledge paths use."""
    here = os.path.dirname(os.path.abspath(reference_path))
    candidates = [
        os.path.abspath(os.path.join(here, "..", "..")),
        os.path.abspath(os.path.join(here, "..", "..", "..")),
    ]
    for candidate in candidates:
        if (
            os.path.isdir(os.path.join(candidate, ".claude-plugin"))
            or os.path.isdir(os.path.join(candidate, ".codex-plugin"))
        ):
            return candidate
    # Second tier like the sibling find_content_root implementations: a git
    # checkout marker (an install may strip the plugin dot-dirs). Final
    # fallback stays candidates[0] — the plugin root — because knowledge_dirs
    # paths in the config are serialized relative to the plugin root.
    for candidate in candidates:
        if (
            os.path.isdir(os.path.join(candidate, ".git"))
            or os.path.isfile(os.path.join(candidate, ".gitignore"))
        ):
            return candidate
    return candidates[0]


def source_scope_matches(source, workflow, tax_year):
    source_workflow = source.get("workflow")
    source_year = source.get("tax_year")
    families = {
        "vat": {"vat_return", "vat_correction", "icp_declaration", "oss_return"},
        "vat_cross_border": {"icp_declaration", "oss_return", "vat_return", "vat_correction"},
        "international": {"international_return"},
        "annual_2026": {"annual_return"},
    }
    family = source.get("workflow_family")
    if family in families and workflow not in families[family]:
        return False, f"{family} workflow-family source cannot be used by {workflow}"
    if family == "annual_2026" and tax_year != 2026:
        return False, "annual_2026 source cannot be used by another tax year"

    # workflow: security marks an all-workflow authorization/guidance source
    # (e.g. machtigen); it applies to every taxpayer-facing workflow rather
    # than being scoped to one of them.
    if source_workflow == "security":
        source_workflow = None

    if source_workflow and source_workflow != workflow:
        return False, f"workflow mismatch: {source_workflow} != {workflow}"

    if source_year is not None:
        try:
            if int(source_year) != int(tax_year):
                return False, f"tax_year mismatch: {source_year} != {tax_year}"
        except (TypeError, ValueError):
            return False, f"invalid source tax_year: {source_year}"

    return True, ""


def validate_active_workflow(workflow, active_ids, active_pairs, source_by_id, plugin_root):
    errors = []
    wid = workflow.get("id")
    wf = workflow.get("workflow")
    tax_year = workflow.get("tax_year")

    if not wid:
        return ["Active workflow without id"]
    if wid in active_ids:
        errors.append(f"Duplicate active workflow id: {wid}")
    active_ids.add(wid)

    if wf not in VALID_WORKFLOWS:
        errors.append(f"{wid}: invalid workflow: {wf}")
    if not isinstance(tax_year, int) or isinstance(tax_year, bool):
        errors.append(f"{wid}: tax_year must be an integer")
        return errors

    pair = (wf, int(tax_year))
    if pair in active_pairs:
        errors.append(f"{wid}: duplicate active workflow/year pair: {pair}")
    active_pairs.add(pair)

    if workflow.get("status") != "active":
        errors.append(f"{wid}: active workflow must have status: active")
    if not workflow.get("profile_candidates"):
        errors.append(f"{wid}: missing profile_candidates")
    errors.extend(validate_active_paths(workflow, wid, wf, tax_year, plugin_root))
    errors.extend(validate_required_sources(workflow, wid, wf, tax_year, source_by_id, plugin_root))
    return errors


def validate_active_paths(workflow, wid, wf, tax_year, plugin_root):
    errors = []
    knowledge_dirs = workflow.get("knowledge_dirs", [])
    if not knowledge_dirs:
        errors.append(f"{wid}: missing knowledge_dirs")
    elif not isinstance(knowledge_dirs, list):
        errors.append(f"{wid}: knowledge_dirs must be a list")
        knowledge_dirs = []
    for rel_path in knowledge_dirs:
        abs_path = os.path.join(plugin_root, rel_path)
        if not os.path.isdir(abs_path):
            errors.append(f"{wid}: knowledge_dir not found: {rel_path}")

    output_paths = workflow.get("output_paths", [])
    if not output_paths:
        errors.append(f"{wid}: missing output_paths")
    elif not isinstance(output_paths, list):
        errors.append(f"{wid}: output_paths must be a list")
        output_paths = []
    for rel_path in output_paths:
        if str(tax_year) not in str(rel_path):
            errors.append(f"{wid}: output path lacks tax year {tax_year}: {rel_path}")
    expected = expected_workpack_path(wf, tax_year)
    if expected is not None and output_paths and list(output_paths) != [expected]:
        errors.append(
            f"{wid}: output_paths must be exactly the one workpack file "
            f"[{expected}], got: {output_paths}"
        )
    return errors


def infer_required_skills(workflow, plugin_root):
    if workflow.get("workflow") == "annual_return" and workflow.get("tax_year") == 2026:
        return {"nl-tax-annual-return-2026"}
    if workflow.get("workflow") in {"vat_return", "vat_correction", "icp_declaration", "oss_return", "international_return"}:
        # VAT owners explicitly declare their source set. Shared mapper and
        # companion skills also serve IB; their all-year IB legal notes do not
        # become VAT dependencies, or correction-only notes return dependencies.
        return {WORKFLOW_SKILLS[workflow["workflow"]]}
    skills = set(COMMON_WORKFLOW_HELPER_SKILLS)
    workflow_skill = WORKFLOW_SKILLS.get(workflow.get("workflow"))
    if workflow_skill:
        skills.add(workflow_skill)

    for rel_path in workflow.get("knowledge_dirs", []):
        candidates = [rel_path.replace(os.sep, "/").lower()]
        abs_path = os.path.join(plugin_root, rel_path)
        if os.path.isdir(abs_path):
            try:
                children = os.listdir(abs_path)
            except OSError:
                children = []
            for child in children:
                candidates.append(child.lower())
        knowledge_text = "/".join(candidates)
        for hint, skill in KNOWLEDGE_SKILL_HINTS:
            if hint in knowledge_text:
                skills.add(skill)

    return skills


def normalize_skill_list(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return value
    return []


def validate_required_sources(workflow, wid, wf, tax_year, source_by_id, plugin_root):
    errors = []
    required_source_ids = workflow.get("required_source_ids", [])
    required_source_id_set = set(required_source_ids)
    if not required_source_ids:
        errors.append(f"{wid}: missing required_source_ids")

    for sid in required_source_ids:
        source = source_by_id.get(sid)
        if source is None:
            errors.append(f"{wid}: unknown required source_id: {sid}")
            continue
        if source.get("content_stage") == "draft_only" and workflow.get("status") == "active":
            errors.append(f"{wid}: active workflow cannot use draft-only source_id: {sid}")
        matches, reason = source_scope_matches(source, wf, tax_year)
        if not matches:
            errors.append(f"{wid}: source_id {sid} {reason}")

    inferred_skills = infer_required_skills(workflow, plugin_root)
    for sid, source in source_by_id.items():
        if not sid:
            continue
        mandatory_for = set(normalize_skill_list(source.get("mandatory_for", [])))
        matching_skills = sorted(mandatory_for.intersection(inferred_skills))
        if not matching_skills:
            continue
        # Security/authorization sources (workflow: security) are treated as
        # all-workflow by source_scope_matches, so a mandatory authorization
        # source must appear in every active workflow's required_source_ids.
        matches, _ = source_scope_matches(source, wf, tax_year)
        if not matches:
            continue
        if sid not in required_source_id_set:
            errors.append(
                f"{wid}: missing mandatory source_id: {sid} "
                f"(required by {', '.join(matching_skills)})"
            )
    return errors


def validate_draft_only_workflow(workflow, draft_ids, source_by_id, plugin_root):
    """A source-backed staging route may prepare drafts without claiming review."""
    wid = workflow.get("id")
    wf = workflow.get("workflow")
    year = workflow.get("tax_year")
    errors = []
    if not wid or wid in draft_ids:
        errors.append(f"Invalid or duplicate draft-only workflow id: {wid}")
    draft_ids.add(wid)
    allowed = {"vat_return", "vat_correction", "icp_declaration", "oss_return", "international_return"}
    if wf not in allowed and not (wf == "annual_return" and year == 2026):
        errors.append(f"{wid}: unsupported draft-only workflow/year")
    if year not in {2025, 2026} or isinstance(year, bool):
        errors.append(f"{wid}: draft-only tax_year must be 2025 or 2026")
        return errors
    if workflow.get("status") != "draft_only":
        errors.append(f"{wid}: draft-only workflow must have status: draft_only")
    if workflow.get("maximum_readiness") != "draft":
        errors.append(f"{wid}: draft-only workflow must set maximum_readiness: draft")
    if workflow.get("may_prepare_workpack") is not True:
        errors.append(f"{wid}: draft-only workflow must set may_prepare_workpack: true")
    if not workflow.get("profile_candidates"):
        errors.append(f"{wid}: missing profile_candidates")
    errors.extend(validate_active_paths(workflow, wid, wf, year, plugin_root))
    errors.extend(validate_required_sources(workflow, wid, wf, year, source_by_id, plugin_root))
    for sid in workflow.get("required_source_ids", []):
        source = source_by_id.get(sid)
        if not source:
            continue
        snapshot = source.get("snapshot_path")
        if not snapshot or not os.path.isfile(os.path.join(plugin_root, snapshot)):
            errors.append(f"{wid}: draft source snapshot missing: {sid}")
    return errors


def validate_blocked_workflow(workflow, blocked_ids, active_pairs):
    errors = []
    warnings = []
    wid = workflow.get("id")
    wf = workflow.get("workflow")
    tax_year = workflow.get("tax_year")

    if not wid:
        return ["Blocked workflow without id"], warnings
    if wid in blocked_ids:
        errors.append(f"Duplicate blocked workflow id: {wid}")
    blocked_ids.add(wid)

    if wf not in VALID_WORKFLOWS:
        errors.append(f"{wid}: invalid workflow: {wf}")
    if not isinstance(tax_year, int) or isinstance(tax_year, bool):
        errors.append(f"{wid}: tax_year must be an integer")
        return errors, warnings

    has_blocked_scope = bool(workflow.get("profile_candidates") or workflow.get("case_scope"))
    if (wf, int(tax_year)) in active_pairs and not has_blocked_scope:
        errors.append(f"{wid}: cannot be both active and blocked")
    if workflow.get("status") not in BLOCKED_STATUSES:
        errors.append(f"{wid}: invalid blocked status: {workflow.get('status')}")
    if workflow.get("may_prepare_workpack") is not False:
        errors.append(f"{wid}: blocked workflow must set may_prepare_workpack: false")
    if workflow.get("output_paths"):
        errors.append(f"{wid}: blocked workflow must not define output_paths")
    if workflow.get("required_source_ids"):
        errors.append(f"{wid}: blocked workflow must not define required_source_ids")
    allowed_output = workflow.get("allowed_output")
    if allowed_output != CONVERSATION_ONLY_OUTPUT:
        errors.append(
            f"{wid}: blocked workflow writes nothing; set allowed_output: "
            f"{CONVERSATION_ONLY_OUTPUT} (got: {allowed_output!r})"
        )
    if not workflow.get("reason"):
        warnings.append(f"{wid}: missing reason")
    if not workflow.get("unlock_condition"):
        warnings.append(f"{wid}: missing unlock_condition")
    return errors, warnings


def validate_terminal_workflow(workflow, terminal_ids):
    """Validate a terminal routing entry (manual_review / unsupported).

    Terminal workflows are intake end-states: they never prepare a workpack and
    write nothing (allowed_output: conversation_only). This guards their shape
    so a typo in may_prepare_workpack / allowed_output / status is caught
    instead of silently ignored.
    """
    errors = []
    warnings = []
    wid = workflow.get("id")
    if not wid:
        return ["Terminal workflow without id"], warnings
    if wid in terminal_ids:
        errors.append(f"Duplicate terminal workflow id: {wid}")
    terminal_ids.add(wid)

    if workflow.get("status") not in TERMINAL_STATUSES:
        errors.append(f"{wid}: invalid terminal status: {workflow.get('status')}")
    if workflow.get("may_prepare_workpack") is not False:
        errors.append(f"{wid}: terminal workflow must set may_prepare_workpack: false")
    if workflow.get("output_paths"):
        errors.append(f"{wid}: terminal workflow must not define output_paths")
    if workflow.get("required_source_ids"):
        errors.append(f"{wid}: terminal workflow must not define required_source_ids")
    allowed_output = workflow.get("allowed_output")
    if not allowed_output:
        errors.append(f"{wid}: terminal workflow must define allowed_output")
    elif allowed_output != CONVERSATION_ONLY_OUTPUT:
        errors.append(
            f"{wid}: terminal workflow writes nothing; allowed_output must be "
            f"{CONVERSATION_ONLY_OUTPUT}: {allowed_output}"
        )
    if not workflow.get("profile_candidates"):
        errors.append(f"{wid}: missing profile_candidates")
    if not workflow.get("reason"):
        warnings.append(f"{wid}: missing reason")
    return errors, warnings


def validate_source_pairs(sources, active_pairs, draft_pairs=None):
    errors = []
    for source in sources:
        wf = source.get("workflow")
        tax_year = source.get("tax_year")
        if wf not in VALID_WORKFLOWS or tax_year is None:
            continue
        try:
            pair = (wf, int(tax_year))
        except (TypeError, ValueError):
            errors.append(f"{source.get('id')}: invalid tax_year: {tax_year}")
            continue
        if source.get("content_stage") == "draft_only":
            if pair not in (draft_pairs or set()):
                errors.append(f"{source.get('id')}: draft source pair {pair} is not declared draft-only")
            continue
        if pair not in active_pairs:
            errors.append(
                f"{source.get('id')}: source-register pair {pair} is not declared active"
            )
    return errors


def validate_config_review_date(config):
    errors = []
    warnings = []
    last_reviewed = config.get("last_reviewed")
    if not last_reviewed:
        errors.append("supported-workflows: missing last_reviewed")
        return errors, warnings
    try:
        reviewed = date.fromisoformat(str(last_reviewed))
    except ValueError:
        errors.append(f"supported-workflows: invalid last_reviewed date: {last_reviewed}")
        return errors, warnings
    if reviewed > date.today():
        errors.append(f"supported-workflows: last_reviewed is in the future: {last_reviewed}")
    elif (date.today() - reviewed).days > LAST_REVIEWED_MAX_AGE_DAYS:
        errors.append(
            f"supported-workflows: last_reviewed {last_reviewed} is older than "
            f"{LAST_REVIEWED_MAX_AGE_DAYS} days — workflow support must be re-reviewed"
        )
    return errors, warnings


def validate(config_path, register_path):
    config = load_yaml_or_json(config_path)
    if not isinstance(config, dict):
        return ["supported-workflows file is empty or not a mapping"], []
    register = load_yaml_or_json(register_path)
    if isinstance(register, list):
        sources = register
    elif isinstance(register, dict):
        sources = register.get("sources", [])
    else:
        return ["source register is empty or not a mapping/list"], []
    sources = [s for s in sources if isinstance(s, dict)]
    source_by_id = {}
    duplicate_source_ids = []
    for source in sources:
        sid = source.get("id")
        if sid in source_by_id:
            # This validator runs standalone; do not rely on
            # validate_source_register.py having caught the duplicate first.
            duplicate_source_ids.append(f"duplicate source id in register: {sid}")
        source_by_id[sid] = source
    # The workflow registry is repository-only; the source register remains in
    # the plugin and therefore provides the stable base for bundled paths.
    plugin_root = find_plugin_root(register_path)
    active_pairs = set()
    active_ids = set()
    blocked_ids = set()
    errors = []
    warnings = []
    errors.extend(duplicate_source_ids)

    review_errors, review_warnings = validate_config_review_date(config)
    errors.extend(review_errors)
    warnings.extend(review_warnings)

    for index, workflow in enumerate(config.get("active_workflows", []) or []):
        if not isinstance(workflow, dict):
            errors.append(f"active_workflows[{index}] must be a mapping, got: {workflow!r}")
            continue
        errors.extend(
            validate_active_workflow(
                workflow,
                active_ids,
                active_pairs,
                source_by_id,
                plugin_root,
            )
        )

    draft_ids = set()
    draft_pairs = set()
    for index, workflow in enumerate(config.get("draft_only_workflows", []) or []):
        if not isinstance(workflow, dict):
            errors.append(f"draft_only_workflows[{index}] must be a mapping")
            continue
        errors.extend(validate_draft_only_workflow(workflow, draft_ids, source_by_id, plugin_root))
        pair = (workflow.get("workflow"), workflow.get("tax_year"))
        if pair in active_pairs or pair in draft_pairs:
            errors.append(f"{workflow.get('id')}: workflow/year pair is duplicated or both active and draft-only")
        draft_pairs.add(pair)
    for source in sources:
        if source.get("content_stage") != "draft_only":
            continue
        owners = set(normalize_skill_list(source.get("mandatory_for")))
        supported_draft_owners = {
            ("nl-tax-annual-return-2026" if wf == "annual_return" and year == 2026 else WORKFLOW_SKILLS.get(wf)) for wf, year in draft_pairs
        }
        if not owners.intersection(supported_draft_owners):
            errors.append(f"{source.get('id')}: draft-only source has no declared draft workflow owner")

    for index, workflow in enumerate(config.get("blocked_workflows", []) or []):
        if not isinstance(workflow, dict):
            errors.append(f"blocked_workflows[{index}] must be a mapping, got: {workflow!r}")
            continue
        blocked_errors, blocked_warnings = validate_blocked_workflow(
            workflow,
            blocked_ids,
            active_pairs,
        )
        errors.extend(blocked_errors)
        warnings.extend(blocked_warnings)

    terminal_ids = set()
    for index, workflow in enumerate(config.get("terminal_workflows", []) or []):
        if not isinstance(workflow, dict):
            errors.append(f"terminal_workflows[{index}] must be a mapping, got: {workflow!r}")
            continue
        terminal_errors, terminal_warnings = validate_terminal_workflow(
            workflow,
            terminal_ids,
        )
        errors.extend(terminal_errors)
        warnings.extend(terminal_warnings)

    errors.extend(validate_source_pairs(sources, active_pairs, draft_pairs))
    return errors, warnings


def main():
    if "-h" in sys.argv[1:] or "--help" in sys.argv[1:]:
        print("validate_supported_workflows.py — validate the supported-workflows gate against the register")
        print("Usage: python3 validate_supported_workflows.py <supported-workflows.yaml> <source-register.yaml>")
        sys.exit(0)

    if len(sys.argv) != 3:
        print(
            "Usage: python3 validate_supported_workflows.py "
            "<supported-workflows.yaml> <source-register.yaml>",
            file=sys.stderr,
        )
        sys.exit(1)

    config_path, register_path = sys.argv[1], sys.argv[2]
    for path in (config_path, register_path):
        if not os.path.isfile(path):
            print(f"Error: file not found: {path}", file=sys.stderr)
            sys.exit(1)

    errors, warnings = validate(config_path, register_path)

    if errors:
        print("VALIDATION FAILED")
        print()
        print("Errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("VALIDATION PASSED")

    if warnings:
        print()
        print("Warnings:")
        for warning in warnings:
            print(f"  - {warning}")

    print()
    print(f"Total: {len(errors)} errors, {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
