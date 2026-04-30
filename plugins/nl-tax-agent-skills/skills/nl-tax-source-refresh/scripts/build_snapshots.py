#!/usr/bin/env python3
"""Build and verify snapshot metadata for source register entries.

Usage:
    python build_snapshots.py <path-to-source-register.yaml>

For each source entry with a snapshot_path:
    - Checks if the snapshot file exists
    - Computes SHA-256 hash if it exists
    - Generates/updates _snapshot-metadata.yaml alongside the snapshot
    - Reports status: present, missing, or hash-changed
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone


def load_yaml_or_json(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    try:
        import yaml
        return yaml.safe_load(content)
    except ImportError:
        return json.loads(content)


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
    """Write metadata, preserving nested per-source entries."""
    try:
        import yaml
        rendered = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=True)
    except ImportError:
        rendered = json.dumps(metadata, indent=2, ensure_ascii=False)
    with open(meta_path, "w", encoding="utf-8") as f:
        f.write(rendered)
        if not rendered.endswith("\n"):
            f.write("\n")


def normalize_directory_metadata(existing_meta):
    """Return directory metadata with one entry per source ID."""
    if not isinstance(existing_meta, dict):
        return {"snapshot_metadata_version": "1.0", "sources": {}}

    if isinstance(existing_meta.get("sources"), dict):
        return existing_meta

    # Backward compatibility with the old single-source file shape.
    if existing_meta.get("source_id"):
        source_id = existing_meta["source_id"]
        return {
            "snapshot_metadata_version": "1.0",
            "sources": {source_id: existing_meta},
        }

    existing_meta["snapshot_metadata_version"] = existing_meta.get(
        "snapshot_metadata_version", "1.0"
    )
    existing_meta["sources"] = {}
    return existing_meta


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
    """Find the root that snapshot_path values are relative to."""
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
        print("Usage: python build_snapshots.py <path-to-source-register.yaml>",
              file=sys.stderr)
        sys.exit(1)

    register_path = sys.argv[1]
    if not os.path.isfile(register_path):
        print(f"Error: source register not found: {register_path}", file=sys.stderr)
        sys.exit(1)

    project_root = find_content_root(register_path)

    data = load_yaml_or_json(register_path)
    sources = data if isinstance(data, list) else data.get("sources", data.get("entries", []))

    results = {"present": [], "missing": [], "hash_changed": [], "errors": []}
    now = datetime.now(timezone.utc).isoformat()

    for source in sources:
        sid = source.get("id", "unknown")
        snapshot_path = source.get("snapshot_path")

        if not snapshot_path:
            continue

        abs_snapshot = os.path.join(project_root, snapshot_path)
        snapshot_dir = os.path.dirname(abs_snapshot)
        meta_path = os.path.join(snapshot_dir, "_snapshot-metadata.yaml")

        if not os.path.isfile(abs_snapshot):
            results["missing"].append(sid)
            print(f"  MISSING  {sid} -> {snapshot_path}")
            continue

        current_hash = compute_sha256(abs_snapshot)
        existing_meta = load_existing_metadata(meta_path)
        existing_source_meta = existing_source_metadata(existing_meta, sid)

        status = "present"
        if existing_source_meta:
            old_hash = existing_source_meta.get("content_hash_sha256", "")
            if old_hash and old_hash != current_hash:
                status = "hash_changed"

        metadata = {
            "source_id": sid,
            "snapshot_created_at": now,
            "source_url": source.get("url", ""),
            "content_hash_sha256": current_hash,
            "review_status": "needs_review" if status == "hash_changed" else "reviewed",
        }

        directory_metadata = normalize_directory_metadata(existing_meta)
        directory_metadata["sources"][sid] = metadata
        write_metadata(meta_path, directory_metadata)
        results[status].append(sid)

        label = "CHANGED" if status == "hash_changed" else "OK"
        print(f"  {label:8s} {sid} -> {snapshot_path}")

    # Summary
    print()
    print("Summary:")
    print(f"  Present:      {len(results['present'])}")
    print(f"  Missing:      {len(results['missing'])}")
    print(f"  Hash changed: {len(results['hash_changed'])}")

    if results["missing"]:
        print()
        print("Missing snapshots:")
        for s in results["missing"]:
            print(f"  - {s}")

    sys.exit(1 if results["missing"] else 0)


if __name__ == "__main__":
    main()
