#!/usr/bin/env python3
"""Validate the source register for completeness and correctness.

Usage:
    python3 validate_source_register.py <path-to-source-register.yaml>

Checks:
    - All required fields present for each entry
    - No duplicate IDs
    - All snapshot_paths point to existing files (error if missing)
    - All URLs use https, carry no embedded credentials, and are on the allowlist
    - No entry has last_checked in the future
    - mandatory_for references valid skill names (error if unknown)
    - draft_only entries record agent research only (last_checked_kind:
      agent_source_research, last_human_reviewed: null); promoted entries
      cannot rest on agent research and need an ISO last_human_reviewed date
"""

import os
import sys
from datetime import date
from urllib.parse import urlparse

REQUIRED_FIELDS = {
    "id", "title", "url", "source_type", "snapshot_path",
    "last_checked", "freshness_policy", "owner", "mandatory_for",
}

VALID_SKILL_NAMES = {
    "nl-tax-shared-resources",
    "nl-tax-intake",
    "nl-tax-knowledge",
    "nl-tax-annual-return",
    "nl-tax-provisional-assessment",
    "nl-tax-box1-home",
    "nl-tax-box2",
    "nl-tax-box3",
    "nl-tax-winst",
    "nl-tax-partner-deductions",
    "nl-tax-field-mapper",
    "nl-tax-submit-companion",
    "nl-tax-vat-return",
    "nl-tax-vat-correction",
    "nl-tax-vat-adjustments",
    "nl-tax-icp",
    "nl-tax-oss",
    "nl-tax-international-return",
    "nl-tax-annual-return-2026",
}

ALLOWED_DOMAINS = {
    "belastingdienst.nl",
    "www.belastingdienst.nl",
    "download.belastingdienst.nl",
    "stichtingenvereniging.belastingdienst.nl",
    "over-ons.belastingdienst.nl",
    "odb.belastingdienst.nl",
    "wetten.overheid.nl",
    "regels.overheid.nl",
    "platform.claude.com",
    "code.claude.com",
    "support.claude.com",
    "learn.chatgpt.com",
    "svb.nl",
    "www.svb.nl",
    "rijksoverheid.nl",
    "www.rijksoverheid.nl",
    "rvo.nl",
    "www.rvo.nl",
    "zoek.officielebekendmakingen.nl",
    "vat-one-stop-shop.ec.europa.eu",
    "eur-lex.europa.eu",
}


def load_yaml_or_json(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    try:
        import yaml
    except ImportError:
        raise SystemExit(
            "PyYAML is required to run this validator "
            "(python3 -m pip install pyyaml)."
        )
    try:
        return yaml.safe_load(content)
    except yaml.YAMLError as exc:
        raise SystemExit(f"Error: invalid YAML in {path}: {exc}")


def extract_domain(url):
    """Parse a URL into (scheme, hostname-lowercased, username).

    Uses urllib.parse so userinfo (user:pass@host) is split out rather than
    being treated as part of the host, and the scheme is exposed so callers can
    require https. Returns lowercased hostname (or "" if absent). Malformed
    URLs (e.g. an invalid IPv6 literal) parse as (\"\", \"\", None) instead of
    crashing the validator.
    """
    try:
        parsed = urlparse(url)
        scheme = (parsed.scheme or "").lower()
        hostname = (parsed.hostname or "").lower()
        username = parsed.username
    except ValueError:
        return "", "", None
    return scheme, hostname, username


def find_content_root(register_path):
    """Find the repo/plugin root that snapshot_path values are relative to.

    Register paths are serialized from this root (for example
    skills/nl-tax-shared-resources/knowledge/...), not from an individual skill directory where
    the same file may be referenced as nl-tax-shared-resources/knowledge/...
    """
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


# Workflow families added as draft_only extensions. Legacy income-tax entries
# carry no workflow_family and keep their own review-date history.
PROMOTION_REVIEW_FAMILIES = {"vat", "vat_cross_border", "international", "annual_2026"}


def provenance_errors(sid, source):
    """Keep agent research apart from human review attestation.

    A draft_only entry records agent public-source research only: it must say
    so (last_checked_kind: agent_source_research) and must carry
    last_human_reviewed: null, so no edit can fabricate a review. A promoted
    (non-draft) entry may keep these fields, but it cannot rest on agent
    research alone, and a recorded human review must be a real ISO date.
    """
    errors = []
    kind = source.get("last_checked_kind")
    if source.get("content_stage") == "draft_only":
        if kind != "agent_source_research":
            errors.append(
                f"{sid}: draft-only source must set last_checked_kind: agent_source_research"
            )
        if "last_human_reviewed" not in source or source.get("last_human_reviewed") is not None:
            errors.append(
                f"{sid}: draft-only source must carry last_human_reviewed: null "
                "(a real review is recorded only on promotion)"
            )
        return errors
    if kind == "agent_source_research":
        errors.append(f"{sid}: a non-draft source cannot rest on agent research only")
    family = source.get("workflow_family")
    if family in PROMOTION_REVIEW_FAMILIES and "last_human_reviewed" not in source:
        # Extension families start draft_only; promoting one (dropping
        # content_stage: draft_only) must record the actual human review date.
        errors.append(f"{sid}: promoted {family} source needs an ISO last_human_reviewed date")
    if "last_human_reviewed" in source:
        reviewed = source.get("last_human_reviewed")
        try:
            reviewed_date = date.fromisoformat(str(reviewed))
        except ValueError:
            errors.append(f"{sid}: promoted source needs an ISO last_human_reviewed date")
        else:
            if reviewed_date > date.today():
                errors.append(f"{sid}: last_human_reviewed is in the future: {reviewed}")
    return errors


def validate(register_path):
    errors = []
    warnings = []

    project_root = find_content_root(register_path)

    data = load_yaml_or_json(register_path)
    if isinstance(data, list):
        sources = data
    elif isinstance(data, dict):
        sources = data.get("sources", data.get("entries", []))
    else:
        sources = []

    if not sources:
        errors.append("Source register is empty or could not be parsed")
        return errors, warnings

    seen_ids = set()

    for i, source in enumerate(sources):
        if not isinstance(source, dict):
            errors.append(f"entry[{i}]: source entry must be a mapping, got: {source!r}")
            continue
        sid = source.get("id", f"entry[{i}]")
        if source.get("content_stage") not in {None, "draft_only"}:
            errors.append(f"{sid}: invalid content_stage (only explicit draft_only staging is supported)")
        if source.get("content_stage") == "draft_only" and source.get("workflow_family") not in {"vat", "vat_cross_border", "international", "annual_2026"}:
            errors.append(f"{sid}: draft-only source must declare a recognized isolated workflow_family")
        errors.extend(provenance_errors(sid, source))

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
                errors.append(f"{sid}: snapshot file not found: {snapshot_path}")

        # URL: require https, reject embedded credentials, enforce allowlist
        url = source.get("url", "")
        if url:
            scheme, hostname, username = extract_domain(url)
            if scheme != "https":
                errors.append(f"{sid}: URL scheme must be https, got: {scheme or '(none)'}")
            if username:
                errors.append(f"{sid}: URL must not contain embedded credentials")
            if hostname not in ALLOWED_DOMAINS:
                errors.append(f"{sid}: URL domain not on allowlist: {hostname}")

        # Future last_checked (parse to a date so an unquoted YAML date does not crash)
        last_checked = source.get("last_checked", "")
        if last_checked:
            try:
                checked_date = date.fromisoformat(str(last_checked))
            except ValueError:
                errors.append(f"{sid}: invalid last_checked date: {last_checked}")
            else:
                if checked_date > date.today():
                    errors.append(f"{sid}: last_checked is in the future: {last_checked}")

        # Valid skill references. Accept the string shorthand plan_source_refresh.py
        # accepts, so a typo'd skill name in string form is validated too.
        mandatory_for = source.get("mandatory_for", [])
        if isinstance(mandatory_for, str):
            mandatory_for = [mandatory_for]
        if isinstance(mandatory_for, list):
            for skill in mandatory_for:
                if skill not in VALID_SKILL_NAMES:
                    errors.append(f"{sid}: unknown skill in mandatory_for: {skill}")
        elif mandatory_for is not None:
            errors.append(
                f"{sid}: mandatory_for must be a list of skill names "
                f"(or a single name), got: {mandatory_for!r}"
            )

    return errors, warnings


def main():
    if "-h" in sys.argv[1:] or "--help" in sys.argv[1:]:
        print("validate_source_register.py — validate the source register schema and references")
        print("Usage: python3 validate_source_register.py <path-to-source-register.yaml>")
        sys.exit(0)

    if len(sys.argv) < 2:
        print("Usage: python3 validate_source_register.py <path-to-source-register.yaml>",
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
