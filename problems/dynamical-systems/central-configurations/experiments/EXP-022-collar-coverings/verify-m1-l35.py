"""Verify the extra rhoq factor in M1's L35 row (for the piece-12 fix).

Claim (hand derivation):  with u = rhoa ca, gam = -2 - rhoa sa,
p = rr rhoa cb, and the B-side height 2 + rr rhoa sb,

    d2B^2 - d2A^2 = rhoa * rhoq * [ rhoa * alpha * (2 + rhoq alpha)
                                     - 4 * Fch ]

where rr = 1 + rhoq alpha, Fch = (sa - rr sb)/rhoq is the extracted hat.
If true, (1/d2A^3 - 1/d2B^3) carries an explicit rhoq factor and M1's L35
row can be divided by one more power of rhoq, which is exactly what the
entry-order probe says it needs.
"""
import mpmath as mp
mp.mp.dps = 40

def circ(t):
    o = 1 + t * t
    return (1 - t * t) / o, 2 * t / o

def check(rhoa, tb, tq, rhoq):
    al_n, be = circ(tq)
    alpha = -al_n
    rr = 1 + rhoq * alpha
    ta = tb + rhoq * be
    ca, sa = circ(ta)
    cb, sb = circ(tb)
    u = rhoa * ca
    gam = -2 - rhoa * sa
    p = rr * rhoa * cb
    hB = 2 + rr * rhoa * sb
    d2A2 = u**2 + gam**2
    d2B2 = p**2 + hB**2
    lhs = d2B2 - d2A2
    Fch = (sa - rr * sb) / rhoq
    rhs = rhoa * rhoq * (rhoa * alpha * (2 + rhoq * alpha) - 4 * Fch)
    return lhs, rhs

print("d2B^2 - d2A^2  vs  rhoa rhoq [rhoa alpha (2 + rhoq alpha) - 4 Fch]:")
for (ra, tb, tq, rq) in ((mp.mpf(1)/8, mp.mpf(1)/3, mp.mpf(1)/5, mp.mpf(1)/64),
                         (mp.mpf(3)/16, -mp.mpf(2)/5, mp.mpf(3)/7, mp.mpf(1)/256),
                         (mp.mpf(1)/16, mp.mpf(4)/5, -mp.mpf(1)/3, mp.mpf(1)/1024)):
    l, r = check(ra, tb, tq, rq)
    rel = abs(l - r) / (abs(l) + mp.mpf(10)**-40)
    print(f"  rhoa={float(ra):.4f} rhoq={float(rq):.2e}: lhs={mp.nstr(l,10)} "
          f"rhs={mp.nstr(r,10)}  rel.err={mp.nstr(rel,3)}")
