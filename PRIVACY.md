# Privacy Policy

This policy covers the `nl-tax-agent-skills` plugin. The plugin is a set of
skills (Markdown and YAML instructions) that runs inside the AI host you choose:
Claude (Cowork, Claude Code, or the Claude apps), ChatGPT Work, or Codex. It has
no backend, no server, and no account. The plugin authors receive none of your
data.

## What the plugin reads

When you ask it to prepare a tax workpack, the plugin instructs the host's AI
model to read:

- the documents you attach or select, such as a jaaropgaaf, mortgage statement,
  or bank overview, which contain personal and financial data; and
- the facts you state in the conversation.

It reads only what you provide for your own tax preparation. It never asks for
DigiD details, passwords, verification codes, or portal sessions, and never
opens Mijn Belastingdienst.

## What the plugin stores

The plugin instructs the model to write working files only under `workspace/` in
your task's working folder: your taxpayer profile, an evidence index, workpacks,
and field maps. These are plaintext Markdown and YAML files. They stay wherever
your host keeps that folder: on your computer for a local task, or in the
task's environment for a cloud task. The plugin does not encrypt them.

## What the plugin sends, and to whom

The plugin sends your data to no one: not to the plugin authors, not to the
Belastingdienst, and not to any other third party. It has no connectors, MCP
servers, scripts, or network calls. An optional Claude reviewer agent may read
public official pages, such as belastingdienst.nl, to check that tax sources are
current; it sends no taxpayer data.

Your AI host does process everything you share with it, under its own terms.
This plugin is **not** a local-only or offline guarantee. See your host's
privacy policy for how it handles prompts and files.

## Retention and deletion

The plugin keeps no data of its own, so there is nothing for the authors to
retain or delete. The files under `workspace/` stay until you delete them; the
plugin never deletes them automatically. When you are done, delete the working
folders you no longer need, for example:

```bash
rm -rf workspace/ uploads/ evidence/
```

Check the contents before deleting, because this cannot be undone. Remember
that cloud-sync folders, backups, and shared drives may hold copies.

## Children

The plugin is intended for adults preparing their own Dutch income tax. It is
not intended for people under 18.

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
