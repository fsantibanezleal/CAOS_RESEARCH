"""EXP-013 batched engine: same mathematics, states processed in batches.

Motivation: the per-state engine was numpy-overhead bound (~700 states/s).
Batching B states into single tensor operations amortizes that overhead.
The mathematics, the filter, the rigorous zero-exclusion and the exact
promotion are IDENTICAL to scan9add.py.

Validation: --regress P1 P2 ... re-runs already-completed partitions and
requires an EXACT match of states, hit_count and promoted against the
results the per-state engine wrote.

Usage:
  python scan9add_fast.py --regress 0 1 2
  python scan9add_fast.py --nproc 20
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
P1 = 2147483647
WINDOW = np.arange(-32, 33, dtype=np.int64)
NW = len(WINDOW)
BATCH = 48


def log(m):
    print(f"[{time.time()-T0:9.1f}s] {m}", flush=True)


def polyvals_mod(poly, p):
    acc = np.zeros(NW, dtype=np.int64)
    for c in reversed(poly):
        acc = (acc * WINDOW + (c % p)) % p
    return acc


def build_pairs(n):
    ai, aj, si, sj = [], [], [], []
    for i in range(n):
        for j in range(i, n):
            ai.append(i); aj.append(j)
    for i in range(n):
        for j in range(n):
            if i != j:
                si.append(i); sj.append(j)
    return (np.array(ai), np.array(aj), np.array(si), np.array(sj))


def worker(task):
    part, threshold, ns = task
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
    AI, AJ, SI, SJ = build_pairs(10)
    nA, nS = len(AI), len(SI)
    vcache = {}
    hits, promoted = [], 0
    inputs = np.array([0, 1, 2], dtype=np.int32)

    for start in range(0, arr.shape[0], BATCH):
        rows = arr[start:start + BATCH]
        B = rows.shape[0]
        ids = np.concatenate([np.tile(inputs, (B, 1)), rows], axis=1)  # (B,10)
        uniq, inv = np.unique(ids, return_inverse=True)
        tbl = np.empty((len(uniq), NW), dtype=np.int64)
        for k, pid in enumerate(uniq):
            v = vcache.get(int(pid))
            if v is None:
                v = polyvals_mod(polys[int(pid)], P1)
                if len(vcache) < 300_000:
                    vcache[int(pid)] = v
            tbl[k] = v
        O = tbl[inv].reshape(B, 10, NW)                       # (B,10,65)
        V = np.concatenate([(O[:, AI] + O[:, AJ]) % P1,
                            (O[:, AI] * O[:, AJ]) % P1,
                            (O[:, SI] - O[:, SJ]) % P1], axis=1)
        nO = (-O) % P1
        Vc = V.astype(np.int32); Oc = O.astype(np.int32)
        nOc = nO.astype(np.int32)
        eqP = (Vc[:, :, None, :] == nOc[:, None, :, :]).sum(axis=3)
        eqM = (Vc[:, :, None, :] == Oc[:, None, :, :]).sum(axis=3)
        dg = np.array([[max(len(polys[int(i)]) - 1, 0) for i in row]
                       for row in ids])                       # (B,10)
        edg = np.concatenate([np.maximum(dg[:, AI], dg[:, AJ]),
                              dg[:, AI] + dg[:, AJ],
                              np.maximum(dg[:, SI], dg[:, SJ])], axis=1)
        interesting = np.maximum(edg[:, :, None], dg[:, None, :]) >= NW
        okP = (eqP >= threshold) & ((eqP < NW) | interesting)
        okM = (eqM >= threshold) & ((eqM < NW) | interesting)
        cand = np.argwhere(okP | okM)
        for bi_, vi, oi in cand:
            row_ids = ids[bi_]
            opolys = [polys[int(i)] for i in row_ids]
            if vi < nA:
                t = padd(opolys[AI[vi]], opolys[AJ[vi]])
            elif vi < 2 * nA:
                k = vi - nA
                t = pmul(opolys[AI[k]], opolys[AJ[k]])
            else:
                k = vi - 2 * nA
                t = psub(opolys[SI[k]], opolys[SJ[k]])
            if not t:
                continue
            b = opolys[oi]
            for f_exact, sign in ((padd(t, b), "+"), (psub(t, b), "-")):
                if not f_exact:
                    continue
                promoted += 1
                R = sorted(integer_roots(f_exact))
                if len(R) >= threshold:
                    hits.append({"state": [int(x) for x in rows[bi_]],
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
    ap.add_argument("--regress", type=int, nargs="*")
    ap.add_argument("--nproc", type=int, default=20)
    a = ap.parse_args()
    if a.regress:
        ok = True
        for p in a.regress:
            ref = json.loads((ART / "parts_final" / f"part{p:03d}.json").read_text("utf-8"))
            t0 = time.time()
            worker((p, 7, "regress"))
            new = json.loads((ART / "parts_regress" / f"part{p:03d}.json").read_text("utf-8"))
            same = (ref["states"] == new["states"] and
                    ref["hit_count"] == new["hit_count"] and
                    ref["promoted"] == new["promoted"])
            ok &= same
            log(f"part {p}: ref(states={ref['states']}, hits={ref['hit_count']}, "
                f"prom={ref['promoted']}) new(states={new['states']}, "
                f"hits={new['hit_count']}, prom={new['promoted']}) "
                f"{'MATCH' if same else 'MISMATCH'} in {time.time()-t0:.0f}s")
        log("REGRESSION: " + ("PASS" if ok else "FAIL"))
        return 0 if ok else 1
    parts = list(range(256))
    done = 0
    with Pool(processes=a.nproc) as pool:
        for _ in pool.imap_unordered(worker, [(p, 7, "final") for p in parts]):
            done += 1
            if done % 16 == 0:
                log(f"  partitions done: {done}/256")
    states = hc = prom = 0; hits = []
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
