"""Does the collapse chart really cover m2's residue? With the real map.

A first attempt compared the two charts' box coordinates directly and
concluded the atlas had a hole. That was wrong: the charts do not share a
parametrisation. m2's box is (Rc, tt, v, tau) and collapse's is
(eps, t, v, q), so the comparison was meaningless and its conclusion is
withdrawn.

The actual relation, from the two docstrings:

  m2:        ct, st = (1 - tt^2, 2 tt)/(1 + tt^2)
             alpha  = sgn (1 - tau^2)/(1 + tau^2),  beta = 2 tau/(1 + tau^2)
             uh = (ct + st alpha)/2,  ph = (ct - st alpha)/2
             u = Rc uh,  p = Rc ph,  f = v - q = Rc st beta

  collapse:  u = eps c,  p = eps s,  (c, s) = (1 - t^2, 2t)/(1 + t^2)
             so eps = sqrt(u^2 + p^2), and t = tan(theta/2) for
             theta = atan2(p, u)

The quantity collapse discards on is cs^2 = eps^2 (c - s)^2 + f^2, and
eps^2 (c - s)^2 = (u - p)^2 = Rc^2 st^2 alpha^2 while f^2 = Rc^2 st^2
beta^2, so with alpha^2 + beta^2 = 1

    cs = Rc * st       EXACTLY.

collapse discards cs < 1/32. m2's residue sits at Rc about 0.056 with
st about 1, so cs is about 0.056, comfortably above 1/32 = 0.03125. The
region should therefore be kept, and this checks it with intervals over
every residual box rather than at a sample point.
"""
import json
from fractions import Fraction as F
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
_s = importlib.util.spec_from_file_location("pipeline", HERE / "pipeline.py")
pl = importlib.util.module_from_spec(_s)
_s.loader.exec_module(pl)
IV = pl.IV

HEAVY = Path("E:/_Datos/caos-research/central-configurations/EXP-022")
SIXT = F(1, 16)


def failed(path):
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
    return out


def image(box, sgn):
    """Interval image of an m2 box: (eps, cs, v, q) in collapse's terms."""
    Rcb, ttb, vb, taub = box
    Rc = IV.raw(*Rcb)
    tt = IV.raw(*ttb)
    tau = IV.raw(*taub)
    v = IV.raw(*vb)
    one, two = IV(1), IV(2)
    iot = (one + tt.sq()).inv()
    ct = (one - tt.sq()) * iot
    st = two * tt * iot
    iop = (one + tau.sq()).inv()
    alpha = (one - tau.sq()) * iop
    if sgn < 0:
        alpha = IV(0) - alpha
    beta = two * tau * iop
    half = F(1, 2)
    uh = (ct + st * alpha) * half
    ph = (ct - st * alpha) * half
    u = Rc * uh
    p = Rc * ph
    eps = (u.sq() + p.sq()).sqrt()
    f = Rc * st * beta
    q = v - f
    cs = Rc * st          # exact, see the docstring
    return eps, cs, v, q, u, p


for tag, sgn in (("m2-L", -1), ("m2-R", 1)):
    path = HEAVY / f"{tag}-certificates.jsonl"
    if not path.exists():
        print(f"{tag}: no certificates on file")
        continue
    boxes = failed(path)
    kept = disc_cs = disc_axis = out_seed = 0
    worst_cs = None
    for b in boxes:
        eps, cs, v, q, u, p = image(b, sgn)
        if cs.hi < F(1, 1024) ** 0 and cs.hi * cs.hi < F(1, 1024):
            disc_cs += 1
            continue
        hit = False
        for xb in ((v.lo, v.hi), (q.lo, q.hi)):
            if xb[0] >= 1 - SIXT and xb[1] <= 1 + SIXT:
                hit = True
            if xb[0] >= -1 - SIXT and xb[1] <= -1 + SIXT:
                hit = True
        if hit:
            disc_axis += 1
            continue
        if not (eps.lo >= 0 and eps.hi <= F(3, 8)
                and v.lo >= -3 and v.hi <= 3
                and q.lo >= -3 and q.hi <= 3):
            out_seed += 1
            continue
        kept += 1
        if worst_cs is None or cs.lo < worst_cs:
            worst_cs = cs.lo
    print(f"{tag}: {len(boxes)} residual boxes, mapped into collapse's chart")
    print(f"   COVERED (inside the seed and kept by the discard): {kept}")
    print(f"   rejected by collapse's cs < 1/32 test: {disc_cs}")
    print(f"   rejected by collapse's axis-body slabs: {disc_axis}")
    print(f"   outside collapse's seed: {out_seed}")
    if worst_cs is not None:
        print(f"   smallest cs over the covered boxes: "
              f"{float(worst_cs):.6f}  (threshold 1/32 = 0.03125)")
    print("")

print("collapse's own state, which the coverage claim rests on")
ck = json.loads((HERE / "artifacts" / "collapse-checkpoint.json")
                .read_text(encoding="utf-8"))
print(f"   {ck['counters']}")
print(f"   stack left: {len(ck['stack'])}")
