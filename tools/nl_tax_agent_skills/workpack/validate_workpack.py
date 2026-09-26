#!/usr/bin/env python3
"""Repository grader for a 0.4 NL tax workpack (Markdown with two YAML appendices).

The installed plugin ships no code: at runtime the owning workflow runs its own
agent checklist and the taxpayer reviews the result. This grader is repository
tooling for tests and the offline eval verifier. It checks the binding 0.4
structure from ``docs/maintainers/0.4-conversation-first-design.md``:

- the required top-level sections (R4), in template order, taken from
  ``nl-tax-annual-return/templates/annual-workpack.md`` or
  ``nl-tax-provisional-assessment/templates/provisional-workpack.md``;
- Appendix A, the resume record (R5): exact keys, format/version, the
  workflow <-> tax-year pairing, exact section keys for the workflow, and the
  status/readiness vocabulary, reconciled with the STATUS banner (R6);
- ``## Sources used`` equals Appendix A ``sources_loaded`` and names registered
  sources of the right workflow;
- every ``ev_NNN`` reference (``F:ev_NNN``, a field-map ``evidence_id``) is a
  row in ``## Documents and sources``; every open Q-ID is a row in
  ``## Open questions``;
- Appendix B holds the literal ``not yet mapped`` or exactly one fenced YAML
  field map for the same workflow (review and stopzetten never map) (R7);
- once Appendix B holds a map, ``## Field map summary`` is the checked surface
  (review amendment A12): it must hold the summary table
  ``| Portal section | Portal label | field_id | Value to enter | Source | Review |``
  defined in ``nl-tax-field-mapper/reference/mapper-flow.md``; every
  ``manual_entry`` field (any entry_mode except ``internal_routing``) appears
  with an equal value after normalization (``EUR``/``€``, thousands separators
  ``.`` and ``,``, decimals, whitespace), a double-entry fact may appear once per
  screen path but always with that value, every ``missing_fields`` entry (and
  every field without a value) appears as a ``MISSING - enter manually`` row
  naming its Q-ID, and no row names a ``field_id`` that Appendix B lacks or an
  ``internal_routing`` record. A requested ``## Manual-entry checklist`` step
  table (``field_id`` and ``Value to enter`` columns) must agree with Appendix B
  the same way unless the checklist is stale;
- stale outputs (review amendment A10): a line ``STALE — predates the change to
  <fact> (<YYYY-MM-DD>); regenerate before use.`` in ``Field map summary``,
  Appendix B (outside the yaml block), or ``Manual-entry checklist`` is valid only
  while Appendix A ``generation_confirmed`` is ``false``; and a mapped workpack
  whose ``generation_confirmed`` is ``false`` must carry that line in the summary,
  in Appendix B, and in a requested checklist, because mapping only follows a
  confirmed generation;
- no BSN-like 9-digit number, IBAN, or file hash; no cross-workflow workpack
  path; no werkelijk-rendement collection in a provisional workpack.

With ``presentation="chat"`` (CLI ``--chat``) it grades a harness capture of the
workpack as shown in the conversation instead of a saved file (review amendment
A8): the rendering holds only filled sections, no template fill notes or
bracketed placeholders, and never Appendix A, Appendix B, or any YAML block.
The resume-record and Appendix B checks are skipped there because the rendering
has neither, and ``Manual-entry checklist`` may be absent. How chat mode knows
whether mapping ran (A12): a conversation rendering of an annual, provisional
request, or provisional change workpack must always state the map's state in
``## Field map summary`` — the literal ``not yet mapped`` before mapping, or the
summary table once mapping has run. Removing the section is an error, and any
mapped-state marker in it (a summary table, a ``Readiness:`` line, or a STALE
line) requires the well-formed table and forbids ``not yet mapped``. Review and
stopzetten renderings may omit the section. Without Appendix B, the table is
checked for internal consistency (field_id and value in every row, one value
per field_id, a Q-ID on every ``MISSING - enter manually`` row), and a
requested, non-stale checklist must show the summary's values; a stale summary
requires the STALE line on a requested checklist too.

The field-map rules themselves are graded by
``tools/nl_tax_agent_skills/field_mapper/validate_field_map.py``.

Usage::

    python3 tools/nl_tax_agent_skills/workpack/validate_workpack.py \
        [--kind annual|provisional] [--expect-saved | --chat] [--plugin-root DIR] \
        <workpack.md> [<workpack.md> ...]

Exit status 0 when every workpack is valid, 1 otherwise.
"""

from __future__ import annotations

import argparse
import datetime as dt
import decimal
import functools
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - maintainer environment has PyYAML.
    raise SystemExit("PyYAML is required: python3 -m pip install pyyaml") from exc


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_PLUGIN_ROOT = REPO_ROOT / "plugins" / "nl-tax-agent-skills"

TEMPLATE_PATHS = {
    "annual": "skills/nl-tax-annual-return/templates/annual-workpack.md",
    "provisional": "skills/nl-tax-provisional-assessment/templates/provisional-workpack.md",
}
PROVISIONAL_FLOW_PATH = "skills/nl-tax-provisional-assessment/reference/provisional-flow.md"
SOURCE_REGISTER_PATH = "skills/nl-tax-shared-resources/source-register.yaml"

# R3: the only files the plugin may write, relative to the working folder.
WORKPACK_PATHS = {
    "annual": "workspace/nl-tax-annual-2025-workpack.md",
    "provisional": "workspace/nl-tax-provisional-2026-workpack.md",
}
WORKPACK_FILENAMES = {kind: Path(path).name for kind, path in WORKPACK_PATHS.items()}
WORKPACK_STEMS = {kind: Path(path).stem for kind, path in WORKPACK_PATHS.items()}

WORKPACK_FORMAT = "nl-tax-workpack"
RESUME_RECORD_KEYS = (
    "workpack_format",
    "workpack_version",
    "plugin_version",
    "workflow",
    "tax_year",
    "created_at",
    "updated_at",
    "save_consent",
    "readiness",
    "generation_confirmed",
    "queued_workflow",
    "sections",
    "sources_loaded",
)
STATUS_VALUES = ("not_started", "in_progress", "complete", "chat_only", "deferred")
DONE_STATUSES = {"complete", "chat_only"}
READINESS_VALUES = ("draft", "review_ready")
SAVE_CONSENT_VALUES = ("given", "not_given")

ANNUAL_WORKFLOW = "annual_2025"
PROVISIONAL_SUBFLOWS = ("request", "change", "review", "stopzetten")
PROVISIONAL_WORKFLOWS = tuple(f"provisional_2026_{name}" for name in PROVISIONAL_SUBFLOWS)
TAX_YEARS = {"annual": 2025, "provisional": 2026}
FIELD_MAP_WORKFLOWS = {"annual": "annual_return", "provisional": "provisional_assessment"}
NO_FIELD_MAP_SUBFLOWS = {"review", "stopzetten"}
# A stopzetten payment case redirected to change keeps its completed
# `stopzetten_direction` section (provisional subflows/stopzetten.md, step 4).
OPTIONAL_SECTION_KEYS = {"provisional_2026_change": {"stopzetten_direction"}}

PRESENTATIONS = ("file", "chat")
# A8: a conversation rendering never shows the YAML appendices, and may omit the
# sections that are still placeholders (the map summary before mapping, an
# unrequested checklist).
CHAT_EXCLUDED_SECTIONS = frozenset({"appendix a - resume record", "appendix b - field map"})
CHAT_OPTIONAL_SECTIONS = frozenset({"field map summary", "manual-entry checklist"})
# A line that opens with a bracket and is neither a checkbox nor a Markdown
# link is a template fill note or placeholder left in the rendering.
FILL_NOTE_LINE = re.compile(r"^\s*(?:\[(?![ xX]\])(?![^\]\n]*\]\()|<!--)")

NOT_YET_MAPPED = "not yet mapped"
PROVISIONAL_BOX3_NOTE = "Werkelijk rendement is not part of provisional 2026."
PROVISIONAL_BOX3_REDIRECT = (
    "Werkelijk rendement may become relevant when filing the annual 2026 return in 2027."
)

# A12: the Field map summary table (nl-tax-field-mapper/reference/mapper-flow.md).
SUMMARY_HEADERS = ("portal section", "portal label", "field_id", "value to enter", "source", "review")
MISSING_MARKER = "missing - enter manually"
MAPPING_SUBFLOWS = ("request", "change")
NOT_REQUESTED = "not requested"
INTERNAL_ROUTING = "internal_routing"
# A10: the visible stale line added after a changed fact.
STALE_TEMPLATE = "STALE — predates the change to <fact> (<YYYY-MM-DD>); regenerate before use."
STALE_START = re.compile(r"^STALE\b")
STALE_MARKER = re.compile(
    r"^STALE\s*(?:—|–|--|-)\s*predates the change to \S.*?\s\((\d{4}-\d{2}-\d{2})\);?\s*"
    r"regenerate before use\.?$"
)
READINESS_LINE = re.compile(r"(?im)^[\s>*_`]*readiness[*_`]*\s*:\s*[*_`]*\s*([a-z_]+)")
TRUE_WORDS = {"true", "yes", "ja", "y"}
FALSE_WORDS = {"false", "no", "nee", "n"}

EVIDENCE_ROW_ID = re.compile(r"^ev_\d+$")
EVIDENCE_REFERENCE = re.compile(r"(?<![A-Za-z0-9_])ev_\d+\b")
QUESTION_ID = re.compile(r"^Q\d+$")
SOURCE_ID = re.compile(r"^[a-z][a-z0-9_]*$")
PLUGIN_VERSION = re.compile(r"^\d+\.\d+\.\d+$")
WORKPACK_VERSION = re.compile(r"^2\.\d+$")

# Privacy: a BSN is nine digits (optionally dotted 1234.56.789). Decimal
# amounts and longer digit runs are not BSN-like.
BSN_LIKE = re.compile(r"(?<![\w.,])(?:\d{9}|\d{4}\.\d{2}\.\d{3})(?![\w]|[.,]\d)")
DUTCH_IBAN = re.compile(r"(?i)\bNL\d{2}\s?[A-Z]{4}\s?\d{4}\s?\d{4}\s?\d{2}\b")
GENERIC_IBAN = re.compile(r"\b[A-Z]{2}\d{2}(?:\s?[A-Z0-9]{4}){2,7}(?:\s?[A-Z0-9]{1,3})?\b")
FILE_HASH = re.compile(r"(?i)(?<![0-9a-f])(?:[0-9a-f]{64}|[0-9a-f]{40})(?![0-9a-f])")
WERKELIJK_RENDEMENT = re.compile(
    r"(?i)werkelijk[\s_-]*rendement|actual[\s_-]*return|\bbox3_actual\b"
)

_FENCE_OPEN = re.compile(r"^(`{3,}|~{3,})\s*([^`\s]*)")
_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


class WorkpackGraderSetupError(RuntimeError):
    """A bundled template, flow, or register needed by the grader is unreadable."""


# ---------------------------------------------------------------------------
# Markdown scanning
# ---------------------------------------------------------------------------


class Section:
    """One H2 section: its heading text, 1-based line, and body."""

    def __init__(self, heading: str, line: int, body: str) -> None:
        self.heading = heading
        self.line = line
        self.body = body


class ParsedMarkdown:
    """The H1 title, the text before the first H2, and the H2 sections."""

    def __init__(
        self, title: str | None, title_line: int | None, preamble: str, sections: list[Section]
    ) -> None:
        self.title = title
        self.title_line = title_line
        self.preamble = preamble
        self.sections = sections


def _is_fence_close(stripped: str, marker: str) -> bool:
    return stripped.startswith(marker) and set(stripped) == {marker[0]}


def parse_markdown(text: str) -> ParsedMarkdown:
    """Split ``text`` into the H1 title, the preamble, and H2 sections.

    Headings inside fenced blocks never delimit sections.
    """
    lines = text.replace("\r\n", "\n").split("\n")
    title = None
    title_line = None
    preamble: list[str] = []
    sections: list[Section] = []
    current: Section | None = None
    body: list[str] = []
    fence = None

    def flush() -> None:
        if current is not None:
            current.body = "\n".join(body)
            sections.append(current)

    for number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if fence is not None:
            if _is_fence_close(stripped, fence):
                fence = None
        else:
            opener = _FENCE_OPEN.match(stripped)
            if opener:
                fence = opener.group(1)
            else:
                heading = _HEADING.match(line)
                if heading and len(heading.group(1)) <= 2:
                    level = len(heading.group(1))
                    if level == 1:
                        if title is None and current is None:
                            title, title_line = heading.group(2), number
                            continue
                    else:
                        flush()
                        current = Section(heading.group(2), number, "")
                        body = []
                        continue
        if current is None:
            preamble.append(line)
        else:
            body.append(line)
    flush()
    return ParsedMarkdown(title, title_line, "\n".join(preamble), sections)


def normalize_heading(heading: str) -> str:
    text = heading.strip().strip("#").strip()
    text = re.sub(r"\s+(?:—|–|--|-)\s+", " - ", text)
    return re.sub(r"\s+", " ", text).lower()


def fenced_blocks(body: str) -> tuple[list[tuple[str, str]], bool]:
    """Return ``([(info, text), ...], unclosed)`` for fenced blocks in ``body``."""
    blocks: list[tuple[str, str]] = []
    fence = None
    info = ""
    collected: list[str] = []
    for line in body.split("\n"):
        stripped = line.strip()
        if fence is not None:
            if _is_fence_close(stripped, fence):
                blocks.append((info, "\n".join(collected)))
                fence = None
                collected = []
            else:
                collected.append(line)
            continue
        opener = _FENCE_OPEN.match(stripped)
        if opener:
            fence = opener.group(1)
            info = opener.group(2).lower()
            collected = []
    return blocks, fence is not None


def text_outside_fences(body: str) -> str:
    kept: list[str] = []
    fence = None
    for line in body.split("\n"):
        stripped = line.strip()
        if fence is not None:
            if _is_fence_close(stripped, fence):
                fence = None
            continue
        opener = _FENCE_OPEN.match(stripped)
        if opener:
            fence = opener.group(1)
            continue
        kept.append(line)
    return "\n".join(kept)


def _split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_tables(body: str) -> list[tuple[list[str], list[list[str]]]]:
    """Return ``[(headers, rows)]`` for every pipe table outside fences."""
    tables: list[tuple[list[str], list[list[str]]]] = []
    headers: list[str] | None = None
    rows: list[list[str]] = []
    for line in text_outside_fences(body).split("\n"):
        stripped = line.strip()
        if not stripped.startswith("|"):
            if headers is not None:
                tables.append((headers, rows))
            headers, rows = None, []
            continue
        cells = _split_row(stripped)
        if headers is None:
            headers = [cell.strip("`* ").lower() for cell in cells]
            continue
        if all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells if cell):
            continue
        rows.append(cells)
    if headers is not None:
        tables.append((headers, rows))
    return tables


def _cell_token(cell: str) -> str:
    return cell.strip().strip("`*").strip()


def section_map(parsed: ParsedMarkdown) -> dict[str, list[Section]]:
    mapping: dict[str, list[Section]] = {}
    for section in parsed.sections:
        mapping.setdefault(normalize_heading(section.heading), []).append(section)
    return mapping


def find_section(parsed: ParsedMarkdown, heading: str) -> Section | None:
    wanted = normalize_heading(heading)
    for section in parsed.sections:
        if normalize_heading(section.heading) == wanted:
            return section
    return None


def _has_line(body: str, literal: str) -> bool:
    wanted = literal.lower()
    return any(
        line.strip().strip("`*_> ").strip().rstrip(".").lower() == wanted
        for line in text_outside_fences(body).split("\n")
    )


# ---------------------------------------------------------------------------
# Plugin-derived contracts (templates, flow table, source register)
# ---------------------------------------------------------------------------


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise WorkpackGraderSetupError(f"cannot read {path}: {exc}") from exc


@functools.lru_cache(maxsize=None)
def template_headings(plugin_root: str, kind: str) -> tuple[tuple[str, str], ...]:
    """Return ``((display, matcher), ...)`` for the template's H2 sections.

    ``matcher`` is the normalized heading, or ``prefix:<text>`` for a heading
    that carries a ``[placeholder]`` (the provisional ``Subflow: [...]``).
    """
    parsed = parse_markdown(_read(Path(plugin_root) / TEMPLATE_PATHS[kind]))
    specs = []
    for section in parsed.sections:
        normalized = normalize_heading(section.heading)
        if "[" in normalized:
            specs.append((section.heading, "prefix:" + normalized.split("[", 1)[0].strip()))
        else:
            specs.append((section.heading, normalized))
    if not specs:
        raise WorkpackGraderSetupError(f"no H2 sections found in the {kind} template")
    return tuple(specs)


@functools.lru_cache(maxsize=None)
def annual_section_keys(plugin_root: str) -> frozenset[str]:
    parsed = parse_markdown(_read(Path(plugin_root) / TEMPLATE_PATHS["annual"]))
    appendix = find_section(parsed, "Appendix A — Resume record")
    if appendix is None:
        raise WorkpackGraderSetupError("annual template has no Appendix A")
    blocks, _ = fenced_blocks(appendix.body)
    record = yaml.safe_load(blocks[0][1]) if blocks else None
    if not isinstance(record, dict) or not isinstance(record.get("sections"), dict):
        raise WorkpackGraderSetupError("annual template Appendix A has no sections mapping")
    return frozenset(record["sections"])


@functools.lru_cache(maxsize=None)
def provisional_section_keys(plugin_root: str) -> dict[str, frozenset[str]]:
    """Per-subflow section keys from the provisional-flow.md status table."""
    text = _read(Path(plugin_root) / PROVISIONAL_FLOW_PATH)
    per_subflow: dict[str, set[str]] = {name: set() for name in PROVISIONAL_SUBFLOWS}
    for line in text.splitlines():
        match = re.match(r"^\|\s*`([a-z0-9_]+)`\s*\|[^|]*\|\s*([^|]+?)\s*\|\s*$", line)
        if not match:
            continue
        key, applies = match.group(1), match.group(2).lower()
        targets = (
            PROVISIONAL_SUBFLOWS
            if applies.strip() == "all"
            else [part.strip() for part in applies.split(",")]
        )
        for target in targets:
            if target in per_subflow:
                per_subflow[target].add(key)
    if not all(per_subflow.values()):
        raise WorkpackGraderSetupError(
            "provisional-flow.md section-status table did not yield keys for every subflow"
        )
    return {name: frozenset(keys) for name, keys in per_subflow.items()}


def expected_section_keys(plugin_root: str, workflow: str) -> tuple[frozenset[str], frozenset[str]]:
    """Return ``(required, optional)`` Appendix A section keys for ``workflow``."""
    if workflow == ANNUAL_WORKFLOW:
        return annual_section_keys(plugin_root), frozenset()
    subflow = workflow.rsplit("_", 1)[-1]
    required = provisional_section_keys(plugin_root)[subflow]
    return required, frozenset(OPTIONAL_SECTION_KEYS.get(workflow, set()))


@functools.lru_cache(maxsize=None)
def source_register(plugin_root: str) -> dict[str, dict[str, Any]] | None:
    path = Path(plugin_root) / SOURCE_REGISTER_PATH
    if not path.is_file():
        return None
    data = yaml.safe_load(_read(path)) or {}
    return {
        entry["id"]: entry
        for entry in data.get("sources", []) or []
        if isinstance(entry, dict) and entry.get("id")
    }


# ---------------------------------------------------------------------------
# Public helpers used by the offline eval verifier
# ---------------------------------------------------------------------------


def kind_for_workflow(workflow: Any) -> str | None:
    if workflow == ANNUAL_WORKFLOW:
        return "annual"
    if workflow in PROVISIONAL_WORKFLOWS:
        return "provisional"
    return None


def kind_for_path(path: str | Path) -> str | None:
    name = Path(path).name
    for kind, filename in WORKPACK_FILENAMES.items():
        if name == filename:
            return kind
    return None


APPENDIX_HEADINGS = {"A": "Appendix A — Resume record", "B": "Appendix B — Field map"}


def appendix_yaml_text(text: str, letter: str) -> str | None:
    """Return the raw text of the single fenced yaml block in Appendix A or B."""
    parsed = parse_markdown(text)
    matches = section_map(parsed).get(normalize_heading(APPENDIX_HEADINGS[letter]), [])
    if len(matches) != 1:
        return None
    blocks, unclosed = fenced_blocks(matches[0].body)
    yaml_blocks = [body for info, body in blocks if info in {"yaml", "yml"}]
    if unclosed or len(yaml_blocks) != 1:
        return None
    return yaml_blocks[0]


def resume_record_block(text: str) -> tuple[Any, list[str]]:
    """Return ``(parsed_record, errors)`` for the Appendix A YAML block."""
    parsed = parse_markdown(text)
    matches = section_map(parsed).get(normalize_heading("Appendix A — Resume record"), [])
    if not matches:
        return None, ["missing '## Appendix A — Resume record'"]
    if len(matches) > 1:
        return None, ["more than one '## Appendix A — Resume record' section"]
    blocks, unclosed = fenced_blocks(matches[0].body)
    if unclosed:
        return None, ["Appendix A has an unclosed fenced block"]
    yaml_blocks = [body for info, body in blocks if info in {"yaml", "yml"}]
    if len(yaml_blocks) != 1:
        return None, [
            f"Appendix A must hold exactly one fenced yaml block (found {len(yaml_blocks)})"
        ]
    try:
        record = yaml.safe_load(yaml_blocks[0])
    except yaml.YAMLError as exc:
        return None, [f"Appendix A yaml does not parse: {exc}"]
    if not isinstance(record, dict):
        return None, ["Appendix A yaml must be a mapping"]
    return record, []


def extract_field_map(text: str) -> tuple[str, Any, list[str]]:
    """Return ``(state, data, errors)`` for Appendix B.

    ``state`` is ``"not_yet_mapped"``, ``"mapped"``, or ``"invalid"``.
    """
    parsed = parse_markdown(text)
    matches = section_map(parsed).get(normalize_heading("Appendix B — Field map"), [])
    if not matches:
        return "invalid", None, ["missing '## Appendix B — Field map'"]
    if len(matches) > 1:
        return "invalid", None, ["more than one '## Appendix B — Field map' section"]
    body = matches[0].body
    blocks, unclosed = fenced_blocks(body)
    if unclosed:
        return "invalid", None, ["Appendix B has an unclosed fenced block"]
    yaml_blocks = [block for info, block in blocks if info in {"yaml", "yml"}]
    placeholder = _has_line(body, NOT_YET_MAPPED)
    if not yaml_blocks:
        if placeholder:
            return "not_yet_mapped", None, []
        return "invalid", None, [
            f"Appendix B must hold the literal line '{NOT_YET_MAPPED}' or one fenced yaml field map"
        ]
    if len(yaml_blocks) > 1:
        return "invalid", None, [
            f"Appendix B must hold exactly one fenced yaml block (found {len(yaml_blocks)})"
        ]
    if placeholder:
        return "invalid", None, [
            f"Appendix B holds both a field map and the '{NOT_YET_MAPPED}' line"
        ]
    try:
        data = yaml.safe_load(yaml_blocks[0])
    except yaml.YAMLError as exc:
        return "invalid", None, [f"Appendix B yaml does not parse: {exc}"]
    if not isinstance(data, dict):
        return "invalid", None, ["Appendix B yaml must be a mapping"]
    return "mapped", data, []


def sources_used(text: str) -> list[str] | None:
    """Return the source IDs listed under ``## Sources used`` (None if absent)."""
    section = find_section(parse_markdown(text), "Sources used")
    if section is None:
        return None
    ids, _ = _sources_used_entries(section.body)
    return ids


def _sources_used_entries(body: str) -> tuple[list[str], list[str]]:
    ids: list[str] = []
    bad: list[str] = []
    for line in text_outside_fences(body).split("\n"):
        match = re.match(r"^\s*[-*]\s+(.*\S)\s*$", line)
        if not match:
            continue
        token = match.group(1).split()[0].strip("`*,;")
        if SOURCE_ID.fullmatch(token):
            ids.append(token)
        else:
            bad.append(match.group(1))
    return ids, bad


def documents_rows(text: str) -> list[dict[str, str]]:
    """Return the ``## Documents and sources`` rows keyed by lower-case header."""
    section = find_section(parse_markdown(text), "Documents and sources")
    if section is None:
        return []
    rows: list[dict[str, str]] = []
    for headers, table_rows in parse_tables(section.body):
        if not headers or headers[0] != "id":
            continue
        for cells in table_rows:
            if not cells or not EVIDENCE_ROW_ID.fullmatch(_cell_token(cells[0])):
                continue
            row = {
                header: (cells[index] if index < len(cells) else "")
                for index, header in enumerate(headers)
            }
            row["id"] = _cell_token(cells[0])
            rows.append(row)
    return rows


def _documents_status_header(headers: list[str]) -> str | None:
    for header in headers:
        if header.startswith("status"):
            return header
    return None


def open_question_rows(text: str) -> dict[str, dict[str, str]]:
    section = find_section(parse_markdown(text), "Open questions")
    if section is None:
        return {}
    rows: dict[str, dict[str, str]] = {}
    for headers, table_rows in parse_tables(section.body):
        for cells in table_rows:
            if not cells or not QUESTION_ID.fullmatch(_cell_token(cells[0])):
                continue
            rows[_cell_token(cells[0])] = {
                header: (cells[index] if index < len(cells) else "")
                for index, header in enumerate(headers)
            }
    return rows


def profile_keys(text: str) -> set[str]:
    section = find_section(parse_markdown(text), "Taxpayer profile summary")
    keys: set[str] = set()
    if section is None:
        return keys
    for headers, table_rows in parse_tables(section.body):
        if not headers or headers[0] != "key":
            continue
        for cells in table_rows:
            if cells:
                keys.add(_cell_token(cells[0]))
    return keys


# ---------------------------------------------------------------------------
# Field map summary, manual-entry checklist, and stale markers (A10, A12)
# ---------------------------------------------------------------------------


def _marker_text(line: str) -> str:
    """Return ``line`` without surrounding Markdown emphasis, quotes, or code ticks."""
    return line.strip().lstrip(">").strip().strip("*_`").strip()


def stale_lines(body: str) -> tuple[list[str], list[str]]:
    """Return ``(valid, malformed)`` STALE lines found outside fenced blocks."""
    valid: list[str] = []
    malformed: list[str] = []
    for line in text_outside_fences(body).split("\n"):
        text = _marker_text(line)
        if not STALE_START.match(text):
            continue
        (valid if STALE_MARKER.match(" ".join(text.split())) else malformed).append(text)
    return valid, malformed


def _is_missing_cell(cell: str) -> bool:
    text = cell.replace("—", "-").replace("–", "-").strip("`*_ ").lower()
    text = re.sub(r"\s*-+\s*", " - ", " ".join(text.split()))
    return MISSING_MARKER in text


def _parse_amount(text: str) -> decimal.Decimal | None:
    compact = re.sub(r"(?i)eur|€|\s", "", text).replace("\u2212", "-")
    compact = re.sub(r"[.,]-$", "", compact)
    if not re.fullmatch(r"[+-]?\d[\d.,]*", compact) or compact[-1] in ".,":
        return None
    sign = ""
    if compact[0] in "+-":
        sign, compact = ("-" if compact[0] == "-" else ""), compact[1:]
    if "." in compact and "," in compact:
        decimal_mark = "." if compact.rfind(".") > compact.rfind(",") else ","
        thousands = "," if decimal_mark == "." else "."
        whole, _, fraction = compact.rpartition(decimal_mark)
        if decimal_mark in whole:
            return None
        compact = whole.replace(thousands, "") + "." + fraction
    else:
        separator = "." if "." in compact else "," if "," in compact else None
        if separator is not None:
            parts = compact.split(separator)
            leading_zero = parts[0].startswith("0")
            if len(parts) > 2 or (len(parts[-1]) == 3 and not leading_zero):
                # One separator before exactly three digits, or several: thousands.
                if any(len(part) != 3 for part in parts[1:]):
                    return None
                compact = "".join(parts)
            else:
                compact = parts[0] + "." + parts[1]
    try:
        return decimal.Decimal(sign + compact)
    except decimal.InvalidOperation:
        return None


def normalize_value(value: Any) -> tuple[str, Any]:
    """Normalize a map value or a table cell for comparison (A12).

    Amounts compare as numbers: ``EUR``/``€``, whitespace, and thousands
    separators (``.`` or ``,``) are ignored, and ``48.250,00`` equals ``48250``.
    Yes/no answers compare as booleans; a trailing parenthetical note after an
    amount or yes/no is ignored; anything else compares as whitespace-collapsed,
    case-insensitive text.
    """
    if value is None:
        return ("missing", None)
    if isinstance(value, bool):
        return ("bool", value)
    if isinstance(value, (int, float, decimal.Decimal)):
        return ("number", decimal.Decimal(str(value)))
    text = str(value).strip().strip("`*_").strip()
    lowered = " ".join(text.lower().split())
    if lowered in TRUE_WORDS:
        return ("bool", True)
    if lowered in FALSE_WORDS:
        return ("bool", False)
    amount = _parse_amount(text)
    if amount is not None:
        return ("number", amount)
    # A value followed by a parenthetical note, e.g. "51,400 (check the
    # pre-fill)": compare the leading value when it is an amount or yes/no.
    noted = re.match(r"^(.+?)\s*\([^()]*\)\s*$", text)
    if noted:
        head = normalize_value(noted.group(1))
        if head[0] in {"number", "bool"}:
            return head
    return ("text", lowered)


def values_equal(expected: Any, shown: Any) -> bool:
    return normalize_value(expected) == normalize_value(shown)


class TableRow:
    """One row of a field-bearing table: its ``field_id``, value cell, and Q-IDs."""

    def __init__(self, field_id: str, value: str, cells: list[str]) -> None:
        self.field_id = field_id
        self.value = value
        self.cells = cells
        self.missing = _is_missing_cell(value)
        self.question_ids = set(re.findall(r"\bQ\d+\b", " ".join(cells)))


def field_table_rows(body: str) -> tuple[list[tuple[list[str], list[TableRow]]], bool]:
    """Return ``([(headers, rows)], found)`` for tables with field_id and value columns."""
    tables: list[tuple[list[str], list[TableRow]]] = []
    for headers, raw_rows in parse_tables(body):
        if "field_id" not in headers or "value to enter" not in headers:
            continue
        field_index = headers.index("field_id")
        value_index = headers.index("value to enter")
        rows = []
        for cells in raw_rows:
            field_id = _cell_token(cells[field_index]) if field_index < len(cells) else ""
            value = cells[value_index].strip() if value_index < len(cells) else ""
            rows.append(TableRow(field_id, value, cells))
        tables.append((headers, rows))
    return tables, bool(tables)


def field_map_summary_rows(body: str) -> tuple[list[TableRow] | None, list[str]]:
    """Return ``(rows, errors)`` for the Field map summary table (None if absent)."""
    tables, found = field_table_rows(body)
    if not found:
        return None, []
    errors: list[str] = []
    rows: list[TableRow] = []
    for headers, table_rows in tables:
        if tuple(headers) != SUMMARY_HEADERS:
            errors.append(
                "'## Field map summary' table must use the columns | Portal section | Portal label | "
                f"field_id | Value to enter | Source | Review | (got {' | '.join(headers)})"
            )
        rows.extend(table_rows)
    errors.extend(_summary_row_errors(rows))
    return rows, errors


def _summary_row_errors(rows: list[TableRow]) -> list[str]:
    errors: list[str] = []
    shown: dict[str, list[TableRow]] = {}
    for row in rows:
        if not row.field_id:
            errors.append("'## Field map summary' has a row without a field_id")
            continue
        if not row.value.strip("`*_ "):
            errors.append(f"'## Field map summary' row {row.field_id} has an empty Value to enter")
        if row.missing and not row.question_ids:
            errors.append(
                f"'## Field map summary' row {row.field_id} shows 'MISSING - enter manually' "
                "without its Q-ID"
            )
        shown.setdefault(row.field_id, []).append(row)
    for field_id, field_rows in shown.items():
        values = {normalize_value(None if row.missing else row.value) for row in field_rows}
        if len(values) > 1:
            errors.append(
                f"'## Field map summary' shows {field_id} with different values "
                f"({', '.join(repr(row.value) for row in field_rows)}); a double-entry fact "
                "keeps one value on every screen path"
            )
    return errors


def expected_summary_values(data: dict[str, Any]) -> tuple[dict[str, tuple[str, Any]], set[str]]:
    """Return ``({field_id: ("value", v) | ("missing", qid)}, internal_routing_ids)``."""
    expected: dict[str, tuple[str, Any]] = {}
    routing: set[str] = set()
    for entry in data.get("missing_fields") or []:
        if isinstance(entry, dict) and entry.get("field_id"):
            expected[str(entry["field_id"])] = ("missing", entry.get("open_question_id"))
    for entry in data.get("fields") or []:
        if not isinstance(entry, dict) or not entry.get("field_id"):
            continue
        field_id = str(entry["field_id"])
        if entry.get("entry_mode") == INTERNAL_ROUTING:
            routing.add(field_id)
            continue
        source = entry.get("source") if isinstance(entry.get("source"), dict) else {}
        if entry.get("value") is None or source.get("type") == "unknown":
            previous = expected.get(field_id)
            expected[field_id] = ("missing", previous[1] if previous else None)
        else:
            expected[field_id] = ("value", entry.get("value"))
    return expected, routing


def compare_rows(
    rows: list[TableRow],
    expected: dict[str, tuple[str, Any]],
    routing: set[str],
    label: str,
    source_label: str,
    errors: list[str],
    *,
    require_every_field: bool,
) -> None:
    """Check table ``rows`` against the expected field values (A12)."""
    shown: dict[str, list[TableRow]] = {}
    for row in rows:
        if not row.field_id:
            continue
        if row.field_id in routing:
            errors.append(
                f"{label} shows {row.field_id}, an internal_routing record that is never a portal row"
            )
        elif row.field_id not in expected:
            errors.append(f"{label} row {row.field_id} is not a field in {source_label}")
        else:
            shown.setdefault(row.field_id, []).append(row)
    for field_id, (kind, payload) in expected.items():
        field_rows = shown.get(field_id, [])
        if not field_rows:
            if require_every_field:
                if kind == "missing":
                    errors.append(
                        f"{source_label} missing field {field_id} has no 'MISSING - enter manually' "
                        f"row in {label}"
                    )
                else:
                    errors.append(f"{source_label} manual_entry field {field_id} is missing from {label}")
            continue
        for row in field_rows:
            if kind == "missing":
                if not row.missing:
                    errors.append(
                        f"{label} shows {field_id} = {row.value!r} but {source_label} has no value; "
                        "show 'MISSING - enter manually'"
                    )
                elif require_every_field and payload and payload not in row.question_ids:
                    errors.append(f"{label} MISSING row {field_id} must name its Q-ID {payload}")
            elif row.missing:
                errors.append(
                    f"{label} shows {field_id} as MISSING but {source_label} holds {payload!r}"
                )
            elif not values_equal(payload, row.value):
                errors.append(
                    f"{label} shows {field_id} = {row.value!r} but {source_label} holds {payload!r}"
                )


def checklist_requested(body: str) -> bool:
    """True when ``## Manual-entry checklist`` holds a checklist, not the placeholder."""
    if _has_line(body, NOT_REQUESTED):
        return False
    content = [
        line
        for line in text_outside_fences(body).split("\n")
        if line.strip() and not FILL_NOTE_LINE.match(line)
    ]
    return bool(content)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


class WorkpackReport:
    """Errors (blocking), warnings, and the parsed parts of one workpack."""

    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.kind: str | None = None
        self.resume_record: dict[str, Any] | None = None
        self.field_map_state: str | None = None
        self.field_map: dict[str, Any] | None = None

    @property
    def ok(self) -> bool:
        return not self.errors


def _parse_timestamp(value: Any) -> dt.datetime | None:
    if isinstance(value, dt.datetime):
        parsed = value
    elif isinstance(value, dt.date):
        parsed = dt.datetime(value.year, value.month, value.day)
    elif isinstance(value, str) and value.strip():
        try:
            parsed = dt.datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
        except ValueError:
            return None
    else:
        return None
    if parsed.tzinfo is not None:
        parsed = parsed.astimezone(dt.timezone.utc).replace(tzinfo=None)
    return parsed


def _tax_year_value(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return None


def _check_structure(
    parsed: ParsedMarkdown,
    kind: str,
    plugin_root: str,
    report: WorkpackReport,
    *,
    excluded: frozenset[str] = frozenset(),
    optional: frozenset[str] = frozenset(),
) -> None:
    specs = tuple(
        spec for spec in template_headings(plugin_root, kind) if spec[1] not in excluded
    )

    def spec_index(heading: str) -> int | None:
        normalized = normalize_heading(heading)
        for index, (_, matcher) in enumerate(specs):
            if matcher.startswith("prefix:"):
                if normalized.startswith(matcher[len("prefix:"):]):
                    return index
            elif normalized == matcher:
                return index
        return None

    seen: dict[int, int] = {}
    order: list[tuple[int, Section]] = []
    for section in parsed.sections:
        index = spec_index(section.heading)
        if index is None:
            report.warnings.append(
                f"line {section.line}: unexpected top-level section '## {section.heading}'"
            )
            continue
        seen[index] = seen.get(index, 0) + 1
        if seen[index] == 1:
            order.append((index, section))
    for index, (display, matcher) in enumerate(specs):
        if index not in seen:
            if matcher not in optional:
                report.errors.append(f"missing required section '## {display}'")
        elif seen[index] > 1:
            report.errors.append(f"section '## {display}' appears {seen[index]} times")
    previous = None
    for index, section in order:
        if previous is not None and index < previous[0]:
            report.errors.append(
                f"section '## {section.heading}' (line {section.line}) is out of order: "
                f"it must come before '## {previous[1].heading}'"
            )
        else:
            previous = (index, section)

    year = str(TAX_YEARS[kind])
    if parsed.title is None:
        report.errors.append("missing the H1 title line")
    elif year not in parsed.title:
        report.errors.append(f"title '{parsed.title}' does not name tax year {year}")


def _check_banner(parsed: ParsedMarkdown, readiness: Any, report: WorkpackReport) -> None:
    banner = next(
        (line for line in parsed.preamble.split("\n") if "STATUS:" in line.upper()),
        None,
    )
    if banner is None:
        report.errors.append("missing the STATUS banner before the first section")
        return
    # The template's bold banner may be followed by fill instructions on the
    # same line; judge only the bold banner when there is one.
    bold = re.search(r"\*\*\s*(STATUS:.*?)\*\*", banner, flags=re.IGNORECASE)
    upper = (bold.group(1) if bold else banner).upper()
    if "NOT FOR FILING" not in upper:
        report.errors.append("STATUS banner must say the workpack is not for filing")
    complete = "COMPLETE DRAFT FOR REVIEW" in upper
    draft_only = "DRAFT" in upper.replace("COMPLETE DRAFT FOR REVIEW", "")
    if complete and draft_only:
        report.errors.append("STATUS banner still holds both template alternatives")
    elif readiness == "review_ready" and not complete:
        report.errors.append(
            "Appendix A readiness is review_ready but the STATUS banner is not COMPLETE DRAFT FOR REVIEW"
        )
    elif readiness == "draft" and (complete or not draft_only):
        report.errors.append("Appendix A readiness is draft but the STATUS banner is not DRAFT")


def _check_resume_record(
    record: dict[str, Any],
    kind: str,
    plugin_root: str,
    expect_saved: bool,
    questions: dict[str, dict[str, str]],
    report: WorkpackReport,
) -> None:
    errors = report.errors
    missing = [key for key in RESUME_RECORD_KEYS if key not in record]
    if missing:
        errors.append(f"Appendix A is missing key(s): {', '.join(missing)}")
    unknown = sorted(str(key) for key in record if key not in RESUME_RECORD_KEYS)
    if unknown:
        errors.append(
            f"Appendix A has unknown key(s) {', '.join(unknown)}; facts never live in the resume record"
        )

    if record.get("workpack_format") != WORKPACK_FORMAT:
        errors.append(f"workpack_format must be '{WORKPACK_FORMAT}'")
    version = record.get("workpack_version")
    if isinstance(version, str):
        if not WORKPACK_VERSION.fullmatch(version.strip()):
            errors.append(f"workpack_version must be \"2.x\" (got {version!r})")
    elif isinstance(version, (int, float)) and not isinstance(version, bool) and str(version).startswith("2."):
        report.warnings.append("workpack_version should be a quoted string such as \"2.0\"")
    else:
        errors.append(f"workpack_version must be \"2.x\" (got {version!r})")
    plugin_version = record.get("plugin_version")
    if not isinstance(plugin_version, str) or not PLUGIN_VERSION.fullmatch(plugin_version.strip()):
        errors.append(f"plugin_version must be a quoted semantic version (got {plugin_version!r})")

    workflow = record.get("workflow")
    expected_year = TAX_YEARS[kind]
    if kind_for_workflow(workflow) != kind:
        errors.append(
            f"workflow {workflow!r} does not belong in the {kind} workpack "
            f"({'annual_2025' if kind == 'annual' else 'provisional_2026_<subflow>'})"
        )
    if _tax_year_value(record.get("tax_year")) != expected_year:
        errors.append(
            f"tax_year must be {expected_year} for {workflow!r} (got {record.get('tax_year')!r})"
        )

    for key in ("created_at", "updated_at"):
        value = record.get(key)
        if value in (None, ""):
            if expect_saved:
                errors.append(f"{key} must be set in a saved workpack")
        elif _parse_timestamp(value) is None:
            errors.append(f"{key} must be an ISO 8601 timestamp (got {value!r})")
    created = _parse_timestamp(record.get("created_at"))
    updated = _parse_timestamp(record.get("updated_at"))
    if created and updated and updated < created:
        errors.append("updated_at is earlier than created_at")

    consent = record.get("save_consent")
    if consent not in SAVE_CONSENT_VALUES:
        errors.append(f"save_consent must be one of {', '.join(SAVE_CONSENT_VALUES)} (got {consent!r})")
    elif expect_saved and consent != "given":
        errors.append("a saved workpack file must record save_consent: given")
    readiness = record.get("readiness")
    if readiness not in READINESS_VALUES:
        errors.append(f"readiness must be one of {', '.join(READINESS_VALUES)} (got {readiness!r})")
    confirmed = record.get("generation_confirmed")
    if not isinstance(confirmed, bool):
        errors.append(f"generation_confirmed must be true or false (got {confirmed!r})")

    queued = record.get("queued_workflow")
    if kind == "annual":
        if queued is not None and queued not in PROVISIONAL_WORKFLOWS:
            errors.append(
                f"queued_workflow must be null or a provisional_2026_<subflow> value (got {queued!r})"
            )
    elif queued is not None:
        errors.append("queued_workflow must be null in a provisional workpack")

    sections = record.get("sections")
    statuses: dict[str, str] = {}
    open_ids: dict[str, str] = {}
    if not isinstance(sections, dict):
        errors.append("sections must be a mapping of section key to {status, open}")
    elif kind_for_workflow(workflow) == kind:
        required, optional = expected_section_keys(plugin_root, workflow)
        keys = set(sections)
        if required - keys:
            errors.append(
                f"sections missing key(s) for {workflow}: {', '.join(sorted(required - keys))}"
            )
        extra = keys - required - optional
        if extra:
            errors.append(
                f"sections has key(s) not used by {workflow}: {', '.join(sorted(map(str, extra)))}"
            )
        for key, entry in sections.items():
            if not isinstance(entry, dict):
                errors.append(f"sections.{key} must be a mapping with status and open")
                continue
            if set(entry) != {"status", "open"}:
                errors.append(f"sections.{key} must hold exactly status and open")
            status = entry.get("status")
            if status not in STATUS_VALUES:
                errors.append(
                    f"sections.{key}.status must be one of {' | '.join(STATUS_VALUES)} (got {status!r})"
                )
            else:
                statuses[str(key)] = status
            open_list = entry.get("open")
            if not isinstance(open_list, list):
                errors.append(f"sections.{key}.open must be a list of Q-IDs")
                open_list = []
            for question in open_list:
                if not isinstance(question, str) or not QUESTION_ID.fullmatch(question):
                    errors.append(f"sections.{key}.open holds a non Q-ID value {question!r}")
                    continue
                if question in open_ids:
                    errors.append(f"{question} is listed under both sections.{open_ids[question]} and sections.{key}")
                open_ids[question] = str(key)
            if status == "deferred" and not open_list:
                errors.append(f"sections.{key} is deferred but lists no open question")

    if statuses and readiness == "review_ready":
        not_done = sorted(key for key, status in statuses.items() if status not in DONE_STATUSES)
        if not_done:
            errors.append(
                "readiness review_ready requires every section complete or chat_only; not done: "
                + ", ".join(not_done)
            )
        blocking = sorted(
            question
            for question in open_ids
            if _is_blocking(questions.get(question))
        )
        if blocking:
            errors.append(
                "readiness review_ready with blocking open question(s): " + ", ".join(blocking)
            )
    if isinstance(confirmed, bool) and "confirm" in statuses:
        if confirmed and statuses["confirm"] != "complete":
            errors.append("generation_confirmed is true but sections.confirm is not complete")
        if not confirmed and statuses["confirm"] == "complete":
            errors.append("sections.confirm is complete but generation_confirmed is false")

    # Q-IDs in Appendix A and the Open questions table must agree.
    if isinstance(sections, dict):
        table_ids = set(questions)
        listed = set(open_ids)
        for question in sorted(listed - table_ids):
            errors.append(f"{question} is open in Appendix A but has no row in '## Open questions'")
        for question in sorted(table_ids - listed):
            errors.append(f"'## Open questions' row {question} is not listed in any Appendix A open list")
        for question, key in open_ids.items():
            row = questions.get(question)
            if not row:
                continue
            section_cell = _cell_token(row.get("section", ""))
            if section_cell in statuses and section_cell != key:
                errors.append(
                    f"{question} belongs to section {section_cell!r} in '## Open questions' "
                    f"but is listed under sections.{key}"
                )

    loaded = record.get("sources_loaded")
    if not isinstance(loaded, list) or not all(isinstance(item, str) for item in loaded):
        errors.append("sources_loaded must be a list of source_id strings")
    elif len(loaded) != len(set(loaded)):
        errors.append("sources_loaded lists a source_id more than once")


def _is_blocking(row: dict[str, str] | None) -> bool:
    if not row:
        return True
    value = _cell_token(row.get("blocking", "")).lower()
    return value not in {"no", "nee", "false", "non-blocking", "nonblocking"}


def _check_sources(
    parsed: ParsedMarkdown,
    record: dict[str, Any] | None,
    kind: str,
    plugin_root: str,
    report: WorkpackReport,
) -> None:
    section = find_section(parsed, "Sources used")
    if section is None:
        return
    ids, bad = _sources_used_entries(section.body)
    for entry in bad:
        report.errors.append(f"'## Sources used' entry is not a source_id: {entry!r}")
    if len(ids) != len(set(ids)):
        report.errors.append("'## Sources used' lists a source_id more than once")
    loaded = record.get("sources_loaded") if isinstance(record, dict) else None
    if isinstance(loaded, list) and sorted(set(ids)) != sorted(set(map(str, loaded))):
        report.errors.append(
            f"'## Sources used' {sorted(set(ids))} must equal Appendix A sources_loaded "
            f"{sorted(set(map(str, loaded)))}"
        )
    register = source_register(plugin_root)
    if register is None:
        report.warnings.append("source register not found; registered-source checks skipped")
        return
    other = FIELD_MAP_WORKFLOWS["provisional" if kind == "annual" else "annual"]
    for source_id in sorted(set(ids)):
        entry = register.get(source_id)
        if entry is None:
            report.errors.append(f"'## Sources used' names unregistered source_id {source_id}")
        elif entry.get("workflow") == other:
            report.errors.append(
                f"{kind} workpack lists {source_id}, a {other} source; source ledgers never mix workflows"
            )


def _check_documents(text: str, parsed: ParsedMarkdown, report: WorkpackReport) -> set[str]:
    section = find_section(parsed, "Documents and sources")
    if section is None:
        return set()
    row_ids: list[str] = []
    for headers, table_rows in parse_tables(section.body):
        if not headers or headers[0] != "id":
            continue
        if len(headers) != 8:
            report.errors.append(
                "'## Documents and sources' table must have 8 columns: ID, document, type, "
                "tax year, owner, location, values taken, status"
            )
        status_header = _documents_status_header(headers)
        for cells in table_rows:
            token = _cell_token(cells[0]) if cells else ""
            if not EVIDENCE_ROW_ID.fullmatch(token):
                continue
            row_ids.append(token)
            if status_header is not None:
                index = headers.index(status_header)
                status = _cell_token(cells[index]).lower() if index < len(cells) else ""
                if status not in {"extracted", "needs review"}:
                    report.errors.append(
                        f"'## Documents and sources' row {token} status must be 'extracted' or "
                        f"'needs review' (got {status!r})"
                    )
    duplicates = sorted({row for row in row_ids if row_ids.count(row) > 1})
    for row in duplicates:
        report.errors.append(f"'## Documents and sources' has duplicate row {row}")
    if FILE_HASH.search(section.body):
        report.errors.append("'## Documents and sources' contains a file hash; record no hashes")

    rows = set(row_ids)
    referenced: set[str] = set()
    for other in parsed.sections:
        if other is section:
            continue
        referenced.update(EVIDENCE_REFERENCE.findall(other.body))
    referenced.update(EVIDENCE_REFERENCE.findall(parsed.preamble))
    for evidence_id in sorted(referenced - rows):
        report.errors.append(
            f"{evidence_id} is referenced but has no row in '## Documents and sources'"
        )
    return rows


def _check_privacy_and_scope(text: str, kind: str, workflow: Any, report: WorkpackReport) -> None:
    for match in BSN_LIKE.finditer(text):
        report.errors.append(f"BSN-like 9-digit number {match.group(0)!r}; never record a BSN")
    seen_ibans: set[str] = set()
    for match in DUTCH_IBAN.finditer(text):
        seen_ibans.add(match.group(0))
    for match in GENERIC_IBAN.finditer(text):
        if _iban_checksum_ok(match.group(0)):
            seen_ibans.add(match.group(0))
    for iban in sorted(seen_ibans):
        report.errors.append(f"IBAN-like value {iban!r}; never record an IBAN")

    other = "provisional" if kind == "annual" else "annual"
    if WORKPACK_STEMS[other] in text:
        report.errors.append(
            f"{kind} workpack mentions the {other} workpack path {WORKPACK_PATHS[other]}; "
            "each workflow owns only its own file"
        )

    if kind == "provisional":
        scrubbed = text
        for allowed in (PROVISIONAL_BOX3_NOTE, PROVISIONAL_BOX3_REDIRECT):
            pattern = r"\s+".join(re.escape(word) for word in allowed.split())
            scrubbed = re.sub(pattern, "", scrubbed, flags=re.IGNORECASE)
        found = sorted({match.group(0) for match in WERKELIJK_RENDEMENT.finditer(scrubbed)})
        if found:
            report.errors.append(
                "provisional workpack collects or references werkelijk rendement "
                f"({', '.join(repr(item) for item in found)}); provisional Box 3 is fictitious-only"
            )
        subflow = workflow.rsplit("_", 1)[-1] if isinstance(workflow, str) else None
        if subflow in {"request", "change"} and PROVISIONAL_BOX3_NOTE.lower() not in " ".join(text.split()).lower():
            report.errors.append(
                f"provisional {subflow} workpack must include the note '{PROVISIONAL_BOX3_NOTE}'"
            )


def _iban_checksum_ok(candidate: str) -> bool:
    compact = re.sub(r"\s+", "", candidate).upper()
    if not 15 <= len(compact) <= 34:
        return False
    rearranged = compact[4:] + compact[:4]
    digits = "".join(str(int(char, 36)) for char in rearranged)
    try:
        return int(digits) % 97 == 1
    except ValueError:
        return False


def _check_subflow_heading(parsed: ParsedMarkdown, workflow: Any, report: WorkpackReport) -> None:
    if not isinstance(workflow, str) or not workflow.startswith("provisional_2026_"):
        return
    subflow = workflow.rsplit("_", 1)[-1]
    for section in parsed.sections:
        normalized = normalize_heading(section.heading)
        if normalized.startswith("subflow:"):
            value = normalized.split(":", 1)[1].strip().strip("`[]* ")
            if value != subflow:
                report.errors.append(
                    f"'## {section.heading}' does not match Appendix A workflow {workflow}"
                )
            return


def _check_field_map(
    text: str,
    parsed: ParsedMarkdown,
    record: dict[str, Any] | None,
    kind: str,
    evidence_rows: set[str],
    questions: dict[str, dict[str, str]],
    report: WorkpackReport,
) -> None:
    state, data, errors = extract_field_map(text)
    report.field_map_state = state
    report.field_map = data if isinstance(data, dict) else None
    report.errors.extend(errors)
    workflow = record.get("workflow") if isinstance(record, dict) else None
    subflow = workflow.rsplit("_", 1)[-1] if isinstance(workflow, str) and kind == "provisional" else None

    summary = find_section(parsed, "Field map summary")
    summary_unmapped = summary is not None and (
        _has_line(summary.body, NOT_YET_MAPPED)
        or re.search(r"(?im)^\s*N/A\b", text_outside_fences(summary.body)) is not None
    )

    if subflow in NO_FIELD_MAP_SUBFLOWS and state == "mapped":
        report.errors.append(f"a provisional {subflow} workpack never holds a field map (Appendix B)")
    if state == "not_yet_mapped" and summary is not None and not summary_unmapped:
        report.errors.append(
            f"'## Field map summary' shows a map but Appendix B holds '{NOT_YET_MAPPED}'"
        )
    _check_stale_markers(parsed, record, state, report)
    if state != "mapped" or not isinstance(data, dict):
        return
    if summary is not None and summary_unmapped:
        report.errors.append(
            "Appendix B holds a field map but '## Field map summary' still reads not yet mapped / N/A"
        )
    elif summary is not None:
        _check_summary_against_map(summary, data, report)
    checklist = find_section(parsed, "Manual-entry checklist")
    if checklist is not None and checklist_requested(checklist.body):
        valid, _ = stale_lines(checklist.body)
        if not valid:
            tables, _ = field_table_rows(checklist.body)
            expected, routing = expected_summary_values(data)
            compare_rows(
                [row for _, rows in tables for row in rows],
                expected,
                routing,
                "'## Manual-entry checklist'",
                "Appendix B",
                report.errors,
                require_every_field=False,
            )

    expected_workflow = FIELD_MAP_WORKFLOWS[kind]
    if data.get("workflow") != expected_workflow:
        report.errors.append(
            f"Appendix B workflow must be {expected_workflow} in the {kind} workpack "
            f"(got {data.get('workflow')!r})"
        )
    if _tax_year_value(data.get("tax_year")) != TAX_YEARS[kind]:
        report.errors.append(
            f"Appendix B tax_year must be {TAX_YEARS[kind]} (got {data.get('tax_year')!r})"
        )
    record_readiness = record.get("readiness") if isinstance(record, dict) else None
    map_readiness = data.get("readiness")
    appendix_b = find_section(parsed, "Appendix B — Field map")
    map_is_stale = appendix_b is not None and bool(stale_lines(appendix_b.body)[0])
    # A10: a stale map keeps its original readiness until regeneration; the
    # STALE line (checked in _check_stale_markers) is what blocks its use.
    if record_readiness == "draft" and map_readiness == "review_ready" and not map_is_stale:
        report.errors.append(
            "Appendix B readiness is review_ready while Appendix A readiness is draft; nothing promotes a draft"
        )
    elif record_readiness == "review_ready" and map_readiness == "draft":
        report.warnings.append(
            "Appendix B readiness is draft while Appendix A is review_ready; acceptable only for a "
            "declared workflow-specific blocker"
        )

    keys = profile_keys(text)
    for index, entry in enumerate(data.get("fields") or []):
        if not isinstance(entry, dict):
            continue
        source = entry.get("source") if isinstance(entry.get("source"), dict) else {}
        evidence_id = source.get("evidence_id")
        # An ev_NNN id without a row is already reported by the document scan.
        if evidence_id not in (None, "") and not (
            isinstance(evidence_id, str) and EVIDENCE_ROW_ID.fullmatch(evidence_id)
        ):
            report.errors.append(
                f"Appendix B fields[{index}] ({entry.get('field_id')}) evidence_id {evidence_id!r} "
                "must name an ev_NNN row in '## Documents and sources'"
            )
        profile_path = source.get("profile_path")
        if isinstance(profile_path, str) and profile_path.strip() and keys:
            path = profile_path.strip()
            if path.startswith("profile."):
                path = path[len("profile."):]
            if path not in keys:
                report.errors.append(
                    f"Appendix B fields[{index}] ({entry.get('field_id')}) profile_path {profile_path!r} "
                    "is not a row Key in '## Taxpayer profile summary'"
                )
    for index, entry in enumerate(data.get("missing_fields") or []):
        if not isinstance(entry, dict):
            continue
        question = entry.get("open_question_id")
        if question not in (None, "") and question not in questions:
            report.errors.append(
                f"Appendix B missing_fields[{index}] open_question_id {question!r} "
                "has no row in '## Open questions'"
            )


def _check_summary_against_map(summary: Section, data: dict[str, Any], report: WorkpackReport) -> None:
    """A12: the Field map summary shows every Appendix B value and gap."""
    rows, errors = field_map_summary_rows(summary.body)
    report.errors.extend(errors)
    if rows is None:
        report.errors.append(
            "'## Field map summary' must hold the summary table (| Portal section | Portal label | "
            "field_id | Value to enter | Source | Review |) once mapping has run (A12)"
        )
        return
    expected, routing = expected_summary_values(data)
    compare_rows(
        rows,
        expected,
        routing,
        "'## Field map summary'",
        "Appendix B",
        report.errors,
        require_every_field=True,
    )
    shown = READINESS_LINE.search(text_outside_fences(summary.body))
    if shown and data.get("readiness") in READINESS_VALUES and shown.group(1) != data.get("readiness"):
        report.errors.append(
            f"'## Field map summary' says Readiness: {shown.group(1)} but Appendix B readiness is "
            f"{data.get('readiness')}"
        )


def _section_body(parsed: ParsedMarkdown, heading: str) -> str | None:
    section = find_section(parsed, heading)
    return section.body if section is not None else None


def _check_stale_markers(
    parsed: ParsedMarkdown, record: dict[str, Any] | None, state: str, report: WorkpackReport
) -> None:
    """A10: map STALE lines appear only while generation_confirmed is false, and always then.

    A requested checklist must be marked while generation is unconfirmed, and may
    stay marked after regeneration until the taxpayer asks for it again.
    """
    confirmed = record.get("generation_confirmed") if isinstance(record, dict) else None
    headings = {
        "summary": "Field map summary",
        "appendix": "Appendix B — Field map",
        "checklist": "Manual-entry checklist",
    }
    stale: dict[str, bool] = {}
    for key, heading in headings.items():
        body = _section_body(parsed, heading)
        if body is None:
            stale[key] = False
            continue
        valid, malformed = stale_lines(body)
        for line in malformed:
            report.errors.append(
                f"'## {heading}' STALE line must read '{STALE_TEMPLATE}' (got {line[:80]!r})"
            )
        stale[key] = bool(valid or malformed)
    # Regeneration re-runs the mapper, so the map sections must be current once
    # generation is confirmed again. A checklist built before the change stays
    # marked until the taxpayer asks for it again (A10), so it may keep its line.
    if (stale["summary"] or stale["appendix"]) and confirmed is True:
        report.errors.append(
            "a STALE line in the field map sections is valid only while Appendix A "
            "generation_confirmed is false; regeneration re-runs the field mapper and removes it (A10)"
        )
    if state != "mapped" and (stale["summary"] or stale["appendix"]):
        report.errors.append("a STALE line in the field map sections needs a field map in Appendix B")
    if state == "mapped" and confirmed is False:
        missing = []
        if not stale["summary"]:
            missing.append("'## Field map summary'")
        if not stale["appendix"]:
            missing.append("Appendix B")
        checklist = _section_body(parsed, "Manual-entry checklist")
        if checklist is not None and checklist_requested(checklist) and not stale["checklist"]:
            missing.append("'## Manual-entry checklist'")
        if missing:
            report.errors.append(
                "generation_confirmed is false but the field map exists, so a sourced fact changed "
                f"after generation: {', '.join(missing)} must carry the line '{STALE_TEMPLATE}' "
                "until regeneration (A10)"
            )


def _chat_subflow(parsed: ParsedMarkdown) -> str | None:
    for section in parsed.sections:
        normalized = normalize_heading(section.heading)
        if normalized.startswith("subflow:"):
            return normalized.split(":", 1)[1].strip().strip("`[]* ")
    return None


def _check_chat_field_map(parsed: ParsedMarkdown, kind: str, report: WorkpackReport) -> None:
    """A10/A12 in a conversation rendering, which has no Appendix B."""
    subflow = _chat_subflow(parsed) if kind == "provisional" else None
    if subflow in NO_FIELD_MAP_SUBFLOWS:
        return
    summary = find_section(parsed, "Field map summary")
    if summary is None:
        report.errors.append(
            "'## Field map summary' is required in the conversation rendering of an annual, "
            "provisional request, or provisional change workpack: it holds the summary table once "
            f"mapping has run, otherwise the line '{NOT_YET_MAPPED}' (A12)"
        )
        return
    body = summary.body
    unmapped = _has_line(body, NOT_YET_MAPPED)
    valid, malformed = stale_lines(body)
    for line in malformed:
        report.errors.append(
            f"'## Field map summary' STALE line must read '{STALE_TEMPLATE}' (got {line[:80]!r})"
        )
    summary_stale = bool(valid or malformed)
    rows, errors = field_map_summary_rows(body)
    report.errors.extend(errors)
    mapped_marker = rows is not None or summary_stale or READINESS_LINE.search(
        text_outside_fences(body)
    ) is not None
    if unmapped and mapped_marker:
        report.errors.append(
            f"'## Field map summary' holds both '{NOT_YET_MAPPED}' and a mapped-state marker"
        )
    elif mapped_marker and rows is None:
        report.errors.append(
            "'## Field map summary' claims a field map (Readiness or STALE line) but holds no summary "
            "table (| Portal section | Portal label | field_id | Value to enter | Source | Review |) (A12)"
        )
    elif not unmapped and rows is None:
        report.errors.append(
            f"'## Field map summary' must hold the summary table once mapping has run, or the line "
            f"'{NOT_YET_MAPPED}' before it (A12)"
        )

    checklist = find_section(parsed, "Manual-entry checklist")
    if checklist is None or not checklist_requested(checklist.body):
        return
    checklist_valid, checklist_malformed = stale_lines(checklist.body)
    for line in checklist_malformed:
        report.errors.append(
            f"'## Manual-entry checklist' STALE line must read '{STALE_TEMPLATE}' (got {line[:80]!r})"
        )
    checklist_stale = bool(checklist_valid or checklist_malformed)
    if summary_stale and not checklist_stale:
        report.errors.append(
            "the field map is STALE, so the manual-entry checklist built from it must carry the "
            f"line '{STALE_TEMPLATE}' until regeneration (A10)"
        )
        return
    if checklist_stale or not rows:
        return
    expected: dict[str, tuple[str, Any]] = {}
    for row in rows:
        if row.field_id and row.field_id not in expected:
            if row.missing:
                expected[row.field_id] = ("missing", next(iter(sorted(row.question_ids)), None))
            else:
                expected[row.field_id] = ("value", row.value)
    tables, _ = field_table_rows(checklist.body)
    compare_rows(
        [row for _, table_rows in tables for row in table_rows],
        expected,
        set(),
        "'## Manual-entry checklist'",
        "'## Field map summary'",
        report.errors,
        require_every_field=False,
    )


def _check_chat_rendering(text: str, parsed: ParsedMarkdown, report: WorkpackReport) -> None:
    """A8: the conversation shows only filled sections and never YAML."""
    for section in parsed.sections:
        if normalize_heading(section.heading) in CHAT_EXCLUDED_SECTIONS:
            report.errors.append(
                f"line {section.line}: the conversation never shows '## {section.heading}'; "
                "the YAML appendices are written only into a saved workpack (A8)"
            )
        elif "[" in section.heading:
            report.errors.append(
                f"line {section.line}: heading '## {section.heading}' still holds a template placeholder"
            )
    blocks, _ = fenced_blocks(text)
    if any(info in {"yaml", "yml"} for info, _ in blocks):
        report.errors.append(
            "the conversation never prints a YAML block; the field map appears as its "
            "Field map summary table (A8)"
        )
    for line in text_outside_fences(text).split("\n"):
        if FILL_NOTE_LINE.match(line):
            report.errors.append(
                f"template fill note or placeholder shown in the conversation: {line.strip()[:70]!r}"
            )


def validate_workpack_text(
    text: str,
    *,
    expected_kind: str | None = None,
    expect_saved: bool = False,
    plugin_root: str | Path | None = None,
    presentation: str = "file",
) -> WorkpackReport:
    """Validate one workpack's Markdown and return a :class:`WorkpackReport`.

    ``presentation="chat"`` grades the conversation rendering (A8) instead of a
    saved file; it cannot be combined with ``expect_saved``.
    """
    if presentation not in PRESENTATIONS:
        raise ValueError(f"presentation must be one of {PRESENTATIONS} (got {presentation!r})")
    root = str(Path(plugin_root or DEFAULT_PLUGIN_ROOT).resolve())
    report = WorkpackReport()
    text = text.replace("\r\n", "\n")
    parsed = parse_markdown(text)
    if presentation == "chat":
        return _validate_chat_rendering(text, parsed, expected_kind, expect_saved, root, report)

    record, record_errors = resume_record_block(text)
    report.errors.extend(record_errors)
    report.resume_record = record

    record_kind = kind_for_workflow(record.get("workflow")) if isinstance(record, dict) else None
    kind = expected_kind or record_kind
    if kind is None and parsed.title:
        kind = "annual" if "2025" in parsed.title else "provisional" if "2026" in parsed.title else None
    if kind not in TAX_YEARS:
        report.errors.append("cannot tell whether this is the annual or the provisional workpack")
        return report
    report.kind = kind
    if expected_kind and record_kind and record_kind != expected_kind:
        report.errors.append(
            f"Appendix A workflow {record.get('workflow')!r} does not belong in the {expected_kind} "
            f"workpack {WORKPACK_PATHS[expected_kind]}"
        )

    questions = open_question_rows(text)
    _check_structure(parsed, kind, root, report)
    readiness = record.get("readiness") if isinstance(record, dict) else None
    _check_banner(parsed, readiness, report)
    if isinstance(record, dict):
        _check_resume_record(record, kind, root, expect_saved, questions, report)
        _check_subflow_heading(parsed, record.get("workflow"), report)
    _check_sources(parsed, record, kind, root, report)
    evidence_rows = _check_documents(text, parsed, report)
    _check_privacy_and_scope(
        text, kind, record.get("workflow") if isinstance(record, dict) else None, report
    )
    _check_field_map(text, parsed, record, kind, evidence_rows, questions, report)
    return report


def _validate_chat_rendering(
    text: str,
    parsed: ParsedMarkdown,
    expected_kind: str | None,
    expect_saved: bool,
    root: str,
    report: WorkpackReport,
) -> WorkpackReport:
    if expect_saved:
        report.errors.append("a conversation rendering is never a saved workpack; drop expect_saved")
    kind = expected_kind
    if kind is None and parsed.title:
        kind = "annual" if "2025" in parsed.title else "provisional" if "2026" in parsed.title else None
    if kind not in TAX_YEARS:
        report.errors.append("cannot tell whether this is the annual or the provisional workpack")
        return report
    report.kind = kind
    _check_chat_rendering(text, parsed, report)
    _check_structure(
        parsed,
        kind,
        root,
        report,
        excluded=CHAT_EXCLUDED_SECTIONS,
        optional=CHAT_OPTIONAL_SECTIONS,
    )
    _check_banner(parsed, None, report)
    _check_sources(parsed, None, kind, root, report)
    _check_documents(text, parsed, report)
    _check_privacy_and_scope(text, kind, None, report)
    _check_chat_field_map(parsed, kind, report)
    return report


def validate_workpack_file(
    path: str | Path,
    *,
    expected_kind: str | None = None,
    expect_saved: bool = False,
    plugin_root: str | Path | None = None,
    presentation: str = "file",
) -> WorkpackReport:
    path = Path(path)
    kind = expected_kind or kind_for_path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        report = WorkpackReport()
        report.errors.append(f"cannot read {path}: {exc}")
        return report
    return validate_workpack_text(
        text,
        expected_kind=kind,
        expect_saved=expect_saved,
        plugin_root=plugin_root,
        presentation=presentation,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate a saved NL tax workpack (.md) against the 0.4 structure."
    )
    parser.add_argument("workpacks", nargs="+", help="Workpack Markdown file(s).")
    parser.add_argument(
        "--kind",
        choices=sorted(TAX_YEARS),
        help="Workpack kind; inferred from the fixed file name or Appendix A when omitted.",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--expect-saved",
        action="store_true",
        help="Require the saved-file state: save_consent: given and timestamps set.",
    )
    mode.add_argument(
        "--chat",
        action="store_true",
        help="Grade a capture of the workpack as shown in the conversation (no appendices, no fill notes).",
    )
    parser.add_argument(
        "--plugin-root",
        default=str(DEFAULT_PLUGIN_ROOT),
        help="Plugin package root holding the templates and source register.",
    )
    args = parser.parse_args(argv)

    failed = False
    for workpack in args.workpacks:
        try:
            report = validate_workpack_file(
                workpack,
                expected_kind=args.kind,
                expect_saved=args.expect_saved,
                plugin_root=args.plugin_root,
                presentation="chat" if args.chat else "file",
            )
        except WorkpackGraderSetupError as exc:
            print(f"WORKPACK GRADER SETUP FAILED: {exc}", file=sys.stderr)
            return 1
        if report.ok:
            print(f"WORKPACK VALID: {workpack}")
        else:
            failed = True
            print(f"WORKPACK INVALID: {workpack}")
            for error in report.errors:
                print(f"  - {error}")
        for warning in report.warnings:
            print(f"  warning: {warning}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
