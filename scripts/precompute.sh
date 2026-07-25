#!/usr/bin/env bash
# Run the offline pipeline (pass-through args). E.g.:  ./scripts/precompute.sh EX02_epidemic --seed 7
set -euo pipefail
cd "$(dirname "$0")/.."
VP=".venv-pipeline/bin/python"; [ -x "$VP" ] || VP=".venv-pipeline/Scripts/python.exe"
if [ ! -x "$VP" ]; then VP=".venv/bin/python"; fi
if [ ! -x "$VP" ]; then VP=".venv/Scripts/python.exe"; fi
if [ ! -x "$VP" ]; then
  echo "No repository Python environment found. Run scripts/setup.sh first." >&2
  exit 1
fi
PYTHONPATH="$PWD/data-pipeline${PYTHONPATH:+:$PYTHONPATH}" "$VP" -m researchlab.pipeline "$@"
