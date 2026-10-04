"""Build filled 0.4 workpacks from the real plugin templates for tests.

Not a test module: test files load it by path. Every sample starts from
``annual-workpack.md`` or ``provisional-workpack.md`` and replaces only the
parts a saved workpack must fill (STATUS banner, Subflow heading, Documents and
sources, Sources used, Open questions, Field map summary, and both appendices),
so structural template changes flow straight into the tests.
"""

from __future__ import annotations

import importlib.util
import pathlib
import re

import yaml


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "nl-tax-agent-skills"
GRADER_PATH = REPO_ROOT / "tools/nl_tax_agent_skills/workpack/validate_workpack.py"
FIELD_MAP_GRADER_PATH = REPO_ROOT / "tools/nl_tax_agent_skills/field_mapper/validate_field_map.py"

TEMPLATES = {
    "annual": PLUGIN_ROOT / "skills/nl-tax-annual-return/templates/annual-workpack.md",
    "provisional": PLUGIN_ROOT
    / "skills/nl-tax-provisional-assessment/templates/provisional-workpack.md",
    "vat": PLUGIN_ROOT / "skills/nl-tax-vat-return/templates/vat-workpack.md",
    "vat_correction": PLUGIN_ROOT / "skills/nl-tax-vat-correction/templates/vat-correction-workpack.md",
}
ANNUAL_PATH = "workspace/nl-tax-annual-2025-workpack.md"
PROVISIONAL_PATH = "workspace/nl-tax-provisional-2026-workpack.md"

ANNUAL_SOURCES = ("bd_box1_rates_2025", "bd_jaaropgaaf_fields_2025")
PROVISIONAL_SOURCES = ("bd_box1_rates_2026", "bd_provisional_request_2026")

ANNUAL_DOCUMENTS = (
    (
        "ev_001",
        "jaaropgaaf-2025",
        "jaaropgaaf",
        "2025",
        "taxpayer",
        "page 1",
        "fiscaal loon: EUR 48,250; loonheffing: EUR 13,100",
        "extracted",
    ),
)
PROVISIONAL_DOCUMENTS = (
    (
        "ev_001",
        "chat 2026-09-20",
        "user_chat",
        "2026",
        "taxpayer",
        "chat",
        'expected salary: "my 2026 salary will be about EUR 58,000"',
        "extracted",
    ),
)

ANNUAL_FIELD_MAP = {
    "field_map_version": "1.1",
    "workflow": "annual_return",
    "tax_year": 2025,
    "created_at": "2026-09-20T10:00:00Z",
    "updated_at": "2026-09-20T10:00:00Z",
    "readiness": "draft",
    "check_performed_by": "checked_by_agent",
    "fields": [
        {
            "field_id": "box1.loon",
            "label": "Loon",
            "entry_mode": "manual_entry",
            "value": 48250,
            "source": {"type": "evidence", "evidence_id": "ev_001"},
            "confidence": 0.95,
            "manual_review_required": False,
            "notes": [],
        },
        {
            "field_id": "box1.loonheffing",
            "label": "Ingehouden loonheffing",
            "entry_mode": "manual_entry",
            "value": 13100,
            "source": {"type": "evidence", "evidence_id": "ev_001"},
            "confidence": 0.95,
            "manual_review_required": False,
            "notes": [],
        },
    ],
    "missing_fields": [],
    "user_chat_values_index": [],
    "notes": [],
}
PROVISIONAL_FIELD_MAP = {
    "field_map_version": "1.1",
    "workflow": "provisional_assessment",
    "tax_year": 2026,
    "created_at": "2026-09-20T10:00:00Z",
    "updated_at": "2026-09-20T10:00:00Z",
    "readiness": "draft",
    "check_performed_by": "checked_by_agent",
    "fields": [
        {
            "field_id": "box1.geschat_loon",
            "label": "Geschat inkomen uit werk",
            "entry_mode": "manual_entry",
            "value": 58000,
            "source": {
                "type": "user_chat",
                "quote": "my 2026 salary will be about EUR 58,000",
                "stated_at": "2026-09-20",
            },
            "confidence": 0.8,
            "manual_review_required": True,
            "notes": [],
        }
    ],
    "missing_fields": [],
    "user_chat_values_index": [
        {
            "field_id": "box1.geschat_loon",
            "value": 58000,
            "quote": "my 2026 salary will be about EUR 58,000",
            "stated_at": "2026-09-20",
        }
    ],
    "notes": [],
}


def _load(path: pathlib.Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_grader():
    return _load(GRADER_PATH, "validate_workpack_under_test")


def load_field_map_grader():
    return _load(FIELD_MAP_GRADER_PATH, "validate_field_map_under_test")


def replace_section(text: str, heading: str, new_body: str) -> str:
    """Replace the body of ``## <heading>`` (outside fences) with ``new_body``."""
    lines = text.split("\n")
    fence = None
    start = end = None
    for index, line in enumerate(lines):
        stripped = line.strip()
        if fence is not None:
            if stripped.startswith(fence) and set(stripped) == {fence[0]}:
                fence = None
            continue
        opener = re.match(r"^(`{3,}|~{3,})", stripped)
        if opener:
            fence = opener.group(1)
            continue
        if line.startswith("## "):
            if start is not None and end is None:
                end = index
                break
            if line[3:].strip() == heading:
                start = index
    if start is None:
        raise KeyError(f"section not found: {heading}")
    end = end if end is not None else len(lines)
    body = new_body.strip("\n").split("\n")
    return "\n".join(lines[: start + 1] + [""] + body + [""] + lines[end:])


def table(headers, rows) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for row in rows:
        out.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(out)


def default_statuses(kind: str, workflow: str, fill: str = "not_started") -> dict:
    grader = load_grader()
    required, _ = grader.expected_section_keys(str(PLUGIN_ROOT.resolve()), workflow)
    return {key: fill for key in sorted(required)}


def build_workpack(
    kind: str = "annual",
    *,
    workflow: str | None = None,
    readiness: str = "draft",
    save_consent: str = "given",
    generation_confirmed: bool | None = None,
    queued_workflow: str | None = None,
    statuses: dict | None = None,
    open_questions: dict | None = None,
    questions: tuple = (),
    sources: tuple | None = None,
    documents: tuple | None = None,
    field_map: dict | None = None,
    checklist_rows: tuple | None = None,
    stale: tuple | None = None,
    created_at: str = "2026-09-20T09:00:00Z",
    updated_at: str = "2026-09-20T10:30:00Z",
    record_overrides: dict | None = None,
) -> str:
    """Return a filled workpack that the grader accepts unless a test breaks it.

    ``questions`` rows are ``(qid, section, question, blocking)``;
    ``open_questions`` maps section key -> list of Q-IDs. A mapped sample
    (``field_map``) defaults to a completed ``confirm`` section, because mapping
    only follows a confirmed generation. ``checklist_rows`` fills the
    Manual-entry checklist with a step table of ``(step, label, value, source,
    field_id)`` rows. ``stale=(fact, date)`` marks the workpack stale after a
    changed fact (review amendment A10): ``generation_confirmed`` false and the
    STALE line at the top of the summary, Appendix B, and a requested checklist.
    """
    workflow = workflow or {"annual": "annual_2025", "provisional": "provisional_2026_request", "vat": "vat_2026_Q3", "vat_correction": "vat_correction_2026_Q3"}[kind]
    subflow = workflow.rsplit("_", 1)[-1] if kind == "provisional" else None
    text = TEMPLATES[kind].read_text(encoding="utf-8")
    identity = load_grader()._VAT.parse_resume_identity(workflow)
    if identity:
        text = text.replace("{year}", str(identity[1])).replace("{period}", identity[2])

    if statuses is None:
        fill = "complete" if readiness == "review_ready" else "not_started"
        statuses = default_statuses(kind, workflow, fill)
        if field_map is not None and "confirm" in statuses:
            statuses["confirm"] = "not_started" if stale else "complete"
    if generation_confirmed is None:
        generation_confirmed = statuses.get("confirm") == "complete"
    open_questions = open_questions or {}
    sections = {
        key: {"status": status, "open": list(open_questions.get(key, []))}
        for key, status in statuses.items()
    }
    default_sources = ANNUAL_SOURCES if kind == "annual" else PROVISIONAL_SOURCES if kind == "provisional" else ()
    sources = tuple(sources if sources is not None else default_sources)
    documents = documents if documents is not None else (
        ANNUAL_DOCUMENTS if kind == "annual" else PROVISIONAL_DOCUMENTS
    )

    open_count = sum(1 for status in statuses.values() if status not in {"complete", "chat_only"})
    banner = (
        "> **STATUS: COMPLETE DRAFT FOR REVIEW — not for filing.** Review and enter it "
        "manually in Mijn Belastingdienst."
        if readiness == "review_ready"
        else f"> **STATUS: DRAFT — {open_count} open section(s) — not for filing.** Review "
        "and enter it manually in Mijn Belastingdienst."
    )
    text = re.sub(r"(?m)^> \*\*STATUS:.*$", banner, text, count=1)

    if kind == "provisional":
        text = re.sub(r"(?m)^## Subflow: \[.*\]$", f"## Subflow: {subflow}", text, count=1)

    doc_headers = ["ID", "Document", "Type", "Tax year", "Owner", "Location", "Values taken", "Status"]
    text = replace_section(
        text,
        "Documents and sources",
        table(doc_headers, documents) if documents else "None yet.",
    )
    text = replace_section(text, "Sources used", "\n".join(f"- {sid}" for sid in sources) or "None yet.")

    if questions:
        body = table(
            ["Q-ID", "Section", "Question", "Blocking", "Status"],
            [(qid, f"`{section}`", question, blocking, "open") for qid, section, question, blocking in questions],
        )
    else:
        body = "None -- no open questions."
    text = replace_section(text, "Open questions", body)

    no_map_subflow = subflow in {"review", "stopzetten"}
    stale_line = stale_marker(*stale) if stale else None
    if field_map is not None:
        summary = summary_table(field_map)
        appendix_b = "```yaml\n" + yaml.safe_dump(field_map, sort_keys=False, allow_unicode=True) + "```"
        if stale_line:
            summary = stale_line + "\n\n" + summary
            appendix_b = stale_line + "\n\n" + appendix_b
    else:
        summary = "N/A — no field map is produced for this subflow." if no_map_subflow else "not yet mapped"
        appendix_b = "not yet mapped"
    text = replace_section(text, "Field map summary", summary)
    text = replace_section(text, "Appendix B — Field map", appendix_b)
    if checklist_rows is not None:
        body = "### 4. Steps\n\n" + table(
            ["Step", "Portal label", "Value to enter", "Source", "field_id"], checklist_rows
        )
        if stale_line:
            body = stale_line + "\n\n" + body
        text = replace_section(text, "Manual-entry checklist", body)

    record = {
        "workpack_format": "nl-tax-workpack",
        "workpack_version": "2.0",
        "plugin_version": "0.4.0",
        "workflow": workflow,
        "tax_year": 2025 if kind == "annual" else 2026,
        "created_at": created_at,
        "updated_at": updated_at,
        "save_consent": save_consent,
        "readiness": readiness,
        "generation_confirmed": generation_confirmed,
        "queued_workflow": queued_workflow,
        "sections": sections,
        "sources_loaded": list(sources),
    }
    if identity:
        record["tax_year"] = identity[1]
        record["period"] = identity[2]
    if record_overrides:
        for key, value in record_overrides.items():
            if value is _DELETE:
                record.pop(key, None)
            else:
                record[key] = value
    appendix_a = "```yaml\n" + yaml.safe_dump(record, sort_keys=False, allow_unicode=True) + "```"
    text = replace_section(text, "Appendix A — Resume record", appendix_a)
    return text


STALE_TEMPLATE = "STALE — predates the change to {fact} ({date}); regenerate before use."


def stale_marker(fact: str, date: str) -> str:
    """Return the A10 stale line for a changed ``fact`` on ``date``."""
    return STALE_TEMPLATE.format(fact=fact, date=date)


def summary_row_values(field_map: dict) -> list[tuple]:
    """Return the Field map summary rows the mapper renders for ``field_map``.

    Internal-routing records are excluded; a field without a value and every
    ``missing_fields`` entry become ``MISSING - enter manually`` rows naming
    their Q-ID (mapper-flow.md section 7).
    """
    questions = {
        entry.get("field_id"): entry.get("open_question_id")
        for entry in field_map.get("missing_fields", []) or []
    }
    rows = []
    seen = set()
    for field in field_map.get("fields", []) or []:
        if field.get("entry_mode") == "internal_routing":
            continue
        seen.add(field["field_id"])
        if field.get("value") is None:
            rows.append(
                ("Box 1", field.get("label", ""), field["field_id"], "MISSING - enter manually",
                 questions.get(field["field_id"]) or "", "Blocking")
            )
        else:
            rows.append(
                ("Box 1", field.get("label", ""), field["field_id"], field.get("value"), "mapped", "check")
            )
    for entry in field_map.get("missing_fields", []) or []:
        if entry.get("field_id") in seen:
            continue
        rows.append(
            ("Box 3", entry.get("label", ""), entry["field_id"], "MISSING - enter manually",
             entry.get("open_question_id") or "", "Blocking")
        )
    return rows


def summary_table(field_map: dict) -> str:
    return table(
        ["Portal section", "Portal label", "field_id", "Value to enter", "Source", "Review"],
        summary_row_values(field_map),
    )


def strip_fill_notes(text: str) -> str:
    """Remove every bracketed block that opens a line (template fill notes).

    Checkboxes (``[ ]``/``[x]``) and Markdown links never open a line in the
    templates, so only fill notes and placeholders (also indented continuation
    placeholders) are removed.
    """
    out: list[str] = []
    index = 0
    at_line_start = True
    while index < len(text):
        char = text[index]
        if at_line_start and char in " \t":
            out.append(char)
            index += 1
            continue
        if at_line_start and char == "[":
            depth = 0
            end = index
            while end < len(text):
                if text[end] == "[":
                    depth += 1
                elif text[end] == "]":
                    depth -= 1
                    if depth == 0:
                        break
                end += 1
            index = end + 1
            if index < len(text) and text[index] == "\n":
                index += 1
            continue
        out.append(char)
        at_line_start = char == "\n"
        index += 1
    return re.sub(r"\n{3,}", "\n\n", "".join(out))


def build_chat_rendering(kind: str = "annual", **kwargs) -> str:
    """Return the workpack as shown in the conversation (review amendment A8).

    Starts from :func:`build_workpack`, then drops both YAML appendices, the
    ``Manual-entry checklist`` section unless ``checklist_rows`` requested it,
    and every template fill note: the conversation shows only filled sections
    and never YAML.
    """
    text = build_workpack(kind, **kwargs)
    headings = ["Appendix A — Resume record", "Appendix B — Field map"]
    if kwargs.get("checklist_rows") is None:
        headings.append("Manual-entry checklist")
    for heading in headings:
        text = remove_section(text, heading)
    return strip_fill_notes(text)


def remove_section(text: str, heading: str) -> str:
    """Remove ``## <heading>`` and its body (outside fences)."""
    lines = text.split("\n")
    fence = None
    start = end = None
    for index, line in enumerate(lines):
        stripped = line.strip()
        if fence is not None:
            if stripped.startswith(fence) and set(stripped) == {fence[0]}:
                fence = None
            continue
        opener = re.match(r"^(`{3,}|~{3,})", stripped)
        if opener:
            fence = opener.group(1)
            continue
        if line.startswith("## "):
            if start is not None and end is None:
                end = index
                break
            if line[3:].strip() == heading:
                start = index
    if start is None:
        raise KeyError(f"section not found: {heading}")
    end = end if end is not None else len(lines)
    return "\n".join(lines[:start] + lines[end:])


class _Delete:
    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return "<delete>"


_DELETE = _Delete()
DELETE = _DELETE
