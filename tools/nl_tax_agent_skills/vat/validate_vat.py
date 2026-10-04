#!/usr/bin/env python3
"""Repository-only VAT identity, arithmetic, and content-review guards.

This grader checks prepared data. It performs no tax classification, workflow
routing, bookkeeping ingestion, or authenticated portal actions.
"""

from decimal import Decimal, InvalidOperation
import hashlib
from pathlib import Path
import re

import yaml


POLICY_PATH = Path(__file__).resolve().parents[3] / "plugins/nl-tax-agent-skills/skills/nl-tax-field-mapper/reference/field-map-rules.yaml"
POLICY = (yaml.safe_load(POLICY_PATH.read_text(encoding="utf-8")) or {}).get("vat")
if not isinstance(POLICY, dict):
    raise ValueError("Canonical field-map-rules.yaml lacks VAT policy")
VAT_WORKFLOWS = set(POLICY["workflows"])
VAT_YEARS = set(POLICY["tax_years"])
PERIOD_PATTERN = re.compile(POLICY["period_pattern"])
# ASCII digits only: a resume token must literally match the saved filename.
RESUME_PATTERN = re.compile(r"^(vat|vat_correction)_([0-9]{4})_(.+)$")
LIABILITY_IDS = tuple(f"vat.{rubric}.vat" for rubric in POLICY["liability_rubrics"])
TURNOVER_IDS = tuple(f"vat.{rubric}.turnover" for rubric in POLICY["turnover_rubrics"])
LIABILITY_TOTAL_ID = POLICY["liability_total_id"]
INPUT_TOTAL_ID = POLICY["input_total_id"]
BALANCE_ID = POLICY["balance_id"]
PREVIOUS_BALANCE_ID = POLICY["previous_balance_id"]
DELTA_ID = POLICY["correction_delta_id"]
TOTAL_IDS = {LIABILITY_TOTAL_ID, INPUT_TOTAL_ID, BALANCE_ID}
CORRECTION_IDS = {PREVIOUS_BALANCE_ID, DELTA_ID}
INTERNAL_IDS = set(POLICY["internal_ids"])
# Real suppletie form entries (vat_correction maps only), never internal totals.
SUPPLETIE_ENTRY_IDS = set(POLICY.get("suppletie_entry_ids") or [])
COVERAGE_PREFIX = POLICY.get("coverage_note_prefix", "vat_rubric_coverage:")
ROUTE_PREFIX = POLICY["correction_route_note_prefix"]
CORRECTION_ROUTES = tuple(POLICY["correction_routes"])
SUPPLETIE_ROUTE = POLICY["suppletie_route"]
REVIEW_BLOCKER = POLICY["source_review_blocker"]


def parse_resume_identity(workflow):
    match = RESUME_PATTERN.fullmatch(workflow) if isinstance(workflow, str) else None
    if not match:
        return None
    slug, year, period = match.groups()
    if int(year) not in VAT_YEARS or not PERIOD_PATTERN.fullmatch(period):
        return None
    return ("vat_correction" if slug == "vat_correction" else "vat_return", int(year), period)


def workpack_path(workflow, tax_year, period):
    if workflow not in VAT_WORKFLOWS or tax_year not in VAT_YEARS or isinstance(tax_year, bool):
        return None
    if not isinstance(period, str) or not PERIOD_PATTERN.fullmatch(period):
        return None
    slug = "vat-correction" if workflow == "vat_correction" else "vat"
    return f"workspace/nl-tax-{slug}-{tax_year}-{period}-workpack.md"


def whole_euros(value):
    """Exact numeric entry, without silently parsing locale or rounded text."""
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        return None
    try:
        amount = Decimal(str(value))
    except InvalidOperation:
        return None
    return amount if amount.is_finite() and amount == amount.to_integral_value() else None


def correction_routes(notes):
    """Return every declared ``vat_correction_route:`` value from map notes."""
    notes = notes if isinstance(notes, list) else []
    return [
        note[len(ROUTE_PREFIX):].strip()
        for note in notes
        if isinstance(note, str) and note.startswith(ROUTE_PREFIX)
    ]


def correction_route_errors(notes, fields):
    """A correction map names one route; only a suppletie maps previous_balance."""
    routes = correction_routes(notes)
    allowed = "|".join(CORRECTION_ROUTES)
    if not routes:
        return [f"vat_correction map must declare {ROUTE_PREFIX} {allowed} in notes"]
    if len(routes) > 1:
        return [f"vat_correction map declares more than one {ROUTE_PREFIX} note"]
    route = routes[0]
    if route not in CORRECTION_ROUTES:
        return [f"Invalid {ROUTE_PREFIX} {route!r}; use one of {allowed}"]
    mapped = {field.get("field_id") for field in fields if isinstance(field, dict)}
    if route != SUPPLETIE_ROUTE and mapped & SUPPLETIE_ENTRY_IDS:
        return [
            f"{PREVIOUS_BALANCE_ID} is a suppletie-only entry row; the {route} route maps no "
            "'Totaalbedrag eerdere btw-aangifte over dit tijdvak' row"
        ]
    return []


def validate_map(data):
    errors = []
    workflow = data.get("workflow")
    if workflow not in VAT_WORKFLOWS:
        return errors
    period = data.get("period")
    if not isinstance(period, str) or not PERIOD_PATTERN.fullmatch(period):
        errors.append("VAT period must be Q1..Q4, M01..M12, or Y")
    fields = data.get("fields") if isinstance(data.get("fields"), list) else []
    allowed = set(LIABILITY_IDS) | set(TURNOVER_IDS) | TOTAL_IDS
    if workflow == "vat_correction":
        allowed |= CORRECTION_IDS
    amounts = {}
    for field in fields:
        if not isinstance(field, dict):
            continue
        fid = field.get("field_id")
        if fid not in allowed:
            errors.append(f"Unsupported VAT rubric field_id: {fid}")
            continue
        if fid in INTERNAL_IDS and field.get("entry_mode") != "internal_routing":
            errors.append(f"{fid} is a calculation, never an established portal entry; use internal_routing")
        if fid in SUPPLETIE_ENTRY_IDS and field.get("entry_mode") == "internal_routing":
            errors.append(f"{fid} is the suppletie's 'Totaalbedrag eerdere btw-aangifte over dit tijdvak' entry row; never mark it internal_routing (map it only on the suppletie route)")
        value = field.get("value")
        if value is None:
            continue
        amount = whole_euros(value)
        if amount is None:
            errors.append(f"VAT entry {fid} must be a finite whole-euro number, never an automatic rounding assumption")
            continue
        amounts[fid] = amount
    if workflow == "vat_correction":
        errors.extend(correction_route_errors(data.get("notes"), fields))
    gaps = data.get("missing_fields") if isinstance(data.get("missing_fields"), list) else []
    for gap in gaps:
        if isinstance(gap, dict) and gap.get("field_id") not in allowed:
            errors.append(f"Unsupported VAT missing field_id: {gap.get('field_id')}")
    coverage = rubric_coverage(data.get("notes"))
    components = []
    for fid in LIABILITY_IDS:
        if fid in amounts:
            components.append(amounts[fid])
        elif fid not in {field.get("field_id") for field in fields if isinstance(field, dict)}:
            status, sourced = coverage.get(fid.split(".")[1], (None, False))
            if status == "not_applicable_sourced" and sourced:
                components.append(Decimal(0))
    if len(components) == len(LIABILITY_IDS) and LIABILITY_TOTAL_ID in amounts:
        total = sum(components, Decimal(0))
        if amounts[LIABILITY_TOTAL_ID] != total:
            errors.append(f"VAT 5a mismatch: expected {total}, got {amounts[LIABILITY_TOTAL_ID]}")
    if TOTAL_IDS <= amounts.keys():
        balance = amounts[LIABILITY_TOTAL_ID] - amounts[INPUT_TOTAL_ID]
        if amounts[BALANCE_ID] != balance:
            errors.append(f"VAT balance mismatch: expected 5a minus 5b = {balance}")
    correction_ids = CORRECTION_IDS | {BALANCE_ID}
    if workflow == "vat_correction" and correction_ids <= amounts.keys():
        delta = amounts[BALANCE_ID] - amounts[PREVIOUS_BALANCE_ID]
        if amounts[DELTA_ID] != delta:
            errors.append(f"VAT correction delta mismatch: expected revised balance minus previous balance = {delta}")
    return errors


# Provenance must open the note's remainder: a document evidence ID or a
# quoted chat statement (vat-field-map.md). A stray "U:" later in free text,
# such as "TODO: U: ask user", is not provenance.
COVERAGE_PROVENANCE = re.compile(r'\s*(?:F:ev_[0-9]{3,}\b|U:"[^"]+")')
DUPLICATE_STATUS = "duplicate"


def _parse_coverage(notes):
    result = {}
    duplicates = set()
    for note in notes if isinstance(notes, list) else []:
        if not isinstance(note, str) or not note.startswith(COVERAGE_PREFIX):
            continue
        match = re.match(r"\s*([1-5][a-e])\s*=\s*([a-z_]+)(?:;\s*(.*))?$", note[len(COVERAGE_PREFIX):])
        if match:
            rubric, status, provenance = match.groups()
            sourced = bool(provenance and COVERAGE_PROVENANCE.match(provenance))
            if rubric in result:
                duplicates.add(rubric)
            result[rubric] = (status, sourced)
    for rubric in duplicates:
        # A rubric declared twice is ambiguous: neither declaration counts.
        result[rubric] = (DUPLICATE_STATUS, False)
    return result, duplicates


def rubric_coverage(notes):
    return _parse_coverage(notes)[0]


def _rubric_of(field_id):
    match = re.fullmatch(r"vat\.([1-5][a-e])\.(?:turnover|vat)", field_id) if isinstance(field_id, str) else None
    return match.group(1) if match else None


def coverage_blockers(notes, fields=None, missing_fields=None):
    """Coverage gaps; with ``fields``, also cross-check declarations against rows.

    ``fields`` (and optionally ``missing_fields``) are the map's field dicts.
    An ``applicable_mapped`` rubric needs a mapped vat.<rubric>.* row (or a
    recorded gap row); a ``not_applicable_sourced`` rubric must not also carry
    a mapped row.
    """
    coverage, duplicates = _parse_coverage(notes)
    required = set(map(str, POLICY["turnover_rubrics"])) | {"5a", "5b"}
    unresolved = sorted(rubric for rubric in required if rubric not in duplicates and coverage.get(rubric, (None, False))[0] not in {"applicable_mapped", "not_applicable_sourced"})
    unsourced = sorted(rubric for rubric in required if coverage.get(rubric, (None, False))[0] == "not_applicable_sourced" and not coverage[rubric][1])
    blockers = (["VAT rubric coverage unresolved: " + ", ".join(unresolved)] if unresolved else []) + (["VAT inapplicable rubric has no provenance: " + ", ".join(unsourced)] if unsourced else [])
    if duplicates:
        blockers.append("VAT rubric coverage declared more than once: " + ", ".join(sorted(duplicates)))
    if fields is not None:
        mapped = {_rubric_of(field.get("field_id")) for field in fields if isinstance(field, dict)} - {None}
        gaps = {_rubric_of(gap.get("field_id")) for gap in (missing_fields or []) if isinstance(gap, dict)} - {None}
        unmapped = sorted(rubric for rubric, (status, _) in coverage.items() if status == "applicable_mapped" and rubric not in mapped | gaps)
        contradicted = sorted(rubric for rubric, (status, _) in coverage.items() if status == "not_applicable_sourced" and rubric in mapped)
        if unmapped:
            blockers.append("VAT rubric declared applicable_mapped has no mapped field: " + ", ".join(unmapped))
        if contradicted:
            blockers.append("VAT rubric declared not_applicable_sourced also has a mapped field: " + ", ".join(contradicted))
    return blockers


def review_blockers(plugin_root, workflow):
    """Fail closed on unreviewed VAT content; never promote a human review."""
    if workflow not in VAT_WORKFLOWS:
        return []
    root = Path(plugin_root)
    register_path = root / "skills/nl-tax-shared-resources/source-register.yaml"
    owner = "nl-tax-vat-correction" if workflow == "vat_correction" else "nl-tax-vat-return"
    try:
        register = yaml.safe_load(register_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError):
        return [f"{REVIEW_BLOCKER}: source register unavailable; human content review required"]
    sources = register.get("sources", []) if isinstance(register, dict) else []
    required = [source for source in sources if isinstance(source, dict) and owner in (source.get("mandatory_for") or [])]
    if not required:
        return [f"{REVIEW_BLOCKER}: source coverage not registered; human content review required"]
    blockers = []
    metadata_root = root.parent.parent / "tools/nl_tax_agent_skills/source_maintenance/metadata"
    for source in required:
        sid = source.get("id", "unknown")
        if source.get("content_stage") == "draft_only":
            blockers.append(f"{REVIEW_BLOCKER}: human review pending for {sid}")
            continue
        snapshot = root / str(source.get("snapshot_path") or "")
        try:
            body = snapshot.read_bytes()
            note = body.decode("utf-8")
            if not re.search(r"(?m)^review_status:\s*reviewed\s*$", note):
                raise ValueError("note not reviewed")
            relative = snapshot.parent.relative_to(root / "skills/nl-tax-shared-resources/knowledge")
            metadata_path = metadata_root / relative / "_snapshot-metadata.yaml"
            metadata = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
            entry = (metadata.get("sources") or {}).get(sid) or {}
            if entry.get("review_status") != "reviewed" or entry.get("reviewed_note_hash_sha256") != hashlib.sha256(body).hexdigest():
                raise ValueError("review metadata not verified")
        except (OSError, UnicodeError, ValueError, AttributeError, yaml.YAMLError):
            blockers.append(f"{REVIEW_BLOCKER}: review missing or inconsistent for {sid}")
    return blockers
