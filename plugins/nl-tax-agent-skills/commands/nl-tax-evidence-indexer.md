---
description: Catalog and hash Dutch tax documents (`jaaropgaaf`, `bankafschrift`, `woz_beschikking`, `hypotheek_jaaroverzicht`, `voorlopige_aanslag_beschikking`) and chat-stated amounts into an evidence index. Use when the user shares or mentions tax documents, or a workflow needs evidence for a section.
argument-hint: "[path-to-upload-folder]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - Bash(python3:*)
---

# NL Tax Evidence Indexer

Follow the bundled `nl-tax-evidence-indexer` workflow internally with arguments: `$ARGUMENTS`. Do not tell the user the skill name or command wrapper; report only the evidence-indexing result or the next needed user action.
