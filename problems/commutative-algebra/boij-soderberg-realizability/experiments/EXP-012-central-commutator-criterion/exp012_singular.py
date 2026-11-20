"""Second instrument of EXP-012: Singular 4.3.2 (Plural) in WSL, one script per case of family X.

A thin layer over EXP-009's generator (`exp009_singular.build_script`, which is EXP-005's: ring over GF(p) with weights (1, 1, 2),
the relation y x = x y - z, the module U / (U f + U g), the graded Betti table from `mres`).  The scripts are generated from the
STORED polynomials of results.json (lists [a, b, c, coefficient]), never from live objects.  The run is bounded inside WSL by
`timeout`, so a script that does not finish leaves no Singular process behind.
"""
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIBLING = HERE.parent / "EXP-009-linear-family-below-2e"
if str(SIBLING) not in sys.path:
    sys.path.append(str(SIBLING))

import exp009_singular as Sg9  # noqa: E402

build_script = Sg9.build_script
parse_output = Sg9.parse_output


def relations_of(stored):
    """[[component, [a, b, c], coefficient], ...] for each stored polynomial [[a, b, c, v], ...] (component 0)."""
    return [[[0, [a, b, c], v] for a, b, c, v in poly] for poly in stored]


def script_text(p, stored_f, stored_g):
    return build_script({"char": p, "degree": 1}, 1, relations_of([stored_f, stored_g]))


def wsl_path(path):
    s = str(Path(path).resolve()).replace("\\", "/")
    return "/mnt/" + s[0].lower() + s[2:]


def run_case(name, p, stored_f, stored_g, script_dir, out_dir, timeout=2400):
    """Write <name>.sing in script_dir, run it with a 40 minute bound, write <name>.out in out_dir; returns
    (Betti table {(i, j): rank} or None, seconds, error or None)."""
    script_dir, out_dir = Path(script_dir), Path(out_dir)
    script_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    sp = script_dir / (name + ".sing")
    sp.write_text(script_text(p, stored_f, stored_g), encoding="utf-8", newline="\n")
    t0 = time.time()
    try:
        proc = subprocess.run(["wsl", "-e", "bash", "-lc", "timeout %d Singular -q < '%s'" % (timeout, wsl_path(sp))],
                              capture_output=True, text=True, timeout=timeout + 120)
    except subprocess.TimeoutExpired:
        return None, time.time() - t0, "timeout after %d s (client)" % timeout
    dt = time.time() - t0
    out = proc.stdout + proc.stderr
    (out_dir / (name + ".out")).write_text(out, encoding="utf-8", newline="\n")
    if proc.returncode == 124:
        return None, dt, "timeout after %d s" % timeout
    try:
        return parse_output(out), dt, None
    except RuntimeError as exc:
        return None, dt, str(exc)[:400]
