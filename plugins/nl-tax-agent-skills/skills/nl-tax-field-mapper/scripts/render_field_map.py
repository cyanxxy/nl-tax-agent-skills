#!/usr/bin/env python3
"""Render a field-map.yaml as a readable Markdown table for human review.

Usage:
    python3 render_field_map.py <path-to-field-map.yaml>

Outputs Markdown to stdout grouped by section.
"""

import math
import os
import re
import sys


def _cell(value):
    """Coerce a value into a safe single-line Markdown table cell.

    Presentation-only hardening: untrusted field-map content (which may include
    evidence quotes or notes) flows into Markdown tables, so escape characters
    that would break table structure or smuggle markup. Returns an em dash for
    empty content.
    """
    if value is None:
        return "—"
    text = str(value)
    # Collapse newlines/tabs to a single space so a cell stays on one row.
    text = re.sub(r"[\r\n\t]+", " ", text)
    # Escape backslash first, then pipe and backtick, then angle brackets.
    text = text.replace("\\", "\\\\")
    text = text.replace("|", "\\|")
    text = text.replace("`", "\\`")
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    text = text.strip()
    return text if text else "—"


def _notes(raw):
    """Render notes that may be a str, a list, or None into one cell."""
    if raw is None:
        return _cell(None)
    if isinstance(raw, (list, tuple)):
        parts = [str(item) for item in raw if item not in (None, "")]
        return _cell("; ".join(parts)) if parts else _cell(None)
    return _cell(raw)


def _confidence(raw):
    """Format a confidence as a percentage, tolerating non-numeric input."""
    if raw is None or isinstance(raw, bool):
        return "—"
    try:
        value = float(raw)
        if not math.isfinite(value):
            return "—"
        return f"{value:.0%}"
    except (TypeError, ValueError):
        return _cell(raw)


def load_yaml(path):
    """Load YAML via PyYAML; require it rather than silently mis-parsing."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    try:
        import yaml
    except ImportError:
        raise SystemExit(
            "PyYAML is required to render the field map "
            "(python3 -m pip install pyyaml). If PyYAML is unavailable on this host, "
            "present the field map to the user directly from the YAML you wrote."
        )
    try:
        return yaml.safe_load(content)
    except yaml.YAMLError as exc:
        raise SystemExit(f"Error: invalid YAML in {path}: {exc}")


def infer_section(field_id):
    """Infer a display section from the field_id."""
    parts = str(field_id or "").lower().split(".")
    section_map = {
        # Canonical field_id first-part prefixes
        # (reference/annual-field-map.md, reference/provisional-field-map.md).
        "personal": "Personal",
        "box1": "Box 1",
        "box2": "Box 2",
        "box3": "Box 3",
        "onderneming": "Winst uit onderneming",
        "business": "Winst uit onderneming",
        "eigenwoning": "Eigen Woning",
        "aftrek": "Deductions",
        "partner": "Partner",
        # Descriptive aliases (kept for non-canonical or legacy ids).
        "income": "Income",
        "wages": "Income",
        "pension": "Income",
        "benefits": "Income",
        "home": "Eigen Woning",
        "mortgage": "Eigen Woning",
        "woz": "Eigen Woning",
        "bank": "Box 3",
        "assets": "Box 3",
        "schulden": "Box 3",
        "deductions": "Deductions",
        "giften": "Deductions",
        "zorgkosten": "Deductions",
        "alimentatie": "Deductions",
        "lijfrente": "Deductions",
    }
    for part in parts:
        if part in section_map:
            return section_map[part]
    return "Other"


def render(data):
    """Render field map data as Markdown."""
    if not isinstance(data, dict):
        raise SystemExit(
            "Error: field map must be a YAML mapping at the top level "
            f"(got {type(data).__name__})."
        )
    workflow = data.get("workflow", "unknown")
    tax_year = data.get("tax_year", "unknown")
    created = data.get("created_at", "unknown")

    lines = []
    lines.append(f"# Field Map — {workflow} {tax_year}")
    lines.append(f"")
    lines.append(f"**Workflow:** {workflow}")
    lines.append(f"**Tax year:** {tax_year}")
    lines.append(f"**Created:** {created}")
    lines.append("")

    fields = data.get("fields", [])
    if not isinstance(fields, list):
        fields = []
    fields = [f for f in fields if isinstance(f, dict)]
    if not fields:
        lines.append("_No fields mapped._")
    else:
        # Group by section
        sections = {}
        for field in fields:
            fid = field.get("field_id", "")
            section = infer_section(fid)
            sections.setdefault(section, []).append(field)

        for section_name in sorted(sections.keys()):
            section_fields = sections[section_name]
            lines.append(f"## {section_name}")
            lines.append("")
            lines.append("| Field | Value | Source | Confidence | Review | Notes |")
            lines.append("|-------|-------|--------|------------|--------|-------|")
            for f in section_fields:
                label = _cell(f.get("label", f.get("field_id")))
                raw_value = f.get("value")
                value = "_missing_" if raw_value is None else _cell(raw_value)
                source = f.get("source", {})
                src_raw = source.get("type") if isinstance(source, dict) else source
                src_type = _cell(src_raw)
                conf_str = _confidence(f.get("confidence"))
                review = "Yes" if f.get("manual_review_required", True) else "No"
                notes = _notes(f.get("notes"))
                lines.append(f"| {label} | {value} | {src_type} | {conf_str} | {review} | {notes} |")
            lines.append("")

    # Missing fields
    missing = data.get("missing_fields", [])
    if not isinstance(missing, list):
        missing = []
    missing = [m for m in missing if isinstance(m, dict)]
    if missing:
        lines.append("## Missing Fields")
        lines.append("")
        lines.append("| Field | Reason | Blocking |")
        lines.append("|-------|--------|----------|")
        for m in missing:
            label = _cell(m.get("label", m.get("field_id")))
            reason = _cell(m.get("reason"))
            blocking = "Yes" if m.get("blocking", True) else "No"
            lines.append(f"| {label} | {reason} | {blocking} |")
        lines.append("")

    return "\n".join(lines)


def main():
    if "-h" in sys.argv[1:] or "--help" in sys.argv[1:]:
        print("render_field_map.py — render a field-map.yaml as a Markdown table")
        print("Usage: python3 render_field_map.py <path-to-field-map.yaml>")
        sys.exit(0)

    if len(sys.argv) < 2:
        print("Usage: python3 render_field_map.py <path-to-field-map.yaml>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.isfile(path):
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    data = load_yaml(path)
    print(render(data))


if __name__ == "__main__":
    main()
