"""TCB-027 / V10: how much of a program's root capacity is realized over Z?

Over F_p the conjecture is FALSE in the strongest way: x^p - x costs about
2 log p gates and has p roots. Over Z the same polynomial has three. This
measures the gap as a census, not an anecdote:

    zmax(tau)  = max distinct INTEGER roots of a tau-gate polynomial
    zpmax(tau) = max over primes p of the distinct roots in F_p

Both maxima are taken over exactly the same enumerated set of polynomials,
so the ratio is a like-for-like statement about the same programs.
"""
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))
from tclib.enum import census_polynomials, integer_roots

DEPTH = 5
def _primes_upto(n):
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return [i for i, ok in enumerate(sieve) if ok]


# Up to 257: a tau<=5 polynomial has degree at most 32, so it cannot have more
# than 32 roots in any F_p; primes well past that bound make the maximum
# meaningful rather than an artifact of where the prime list stopped.
PRIMES = _primes_upto(257)
CHUNK = 20000

t0 = time.time()
per_depth, first_seen, complete = census_polynomials(DEPTH)
print(f"census to depth {DEPTH}: {len(first_seen):,} distinct polynomials "
      f"in {time.time()-t0:.0f}s; complete={complete}")

by_tau = {}
for poly, tau in first_seen.items():
    if not poly:                      # the zero polynomial vanishes everywhere
        continue
    by_tau.setdefault(tau, []).append(poly)

print()
print(f"{'tau':>4} {'polys':>9} {'zmax(Z)':>8} {'zpmax(F_p)':>11} {'at p':>5} "
      f"{'maxdeg':>7}  witness of zpmax")
print("-" * 96)
rows = []
for tau in sorted(by_tau):
    polys = by_tau[tau]
    maxdeg = max(len(p) for p in polys) - 1
    C = np.zeros((len(polys), maxdeg + 1), dtype=np.int64)
    for i, p in enumerate(polys):
        C[i, :len(p)] = p

    zint = 0
    for p in polys:
        n = len(integer_roots(p))
        if n > zint:
            zint = n

    best = (0, None, None)
    for q in PRIMES:
        r = np.arange(q, dtype=np.int64)
        counts = np.zeros(len(polys), dtype=np.int64)
        for s in range(0, len(polys), CHUNK):
            blk = C[s:s + CHUNK] % q
            acc = np.zeros((blk.shape[0], q), dtype=np.int64)
            for k in range(maxdeg, -1, -1):        # Horner, high to low
                acc = (acc * r + blk[:, k:k + 1]) % q
            counts[s:s + CHUNK] = (acc == 0).sum(axis=1)
        # A polynomial whose coefficients are ALL divisible by q reduces to
        # the zero polynomial of F_q and vanishes at every residue. That is the
        # F_q analogue of f = 0, not a root count, and it is the same trap that
        # produced the zero-polynomial floods in the CEGAR loop and in EXP-013.
        # Exclude it, exactly as the integer instrument excludes f = 0.
        nonzero_mod_q = (C % q).any(axis=1)
        counts = np.where(nonzero_mod_q, counts, -1)
        i = int(counts.argmax())
        if counts[i] > best[0]:
            best = (int(counts[i]), q, polys[i])
    rows.append((tau, len(polys), zint, best[0], best[1], maxdeg, best[2]))
    w = str(best[2])
    print(f"{tau:>4} {len(polys):>9,} {zint:>8} {best[0]:>11} {best[1]:>5} "
          f"{maxdeg:>7}  {w if len(w) < 34 else w[:31] + '...'}")

print()
print("reading: zpmax is capped by the degree, so it cannot exceed 2^tau; what")
print("matters is whether the F_p count runs AHEAD of the integer count on the")
print("same programs, and by how much.")
for tau, n, zi, zp, q, d, w in rows:
    print(f"  tau={tau}: F_p/Z ratio = {zp}/{zi} = {zp/zi:.2f}   (degree ceiling {d})")
