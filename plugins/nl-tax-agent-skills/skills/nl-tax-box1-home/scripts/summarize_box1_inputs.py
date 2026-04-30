#!/usr/bin/env python3
"""Summarise box 1 evidence inputs from the taxpayer evidence index.

Reads workspace/taxpayer/evidence-index.yaml (falls back to .json) and
filters for evidence items relevant to box 1 income.  Outputs a summary
table and identifies gaps (missing evidence types).

Usage:
    python summarize_box1_inputs.py [--evidence-dir PATH]

Options:
    --evidence-dir PATH   Directory containing the evidence index.
                          Defaults to workspace/taxpayer.

Uses standard library only (yaml if available, json fallback).
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# YAML loader — best-effort, falls back to JSON if pyyaml is not installed
# ---------------------------------------------------------------------------

_yaml_available = False
try:
    import yaml  # type: ignore[import-untyped]

    _yaml_available = True
except ImportError:
    pass


def _load_file(path: Path) -> dict | list | None:
    """Load a YAML or JSON file and return parsed content."""
    text = path.read_text(encoding="utf-8")
    if path.suffix in (".yaml", ".yml"):
        if _yaml_available:
            return yaml.safe_load(text)
        # Attempt naive JSON parse as last resort (will fail on pure YAML).
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            print(
                f"ERROR: pyyaml is not installed and {path.name} is not valid JSON.",
                file=sys.stderr,
            )
            return None
    return json.loads(text)


# ---------------------------------------------------------------------------
# Evidence types relevant to box 1 income
# ---------------------------------------------------------------------------

BOX1_EVIDENCE_TYPES: set[str] = {
    "jaaropgaaf",
    "pensioenoverzicht",
    "uitkeringsspecificatie",
}

# Evidence types relevant to own-home (also feeds into box 1)
OWN_HOME_EVIDENCE_TYPES: set[str] = {
    "woz_beschikking",
    "hypotheek_jaaroverzicht",
}

ALL_RELEVANT_TYPES = BOX1_EVIDENCE_TYPES | OWN_HOME_EVIDENCE_TYPES

# Minimum expected evidence for a complete box 1 picture
EXPECTED_INCOME_TYPES: set[str] = {
    "jaaropgaaf",  # At least one employment/benefit jaaropgaaf
}

EXPECTED_OWN_HOME_TYPES: set[str] = {
    "woz_beschikking",
    "hypotheek_jaaroverzicht",
}


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------


def find_evidence_index(evidence_dir: Path) -> Path | None:
    """Locate the evidence index file, preferring YAML over JSON."""
    for name in ("evidence-index.yaml", "evidence-index.yml", "evidence-index.json"):
        candidate = evidence_dir / name
        if candidate.is_file():
            return candidate
    return None


def filter_box1_items(items: list[dict]) -> list[dict]:
    """Return evidence items whose type is relevant to box 1 or own-home."""
    return [
        item
        for item in items
        if item.get("evidence_type") in ALL_RELEVANT_TYPES
    ]


def identify_gaps(items: list[dict]) -> list[str]:
    """Identify missing evidence types that are expected for box 1."""
    found_types = {item.get("evidence_type") for item in items}

    gaps: list[str] = []

    # Income evidence
    if not found_types & EXPECTED_INCOME_TYPES:
        gaps.append(
            "No jaaropgaaf found. Cannot determine employment/benefit income "
            "for box 1. Upload at least one jaaropgaaf."
        )

    # Own-home evidence
    if not found_types & {"woz_beschikking"}:
        gaps.append(
            "No WOZ-beschikking found. Cannot calculate eigenwoningforfait. "
            "Upload the WOZ-beschikking if an eigen woning is applicable."
        )

    if not found_types & {"hypotheek_jaaroverzicht"}:
        gaps.append(
            "No hypotheek jaaroverzicht found. Cannot determine deductible "
            "mortgage interest. Upload the mortgage annual statement if a "
            "mortgage is applicable."
        )

    return gaps


def format_summary_table(items: list[dict]) -> str:
    """Format the filtered items as a readable summary table."""
    if not items:
        return "(no box 1 or own-home evidence items found)\n"

    # Column widths
    col_id = max(len(item.get("evidence_id", "?")) for item in items)
    col_id = max(col_id, len("evidence_id"))

    col_type = max(len(item.get("evidence_type", "?")) for item in items)
    col_type = max(col_type, len("type"))

    header = (
        f"{'evidence_id':<{col_id}}  "
        f"{'type':<{col_type}}  "
        f"{'tax_year':<9}  "
        f"{'owner':<10}  "
        f"{'confidence':<10}"
    )
    separator = "-" * len(header)

    rows = [header, separator]
    for item in items:
        eid = item.get("evidence_id", "?")
        etype = item.get("evidence_type", "?")
        tyear = str(item.get("tax_year", "?"))
        owner = item.get("owner", "?")
        conf = item.get("confidence", "?")
        if isinstance(conf, float):
            conf = f"{conf:.2f}"
        rows.append(
            f"{eid:<{col_id}}  "
            f"{etype:<{col_type}}  "
            f"{tyear:<9}  "
            f"{owner:<10}  "
            f"{str(conf):<10}"
        )

    return "\n".join(rows) + "\n"


def format_gaps(gaps: list[str]) -> str:
    """Format the gap list as readable output."""
    if not gaps:
        return "No gaps identified -- all expected box 1 evidence types are present.\n"

    lines = ["GAPS IDENTIFIED:"]
    for i, gap in enumerate(gaps, start=1):
        lines.append(f"  [{i}] {gap}")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    # Parse arguments
    evidence_dir = Path("workspace/taxpayer")

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--evidence-dir" and i + 1 < len(args):
            evidence_dir = Path(args[i + 1])
            i += 2
        else:
            print(f"Unknown argument: {args[i]}", file=sys.stderr)
            return 1

    # Locate evidence index
    index_path = find_evidence_index(evidence_dir)
    if index_path is None:
        print(
            f"ERROR: No evidence index found in {evidence_dir}. "
            f"Expected evidence-index.yaml or evidence-index.json.",
            file=sys.stderr,
        )
        return 1

    print(f"Reading evidence index: {index_path}\n")

    # Load
    data = _load_file(index_path)
    if data is None:
        return 1

    # The evidence index may be a dict with an "items" key or a bare list
    if isinstance(data, dict):
        items = data.get("items") or data.get("evidence") or []
    elif isinstance(data, list):
        items = data
    else:
        print("ERROR: Unexpected evidence index format.", file=sys.stderr)
        return 1

    if not isinstance(items, list):
        print("ERROR: Evidence items is not a list.", file=sys.stderr)
        return 1

    # Filter
    box1_items = filter_box1_items(items)

    # Summary
    print("=== Box 1 & Own-Home Evidence Summary ===\n")
    print(format_summary_table(box1_items))

    # Statistics
    income_count = sum(
        1 for it in box1_items if it.get("evidence_type") in BOX1_EVIDENCE_TYPES
    )
    home_count = sum(
        1 for it in box1_items if it.get("evidence_type") in OWN_HOME_EVIDENCE_TYPES
    )
    print(f"Income evidence items:   {income_count}")
    print(f"Own-home evidence items: {home_count}")
    print(f"Total relevant items:    {len(box1_items)}")
    print(f"Total items in index:    {len(items)}\n")

    # Gaps
    print(format_gaps(identify_gaps(box1_items)))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
