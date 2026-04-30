#!/usr/bin/env python3
"""Validate the source register for completeness and correctness.

Usage:
    python validate_source_register.py <path-to-source-register.yaml>

Checks:
    - All required fields present for each entry
    - No duplicate IDs
    - All snapshot_paths point to existing files
    - All URLs are on the allowlist
    - No entry has last_checked in the future
    - mandatory_for references valid skill names
"""

import json
import os
import sys
from datetime import date

REQUIRED_FIELDS = {
    "id", "title", "url", "source_type", "snapshot_path",
    "last_checked", "freshness_policy", "owner", "mandatory_for",
}

VALID_SKILL_NAMES = {
    "nl-tax-intake",
    "nl-tax-evidence-indexer",
    "nl-tax-annual-return",
    "nl-tax-provisional-assessment",
    "nl-tax-box1-home",
    "nl-tax-box3",
    "nl-tax-partner-deductions",
    "nl-tax-field-mapper",
    "nl-tax-submit-companion",
    "nl-tax-source-refresh",
}

ALLOWED_DOMAINS = {
    "belastingdienst.nl",
    "www.belastingdienst.nl",
    "over-ons.belastingdienst.nl",
    "odb.belastingdienst.nl",
    "wetten.overheid.nl",
    "regels.overheid.nl",
    "platform.claude.com",
    "code.claude.com",
}


def load_yaml_or_json(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    try:
        import yaml
        return yaml.safe_load(content)
    except ImportError:
        return json.loads(content)


def extract_domain(url):
    """Extract domain from URL without urllib."""
    url = url.replace("https://", "").replace("http://", "")
    return url.split("/")[0].split(":")[0]


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


def validate(register_path):
    errors = []
    warnings = []

    project_root = find_content_root(register_path)

    data = load_yaml_or_json(register_path)
    sources = data if isinstance(data, list) else data.get("sources", data.get("entries", []))

    if not sources:
        errors.append("Source register is empty or could not be parsed")
        return errors, warnings

    seen_ids = set()
    today = date.today().isoformat()

    for i, source in enumerate(sources):
        sid = source.get("id", f"entry[{i}]")

        # Required fields
        for field in REQUIRED_FIELDS:
            if field not in source or source[field] is None:
                errors.append(f"{sid}: missing required field '{field}'")

        # Duplicate IDs
        if sid in seen_ids:
            errors.append(f"Duplicate source ID: {sid}")
        seen_ids.add(sid)

        # Snapshot exists
        snapshot_path = source.get("snapshot_path", "")
        if snapshot_path:
            abs_path = os.path.join(project_root, snapshot_path)
            if not os.path.isfile(abs_path):
                warnings.append(f"{sid}: snapshot file not found: {snapshot_path}")

        # URL allowlist
        url = source.get("url", "")
        if url:
            domain = extract_domain(url)
            if domain not in ALLOWED_DOMAINS:
                errors.append(f"{sid}: URL domain not on allowlist: {domain}")

        # Future last_checked
        last_checked = source.get("last_checked", "")
        if last_checked and last_checked > today:
            errors.append(f"{sid}: last_checked is in the future: {last_checked}")

        # Valid skill references
        mandatory_for = source.get("mandatory_for", [])
        if isinstance(mandatory_for, list):
            for skill in mandatory_for:
                if skill not in VALID_SKILL_NAMES:
                    warnings.append(f"{sid}: unknown skill in mandatory_for: {skill}")

    return errors, warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_source_register.py <path-to-source-register.yaml>",
              file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.isfile(path):
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    errors, warnings = validate(path)

    if errors:
        print("VALIDATION FAILED")
        print()
        print("Errors:")
        for e in errors:
            print(f"  - {e}")
    else:
        print("VALIDATION PASSED")

    if warnings:
        print()
        print("Warnings:")
        for w in warnings:
            print(f"  - {w}")

    print()
    print(f"Total: {len(errors)} errors, {len(warnings)} warnings")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
