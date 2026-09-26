# OpenAI Plugin Directory release 0.4.0

NL Tax Agent Skills is a skills-only plugin for preparing source-traceable Dutch
individual income-tax workpacks for manual Mijn Belastingdienst entry. It
supports annual 2025 preparation, the 2026 voorlopige aanslag request, change,
review, and stopzetten workflows, and read-only rule questions for both years.

This release makes the plugin conversation-first. Nothing is written by
default: collection, recaps, the workpack, the field map, and the manual-entry
checklist all happen in the conversation. Only when the user agrees does the
plugin keep one workpack file per workflow in the user's working folder
(`workspace/nl-tax-annual-2025-workpack.md` or
`workspace/nl-tax-provisional-2026-workpack.md`), updated in place. That one
file holds the readable workpack, a short resume record, and the field map, so
the user can attach it later to continue. The background profile, session,
evidence-index, notes, and separate map, delta, review-question, and checklist
files are gone, and so is the separate evidence-indexer skill: documents are
read directly inside the annual or provisional workflow and recorded as rows
in the workpack's Documents and sources section.

No tax rule, rate, threshold, or cited source changed. Annual 2025 and
provisional 2026 remain rigorously separate, including the box 3 rule that
provisional 2026 uses the fictitious method only and never collects or
computes werkelijk rendement.

The package still ships Markdown and YAML only: no scripts, hooks, MCP servers,
or package installs, and no shell or Python is needed. The plugin has no
connected apps, external authentication, portal automation, filing, signing,
or submission capability. That boundary applies even when Chrome, computer
use, connectors, credentials, or user permission are available: the taxpayer
or an authorized human performs every authenticated portal action.
