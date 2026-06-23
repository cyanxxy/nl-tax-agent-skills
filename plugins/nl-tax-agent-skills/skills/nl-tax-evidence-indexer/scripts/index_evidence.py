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

Security model:
    All uploaded content is untrusted. The catalog gate is extension-based;
    extensions are NOT a trust signal — type safety must never be inferred from
    an extension. Symlinks are never followed, files reached outside the scanned
    directory are skipped, and a small fixed marker scan over text-like files
    provides defense-in-depth flagging only (it never quarantines or suppresses
    legitimate data). Resource limits cap the number/size of files processed.
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

# Extensions that warrant an active-content / macro security note.
# .xls is a legacy binary spreadsheet format that can carry VBA macros, so it
# is flagged alongside the explicitly macro-enabled OOXML extensions.
MACRO_EXTENSIONS = {".xlsm", ".xltm", ".xlam", ".xls"}

# Text-like extensions whose first bytes we scan for adversarial markers.
# Binary formats are NEVER decoded here.
TEXT_LIKE_EXTENSIONS = {".txt", ".md", ".csv", ".xml"}

# Small fixed marker list for defense-in-depth content scanning. A hit only
# sets a flag — it never suppresses data and never quarantines a file.
CONTENT_MARKERS = (
    "ignore previous instructions",
    "system prompt:",
    "<script",
    "__import__",
)

# Cap on bytes read for the marker scan (per file).
MARKER_SCAN_MAX_BYTES = 64 * 1024  # 64 KiB

# Resource limits — on a tripped limit we skip the file with a note, never abort.
MAX_FILES = 500
MAX_FILE_BYTES = 50 * 1024 * 1024            # 50 MiB per file
MAX_TOTAL_BYTES = 2 * 1024 * 1024 * 1024     # 2 GiB cumulative budget
MAX_DEPTH = 10                               # directory recursion depth


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


def scan_text_markers(file_path: str):
    """Scan the first MARKER_SCAN_MAX_BYTES of a text-like file for markers.

    Returns a list of matched marker strings (possibly empty). Binary formats
    must not be passed here. Decoding uses errors='replace' and never raises.
    """
    hits = []
    try:
        with open(file_path, "rb") as f:
            raw = f.read(MARKER_SCAN_MAX_BYTES)
    except (OSError, IOError):
        return hits
    text = raw.decode("utf-8", errors="replace").lower()
    for marker in CONTENT_MARKERS:
        if marker in text:
            hits.append(marker)
    return hits


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
    """
    Scan a directory for supported evidence files.

    Returns a list of dicts with relative file_path, file_sha256,
    file_size_bytes, file_extension, and file_name for each supported file.

    Security guarantees:
        - Symlinks and non-regular files are skipped and never followed.
        - Files whose real path resolves outside the scanned directory are
          skipped (no symlink escape via directory components).
        - Resource limits (file count, per-file size, total bytes, depth) skip
          offending files with a note rather than aborting the scan.
    """
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    base = os.path.realpath(directory)
    entries = []
    seen_ids = set()
    file_count = 0
    total_bytes = 0
    limit_notes = []

    # Walk the directory tree (including subdirectories). followlinks defaults
    # to False, so symlinked directories are not descended into.
    for root, dirs, files in sorted(os.walk(directory)):
        # Enforce recursion depth relative to the scanned directory.
        rel_root = os.path.relpath(root, directory)
        depth = 0 if rel_root == "." else rel_root.count(os.sep) + 1
        if depth >= MAX_DEPTH:
            # Do not descend further; record once and stop pruning chatter.
            dirs[:] = []
            limit_notes.append(
                f"SECURITY: directory depth limit ({MAX_DEPTH}) reached at "
                f"'{rel_root}' — deeper files not scanned"
            )
            continue
        # Keep traversal deterministic.
        dirs.sort()

        for file_name in sorted(files):
            # Skip hidden files and editor/backup temp files.
            if file_name.startswith(".") or file_name.startswith("~"):
                continue

            file_path = os.path.join(root, file_name)
            _, ext = os.path.splitext(file_name)
            ext_lower = ext.lower()

            if ext_lower not in SUPPORTED_EXTENSIONS:
                continue

            # --- Symlink / non-regular-file containment (HI-12) ---
            if os.path.islink(file_path) or not os.path.isfile(file_path):
                entry = _make_skipped_entry(
                    directory, file_path, file_name, ext_lower, seen_ids,
                    "SECURITY: symlink/non-regular file skipped (not followed)",
                )
                entries.append(entry)
                continue

            # Containment: the resolved real path must stay inside base.
            real = os.path.realpath(file_path)
            try:
                if os.path.commonpath([base, real]) != base:
                    entry = _make_skipped_entry(
                        directory, file_path, file_name, ext_lower, seen_ids,
                        "SECURITY: path resolves outside the scanned directory "
                        "— skipped (not followed)",
                    )
                    entries.append(entry)
                    continue
            except ValueError:
                # commonpath raises on paths on different drives (Windows).
                entry = _make_skipped_entry(
                    directory, file_path, file_name, ext_lower, seen_ids,
                    "SECURITY: path resolves to a different drive/root "
                    "— skipped (not followed)",
                )
                entries.append(entry)
                continue

            # --- Resource limits (ME-18) ---
            if file_count >= MAX_FILES:
                limit_notes.append(
                    f"SECURITY: file count limit ({MAX_FILES}) reached "
                    f"— '{os.path.relpath(file_path, directory)}' and later "
                    "files were skipped"
                )
                # Stop processing further files entirely.
                return entries

            file_size = get_file_size(file_path)
            if file_size > MAX_FILE_BYTES:
                entry = _make_skipped_entry(
                    directory, file_path, file_name, ext_lower, seen_ids,
                    f"SECURITY: file size {file_size} bytes exceeds per-file "
                    f"limit ({MAX_FILE_BYTES}) — skipped (not hashed)",
                )
                entries.append(entry)
                continue

            if file_size >= 0 and total_bytes + file_size > MAX_TOTAL_BYTES:
                entry = _make_skipped_entry(
                    directory, file_path, file_name, ext_lower, seen_ids,
                    f"SECURITY: cumulative byte budget ({MAX_TOTAL_BYTES}) "
                    "would be exceeded — skipped (not hashed)",
                )
                entries.append(entry)
                continue

            # --- Hash + catalog ---
            file_hash = compute_sha256(file_path)
            file_count += 1
            if file_size >= 0:
                total_bytes += file_size

            rel_path = os.path.relpath(file_path, directory)
            evidence_id = _make_evidence_id(file_hash, rel_path, seen_ids)

            entry = _new_entry(
                evidence_id, rel_path, file_name, ext_lower, file_hash, file_size
            )

            if file_hash is None:
                # Hash failure (ME-19): never store an error string in the hash.
                entry["file_sha256"] = None
                entry["extraction_status"] = "failed"
                entry["review_required"] = True
                entry["notes"].append(
                    "SECURITY: file could not be read/hashed — extraction "
                    "marked failed; verify the file manually"
                )

            # Flag macro-enabled / active-content files.
            if ext_lower in MACRO_EXTENSIONS:
                if ext_lower == ".xls":
                    entry["notes"].append(
                        "SECURITY: legacy .xls binary spreadsheet may contain "
                        "VBA macros — review before opening outside this tool"
                    )
                else:
                    entry["notes"].append(
                        f"SECURITY: File has macro-enabled extension "
                        f"({ext_lower}) — review before opening outside this tool"
                    )
                entry["suspicious_content_detected"] = True

            # Defense-in-depth content marker scan (text-like extensions only).
            if file_hash is not None and ext_lower in TEXT_LIKE_EXTENSIONS:
                hits = scan_text_markers(file_path)
                if hits:
                    entry["suspicious_content_detected"] = True
                    entry["notes"].append(
                        "SECURITY: adversarial marker(s) found in file content "
                        f"({', '.join(sorted(set(hits)))}) — flagged only; "
                        "content was NOT followed and legitimate data is kept"
                    )

            entries.append(entry)

    # Attach any directory-level limit notes to a synthetic note carrier so the
    # information is not lost. We surface them via stderr in main(); also leave
    # them discoverable by stashing on the function attribute for callers.
    scan_directory.last_limit_notes = limit_notes
    return entries


# Default attribute so callers can read it even before a scan runs.
scan_directory.last_limit_notes = []


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
        "owner": "taxpayer",
        "extraction_status": "indexed_only",
        "confidence": None,
        "review_required": True,
        "suspicious_content_detected": False,
        "notes": [],
        "extracted_fields": {},
    }


def _make_skipped_entry(directory, file_path, file_name, ext_lower, seen_ids, note):
    """Build a cataloged-but-skipped entry (no hash, not processed).

    Used for symlinks/non-regular files, containment failures, and tripped
    resource limits. The id is derived from the relative path so it is stable
    and never collides with content-hash ids.
    """
    rel_path = os.path.relpath(file_path, directory)
    evidence_id = _make_evidence_id(None, rel_path, seen_ids)
    entry = _new_entry(evidence_id, rel_path, file_name, ext_lower, None, -1)
    entry["extraction_status"] = "failed"
    entry["suspicious_content_detected"] = True
    entry["notes"].append(note)
    return entry


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
        "suspicious_count": sum(
            1 for e in entries if e["suspicious_content_detected"]
        ),
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

    entries = scan_directory(directory)

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
    suspicious = sum(1 for e in entries if e["suspicious_content_detected"])
    if suspicious:
        print(f"Suspicious files: {suspicious}", file=sys.stderr)
    for note in getattr(scan_directory, "last_limit_notes", []):
        print(note, file=sys.stderr)
    print(f"Output format: {'YAML' if 'yaml' in sys.modules else 'JSON'}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
