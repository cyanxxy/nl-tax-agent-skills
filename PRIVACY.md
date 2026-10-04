# Privacy Policy

This policy covers the `nl-tax-agent-skills` plugin. The plugin is a set of
skills (Markdown and YAML instructions) that runs inside the AI host you choose:
Claude (Cowork, Claude Code, or the Claude apps), ChatGPT Work, or Codex. It has
no backend, no server, and no account. The plugin authors receive none of your
data.

## In short

- **Reads personal data:** yes, the documents and facts you share for your own
  tax preparation, which for VAT, ICP, and OSS can include personal data of
  your customers and suppliers.
- **Stores personal data:** only if you ask. Then it keeps one workpack file per
  workflow (and, for VAT, ICP, and OSS, one per period or scheme) in your own
  working folder, until you delete it.
- **Sends data elsewhere:** no.

## What the plugin reads

When you ask it to prepare a tax workpack, the plugin instructs the host's AI
model to read:

- the documents you attach or select, such as a jaaropgaaf, mortgage statement,
  or bank overview, which contain personal and financial data;
- for the draft VAT, ICP, and OSS workflows: sales and purchase invoices and
  ledgers, which can include your customers' and suppliers' names, addresses,
  and VAT numbers; for the draft M (migration) and C (nonresident) returns:
  residence, insurance, and foreign-income records. The workpack keeps only
  aliases, countries, dates, and amounts from these documents;
- the facts you state in the conversation; and
- a workpack you saved earlier, when you attach it or it is in your working
  folder, so you can continue where you left off.

It reads only what you provide for your own tax preparation. It never asks for
a BSN, an IBAN, DigiD details, passwords, verification codes, or portal
sessions, and never opens Mijn Belastingdienst.

## What the plugin stores

Nothing, unless you ask. By default the whole preparation (your facts, the
questions, the workpack, the field map, and the manual-entry checklist) stays in
the conversation, and the plugin writes no file.

If you agree to save, or ask it to ("save my workpack"), the plugin keeps
**one file per workflow, period or scheme** in a `workspace/` folder inside
your working folder:

- `workspace/nl-tax-annual-2025-workpack.md` for the annual 2025 return;
- `workspace/nl-tax-provisional-2026-workpack.md` for the 2026 voorlopige
  aanslag;
- `workspace/nl-tax-annual-2026-workpack.md` for the draft annual return 2026;
- `workspace/nl-tax-vat-<year>-<period>-workpack.md` for a draft 2025/2026 VAT
  return, and `workspace/nl-tax-vat-correction-<year>-<period>-workpack.md`
  for a draft VAT correction;
- `workspace/nl-tax-icp-<year>-<period>-workpack.md` for a draft ICP
  declaration;
- `workspace/nl-tax-oss-<scheme>-<year>-<period>-workpack.md` for a draft OSS
  or IOSS return; and
- `workspace/nl-tax-international-<year>-<form>-workpack.md` for a draft M
  (migration) or C (nonresident) return.

Each confirmed monthly, quarterly, or annual period, each OSS scheme, and each
M or C form stays in its own file. The VAT adjustment helper writes no file.
The VAT, ICP, and OSS workpacks use local evidence IDs and customer aliases
instead of retaining VAT identification numbers, invoice numbers, or
customers' and suppliers' personal data. The dates, countries, amounts, and
eligibility evidence that the tax rules need are kept as sourced facts. You
check and enter real customer VAT identification numbers, and any registration
or payment details, yourself in Mijn Belastingdienst Zakelijk. If they appear
in documents you share, the assistant does not copy them into the workpack.

Each is a plaintext Markdown file holding the facts you provided with their
sources, open questions, the field map, and the manual-entry checklist. The
plugin does not encrypt it. The workpack never records a full BSN, IBAN,
policy, contract, or aanslag number, or any credential: a provider name and tax
year identify each document. The plugin keeps each workpack file up to date
while you work, writes no other file, and never copies, moves, renames, or changes
your own documents. Say "stop saving" and it stops updating the file.

Your consent covers the current conversation. In a new conversation, the
assistant confirms a saved file before it uses or updates it, and it never
overwrites an older workpack you did not resume without asking whether to
replace it. Showing the workpack in the conversation creates no file; a
download counts as saving and is offered only with your consent.

The file stays wherever your host keeps the working folder: on your computer
for a local task with a local folder. In a cloud task without a connected local
folder, the file lives in the host's task storage and may not outlast the
session, so the assistant also gives you the workpack as a download at pauses
and when it is generated: the download is the copy you keep, to attach later.
If your host offers no writable folder at all, the download is the only copy.

## What the plugin sends, and to whom

The plugin sends your data to no one: not to the plugin authors, not to the
Belastingdienst, and not to any other third party. It has no connectors, MCP
servers, or scripts, and makes no network calls by default. When a workflow
calls for a freshness check, the assistant or the optional Claude reviewer
agent may read public official pages, such as belastingdienst.nl, to check that
tax sources are current; this sends no taxpayer data.

Your AI host does process everything you share with it, under its own terms.
This plugin is **not** a local-only or offline guarantee. See your host's
privacy policy for how it handles prompts and files.

## Retention and deletion

The plugin keeps no data of its own, so there is nothing for the authors to
retain or delete. A saved workpack stays until you delete it; the plugin never
deletes files. When you no longer need it, delete the file for that workflow,
period, scheme, or form:

- `workspace/nl-tax-annual-2025-workpack.md`
- `workspace/nl-tax-provisional-2026-workpack.md`
- `workspace/nl-tax-annual-2026-workpack.md`
- `workspace/nl-tax-vat-<year>-<period>-workpack.md`
- `workspace/nl-tax-vat-correction-<year>-<period>-workpack.md`
- `workspace/nl-tax-icp-<year>-<period>-workpack.md`
- `workspace/nl-tax-oss-<scheme>-<year>-<period>-workpack.md`
- `workspace/nl-tax-international-<year>-<form>-workpack.md`

For example, from your working folder, list what is there first and then
delete all saved workpacks:

```bash
ls workspace/nl-tax-*-workpack.md
rm workspace/nl-tax-*-workpack.md
```

Check the contents before deleting, because this cannot be undone. Remember
that cloud-sync folders, backups, shared drives, and any `uploads/` or
`evidence/` folders where you kept your own documents may hold copies.

The conversation itself, including the documents you attached to it, is kept
by your AI host under its own retention settings. Delete it there if you no
longer want it kept.

## Children

The plugin is intended for adults preparing their own Dutch income tax or
sole-trader VAT. It is not intended for people under 18.

## Contact

Ask privacy questions or report a concern through
[GitHub Issues](https://github.com/cyanxxy/nl-tax-agent-skills/issues). For a
sensitive report, use a private
[GitHub Security Advisory](https://github.com/cyanxxy/nl-tax-agent-skills/security/advisories/new),
as described in [SECURITY.md](SECURITY.md). Never include real taxpayer data,
BSNs, IBANs, or official documents in a report.

## Changes

Changes to this policy are recorded in the repository history and in
[CHANGELOG.md](CHANGELOG.md).
