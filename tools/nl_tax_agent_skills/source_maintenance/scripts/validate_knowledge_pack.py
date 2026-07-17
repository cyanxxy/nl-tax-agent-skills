#!/usr/bin/env python3
"""Validate knowledge pack against source register.

Usage:
    python3 validate_knowledge_pack.py <path-to-source-register.yaml>

Checks:
    - Every mandatory snapshot file exists
    - Every snapshot references a source_id from the register
    - Freshness thresholds are met
    - Knowledge files without source_id references are flagged
    - Every source_id reference anywhere in skills/*.md is registered
    - Active reviewed knowledge files do not contain unverified-value markers

Scope and honesty note:
    These validators verify METADATA consistency only -- ids, snapshot paths,
    local reviewed-note hashes, review_status flags, and that every cited source_id is
    registered. A `review_status: reviewed` marker is a HUMAN attestation that a
    person checked the file; it is NOT machine proof of legal or tax-rate
    accuracy. Passing this validator means the bookkeeping is internally
    consistent, not that the underlying numbers or rules are correct.
"""

import hashlib
import os
import re
import sys
from datetime import date, timedelta


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
        # Normalize to ValueError so callers can catch parse failures without
        # importing yaml themselves.
        raise ValueError(f"invalid YAML in {path}: {exc}") from exc


def compute_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


FRESHNESS_DAYS = {
    "refresh-before-1-dec-and-before-filing-season": 90,
    "refresh-annually": 365,
    "refresh-on-law-change": 365,
    "refresh-on-demand": 730,
}

# The register also uses free-text prose policies ("check monthly",
# "after Prinsjesdag", "review each filing season", "on law change", etc.).
# When a policy is not one of the enum keys above, map it to a threshold by
# scanning for these keywords (first/smallest match wins). Without this, every
# prose policy silently fell back to 365 days.
POLICY_KEYWORD_DAYS = [
    ("monthly", 31),
    ("quarter", 92),
    ("filing season", 90),
    ("prinsjesdag", 120),
    ("annual", 365),
    ("law change", 365),
    ("on demand", 730),
]

# Season-opening policies ("check when provisional assessment season opens
# (January)") are calendar events, not rolling cadences: the source needs one
# re-attestation after each January 1, then stays fresh for the rest of the
# year. Handled by date logic in check_freshness(), not by a day threshold.
SEASON_POLICY_KEYWORDS = ("provisional assessment season", "january")

VALID_KNOWLEDGE_WORKFLOWS = {"all", "annual_return", "provisional_assessment"}


REVIEW_BLOCKING_PATTERNS = [
    ("pending verification", re.compile(r"pending verification", re.IGNORECASE)),
    ("verify against", re.compile(r"verify against", re.IGNORECASE)),
    ("may differ from", re.compile(r"may differ from", re.IGNORECASE)),
    ("approximate marker", re.compile(r"\bapprox(?:imate|imately)?\b", re.IGNORECASE)),
    ("indicative marker", re.compile(r"\bindicative\b", re.IGNORECASE)),
    ("approximate EUR marker", re.compile(r"~\s*EUR", re.IGNORECASE)),
    ("approximate numeric marker", re.compile(r"~\s*\d+(?:[.,]\d+)?\s*%?")),
]


def check_freshness(last_checked, policy):
    if not last_checked:
        return True, "no last_checked date"
    try:
        checked = date.fromisoformat(str(last_checked))
    except ValueError:
        return True, f"invalid date format: {last_checked}"

    lc = str(policy).lower()
    threshold = FRESHNESS_DAYS.get(policy)

    # Season-opening policies: stale only when last_checked predates the most
    # recent season opening (January 1), i.e. one re-attestation per year at
    # the moment the developer already knows matters.
    if threshold is None and any(kw in lc for kw in SEASON_POLICY_KEYWORDS):
        season_open = date(date.today().year, 1, 1)
        if checked < season_open:
            return True, (
                f"last checked {last_checked}, before the season opened on "
                f"{season_open.isoformat()}"
            )
        return False, ""

    if threshold is None:
        threshold = min(
            (days for keyword, days in POLICY_KEYWORD_DAYS if keyword in lc),
            default=365,
        )
    age = (date.today() - checked).days
    if age > threshold:
        return True, f"last checked {age} days ago (threshold: {threshold})"
    return False, ""


# These runtime subtrees hold authored conversation or product-scope guidance
# that is not a tax-rule restatement. They are exempt from the "every knowledge
# file must cite a source_id" check. Maintainer-only platform, compatibility,
# and authoring notes live outside the plugin under docs/maintainers/.
INTERNAL_KNOWLEDGE_PREFIXES = (
    "methods",
    "security",
)


def _is_internal_knowledge(rel_from_knowledge_dir):
    """Return true for authored internal knowledge that is not source-backed."""
    norm = rel_from_knowledge_dir.replace(os.sep, "/")
    return any(
        norm == prefix or norm.startswith(prefix + "/")
        for prefix in INTERNAL_KNOWLEDGE_PREFIXES
    )


def find_knowledge_files(knowledge_dir):
    """Find source-backed .md files in the knowledge directory."""
    result = []
    for root, dirs, files in os.walk(knowledge_dir):
        rel = os.path.relpath(root, knowledge_dir)
        if rel == ".":
            rel = ""
        # Prune internal subtrees so the walk never descends into them.
        dirs[:] = [
            d for d in dirs
            if not _is_internal_knowledge(os.path.join(rel, d).replace(os.sep, "/"))
        ]
        if rel and _is_internal_knowledge(rel):
            continue
        for f in files:
            if f.endswith(".md") and not f.startswith("_"):
                result.append(os.path.join(root, f))
    return result


def find_markdown_files(root_dir):
    """Find all .md files under a directory."""
    result = []
    for root, _, files in os.walk(root_dir):
        for f in files:
            if f.endswith(".md") and not f.startswith("_"):
                result.append(os.path.join(root, f))
    return result


def find_reference_files(skills_dir):
    """Find .md files in skill reference directories."""
    result = []
    for root, _, files in os.walk(skills_dir):
        if os.path.basename(root) != "reference":
            continue
        for f in files:
            if f.endswith(".md") and not f.startswith("_"):
                result.append(os.path.join(root, f))
    return result


def is_relative_to(path, parent):
    """Return whether path is inside parent, without pathlib for Py3.8 compatibility."""
    try:
        os.path.relpath(path, parent)
        return os.path.commonpath([os.path.abspath(path), os.path.abspath(parent)]) == os.path.abspath(parent)
    except ValueError:
        return False


def find_content_root(register_path):
    """Find the repo/plugin root that snapshot_path values are relative to.

    Register paths are serialized from this root (for example
    skills/_shared/knowledge/...), not from an individual skill directory where
    the same file may be referenced as _shared/knowledge/...
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


def find_repository_metadata_root(project_root):
    """Return the repo-only metadata root for a plugin in plugins/."""
    plugins_dir = os.path.dirname(os.path.abspath(project_root))
    if os.path.basename(plugins_dir) != "plugins":
        return None
    candidate = os.path.join(
        os.path.dirname(plugins_dir),
        "tools",
        "nl_tax_agent_skills",
        "source_maintenance",
        "metadata",
    )
    return candidate if os.path.isdir(candidate) else None


def metadata_path_for_snapshot(abs_snapshot, project_root, metadata_root=None):
    """Map a reviewed note to external metadata, with legacy fallback."""
    if metadata_root:
        knowledge_root = os.path.join(
            project_root, "skills", "_shared", "knowledge"
        )
        snapshot_dir = os.path.dirname(abs_snapshot)
        try:
            if os.path.commonpath([knowledge_root, snapshot_dir]) == knowledge_root:
                relative_dir = os.path.relpath(snapshot_dir, knowledge_root)
                return os.path.join(
                    metadata_root, relative_dir, "_snapshot-metadata.yaml"
                )
        except ValueError:
            pass
    return os.path.join(os.path.dirname(abs_snapshot), "_snapshot-metadata.yaml")


def extract_source_ids(filepath):
    """Extract source_id references from a knowledge file, skipping code blocks."""
    ids = set()
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        in_code_block = False
        in_source_ids_block = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            # Block-style YAML list continuation:
            #   source_ids:
            #     - some_source
            if in_source_ids_block:
                item = re.match(r"-\s*(.+)", stripped)
                if item:
                    sid = item.group(1).strip().strip('"').strip("'")
                    if sid and not sid.startswith("#") and not sid.startswith("<"):
                        ids.add(sid)
                    continue
                in_source_ids_block = False
            match = re.match(r"source_ids?:\s*(.*)", stripped)
            if match:
                raw = match.group(1).strip()
                if not raw:
                    in_source_ids_block = True
                    continue
                for sid in re.split(r"[,\s]+", raw):
                    sid = sid.strip().strip("-").strip().strip('"').strip("'")
                    if sid and not sid.startswith("#") and not sid.startswith("<"):
                        ids.add(sid)
    except (OSError, UnicodeDecodeError):
        pass
    return ids


def extract_metadata_value(filepath, key):
    """Extract a simple `key: value` metadata field from a markdown file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                if stripped.startswith("## "):
                    break
                match = re.match(rf"{re.escape(key)}:\s*(.+)", stripped)
                if match:
                    return match.group(1).strip().strip('"').strip("'")
    except (OSError, UnicodeDecodeError):
        pass
    return ""


def split_metadata_values(raw):
    """Split comma-separated metadata such as `workflow: annual_return, all`."""
    return [part.strip() for part in raw.split(",") if part.strip()]


def find_review_blocking_markers(filepath):
    """Find unverified-value markers that are not allowed in active reviewed files."""
    markers = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for lineno, line in enumerate(f, start=1):
                for label, pattern in REVIEW_BLOCKING_PATTERNS:
                    if pattern.search(line):
                        markers.append((lineno, label, line.strip()))
    except (OSError, UnicodeDecodeError):
        pass
    return markers


def parse_args(argv):
    if "-h" in argv[1:] or "--help" in argv[1:]:
        print("validate_knowledge_pack.py — validate knowledge-pack snapshots and freshness")
        print("Usage: python3 validate_knowledge_pack.py <path-to-source-register.yaml>")
        sys.exit(0)

    if len(argv) < 2:
        print(
            "Usage: python3 validate_knowledge_pack.py <path-to-source-register.yaml>",
            file=sys.stderr,
        )
        sys.exit(1)

    register_path = argv[1]
    if not os.path.isfile(register_path):
        print(f"Error: file not found: {register_path}", file=sys.stderr)
        sys.exit(1)
    return register_path


def collect_source_status(sources, project_root):
    registered_ids = set()
    missing_snapshots = []
    stale_sources = []

    for source in sources:
        sid = source.get("id", "")
        registered_ids.add(sid)

        snapshot_path = source.get("snapshot_path", "")
        if snapshot_path:
            abs_path = os.path.join(project_root, snapshot_path)
            if not os.path.isfile(abs_path):
                missing_snapshots.append(sid)

        is_stale, reason = check_freshness(
            source.get("last_checked", ""),
            source.get("freshness_policy", "refresh-annually"),
        )
        if is_stale:
            mandatory_for = source.get("mandatory_for") or []
            is_mandatory = bool(mandatory_for)
            stale_sources.append((sid, reason, is_mandatory))

    return registered_ids, missing_snapshots, stale_sources


def metadata_for_source(metadata, source_id):
    if not isinstance(metadata, dict):
        return None

    sources = metadata.get("sources")
    if isinstance(sources, dict):
        entry = sources.get(source_id)
        return entry if isinstance(entry, dict) else None

    if metadata.get("source_id") == source_id:
        return metadata

    return None


def collect_snapshot_metadata_errors(sources, project_root, metadata_root=None):
    errors = []

    for source in sources:
        sid = source.get("id", "")
        snapshot_path = source.get("snapshot_path", "")
        if not sid or not snapshot_path:
            continue

        abs_snapshot = os.path.join(project_root, snapshot_path)
        if not os.path.isfile(abs_snapshot):
            continue
        rel_snapshot = os.path.relpath(abs_snapshot, project_root)

        meta_path = metadata_path_for_snapshot(
            abs_snapshot, project_root, metadata_root
        )
        rel_meta_path = os.path.relpath(meta_path, project_root)
        if not os.path.isfile(meta_path):
            errors.append((sid, "missing snapshot metadata file", rel_meta_path))
            continue

        try:
            metadata = load_yaml_or_json(meta_path)
        except (OSError, ValueError) as exc:
            errors.append((sid, f"unreadable snapshot metadata: {exc}", rel_meta_path))
            continue

        if not isinstance(metadata, dict) or metadata.get("metadata_version") != "1.1":
            errors.append((sid, "snapshot metadata_version is not 1.1", rel_meta_path))
            continue

        source_meta = metadata_for_source(metadata, sid)
        if not source_meta:
            errors.append((sid, "missing snapshot metadata entry", rel_meta_path))
            continue

        stored_hash = source_meta.get("reviewed_note_hash_sha256", "")
        current_hash = compute_sha256(abs_snapshot)
        if stored_hash != current_hash:
            errors.append((sid, "hash mismatch", rel_meta_path))

        stored_url = source_meta.get("source_url", "")
        source_url = source.get("url", "")
        if stored_url != source_url:
            errors.append((sid, "source_url mismatch", rel_meta_path))

        if source_meta.get("review_status") != "reviewed":
            errors.append((sid, "snapshot metadata not reviewed", rel_meta_path))

        if not source_meta.get("reviewed_note_hash_recorded_at"):
            errors.append((sid, "missing reviewed-note hash timestamp", rel_meta_path))

        snapshot_refs = extract_source_ids(abs_snapshot)
        if sid not in snapshot_refs:
            errors.append((sid, "snapshot does not reference source_id", rel_snapshot))

    return errors


def collect_skill_source_reference_errors(skills_dir, project_root, registered_ids):
    source_reference_errors = []
    if not os.path.isdir(skills_dir):
        return source_reference_errors

    for mf in find_markdown_files(skills_dir):
        refs = extract_source_ids(mf)
        unknown = refs - registered_ids
        if unknown:
            rel_path = os.path.relpath(mf, project_root)
            for source_id in sorted(unknown):
                source_reference_errors.append((rel_path, source_id))
    return source_reference_errors


def source_backed_markdown_files(knowledge_dir, skills_dir):
    files = set(find_knowledge_files(knowledge_dir))
    if os.path.isdir(skills_dir):
        files.update(find_reference_files(skills_dir))
    return sorted(files)


def should_require_source_refs(filepath, knowledge_dir):
    status = extract_metadata_value(filepath, "status").lower()
    review_status = extract_metadata_value(filepath, "review_status").lower()
    return is_relative_to(filepath, knowledge_dir) or (
        status == "active" and review_status == "reviewed"
    )


def collect_knowledge_file_errors(knowledge_dir, skills_dir, project_root, registered_ids):
    unreferenced = []
    review_marker_errors = []
    workflow_metadata_errors = []
    unknown_reference_errors = []

    if not os.path.isdir(knowledge_dir):
        return (
            unreferenced,
            review_marker_errors,
            workflow_metadata_errors,
            unknown_reference_errors,
        )

    for kf in source_backed_markdown_files(knowledge_dir, skills_dir):
        refs = extract_source_ids(kf)
        rel_path = os.path.relpath(kf, project_root)
        if not refs:
            if should_require_source_refs(kf, knowledge_dir):
                unreferenced.append(rel_path)
        else:
            for source_id in sorted(refs - registered_ids):
                unknown_reference_errors.append((rel_path, source_id))

        status = extract_metadata_value(kf, "status").lower()
        review_status = extract_metadata_value(kf, "review_status").lower()
        if status != "active" or review_status != "reviewed":
            continue

        workflow = extract_metadata_value(kf, "workflow")
        workflows = split_metadata_values(workflow) if workflow else []
        invalid_workflows = [
            wf for wf in workflows if wf not in VALID_KNOWLEDGE_WORKFLOWS
        ]
        if invalid_workflows:
            workflow_metadata_errors.append((rel_path, workflow))

        for lineno, label, text in find_review_blocking_markers(kf):
            review_marker_errors.append((rel_path, lineno, label, text))

    return (
        unreferenced,
        review_marker_errors,
        workflow_metadata_errors,
        unknown_reference_errors,
    )


def print_section(title, rows, formatter):
    if not rows:
        return
    print(title)
    for row in rows:
        print(f"  - {formatter(row)}")
    print()


def print_report(
    sources,
    missing_snapshots,
    stale_sources,
    snapshot_metadata_errors,
    unreferenced,
    review_marker_errors,
    workflow_metadata_errors,
    source_reference_errors,
):
    stale_mandatory = [row for row in stale_sources if len(row) > 2 and row[2]]
    stale_warning = [row for row in stale_sources if not (len(row) > 2 and row[2])]

    print_section("MISSING SNAPSHOTS:", missing_snapshots, lambda source_id: source_id)
    print_section(
        "STALE MANDATORY SOURCES (blocking):",
        stale_mandatory,
        lambda row: f"{row[0]}: {row[1]}",
    )
    print_section(
        "STALE SOURCES (warning):",
        stale_warning,
        lambda row: f"{row[0]}: {row[1]}",
    )
    print_section(
        "SNAPSHOT METADATA ERRORS:",
        snapshot_metadata_errors,
        lambda row: f"{row[0]}: {row[1]} ({row[2]})",
    )
    print_section("KNOWLEDGE FILES WITHOUT SOURCE REFERENCES:", unreferenced, lambda path: path)
    print_section(
        "ACTIVE REVIEWED FILES WITH UNVERIFIED-VALUE MARKERS:",
        review_marker_errors,
        lambda row: f"{row[0]}:{row[1]}: {row[2]}: {row[3]}",
    )
    print_section(
        "ACTIVE REVIEWED FILES WITH INVALID WORKFLOW METADATA:",
        workflow_metadata_errors,
        lambda row: f"{row[0]}: workflow: {row[1]}",
    )
    print_section(
        "SOURCE_ID REFERENCES NOT PRESENT IN SOURCE REGISTER:",
        source_reference_errors,
        lambda row: f"{row[0]}: source_id: {row[1]}",
    )

    print(f"Summary: {len(sources)} sources, "
          f"{len(missing_snapshots)} missing, "
          f"{len(stale_sources)} stale, "
          f"{len(snapshot_metadata_errors)} metadata errors, "
          f"{len(unreferenced)} unreferenced files, "
          f"{len(review_marker_errors)} review marker errors, "
          f"{len(workflow_metadata_errors)} workflow metadata errors, "
          f"{len(source_reference_errors)} unknown source_id errors")


def main():
    register_path = parse_args(sys.argv)
    base_dir = os.path.dirname(os.path.abspath(register_path))
    project_root = find_content_root(register_path)
    metadata_root = find_repository_metadata_root(project_root)
    knowledge_dir = os.path.join(base_dir, "knowledge")
    skills_dir = os.path.dirname(base_dir)

    data = load_yaml_or_json(register_path)
    if isinstance(data, list):
        sources = data
    elif isinstance(data, dict):
        sources = data.get("sources", data.get("entries", []))
    else:
        print(f"VALIDATION FAILED\n\nRegister is empty or not a mapping/list: {register_path}")
        sys.exit(1)

    registered_ids, missing_snapshots, stale_sources = collect_source_status(
        sources,
        project_root,
    )
    snapshot_metadata_errors = collect_snapshot_metadata_errors(
        sources, project_root, metadata_root
    )
    source_reference_errors = collect_skill_source_reference_errors(
        skills_dir,
        project_root,
        registered_ids,
    )
    (
        unreferenced,
        review_marker_errors,
        workflow_metadata_errors,
        unknown_reference_errors,
    ) = collect_knowledge_file_errors(
        knowledge_dir,
        skills_dir,
        project_root,
        registered_ids,
    )
    # Knowledge/reference files are also covered by the skills-wide walk;
    # merge both passes so an unknown source_id always fails validation.
    source_reference_errors = sorted(
        set(source_reference_errors) | set(unknown_reference_errors)
    )

    # A stale source that is mandatory_for at least one skill is a blocking
    # error; non-mandatory staleness stays a warning.
    stale_mandatory = [row for row in stale_sources if len(row) > 2 and row[2]]
    stale_warning = [row for row in stale_sources if not (len(row) > 2 and row[2])]

    has_errors = bool(
        missing_snapshots
        or snapshot_metadata_errors
        or review_marker_errors
        or workflow_metadata_errors
        or source_reference_errors
        or stale_mandatory
    )

    print_report(
        sources,
        missing_snapshots,
        stale_sources,
        snapshot_metadata_errors,
        unreferenced,
        review_marker_errors,
        workflow_metadata_errors,
        source_reference_errors,
    )

    if has_errors:
        print("VALIDATION FAILED")
    elif stale_warning or unreferenced:
        print("VALIDATION PASSED WITH WARNINGS")
    else:
        print("VALIDATION PASSED")

    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
