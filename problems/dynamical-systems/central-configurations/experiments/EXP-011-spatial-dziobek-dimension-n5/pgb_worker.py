"""EXP-011 partial-GB worker (CCB-037, Dias-Pan Lemma 7.5 pattern).

Reads a JSON job file: {"gens": [names], "eqs": [expr strings], "order": "grevlex"}.
Computes the reduced Groebner basis of the subideal and prints the leading
monomials as exponent tuples (JSON). The CALLER enforces the wall-clock cap by
running this in a subprocess; leading monomials of ANY subideal are members of
the full ideal's leading-term ideal, so their union is a valid dimension bound
(their Lemma 6.4: more leading terms only tighten, fewer only weaken).
"""
import json
import sys

import sympy as sp


def main():
    job = json.loads(open(sys.argv[1], encoding="utf-8").read())
    gens = [sp.Symbol(g) for g in job["gens"]]
    local = {g: s for g, s in zip(job["gens"], gens)}
    eqs = [sp.sympify(e, locals=local) for e in job["eqs"]]
    gb = sp.groebner(eqs, *gens, order=job.get("order", "grevlex"))
    leads = [list(p.monoms()[0]) for p in gb.polys]
    print(json.dumps({"gb_size": len(gb.polys), "leads": leads}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
