"""EXP-139: write the Singular inputs for the exact Case 1 unit-ideal test (hypothesis.md).

Builds our 13 Case 1 compatibility equations with EXP-137's own cascade (p3_link.case1_link), then writes:
  artifacts/case1_Q.sing          I = (E_1..E_13, H(u)) over Q in q0..q5, u; std; UNIT/NONUNIT
  artifacts/gate_p<p>.sing        the same equations at a simple root r of H modulo p (u -> r), s kept as a variable
  artifacts/control_p<p>.sing     layers 3..-1 only, same specialization (must be non-unit)
Run from the repository root with the repository venv.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
E137 = HERE.parent / "EXP-137-helali-72108-independent-verification"
sys.path.insert(0, str(E137))
ART = HERE / "artifacts"

import addendum_a as AA  # noqa: E402
import p3_link as LK  # noqa: E402

NAMES = [f"q{i}" for i in range(6)] + ["u"]
GATE_PRIMES = (1021, 1031, 1033, 1049, 1061)


def frac(q) -> str:
    num, den = int(q.p), int(q.q)
    return str(num) if den == 1 else f"{num}/{den}"


def term(co: str, mon: tuple, upow: int) -> str:
    facs = [f"{NAMES[i]}^{e}" if e > 1 else NAMES[i] for i, e in enumerate(mon) if e]
    if upow:
        facs.append(f"u^{upow}" if upow > 1 else "u")
    return f"({co})" + ("*" + "*".join(facs) if facs else "")


def poly_Q(poly) -> str:
    terms = []
    for mon, c in poly.d.items():
        cp = c.p
        for i in range(cp.degree() + 1):
            if cp[i] != 0:
                terms.append(term(frac(cp[i]), mon, i))
    return "+".join(terms) if terms else "0"


def poly_p(poly, r: int, p: int) -> str:
    terms = []
    for mon, c in poly.d.items():
        v = AA.kel_mod(c, r, p)
        if v:
            terms.append(term(str(v), mon, 0))
    return "+".join(terms) if terms else "0"


def script(char: str, names: list[str], gens: list[str]) -> str:
    return (f"ring R={char},({','.join(names)}),dp;\noption(redSB);\nideal I=\n" + ",\n".join(gens) + ";\n"
            "int t0=timer;\nideal J=std(I);\n"
            "if(size(J)==1 && deg(J[1])==0){ \"UNIT\"; } else { \"NONUNIT\"; \"DIM=\"+string(dim(J)); }\n"
            "\"SECONDS=\"+string(timer-t0);\nquit;\n")


def main() -> int:
    F, A, D = LK.our_field(log=print)
    link = LK.case1_link(F, A, D, log=print)
    cas = link["_cascade"]
    compat = [p for _k, p in cas.compat]
    layers = [k for k, _p in cas.compat]
    print(f"{len(compat)} compatibility equations, layers {layers}")
    H = F.m
    hstr = "+".join(term(frac(H[i]), (0,) * 6, i) for i in range(H.degree() + 1) if H[i] != 0)
    ART.mkdir(exist_ok=True)
    (ART / "case1_Q.sing").write_text(script("0", NAMES, [poly_Q(p) for p in compat] + [hstr]), encoding="utf-8")
    hcoeffs = [H[i] for i in range(H.degree() + 1)]
    for p in GATE_PRIMES:
        hm = [AA.frac_mod(c, p) for c in hcoeffs]
        deriv = [(i * hm[i]) % p for i in range(1, len(hm))]
        roots = [r for r in AA.poly_mod_roots(hm, p) if sum(co * pow(r, i, p) for i, co in enumerate(deriv)) % p]
        r = roots[0]
        gens = [poly_p(q, r, p) for q in compat]
        (ART / f"gate_p{p}.sing").write_text(script(str(p), NAMES[:6], gens), encoding="utf-8")
        upper = [poly_p(q, r, p) for q, k in zip(compat, layers) if k >= -1]
        (ART / f"control_p{p}.sing").write_text(script(str(p), NAMES[:6], upper), encoding="utf-8")
        print(f"p={p}: root {r}")
    print("written", sorted(x.name for x in ART.glob("*.sing")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
