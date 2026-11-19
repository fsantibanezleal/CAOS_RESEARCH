"""Instrument I2 of EXP-002: graded Betti numbers by Singular 4.3.2 Plural (run in WSL).

This file imports nothing from the uhlib library (instrument I1): it receives a presentation as plain
data (generator degrees and relation vectors with JSON coefficients), writes one Singular script, runs it
and parses the DEGREES of the generators of each module of the minimal resolution `mres` (never betti(),
whose output on G-algebras is not reliable).

A presentation is  {"field": {"char": c, "deg": k, "modulus": [..]},  "shifts": [s_1..s_r],
                    "rels": [[[comp, [a, b, c], coef], ...], ...]}
where a term is coef * x^a y^b z^c in component comp (0-based) of the free module sum U(-s_i).
Coefficient JSON: "n/d" string (QQ), int (GF(p)), list of ints (GF(p^k), coefficients of a^0, a^1, ...).
"""
import subprocess
import time
from pathlib import Path


# Resolve and print the degrees of the generators of every module of the minimal resolution (zero vectors skipped).
RESOLVE_PROGRAM = """list L = mres(M, 0);
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


def _wsl_path(p):
    p = str(Path(p).resolve()).replace("\\", "/")
    return "/mnt/" + p[0].lower() + p[2:]


def _ring_header(field):
    char, deg = field["char"], field["deg"]
    if char == 0:
        head, extra = "0", ""
    elif deg == 1:
        head, extra = str(char), ""
    else:
        mod = field["modulus"]  # low to high, monic
        terms = ["a^%d" % i if c == 1 else "%d*a^%d" % (c, i) for i, c in enumerate(mod) if c]
        head = "(%d,a)" % char
        extra = "minpoly = %s;\n" % "+".join(reversed(terms))
    return (
        "ring r0 = %s,(x,y,z),wp(1,1,2);\n%s"
        "matrix D[3][3];\nD[1,2] = -z;\n"
        "def S = nc_algebra(1,D);\nsetring S;\n" % (head, extra)
    )


def _coef(field, c):
    if field["char"] == 0:
        n, _, d = str(c).partition("/")
        return "(%s/%s)" % (n, d) if d else "(%s)" % n
    if field["deg"] == 1:
        return "(%d)" % c
    return "(" + "+".join("%d*a^%d" % (v, i) for i, v in enumerate(c) if v) + ")" if any(c) else "0"


def _term(field, coef, mono):
    a, b, c = mono
    mon = "*".join(s for s in ("x^%d" % a if a else "", "y^%d" % b if b else "", "z^%d" % c if c else "") if s)
    cs = _coef(field, coef)
    return cs + ("*" + mon if mon else "")


def build_script(pres):
    field, shifts, rels = pres["field"], pres["shifts"], pres["rels"]
    r = len(shifts)
    lines = [_ring_header(field)]
    vecs = []
    for rel in rels:
        comps = [[] for _ in range(r)]
        for comp, mono, coef in rel:
            comps[comp].append(_term(field, coef, mono))
        vecs.append("[" + ",".join("+".join(t) if t else "0" for t in comps) + "]")
    lines.append("module M = %s;\n" % ",".join(vecs))
    lines.append("intvec sh0 = %s;\n" % ",".join(str(s) for s in shifts))
    lines.append(
        "proc vdeg(vector v, intvec sh)\n{\n  int i; intvec e;\n"
        "  for (i = 1; i <= size(sh); i++)\n  {\n    if (v[i] != 0)\n    {\n"
        "      e = leadexp(v[i]);\n      return(e[1] + e[2] + 2*e[3] + sh[i]);\n    }\n  }\n  return(-1000000);\n}\n"
    )
    lines.append(RESOLVE_PROGRAM)
    return "".join(lines)


def parse_output(text):
    """Betti table {(i, degree): rank} from the DEG lines."""
    table = {}
    seen_end = False
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("DEG "):
            parts = line.split()
            i = int(parts[1])
            degs = [int(t) for t in " ".join(parts[2:]).replace(",", " ").split()]
            for d in degs:
                table[(i, d)] = table.get((i, d), 0) + 1
        elif line == "END":
            seen_end = True
    if not seen_end:
        raise RuntimeError("Singular did not reach END; output was:\n" + text[-2000:])
    return table


def run(pres, script_path, timeout=900):
    """Write the script, run Singular in WSL, return (Betti table, seconds, raw output)."""
    script_path = Path(script_path)
    script_path.parent.mkdir(parents=True, exist_ok=True)
    script_path.write_text(build_script(pres), encoding="utf-8", newline="\n")
    t0 = time.time()
    proc = subprocess.run(
        ["wsl", "-e", "bash", "-lc", "Singular -q < '%s'" % _wsl_path(script_path)],
        capture_output=True, text=True, timeout=timeout,
    )
    dt = time.time() - t0
    out = proc.stdout + proc.stderr
    return parse_output(out), dt, out
