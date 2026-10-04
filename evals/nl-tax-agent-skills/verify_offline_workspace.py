#!/usr/bin/env python3
"""Verify hard 0.4 workspace contracts for the offline NL tax fixture library.

0.4 is conversation-first (docs/maintainers/0.4-conversation-first-design.md):
nothing is written by default, and only with the taxpayer's consent does the
plugin keep exactly one workpack file per workflow identity. Income tax has two
fixed paths (``global.workpack_paths``):

- ``workspace/nl-tax-annual-2025-workpack.md``
- ``workspace/nl-tax-provisional-2026-workpack.md``

The draft-only extension workflows (VAT return, VAT correction, ICP, OSS,
international, annual 2026) write one file per exact identity, for example
``workspace/nl-tax-vat-2026-Q3-workpack.md``. Their path templates come from
the workpack grader's ``WORKPACK_PATHS`` (mirrored in
``global.identity_workpack_paths``) and are matched with the grader's
token-aware regexes. Such a path is a permitted output only in a case that
lists it in ``expected_files``, which is how a case declares the taxpayer's save
consent for that identity.

For a selected case this verifier checks that the test workspace holds exactly
the expected workpacks (plus harness captures under ``workspace/eval/``), that
no 0.3 ledger path or other file was written, that seeded user files and 0.3
ledgers are byte-identical afterwards, that every expected workpack passes the
repository workpack grader, that Appendix B passes the field-map grader when
the case expects a map, and that each workpack's ``## Sources used`` equals its
Appendix A ``sources_loaded``. A harness capture of the workpack as shown in
the conversation (``presentation: chat``) is graded in the grader's chat mode:
only filled sections, no fill notes, and never Appendix A, Appendix B, or YAML
(review amendment A8). It never scores prose; agent behavior is graded from the
fixture expectations and the rubric.
"""

from __future__ import annotations

import argparse
import glob
import importlib.util
import os
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - local validation environment has PyYAML.
    raise SystemExit("PyYAML is required: python3 -m pip install pyyaml") from exc


SCRIPT_DIR = Path(__file__).resolve().parent
# SCRIPT_DIR is evals/nl-tax-agent-skills; parents[1] is the repository root.
REPO_ROOT = SCRIPT_DIR.parents[1]
DEFAULT_DATASET = SCRIPT_DIR / "offline-dataset.yaml"

WORKPACK_GRADER_REL = "tools/nl_tax_agent_skills/workpack/validate_workpack.py"
FIELD_MAP_GRADER_REL = "tools/nl_tax_agent_skills/field_mapper/validate_field_map.py"

DEFAULT_WORKPACK_PATHS = {
    "annual_2025": "workspace/nl-tax-annual-2025-workpack.md",
    "provisional_2026": "workspace/nl-tax-provisional-2026-workpack.md",
}
# Grader kinds whose path is one of the two fixed income-tax paths above; every
# other grader kind writes an identity-scoped path that a case must consent to.
FIXED_PATH_KINDS = {"annual": "annual_2025", "provisional": "provisional_2026"}
DEFAULT_HARNESS_GLOBS = ["workspace/eval/**"]
DEFAULT_LEGACY_PATHS = [
    "workspace/taxpayer/**",
    "workspace/shared/**",
    "workspace/annual/**",
    "workspace/provisional/**",
]
FIELD_MAP_EXPECTATIONS = {"expected", "not_yet_mapped"}
SAVE_CONSENT_VALUES = {"given", "not_given"}
PRESENTATIONS = {"file", "chat"}
# Keys that describe Appendix A / Appendix B, which a conversation rendering
# never shows (A8); a chat capture rule must not carry them.
APPENDIX_RULE_KEYS = (
    "save_consent",
    "readiness",
    "generation_confirmed",
    "queued_workflow",
    "sections",
    "field_map",
    "updated_after_created",
)
NO_FIELD_MAP_WORKFLOWS = {"provisional_2026_review", "provisional_2026_stopzetten"}
SKIPPED_DIRS = {"__pycache__", ".git", ".plugin-eval"}


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected YAML mapping in {path}")
    return data


def resolve_workspace_path(workspace: Path, pattern: str) -> Path:
    return workspace / pattern


def has_glob(pattern: str) -> bool:
    return any(char in pattern for char in "*?[")


def glob_matches(workspace: Path, pattern: str) -> list[Path]:
    # Escape the workspace prefix: a workspace path containing glob
    # metacharacters (e.g. "~/Projects [2026]/run1") must not silently match
    # nothing and fail every expected-files check.
    full_pattern = glob.escape(str(workspace)) + os.sep + pattern
    return [Path(match) for match in glob.glob(full_pattern, recursive=True)]


def path_exists(workspace: Path, pattern: str) -> bool:
    if has_glob(pattern):
        return bool(glob_matches(workspace, pattern))
    return resolve_workspace_path(workspace, pattern).exists()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def iter_text_files(root: Path) -> list[Path]:
    if not root.exists():
        return []

    result: list[Path] = []
    for current_root, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIPPED_DIRS]
        for filename in files:
            path = Path(current_root) / filename
            try:
                with path.open("rb") as handle:
                    chunk = handle.read(4096)
                if b"\0" in chunk:
                    continue
            except OSError:
                continue
            result.append(path)
    return result


def _pattern_regex(pattern: str) -> re.Pattern[str]:
    parts: list[str] = []
    index = 0
    while index < len(pattern):
        if pattern.startswith("**", index):
            parts.append(".*")
            index += 2
        elif pattern[index] == "*":
            parts.append("[^/]*")
            index += 1
        elif pattern[index] == "?":
            parts.append("[^/]")
            index += 1
        else:
            parts.append(re.escape(pattern[index]))
            index += 1
    return re.compile("^" + "".join(parts) + "$")


def matches_pattern(relative_path: str, pattern: str) -> bool:
    return bool(_pattern_regex(pattern).match(relative_path))


def selected_case_ids(args: argparse.Namespace, dataset: dict[str, Any]) -> list[str]:
    if args.case:
        return args.case
    if args.all:
        return [case["id"] for case in dataset.get("cases", [])]
    raise ValueError(
        "No structural contract selected. Pass --case <id> or --all; "
        "agentic benchmark runs never select cases through output marker files."
    )


def find_case(dataset: dict[str, Any], case_id: str) -> dict[str, Any]:
    for case in dataset.get("cases", []):
        if case.get("id") == case_id:
            return case
    raise KeyError(f"Unknown case id: {case_id}")


def contains(text: str, needle: str) -> bool:
    return needle.lower() in text.lower()


# ---------------------------------------------------------------------------
# Repository graders
# ---------------------------------------------------------------------------

_module_cache: dict[str, Any] = {}


def _load_repo_module(relative_path: str, module_name: str, label: str):
    if module_name in _module_cache:
        return _module_cache[module_name]
    candidates = [REPO_ROOT / relative_path, Path.cwd() / relative_path]
    for script in candidates:
        if script.is_file():
            spec = importlib.util.spec_from_file_location(module_name, script)
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
            except Exception as exc:  # a broken grader must not crash the eval
                raise ImportError(f"{label} failed to load from {script}: {exc}") from exc
            _module_cache[module_name] = module
            return module
    rendered = ", ".join(str(path) for path in candidates)
    raise FileNotFoundError(f"{label} not found; checked: {rendered}")


def load_workpack_grader():
    return _load_repo_module(
        WORKPACK_GRADER_REL, "validate_workpack_for_offline_eval", "workpack grader"
    )


def load_field_map_validator(workspace: Path | None = None, dataset: dict[str, Any] | None = None):
    # The field-map grader is repository tooling, not a plugin script: the
    # runtime check is the agent checklist plus human review. This harness
    # uses the grader after the fact to measure that the Appendix B map obeys
    # the canonical rules in reference/field-map-rules.yaml.
    return _load_repo_module(
        FIELD_MAP_GRADER_REL, "validate_field_map_for_offline_eval", "field-map validator"
    )


def plugin_root_for(dataset: dict[str, Any]) -> Path:
    plugin_root_rel = (dataset.get("global", {}) or {}).get(
        "plugin_root", "plugins/nl-tax-agent-skills"
    )
    candidates = [REPO_ROOT / plugin_root_rel, Path.cwd() / plugin_root_rel]
    return next((c for c in candidates if c.is_dir()), candidates[0])


# ---------------------------------------------------------------------------
# Layout, seeds, and generated-output scans
# ---------------------------------------------------------------------------


def _global(dataset: dict[str, Any]) -> dict[str, Any]:
    return dataset.get("global", {}) or {}


def workpack_paths(dataset: dict[str, Any]) -> dict[str, str]:
    return dict(_global(dataset).get("workpack_paths") or DEFAULT_WORKPACK_PATHS)


def identity_workpack_templates() -> dict[str, str]:
    """Grader path templates for the identity-scoped (non-fixed) workpack kinds."""
    grader = load_workpack_grader()
    return {
        kind: path for kind, path in grader.WORKPACK_PATHS.items() if kind not in FIXED_PATH_KINDS
    }


def _grader_or_none():
    try:
        return load_workpack_grader()
    except (FileNotFoundError, ImportError, OSError):
        return None


def identity_workpack_kind(relative: str) -> str | None:
    """Return the grader kind when ``relative`` is an identity-scoped workpack path.

    Without a loadable grader no identity-scoped path is recognized, so such a
    file is reported as unexpected (fail closed).
    """
    grader = _grader_or_none()
    if grader is None:
        return None
    for kind, regex in grader.WORKPACK_PATH_RES.items():
        if kind not in FIXED_PATH_KINDS and regex.match(relative):
            return kind
    return None


def is_workpack_filename(name: str) -> bool:
    """True for a canonical workpack file name of any kind (fixed or templated)."""
    grader = _grader_or_none()
    if grader is None:
        return name in {Path(path).name for path in DEFAULT_WORKPACK_PATHS.values()}
    return any(
        grader.WORKPACK_PATH_RES[kind].match("workspace/" + name) for kind in grader.WORKPACK_PATH_RES
    )


def consented_workpack_paths(dataset: dict[str, Any], case: dict[str, Any]) -> set[str]:
    """Workpack paths this case permits: an expected fixed or identity-scoped path."""
    fixed = set(workpack_paths(dataset).values())
    expected = set(case.get("expected_files") or [])
    return {
        relative
        for relative in expected
        if relative in fixed or identity_workpack_kind(relative) is not None
    }


def harness_globs(dataset: dict[str, Any]) -> list[str]:
    return list(_global(dataset).get("harness_output_globs", DEFAULT_HARNESS_GLOBS) or [])


def legacy_paths(dataset: dict[str, Any]) -> list[str]:
    return list(_global(dataset).get("legacy_forbidden_paths", DEFAULT_LEGACY_PATHS) or [])


def workspace_files(workspace: Path, root_relative: str) -> list[str]:
    root = workspace / root_relative
    if not root.exists():
        return []
    files: list[str] = []
    for current_root, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIPPED_DIRS]
        for name in names:
            files.append((Path(current_root) / name).relative_to(workspace).as_posix())
    return sorted(files)


def fixture_for_case(case: dict[str, Any]) -> dict[str, Any]:
    fixture = case.get("fixture")
    if not isinstance(fixture, str):
        return {}
    path = REPO_ROOT / fixture
    if not path.is_file():
        return {}
    try:
        return load_yaml(path)
    except (OSError, ValueError, yaml.YAMLError):
        return {}


def seed_files(case: dict[str, Any]) -> list[dict[str, str]]:
    seeds = fixture_for_case(case).get("seed_files") or []
    return [seed for seed in seeds if isinstance(seed, dict) and seed.get("path") and seed.get("from")]


def check_seeds(workspace: Path, case_id: str, seeds: list[dict[str, str]], errors: list[str]) -> None:
    for seed in seeds:
        target = workspace / seed["path"]
        source = REPO_ROOT / seed["from"]
        if not source.is_file():
            errors.append(f"{case_id}: seed source missing from the repository: {seed['from']}")
            continue
        if not target.is_file():
            errors.append(
                f"{case_id}: seeded file missing: {seed['path']} "
                "(the plugin never moves, renames, or deletes the user's files)"
            )
        elif target.read_bytes() != source.read_bytes():
            errors.append(
                f"{case_id}: seeded file changed: {seed['path']} "
                "(the plugin never rewrites the user's documents or 0.3 ledgers)"
            )


def check_layout(
    workspace: Path,
    dataset: dict[str, Any],
    case_id: str,
    case: dict[str, Any],
    seed_paths: set[str],
    errors: list[str],
) -> None:
    root_relative = _global(dataset).get("generated_output_root", "workspace")
    fixed_workpacks = set(workpack_paths(dataset).values())
    consented = consented_workpack_paths(dataset, case)
    harness = harness_globs(dataset)
    legacy = legacy_paths(dataset)

    for relative in workspace_files(workspace, root_relative):
        if relative in seed_paths:
            continue
        if any(matches_pattern(relative, pattern) for pattern in legacy):
            errors.append(
                f"{case_id}: legacy 0.3 path written: {relative} "
                "(0.4 writes only the consented workpack file)"
            )
        elif relative in fixed_workpacks or identity_workpack_kind(relative) is not None:
            if relative not in consented:
                errors.append(
                    f"{case_id}: workpack written without this case's save consent: {relative}"
                )
        elif any(matches_pattern(relative, pattern) for pattern in harness):
            continue
        else:
            permitted = ", ".join(sorted(consented)) or "none in this case"
            errors.append(
                f"{case_id}: unexpected file under {root_relative}/: {relative} "
                f"(the plugin may write only the case's consented workpack path(s): {permitted})"
            )

    # R3: no copy, versioned or dated variant, or second workspace/ tree
    # anywhere in the task folder.
    for current_root, dirs, names in os.walk(workspace):
        dirs[:] = [d for d in dirs if d not in SKIPPED_DIRS]
        current = Path(current_root)
        for directory in dirs:
            relative = (current / directory).relative_to(workspace).as_posix()
            if directory == root_relative and relative != root_relative:
                errors.append(f"{case_id}: second workspace tree: {relative}/")
        for name in names:
            relative = (current / name).relative_to(workspace).as_posix()
            if relative in seed_paths or relative in fixed_workpacks or relative in consented:
                continue
            if name.startswith("nl-tax-") and "workpack" in name:
                canonical = is_workpack_filename(name)
                if canonical and not relative.startswith(root_relative + "/"):
                    # A file with a canonical workpack name outside workspace/
                    # is only acceptable as a seeded attachment (handled above).
                    errors.append(f"{case_id}: workpack copy outside {root_relative}/: {relative}")
                elif not canonical:
                    errors.append(f"{case_id}: workpack copy or variant: {relative}")

    for pattern in case.get("forbidden_files", []) or []:
        matches = glob_matches(workspace, pattern) if has_glob(pattern) else []
        if not has_glob(pattern) and resolve_workspace_path(workspace, pattern).exists():
            matches = [resolve_workspace_path(workspace, pattern)]
        matches = [m for m in matches if m.relative_to(workspace).as_posix() not in seed_paths]
        if matches:
            rel_matches = ", ".join(str(match.relative_to(workspace)) for match in matches[:5])
            errors.append(f"{case_id}: forbidden path exists for {pattern}: {rel_matches}")


# Memo for the forbidden-regex sweep: the output tree is static during a
# verification run, so scan it once per (root, patterns) instead of once per
# case when --all or a multi-case marker is used.
_generated_output_scan_cache: dict[tuple, list[tuple[str, str]]] = {}


def _scan_generated_output(workspace: Path, output_root: Path, patterns: list[str]) -> list[tuple[str, str]]:
    key = (str(output_root), tuple(patterns))
    if key not in _generated_output_scan_cache:
        hits: list[tuple[str, str]] = []
        compiled = [(pattern, re.compile(pattern)) for pattern in patterns]
        for path in iter_text_files(output_root):
            text = read_text(path)
            rel_path = str(path.relative_to(workspace))
            for pattern, regex in compiled:
                if regex.search(text):
                    hits.append((rel_path, pattern))
        _generated_output_scan_cache[key] = hits
    return _generated_output_scan_cache[key]


def check_generated_output_regex(
    workspace: Path,
    dataset: dict[str, Any],
    case_id: str,
    errors: list[str],
) -> None:
    global_config = _global(dataset)
    output_root = workspace / global_config.get("generated_output_root", "workspace")
    patterns = global_config.get("forbidden_generated_output_regex", []) or []
    if not patterns:
        return

    for rel_path, pattern in _scan_generated_output(workspace, output_root, patterns):
        errors.append(f"{case_id}: {rel_path} matches forbidden generated-output regex: {pattern}")


# ---------------------------------------------------------------------------
# Workpack, field-map, appendix, and source-ledger checks
# ---------------------------------------------------------------------------


def _kind_for_workflow(workflow: Any) -> str | None:
    """The grader's kind for an Appendix A workflow identity (None when unknown)."""
    try:
        grader = load_workpack_grader()
    except (FileNotFoundError, ImportError, OSError):
        return None
    return grader.kind_for_workflow(workflow)


def check_field_map(
    workspace: Path,
    case_id: str,
    relative: str,
    errors: list[str],
    warnings: list[str],
) -> None:
    try:
        grader = load_workpack_grader()
        validator = load_field_map_validator()
    except (FileNotFoundError, ImportError, OSError) as exc:
        errors.append(f"{case_id}: field-map validation unavailable: {exc}")
        return
    state, data, extract_errors = grader.extract_field_map(read_text(workspace / relative))
    if state != "mapped":
        detail = "; ".join(extract_errors) or "Appendix B holds 'not yet mapped'"
        errors.append(
            f"{case_id}: field-map validation failed for {relative}: expected an Appendix B field map ({detail})"
        )
        return
    validation_errors, validation_warnings = validator.validate(data)
    for error in validation_errors:
        errors.append(f"{case_id}: field-map validation failed for {relative}: {error}")
    # Warnings are informational only: surfaced for visibility but never fatal.
    for warning in validation_warnings:
        warnings.append(f"{case_id}: field-map validation warning for {relative}: {warning}")


def _documents_expectations(
    grader, text: str, case_id: str, relative: str, rule: dict[str, Any], errors: list[str]
) -> None:
    expectations = rule.get("documents") or {}
    if not expectations:
        return
    rows = grader.documents_rows(text)
    minimum = expectations.get("min_rows")
    if isinstance(minimum, int) and len(rows) < minimum:
        errors.append(
            f"{case_id}: {relative} '## Documents and sources' has {len(rows)} row(s); expected at least {minimum}"
        )
    statuses = {
        _plain(row.get(header, "")).lower()
        for row in rows
        for header in row
        if header.startswith("status")
    }
    for status in expectations.get("statuses_present", []) or []:
        if str(status).lower() not in statuses:
            errors.append(
                f"{case_id}: {relative} '## Documents and sources' has no row with status {status!r}"
            )
    names = [
        _plain(row.get(header, "")).lower()
        for row in rows
        for header in row
        if header.startswith("document")
    ]
    for needle in expectations.get("document_contains_any", []) or []:
        options = needle if isinstance(needle, list) else [needle]
        if not any(str(option).lower() in name for option in options for name in names):
            rendered = ", ".join(repr(str(option)) for option in options)
            errors.append(
                f"{case_id}: {relative} '## Documents and sources' names no document matching {rendered}"
            )


def _plain(cell: str) -> str:
    return str(cell).strip().strip("`*").strip()


def check_workpacks(
    workspace: Path,
    dataset: dict[str, Any],
    case_id: str,
    case: dict[str, Any],
    errors: list[str],
    warnings: list[str],
) -> None:
    rules = case.get("workpacks") or []
    if not rules:
        return
    try:
        grader = load_workpack_grader()
    except (FileNotFoundError, ImportError, OSError) as exc:
        errors.append(f"{case_id}: workpack validation unavailable: {exc}")
        return
    plugin_root = plugin_root_for(dataset)

    for rule in rules:
        relative = rule.get("path")
        workflow = rule.get("workflow")
        kind = _kind_for_workflow(workflow)
        if not isinstance(relative, str) or kind is None:
            errors.append(f"{case_id}: invalid workpack rule: {rule!r}")
            continue
        path = workspace / relative
        if not path.is_file():
            errors.append(f"{case_id}: expected workpack missing: {relative}")
            continue
        if rule.get("presentation") == "chat":
            report = grader.validate_workpack_file(
                path, expected_kind=kind, plugin_root=plugin_root, presentation="chat"
            )
            for error in report.errors:
                errors.append(f"{case_id}: conversation rendering check failed for {relative}: {error}")
            for warning in report.warnings:
                warnings.append(f"{case_id}: conversation rendering warning for {relative}: {warning}")
            _documents_expectations(grader, read_text(path), case_id, relative, rule, errors)
            continue
        consent = rule.get("save_consent", "given")
        report = grader.validate_workpack_file(
            path,
            expected_kind=kind,
            expect_saved=consent == "given",
            plugin_root=plugin_root,
        )
        for error in report.errors:
            errors.append(f"{case_id}: workpack validation failed for {relative}: {error}")
        for warning in report.warnings:
            warnings.append(f"{case_id}: workpack validation warning for {relative}: {warning}")

        record = report.resume_record if isinstance(report.resume_record, dict) else {}
        if record.get("workflow") != workflow:
            errors.append(
                f"{case_id}: {relative} Appendix A workflow {record.get('workflow')!r} != {workflow!r}"
            )
        if record.get("save_consent") != consent:
            errors.append(
                f"{case_id}: {relative} Appendix A save_consent {record.get('save_consent')!r} != {consent!r}"
            )
        for key in ("readiness", "generation_confirmed", "queued_workflow"):
            if key in rule and record.get(key) != rule[key]:
                errors.append(
                    f"{case_id}: {relative} Appendix A {key} {record.get(key)!r} != {rule[key]!r}"
                )
        sections = record.get("sections") if isinstance(record.get("sections"), dict) else {}
        for section, allowed in (rule.get("sections") or {}).items():
            allowed_list = [allowed] if isinstance(allowed, str) else list(allowed)
            entry = sections.get(section) if isinstance(sections.get(section), dict) else {}
            status = entry.get("status")
            if status not in allowed_list:
                errors.append(
                    f"{case_id}: {relative} sections.{section}.status {status!r} not in {allowed_list!r}"
                )
        if rule.get("updated_after_created"):
            created = grader._parse_timestamp(record.get("created_at"))
            updated = grader._parse_timestamp(record.get("updated_at"))
            if not (created and updated and updated > created):
                errors.append(
                    f"{case_id}: {relative} must have been kept current after it was first "
                    "saved (updated_at later than created_at)"
                )

        text = read_text(path)
        _documents_expectations(grader, text, case_id, relative, rule, errors)

        expectation = rule.get("field_map")
        if expectation == "expected":
            check_field_map(workspace, case_id, relative, errors, warnings)
        elif expectation == "not_yet_mapped" and report.field_map_state != "not_yet_mapped":
            errors.append(
                f"{case_id}: {relative} Appendix B must read 'not yet mapped' "
                f"(found {report.field_map_state})"
            )


def check_text_rule(
    workspace: Path, case_id: str, rule: dict[str, Any], errors: list[str]
) -> None:
    """Contains-checks on one YAML appendix of a workpack, never on prose."""
    relative = rule.get("path", "")
    path = resolve_workspace_path(workspace, relative)
    if not path.is_file():
        errors.append(f"{case_id}: text check file missing: {relative}")
        return
    letter = str(rule.get("appendix", "")).upper()
    try:
        grader = load_workpack_grader()
    except (FileNotFoundError, ImportError, OSError) as exc:
        errors.append(f"{case_id}: workpack grader unavailable for text checks: {exc}")
        return
    if letter not in {"A", "B"}:
        errors.append(f"{case_id}: text check on {relative} must target appendix A or B")
        return
    text = grader.appendix_yaml_text(read_text(path), letter)
    if text is None:
        errors.append(f"{case_id}: {relative} has no single Appendix {letter} yaml block to check")
        return
    label = f"{relative} Appendix {letter}"

    for needle in rule.get("all", []) or []:
        if not contains(text, str(needle)):
            errors.append(f"{case_id}: {label} missing required text: {needle!r}")

    for group in rule.get("any", []) or []:
        options = group if isinstance(group, list) else [group]
        if not any(contains(text, str(option)) for option in options):
            rendered = ", ".join(repr(str(option)) for option in options)
            errors.append(f"{case_id}: {label} missing one of: {rendered}")

    for needle in rule.get("none", []) or []:
        if contains(text, str(needle)):
            errors.append(f"{case_id}: {label} contains forbidden text: {needle!r}")


def check_source_ledger(
    workspace: Path,
    case_id: str,
    case: dict[str, Any],
    errors: list[str],
    dataset: dict[str, Any] | None = None,
) -> None:
    """Each workpack's ``## Sources used`` equals its own Appendix A ledger.

    Ledgers are workflow-scoped: an annual ledger never holds a
    provisional-assessment source and vice versa, so neither is a union of
    both workflows' consultations.
    """
    config = case.get("source_ledger_check")
    if not config:
        return
    try:
        grader = load_workpack_grader()
    except (FileNotFoundError, ImportError, OSError) as exc:
        errors.append(f"{case_id}: source-ledger check unavailable: {exc}")
        return
    register = grader.source_register(str(plugin_root_for(dataset or {})))

    for relative in config.get("workpacks", []) or []:
        path = resolve_workspace_path(workspace, relative)
        if not path.is_file():
            errors.append(f"{case_id}: source-ledger workpack missing: {relative}")
            continue
        text = read_text(path)
        record, record_errors = grader.resume_record_block(text)
        if record_errors:
            errors.append(f"{case_id}: source-ledger resume record invalid in {relative}: {record_errors[0]}")
            continue
        loaded = record.get("sources_loaded")
        used = grader.sources_used(text)
        if used is None:
            errors.append(f"{case_id}: {relative} missing Sources used section")
            continue
        if not isinstance(loaded, list) or sorted(set(used)) != sorted(set(map(str, loaded))):
            errors.append(
                f"{case_id}: {relative} Sources used {used!r} must equal Appendix A "
                f"sources_loaded {loaded!r}"
            )
        kind = grader.kind_for_workflow(record.get("workflow"))
        if register is None or kind is None or not isinstance(loaded, list):
            continue
        # The grader's own compatibility rule (register workflow against
        # FIELD_MAP_WORKFLOWS[kind], workflow_family, ICP/OSS ownership, tax
        # year), so the verifier and the grader never drift apart.
        crossed = []
        for source_id in loaded:
            entry = register.get(str(source_id))
            if entry is None:
                continue
            problem = grader.source_scope_error(str(source_id), entry, kind, record.get("tax_year"))
            if problem:
                crossed.append(problem)
        if crossed:
            errors.append(
                f"{case_id}: {relative} sources_loaded holds source(s) of another workflow or year "
                f"({'; '.join(crossed)}); a workflow ledger is never a cross-workflow union"
            )


def verify_case(
    workspace: Path,
    dataset: dict[str, Any],
    case: dict[str, Any],
    warnings: list[str] | None = None,
) -> list[str]:
    errors: list[str] = []
    # Warnings are informational only and never affect pass/fail. Callers that
    # want to surface them pass a list to accumulate into; otherwise they are
    # collected in a local list and discarded. verify_case's return contract
    # stays a plain errors list.
    if warnings is None:
        warnings = []
    case_id = case["id"]

    for pattern in case.get("expected_files", []) or []:
        if not path_exists(workspace, pattern):
            errors.append(f"{case_id}: expected file missing: {pattern}")

    seeds = seed_files(case)
    seed_paths = {seed["path"] for seed in seeds}
    check_seeds(workspace, case_id, seeds, errors)
    check_layout(workspace, dataset, case_id, case, seed_paths, errors)
    check_workpacks(workspace, dataset, case_id, case, errors, warnings)
    for rule in case.get("text_checks", []) or []:
        check_text_rule(workspace, case_id, rule, errors)
    check_source_ledger(workspace, case_id, case, errors, dataset)
    check_generated_output_regex(workspace, dataset, case_id, errors)

    unique: list[str] = []
    for error in errors:
        if error not in unique:
            unique.append(error)
    return unique


def validate_dataset_paths(dataset_path: Path, dataset: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    cases = dataset.get("cases", []) or []
    case_ids = [case.get("id") for case in cases]
    fixture_paths = [case.get("fixture") for case in cases]
    default_ids = dataset.get("contract_default_cases", []) or []

    if len(case_ids) != len(set(case_ids)):
        errors.append("dataset case ids must be unique")
    if len(default_ids) != len(set(default_ids)):
        errors.append("contract_default_cases must not contain duplicates")
    if set(default_ids) != set(case_ids):
        missing = sorted(set(case_ids) - set(default_ids))
        extra = sorted(set(default_ids) - set(case_ids))
        errors.append(
            "contract_default_cases must equal dataset case ids "
            f"(missing={missing}, extra={extra})"
        )
    if len(fixture_paths) != len(set(fixture_paths)):
        errors.append("each dataset case must reference a unique fixture path")

    fixture_root = REPO_ROOT / "evals/nl-tax-agent-skills/fixtures"
    shipped = {
        path.relative_to(REPO_ROOT).as_posix()
        for path in fixture_root.glob("*/*.yaml")
    }
    referenced = {path for path in fixture_paths if isinstance(path, str)}
    if referenced != shipped:
        errors.append(
            "dataset fixture paths must equal repository fixture paths "
            f"(missing={sorted(shipped - referenced)}, extra={sorted(referenced - shipped)})"
        )

    global_config = _global(dataset)
    if "case_marker" in global_config:
        errors.append("global must not define a case marker")
    workpacks_by_family = workpack_paths(dataset)
    if workpacks_by_family != DEFAULT_WORKPACK_PATHS:
        errors.append(
            f"global.workpack_paths must be the two fixed 0.4 workpack paths {DEFAULT_WORKPACK_PATHS}"
        )
    allowed_workpacks = set(workpacks_by_family.values())
    try:
        grader = load_workpack_grader()
        templates = identity_workpack_templates()
    except (FileNotFoundError, ImportError, OSError) as exc:
        return errors + [f"workpack grader unavailable for dataset checks: {exc}"]
    declared = global_config.get("identity_workpack_paths")
    if declared != templates:
        errors.append(
            "global.identity_workpack_paths must mirror the workpack grader's WORKPACK_PATHS "
            f"for the identity-scoped workflows {templates} (got {declared!r})"
        )
    harness = harness_globs(dataset)
    legacy = legacy_paths(dataset)
    if not set(DEFAULT_LEGACY_PATHS) <= set(legacy):
        errors.append(f"global.legacy_forbidden_paths must include {DEFAULT_LEGACY_PATHS}")

    for case in cases:
        case_id = case.get("id", "<unknown>")
        fixture = case.get("fixture")
        if fixture and not (REPO_ROOT / fixture).is_file():
            errors.append(f"{case_id}: fixture does not exist: {fixture}")
        if "prompt" in case:
            errors.append(f"{case_id}: structural cases carry no model prompt")
        expected = case.get("expected_files", []) or []
        for pattern in expected:
            if any(matches_pattern(pattern, legacy_pattern) for legacy_pattern in legacy):
                errors.append(f"{case_id}: expected file is a legacy 0.3 path: {pattern}")
            elif (
                pattern not in allowed_workpacks
                and identity_workpack_kind(pattern) is None
                and not any(matches_pattern(pattern, glob_pattern) for glob_pattern in harness)
            ):
                errors.append(
                    f"{case_id}: expected file is neither a workpack nor a harness capture: {pattern}"
                )
            if pattern.endswith("current-case.txt"):
                errors.append(f"{case_id}: expected files must not include a case marker")

        rules = case.get("workpacks", []) or []
        rule_paths = set()
        for rule in rules:
            relative = rule.get("path")
            workflow = rule.get("workflow")
            kind = _kind_for_workflow(workflow)
            rule_paths.add(relative)
            if relative not in expected:
                errors.append(f"{case_id}: workpack rule path {relative!r} is not an expected file")
            if kind is None:
                errors.append(f"{case_id}: workpack rule has unknown workflow {workflow!r}")
            consent = rule.get("save_consent", "given")
            if consent not in SAVE_CONSENT_VALUES:
                errors.append(f"{case_id}: workpack rule save_consent must be given or not_given")
            presentation = rule.get("presentation", "file")
            if presentation not in PRESENTATIONS:
                errors.append(f"{case_id}: workpack rule presentation must be one of {sorted(PRESENTATIONS)}")
            if relative in allowed_workpacks or identity_workpack_kind(relative) is not None:
                own_path = grader.workpack_path_for_workflow(workflow) if kind is not None else None
                if kind is not None and own_path != relative:
                    errors.append(f"{case_id}: {workflow} belongs in {own_path}, not {relative}")
                if consent != "given":
                    errors.append(f"{case_id}: a saved workpack file implies save_consent: given")
                if presentation == "chat":
                    errors.append(f"{case_id}: {relative} is a saved file, not a conversation rendering")
            else:
                if presentation != "chat":
                    errors.append(
                        f"{case_id}: {relative} is a harness capture of the workpack shown in the "
                        "conversation; use presentation: chat"
                    )
                stray = [key for key in APPENDIX_RULE_KEYS if key in rule]
                if stray:
                    errors.append(
                        f"{case_id}: {relative} is a conversation rendering without Appendix A/B; "
                        f"drop {', '.join(stray)}"
                    )
            field_map = rule.get("field_map")
            if field_map is not None and field_map not in FIELD_MAP_EXPECTATIONS:
                errors.append(f"{case_id}: field_map must be one of {sorted(FIELD_MAP_EXPECTATIONS)}")
            if workflow in NO_FIELD_MAP_WORKFLOWS and field_map == "expected":
                errors.append(f"{case_id}: {workflow} never produces a field map")
        for relative in expected:
            if (
                relative in allowed_workpacks or identity_workpack_kind(relative) is not None
            ) and relative not in rule_paths:
                errors.append(f"{case_id}: expected workpack {relative} has no workpacks rule")

        chat_paths = {
            rule.get("path") for rule in rules if rule.get("presentation") == "chat"
        }
        for rule in case.get("text_checks", []) or []:
            if str(rule.get("appendix", "")).upper() not in {"A", "B"}:
                errors.append(f"{case_id}: text checks target a YAML appendix (A or B), never prose")
            if rule.get("path") not in rule_paths:
                errors.append(f"{case_id}: text check path {rule.get('path')!r} has no workpacks rule")
            elif rule.get("path") in chat_paths:
                errors.append(
                    f"{case_id}: text check path {rule.get('path')!r} is a conversation rendering, "
                    "which never shows the YAML appendices"
                )

        ledger = case.get("source_ledger_check") or {}
        for relative in ledger.get("workpacks", []) or []:
            if relative not in rule_paths:
                errors.append(f"{case_id}: source-ledger workpack {relative!r} has no workpacks rule")
            elif relative in chat_paths:
                errors.append(
                    f"{case_id}: source-ledger workpack {relative!r} is a conversation rendering "
                    "without Appendix A sources_loaded"
                )

        for seed in seed_files(case):
            if not (REPO_ROOT / seed["from"]).is_file():
                errors.append(f"{case_id}: seed source does not exist: {seed['from']}")
            if seed["path"] in allowed_workpacks or identity_workpack_kind(seed["path"]) is not None:
                errors.append(
                    f"{case_id}: a seed must not occupy a fixed workpack path; put an attached "
                    "workpack outside workspace/"
                )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=".", help="Workspace root to verify. Defaults to current directory.")
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET), help="Offline dataset YAML path.")
    parser.add_argument("--case", action="append", help="Case id to verify. Can be passed more than once.")
    parser.add_argument("--all", action="store_true", help="Verify every case in the dataset.")
    parser.add_argument("--check-dataset", action="store_true", help="Validate dataset fixture paths and exit.")
    parser.add_argument("--list", action="store_true", help="List case ids and exit.")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    dataset_path = Path(args.dataset).resolve()
    dataset = load_yaml(dataset_path)

    if args.list:
        for case in dataset.get("cases", []) or []:
            print(case["id"])
        return 0

    errors = validate_dataset_paths(dataset_path, dataset)
    if args.check_dataset:
        if errors:
            print("OFFLINE DATASET FAILED")
            for error in errors:
                print(f"  - {error}")
            return 1
        print("OFFLINE DATASET PASSED")
        return 0

    warnings: list[str] = []
    case_ids: list[str] = []
    try:
        case_ids = selected_case_ids(args, dataset)
        for case_id in case_ids:
            errors.extend(
                verify_case(workspace, dataset, find_case(dataset, case_id), warnings)
            )
    except (KeyError, ValueError) as exc:
        # KeyError renders its message with extra quotes; unwrap it.
        errors.append(exc.args[0] if exc.args else str(exc))

    if errors:
        print("OFFLINE EVAL FAILED")
        for error in errors:
            print(f"  - {error}")
        # Warnings are informational and do not affect pass/fail, but surface them
        # alongside failures for context.
        if warnings:
            print("Warnings:")
            for warning in warnings:
                print(f"  - {warning}")
        return 1

    print("OFFLINE EVAL PASSED")
    print(f"Verified cases: {', '.join(case_ids)}")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"  - {warning}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
