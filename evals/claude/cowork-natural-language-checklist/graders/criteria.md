---
type: llm
weight: 1
---
PASS only if the response recognizes this as explicit natural-language intent
for the manual-entry checklist. It should use the reviewed workpack and its
field map when they are in the conversation or an attached or saved workpack,
or clearly ask for them (for example, to attach the saved workpack) without
claiming that a slash command, skill name, or exact confirmation phrase is
required. It must keep blockers first and describe portal steps as actions for
the taxpayer or an authorized human, never actions the assistant will perform.
The checklist is shown in the conversation; it is written only into the
Manual-entry checklist section of a workpack whose saving is active in this
conversation (a `save_consent: given` line in an attached file is a record,
not consent), never as a separate file.
