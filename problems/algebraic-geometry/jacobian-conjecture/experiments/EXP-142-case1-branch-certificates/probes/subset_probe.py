"""Contingency probe for EXP-141 (not a result): which subsets of the 13 equations already give the unit ideal mod p.

At three primes with a root of P, specialise E''_e (cert.py helpers), then ask Singular std for leave-one-out
subsets and a greedy minimal unit subset (drop the heaviest equations first). Prints the subsets found.
"""
import os
from pathlib import Path as _P
_EXP141 = str(_P(__file__).resolve().parents[2] / "EXP-141-case1-modular-certificate")
_W141 = os.environ["JCB141_WORK"]   # cert.py build output (eqs.json)
_W142 = os.environ.get("JCB142_WORK", "")   # branches.py output (branch_plus/, branch_minus/)
import json
import sys
from pathlib import Path

sys.path.insert(0, _EXP141)
from cert import any_root_mod, fmt_poly, load_eqs, specialise, wsl, wsl_path  # noqa: E402

W = Path(os.path.join(_W141, "..", "probe"))
W.mkdir(parents=True, exist_ok=True)
names, eqs = load_eqs(_W141)
digits = [max(len(str(abs(c))) for _, cs in e for c in cs) for e in eqs]


def unit(p, sp, subset):
    s = (f"ring R={p},({','.join(names)}),dp;\noption(redSB);\nideal I=\n" +
         ",\n".join(fmt_poly(sp[i], names) for i in subset) + ";\nideal J=std(I);\n"
         "if(size(J)==1 && deg(J[1])==0){ \"UNIT\"; } else { \"NONUNIT DIM=\"+string(dim(J)); }\nquit;\n")
    f = W / f"s_{p}.sing"
    f.write_text(s, encoding="utf-8", newline="\n")
    code, out, err = wsl(["Singular", "-q", wsl_path(f)], timeout=600)
    return out.strip()


for p in (1021, 1031, 1033):
    r = any_root_mod(p)
    sp = specialise(eqs, r, p)
    full = list(range(13))
    print(f"p={p} root={r} full: {unit(p, sp, full)}", flush=True)
    loo = {i + 1: unit(p, sp, [j for j in full if j != i]) for i in full}
    print("  leave-one-out (equation dropped: result):", loo, flush=True)
    order = sorted(full, key=lambda i: -digits[i])
    keep = list(full)
    for i in order:
        trial = [j for j in keep if j != i]
        if unit(p, sp, trial) == "UNIT":
            keep = trial
    print(f"  greedy minimal unit subset (heaviest dropped first): {[i + 1 for i in keep]}, "
          f"max digits {max(digits[i] for i in keep)}", flush=True)
print("digits per equation:", digits)
