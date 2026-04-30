#!/usr/bin/env python3
"""
NL Tax Evidence Indexer — File Scanner and Hasher

Scans a directory of uploaded evidence files, computes SHA-256 hashes,
and outputs a YAML-compatible (or JSON fallback) list of file entries.

This script handles cataloging only. Classification of evidence types
is performed by the skill/model, not by this script.

Usage:
    python index_evidence.py <directory_path>
    python index_evidence.py uploads/
    python index_evidence.py /absolute/path/to/evidence

Output:
    YAML-formatted list to stdout (or JSON if PyYAML is not available).

Supported file types:
    PDF, JPG, JPEG, PNG, XLSX, XLS, CSV, MD, TXT, DOCX, XML, ODS
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
}

# Extensions that warrant a security note
MACRO_EXTENSIONS = {".xlsm", ".xltm", ".xlam"}


def compute_sha256(file_path: str) -> str:
    """Compute the SHA-256 hash of a file, reading in chunks for memory efficiency."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                sha256.update(chunk)
        return sha256.hexdigest()
    except (OSError, IOError) as e:
        return f"ERROR: {e}"


def get_file_size(file_path: str) -> int:
    """Return file size in bytes."""
    try:
        return os.path.getsize(file_path)
    except OSError:
        return -1


def scan_directory(directory: str) -> list:
    """
    Scan a directory for supported evidence files.

    Returns a list of dicts with file_path, file_sha256, file_size_bytes,
    file_extension, and file_name for each supported file found.
    """
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    entries = []
    evidence_counter = 0

    # Walk the directory tree (including subdirectories)
    for root, _dirs, files in sorted(os.walk(directory)):
        for file_name in sorted(files):
            # Skip hidden files and system files
            if file_name.startswith(".") or file_name.startswith("~"):
                continue

            file_path = os.path.join(root, file_name)
            _, ext = os.path.splitext(file_name)
            ext_lower = ext.lower()

            if ext_lower not in SUPPORTED_EXTENSIONS:
                continue

            evidence_counter += 1
            evidence_id = f"ev_{evidence_counter:03d}"

            file_hash = compute_sha256(file_path)
            file_size = get_file_size(file_path)

            entry = {
                "evidence_id": evidence_id,
                "file_path": file_path,
                "file_name": file_name,
                "file_extension": ext_lower,
                "file_sha256": file_hash,
                "file_size_bytes": file_size,
                "evidence_type": "",
                "tax_year": None,
                "owner": "taxpayer",
                "extraction_status": "indexed_only",
                "confidence": None,
                "review_required": True,
                "suspicious_content_detected": False,
                "notes": [],
            }

            # Flag macro-enabled files
            if ext_lower in MACRO_EXTENSIONS:
                entry["notes"].append(
                    f"SECURITY: File has macro-enabled extension ({ext_lower}) "
                    "— review before opening outside this tool"
                )
                entry["suspicious_content_detected"] = True

            entries.append(entry)

    return entries


def format_output(entries: list, directory: str) -> str:
    """
    Format the scanned entries as YAML (preferred) or JSON (fallback).

    Returns the formatted string.
    """
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    output_data = {
        "evidence_index_version": "1.0",
        "created_at": now,
        "updated_at": now,
        "source_directory": os.path.abspath(directory),
        "total_files": len(entries),
        "classified_files": 0,
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
        print("Usage: python index_evidence.py <directory_path>", file=sys.stderr)
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
    print(f"Output format: {'YAML' if 'yaml' in sys.modules else 'JSON'}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
