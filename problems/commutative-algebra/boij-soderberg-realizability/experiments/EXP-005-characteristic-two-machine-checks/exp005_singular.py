"""Second instrument of EXP-005: Singular 4.3.2 (Plural) in WSL, scripts generated from the STORED relations.

This file imports nothing from `uhlib` and nothing from exp005_routine: it receives a case record as plain data
(field record, relations as JSON lists [component, [i, j, k], coefficient]) and writes a Singular script for the
module U^a / (U F_1 + ... + U F_b) over the enveloping algebra of the Heisenberg Lie algebra,
y x = x y - z (Plural: D[1,2] = -z), weights (1, 1, 2).  The graded Betti table is read from the degrees of the
generators of the minimal free resolution `mres`; the Hilbert function is the alternating sum of the table, with
dim U_n counted here by its own closed formula.  Coefficient JSON: "n/d" strings (QQ), ints (GF(p)), lists of ints
(GF(p^k), coefficients of a^0, a^1, ...).  Field moduli are taken from the case record (low to high, monic).
"""
import subprocess
import time
from pathlib import Path

PROGRAM = """list L = mres(M, 0);
int i, j, n, t;
intvec sh = sh0;
intvec nsh;
print("DEG 0 " + string(sh0));
for (i = 1; i <= size(L); i++)
{
  n = 0;
  for (j = 1; j <= ncols(L[i]); j++) { if (L[i][j] != 0) { n++; } }
  if (n == 0) { print("DEG " + string(i)); break; }
  nsh = 0:n;
  t = 0;
  for (j = 1; j <= ncols(L[i]); j++)
  {
    if (L[i][j] != 0) { t++; nsh[t] = vdeg(L[i][j], sh); }
  }
  print("DEG " + string(i) + " " + string(nsh));
  sh = nsh;
}
print("END");
quit;
"""

VDEG = (
    "proc vdeg(vector v, intvec sh)\n{\n  int i; intvec e;\n"
    "  for (i = 1; i <= size(sh); i++)\n  {\n    if (v[i] != 0)\n    {\n"
    "      e = leadexp(v[i]);\n      return(e[1] + e[2] + 2*e[3] + sh[i]);\n    }\n  }\n  return(-1000000);\n}\n"
)


def dim_u(n):
    """dim U_n = number of (i, j, k) with i + j + 2k = n, closed formula (m + 1)(n + 1 - m), m = n // 2."""
    if n < 0:
        return 0
    m = n // 2
    return (m + 1) * (n + 1 - m)


def ring_header(field):
    char, deg = field["char"], field["degree"]
    if char == 0:
        head, extra = "0", ""
    elif deg == 1:
        head, extra = str(char), ""
    else:
        terms = ["a^%d" % i if c == 1 else "%d*a^%d" % (c, i) for i, c in enumerate(field["modulus"]) if c]
        head, extra = "(%d,a)" % char, "minpoly = %s;\n" % "+".join(reversed(terms))
    return ("ring r0 = %s,(x,y,z),wp(1,1,2);\n%s" % (head, extra)
            + "matrix D[3][3];\nD[1,2] = -z;\ndef S = nc_algebra(1,D);\nsetring S;\n")


def coef_text(field, c):
    if field["char"] == 0:
        n, _, d = str(c).partition("/")
        return "(%s/%s)" % (n, d) if d else "(%s)" % n
    if field["degree"] == 1:
        return "(%d)" % c
    return "(" + "+".join("%d*a^%d" % (v, i) for i, v in enumerate(c) if v) + ")" if any(c) else "0"


def term_text(field, c, mono):
    i, j, k = mono
    mon = "*".join(s for s in ("x^%d" % i if i else "", "y^%d" % j if j else "", "z^%d" % k if k else "") if s)
    return coef_text(field, c) + ("*" + mon if mon else "")


def build_script(field, a, relations, shifts=None):
    """Singular script for the module U^a / (relations); zero relations are dropped (they generate nothing)."""
    shifts = shifts if shifts is not None else [0] * a
    vecs = []
    for rel in relations:
        comps = [[] for _ in range(a)]
        for comp, mono, c in rel:
            comps[comp].append(term_text(field, c, mono))
        if any(comps):
            vecs.append("[" + ",".join("+".join(t) if t else "0" for t in comps) + "]")
    if not vecs:
        raise ValueError("no nonzero relation")
    return (ring_header(field) + "module M = %s;\n" % ",".join(vecs)
            + "intvec sh0 = %s;\n" % ",".join(str(s) for s in shifts) + VDEG + PROGRAM)


def wsl_path(p):
    p = str(Path(p).resolve()).replace("\\", "/")
    return "/mnt/" + p[0].lower() + p[2:]


def parse_output(text):
    table, seen_end = {}, False
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("DEG "):
            parts = line.split()
            i = int(parts[1])
            for d in [int(t) for t in " ".join(parts[2:]).replace(",", " ").split()]:
                table[(i, d)] = table.get((i, d), 0) + 1
        elif line == "END":
            seen_end = True
    if not seen_end:
        raise RuntimeError("Singular did not reach END; output was:\n" + text[-1500:])
    return table


def hilbert_from_table(table, D):
    return [sum((-1) ** i * r * dim_u(n - j) for (i, j), r in table.items()) for n in range(D + 1)]


def run_script(script_path, timeout=1200):
    """Run Singular on a script file through WSL; returns (output text, seconds)."""
    t0 = time.time()
    proc = subprocess.run(["wsl", "-e", "bash", "-lc", "Singular -q < '%s'" % wsl_path(script_path)],
                          capture_output=True, text=True, timeout=timeout)
    return proc.stdout + proc.stderr, time.time() - t0


def run_case(name, field, a, relations, script_dir, shifts=None, timeout=1200):
    """Write <name>.sing, run it, store <name>.out; return (Betti table, seconds, error or None)."""
    script_dir = Path(script_dir)
    script_dir.mkdir(parents=True, exist_ok=True)
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in name)
    sp = script_dir / (safe + ".sing")
    try:
        sp.write_text(build_script(field, a, relations, shifts), encoding="utf-8", newline="\n")
        out, dt = run_script(sp, timeout)
    except subprocess.TimeoutExpired:
        return None, float(timeout), "timeout after %d s" % timeout
    except Exception as exc:  # recorded, never hidden
        return None, 0.0, repr(exc)[:400]
    (script_dir / (safe + ".out")).write_text(out, encoding="utf-8", newline="\n")
    try:
        return parse_output(out), dt, None
    except RuntimeError as exc:
        return None, dt, str(exc)[:400]
