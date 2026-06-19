#!/usr/bin/env python3
"""Validate cross-host invocation policy for the bundled skills.

Usage:
    python3 validate_invocation_policy.py <path-to-skills-dir>

On Codex, the Claude frontmatter keys `disable-model-invocation: true` and
`user-invocable: false` are ignored, as is `allowed-tools`. The ONLY thing that
keeps a background helper or manual-only skill from being implicitly invoked on
Codex is its `agents/openai.yaml` with `policy.allow_implicit_invocation: false`.

This validator fails closed: for every skill whose SKILL.md frontmatter marks it
non-implicitly-invocable (`disable-model-invocation: true` or
`user-invocable: false`), it asserts that `agents/openai.yaml` exists and sets
`policy.allow_implicit_invocation: false`. Without this check, a developer can add
a new helper, forget the openai.yaml, pass every other validator and the test
suite, and silently make the helper implicitly invocable on Codex.
"""

import os
import sys


def _require_yaml():
    try:
        import yaml
    except ImportError:
        raise SystemExit(
            "PyYAML is required to validate invocation policy "
            "(python3 -m pip install pyyaml)."
        )
    return yaml


def parse_frontmatter(skill_md_path):
    """Return the parsed YAML frontmatter block of a SKILL.md (or {})."""
    yaml = _require_yaml()
    with open(skill_md_path, "r", encoding="utf-8") as f:
        text = f.read()
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    data = yaml.safe_load(parts[1])
    return data if isinstance(data, dict) else {}


def _as_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "1"}
    return None


def is_non_user_invocable(frontmatter):
    """True if the skill must NOT be implicitly invocable."""
    if _as_bool(frontmatter.get("disable-model-invocation")) is True:
        return True
    user_invocable = _as_bool(frontmatter.get("user-invocable"))
    if user_invocable is False:
        return True
    return False


def openai_policy_ok(openai_yaml_path):
    """True if agents/openai.yaml sets policy.allow_implicit_invocation: false."""
    if not os.path.isfile(openai_yaml_path):
        return False, "missing agents/openai.yaml"
    yaml = _require_yaml()
    with open(openai_yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        return False, "agents/openai.yaml is not a mapping"
    policy = data.get("policy")
    if not isinstance(policy, dict):
        return False, "agents/openai.yaml has no policy block"
    if _as_bool(policy.get("allow_implicit_invocation")) is not False:
        return False, "policy.allow_implicit_invocation must be false"
    return True, ""


def collect_errors(skills_dir):
    errors = []
    checked = []
    for name in sorted(os.listdir(skills_dir)):
        skill_dir = os.path.join(skills_dir, name)
        skill_md = os.path.join(skill_dir, "SKILL.md")
        if not os.path.isfile(skill_md):
            continue
        frontmatter = parse_frontmatter(skill_md)
        if not is_non_user_invocable(frontmatter):
            continue
        checked.append(name)
        ok, reason = openai_policy_ok(os.path.join(skill_dir, "agents", "openai.yaml"))
        if not ok:
            errors.append((name, reason))
    return errors, checked


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: python3 validate_invocation_policy.py <path-to-skills-dir>",
            file=sys.stderr,
        )
        sys.exit(1)

    skills_dir = sys.argv[1]
    if not os.path.isdir(skills_dir):
        print(f"Error: skills dir not found: {skills_dir}", file=sys.stderr)
        sys.exit(1)

    errors, checked = collect_errors(skills_dir)

    if errors:
        print("VALIDATION FAILED")
        print()
        print("Invocation-policy errors:")
        for name, reason in errors:
            print(f"  - {name}: {reason}")
    else:
        print("VALIDATION PASSED")

    print()
    print(
        f"Checked {len(checked)} non-user-invocable skill(s): "
        f"{', '.join(checked) if checked else '(none)'}"
    )

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
