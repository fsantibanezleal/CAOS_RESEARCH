"""Rerun every experiment runner at its RECORDED arguments and diff against the record.

Round 2 and round 3 refactored the library under these runners: `nslib` gained
`cmz_budget`, `steering` and `ab_schedule`, the co-rotating solver was split out of
`steering` into `corotating`, and `__init__` changed which modules are eager. None of that
should move a published number, and this script is how that claim is checked rather than
assumed. It reruns EXP-002, EXP-003 and EXP-004 with the arguments stored in their own
result files and compares the headline quantities.

Usage:
    python reproduce_all.py                 # all three, at recorded settings
    python reproduce_all.py --only exp003   # one of them
    python reproduce_all.py --tolerance 1e-6
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent / "experiments"

# Each entry: the runner, the recorded result to diff against, the CLI reproducing it, and
# the (dotted) paths of the numbers that carry the verdict.
CASES = {
    "exp002": {
        "runner": "run_exp002.py",
        "record": EXPERIMENTS / "EXP-002-reduction-control/result.json",
        "argv": ["--n", "768", "--A0", "4.0", "--lam0", "1", "--dt", "5e-4", "--mode", "all"],
        "keys": [
            "cases.P1_inviscid.p1_max_rel_err",
            "cases.P3_lambda_sweep.peak_spread_rel",
        ],
    },
    "exp003": {
        "runner": "run_exp003.py",
        "record": EXPERIMENTS / "EXP-003-threshold-sweep/result.json",
        "argv": ["--stages", "400", "--batch", "1000000", "--nu", "1e-10"],
        "keys": [
            "H1.max_rel_err_vs_corrected",
            "H2.n_c4_binds_while_c2_holds",
            "H3.abs_diff",
        ],
    },
    "exp004": {
        "runner": "run_exp004.py",
        "record": EXPERIMENTS / "EXP-004-multilayer-handoff/result-frozen.json",
        "argv": ["--n", "1024", "--mode", "frozen", "--lam1b", "16", "--lam2", "192",
                 "--dt", "4e-4"],
        "keys": [
            "H1_full_two_scale_gradient.corr",
            "H2_control_base_only.corr",
            "H1_full_two_scale_gradient.slope",
        ],
    },
}


def dig(d: dict, dotted: str):
    """Fetch a dotted path, returning None when any level is missing."""
    cur = d
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


# Wall-clock fields are measurements of this machine on this day, not results. Comparing
# them makes every rerun "fail" for the one reason that carries no information, which is
# what the first run of this script did.
TIMING_KEYS = ("seconds", "wall_seconds", "elapsed", "duration")


def is_timing(key: str) -> bool:
    return key.rsplit(".", 1)[-1] in TIMING_KEYS


def leaves(d, prefix=""):
    """Every numeric leaf of a result except timings, so a diff needs no key list."""
    out = {}
    if isinstance(d, dict):
        for k, v in d.items():
            if k == "args":
                continue
            out.update(leaves(v, f"{prefix}{k}."))
    elif isinstance(d, (int, float)) and not isinstance(d, bool):
        key = prefix.rstrip(".")
        if not is_timing(key):
            out[key] = float(d)
    return out


def compare(old: dict, new: dict, tolerance: float) -> tuple[list[str], list[str]]:
    """Return (mismatches, missing) over every shared numeric leaf."""
    a, b = leaves(old), leaves(new)
    mismatches, missing = [], []
    for key, va in sorted(a.items()):
        if key not in b:
            missing.append(key)
            continue
        vb = b[key]
        scale = max(abs(va), abs(vb), 1e-300)
        if abs(va - vb) / scale > tolerance:
            mismatches.append(f"{key}: recorded {va!r} -> rerun {vb!r}")
    return mismatches, missing


def run_case(name: str, case: dict, tolerance: float, python: str) -> dict:
    out_path = HERE / f"_reproduce_{name}.json"
    cmd = [python, "-u", str(HERE / case["runner"]), *case["argv"], "--out", str(out_path)]
    print(f"--- {name}: {' '.join(cmd[2:])}", flush=True)
    started = time.time()
    proc = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True)
    seconds = round(time.time() - started, 1)
    if not out_path.exists():
        return {"name": name, "ok": False, "seconds": seconds,
                "error": f"no output written; exit {proc.returncode}",
                "stderr_tail": proc.stderr.strip().splitlines()[-5:]}

    new = json.loads(out_path.read_text(encoding="utf-8"))
    old = json.loads(case["record"].read_text(encoding="utf-8"))
    mismatches, missing = compare(old, new, tolerance)
    headline = {k: (dig(old, k), dig(new, k)) for k in case["keys"]}
    out_path.unlink()
    return {
        "name": name,
        "exit_code": proc.returncode,       # a runner exits nonzero when a gate fails
        "seconds": seconds,
        "headline": headline,
        "n_leaves_compared": len(leaves(old)),
        "mismatches": mismatches,
        "missing_from_rerun": missing,
        "ok": not mismatches and not missing,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=sorted(CASES), default=None)
    ap.add_argument("--tolerance", type=float, default=1e-9,
                    help="relative tolerance; these runs are deterministic, so it is tight")
    ap.add_argument("--python", default=sys.executable)
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    names = [args.only] if args.only else list(CASES)
    results = [run_case(n, CASES[n], args.tolerance, args.python) for n in names]
    report = {"tolerance": args.tolerance, "results": results,
              "all_reproduce": all(r["ok"] for r in results)}
    print(json.dumps(report, indent=2, default=str))
    if args.out:
        Path(args.out).write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    return 0 if report["all_reproduce"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
