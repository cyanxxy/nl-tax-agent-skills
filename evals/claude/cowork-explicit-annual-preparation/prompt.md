---
schema_version: "1.1"
name: cowork-explicit-annual-preparation
description: An explicit annual-return preparation request must enter the intake workflow.
tags:
  - cowork
  - routing
runs: 1
max_turns: 5
timeout_seconds: 300
expected_outcome: Start the annual preparation workflow and request only the remaining screening facts or relevant documents.
---
Help me prepare my Dutch 2025 income-tax return. I was resident in the
Netherlands for all of 2025, I am filing as an individual, and this is for me
while I am alive. I have my jaaropgave and bank statements ready.
