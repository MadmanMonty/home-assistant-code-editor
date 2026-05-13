#!/usr/bin/env python3
"""Strip legacy-syntax property markers from vscode-home-assistant schemas.

The upstream extension marks deprecated keys (e.g. ``platform:`` on triggers,
``service:`` on ``ServiceAction``) with ``pattern: "LEGACY_SYNTAX^"`` — an
impossible regex. Validation already rejects those values, but the YAML LSP
still surfaces the property names in autocomplete, leading users to insert
the legacy form. Deleting the marker properties removes them from the
completion dropdown, leaving only the modern keys (``trigger:``, ``action:``).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

LEGACY_MARKER = "LEGACY_SYNTAX^"
SCHEMA_SUBPATH = Path("extension/out/language-service/dist/schemas/json")


def strip_legacy(node) -> int:
    removed = 0
    if isinstance(node, dict):
        props = node.get("properties")
        if isinstance(props, dict):
            for key in list(props.keys()):
                value = props[key]
                if isinstance(value, dict) and value.get("pattern") == LEGACY_MARKER:
                    del props[key]
                    removed += 1
        for value in node.values():
            removed += strip_legacy(value)
    elif isinstance(node, list):
        for item in node:
            removed += strip_legacy(item)
    return removed


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: patch-ha-schemas.py <unpacked_extension_dir>", file=sys.stderr)
        return 2

    schema_dir = Path(argv[1]) / SCHEMA_SUBPATH
    if not schema_dir.is_dir():
        print(f"schema dir not found: {schema_dir}", file=sys.stderr)
        return 1

    total_removed = 0
    files_patched = 0
    for path in sorted(schema_dir.glob("*.json")):
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
        removed = strip_legacy(data)
        if removed:
            with path.open("w", encoding="utf-8") as f:
                json.dump(data, f, separators=(",", ":"))
            files_patched += 1
            total_removed += removed
            print(f"  {path.name}: removed {removed} legacy property markers")

    print(
        f"patched {files_patched} schema file(s), "
        f"removed {total_removed} legacy property markers"
    )

    if total_removed == 0:
        # Pinned upstream version means the markers should always be present;
        # a zero count means upstream layout changed and the patch is stale.
        print(
            "ERROR: no LEGACY_SYNTAX markers found — upstream schema layout "
            "may have changed; revisit patch-ha-schemas.py",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
