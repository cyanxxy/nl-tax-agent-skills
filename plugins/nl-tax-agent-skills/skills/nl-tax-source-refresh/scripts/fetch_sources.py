#!/usr/bin/env python3
"""
NL Tax Source Refresh -- Fetch Sources

Reads source-register.yaml, filters by scope and year, checks freshness
against each source's freshness_policy, and reports which sources need
refreshing.

Usage:
    python fetch_sources.py <scope> [year] [--fetch]
    python fetch_sources.py annual
    python fetch_sources.py provisional 2026
    python fetch_sources.py box3 2025
    python fetch_sources.py all
    python fetch_sources.py all --fetch

Scope:
    annual       -- sources with workflow: annual_return
    provisional  -- sources with workflow: provisional_assessment
    box3         -- sources with IDs containing 'box3'
    all          -- every source in the register

The --fetch flag is accepted for forward compatibility but in this v1 stub
only reports what would be fetched. Live HTTP fetching requires the developer
to use the skill with appropriate network permissions.

Output:
    YAML-formatted report to stdout (or JSON fallback).

Standard library only (no pip dependencies).
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# YAML loader -- try PyYAML, fall back to a minimal inline parser
# ---------------------------------------------------------------------------

try:
    import yaml

    def load_yaml(path):
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def dump_output(data):
        return yaml.dump(data, default_flow_style=False, allow_unicode=True,
                         sort_keys=False)
except ImportError:
    yaml = None

    def load_yaml(path):
        """Fallback: parse YAML-subset via json if the file is also valid JSON,
        otherwise do a best-effort line parse for the fields we need."""
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return _parse_yaml_subset(content)

    def dump_output(data):
        return json.dumps(data, indent=2, ensure_ascii=False, default=str)

    def _parse_yaml_subset(content):
        """Minimal YAML-subset parser for source-register.yaml structure."""
        sources = []
        current = None
        current_list_key = None

        for line in content.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            # Detect new list item under 'sources:'
            if stripped.startswith("- id:"):
                if current is not None:
                    sources.append(current)
                current = {"id": stripped.split(":", 1)[1].strip().strip('"')}
                current_list_key = None
                continue

            if current is not None:
                # Continuation of a list value (e.g., mandatory_for items)
                if stripped.startswith("- ") and current_list_key:
                    val = stripped[2:].strip().strip('"')
                    current.setdefault(current_list_key, []).append(val)
                    continue

                if ":" in stripped:
                    key, _, val = stripped.partition(":")
                    key = key.strip()
                    val = val.strip().strip('"')
                    if not val:
                        current_list_key = key
                    else:
                        current_list_key = None
                        # Parse tax_year as int if numeric
                        if key == "tax_year" and val.isdigit():
                            val = int(val)
                        current[key] = val

        if current is not None:
            sources.append(current)

        return {"sources": sources}


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
    """Check if a URL is on the domain allowlist."""
    if not url:
        return False
    # Extract domain from URL
    try:
        # Remove protocol
        after_proto = url.split("://", 1)[-1]
        domain = after_proto.split("/", 1)[0].split(":")[0].lower()
        return domain in ALLOWED_DOMAINS
    except (IndexError, AttributeError):
        return False


def matches_scope(source, scope, year=None):
    """Check if a source matches the given scope and optional year filter."""
    scope = scope.lower()

    if scope == "all":
        match = True
    elif scope == "annual":
        match = source.get("workflow") == "annual_return"
    elif scope == "provisional":
        match = source.get("workflow") == "provisional_assessment"
    elif scope == "box3":
        match = "box3" in source.get("id", "").lower()
    else:
        print(f"Error: Unknown scope '{scope}'. "
              f"Use: annual, provisional, box3, all", file=sys.stderr)
        sys.exit(1)

    if not match:
        return False

    if year is not None:
        source_year = source.get("tax_year")
        if source_year is not None:
            try:
                if int(source_year) != int(year):
                    return False
            except (ValueError, TypeError):
                pass

    return True


def check_staleness(source, now):
    """Check if a source is stale based on its last_checked date and source_type."""
    last_checked = parse_date(source.get("last_checked"))
    if last_checked is None:
        return True, "never_checked"

    source_type = source.get("source_type", "")
    threshold_days = STALENESS_DAYS.get(source_type, DEFAULT_STALENESS_DAYS)
    age_days = (now - last_checked).days

    if age_days > threshold_days:
        return True, f"last_checked {age_days} days ago (threshold: {threshold_days})"

    return False, f"fresh (checked {age_days} days ago, threshold: {threshold_days})"


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
# Main
# ---------------------------------------------------------------------------

def find_source_register():
    """Locate source-register.yaml relative to the script or working directory."""
    candidates = [
        os.path.join(os.getcwd(), ".claude", "skills", "_shared",
                     "source-register.yaml"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                     "_shared", "source-register.yaml"),
    ]
    for path in candidates:
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


def main():
    if len(sys.argv) < 2:
        print("Usage: python fetch_sources.py <scope> [year] [--fetch]",
              file=sys.stderr)
        print("", file=sys.stderr)
        print("Scope: annual | provisional | box3 | all", file=sys.stderr)
        print("Year:  optional tax year filter (e.g., 2025)", file=sys.stderr)
        print("--fetch: v1 stub, reports what would be fetched", file=sys.stderr)
        sys.exit(1)

    scope = sys.argv[1]
    year = None
    fetch_flag = False

    for arg in sys.argv[2:]:
        if arg == "--fetch":
            fetch_flag = True
        elif arg.isdigit() and len(arg) == 4:
            year = int(arg)
        else:
            print(f"Warning: Ignoring unknown argument '{arg}'", file=sys.stderr)

    # Locate source register
    register_path = find_source_register()
    if register_path is None:
        print("Error: Could not find source-register.yaml.", file=sys.stderr)
        print("Expected at: skills/_shared/source-register.yaml or "
              ".claude/skills/_shared/source-register.yaml", file=sys.stderr)
        sys.exit(1)

    repo_root = find_repo_root(register_path)
    now = datetime.now(timezone.utc)

    # Load register
    data = load_yaml(register_path)
    sources = data.get("sources", [])

    if not sources:
        print("Error: No sources found in source-register.yaml.", file=sys.stderr)
        sys.exit(1)

    # Filter by scope and year
    matched = [s for s in sources if matches_scope(s, scope, year)]

    if not matched:
        print(f"Warning: No sources match scope='{scope}'"
              f"{f', year={year}' if year else ''}.", file=sys.stderr)

    # Check each source
    results = {
        "report_type": "source_freshness_check",
        "generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "scope": scope,
        "year_filter": year,
        "fetch_requested": fetch_flag,
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

    for source in matched:
        source_id = source.get("id", "unknown")
        url = source.get("url", "")
        is_stale, staleness_reason = check_staleness(source, now)
        snapshot_exists, snapshot_detail = check_snapshot_exists(source, repo_root)
        url_allowed = is_url_allowed(url)

        entry = {
            "source_id": source_id,
            "title": source.get("title", ""),
            "url": url,
            "source_type": source.get("source_type", ""),
            "last_checked": source.get("last_checked", ""),
            "is_stale": is_stale,
            "staleness_detail": staleness_reason,
            "snapshot_exists": snapshot_exists,
            "snapshot_path": source.get("snapshot_path", ""),
            "url_on_allowlist": url_allowed,
        }

        if fetch_flag and is_stale:
            if url_allowed:
                entry["fetch_action"] = "WOULD_FETCH (v1 stub -- no live HTTP)"
            else:
                entry["fetch_action"] = "BLOCKED -- URL not on domain allowlist"

        results["sources_checked"].append(entry)

        # Update summary
        if is_stale:
            results["summary"]["stale"] += 1
        else:
            results["summary"]["fresh"] += 1
        if snapshot_exists:
            results["summary"]["snapshot_present"] += 1
        else:
            results["summary"]["snapshot_missing"] += 1
        if not url_allowed:
            results["summary"]["url_not_allowed"] += 1

    # Output
    print(dump_output(results))

    # Summary to stderr
    s = results["summary"]
    print(f"\n--- Freshness Check Summary ---", file=sys.stderr)
    print(f"Scope: {scope}"
          f"{f' (year={year})' if year else ''}", file=sys.stderr)
    print(f"Sources matched: {len(matched)} / {len(sources)}", file=sys.stderr)
    print(f"Fresh: {s['fresh']}  |  Stale: {s['stale']}", file=sys.stderr)
    print(f"Snapshots present: {s['snapshot_present']}  |  "
          f"Missing: {s['snapshot_missing']}", file=sys.stderr)
    if s["url_not_allowed"] > 0:
        print(f"URLs NOT on allowlist: {s['url_not_allowed']}", file=sys.stderr)
    if fetch_flag:
        print(f"Fetch mode: v1 stub (no live HTTP requests performed)",
              file=sys.stderr)


if __name__ == "__main__":
    main()
