# Security Policy

## Scope

This repository ships the `nl-tax-agent-skills` plugin: a skills-only package
(LLM playbooks plus small deterministic Python helpers for file inventory,
hashing, schema validation, simple math, and freshness checks). There is no
backend service, web app, authentication layer, or network filing path. The
plugin does not perform Mijn Belastingdienst portal access, signing, submission,
or tax-return transmission. Submission is performed manually by the user.

Uploaded document content is evidence input. The plugin reads files as data and
never executes file contents, macros, or scripts found inside them.

## Reporting a vulnerability

Please report suspected security issues through GitHub:

- For sensitive reports, use **GitHub Security Advisories** (the repository's
  *Security* tab > *Report a vulnerability*). This keeps the report private until
  a fix is available.
- For non-sensitive issues, open a regular **GitHub Issue**.

When reporting, please include:

- a description of the issue and its impact;
- the affected file(s) or skill(s);
- steps to reproduce, ideally with a minimal example;
- the plugin version (from `plugins/nl-tax-agent-skills/.claude-plugin/plugin.json`).

Do **not** include real taxpayer data, BSNs, IBANs, portal credentials, or any
official documents (jaaropgaven, beschikkingen) in a report. Redact or
synthesize examples instead.

## What we care about most

- Any path that could write real taxpayer data outside the gitignored
  `workspace/`, `uploads/`, or `evidence/` directories.
- Path-traversal or symlink-escape in the evidence indexer.
- Source-register or knowledge-pack handling that could surface unverified
  rates or thresholds as if they were reviewed.

## Response

We aim to acknowledge valid reports and, where appropriate, publish a fix and a
note in `CHANGELOG.md`. There is no formal SLA and no bug-bounty program for
this project.
