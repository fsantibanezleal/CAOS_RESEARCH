"""Close band's residue with the TRAP, which band never tried.

band certifies only rank >= 3, by an interval minor or its mean-value
form. At the cross point the rank IS 2, so no rank-3 certificate can
exist there and no amount of bisection will produce one. But the
dimension count does not need rank 3 everywhere; it needs
dim R_2 <= 2. EXP-021 already has the certificate for that, certify_ball:

  * a 2x2 minor interval-nonzero over the box, so rank >= 2 everywhere on
    it and R_1 meets it nowhere; and
  * two 3x3 minors whose gradients have a nonzero 2x2 subdeterminant over
    the box, so R_2 meets the box inside a smooth codimension-2 manifold.

Codimension 2 in a 4-dimensional shape space is dimension 2, which is
exactly the bound. So if this fires on band's residual boxes, the residue
is closed and the covering is complete, WITH a genuine rank-2 point
sitting inside it.
"""
import json
import sys
from fractions import Fraction as F
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
E21 = HERE.parent / "EXP-021-verified-covering"
spec = importlib.util.spec_from_file_location("integ", E21 / "integrated.py")
integ = importlib.util.module_from_spec(spec)
spec.loader.exec_module(integ)

CERTS = Path("E:/_Datos/caos-research/central-configurations/EXP-022"
             "/band-certificates.jsonl")
RESID = Path("E:/_Datos/caos-research/central-configurations/EXP-022"
             "/band-residue-certificates.jsonl")


def failed_boxes(path):
    seen, out = set(), []
    if not path.exists():
        return out
    for line in path.open(encoding="utf-8"):
        if "FAILED" not in line:
            continue
        raw = json.loads(line)["box"]
        key = json.dumps(raw)
        if key in seen:
            continue
        seen.add(key)
        out.append(integ.dec_box(raw))
    return out


def main():
    for tag, path in (("band", CERTS), ("band-residue", RESID)):
        boxes = failed_boxes(path)
        if not boxes:
            print(f"{tag}: no residue on file")
            continue
        print(f"{tag}: {len(boxes)} residual boxes")
        trapped = failed = 0
        witnesses = []
        for b in boxes:
            bl = [tuple(x) for x in b]
            try:
                c = integ.certify_ball(bl)
            except Exception as e:
                c = None
                print(f"   error on a box: {type(e).__name__}: {e}")
            if c is not None:
                trapped += 1
                if len(witnesses) < 3:
                    witnesses.append((bl, c))
            else:
                failed += 1
        print(f"   TRAPPED {trapped}   still open {failed}")
        for bl, c in witnesses:
            print(f"   witness box u={[float(x) for x in bl[0]]} "
                  f"v={[float(x) for x in bl[1]]}")
            print(f"      rank>=2 by minor rows {c['rank2']['rows']} "
                  f"cols {c['rank2']['cols']}, enclosure "
                  f"[{float(F(c['rank2']['enclosure'][0])):.3e}, "
                  f"{float(F(c['rank2']['enclosure'][1])):.3e}]")
            print(f"      R_2 confined by minors {c['minor1']} and "
                  f"{c['minor2']}, gradient subdet cols {c['subdet_cols']}, "
                  f"enclosure [{float(F(c['enclosure'][0])):.3e}, "
                  f"{float(F(c['enclosure'][1])):.3e}]")
        print("")

    print("NEGATIVE CONTROLS: the trap must DECLINE where it should")
    controls = [
        ("box 2^12 times wider in every axis", [
            (F(6309175, 10 ** 7) - F(1, 256), F(6309175, 10 ** 7) + F(1, 256)),
            (F(-1, 256), F(1, 256)),
            (F(14509074, 10 ** 7) - F(1, 256), F(14509074, 10 ** 7) + F(1, 256)),
            (F(-1, 256), F(1, 256))]),
        ("box 2^18 times wider", [
            (F(6309175, 10 ** 7) - F(1, 4), F(6309175, 10 ** 7) + F(1, 4)),
            (F(-1, 4), F(1, 4)),
            (F(14509074, 10 ** 7) - F(1, 4), F(14509074, 10 ** 7) + F(1, 4)),
            (F(-1, 4), F(1, 4))]),
    ]
    for tag, bl in controls:
        try:
            c = integ.certify_ball(bl)
            fired = c is not None
            note = ""
        except AssertionError as e:
            fired = False
            note = f"  (declined: {e})"
        print(f"   {tag}: trap fires = {fired}{note}")


if __name__ == "__main__":
    main()
