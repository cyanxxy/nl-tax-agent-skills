# NL Tax Agent Skills

Prepare your Dutch income tax with an assistant that reads your documents,
asks only the questions that matter, and builds a reviewable, source-cited
workpack for manual entry in Mijn Belastingdienst. It covers the **annual
return 2025** and the **voorlopige aanslag 2026** (request, change, review, or
stopzetten), and answers rule questions for both years.

> **Not tax advice.** This plugin prepares workpacks and manual-entry guidance
> only. It never logs in, signs, or submits anything, and its output is not an
> official calculation. You review everything and enter it yourself.

## How to use it

Attach or select your documents (jaaropgaaf, mortgage statement, bank
overview, and so on) and ask in plain language:

```text
Help me prepare my 2025 Dutch income-tax workpack. I have my year statement and mortgage summary.
```

```text
Help me request a 2026 voorlopige aanslag. Ask me for the estimates you still need.
```

```text
What is the Box 3 heffingsvrij vermogen for 2025?
```

Everything happens in the conversation. The assistant reads your documents
directly, asks for missing facts, and shows the workpack, in which every amount
names its source. It then maps each amount to its Mijn Belastingdienst field and
can produce a manual-entry checklist. A rule question gets a sourced answer with
the tax year.

If you correct a figure after the workpack is generated, the field map and any
checklist are marked **STALE** and the assistant will not give you checklist
values until you confirm regenerating them, so an old amount is never copied
into the portal.

## Saving your work

The plugin writes nothing unless you ask. Tax preparation can take a few
sessions, so the assistant offers to keep your workpack as a file when the
workflow starts, when you pause, and after the workpack is generated, each at
most once and always as the only question in its reply (tell it not to ask
again and it stops). Say yes, or "save my workpack" at any time, and it keeps
**one file per workflow** in a `workspace/` folder inside your working folder:

- `workspace/nl-tax-annual-2025-workpack.md` for the annual 2025 return
- `workspace/nl-tax-provisional-2026-workpack.md` for the 2026 voorlopige aanslag

That one readable Markdown file holds your facts with their sources, the open
questions, the field map, and the manual-entry checklist. It is your file: to
continue later, attach it or keep it in the working folder. Consent covers the
current conversation: in a new one, the assistant confirms a saved file before
using or updating it, and asks before replacing an older file it did not
resume; it never merges into one. Showing the workpack in the chat creates no
file. In a cloud task whose folder may not outlast the session, it also gives
you the workpack as a download at pauses and at generation: keep that download
to resume. Delete the file whenever you like; the plugin never deletes files.
Say "stop saving" and it stops updating the file.

## What the plugin runs, reads, writes, and fetches

- **Runs:** nothing. The package ships Markdown and YAML only: no scripts,
  hooks, MCP servers, or package installs. No shell or Python is needed, and
  skills pre-approve no shell commands.
- **Reads:** its bundled, source-cited Dutch tax notes, plus the documents,
  folders, and saved workpack you select or attach.
- **Writes:** nothing by default. Only after you agree to save, one workpack
  file per workflow (the two paths above) and nothing else. Skills pre-approve
  file edits for `./workspace/**` only, and never copy, move, rename, or change
  your documents.
- **Fetches:** nothing by default; skills answer from the bundled notes. When a
  workflow calls for a freshness check, the assistant may read public official
  pages such as belastingdienst.nl. The plugin sends your data to no one and
  never opens Mijn Belastingdienst or any other authenticated portal.

The plugin runs inside your AI host, which processes the documents and
conversation you share under its own terms.

## What is supported

| Workflow | Year |
|---|---|
| Annual income-tax return, including Box 1 and own home, Box 2, Box 3, and deductions | 2025 |
| Winst uit onderneming for a straightforward eenmanszaak / ZZP | 2025 |
| Voorlopige aanslag: request, change, review, stopzetten | 2026 |
| Rule questions | 2025 / 2026 |

For Box 3, annual 2025 compares the fictitious and actual-return methods as
information only; provisional 2026 uses the fictitious method only. Other
business forms (VOF, maatschap, CV, DGA/BV, staking), part-year residence, and
tax year 2027 are routed to manual review or blocked.

## Skills

| Skill | Role |
|---|---|
| `nl-tax-intake` | Checks scope and starts the right workflow; writes nothing |
| `nl-tax-knowledge` | Answers 2025 / 2026 rule questions; writes nothing |
| `nl-tax-annual-return` | Prepares the annual 2025 workpack and reads your documents |
| `nl-tax-provisional-assessment` | Prepares the 2026 voorlopige aanslag workpack and reads your documents |
| `nl-tax-field-mapper` | Maps workpack amounts to Mijn Belastingdienst fields; the only author of the field map |
| `nl-tax-submit-companion` | Builds a manual-entry checklist when you ask for one |
| `nl-tax-box1-home`, `nl-tax-box2`, `nl-tax-box3`, `nl-tax-winst`, `nl-tax-partner-deductions` | Background helpers the workflows consult; they write nothing |

`skills/nl-tax-shared-resources/` holds the reviewed knowledge notes, the source
register, and the shared runtime contract. Install the plugin as one package:
the skills reference each other through sibling paths.

## More

- [Privacy](https://github.com/cyanxxy/nl-tax-agent-skills/blob/main/PRIVACY.md):
  what the plugin reads, stores, and sends (it sends nothing), and how to delete
  a saved workpack.
- Install steps and contributor docs: <https://github.com/cyanxxy/nl-tax-agent-skills>. Licensed under Apache-2.0;
see the bundled [LICENSE](LICENSE).
