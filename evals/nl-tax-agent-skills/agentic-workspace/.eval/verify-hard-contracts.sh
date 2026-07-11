#!/usr/bin/env bash
set -euo pipefail

if [[ -e workspace/eval/current-case.txt ]]; then
  echo "Agentic benchmark must not use an exact case marker." >&2
  exit 1
fi

if [[ -d workspace/annual && -d workspace/provisional ]]; then
  echo "Annual and provisional output trees must not be mixed in one scenario." >&2
  exit 1
fi

if [[ -d workspace ]]; then
  unexpected_maps="$(find workspace -type f -name field-map.yaml \
    ! -path 'workspace/annual/2025/field-map.yaml' \
    ! -path 'workspace/provisional/2026/field-map.yaml' -print)"
  if [[ -n "$unexpected_maps" ]]; then
    echo "Field maps must use canonical workflow paths:" >&2
    echo "$unexpected_maps" >&2
    exit 1
  fi

  if find workspace/shared -maxdepth 1 -type f \
      \( -name 'box*-notes.md' -o -name 'allocation-options.md' \) \
      -print -quit 2>/dev/null | grep -q .; then
    echo "Background helpers must not persist legacy shared-note artifacts." >&2
    exit 1
  fi
fi

echo "AGENTIC HARD-CONTRACT CHECK PASSED"
