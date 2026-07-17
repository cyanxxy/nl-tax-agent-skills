<div align="center">

<img src="plugins/nl-tax-agent-skills/assets/icon.png" alt="NL Tax Agent Skills" width="170" />

<h1>NL Tax Agent Skills</h1>

<p>
  <strong>Turn scattered Dutch tax paperwork into a reviewable, source-cited workpack for manual Mijn Belastingdienst entry.</strong>
  <br />
  <sub>A Cowork-first, cross-platform Agent Skills plugin for Claude, ChatGPT Work, and Codex — annual 2025 &amp; voorlopige aanslag 2026.</sub>
</p>

<br />
<br />

<a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/License-Apache--2.0-blue.svg" /></a>
<a href="#claude-cowork--personal"><img alt="Cowork" src="https://img.shields.io/badge/Cowork-primary-6E56CF" /></a>
<a href="#chatgpt-work"><img alt="ChatGPT Work" src="https://img.shields.io/badge/ChatGPT%20Work-ready-10A37F" /></a>
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
> This plugin **prepares workpacks for review**. It is not tax advice. You or an
> authorized human performs every authenticated Mijn Belastingdienst action;
> the assistant never opens or operates the portal, signs, sends, or submits.

---

## 🎯 What it does

Filing Dutch income tax means a yearly slog of chasing documents, decoding **Mijn Belastingdienst** fields, and keeping track of box 3 rules that change every year — only to repeat the process months later for the voorlopige aanslag.

Off-the-shelf tax software wraps the official forms in its own interface. This
plugin leaves you in control of Mijn Belastingdienst while handling gathering,
classification, and field mapping up to the point of human-only manual entry.

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
      A final field map connects each reviewed amount to its Mijn Belastingdienst field for you to enter and verify. Ask naturally for a manual-entry checklist, or accept the mapper's offer; no slash command or magic phrase is required.
    </td>
  </tr>
</table>

<br />

## 🚀 Quickstart

Once the plugin is [installed](#-install), open Claude Cowork, ChatGPT Work,
Codex, or another
supported Agent Skills host, provide the documents you want it to use, and
describe the result you need. The agent drives the workflow: it asks only the
missing questions that matter for the facts you supplied, chooses the relevant
guidance as the conversation develops, and prepares artifacts for your review.
The saved progress record supports resuming later; it is not a questionnaire or
rules engine that dictates the conversation.

Natural-language intent drives the workflow. At final review, a contextual
“yes,” “go ahead,” or equivalent answer to the agent's scoped generation or
checklist question is enough; exact confirmation wording is never required.

On hosts with subagents, the main assistant may ask specialist reviewers to
cross-check independent sections after the facts are collected. This remains
agentic rather than a scripted tax flow: the main assistant is the only writer,
question asker, workflow router, and readiness authority. Claude Cowork can use
the packaged reviewer; ChatGPT Work and Codex can use built-in subagents. The
workflow also works fully inline when subagents are unavailable.

For finite-choice intake questions, the plugin prefers a native in-chat control
or compact form when the active host can return selections to the conversation.
Where that capability is unavailable, it asks the same short questions in chat;
interactive UI is never required to complete a workflow.
In Claude Cowork this means native interactive inputs when offered, not a custom
HTML visual whose clicks cannot return answers to the conversation.

On Work web or mobile, upload documents to the conversation or project. On
desktop, select a local folder or attach files. The plugin never assumes that a
cloud task can see files that remain only on your computer.

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

You can also request both in one sentence, for example: “Help me prepare my
2025 return, then request a 2026 voorlopige aanslag.” The plugin finishes and
validates the annual workpack first, then continues naturally with the chosen
2026 subflow without asking you to activate it again. Each workpack still has
its own final-generation confirmation, facts, sources, and output folder.

<details>
<summary><strong>Advanced: invoke a skill directly</strong></summary>

```text
/nl-tax-agent-skills:nl-tax-intake annual
```

For a provisional workflow, you can invoke the workflow skill directly:

```text
/nl-tax-agent-skills:nl-tax-provisional-assessment 2026 request
```

Replace `request` with `change`, `review`, or `stopzetten`. Direct invocation
syntax varies by host; the portable path is the natural-language request above.
Codex users can name a discovered skill explicitly.

</details>

---

## 📦 Install

### Claude Cowork — personal

<sup><em>Public repository supported</em></sup>

1. Open Claude Desktop → **Cowork**, then open **Customize**.
2. Open **Plugins**. Under **Personal plugins**, select **+** → **Add marketplace**.
3. Choose **Add from a repository**, then enter `https://github.com/cyanxxy/nl-tax-agent-skills`.
4. Select **Install** on the `nl-tax-agent-skills` entry.

Public GitHub repositories are accepted for personal marketplaces — no fork or ZIP upload is required.

### ChatGPT Work

For a published release, open ChatGPT **Plugins**, find **NL Tax Agent Skills**
in the Plugin Directory, and select **Install**. Start a fresh task after an
install or update so Work loads the current skill metadata.

For an unpublished reviewer build, first run
`python3 submission/openai/build_bundle.py`, then use the resulting
`dist/openai/nl-tax-agent-skills.zip` in the workspace's Apps Management draft
and test flow. This route requires publisher verification and Apps Management
write permission; the repository cannot complete those account-level gates.

Work web and mobile use uploaded or project files. Work desktop can also use a
local folder selected for the task. No connected app or external account
authorization is required by this plugin.

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

### Codex CLI

Add the GitHub marketplace and install the plugin:

```bash
codex plugin marketplace add cyanxxy/nl-tax-agent-skills --ref main
codex plugin add nl-tax-agent-skills@nl-tax-agent-skills-local
```

Confirm that it is installed and enabled:

```bash
codex plugin list
```

Then open Codex and ask naturally, for example: “Help me prepare my 2025 Dutch
income-tax workpack.”

### Supported hosts

The plugin is Cowork-first and supports **Claude Cowork**, **ChatGPT Work**,
**Codex**, and **Claude Code**. Each host uses the same bundled Agent Skills and reviewed tax
knowledge. File access follows the active surface: upload or project files on
Work web/mobile, and user-selected local files or attachments on desktop.

Python is optional. The agent can complete the documented workflow without
asking a taxpayer to install Python.

<details>
<summary><strong>Other installation paths</strong> — Cowork team/organization, community directory, and ZIP fallback</summary>

<br />

#### Cowork — team / enterprise

<sup><em>Private fork required</em></sup>

Cowork's organization marketplace accepts only **private or internal** GitHub repositories. Fork or mirror this repository privately under your organization, then open **Organization settings → Plugins → Add plugin → GitHub**, enter `your-org/your-fork`, and set availability to *Available*, *Installed by default*, *Not available*, or *Required*.

#### Community directory

Open-source plugins can be submitted to the Anthropic community directory at [clau.de/plugin-directory-submission](https://clau.de/plugin-directory-submission). Accepted plugins install from the in-product catalog without marketplace setup or forking.

#### ZIP fallback

Use this path if the GitHub marketplace is unavailable in your host build:

```bash
cd plugins/nl-tax-agent-skills
zip -r ../../nl-tax-agent-skills.plugin.zip . \
  -x "*.DS_Store" -x "__MACOSX/*" -x ".git/*" -x ".claude/*" \
  -x ".plugin-eval/" -x ".plugin-eval/*" \
  -x ".agents/*" -x ".codex/*" -x "workspace/*" -x "uploads/*" \
  -x "evidence/*" -x "__pycache__/" -x "__pycache__/*" \
  -x "*/__pycache__/" -x "*/__pycache__/*" -x "*.pyc"
```

Download the Cowork ZIP from the matching GitHub release, or build it locally
with the command above. In Claude Desktop, open **Customize → Plugins**; under
**Personal plugins**, select **+** and upload the custom plugin file. Versioning
and release mechanics are documented in [CONTRIBUTING.md](CONTRIBUTING.md#release-process).

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

Documents are processed inside the active ChatGPT Work, Codex, Claude, or other
supported host task under that host's data-handling terms. Repository work
folders are git-ignored so taxpayer files are not committed or packaged, but
git-ignore is not an offline guarantee. See [PRIVACY.md](PRIVACY.md) for
retention and cleanup details and [SECURITY.md](SECURITY.md) to report a
sensitive issue.

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
  Built for ChatGPT Work, Codex, Claude Code, and Cowork
  &nbsp;&nbsp;·&nbsp;&nbsp;
  Submission is always manual through Mijn Belastingdienst
</sub>

</div>
