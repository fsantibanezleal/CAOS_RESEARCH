"""EXP-022 shared covering pipeline (any chart, any rescaled matrix).

Three certificate types per box, tried in order:
  1. rank >= 3: some 3x3 minor of the 6x4 chart matrix excludes zero
     (plain intervals; mean-value form when the box is small). The box
     contributes NOTHING to R_2 and nothing to R_1.
  2. trap: a 2x2 minor excludes zero over the box (rank >= 2 everywhere,
     so R_1 meet box is EMPTY) AND two 3x3 minors have gradients with a
     2x2 interval subdeterminant excluding zero over the box (their common
     zero set is a smooth codim-2 manifold containing R_2 meet box). The
     box contributes at most a 2-dimensional piece to R_2.
  3. bisect (up to a depth cap; residual failures fail the run).

This yields dim(R_2 meet region) <= 2 and R_1 meet region = EMPTY, the
full ladder for the k = 3 chain step, in one uniform certificate list.
Chart matrices are supplied by the caller as entry builders over IV / DV;
row/column rescalings by nonzero factors (done inside the builders) do not
change ranks at interior points.
"""
import json, time
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import importlib.util

E21 = Path(__file__).resolve().parent.parent / "EXP-021-verified-covering"

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

p3 = _load("phase3", E21 / "phase3.py")
r21 = p3.r21
IV, DV, det3, det3d, MENU = r21.IV, p3.DV, r21.det3, p3.det3d, r21.MENU
PAIRS2 = [(r, c) for r in combinations(range(6), 2) for c in combinations(range(4), 2)]

def _dual_args(boxes, mids=False):
    E = [[IV(1) if i == j else IV(0) for i in range(4)] for j in range(4)]
    if mids:
        return [DV(IV((b[0] + b[1]) / 2), E[i]) for i, b in enumerate(boxes)]
    return [DV(IV.raw(*b), E[i]) for i, b in enumerate(boxes)]

def rank3_plain(J):
    for rows, cols in MENU:
        try:
            if det3(J, rows, cols).excludes_zero():
                return (rows, cols)
        except AssertionError:
            continue
    return None

def rank3_mv(entry_dv, boxes):
    rads = [(b[1] - b[0]) / 2 for b in boxes]
    try:
        Jm = entry_dv(_dual_args(boxes, mids=True))
        Jb = entry_dv(_dual_args(boxes))
    except AssertionError:
        return None
    for rows, cols in MENU:
        try:
            dm = det3d(Jm, rows, cols)
            db = det3d(Jb, rows, cols)
            enc = dm.v
            for i in range(4):
                gi = db.g[i]
                mag = max(abs(gi.lo), abs(gi.hi))
                enc = enc + IV.raw(-mag * rads[i], mag * rads[i])
            if enc.excludes_zero():
                return (rows, cols)
        except AssertionError:
            continue
    return None

def trap(entry_iv, entry_dv, boxes):
    try:
        J = entry_iv([tuple(b) for b in boxes])
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
        Jb = entry_dv(_dual_args(boxes))
    except AssertionError:
        return None
    packs = []
    for rows, cols in MENU:
        try:
            d = det3d(Jb, rows, cols)
            packs.append(((rows, cols), d.g))
        except AssertionError:
            continue
    def norm(g):
        return max(max(abs(x.lo), abs(x.hi)) for x in g)
    packs.sort(key=lambda pk: -norm(pk[1]))
    top = packs[:25]
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

def enc_box(b):
    return [[str(x) for x in ax] for ax in b]

def dec_box(r):
    return tuple(tuple(F(x) for x in ax) for ax in r)

def run_covering(name, seed, entry_iv, entry_dv, art_dir, heavy_dir,
                 discard=None, depth=44, mvw=F(1, 64), trapw=F(1, 128),
                 budget=43200, resume=False):
    """seed: list of 4-tuples of (lo,hi) Fraction pairs."""
    art_dir = Path(art_dir); art_dir.mkdir(parents=True, exist_ok=True)
    heavy_dir = Path(heavy_dir); heavy_dir.mkdir(parents=True, exist_ok=True)
    ckpt = art_dir / f"{name}-checkpoint.json"
    certs = heavy_dir / f"{name}-certificates.jsonl"
    t0 = time.time()
    if resume and ckpt.exists():
        ck = json.loads(ckpt.read_text(encoding="utf-8"))
        stack = [(dec_box(r), d) for r, d in ck["stack"]]
        cnt = ck["counters"]
        print(f"RESUME {name}: stack {len(stack)} {cnt}", flush=True)
    else:
        stack = [(tuple(b), 0) for b in seed]
        cnt = {"processed": 0, "certified": 0, "mv_certified": 0,
               "trapped": 0, "discarded": 0, "failed": 0}
        certs.write_text("", encoding="utf-8")
    out = open(certs, "a", encoding="utf-8", buffering=1 << 20)
    last_ck = time.time()
    while stack:
        if time.time() - t0 > budget:
            print(f"{name}: BUDGET EXHAUSTED, run FAILS", flush=True)
            cnt["failed"] += len(stack)
            break
        box, d = stack.pop()
        cnt["processed"] += 1
        if discard is not None and discard(box):
            cnt["discarded"] += 1
            continue
        try:
            J = entry_iv([tuple(b) for b in box])
            got = rank3_plain(J)
        except AssertionError:
            got = None
        if got is not None:
            cnt["certified"] += 1
            out.write(json.dumps({"box": enc_box(box), "by": str(got)}) + "\n")
            continue
        mw = max(b[1] - b[0] for b in box)
        if mw < mvw:
            got = rank3_mv(entry_dv, box)
            if got is not None:
                cnt["mv_certified"] += 1
                out.write(json.dumps({"box": enc_box(box), "by": "mv" + str(got)}) + "\n")
                continue
        if mw < trapw:
            got = trap(entry_iv, entry_dv, box)
            if got is not None:
                cnt["trapped"] += 1
                out.write(json.dumps({"box": enc_box(box), "by": got}) + "\n")
                continue
        if d >= depth:
            cnt["failed"] += 1
            out.write(json.dumps({"box": enc_box(box), "by": "FAILED"}) + "\n")
            continue
        widths = [b[1] - b[0] for b in box]
        wi = widths.index(max(widths))
        bl = [list(x) for x in box]
        lo, hi = bl[wi]
        mid = (lo + hi) / 2
        for half in ((lo, mid), (mid, hi)):
            nb = [tuple(x) for x in bl]
            nb[wi] = half
            stack.append((tuple(nb), d + 1))
        if cnt["processed"] % 50000 == 0:
            print(f"[{name} {time.time()-t0:.0f}s] {cnt} stack {len(stack)}", flush=True)
        if time.time() - last_ck > 150:
            out.flush()
            ckpt.write_text(json.dumps(
                {"stack": [[enc_box(b), dd] for b, dd in stack],
                 "counters": cnt}), encoding="utf-8")
            last_ck = time.time()
    out.close()
    ok = cnt["failed"] == 0 and not stack
    summary = {"ok": ok, "counters": cnt, "depth_cap": depth,
               "wall_s": round(time.time() - t0)}
    (art_dir / f"{name}-summary.json").write_text(
        json.dumps(summary, indent=1), encoding="utf-8")
    print(f"{name} DONE ok={ok} {cnt}", flush=True)
    return summary
