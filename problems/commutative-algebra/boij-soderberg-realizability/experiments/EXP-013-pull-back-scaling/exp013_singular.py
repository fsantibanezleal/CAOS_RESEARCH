"""Second instrument of EXP-013: Singular 4.3.2 (Plural) in WSL, one script per module, generated from the STORED polynomials of
results.json (never from live objects): the generators of M' and the stored images of exactly those generators.

The script generator, the output parser and the WSL path helper are those of EXP-005 (`exp005_singular`, which imports nothing from
`uhlib`); the ring is GF(p), weights (1, 1, 2), the relation y x = x y - z (D[1,2] = -z) and the left module U / (U g_1 + ... + U g_k),
the same side and relation as `uhlib`.  The length is derived from the Betti table printed by Singular (alternating sum with the
dimension of U_n of EXP-005's own formula), not from `uhlib`.
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


def field_record(p):
    return {"char": p, "degree": 1}


def relations_of(gens_list):
    """Relations [[component, [i, j, k], coefficient], ...] of stored polynomials (lists [[i, j, k], c])."""
    return [[[0, list(m), c] for m, c in poly] for poly in gens_list]


def script_text(p, gens_list):
    return build_script(field_record(p), 1, relations_of(gens_list))


def length_from_table(table):
    """(length, True) when the Hilbert function recovered from the table vanishes in the last four degrees computed, else
    (None, False): the module is then not of finite length (or the table is not that of a module of finite length)."""
    top = max(j for (_, j) in table) + 4
    dims = Sg.hilbert_from_table(table, top)
    if any(dims[-4:]) or any(v < 0 for v in dims):
        return None, False
    return sum(dims), True


def run_case(name, p, gens_list, script_dir, timeout=2400):
    """(Betti table {(i, j): rank} or None, length or None, seconds, error or None); writes <name>.sing and <name>.out in script_dir.
    The time limit is enforced inside WSL by `timeout`, so that no Singular process outlives its limit."""
    script_dir = Path(script_dir)
    script_dir.mkdir(parents=True, exist_ok=True)
    sp = script_dir / (name + ".sing")
    sp.write_text(script_text(p, gens_list), encoding="utf-8", newline="\n")
    t0 = time.time()
    proc = subprocess.run(["wsl", "-e", "bash", "-lc", "timeout %d Singular -q < '%s'" % (timeout, Sg.wsl_path(sp))],
                          capture_output=True, text=True, timeout=timeout + 300)
    out, dt = proc.stdout + proc.stderr, time.time() - t0
    (script_dir / (name + ".out")).write_text(out, encoding="utf-8", newline="\n")
    try:
        table = parse_output(out)
    except RuntimeError as exc:
        why = "timeout after %d s" % timeout if dt >= timeout - 5 else str(exc)[:400]
        return None, None, dt, why
    length, _ = length_from_table(table)
    return table, length, dt, None
