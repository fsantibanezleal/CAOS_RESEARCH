"""EXP-009 analyzer: decide the torus census from msolve output, exactly.

Standalone (the original runner was interrupted by a shell teardown; the solves are
enforced by finish.sh in WSL). Reads artifacts/routeA.out and/or routeB.out and
reports, per route: the dimension msolve declares, the number of real solution
boxes, how many are positive in the six distance coordinates, how many of those are
REALIZABLE as four points in the plane, and how many relabeling classes they form.

Exactness policy: msolve's boxes are rational, so positivity of a coordinate is
decided exactly (lower endpoint > 0). Realizability uses the squared-distance Heron
form on every triple, evaluated on the box midpoint, and any triple whose value
straddles zero across the box is reported as UNDECIDED rather than assumed; with
isolating boxes this normally does not happen, and the count of undecided cases is
printed so the verdict can state it.
"""
import json
import sys
from fractions import Fraction
from itertools import combinations, permutations
from pathlib import Path

HERE = Path(__file__).resolve().parent
ART = HERE / "artifacts"
PAIRS = list(combinations(range(1, 5), 2))


def parse(text, nvars):
    import re
    pat = re.compile(r"\[\s*(-?\d+(?:\s*/\s*2\^\d+)?)\s*,\s*(-?\d+(?:\s*/\s*2\^\d+)?)\s*\]")

    def toF(s):
        s = s.replace(" ", "")
        if "/2^" in s:
            n, e = s.split("/2^")
            return Fraction(int(n), 2 ** int(e))
        return Fraction(int(s))

    pairs = [(toF(a), toF(b)) for a, b in pat.findall(text)]
    return [pairs[i:i + nvars] for i in range(0, len(pairs) - nvars + 1, nvars)]


def dim_of(text):
    t = text.strip()
    try:
        return int(t[1:t.index(",")])
    except Exception:
        return None


def heron_sq(x, y, z):
    """16 * area^2 from SQUARED side lengths; >= 0 iff the triple is realizable."""
    return 2 * x * y + 2 * y * z + 2 * z * x - x * x - y * y - z * z


def analyze(path, nvars, dist_slice):
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    d = dim_of(text)
    boxes = parse(text, nvars)
    positive, realizable, undecided = [], [], 0
    for bx in boxes:
        dist = [bx[i] for i in dist_slice]
        if any(lo <= 0 for lo, _ in dist):
            continue
        positive.append(dist)
        mids = {p: (lo + hi) / 2 for p, (lo, hi) in zip(PAIRS, dist)}
        sq = {p: v * v for p, v in mids.items()}
        ok, unsure = True, False
        for a, b, c in combinations(range(1, 5), 3):
            h = heron_sq(sq[(min(a, b), max(a, b))], sq[(min(a, c), max(a, c))],
                         sq[(min(b, c), max(b, c))])
            if h < 0:
                ok = False
                break
            if h == 0:
                unsure = True
        if ok:
            realizable.append(mids)
        if unsure:
            undecided += 1

    def key(mids):
        best = None
        for p in permutations(range(1, 5)):
            m = {}
            for (i, j), v in mids.items():
                a, b = p[i - 1], p[j - 1]
                m[(min(a, b), max(a, b))] = v
            k = tuple(str(m[q]) for q in PAIRS)
            if best is None or k < best:
                best = k
        return best

    classes = {}
    for mids in realizable:
        classes.setdefault(key(mids), []).append(mids)
    return {"dimension": d, "boxes": len(boxes), "positive": len(positive),
            "realizable": len(realizable), "classes": len(classes),
            "boundary_undecided": undecided,
            "class_sizes": sorted(len(v) for v in classes.values())}


if __name__ == "__main__":
    out = {}
    a = ART / "routeA.out"
    if a.exists() and a.stat().st_size:
        # route A variables: r12 r13 r14 r23 r24 r34 t  -> distances are 0..5
        out["routeA"] = analyze(a, 7, list(range(6)))
    b = ART / "routeB.out"
    if b.exists() and b.stat().st_size:
        # route B variables: z1..z4 k r12..r34 t -> distances are 5..10
        out["routeB"] = analyze(b, 12, list(range(5, 11)))
    (ART / "analysis.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    sys.exit(0)
