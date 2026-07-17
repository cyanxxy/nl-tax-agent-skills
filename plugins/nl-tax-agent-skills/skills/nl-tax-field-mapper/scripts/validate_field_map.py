#!/usr/bin/env python3
"""Validate a field-map.yaml for correctness and policy compliance.

Usage:
    python3 validate_field_map.py <path-to-field-map.yaml>

Checks:
    - All required metadata fields present
    - No workflow mismatch (annual field in provisional map)
    - No authenticated-portal action fields in fields or missing_fields
    - No browser-automation metadata keys in fields or missing_fields
    - Confidence values in range 0.0-1.0
    - Source types are valid (v1.1 schema: includes user_chat, assumption, unknown)
    - Per-source-type required fields are present
    - For provisional: no werkelijk rendement field
    - source.type = unknown rows are listed in missing_fields
    - Structural guards: root must be a mapping; fields/missing_fields must be lists;
      duplicate field_id detection; non-finite numeric values rejected
    - Structural readiness candidate: a false agent declaration is rejected, but
      the script never promotes an agent-declared draft to review-ready

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
# runtime contract's human-only portal boundary, regardless of host permissions.
SENSITIVE_IDENTIFIER_KEYWORDS = {"bsn", "burgerservicenummer", "iban"}
PORTAL_AUTOMATION_TERMS = (
    "browser",
    "chrome",
    "computer use",
    "computer control",
    "screen interaction",
    "screen control",
    "session",
    "authenticate",
    "authenticated",
    "authenticating",
    "authentication",
    "login",
    "log in",
    "logged in",
    "logging in",
    "log into",
    "logged into",
    "logging into",
    "inloggen",
    "digid",
    "form fill",
    "form filling",
    "form entry",
    "fill form",
    "invullen",
    "enter value",
    "enter values",
    "entered value",
    "entered values",
    "entering value",
    "entering values",
    "click",
    "clicking",
    "submit",
    "submitted",
    "submitting",
    "submission",
    "sign",
    "signed",
    "signing",
    "signature",
    "onderteken",
    "ondertekenen",
    "send",
    "sending",
    "sent",
    "verzenden",
    "indienen",
)
# These are metadata *key* tokens, not free-text action terms. Match them only
# as complete normalized tokens/phrases so ``selection`` and ``location`` stay
# valid while ``cssSelector``, ``DOM_locator``, and ``browser-locator`` do not.
PORTAL_AUTOMATION_METADATA_KEY_TERMS = (
    "css selector",
    "dom locator",
    "browser locator",
    "element locator",
    "selector",
    "selectors",
    "xpath",
    "x path",
    "locator",
    "locators",
)
# Catch every common spelling of "actual return" — Dutch and English, joined and
# space-separated — so a provisional field cannot smuggle werkelijk rendement past
# the box-3 fictitious-only guard via a clean field_id plus a prose label.
WERKELIJK_KEYWORDS = {
    "werkelijk", "werkelijk rendement", "werkelijk_rendement",
    "actual_return", "actual-return", "actual return",
    "actueel rendement", "echt rendement",
}
# Provisional 2026 has one dedicated business field. Every other onderneming
# field or entrepreneur-deduction term remains rejected.
PROVISIONAL_EXPECTED_PROFIT_FIELD = "onderneming.geschatte_winst"
PARTNER_ALLOCATION_TOKENS = {"allocation", "verdeling", "toedeling"}
ENTREPRENEUR_KEYWORDS = {
    "onderneming.", "zelfstandigenaftrek", "startersaftrek",
    "mkb-winstvrijstelling", "mkb_winstvrijstelling", "ondernemersaftrek",
    "investeringsaftrek", "kleinschaligheidsinvesteringsaftrek",
}
ENTREPRENEUR_DEDUCTION_KEYWORDS = ENTREPRENEUR_KEYWORDS - {"onderneming."}
ENTREPRENEUR_TOKEN_PATTERNS = (
    re.compile(r"\bkia\b"),
)
BUSINESS_PROFIT_PATTERNS = (
    re.compile(r"\bwinst[\s_.-]*uit[\s_.-]*onderneming\b"),
    re.compile(r"\bondernemings[\s_.-]*winst\b"),
    re.compile(r"\bbusiness[\s_.-]*(?:profit|income|earnings)\b"),
    re.compile(r"\benterprise[\s_.-]*(?:profit|income|earnings)\b"),
    re.compile(
        r"\bself[\s_.-]*(?:employment|employed)[\s_.-]*"
        r"(?:income|profit|earnings)\b"
    ),
)
# Top-level keys the schema knows about. Anything else is warned on so a typo'd
# key (e.g. "field" instead of "fields") doesn't silently drop data.
# Keep this set in sync with templates/field-map-template.yaml.
KNOWN_TOP_LEVEL_KEYS = {
    "field_map_version", "workflow", "tax_year", "created_at", "updated_at",
    "fields", "missing_fields", "user_chat_values_index", "notes", "readiness",
    "check_performed_by",
}
# Optional top-level readiness self-declaration (ME-30).
VALID_READINESS_VALUES = {"draft", "review_ready"}
VALID_CHECK_TRAILS = {"checked_by_script", "checked_by_agent"}

# Stable identifiers shared with the no-Python checklist in
# reference/mapping-principles.md. Keep the identifiers stable even if the
# implementation of an individual check evolves.
CHECK_IDS = (
    "FM-METADATA",
    "FM-WORKFLOW-YEAR",
    "FM-STRUCTURE",
    "FM-SOURCE",
    "FM-CONFIDENCE-FINITE",
    "FM-REFERENCE-COVERAGE",
    "FM-MISSING-STRUCTURE",
    "FM-PROVISIONAL-METHOD",
)


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
    try:
        return yaml.safe_load(content)
    except yaml.YAMLError as exc:
        raise SystemExit(f"Error: invalid YAML in {path}: {exc}")


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

    try:
        required_ids = required_reference_fields(reference_path)
    except OSError as exc:
        errors.append(
            f"Cannot read field reference {reference_path.name}: {exc} "
            "(reference coverage not checked)"
        )
        return missing_field_ids

    prefilled_field_ids = portal_prefilled_reference_fields(reference_path)
    represented_field_ids = field_ids | missing_field_ids
    for required_field_id in sorted(
        required_ids
        - prefilled_field_ids
        - represented_field_ids
    ):
        errors.append(
            "Required reference field not represented in fields or "
            f"missing_fields: {required_field_id}"
        )

    return missing_field_ids


def _normalized_action_text(value):
    """Normalize separators while preserving whole-token matching."""
    return re.sub(r"[^a-z0-9]+", " ", str(value or "").lower()).strip()


def _normalized_metadata_key(value):
    """Normalize snake/kebab/space/camel/Pascal-case metadata keys."""
    text = str(value or "")
    text = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", text)
    text = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", text)
    return _normalized_action_text(text)


def find_portal_automation_term(*values):
    """Return the first whole token/phrase naming a prohibited portal action."""
    normalized_values = [f" {_normalized_action_text(value)} " for value in values]
    for term in PORTAL_AUTOMATION_TERMS:
        normalized_term = _normalized_action_text(term)
        if any(f" {normalized_term} " in value for value in normalized_values):
            return term
    return None


def find_portal_automation_metadata_keys(value):
    """Return prohibited metadata key matches recursively as ``(term, path)``.

    A field-map row must contain tax values and provenance, never DOM/browser
    targeting hints. Recursion prevents an otherwise harmless wrapper mapping
    from hiding a selector or locator. A seen-set also makes YAML aliases safe.
    """
    matches = []
    seen = set()

    def visit(node, path):
        if not isinstance(node, (dict, list)):
            return
        node_id = id(node)
        if node_id in seen:
            return
        seen.add(node_id)

        if isinstance(node, dict):
            for key, nested in node.items():
                key_text = str(key)
                key_path = path + (key_text,)
                normalized_key = f" {_normalized_metadata_key(key)} "
                for term in PORTAL_AUTOMATION_METADATA_KEY_TERMS:
                    normalized_term = _normalized_action_text(term)
                    if f" {normalized_term} " in normalized_key:
                        matches.append((term, ".".join(key_path)))
                        break
                visit(nested, key_path)
        else:
            for index, nested in enumerate(node):
                visit(nested, path + (f"[{index}]",))

    visit(value, ())
    return matches


def is_partner_allocation_field_id(field_id):
    """Recognize partner-allocation IDs without relying on one spelling/order.

    Field IDs use a ``partner`` namespace. Within that namespace, an exact
    allocation token may appear before or after the tax concept, for example
    ``partner.verdeling_box3_grondslag``, ``partner.allocation_box3``, or
    ``partner.box3_allocation``. Exact normalized tokens avoid treating words
    such as ``reallocation`` as allocation fields.
    """
    tokens = _normalized_action_text(field_id).split()
    return bool(
        tokens
        and tokens[0] == "partner"
        and PARTNER_ALLOCATION_TOKENS.intersection(tokens[1:])
    )


def validate_portal_automation_fields(fid, texts, errors):
    """Reject browser/computer-use/login/form-entry/submission fields.

    The tool prepares a workpack for human-only manual entry. Authenticated
    portal actions remain outside product scope even when the host exposes a
    browser or computer-control capability.
    """
    term = find_portal_automation_term(*texts)
    if term:
        errors.append(
            f"Authenticated-portal action field detected ({term}): {fid}"
        )


def validate_portal_automation_metadata(row, fid, location, errors):
    """Reject DOM/browser targeting metadata anywhere inside a map row."""
    for term, key_path in find_portal_automation_metadata_keys(row):
        errors.append(
            "Authenticated-portal automation metadata key detected "
            f"({term}) in {location} for {fid}: {key_path}"
        )


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


def validate_user_chat_index(data, fields, errors, warnings):
    """Validate the optional chat-value cross-index and reject silent extra rows."""
    index = data.get("user_chat_values_index")
    if index is None:
        index = []
    if not isinstance(index, list):
        errors.append("user_chat_values_index must be a list")
        return

    indexed = {}
    for position, row in enumerate(index):
        if not isinstance(row, dict):
            errors.append(f"user_chat_values_index[{position}] must be a mapping")
            continue
        fid = row.get("field_id")
        if not isinstance(fid, str) or not fid.strip():
            errors.append(
                f"user_chat_values_index[{position}] requires a non-empty string field_id"
            )
            continue
        if fid in indexed:
            errors.append(f"Duplicate user_chat_values_index field_id: {fid}")
        indexed[fid] = row

    chat_fields = {}
    for field in fields:
        source = field.get("source")
        fid = field.get("field_id")
        if (
            isinstance(fid, str)
            and fid.strip()
            and isinstance(source, dict)
            and source.get("type") == "user_chat"
        ):
            chat_fields[fid] = field

    for fid in sorted(set(indexed) - set(chat_fields)):
        errors.append(f"user_chat_values_index contains no matching user_chat field: {fid}")
    for fid in sorted(set(chat_fields) - set(indexed)):
        message = f"user_chat field missing from user_chat_values_index: {fid}"
        if data.get("readiness") == "review_ready":
            errors.append(message)
        else:
            warnings.append(message)
    for fid in sorted(set(indexed) & set(chat_fields)):
        row = indexed[fid]
        field = chat_fields[fid]
        source = field.get("source", {})
        for key, expected in (
            ("value", field.get("value")),
            ("quote", source.get("quote")),
            ("stated_at", source.get("stated_at")),
        ):
            if row.get(key) != expected:
                errors.append(f"user_chat_values_index mismatch for {fid}: {key}")


def contains_entrepreneur_keyword(scanned_texts):
    return any(
        any(kw in text for kw in ENTREPRENEUR_KEYWORDS)
        or any(pattern.search(text) for pattern in ENTREPRENEUR_TOKEN_PATTERNS)
        for text in scanned_texts
    )


def contains_entrepreneur_deduction_keyword(scanned_texts):
    """Reject annual deduction concepts without rejecting the allowed field id."""
    return any(
        any(kw in text for kw in ENTREPRENEUR_DEDUCTION_KEYWORDS)
        or any(pattern.search(text) for pattern in ENTREPRENEUR_TOKEN_PATTERNS)
        for text in scanned_texts
    )


def contains_business_profit_indicator(scanned_texts):
    return any(
        pattern.search(text)
        for text in scanned_texts
        for pattern in BUSINESS_PROFIT_PATTERNS
    )


def validate_field(field, index, workflow, missing_field_ids, errors, warnings):
    raw_fid = field.get("field_id")
    if not isinstance(raw_fid, str) or not raw_fid.strip():
        errors.append(f"fields[{index}] requires a non-empty string field_id")
        fid = f"field[{index}]"
    else:
        fid = raw_fid
    label_lower = str(field.get("label") or "").lower()

    validate_portal_automation_fields(
        fid,
        (fid, label_lower, field.get("notes")),
        errors,
    )
    validate_portal_automation_metadata(field, fid, "fields", errors)

    value = field.get("value")
    if (
        workflow == "annual_return"
        and fid == "business.has_onderneming"
        and not isinstance(value, bool)
    ):
        errors.append(
            f"business.has_onderneming must be a real boolean ({value!r})"
        )
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

    if is_partner_allocation_field_id(fid):
        source = field.get("source", {})
        if not isinstance(source, dict) or source.get("type") != "user_chat":
            errors.append(
                "Partner allocation requires an explicit taxpayer choice with "
                f"user_chat provenance; leave it unresolved otherwise ({fid})"
            )
        if field.get("manual_review_required") is not True:
            errors.append(f"Partner allocation requires manual review ({fid})")

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
        if fid == PROVISIONAL_EXPECTED_PROFIT_FIELD:
            if contains_entrepreneur_deduction_keyword(scanned_texts):
                errors.append(
                    "CRITICAL: entrepreneur deduction content in provisional "
                    f"expected-profit field: {fid}"
                )
            if not isinstance(source, dict) or source.get("type") not in {
                "evidence", "user_chat", "baseline"
            }:
                errors.append(
                    f"Expected-profit field requires concrete provenance ({fid})"
                )
            elif source.get("type") == "user_chat" and (
                not source.get("quote") or not source.get("stated_at")
            ):
                errors.append(
                    f"Expected-profit user_chat provenance requires quote and stated_at ({fid})"
                )
            elif source.get("type") == "baseline" and not source.get("baseline_ref"):
                errors.append(
                    f"Expected-profit baseline provenance requires baseline_ref ({fid})"
                )
            elif source.get("type") == "evidence" and not source.get("evidence_id"):
                errors.append(
                    f"Expected-profit evidence provenance requires evidence_id ({fid})"
                )
            if field.get("manual_review_required") is not True:
                errors.append(
                    f"Expected-profit field requires manual review ({fid})"
                )
        elif contains_business_profit_indicator(scanned_texts):
            errors.append(
                "Business profit requires the dedicated expected-profit field "
                f"{PROVISIONAL_EXPECTED_PROFIT_FIELD}; do not substitute {fid}"
            )
        elif contains_entrepreneur_keyword(scanned_texts):
            errors.append(
                f"CRITICAL: entrepreneur (winst uit onderneming) deduction field "
                f"in provisional map: {fid} — winst deductions are annual 2025 only"
            )

    if field.get("manual_review_required") is None:
        warnings.append(f"No manual_review_required set for {fid}")


def validate_missing_fields(missing, workflow, errors, warnings):
    for m in missing:
        if not m.get("field_id") and not m.get("label"):
            warnings.append("Missing field entry without field_id or label")
        fid = m.get("field_id") or m.get("label") or "missing_fields entry"
        scanned_texts = [
            str(m.get("field_id") or "").lower(),
            str(m.get("label") or "").lower(),
            str(m.get("reason") or "").lower(),
            str(m.get("notes") or "").lower(),
        ]
        validate_portal_automation_fields(fid, scanned_texts, errors)
        validate_portal_automation_metadata(m, fid, "missing_fields", errors)
        if _is_provisional(workflow):
            # A missing_fields entry is an instruction to go COLLECT the data,
            # so the werkelijk-rendement ban applies here just as hard as it
            # does to populated fields.
            for kw in WERKELIJK_KEYWORDS:
                if any(kw in text for text in scanned_texts):
                    errors.append(
                        "CRITICAL: werkelijk rendement in provisional map "
                        f"missing_fields: {fid}"
                    )
                    break
            if (
                str(m.get("field_id") or "") == PROVISIONAL_EXPECTED_PROFIT_FIELD
                and contains_entrepreneur_deduction_keyword(scanned_texts)
            ):
                errors.append(
                    "CRITICAL: entrepreneur deduction content in provisional "
                    f"expected-profit missing field: {fid}"
                )
            elif (
                str(m.get("field_id") or "") != PROVISIONAL_EXPECTED_PROFIT_FIELD
                and contains_business_profit_indicator(scanned_texts)
            ):
                errors.append(
                    "Business profit requires the dedicated expected-profit field "
                    f"{PROVISIONAL_EXPECTED_PROFIT_FIELD}; do not substitute {fid}"
                )
            elif (
                str(m.get("field_id") or "") != PROVISIONAL_EXPECTED_PROFIT_FIELD
                and contains_entrepreneur_keyword(scanned_texts)
            ):
                errors.append(
                    "CRITICAL: entrepreneur (winst uit onderneming) deduction in "
                    f"provisional map missing_fields: {fid} — annual 2025 only"
                )


# Top-level notes MAY mention werkelijk rendement as an explanation/redirect
# ("Werkelijk rendement is not part of provisional 2026."). Only notes that
# lack such a negation are treated as collection instructions and rejected.
_WERKELIJK_NOTE_NEGATIONS = (
    "not part of",
    "no part of",
    "may become relevant",
    "niet van toepassing",
    "geen onderdeel",
)


def validate_top_level_notes(data, workflow, errors):
    """Scan top-level notes for werkelijk rendement in provisional maps."""
    if not _is_provisional(workflow):
        return
    notes = data.get("notes")
    if isinstance(notes, list):
        texts = [str(n).lower() for n in notes]
    elif notes is None:
        texts = []
    else:
        texts = [str(notes).lower()]
    for text in texts:
        if any(kw in text for kw in WERKELIJK_KEYWORDS) and not any(
            neg in text for neg in _WERKELIJK_NOTE_NEGATIONS
        ):
            errors.append(
                "CRITICAL: werkelijk rendement in provisional map top-level notes"
            )
            break


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
    """Assess whether map structure could support review-ready status.

    This mechanical candidate never overrides the agent declaration derived from
    session-progress.yaml. Returns
    {ready, populated_count, required_unpopulated, blockers}:
      - populated_count: fields with a non-empty value AND usable provenance
        (source.type known/not unknown; baseline/calculated carry their ref).
      - required_unpopulated: required reference field_ids that are not populated,
        EXCLUDING BSN/IBAN-class identifiers (portal-prefilled, intentionally blank).
      - blockers: workflow-specific manual-review blockers.
      - ready: at least one populated field, no required reference field left
        unpopulated, and no blocker.
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
        try:
            required = required_reference_fields(reference_path)
        except OSError:
            required = set()
        prefilled = portal_prefilled_reference_fields(reference_path)
        required_unpopulated = sorted(
            rid
            for rid in required
            if rid not in populated_ids
            and not _is_identifier_field(rid)
            and rid not in prefilled
        )

    blockers = []
    if workflow == "annual_return" and parsed_tax_year == 2025:
        has_annual_business = any(
            isinstance(field, dict)
            and (
                str(field.get("field_id") or "").startswith("onderneming.")
                or (
                    field.get("field_id") == "business.has_onderneming"
                    and field.get("value") is not False
                    and field.get("value") is not None
                )
            )
            for field in fields
        )
        if has_annual_business:
            blockers.append("business-section schema review")

    ready = populated_count > 0 and not required_unpopulated and not blockers
    return {
        "ready": ready,
        "populated_count": populated_count,
        "required_unpopulated": required_unpopulated,
        "blockers": blockers,
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

    check_trail = data.get("check_performed_by")
    if check_trail is None:
        errors.append("Missing required metadata: check_performed_by")
    elif check_trail not in VALID_CHECK_TRAILS:
        errors.append(
            "Invalid check_performed_by value: "
            f"{check_trail!r}; use checked_by_script or checked_by_agent"
        )

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
        if isinstance(fid, str) and fid.strip():
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
    validate_user_chat_index(data, clean_fields, errors, warnings)
    validate_missing_fields(clean_missing, workflow, errors, warnings)
    validate_top_level_notes(data, workflow, errors)

    readiness = assess_readiness(clean_fields, clean_missing, workflow, parsed_tax_year)
    if readiness_decl == "review_ready" and not readiness["ready"]:
        blocker_detail = (
            f", blockers={', '.join(readiness['blockers'])}"
            if readiness.get("blockers")
            else ""
        )
        errors.append(
            "readiness declared review_ready but assess_readiness says NOT ready "
            f"(populated_count={readiness['populated_count']}, "
            f"required_unpopulated={len(readiness['required_unpopulated'])}"
            f"{blocker_detail})"
        )

    return errors, warnings


def _readiness_for(data):
    """Combine authoritative agent declaration with mechanical eligibility."""
    if not isinstance(data, dict):
        return {
            "ready": False,
            "declared": None,
            "structurally_ready": False,
            "populated_count": 0,
            "required_unpopulated": [],
            "blockers": [],
        }
    workflow, parsed_tax_year = data.get("workflow"), _parse_tax_year(data.get("tax_year"))
    fields = data.get("fields", []) or []
    fields = [f for f in fields if isinstance(f, dict)] if isinstance(fields, list) else []
    missing = data.get("missing_fields", []) or []
    missing = [m for m in missing if isinstance(m, dict)] if isinstance(missing, list) else []
    result = assess_readiness(fields, missing, workflow, parsed_tax_year)
    structurally_ready = result["ready"]
    declared = data.get("readiness")
    result["declared"] = declared
    result["structurally_ready"] = structurally_ready
    result["ready"] = declared == "review_ready" and structurally_ready
    return result


def main():
    if "-h" in sys.argv[1:] or "--help" in sys.argv[1:]:
        print("validate_field_map.py — validate a field-map.yaml for correctness and policy")
        print("Usage: python3 validate_field_map.py [--strict|--require-ready] <path-to-field-map.yaml>")
        sys.exit(0)

    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    flags = {a for a in sys.argv[1:] if a.startswith("-")}
    known_flags = {"--require-ready", "--strict"}
    unknown_flags = flags - known_flags
    if unknown_flags:
        # A typo'd --require-readi must not silently disable strict mode in CI.
        print(
            f"Error: unknown flag(s): {', '.join(sorted(unknown_flags))}. "
            "Known flags: --strict, --require-ready",
            file=sys.stderr,
        )
        sys.exit(1)
    require_ready = bool(flags & known_flags)

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
        print("CHECK_TRAIL: checked_by_script")

    if warnings:
        print()
        print("Warnings:")
        for w in warnings:
            print(f"  - {w}")

    print()
    if readiness["ready"]:
        print(
            f"READINESS: REVIEW_READY "
            f"(populated_count={readiness['populated_count']})"
        )
    elif readiness.get("declared") == "draft":
        print(
            f"READINESS: DRAFT (agent-declared, "
            f"structurally_ready={str(readiness['structurally_ready']).lower()}, "
            f"populated_count={readiness['populated_count']}, "
            f"required_unpopulated={len(readiness['required_unpopulated'])})"
        )
    else:
        print(
            f"READINESS: UNDECLARED_OR_BLOCKED "
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
