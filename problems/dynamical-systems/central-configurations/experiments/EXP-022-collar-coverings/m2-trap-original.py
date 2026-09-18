"""Close m2's residue with the trap, in the ORIGINAL coordinates.

m2's own covering already tries pipeline's trap (its boxes are far below
the trap width), and it fails there. But that trap runs in m2's blown-up
chart, where the entries carry the corner's rescalings. The residue's
configurations are not actually singular: mapping a residual box back
gives u and p around 1e-4, small but nonzero, with the pairs at heights
near 2.95 and the axis bodies at +-1. So the ORIGINAL matrix is defined,
and EXP-021's certify_ball may fire where the chart's own trap does not.

That is exactly what happened with band, whose residue closed instantly
once the trap was applied in the original coordinates.

Map, from m2chart.py's docstring:
    ct, st  = (1 - tt^2, 2 tt)/(1 + tt^2)
    alpha   = sgn (1 - tau^2)/(1 + tau^2),   beta = 2 tau/(1 + tau^2)
    uh, ph  = (ct +- st alpha)/2
    u = Rc uh,  p = Rc ph,  f = Rc st beta,  q = v - f
"""
import json
from fractions import Fraction as F
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
E21 = HERE.parent / "EXP-021-verified-covering"
_s = importlib.util.spec_from_file_location("integ", E21 / "integrated.py")
integ = importlib.util.module_from_spec(_s)
_s.loader.exec_module(integ)
_p = importlib.util.spec_from_file_location("pipeline", HERE / "pipeline.py")
pl = importlib.util.module_from_spec(_p)
_p.loader.exec_module(pl)
IV = pl.IV

HEAVY = Path("E:/_Datos/caos-research/central-configurations/EXP-022")


def failed(path, cap=None):
    seen, out = set(), []
    for line in path.open(encoding="utf-8"):
        if "FAILED" not in line:
            continue
        raw = json.loads(line)["box"]
        k = json.dumps(raw)
        if k in seen:
            continue
        seen.add(k)
        out.append(tuple(tuple(F(x) for x in ax) for ax in raw))
        if cap and len(out) >= cap:
            break
    return out


def to_original(box, sgn):
    Rcb, ttb, vb, taub = box
    Rc, tt, tau = IV.raw(*Rcb), IV.raw(*ttb), IV.raw(*taub)
    v = IV.raw(*vb)
    one, two = IV(1), IV(2)
    iot = (one + tt.sq()).inv()
    ct, st = (one - tt.sq()) * iot, two * tt * iot
    iop = (one + tau.sq()).inv()
    alpha = (one - tau.sq()) * iop
    if sgn < 0:
        alpha = IV(0) - alpha
    beta = two * tau * iop
    half = F(1, 2)
    u = Rc * ((ct + st * alpha) * half)
    p = Rc * ((ct - st * alpha) * half)
    q = v - Rc * st * beta
    return [(u.lo, u.hi), (v.lo, v.hi), (p.lo, p.hi), (q.lo, q.hi)]


for tag, sgn in (("m2-L", -1), ("m2-R", 1)):
    path = HEAVY / f"{tag}-certificates.jsonl"
    if not path.exists():
        print(f"{tag}: no certificates")
        continue
    boxes = failed(path, cap=4000)
    trapped = open_ = errored = 0
    witness = None
    widths = []
    for b in boxes:
        bl = to_original(b, sgn)
        widths.append(max(float(x[1] - x[0]) for x in bl))
        try:
            c = integ.certify_ball(bl)
        except AssertionError:
            errored += 1
            continue
        except Exception:
            errored += 1
            continue
        if c is not None:
            trapped += 1
            if witness is None:
                witness = (bl, c)
        else:
            open_ += 1
    print(f"{tag}: {len(boxes)} residual boxes (capped), mapped to "
          "original coordinates")
    print(f"   TRAPPED {trapped}   open {open_}   not evaluable {errored}")
    if widths:
        print(f"   original-box widths: max {max(widths):.3e}, "
              f"min {min(widths):.3e}")
    if witness:
        bl, c = witness
        print(f"   witness u={[float(x) for x in bl[0]]} "
              f"p={[float(x) for x in bl[2]]}")
        print(f"      v={[float(x) for x in bl[1]]} "
              f"q={[float(x) for x in bl[3]]}")
        print(f"      rank>=2 minor rows {c['rank2']['rows']} "
              f"cols {c['rank2']['cols']}")
        print(f"      R_2 confined, gradient subdet enclosure "
              f"[{float(F(c['enclosure'][0])):.3e}, "
              f"{float(F(c['enclosure'][1])):.3e}]")
    print("")
