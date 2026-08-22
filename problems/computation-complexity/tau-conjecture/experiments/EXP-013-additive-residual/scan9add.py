"""EXP-013: the ADDITIVE residual at depth 9 (final gate + or -).

Method (design note 2026-08-20, with the overflow fix): evaluate every
operand and every one-gate extension on the window W = [-32, 32] MODULO
two 61-bit primes, vectorized with numpy. f = v8 -+ b vanishes at r only
if v8(r) = -+ b(r) exactly, hence also mod p; so counting modular
agreements never misses a true witness (no false negatives). Candidates
with >= 7 agreements are promoted to EXACT polynomial construction and
exact integer-root counting.

Usage:
  python scan9add.py --gate    (known-answer: threshold 6 on a slice;
                                must find hits)
  python scan9add.py           (production: threshold 7, all partitions)
"""
import argparse, json, pickle, sys, time
from multiprocessing import Pool
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "code"))
T0 = time.time()
ART = HERE / "artifacts"
ASSETS = Path("E:/_Datos/caos-research/tau-conjecture")
FRONTIER = ASSETS / "frontier7"
POLYS = ASSETS / "polys.pkl"
WIDTH = 7
# 31-bit primes: products of residues stay below 2^63 (int64-safe).
P1 = 2147483647             # 2^31 - 1
P2 = 2147483629             # second 31-bit prime
WINDOW = np.arange(-32, 33, dtype=np.int64)


def log(m):
    print(f"[{time.time()-T0:9.1f}s] {m}", flush=True)


def polyvals_mod(poly, xs, p):
    """Horner mod p, exact for integer polys (python ints -> int64)."""
    acc = np.zeros(len(xs), dtype=np.int64)
    for c in reversed(poly):
        acc = (acc * xs + (c % p)) % p
    return acc


def build_pairs(n):
    """Index arrays for all ops over n operands (comm ops i<=j, sub i!=j)."""
    ai, aj, mi, mj, si, sj = [], [], [], [], [], []
    for i in range(n):
        for j in range(i, n):
            ai.append(i); aj.append(j)
            mi.append(i); mj.append(j)
    for i in range(n):
        for j in range(n):
            if i != j:
                si.append(i); sj.append(j)
    return (np.array(ai), np.array(aj), np.array(mi), np.array(mj),
            np.array(si), np.array(sj))


def worker(task):
    part, threshold, ns, rows = task
    out = ART / f"parts_{ns}" / f"part{part:03d}.json"
    if out.exists():
        return part
    sys.path.insert(0, str(HERE.parent.parent / "code"))
    from tclib.enum import integer_roots, padd, pmul, psub
    with open(POLYS, "rb") as fh:
        polys = pickle.load(fh)["polys"]
    f = FRONTIER / f"uniq{part:03d}.bin"
    if not f.exists():
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"part": part, "states": 0, "hits": [],
                                   "hit_count": 0, "promoted": 0}), "utf-8")
        return part
    arr = np.fromfile(f, dtype=np.int32).reshape(-1, WIDTH)
    if rows:
        arr = arr[:rows]
    vcache1, vcache2 = {}, {}

    def vals(i, p, cache):
        v = cache.get(i)
        if v is None:
            v = polyvals_mod(polys[i], WINDOW, p)
            if len(cache) < 400_000:
                cache[i] = v
        return v

    def vals2(i, p, cache):
        return vals(i, p, cache)

    n = 10
    AI, AJ, MI, MJ, SI, SJ = build_pairs(n)
    fns = (padd, pmul, psub)
    hits, promoted = [], 0
    for row in arr:
        ids = (0, 1, 2) + tuple(int(x) for x in row)
        O1 = np.stack([vals(i, P1, vcache1) for i in ids])       # (10,65)
        V1 = np.concatenate([(O1[AI] + O1[AJ]) % P1,
                             (O1[MI] * O1[MJ]) % P1,
                             (O1[SI] - O1[SJ]) % P1])
        nO1 = (-O1) % P1
        # residues are < 2^31, so compare in int32 (halves memory traffic)
        V1c = V1.astype(np.int32)
        O1c = O1.astype(np.int32)
        nO1c = nO1.astype(np.int32)
        eqP = (V1c[:, None, :] == nO1c[None, :, :]).sum(axis=2)
        eqM = (V1c[:, None, :] == O1c[None, :, :]).sum(axis=2)
        # Full-window agreement means f vanishes at all |W| points, so
        # either f is identically zero or deg f >= |W| (rigorous). Only
        # the second case can matter, and it is detectable by degrees.
        dg = np.array([max(len(polys[i]) - 1, 0) for i in ids])
        edg = np.concatenate([np.maximum(dg[AI], dg[AJ]),
                              dg[MI] + dg[MJ],
                              np.maximum(dg[SI], dg[SJ])])
        maxdeg = np.maximum(edg[:, None], dg[None, :])
        interesting = maxdeg >= len(WINDOW)
        okP = (eqP >= threshold) & ((eqP < len(WINDOW)) | interesting)
        okM = (eqM >= threshold) & ((eqM < len(WINDOW)) | interesting)
        cand = np.argwhere(okP | okM)
        if cand.size == 0:
            continue
        # rebuild the candidate extension polynomials exactly
        na, nm = len(AI), len(MI)
        opolys = [polys[i] for i in ids]
        for vi, bi in cand:
            if vi < na:
                t = padd(opolys[AI[vi]], opolys[AJ[vi]])
            elif vi < na + nm:
                k = vi - na
                t = pmul(opolys[MI[k]], opolys[MJ[k]])
            else:
                k = vi - na - nm
                t = psub(opolys[SI[k]], opolys[SJ[k]])
            if not t:
                continue
            b = opolys[bi]
            for f_exact, sign in ((padd(t, b), "+"), (psub(t, b), "-")):
                if not f_exact:
                    continue
                promoted += 1
                R = sorted(integer_roots(f_exact))
                if len(R) >= threshold:
                    hits.append({"state": [int(x) for x in row],
                                 "v8": list(t), "b": list(b),
                                 "sign": sign, "roots": R})
    res = {"part": part, "states": int(arr.shape[0]),
           "hit_count": len(hits), "hits": hits[:20], "promoted": promoted}
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".tmp"); tmp.write_text(json.dumps(res), "utf-8")
    tmp.replace(out)
    return part


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", action="store_true")
    ap.add_argument("--rows", type=int, default=0)
    ap.add_argument("--gthr", type=int, default=5)
    ap.add_argument("--nproc", type=int, default=20)
    a = ap.parse_args()
    if a.gate:
        log(f"known-answer gate: threshold {a.gthr}, partition 0, rows={a.rows}")
        worker((0, a.gthr, "gate", a.rows))
        d = json.loads((ART / "parts_gate" / "part000.json").read_text("utf-8"))
        ok = d["hit_count"] > 0
        log(f"GATE: states={d['states']} promoted={d['promoted']} "
            f"hits={d['hit_count']}: {'PASS' if ok else 'FAIL'}")
        (ART / "gate.json").write_text(json.dumps(d), "utf-8")
        return 0 if ok else 1
    parts = list(range(256))
    done = 0
    with Pool(processes=a.nproc) as pool:
        for _ in pool.imap_unordered(worker, [(p, 7, "final", 0) for p in parts]):
            done += 1
            if done % 16 == 0:
                log(f"  partitions done: {done}/256")
    states = hc = prom = 0
    hits = []
    for p in parts:
        d = json.loads((ART / "parts_final" / f"part{p:03d}.json").read_text("utf-8"))
        states += d["states"]; hc += d["hit_count"]; prom += d["promoted"]
        hits.extend(d["hits"])
    log(f"SCAN9ADD: states={states} promoted={prom} hits(z>=7)={hc}")
    (ART / "final.json").write_text(json.dumps(
        {"states": states, "promoted": prom, "hit_count": hc,
         "hits": hits[:50]}), "utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
