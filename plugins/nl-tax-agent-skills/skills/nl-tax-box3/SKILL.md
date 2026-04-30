---
name: nl-tax-box3
description: Background Dutch box 3 knowledge for annual return 2025 and voorlopige aanslag 2026. Use for asset classification, annual actual-vs-fictitious comparison notes, and provisional fictitious box 3 notes.
user-invocable: false
allowed-tools: Read Grep Bash(python ${CLAUDE_SKILL_DIR}/../nl-tax-box3/scripts/*.py *)
---

# nl-tax-box3

THIS IS A CRITICAL SKILL that enforces the annual/provisional box 3 distinction.

## What it does

1. Classify assets into banktegoeden, overige bezittingen, schulden
2. For annual 2025: support BOTH fictitious and actual-return notes
3. For provisional 2026: use ONLY fictitious provisional method
4. Generate partner allocation notes where applicable

## HARD RULES

- **Annual 2025 path**: collect data for BOTH fictitious and werkelijk rendement, compare, note which appears favorable
- **Provisional 2026 path**: ONLY fictitious method. NEVER ask for werkelijk rendement.
- If workflow is provisional and user asks about actual return: explain it may be relevant later in the annual 2026 return

## Knowledge sources

- `${CLAUDE_SKILL_DIR}/../_shared/knowledge/years/2025/box3/fictitious.md`
- `${CLAUDE_SKILL_DIR}/../_shared/knowledge/years/2025/box3/actual-return.md`
- `${CLAUDE_SKILL_DIR}/../_shared/knowledge/years/2025/box3/examples.md`
- `${CLAUDE_SKILL_DIR}/../_shared/knowledge/years/2026/provisional/box3-provisional.md`
- `${CLAUDE_SKILL_DIR}/../nl-tax-box3/reference/**`

## Output

- `workspace/shared/box3-notes.md`
- `workspace/shared/box3-review-questions.md`

## Must NOT write to

- `workspace/annual/2025/return-pack.md`
- `workspace/provisional/2026/provisional-pack.md`
