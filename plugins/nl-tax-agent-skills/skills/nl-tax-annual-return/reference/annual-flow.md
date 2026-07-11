# Annual Return Workpack Generation Flow

This is the common contract and ordered index for the 2025 annual-return workflow. Follow all 14 phases in order. If a phase cannot be completed because data is missing, record the gap and continue. The owning skill persists all state and artifacts; background helpers return facts and questions only.

Every time a knowledge file or rate sheet is loaded, record its matching `source_id` from `_shared/source-register.yaml` in `session-progress.yaml` → `sources_loaded` once. Only those IDs may appear in the workpack's Sources used section.

## Progressive loading

Load this common index when the annual workflow starts. Then load exactly one active phase file at a time, immediately before performing that phase. Each phase is linked directly here and from `SKILL.md`; do not follow a deeper reference chain.

1. [Phase 1 — Pre-flight checks](phases/01-preflight.md)
2. [Phase 1.5 — Filing status and late-filing exposure](phases/01-5-filing-status.md)
3. [Phase 2 — Income compilation](phases/02-income.md)
4. [Phase 2A — Winst uit onderneming preparation-only](phases/02a-winst.md)
5. [Phase 3 — Own-home compilation](phases/03-own-home.md)
6. [Phase 3A — Box 2 compilation](phases/03a-box2.md)
7. [Phase 4 — Box 3 compilation](phases/04-box3.md)
8. [Phase 5 — Deductions compilation](phases/05-deductions.md)
9. [Phase 5.5 — Credits screening](phases/05-5-credits.md)
10. [Phase 6 — Partner handling](phases/06-partner.md)
11. [Phase 7 — Field map generation](phases/07-field-map.md)
12. [Phase 8 — Missing info compilation](phases/08-missing-info.md)
13. [Phase 9 — Review question generation](phases/09-review-questions.md)
14. [Phase 10 — Workpack assembly](phases/10-assembly.md)

## Common contract

- Apply the conversational contract and generation gate in `SKILL.md` throughout.
- Keep annual and provisional notes and output paths separate.
- Never invent a missing amount or silently treat it as zero.
- Load phase-specific reviewed knowledge only when that phase needs it.
- Load the output contract and workpack template only after the generation gate opens in Phase 10.
- Preserve the phase order and all requirements in the linked phase files.
