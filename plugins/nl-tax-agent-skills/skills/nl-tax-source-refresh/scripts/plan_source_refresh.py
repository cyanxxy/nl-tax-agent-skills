#!/usr/bin/env python3
"""
NL Tax Source Refresh -- Plan Source Refresh

Reads source-register.yaml, filters by scope and year, checks freshness by
thresholding each source's last_checked date against STALENESS_DAYS keyed by
its source_type (not by the free-text freshness_policy prose), and reports
which sources need a manual refresh plan.

Usage:
    python3 plan_source_refresh.py <scope> [year] [--fetch]
    python3 plan_source_refresh.py annual
    python3 plan_source_refresh.py provisional 2026
    python3 plan_source_refresh.py box3 2025
    python3 plan_source_refresh.py all
    python3 plan_source_refresh.py all --fetch

Scope:
    annual       -- sources with workflow: annual_return
    provisional  -- sources with workflow: provisional_assessment
    box3         -- sources with IDs containing 'box3'
    all          -- every source in the register

The --fetch flag is accepted for compatibility but remains a plan-only report.
It reports what would need manual refresh; it does not perform live HTTP
requests or rewrite source snapshots.

Output:
    YAML-formatted report to stdout. PyYAML is required; this developer script
    hard-requires it (matching the validators) so the committed/emitted format
    never silently switches to JSON depending on the environment. Each source
    entry includes machine-readable `staleness_threshold_days`, `age_days`, and
    `expires_on` fields derived from `last_checked` and `source_type`.
"""

import os
import sys
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse

# ---------------------------------------------------------------------------
# YAML loader -- PyYAML is required (no JSON fallback, so output is stable)
# ---------------------------------------------------------------------------

try:
    import yaml
except ImportError:
    raise SystemExit(
        "PyYAML is required to run plan_source_refresh "
        "(python3 -m pip install pyyaml)."
    )


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def dump_output(data):
    return yaml.dump(data, default_flow_style=False, allow_unicode=True,
                     sort_keys=False)


# ---------------------------------------------------------------------------
# Domain allowlist
# ---------------------------------------------------------------------------

ALLOWED_DOMAINS = {
    "belastingdienst.nl",
    "www.belastingdienst.nl",
    "over-ons.belastingdienst.nl",
    "odb.belastingdienst.nl",
    "wetten.overheid.nl",
    "regels.overheid.nl",
    "platform.claude.com",
    "code.claude.com",
    "svb.nl",
    "www.svb.nl",
    "rijksoverheid.nl",
    "www.rijksoverheid.nl",
}

# ---------------------------------------------------------------------------
# Staleness thresholds (days)
# ---------------------------------------------------------------------------

STALENESS_DAYS = {
    "official_rates": 90,
    "official_guidance": 180,
    "official_doctrine": 180,
    "law": 365,
    "platform_docs": 180,
    "developer_reference": 180,
    "methodology": 365,
    "official_algorithm_register": 365,
}

DEFAULT_STALENESS_DAYS = 180


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_date(date_str):
    """Parse an ISO date string (YYYY-MM-DD) into a datetime."""
    if not date_str:
        return None
    try:
        return datetime.strptime(str(date_str).strip('"'), "%Y-%m-%d").replace(
            tzinfo=timezone.utc
        )
    except (ValueError, TypeError):
        return None


def is_url_allowed(url):
    """Check if a URL is HTTPS and its host is on the domain allowlist.

    Uses urlparse (like validate_source_register.py) rather than manual string
    splitting: a hand-rolled split resolves userinfo tricks like
    ``https://allowed.nl:pw@evil.com/`` to the allowed host.
    """
    if not url:
        return False
    try:
        parsed = urlparse(str(url).strip())
    except ValueError:
        return False
    if parsed.scheme != "https":
        return False
    host = (parsed.hostname or "").lower()
    return host in ALLOWED_DOMAINS


def has_mandatory_for(source, skill_name):
    """Return whether a source is mandatory for a skill."""
    mandatory_for = source.get("mandatory_for", [])
    if isinstance(mandatory_for, str):
        mandatory_for = [mandatory_for]
    return skill_name in mandatory_for


def applies_to_year(source, year):
    """Return whether a source is relevant for a year filter.

    Sources without tax_year are shared knowledge sources. Keep them in
    year-filtered workflow checks so source refresh does not silently omit
    shared sources required by supported-workflows.yaml.
    """
    if year is None:
        return True

    source_year = source.get("tax_year")
    if source_year is None:
        return True

    try:
        return int(source_year) == int(year)
    except (ValueError, TypeError):
        return False


def matches_scope(source, scope, year=None):
    """Check if a source matches the given scope and optional year filter."""
    scope = scope.lower()

    if scope == "all":
        match = True
    elif scope == "annual":
        match = (
            source.get("workflow") == "annual_return"
            or has_mandatory_for(source, "nl-tax-annual-return")
        )
    elif scope == "provisional":
        match = (
            source.get("workflow") == "provisional_assessment"
            or has_mandatory_for(source, "nl-tax-provisional-assessment")
        )
    elif scope == "box3":
        match = "box3" in source.get("id", "").lower()
    else:
        print(f"Error: Unknown scope '{scope}'. "
              "Use: annual, provisional, box3, all", file=sys.stderr)
        sys.exit(1)

    if not match:
        return False

    return applies_to_year(source, year)


def staleness_metadata(source, now):
    """Return machine-readable staleness metadata for a source."""
    last_checked = parse_date(source.get("last_checked"))
    source_type = source.get("source_type", "")
    threshold_days = STALENESS_DAYS.get(source_type, DEFAULT_STALENESS_DAYS)

    if last_checked is None:
        return {
            "is_stale": True,
            "staleness_detail": "never_checked",
            "staleness_threshold_days": threshold_days,
            "age_days": None,
            "expires_on": None,
        }

    age_days = (now - last_checked).days
    expires_on = (last_checked + timedelta(days=threshold_days)).strftime("%Y-%m-%d")

    if age_days > threshold_days:
        detail = f"last_checked {age_days} days ago (threshold: {threshold_days})"
        is_stale = True
    else:
        detail = f"fresh (checked {age_days} days ago, threshold: {threshold_days})"
        is_stale = False

    return {
        "is_stale": is_stale,
        "staleness_detail": detail,
        "staleness_threshold_days": threshold_days,
        "age_days": age_days,
        "expires_on": expires_on,
    }


def check_snapshot_exists(source, base_dir):
    """Check if the snapshot file for a source exists."""
    snapshot_path = source.get("snapshot_path", "")
    if not snapshot_path:
        return False, "no_snapshot_path"

    full_path = os.path.join(base_dir, snapshot_path)
    if os.path.isfile(full_path):
        return True, full_path
    return False, full_path


# ---------------------------------------------------------------------------
def find_source_register():
    """Locate source-register.yaml relative to this script."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                        "_shared", "source-register.yaml")
    resolved = os.path.normpath(path)
    if os.path.isfile(resolved):
        return resolved
    return None


def find_repo_root(register_path):
    """Derive the repository root from the source-register.yaml location."""
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


def parse_cli_args(argv):
    if "-h" in argv[1:] or "--help" in argv[1:]:
        print("plan_source_refresh.py — report which registered sources need a manual refresh")
        print("Usage: python3 plan_source_refresh.py <scope> [year] [--fetch]")
        print("Scope: annual | provisional | box3 | all")
        sys.exit(0)

    if len(argv) < 2:
        print("Usage: python3 plan_source_refresh.py <scope> [year] [--fetch]",
              file=sys.stderr)
        print("", file=sys.stderr)
        print("Scope: annual | provisional | box3 | all", file=sys.stderr)
        print("Year:  optional tax year filter (e.g., 2025)", file=sys.stderr)
        print("--fetch: plan-only, lists sources needing manual refresh", file=sys.stderr)
        sys.exit(1)

    scope = argv[1]
    year = None
    fetch_flag = False

    for arg in argv[2:]:
        if arg == "--fetch":
            fetch_flag = True
        elif arg.isdigit() and len(arg) == 4:
            year = int(arg)
        else:
            print(f"Warning: Ignoring unknown argument '{arg}'", file=sys.stderr)

    return scope, year, fetch_flag


def load_sources(register_path):
    try:
        data = load_yaml(register_path)
    except yaml.YAMLError as exc:
        print(f"Error: source-register.yaml is invalid YAML: {exc}", file=sys.stderr)
        sys.exit(1)
    sources = data.get("sources", []) if isinstance(data, dict) else []
    if not sources:
        print("Error: No sources found in source-register.yaml.", file=sys.stderr)
        sys.exit(1)
    return sources


def base_report(now, scope, year, fetch_flag, register_path, sources, matched):
    return {
        "report_type": "source_refresh_plan" if fetch_flag else "source_freshness_check",
        "generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "scope": scope,
        "year_filter": year,
        "operation": "plan_only_no_live_http" if fetch_flag else "validate_freshness",
        "refresh_plan_requested": fetch_flag,
        "register_path": register_path,
        "total_sources": len(sources),
        "matched_sources": len(matched),
        "sources_checked": [],
        "summary": {
            "fresh": 0,
            "stale": 0,
            "snapshot_present": 0,
            "snapshot_missing": 0,
            "url_not_allowed": 0,
        },
    }


def source_report_entry(source, now, repo_root, fetch_flag):
    source_id = source.get("id", "unknown")
    url = source.get("url", "")
    freshness = staleness_metadata(source, now)
    snapshot_exists, _ = check_snapshot_exists(source, repo_root)
    url_allowed = is_url_allowed(url)

    entry = {
        "source_id": source_id,
        "title": source.get("title", ""),
        "url": url,
        "source_type": source.get("source_type", ""),
        "last_checked": source.get("last_checked", ""),
        "is_stale": freshness["is_stale"],
        "staleness_detail": freshness["staleness_detail"],
        "staleness_threshold_days": freshness["staleness_threshold_days"],
        "age_days": freshness["age_days"],
        "expires_on": freshness["expires_on"],
        "snapshot_exists": snapshot_exists,
        "snapshot_path": source.get("snapshot_path", ""),
        "url_on_allowlist": url_allowed,
    }

    if fetch_flag and freshness["is_stale"]:
        if url_allowed:
            entry["refresh_action"] = "PLAN_REFRESH (plan-only -- no live HTTP)"
        else:
            entry["refresh_action"] = "BLOCKED -- URL not on domain allowlist"

    return entry


def add_entry_to_summary(results, entry):
    summary = results["summary"]
    if entry["is_stale"]:
        summary["stale"] += 1
    else:
        summary["fresh"] += 1
    if entry["snapshot_exists"]:
        summary["snapshot_present"] += 1
    else:
        summary["snapshot_missing"] += 1
    if not entry["url_on_allowlist"]:
        summary["url_not_allowed"] += 1


def build_report(sources, matched, now, repo_root, register_path, scope, year, fetch_flag):
    results = base_report(now, scope, year, fetch_flag, register_path, sources, matched)
    for source in matched:
        entry = source_report_entry(source, now, repo_root, fetch_flag)
        results["sources_checked"].append(entry)
        add_entry_to_summary(results, entry)
    return results


def print_summary(results, scope, year, fetch_flag):
    s = results["summary"]
    print("\n--- Freshness Check Summary ---", file=sys.stderr)
    print(f"Scope: {scope}"
          f"{f' (year={year})' if year else ''}", file=sys.stderr)
    print(f"Sources matched: {results['matched_sources']} / {results['total_sources']}",
          file=sys.stderr)
    print(f"Fresh: {s['fresh']}  |  Stale: {s['stale']}", file=sys.stderr)
    print(f"Snapshots present: {s['snapshot_present']}  |  "
          f"Missing: {s['snapshot_missing']}", file=sys.stderr)
    if s["url_not_allowed"] > 0:
        print(f"URLs NOT on allowlist: {s['url_not_allowed']}", file=sys.stderr)
    if fetch_flag:
        print("Refresh plan: plan-only (no live HTTP requests performed)",
              file=sys.stderr)


def main():
    scope, year, fetch_flag = parse_cli_args(sys.argv)
    register_path = find_source_register()
    if register_path is None:
        print("Error: Could not find source-register.yaml.", file=sys.stderr)
        print("Expected at: skills/_shared/source-register.yaml",
              file=sys.stderr)
        sys.exit(1)

    repo_root = find_repo_root(register_path)
    now = datetime.now(timezone.utc)
    sources = load_sources(register_path)
    matched = [s for s in sources if matches_scope(s, scope, year)]

    if not matched:
        print(f"Warning: No sources match scope='{scope}'"
              f"{f', year={year}' if year else ''}.", file=sys.stderr)

    results = build_report(
        sources,
        matched,
        now,
        repo_root,
        register_path,
        scope,
        year,
        fetch_flag,
    )
    print(dump_output(results))
    print_summary(results, scope, year, fetch_flag)


if __name__ == "__main__":
    main()
