#!/usr/bin/env python3
"""Validate knowledge pack against source register.

Usage:
    python validate_knowledge_pack.py <path-to-source-register.yaml>

Checks:
    - Every mandatory snapshot file exists
    - Every snapshot references a source_id from the register
    - Freshness thresholds are met
    - Knowledge files without source_id references are flagged
    - Every source_id reference anywhere in skills/*.md is registered
    - Active reviewed knowledge files do not contain unverified-value markers
"""

import json
import os
import re
import sys
from datetime import date, timedelta


def load_yaml_or_json(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    try:
        import yaml
        return yaml.safe_load(content)
    except ImportError:
        return json.loads(content)


FRESHNESS_DAYS = {
    "refresh-before-1-dec-and-before-filing-season": 90,
    "refresh-annually": 365,
    "refresh-on-law-change": 365,
    "refresh-on-demand": 730,
}

VALID_KNOWLEDGE_WORKFLOWS = {"all", "annual_return", "provisional_assessment"}


REVIEW_BLOCKING_PATTERNS = [
    ("pending verification", re.compile(r"pending verification", re.IGNORECASE)),
    ("verify against", re.compile(r"verify against", re.IGNORECASE)),
    ("may differ from", re.compile(r"may differ from", re.IGNORECASE)),
    ("approximate marker", re.compile(r"\bapprox(?:imate|imately)?\b", re.IGNORECASE)),
    ("indicative marker", re.compile(r"\bindicative\b", re.IGNORECASE)),
    ("approximate EUR marker", re.compile(r"~\s*EUR", re.IGNORECASE)),
    ("approximate numeric marker", re.compile(r"~\s*\d+(?:[.,]\d+)?\s*%?")),
]


def check_freshness(last_checked, policy):
    if not last_checked:
        return True, "no last_checked date"
    threshold = FRESHNESS_DAYS.get(policy, 365)
    try:
        checked = date.fromisoformat(last_checked)
        age = (date.today() - checked).days
        if age > threshold:
            return True, f"last checked {age} days ago (threshold: {threshold})"
    except ValueError:
        return True, f"invalid date format: {last_checked}"
    return False, ""


def find_knowledge_files(knowledge_dir):
    """Find all .md files in the knowledge directory."""
    return find_markdown_files(knowledge_dir)


def find_markdown_files(root_dir):
    """Find all .md files under a directory."""
    result = []
    for root, _, files in os.walk(root_dir):
        for f in files:
            if f.endswith(".md") and not f.startswith("_"):
                result.append(os.path.join(root, f))
    return result


def find_reference_files(skills_dir):
    """Find .md files in skill reference directories."""
    result = []
    for root, _, files in os.walk(skills_dir):
        if os.path.basename(root) != "reference":
            continue
        for f in files:
            if f.endswith(".md") and not f.startswith("_"):
                result.append(os.path.join(root, f))
    return result


def is_relative_to(path, parent):
    """Return whether path is inside parent, without pathlib for Py3.8 compatibility."""
    try:
        os.path.relpath(path, parent)
        return os.path.commonpath([os.path.abspath(path), os.path.abspath(parent)]) == os.path.abspath(parent)
    except ValueError:
        return False


def find_content_root(register_path):
    """Find the root that snapshot_path values are relative to."""
    base_dir = os.path.dirname(os.path.abspath(register_path))
    candidates = [
        os.path.abspath(os.path.join(base_dir, "..", "..")),
        os.path.abspath(os.path.join(base_dir, "..", "..", "..")),
    ]

    for candidate in candidates:
        if (
            os.path.isdir(os.path.join(candidate, ".claude-plugin"))
            or os.path.isdir(os.path.join(candidate, ".codex-plugin"))
        ):
            return candidate

    for candidate in candidates:
        if (
            os.path.isdir(os.path.join(candidate, ".git"))
            or os.path.isfile(os.path.join(candidate, ".gitignore"))
        ):
            return candidate

    return candidates[-1]


def extract_source_ids(filepath):
    """Extract source_id references from a knowledge file, skipping code blocks."""
    ids = set()
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        in_code_block = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            match = re.match(r"source_ids?:\s*(.+)", stripped)
            if match:
                raw = match.group(1).strip()
                for sid in re.split(r"[,\s]+", raw):
                    sid = sid.strip().strip("-").strip().strip('"').strip("'")
                    if sid and not sid.startswith("#") and not sid.startswith("<"):
                        ids.add(sid)
    except (OSError, UnicodeDecodeError):
        pass
    return ids


def extract_metadata_value(filepath, key):
    """Extract a simple `key: value` metadata field from a markdown file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                if stripped.startswith("## "):
                    break
                match = re.match(rf"{re.escape(key)}:\s*(.+)", stripped)
                if match:
                    return match.group(1).strip().strip('"').strip("'")
    except (OSError, UnicodeDecodeError):
        pass
    return ""


def split_metadata_values(raw):
    """Split comma-separated metadata such as `workflow: annual_return, all`."""
    return [part.strip() for part in raw.split(",") if part.strip()]


def find_review_blocking_markers(filepath):
    """Find unverified-value markers that are not allowed in active reviewed files."""
    markers = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for lineno, line in enumerate(f, start=1):
                for label, pattern in REVIEW_BLOCKING_PATTERNS:
                    if pattern.search(line):
                        markers.append((lineno, label, line.strip()))
    except (OSError, UnicodeDecodeError):
        pass
    return markers


def parse_args(argv):
    if len(argv) < 2:
        print(
            "Usage: python validate_knowledge_pack.py <path-to-source-register.yaml>",
            file=sys.stderr,
        )
        sys.exit(1)

    register_path = argv[1]
    if not os.path.isfile(register_path):
        print(f"Error: file not found: {register_path}", file=sys.stderr)
        sys.exit(1)
    return register_path


def collect_source_status(sources, project_root):
    registered_ids = set()
    missing_snapshots = []
    stale_sources = []

    for source in sources:
        sid = source.get("id", "")
        registered_ids.add(sid)

        snapshot_path = source.get("snapshot_path", "")
        if snapshot_path:
            abs_path = os.path.join(project_root, snapshot_path)
            if not os.path.isfile(abs_path):
                missing_snapshots.append(sid)

        is_stale, reason = check_freshness(
            source.get("last_checked", ""),
            source.get("freshness_policy", "refresh-annually"),
        )
        if is_stale:
            stale_sources.append((sid, reason))

    return registered_ids, missing_snapshots, stale_sources


def collect_skill_source_reference_errors(skills_dir, project_root, registered_ids):
    source_reference_errors = []
    if not os.path.isdir(skills_dir):
        return source_reference_errors

    for mf in find_markdown_files(skills_dir):
        refs = extract_source_ids(mf)
        unknown = refs - registered_ids
        if unknown:
            rel_path = os.path.relpath(mf, project_root)
            for source_id in sorted(unknown):
                source_reference_errors.append((rel_path, source_id))
    return source_reference_errors


def source_backed_markdown_files(knowledge_dir, skills_dir):
    files = set(find_knowledge_files(knowledge_dir))
    if os.path.isdir(skills_dir):
        files.update(find_reference_files(skills_dir))
    return sorted(files)


def should_require_source_refs(filepath, knowledge_dir):
    status = extract_metadata_value(filepath, "status").lower()
    review_status = extract_metadata_value(filepath, "review_status").lower()
    return is_relative_to(filepath, knowledge_dir) or (
        status == "active" and review_status == "reviewed"
    )


def collect_knowledge_file_errors(knowledge_dir, skills_dir, project_root, registered_ids):
    unreferenced = []
    review_marker_errors = []
    workflow_metadata_errors = []

    if not os.path.isdir(knowledge_dir):
        return unreferenced, review_marker_errors, workflow_metadata_errors

    for kf in source_backed_markdown_files(knowledge_dir, skills_dir):
        refs = extract_source_ids(kf)
        rel_path = os.path.relpath(kf, project_root)
        if not refs:
            if should_require_source_refs(kf, knowledge_dir):
                unreferenced.append(rel_path)
        else:
            for source_id in refs - registered_ids:
                print(f"  WARNING: {rel_path} references unknown source_id: {source_id}")

        status = extract_metadata_value(kf, "status").lower()
        review_status = extract_metadata_value(kf, "review_status").lower()
        if status != "active" or review_status != "reviewed":
            continue

        workflow = extract_metadata_value(kf, "workflow")
        workflows = split_metadata_values(workflow) if workflow else []
        invalid_workflows = [
            wf for wf in workflows if wf not in VALID_KNOWLEDGE_WORKFLOWS
        ]
        if invalid_workflows:
            workflow_metadata_errors.append((rel_path, workflow))

        for lineno, label, text in find_review_blocking_markers(kf):
            review_marker_errors.append((rel_path, lineno, label, text))

    return unreferenced, review_marker_errors, workflow_metadata_errors


def print_section(title, rows, formatter):
    if not rows:
        return
    print(title)
    for row in rows:
        print(f"  - {formatter(row)}")
    print()


def print_report(
    sources,
    missing_snapshots,
    stale_sources,
    unreferenced,
    review_marker_errors,
    workflow_metadata_errors,
    source_reference_errors,
):
    print_section("MISSING SNAPSHOTS:", missing_snapshots, lambda source_id: source_id)
    print_section(
        "STALE SOURCES:",
        stale_sources,
        lambda row: f"{row[0]}: {row[1]}",
    )
    print_section("KNOWLEDGE FILES WITHOUT SOURCE REFERENCES:", unreferenced, lambda path: path)
    print_section(
        "ACTIVE REVIEWED FILES WITH UNVERIFIED-VALUE MARKERS:",
        review_marker_errors,
        lambda row: f"{row[0]}:{row[1]}: {row[2]}: {row[3]}",
    )
    print_section(
        "ACTIVE REVIEWED FILES WITH INVALID WORKFLOW METADATA:",
        workflow_metadata_errors,
        lambda row: f"{row[0]}: workflow: {row[1]}",
    )
    print_section(
        "SOURCE_ID REFERENCES NOT PRESENT IN SOURCE REGISTER:",
        source_reference_errors,
        lambda row: f"{row[0]}: source_id: {row[1]}",
    )

    print(f"Summary: {len(sources)} sources, "
          f"{len(missing_snapshots)} missing, "
          f"{len(stale_sources)} stale, "
          f"{len(unreferenced)} unreferenced files, "
          f"{len(review_marker_errors)} review marker errors, "
          f"{len(workflow_metadata_errors)} workflow metadata errors, "
          f"{len(source_reference_errors)} unknown source_id errors")


def main():
    register_path = parse_args(sys.argv)
    base_dir = os.path.dirname(os.path.abspath(register_path))
    project_root = find_content_root(register_path)
    knowledge_dir = os.path.join(base_dir, "knowledge")
    skills_dir = os.path.dirname(base_dir)

    data = load_yaml_or_json(register_path)
    sources = data if isinstance(data, list) else data.get("sources", data.get("entries", []))

    registered_ids, missing_snapshots, stale_sources = collect_source_status(
        sources,
        project_root,
    )
    source_reference_errors = collect_skill_source_reference_errors(
        skills_dir,
        project_root,
        registered_ids,
    )
    (
        unreferenced,
        review_marker_errors,
        workflow_metadata_errors,
    ) = collect_knowledge_file_errors(
        knowledge_dir,
        skills_dir,
        project_root,
        registered_ids,
    )

    has_errors = bool(
        missing_snapshots
        or review_marker_errors
        or workflow_metadata_errors
        or source_reference_errors
    )

    print_report(
        sources,
        missing_snapshots,
        stale_sources,
        unreferenced,
        review_marker_errors,
        workflow_metadata_errors,
        source_reference_errors,
    )

    if not has_errors and not stale_sources:
        print("VALIDATION PASSED")
    elif has_errors:
        print("VALIDATION FAILED")
    else:
        print("VALIDATION PASSED WITH WARNINGS")

    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
