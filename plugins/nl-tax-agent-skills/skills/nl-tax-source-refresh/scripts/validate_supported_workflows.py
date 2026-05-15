#!/usr/bin/env python3
"""Validate source-backed workflow support declarations.

Usage:
    python validate_supported_workflows.py \
      <path-to-supported-workflows.yaml> <path-to-source-register.yaml>

Checks:
    - Active workflows have source IDs, knowledge dirs, output paths, and
      source-register coverage for the exact workflow/year or required shared
      all-year sources.
    - Blocked future workflows cannot produce workpacks.
    - Source-register workflow/year pairs are declared as active before they
      can be treated as supported.
"""

import json
import os
import sys


VALID_WORKFLOWS = {"annual_return", "provisional_assessment"}
BLOCKED_STATUSES = {"blocked_pending_official_sources"}


def load_yaml_or_json(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    try:
        import yaml
        return yaml.safe_load(content)
    except ImportError:
        return json.loads(content)


def find_plugin_root(config_path):
    """Find the plugin root that paths in supported-workflows.yaml use."""
    here = os.path.dirname(os.path.abspath(config_path))
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
    return candidates[0]


def source_scope_matches(source, workflow, tax_year):
    source_workflow = source.get("workflow")
    source_year = source.get("tax_year")

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
    if not isinstance(tax_year, int):
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
    errors.extend(validate_active_paths(workflow, wid, tax_year, plugin_root))
    errors.extend(validate_required_sources(workflow, wid, wf, tax_year, source_by_id))
    return errors


def validate_active_paths(workflow, wid, tax_year, plugin_root):
    errors = []
    knowledge_dirs = workflow.get("knowledge_dirs", [])
    if not knowledge_dirs:
        errors.append(f"{wid}: missing knowledge_dirs")
    for rel_path in knowledge_dirs:
        abs_path = os.path.join(plugin_root, rel_path)
        if not os.path.isdir(abs_path):
            errors.append(f"{wid}: knowledge_dir not found: {rel_path}")

    output_paths = workflow.get("output_paths", [])
    if not output_paths:
        errors.append(f"{wid}: missing output_paths")
    for rel_path in output_paths:
        if str(tax_year) not in rel_path:
            errors.append(f"{wid}: output path lacks tax year {tax_year}: {rel_path}")
    return errors


def validate_required_sources(workflow, wid, wf, tax_year, source_by_id):
    errors = []
    required_source_ids = workflow.get("required_source_ids", [])
    if not required_source_ids:
        errors.append(f"{wid}: missing required_source_ids")

    for sid in required_source_ids:
        source = source_by_id.get(sid)
        if source is None:
            errors.append(f"{wid}: unknown required source_id: {sid}")
            continue
        matches, reason = source_scope_matches(source, wf, tax_year)
        if not matches:
            errors.append(f"{wid}: source_id {sid} {reason}")
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
    if not isinstance(tax_year, int):
        errors.append(f"{wid}: tax_year must be an integer")
        return errors, warnings

    if (wf, int(tax_year)) in active_pairs:
        errors.append(f"{wid}: cannot be both active and blocked")
    if workflow.get("status") not in BLOCKED_STATUSES:
        errors.append(f"{wid}: invalid blocked status: {workflow.get('status')}")
    if workflow.get("may_prepare_workpack") is not False:
        errors.append(f"{wid}: blocked workflow must set may_prepare_workpack: false")
    if workflow.get("output_paths"):
        errors.append(f"{wid}: blocked workflow must not define output_paths")
    if workflow.get("required_source_ids"):
        errors.append(f"{wid}: blocked workflow must not define required_source_ids")
    if not workflow.get("reason"):
        warnings.append(f"{wid}: missing reason")
    if not workflow.get("unlock_condition"):
        warnings.append(f"{wid}: missing unlock_condition")
    return errors, warnings


def validate_source_pairs(sources, active_pairs):
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
        if pair not in active_pairs:
            errors.append(
                f"{source.get('id')}: source-register pair {pair} is not declared active"
            )
    return errors


def validate(config_path, register_path):
    config = load_yaml_or_json(config_path)
    register = load_yaml_or_json(register_path)
    sources = register if isinstance(register, list) else register.get("sources", [])
    source_by_id = {source.get("id"): source for source in sources}
    plugin_root = find_plugin_root(config_path)
    active_pairs = set()
    active_ids = set()
    blocked_ids = set()
    errors = []
    warnings = []

    for workflow in config.get("active_workflows", []):
        errors.extend(
            validate_active_workflow(
                workflow,
                active_ids,
                active_pairs,
                source_by_id,
                plugin_root,
            )
        )

    for workflow in config.get("blocked_workflows", []):
        blocked_errors, blocked_warnings = validate_blocked_workflow(
            workflow,
            blocked_ids,
            active_pairs,
        )
        errors.extend(blocked_errors)
        warnings.extend(blocked_warnings)

    errors.extend(validate_source_pairs(sources, active_pairs))
    return errors, warnings


def main():
    if len(sys.argv) != 3:
        print(
            "Usage: python validate_supported_workflows.py "
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
