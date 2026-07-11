<div align="center">

<img src="plugins/nl-tax-agent-skills/assets/icon.png" alt="NL Tax Agent Skills" width="170" />

<h1>NL Tax Agent Skills</h1>

<p>
  <strong>Turn scattered Dutch tax paperwork into a reviewable, source-cited workpack for manual Mijn Belastingdienst entry.</strong>
  <br />
  <sub>A Cowork-first Agent Skills plugin — annual 2025 &amp; voorlopige aanslag 2026.</sub>
</p>

<br />
<br />

<a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/License-Apache--2.0-blue.svg" /></a>
<a href="https://claude.ai"><img alt="Cowork" src="https://img.shields.io/badge/Cowork-supported-6E56CF" /></a>
<a href="https://claude.com/claude-code"><img alt="Claude Code" src="https://img.shields.io/badge/Claude%20Code-supported-D97757" /></a>
<a href="#-install"><img alt="Codex" src="https://img.shields.io/badge/Codex-compatible-111111" /></a>
<a href="#-supported-workflows"><img alt="Years" src="https://img.shields.io/badge/Years-2025%20annual%20%C2%B7%202026%20provisional-2EA44F" /></a>

<br />
<br />

<a href="#-what-it-does">What it does</a>
&nbsp;&nbsp;·&nbsp;&nbsp;
<a href="#-how-it-works">How it works</a>
&nbsp;&nbsp;·&nbsp;&nbsp;
<a href="#-quickstart">Quickstart</a>
&nbsp;&nbsp;·&nbsp;&nbsp;
<a href="#-install">Install</a>
&nbsp;&nbsp;·&nbsp;&nbsp;
<a href="#-supported-workflows">Workflows</a>
&nbsp;&nbsp;·&nbsp;&nbsp;
<a href="#-privacy">Privacy</a>

</div>

<br />

> [!NOTE]
> This plugin **prepares workpacks for review**. It is not tax advice. Submission to the Belastingdienst is manual.

---

## 🎯 What it does

Filing Dutch income tax means a yearly slog of chasing documents, decoding **Mijn Belastingdienst** fields, and keeping track of box 3 rules that change every year — only to repeat the process months later for the voorlopige aanslag.

Off-the-shelf tax software wraps the official forms in its own interface. This plugin keeps you in Mijn Belastingdienst while handling the gathering, classification, and field mapping up to the point of manual entry.

There is no autonomous filing. By design, the skills read a bundled, source-cited knowledge pack instead of fetching live web pages at runtime.

---

## 🪜 How it works

*No tax or technical background is needed — the entire workflow comes down to four steps.*

<table>
  <tr>
    <td align="center" width="64">📂</td>
    <td>
      <strong>1 &nbsp;Share your documents</strong><br />
      Attach your jaaropgaaf, mortgage statement, bank overview, and similar papers in the chat, or place them in an <code>uploads/</code> folder. You can also state amounts directly in the conversation.
    </td>
  </tr>
  <tr>
    <td align="center">🔎</td>
    <td>
      <strong>2 &nbsp;The assistant reads and sorts them</strong><br />
      It determines what each document is and where it belongs in your tax return, using reviewed, source-cited Dutch tax guidance for the supported year.
    </td>
  </tr>
  <tr>
    <td align="center">📋</td>
    <td>
      <strong>3 &nbsp;You receive a clear, reviewable summary</strong><br />
      A “workpack” lists every amount, its source, and any open questions, so you can verify the numbers before anything goes near the tax office.
    </td>
  </tr>
  <tr>
    <td align="center">✅</td>
    <td>
      <strong>4 &nbsp;You enter the numbers yourself</strong><br />
      A final field map connects each reviewed amount to its Mijn Belastingdienst field for you to enter and verify.
    </td>
  </tr>
</table>

<br />

## 🚀 Quickstart

Once the plugin is [installed](#-install), open Cowork, attach or select the
documents you want it to use, and describe the result you need. The agent drives
the workflow: it asks only the missing intake questions, chooses the relevant
skills, and prepares artifacts for your review.

### Annual return — 2025

```text
Help me prepare my 2025 Dutch income-tax workpack. I have my year statement and mortgage summary.
```

### Voorlopige aanslag — 2026

```text
Help me request a 2026 voorlopige aanslag. Ask me for the estimates you still need.
```

You can ask instead to change, review, or stopzetten an existing 2026 voorlopige
aanslag. Annual and provisional work stay separate, and the agent explains each
output it prepares.

<details>
<summary><strong>Advanced: invoke a skill directly</strong></summary>

```text
/nl-tax-agent-skills:nl-tax-intake annual
```

For a provisional workflow, you can invoke the workflow skill directly:

```text
/nl-tax-agent-skills:nl-tax-provisional-assessment 2026 request
```

Replace `request` with `change`, `review`, or `stopzetten`. Direct invocation is
an advanced Claude interface; ordinary Cowork use should start with the natural-
language request above. Codex users can name a discovered skill explicitly.

</details>

---

## 📦 Install

### Claude Cowork — personal

<sup><em>Public repository supported</em></sup>

1. Open Claude Desktop → **Cowork** → **Customize** → **Browse plugins** → **Personal**.
2. Select **+** → **Add marketplace from GitHub**, then enter `https://github.com/cyanxxy/nl-tax-agent-skills`.
3. Select **Install** on the `nl-tax-agent-skills` entry.

Public GitHub repositories are accepted for personal marketplaces — no fork or ZIP upload is required.

### Claude Code

Install from the marketplace:

```text
/plugin marketplace add cyanxxy/nl-tax-agent-skills
/plugin install nl-tax-agent-skills@nl-tax-agent-skills-marketplace
```

Or run the plugin locally without installing the marketplace:

```bash
claude --plugin-dir ./plugins/nl-tax-agent-skills
```

### Supported hosts

The plugin is designed primarily for **Claude Cowork** and also works with
**Claude Code**. Both use the same bundled Agent Skills and reviewed tax
knowledge. In Cowork, select or attach the documents you want the agent to use.

Python is optional. The agent can complete the documented workflow without
asking a taxpayer to install Python.

<details>
<summary><strong>Other installation paths</strong> — Cowork team/organization, community directory, Codex, and ZIP fallback</summary>

<br />

#### Cowork — team / enterprise

<sup><em>Private fork required</em></sup>

Cowork's organization marketplace accepts only **private or internal** GitHub repositories. Fork or mirror this repository privately under your organization, then open **Organization settings → Plugins → Add plugin → GitHub**, enter `your-org/your-fork`, and set availability to *Available*, *Installed by default*, *Not available*, or *Required*.

#### Community directory

Open-source plugins can be submitted to the Anthropic community directory at [clau.de/plugin-directory-submission](https://clau.de/plugin-directory-submission). Accepted plugins install from the in-product catalog without marketplace setup or forking.

#### Codex

A compatible Codex manifest is included for developers who use the repository
there. See [CONTRIBUTING.md](CONTRIBUTING.md#cross-host-invocation-policy) for
host-specific setup and invocation details.

#### ZIP fallback

Use this path if the GitHub marketplace is unavailable in your host build:

```bash
cd plugins/nl-tax-agent-skills
zip -r ../../nl-tax-agent-skills.plugin.zip . \
  -x "*.DS_Store" -x "__MACOSX/*" -x ".git/*" -x ".claude/*" \
  -x ".agents/*" -x ".codex/*" -x "workspace/*" -x "uploads/*" \
  -x "evidence/*" -x "__pycache__/*" -x "*.pyc"
```

Upload the ZIP through the same **Browse plugins** modal. Versioning and release mechanics are documented in [CONTRIBUTING.md](CONTRIBUTING.md#release-process).

</details>

---

## 🗓️ Supported workflows

| Workflow | Year | What you receive |
|---|:---:|---|
| ✅ Annual income-tax return | **2025** | Reviewable tax workpack and manual-entry field guide |
| ✅ Winst uit onderneming (eenmanszaak / ZZP), within the annual return | **2025** | Preparation notes integrated into the annual workpack |
| ✅ Voorlopige aanslag — request | **2026** | Estimate workpack and manual-entry field guide |
| ✅ Voorlopige aanslag — change | **2026** | Updated estimates and a clear change summary |
| ✅ Voorlopige aanslag — review | **2026** | Review summary and unresolved questions |
| ✅ Voorlopige aanslag — stopzetten | **2026** | Guided support checklist |
| 🚫 Complex business forms (VOF / maatschap / CV, DGA / BV winst, agrarisch, zeevarenden, staking) | 2025 | *blocked — routed to manual review; only a straightforward eenmanszaak / ZZP is supported* |
| 🚫 Annual income-tax return | 2026 | *blocked — filed in 2027; only the provisional 2026 flows are active for tax year 2026* |
| 🚫 Annual return / Voorlopige aanslag | 2027 | *blocked until 2027 sources are registered and validated* |

> [!WARNING]
> **Box 3 rule split.** Annual 2025 collects both methods — **fictitious (forfaitair)** and **werkelijk rendement** — and presents a comparison for the user to choose from. Provisional 2026 uses **fictitious only**; werkelijk rendement is never requested in any provisional flow.

Annual 2025 also includes reviewed deduction guidance for the income-dependent
specific-healthcare-cost threshold and increase, the EUR 925 limited-mobility
transport forfait, the narrow legacy DUO prestatiebeurs study-cost exception,
and jaarruimte/reserveringsruimte. For lijfrente limits, the agent gathers and
explains the inputs and preserves the result from the official Belastingdienst
Hulpmiddel Lijfrentepremie; the plugin does not substitute a universal local
calculator for that official tool. Missing eligibility facts or evidence remain
visible review items in the workpack.

Rules are kept separate by tax year. The plugin will not reuse 2025 annual
figures for a future annual return or present unsupported future-year guidance
as complete.

---

## 🔒 Privacy

Documents are processed inside the active Cowork or Claude Code task under that
host's data-handling terms. Repository work folders are git-ignored so taxpayer
files are not committed or packaged, but git-ignore is not an offline guarantee.
See [PRIVACY.md](PRIVACY.md) for retention and cleanup details and
[SECURITY.md](SECURITY.md) to report a sensitive issue.

---

## 🤝 Contributing

Skill-authoring internals, the full validation gate, package layout, and release process are documented in [**CONTRIBUTING.md**](CONTRIBUTING.md).

CI runs the full gate on every push and pull request.

Tax-content correctness — rates, thresholds, rules, and cited sources — is owned by the tax-content owner. Report suspected inaccuracies or stale sources through GitHub Issues.

---

<div align="center">

<sub>
  Licensed under <a href="LICENSE">Apache-2.0</a>
  &nbsp;&nbsp;·&nbsp;&nbsp;
  Built for Claude Code, Cowork, and Codex
  &nbsp;&nbsp;·&nbsp;&nbsp;
  Submission is always manual through Mijn Belastingdienst
</sub>

</div>
