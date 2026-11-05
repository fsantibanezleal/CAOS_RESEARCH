"""Precompute, for every interned polynomial, its residues at the 2-adic points mod 2^64,
its residues at the 3-adic points mod 3^20, its degree and its trailing index.

The coefficients are reduced mod the modulus first (exact Python integers), then
evaluated by Horner in numpy (uint64 wraps exactly mod 2^64; the 3-adic Horner
reduces after every step, all products below 2^64). A random subset is re-checked
against tclib.padic.Layer.values, which evaluates with exact Python integers.

Usage: python residues.py <assets dir> [check count]
Writes <assets>/res_val2.npy, res_val3.npy, res_deg.npy, res_tz.npy, and the packed
polynomial store polys_blob.bin + polys_off.npy (round-trip checked on every polynomial).
"""
import pickle
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "code"))
from tclib.padic import Layer  # noqa: E402

ASSETS = Path(sys.argv[1])
CHECK = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
t0 = time.time()
with open(ASSETS / "polys.pkl", "rb") as fh:
    polys = pickle.load(fh)["polys"]
N = len(polys)
DMAX = max(len(p) for p in polys)
l2, l3 = Layer(2, 4, 64, 7), Layer(3, 2, 20, 7)
M2, M3 = 1 << 64, l3.mod

c2 = np.zeros((N, DMAX), dtype=np.uint64)
c3 = np.zeros((N, DMAX), dtype=np.uint64)
deg = np.zeros(N, dtype=np.int16)
tz = np.zeros(N, dtype=np.int16)
for i, p in enumerate(polys):
    n = len(p)
    c2[i, :n] = [c % M2 for c in p]
    c3[i, :n] = [c % M3 for c in p]
    deg[i] = n - 1
    m = 0
    while p[m] == 0:
        m += 1
    tz[i] = m
print(f"reduced {N:,} polys (max length {DMAX}) in {time.time()-t0:.0f}s", flush=True)


def horner(coef, points, mod):
    out = np.zeros((coef.shape[0], len(points)), dtype=np.uint64)
    for j, x in enumerate(points):
        xr = np.uint64(x % mod) if mod else np.uint64(x % (1 << 64))
        acc = np.zeros(coef.shape[0], dtype=np.uint64)
        for d in range(coef.shape[1] - 1, -1, -1):
            if mod:
                acc = (acc * xr % np.uint64(mod) + coef[:, d]) % np.uint64(mod)
            else:
                acc = acc * xr + coef[:, d]
        out[:, j] = acc
    return out


with np.errstate(over="ignore"):
    val2 = horner(c2, l2.points, 0)
    val3 = horner(c3, l3.points, M3)
print(f"evaluated in {time.time()-t0:.0f}s", flush=True)

rng = np.random.default_rng(1)
bad = 0
for i in rng.choice(N, size=min(CHECK, N), replace=False):
    if not (np.array_equal(val2[i], l2.values(polys[i])) and np.array_equal(val3[i], l3.values(polys[i]))):
        bad += 1
print(f"exact re-check of {min(CHECK, N)} random polys: {bad} mismatches", flush=True)
if bad:
    sys.exit(1)
blob, off = bytearray(), [0]
for p in polys:
    blob += pickle.dumps(tuple(int(c) for c in p), protocol=5)
    off.append(len(blob))
(ASSETS / "polys_blob.bin").write_bytes(bytes(blob))
np.save(ASSETS / "polys_off.npy", np.array(off, dtype=np.int64))
roundtrip = all(pickle.loads(bytes(blob[off[i]:off[i + 1]])) == tuple(polys[i]) for i in range(N))
print(f"packed {N:,} polys into {len(blob):,} bytes; full round-trip equal: {roundtrip}", flush=True)
if not roundtrip:
    sys.exit(1)
np.save(ASSETS / "res_val2.npy", val2)
np.save(ASSETS / "res_val3.npy", val3)
np.save(ASSETS / "res_deg.npy", deg)
np.save(ASSETS / "res_tz.npy", tz)
print(f"written in {time.time()-t0:.0f}s")
