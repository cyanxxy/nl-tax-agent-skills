# NL Tax Agent Skills

Prepare your Dutch income tax with an assistant that reads your documents,
asks only the questions that matter, and produces a reviewable, source-cited
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

The assistant sorts your evidence, asks for missing facts, and writes a
workpack in which every amount shows its source. It then maps each amount to its
Mijn Belastingdienst field and can produce a manual-entry checklist. A rule
question gets a sourced answer with the tax year, and creates no files.

## What the plugin runs, reads, and writes

- **Runs:** nothing. The package ships Markdown and YAML only: no scripts,
  hooks, MCP servers, or package installs. No shell or Python is needed, and
  skills pre-approve no shell commands.
- **Reads:** its bundled, source-cited Dutch tax notes, plus the documents and
  folders you select or attach.
- **Writes:** only under `workspace/` in the task's working folder (skills
  pre-approve file edits for `./workspace/**` only).
- **Fetches:** skills answer from the bundled notes. The optional Claude
  reviewer agent may read public official pages such as belastingdienst.nl to
  check freshness. The plugin sends no taxpayer data anywhere and never opens
  Mijn Belastingdienst or any other authenticated portal.

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
| `nl-tax-intake` | Checks scope and starts the right workflow |
| `nl-tax-knowledge` | Answers 2025 / 2026 rule questions; writes nothing |
| `nl-tax-evidence-indexer` | Catalogs your documents and chat amounts with their sources |
| `nl-tax-annual-return` | Prepares the annual 2025 workpack |
| `nl-tax-provisional-assessment` | Prepares the 2026 voorlopige aanslag workpacks |
| `nl-tax-field-mapper` | Maps workpack amounts to Mijn Belastingdienst fields |
| `nl-tax-submit-companion` | Writes a manual-entry checklist when you ask for one |
| `nl-tax-box1-home`, `nl-tax-box2`, `nl-tax-box3`, `nl-tax-winst`, `nl-tax-partner-deductions` | Background helpers the workflows consult; they write nothing |

`skills/nl-tax-shared-resources/` holds the reviewed knowledge notes, the source
register, and the shared runtime contract. Install the plugin as one package:
the skills reference each other through sibling paths.

## More

Install steps, privacy, and contributor docs live in the repository:
<https://github.com/cyanxxy/nl-tax-agent-skills>. Licensed under Apache-2.0;
see the bundled [LICENSE](LICENSE).
