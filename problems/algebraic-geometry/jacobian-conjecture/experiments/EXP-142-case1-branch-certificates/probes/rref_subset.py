"""Contingency probe (not a result): which subsets of the row-reduced branch basis are unit mod p?
Greedy: drop the tallest rows first while the ideal stays unit at three primes; also the time and size of a lift on
the minimal subset found, at a prime near 2^31."""
import os
from pathlib import Path as _P
_EXP141 = str(_P(__file__).resolve().parents[2] / "EXP-141-case1-modular-certificate")
_W141 = os.environ["JCB141_WORK"]   # cert.py build output (eqs.json)
_W142 = os.environ.get("JCB142_WORK", "")   # branches.py output (branch_plus/, branch_minus/)
import json
import sys
from pathlib import Path

sys.path.insert(0, _EXP141)
from cert import any_root_mod, fmt_poly, is_prime, lift_script, load_eqs, parse_lift, roots_mod, specialise, wsl, wsl_path  # noqa: E402

W = Path(os.path.join(_W142, "rref_plus"))
names, eqs = load_eqs(W)
dig = json.load(open(W / "eqs.json"))["digits"]


def unit(p, sp, subset):
    s = (f"ring R={p},({','.join(names)}),dp;\noption(redSB);\nideal I=\n" +
         ",\n".join(fmt_poly(sp[i], names) for i in subset) + ";\nideal J=std(I);\n"
         "if(size(J)==1 && deg(J[1])==0){ \"UNIT\"; } else { \"NONUNIT DIM=\"+string(dim(J)); }\nquit;\n")
    f = W / f"u_{p}.sing"
    f.write_text(s, encoding="utf-8", newline="\n")
    return wsl(["Singular", "-q", wsl_path(f)], timeout=900)[1].strip()


keeps = []
for p in (1021, 1031, 1033):
    sp = specialise(eqs, any_root_mod(p), p)
    keep = list(range(len(eqs)))
    print(f"p={p} all rows: {unit(p, sp, keep)}", flush=True)
    for i in sorted(keep, key=lambda i: -dig[i]):
        trial = [j for j in keep if j != i]
        if unit(p, sp, trial) == "UNIT":
            keep = trial
    keeps.append(keep)
    print(f"  minimal unit subset (tallest dropped first): rows {keep}, digits {[dig[i] for i in keep]}", flush=True)
keep = keeps[0]
p = 2 ** 31 - 1
while True:
    p -= 2
    if is_prime(p) and roots_mod(p):
        break
sub = [eqs[i] for i in keep]
s = lift_script(p, names, [specialise(sub, roots_mod(p)[0], p)])
f = W / "lift_sub.sing"
f.write_text(s, encoding="utf-8", newline="\n")
out = wsl(["Singular", "-q", wsl_path(f)], timeout=1800)[1]
per, chk = parse_lift(out, p, 1)
print(f"lift on rows {keep} mod {p}: check {chk}, cofactor terms {len(per[0])}")
