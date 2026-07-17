#!/usr/bin/env python3
"""Build and verify snapshot metadata for source register entries.

Usage:
    python3 build_snapshots.py <path-to-source-register.yaml>

For each source entry with a snapshot_path:
    - Checks if the snapshot file exists
    - Computes a SHA-256 hash of the local reviewed note if it exists
    - Generates/updates repository-only metadata outside the runtime plugin
    - Reports status: present, missing, or reviewed-note-hash-changed
"""

import hashlib
import os
import sys
from datetime import datetime, timezone


def load_yaml_or_json(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    try:
        import yaml
    except ImportError:
        raise SystemExit(
            "PyYAML is required to build snapshot metadata "
            "(python3 -m pip install pyyaml)."
        )
    try:
        return yaml.safe_load(content)
    except yaml.YAMLError as exc:
        raise SystemExit(f"Error: invalid YAML in {path}: {exc}")


def compute_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def load_existing_metadata(meta_path):
    if not os.path.isfile(meta_path):
        return None
    return load_yaml_or_json(meta_path)


def write_metadata(meta_path, metadata):
    """Write metadata as YAML, preserving nested per-source entries.

    PyYAML is hard-required (no JSON fallback) so the committed
    _snapshot-metadata.yaml is never silently rewritten as JSON depending on the
    environment in which this developer script happens to run.
    """
    try:
        import yaml
    except ImportError:
        raise SystemExit(
            "PyYAML is required to build snapshot metadata "
            "(python3 -m pip install pyyaml)."
        )
    rendered = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=True)
    try:
        os.makedirs(os.path.dirname(meta_path), exist_ok=True)
        with open(meta_path, "w", encoding="utf-8") as f:
            f.write(rendered)
            if not rendered.endswith("\n"):
                f.write("\n")
    except OSError as exc:
        raise SystemExit(
            f"Error: cannot write snapshot metadata to {meta_path}: {exc}\n"
            "(read-only install?) — run this developer script from a writable "
            "clone of the repo."
        )


def normalize_directory_metadata(existing_meta):
    """Return directory metadata with one entry per source ID."""
    if not isinstance(existing_meta, dict):
        return {"metadata_version": "1.1", "sources": {}}

    if isinstance(existing_meta.get("sources"), dict):
        return {
            "metadata_version": "1.1",
            "sources": existing_meta["sources"],
        }

    # Backward compatibility with the old single-source file shape.
    if existing_meta.get("source_id"):
        source_id = existing_meta["source_id"]
        return {
            "metadata_version": "1.1",
            "sources": {source_id: existing_meta},
        }

    return {"metadata_version": "1.1", "sources": {}}


def existing_source_metadata(existing_meta, source_id):
    if not isinstance(existing_meta, dict):
        return None
    sources = existing_meta.get("sources")
    if isinstance(sources, dict):
        entry = sources.get(source_id)
        return entry if isinstance(entry, dict) else None
    if existing_meta.get("source_id") == source_id:
        return existing_meta
    return None


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
    """Map a reviewed runtime note to repository-only metadata."""
    if not metadata_root:
        raise ValueError("repository-only snapshot metadata root is unavailable")

    knowledge_root = os.path.join(
        project_root, "skills", "_shared", "knowledge"
    )
    snapshot_dir = os.path.dirname(abs_snapshot)
    try:
        inside_knowledge = (
            os.path.commonpath([knowledge_root, snapshot_dir]) == knowledge_root
        )
    except ValueError as exc:
        raise ValueError("snapshot is outside the runtime knowledge tree") from exc
    if not inside_knowledge:
        raise ValueError("snapshot is outside the runtime knowledge tree")

    relative_dir = os.path.relpath(snapshot_dir, knowledge_root)
    return os.path.join(
        metadata_root, relative_dir, "_snapshot-metadata.yaml"
    )


def main():
    if "-h" in sys.argv[1:] or "--help" in sys.argv[1:]:
        print("build_snapshots.py — recompute snapshot hashes/metadata for the source register")
        print("Usage: python3 build_snapshots.py <path-to-source-register.yaml>")
        sys.exit(0)

    if len(sys.argv) < 2:
        print("Usage: python3 build_snapshots.py <path-to-source-register.yaml>",
              file=sys.stderr)
        sys.exit(1)

    register_path = sys.argv[1]
    if not os.path.isfile(register_path):
        print(f"Error: source register not found: {register_path}", file=sys.stderr)
        sys.exit(1)

    project_root = find_content_root(register_path)
    metadata_root = find_repository_metadata_root(project_root)
    if metadata_root is None:
        print(
            "Error: repository-only snapshot metadata directory not found. "
            "Run this maintainer tool from the source repository, where "
            "tools/nl_tax_agent_skills/source_maintenance/metadata exists; "
            "runtime plugin knowledge directories are never a metadata fallback.",
            file=sys.stderr,
        )
        sys.exit(1)

    data = load_yaml_or_json(register_path)
    if isinstance(data, list):
        sources = data
    elif isinstance(data, dict):
        sources = data.get("sources", data.get("entries", []))
    else:
        sources = None
    if not sources:
        print(f"Error: no sources found in register: {register_path}", file=sys.stderr)
        sys.exit(1)

    results = {"present": [], "missing": [], "hash_changed": [], "invalid": []}
    now = datetime.now(timezone.utc).isoformat()

    for source in sources:
        if not isinstance(source, dict):
            results["invalid"].append("non-mapping source entry")
            print("  INVALID  non-mapping source entry")
            continue
        sid = source.get("id", "unknown")
        snapshot_path = source.get("snapshot_path")

        if not snapshot_path:
            continue

        abs_snapshot = os.path.join(project_root, snapshot_path)
        try:
            meta_path = metadata_path_for_snapshot(
                abs_snapshot, project_root, metadata_root
            )
        except ValueError as exc:
            results["invalid"].append(sid)
            print(f"  INVALID  {sid} -> {exc}")
            continue

        if not os.path.isfile(abs_snapshot):
            results["missing"].append(sid)
            print(f"  MISSING  {sid} -> {snapshot_path}")
            continue

        current_hash = compute_sha256(abs_snapshot)
        existing_meta = load_existing_metadata(meta_path)
        existing_source_meta = existing_source_metadata(existing_meta, sid)

        status = "present"
        if existing_source_meta:
            old_hash = existing_source_meta.get("reviewed_note_hash_sha256", "")
            if old_hash and old_hash != current_hash:
                status = "hash_changed"

        # Preserve the time at which this exact note hash was recorded unless
        # the reviewed note changed, so an unchanged rebuild is a no-op.
        if existing_source_meta and status != "hash_changed":
            recorded_at = existing_source_meta.get(
                "reviewed_note_hash_recorded_at", now
            )
        else:
            recorded_at = now

        # New or changed content always needs human review; an unchanged
        # snapshot keeps its recorded review_status (this script must never
        # promote a snapshot to "reviewed" on its own).
        if status == "hash_changed" or not existing_source_meta:
            review_status = "needs_review"
        else:
            review_status = existing_source_meta.get("review_status", "needs_review")

        metadata = {
            "source_id": sid,
            "reviewed_note_hash_recorded_at": recorded_at,
            "source_url": source.get("url", ""),
            "reviewed_note_hash_sha256": current_hash,
            "review_status": review_status,
        }

        results[status].append(sid)
        label = "CHANGED" if status == "hash_changed" else "OK"
        print(f"  {label:8s} {sid} -> {snapshot_path}")

        # Skip rewriting the directory file when this entry is already identical.
        if existing_source_meta == metadata:
            continue

        directory_metadata = normalize_directory_metadata(existing_meta)
        directory_metadata["sources"][sid] = metadata
        write_metadata(meta_path, directory_metadata)

    # Summary
    print()
    print("Summary:")
    print(f"  Present:      {len(results['present'])}")
    print(f"  Missing:      {len(results['missing'])}")
    print(f"  Hash changed: {len(results['hash_changed'])}")
    print(f"  Invalid entries: {len(results['invalid'])}")

    if results["missing"]:
        print()
        print("Missing snapshots:")
        for s in results["missing"]:
            print(f"  - {s}")

    if results["hash_changed"]:
        print()
        print(
            "Note: changed snapshots were demoted to review_status: needs_review. "
            "Exit code 0 covers both no-op and changed runs; check the CHANGED "
            "lines above."
        )

    sys.exit(1 if results["missing"] or results["invalid"] else 0)


if __name__ == "__main__":
    main()
