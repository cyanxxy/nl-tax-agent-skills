#!/usr/bin/env python3
"""Validate a field-map.yaml for correctness and policy compliance.

Usage:
    python validate_field_map.py <path-to-field-map.yaml>

Checks:
    - All required metadata fields present
    - No workflow mismatch (annual field in provisional map)
    - No credential/login/browser/submission fields
    - Confidence values in range 0.0-1.0
    - Source types are valid (v1.1 schema: includes user_chat, assumption, unknown)
    - Per-source-type required fields are present
    - For provisional: no werkelijk rendement field
    - source.type = unknown rows are listed in missing_fields
"""

import json
import os
import sys

VALID_SOURCE_TYPES = {
    "evidence",
    "user_chat",
    "estimate",
    "baseline",
    "calculated",
    "assumption",
    "unknown",
}
VALID_WORKFLOWS = {
    "annual",
    "provisional",
    "annual_return",
    "provisional_assessment",
}
CREDENTIAL_KEYWORDS = {
    "digid", "wachtwoord", "password", "inloggegevens",
    "username", "login", "credential", "secret", "pin",
}
PORTAL_AUTOMATION_KEYWORDS = {
    "browser", "session", "submit", "submission", "sign", "signature",
    "onderteken", "verzenden", "indienen",
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


def _is_provisional(workflow):
    return workflow in {"provisional", "provisional_assessment"}


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

    fields = data.get("fields", []) or []
    missing = data.get("missing_fields", []) or []
    missing_field_ids = {m.get("field_id") for m in missing if m.get("field_id")}

    for i, field in enumerate(fields):
        fid = field.get("field_id", f"field[{i}]")

        # Credential and portal-automation checks
        fid_lower = fid.lower()
        label_lower = (field.get("label") or "").lower()
        for kw in CREDENTIAL_KEYWORDS:
            if kw in fid_lower or kw in label_lower:
                errors.append(f"Credential/login field detected: {fid}")
        for kw in PORTAL_AUTOMATION_KEYWORDS:
            if kw in fid_lower or kw in label_lower:
                errors.append(f"Browser/submission automation field detected: {fid}")

        # Confidence range
        confidence = field.get("confidence")
        if confidence is not None:
            if not (0.0 <= confidence <= 1.0):
                errors.append(f"Confidence out of range [0,1] for {fid}: {confidence}")

        # Source type and per-type required fields
        source = field.get("source", {})
        if not isinstance(source, dict):
            errors.append(f"Source for {fid} is not a mapping")
        else:
            src_type = source.get("type")
            if not src_type:
                warnings.append(f"No source.type set for {fid}")
            elif src_type not in VALID_SOURCE_TYPES:
                errors.append(f"Invalid source.type for {fid}: {src_type}")
            else:
                if src_type == "evidence" and not source.get("evidence_id"):
                    errors.append(
                        f"source.type=evidence requires evidence_id ({fid})"
                    )
                if src_type == "user_chat":
                    if not source.get("quote"):
                        errors.append(
                            f"source.type=user_chat requires source.quote ({fid})"
                        )
                    if not source.get("stated_at"):
                        warnings.append(
                            f"source.type=user_chat without stated_at ({fid})"
                        )
                if src_type == "assumption" and not source.get("assumption_id"):
                    errors.append(
                        f"source.type=assumption requires assumption_id ({fid})"
                    )
                if src_type == "baseline" and not source.get("baseline_ref"):
                    warnings.append(
                        f"source.type=baseline without baseline_ref ({fid})"
                    )
                if src_type == "calculated" and not source.get("calculated_from"):
                    warnings.append(
                        f"source.type=calculated without calculated_from ({fid})"
                    )
                if src_type == "unknown":
                    if field.get("value") not in (None, ""):
                        errors.append(
                            f"source.type=unknown must have null value ({fid})"
                        )
                    if fid not in missing_field_ids:
                        errors.append(
                            f"source.type=unknown requires entry in missing_fields ({fid})"
                        )

        # Provisional: no werkelijk rendement
        if _is_provisional(workflow):
            for kw in WERKELIJK_KEYWORDS:
                if kw in fid_lower or kw in label_lower:
                    errors.append(
                        f"CRITICAL: werkelijk rendement field in provisional map: {fid}"
                    )

        # Manual review flag
        if field.get("manual_review_required") is None:
            warnings.append(f"No manual_review_required set for {fid}")

    # Missing fields section sanity
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
