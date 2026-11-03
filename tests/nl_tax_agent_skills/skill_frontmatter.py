"""Shared SKILL.md frontmatter helpers for the test suite."""


def split_allowed_tools(metadata):
    """Split the spec's space-separated `allowed-tools` string into a list.

    Tests then check real tool names; iterating the raw string would walk its
    characters and let every per-tool assertion pass vacuously.
    """
    tools = metadata.get("allowed-tools")
    if isinstance(tools, str):
        metadata["allowed-tools"] = tools.split()
    return metadata
