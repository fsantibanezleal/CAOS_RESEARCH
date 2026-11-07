"""EXP-140: rewrite EXP-139's exact Case 1 ideal over the quintic subfield Q(v), v = u^7 (hypothesis.md).

Input: EXP-139 `artifacts/case1_Q.sing` (13 equations in q0..q5, u with rational coefficients, then H(u)).
For equation e and each term c * u^j * q^m: j' = j - w.m must be = c_e (mod 7) for one c_e per equation; write
j' = c_e + 7 t, divide the equation by u^(c_e) and multiply by v^(T_e), T_e = max(0, -min t), giving
E'_e = sum c * v^(t + T_e) * q^m. With h(v) from H(u) = h(u^7):
  artifacts/caseL_Q.sing      ideal (E'_1..E'_13, h(v)) over Q in q0..q5, v; std; UNIT/NONUNIT
  artifacts/gateL_p<p>.sing   the E'_e at a simple root r of h mod p (v -> r)
  artifacts/controlL_p<p>.sing  equations of layers 3..-1 (the first four) only
  artifacts/identity-check.txt  E_e(u^(-w) q) == u^(c_e) v^(-T_e) E'_e(q) at random points mod a 61-bit prime
"""
import random
import re
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "EXP-139-case1-unit-certificate" / "artifacts" / "case1_Q.sing"
ART = HERE / "artifacts"
W = (2, 3, 2, 1, 2, 1)
VARS = [f"q{i}" for i in range(6)]
UPPER = 4                                    # layers [0, 0, -1, -1] = the first four equations
GATE_PRIMES = (1021, 1031, 1033, 1049, 1061, 1063, 1069, 1087, 1091, 1093)


def parse(gen):
    terms = []
    for co, rest in re.findall(r"\(([^)]*)\)((?:\*[a-z]\d?(?:\^\d+)?)*)", gen):
        mon, j = [0] * 6, 0
        for name, ex in re.findall(r"\*([a-z]\d?)(?:\^(\d+))?", rest):
            if name == "u":
                j = int(ex or 1)
            else:
                mon[VARS.index(name)] = int(ex or 1)
        terms.append((Fraction(co), tuple(mon), j))
    return terms


def fmt(terms, varnames, last):
    out = []
    for c, mon, k in terms:
        facs = [f"{varnames[i]}^{e}" if e > 1 else varnames[i] for i, e in enumerate(mon) if e]
        if k:
            facs.append(f"{last}^{k}" if k > 1 else last)
        cs = str(c.numerator) if c.denominator == 1 else f"{c.numerator}/{c.denominator}"
        out.append(f"({cs})" + ("*" + "*".join(facs) if facs else ""))
    return "+".join(out) if out else "0"


def script(char, names, gens):
    return (f"ring R={char},({','.join(names)}),dp;\noption(redSB);\nideal I=\n" + ",\n".join(gens) + ";\n"
            "int t0=timer;\nideal J=std(I);\n"
            "if(size(J)==1 && deg(J[1])==0){ \"UNIT\"; } else { \"NONUNIT\"; \"DIM=\"+string(dim(J)); }\n"
            "\"SECONDS=\"+string(timer-t0);\nquit;\n")


def modp_terms(terms, r, p):
    out = {}
    for c, mon, k in terms:
        v = c.numerator * pow(c.denominator, -1, p) * pow(r, k, p) % p
        out[mon] = (out.get(mon, 0) + v) % p
    return [(Fraction(v), mon, 0) for mon, v in out.items() if v]


def main():
    text = SRC.read_text(encoding="utf-8")
    gens = [g.strip() for g in text.split("ideal I=", 1)[1].split(";", 1)[0].split(",\n")]
    eqs, Hterms = [parse(g) for g in gens[:-1]], parse(gens[-1])
    assert all(j % 7 == 0 and mon == (0,) * 6 for _, mon, j in Hterms), "H is not a polynomial in u^7"
    h = [(c, (0,) * 6, j // 7) for c, _, j in Hterms]
    new, meta = [], []
    for e, terms in enumerate(eqs):
        shifted = [(c, mon, j - sum(a * b for a, b in zip(W, mon))) for c, mon, j in terms]
        res = {jp % 7 for _, _, jp in shifted}
        assert len(res) == 1, f"equation {e} not homogeneous mod 7"
        ce = res.pop()
        ts = [(jp - ce) // 7 for _, _, jp in shifted]
        T = max(0, -min(ts))
        new.append([(c, mon, t + T) for (c, mon, _), t in zip(shifted, ts)])
        meta.append((ce, T))
    ART.mkdir(exist_ok=True)
    (ART / "caseL_Q.sing").write_text(
        script("0", VARS + ["v"], [fmt(t, VARS, "v") for t in new] + [fmt(h, VARS, "v")]), encoding="utf-8")
    # identity check: E_e(u^-w q) == u^c_e * v^-T_e * E'_e(q) with v = u^7, at random points mod a prime
    P = (1 << 61) - 1
    rng = random.Random(20261107)
    bad = 0
    for _ in range(5):
        u = rng.randrange(2, P)
        q = [rng.randrange(1, P) for _ in range(6)]
        uinv = pow(u, -1, P)
        qs = [q[i] * pow(uinv, W[i], P) % P for i in range(6)]          # q_old = u^(-w) q_new
        v = pow(u, 7, P)
        for e in range(len(eqs)):
            lhs = 0
            for c, mon, j in eqs[e]:
                term = c.numerator * pow(c.denominator, -1, P) * pow(u, j, P)
                for i, ex in enumerate(mon):
                    term = term * pow(qs[i], ex, P) % P
                lhs = (lhs + term) % P
            rhs = 0
            for c, mon, k in new[e]:
                term = c.numerator * pow(c.denominator, -1, P) * pow(v, k, P)
                for i, ex in enumerate(mon):
                    term = term * pow(q[i], ex, P) % P
                rhs = (rhs + term) % P
            ce, T = meta[e]
            rhs = rhs * pow(u, ce, P) * pow(pow(v, T, P), -1, P) % P
            bad += lhs != rhs
    (ART / "identity-check.txt").write_text(
        f"5 random points mod 2^61-1, 13 equations each: mismatches {bad}\noffsets (c_e, T_e): {meta}\n",
        encoding="utf-8")
    print("identity mismatches:", bad, "offsets:", meta)
    # modular gates
    written = 0
    for p in GATE_PRIMES:
        hp = [c.numerator * pow(c.denominator, -1, p) % p for c, _, _ in sorted(h, key=lambda x: x[2])]
        degs = sorted(k for _, _, k in h)
        coef = {k: c for k, c in zip(degs, hp)}
        poly = [coef.get(k, 0) for k in range(max(degs) + 1)]
        der = [(k * poly[k]) % p for k in range(1, len(poly))]
        roots = [x for x in range(p) if sum(a * pow(x, k, p) for k, a in enumerate(poly)) % p == 0
                 and sum(a * pow(x, k, p) for k, a in enumerate(der)) % p]
        if not roots:
            continue
        r = roots[0]
        gens_p = [fmt(modp_terms(t, r, p), VARS, "v") for t in new]
        (ART / f"gateL_p{p}.sing").write_text(script(str(p), VARS, gens_p), encoding="utf-8")
        (ART / f"controlL_p{p}.sing").write_text(script(str(p), VARS, gens_p[:UPPER]), encoding="utf-8")
        written += 1
        print(f"p={p}: root {r}")
        if written == 5:
            break
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
