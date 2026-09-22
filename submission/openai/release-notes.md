# OpenAI Plugin Directory release 0.3.0

NL Tax Agent Skills is a skills-only plugin for preparing source-traceable Dutch
individual income-tax workpacks for manual Mijn Belastingdienst entry. The
release supports annual 2025 preparation and 2026 voorlopige aanslag
request, change, review, and stopzetten workflows.

This release makes the bundled, reviewed knowledge pack usable as an on-demand
knowledge base in Codex, Claude, and other Agent Skills hosts. A new read-only
skill, `nl-tax-knowledge`, answers 2025 annual and 2026 provisional rule
questions from the reviewed notes. It states the tax year of every figure,
names the official source, asks no screening questions, collects no personal
data, and writes no files. Codex may select it implicitly for a plain rule
question.

A new `knowledge-index.md` maps every topic, tax year, and workflow to the one
reviewed note that answers it, with the Dutch and English terms that select it.
Agents open the index and then only the matching note, instead of guessing
filenames or answering from model memory. Every note in the knowledge pack is
now reachable, including the law, authorization, and Box 3 example notes.

The shared resource folder is now named `nl-tax-shared-resources`, matching its
skill name as the Agent Skills specification requires. Every bundled path is
written relative to the skill directory, and the annual and provisional
workflows name each helper skill's file path, so hosts without a skill-invocation
tool can follow a helper's instructions directly. Install the plugin as one
package; the skills reference each other as siblings.

No tax rule, rate, threshold, or cited source changed in this release. The 17
reviewed notes touched were changed only by the folder rename and a uniform
header-key format, verified byte-for-byte against the previous release.

Annual 2025 and provisional 2026 remain rigorously separate, including the box 3
rule that provisional 2026 uses the fictitious method only and never collects or
computes werkelijk rendement.

The plugin has no connected apps, external authentication, portal automation,
filing, signing, or submission capability. That boundary applies even when
Chrome, computer use, connectors, credentials, or user permission are available:
the assistant creates an explicitly human-owned checklist, and the taxpayer or
an authorized human performs every authenticated portal action. The release
passes 448 repository tests and validates all 237 registered sources without
errors or warnings. Python remains optional.
