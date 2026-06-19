#!/usr/bin/env python3
"""Validate a field-map.yaml for correctness and policy compliance.

Usage:
    python3 validate_field_map.py <path-to-field-map.yaml>

Checks:
    - All required metadata fields present
    - No workflow mismatch (annual field in provisional map)
    - No credential/login/browser/submission fields
    - No BSN/IBAN data-entry field, and no stored BSN (elfproef) or NL IBAN value
    - Confidence values in range 0.0-1.0
    - Source types are valid (v1.1 schema: includes user_chat, assumption, unknown)
    - Per-source-type required fields are present
    - For provisional: no werkelijk rendement field
    - source.type = unknown rows are listed in missing_fields
"""

import os
import re
import sys
from pathlib import Path

VALID_SOURCE_TYPES = {
    "evidence",
    "user_chat",
    "estimate",
    "baseline",
    "calculated",
    "assumption",
    "unknown",
}
REFERENCE_DIR = Path(__file__).resolve().parents[1] / "reference"
SUPPORTED_WORKFLOW_YEARS = {
    ("annual_return", 2025): REFERENCE_DIR / "annual-field-map.md",
    ("provisional_assessment", 2026): REFERENCE_DIR / "provisional-field-map.md",
}
VALID_WORKFLOWS = {workflow for workflow, _ in SUPPORTED_WORKFLOW_YEARS}
CREDENTIAL_KEYWORDS = {
    "digid", "wachtwoord", "password", "inloggegevens",
    "username", "login", "credential", "secret", "pin",
}
# BSN and IBAN are the two highest-value Dutch identifiers and must never be
# stored as a data-entry field value. The portal pre-fills them; the field map
# lists BSN as a coverage placeholder in missing_fields (no value) only.
SENSITIVE_IDENTIFIER_KEYWORDS = {"bsn", "burgerservicenummer", "iban"}
_IBAN_VALUE_RE = re.compile(r"\bNL\d{2}[A-Z]{4}\d{10}\b", re.IGNORECASE)
_BSN_CANDIDATE_RE = re.compile(r"\b\d{9}\b")
PORTAL_AUTOMATION_KEYWORDS = {
    "browser", "session", "submit", "submission", "sign", "signature",
    "onderteken", "verzenden", "indienen",
}
# Catch every common spelling of "actual return" — Dutch and English, joined and
# space-separated — so a provisional field cannot smuggle werkelijk rendement past
# the box-3 fictitious-only guard via a clean field_id plus a prose label.
WERKELIJK_KEYWORDS = {
    "werkelijk", "werkelijk rendement", "werkelijk_rendement",
    "actual_return", "actual-return", "actual return",
    "actueel rendement", "echt rendement",
}


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    try:
        import yaml
    except ImportError:
        raise SystemExit(
            "PyYAML is required to run this validator "
            "(python3 -m pip install pyyaml). If PyYAML is unavailable on this host, "
            "validate the field map by hand per reference/mapping-principles.md."
        )
    return yaml.safe_load(content)


def _is_provisional(workflow):
    return workflow in {"provisional", "provisional_assessment"}


def _parse_tax_year(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def required_reference_fields(reference_path):
    required = set()
    headers = None

    with open(reference_path, "r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line.startswith("|") or not line.endswith("|"):
                headers = None
                continue

            cells = [cell.strip() for cell in line.strip("|").split("|")]
            normalized = [cell.lower() for cell in cells]
            if "field_id" in normalized and "required" in normalized:
                headers = normalized
                continue
            if headers is None or all(set(cell) <= {"-"} for cell in cells):
                continue
            if "field_id" not in headers or "required" not in headers:
                continue

            field_index = headers.index("field_id")
            required_index = headers.index("required")
            if len(cells) <= max(field_index, required_index):
                continue
            if cells[required_index].strip().lower() != "required":
                continue

            match = re.search(r"`([^`]+)`", cells[field_index])
            if match:
                required.add(match.group(1))

    return required


def validate_metadata(data, errors):
    workflow = data.get("workflow")
    tax_year = data.get("tax_year")
    parsed_tax_year = _parse_tax_year(tax_year)
    version = data.get("field_map_version")

    if not version:
        errors.append("Missing field_map_version")
    if not workflow:
        errors.append("Missing workflow")
    elif workflow not in VALID_WORKFLOWS:
        errors.append(f"Invalid workflow: {workflow}")
    if not tax_year:
        errors.append("Missing tax_year")
    elif parsed_tax_year is None:
        errors.append(f"Invalid tax_year: {tax_year}")
    if workflow and tax_year and (workflow, parsed_tax_year) not in SUPPORTED_WORKFLOW_YEARS:
        errors.append(
            f"Unsupported workflow/tax_year combination: {workflow} {tax_year}"
        )

    return workflow, parsed_tax_year


def validate_reference_coverage(workflow, parsed_tax_year, fields, missing, errors):
    field_ids = {field.get("field_id") for field in fields if field.get("field_id")}
    missing_field_ids = {m.get("field_id") for m in missing if m.get("field_id")}

    reference_path = SUPPORTED_WORKFLOW_YEARS.get((workflow, parsed_tax_year))
    if not reference_path:
        return missing_field_ids

    represented_field_ids = field_ids | missing_field_ids
    for required_field_id in sorted(
        required_reference_fields(reference_path) - represented_field_ids
    ):
        errors.append(
            "Required reference field not represented in fields or "
            f"missing_fields: {required_field_id}"
        )

    return missing_field_ids


def _passes_elfproef(digits):
    """True if a 9-digit string satisfies the Dutch BSN 11-test."""
    if len(digits) != 9 or not digits.isdigit():
        return False
    weights = [9, 8, 7, 6, 5, 4, 3, 2, -1]
    total = sum(int(d) * w for d, w in zip(digits, weights))
    return total % 11 == 0


def validate_sensitive_field_names(fid, label_lower, errors):
    fid_lower = fid.lower()
    for kw in CREDENTIAL_KEYWORDS:
        if kw in fid_lower or kw in label_lower:
            errors.append(f"Credential/login field detected: {fid}")
    for kw in SENSITIVE_IDENTIFIER_KEYWORDS:
        if kw in fid_lower or kw in label_lower:
            errors.append(
                "Sensitive identifier field detected (BSN/IBAN must never be a "
                f"data-entry field; list BSN in missing_fields without a value): {fid}"
            )
    for kw in PORTAL_AUTOMATION_KEYWORDS:
        if kw in fid_lower or kw in label_lower:
            errors.append(f"Browser/submission automation field detected: {fid}")


def validate_sensitive_field_values(fid, field, errors):
    """Reject a stored BSN (elfproef) or NL IBAN in the value or source.quote."""
    source = field.get("source", {})
    quote = source.get("quote") if isinstance(source, dict) else ""
    for text in (str(field.get("value") or ""), str(quote or "")):
        if _IBAN_VALUE_RE.search(text):
            errors.append(f"Sensitive identifier value (NL IBAN) must not be stored: {fid}")
        for candidate in _BSN_CANDIDATE_RE.findall(text):
            if _passes_elfproef(candidate):
                errors.append(f"Sensitive identifier value (BSN) must not be stored: {fid}")
                break


def validate_source(fid, field, missing_field_ids, errors, warnings):
    source = field.get("source", {})
    if not isinstance(source, dict):
        errors.append(f"Source for {fid} is not a mapping")
        return

    src_type = source.get("type")
    if not src_type:
        warnings.append(f"No source.type set for {fid}")
    elif src_type not in VALID_SOURCE_TYPES:
        errors.append(f"Invalid source.type for {fid}: {src_type}")
    elif src_type == "evidence" and not source.get("evidence_id"):
        errors.append(f"source.type=evidence requires evidence_id ({fid})")
    elif src_type == "user_chat":
        if not source.get("quote"):
            errors.append(f"source.type=user_chat requires source.quote ({fid})")
        if not source.get("stated_at"):
            warnings.append(f"source.type=user_chat without stated_at ({fid})")
    elif src_type == "assumption" and not source.get("assumption_id"):
        errors.append(f"source.type=assumption requires assumption_id ({fid})")
    elif src_type == "baseline" and not source.get("baseline_ref"):
        warnings.append(f"source.type=baseline without baseline_ref ({fid})")
    elif src_type == "calculated" and not source.get("calculated_from"):
        warnings.append(f"source.type=calculated without calculated_from ({fid})")
    elif src_type == "unknown":
        if field.get("value") not in (None, ""):
            errors.append(f"source.type=unknown must have null value ({fid})")
        if fid not in missing_field_ids:
            errors.append(f"source.type=unknown requires entry in missing_fields ({fid})")


def validate_field(field, index, workflow, missing_field_ids, errors, warnings):
    fid = field.get("field_id", f"field[{index}]")
    label_lower = (field.get("label") or "").lower()

    validate_sensitive_field_names(fid, label_lower, errors)
    validate_sensitive_field_values(fid, field, errors)

    confidence = field.get("confidence")
    if confidence is not None:
        if not isinstance(confidence, (int, float)) or isinstance(confidence, bool):
            errors.append(f"Confidence must be a number in [0,1] for {fid}: {confidence!r}")
        elif not (0.0 <= confidence <= 1.0):
            errors.append(f"Confidence out of range [0,1] for {fid}: {confidence}")

    validate_source(fid, field, missing_field_ids, errors, warnings)

    if _is_provisional(workflow):
        source = field.get("source", {})
        scanned_texts = [
            fid.lower(),
            label_lower,
            str(field.get("notes") or "").lower(),
            str(source.get("quote") or "").lower() if isinstance(source, dict) else "",
        ]
        for kw in WERKELIJK_KEYWORDS:
            if any(kw in text for text in scanned_texts):
                errors.append(
                    f"CRITICAL: werkelijk rendement field in provisional map: {fid}"
                )
                break

    if field.get("manual_review_required") is None:
        warnings.append(f"No manual_review_required set for {fid}")


def validate_missing_fields(missing, warnings):
    for m in missing:
        if not m.get("field_id") and not m.get("label"):
            warnings.append("Missing field entry without field_id or label")


def validate(data):
    errors = []
    warnings = []

    workflow, parsed_tax_year = validate_metadata(data, errors)
    fields = data.get("fields", []) or []
    missing = data.get("missing_fields", []) or []
    if not fields and not missing:
        errors.append("Field map must include at least one entry in fields or missing_fields")

    missing_field_ids = validate_reference_coverage(
        workflow, parsed_tax_year, fields, missing, errors
    )
    for index, field in enumerate(fields):
        validate_field(field, index, workflow, missing_field_ids, errors, warnings)
    validate_missing_fields(missing, warnings)

    return errors, warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_field_map.py <path-to-field-map.yaml>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.isfile(path):
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    data = load_yaml(path)
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
