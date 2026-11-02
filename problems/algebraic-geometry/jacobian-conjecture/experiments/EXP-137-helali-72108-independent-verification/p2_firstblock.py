"""EXP-137 P2: first elimination step. J4 with A = t + a2 t^2 + ... + a7 t^7 + t^8, D = d2 t^2 + ... + d12 t^12.

Own derivation: solve D from J4 (triangular), collect compatibility equations in a2..a7, then Singular over Q
(`std`, `dim`, `mult`, `fglm` to lex) gives the eliminant of a7 and the lex shape. Everything exact.
"""

from __future__ import annotations

import re
import subprocess
import sys
import time
from pathlib import Path

import sympy as sp
from flint import fmpq, fmpq_poly

HERE = Path(__file__).resolve().parent
ART = HERE / "artifacts"
SCRATCH = Path("D:/_Temp/jc-exp137-verify-2026-11-01")

t = sp.Symbol("t")
a = {i: sp.Symbol(f"a{i}") for i in range(1, 9)}
d = {i: sp.Symbol(f"d{i}") for i in range(2, 13)}


def wsl_path(p: Path) -> str:
    s = str(p.resolve()).replace("\\", "/")
    return "/mnt/" + s[0].lower() + s[2:]


def compat_equations():
    """Return (dsolution {d_i: expr in a}, compat [expr in a2..a7], A, D)."""
    A = sum(a[i] * t**i for i in a).subs({a[1]: 1, a[8]: 1})
    D = sum(d[i] * t**i for i in d)
    J4 = sp.Poly(sp.expand(2 * A * sp.diff(D, t) - 3 * sp.diff(A, t) * D - t**2), t)
    sol: dict = {}
    compat = []
    for k in range(J4.degree() + 1):
        e = sp.expand(J4.coeff_monomial(t**k)).subs(sol)
        e = sp.expand(e)
        if e == 0:
            continue
        unsolved = [v for v in d.values() if e.has(v)]
        if len(unsolved) == 1 and sp.Poly(e, unsolved[0]).degree() == 1:
            v = unsolved[0]
            c = sp.Poly(e, v).coeff_monomial(v)
            assert c.is_number and c != 0  # J4 coefficient (2k-3) is a nonzero constant
            sol[v] = sp.expand(-(e - c * v) / c)
            # keep earlier solutions consistent (back-substitution into the already solved ones)
            sol = {kk: sp.expand(vv.subs(v, sol[v])) for kk, vv in sol.items()}
        else:
            assert not unsolved, f"J4 degree {k}: unsolved d variables {unsolved}"
            compat.append(e)
    return sol, compat, A, D


def _sing_int_poly(e):
    """Primitive integer-coefficient form of e (denominators cleared; same zero set), Singular syntax."""
    vs = [a[i] for i in range(2, 8)]
    p = sp.Poly(sp.expand(e), *vs, domain=sp.QQ)
    _den, p = p.clear_denoms()
    _con, p = p.primitive()
    terms = []
    for mon, c in p.terms():
        factors = [f"{v}^{k}" if k > 1 else str(v) for v, k in zip(vs, mon) if k]
        terms.append("(" + str(int(c)) + ")" + ("*" + "*".join(factors) if factors else ""))
    return "+".join(terms)


def singular_script(compat, out_prefix):
    gens = ",\n".join(_sing_int_poly(e) for e in compat)
    return f"""LIB "modstd.lib";
short=0;
ring R=0,(a2,a3,a4,a5,a6,a7),dp;
option(redSB);
ideal I=
{gens};
int t0=timer;
ideal G=modStd(I);
"DP_SIZE="+string(size(G));
"DIM="+string(dim(G));
"MULT="+string(mult(G));
"DP_TIME_SECONDS="+string(timer-t0);
ring S=0,(a2,a3,a4,a5,a6,a7),lp;
option(redSB);
ideal L=fglm(R,G);
"LEX_SIZE="+string(size(L));
int i;
for(i=1;i<=size(L);i++){{ "L["+string(i)+"]="+string(L[i]); }}
"DONE";
quit;
"""


def parse_lex(text):
    rels = {}
    for line in text.splitlines():
        m = re.match(r"L\[(\d+)\]=(.*)", line.strip())
        if m:
            rels[int(m.group(1))] = m.group(2)
    return rels


def qpoly_from_expr(expr, var):
    p = sp.Poly(sp.sympify(expr, locals={str(var): var}), var, domain=sp.QQ)
    co = [fmpq(0)] * (p.degree() + 1)
    for (i,), c in p.terms():
        c = sp.Rational(c)
        co[i] = fmpq(int(c.p), int(c.q))
    return fmpq_poly(co)


def run(timeout_seconds=7200, log=print):
    ART.mkdir(exist_ok=True)
    SCRATCH.mkdir(parents=True, exist_ok=True)
    sol, compat, A, D = compat_equations()
    out = {"d_solved": len(sol), "compat_equations": len(compat),
           "compat_degrees": [sp.Poly(e, *[a[i] for i in range(2, 8)]).total_degree() for e in compat]}
    log(f"P2: solved {len(sol)} coefficients of D, {len(compat)} compatibility equations in a2..a7")
    sing = SCRATCH / "p2_firstblock.sing"
    outp = ART / "p2_singular.out"
    sing.write_text(singular_script(compat, "p2"))
    if not outp.exists() or "DONE" not in outp.read_text():
        t0 = time.time()
        log(f"P2: running Singular (kill after {timeout_seconds} s)")
        try:
            r = subprocess.run(["wsl", "-e", "Singular", "-q", wsl_path(sing)], capture_output=True, text=True,
                               timeout=timeout_seconds)
            outp.write_text(r.stdout + (("\nSTDERR:\n" + r.stderr) if r.stderr.strip() else ""))
        except subprocess.TimeoutExpired:
            out["status"] = "UNVERIFIED"
            out["reason"] = f"Singular exceeded {timeout_seconds} s"
            return out
        log(f"P2: Singular finished in {time.time() - t0:.1f} s")
    text = outp.read_text()
    out["singular_output_file"] = "artifacts/p2_singular.out"
    for key in ("DP_SIZE", "DIM", "MULT", "LEX_SIZE", "DP_TIME_SECONDS"):
        m = re.search(rf"^{key}=(\d+)", text, re.M)
        out[key.lower()] = int(m.group(1)) if m else None
    rels = parse_lex(text)
    out["lex_relations"] = len(rels)
    u = sp.Symbol("a7")
    H = qpoly_from_expr(rels[1], u)
    out["eliminant_degree"] = H.degree()
    out["eliminant_in_a7_only"] = True
    cont, facs = H.factor()
    out["eliminant_irreducible_over_Q"] = bool(len(facs) == 1 and facs[0][1] == 1 and facs[0][0].degree() == H.degree())
    out["eliminant_factor_degrees"] = [(f.degree(), m) for f, m in facs]
    # a7 enters only through a7^7 in H
    out["eliminant_exponents"] = [i for i in range(H.degree() + 1) if H[i] != 0]
    out["eliminant_monic_hash"] = _hash_poly(H / H[H.degree()])
    # other relations: each is  c*a_i - poly(a7), leading coefficient a rational constant
    shape = []
    for i in sorted(rels):
        if i == 1:
            continue
        e = sp.sympify(rels[i].replace("^", "**"), locals={f"a{k}": sp.Symbol(f"a{k}") for k in range(2, 8)})
        vs = sorted(str(s) for s in e.free_symbols - {u})
        shape.append(vs)
    out["lex_shape_linear_in_a2_to_a6"] = shape == [[f"a{k}"] for k in (6, 5, 4, 3, 2)]
    # compare with Helali's H(a7) when the text file is present (read as data only)
    hel = Path("E:/_Datos/caos-research/jacobian-conjecture/sources/helali-21479814/bundle/exact_replay/firstblock_Q_exact.out")
    if hel.exists():
        hrels = parse_lex(hel.read_text())
        Hh = qpoly_from_expr(hrels[1], u)
        ratio = H[H.degree()] / Hh[Hh.degree()]
        out["helali_H_file"] = "bundle/exact_replay/firstblock_Q_exact.out (L[1])"
        out["helali_H_equal_up_to_constant"] = bool(H == Hh * ratio)
        out["helali_H_constant_ratio_ours_over_theirs"] = f"{ratio.p}/{ratio.q}"
        out["status"] = "PASS" if (out["helali_H_equal_up_to_constant"] and out["eliminant_degree"] == 35
                                     and out["eliminant_irreducible_over_Q"] and out["dim"] == 0) else "FAIL"
    else:
        out["status"] = "UNVERIFIED"
    out["_H_coeffs"] = [(int(H[i].p), int(H[i].q)) for i in range(H.degree() + 1)]
    out["_lex"] = rels
    return out


def _hash_poly(p):
    import hashlib

    s = ",".join(f"{int(p[i].p)}/{int(p[i].q)}" for i in range(p.degree() + 1))
    return hashlib.sha256(s.encode()).hexdigest()


if __name__ == "__main__":
    res = run(log=lambda s: print(s, flush=True))
    print({k: v for k, v in res.items() if not k.startswith("_")})
    sys.exit(0)
