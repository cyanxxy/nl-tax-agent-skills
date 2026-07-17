#!/usr/bin/env python3
"""Build lossless human-subject projections of reviewed portal-flow notes.

The reviewed notes remain the attested provenance snapshots. Runtime projections
copy their bodies exactly and insert only ``**Taxpayer:**`` before portal-action
imperatives so an agent never receives a bare authenticated-portal instruction.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
PLUGIN = REPO / "plugins" / "nl-tax-agent-skills"
KNOWLEDGE = PLUGIN / "skills/_shared/knowledge/years/2026/provisional"
OUTPUT = (
    PLUGIN
    / "skills/nl-tax-provisional-assessment/reference/source-projections"
)


@dataclass(frozen=True)
class Projection:
    source_name: str
    output_name: str
    source_ids: tuple[str, ...]


PROJECTIONS = (
    Projection(
        "request-flow.md",
        "request-flow-human.md",
        ("bd_provisional_landing_2026", "bd_provisional_request_2026"),
    ),
    Projection(
        "change-flow.md",
        "change-flow-human.md",
        ("bd_provisional_change_2026",),
    ),
    Projection(
        "stopzetten-flow.md",
        "stopzetten-flow-human.md",
        ("bd_provisional_stopzetten_2026",),
    ),
)

ACTION_LINE = re.compile(
    r"^(?P<indent>\s*)(?P<marker>(?:\d+\. |- )?)"
    r"(?P<action>(?:Prepare|Log in|Enter|Review|Verify|Sign and send|Open|Choose|"
    r"Navigate|Select|Confirm)\b.*)$"
)
BODY_MARKER = "## Rule\n"
SUBJECT_PREFIX = "**Taxpayer:** "


def reviewed_body(source_text: str, source_path: Path) -> str:
    offset = source_text.find(BODY_MARKER)
    if offset < 0:
        raise ValueError(f"reviewed note has no {BODY_MARKER.strip()!r}: {source_path}")
    return source_text[offset:]


def add_human_subjects(body: str) -> str:
    lines = []
    for line in body.splitlines(keepends=True):
        content = line[:-1] if line.endswith("\n") else line
        newline = "\n" if line.endswith("\n") else ""
        match = ACTION_LINE.match(content)
        if match and SUBJECT_PREFIX not in content:
            content = (
                match.group("indent")
                + match.group("marker")
                + SUBJECT_PREFIX
                + match.group("action")
            )
        lines.append(content + newline)
    return "".join(lines)


def strip_human_subjects(projected_body: str) -> str:
    """Reverse the one allowed transform for regression verification."""
    return re.sub(
        r"^(\s*(?:\d+\. |- )?)\*\*Taxpayer:\*\* ",
        r"\1",
        projected_body,
        flags=re.MULTILINE,
    )


def render_projection(config: Projection) -> str:
    source_path = KNOWLEDGE / config.source_name
    source_bytes = source_path.read_bytes()
    source_text = source_bytes.decode("utf-8")
    digest = hashlib.sha256(source_bytes).hexdigest()
    relative_source = source_path.relative_to(PLUGIN).as_posix()
    header = (
        f"# Human-only runtime projection: {config.source_name}\n\n"
        'projection_version: "1"\n'
        f"derived_from: {relative_source}\n"
        f"derived_note_sha256: {digest}\n"
        f"source_ids: {', '.join(config.source_ids)}\n\n"
        "This is a mechanically reversible runtime projection, not an "
        "independently reviewed tax note. The cited reviewed snapshot remains "
        "the provenance authority. The only permitted body transformation is "
        "inserting `**Taxpayer:**` before portal-action imperatives.\n\n"
    )
    return header + add_human_subjects(reviewed_body(source_text, source_path))


def build() -> tuple[Path, ...]:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    written = []
    for config in PROJECTIONS:
        destination = OUTPUT / config.output_name
        destination.write_text(render_projection(config), encoding="utf-8")
        written.append(destination)
    return tuple(written)


def main() -> None:
    for path in build():
        print(path)


if __name__ == "__main__":
    main()
