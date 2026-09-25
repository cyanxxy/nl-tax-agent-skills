#!/usr/bin/env python3
"""
NL Tax Evidence Indexer — File Scanner and Hasher

Scans a directory of uploaded evidence files, computes SHA-256 hashes,
and outputs a YAML-compatible (or JSON fallback) list of file entries.

This script handles cataloging only. Classification of evidence types
is performed by the skill/model, not by this script.

Usage:
    python3 index_evidence.py <directory_path>
    python3 index_evidence.py uploads/
    python3 index_evidence.py /absolute/path/to/evidence

Output:
    YAML-formatted list to stdout (or JSON if PyYAML is not available).

Supported file types:
    PDF, JPG, JPEG, PNG, XLSX, XLS, XLSM, XLTM, XLAM, CSV, MD, TXT, DOCX, XML, ODS

This script catalogs and hashes only; it reads content as data and performs no
sandboxing or content inspection of its own — the host environment owns
operational file-handling safety.
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone

# Supported file extensions (lowercase)
SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png",
    ".xlsx",
    ".xls",
    ".xlsm",
    ".csv",
    ".md",
    ".txt",
    ".docx",
    ".xml",
    ".ods",
    ".xltm",
    ".xlam",
}

def compute_sha256(file_path: str):
    """Compute the SHA-256 hash of a file, reading in chunks.

    Returns the lowercase hex digest, or None on any read failure. Never
    returns an error string — callers treat None as "hash unavailable".
    """
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                sha256.update(chunk)
        return sha256.hexdigest()
    except (OSError, IOError):
        return None


def get_file_size(file_path: str) -> int:
    """Return file size in bytes, or -1 if it cannot be determined."""
    try:
        return os.path.getsize(file_path)
    except OSError:
        return -1


def _make_evidence_id(digest, rel_path: str, seen_ids: set) -> str:
    """Derive a stable evidence_id from the content hash.

    Stability goal: an item's id depends only on its own content (or, if the
    hash failed, its own path) — not on scan order — so adding, deleting, or
    renaming OTHER files does not renumber this item. Caveat: two files with
    IDENTICAL content share a base id, so their _2/_3/... collision suffix is
    assigned in scan order; reordering such duplicates can swap their suffixes.
    """
    if digest:
        basis = digest
    else:
        # Hash failed — fall back to a hash of the relative path so the id is
        # still deterministic for this file.
        basis = hashlib.sha256(rel_path.encode("utf-8")).hexdigest()
    base_id = "ev_" + basis[:10]
    candidate = base_id
    suffix = 1
    while candidate in seen_ids:
        suffix += 1
        candidate = f"{base_id}_{suffix}"
    seen_ids.add(candidate)
    return candidate


def scan_directory(directory: str) -> list:
    """Scan a directory for supported evidence files.

    Returns a list of dicts with relative file_path, file_sha256,
    file_size_bytes, file_extension, and file_name for each supported file.
    Classification of evidence types is left to the skill/model. This catalogs
    and hashes only — operational file-handling safety is the host's job.
    """
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    entries = []
    seen_ids = set()

    for root, dirs, files in os.walk(directory):
        # In-place edits steer os.walk: sort for deterministic traversal and
        # prune hidden directories (e.g. .stversions, .backup) to match the
        # hidden-file skip below.
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        for file_name in sorted(files):
            # Skip hidden files and editor/backup temp files.
            if file_name.startswith(".") or file_name.startswith("~"):
                continue

            file_path = os.path.join(root, file_name)
            _, ext = os.path.splitext(file_name)
            ext_lower = ext.lower()
            if ext_lower not in SUPPORTED_EXTENSIONS:
                continue

            file_size = get_file_size(file_path)
            file_hash = compute_sha256(file_path)
            rel_path = os.path.relpath(file_path, directory)
            evidence_id = _make_evidence_id(file_hash, rel_path, seen_ids)

            entry = _new_entry(
                evidence_id, rel_path, file_name, ext_lower, file_hash, file_size
            )

            if file_hash is None:
                # Hash failure: never store an error string in the hash field.
                entry["file_sha256"] = None
                entry["extraction_status"] = "failed"
                entry["review_required"] = True
                entry["notes"].append(
                    "file could not be read/hashed — extraction marked failed; "
                    "verify the file manually"
                )

            entries.append(entry)

    return entries


def index_directory(directory: str) -> list:
    """Inventory a user-selected directory without classifying its files.

    This named entry point makes the script's deliberately narrow contract
    explicit: the returned rows contain file metadata and an optional hash;
    classification remains agent work.
    """
    return scan_directory(directory)


def _new_entry(evidence_id, rel_path, file_name, ext_lower, file_hash, file_size):
    """Build a fully-populated evidence entry dict with default fields."""
    return {
        "evidence_id": evidence_id,
        "source": "file",
        "file_path": rel_path,
        "file_name": file_name,
        "file_extension": ext_lower,
        "file_sha256": file_hash,
        "file_size_bytes": file_size,
        "quote": None,
        "stated_at": None,
        "evidence_type": "",
        "tax_year": None,
        "owner": None,
        "extraction_status": "indexed_only",
        "confidence": None,
        "review_required": True,
        "notes": [],
        "extracted_fields": {},
    }


def format_output(entries: list, directory: str) -> str:
    """
    Format the scanned entries as YAML (preferred) or JSON (fallback).

    Returns the formatted string. The source_directory is recorded as the
    basename only (relative convention) — the absolute host path is not stored.
    """
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    output_data = {
        "evidence_index_version": "1.1",
        "created_at": now,
        "updated_at": now,
        "source_directory": os.path.basename(os.path.normpath(directory)) or ".",
        "total_files": len(entries),
        "classified_files": 0,
        "user_chat_items": 0,
        "review_required_count": sum(1 for e in entries if e["review_required"]),
        "check_performed_by": "checked_by_script",
        "items": entries,
    }

    # Try YAML first, fall back to JSON
    try:
        import yaml

        return yaml.dump(
            output_data,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )
    except ImportError:
        return json.dumps(output_data, indent=2, ensure_ascii=False, default=str)


def main():
    if "-h" in sys.argv[1:] or "--help" in sys.argv[1:]:
        print("index_evidence.py — catalog a directory of tax evidence into a YAML/JSON index")
        print("Usage: python3 index_evidence.py <directory_path>")
        sys.exit(0)

    if len(sys.argv) < 2:
        print("Usage: python3 index_evidence.py <directory_path>", file=sys.stderr)
        print("", file=sys.stderr)
        print("Scans a directory of tax evidence files and outputs a", file=sys.stderr)
        print(
            "YAML/JSON index with file paths, SHA-256 hashes, and sizes.",
            file=sys.stderr,
        )
        sys.exit(1)

    directory = sys.argv[1]

    # Resolve relative paths
    if not os.path.isabs(directory):
        directory = os.path.abspath(directory)

    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.", file=sys.stderr)
        sys.exit(1)

    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    entries = index_directory(directory)

    if not entries:
        print(
            f"Warning: No supported files found in '{directory}'.", file=sys.stderr
        )
        print("Supported extensions: " + ", ".join(sorted(SUPPORTED_EXTENSIONS)),
              file=sys.stderr)

    output = format_output(entries, directory)
    print(output)

    # Print summary to stderr (so stdout stays clean for piping)
    print(f"\n--- Summary ---", file=sys.stderr)
    print(f"Directory: {os.path.abspath(directory)}", file=sys.stderr)
    print(f"Files found: {len(entries)}", file=sys.stderr)
    print(f"Output format: {'YAML' if 'yaml' in sys.modules else 'JSON'}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
