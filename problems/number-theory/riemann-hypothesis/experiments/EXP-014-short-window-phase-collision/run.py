"""CPU integer collision certificate; declared budget 30 seconds."""

import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
CODE = HERE.parents[1] / "code"
sys.path.insert(0, str(CODE))


def main():
    from short_window_phase import certificate

    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    print("EXP-014: exact collision identities and directed log bounds", flush=True)
    result = certificate()
    bindings = [HERE / "hypothesis.md", HERE / "proof.md", HERE / "run.py", CODE / "short_window_phase.py"]
    result["bindings"] = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in bindings}
    if time.monotonic() - started > 30:
        raise TimeoutError("declared budget exceeded; inconclusive")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode()
    (args.output_dir / "result.json").write_bytes(payload)
    print("EXP-014: all exact checks passed; " + hashlib.sha256(payload).hexdigest(), flush=True)


if __name__ == "__main__":
    main()
