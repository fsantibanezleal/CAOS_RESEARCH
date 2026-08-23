"""The face v = q = 0 of the (2,2) stratum: is any point of it a central
configuration?

band's residue led here. On that face all four pair bodies lie on one
horizontal line through the origin while the two axis bodies sit at
(0, +-1), so the configuration has TWO reflection symmetries: the cross.
Measured: sigma_4 vanishes IDENTICALLY on the face (1e-51 at every sample)
while sigma_3 stays nonzero, so the rank there is exactly 3 and the kernel
is exactly one-dimensional. That means every point of the face determines
a UNIQUE mass ray, and the only question left is whether that ray is ever
positive.

If it is, the face carries a two-parameter family of central
configurations and the covering is right to refuse a certificate there.
If it never is, the face carries none and the residue is bookkeeping.
"""
import mpmath as mp

mp.mp.dps = 40

ROWS = [(0, 2), (0, 4), (1, 2), (1, 4), (2, 4), (2, 5)]
PAIR_OF = [None, None, 2, 2, 3, 3]


def M_of(u, v, p, q):
    P = [(mp.mpf(0), mp.mpf(1)), (mp.mpf(0), mp.mpf(-1)),
         (u, v), (-u, v), (p, q), (-p, q)]
    rows = []
    for (i, j) in ROWS:
        c = [mp.mpf(0)] * 4
        for k in range(6):
            if k == i or k == j:
                continue
            rik = mp.sqrt((P[i][0] - P[k][0]) ** 2 + (P[i][1] - P[k][1]) ** 2)
            rjk = mp.sqrt((P[j][0] - P[k][0]) ** 2 + (P[j][1] - P[k][1]) ** 2)
            area = ((P[j][0] - P[i][0]) * (P[k][1] - P[i][1])
                    - (P[j][1] - P[i][1]) * (P[k][0] - P[i][0]))
            col = k if k < 2 else PAIR_OF[k]
            c[col] += (rik ** -3 - rjk ** -3) * area
        rows.append(c)
    return rows


def rank_kernel(u, p):
    A = mp.matrix(6, 4)
    M = M_of(u, mp.mpf(0), p, mp.mpf(0))
    for i in range(6):
        n = max(abs(x) for x in M[i]) or mp.mpf(1)
        for j in range(4):
            A[i, j] = M[i][j] / n
    U, S, V = mp.svd_r(A)
    sv = [S[i] for i in range(4)]
    ker = [V[3, j] for j in range(4)]
    nrm = max(abs(k) for k in ker)
    ker = [k / nrm for k in ker]
    if sum(1 for k in ker if k > 0) < 2:
        ker = [-k for k in ker]
    return sv, ker


print("scanning the face v = q = 0 over (u, p), u < p, no collisions")
print("reporting the kernel sign pattern; '++++' would be a central")
print("configuration\n")
print("     u       p     sigma_3     kernel (m1, m2, mA, mB)          sign")
found = []
N = 26
for iu in range(1, N):
    u = mp.mpf(iu) / 10
    for ip in range(iu + 1, N + 6):
        p = mp.mpf(ip) / 10
        if p - u < mp.mpf("0.05"):
            continue
        sv, ker = rank_kernel(u, p)
        pat = "".join("+" if k > 0 else "-" for k in ker)
        if pat == "++++":
            found.append((u, p, sv, ker))
        if iu in (5, 6, 7) and ip in (13, 14, 15, 16):
            print(f"  {float(u):6.2f}  {float(p):6.2f}  {float(sv[2]):.3e}  "
                  + ", ".join(f"{float(k):+.5f}" for k in ker) + f"   {pat}")
print(f"\n  points scanned with all-positive kernel: {len(found)}")
if found:
    for (u, p, sv, ker) in found[:8]:
        print(f"    u={float(u):.3f} p={float(p):.3f}  sigma_3={float(sv[2]):.3e}"
              "  kernel " + ", ".join(f"{float(k):+.5f}" for k in ker))
else:
    print("    NONE: the face carries no central configuration")

print("\nsign patterns seen across the whole scan:")
pats = {}
for iu in range(1, N):
    u = mp.mpf(iu) / 10
    for ip in range(iu + 1, N + 6):
        p = mp.mpf(ip) / 10
        if p - u < mp.mpf("0.05"):
            continue
        _, ker = rank_kernel(u, p)
        pat = "".join("+" if k > 0 else "-" for k in ker)
        pats[pat] = pats.get(pat, 0) + 1
for k, v in sorted(pats.items(), key=lambda kv: -kv[1]):
    print(f"    {k}: {v}")
