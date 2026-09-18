"""EXP-007: check an existing (formula, DRAT proof) pair with drat-trim and write the result file.

Used when the runner's wall-clock limit expired after the external solver had already started
writing the proof of the final formula: the solver process finishes on its own, and the proof it
leaves on disk is checked here. The formula is the one the runner wrote (base plus attach clauses
plus every learned cut, none in all cases so far); nothing is re-derived.

    .venv/Scripts/python.exe .../certify_existing.py --graph G52b --k 42 [--timeout 80000]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path

import sys

HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parents[1]
sys.path.insert(0, str(PROBLEM / "code"))

from pcclib import solver  # noqa: E402

HEAVY = Path("E:/_Datos/caos-research/petersen-coloring/EXP-007")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", required=True)
    ap.add_argument("--k", type=int, required=True)
    ap.add_argument("--timeout", type=int, default=80000)
    args = ap.parse_args()
    tag = f"{args.graph}_k{args.k}"
    cnf, proof = HEAVY / f"{tag}.cnf", HEAVY / f"{tag}.drat"
    header = cnf.open("r", encoding="utf-8", errors="replace")
    nvars = nclauses = None
    comment = ""
    for line in header:
        if line.startswith("c ") and not comment:
            comment = line.strip()
        if line.startswith("p cnf"):
            _, _, nvars, nclauses = line.split()
            break
    header.close()
    t0 = time.time()
    chk = subprocess.run(["wsl.exe", "-e", solver.DRAT_TRIM, solver.wsl_path(cnf), solver.wsl_path(proof), "-t", str(args.timeout)],
                         capture_output=True, text=True, timeout=args.timeout + 600)
    verified = "s VERIFIED" in chk.stdout
    result = {"graph": args.graph, "k": args.k, "status": "UNSAT" if verified else "UNVERIFIED", "verified": verified,
              "proof_bytes": proof.stat().st_size, "proof_sha256": solver.sha256_file(proof), "cnf_sha256": solver.sha256_file(cnf),
              "reduced": True, "post_hoc_check": True, "formula_comment": comment, "variables": int(nvars), "clauses": int(nclauses),
              "certify_solve_seconds": None, "check_seconds": round(time.time() - t0, 1), "rounds": 1, "learned_cuts": 0,
              "drat_trim_tail": chk.stdout[-300:]}
    out = HERE / "artifacts" / f"result-{args.graph}-k{args.k}.json"
    if verified:
        out.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    print(time.strftime("%H:%M:%S"), json.dumps({k: v for k, v in result.items() if k != "drat_trim_tail"}), flush=True)


if __name__ == "__main__":
    main()
