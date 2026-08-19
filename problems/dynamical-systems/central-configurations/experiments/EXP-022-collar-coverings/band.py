"""EXP-022 part (a): certified covering of the band A_band.

A_band = {u, p in [1/4,3], v, q in [-3,3], |f| <= 1/4,
          max(|u-p|, |f|) >= 1/16},  f = v - q.

Nonsingular region (cs >= 1/16), so the EXP-021 machinery applies verbatim:
80-minor menu, plain intervals, mean-value fallback on small boxes,
bisection to depth 44, checkpoint every 150 s, certificates streamed to the
heavy store. Boxes wholly inside {|u-p| < 1/16 and |f| < 1/16} are the
A_tube region: discarded here, covered by part (b). Boxes wholly outside
{|f| <= 1/4} are A_core: discarded here (EXP-021 covers them).
"""
import json, sys, time
from fractions import Fraction as F
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
E21 = HERE.parent / "EXP-021-verified-covering"
ART = HERE / "artifacts"
ART.mkdir(exist_ok=True)
HEAVY = Path("E:/_Datos/caos-research/central-configurations/EXP-022")
HEAVY.mkdir(parents=True, exist_ok=True)

spec = importlib.util.spec_from_file_location("integ", E21 / "integrated.py")
integ = importlib.util.module_from_spec(spec)
spec.loader.exec_module(integ)
r21, mv_which = integ.r21, integ.mv_which

CKPT = ART / "band-checkpoint.json"
CERTS = HEAVY / "band-certificates.jsonl"
DEPTH = 44
MVW = F(1, 64)
BUDGET = 43200
SIXT = F(1, 16)

enc_box, dec_box = integ.enc_box, integ.dec_box

def main():
    resume = "--resume" in sys.argv
    t0 = time.time()
    if resume and CKPT.exists():
        ck = json.loads(CKPT.read_text(encoding="utf-8"))
        stack = [(dec_box(r), d) for r, d in ck["stack"]]
        cnt = ck["counters"]
        print(f"RESUME: stack {len(stack)}, counters {cnt}", flush=True)
    else:
        region = ((F(1, 4), F(3)), (F(-3), F(3)), (F(1, 4), F(3)), (F(-3), F(3)))
        stack = [(region, 0)]
        cnt = {"processed": 0, "certified": 0, "mv_certified": 0,
               "core_discard": 0, "tube_discard": 0, "failed": 0}
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
        # f-range and (u-p)-range of the box
        flo, fhi = vb[0] - qb[1], vb[1] - qb[0]
        tlo, thi = ub[0] - pb[1], ub[1] - pb[0]
        # wholly in A_core (|f| >= 1/4): EXP-021's job
        if flo >= F(1, 4) or fhi <= F(-1, 4):
            cnt["core_discard"] += 1
            continue
        # wholly in A_tube (|u-p| < 1/16 and |f| < 1/16): part (b)'s job
        if (thi < SIXT and tlo > -SIXT) and (fhi < SIXT and flo > -SIXT):
            cnt["tube_discard"] += 1
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
                {"stack": [[enc_box(b), dd] for b, dd in stack],
                 "counters": cnt}), encoding="utf-8")
            last_ck = time.time()
    out.close()
    ok = cnt["failed"] == 0 and not stack
    (ART / "band-summary.json").write_text(json.dumps(
        {"ok": ok, "counters": cnt, "depth_cap": DEPTH,
         "wall_s": round(time.time() - t0)}, indent=1), encoding="utf-8")
    print(f"BAND DONE ok={ok} {cnt}", flush=True)

if __name__ == "__main__":
    main()
