"""Lemma piece 11: the pair-collapse face rank floor (both pairs).

Setting: u = eps a, p = eps b with a, b > 0 fixed and eps -> 0, heights
v, q fixed and distinct. Both mirror pairs collapse onto the axis (bodies
3, 4 coincide at (0, v); bodies 5, 6 coincide at (0, q)): a DOUBLE
COLLISION, outside the open stratum, and the face where m2's residue and
deep's/uplow's deepest boxes sit.

Hand derivation (verified below). With the mass-column rescales already in
those charts (mA by 4u^2, mB by 4p^2), the entries behave as

  (L13, mA) -> h1,  (L15, mB) -> g1,  (L23, mA) -> gam, (L25, mB) -> g2,
  (L35, mA) -> -f,  (L35, mB) -> f,   (L36, mA) -> -f,  (L36, mB) -> -f,
  every m1 and m2 entry = O(eps),  the mA/mB cross entries = O(eps^3),

so the face matrix has rank 2 and no box containing it can certify. But
dividing the m1 and m2 COLUMNS by eps makes them O(1), and the rescaled
face matrix is generically RANK 4. Its 4 x 4 minor on rows
{L13, L15, L23, L25} evaluates in closed form to

    4 a b [ phi(h1) phi(g2) - phi(gam) phi(g1) ],
    phi(x) = x (1/8 - 1/|x|^3),
    h1 = 1 - v,  gam = -1 - v,  g1 = 1 - q,  g2 = -1 - q.

Hence rank 4 (so certainly >= 3) for all small eps > 0 wherever
phi(1-v) phi(-1-q) != phi(-1-v) phi(1-q). This script checks the closed
form against the true minor, then builds the branch table on its zero set.
"""
import mpmath as mp

mp.mp.dps = 40

def J_orig(u, v, p, q):
    h1 = 1 - v; gam = -1 - v; g1 = 1 - q; g2 = -1 - q; f = v - q
    d1A = mp.sqrt(u**2 + h1**2); d2A = mp.sqrt(u**2 + gam**2)
    d1B = mp.sqrt(p**2 + g1**2); d2B = mp.sqrt(p**2 + g2**2)
    cs = mp.sqrt((u - p)**2 + f**2); cx = mp.sqrt((u + p)**2 + f**2)
    wA = 2 * u; wB = 2 * p; r12 = mp.mpf(2)
    s = lambda a, b: a**-3 - b**-3
    J = [[mp.mpf(0)] * 4 for _ in range(6)]
    J[0][1] = s(r12, d2A) * (-2 * u); J[0][2] = s(d1A, wA) * (-2 * u * h1)
    J[0][3] = s(d1B, cs) * (p * h1 - u * g1) + s(d1B, cx) * (-(u * g1 + p * h1))
    J[1][1] = s(r12, d2B) * (-2 * p)
    J[1][2] = s(d1A, cs) * (u * g1 - p * h1) + s(d1A, cx) * (-(p * h1 + u * g1))
    J[1][3] = s(d1B, wB) * (-2 * p * g1)
    J[2][0] = s(r12, d1A) * (2 * u); J[2][2] = s(d2A, wA) * (-2 * u * gam)
    J[2][3] = s(d2B, cs) * (p * gam - u * g2) + s(d2B, cx) * (-(u * g2 + p * gam))
    J[3][0] = s(r12, d1B) * (2 * p)
    J[3][2] = s(d2A, cs) * (u * g2 - p * gam) + s(d2A, cx) * (-(p * gam + u * g2))
    J[3][3] = s(d2B, wB) * (-2 * p * g2)
    J[4][0] = s(d1A, d1B) * (p * h1 - u * g1); J[4][1] = s(d2A, d2B) * (p * gam - u * g2)
    J[4][2] = s(wA, cx) * (-2 * f * u); J[4][3] = s(cx, wB) * (-2 * f * p)
    J[5][0] = s(d1A, d1B) * (-(u * g1 + p * h1)); J[5][1] = s(d2A, d2B) * (-(u * g2 + p * gam))
    J[5][2] = s(wA, cs) * (-2 * f * u); J[5][3] = s(cs, wB) * (2 * f * p)
    return J

def rescaled(a, b, v, q, eps):
    """chart matrix: mA x 4u^2, mB x 4p^2, m1 and m2 columns / eps."""
    u, p = eps * a, eps * b
    J = J_orig(u, v, p, q)
    col = [1 / eps, 1 / eps, 4 * u**2, 4 * p**2]
    return [[J[i][j] * col[j] for j in range(4)] for i in range(6)]

def det4(M, rows):
    import itertools
    tot = mp.mpf(0)
    for perm in itertools.permutations(range(4)):
        sgn = 1
        pl = list(perm)
        for i in range(4):
            for j in range(i + 1, 4):
                if pl[i] > pl[j]:
                    sgn = -sgn
        term = mp.mpf(sgn)
        for i in range(4):
            term *= M[rows[i]][perm[i]]
        tot += term
    return tot

def det3(M, rows, cols):
    a, b, c = rows; x, y, z = cols
    return (M[a][x] * (M[b][y] * M[c][z] - M[b][z] * M[c][y])
            - M[a][y] * (M[b][x] * M[c][z] - M[b][z] * M[c][x])
            + M[a][z] * (M[b][x] * M[c][y] - M[b][y] * M[c][x]))

def phi(x):
    return x * (mp.mpf(1) / 8 - 1 / abs(x)**3)

def C2(a, b, v, q):
    return 4 * a * b * (phi(1 - v) * phi(-1 - q) - phi(-1 - v) * phi(1 - q))

print("A. the 4x4 minor of the rescaled face matrix vs the closed form")
print("   C2 = 4ab[phi(1-v)phi(-1-q) - phi(-1-v)phi(1-q)]:")
CASES = [(mp.mpf(1), mp.mpf(2), mp.mpf(1)/3, -mp.mpf(3)/2),
         (mp.mpf(3)/2, mp.mpf(1)/2, mp.mpf(9)/4, mp.mpf(1)/4),
         (mp.mpf(2), mp.mpf(5)/2, -mp.mpf(7)/4, mp.mpf(5)/2)]
for (a, b, v, q) in CASES:
    pred = C2(a, b, v, q)
    vals = [det4(rescaled(a, b, v, q, mp.mpf(10) ** -e), (0, 1, 2, 3))
            for e in (3, 5, 7)]
    print(f"  a={float(a):.2f} b={float(b):.2f} v={float(v):+.3f} q={float(q):+.3f}: "
          f"M(1e-3)={mp.nstr(vals[0],8)} M(1e-5)={mp.nstr(vals[1],8)} "
          f"M(1e-7)={mp.nstr(vals[2],8)}   C2={mp.nstr(pred,8)}")

print("\nB. the zero set of C2 and the branch table")
# solve phi(1-v)phi(-1-q) = phi(-1-v)phi(1-q) for q at sample v
def bracket(v, q):
    return phi(1 - v) * phi(-1 - q) - phi(-1 - v) * phi(1 - q)

roots = []
for v0 in (mp.mpf(1)/3, mp.mpf(3)/2, -mp.mpf(2)/3):
    for guess in (mp.mpf(-2), mp.mpf(-1)/2, mp.mpf(1)/2, mp.mpf(2), mp.mpf(3)):
        try:
            r = mp.findroot(lambda q: bracket(v0, q), guess)
            if abs(bracket(v0, r)) < mp.mpf(10) ** -20 and abs(r - v0) > mp.mpf(1)/100:
                if all(abs(r - rr) > mp.mpf(1)/1000 for vv, rr in roots if vv == v0):
                    roots.append((v0, r))
        except Exception:
            pass
print(f"  found {len(roots)} zero-curve points (v, q) with C2 = 0:")
MENU = [((i, j, k), (x, y, z))
        for i in range(6) for j in range(i + 1, 6) for k in range(j + 1, 6)
        for x in range(4) for y in range(x + 1, 4) for z in range(y + 1, 4)]
for v0, q0 in roots[:6]:
    a, b = mp.mpf(1), mp.mpf(2)
    best = None
    for rows, cols in MENU:
        try:
            m4 = det3(rescaled(a, b, v0, q0, mp.mpf(10) ** -4), rows, cols)
            m6 = det3(rescaled(a, b, v0, q0, mp.mpf(10) ** -6), rows, cols)
        except Exception:
            continue
        if m4 == 0 or abs(m6) < mp.mpf(10) ** -9:
            continue
        ratio = abs(m6 / m4)
        if 0.2 < ratio < 5 and (best is None or abs(m6) > abs(best[1])):
            best = ((rows, cols), m6)
    tag = (f"{best[0][0]}x{best[0][1]} limit {mp.nstr(best[1], 6)}"
           if best else "NO order-0 minor")
    print(f"   v={float(v0):+.4f} q={float(q0):+.4f}  C2=0  ->  {tag}")
