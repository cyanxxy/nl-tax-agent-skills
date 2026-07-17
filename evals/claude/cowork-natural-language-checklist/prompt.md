---
schema_version: "1.1"
name: cowork-natural-language-checklist
description: A direct natural-language checklist request activates the manual-entry companion without a magic phrase.
tags:
  - cowork
  - routing
  - checklist
runs: 1
max_turns: 5
timeout_seconds: 300
expected_outcome: Recognize explicit checklist intent and create or continue the human-only manual-entry checklist from the reviewed artifacts.
---
We have finished reviewing my Dutch tax workpack and its field map. Please make
the human-only manual-entry checklist for me now, with unresolved items first.
I do not want to use a slash command.
