# NL Tax Agent Skills Plugin

Plugin package for preparing Dutch individual income-tax workpacks through LLM-native Agent Skills.

This directory is the product package. The skills are bundled inside the plugin under `skills/`.

The repository root contains the Claude marketplace manifest:

```text
.claude-plugin/marketplace.json
```

That marketplace points at this plugin directory.

## Package Contents

```text
nl-tax-agent-skills/
  .claude-plugin/plugin.json    # Claude Code plugin manifest
  .codex-plugin/plugin.json     # Codex plugin manifest
  assets/
    icon.png
    logo.png
  skills/                       # Bundled Agent Skills
    _shared/                    # Source pack, templates, eval fixtures
    nl-tax-intake/
    nl-tax-evidence-indexer/
    nl-tax-annual-return/
    nl-tax-provisional-assessment/
    nl-tax-box1-home/
    nl-tax-box3/
    nl-tax-partner-deductions/
    nl-tax-field-mapper/
    nl-tax-submit-companion/
    nl-tax-source-refresh/
```

The bundled skills cover:

- annual income-tax return workpack for tax year 2025;
- voorlopige aanslag 2026 request, change, review, and stopzetten guidance;
- evidence indexing with untrusted-content handling;
- box 1, box 3, partner/deduction, field-map, source-refresh, and manual submission companion workflows.

The plugin intentionally does not include a backend service, web app, browser automation, DigiD collection, signing, filing, Digipoort transport, or autonomous submission.

## Claude Code

Install through the repository marketplace at `https://github.com/cyanxxy/nl-tax-agent-skills`:

```bash
claude plugin marketplace add cyanxxy/nl-tax-agent-skills
claude plugin install nl-tax-agent-skills@nl-tax-agent-skills-marketplace
```

Load the plugin directly during local development:

```bash
claude --plugin-dir ./plugins/nl-tax-agent-skills
```

Plugin skills are namespaced. Examples:

```text
/nl-tax-agent-skills:nl-tax-intake annual
/nl-tax-agent-skills:nl-tax-provisional-assessment 2026 change
/nl-tax-agent-skills:nl-tax-field-mapper annual 2025
```

## Claude Cowork

Personal marketplace install:

1. Open Claude Desktop and switch to **Cowork**.
2. Open **Customize**.
3. Click **Browse plugins**.
4. Select **Personal**.
5. Click **+** and choose **Add marketplace from GitHub**.
6. Enter `https://github.com/cyanxxy/nl-tax-agent-skills`.
7. Install **NL Tax Agent Skills** from the marketplace.

Organization marketplace install:

1. An owner on a Team or Enterprise plan opens **Organization settings > Plugins**.
2. Choose GitHub as the source and enter `cyanxxy/nl-tax-agent-skills`.
3. Set **NL Tax Agent Skills** to **Available for install**, **Installed by default**, or **Required**.

For one-off local testing in Cowork, ZIP this plugin directory and upload the custom plugin file:

```bash
cd plugins/nl-tax-agent-skills
zip -r ../../nl-tax-agent-skills.plugin.zip . -x "*.DS_Store" "workspace/*" "uploads/*" "evidence/*"
```

## Codex

For local Codex discovery, use a machine-local marketplace entry at:

```text
.agents/plugins/marketplace.json
```

That path is ignored by Git and should stay outside the plugin package.

The plugin manifest for Codex is:

```text
plugins/nl-tax-agent-skills/.codex-plugin/plugin.json
```

## Privacy Boundary

Real taxpayer data belongs only in ignored local workspace paths such as `workspace/`, `uploads/`, and `evidence/`. Do not add real taxpayer files, DigiD credentials, BSNs, IBANs, screenshots, PDFs, or spreadsheets to this plugin package.

## Source Model

Taxpayer-facing skills must use the bundled local source pack under:

```text
plugins/nl-tax-agent-skills/skills/_shared/knowledge/
```

Only the developer-only `nl-tax-source-refresh` skill may refresh official source snapshots.
