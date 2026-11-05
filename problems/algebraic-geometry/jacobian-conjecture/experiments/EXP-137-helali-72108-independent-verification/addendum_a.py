"""EXP-137 addendum A: modular unit test of the Case 1 branch ideals (declared in hypothesis.md, Addendum A).

Our own 13 Case 1 compatibility equations over K = Q[u]/(H) (cascade layers 3..-3, our derivation) are
reduced at primes p where H has a simple root r modulo p. The branch value s is taken from OUR first
compatibility equation, kappa*(s^2 - gamma)^2: at each prime both square roots of gamma(r) are used (s = +c, -c),
so no external data enters. Singular std over F_p decides whether each specialized branch ideal is the unit
ideal. Control: the equations of the upper layers alone (layers 3..-1) must be allowed to be non-unit.

Run from the repository root:
  .venv/Scripts/python.exe problems/algebraic-geometry/jacobian-conjecture/experiments/EXP-137-helali-72108-independent-verification/addendum_a.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

from sympy import isprime
from sympy.ntheory import sqrt_mod

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
ART = HERE / "artifacts"

import p3_link as LK  # noqa: E402

LOG: list[str] = []
S_INDEX, PARAMS = 1, 6


def log(msg: str) -> None:
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    LOG.append(line)
    print(line, flush=True)


def frac_mod(q, p: int) -> int:
    num, den = int(q.p), int(q.q)
    if den % p == 0:
        raise ZeroDivisionError
    return num * pow(den, -1, p) % p


def kel_mod(c, r: int, p: int) -> int:
    poly = c.p
    acc = 0
    for i in range(poly.degree(), -1, -1):
        acc = (acc * r + frac_mod(poly[i], p)) % p
    return acc


def poly_mod_roots(coeffs: list[int], p: int) -> list[int]:
    roots = []
    for x in range(p):
        acc = 0
        for co in reversed(coeffs):
            acc = (acc * x + co) % p
        if acc == 0:
            roots.append(x)
    return roots


def singular_script(p: int, polys: list[dict], names: list[str]) -> str:
    gens = []
    for d in polys:
        terms = []
        for mon, co in d.items():
            if co == 0:
                continue
            facs = [f"{names[i]}^{e}" if e > 1 else names[i] for i, e in enumerate(mon) if e]
            terms.append(str(co) + ("*" + "*".join(facs) if facs else ""))
        gens.append("+".join(terms) if terms else "0")
    return (f"ring R={p},({','.join(names)}),dp;\noption(redSB);\nideal I=\n" + ",\n".join(gens) + ";\n"
            "int t0=timer;\nideal J=std(I);\n"
            "if(size(J)==1 && deg(J[1])==0){ \"UNIT\"; } else { \"NONUNIT\"; \"DIM=\"+string(dim(J)); }\n"
            "\"SECONDS=\"+string(timer-t0);\nquit;\n")


def run_singular(path: Path, timeout: int = 600) -> str:
    wsl = "/mnt/" + str(path).replace("\\", "/").replace(":", "", 1)
    wsl = wsl[:5] + wsl[5].lower() + wsl[6:]
    try:
        r = subprocess.run(["wsl", "-e", "Singular", "-q", wsl], capture_output=True, text=True, timeout=timeout)
        return r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return "TIMEOUT"


def main() -> int:
    started = time.time()
    F, A, D = LK.our_field(log=log)
    link = LK.case1_link(F, A, D, log=log)
    cas = link["_cascade"]
    compat = [p for _k, p in cas.compat]
    layers = [k for k, _p in cas.compat]
    log(f"our Case 1 compatibility equations: {len(compat)} (layers {layers})")
    first = compat[0]
    by_deg = {m[S_INDEX]: c for m, c in first.d.items()}
    c4, c2 = by_deg[4], by_deg[2]
    gamma = (-c2) / (c4 * 2)
    hcoeffs = [F.m[i] for i in range(F.m.degree() + 1)]
    others = [i for i in range(PARAMS) if i != S_INDEX]
    names = [f"q{i}" for i in others]
    results = []
    p = 1000
    while len([r for r in results if r["kind"] == "branch"]) < 10 and p < 40000:
        p += 1
        if not isprime(p):
            continue
        try:
            hm = [frac_mod(c, p) for c in hcoeffs]
        except ZeroDivisionError:
            continue
        roots = poly_mod_roots(hm, p)
        deriv = [(i * hm[i]) % p for i in range(1, len(hm))]
        simple = [r for r in roots if poly_mod_roots and sum(co * pow(r, i, p) for i, co in enumerate(deriv)) % p]
        if not simple:
            continue
        r = simple[0]
        try:
            g = kel_mod(gamma, r, p)
            reduced = []
            for poly in compat:
                reduced.append({m: kel_mod(c, r, p) for m, c in poly.d.items()})
        except ZeroDivisionError:
            continue
        if g == 0:
            continue
        sq = sqrt_mod(g, p, all_roots=True)
        if not sq:
            continue
        for sign, sval in (("s=+c", sq[0]), ("s=-c", (p - sq[0]) % p)):
            polys = []
            for d in reduced:
                out: dict = {}
                for m, co in d.items():
                    co = co * pow(sval, m[S_INDEX], p) % p
                    if co == 0:
                        continue
                    key = tuple(m[i] for i in others)
                    out[key] = (out.get(key, 0) + co) % p
                out = {k: v for k, v in out.items() if v}
                if out:
                    polys.append(out)
            script = ART / f"addA_p{p}_{'plus' if sign == 's=+c' else 'minus'}.sing"
            script.write_text(singular_script(p, polys, names), encoding="utf-8")
            text = run_singular(script)
            unit = "UNIT" in text.split() and "NONUNIT" not in text
            rec = {"kind": "branch", "p": p, "root": r, "branch": sign, "equations": len(polys),
                   "unit": unit, "singular": text.strip().splitlines()[-2:] if text != "TIMEOUT" else ["TIMEOUT"]}
            results.append(rec)
            log(f"p={p} r={r} {sign}: {len(polys)} equations, unit={unit} ({rec['singular']})")
            script.unlink()
        # control at the first usable prime: upper layers only
        if not any(x["kind"] == "control" for x in results):
            upper = [d for d, k in zip(reduced, layers) if k >= -1]
            polys = []
            for d in upper:
                out = {}
                for m, co in d.items():
                    key = tuple(m[i] for i in others) + (m[S_INDEX],)
                    out[key] = co
                out = {k: v for k, v in out.items() if v}
                if out:
                    polys.append(out)
            script = ART / f"addA_control_p{p}.sing"
            script.write_text(singular_script(p, polys, names + ["s"]), encoding="utf-8")
            text = run_singular(script)
            results.append({"kind": "control", "p": p, "equations": len(polys),
                            "unit": "UNIT" in text.split() and "NONUNIT" not in text,
                            "singular": text.strip().splitlines()[-2:]})
            log(f"control p={p}: upper layers only, {len(polys)} equations: {text.strip().splitlines()[-2:]}")
            script.unlink()
    branches = [r for r in results if r["kind"] == "branch"]
    primes = sorted({r["p"] for r in branches})
    control = next(r for r in results if r["kind"] == "control")
    passed = len(primes) >= 5 and all(r["unit"] for r in branches) and not control["unit"]
    out = {"addendum": "A", "status": "PASS" if passed else "FAIL_OR_INCONCLUSIVE", "primes": primes,
           "branch_tests": branches, "control": control,
           "what_pass_shows": "strong evidence, not a proof, that Case 1 has no solution over the algebraic closure",
           "external_data_used": False, "seconds": round(time.time() - started, 1)}
    (ART / "addendum-a.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    (ART / "addendum-a-log.txt").write_text("\n".join(LOG) + "\n", encoding="utf-8")
    log(f"addendum A: {out['status']} on {len(primes)} primes, control unit={control['unit']}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
