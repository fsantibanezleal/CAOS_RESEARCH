"""EXP-021 integrated rerun: ONE pipeline, ONE certificate artifact.

Per hypothesis-addendum-integrated.md (committed before this run):
  - four dyadic exclusion balls around the pentagon copies, each carrying a
    dual-interval gradient-pair certificate (rank<=2 locus inside a smooth
    2-manifold on the whole ball, explicit radius, no IFT);
  - every other box certified rank >= 3 by the 80-minor menu, plain
    intervals first, mean-value form when the box is small, bisection to
    depth 44; zero residual failures required;
  - checkpoint every 150 s, resumable with --resume; certificates streamed
    to the heavy store as jsonl.
"""
import json, math, sys, time
from fractions import Fraction as F
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
ART = HERE / "artifacts"
HEAVY = Path("E:/_Datos/caos-research/central-configurations/EXP-021")
HEAVY.mkdir(parents=True, exist_ok=True)

def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

p3 = load("phase3")
r21 = p3.r21          # phase3 already loaded run.py; reuse the SAME classes
IV, MENU, det3 = r21.IV, r21.MENU, r21.det3
DV, det3d = p3.DV, p3.det3d

# ---------- the four pentagon copies, enclosed to 2^-20 ----------
K = 1 << 20
def dy(fr):
    return F(round(fr * K), K)

def sqrt_dy(fr):
    """Dyadic approximation of sqrt(fr) to the 2^-20 grid (fr a Fraction)."""
    n = math.isqrt((fr.numerator * K * K) // fr.denominator)
    return F(n, K)

S5 = sqrt_dy(F(5))                       # ~ sqrt(5)
US = sqrt_dy((5 + S5) / 2)               # u* = sqrt((5+sqrt5)/2) = 2 sin 72
PS = sqrt_dy((5 - S5) / 2)               # p* = sqrt((5-sqrt5)/2) = 2 sin 36
VS = dy((-3 + S5) / 2)                   # v*
QS = dy((-3 - S5) / 2)                   # q*
P0 = (US, VS, PS, QS)
COPIES = [P0,
          (US, -VS, PS, -QS),            # mirror
          (PS, QS, US, VS),              # pair swap
          (PS, -QS, US, -VS)]            # mirror of swap
RAD = F(1, 256)                          # 2^-8 per axis

def ball(center):
    return tuple((c - RAD, c + RAD) for c in center)

BALLS = [ball(c) for c in COPIES]

def inside(box, bl):
    return all(b[0] >= s[0] and b[1] <= s[1] for b, s in zip(box, bl))

# ---------- ball certificates: gradient pair independent over the ball ----------
def grad_pack(boxes):
    E = [[IV(1) if i == j else IV(0) for i in range(4)] for j in range(4)]
    duals = [DV(IV.raw(*b), E[i]) for i, b in enumerate(boxes)]
    J = p3.entry_matrix_dual(*duals)
    out = []
    for rows, cols in MENU:
        try:
            d = det3d(J, rows, cols)
            out.append(((rows, cols), d.g))
        except AssertionError:
            out.append(((rows, cols), None))
    return out

def rank2_ball(bl):
    """A 2x2 minor of J interval-nonzero over the whole ball: rank >= 2
    everywhere on the ball, hence R_1 meet ball is EMPTY (ladder level j=1)."""
    from itertools import combinations
    J = r21.entry_matrix(*[tuple(b) for b in bl])
    for r in combinations(range(6), 2):
        for c in combinations(range(4), 2):
            m = J[r[0]][c[0]] * J[r[1]][c[1]] - J[r[0]][c[1]] * J[r[1]][c[0]]
            if m.excludes_zero():
                return {"rows": list(r), "cols": list(c),
                        "enclosure": [str(m.lo), str(m.hi)]}
    return None

def certify_ball(bl):
    r2 = rank2_ball(bl)
    if r2 is None:
        return None
    packs = [pk for pk in grad_pack(list(bl)) if pk[1] is not None]
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
                        return {"minor1": str(top[i][0]), "minor2": str(top[j][0]),
                                "subdet_cols": [a, b],
                                "enclosure": [str(sub.lo), str(sub.hi)],
                                "rank2": r2}
    return None

# ---------- mean-value certification returning the minor ----------
def mv_which(ub, vb, pb, qb):
    E = [[IV(1) if i == j else IV(0) for i in range(4)] for j in range(4)]
    mids = [(b[0] + b[1]) / 2 for b in (ub, vb, pb, qb)]
    rads = [(b[1] - b[0]) / 2 for b in (ub, vb, pb, qb)]
    try:
        Jm = p3.entry_matrix_dual(*[DV(IV(m), E[i]) for i, m in enumerate(mids)])
        Jb = p3.entry_matrix_dual(*[DV(IV.raw(*b), E[i])
                                    for i, b in enumerate((ub, vb, pb, qb))])
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

# ---------- the integrated covering ----------
CKPT = ART / "integrated-checkpoint.json"
CERTS = HEAVY / "integrated-certificates.jsonl"
DEPTH = 44
MVW = F(1, 64)          # try mean-value only below this width
BUDGET = 43200          # declared 12 h

def enc_box(b):
    return [[str(x) for x in ax] for ax in b]

def dec_box(r):
    return tuple(tuple(F(x) for x in ax) for ax in r)

def main():
    resume = "--resume" in sys.argv
    t0 = time.time()
    if resume and CKPT.exists():
        ck = json.loads(CKPT.read_text(encoding="utf-8"))
        stack = [(dec_box(r), d) for r, d in ck["stack"]]
        cnt = ck["counters"]
        ball_certs = ck["ball_certs"]
        print(f"RESUME: stack {len(stack)}, counters {cnt}", flush=True)
    else:
        ball_certs = []
        for i, bl in enumerate(BALLS):
            got = certify_ball(bl)
            if got is None:
                print(f"BALL {i} CERTIFICATE FAILED at radius {RAD}")
                json.dump({"failed_ball": i}, open(ART / "integrated-summary.json",
                          "w", encoding="utf-8"))
                return
            got["ball"] = i
            got["center"] = [str(c) for c in COPIES[i]]
            got["radius"] = str(RAD)
            ball_certs.append(got)
            print(f"ball {i} certified: {got['minor1']} + {got['minor2']} "
                  f"cols {got['subdet_cols']}", flush=True)
        core = ((F(1, 4), F(3)), (F(-3), F(3)), (F(1, 4), F(3)), (F(-3), F(3)))
        stack = [(core, 0)]
        cnt = {"processed": 0, "certified": 0, "mv_certified": 0,
               "discarded": 0, "ball_covered": 0, "failed": 0}
        CERTS.write_text("", encoding="utf-8")
    out = open(CERTS, "a", encoding="utf-8", buffering=1 << 20)
    last_ck = time.time()
    while stack:
        if time.time() - t0 > BUDGET:
            print("BUDGET EXHAUSTED: run FAILS per declaration", flush=True)
            cnt["failed"] += len(stack)
            break
        box, d = stack.pop()
        cnt["processed"] += 1
        ub, vb, pb, qb = box
        if qb[1] - vb[0] < F(1, 4) and qb[0] - vb[1] > F(-1, 4):
            cnt["discarded"] += 1
            continue
        hit = next((i for i, bl in enumerate(BALLS) if inside(box, bl)), None)
        if hit is not None:
            cnt["ball_covered"] += 1
            out.write(json.dumps({"box": enc_box(box), "by": f"ball{hit}"}) + "\n")
            continue
        got = r21.any_minor_certifies(ub, vb, pb, qb)
        if got is not None:
            cnt["certified"] += 1
            out.write(json.dumps({"box": enc_box(box), "by": str(got)}) + "\n")
            continue
        if max(b[1] - b[0] for b in box) < MVW:
            got = mv_which(ub, vb, pb, qb)
            if got is not None:
                cnt["mv_certified"] += 1
                out.write(json.dumps({"box": enc_box(box), "by": "mv" + str(got)}) + "\n")
                continue
        if d >= DEPTH:
            cnt["failed"] += 1
            out.write(json.dumps({"box": enc_box(box), "by": "FAILED"}) + "\n")
            continue
        widths = [b[1] - b[0] for b in box]
        w = widths.index(max(widths))
        bl2 = [list(x) for x in box]
        lo, hi = bl2[w]
        mid = (lo + hi) / 2
        for half in ((lo, mid), (mid, hi)):
            nb = [tuple(x) for x in bl2]
            nb[w] = half
            stack.append((tuple(nb), d + 1))
        if cnt["processed"] % 50000 == 0:
            print(f"[{time.time()-t0:.0f}s] {cnt} stack {len(stack)}", flush=True)
        if time.time() - last_ck > 150:
            out.flush()
            CKPT.write_text(json.dumps(
                {"stack": [[enc_box(b), d] for b, d in stack],
                 "counters": cnt, "ball_certs": ball_certs}), encoding="utf-8")
            last_ck = time.time()
    out.close()
    ok = cnt["failed"] == 0 and not stack
    summary = {"ok": ok, "counters": cnt, "ball_certs": ball_certs,
               "depth_cap": DEPTH, "radius": str(RAD),
               "wall_s": round(time.time() - t0)}
    (ART / "integrated-summary.json").write_text(json.dumps(summary, indent=1),
                                                 encoding="utf-8")
    print(f"INTEGRATED DONE ok={ok} {cnt}", flush=True)

if __name__ == "__main__":
    main()
