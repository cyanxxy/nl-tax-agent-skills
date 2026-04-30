#!/usr/bin/env python3
"""Validate knowledge pack against source register.

Usage:
    python validate_knowledge_pack.py <path-to-source-register.yaml>

Checks:
    - Every mandatory snapshot file exists
    - Every snapshot references a source_id from the register
    - Freshness thresholds are met
    - Knowledge files without source_id references are flagged
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
    result = []
    for root, _, files in os.walk(knowledge_dir):
        for f in files:
            if f.endswith(".md") and not f.startswith("_"):
                result.append(os.path.join(root, f))
    return result


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


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: python validate_knowledge_pack.py <path-to-source-register.yaml>",
            file=sys.stderr,
        )
        sys.exit(1)

    register_path = sys.argv[1]
    if not os.path.isfile(register_path):
        print(f"Error: file not found: {register_path}", file=sys.stderr)
        sys.exit(1)

    base_dir = os.path.dirname(os.path.abspath(register_path))
    project_root = find_content_root(register_path)
    knowledge_dir = os.path.join(base_dir, "knowledge")

    data = load_yaml_or_json(register_path)
    sources = data if isinstance(data, list) else data.get("sources", data.get("entries", []))

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

    # Find knowledge files and check source references
    unreferenced = []
    if os.path.isdir(knowledge_dir):
        knowledge_files = find_knowledge_files(knowledge_dir)
        for kf in knowledge_files:
            refs = extract_source_ids(kf)
            if not refs:
                rel_path = os.path.relpath(kf, project_root)
                unreferenced.append(rel_path)
            else:
                unknown = refs - registered_ids
                if unknown:
                    rel_path = os.path.relpath(kf, project_root)
                    for u in unknown:
                        print(f"  WARNING: {rel_path} references unknown source_id: {u}")

    # Report
    has_errors = bool(missing_snapshots)

    if missing_snapshots:
        print("MISSING SNAPSHOTS:")
        for s in missing_snapshots:
            print(f"  - {s}")
        print()

    if stale_sources:
        print("STALE SOURCES:")
        for sid, reason in stale_sources:
            print(f"  - {sid}: {reason}")
        print()

    if unreferenced:
        print("KNOWLEDGE FILES WITHOUT SOURCE REFERENCES:")
        for f in unreferenced:
            print(f"  - {f}")
        print()

    total_sources = len(sources)
    print(f"Summary: {total_sources} sources, "
          f"{len(missing_snapshots)} missing, "
          f"{len(stale_sources)} stale, "
          f"{len(unreferenced)} unreferenced files")

    if not has_errors and not stale_sources:
        print("VALIDATION PASSED")
    elif has_errors:
        print("VALIDATION FAILED")
    else:
        print("VALIDATION PASSED WITH WARNINGS")

    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
