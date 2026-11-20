"""Second instrument of EXP-011: Singular 4.3.2 (Plural) in WSL, one script per case, generated from the STORED polynomials f and g
of results.json (never from live objects).

The script generator, the output parser and the WSL runner are those of EXP-005 (`exp005_singular`, which imports nothing from
`uhlib` and nothing from the first instrument); the ring is GF(p), weights (1, 1, 2), the relation y x = x y - z
(D[1,2] = -z) and the left module U / (U f + U g), the same side and relation as `uhlib`.
"""
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIBLING = HERE.parent / "EXP-005-characteristic-two-machine-checks"
if str(SIBLING) not in sys.path:
    sys.path.append(str(SIBLING))

import exp005_singular as Sg  # noqa: E402

build_script = Sg.build_script
parse_output = Sg.parse_output
run_script = Sg.run_script


def field_record(p):
    return {"char": p, "degree": 1}


def relations_of(f_list, g_list):
    """Relations [[component, [i, j, k], coefficient], ...] of the stored polynomials (lists [[i, j, k], c])."""
    return [[[0, list(m), c] for m, c in poly] for poly in (f_list, g_list)]


def script_text(p, f_list, g_list):
    return build_script(field_record(p), 1, relations_of(f_list, g_list))


def run_case(cid, p, f_list, g_list, script_dir, timeout=2400):
    """(Betti table {(i, j): rank} or None, seconds, error or None); writes <cid>.sing and <cid>.out in script_dir.  The time limit is
    enforced inside WSL by `timeout`, so that no Singular process outlives its limit."""
    script_dir = Path(script_dir)
    script_dir.mkdir(parents=True, exist_ok=True)
    sp = script_dir / (cid + ".sing")
    sp.write_text(script_text(p, f_list, g_list), encoding="utf-8", newline="\n")
    t0 = time.time()
    proc = subprocess.run(["wsl", "-e", "bash", "-lc", "timeout %d Singular -q < '%s'" % (timeout, Sg.wsl_path(sp))],
                          capture_output=True, text=True, timeout=timeout + 120)
    out, dt = proc.stdout + proc.stderr, time.time() - t0
    (script_dir / (cid + ".out")).write_text(out, encoding="utf-8", newline="\n")
    try:
        return parse_output(out), dt, None
    except RuntimeError as exc:
        why = "timeout after %d s" % timeout if dt >= timeout - 5 else str(exc)[:400]
        return None, dt, why
