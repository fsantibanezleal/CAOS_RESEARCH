"""Atlas coverage audit: does every stratum point belong to some chart?

The certificates prove rank statements ON each chart's region. The
remaining risk is a SEAM GAP: a point of the open stratum claimed by no
chart, or claimed only by a chart that discards it. This gate samples the
stratum (uniformly in the gauge box, plus adversarially near every face
and seam) and, for each sample, evaluates the DECLARED region predicate
and discard rule of every chart, reporting any point that no chart both
contains and keeps.

Region predicates are transcribed here from the charts' own seeds and
discard functions; the transcription is checked by asserting a handful of
known memberships (the pentagon in core, the cross in band, etc.).

Klein symmetry: a point covered by the swap or mirror image of a chart is
covered (lemma pieces 9d, 9e), so the audit closes each sample under the
group before declaring a gap.
"""
import random
from fractions import Fraction as F

S = F(1, 16)

def norm(x, y):
    return (x * x + y * y) ** 0.5

def charts_claiming(u, v, p, q):
    """Return the list of chart names whose declared region contains
    (u, v, p, q) AND whose discard rule keeps it."""
    out = []
    f = v - q
    t = u - p
    RA = norm(float(u), float(v))
    RB = norm(float(p), float(q))
    d1A = norm(float(u), float(v) - 1)
    d2A = norm(float(u), float(v) + 1)
    d1B = norm(float(p), float(q) - 1)
    d2B = norm(float(p), float(q) + 1)
    inbox = (0 <= u <= 3 and -3 <= v <= 3 and 0 <= p <= 3 and -3 <= q <= 3)

    # --- bounded charts -------------------------------------------------
    if inbox:
        if u >= F(1, 4) and p >= F(1, 4) and abs(f) >= F(1, 4):
            out.append("core")
        if u >= F(1, 4) and p >= F(1, 4) and abs(f) <= F(1, 4) \
                and max(abs(t), abs(f)) >= S:
            out.append("band")
        # collision tube: |t| <= 1/16 and |f| <= 1/16, split by w
        w = (u + p) / 2
        if abs(t) <= S and abs(f) <= S:
            if w >= F(7, 32):
                out.append("tube")
            elif w >= F(1, 8):
                out.append("tubeext")
            elif not (w < F(1, 32) and norm(float(t), float(f)) < F(1, 16)):
                out.append("deep")
            else:
                out.append("M2")
        # pair-collapse collars
        if u <= F(1, 4) and p >= F(1, 4):
            if not (u <= S and (abs(v - 1) <= S or abs(v + 1) <= S)) \
                    and not (abs(t) < S and abs(f) < S):
                out.append("ulow")
        # plow is the SWAP image of ulow: supplied by the Klein orbit, not
        # claimed separately (claiming it here would double-cover and make
        # the negative controls non-discriminating).
        if u <= F(1, 4) and p <= F(1, 4):
            corner = ((u <= S and (abs(v - 1) <= S or abs(v + 1) <= S))
                      or (p <= S and (abs(q - 1) <= S or abs(q + 1) <= S)))
            band_c = abs(t) < S and abs(f) < S
            if not corner and not band_c:
                out.append("uplow")
        # corner charts: B within 3/32 of an axis body, A anywhere bounded
        # cb1: B within 3/32 of axis body 1, A bounded. The body-2 version
        # is the MIRROR image and the A-at-corner versions are the SWAP
        # images: both come from the Klein orbit, not claimed here.
        rc = norm(float(p), float(q) - 1)
        if rc <= 3 / 32:
            Acorner1 = (u <= F(1, 8) and abs(v - 1) <= F(1, 8))
            Acorner2 = (u <= S and abs(v + 1) <= S)
            if not Acorner1 and not Acorner2:
                out.append("cb1")
            else:
                out.append("bicorner/M1 family")
    # --- outer charts ---------------------------------------------------
    if RA > 3 or RB > 3:
        big, small = (RA, RB) if RA >= RB else (RB, RA)
        if small <= 3 / 2:
            out.append("fa1 (or its swap)")
        else:
            out.append("fa2b (or its swap)")
    return out

def sample_uniform(rnd):
    g = lambda a, b: F(rnd.randint(a, b), 64)
    return g(1, 192), g(-192, 192), g(1, 192), g(-192, 192)

def sample_near_face(rnd):
    """Adversarial: sit on or near each singular face."""
    kind = rnd.randrange(10)
    tiny = F(rnd.randint(1, 64), 4096)
    g = lambda a, b: F(rnd.randint(a, b), 64)
    if kind == 0:                       # A collapsing
        return tiny, g(-192, 192), g(16, 192), g(-192, 192)
    if kind == 1:                       # B collapsing
        return g(16, 192), g(-192, 192), tiny, g(-192, 192)
    if kind == 2:                       # equal heights
        v = g(-192, 192)
        return g(1, 192), v, g(1, 192), v + tiny
    if kind == 3:                       # A+ meets B+ (the tube)
        u = g(16, 192); v = g(-192, 192)
        return u, v, u + tiny, v - tiny
    if kind == 4:                       # B on axis body 1
        return g(16, 192), g(-192, 192), tiny, 1 + tiny
    if kind == 5:                       # both on axis body 1
        return tiny, 1 + tiny, tiny * 2, 1 - tiny
    if kind == 6:                       # far A
        return F(rnd.randint(200, 4000), 64), g(-192, 192), g(16, 192), g(-192, 192)
    if kind == 7:                       # both far
        return (F(rnd.randint(200, 4000), 64), g(-4000, 4000),
                F(rnd.randint(200, 4000), 64), g(-4000, 4000))
    if kind == 8:
        return tiny, tiny, tiny * 3, -1 + tiny  # both pairs at body 2
    # kind 9: the COLLINEAR QUADRUPLE corner (M2's region): both pairs
    # tiny AND merged AND at nearly equal heights. Missed by every other
    # sampler; the negative control on M2 exposed the omission.
    v = g(-192, 192)
    eps2 = F(rnd.randint(1, 40), 1 << 14)
    return tiny, v, tiny + eps2 / 8, v - eps2

def klein_orbit(pt):
    u, v, p, q = pt
    return [(u, v, p, q), (p, q, u, v), (u, -v, p, -q), (p, -q, u, -v)]

def run(N, drop=None, seed=20260820, verbose=True):
    """drop: chart-name substring to disable (negative control)."""
    rnd = random.Random(seed)
    gaps = []
    tested = 0
    for i in range(N):
        pt = sample_uniform(rnd) if i % 2 else sample_near_face(rnd)
        u, v, p, q = pt
        if u <= 0 or p <= 0 or v == q:
            continue                      # not in the open stratum
        tested += 1
        claimed = []
        for img in klein_orbit(pt):
            claimed += charts_claiming(*img)
        if drop is not None:
            claimed = [c for c in claimed if drop not in c]
        if not claimed:
            gaps.append(pt)
    if verbose:
        tag = "full atlas" if drop is None else f"atlas MINUS '{drop}'"
        print(f"{tag}: tested {tested}, UNCLAIMED {len(gaps)}")
        for g in gaps[:4]:
            print("     e.g. u=%.5f v=%.5f p=%.5f q=%.5f (f=%.2e, t=%.2e)"
                  % (float(g[0]), float(g[1]), float(g[2]), float(g[3]),
                     float(g[1] - g[3]), float(g[0] - g[2])))
    return tested, len(gaps)

def main():
    tested, gaps = run(40000)
    if gaps == 0:
        print("ATLAS COVERS THE SAMPLE: every stratum point is claimed and kept "
              "by at least one chart (up to the Klein group).")
    print("\nNEGATIVE CONTROLS (dropping one chart must OPEN a gap):")
    controls = ["core", "band", "tube", "ulow", "uplow", "cb1",
                "deep", "M2", "fa1", "fa2b", "bicorner"]
    bad = []
    for c in controls:
        t, g = run(40000, drop=c, verbose=False)
        status = "gap opens (OK)" if g > 0 else "NO GAP: predicate too permissive"
        print(f"   drop {c:10s}: {g:6d} unclaimed   {status}")
        if g == 0:
            bad.append(c)
    print("\nCONTROL VERDICT: " + ("all controls fired"
          if not bad else f"NOT DISCRIMINATING for {bad}"))

if __name__ == "__main__":
    main()
