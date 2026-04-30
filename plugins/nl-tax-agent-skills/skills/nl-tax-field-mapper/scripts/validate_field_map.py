#!/usr/bin/env python3
"""Validate a field-map.yaml for correctness and policy compliance.

Usage:
    python validate_field_map.py <path-to-field-map.yaml>

Checks:
    - All required metadata fields present
    - No workflow mismatch (annual field in provisional map)
    - No credential/login fields
    - Confidence values in range 0.0-1.0
    - Source types are valid
    - For provisional: no werkelijk rendement field
"""

import json
import os
import sys

VALID_SOURCE_TYPES = {"evidence", "estimate", "baseline", "calculated"}
VALID_WORKFLOWS = {"annual_return", "provisional_assessment"}
CREDENTIAL_KEYWORDS = {
    "digid", "wachtwoord", "password", "inloggegevens",
    "username", "login", "credential", "secret", "pin",
}
WERKELIJK_KEYWORDS = {"werkelijk", "actual_return", "actual-return", "werkelijk_rendement"}


def load_yaml_or_json(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    try:
        import yaml
        return yaml.safe_load(content)
    except ImportError:
        return json.loads(content)


def validate(data):
    errors = []
    warnings = []

    # Top-level metadata
    workflow = data.get("workflow")
    tax_year = data.get("tax_year")
    version = data.get("field_map_version")

    if not version:
        errors.append("Missing field_map_version")
    if not workflow:
        errors.append("Missing workflow")
    elif workflow not in VALID_WORKFLOWS:
        errors.append(f"Invalid workflow: {workflow}")
    if not tax_year:
        errors.append("Missing tax_year")

    fields = data.get("fields", [])

    for i, field in enumerate(fields):
        fid = field.get("field_id", f"field[{i}]")

        # Credential check
        fid_lower = fid.lower()
        label_lower = (field.get("label") or "").lower()
        for kw in CREDENTIAL_KEYWORDS:
            if kw in fid_lower or kw in label_lower:
                errors.append(f"Credential/login field detected: {fid}")

        # Confidence range
        confidence = field.get("confidence")
        if confidence is not None:
            if not (0.0 <= confidence <= 1.0):
                errors.append(f"Confidence out of range [0,1] for {fid}: {confidence}")

        # Source type
        source = field.get("source", {})
        if isinstance(source, dict):
            src_type = source.get("type")
            if src_type and src_type not in VALID_SOURCE_TYPES:
                errors.append(f"Invalid source type for {fid}: {src_type}")

        # Provisional: no werkelijk rendement
        if workflow == "provisional_assessment":
            for kw in WERKELIJK_KEYWORDS:
                if kw in fid_lower or kw in label_lower:
                    errors.append(
                        f"CRITICAL: werkelijk rendement field in provisional map: {fid}"
                    )

        # Manual review flag
        if field.get("manual_review_required") is None:
            warnings.append(f"No manual_review_required set for {fid}")

    # Missing fields section
    missing = data.get("missing_fields", [])
    for m in missing:
        if not m.get("field_id") and not m.get("label"):
            warnings.append("Missing field entry without field_id or label")

    return errors, warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_field_map.py <path-to-field-map.yaml>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.isfile(path):
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    data = load_yaml_or_json(path)
    errors, warnings = validate(data)

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

    if not errors and not warnings:
        print("No issues found.")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
