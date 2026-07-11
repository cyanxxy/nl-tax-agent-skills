<div align="center">

<img src="plugins/nl-tax-agent-skills/assets/icon.png" alt="NL Tax Agent Skills" width="170" />

<h1>NL Tax Agent Skills</h1>

<p>
  <strong>Turn scattered Dutch tax paperwork into a reviewable, source-cited workpack for manual Mijn Belastingdienst entry.</strong>
  <br />
  <sub>An Agent Skills plugin for Claude Code, Cowork, and Codex — annual 2025 &amp; voorlopige aanslag 2026.</sub>
</p>

<br />
<br />

<a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/License-Apache--2.0-blue.svg" /></a>
<a href="https://claude.com/claude-code"><img alt="Claude Code" src="https://img.shields.io/badge/Claude%20Code-supported-D97757" /></a>
<a href="https://claude.ai"><img alt="Cowork" src="https://img.shields.io/badge/Cowork-supported-6E56CF" /></a>
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
<a href="#-architecture--data-flow">Architecture</a>
&nbsp;&nbsp;·&nbsp;&nbsp;
<a href="#-skill-inventory">Skills</a>
&nbsp;&nbsp;·&nbsp;&nbsp;
<a href="#-privacy">Privacy</a>
&nbsp;&nbsp;·&nbsp;&nbsp;
<a href="#-evals--tests">Evals</a>

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
      It determines what each document is and where it belongs in your tax return, using the official 2025 / 2026 Dutch tax rules. Every rule note cites a registered source.
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
output it creates under `workspace/`.

<details>
<summary><strong>Advanced: invoke a skill directly</strong></summary>

```text
/nl-tax-agent-skills:nl-tax-intake annual
/nl-tax-agent-skills:nl-tax-evidence-indexer uploads/
/nl-tax-agent-skills:nl-tax-annual-return 2025
/nl-tax-agent-skills:nl-tax-field-mapper annual 2025
/nl-tax-agent-skills:nl-tax-submit-companion annual 2025
```

For a provisional workflow, invoke the actual provisional skill:

```text
/nl-tax-agent-skills:nl-tax-provisional-assessment 2026 request
```

Replace `request` with `change`, `review`, or `stopzetten`. Direct invocation is
an advanced Claude interface; ordinary Cowork use should start with the natural-
language request above. Codex users can name a discovered skill explicitly.

</details>

---

## 📦 Install

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

### Claude Cowork — personal

<sup><em>Public repository supported</em></sup>

1. Open Claude Desktop → **Cowork** → **Customize** → **Browse plugins** → **Personal**.
2. Select **+** → **Add marketplace from GitHub**, then enter `https://github.com/cyanxxy/nl-tax-agent-skills`.
3. Select **Install** on the `nl-tax-agent-skills` entry.

Public GitHub repositories are accepted for personal marketplaces — no fork or ZIP upload is required.

### Host compatibility

| Host | Discovery path | Implicit-invocation control | Status |
|---|---|---|---|
| Claude Code | `.claude-plugin/marketplace.json` → nested plugin | Claude skill frontmatter | ✅ First-party manifest and skill validation |
| Cowork | Same `.claude-plugin/marketplace.json` — personal or organization marketplace | Claude skill frontmatter | ⚠️ Package validated; release UI smoke still required |
| Codex | `.agents/plugins/marketplace.json` → nested plugin | `agents/openai.yaml` with `policy.allow_implicit_invocation: false` | ⚠️ Compatible — see note |

Cowork tasks may use local or remote execution environments. Available files,
tools, and shell visibility depend on the session, so select or attach the
documents for that task. The skills resolve bundled resources with host file
tools; they do not assume Bash can discover the plugin cache. If an optional
helper is unavailable, the LLM agent performs the documented check from the
same references.

Python is optional at runtime; do not ask a taxpayer to install it. For hosts
and maintainers that already provide Python 3.10+, the 14 mechanical helpers
belong to four conceptual components: evidence inventory/hash, field-map
checks, source-pinned arithmetic checks, and developer consistency/source
maintenance. The LLM agent still owns interpretation, evidence sufficiency,
workflow decisions, and the workpack.

The release gate validates Claude manifests and skill discovery with first-party
Claude tooling when available. That does not prove the Cowork desktop flow: a
human must still install/update the plugin in Cowork, open a fresh task, run the
annual and provisional smoke prompts, and record the result. Codex invocation
metadata is validated statically but should likewise be checked in the target
host build.

<details>
<summary><strong>Other installation paths</strong> — Cowork team/organization, community directory, Codex, and ZIP fallback</summary>

<br />

#### Cowork — team / enterprise

<sup><em>Private fork required</em></sup>

Cowork's organization marketplace accepts only **private or internal** GitHub repositories. Fork or mirror this repository privately under your organization, then open **Organization settings → Plugins → Add plugin → GitHub**, enter `your-org/your-fork`, and set availability to *Available*, *Installed by default*, *Not available*, or *Required*.

#### Community directory

Open-source plugins can be submitted to the Anthropic community directory at [clau.de/plugin-directory-submission](https://clau.de/plugin-directory-submission). Accepted plugins install from the in-product catalog without marketplace setup or forking.

#### Codex

Discovery uses two files. `.agents/plugins/marketplace.json`, the repository-scoped marketplace, points Codex to `plugins/nl-tax-agent-skills/`, which contains the required `.codex-plugin/plugin.json`.

Codex indexes each skill's `name`, `description`, and path, then loads the full `SKILL.md` when the skill is selected. It does not honor the Claude `disable-model-invocation`, `user-invocable`, or `allowed-tools` keys, so manual-only and background skills include `agents/openai.yaml` with `policy.allow_implicit_invocation: false`.

See [CONTRIBUTING.md](CONTRIBUTING.md#cross-host-invocation-policy).

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

| Workflow | Year | Output |
|---|:---:|---|
| ✅ Annual income-tax return | **2025** | `workspace/annual/2025/return-pack.md` |
| ✅ Winst uit onderneming (eenmanszaak / ZZP), within the annual return | **2025** | winst uit onderneming section of `workspace/annual/2025/return-pack.md` |
| ✅ Voorlopige aanslag — request | **2026** | `workspace/provisional/2026/provisional-pack.md` + field map |
| ✅ Voorlopige aanslag — change | **2026** | provisional pack, field map, delta summary |
| ✅ Voorlopige aanslag — review | **2026** | provisional pack, review questions |
| ✅ Voorlopige aanslag — stopzetten | **2026** | guided support checklist |
| 🚫 Complex business forms (VOF / maatschap / CV, DGA / BV winst, agrarisch, zeevarenden, staking) | 2025 | *blocked — routed to manual review; only a straightforward eenmanszaak / ZZP is supported* |
| 🚫 Annual income-tax return | 2026 | *blocked — filed in 2027; only the provisional 2026 flows are active for tax year 2026* |
| 🚫 Annual return / Voorlopige aanslag | 2027 | *blocked until 2027 sources are registered and validated* |

> [!WARNING]
> **Box 3 rule split.** Annual 2025 collects both methods — **fictitious (forfaitair)** and **werkelijk rendement** — and presents a comparison for the user to choose from. Provisional 2026 uses **fictitious only**; werkelijk rendement is never requested in any provisional flow.

Active declarations live in [`supported-workflows.yaml`](plugins/nl-tax-agent-skills/skills/_shared/supported-workflows.yaml). A workflow is supported only when its workflow/year pair has reviewed source-register entries, local knowledge snapshots, and passing validators.

The plugin must not reuse rates, thresholds, field maps, or box 3 logic across tax years — not 2025 annual values for the 2026 annual return, and not 2025/2026 values for 2027.

---

## 🧩 Architecture & data flow

```mermaid
flowchart TB
    chat(["💬 interactive chat"]) --> intake["nl-tax-intake"]
    docs[("📂 uploads/ · evidence/")] --> indexer["nl-tax-evidence-indexer"]
    intake --> profile[/"taxpayer/profile.yaml"/]
    indexer --> evidx[/"taxpayer/evidence-index.yaml"/]

    profile --> annual["nl-tax-annual-return · 2025"]
    profile --> prov["nl-tax-provisional-assessment · 2026"]
    evidx --> annual
    evidx --> prov

    subgraph helpers ["background helpers → facts and questions returned to caller"]
        direction LR
        b1["box1-home"] ~~~ b2["box2"] ~~~ b3["box3"] ~~~ wn["winst"] ~~~ pd["partner-deductions"]
    end
    annual <-.-> helpers
    prov <-.-> helpers

    annual --> apack[/"annual/2025/<br/>return-pack.md"/]
    prov --> ppack[/"provisional/2026/<br/>provisional-pack.md<br/>delta-summary.md (change) · review-questions.md (review)"/]

    apack --> mapper["nl-tax-field-mapper"]
    ppack --> mapper
    mapper --> maps[/"canonical annual/provisional<br/>field-map.yaml"/]
    maps --> submit["nl-tax-submit-companion"]
    submit --> portal(["✅ you type into Mijn Belastingdienst"])

    classDef skill fill:#D97757,stroke:#B85C3E,color:#fff
    classDef file fill:#F6F1EB,stroke:#C9BBA8,color:#3B3B3B
    classDef endpoint fill:#2EA44F,stroke:#22863A,color:#fff
    classDef input fill:#6E56CF,stroke:#5A45B0,color:#fff
    class intake,indexer,annual,prov,mapper,submit,b1,b2,b3,wn,pd skill
    class profile,evidx,apack,ppack,maps file
    class portal endpoint
    class chat,docs input
```

Skills compose without hidden state. Owning workflow skills persist taxpayer,
session, annual, and provisional artifacts. Background helpers — `box1-home`,
`box2`, `box3`, `winst`, and `partner-deductions` — return structured facts,
questions, and review notes to the caller and write no artifacts. The field
mapper alone writes the canonical annual/provisional field map.

The skills are instructed to trace every value in a workpack to evidence, profile data, a calculation that cites a `source_id`, or a logged assumption. Review the workpack to confirm this before entry.

The full annotated `workspace/` tree and skill-authoring internals are documented in [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 🧰 Skill inventory

| Skill | Type | Responsibility |
|---|:---:|---|
| `nl-tax-intake` | 🙋 user entry | Screen scope, route to a supported workflow, write `workspace/taxpayer/profile.yaml` |
| `nl-tax-evidence-indexer` | 🙋 user entry | Hash and index local evidence files, classify without deciding tax treatment |
| `nl-tax-annual-return` | 🙋 user entry | Prepare `workspace/annual/2025/return-pack.md`; invoke the mapper for its field map (incl. preparation-only winst for an eenmanszaak / ZZP) |
| `nl-tax-provisional-assessment` | 🙋 user entry | Prepare 2026 request, change, review, and stopzetten packages |
| `nl-tax-field-mapper` | 🙋 user entry | Convert workpack findings into manual-entry field maps and review tables |
| `nl-tax-submit-companion` | 🔒 manual-only | Produce a human checklist for official Belastingdienst submission |
| `nl-tax-box1-home` | ⚙️ background | Return sourced Box 1/eigen-woning facts and questions to the owning workflow |
| `nl-tax-box2` | ⚙️ background | Return standard Box 2 facts and questions to the owning workflow |
| `nl-tax-box3` | ⚙️ background | Return classified-row review and method-specific Box 3 facts without mixing methods |
| `nl-tax-winst` | ⚙️ background | Return annual-2025 preparation facts or one sourced provisional-2026 expected-profit forecast |
| `nl-tax-partner-deductions` | ⚙️ background | Return fiscal-partner, allocation, and deduction facts and questions |
| `nl-tax-source-refresh` | 🛠️ developer | Validate and refresh local source snapshots and workflow declarations |

Top-level workflow skills own `workspace/annual/**` and
`workspace/provisional/**`. Intake owns taxpayer/session creation, the field
mapper owns canonical field maps, and background helpers persist nothing.

---

## 🔒 Privacy

Taxpayer files live only in git-ignored paths — `workspace/`, `uploads/`, `evidence/` — so they never enter the repository, forks, or marketplaces. The skills run inside an agent host (Claude Code, Cowork, or Codex) that reads those files to do its work under that host's data-handling terms; the git-ignore boundary is not an offline guarantee. For hard limits on network or file access, use your host's deny-rules and sandboxing. See [PRIVACY.md](PRIVACY.md) for retention and cleanup, and [SECURITY.md](SECURITY.md) to report a sensitive issue.

---

## 📚 Source register & knowledge pack

Taxpayer-facing skills read a bundled knowledge pack — not live websites — under `plugins/nl-tax-agent-skills/skills/_shared/`:

```text
knowledge/            # source-cited rule notes (laws, own-home, partners, box2/box3, years/…)
source-register.yaml  # every cited source_id with metadata (url, snapshot, freshness, owner)
supported-workflows.yaml
```

Every rule note must cite a `source_id` registered in [`source-register.yaml`](plugins/nl-tax-agent-skills/skills/_shared/source-register.yaml). Only `nl-tax-source-refresh` maintains snapshots.

At runtime the workflow skills check the register's `last_checked` dates against each source's re-check cadence. A stale source pack produces a one-line warning to the user (naming the stale `source_id`s) and a note in the workpack's review checklist — it never blocks workpack generation.

The active supported pairs are **annual return 2025** and **provisional assessment 2026**. **2027 is blocked** until official sources are registered and validated.

The register schema, freshness gate, and process for adding a source are documented in [CONTRIBUTING.md](CONTRIBUTING.md#source-register--knowledge-pack).

---

## 🧪 Evals & tests

Behavior is assessed at three deliberately separate layers; none logs in or files:

- **Agentic conversations** — [`evals/nl-tax-agent-skills/`](evals/nl-tax-agent-skills/) defines five natural Cowork-style prompts and a weighted rubric for reasoning, source use, question quality, uncertainty, usefulness, progressive loading, and agent ownership. The live benchmark uses a minimal workspace and only one hard-contract verifier.
- **Structural fixtures** — [`skills/_shared/eval-fixtures/`](plugins/nl-tax-agent-skills/skills/_shared/eval-fixtures/) and `offline-dataset.yaml` retain annual, provisional, and boundary invariants without acting as model prompts or exact answer templates:

  ```bash
  python3 evals/nl-tax-agent-skills/verify_offline_workspace.py --check-dataset
  ```

  See [`evals/nl-tax-agent-skills/README.md`](evals/nl-tax-agent-skills/README.md) for the five conversational profiles, shared rubric, structural-contract boundary, and benchmark command.
- **Unit tests** — `plugins/nl-tax-agent-skills/tests/` covers hard contracts, optional mechanical helpers, rate parity, fixture shape, and cross-host invocation policy:

  ```bash
  python3 -m unittest discover -s plugins/nl-tax-agent-skills/tests -p 'test_*.py'
  ```

  The suite also passes when run from the shipped plugin package alone; repo-only checks (marketplace manifests, changelog) skip themselves cleanly.

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
