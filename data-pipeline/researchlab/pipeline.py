"""researchlab pipeline: the offline lane that bakes the web artifacts (CONTRACT 2).

The heavy engine of this repository is the experiment layer under problems/ (exact sympy runs
with persisted artifacts); this pipeline is the export stage that turns the program registry and
the per-problem payloads into the compact JSON the static web app replays.

Run: python -m researchlab.pipeline all
"""
from __future__ import annotations

import sys

from .stages import export_registry

STAGES = [("export_registry", export_registry.run)]


def main(argv: list[str]) -> int:
    target = argv[0] if argv else "all"
    if target not in ("all", "export_registry"):
        print(f"unknown target {target!r}; use: all | export_registry")
        return 2
    for name, fn in STAGES:
        written = fn()
        print(f"[{name}] wrote {len(written)} files")
        for p in written:
            print(f"  {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
