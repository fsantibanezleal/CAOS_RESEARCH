"""Contingency probe (not a result): dimension and degree (vdim) mod p of the minimal unit subset of the reduced
branch basis with one row removed, at p = 1021."""
import os
from pathlib import Path as _P
_EXP141 = str(_P(__file__).resolve().parents[2] / "EXP-141-case1-modular-certificate")
_W141 = os.environ["JCB141_WORK"]   # cert.py build output (eqs.json)
_W142 = os.environ.get("JCB142_WORK", "")   # branches.py output (branch_plus/, branch_minus/)
import sys
from pathlib import Path

sys.path.insert(0, _EXP141)
from cert import any_root_mod, fmt_poly, load_eqs, specialise, wsl, wsl_path  # noqa: E402

W = Path(os.path.join(_W142, "rref_plus"))
names, eqs = load_eqs(W)
p = 1021
sp = specialise(eqs, any_root_mod(p), p)
base = [1, 3, 4, 5, 6, 7]
for drop in base:
    sub = [i for i in base if i != drop]
    s = (f"ring R={p},({','.join(names)}),dp;\noption(redSB);\nideal I=\n" +
         ",\n".join(fmt_poly(sp[i], names) for i in sub) + ";\nideal J=std(I);\n"
         "\"dim=\"+string(dim(J))+\" vdim=\"+string(vdim(J));\nquit;\n")
    f = W / "d.sing"
    f.write_text(s, encoding="utf-8", newline="\n")
    out = wsl(["Singular", "-q", wsl_path(f)], timeout=900)[1].strip()
    print(f"drop row {drop} (keep {sub}): {out}", flush=True)
