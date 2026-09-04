"""Run CaDiCaL inside WSL with DRAT output, check proofs with drat-trim, record hashes and times.

Every call returns a record dict that the experiment manifest persists. A status is one of
"SAT", "UNSAT", "TIMEOUT", "ERROR". UNSAT is only reported as certified when drat-trim printed
"s VERIFIED".
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

CADICAL = "/usr/bin/cadical"
DRAT_TRIM = "/mnt/e/_Datos/caos-research/huneke-wiegand/tools/drat-trim/drat-trim"


def wsl_path(path: Path) -> str:
    out = subprocess.run(
        ["wsl.exe", "-e", "wslpath", "-a", str(Path(path).resolve())],
        capture_output=True,
        text=True,
        check=True,
    )
    return out.stdout.strip()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tool_versions() -> dict:
    v = subprocess.run(["wsl.exe", "-e", CADICAL, "--version"], capture_output=True, text=True)
    d = subprocess.run(["wsl.exe", "-e", DRAT_TRIM], capture_output=True, text=True)
    return {"cadical": v.stdout.strip(), "drat_trim_banner": (d.stdout or d.stderr).splitlines()[0:2]}


def log(msg: str) -> None:
    print(msg, flush=True)


def solve(cnf_path: Path, proof_path: Path, timeout_s: int, want_proof: bool = True) -> dict:
    """Solve a DIMACS file. Returns status, model (set of true vars) when SAT, hashes, timing."""
    cnf_path = Path(cnf_path)
    proof_path = Path(proof_path)
    args = ["wsl.exe", "-e", CADICAL, "-q", wsl_path(cnf_path)]
    if want_proof:
        args.append(wsl_path(proof_path))
    t0 = time.time()
    try:
        run = subprocess.run(args, capture_output=True, text=True, timeout=timeout_s)
    except subprocess.TimeoutExpired:
        return {"status": "TIMEOUT", "seconds": round(time.time() - t0, 3), "cnf_sha256": sha256_file(cnf_path)}
    seconds = round(time.time() - t0, 3)
    status = "ERROR"
    model: set[int] = set()
    for line in run.stdout.splitlines():
        if line.startswith("s SATISFIABLE"):
            status = "SAT"
        elif line.startswith("s UNSATISFIABLE"):
            status = "UNSAT"
        elif line.startswith("v "):
            for tok in line[2:].split():
                lit = int(tok)
                if lit > 0:
                    model.add(lit)
    rec = {
        "status": status,
        "exit_code": run.returncode,
        "seconds": seconds,
        "cnf_sha256": sha256_file(cnf_path),
        "solver_stdout_tail": run.stdout[-400:],
        "solver_stderr_tail": run.stderr[-400:],
    }
    if status == "SAT":
        rec["model"] = sorted(model)
    if status == "UNSAT" and want_proof:
        rec["proof_sha256"] = sha256_file(proof_path)
        rec["proof_bytes"] = proof_path.stat().st_size
        t1 = time.time()
        chk = subprocess.run(
            ["wsl.exe", "-e", DRAT_TRIM, wsl_path(cnf_path), wsl_path(proof_path)],
            capture_output=True,
            text=True,
            timeout=max(timeout_s, 600),
        )
        rec["drat_trim_seconds"] = round(time.time() - t1, 3)
        rec["drat_trim_verified"] = "s VERIFIED" in chk.stdout
        rec["drat_trim_tail"] = chk.stdout[-400:]
    return rec


def write_json(path: Path, obj: dict) -> None:
    Path(path).write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", flush=True)
    sys.exit(1)
