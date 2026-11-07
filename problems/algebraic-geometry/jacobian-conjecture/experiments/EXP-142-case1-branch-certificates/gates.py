"""EXP-142 gate 2: each branch system, specialised at a root of P modulo EXP-140's five gate primes, is the unit
ideal (Singular std). Usage: python gates.py --work <work root with branch_plus/ and branch_minus/>."""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "EXP-141-case1-modular-certificate"))
from cert import GATE_PRIMES, any_root_mod, fmt_poly, load_eqs, specialise, wsl, wsl_path  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    ok = True
    for tag in ("plus", "minus"):
        W = Path(a.work) / f"branch_{tag}"
        names, eqs = load_eqs(W)
        for p in GATE_PRIMES:
            r = any_root_mod(p)
            sp = specialise(eqs, r, p)
            s = (f"ring R={p},({','.join(names)}),dp;\noption(redSB);\nideal I=\n" +
                 ",\n".join(fmt_poly(d, names) for d in sp) + ";\nideal J=std(I);\n"
                 "if(size(J)==1 && deg(J[1])==0){ \"UNIT\"; } else { \"NONUNIT DIM=\"+string(dim(J)); }\nquit;\n")
            f = W / f"gate_{p}.sing"
            f.write_text(s, encoding="utf-8", newline="\n")
            code, out, err = wsl(["Singular", "-q", wsl_path(f)], timeout=600)
            f.unlink()
            res = out.strip()
            ok &= res == "UNIT"
            print(f"branch {tag} p={p} root={r}: {res} {'PASS' if res == 'UNIT' else 'FAIL'}")
    print("GATE 2", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
