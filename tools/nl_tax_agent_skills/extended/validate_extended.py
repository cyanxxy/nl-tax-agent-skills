#!/usr/bin/env python3
"""Repository-only identity, field-shape and draft-ceiling checks.

This grader does not decide residence, VAT schemes, destinations, rates or
filing actions. The installed plugin supplies only declarative instructions.
"""

from calendar import monthrange
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
import re

import yaml


REPO_ROOT = Path(__file__).resolve().parents[3]
POLICY_PATH = REPO_ROOT / "plugins/nl-tax-agent-skills/skills/nl-tax-shared-resources/reference/workflow-scopes.yaml"
POLICY = yaml.safe_load(POLICY_PATH.read_text(encoding="utf-8"))
if not isinstance(POLICY, dict) or not isinstance(POLICY.get("scopes"), dict):
    raise ValueError("Canonical workflow-scopes.yaml lacks extension scopes")
SCOPES = POLICY["scopes"]
MAXIMUM_READINESS = POLICY.get("policy", {}).get("maximum_readiness", "draft")
if MAXIMUM_READINESS != "draft":
    raise ValueError("Extension policy cannot promote unreviewed scopes beyond draft")

PERIOD = re.compile(r"Q[1-4]|M(?:0[1-9]|1[0-2])|Y")
QUARTER = re.compile(r"Q[1-4]")
MONTH = re.compile(r"M(?:0[1-9]|1[0-2])")
ALIAS = r"[a-z][a-z0-9_]*"
# A lowercased VAT-ID shape (country prefix plus seven or more digits, e.g.
# de123456789, nl123456789b01, ie1234567wa) is an identifier, never an alias.
VAT_ID_LIKE = re.compile(r"[a-z]{0,3}[0-9]{7,}[0-9a-z]*")
FIELD_PATTERNS = {
    "icp": re.compile(rf"icp\.row\.{ALIAS}\.(?:goods_amount|services_amount|triangulation_amount)"),
    "oss": re.compile(rf"oss\.row\.{ALIAS}\.(?:taxable_base|vat_amount)"),
}
ISO_DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
COUNTRY = re.compile(r"[A-Z]{2}")
VAT_MEMBER_STATES = {"AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "EL", "ES", "FI", "FR", "HR", "HU", "IE", "IT", "LT", "LU", "LV", "MT", "NL", "PL", "PT", "RO", "SE", "SI", "SK"}
OSS_TOTAL = re.compile(r"oss\.total\.(?:(?:payable|refund)|(?:[a-z]{2})\.(?:current_vat|corrections|balance|payable|refund))")
FORBIDDEN_DIMENSION_KEYS = {
    "vat_id", "vat_number", "customer_vat_id", "ioss_number", "registration_number",
    "bsn", "iban", "invoice_number", "reference_number", "payment_reference",
    "customer_name", "customer_address",
}


def _year(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and re.fullmatch(r"[0-9]{4}", value):
        return int(value)
    return None


def _period_matches(kind, period, scheme=None):
    if not isinstance(period, str):
        return False
    if kind == "oss":
        if not isinstance(scheme, str):
            return False
        expression = MONTH if scheme == "ioss" else QUARTER if scheme in {"union", "non_union"} else None
        return bool(expression and expression.fullmatch(period))
    return bool(PERIOD.fullmatch(period))


def parse_resume_identity(workflow):
    """Return canonical extension identity or None; never normalize bad tokens."""
    if not isinstance(workflow, str):
        return None
    for kind, scope in SCOPES.items():
        match = re.fullmatch(scope["resume_pattern"], workflow)
        if not match:
            continue
        groups = match.groupdict()
        tax_year = _year(groups.get("tax_year"))
        if tax_year not in scope["tax_years"]:
            return None
        if kind in {"icp", "oss"} and not _period_matches(kind, groups.get("period"), groups.get("scheme")):
            return None
        return {"kind": kind, "tax_year": tax_year, **{key: groups[key] for key in scope.get("identity_keys", [])}}
    return None


def scope_for_map(data):
    """Identify a workflow/year pair even when period metadata is incomplete."""
    if not isinstance(data, dict):
        return None
    workflow, tax_year = data.get("workflow"), _year(data.get("tax_year"))
    for kind, scope in SCOPES.items():
        if workflow == scope["map_workflow"] and tax_year in scope["tax_years"]:
            return kind, scope
    return None


def _number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        return None
    try:
        amount = Decimal(str(value))
    except InvalidOperation:
        return None
    return amount if amount.is_finite() else None


def _valid_iso_date(value):
    if not isinstance(value, str) or not ISO_DATE.fullmatch(value):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def _cent_precision(value):
    digits, exponent = value.as_tuple().digits, value.as_tuple().exponent
    if exponent >= -2:
        return True
    # Inspect trailing digits instead of quantize(), which can overflow the
    # Decimal context for a maliciously large finite input.
    tail = min(len(digits), -exponent - 2)
    return all(digit == 0 for digit in digits[-tail:])


def _valid_field_id(kind, scope, fid):
    if not isinstance(fid, str):
        return False
    pattern = scope.get("field_id_pattern")
    if pattern:
        return bool(re.fullmatch(pattern, fid))
    if kind in FIELD_PATTERNS:
        return bool(FIELD_PATTERNS[kind].fullmatch(fid) or (kind == "oss" and OSS_TOTAL.fullmatch(fid)))
    prefix = scope.get("field_prefix")
    return bool(prefix and re.fullmatch(re.escape(prefix) + r"[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)*", fid))


ORIGINAL_PERIOD_SHAPE_ERROR = (
    "original_period must be earlier non-overlapping year_period metadata in the same scheme; OSS starts July 2021"
)
OSS_WINDOW_ERROR = "original_period outside the OSS three-year correction window; consumption-state route required"


def _period_bounds(year, token):
    if token == "Y":
        first, last = 1, 12
    elif token.startswith("Q"):
        first = (int(token[1]) - 1) * 3 + 1
        last = first + 2
    else:
        first = last = int(token[1:])
    return date(year, first, 1), date(year, last, monthrange(year, last)[1])


def _oss_correction_window_end(original_end):
    """Original due date (last day of the following month) plus three years."""
    due_year, due_month = (original_end.year + 1, 1) if original_end.month == 12 else (original_end.year, original_end.month + 1)
    due = date(due_year, due_month, monthrange(due_year, due_month)[1])
    end_year = due.year + 3
    # A 29 February due date has no anniversary in a common year: use 28 February.
    return date(end_year, due.month, min(due.day, monthrange(end_year, due.month)[1]))


def _original_period_error(value, kind, scheme, current_year, current_period):
    """Return None for valid correction metadata, otherwise the error text."""
    if not isinstance(value, str) or not isinstance(current_year, int) or not isinstance(current_period, str):
        return ORIGINAL_PERIOD_SHAPE_ERROR
    match = re.fullmatch(r"(20[0-9]{2})_(Q[1-4]|M(?:0[1-9]|1[0-2])|Y)", value)
    if not match:
        return ORIGINAL_PERIOD_SHAPE_ERROR
    year, period = int(match[1]), match[2]
    if not _period_matches(kind, period, scheme):
        return ORIGINAL_PERIOD_SHAPE_ERROR
    # ICP may change frequency, but a correction still needs earlier complete,
    # non-overlapping coverage. The owner's evidence establishes the assignment.
    original_start, original_end = _period_bounds(year, period)
    if kind == "oss" and original_start < date(2021, 7, 1):
        return ORIGINAL_PERIOD_SHAPE_ERROR
    current_start, current_end = _period_bounds(current_year, current_period)
    if not original_end < current_start:
        return ORIGINAL_PERIOD_SHAPE_ERROR
    # Historical metadata identifies filed evidence, not a supported historical
    # return. The OSS window runs from the original due date, never from the
    # original's actual filing date. A current return cannot be filed before
    # its period ends, so a period ending on or after the window end is
    # provably late (it can be filed at the earliest the day after it ends);
    # an earlier period end still needs the owner's check of the actual
    # submission date against the window end.
    if kind == "oss" and current_end >= _oss_correction_window_end(original_end):
        return OSS_WINDOW_ERROR
    return None


def _original_period(value, kind, scheme, current_year, current_period):
    return _original_period_error(value, kind, scheme, current_year, current_period) is None


def _dimensions_errors(field, data, kind):
    fid = field.get("field_id")
    dimensions = field.get("dimensions")
    errors = []
    if not isinstance(dimensions, dict):
        return [f"{fid}: {kind.upper()} row requires dimensions"]
    if any(key in FORBIDDEN_DIMENSION_KEYS for key in dimensions):
        errors.append(f"{fid}: full identifiers or personal identity dimensions are forbidden")
    member_state = dimensions.get("member_state")
    if not isinstance(member_state, str) or not COUNTRY.fullmatch(member_state):
        errors.append(f"{fid}: member_state must be a confirmed uppercase country code")
    elif member_state == "XI" and kind == "oss":
        if not (data.get("scheme") == "union" and dimensions.get("supply_kind") == "goods"):
            errors.append(f"{fid}: XI is valid only for Union-scheme goods (Northern Ireland distance sales of goods)")
    elif member_state not in VAT_MEMBER_STATES | ({"XI"} if kind == "icp" else set()):
        errors.append(f"{fid}: member_state must be an applicable EU VAT country code; use EL for Greece")
    elif kind == "icp" and member_state == "NL":
        errors.append(f"{fid}: domestic Netherlands customers are not ordinary ICP customers")
    original = dimensions.get("original_period")
    if original is not None:
        original_error = _original_period_error(original, kind, data.get("scheme"), _year(data.get("tax_year")), data.get("period"))
        if original_error:
            errors.append(f"{fid}: {original_error}")
    if kind == "icp":
        customer_alias = dimensions.get("customer_alias")
        row_alias = str(fid).split(".")[2] if str(fid).count(".") >= 3 else ""
        if (not isinstance(customer_alias, str) or not re.fullmatch(ALIAS, customer_alias)
                or VAT_ID_LIKE.fullmatch(customer_alias) or VAT_ID_LIKE.fullmatch(row_alias)):
            errors.append(f"{fid}: ICP row requires a customer_alias dimension (lowercase local alias, never an identifier)")
        if member_state == "XI" and str(fid).endswith("services_amount"):
            errors.append(f"{fid}: XI Northern Ireland treatment cannot be used for services")
        verification = dimensions.get("human_vat_id_verified")
        if verification is not None and not isinstance(verification, bool):
            errors.append(f"{fid}: human_vat_id_verified must be a Boolean, never an alias as verification")
        if verification is True and not _valid_iso_date(dimensions.get("human_vat_id_verified_at")):
            errors.append(f"{fid}: actual-ID verification needs a valid dated human confirmation")
    else:
        if dimensions.get("scheme") != data.get("scheme"):
            errors.append(f"{fid}: row scheme must match its OSS map")
        rate = _number(dimensions.get("rate"))
        if original is None and (rate is None or rate <= 0 or rate > 100):
            errors.append(f"{fid}: current OSS row needs a verified numeric rate greater than zero and at most 100")
        if original is not None and str(fid).endswith("taxable_base"):
            errors.append(f"{fid}: OSS earlier-period correction is a signed VAT delta, not a current taxable-base row")
        value = _number(field.get("value"))
        if original is None and value is not None and value < 0:
            errors.append(f"{fid}: current OSS supplies cannot be negative; use an original-period correction")
    return errors


def _oss_row_sums(fields):
    """Sum each country's current and correction VAT rows; flag incomplete countries."""
    current, corrections, incomplete = {}, {}, set()
    for field in fields:
        if not isinstance(field, dict):
            continue
        fid = field.get("field_id")
        if not isinstance(fid, str) or OSS_TOTAL.fullmatch(fid) or not fid.startswith("oss.row.") or not fid.endswith(".vat_amount"):
            continue
        dimensions = field.get("dimensions") if isinstance(field.get("dimensions"), dict) else {}
        member_state = dimensions.get("member_state")
        if not isinstance(member_state, str):
            continue
        country = member_state.lower()
        bucket = corrections if dimensions.get("original_period") is not None else current
        value = _number(field.get("value"))
        if value is None:
            # A draft gap: do not compare this country's totals with partial rows.
            incomplete.add(country)
            continue
        bucket[country] = bucket.get(country, Decimal(0)) + value
    return current, corrections, incomplete


def _xi_rows_are_union_goods(fields, scheme):
    for field in fields:
        dimensions = field.get("dimensions") if isinstance(field, dict) and isinstance(field.get("dimensions"), dict) else {}
        if dimensions.get("member_state") == "XI" and dimensions.get("supply_kind") != "goods":
            return False
    return scheme == "union"


def _oss_totals_errors(fields, scheme=None):
    totals = {field["field_id"]: _number(field.get("value")) for field in fields
              if isinstance(field, dict) and isinstance(field.get("field_id"), str)
              and OSS_TOTAL.fullmatch(field["field_id"])}
    errors, balances = [], {}
    countries = {fid.split(".")[2] for fid in totals if len(fid.split(".")) == 4}
    row_current, row_corrections, incomplete = _oss_row_sums(fields)
    # Every consumption state with oss.row VAT rows keeps its own totals once
    # any total exists; a country with rows but no totals would otherwise drop
    # out of the overall payable/refund tie-out.
    row_countries = set(row_current) | set(row_corrections) | incomplete
    if totals:
        for country in sorted(row_countries):
            for key in ("current_vat", "corrections", "balance"):
                if f"oss.total.{country}.{key}" not in totals:
                    errors.append(f"oss.total.{country}.{key} missing while oss.row VAT rows exist for {country.upper()}; every consumption state keeps its own totals")
        countries |= row_countries
    for country in sorted(countries):
        if country.upper() not in VAT_MEMBER_STATES and not (country == "xi" and _xi_rows_are_union_goods(fields, scheme)):
            errors.append(f"oss.total.{country}: unsupported consumption-state calculation")
        prefix = f"oss.total.{country}."
        current, corrections, balance = (totals.get(prefix + key) for key in ("current_vat", "corrections", "balance"))
        if country not in incomplete:
            for key, total, sums in (("current_vat", current, row_current), ("corrections", corrections, row_corrections)):
                if total is not None and total != sums.get(country, Decimal(0)):
                    errors.append(f"{prefix}{key} must equal this country's own oss.row VAT rows; never book another country's rows here")
        if current is not None and corrections is not None and balance is not None:
            if current + corrections != balance:
                errors.append(f"{prefix}balance mismatch: current VAT plus this country's corrections")
        if balance is not None:
            balances[country] = balance
            for key, expected in (("payable", max(Decimal(0), balance)), ("refund", max(Decimal(0), -balance))):
                if totals.get(prefix + key) is not None and totals[prefix + key] != expected:
                    errors.append(f"{prefix}{key} mismatch: do not net another country's balance")
    if countries and len(balances) == len(countries):
        for key, expected in (("payable", sum((max(Decimal(0), value) for value in balances.values()), Decimal(0))),
                              ("refund", sum((max(Decimal(0), -value) for value in balances.values()), Decimal(0)))):
            if totals.get("oss.total." + key) is not None and totals["oss.total." + key] != expected:
                errors.append(f"oss.total.{key} mismatch: positive payable and negative refund balances must remain separate")
    return errors


def validate_map(data):
    """Extension-specific checks; shared grader retains provenance/ownership checks."""
    if not isinstance(data, dict):
        return ["Extended field map must be a mapping"]
    matched = scope_for_map(data)
    if not matched:
        extension_workflows = {scope["map_workflow"] for kind, scope in SCOPES.items() if kind != "annual_2026"}
        if isinstance(data.get("workflow"), str) and data.get("workflow") in extension_workflows:
            return ["Unsupported extension workflow/tax_year pair"]
        return []
    kind, scope = matched
    errors = []
    if data.get("readiness") != MAXIMUM_READINESS:
        errors.append(f"{kind}: unreviewed extension must remain draft; review_ready is not supported")
    identity_ok = True
    if kind in {"icp", "oss"}:
        identity_ok = _period_matches(kind, data.get("period"), data.get("scheme"))
        if not identity_ok:
            errors.append(f"{kind}: invalid period/scheme identity")
    if kind == "international" and (not isinstance(data.get("return_form"), str) or data.get("return_form") not in {"migration", "nonresident"}):
        errors.append("international: return_form must be migration or nonresident")
    for identity_key in {"period", "scheme", "return_form"} - set(scope.get("identity_keys", [])):
        if identity_key in data:
            errors.append(f"{kind}: unexpected identity key {identity_key}")
    fields = data.get("fields")
    if not isinstance(fields, list):
        errors.append("Extended fields must be a list")
        fields = []
    seen = set()
    for field in fields:
        if not isinstance(field, dict):
            errors.append("Extended field row must be a mapping")
            continue
        fid = field.get("field_id")
        if not _valid_field_id(kind, scope, fid):
            errors.append(f"{kind}: unsupported field_id {fid}")
            continue
        if fid in seen:
            errors.append(f"{kind}: duplicate field_id {fid}")
        seen.add(fid)
        is_total = kind == "oss" and bool(OSS_TOTAL.fullmatch(fid))
        if is_total and field.get("entry_mode") != "internal_routing":
            errors.append(f"{fid}: calculated OSS totals must use internal_routing, never a portal entry")
        if scope.get("internal_only") and field.get("entry_mode") != "internal_routing":
            errors.append(f"{fid}: preparation-only facts must use internal_routing, never invented portal entries")
        if field.get("value") is not None and kind in {"icp", "oss"}:
            value = _number(field["value"])
            if value is None:
                errors.append(f"{fid}: amount must be a finite number, not text or Boolean")
            elif not _cent_precision(value):
                errors.append(f"{fid}: preserve confirmed cents; amount must not have more than two decimal places")
        if kind in {"icp", "oss"} and identity_ok and not is_total:
            errors.extend(_dimensions_errors(field, data, kind))
    gaps = data.get("missing_fields")
    if not isinstance(gaps, list):
        errors.append("Extended missing_fields must be a list")
        gaps = []
    for gap in gaps:
        if isinstance(gap, dict) and not _valid_field_id(kind, scope, gap.get("field_id")):
            errors.append(f"{kind}: unsupported missing field_id {gap.get('field_id')}")
    if kind == "oss":
        errors.extend(_oss_totals_errors(fields, data.get("scheme")))
    return errors


def review_readiness_blockers(data, plugin_root):
    """An agent/hash/URL can never lift the intentionally unreviewed draft ceiling."""
    matched = scope_for_map(data)
    if not matched:
        return []
    kind, scope = matched
    return [f"{scope['review_blocker']}: {kind} is draft-only; human tax-content and form-schema review remain required"]
