#!/usr/bin/env python3
"""Verify generated workspaces for the offline NL tax benchmark dataset."""

from __future__ import annotations

import argparse
import glob
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
DEFAULT_DATASET = SCRIPT_DIR / "offline-dataset.yaml"


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
    return [Path(match) for match in glob.glob(str(workspace / pattern), recursive=True)]


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
        dirs[:] = [d for d in dirs if d not in {"__pycache__", ".git", ".plugin-eval"}]
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


def normalize_case_ids(raw: str) -> list[str]:
    case_ids: list[str] = []
    for line in raw.replace(",", "\n").splitlines():
        cleaned = line.strip()
        if not cleaned or cleaned.startswith("#"):
            continue
        if ":" in cleaned:
            cleaned = cleaned.split(":", 1)[1].strip()
        case_ids.extend(part.strip() for part in cleaned.split() if part.strip())
    return case_ids


def selected_case_ids(args: argparse.Namespace, dataset: dict[str, Any], workspace: Path) -> list[str]:
    if args.case:
        return args.case
    if args.all:
        return [case["id"] for case in dataset.get("cases", [])]

    marker = workspace / dataset.get("global", {}).get("case_marker", "workspace/eval/current-case.txt")
    if not marker.exists():
        raise ValueError(
            f"No case selected and marker not found: {marker}. "
            "Pass --case <id> or write the marker during the benchmark run."
        )
    case_ids = normalize_case_ids(read_text(marker))
    if not case_ids:
        raise ValueError(f"Case marker is empty: {marker}")
    return case_ids


def find_case(dataset: dict[str, Any], case_id: str) -> dict[str, Any]:
    for case in dataset.get("cases", []):
        if case.get("id") == case_id:
            return case
    raise KeyError(f"Unknown case id: {case_id}")


def contains(text: str, needle: str) -> bool:
    return needle.lower() in text.lower()


def check_text_rule(workspace: Path, case_id: str, rule: dict[str, Any], errors: list[str]) -> None:
    path = resolve_workspace_path(workspace, rule["path"])
    if not path.is_file():
        errors.append(f"{case_id}: text check file missing: {rule['path']}")
        return

    text = read_text(path)
    for needle in rule.get("all", []) or []:
        if not contains(text, str(needle)):
            errors.append(f"{case_id}: {rule['path']} missing required text: {needle!r}")

    for group in rule.get("any", []) or []:
        options = group if isinstance(group, list) else [group]
        if not any(contains(text, str(option)) for option in options):
            rendered = ", ".join(repr(str(option)) for option in options)
            errors.append(f"{case_id}: {rule['path']} missing one of: {rendered}")

    for needle in rule.get("none", []) or []:
        if contains(text, str(needle)):
            errors.append(f"{case_id}: {rule['path']} contains forbidden text: {needle!r}")


def check_generated_output_regex(
    workspace: Path,
    dataset: dict[str, Any],
    case_id: str,
    errors: list[str],
) -> None:
    global_config = dataset.get("global", {})
    output_root = workspace / global_config.get("generated_output_root", "workspace")
    patterns = global_config.get("forbidden_generated_output_regex", []) or []
    if not patterns:
        return

    compiled = [(pattern, re.compile(pattern)) for pattern in patterns]
    for path in iter_text_files(output_root):
        text = read_text(path)
        rel_path = path.relative_to(workspace)
        for pattern, regex in compiled:
            if regex.search(text):
                errors.append(f"{case_id}: {rel_path} matches forbidden generated-output regex: {pattern}")


def verify_case(workspace: Path, dataset: dict[str, Any], case: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    case_id = case["id"]

    for pattern in case.get("expected_files", []) or []:
        if not path_exists(workspace, pattern):
            errors.append(f"{case_id}: expected file missing: {pattern}")

    for pattern in case.get("forbidden_files", []) or []:
        matches = glob_matches(workspace, pattern) if has_glob(pattern) else []
        if not has_glob(pattern) and resolve_workspace_path(workspace, pattern).exists():
            matches = [resolve_workspace_path(workspace, pattern)]
        if matches:
            rel_matches = ", ".join(str(match.relative_to(workspace)) for match in matches[:5])
            errors.append(f"{case_id}: forbidden path exists for {pattern}: {rel_matches}")

    for rule in case.get("text_checks", []) or []:
        check_text_rule(workspace, case_id, rule, errors)

    check_generated_output_regex(workspace, dataset, case_id, errors)
    return errors


def validate_dataset_paths(dataset_path: Path, dataset: dict[str, Any]) -> list[str]:
    workspace_root = Path.cwd()
    plugin_root = workspace_root / dataset.get("global", {}).get("plugin_root", "plugins/nl-tax-agent-skills")
    errors: list[str] = []
    for case in dataset.get("cases", []) or []:
        fixture = case.get("fixture")
        if fixture and not (plugin_root / fixture).is_file():
            errors.append(f"{case.get('id', '<unknown>')}: fixture does not exist: {fixture}")
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

    try:
        case_ids = selected_case_ids(args, dataset, workspace)
        for case_id in case_ids:
            errors.extend(verify_case(workspace, dataset, find_case(dataset, case_id)))
    except (KeyError, ValueError) as exc:
        errors.append(str(exc))

    if errors:
        print("OFFLINE EVAL FAILED")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("OFFLINE EVAL PASSED")
    print(f"Verified cases: {', '.join(case_ids)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
