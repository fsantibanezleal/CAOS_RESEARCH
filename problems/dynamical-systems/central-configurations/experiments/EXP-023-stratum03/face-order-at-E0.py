"""On the surface E = 0, how does the cleared entry behave at rho > 0?

E is only the LIMIT of row (2,4) column 0. On the surface where E vanishes
the entry is not identically zero for rho > 0; it is whatever the next
order in rho supplies. Measuring that order and coefficient says exactly
what a blow-up sub-chart would have to divide by, and whether rank 3 is
restored at positive separation.
"""
import mpmath as mp

mp.mp.dps = 60


def entry(rho, tau, wu, wv):
    o = 1 + tau * tau
    al, be = (1 - tau * tau) / o, 2 * tau / o
    uv = [(mp.mpf(1), mp.mpf(0)),
          (wu + rho * al / 2, wv + rho * be / 2),
          (wu - rho * al / 2, wv - rho * be / 2)]
    P = []
    for (u, v) in uv:
        P.append((u, v))
        P.append((-u, v))
    i, j = 2, 4
    tot = mp.mpf(0)
    for k in (0, 1):
        rik = mp.sqrt((P[i][0] - P[k][0]) ** 2 + (P[i][1] - P[k][1]) ** 2)
        rjk = mp.sqrt((P[j][0] - P[k][0]) ** 2 + (P[j][1] - P[k][1]) ** 2)
        area = ((P[j][0] - P[i][0]) * (P[k][1] - P[i][1])
                - (P[j][1] - P[i][1]) * (P[k][0] - P[i][0]))
        tot += (rik ** -3 - rjk ** -3) * area
    return tot / (rho * rho)


def E_closed(tau, wu, wv):
    o = 1 + tau * tau
    n = ((1 - tau * tau) / o, 2 * tau / o)
    tot = mp.mpf(0)
    for Pk in ((mp.mpf(1), mp.mpf(0)), (mp.mpf(-1), mp.mpf(0))):
        g = (wu - Pk[0], wv - Pk[1])
        dot = n[0] * g[0] + n[1] * g[1]
        crs = n[0] * g[1] - n[1] * g[0]
        gn = mp.sqrt(g[0] ** 2 + g[1] ** 2)
        tot += dot * crs / gn ** 5
    return -3 * tot


def root(wu, wv, lo, hi):
    a, b = mp.mpf(lo), mp.mpf(hi)
    fa = E_closed(a, wu, wv)
    for _ in range(300):
        m = (a + b) / 2
        fm = E_closed(m, wu, wv)
        if fa * fm <= 0:
            b = m
        else:
            a, fa = m, fm
    return (a + b) / 2


cases = [(mp.mpf("0.97"), mp.mpf("0.99"), -2, -0.5),
         (mp.mpf("0.5"), mp.mpf("0.25"), -2, -0.5),
         (mp.mpf("0.2"), mp.mpf("-0.7"), -2, 0),
         (mp.mpf("0.75"), mp.mpf("0.4"), -2, 0)]

print("on E = 0: the entry at shrinking rho, and its order")
for (wu, wv, lo, hi) in cases:
    t = root(wu, wv, lo, hi)
    vals = []
    for k in (8, 10, 12, 14):
        r = mp.mpf(2) ** -k
        vals.append((k, entry(r, t, wu, wv)))
    o1 = mp.log(abs(vals[0][1] / vals[1][1])) / mp.log(4)
    o2 = mp.log(abs(vals[1][1] / vals[2][1])) / mp.log(4)
    o3 = mp.log(abs(vals[2][1] / vals[3][1])) / mp.log(4)
    print(f"\n  w=({float(wu):.2f},{float(wv):+.2f})  tau*={float(t):+.9f}"
          f"  E={float(E_closed(t, wu, wv)):+.2e}")
    for (k, v) in vals:
        print(f"     rho=2^-{k:<3} entry = {float(v):+.6e}")
    print(f"     measured order in rho: {float(o1):+.3f}, {float(o2):+.3f}, "
          f"{float(o3):+.3f}")
    c = vals[-1][1] / (mp.mpf(2) ** -14) ** 2
    print(f"     entry/rho^2 at the last point = {float(c):+.6e}")
