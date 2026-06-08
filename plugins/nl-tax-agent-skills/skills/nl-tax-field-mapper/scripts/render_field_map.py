#!/usr/bin/env python3
"""Render a field-map.yaml as a readable Markdown table for human review.

Usage:
    python3 render_field_map.py <path-to-field-map.yaml>

Outputs Markdown to stdout grouped by section.
"""

import os
import sys

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
    return yaml.safe_load(content)


def infer_section(field_id):
    """Infer a display section from the field_id."""
    parts = field_id.lower().split(".")
    section_map = {
        # Canonical field_id first-part prefixes
        # (reference/annual-field-map.md, reference/provisional-field-map.md).
        "personal": "Personal",
        "box1": "Box 1",
        "box2": "Box 2",
        "box3": "Box 3",
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
                label = f.get("label", f.get("field_id", "—"))
                value = f.get("value", "—")
                if value is None:
                    value = "_missing_"
                source = f.get("source", {})
                src_type = source.get("type", "—") if isinstance(source, dict) else str(source)
                confidence = f.get("confidence")
                conf_str = f"{confidence:.0%}" if confidence is not None else "—"
                review = "Yes" if f.get("manual_review_required", True) else "No"
                notes = "; ".join(f.get("notes", [])) or "—"
                lines.append(f"| {label} | {value} | {src_type} | {conf_str} | {review} | {notes} |")
            lines.append("")

    # Missing fields
    missing = data.get("missing_fields", [])
    if missing:
        lines.append("## Missing Fields")
        lines.append("")
        lines.append("| Field | Reason | Blocking |")
        lines.append("|-------|--------|----------|")
        for m in missing:
            label = m.get("label", m.get("field_id", "—"))
            reason = m.get("reason", "—")
            blocking = "Yes" if m.get("blocking", True) else "No"
            lines.append(f"| {label} | {reason} | {blocking} |")
        lines.append("")

    return "\n".join(lines)


def main():
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
