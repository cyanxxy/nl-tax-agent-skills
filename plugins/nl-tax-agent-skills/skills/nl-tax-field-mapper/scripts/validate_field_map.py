#!/usr/bin/env python3
"""Validate a field-map.yaml for correctness and policy compliance.

Usage:
    python3 validate_field_map.py <path-to-field-map.yaml>

Checks:
    - All required metadata fields present
    - No workflow mismatch (annual field in provisional map)
    - No browser/submission (portal-automation) fields (the tool is prep-only)
    - Confidence values in range 0.0-1.0
    - Source types are valid (v1.1 schema: includes user_chat, assumption, unknown)
    - Per-source-type required fields are present
    - For provisional: no werkelijk rendement field
    - source.type = unknown rows are listed in missing_fields
    - Structural guards: root must be a mapping; fields/missing_fields must be lists;
      duplicate field_id detection; non-finite numeric values rejected
    - Readiness assessment: a map with zero populated fields is never reported as
      "No issues found." and surfaces an explicit NOT_READY_FOR_ENTRY summary

Exit codes:
    Default exit stays unchanged (nonzero only on errors). Pass --strict /
    --require-ready to also exit nonzero when the map is not ready for entry.
"""

import math
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
# BSN/IBAN are portal-prefilled identifiers the taxpayer confirms in the portal,
# so a field map intentionally omits them; they must not count against readiness
# as "unpopulated required fields". Used only by the readiness/coverage logic
# below (_is_identifier_field) — not as a data ban. Sensitive-data handling is the
# host's responsibility (see CLAUDE.md "Host execution model"), not the plugin's.
SENSITIVE_IDENTIFIER_KEYWORDS = {"bsn", "burgerservicenummer", "iban"}
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
# Top-level keys the schema knows about. Anything else is warned on so a typo'd
# key (e.g. "field" instead of "fields") doesn't silently drop data.
KNOWN_TOP_LEVEL_KEYS = {
    "field_map_version", "workflow", "tax_year", "created_at",
    "fields", "missing_fields", "notes", "readiness",
}
# Optional top-level readiness self-declaration (ME-30).
VALID_READINESS_VALUES = {"draft", "review_ready"}


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

    prefilled_field_ids = portal_prefilled_reference_fields(reference_path)
    represented_field_ids = field_ids | missing_field_ids
    for required_field_id in sorted(
        required_reference_fields(reference_path)
        - prefilled_field_ids
        - represented_field_ids
    ):
        errors.append(
            "Required reference field not represented in fields or "
            f"missing_fields: {required_field_id}"
        )

    return missing_field_ids


def validate_portal_automation_fields(fid, label_lower, errors):
    """Reject browser/login-automation or submission fields.

    The tool prepares a workpack for manual entry; it never logs in, signs, or
    submits, so a field that names a portal action is out of scope. This is a
    product-scope guard (prep-only), not a security control.
    """
    fid_lower = fid.lower()
    for kw in PORTAL_AUTOMATION_KEYWORDS:
        if kw in fid_lower or kw in label_lower:
            errors.append(f"Browser/submission automation field detected: {fid}")


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

    validate_portal_automation_fields(fid, label_lower, errors)

    value = field.get("value")
    if (
        isinstance(value, float)
        and not isinstance(value, bool)
        and not math.isfinite(value)
    ):
        errors.append(f"Non-finite numeric value (NaN/inf) for {fid}: {value!r}")

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


def _is_identifier_field(field_id):
    """True for BSN/IBAN-class identifiers that the portal pre-fills.

    These are intentionally left blank in the field map, so they must NOT count
    against readiness as "unpopulated required reference fields".
    """
    fid_lower = (field_id or "").lower()
    return any(kw in fid_lower for kw in SENSITIVE_IDENTIFIER_KEYWORDS)


def _has_usable_provenance(field):
    """A populated field needs a concrete value AND a known, sourced provenance.

    Per ME-23, a value carried by a baseline/calculated source without its
    baseline_ref/calculated_from has no usable provenance and does not count as
    populated (even though the missing ref is only a warning by default).
    """
    value = field.get("value")
    if value is None or value == "":
        return False

    source = field.get("source", {})
    if not isinstance(source, dict):
        return False
    src_type = source.get("type")
    if src_type in (None, "", "unknown"):
        return False

    if src_type == "baseline" and not source.get("baseline_ref"):
        return False
    if src_type == "calculated" and not source.get("calculated_from"):
        return False

    return True


def portal_prefilled_reference_fields(reference_path):
    """Required reference fields the portal pre-fills (BRP / portal / VIA login).

    These are intentionally left blank in the field map (the taxpayer confirms them
    in the portal, they are not hand-entered from evidence), so they must not count
    against readiness. Detected from the reference table by a "pre-fill" / "not
    manually entered" marker in the row.
    """
    prefilled = set()
    headers = None
    try:
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
                if "field_id" not in headers:
                    continue
                field_index = headers.index("field_id")
                if len(cells) <= field_index:
                    continue
                match = re.search(r"`([^`]+)`", cells[field_index])
                if not match:
                    continue
                row_text = " ".join(normalized)
                if (
                    "pre-fill" in row_text
                    or "prefill" in row_text
                    or "vooringevuld" in row_text
                    or "vooraf ingevuld" in row_text
                    or "auto-fill" in row_text
                    or "not manually entered" in row_text
                ):
                    prefilled.add(match.group(1))
    except OSError:
        return set()
    return prefilled


def assess_readiness(fields, missing, workflow, parsed_tax_year):
    """Assess whether the field map is ready for manual portal entry.

    Returns a dict {ready, populated_count, required_unpopulated}:
      - populated_count: fields with a non-empty value AND usable provenance
        (source.type known/not unknown; baseline/calculated carry their ref).
      - required_unpopulated: required reference field_ids that are not populated,
        EXCLUDING BSN/IBAN-class identifiers (portal-prefilled, intentionally blank).
      - ready: at least one populated field AND no required reference field left
        unpopulated.
    """
    populated_ids = {
        field.get("field_id")
        for field in fields
        if isinstance(field, dict)
        and field.get("field_id")
        and _has_usable_provenance(field)
    }
    populated_count = sum(
        1 for field in fields if isinstance(field, dict) and _has_usable_provenance(field)
    )

    reference_path = SUPPORTED_WORKFLOW_YEARS.get((workflow, parsed_tax_year))
    required_unpopulated = []
    if reference_path:
        required = required_reference_fields(reference_path)
        prefilled = portal_prefilled_reference_fields(reference_path)
        required_unpopulated = sorted(
            rid
            for rid in required
            if rid not in populated_ids
            and not _is_identifier_field(rid)
            and rid not in prefilled
        )

    ready = populated_count > 0 and not required_unpopulated
    return {
        "ready": ready,
        "populated_count": populated_count,
        "required_unpopulated": required_unpopulated,
    }


def validate(data):
    errors = []
    warnings = []

    if not isinstance(data, dict):
        return (["Field map root must be a mapping"], [])

    for key in data:
        if key not in KNOWN_TOP_LEVEL_KEYS:
            warnings.append(f"Unknown top-level key: {key}")

    workflow, parsed_tax_year = validate_metadata(data, errors)

    readiness_decl = data.get("readiness")
    if readiness_decl is not None and readiness_decl not in VALID_READINESS_VALUES:
        errors.append(f"Invalid readiness value: {readiness_decl}")

    fields = data.get("fields", []) or []
    if not isinstance(fields, list):
        errors.append("fields must be a list")
        fields = []
    missing = data.get("missing_fields", []) or []
    if not isinstance(missing, list):
        errors.append("missing_fields must be a list")
        missing = []
    if not fields and not missing:
        errors.append("Field map must include at least one entry in fields or missing_fields")

    clean_fields = []
    for index, field in enumerate(fields):
        if not isinstance(field, dict):
            errors.append(f"fields[{index}] must be a mapping")
            continue
        clean_fields.append(field)

    seen_field_ids = set()
    for field in clean_fields:
        fid = field.get("field_id")
        if fid:
            if fid in seen_field_ids:
                errors.append(f"Duplicate field_id: {fid}")
            seen_field_ids.add(fid)

    clean_missing = [m for m in missing if isinstance(m, dict)]
    for index, m in enumerate(missing):
        if not isinstance(m, dict):
            errors.append(f"missing_fields[{index}] must be a mapping")

    missing_field_ids = validate_reference_coverage(
        workflow, parsed_tax_year, clean_fields, clean_missing, errors
    )
    for index, field in enumerate(clean_fields):
        validate_field(field, index, workflow, missing_field_ids, errors, warnings)
    validate_missing_fields(clean_missing, warnings)

    readiness = assess_readiness(clean_fields, clean_missing, workflow, parsed_tax_year)
    if readiness_decl == "review_ready" and not readiness["ready"]:
        warnings.append(
            "readiness declared review_ready but assess_readiness says NOT ready "
            f"(populated_count={readiness['populated_count']}, "
            f"required_unpopulated={len(readiness['required_unpopulated'])})"
        )

    return errors, warnings


def _readiness_for(data):
    """Recompute readiness for output in main() without changing validate()'s
    2-tuple contract (the test suite asserts on validate()'s return shape)."""
    if not isinstance(data, dict):
        return {"ready": False, "populated_count": 0, "required_unpopulated": []}
    workflow, parsed_tax_year = data.get("workflow"), _parse_tax_year(data.get("tax_year"))
    fields = data.get("fields", []) or []
    fields = [f for f in fields if isinstance(f, dict)] if isinstance(fields, list) else []
    missing = data.get("missing_fields", []) or []
    missing = [m for m in missing if isinstance(m, dict)] if isinstance(missing, list) else []
    return assess_readiness(fields, missing, workflow, parsed_tax_year)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    flags = {a for a in sys.argv[1:] if a.startswith("-")}
    require_ready = bool(flags & {"--require-ready", "--strict"})

    if not args:
        print("Usage: python3 validate_field_map.py [--strict|--require-ready] "
              "<path-to-field-map.yaml>", file=sys.stderr)
        sys.exit(1)

    path = args[0]
    if not os.path.isfile(path):
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    data = load_yaml(path)
    errors, warnings = validate(data)
    readiness = _readiness_for(data)

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
    if readiness["ready"]:
        print(
            f"READINESS: READY_FOR_ENTRY "
            f"(populated_count={readiness['populated_count']})"
        )
    else:
        print(
            f"READINESS: NOT_READY_FOR_ENTRY "
            f"(populated_count={readiness['populated_count']}, "
            f"required_unpopulated={len(readiness['required_unpopulated'])})"
        )
        for rid in readiness["required_unpopulated"]:
            print(f"  - required field unpopulated: {rid}")

    if not errors and not warnings and readiness["ready"]:
        print("No issues found.")

    exit_code = 0
    if errors:
        exit_code = 1
    elif require_ready and not readiness["ready"]:
        exit_code = 1
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
