#!/usr/bin/env python3
"""Build a clean OpenAI submission bundle from the cross-host source plugin."""

from __future__ import annotations

import argparse
import shutil
import zipfile
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
SOURCE_PLUGIN = REPO / "plugins" / "nl-tax-agent-skills"
DEFAULT_OUTPUT = REPO / "dist" / "openai" / "nl-tax-agent-skills"
PLUGIN_DIRS = (".codex-plugin", "assets", "skills")
PLUGIN_FILES = ("LICENSE", "README.md")
CLAUDE_ONLY_KEYS = {
    "allowed-tools",
    "argument-hint",
    "disable-model-invocation",
    "disable_model_invocation",
    "user-invocable",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the skills-only OpenAI Plugin Directory bundle."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output plugin directory (default: dist/openai/nl-tax-agent-skills).",
    )
    parser.add_argument(
        "--zip-path",
        type=Path,
        help="Output ZIP path (default: <output-dir>.zip).",
    )
    return parser.parse_args()


def _frontmatter_bounds(text: str, path: Path) -> tuple[int, int]:
    if not text.startswith("---\n"):
        raise ValueError(f"missing YAML frontmatter: {path}")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError(f"unterminated YAML frontmatter: {path}")
    return 4, end


def sanitize_skill(path: Path) -> int:
    """Remove Claude-only invocation keys from one copied SKILL.md."""
    text = path.read_text(encoding="utf-8")
    start, end = _frontmatter_bounds(text, path)
    lines = text[start:end].splitlines()
    kept: list[str] = []
    removed = 0
    skipping_value = False
    for line in lines:
        if skipping_value:
            if not line or line.startswith((" ", "\t")):
                continue
            skipping_value = False
        stripped = line.lstrip()
        key = stripped.split(":", 1)[0] if ":" in stripped else ""
        if not line.startswith((" ", "\t")) and key in CLAUDE_ONLY_KEYS:
            removed += 1
            skipping_value = True
            continue
        kept.append(line)
    sanitized = "---\n" + "\n".join(kept) + text[end:]
    path.write_text(sanitized, encoding="utf-8")
    return removed


def _assert_safe_output(output_dir: Path) -> None:
    output = output_dir.resolve()
    source = SOURCE_PLUGIN.resolve()
    if output == source or source in output.parents:
        raise ValueError("output directory must not be inside the source plugin")
    if output == REPO.resolve():
        raise ValueError("output directory must not replace the repository root")


def build_bundle(output_dir: Path, zip_path: Path | None = None) -> tuple[Path, Path, int]:
    output_dir = output_dir.resolve()
    _assert_safe_output(output_dir)
    zip_path = (zip_path or output_dir.with_suffix(".zip")).resolve()

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    for name in PLUGIN_DIRS:
        shutil.copytree(
            SOURCE_PLUGIN / name,
            output_dir / name,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
        )
    for name in PLUGIN_FILES:
        shutil.copy2(SOURCE_PLUGIN / name, output_dir / name)

    removed = sum(sanitize_skill(path) for path in output_dir.glob("skills/*/SKILL.md"))

    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(p for p in output_dir.rglob("*") if p.is_file()):
            relative = path.relative_to(output_dir.parent).as_posix()
            info = zipfile.ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())

    return output_dir, zip_path, removed


def main() -> None:
    args = parse_args()
    output, zip_path, removed = build_bundle(args.output_dir, args.zip_path)
    print(f"OpenAI bundle directory: {output}")
    print(f"OpenAI bundle ZIP: {zip_path}")
    print(f"Removed {removed} Claude-only frontmatter field(s)")


if __name__ == "__main__":
    main()
