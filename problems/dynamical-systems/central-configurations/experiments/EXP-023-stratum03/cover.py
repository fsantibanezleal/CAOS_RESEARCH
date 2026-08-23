"""EXP-023: certified covering of the (0,3) stratum's bounded region.

COMPACT GAUGE (adopted 2026-08-20 after the ping-pong diagnosis, finding
15): translation v1 = 0, and scale fixed by max(u1, u2, u3, |v2|, |v3|) = 1
rather than by u1 = 1 alone. This chart is the case where the maximum is
attained by u1, so u1 = 1 AND every other coordinate lies in [-1, 1]: the
region is COMPACT and its boundaries are geometric (the maximum switching
to another coordinate) rather than arbitrary truncations. The other four
cases are charts U2, U3, V2, V3.

Free parameters (u2, u3, v2, v3) in [0,1]^2 x [-1,1]^2.

The matrix is 6 x 3, so a rank-3 certificate is FULL rank: the kernel is
trivial and the box contains NO central configuration of the stratum at
all. Where rank 3 cannot be certified, the trap certificate bounds the
rank-2 locus: a 2 x 2 minor nonzero over the box (so rank >= 2 there,
which empties R_1 and R_0) together with two 3 x 3 minors whose gradients
have a nonzero 2 x 2 subdeterminant over the box (so R_2 lies in a smooth
codimension-2 set, dimension 2). Those are exactly the stratum's three
requirements.

Entries are assembled generically from the six positions rather than
hand-transcribed: for each equation L_ij the coefficient of the mass of
pair(k) accumulates (R_ik - R_jk) * Delta_ijk. The construction is
crosschecked against the independent mpmath derivation in derive.py.
"""
import json
import sys
import time
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
E22 = HERE.parent / "EXP-022-collar-coverings"
spec = importlib.util.spec_from_file_location("pipeline", E22 / "pipeline.py")
pl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pl)
IV, DV = pl.IV, pl.DV

PAIR_OF = [0, 0, 1, 1, 2, 2]
ROWS = [(0, 2), (0, 3), (0, 4), (0, 5), (2, 4), (2, 5)]
NAMES = ["L13", "L14", "L15", "L16", "L35", "L36"]
MENU3 = list(combinations(range(6), 3))                    # 20 minors
PAIRS2 = [(r, c) for r in combinations(range(6), 2)
          for c in combinations(range(3), 2)]              # 45 rank-2 witnesses

def dv_inv(x):
    iv = x.v.inv()
    isq = (x.v * x.v).inv()
    return DV(iv, [IV(-1) * isq * g for g in x.g])

def K_inv(x):
    return x.inv() if isinstance(x, IV) else dv_inv(x)

def entry_factory(mode):
    def entries(args):
        if mode == "iv":
            u2, u3, v2, v3 = (IV.raw(*b) for b in args)
            one, Z = IV(1), IV(0)
        else:
            u2, u3, v2, v3 = args
            one, Z = DV(1), DV(0)
        P = [(one, Z), (Z - one, Z),
             (u2, v2), (Z - u2, v2),
             (u3, v3), (Z - u3, v3)]
        # inverse cubes of all pairwise distances
        icu = {}
        for i in range(6):
            for j in range(i + 1, 6):
                dx = P[i][0] - P[j][0]
                dy = P[i][1] - P[j][1]
                d2 = dx.sq() + dy.sq()
                d = d2.sqrt()
                icu[(i, j)] = icu[(j, i)] = K_inv(d * d * d)
        def area2(i, j, k):
            return ((P[j][0] - P[i][0]) * (P[k][1] - P[i][1])
                    - (P[j][1] - P[i][1]) * (P[k][0] - P[i][0]))
        J = []
        for (i, j) in ROWS:
            row = [Z, Z, Z]
            for k in range(6):
                if k == i or k == j:
                    continue
                row[PAIR_OF[k]] = row[PAIR_OF[k]] + \
                    (icu[(i, k)] - icu[(j, k)]) * area2(i, j, k)
            J.append(row)
        return J
    return entries

def det3(J, rows):
    a, b, c = rows
    return (J[a][0] * (J[b][1] * J[c][2] - J[b][2] * J[c][1])
            - J[a][1] * (J[b][0] * J[c][2] - J[b][2] * J[c][0])
            + J[a][2] * (J[b][0] * J[c][1] - J[b][1] * J[c][0]))

def det3d(J, rows):
    return det3(J, rows)

def rank3_plain(J):
    for rows in MENU3:
        try:
            if det3(J, rows).excludes_zero():
                return rows
        except AssertionError:
            continue
    return None

E3 = [[IV(1) if i == j else IV(0) for i in range(4)] for j in range(4)]

def duals(boxes, mids=False):
    if mids:
        return [DV(IV((b[0] + b[1]) / 2), E3[i]) for i, b in enumerate(boxes)]
    return [DV(IV.raw(*b), E3[i]) for i, b in enumerate(boxes)]

def rank3_mv(edv, box):
    rads = [(b[1] - b[0]) / 2 for b in box]
    try:
        Jm = edv(duals(box, mids=True))
        Jb = edv(duals(box))
    except AssertionError:
        return None
    for rows in MENU3:
        try:
            dm = det3d(Jm, rows)
            db = det3d(Jb, rows)
            enc = dm.v
            for i in range(4):
                g = db.g[i]
                mag = max(abs(g.lo), abs(g.hi))
                enc = enc + IV.raw(-mag * rads[i], mag * rads[i])
            if enc.excludes_zero():
                return rows
        except AssertionError:
            continue
    return None

def trap(eiv, edv, box):
    try:
        J = eiv([tuple(b) for b in box])
    except AssertionError:
        return None
    r2 = None
    for r, c in PAIRS2:
        m = J[r[0]][c[0]] * J[r[1]][c[1]] - J[r[0]][c[1]] * J[r[1]][c[0]]
        if m.excludes_zero():
            r2 = {"rows": list(r), "cols": list(c)}
            break
    if r2 is None:
        return None
    try:
        Jb = edv(duals(box))
    except AssertionError:
        return None
    packs = []
    for rows in MENU3:
        try:
            packs.append((rows, det3d(Jb, rows).g))
        except AssertionError:
            continue
    packs.sort(key=lambda pk: -max(max(abs(x.lo), abs(x.hi)) for x in pk[1]))
    top = packs[:20]
    for i in range(len(top)):
        for j in range(i + 1, len(top)):
            gi, gj = top[i][1], top[j][1]
            for a in range(4):
                for b in range(a + 1, 4):
                    sub = gi[a] * gj[b] - gi[b] * gj[a]
                    if sub.excludes_zero():
                        return {"rank2": r2, "minor1": str(top[i][0]),
                                "minor2": str(top[j][0]), "grad_cols": [a, b]}
    return None


def collision_discard(uvs, sixt=F(1, 16)):
    """Shared discard for every compact chart.

    uvs is [(u_lo,u_hi,v_lo,v_hi)] x 3, one entry per pair, in the chart's
    own coordinates. A box is discarded when it lies ENTIRELY inside a
    collision neighbourhood, which is what the face charts own:

      * a pair collapsing onto the axis:  u_i < sixt throughout
      * two pairs merging:                |u_i - u_j| < sixt AND
                                          |v_i - v_j| < sixt throughout

    Containment, not overlap: an overlap test discards whole seeds (a bug
    this campaign hit once already).
    """
    for (ulo, uhi, vlo, vhi) in uvs:
        if uhi < sixt:
            return True
    for a in range(3):
        for b in range(a + 1, 3):
            ua_lo, ua_hi, va_lo, va_hi = uvs[a]
            ub_lo, ub_hi, vb_lo, vb_hi = uvs[b]
            du_hi = ua_hi - ub_lo
            du_lo = ua_lo - ub_hi
            dv_hi = va_hi - vb_lo
            dv_lo = va_lo - vb_hi
            if du_hi < sixt and du_lo > -sixt and dv_hi < sixt and dv_lo > -sixt:
                return True
    return False

SIXT = F(1, 16)
VMAX = F(1)   # compact gauge: max coordinate = 1, so |v| <= 1

def discard(box):
    u2b, u3b, v2b, v3b = box
    # pair collapses (faces closed by pieces 11/12; their own charts later)
    if u2b[1] < SIXT or u3b[1] < SIXT:
        return True
    # pair-pair merges: B+ meets C+ or C-, or B/C meets A
    if (abs(u2b[1] - u3b[0]) < SIXT and abs(v2b[1] - v3b[0]) < SIXT
            and u2b[0] - u3b[1] > -SIXT and v2b[0] - v3b[1] > -SIXT):
        return True
    for ub, vb in ((u2b, v2b), (u3b, v3b)):
        if ub[0] > 1 - SIXT and ub[1] < 1 + SIXT and vb[0] > -SIXT and vb[1] < SIXT:
            return True                    # that pair meets pair A
    return False

def run_cover(name, seed, eiv, edv, disc, budget=43200, resume=False):
    """Shared covering loop for every (0,3) chart."""
    art = HERE / "artifacts"
    art.mkdir(exist_ok=True)
    heavy = Path("E:/_Datos/caos-research/central-configurations/EXP-023")
    heavy.mkdir(parents=True, exist_ok=True)
    ckpt = art / f"{name}-checkpoint.json"
    certs = heavy / f"{name}-certificates.jsonl"
    t0 = time.time()
    if resume and ckpt.exists():
        ck = json.loads(ckpt.read_text(encoding="utf-8"))
        stack = [(pl.dec_box(r), d) for r, d in ck["stack"]]
        cnt = ck["counters"]
    else:
        stack = [(tuple(seed), 0)]
        cnt = {"processed": 0, "certified": 0, "mv_certified": 0,
               "trapped": 0, "discarded": 0, "failed": 0}
        certs.write_text("", encoding="utf-8")
    out = open(certs, "a", encoding="utf-8", buffering=1 << 20)
    last = time.time()
    DEPTH, BUDGET = 60, budget
    while stack:
        if time.time() - t0 > BUDGET:
            print("BUDGET EXHAUSTED", flush=True)
            cnt["failed"] += len(stack)
            break
        box, d = stack.pop()
        cnt["processed"] += 1
        if disc(box):
            cnt["discarded"] += 1
            continue
        got = None
        try:
            got = rank3_plain(eiv([tuple(b) for b in box]))
        except AssertionError:
            pass
        if got is not None:
            cnt["certified"] += 1
            out.write(json.dumps({"box": pl.enc_box(box), "by": str(got)}) + "\n")
            continue
        mw = max(b[1] - b[0] for b in box)
        if mw < F(1, 64):
            got = rank3_mv(edv, box)
            if got is not None:
                cnt["mv_certified"] += 1
                out.write(json.dumps({"box": pl.enc_box(box), "by": "mv" + str(got)}) + "\n")
                continue
        if mw < F(1, 128):
            got = trap(eiv, edv, box)
            if got is not None:
                cnt["trapped"] += 1
                out.write(json.dumps({"box": pl.enc_box(box), "by": got}) + "\n")
                continue
        if d >= DEPTH:
            cnt["failed"] += 1
            out.write(json.dumps({"box": pl.enc_box(box), "by": "FAILED"}) + "\n")
            continue
        widths = [b[1] - b[0] for b in box]
        w = widths.index(max(widths))
        bl = [list(x) for x in box]
        lo, hi = bl[w]
        mid = (lo + hi) / 2
        for half in ((lo, mid), (mid, hi)):
            nb = [tuple(x) for x in bl]
            nb[w] = half
            stack.append((tuple(nb), d + 1))
        if cnt["processed"] % 50000 == 0:
            print(f"[{time.time()-t0:.0f}s] {cnt} stack {len(stack)}", flush=True)
        if time.time() - last > 150:
            out.flush()
            ckpt.write_text(json.dumps(
                {"stack": [[pl.enc_box(b), dd] for b, dd in stack],
                 "counters": cnt}), encoding="utf-8")
            last = time.time()
    out.close()
    ok = cnt["failed"] == 0 and not stack
    (art / f"{name}-summary.json").write_text(json.dumps(
        {"ok": ok, "counters": cnt, "depth_cap": DEPTH,
         "wall_s": round(time.time() - t0)}, indent=1), encoding="utf-8")
    print(f"EXP-023 {name} DONE ok={ok} {cnt}", flush=True)

def main():
    seed = ((F(0), F(1)), (F(0), F(1)), (-VMAX, VMAX), (-VMAX, VMAX))
    run_cover("cover", seed, entry_factory("iv"), entry_factory("dv"),
              discard, resume="--resume" in sys.argv)

if __name__ == "__main__":
    main()
