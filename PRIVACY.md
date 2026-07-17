# Privacy and Data Handling

This document describes how the `nl-tax-agent-skills` plugin handles data. It is
not a corporate privacy policy for a hosted service — the plugin is not a hosted
service. It runs inside whatever LLM agent host (Claude Code, Cowork, Codex, or
another compatible host) you choose to run it in.

## Important: this is not a "local-only" guarantee

The plugin is a set of skills and small helper scripts. It runs inside an LLM
agent host that reads your files in order to help you. Any taxpayer data you
place in the workspace, or paste into the conversation, is read by that host and
its model, and may be processed according to that host's own privacy terms.
Review your host provider's privacy policy for how prompts, files, and tool
output are handled. This plugin does not, by itself, send your data to the
Belastingdienst, to the plugin authors, or to any third party.

## What the plugin does and does not do

- It **does** guide intake, evidence indexing, source checks, field maps, and
  manual-submission checklists, writing working files into the local workspace.
- It **does not** perform Mijn Belastingdienst portal access, signing,
  submission, filing, or portal automation. It never uses Chrome, browser
  control, computer use, screen interaction, or a connector to operate an
  authenticated portal. You or an authorized human types and verifies the
  prepared figures and decides whether to submit.

## Portal Access

Portal credentials are not part of this plugin's data model. The plugin must
not request, collect, store, or process DigiD details, passwords, verification
codes, app approvals, cookies, or authenticated sessions. User permission does
not change this boundary. Public read-only research on official tax sources is
separate and remains allowed.

## Evidence Content

Uploaded documents are used as evidence for workpack preparation. The host model
reads them; prompt-injection resistance and sensitive-data handling are the
host's responsibility, not the plugin's.

## Where data lives

Real taxpayer data — BSNs, IBANs, jaaropgaven, beschikkingen, screenshots, and
any prepared workpacks — belongs only in the gitignored local directories:

```text
workspace/
uploads/
evidence/
```

These paths, plus common document types (`*.pdf`, `*.xlsx`, `*.csv`, `*.zip`,
and similar), are excluded from version control by `.gitignore`. The single
allow-listed binary exception is the plugin icon/logo under
`plugins/**/assets/*.png`. Do not place real evidence under any other path.

Files the plugin writes are **plaintext on your local filesystem** (Markdown and
YAML). They are not encrypted at rest by the plugin. Anyone with access to your
machine, backups, or sync folders can read them.

## Retention and cleanup

The plugin does not auto-delete anything. You are responsible for retention.

- When you finish a tax task, remove generated working files you no longer need,
  for example `workspace/`, `uploads/`, and `evidence/`.
- Be mindful of cloud-sync folders, machine backups, and shared drives that may
  copy these plaintext files elsewhere.
- Keep only what you need for your own records, and store it securely.

A simple cleanup, run from the repository root, removes the local working
directories:

```bash
rm -rf workspace/ uploads/ evidence/
```

Verify the contents before deleting; this is irreversible.
