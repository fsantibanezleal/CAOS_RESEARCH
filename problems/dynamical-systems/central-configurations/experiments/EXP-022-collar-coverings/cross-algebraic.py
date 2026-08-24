"""Is the cross point algebraic, and can its minimal polynomial be found?

The point is currently a forty-digit numeric. Central configurations are
solutions of a polynomial system in the mutual distances, so u* and p*
must be algebraic; recovering their minimal polynomials would turn the
result from a numeric into a checkable exact statement.

Two steps: refine (u*, p*) far past forty digits by Newton on the rank-2
conditions, then run PSLQ on the powers of each to look for an integer
relation, i.e. a minimal polynomial.
"""
import mpmath as mp

mp.mp.dps = 260

ROWS = [(0, 2), (0, 4), (1, 2), (1, 4), (2, 4), (2, 5)]
COL = [0, 1, 2, 2, 3, 3]


def rows_at(u, v, p, q):
    P = [(mp.mpf(0), mp.mpf(1)), (mp.mpf(0), mp.mpf(-1)),
         (u, v), (-u, v), (p, q), (-p, q)]
    out = []
    for (i, j) in ROWS:
        c = [mp.mpf(0)] * 4
        for k in range(6):
            if k == i or k == j:
                continue
            rik = mp.sqrt((P[i][0] - P[k][0]) ** 2 + (P[i][1] - P[k][1]) ** 2)
            rjk = mp.sqrt((P[j][0] - P[k][0]) ** 2 + (P[j][1] - P[k][1]) ** 2)
            area = ((P[j][0] - P[i][0]) * (P[k][1] - P[i][1])
                    - (P[j][1] - P[i][1]) * (P[k][0] - P[i][0]))
            c[COL[k]] += (rik ** -3 - rjk ** -3) * area
        out.append(c)
    return out


def cross_system(u, p):
    """The 3 x 4 system in (m1, mA, mB, lambda), built directly."""
    B = [(mp.mpf(0), mp.mpf(1)), (mp.mpf(0), mp.mpf(-1)),
         (u, mp.mpf(0)), (-u, mp.mpf(0)), (p, mp.mpf(0)), (-p, mp.mpf(0))]
    grp = [0, 0, 1, 1, 2, 2]

    def row(i, comp):
        c = [mp.mpf(0)] * 4
        for j in range(6):
            if j == i:
                continue
            dx = B[j][0] - B[i][0]
            dy = B[j][1] - B[i][1]
            r3 = (dx * dx + dy * dy) ** mp.mpf("1.5")
            c[grp[j]] += (dx if comp == 0 else dy) / r3
        c[3] = B[i][0] if comp == 0 else B[i][1]
        return c
    return [row(2, 0), row(4, 0), row(0, 1)]


def minors(u, p):
    """Two independent 3x3 minors of the 3x4 system; both vanish at rank 2."""
    M = cross_system(u, p)

    def d3(cols):
        a = [[M[r][c] for c in cols] for r in range(3)]
        return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
                - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
                + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))
    return [d3((0, 1, 2)), d3((0, 1, 3))]


print("A. Newton refinement of (u*, p*) at 260 digits")
u0 = mp.mpf("0.6309181371067367971679885968642467138842")
p0 = mp.mpf("1.450907465908073057191660806806502905941")
sol = mp.findroot(lambda a, b: minors(a, b), (u0, p0),
                  tol=mp.mpf(10) ** -240)
u, p = sol[0], sol[1]
r = minors(u, p)
print(f"   residuals: {mp.nstr(r[0], 6)}, {mp.nstr(r[1], 6)}")
print(f"   u = {mp.nstr(u, 60)}")
print(f"   p = {mp.nstr(p, 60)}")

A = mp.matrix(3, 4)
M = cross_system(u, p)
for i in range(3):
    n = max(abs(x) for x in M[i])
    for j in range(4):
        A[i, j] = M[i][j] / n
_, S, _ = mp.svd_r(A)
print(f"   sigma_3/sigma_1 of the 3x4 system = {mp.nstr(S[2] / S[0], 6)}")

Mr = rows_at(u, mp.mpf(0), p, mp.mpf(0))
Ar = mp.matrix(6, 4)
for i in range(6):
    n = max(abs(x) for x in Mr[i])
    for j in range(4):
        Ar[i, j] = Mr[i][j] / n
_, Sr, _ = mp.svd_r(Ar)
print(f"   sigma_3/sigma_1 of the 6x4 reduced matrix = "
      f"{mp.nstr(Sr[2] / Sr[0], 6)}")

print("")
print("B. PSLQ on the powers: is there a minimal polynomial?")
for name, val in (("u*", u), ("p*", p), ("u*+p*", u + p), ("u**p*", u * p),
                  ("p*/u*", p / u)):
    hit = None
    for deg in range(2, 17):
        try:
            rel = mp.pslq([val ** k for k in range(deg + 1)],
                          tol=mp.mpf(10) ** -180, maxcoeff=10 ** 22,
                          maxsteps=40000)
        except Exception:
            rel = None
        if rel:
            hit = (deg, rel)
            break
    if hit:
        deg, rel = hit
        print(f"   {name}: degree {deg} relation {rel}")
    else:
        print(f"   {name}: no integer relation up to degree 16 "
              "with coefficients under 1e22")

print("")
print("C. the mutual distances, which is what the classical systems use")
d = {"r_AA": 2 * u, "r_BB": 2 * p, "r_AB_near": p - u, "r_AB_far": p + u,
     "r_12": mp.mpf(2), "r_1A": mp.sqrt(u * u + 1),
     "r_1B": mp.sqrt(p * p + 1)}
for k, val in d.items():
    print(f"   {k} = {mp.nstr(val, 40)}")
for name in ("r_1A", "r_1B"):
    val = d[name]
    hit = None
    for deg in range(2, 13):
        try:
            rel = mp.pslq([val ** k for k in range(deg + 1)],
                          tol=mp.mpf(10) ** -180, maxcoeff=10 ** 22,
                          maxsteps=40000)
        except Exception:
            rel = None
        if rel:
            hit = (deg, rel)
            break
    print(f"   {name}: " + (f"degree {hit[0]} relation {hit[1]}" if hit
                            else "no relation found"))
