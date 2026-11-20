"""Generate the numbers, tables and figures of the primitive-points preprint from the archived computations.

Inputs (read-only), under problems/commutative-algebra/boij-soderberg-realizability/ of this repository:
  experiments/EXP-001-pure-ray-census/artifacts/results.json     the census of the 220 rays with d3 <= 12 over k[x,y,z]
  experiments/EXP-001-pure-ray-census/artifacts/qq-modules.json   the rational modules of the rays with d3 <= 9 (with hashes)
  experiments/EXP-001-pure-ray-census/artifacts/hits-manifest.json, background.json
  experiments/EXP-001-pure-ray-census/results-summary.md          the stage 1b count (rays pure at the Soderberg multiple)
  experiments/EXP-002-heisenberg-primitive-points/artifacts/results.json   Kostant modules, U/U(x^2,y^2), U/U(x^e,y^e), 2 by 3 quadrics
  experiments/EXP-003-heisenberg-characteristic-two/artifacts/results.json characteristic 2, the family, the bad primes
  context/references.md                                           SHA-256 of the archived sources
experiments/EXP-004-lift-certificates/artifacts/results.json, second-system.json   rank certificates for the lift to characteristic 0
Outputs (next to this script): numbers.tex, tab_*.tex (tabular bodies), fig_*.tex (tikzpicture bodies).

Besides reading artifacts, the script recomputes with exact integer and rational arithmetic the finite statements that the proofs of
the paper use: the normal-ordering identity, the Hilbert series identities, the dimension of every weight block of U/U(x^e,y^e) over Q
and over the primes up to 31 for e <= 8 (compared with the closed form of the proof and with the machine Hilbert functions), the set of
primes at which the module is not pure, the rays to which the characteristic 2 theorem applies, and the field scope of the table of
the 84 rays with d3 <= 9. A value that differs from the one the text relies on stops the script with exit 1.

Typed in this script, and so not read from an artifact (the complete list):
  - the notation table, the resolution of the trivial module with its maps, and the two diagrams (fig_resolution.tex, fig_char2.tex);
  - the names of the obstructions O1 to O6 and the module that realizes each of the ten rays (MODULE_OF), compared with the artifacts;
  - the labels of the procedures table and its arithmetic domains (the costs in it are read from the artifacts);
  - the three rays of the characteristic 2 theorem and the five rays realized in characteristic 2 by search (compared with the
    computed list and with EXP-003).
With --check nothing is written and the script exits 1 when a committed output differs from a fresh one.

Usage (from the repository root, with the repository .venv):
  python manuscripts/boij-soderberg-realizability/primitive-points-realizability/make_tables.py [--check]
"""
import argparse
import hashlib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PROBLEM = REPO / "problems" / "commutative-algebra" / "boij-soderberg-realizability"
E1 = PROBLEM / "experiments" / "EXP-001-pure-ray-census"
E2 = PROBLEM / "experiments" / "EXP-002-heisenberg-primitive-points"
E3 = PROBLEM / "experiments" / "EXP-003-heisenberg-characteristic-two"
E5 = PROBLEM / "experiments" / "EXP-005-characteristic-two-machine-checks"
E6 = PROBLEM / "experiments" / "EXP-006-odd-characteristic-below-2e"
E7 = PROBLEM / "experiments" / "EXP-007-pure-family-at-the-power-pair"
E8 = PROBLEM / "experiments" / "EXP-008-odd-characteristic-e5-e6"
E9 = PROBLEM / "experiments" / "EXP-009-linear-family-below-2e"
E11 = PROBLEM / "experiments" / "EXP-011-central-pair-machine-checks"
E12 = PROBLEM / "experiments" / "EXP-012-central-commutator-criterion"
E10 = PROBLEM / "experiments" / "EXP-010-weight-class-strata"
E13 = PROBLEM / "experiments" / "EXP-013-pull-back-scaling"
E14 = PROBLEM / "experiments" / "EXP-014-middle-strata"
REFS = PROBLEM / "context" / "references.md"

FAILS = []
OUT = {}


def need(cond, what):
    if not cond:
        FAILS.append(what)
        print(f"MISMATCH: {what}", file=sys.stderr)


def jload(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


TEXT_SUFFIXES = {".json", ".md", ".txt", ".py", ".tex"}


def norm_bytes(p):
    """The bytes of an artifact as committed: for a text artifact CRLF line ends are replaced by LF (a working copy checked out
    with CRLF hashes differently from the blob of the repository, whose line ends are LF)."""
    b = Path(p).read_bytes()
    return b.replace(b"\r\n", b"\n") if Path(p).suffix.lower() in TEXT_SUFFIXES else b


def sha(p):
    return hashlib.sha256(norm_bytes(p)).hexdigest()


def thousands(n):
    return f"{n:,}".replace(",", "{,}")


def macro(name, value):
    return "\\newcommand{\\n%s}{%s}" % (name, value)


def ray_str(d):
    return "(" + ",".join(str(x) for x in d) + ")"


def vec(b):
    return "(" + ",".join(str(x) for x in b) + ")"


def primes_upto(n):
    return [p for p in range(2, n + 1) if all(p % q for q in range(2, int(p ** 0.5) + 1))]


def table(colspec, header, rows, small=True):
    """A booktabs tabular as TeX; rows are lists of cell strings."""
    colspec = re.sub(r"p\{([^}]*)\}", lambda m: ">{\\raggedright\\arraybackslash}p{" + m.group(1) + "}", colspec)
    lines = ["\\begin{tabular}{%s}" % colspec, "\\toprule", " & ".join(header) + "\\\\", "\\midrule"]
    for r in rows:
        lines.append(" & ".join(r) + "\\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------------------------------------------------------
# exact recomputations used by the proofs
# --------------------------------------------------------------------------------------------------------------------------

def poly_mul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def poly_trim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def h_series(e):
    """(1 + ... + t^(e-1))^2 (1 + t^2 + ... + t^(2e-2)) as a coefficient list."""
    s = [1] * e
    q = [0] * (2 * e - 1)
    for i in range(e):
        q[2 * i] = 1
    return poly_mul(poly_mul(s, s), q)


def numerator(e):
    n = [0] * (4 * e + 1)
    n[0], n[e], n[3 * e], n[4 * e] = 1, -2, 2, -1
    return n


def series_div(num, den_factors, length):
    """Coefficients of num / prod(1 - t^k) for k in den_factors, to the given length."""
    c = list(num) + [0] * max(0, length - len(num))
    c = c[:length]
    for k in den_factors:
        for i in range(k, length):
            c[i] += c[i - k]
    return c


def weight_block_dim(e, w, n, p=None):
    """dim of the piece of weight w and degree 2n + w of U/U(x^e,y^e): |R_n| - rank of [(a!/a'!) binom(e, a-a')]."""
    rows = list(range(max(0, -w), min(n, e - 1) + 1))
    cols = list(range(max(0, e - w), n + 1))
    if not rows:
        return 0
    if not cols:
        return len(rows)
    m = []
    for ap in rows:
        r = []
        for a in cols:
            k = a - ap
            r.append((math.factorial(a) // math.factorial(ap)) * math.comb(e, k) if 0 <= k <= e else 0)
        m.append(r)
    return len(rows) - (rank_q(m) if p is None else rank_p(m, p))


def rank_q(m):
    m = [[Fraction(x) for x in r] for r in m]
    rk, ncol = 0, len(m[0]) if m else 0
    for c in range(ncol):
        piv = next((i for i in range(rk, len(m)) if m[i][c] != 0), None)
        if piv is None:
            continue
        m[rk], m[piv] = m[piv], m[rk]
        for i in range(len(m)):
            if i != rk and m[i][c] != 0:
                f = m[i][c] / m[rk][c]
                m[i] = [x - f * y for x, y in zip(m[i], m[rk])]
        rk += 1
    return rk


def rank_p(m, p):
    m = [[x % p for x in r] for r in m]
    rk, ncol = 0, len(m[0]) if m else 0
    for c in range(ncol):
        piv = next((i for i in range(rk, len(m)) if m[i][c] % p), None)
        if piv is None:
            continue
        m[rk], m[piv] = m[piv], m[rk]
        inv = pow(m[rk][c], -1, p)
        m[rk] = [(x * inv) % p for x in m[rk]]
        for i in range(len(m)):
            if i != rk and m[i][c] % p:
                f = m[i][c]
                m[i] = [(x - f * y) % p for x, y in zip(m[i], m[rk])]
        rk += 1
    return rk


def dq(e, w, n):
    """The closed form of step 4: min(n'+1, e-q) for n' <= e-1, max(0, 2e-1-q-n') for n' >= e; zero for |w| >= e."""
    q = abs(w)
    if q >= e:
        return 0
    npr = n - max(0, -w)
    if npr < 0:
        return 0
    return min(npr + 1, e - q) if npr <= e - 1 else max(0, 2 * e - 1 - q - npr)


def block_check(N):
    """Steps 2 to 4 and 7 of Theorem A by exact arithmetic, for 2 <= e <= 8."""
    res = {}
    for e in range(2, 9):
        nblocks = 0
        hf = defaultdict(int)
        for w in range(-e - 1, e + 2):
            for n in range(0, 3 * e + 2):
                dim = weight_block_dim(e, w, n)
                need(dim == dq(e, w, n), f"block e={e} w={w} n={n}: rank computation {dim} vs closed form {dq(e, w, n)}")
                nblocks += 1
                if dim and 2 * n + w >= 0:
                    hf[2 * n + w] += dim
        target = h_series(e)
        got = [hf.get(d, 0) for d in range(len(target) + 6)]
        need(got == target + [0] * 6, f"e={e}: Hilbert function from the blocks differs from h_e")
        need(sum(target) == e ** 3, f"e={e}: length differs from e^3")
        ok_primes, bad_primes = [], []
        for p in primes_upto(31):
            # characteristic p: unscaled matrices; pure Hilbert function iff every block equals the closed form
            same = all(weight_block_dim(e, w, n, p) == dq(e, w, n) for w in range(-e - 1, e + 2) for n in range(0, 3 * e + 2))
            top = weight_block_dim(e, 0, 2 * e - 1, p)
            if p >= 2 * e:
                need(same and top == 0, f"e={e} p={p}: expected the generic block dimensions")
                ok_primes.append(p)
            else:
                need(top > 0, f"e={e} p={p}: expected a nonzero piece in degree 4e-2 (step 7)")
                bad_primes.append(p)
        res[e] = (nblocks, len(ok_primes), len(bad_primes), bad_primes)
    N["blocksChecked"] = thousands(sum(v[0] for v in res.values()))
    N["blocksPrimes"] = len(primes_upto(31))
    return res


def numerator_checks(N):
    for e in range(1, 13):
        num = numerator(e)
        q = series_div(num, [1, 1, 2], 4 * e + 8)
        need(poly_trim(q) == h_series(e), f"e={e}: numerator / ((1-t)^2 (1-t^2)) differs from h_e")
    # the trapezoid grouping of step 4
    for e in range(1, 13):
        tot = [0] * (2 * e - 1)
        for w in range(-(e - 1), e):
            q = abs(w)
            for i in range(e - q):
                tot[q + 2 * i] += 1
        need(tot == poly_mul([1] * e, [1] * e), f"e={e}: trapezoid grouping differs from (1+...+t^(e-1))^2")
    N["numeratorE"] = 12
    # the resolution of the trivial module: Euler characteristic
    e1 = poly_mul(poly_mul([1, -1], [1, -1]), [1, 0, -1])
    need(poly_trim(e1) == [1, -2, 0, 2, -1], "Euler characteristic of the resolution of the trivial module")


class Pbw:
    """U(H) with PBW basis y^b x^a z^c (x to the right), xy = yx + z, z central; used to check the identities of the proofs."""

    @staticmethod
    def add(d, k, v):
        d[k] = d.get(k, 0) + v
        if d[k] == 0:
            del d[k]

    @classmethod
    def xleft(cls, elt):
        out = {}
        for (b, a, c), v in elt.items():
            # x y^b x^a z^c = y^b x^(a+1) z^c + b y^(b-1) x^a z^(c+1)
            cls.add(out, (b, a + 1, c), v)
            if b:
                cls.add(out, (b - 1, a, c + 1), b * v)
        return out

    @classmethod
    def yleft(cls, elt):
        return {(b + 1, a, c): v for (b, a, c), v in elt.items()}

    @classmethod
    def word(cls, w, coef=1):
        elt = {(0, 0, 0): coef}
        for ch in reversed(w):
            elt = cls.xleft(elt) if ch == "x" else cls.yleft(elt)
        return elt


def normal_ordering_check(N):
    """x^a y^e = sum_j j! C(a,j) C(e,j) z^j y^(e-j) x^(a-j), for a, e <= 9."""
    count = 0
    for a in range(0, 10):
        for e in range(0, 10):
            lhs = Pbw.word("x" * a + "y" * e)
            rhs = {}
            for j in range(0, min(a, e) + 1):
                Pbw.add(rhs, (e - j, a - j, j), math.factorial(j) * math.comb(a, j) * math.comb(e, j))
            need(lhs == rhs, f"normal ordering a={a} e={e}")
            count += 1
    N["normalOrderingCount"] = count
    # the two relations of step 6: y(yx - 2xy) + x y^2 = 0 and y x^2 - x(2yx - xy) = 0
    def comb(*terms):
        out = {}
        for coef, w in terms:
            for k, v in Pbw.word(w, coef).items():
                Pbw.add(out, k, v)
        return out
    need(comb((1, "yyx"), (-2, "yxy"), (1, "xyy")) == {}, "y(yx-2xy) + x y^2 is not zero in U")
    need(comb((1, "yxx"), (-2, "xyx"), (1, "xxy")) == {}, "y x^2 - x(2yx - xy) is not zero in U")
    # r1 = [x,[x,y]] and r2 = [y,[x,y]] vanish because z is central
    r1 = comb((1, "xxy"), (-2, "xyx"), (1, "yxx"))
    r2 = comb((1, "yyx"), (-2, "yxy"), (1, "xyy"))
    need(r1 == {} and r2 == {}, "r1 or r2 does not vanish")
    # characteristic 2: x^2 y - y x^2 = 2xz and y^2 x - x y^2 = -2yz
    d1 = comb((1, "xxy"), (-1, "yxx"))
    d2 = comb((1, "yyx"), (-1, "xyy"))
    need(d1 == {(0, 1, 1): 2} and d2 == {(1, 0, 1): -2}, "commutators of x^2 and y^2")
    # the centre in characteristic 2 and the multiplication table of step 1 (C-basis 1, x, y, yx)
    # x.yx = y x^2 + z x; yx.x = y x^2 ; (reduced modulo 2 the products are those of the table)
    t = comb((1, "xyx"))
    need(t == {(1, 2, 0): 1, (0, 1, 1): 1}, "x.yx = X y + Z x")
    N["pbwIdentities"] = 6


# --------------------------------------------------------------------------------------------------------------------------
# artifacts
# --------------------------------------------------------------------------------------------------------------------------

OBST = {"O1": "second syzygy", "O2": "codimension", "O3": "regularity", "O4": "even cyclic Gorenstein", "O5": "three relations", "O6": "dual"}
MODULE_OF = {  # typed: the module that realizes the primitive point over U in characteristic 0 (compared with EXP-002)
    (0, 1, 3, 4): "$k=U/U(x,y)=L(0,0)$",
    (0, 1, 5, 6): "$L(1,1)$",
    (0, 1, 7, 8): "$L(2,2)$",
    (0, 1, 9, 10): "$L(3,3)$",
    (0, 1, 11, 12): "$L(4,4)$",
    (0, 2, 6, 8): "$U/U(x^2,y^2)$",
    (0, 2, 10, 12): "coker of a $2\\times3$ matrix of quadrics",
    (0, 3, 5, 8): "$L(2,0)$",
    (0, 3, 9, 12): "$U/U(x^3,y^3)$",
    (0, 5, 7, 12): "$L(4,0)$",
    (0, 3, 7, 10): "$L(3,1)$",
}
CHAR2_THEOREM_RAYS = {(0, 2, 6, 8), (0, 3, 9, 12), (0, 2, 10, 12)}
CHAR2_SEARCH_RAYS = {(0, 1, 5, 6), (0, 1, 7, 8), (0, 1, 9, 10), (0, 1, 11, 12), (0, 3, 5, 8)}


def parse_pure_hf(key):
    m = re.match(r"\[([0-9, ]+)\]", key)
    return [int(x) for x in m.group(1).split(",")]


def eventual_value(hf):
    tail = hf[-4:]
    return tail[0] if len(set(tail)) == 1 else None


def read_all():
    d = {}
    d["r1"] = jload(E1 / "artifacts" / "results.json")
    d["qq"] = jload(E1 / "artifacts" / "qq-modules.json")
    d["bg"] = jload(E1 / "artifacts" / "background.json")
    d["r2"] = jload(E2 / "artifacts" / "results.json")
    d["r3"] = jload(E3 / "artifacts" / "results.json")
    d["summary1"] = (E1 / "results-summary.md").read_text(encoding="utf-8")
    d["notes1"] = (E1 / "artifacts" / "summary-notes.md").read_text(encoding="utf-8")
    d["refs"] = REFS.read_text(encoding="utf-8")
    return d


def classify_field(x):
    fs = {e["field"] for e in x["realized"].get("1", [])}
    if fs & {"any field", "infinite field"}:
        return "every"
    if "characteristic 0" in fs:
        return "zero"
    if fs:
        return "prime"
    return "none"


def census(d, N, F):
    r = d["r1"]
    rays = r["rays"]
    c = r["counts"]
    st = r["counts_by_stage"]
    N["rays"] = c["rays"]
    N["cyclic"] = c["cyclic_B0_1"]
    N["parityPassing"] = c["parity_passing"]
    N["realized"] = c["primitive_realized"]
    N["excluded"] = c["primitive_excluded"]
    N["open"] = c["primitive_open"]
    N["realizedZero"] = c["primitive_realized_char0"]
    N["realizedEvery"] = c["primitive_realized_any_or_infinite_field"]
    N["realizedPrimeOnly"] = c["primitive_realized"] - c["primitive_realized_char0"]
    N["cDetermined"] = c["c_determined"]
    N["raysLeNine"] = c["rays_d3_le_9"]
    N["conflicts"] = c["conflicts"]
    need(len(rays) == 220 and c["rays"] == 220, "220 rays")
    # status of each ray, recomputed
    status = Counter(x["status_primitive"] for x in rays)
    need(status["realized"] == 193 and status["excluded"] == 12 and status["open"] == 15, "status counts")
    cls = {tuple(x["d"]): classify_field(x) if x["status_primitive"] == "realized" else x["status_primitive"] for x in rays}
    n_every = sum(1 for v in cls.values() if v == "every")
    n_zero_or_more = sum(1 for v in cls.values() if v in ("every", "zero"))
    need(n_every == c["primitive_realized_any_or_infinite_field"], f"every-field count {n_every}")
    need(n_zero_or_more == c["primitive_realized_char0"], f"characteristic 0 count {n_zero_or_more}")
    N["realizedZeroOnly"] = n_zero_or_more - n_every
    F["cls"] = cls
    # stages
    names = ["stage 0", "after 1a", "after 1b", "after 1c", "after 1d (QQ rechecks)"]
    need(list(st.keys()) == names, f"stage keys {list(st.keys())}")
    labels = ["formulas and closures", "known-answer runs", "level-module family", "search", "rational rechecks"]
    rows = []
    for n, lab in zip(names, labels):
        s = st[n]
        rows.append([lab, str(s["primitive_realized"]), str(s["primitive_realized_any_or_infinite_field"]), str(s["primitive_realized_char0"]),
                     str(s["primitive_excluded"]), str(s["primitive_open"]), str(s["c_determined"])])
    OUT["tab_stage.tex"] = table("@{}lrrrrrr@{}", ["After", "realized", "every field", "char.\\ 0", "excluded", "open", "$c_d$ known"], rows)
    F["stages"] = [(lab, st[n]) for n, lab in zip(names, labels)]
    F["stage_rows"] = rows
    N["stageZeroRealized"] = st["stage 0"]["primitive_realized"]
    N["stageZeroOpen"] = st["stage 0"]["primitive_open"]
    N["stageZeroEvery"] = st["stage 0"]["primitive_realized_any_or_infinite_field"]
    N["stageZeroWeyman"] = st["stage 0"]["primitive_realized"] - st["stage 0"]["primitive_realized_any_or_infinite_field"]
    N["afterOneAOpen"] = st["after 1a"]["primitive_open"]
    # search
    o = r["outcomes"]
    N["cellsHit"], N["cellsMiss"], N["cellsErr"] = thousands(o["hit"]), thousands(o["miss"]), o["error"]
    N["cellsTotal"] = thousands(sum(o.values()))
    need(sum(o.values()) == len(r["search"]), "search cells")
    secs = sorted(v["seconds"] for v in r["search"].values() if "seconds" in v)
    N["cellSecondsTotal"] = thousands(round(sum(secs)))
    N["cellSecondsMedian"] = f"{secs[len(secs) // 2]:.2f}"
    N["cellSecondsMax"] = f"{secs[-1]:.0f}"
    wall = d["bg"]
    t0 = re.search(r"T(\d\d):(\d\d):(\d\d)", wall["last_start"])
    t1 = re.search(r"T(\d\d):(\d\d):(\d\d)", wall["finished"])
    a = int(t0.group(1)) * 3600 + int(t0.group(2)) * 60 + int(t0.group(3))
    b = int(t1.group(1)) * 3600 + int(t1.group(2)) * 60 + int(t1.group(3))
    N["searchWallMin"] = f"{(b - a) / 60:.0f}"
    sc = Counter((v["outcome"], v.get("stage")) for v in r["search"].values())
    N["hitsOneB"] = sc[("hit", "1b")]
    N["hitsOneC"] = sc[("hit", "1c")]
    N["hitsOneA"] = sc[("hit", "1a")]
    N["cellsOneE"] = sc[("hit", "1e")] + sc[("miss", "1e")] + sc[("error", "1e")]
    N["cellsMain"] = sum(sc.values()) - N["cellsOneE"]
    N["hitsMain"] = N["hitsOneA"] + N["hitsOneB"] + N["hitsOneC"]
    N["hitsFlag"] = sc[("hit", "1e")]
    need((N["cellsMain"], N["hitsMain"], N["hitsFlag"], N["cellsOneE"]) == (1046, 240, 1013, 1950), "search cells split")
    m = re.search(r"Rays pure on every finished seed at m = s/beta_0: (\d+) of (\d+)", d["summary1"])
    need(m is not None, "stage 1b line of results-summary.md")
    N["soderbergPure"], N["soderbergRays"] = m.group(1), m.group(2)
    # gates
    g = r["gates"]
    need(all(g[k].get("passed", True) for k in g), "a gate of EXP-001 did not pass")
    N["gatesPassed"] = len(g)
    N["gateThreeEach"] = g["G3"]["summary"]["32003"].split("/")[0]
    need(g["G7"]["pureCharFree_python"] == g["G7"]["pureCharFree_macaulay2"] == 15400 and g["G7"]["multiple"] == 3080, "G7")
    N["gateSevenES"] = g["G7"]["pureCharFree_macaulay2"]
    g5 = g["G5"]
    N["verified"], N["qqOk"], N["qqFailed"] = g5["verified"], g5["qq_ok"], len(g5["qq_failed"])
    N["qqTimeout"], N["qqNotRun"] = len(g5["qq_timeout"]), g5["qq_not_run"]
    N["qqCompleted"] = g5["qq_ok"]   # the recheck completed with a result on these; the two recorded failures ended without a result
    need(g5["qq_ok"] + len(g5["qq_failed"]) + len(g5["qq_timeout"]) + g5["qq_not_run"] == g5["verified"], "rechecks add up")
    m = re.search(r"(\d+) records with fresh=False were discarded", d["notes1"])
    need(m is not None, "discarded records line of summary-notes.md")
    N["discarded"] = m.group(1)
    # excluded table
    ex = [x for x in rays if x["status_primitive"] == "excluded"]
    rows = []
    for x in sorted(ex, key=lambda x: x["d"]):
        dd = tuple(x["d"])
        codes = x["excluded"]["1"]
        direct = [k for k in codes if not k.startswith("O6")]
        dual = [k for k in codes if k.startswith("O6")]
        dtxt = ", ".join(direct)
        duals = ", ".join(sorted(set(dual[0].split(":")[1].split("+")))) if dual else ""
        mod = MODULE_OF.get(dd)
        rows.append(["$" + ray_str(dd) + "$", "$" + vec(x["beta"]) + "$", str(x["parity"]), dtxt + (" (dual: " + duals + ")" if duals else ""),
                     str(x["low"]) if x["low"] == x["up"] else f"{x['low']}--{x['up']}", mod if mod else "none ($p(-1)\\ne0$)"])
        if mod is None:
            need(x["parity"] != 0, f"excluded ray {dd} without module has parity 0")
        else:
            need(x["parity"] == 0, f"excluded ray {dd} with module has parity != 0")
        need(x["low"] == 2 and x["up"] == 2, f"c_d of {dd}")
    OUT["tab_excluded.tex"] = table("@{}lllllp{3.6cm}@{}", ["ray", "primitive point", "$p(-1)$", "obstructions (O1 to O6)", "$c_d$", "module over $U$"], rows)
    N["excludedParityPass"] = sum(1 for x in ex if x["parity"] == 0)
    N["excludedParityFail"] = sum(1 for x in ex if x["parity"] != 0)
    # open rays
    op = sorted([x for x in rays if x["status_primitive"] == "open"], key=lambda x: x["d"])
    rows = [["$" + ray_str(x["d"]) + "$", "$" + vec(x["beta"]) + "$", str(x["parity"]), str(x["low"]), str(x["up"]), "$" + ray_str(x["dual"]) + "$"] for x in op]
    OUT["tab_open.tex"] = table("@{}lllrrl@{}", ["ray", "primitive point", "$p(-1)$", "$c_d \\ge$", "$c_d \\le$", "dual ray"], rows)
    need(all(x["d"][3] >= 10 for x in op), "open rays have d3 >= 10")
    N["openMaxUp"] = max(x["up"] for x in op)
    N["openParityZero"] = sum(1 for x in op if x["parity"] == 0)
    # the rays with d3 <= 9
    low9 = [x for x in rays if x["d"][3] <= 9]
    need(len(low9) == 84, "84 rays with d3 <= 9")
    kinds = Counter()
    scope = Counter()
    formula_routes = {"Eisenbud-Schreyer", "EFW Weyman", "EFW two-invariant", "Koszul", "S/m^a", "dual of S/m^a", "Buchsbaum-Rim", "generic Pfaffians"}
    for x in low9:
        if x["status_primitive"] == "excluded":
            kinds["excluded"] += 1
            continue
        ent = [e for e in x["realized"].get("1", []) if e["field"] in ("any field", "infinite field", "characteristic 0")]
        routes = {e["route"] for e in ent}
        if routes & formula_routes:
            kinds["formula"] += 1
        elif routes == {"scaling"}:
            kinds["scaling"] += 1
        elif routes == {"duality"}:
            kinds["dual"] += 1
        elif routes <= {"QQ recheck of search:socle", "QQ recheck of search:module"} and routes:
            kinds["socle" if "QQ recheck of search:socle" in routes else "module"] += 1
        else:
            need(False, f"unclassified ray {x['d']}: {routes}")
        scope[classify_field(x)] += 1
    need((kinds["formula"], kinds["scaling"], kinds["socle"] + kinds["module"], kinds["dual"], kinds["excluded"]) == (35, 2, 29, 13, 5),
         f"evidence classes {dict(kinds)}")
    need((kinds["socle"], kinds["module"]) == (14, 15), f"level module and presentation hits {kinds}")
    need((scope["every"], scope["zero"]) == (29, 50), f"field scope {dict(scope)}")
    for k in ("formula", "scaling", "socle", "module", "dual", "excluded"):
        N["lowNine" + k.capitalize()] = kinds[k]
    N["lowNineEvery"], N["lowNineZero"] = scope["every"], scope["zero"]
    # split of the 29 every-field rays: any field and infinite field
    anyf = sum(1 for x in low9 if x["status_primitive"] == "realized" and any(e["field"] == "any field" for e in x["realized"]["1"]))
    inf = scope["every"] - anyf
    need((anyf, inf) == (26, 3), f"any field / infinite field split {(anyf, inf)}")
    N["lowNineAny"], N["lowNineInfinite"] = anyf, inf
    f_any = f_inf = f_zero = 0
    for x in low9:
        if x["status_primitive"] == "excluded":
            continue
        ent = [e for e in x["realized"].get("1", []) if e["field"] in ("any field", "infinite field", "characteristic 0")]
        if not ({e["route"] for e in ent} & formula_routes):
            continue
        fl = {e["field"] for e in ent if e["route"] in formula_routes}
        if "any field" in fl:
            f_any += 1
        elif "infinite field" in fl:
            f_inf += 1
        else:
            f_zero += 1
    need((f_any, f_inf, f_zero) == (24, 3, 8) and f_any + f_inf + f_zero == kinds["formula"], f"formula rays by field {(f_any, f_inf, f_zero)}")
    N["formulaAny"], N["formulaInf"], N["formulaZero"] = f_any, f_inf, f_zero
    rows = [
        ["formula: Eisenbud--Schreyer, the two Eisenbud--Fl{\\o}ystad--Weyman constructions, Koszul, $S/\\mathfrak m^a$ and its dual, Buchsbaum--Rim, or generic Pfaffians", str(kinds["formula"]), "%d any field, %d infinite field, %d characteristic 0 only" % (f_any, f_inf, f_zero)],
        ["scaling of a formula ray (flat base change $x_i\\mapsto x_i^2$)", str(kinds["scaling"]), "any field"],
        ["explicit module over $\\mathbb{Q}$, level-module generator", str(kinds["socle"]), "characteristic 0"],
        ["explicit module over $\\mathbb{Q}$, generic presentation", str(kinds["module"]), "characteristic 0"],
        ["$\\mathrm{Ext}^3$ dual of a module of the two previous rows", str(kinds["dual"]), "characteristic 0"],
        ["excluded over $S$, realized over $U$ (Table~\\ref{tab:ten})", str(kinds["excluded"]), "characteristic 0"],
        ["total", "84", "79 over $S$, 5 over $U$"],
    ]
    # the 8 = formula rays carried only by EFW Weyman with characteristic 0
    only_zero_formula = sum(1 for x in low9 if x["status_primitive"] == "realized" and classify_field(x) == "zero" and
                            {e["route"] for e in x["realized"]["1"] if e["field"] == "characteristic 0"} & formula_routes)
    need(only_zero_formula == 8, f"formula rays with characteristic 0 scope {only_zero_formula}")
    need(rows[0][2] == "%d any field, %d infinite field, %d characteristic 0 only" % (anyf - kinds["scaling"], inf, only_zero_formula), "field-scope cell of tab_lownine differs from the artifact counts")
    OUT["tab_lownine.tex"] = table("@{}p{7.6cm}rp{3.8cm}@{}", ["evidence for the primitive point", "rays", "field scope"], rows)
    # qq modules
    q = d["qq"]
    mods = q["modules"]
    qc = q["counts"]
    N["qqModules"], N["qqWithDual"], N["qqDualsPure"] = qc["modules"], qc["with_dual"], qc["duals_pure"]
    need(qc["modules"] == len(mods), "qq-modules.json counts")
    need(len({tuple(m_["ray"]) for m_ in mods}) == 29, "29 rays with an explicit rational module")
    N["qqRays"] = 29
    mod_rays = {tuple(m_["ray"]) for m_ in mods}
    direct = [m_ for m_ in mods if m_.get("ext3_dual") and m_["ext3_dual"].get("pure") and tuple(m_["ext3_dual"]["ray"]) not in mod_rays]
    N["qqDualsDirect"] = len(direct)
    N["qqDualsClosure"] = 13 - len(direct)
    pure = sum(1 for m_ in mods if m_.get("equals_primitive_point"))
    need(pure == len(mods) and qc["pure"] == pure, "a rational module of qq-modules.json is not pure")
    N["qqPure"] = pure
    N["qqFileCount"] = sum(len(m_.get("files", [])) for m_ in mods)
    F["lowNine"] = low9
    return rays


MANIFEST = [  # (label printed, path relative to the repository root): the artifacts whose bytes and hash the paper prints
    ("hits-manifest.json", "experiments/EXP-001-pure-ray-census/artifacts/hits-manifest.json"),
    ("qq-modules.json", "experiments/EXP-001-pure-ray-census/artifacts/qq-modules.json"),
    ("EXP-005/results.json", "experiments/EXP-005-characteristic-two-machine-checks/artifacts/results.json"),
    ("EXP-006/results.json", "experiments/EXP-006-odd-characteristic-below-2e/artifacts/results.json"),
    ("EXP-007/results.json", "experiments/EXP-007-pure-family-at-the-power-pair/artifacts/results.json"),
    ("EXP-008/results.json", "experiments/EXP-008-odd-characteristic-e5-e6/artifacts/results.json"),
    ("EXP-009/results.json", "experiments/EXP-009-linear-family-below-2e/artifacts/results.json"),
    ("EXP-011/results.json", "experiments/EXP-011-central-pair-machine-checks/artifacts/results.json"),
    ("EXP-012/results.json", "experiments/EXP-012-central-commutator-criterion/artifacts/results.json"),
    ("EXP-010/results.json", "experiments/EXP-010-weight-class-strata/artifacts/results.json"),
    ("EXP-013/results.json", "experiments/EXP-013-pull-back-scaling/artifacts/results.json"),
    ("EXP-014/results.json", "experiments/EXP-014-middle-strata/artifacts/results.json"),
    ("EXP-015/results.json", "experiments/EXP-015-linear-rule-and-e9/artifacts/results.json"),
    ("EXP-017/results.json", "experiments/EXP-017-odd-stratum-filter/artifacts/results.json"),
    ("EXP-017/stored.json", "experiments/EXP-017-odd-stratum-filter/artifacts/stored-members-filter.json"),
    ("EXP-016/results.json", "experiments/EXP-016-congruence-lists/artifacts/results.json"),
    ("EXP-018/results.json", "experiments/EXP-018-largest-exponent-strata/artifacts/results.json"),
    ("EXP-019/results.json", "experiments/EXP-019-filter-every-exponent/artifacts/results.json"),
    ("EXP-020/results.json", "experiments/EXP-020-symmetric-members/artifacts/results.json"),
]
PROBLEM_REL = "problems/commutative-algebra/boij-soderberg-realizability"


def manifest_files():
    return [(lab, PROBLEM / rel) for lab, rel in MANIFEST]


def hash_table(d, N):
    rows = []
    for line in d["refs"].splitlines():
        m = re.match(r"\|\s*([^|\s]+\.(?:pdf|md))\s*\|\s*(.*?)\s*\|\s*`([0-9a-f]{64})`\s*\|\s*(\[[^\]]*\])", line)
        if not m:
            continue
        fname, src, h, mark = m.groups()
        label = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", src)
        label = label.split(",")[0] if "arXiv" not in label else label
        short = re.search(r"arXiv:((?:[a-z-]+/)?[0-9.]+(?:v\d)?)", src)
        rows.append((fname, short.group(1) if short else "raw output", h, mark))
    need(len(rows) == 15, f"references.md lists {len(rows)} archived sources")
    N["sourcesArchived"] = len(rows)
    body = []
    for fname, ident, h, mark in rows:
        body.append(["{\\scriptsize\\path{" + fname + "}}", ident, mark.replace("[", "").replace("]", ""),
                     "\\texttt{\\scriptsize " + h[:32] + "\\allowbreak " + h[32:] + "}"])
    OUT["tab_sources.tex"] = table("@{}p{4.4cm}p{2.6cm}p{0.9cm}p{5.8cm}@{}", ["archived file", "arXiv", "read", "SHA-256"], body)
    # hashes of the manifests
    body = []
    for n_, p_ in manifest_files():
        h = sha(p_)
        body.append(["\\texttt{" + n_ + "}", str(len(norm_bytes(p_))), "\\texttt{\\scriptsize " + h[:32] + "\\allowbreak " + h[32:] + "}"])
    OUT["tab_manifests.tex"] = table("@{}p{4.2cm}rp{7cm}@{}", ["artifact", "bytes", "SHA-256"], body)
    hm = jload(E1 / "artifacts" / "hits-manifest.json")
    N["hitFiles"] = thousands(len(hm) if isinstance(hm, list) else len(hm.get("hits", hm)))


def kostant_and_ten(d, N, rays, F):
    r2 = d["r2"]
    c = r2["claims"]
    need(r2["status"] == "complete", "EXP-002 status")
    N["twoWall"] = f"{r2['wall_seconds']:.0f}"
    cases = {x["name"]: x for x in c["C0"]["cases"]}
    need(c["C0"]["all_ok"], "EXP-002 calibration")
    N["calibModules"] = len(cases)
    kos = [n for n in cases if n.startswith("L(")]
    N["kostantCount"] = len(kos)
    rows = []
    for n in sorted(kos, key=lambda s: (int(s[2]), int(s[4]))):
        p, q = int(n[2]), int(n[4])
        x = cases[n]
        exp = [[0, 0, q + 1], [1, p - q + 1, p + 2], [2, p + q + 3, p + 2], [3, 2 * p + 4, q + 1]]
        need(x["betti_I1"] == exp and x["betti_I2"] == exp, f"{n}: table differs from (q+1, p+2, p+2, q+1)")
        need(x["total_dimension"] == (p - q + 1) * (q + 1) * (p + 2) * (p + q + 3) // 6, f"{n}: dimension differs from the Weyl dimension")
        need(x["agree"] and x["module_is_UH_module"] and x["dimension_matches_weyl"], f"{n}: flags")
        rows.append(["$L(%d,%d)$" % (p, q), str(x["total_dimension"]), "$" + vec(x["hilbert_function"]) + "$", "$" + vec([t[2] for t in x["betti_I1"]]) + "$",
                     "$" + vec([0] + [t[1] for t in x["betti_I1"][1:]]) + "$"])
    OUT["tab_kostant.tex"] = table("@{}lrlll@{}", ["module", "length", "Hilbert function", "Betti numbers", "degrees $(d_0,d_1,d_2,d_3)$"], rows)
    # agreement
    agree = sum(1 for x in c["C0"]["cases"] if x["agree"])
    N["calibAgree"] = agree
    # ten rays and their modules
    low = {tuple(x["d"]): x for x in rays}
    c1 = c["C1"]["fields"]
    qq1 = next(x for x in c1 if x["field"] == "QQ")
    gf1 = next(x for x in c1 if x["field"] == "GF(32003)")
    need(qq1["hilbert_function"] == [1, 2, 2, 2, 1] and qq1["table_equals_primitive_pure"] and gf1["table_equals_primitive_pure"], "C1")
    N["oneIdealDims"] = ", ".join(str(qq1["ideal_pieces"][k]["dimension"]) for k in ("2", "3", "4", "5"))
    c3 = {x["name"]: x for x in c["C3"]["cases"]}
    c4 = c["C4"]
    need(c4["hits_of_10"] == {"GF(32003)": 10, "QQ": 10}, "C4 hits")
    modrows = []
    spec = [
        ((0, 1, 3, 4), cases["L(0,0)"], "$k=U/U(x,y)=L(0,0)$"),
        ((0, 1, 5, 6), cases["L(1,1)"], "$L(1,1)$"),
        ((0, 1, 7, 8), cases["L(2,2)"], "$L(2,2)$"),
        ((0, 1, 9, 10), cases["L(3,3)"], "$L(3,3)$"),
        ((0, 1, 11, 12), cases["L(4,4)"], "$L(4,4)$"),
        ((0, 2, 6, 8), qq1, "$U/U(x^2,y^2)$"),
        ((0, 2, 10, 12), None, "coker of a $2\\times3$ matrix of quadrics"),
        ((0, 3, 5, 8), cases["L(2,0)"], "$L(2,0)$"),
        ((0, 3, 9, 12), c3["U/U(x3,y3)"], "$U/U(x^3,y^3)$"),
        ((0, 5, 7, 12), cases["L(4,0)"], "$L(4,0)$"),
        ((0, 3, 7, 10), cases["L(3,1)"], "$L(3,1)$"),
    ]
    c4first = next(x for x in c4["cases"] if x["field"] == "QQ") if any(x["field"] == "QQ" for x in c4["cases"]) else c4["cases"][0]
    for dd, x, label in spec:
        if x is None:
            x = c4first
        beta = low[dd]["beta"]
        got = [t[2] for t in x["betti_I1"]]
        degs = [t[1] for t in x["betti_I1"]]
        need(got == beta and degs == list(dd), f"module of {dd}: table {got} on {degs} differs from the primitive point {beta}")
        need(x["agree"] if "agree" in x else True, f"module of {dd}: instruments disagree")
        stS = low[dd]["status_primitive"]
        modrows.append(["$" + ray_str(dd) + "$", "$" + vec(beta) + "$", label, str(x["total_dimension"]), "$" + vec(x["hilbert_function"]) + "$",
                        "excluded" if stS == "excluded" else "open"])
    OUT["tab_ten.tex"] = table("@{}llp{3.9cm}rp{4cm}l@{}", ["ray", "primitive point", "module over $U$ (char.\\ 0)", "length", "Hilbert function", "over $S$"], modrows)
    N["tenRays"] = 10
    # C4 numbers
    N["fourSeeds"] = len(c4["seeds"])
    need(all(x.get("table_equals_primitive_pure", x.get("agree")) for x in c4["cases"]), "C4 pure tables")
    # C5: random pairs of quadrics in characteristic 2 and 3
    rows = []
    for f in c["C5"]["fields"]:
        rows.append([f["field"].replace("^", "\\textasciicircum{}") if False else "$" + re.sub(r"\^(\d)", r"^{\1}", f["field"].replace("GF(", "\\mathrm{GF}(")) + "$",
                     str(len(f["seeds"])), str(f["finite"]), str(f["infinite_or_unfinished"]), str(f["table_hits"])])
    OUT["tab_pairs.tex"] = table("@{}lrrrr@{}", ["field", "pairs", "finite length", "not finished at degree 14", "table $(1,2,2,1)$ on $(0,2,6,8)$"], rows)
    f2 = [f for f in c["C5"]["fields"] if f["field"].startswith("GF(2")]
    f3 = [f for f in c["C5"]["fields"] if f["field"].startswith("GF(3")]
    N["pairsCharTwo"] = sum(len(f["seeds"]) for f in f2)
    N["pairsCharTwoFinite"] = sum(f["finite"] for f in f2)
    need(N["pairsCharTwoFinite"] == 0, "EXP-002 C5: a pair of quadrics of finite length in characteristic 2")
    N["pairsCharThree"] = sum(len(f["seeds"]) for f in f3)
    N["pairsCharThreeHits"] = sum(f["table_hits"] for f in f3)
    gf3 = next(f for f in c["C5"]["fields"] if f["field"] == "GF(3)")
    gf9 = next(f for f in c["C5"]["fields"] if f["field"] == "GF(3^2)")
    N["gfThreeHits"], N["gfNineHits"], N["gfNineFinite"] = gf3["table_hits"], gf9["table_hits"], gf9["finite"]
    N["gfTwentySevenHits"] = next(f for f in c["C5"]["fields"] if f["field"] == "GF(3^3)")["table_hits"]
    N["gfEightyOneHits"] = next(f for f in c["C5"]["fields"] if f["field"] == "GF(3^4)")["table_hits"]
    # wrong tables with the right Hilbert function
    wrong = 0
    for f in c["C5"]["fields"]:
        if not f["field"].startswith("GF(3"):
            continue
        for h, n_ in f["hilbert_counts"].items():
            if h == "[1, 2, 2, 2, 1]":
                wrong += n_
    N["pairsRightHF"] = wrong
    N["pairsRightHFWrongTable"] = wrong - N["pairsCharThreeHits"]
    # an explicit pair over GF(3) read from the artifact
    explicit = None
    for f in c["C5"]["fields"]:
        if f["field"] == "GF(3)" and f["hits"]:
            h = f["hits"][0]
            explicit = h
    F["gf3hit"] = explicit
    # C6 duality
    c6 = c["C6"]
    N["dualCases"] = len(c6["cases"])
    N["dualHolds"] = c6["duality_holds_count"]
    need(c6["duality_holds_count"] == len(c6["cases"]), "C6 duality")
    # C2
    for f in c["C2"]["fields"]:
        need(not f["finite_length"], "C2: a finite quotient in characteristic 2 or 3")
    # instruments
    N["twoPairs"] = 96
    # C3 range
    N["twoLengths"] = ", ".join(str(c3[k]["total_dimension"]) for k in ("U/U(x3,y3)",))
    return cases


def char_two(d, N, rays, F):
    r3 = d["r3"]
    t = r3["tasks"]
    need(r3["status"] == "complete", "EXP-003 status")
    N["threeWall"] = f"{r3['wall_seconds']:.1f}"
    N["threeCalib"] = len(r3["C0"]["cases"])
    # A1, A2
    rows = []
    agg = {}
    for fld in ("GF(2)", "GF(2^2)", "GF(2^4)", "GF(2^8)"):
        recs = []
        total = None
        for k, v in t.items():
            if (k.startswith("A1:") or k.startswith("A2:")) and v["field"] == fld:
                recs += v["records"]
                total = v["total_subspaces"]
        recs.sort(key=lambda r_: r_["index"])
        n = len(recs)
        cen = Counter(r_["derivation"]["central_dimension"] for r_ in recs)
        det0 = sum(1 for r_ in recs if r_["derivation"]["central_dimension"] == 1 and r_["derivation"]["det_is_zero"])
        detdeg = sorted({r_["derivation"]["det_degree"] for r_ in recs if r_["derivation"].get("det_degree")})
        nz = sum(1 for r_ in recs if r_["nonzero_every_degree_2_to_20"])
        ev = Counter(eventual_value(r_["hilbert_0_to_20"]) for r_ in recs)
        growing = {r_["index"] for r_ in recs if eventual_value(r_["hilbert_0_to_20"]) is None}
        zero_det = {r_["index"] for r_ in recs if r_["derivation"]["central_dimension"] == 1 and r_["derivation"]["det_is_zero"]}
        need(growing == zero_det, f"{fld}: the subspaces with a growing Hilbert function are not exactly those with det = 0")
        agg[fld] = (n, nz, cen, det0, detdeg, ev)
        need(n == total, f"A1/A2 {fld}: {n} records, {total} subspaces")
        need(nz == n, f"A1/A2 {fld}: a quotient is zero in some degree")
        rows.append(["$\\mathrm{GF}(%s)$" % fld[3:-1].replace("^", "^") if False else "$\\mathrm{GF}(%s)$" % fld[3:-1], str(n), str(nz), str(cen.get(0, 0)),
                     str(cen.get(1, 0)), str(cen.get(2, 0)), str(det0), "$%s$" % ",".join(str(x) for x in detdeg) if detdeg else "-", str(ev.get(2, 0)), str(n - ev.get(2, 0))])
    OUT["tab_char2.tex"] = table("@{}lrrrrrrlrr@{}", ["field", "subspaces", "nonzero", "$c=0$", "$c=1$", "$c=2$", "$\\det=0$", "$\\deg\\det$", "eventually 2", "growing"], rows)
    need(agg["GF(2)"][0] == 35 and agg["GF(2^2)"][0] == 357, "Gaussian binomials 35 and 357")
    N["subGFtwo"], N["subGFfour"] = agg["GF(2)"][0], agg["GF(2^2)"][0]
    N["subGFsixteen"], N["subGFtwofiftysix"] = agg["GF(2^4)"][0], agg["GF(2^8)"][0]
    N["centralOneTwo"], N["centralTwoTwo"] = agg["GF(2)"][2][1], agg["GF(2)"][2][2]
    N["centralOneFour"], N["centralTwoFour"] = agg["GF(2^2)"][2][1], agg["GF(2^2)"][2][2]
    N["detZeroTwo"], N["detZeroFour"] = agg["GF(2)"][3], agg["GF(2^2)"][3]
    N["detNonzeroTwo"], N["detNonzeroFour"] = agg["GF(2)"][2][1] - agg["GF(2)"][3], agg["GF(2^2)"][2][1] - agg["GF(2^2)"][3]
    need((N["detNonzeroTwo"], N["detNonzeroFour"]) == (22, 326), "determinant of degree 8 on 22 and 326 subspaces")
    N["evTwoGFtwo"] = agg["GF(2)"][5].get(2, 0)
    N["growGFtwo"] = N["subGFtwo"] - N["evTwoGFtwo"]
    need(N["evTwoGFtwo"] == 29 and N["growGFtwo"] == 6, "29 eventually constant 2, 6 growing over GF(2)")
    # B1
    byray = defaultdict(dict)
    for k, v in t.items():
        if k.startswith("B1:"):
            byray[tuple(v["ray"])][v["field"]] = v
    rays_b1 = sorted(byray)
    need(len(rays_b1) == 8, "eight rays in B1")
    rows = []
    for dd in rays_b1:
        v = byray[dd]
        any_ = next(iter(v.values()))
        cells = []
        for fld in ("GF(32003)", "GF(2)", "GF(2^2)", "GF(2^4)"):
            x = v[fld]
            rate = x["hits"] / x["seeds"]
            se = (rate * (1 - rate) / x["seeds"]) ** 0.5
            cells.append(f"{x['hits']}/{x['seeds']}, ${rate:.2f}\\pm{se:.2f}$")
        rows.append(["$" + ray_str(dd) + "$", "$%d\\times%d$, $d_1=%d$" % (any_["B0"], any_["B1"], any_["d1"])] + cells)
    OUT["tab_b1.tex"] = table("@{}lp{2cm}p{2.2cm}p{2.2cm}p{2.2cm}p{2.2cm}@{}", ["ray", "presentation", "$\\mathrm{GF}(32003)$", "$\\mathrm{GF}(2)$", "$\\mathrm{GF}(4)$", "$\\mathrm{GF}(16)$"], rows)
    hit2 = {dd for dd in rays_b1 if any(byray[dd][f]["hits"] > 0 for f in ("GF(2)", "GF(2^2)", "GF(2^4)"))}
    need(hit2 == CHAR2_SEARCH_RAYS, f"rays hit in characteristic 2: {sorted(hit2)}")
    nohit = {dd for dd in rays_b1 if byray[dd]["GF(32003)"]["hits"] > 0 and all(byray[dd][f]["hits"] == 0 for f in ("GF(2)", "GF(2^2)", "GF(2^4)"))}
    need(nohit == {(0, 3, 9, 12), (0, 2, 10, 12)}, f"rays hit over GF(32003) and never in characteristic 2: {sorted(nohit)}")
    need(byray[(0, 5, 7, 12)]["GF(32003)"]["hits"] == 0, "(0,5,7,12) not hit over GF(32003)")
    N["bOneSeedsControl"] = byray[(0, 2, 10, 12)]["GF(32003)"]["seeds"]
    for tag, dd in (("Six", (0, 1, 5, 6)), ("Eight", (0, 1, 7, 8)), ("FiveEight", (0, 3, 5, 8))):
        for fk, fn in (("GF(2)", "Two"), ("GF(2^2)", "Four"), ("GF(2^4)", "Sixteen")):
            N["bOne" + tag + fn] = byray[dd][fk]["hits"]
    N["bOneSeedsCharTwo"] = byray[(0, 2, 10, 12)]["GF(2)"]["seeds"]
    # eventual Hilbert values predicted by the intersection numbers
    def pred(e, a):
        m = e // 2
        ll = 2 * m * m if e % 2 == 0 else 2 * m * (m + 1)
        return ll * a * (a + 1) // 2
    pv = {}
    for dd, e_, a_ in (((0, 3, 9, 12), 3, 1), ((0, 2, 10, 12), 2, 2)):
        pv[dd] = pred(e_, a_)
        row = {}
        for fld in ("GF(2)", "GF(2^2)", "GF(2^4)"):
            hc = byray[dd][fld]["hilbert_counts"]
            n_ev = 0
            for key, cnt in hc.items():
                hf = parse_pure_hf(key)
                if eventual_value(hf) == pv[dd] and not hf[-1] == 0:
                    n_ev += cnt
            row[fld] = n_ev
        pv[dd] = (pv[dd], row)
    need(pv[(0, 3, 9, 12)][0] == 4 and pv[(0, 2, 10, 12)][0] == 6, "predicted eventual values 4 and 6")
    N["evCubicTwo"], N["evCubicFour"], N["evCubicSixteen"] = (pv[(0, 3, 9, 12)][1][f] for f in ("GF(2)", "GF(2^2)", "GF(2^4)"))
    N["evQuadTwo"], N["evQuadFour"], N["evQuadSixteen"] = (pv[(0, 2, 10, 12)][1][f] for f in ("GF(2)", "GF(2^2)", "GF(2^4)"))
    need((N["evCubicTwo"], N["evCubicFour"], N["evCubicSixteen"]) == (34, 39, 40), f"cubic pairs eventually 4: {N['evCubicTwo'], N['evCubicFour'], N['evCubicSixteen']}")
    need((N["evQuadTwo"], N["evQuadFour"], N["evQuadSixteen"]) == (28, 39, 40), f"2x3 quadrics eventually 6: {N['evQuadTwo'], N['evQuadFour'], N['evQuadSixteen']}")
    # the table of eventual values from the theory
    rows = []
    for name, e_, a_, b_ in (("two quadrics", 2, 1, 2), ("two cubics", 3, 1, 2), ("two quartics", 4, 1, 2), ("two quintics", 5, 1, 2),
                             ("$2\\times3$ matrix of quadrics", 2, 2, 3), ("$2\\times3$ matrix of cubics", 3, 2, 3)):
        m_ = e_ // 2
        ll = 2 * m_ * m_ if e_ % 2 == 0 else 2 * m_ * (m_ + 1)
        rows.append([name, str(e_), str(m_), ("$2m^2=%d$" if e_ % 2 == 0 else "$2m(m+1)=%d$") % ll if a_ == 1 else "$\\tfrac{a(a+1)}{2}\\cdot%d=%d$" % (ll, pred(e_, a_)), str(pred(e_, a_))])
    OUT["tab_eventual.tex"] = table("@{}lrrll@{}", ["presentation", "$e$", "$m$", "predicted eventual value", "number"], rows)
    # C1, C2, C3
    rows = []
    c1 = {int(k.split(":")[1]): v for k, v in t.items() if k.startswith("C1:") and k.endswith(":QQ")}
    c2 = {v["e"]: v for k, v in t.items() if k.startswith("C2:")}
    c3 = {v["e"]: v for k, v in t.items() if k.startswith("C3:")}
    secs = {}
    for e in range(2, 9):
        v = c1[e]
        need(v["hilbert_function"] == h_series(e), f"C1 e={e}: machine Hilbert function differs from h_e")
        need(v["total_dimension"] == e ** 3 and v["hilbert_equals_product_formula"] and v["weight_pieces_equal_D_q"], f"C1 e={e} flags")
        need(v["socle"] == {f"{4 * e - 4},0": 1} and v["socle_is_weight0_degree_4e_minus_4_dim1"], f"C1 e={e}: socle")
        need(v["kernel_y"]["kernel_y_equals_span_of_z_c_g_a"], f"C1 e={e}: kernel of y")
        # the weight pieces equal the closed form
        for key, val in v["weight_pieces"].items():
            w_, d_ = (int(s) for s in key.split(","))
            n_ = (d_ - w_) // 2
            need(dq(e, w_, n_) == val, f"C1 e={e} piece {key}")
        nz_formula = sum(1 for w_ in range(-e + 1, e) for n_ in range(0, 3 * e) if dq(e, w_, n_) > 0)
        need(nz_formula == len(v["weight_pieces"]), f"C1 e={e}: number of nonzero pieces")
        bad = c3[e]["observed_non_pure_primes"] if e in c3 else None
        if e in c3:
            need(bad == [p for p in primes_upto(23) if p < 2 * e], f"C3 e={e}: observed bad primes {bad}")
            need(c3[e]["observed_equals_predicted"], f"C3 e={e}: observed differs from the predicted set")
        rows.append([str(e), str(v["total_dimension"]), "$(%d,0)$" % (4 * e - 4), str(len(v["weight_pieces"])),
                     ("$\\{%s\\}$" % ",".join(map(str, bad))) if bad is not None else "--",
                     "yes" if e in c2 and c2[e]["blocks_equal_prediction"] else "--", f"{v['seconds']:.1f}"])
        secs[e] = v["seconds"]
    OUT["tab_family.tex"] = table("@{}rrlrp{3.1cm}lr@{}", ["$e$", "length $e^3$", "socle (degree, weight)", "nonzero pieces", "primes $\\le23$ with a non-pure quotient", "$k[z]$-pattern", "seconds"], rows)
    N["familyMaxE"] = 8
    N["familySecondsMax"] = f"{max(secs.values()):.1f}"
    N["familyPiecesEFour"] = len(c1[4]["weight_pieces"])
    F["c1"] = c1
    F["c3"] = c3
    # D1
    d1 = {v["e"]: v for k, v in t.items() if k.startswith("D1:")}
    for e in (2, 3):
        need(d1[e]["pure_count"] == d1[e]["pairs_count"], f"D1 e={e}")
    for e in (4, 5, 10):
        need(d1[e]["pure_count"] == 0 and d1[e]["all_hilbert_equal_maxrank"], f"D1 e={e}")
    N["generalPairs"] = d1[4]["pairs_count"]
    N["generalPureTwoThree"] = d1[2]["pure_count"]
    N["generalPureFourFiveTen"] = sum(d1[e]["pure_count"] for e in (4, 5, 10))
    # the negative coefficient at degree 4e-4 of (1 - 2t^e)/((1-t)^2(1-t^2))
    need(series_div([1, 0, 0, 0, -2], [1, 1, 2], 13)[12] == -1, "coefficient of t^12 in (1-2t^4)/((1-t)^2(1-t^2))")
    # for e = 4 the series (1-2t^4)/((1-t)^2(1-t^2)) in degree 12: 49 - 50 (two terms)
    s4 = series_div([1], [1, 1, 2], 13)[12]
    s4b = series_div([1], [1, 1, 2], 13)[8]
    need(s4 == 49 and 2 * s4b == 50, f"degree 12 coefficient of 1/((1-t)^2(1-t^2)) is {s4}, twice degree 8 is {2 * s4b}")
    # D2
    d2 = t["D2"]
    cub = d2["random_matrices_of_cubics"]["seeds"]
    need(all(x["table_equals_primitive_pure"] for x in cub), "D2 pure")
    N["dTwoSeeds"] = len(cub)
    sub = d2["substitution_in_L11"]
    N["dTwoSubs"] = len(sub) if isinstance(sub, list) else len(sub.get("cases", sub))
    # instrument agreement of EXP-003
    # unique-pair counts are quoted from results-summary.md of EXP-003
    # procedures: seconds per claim
    byclaim = defaultdict(float)
    for k, v in t.items():
        byclaim[k.split(":")[0]] += v.get("task_seconds", 0)
    N["threeSecA"] = f"{byclaim['A1'] + byclaim['A2']:.0f}"
    N["threeSecB"] = f"{byclaim['B1']:.0f}"
    N["threeSecC"] = f"{byclaim['C1'] + byclaim['C2'] + byclaim['C3']:.0f}"
    N["threeSecD"] = f"{byclaim['D1'] + byclaim['D2']:.0f}"
    return t


def char_two_rays(rays, N):
    """The rays with beta_1 = beta_0 + 1 and d_1 >= 2 (Corollary 2 of Theorem B)."""
    cand = [x for x in rays if x["beta"][1] == x["beta"][0] + 1]
    need(len(cand) == 8 and sum(1 for x in cand if x["d"][1] == 1) == 5, "eight rays with beta_1 = beta_0 + 1, five with d_1 = 1")
    need(all(x["parity"] == 0 for x in cand), "these eight rays pass the parity test")
    app = {tuple(x["d"]) for x in cand if x["d"][1] >= 2}
    need(app == CHAR2_THEOREM_RAYS, f"rays of Corollary 2: {sorted(app)}")
    N["betaOneRays"] = len(cand)
    N["betaOneRaysDone"] = sum(1 for x in cand if x["d"][1] == 1)
    N["thmRays"] = len(app)
    ten = {tuple(x["d"]) for x in rays if x["parity"] == 0 and x["status_primitive"] == "excluded"}
    need(len(ten) == 10, "ten parity-passing excluded rays")
    return cand


# --------------------------------------------------------------------------------------------------------------------------
# static tables
# --------------------------------------------------------------------------------------------------------------------------

def static_tables(N):
    notation = [
        ["$k$", "a field; $\\operatorname{char}k$ its characteristic", "Section~\\ref{sec:rings}"],
        ["$S=k[x,y,z]$", "polynomial ring, $\\deg x=\\deg y=\\deg z=1$", "Section~\\ref{sec:rings}"],
        ["$U=U(H)$", "$k\\langle x,y,z\\rangle/(xy-yx-z,\\ xz-zx,\\ yz-zy)$, $\\deg x=\\deg y=1$, $\\deg z=2$", "Section~\\ref{sec:rings}"],
        ["$y^bx^az^c$", "PBW basis of $U$, weight $w=b-a$", "Section~\\ref{sec:rings}"],
        ["$d=(0,d_1,d_2,d_3)$", "degree sequence; $\\beta_d$ its primitive point", "Section~\\ref{sec:parity}"],
        ["$p_\\beta(t)$", "$\\sum_i(-1)^i\\beta_it^{d_i}$, numerator of the Hilbert series", "Section~\\ref{sec:parity}"],
        ["$c_d(k)$", "least $m$ with $m\\beta_d$ the Betti table of a finite length module over $S\\otimes k$; $k$ of characteristic 0 unless stated", "Section~\\ref{sec:realizability}"],
        ["$M_e$", "$U/U(x^e,y^e)$", "Theorem~\\ref{thm:A}"],
        ["$h_e(t)$", "$(1+\\dots+t^{e-1})^2(1+t^2+\\dots+t^{2e-2})$", "Theorem~\\ref{thm:A}"],
        ["$P$, $N$", "$U/Ux^e$ and the image of $Uy^e$ in it", "Theorem~\\ref{thm:A}, step 1"],
        ["$T[R_n,C_n]$", "the matrix $[\\binom{e}{a-a'}]$ on rows $R_n$ and columns $C_n$", "Theorem~\\ref{thm:A}, step 2"],
        ["$D_q(n')$", "dimension of the block of weight $\\pm q$ and shifted $z$-degree $n'$", "Theorem~\\ref{thm:A}, step 4"],
        ["$C,\\ X,Y,Z$", "$k[X,Y,Z]$ with $X=x^2$, $Y=y^2$, $Z=z$ (characteristic 2)", "Theorem~\\ref{thm:B}"],
        ["$B,\\ \\Sigma$", "$C[t]/(t^2+Zt+XY)$ and $\\operatorname{Proj}B\\cong\\mathbb{P}^1\\times\\mathbb{P}^1$", "Theorem~\\ref{thm:C}"],
        ["$(a,b,e)$", "generators, relations and relation degree of a presentation", "Theorem~\\ref{thm:C}"],
        ["$u(n)$", "$\\dim U_n=\\lfloor(n+2)^2/4\\rfloor$ for $n\\ge0$, and $0$ for $n<0$", "Section~\\ref{sec:pairsetting}"],
        ["$G_e,\\ M_W$", "$\\operatorname{Gr}(2,U_e)$, of dimension $2(u(e)-2)$; the cyclic module $U/UW$ of $W\\in G_e$", "Section~\\ref{sec:pairsetting}"],
        ["$\\mu_n(W)$", "left multiplication $U_{n-e}\\otimes W\\to U_n$; $\\dim(M_W)_n=u(n)-\\operatorname{rank}\\mu_n(W)$", "Section~\\ref{sec:pairsetting}"],
        ["$h_e(n),\\ r$", "coefficient of $t^n$ in $h_e(t)$; $r=2u(2e)-2$", "Section~\\ref{sec:pairsetting}"],
        ["$P_e,\\ D_e,\\ R_e$", "pure spaces; spaces with $\\operatorname{rank}\\mu_{3e}\\le r$; spaces whose forms have a common factor modulo $z$", "Section~\\ref{sec:pairsetting}, Theorem~\\ref{thm:family}"],
        ["$W_0$, $S_e$", "$\\langle x^e,y^e\\rangle$; the span of the $e$-th powers of linear forms in $U_e$", "Theorem~\\ref{thm:family}"],
        ["$\\mathcal Z,\\ X,Y$", "$k[X,Y,z]$ with $X=x^p$, $Y=y^p$, the centre of $U$ in characteristic $p$ odd; $U(q)$ its fibre at a point $q$", "Section~\\ref{sec:rings}"],
        ["$\\omega,\\ U_{(n,w)}$", "class weight $b+c$ of $x^ay^bz^c$; the part of degree $n$ and class weight $w$; $u_k(n)$ the dimension of the part of class $k$ modulo $m$", "Section~\\ref{sec:rings}"],
        ["$S(m;i,j)$", "stratum of the planes $\\langle f,g\\rangle$ with $f,g$ of classes $i,j$ modulo $m$; admissible and refined admissible", "Section~\\ref{sec:strata}"],
        ["$V_e,\\ n(f),\\ D$", "forms $A+\\beta_1x+\\beta_2y$ with $A\\in\\mathcal Z_e$, $\\beta_i\\in\\mathcal Z_{e-1}$; $A^p+\\beta_1^pX+\\beta_2^pY$; $\\beta_1\\delta_2-\\beta_2\\delta_1$", "Section~\\ref{sec:criterion}"],
        ["$\\varphi,\\ U_\\varphi,\\ \\varphi^*M'$", "endomorphism of $U$ with $x\\mapsto f$, $y\\mapsto g$; $U$ as a right module through $\\varphi$; the pull-back of $M'$", "Section~\\ref{sec:scaling}"],
        ["{[MV]}, {[D]}, {[V]}, {[U]}, {[C]}", "machine-verified, proved here, read on the source, not confirmed, conjectural", "Section~\\ref{sec:results-list}"],
    ]
    OUT["tab_notation.tex"] = table("@{}p{2.7cm}p{9.2cm}l@{}", ["symbol", "meaning", "introduced in"], notation)
    trivial = [
        ["$0$", "$U$", "$0$", "$u\\mapsto$ augmentation ($x,y\\mapsto0$)"],
        ["$1$", "$U(-1)^2$", "$1$", "$(u,v)\\mapsto ux+vy$"],
        ["$2$", "$U(-3)^2$", "$3$", "$(s,t)\\mapsto(s,t)\\bigl(\\begin{smallmatrix}yx-2xy&x^2\\\\-y^2&2yx-xy\\end{smallmatrix}\\bigr)$"],
        ["$3$", "$U(-4)$", "$4$", "$w\\mapsto w\\,(y,\\,-x)$"],
    ]
    OUT["tab_trivial.tex"] = table("@{}clcl@{}", ["position", "free module", "generator degree", "map to the previous position"], trivial)
    # the Euler series of the resolution checked in numerator_checks()
    proc = [
        ["PBW product and quotient modules", "$\\mathbb{Q}$, $\\mathbb{F}_p$, $\\mathbb{F}_{2^r}$", "left ideal, degree by degree, row reduction", ""],
        ["Tor complex through the resolution of $k$", "same", "graded quotient with the actions of $x$ and $y$", ""],
        ["Plural resolution (second system)", "same", "left presentation, weights $(1,1,2)$", ""],
        ["Census of formulas, obstructions, closures", "$\\mathbb{Q}$", "220 rays", ""],
        ["Search: level modules and presentations", "$\\mathbb{F}_{32003}$", "one ray, one multiple, one seed", ""],
        ["Rational recheck of a hit", "$\\mathbb{Q}$", "integer lift of the generator matrix", ""],
    ]
    return proc


def lift_certificates(d, N, rays, F):
    """EXP-004: rank certificates for the lift to characteristic 0; its outcome, its two modules, its cost."""
    E4 = PROBLEM / "experiments" / "EXP-004-lift-certificates" / "artifacts"
    r4 = jload(E4 / "results.json")
    s4 = jload(E4 / "second-system.json")
    g = r4["gates"]
    need(all(g[k]["passed"] for k in ("G1", "G2", "G3", "G4")), "EXP-004 gates")
    N["fourMatrices"] = thousands(g["G1"]["detail"]["matrices"])
    N["fourHits"] = r4["hits_total"]
    N["fourKnown"] = g["G2"]["pass"]
    N["fourAgree"], N["fourCompared"] = g["G3"]["agree"], g["G3"]["compared"]
    N["fourUnitTests"] = re.match(r"(\d+) passed", g["G4"]["detail"]["summary"]).group(1)
    c = r4["counts"]
    need(c["all"] == {"fail": 0, "pass": 129, "undecided": 1}, "EXP-004 counts")
    need(r4["counts_with_second_instrument_completing"]["pass"] == 130, "EXP-004 130 passes")
    N["fourPassOne"], N["fourPassAll"] = c["all"]["pass"], 130
    N["fourRest"] = c["rest"]["pass"] + c["rest"]["undecided"]
    N["fourRestPass"] = c["rest"]["pass"]
    rr = r4["rays"]
    N["fourRaysOnly"] = rr["only_gf32003_rays"]
    r1rays = {tuple(x["d"]): x for x in rays}
    prime_rays = [dd for dd, x in r1rays.items() if x["status_primitive"] == "realized" and classify_field(x) == "prime"]
    need(len(prime_rays) == N["fourRaysOnly"] == 46, "46 rays realized over GF(32003) only")
    direct = {dd for dd in prime_rays if any(tuple(h["d"]) == dd and h["m"] == 1 and h["verdict_two_instruments"] == "pass" for h in r4["hits"])}
    dual = [dd for dd in prime_rays if dd not in direct and tuple(r1rays[dd]["dual"]) in direct]
    need(len(direct) + len(dual) == 46, "direct and dual rays sum to 46")
    need((0, 3, 10, 12) in direct, "(0,3,10,12) has a passing hit on the ray")
    N["fourDirect"], N["fourDual"] = len(direct), len(dual)
    N["fourCharZeroAfter"] = rr["census_closure"]["char0_after"]
    need(rr["census_closure"]["char0_before"] == N["realizedZero"] and rr["census_closure"]["realized_after"] == N["realized"], "EXP-004 census closure")
    need(N["fourCharZeroAfter"] + 2 == N["realized"], "191 plus the two rays decided by one matrix is 193")
    N["fourLargestRows"], N["fourLargestCols"] = r4["largest_matrix"]["rows"], r4["largest_matrix"]["cols"]
    N["fourLongestSec"] = f"{r4['longest_rank_qq_seconds']['seconds']:.0f}"
    tot = sum(h["seconds"] for h in r4["hits"])
    N["fourTotalSec"] = thousands(round(tot))
    N["fourMaxSecHit"] = f"{max(h['seconds'] for h in r4['hits']):.0f}"
    gp = g["G3"]["gp_only_on_flint_undecided"]
    need(len(gp) == 1 and gp[0]["tag"].startswith("0-3-10-12"), "the one matrix decided by one instrument")
    N["fourOneRows"], N["fourOneCols"] = gp[0]["rows"], gp[0]["cols"]
    need(r4["predictions"]["P3"]["contradiction_a_hit_passes"], "P3 refuted")
    rows = []
    for m_ in s4["modules"]:
        tag = m_["tag"]
        p3 = r4["p3_hits"][tag]
        need(all(x["rank_p"] == x["rank_qq"] for x in p3["degrees"]), f"{tag}: ranks differ")
        dd = tuple(m_["ray"])
        beta = next(x for x in rays if tuple(x["d"]) == dd)["beta"]
        need([t[2] for t in m_["betti_table_over_QQ"]] == beta and [t[1] for t in m_["betti_table_over_QQ"]] == list(dd), f"{tag}: Singular table")
        need(m_["length"] == sum(x["hilbert"] for x in p3["degrees"]), f"{tag}: length differs from the sum of the Hilbert function")
        rows.append(["$" + ray_str(dd) + "$", "$" + vec(beta) + "$", "no result (run ended at about 110 s)", "equal in all %d degrees" % len(p3["degrees"]),
                     "$" + vec([t[2] for t in m_["betti_table_over_QQ"]]) + "$", str(m_["length"]), str(m_["seconds"])])
    lift_rows = rows
    scope_rows = [
        ["over every field or every infinite field", str(N["realizedEvery"]), "formula or standard complex, any field or infinite field [V]; scaling [D]", "yes"],
        ["characteristic 0 only", str(N["realizedZeroOnly"]), "formula valid in characteristic 0, or a resolution over $\\mathbb{Q}$ of a lifted hit, or its dual [V, MV]", "yes"],
        ["over $\\mathbb{F}_{32003}$ by a hit of the search", str(N["realizedPrimeOnly"]), "hit, rank certificate and Proposition~\\ref{prop:lift} [D, MV]", "yes"],
        ["total", str(N["realized"]), "", "%s" % N["realized"]],
    ]
    need(N["realizedEvery"] + N["realizedZeroOnly"] + N["realizedPrimeOnly"] == N["realized"], "scope rows add up")
    need(scope_rows[0][1] == "52" and scope_rows[1][1] == "95" and scope_rows[2][1] == "46" and scope_rows[3][1] == "193", "field-scope table differs from the artifact counts")
    OUT["tab_scope.tex"] = table("@{}p{4.2cm}rp{6.2cm}r@{}", ["group of rays", "rays", "evidence for the primitive point and its mark", "in characteristic 0"], scope_rows)
    N["fourLenA"], N["fourLenB"] = s4["modules"][0]["length"], s4["modules"][1]["length"]
    last = dict(F["stages"][-1][1])
    cert = dict(last, primitive_realized_char0=N["realized"])
    F["stages"].append(("rank certificates", cert))
    F["stage_rows"].append(["rank certificates", str(cert["primitive_realized"]), str(cert["primitive_realized_any_or_infinite_field"]), str(cert["primitive_realized_char0"]),
                            str(cert["primitive_excluded"]), str(cert["primitive_open"]), str(cert["c_determined"])])
    OUT["tab_stage.tex"] = table("@{}lrrrrrr@{}", ["After", "realized", "every field", "char.\\ 0", "excluded", "open", "$c_d$ known"], F["stage_rows"])
    OUT["tab_lift.tex"] = table("@{}p{2.1cm}p{2cm}p{1.8cm}p{2.2cm}p{2.2cm}rr@{}", ["ray", "primitive point", "Macaulay2 over $\\mathbb{Q}$", "rank test", "Singular over $\\mathbb{Q}$", "length", "seconds"], lift_rows)
    need(len(lift_rows) == 2 and sorted(r_[5] for r_ in lift_rows) == ["280", "396"], "tab_lift rows are not the two disputed modules")


def controls(d, N):
    """The table of controls and what each one caught; numbers read from the summaries and results of the three experiments."""
    s2 = (E2 / "results-summary.md").read_text(encoding="utf-8")
    s3 = (E3 / "results-summary.md").read_text(encoding="utf-8")
    m = re.search(r"Modules with both an I1 and an I2 table: (\d+); of these the tables agree in (\d+) and differ in (\d+)", s2)
    need(m is not None and m.group(1) == m.group(2) and m.group(3) == "0", "instrument agreement of EXP-002")
    N["agreeTwo"] = m.group(2)
    m = re.search(r"agree True = (\d+), False = (\d+)", s3)
    need(m is not None and m.group(2) == "0", "instrument agreement of EXP-003")
    N["agreeThree"] = m.group(1)
    m = re.search(r"pure table on (\d+), (\d+) and (\d+) of the (\d+) generators \((\d+), (\d+) and (\d+) of (\d+) seeds\)", d["notes1"])
    need(m is not None, "stage 1e line of summary-notes.md")
    N["flagTwo"], N["flagThree"], N["flagFive"], N["flagGen"] = m.group(1), m.group(2), m.group(3), m.group(4)
    N["flagSeedsTwo"], N["flagSeedsThree"], N["flagSeedsFive"], N["flagSeeds"] = m.group(5), m.group(6), m.group(7), m.group(8)
    m = re.search(r"never hit in 5 seeds on (\d+) rays over GF\(2\) and on (\d+) rays over GF\(3\)", d["notes1"])
    need(m is not None, "never-hit line of summary-notes.md")
    N["flagRaysTwo"], N["flagRaysThree"] = m.group(1), m.group(2)
    r = d["r1"]
    need(r["gates"]["G4"]["passed"], "G4")
    rows = [
        ["known-answer modules before any claim", "instruments and conventions",
         "%s modules of EXP-002 and %s of EXP-003 reproduce their expected tables; the two instruments agree on %s and %s finite length modules" % (N["calibModules"], N["threeCalib"], N["agreeTwo"], N["agreeThree"])],
        ["a hit on a point excluded by O1 to O6", "obstructions and constructions", "none in the %s cells of the search and the flags" % N["cellsTotal"]],
        ["lift of each hit to $\\mathbb{Q}$", "persistence of a prime-field hit", "%s rechecks completed, all pure; the runs on $(0,3,8,10)$ and $(0,3,11,12)$ ended without a result and were recorded as failures; the rank test passes on both and Singular over $\\mathbb{Q}$ gives the pure tables" % N["qqOk"]],
        ["first version of the rational recheck script", "the recheck itself", "a shadowed variable made %s fresh-process records fail; they were discarded and recomputed" % N["discarded"]],
        ["positive control over $\\mathbb{F}_{32003}$ for the characteristic 2 searches", "reach of generic presentations",
         "seven of the eight rays hit on %s of %s seeds, against zero hits in characteristic 2 on $(0,3,9,12)$ and $(0,2,10,12)$; $(0,5,7,12)$ is not hit in any field" % (N["bOneSeedsControl"], N["bOneSeedsControl"])],
        ["pairs of quadrics over $\\mathbb{F}_3,\\dots,\\mathbb{F}_{81}$", "Hilbert function as a certificate",
         "%s pairs have the Hilbert function $(1,2,2,2,1)$, %s of them have the table $(1,2,2,1)$ and %s have extra Betti numbers" % (N["pairsRightHF"], N["pairsCharThreeHits"], N["pairsRightHFWrongTable"])],
        ["a general pair of forms of degree $e$", "whether $(x^e,y^e)$ is special", "pure for $e=2,3$ on %s of %s pairs each; pure on %s of %s pairs for $e=4,5,10$" % (N["generalPureTwoThree"], N["generalPairs"], N["generalPureFourFiveTen"], 3 * N["generalPairs"])],
        ["generic modules over $\\mathbb{F}_2$, $\\mathbb{F}_3$, $\\mathbb{F}_5$ for the %s verified generators" % N["flagGen"], "small-characteristic behaviour of the search",
         "at least one of five seeds is pure on %s, %s and %s generators; a miss is a flag and no statement" % (N["flagTwo"], N["flagThree"], N["flagFive"])],
    ]
    OUT["tab_controls.tex"] = table("@{}p{4.3cm}p{3.1cm}p{6.1cm}@{}", ["control", "what it tests", "outcome"], rows)


def procedures(d, N, cases):
    r3 = d["r3"]
    c1 = r3["tasks"]["C1:8:QQ"]["seconds"]
    c0 = d["r2"]["claims"]["C0"]["cases"]
    i1 = max(x["seconds_I1"] for x in c0)
    i2 = max(x["seconds_I2"] for x in c0)
    N["calibMaxOne"] = f"{i1:.2f}"
    N["calibMaxTwo"] = f"{i2:.2f}"
    rows = [
        ["Exact quotient of $U$ by a left ideal, Tor complex (Algorithm~\\ref{alg:module})", "$\\mathbb{Q}$, $\\mathbb{F}_p$, $\\mathbb{F}_{2^r}$",
         "$e=8$ over $\\mathbb{Q}$: %.1f s; calibration modules: at most %.2f s" % (c1, i1)],
        ["Resolution in Plural, degrees read from the generators of each syzygy module", "same", "calibration modules: at most %.2f s" % i2],
        ["Census (Algorithm~\\ref{alg:census})", "$\\mathbb{Q}$", "220 rays; not timed separately"],
        ["Search (Algorithm~\\ref{alg:search}) and characteristic flags", "$\\mathbb{F}_{32003}$; flags $\\mathbb{F}_2,\\mathbb{F}_3,\\mathbb{F}_5$", "%s cells, of which %s over $\\mathbb{F}_{32003}$ (%s hits) and %s characteristic flags; %s s of summed process time for all of them, median %s s, maximum %s s, %s min wall time" % (N["cellsTotal"], N["cellsMain"], N["hitsMain"], N["cellsOneE"], N["cellSecondsTotal"], N["cellSecondsMedian"], N["cellSecondsMax"], N["searchWallMin"])],
        ["Rational recheck (Algorithm~\\ref{alg:recheck})", "$\\mathbb{Q}$", "%s completed rechecks, %s runs without a result, %s stopped at the 30 minute limit" % (N["qqCompleted"], N["qqFailed"], N["qqTimeout"])],
        ["Rank certificate of a lift (Algorithm~\\ref{alg:rank})", "$\\mathbb{Q}$ and $\\mathbb{F}_{32003}$",
         "%s hits, %s s of summed time; largest matrix $%s\\times%s$; longest rank over $\\mathbb{Q}$ %s s" % (N["fourHits"], N["fourTotalSec"], N["fourLargestRows"], N["fourLargestCols"], N["fourLongestSec"])],
        ["Characteristic 2 enumerations and searches", "$\\mathbb{F}_{2^r}$", "%s s of summed task time in total, %s s wall time" % (N["threeSecA"], N["threeWall"])],
        ["Archived checks of the characteristic 2 theorem", "$\\mathbb{F}_{2^r}$, $\\mathbb{F}_{32003}$, $\\mathbb{Q}$, $\\mathbb{F}_p$", "%s presentations and 24 modules; %s s wall time" % (N["fiveCasesAll"], N["fiveWall"])],
        ["Search for pure pairs of forms (Algorithm~\\ref{alg:pairs})", "$\\mathbb{F}_q$, $q\\le27$", "%s spaces in 12 families and fields, %s s of summed process time, %s min wall time (EXP-006); %s spaces in 3 families stopped early, %s s, %s min (EXP-008)" % (N["sixSpacesTotal"], N["sixCpu"], N["sixWallMin"], N["eightSpacesTotal"], N["eightCpu"], N["eightWallMin"])],
        ["Tangent space of the rank locus (Algorithm~\\ref{alg:tangent})", "$\\mathbb{Q}$, $\\mathbb{F}_p$", "all cases of Section~\\ref{sec:resfamily}: %s s wall time" % N["sevenWall"]],
        ["Enumeration of the linear family (Algorithm~\\ref{alg:lf})", "$\\mathbb{F}_p$, $\\mathbb{F}_{p^2}$", "%s members over $\\mathbb{F}_p$ in the fifteen pairs below $2e$ and %s over $\\mathbb{F}_{p^2}$; %s min wall time" % (N["lfFamilyMembersBelow"], N["lfYMembers"], N["lfWallMin"])],
        ["Central pairs of Theorem~\\ref{thm:central}", "$\\mathbb{F}_p$", "%s cases, both instruments: %s s wall time" % (N["cenCases"], N["cenSeconds"])],
        ["Criterion of Theorem~\\ref{thm:crit} (Algorithm~\\ref{alg:crit})", "$\\mathbb{F}_p$", "%s explicit pairs and %s random pairs: %s s of summed time for the random families" % (N["critXCases"], N["critRandomPairs"], N["critRSeconds"])],
    ]
    # the census runs in seconds: read from the experiment note of the hypothesis (stage 0 "seconds") -> not an artifact: keep the text
    OUT["tab_procedures.tex"] = table("@{}p{5.6cm}p{2.6cm}p{5.2cm}@{}", ["procedure", "arithmetic", "measured cost"], rows)


# --------------------------------------------------------------------------------------------------------------------------
# EXP-005 (characteristic 2 machine checks), EXP-006 (odd characteristic below 2e), EXP-007 (the family of pure pairs)
# --------------------------------------------------------------------------------------------------------------------------

def UN(n):
    """u(n) = dim U_n = floor((n+2)^2/4) for n >= 0, and 0 for n < 0."""
    return 0 if n < 0 else (n + 2) ** 2 // 4


def he_val(e, n):
    """The Hilbert function of the pure table (1,2,2,1) on (0,e,3e,4e): u(n) - 2u(n-e) + 2u(n-3e) - u(n-4e)."""
    return UN(n) - 2 * UN(n - e) + 2 * UN(n - 3 * e) - UN(n - 4 * e)


def target_rank(e):
    """r = 2u(2e) - 2, the rank of left multiplication into degree 3e of a pure pair."""
    return 2 * UN(2 * e) - 2


EW = {3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven"}


def fld_parse(name):
    m = re.match(r"GF\((\d+)(?:\^(\d+))?\)$", name)
    need(m is not None, f"field name {name}")
    n, k = int(m.group(1)), m.group(2)
    if k is not None:
        return n, int(k)
    # GF(n) with n the order of the field (GF(9), GF(25), GF(27)) or a prime
    for pr in primes_upto(n):
        if n % pr == 0:
            kk, t = 0, n
            while t % pr == 0:
                t //= pr
                kk += 1
            need(t == 1, f"field order {n} is not a prime power")
            return pr, kk
    return n, 1


def fld_tex(name):
    p, k = fld_parse(name)
    return "$\\F_{%d}$" % (p ** k)


def pct(x, nd=1):
    """100 x with nd decimals, rounded half up on the decimal representation of x (43.55 prints 43.6, not 43.5)."""
    from decimal import Decimal, ROUND_HALF_UP
    return str((Decimal(repr(x)) * 100).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP))


def pctv(x):
    """A share in percent with two decimals, three below 0.1 percent."""
    return pct(x, 2) if x >= 0.001 else pct(x, 3)


def heuristic(e, q):
    """q^(-(dim G_e - (4e-4))) = q^(-2 h_e(3e)); None at e = 3, where the pure set is open in G_3 and no comparison is made."""
    h = he_val(e, 3 * e)
    return None if h == 0 else q ** (-2 * h)


FAMW = {"A1": "AOne", "A2": "ATwo", "B1": "BOne", "B2": "BTwo", "B3": "BThree", "C": "C"}
FLDW = {"GF(3)": "Three", "GF(5)": "Five", "GF(7)": "Seven", "GF(9)": "Nine", "GF(11)": "Eleven", "GF(13)": "Thirteen",
        "GF(25)": "TwentyFive", "GF(27)": "TwentySeven"}


def mono_tex(i, j, k):
    parts = []
    for v, x in (("x", i), ("y", j), ("z", k)):
        if x == 1:
            parts.append(v)
        elif x > 1:
            parts.append("%s^{%d}" % (v, x))
    return "".join(parts) or "1"


def poly_tex(terms, p=None):
    """terms: list of ((i, j, k), coefficient); the monomial x^i y^j z^k is the product in this order; coefficients modulo p
    are printed as the representatives of least absolute value."""
    items = []
    for (i, j, k), c in sorted(terms, key=lambda t: (-t[0][0], -t[0][2], -t[0][1])):
        c = int(c)
        if p:
            c %= p
            if c > p // 2:
                c -= p
        if c == 0:
            continue
        m = mono_tex(i, j, k)
        a = abs(c)
        body = m if (a == 1 and m != "1") else (str(a) + m if m != "1" else str(a))
        items.append(("-" if c < 0 else "+", body))
    s = ""
    for n, (sg, b) in enumerate(items):
        s += (("-" if sg == "-" else "") + b) if n == 0 else " %s %s" % (sg, b)
    return s


def elt_from_terms(terms):
    out = {}
    for (i, j, k), c in terms:
        for (b, a, cc), v in Pbw.word("x" * i + "y" * j, int(c)).items():
            Pbw.add(out, (b, a, cc + k), v)
    return out


def mul_left(mono, elt):
    b, a, c = mono
    cur = {(bb, aa, cc + c): v for (bb, aa, cc), v in elt.items()}
    for _ in range(a):
        cur = Pbw.xleft(cur)
    for _ in range(b):
        cur = Pbw.yleft(cur)
    return cur


def basis_deg(d):
    """The PBW monomials y^b x^a z^c of degree d, as (b, a, c)."""
    return [(d - 2 * c - a, a, c) for c in range(d // 2 + 1) for a in range(d - 2 * c + 1)]


def mu_rank(forms, e, n, p=None):
    """Rank of left multiplication U_(n-e) tensor W -> U_n, W spanned by the elements `forms` (dictionaries in the PBW basis)."""
    if n < e:
        return 0
    cols = {m: i for i, m in enumerate(basis_deg(n))}
    rows = []
    for mono in basis_deg(n - e):
        for f in forms:
            r = [0] * len(cols)
            for key, v in mul_left(mono, f).items():
                r[cols[key]] = v
            rows.append(r)
    return rank_p(rows, p) if p else rank_q(rows)


_HF_CACHE = {}


def hilbert_pair(terms_pair, e, p, nmax):
    """Hilbert function of U/(U f + U g) in degrees 0..nmax by exact arithmetic of this script."""
    key = (p, e, nmax, repr(terms_pair))
    if key not in _HF_CACHE:
        forms = [elt_from_terms(t) for t in terms_pair]
        _HF_CACHE[key] = [UN(n) - mu_rank(forms, e, n, p) for n in range(nmax + 1)]
    return _HF_CACHE[key]


def read_artifacts(root):
    ex = Path(root) / "experiments"
    return (jload(ex / E5.name / "artifacts" / "results.json"), jload(ex / E6.name / "artifacts" / "results.json"),
            jload(ex / E7.name / "artifacts" / "results.json"), jload(ex / E8.name / "artifacts" / "results.json"))


# ---- EXP-005 ----

FAM5 = {
    "C1a": ((1, 2, 2), "all two-dimensional subspaces of $U_2$"),
    "C1b": ((1, 2, 3), "all two-dimensional subspaces of $U_3$"),
    "C1c": ((1, 1, 3), "all one-dimensional subspaces of $U_3$"),
    "C2a": ((1, 2, 4), "random pairs of quartics"),
    "C2b": ((1, 2, 5), "random pairs of quintics"),
    "C2c": ((1, 2, 6), "random pairs of sextics"),
    "C2d": ((1, 2, 7), "random pairs of septics"),
    "C2e": ((2, 3, 3), "random $2\\times3$ matrices of cubics"),
    "C2f": ((2, 3, 2), "random $2\\times3$ matrices of quadrics"),
    "C2g": ((3, 4, 2), "random $3\\times4$ matrices of quadrics"),
}
SHAPES5 = [(1, 3, 2), (1, 3, 3), (1, 3, 4), (2, 4, 2)]


def exp5(r5, N, out):
    need(r5["experiment"] == "EXP-005", "EXP-005 results file")
    for g in ("G1", "G2", "G3", "G4"):
        need(r5["gates"][g]["passed"] is True, f"EXP-005 gate {g}")
    cases = r5["cases"]
    by = defaultdict(Counter)
    for c in cases.values():
        fam = c["family"]
        need(c["status"] == "done", f"EXP-005 case {c['id']} unfinished")
        if fam in FAM5:
            need((c["a"], c["b"], c["e"]) == FAM5[fam][0], f"EXP-005 {c['id']}: shape differs from the family")
        elif fam == "C3":
            need((c["a"], c["b"], c["e"]) in SHAPES5, f"EXP-005 {c['id']}: shape of C3")
        else:
            need(False, f"EXP-005 unknown family {fam}")
        k = (fam, c["field"])
        by[k]["cases"] += 1
        by[k][c["cls"]] += 1
        if c["cls"] == "eventually constant":
            by[k]["val%d" % c["value"]] += 1
    pff = r5["totals"]["per_family_field"]
    for (fam, fld), cnt in by.items():
        if fam == "C3":
            continue
        t = pff[f"{fam}|{fld}"]
        need(t["cases"] == cnt["cases"], f"EXP-005 {fam}|{fld}: case count {t['cases']} vs {cnt['cases']}")
        need(t["growing"] == cnt["growing"], f"EXP-005 {fam}|{fld}: growing {t['growing']} vs {cnt['growing']}")
        need(t["eventually_constant"] == cnt["eventually constant"], f"EXP-005 {fam}|{fld}: eventually constant")
        need(t["finite_length"] == cnt["finite length"] == 0, f"EXP-005 {fam}|{fld}: a case of finite length")
        need(t["unclassified"] == 0 and t["unfinished"] == 0, f"EXP-005 {fam}|{fld}: unclassified or unfinished")
        vals = {int(v): n for v, n in t["constant_values"].items()}
        need(all(cnt["val%d" % v] == n for v, n in vals.items()) and sum(vals.values()) == t["eventually_constant"], f"EXP-005 {fam}|{fld}: values")
    # the eventual values predicted by the theorem: a(a+1)/2 L.L with L.L = 2m^2 (e = 2m) or 2m(m+1) (e = 2m+1)
    def predicted(a, e):
        m = e // 2
        ll = 2 * m * m if e % 2 == 0 else 2 * m * (m + 1)
        return a * (a + 1) // 2 * ll
    for fam, ((a, b, e), _) in FAM5.items():
        if b == a + 1:
            for fld in {f for (f2, f) in by if f2 == fam}:
                t = pff[f"{fam}|{fld}"]
                need(set(map(int, t["constant_values"])) <= {predicted(a, e)}, f"EXP-005 {fam}|{fld}: eventual value differs from a(a+1)/2 L.L = {predicted(a, e)}")
    need(set(map(int, pff["C1c|GF(2)"]["constant_values"])) == set() and pff["C1c|GF(2)"]["growing"] == 63, "EXP-005: every single cubic grows")
    p = r5["totals"]["predictions"]
    need(p["P1"]["holds"] and p["P4"]["holds"] and all(v["holds"] for v in p["P3"].values()), "EXP-005 predictions P1, P3, P4")
    need(all(p["P2"][k] for k in ("holds_value", "holds_no_unclassified", "holds_gf16_share", "holds_c1c_all_grow")), "EXP-005 prediction P2")
    done = sum(1 for c in cases.values() if c["family"] != "C3")
    need(p["P1"]["cases_done"] == done and p["P1"]["finite_length"] == 0, "EXP-005: cases of C1 and C2 with finite length")
    exh = sum(pff[k]["cases"] for k in ("C1a|GF(2)", "C1b|GF(2)", "C1c|GF(2)"))
    ba1 = [k for k in pff if k.split("|")[0] in ("C1a", "C1b", "C2a", "C2b", "C2c", "C2d", "C2e", "C2f", "C2g")]
    n_ba1 = sum(pff[k]["cases"] for k in ba1)
    n_const = sum(pff[k]["eventually_constant"] for k in ba1)
    n_grow = sum(pff[k]["growing"] for k in ba1)
    need(p["P2"]["cases_b_eq_a_plus_1_done"] == n_ba1 and p["P2"]["eventually_constant"] == n_const, "EXP-005: counts of the cases with b = a + 1")
    gr = p["P2"]["growing_by_field"]
    need(sum(v[0] for v in gr.values()) == n_grow, "EXP-005: growing cases by field")
    c3 = r5["totals"]["c3_per_shape"]
    for sh in SHAPES5:
        t = c3[str(sh)]
        need(t["cases"] == 10 and t["finite_length"] >= 8 and t["unfinished"] == 0, f"EXP-005 C3 {sh}")
    c4 = r5["c4"]
    need(len(c4) == 24, "EXP-005 C4 modules")
    c4rows = {}
    for cid, c in c4.items():
        e = c["e"]
        fld = c["field"]
        pr = 0 if fld == "QQ" else int(fld[3:-1])
        should = fld == "QQ" or pr >= 2 * e
        need(c["pure_table_I1"] == should and c["pure_table_I2"] == should and c["finite_length"] == should, f"EXP-005 C4 {cid}: purity differs from the rule char = 0 or >= 2e")
        need(c["hilbert_equals_pure_prediction"] == should, f"EXP-005 C4 {cid}: Hilbert function")
        if should:
            need(c["tables_agree"] is True and c["betti_I1"] == [[0, 0, 1], [1, e, 2], [2, 3 * e, 2], [3, 4 * e, 1]], f"EXP-005 C4 {cid}: table")
        c4rows.setdefault(e, {"pure": [], "other": []})["pure" if should else "other"].append(fld)
    need(r5["gates"]["G3"]["c4_modules"] == 24 and r5["gates"]["G3"]["c4_failing"] == [], "EXP-005 G3 on the modules of the family")
    # macros
    N["fiveCasesAll"] = thousands(len(cases))
    N["fiveDone"] = thousands(done)
    N["fiveFinite"] = 0
    N["fiveExhaustive"] = exh
    N["fiveRandom"] = thousands(done - exh)
    N["fiveBaOne"] = thousands(p["P2"]["cases_b_eq_a_plus_1_done"])
    N["fiveConstant"] = thousands(n_const)
    N["fiveGrowing"] = n_grow
    N["fiveGrowGFtwo"] = gr["GF(2)"][0]
    N["fiveGrowGFfour"] = gr["GF(2^2)"][0]
    N["fiveGrowGFsixteen"] = gr["GF(2^4)"][0]
    N["fiveGFsixteenCases"] = gr["GF(2^4)"][1]
    N["fiveCThreeCases"] = r5["totals"]["per_family"]["C3"]["cases"]
    N["fiveCThreeFinite"] = r5["totals"]["per_family"]["C3"]["finite_length"]
    for name, key in (("Coa", "C1a|GF(2)"), ("Cob", "C1b|GF(2)")):
        N["five%sConst" % name] = pff[key]["eventually_constant"]
        N["five%sGrow" % name] = pff[key]["growing"]
    N["fiveCoaCases"] = pff["C1a|GF(2)"]["cases"]
    N["fiveCobCases"] = pff["C1b|GF(2)"]["cases"]
    N["fiveCocCases"] = pff["C1c|GF(2)"]["cases"]
    g = r5["gates"]
    N["fiveGOneCompared"] = g["G1"]["compared"]
    N["fiveGTwoCompared"] = g["G2"]["compared"]
    N["fiveGThreeCompared"] = g["G3"]["sample_cases"]
    N["fiveGThreeAgree"] = g["G3"]["agree"]
    N["fiveFamilyTablesAgree"] = g["G3"]["c4_i1_i2_tables_agree"]
    N["fiveWall"] = f"{r5['wall_seconds_total']:.0f}"
    # the case noted in the experiment: three quartics over GF(16) with eventual value 1
    odd = [c for c in cases.values() if c["family"] == "C3" and c["cls"] == "eventually constant"]
    need(len(odd) == 1 and odd[0]["value"] == 1 and (odd[0]["a"], odd[0]["b"], odd[0]["e"]) == (1, 3, 4), "EXP-005: the single C3 case without finite length")
    N["fiveOddHilbert"] = ",".join(str(x) for x in odd[0]["hilbert"][:8])
    # the printed case: its Hilbert function must be the one of the Singular Betti table of the second instrument
    c = odd[0]
    need(c["id"] == "C3|GF(2^4)|21" and c.get("hilbert_equals_I2") is True, "EXP-005: the printed C3 case and its second instrument")
    num = [0] * (len(c["hilbert"]))
    for i_, j_, b_ in c["betti_I2"]:
        if j_ < len(num):
            num[j_] += (-1) ** i_ * b_
    need(series_div(num, [1, 1, 2], len(c["hilbert"])) == c["hilbert"], "EXP-005: the Hilbert function of the printed C3 case differs from its Singular Betti table")
    need(all(x == 1 for x in c["hilbert"][8:]) and c["hilbert"][:8] == [1, 2, 4, 6, 6, 6, 4, 2], "EXP-005: the printed C3 case: 1,2,4,6,6,6,4,2 and then 1")
    # tables
    order = ["C1a", "C1b", "C1c", "C2a", "C2b", "C2c", "C2d", "C2e", "C2f", "C2g"]
    rows = []
    for fam in order:
        (a, b, e), desc = FAM5[fam]
        for fld in sorted((f for (f2, f) in by if f2 == fam), key=lambda f: fld_parse(f)):
            t = pff[f"{fam}|{fld}"]
            cv = ", ".join("%d (value %s)" % (n, v) for v, n in sorted(t["constant_values"].items(), key=lambda kv: int(kv[0]))) or "0"
            rows.append(["$(%d,%d,%d)$" % (a, b, e), desc, fld_tex(fld), str(t["cases"]), "0", cv, str(t["growing"])])
    out["tab_five.tex"] = table("@{}lp{4.4cm}rrrp{2.6cm}r@{}", ["$(a,b,e)$", "sample", "field", "cases", "finite", "eventually constant", "growing"], rows)
    rows = []
    for sh in SHAPES5:
        t = c3[str(sh)]
        rows.append(["$(%d,%d,%d)$" % sh, str(t["cases"]), str(t["finite_length"]), str(t["eventually_constant"]), str(t["growing"])])
    out["tab_fivecthree.tex"] = table("@{}lrrrr@{}", ["$(a,b,e)$", "presentations", "finite length", "eventually constant", "growing"], rows)
    rows = []
    for e in sorted(c4rows):
        pure = sorted(f for f in c4rows[e]["pure"] if f != "QQ")
        other = sorted(c4rows[e]["other"], key=lambda f: int(f[3:-1]))
        rows.append([str(e), "$(0,%d,%d,%d)$" % (e, 3 * e, 4 * e), "$\\Q$ and $p\\in\\{%s\\}$" % ",".join(f[3:-1] for f in sorted(pure, key=lambda f: int(f[3:-1]))),
                     "$p\\in\\{%s\\}$" % ",".join(f[3:-1] for f in other), "%d" % sum(1 for c in c4.values() if c["e"] == e and c["tables_agree"] is True)])
    out["tab_fivecfour.tex"] = table("@{}rlp{3.4cm}p{3.2cm}r@{}", ["$e$", "degrees", "pure table", "not pure", "tables agreeing"], rows)


# ---- EXP-006 ----

FAM6 = {"A1": 3, "A2": 3, "B1": 4, "B2": 4, "B3": 4, "C": 5}
PAIRS6 = [("6", "A1", "GF(3)", "index", 91), ("6", "A2", "GF(5)", "seed", 20261122), ("6", "B1", "GF(3)", "seed", 20261137),
          ("6", "B1", "GF(5)", "seed", 20261156), ("6", "B1", "GF(7)", "seed", 20261132), ("6", "C", "GF(3)", "seed", 20263616),
          ("8", "A", "GF(5)", "seed", 20267546), ("8", "B", "GF(7)", "seed", 20261985), ("8", "C", "GF(3)", "seed", 20264514)]
FAM8 = {"A": (5, "GF(5)"), "B": (5, "GF(7)"), "C": (6, "GF(3)")}
FAM8W = {"A": "AFive", "B": "BSeven", "C": "CThree"}


def pure_table(e):
    return [[0, 0, 1], [1, e, 2], [2, 3 * e, 2], [3, 4 * e, 1]]


def exp6(r6, r8, N, out, data_root=None):
    need(r6["experiment"] == "EXP-006", "EXP-006 results file")
    for g in ("G1", "G2", "G3", "G4"):
        need(r6["gates"][g]["passed"] is True, f"EXP-006 gate {g}")
    fr = r6["full_results"]
    need(re.fullmatch(r"[0-9a-f]{64}", fr["sha256"]) is not None and fr["sha256"] != "0" * 64 and fr["bytes"] > 0, "EXP-006: the recorded hash of the full results file")
    if data_root is not None:
        full = Path(data_root) / fr["file"].split(" (")[0]
        if full.exists():
            need(hashlib.sha256(full.read_bytes()).hexdigest() == fr["sha256"] and full.stat().st_size == fr["bytes"], "EXP-006: the full results file under the data root differs from its recorded hash")
    need(r6["gates"]["G3"]["sample_spaces"] == r6["gates"]["G3"]["agree_and_pure_in_I2"] == 270 and r6["gates"]["G3"]["failing_cases"] == [], "EXP-006 second instrument")
    pf = r6["totals"]["per_field"]
    chunks = r6["chunks"]
    rows3, rowsc, fig = [], [], defaultdict(list)
    order = [("A1", "GF(3)"), ("A2", "GF(5)"), ("A2", "GF(9)"), ("A2", "GF(25)"), ("A2", "GF(27)"), ("B1", "GF(3)"), ("B1", "GF(5)"), ("B1", "GF(7)"),
             ("B3", "GF(9)"), ("B2", "GF(11)"), ("B2", "GF(13)"), ("C", "GF(3)")]
    need(sorted(f"{a}|{b}" for a, b in order) == sorted(pf), "EXP-006: families and fields")
    ratios = []
    for fam, fld in order:
        x = pf[f"{fam}|{fld}"]
        e = FAM6[fam]
        pp, kk = fld_parse(fld)
        q = pp ** kk
        need(x["e"] == e and x["q"] == q and x["char"] == pp, f"EXP-006 {fam}|{fld}: e, q, characteristic")
        need(x["complete"] is True and x["spaces"] == x["planned"], f"EXP-006 {fam}|{fld}: incomplete")
        need(x["target_rank"] == target_rank(e), f"EXP-006 {fam}|{fld}: target rank {x['target_rank']} vs {target_rank(e)}")
        need(abs(x["q_minus_2"] - 1.0 / q ** 2) < 1e-12, f"EXP-006 {fam}|{fld}: q^-2")
        need(abs(x["share_pure"] - x["pure"] / x["spaces"]) < 1e-12, f"EXP-006 {fam}|{fld}: share of pure spaces")
        need(abs(x["share_rank_le_target"] - x["rank_le_target"] / x["spaces"]) < 1e-12, f"EXP-006 {fam}|{fld}: share of the rank condition")
        cs = [c for k, c in chunks.items() if k.startswith(f"{fam}|{fld}|")]
        need(sum(c["n"] for c in cs) == x["spaces"] and sum(c["pure"] for c in cs) == x["pure"] and sum(c["pure_hilbert"] for c in cs) == x["pure_hilbert"],
             f"EXP-006 {fam}|{fld}: chunk totals differ from the field totals")
        need(sum(sum(1 for s in c["spaces"] if s.get("pure")) for c in cs) == x["pure"], f"EXP-006 {fam}|{fld}: stored pure spaces differ from the count")
        nonpure = sum(x["nonpure_tables"].values())
        need(nonpure == x["pure_hilbert"] - x["pure"], f"EXP-006 {fam}|{fld}: spaces with the pure Hilbert function and another table")
        need(sum(v for k_, v in x["rank_hist"].items() if int(k_) <= x["target_rank"]) == x["rank_le_target"], f"EXP-006 {fam}|{fld}: rank histogram")
        ratio = x["share_rank_le_target"] / x["q_minus_2"]
        if fam in ("B1", "B2", "B3"):
            ratios.append(ratio)
            fig["rank4"].append((q, x["share_rank_le_target"]))
            fig["pure4"].append((q, x["share_pure"]))
        else:
            if fam in ("A1", "A2"):
                fig["pure3"].append((q, x["share_pure"]))
            if fam == "C":
                fig["pure5"].append((q, x["share_pure"]))
        key = FAMW[fam] + (FLDW.get(fld) or fld)
        N["six%sSpaces" % key] = thousands(x["spaces"])
        N["six%sPure" % key] = thousands(x["pure"])
        N["six%sPureHF" % key] = thousands(x["pure_hilbert"])
        N["six%sRank" % key] = thousands(x["rank_le_target"])
        N["six%sSharePure" % key] = pct(x["share_pure"], 1) if x["share_pure"] >= 0.01 else pct(x["share_pure"], 2)
        N["six%sShareRank" % key] = pct(x["share_rank_le_target"], 1)
        N["six%sRatioRank" % key] = f"{ratio:.1f}"
        hq = heuristic(e, q)
        N["six%sRatioPure" % key] = f"{x['share_pure'] / hq:.2f}" if hq else "--"
        N["six%sNonpure" % key] = thousands(nonpure)
        N["six%sTables" % key] = len(x["nonpure_tables"])
        rows3.append([str(e), fld_tex(fld), thousands(x["spaces"]), "%s (%s\\%%)" % (thousands(x["rank_le_target"]), pct(x["share_rank_le_target"], 1)),
                      thousands(x["pure_hilbert"]), thousands(x["pure"]), pctv(x["share_pure"]) + "\\%",
                      ("$q^{-%d}$ = %s\\%%" % (2 * he_val(e, 3 * e), pctv(hq))) if hq else "--",
                      f"{x['share_pure'] / hq:.2f}" if hq else "--"])
        rowsc.append([str(e), fld_tex(fld), thousands(x["pure_hilbert"]), thousands(x["pure"]), thousands(nonpure), str(len(x["nonpure_tables"])),
                      pct(nonpure / x["pure_hilbert"], 1) + "\\%"])
    exp8(r8, N, fig, rows3, rowsc)
    out["tab_sixcounts.tex"] = table("@{}rrrp{2.0cm}rrrp{1.9cm}r@{}", ["$e$", "field", "spaces", "rank$\\,\\mu_{3e}\\le r$", "pure Hilbert function", "pure", "share pure", "heuristic $q^{-2h_e(3e)}$", "pure / heuristic"], rows3)
    out["tab_sixcancel.tex"] = table("@{}rrp{2.2cm}rp{1.8cm}p{1.8cm}p{2.2cm}@{}", ["$e$", "field", "pure Hilbert function", "pure", "another table", "distinct tables", "share of another table"], rowsc)
    # predictions, as the artifacts state them
    pr = r6["predictions"]
    need(pr["P1"]["holds"] and pr["P3"]["holds"] and pr["P4"]["holds"], "EXP-006 predictions P1, P3, P4")
    need(pr["P2"]["holds"] is False and not any(v["in_interval_0.3_to_3"] for k, v in pr["P2"].items() if k != "holds"), "EXP-006: the share prediction P2 is refuted in all six fields")
    need(len(ratios) == 6, "EXP-006: six fields with the rank condition")
    N["sixRatioMin"] = f"{min(ratios):.1f}"
    N["sixRatioMax"] = f"{max(ratios):.1f}"
    orb = pr["P4"]
    need(orb["B2|GF(11)"]["in_orbit"] == 0 and orb["B2|GF(13)"]["in_orbit"] == 0 and orb["B2|GF(11)"]["pure"] == orb["B2|GF(11)"]["outside_orbit"], "EXP-006 orbit test")
    need(gauss_binomial(6, 2, 3) == pf["A1|GF(3)"]["spaces"] == 11011, "EXP-006: all two-dimensional subspaces of U_3 over GF(3)")
    N["sixSpacesTotal"] = thousands(sum(x["spaces"] for x in pf.values()))
    N["sixCpu"] = thousands(int(sum(x["seconds_cpu"] for x in pf.values())))
    N["sixFullShaA"] = r6["full_results"]["sha256"][:32]
    N["sixFullShaB"] = r6["full_results"]["sha256"][32:]
    N["sixControlTotal"] = orb["B2|GF(11)"]["pure"] + orb["B2|GF(13)"]["pure"]
    N["sixSingularSample"] = r6["gates"]["G3"]["sample_spaces"]
    N["sixUnitTests"] = int(re.match(r"(\d+) passed", r6["gates"]["G4"]["last_line"]).group(1))
    N["sixWallMin"] = f"{r6['wall_seconds_total'] / 60:.0f}"
    N["sixFullBytes"] = thousands(r6["full_results"]["bytes"])
    # the three tables with a cancelling pair at e = 3 over GF(3): degrees 10, 11, or both
    t3 = set(pf["A1|GF(3)"]["nonpure_tables"])
    base = [[0, 0, 1], [1, 3, 2], [2, 9, 2]]
    want = {repr(base + [[2, 10, 1], [3, 10, 1], [3, 12, 1]]), repr(base + [[2, 11, 1], [3, 11, 1], [3, 12, 1]]),
            repr(base + [[2, 10, 1], [2, 11, 1], [3, 10, 1], [3, 11, 1], [3, 12, 1]])}
    need(t3 == want, "EXP-006: the three other tables over GF(3) at e = 3")
    # explicit pairs, printed from the stored bases and recomputed Hilbert function by this script's own arithmetic
    rows = []
    pair_rows = []
    for src, fam, fld, kind, val in PAIRS6:
        e = FAM6[fam] if src == "6" else FAM8[fam][0]
        pp, kk = fld_parse(fld)
        need(kk == 1, "explicit pairs are over prime fields")
        chs = chunks if src == "6" else r8["chunks"]
        found = [s for k, c in chs.items() if k.startswith(f"{fam}|{fld}|" if src == "6" else f"{fam}|") for s in c["spaces"] if s.get(kind) == val]
        need(len(found) == 1, f"EXP-006 pair {fam}|{fld}|{kind} {val}: found {len(found)}")
        s = found[0]
        need(s["pure"] is True and s["betti"] == pure_table(e), f"EXP-006 pair {fam}|{fld}|{val}: Betti table")
        pair = [[(tuple(m), c) for m, c in f] for f in s["basis"]]
        hf = hilbert_pair(pair, e, pp, 4 * e - 3)
        need(hf == [he_val(e, n) for n in range(4 * e - 2)] and hf[-1] == 0 and sum(hf) == e ** 3, f"EXP-006 pair {fam}|{fld}|{val}: Hilbert function recomputed differs from h_e")
        need("hilbert" not in s or hf == s["hilbert"][:4 * e - 2], f"EXP-006 pair {fam}|{fld}|{val}: stored Hilbert function")
        pair_rows.append((e, pp, [str(e), fld_tex(fld), "$f=%s$\\newline $g=%s$" % (poly_tex(pair[0], pp), poly_tex(pair[1], pp)), str(e ** 3)]))
        N["sixPairLength" + EW[e]] = e ** 3
    rows = [r for _, _, r in sorted(pair_rows, key=lambda t: (t[0], t[1]))]
    out["tab_sixpairs.tex"] = table("@{}rrp{9.6cm}r@{}", ["$e$", "field", "forms of degree $e$", "length"], rows)
    # figure: the share of pure spaces against q, with the heuristic values q^(-2 h_e(3e))
    lines = ["\\begin{tikzpicture}",
             "\\begin{axis}[xmode=log, ymode=log, width=0.92\\textwidth, height=8cm, xlabel={field size $q$}, ylabel={share of random spaces}, ymin=0.00001, ymax=1, "
             "xtick={3,5,7,9,11,13,25,27}, xticklabels={3,5,7,9,11,13,25,27}, minor xtick={}, ytick={0.00001,0.0001,0.001,0.01,0.1,1}, yticklabels={$10^{-5}$,$10^{-4}$,$10^{-3}$,$10^{-2}$,$10^{-1}$,$1$}, minor ytick={}, "
             "tick label style={font=\\scriptsize}, label style={font=\\small}, grid=major, grid style={gray!25}, legend style={font=\\scriptsize, at={(0.5,-0.2)}, anchor=north}, legend columns=3]"]
    for key, mark, lab in (("pure3", "*", "pure, $e=3$"), ("pure4", "square*", "pure, $e=4$"), ("pure5", "diamond*", "pure, $e=5$"), ("pure6", "pentagon*", "pure, $e=6$"),
                           ("rank4", "triangle*", "rank$\\,\\mu_{12}\\le48$, $e=4$")):
        pts = " ".join("(%d,%.6f)" % (q, v) for q, v in sorted(fig[key]))
        lines.append("\\addplot[only marks, mark=%s, mark size=2pt] coordinates {%s};" % (mark, pts))
        lines.append("\\addlegendentry{%s}" % lab)
    for ex, style in ((2, "dashed"), (4, "dash dot"), (8, "densely dashed")):
        lines.append("\\addplot[%s, thick] coordinates {(3,%.9f) (27,%.15f)};" % (style, 3.0 ** (-ex), 27.0 ** (-ex)))
        lines.append("\\addlegendentry{$q^{-%d}$}" % ex)
    lines.append("\\addplot[dotted, thick] coordinates {(3,%.5f) (27,%.6f)};" % (1 / 3.0, 1 / 27.0))
    lines.append("\\addlegendentry{$q^{-1}$}")
    lines += ["\\end{axis}", "\\end{tikzpicture}"]
    out["fig_sixshare.tex"] = "\n".join(lines) + "\n"


def exp8(r8, N, fig, rows3, rowsc):
    """EXP-008: pure pairs of quintics over GF(5) and GF(7) and of sextics over GF(3), each family stopped at 40 pure spaces."""
    need(r8["experiment"] == "EXP-008", "EXP-008 results file")
    g = r8["gates"]
    need(g["G1"]["passed"] is True and len(g["G1"]["cases"]) == 9 and all(c["ok"] for c in g["G1"]["cases"]), "EXP-008 gate G1")
    need(g["G2"]["passed"] is True and g["G2"]["sample_spaces"] == g["G2"]["agree_and_pure_in_I2"] == 60 and g["G2"]["failing_cases"] == [], "EXP-008 second instrument")
    need(g["G3"]["passed"] is True, "EXP-008 gate G3")
    pr = r8["predictions"]
    need(pr["P1"]["holds"] and pr["P2"]["holds"] and pr["P3"]["holds"] and pr["P1_and_P2_hold"], "EXP-008 predictions")
    need(sorted(r8["totals"]) == ["A", "B", "C"], "EXP-008 families")
    wall = 0.0
    for fam in ("A", "B", "C"):
        x = r8["totals"][fam]
        e, fld = FAM8[fam]
        pp, kk = fld_parse(fld)
        q = pp ** kk
        need(x["e"] == e and x["field"] == fld and x["q"] == q, f"EXP-008 {fam}: e, field, q")
        need(x["stopped_early"] is True and x["complete"] is False and x["pure"] >= 40 and x["spaces"] < x["planned"], f"EXP-008 {fam}: the early stop at 40 pure spaces")
        need(x["target_rank"] == target_rank(e) and x["h_e_3e"] == he_val(e, 3 * e), f"EXP-008 {fam}: target rank and h_e(3e)")
        hq = heuristic(e, q)
        need(abs(x["q_minus_2h"] - hq) < 1e-12, f"EXP-008 {fam}: heuristic value q^(-2h)")
        need(abs(x["share_pure"] - x["pure"] / x["spaces"]) < 1e-12 and abs(x["ratio_pure_to_q"] - x["share_pure"] / hq) < 1e-9, f"EXP-008 {fam}: share and ratio")
        need(abs(x["share_rank_eq_target"] - x["rank_eq_target"] / x["spaces"]) < 1e-12, f"EXP-008 {fam}: share of the rank condition")
        cs = [c for k, c in r8["chunks"].items() if k.startswith(fam + "|")]
        need(len(cs) == x["chunks"] and sum(c["n"] for c in cs) == x["spaces"] and sum(c["pure"] for c in cs) == x["pure"] and sum(c["pure_hilbert"] for c in cs) == x["pure_hilbert"],
             f"EXP-008 {fam}: chunk totals differ from the family totals")
        need(sum(sum(1 for s_ in c["spaces"] if s_.get("pure")) for c in cs) == x["pure"], f"EXP-008 {fam}: stored pure spaces differ from the count")
        need(sum(x["rank_hist"].values()) == x["spaces"] and x["rank_hist"][str(x["target_rank"])] == x["rank_eq_target"], f"EXP-008 {fam}: rank histogram")
        nonpure = sum(x["nonpure_tables"].values())
        need(nonpure == x["pure_hilbert"] - x["pure"], f"EXP-008 {fam}: spaces with the pure Hilbert function and another table")
        wall += x["seconds_wall"]
        key = FAM8W[fam]
        N["eight%sSpaces" % key] = thousands(x["spaces"])
        N["eight%sPlanned" % key] = thousands(x["planned"])
        N["eight%sPure" % key] = x["pure"]
        N["eight%sPureHF" % key] = x["pure_hilbert"]
        # the rank column of the paper counts rank at most r, as for the earlier search: summed from the stored histogram
        rank_le = sum(v for k_, v in x["rank_hist"].items() if int(k_) <= x["target_rank"])
        need(x["rank_eq_target"] <= rank_le <= x["spaces"], f"EXP-008 {fam}: rank at most r from the histogram")
        N["eight%sRank" % key] = thousands(rank_le)
        N["eight%sShareRank" % key] = pct(rank_le / x["spaces"], 1)
        N["eight%sSharePure" % key] = pctv(x["share_pure"])
        N["eight%sHeur" % key] = pctv(hq)
        N["eight%sRatio" % key] = f"{x['share_pure'] / hq:.2f}"
        N["eight%sNonpure" % key] = nonpure
        N["eight%sTables" % key] = len(x["nonpure_tables"])
        N["eight%sWallMin" % key] = f"{x['seconds_wall'] / 60:.0f}"
        fig["pure%d" % e].append((q, x["share_pure"]))
        rows3.append([str(e), fld_tex(fld), thousands(x["spaces"]) + "$^\\dagger$", "%s (%s\\%%)" % (thousands(rank_le), pct(rank_le / x["spaces"], 1)),
                      thousands(x["pure_hilbert"]), thousands(x["pure"]), pctv(x["share_pure"]) + "\\%", "$q^{-%d}$ = %s\\%%" % (2 * he_val(e, 3 * e), pctv(hq)),
                      f"{x['share_pure'] / hq:.2f}"])
        rowsc.append([str(e), fld_tex(fld), thousands(x["pure_hilbert"]), thousands(x["pure"]), thousands(nonpure), str(len(x["nonpure_tables"])),
                      pct(nonpure / x["pure_hilbert"], 1) + "\\%"])
    need(abs(wall - sum(r["seconds"] for r in r8["runs"] if r["command"] == "cases")) < 0.5, "EXP-008: wall times of the families")
    N["eightSpacesTotal"] = thousands(sum(x["spaces"] for x in r8["totals"].values()))
    N["eightCpu"] = thousands(int(sum(x["seconds_cpu"] for x in r8["totals"].values())))
    N["eightSingularSample"] = g["G2"]["sample_spaces"]
    N["eightGOneCases"] = len(g["G1"]["cases"])
    N["eightWallMin"] = f"{r8['wall_seconds_total'] / 60:.0f}"
    N["eightEarlyStop"] = 40


# ---- EXP-007 ----

POS_CHAR = [(4, "GF(13)"), (4, "GF(17)"), (4, "GF(32003)"), (5, "GF(13)"), (5, "GF(17)"), (5, "GF(32003)"), (6, "GF(13)"), (6, "GF(17)"), (6, "GF(32003)"),
            (7, "GF(17)"), (7, "GF(32003)")]


def powers_span_dim(e, forms):
    """dim of the span of the e-th powers (x + t y)^e, t = 0..e-1, and y^e (dimension e+1 in characteristic 0), and of that span plus `forms`."""
    gens = []
    for t in list(range(e)) + [None]:
        if t is None:
            gens.append(elt_from_terms([((0, e, 0), 1)]))
            continue
        cur = {(0, 0, 0): 1}
        for _ in range(e):
            nxt = Pbw.xleft(cur)
            for k, v in Pbw.yleft(cur).items():
                Pbw.add(nxt, k, t * v)
            cur = nxt
        gens.append(cur)
    keys = sorted({k for g in gens + forms for k in g})
    idx = {k: i for i, k in enumerate(keys)}

    def mat(es):
        rows = []
        for g in es:
            r = [0] * len(keys)
            for k, v in g.items():
                r[idx[k]] = v
            rows.append(r)
        return rows
    return rank_q(mat(gens)), rank_q(mat(gens + forms))


def exp7(r7, N, out):
    need(r7["experiment"] == "EXP-007", "EXP-007 results file")
    for g in ("G1", "G2", "G3", "G4"):
        need(r7["gates"][g]["passed"] is True, f"EXP-007 gate {g}")
    st = r7["statements"]
    pr = r7["predictions"]
    need(all(pr[k]["holds"] for k in ("P1", "P2", "P3", "P4", "P5", "P6")), "EXP-007 predictions")
    need(r7["gates"]["G3"]["spaces"] == r7["gates"]["G3"]["agree"] == 9 and r7["gates"]["G3"]["failing_cases"] == [], "EXP-007 second instrument")
    # T1: the tangent space at W_0 over the rationals
    t1 = {row["e"]: row for row in st["T1"]["rows"]}
    need(sorted(t1) == [4, 5, 6, 7] and st["T1"]["complete"], "EXP-007 T1: e = 4..7")
    for e, row in t1.items():
        need(row["r"] == target_rank(e) and row["rank_A"] == row["r"], f"EXP-007 T1 e={e}: rank of A")
        need(row["matrix"] == [2 * UN(2 * e), UN(3 * e)], f"EXP-007 T1 e={e}: matrix size")
        need(row["dim_K"] == 2 and row["coker_dim"] == he_val(e, 3 * e) == row["coker_expected"], f"EXP-007 T1 e={e}: kernel and cokernel")
        need(row["coordinates"] == 2 * (UN(e) - 2), f"EXP-007 T1 e={e}: chart coordinates")
        need(row["bound"] == 4 * e - 4 == 2 * UN(e) - 4 - 2 * he_val(e, 3 * e), f"EXP-007 T1 e={e}: the bound 4e-4")
        need(row["tangent_dim"] == row["coordinates"] - row["rank_T"] == 4 * e - 4, f"EXP-007 T1 e={e}: tangent dimension {row['tangent_dim']} vs {4 * e - 4}")
        need(row["orbit_in_tangent"] is True and row["orbit_rank"] == 2, f"EXP-007 T1 e={e}: orbit directions")
        N["sevenTangent" + EW[e]] = row["tangent_dim"]
        N["sevenCoker" + EW[e]] = row["coker_dim"]
        N["sevenRank" + EW[e]] = row["r"]
        N["sevenCoords" + EW[e]] = row["coordinates"]
    # T2
    t2 = {(row["e"], row["field"]): row for row in st["T2"]["rows"]}
    need(sorted(t2) == sorted(POS_CHAR) and st["T2"]["complete"], "EXP-007 T2: cases")
    expected2 = {(4, "GF(13)"): 12, (4, "GF(17)"): 12, (4, "GF(32003)"): 12, (5, "GF(13)"): 16, (5, "GF(17)"): 16, (5, "GF(32003)"): 16,
                 (6, "GF(13)"): 22, (6, "GF(17)"): 20, (6, "GF(32003)"): 20, (7, "GF(17)"): 26, (7, "GF(32003)"): 24}
    for k, row in t2.items():
        need(row["tangent_dim"] == expected2[k] and row["holds"], f"EXP-007 T2 {k}: tangent dimension {row['tangent_dim']}")
        need(row["tangent_dim"] >= 4 * k[0] - 4, f"EXP-007 T2 {k}: below 4e-4")
    # the table of tangent dimensions
    rows = []
    for e in (4, 5, 6, 7):
        r = t1[e]
        cells = [str(e), "%d$\\times$%d" % tuple(r["matrix"]), str(r["r"]), str(r["coker_dim"]), str(r["coordinates"]), str(r["rank_T"]), str(r["tangent_dim"]), str(4 * e - 4)]
        for fld in ("GF(13)", "GF(17)", "GF(32003)"):
            cells.append(str(t2[(e, fld)]["tangent_dim"]) if (e, fld) in t2 else "--")
        rows.append(cells)
    out["tab_seventangent.tex"] = table("@{}rlrrrrrrrrr@{}", ["$e$", "$A$", "$r$", "$h_e(3e)$", "chart", "rank $T$", "$\\Q$", "$4e-4$", "$\\F_{13}$", "$\\F_{17}$", "$\\F_{32003}$"], rows)
    # T3: explicit pairs over the rationals and controls; the ranks and the orbit test by this script's own arithmetic
    t3 = {row["name"]: row for row in st["T3"]["rows"]}
    cases = r7["cases"]
    rows = []
    for name in ("W0_e4", "W0_e5", "P1", "P2", "P3", "P4", "P5", "C1", "C2"):
        row = t3[name]
        c = cases["T3|" + name]
        e = c["e"]
        need(row["rank_mu_3e"] == c["rank_mu_3e"] and row["r"] == target_rank(e) and c["target_rank_r"] == target_rank(e), f"EXP-007 {name}: rank")
        pair = [[(tuple(m), int(v)) for m, v in f] for f in c["basis"]]
        forms = [elt_from_terms(t) for t in pair]
        rk = mu_rank(forms, e, 3 * e)
        need(rk == c["rank_mu_3e"], f"EXP-007 {name}: rank of mu_3e recomputed {rk} vs stored {c['rank_mu_3e']}")
        dS, dSW = powers_span_dim(e, forms)
        need(dS == e + 1 == row["dim_S"] and dSW == row["dim_S_plus_W"], f"EXP-007 {name}: dimension of the span of the e-th powers and of its sum with W: {dS}, {dSW}")
        need(row["outside_orbit"] == (dSW > e + 1), f"EXP-007 {name}: orbit test")
        expect_pure = name in ("W0_e4", "W0_e5", "P1", "P2", "P3", "P4", "P5")
        need(row["pure"] is expect_pure and row["holds_first"] and row["g3"]["agree"], f"EXP-007 {name}: purity and agreement of the two instruments")
        if expect_pure:
            need(row["betti_I1"] == pure_table(e) and rk == target_rank(e) and row["g3"]["betti_I2"] == pure_table(e), f"EXP-007 {name}: pure table")
        need((name in ("W0_e4", "W0_e5")) == (not row["outside_orbit"]), f"EXP-007 {name}: inside or outside the orbit")
        if name == "C1":
            need(rk == 49 and row["betti_I1"] == [[0, 0, 1], [1, 4, 2], [2, 12, 1], [2, 13, 2], [3, 15, 2]], "EXP-007 C1 control")
            tab = "$b_{2,12}=1$, $b_{2,13}=2$, $b_{3,15}=2$"
        elif name == "C2":
            need(rk == 46 and row["nonzero_to_24"] is True and row["finite_length"] is False, "EXP-007 C2 control")
            tab = "infinite length"
        else:
            tab = "$(1,2,2,1)$ on $(0,%d,%d,%d)$" % (e, 3 * e, 4 * e)
        lab = {"W0_e4": "$W_0$", "W0_e5": "$W_0$"}.get(name, "$%s$" % (name if not name.startswith("C") else name))
        if name.startswith("P"):
            lab = "$P_%s$" % name[1]
        if name.startswith("C"):
            lab = "$C_%s$" % name[1]
        rows.append([lab, str(e), "$f=%s$\\newline $g=%s$" % (poly_tex(pair[0]), poly_tex(pair[1])), "%d / %d" % (rk, target_rank(e)), tab, "%d / %d" % (dSW, dS)])
    out["tab_sevenpairs.tex"] = table("@{}lrp{4.9cm}p{1.9cm}p{2.8cm}p{2.2cm}@{}", ["space", "$e$", "forms over $\\Q$", "rank $\\mu_{3e}$ / $r$", "Betti table", "$\\dim(S_e{+}W)$ / $\\dim S_e$"], rows)
    # T4, T5, T6
    t4, t5, t6 = st["T4"], st["T5"], st["T6"]
    rows = []
    for e in ("4", "5"):
        r = target_rank(int(e))
        q, g = t4[e]["qq"], t4[e]["gf"]
        need(q["members"] == q["planned"] == 625 and q["rank_le_r"] == 625 and q["above_r"] == 0 and not q["unfinished"] and not q["failing"], f"EXP-007 T4 e={e} over Q")
        need(g["members"] == g["planned"] == 200 and g["pure_and_outside"] >= 190 and g["rank_le_r"] == 200 and not g["unfinished"], f"EXP-007 T4 e={e} over GF(32003)")
        need(sum(q["rank_hist"].values()) == q["members"] and sum(g["rank_hist"].values()) == g["members"], f"EXP-007 T4 e={e}: a rank histogram does not sum to its member count")
        rr = q["rank_hist"][str(r)]
        N["sevenLQQAt%s" % ("Four" if e == "4" else "Five")] = rr
        N["sevenLGFPure%s" % ("Four" if e == "4" else "Five")] = g["pure_and_outside"]
        N["sevenLQQMin%s" % ("Four" if e == "4" else "Five")] = min(int(k) for k in q["rank_hist"])
        rows.append(["$L_%s$" % e, e, "$\\Q$, parameters in $\\{-2,\\dots,2\\}$", "625", "625", str(rr), "--"])
        rows.append(["$L_%s$" % e, e, "$\\F_{32003}$, random", "200", "200", str(g["rank_hist"][str(r)]), "%d" % g["pure_and_outside"]])
    gr = t5["grid"]
    need(gr["spaces_done"] == gr["spaces_planned"] == 729 and gr["plane_points"] == 1 and gr["rank_le_48"] == 1 and gr["mismatches"] == [] and not gr["unfinished"] and gr["rank_hist"] == {"48": 1, "49": 728},
         "EXP-007 T5 grid")
    need(len(t5["pure"]) == 6 and all(x["pure"] and x["rank_mu_3e"] == 48 and x["equation_value"] == 0 for x in t5["pure"]), "EXP-007 T5 pure points on the plane")
    rows.append(["section $\\Pi$", "4", "$\\Q$, grid $\\{-4,\\dots,4\\}^3$", "729", "1", "1", "--"])
    for e in ("4", "5", "6"):
        t = t6[e]
        need(t["rank_le_r"] == t["spaces"] == t["planned"] == 20 and t["r"] == target_rank(int(e)) and t["holds"] and t["d"] == he_val(int(e), 3 * int(e)), f"EXP-007 T6 e={e}")
        rows.append(["common factor of degree %d" % t["d"], e, "$\\F_{32003}$, random", "20", "20", str(t["rank_hist"][str(t["r"])]), "--"])
    need(t6["4"]["infinite_length"] == 20, "EXP-007 T6: infinite length at e = 4")
    out["tab_sevenfam.tex"] = table("@{}lrlrrrr@{}", ["family", "$e$", "field and sampling", "spaces", "rank $\\le r$", "rank $=r$", "pure, outside orbit"], rows)
    N["sevenGridSpaces"] = gr["spaces_done"]
    N["sevenGridOff"] = gr["rank_hist"]["49"]
    N["sevenCommon"] = 20
    N["sevenWall"] = f"{r7['wall_seconds_total']:.0f}"
    N["sevenGThreeSpaces"] = r7["gates"]["G3"]["spaces"]


def gauss_binomial(n, k, q):
    num = den = 1
    for i in range(k):
        num *= q ** (n - i) - 1
        den *= q ** (i + 1) - 1
    return num // den


def formula_checks(N):
    """u(n), h_e(n), h_e(3e) and the bound 4e-4 against the Hilbert series of U and the closed forms used in the text."""
    ser = series_div([1], [1, 1, 2], 80)
    need(all(UN(n) == ser[n] for n in range(80)), "u(n) = floor((n+2)^2/4) differs from the Hilbert series of U")
    for e in range(2, 13):
        h = [he_val(e, n) for n in range(0, 5 * e + 3)]
        need(h == (h_series(e) + [0] * (5 * e + 3))[:len(h)], f"e={e}: h_e(n) from u differs from the series h_e(t)")
        need(sum(h) == e ** 3 and all(x >= 0 for x in h), f"e={e}: the pure Hilbert function")
        h3 = he_val(e, 3 * e)
        need(h3 == (((e - 2) // 2) ** 2 if e % 2 == 0 else (e - 1) * (e - 3) // 4), f"e={e}: closed form of h_e(3e)")
        need(2 * UN(e) - 4 - 2 * h3 == 4 * e - 4, f"e={e}: 2u(e) - 4 - 2h_e(3e) = 4e - 4")
        need(h3 == UN(3 * e) - 2 * UN(2 * e) + 2, f"e={e}: h_e(3e)")
        # the maximal-rank function agrees with h_e except in the degrees 3e .. 4e-4 (and only for e >= 4)
        mr = [max(0, UN(n) - 2 * UN(n - e)) for n in range(5 * e)]
        diff = [n for n in range(5 * e) if mr[n] != he_val(e, n)]
        need(diff == ([] if e <= 3 else list(range(3 * e, 4 * e - 3))), f"e={e}: degrees where the maximal-rank function differs from h_e: {diff}")
    N["formulaMaxE"] = 12


# --------------------------------------------------------------------------------------------------------------------------
# the later computations: EXP-009 (linear family below 2e), EXP-011 (central pairs), EXP-012 (central-commutator criterion);
# the weight-class strata; the state of the pairs (e, p)
# --------------------------------------------------------------------------------------------------------------------------

PW = {3: "Three", 5: "Five", 7: "Seven", 11: "Eleven", 13: "Thirteen"}
EWL = {2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten", 11: "Eleven",
       12: "Twelve", 13: "Thirteen", 15: "Fifteen"}
LF_PAIRS = [(4, 3), (4, 5), (4, 7), (4, 11), (4, 13), (5, 3), (5, 5), (5, 7), (5, 11), (5, 13), (6, 3), (6, 5), (6, 7), (6, 11), (6, 13),
            (7, 3), (7, 5), (7, 7), (7, 11), (7, 13)]
LF_BELOW = [(e, p) for e, p in LF_PAIRS if p < 2 * e]            # the fifteen pairs with p < 2e
LF_PURE = [(4, 5), (4, 7), (5, 7), (6, 11), (7, 11), (7, 13)]    # the pairs below 2e where the family holds a pure member


def read_later(root):
    ex = Path(root) / "experiments"
    return tuple(jload(ex / d.name / "artifacts" / "results.json") for d in (E9, E11, E12))


def terms4(lst):
    """EXP-012 stores a monomial x^a y^b z^c (or X^a Y^b z^c) with its coefficient as [a, b, c, coefficient]."""
    return [((int(a), int(b), int(c)), int(v)) for a, b, c, v in lst]


def terms_nested(lst):
    """EXP-009 and EXP-011 store a pair as [[[a, b, c], coefficient], ...]."""
    return [(tuple(int(t) for t in m), int(v)) for m, v in lst]


def pbw_mul(f, g, p):
    """The product f g of two elements of U (dictionaries in the PBW basis y^b x^a z^c), coefficients reduced modulo p."""
    out = {}
    for mono, cf in f.items():
        for key, v in mul_left(mono, g).items():
            Pbw.add(out, key, cf * v)
    return {k: v % p for k, v in out.items() if v % p}


def pbw_sub(f, g, p):
    out = dict(f)
    for k, v in g.items():
        out[k] = (out.get(k, 0) - v) % p
    return {k: v for k, v in out.items() if v % p}


def commutator(f, g, p):
    """g f - f g."""
    return pbw_sub(pbw_mul(g, f, p), pbw_mul(f, g, p), p)


def central_poly(terms, p, shift_z=0):
    """The element sum c X^i Y^j z^k of U for a list of ((i, j, k), c), with X = x^p and Y = y^p (central); multiplied by z^shift_z."""
    return elt_from_terms([((p * i, p * j, k + shift_z), c) for (i, j, k), c in terms])


def need_pure_pair(label, terms_pair, e, p, N=None):
    """Recompute, in the arithmetic of this script, the Hilbert function of U/(Uf + Ug) (it must be h_e, which vanishes from degree
    4e - 3 on, so the module has length e^3) and the rank of mu_{3e} (it must be r)."""
    key = (e, p, repr(terms_pair))
    if key in _PURE_PAIR_OK:  # a pair that passed is not recomputed (the result is a function of the pair alone)
        return _PURE_PAIR_OK[key]
    nfail = len(FAILS)
    hf = hilbert_pair(terms_pair, e, p, 4 * e)
    need(hf[: 4 * e + 1] == [he_val(e, n) for n in range(4 * e + 1)], f"{label}: Hilbert function differs from h_e")
    need(sum(hf) == e ** 3, f"{label}: length {sum(hf)} differs from e^3")
    forms = [elt_from_terms(t) for t in terms_pair]
    need(mu_rank(forms, e, 3 * e, p) == target_rank(e), f"{label}: rank of mu_3e differs from r")
    if len(FAILS) == nfail:
        _PURE_PAIR_OK[key] = sum(hf)
    return sum(hf)


_PURE_PAIR_OK = {}


# ---- EXP-009 ----

def exp9(r9, N, out):
    need(r9["experiment"] == "EXP-009", "EXP-009 results file")
    for g in ("G1", "G2", "G3"):
        need(r9["gates"][g]["passed"] is True, f"EXP-009 gate {g}")
    need(r9["gates"]["G2"]["sample_members"] == r9["gates"]["G2"]["agree_and_pure_in_I2"] == 55 and r9["gates"]["G2"]["failing_cases"] == [],
         "EXP-009 second instrument")
    tot = r9["totals"]
    rows, top = [], 0
    for e, p in LF_PAIRS:
        t = tot[f"{e}|{p}|X"]
        r = target_rank(e)
        need(t["members"] == t["members_planned"] == p ** 4 and t["target_rank"] == r, f"EXP-009 X {e},{p}: members and target rank")
        need(sum(t["rank_hist"].values()) == t["members"], f"EXP-009 X {e},{p}: the rank histogram does not sum to its member count")
        need(t["rank_above_r"] == 0 and t["rank_at_most_r"] == t["members"] and t["above_members"] == [], f"EXP-009 X {e},{p}: a member of rank above r")
        need(t["rank_exactly_r"] == t["rank_hist"].get(str(r), 0), f"EXP-009 X {e},{p}: members of rank r")
        need(t["examined"] <= t["rank_exactly_r"] and t["pure"] <= t["tables"] <= t["pure_hilbert"] <= t["examined"], f"EXP-009 X {e},{p}: counts")
        if p < 2 * e:
            need((t["pure"] > 0) == ((e, p) in LF_PURE), f"EXP-009 X {e},{p}: pure members {t['pure']}")
            need(t["rank_complete"] and (t["pure"] > 0 or t["s2_complete"]), f"EXP-009 X {e},{p}: an unfinished second stage with no pure member")
        else:
            need(t["pure"] >= t["tables"] // 2 and t["pure"] > 0, f"EXP-009 control {e},{p}: at least half of the tables pure")
        top += t["members"]
        for key, name in (("members", "Members"), ("rank_exactly_r", "RankR"), ("examined", "Examined"), ("pure_hilbert", "PureHF"), ("pure", "Pure")):
            N["lf%s%s%s" % (EW[e], PW[p], name)] = t[key]
        N["lf%s%sNonPure" % (EW[e], PW[p])] = t["tables"] - t["pure"]
        N["lf%s%sTables" % (EW[e], PW[p])] = t["tables"]
        y = tot.get(f"{e}|{p}|Y")
        rows.append((e, p, t, y))
    N["lfFamilyMembersBelow"] = thousands(sum(tot[f"{e}|{p}|X"]["members"] for e, p in LF_BELOW))
    # family Y
    ys = {(e, p): tot[f"{e}|{p}|Y"] for e, p in LF_BELOW if f"{e}|{p}|Y" in tot}
    need(sorted(ys) == sorted(k for k in LF_BELOW if k not in LF_PURE), "EXP-009: the pairs of family Y")
    for (e, p), y in ys.items():
        need(y["members"] == 20000 and y["rank_above_r"] == 0 and y["pure"] == 0 and y["field"] == f"GF({p * p})", f"EXP-009 Y {e},{p}")
        need(sum(y["rank_hist"].values()) == 20000 and y["rank_exactly_r"] == y["rank_hist"].get(str(target_rank(e)), 0), f"EXP-009 Y {e},{p}: histogram")
    N["lfYMembers"] = thousands(sum(y["members"] for y in ys.values()))
    N["lfYPairs"] = len(ys)
    N["lfYFiveFiveRankR"] = thousands(ys[(5, 5)]["rank_exactly_r"])
    N["lfYSixSevenRankR"] = thousands(ys[(6, 7)]["rank_exactly_r"])
    # predictions
    pr = r9["predictions"]
    need(all(v["holds"] for v in pr["P1"].values()) and len(pr["P1"]) == 15, "EXP-009 P1")
    need(sorted(k for k, v in pr["P2"].items() if v["holds"]) == sorted(f"{e},{p}" for e, p in LF_PURE) and [k for k, v in pr["P2"].items() if not v["holds"]] == ["6,7"], "EXP-009 P2: six pairs hold, (6,7) fails")
    need(len(pr["P3"]) == 8 and not any(v["holds"] for v in pr["P3"].values()), "EXP-009 P3: fails in all eight pairs")
    need(pr["P2"]["6,7"]["Y_pure_over_GF(p^2)"] == 0 and pr["P2"]["6,7"]["Y_examined"] == ys[(6, 7)]["rank_exactly_r"], "EXP-009 P2 at (6,7) over GF(49)")
    N["lfPtwoHold"] = len(LF_PURE)
    N["lfPthreeFail"] = 8
    N["lfBelowPairs"] = len(LF_BELOW)
    # the first pure member of each pair of the family: recomputed here
    prow = []
    for e, p in LF_PURE:
        s2 = r9["pairs"][f"{e}|{p}|X"]["s2"]
        mem = next(m for m in s2["members_pure_hilbert"] if m["pure"])
        a, b, c, d = mem["params"]
        pair = [terms_nested(x) for x in mem["basis"]]
        # the printed member is L_e(a, b, c, d) = < x^e + a x y^(e-1) + b y^(e-2) z, y^e + c x^(e-1) y + d x^(e-2) z >
        ref = [{(e, 0, 0): 1, (1, e - 1, 0): a % p, (0, e - 2, 1): b % p}, {(0, e, 0): 1, (e - 1, 1, 0): c % p, (e - 2, 0, 1): d % p}]
        for got, exp_ in zip(pair, ref):
            have = {m: v % p for m, v in got if v % p}
            need(have == {m: v for m, v in exp_.items() if v}, f"EXP-009 member {e},{p}: the stored basis is not L_e{tuple(mem['params'])}")
        ln = need_pure_pair(f"EXP-009 pair {e},{p}", pair, e, p)
        prow.append([f"$({e},{p})$", "$(%d,%d,%d,%d)$" % (a, b, c, d), "$f=%s$\\newline $g=%s$" % (poly_tex(pair[0], p), poly_tex(pair[1], p)), str(ln),
                     "$(1,2,2,1)$ on $(0,%d,%d,%d)$" % (e, 3 * e, 4 * e)])
    out["tab_lfampairs.tex"] = table("@{}lcp{5.4cm}rl@{}", ["$(e,p)$", "$(a,b,c,d)$", "forms over $\\F_p$", "length", "Betti table (both instruments)"], prow)
    # the table of the counts
    body = []
    for e, p, t, y in rows:
        if p < 2 * e:
            status = "pure members" if (e, p) in LF_PURE else "no pure member"
        else:
            status = "control"
        body.append([str(e), str(p), thousands(t["members"]), thousands(t["rank_exactly_r"]), str(t["rank_above_r"]), str(t["examined"]), str(t["pure_hilbert"]),
                     str(t["pure"]), ("%s of %s" % (thousands(y["pure"]), thousands(y["rank_exactly_r"]))) if y else "--", status])
    out["tab_lfam.tex"] = table("@{}rrrrrrrrrl@{}", ["$e$", "$p$", "members", "rank $r$", "rank $>r$", "examined", "pure $h_e$", "pure", "$\\F_{p^2}$: pure of rank $r$", "reading"], body)
    N["lfWallMin"] = f"{r9['wall_seconds_total'] / 60:.0f}"
    N["lfSingularSample"] = r9["gates"]["G2"]["sample_members"]


# ---- EXP-011 ----

CENTRAL_PURE = ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11", "T12", "T13", "G1", "G2", "G3"]
CENTRAL_N = ["N1", "N2", "N3", "N4", "N5"]


def exp11(r11, N, out):
    need(r11["experiment"] == "EXP-011", "EXP-011 results file")
    for g in ("G1", "G2", "G3"):
        need(r11["gates"][g]["passed"] is True, f"EXP-011 gate {g}")
    need(r11["gates"]["G2"]["compared"] == 16 and r11["gates"]["G2"]["failing_cases"] == [], "EXP-011 second instrument")
    cases = r11["cases"]
    need(sorted(cases) == sorted(CENTRAL_PURE + CENTRAL_N), "EXP-011 cases")
    need(r11["predictions"]["P1"]["holds"] and r11["predictions"]["P2"]["holds"], "EXP-011 predictions")
    rows = []
    for cid in CENTRAL_PURE:
        c = cases[cid]
        e, p = c["e"], c["p"]
        need(c["identities"]["all"] and all(c["identities"][k] for k in ("A_B_central", "commutator_is_lambda_z_e", "syzygy_s1", "syzygy_s2", "third_relation")), f"EXP-011 {cid}: identities")
        need(c["hilbert_equals_h_e"] and c["hilbert"][: 4 * e + 1] == [he_val(e, n) for n in range(4 * e + 1)], f"EXP-011 {cid}: Hilbert function")
        need(c["length"] == e ** 3 and c["length_equals_e3"], f"EXP-011 {cid}: length")
        for inst in ("betti_uhlib", "betti_singular"):
            need(c[inst]["status"] == "computed" and c[inst]["pure"] and c[inst]["table"] == pure_table(e), f"EXP-011 {cid}: {inst}")
        need(e % p == 0 and e % 2 == 1, f"EXP-011 {cid}: p divides the odd e")
        pair = [terms_nested(c["f"]), terms_nested(c["g"])]
        # the commutator g f - f g = lambda z^e, by the arithmetic of this script, for every case
        f_, g_ = elt_from_terms(pair[0]), elt_from_terms(pair[1])
        comm = commutator(f_, g_, p)
        lam = c["lambda"] % p
        need(lam != 0 and comm == {(0, 0, e): lam}, f"EXP-011 {cid}: g f - f g is not {lam} z^{e} (found {comm})")
        if e <= 13:
            need_pure_pair(f"EXP-011 {cid}", pair, e, p)
        rows.append([cid, f"$({e},{p})$", "$f=%s$\\newline $g=%s$" % (poly_tex(pair[0], p), poly_tex(pair[1], p)), str(lam), str(c["length"]), "yes" if c["betti_singular"]["pure"] else "no"])
    out["tab_central.tex"] = table("@{}llp{6.2cm}rrl@{}", ["case", "$(e,p)$", "forms over $\\F_p$", "$\\lambda$", "length", "pure in both instruments"], rows)
    # family N: outside the hypotheses
    nrows = []
    why = {"N1": "$l_1=0$", "N2": "$l_1,l_2$ dependent", "N3": "$p\\nmid e$", "N4": "$p\\nmid e$", "N5": "$\\bar A,\\bar B$ with a common factor"}
    for cid in CENTRAL_N:
        c = cases[cid]
        e, p = c["e"], c["p"]
        need(c["hilbert_equals_h_e"] is False and c["finite_length"] is False, f"EXP-011 {cid}: not of finite length within 5e")
        pair = [terms_nested(c["f"]), terms_nested(c["g"])]
        f_, g_ = elt_from_terms(pair[0]), elt_from_terms(pair[1])
        comm = commutator(f_, g_, p)
        is_pow = (len(comm) == 1 and list(comm)[0][:2] == (0, 0) and list(comm)[0][2] == e)
        need(is_pow == c["identities"]["commutator_is_lambda_z_e"], f"EXP-011 {cid}: the stored commutator identity")
        if cid in ("N1", "N2", "N3", "N4"):
            need(not is_pow, f"EXP-011 {cid}: the commutator is a multiple of z^e")
        nrows.append([cid, f"$({e},{p})$", "$f=%s$\\newline $g=%s$" % (poly_tex(pair[0], p), poly_tex(pair[1], p)), why[cid],
                      "yes" if is_pow else "no", "no"])
    out["tab_centralneg.tex"] = table("@{}llp{5.0cm}p{3.0cm}ll@{}", ["case", "$(e,p)$", "forms over $\\F_p$", "outside the hypotheses because", "$gf-fg=\\lambda z^e$", "finite length"], nrows)
    N["cenCases"] = len(CENTRAL_PURE)
    N["cenNegCases"] = len(CENTRAL_N)
    N["cenMaxLength"] = thousands(max(cases[c]["length"] for c in CENTRAL_PURE))
    N["cenSingular"] = r11["gates"]["G2"]["compared"]
    N["cenSeconds"] = f"{r11['spent_seconds']:.0f}"


# ---- EXP-012 ----

CRIT_X = ["B1", "B2", "B3", "B4", "B5", "C1", "C2", "C3", "D1", "D2", "D3"]
CRIT_R = ["4,3", "6,3", "6,5", "7,3", "7,7", "8,7", "9,3", "10,3"]
CASE_OF = {"B": "B", "C": "C", "D": "D"}


def exp12(r12, N, out):
    need(r12["experiment"] == "EXP-012", "EXP-012 results file")
    for g in ("G1", "G3"):
        need(r12["gates"][g]["passed"] is True, f"EXP-012 gate {g}")
    need(sorted(r12["X"]) == sorted(CRIT_X) and sorted(r12["R"]) == sorted(CRIT_R) and sorted(r12["N"]) == ["N1", "N2", "N3"], "EXP-012 cases")
    pr = r12["predictions"]
    need(pr["P1"]["holds"] and pr["P2"]["holds"] and pr["P3"]["holds"], "EXP-012 predictions")
    need(pr["P1"]["failing"] == {} and pr["P2"]["failing_identity"] == {} and pr["P2"]["disagreements"] == {}, "EXP-012 failures")
    rows = []
    for cid in CRIT_X:
        c = r12["X"][cid]
        e, p = c["e"], c["p"]
        need(c["identities"] == {"commutator": True, "s1": True, "s2": True, "g_s1_plus_f_s2": True}, f"EXP-012 {cid}: identities")
        need(c["criterion"]["holds"] is True and c["hilbert_is_h_e"] and c["length"] == e ** 3, f"EXP-012 {cid}: criterion, Hilbert function, length")
        need(c["betti_uhlib"] == pure_table(e) and c["singular"]["betti"] == pure_table(e) and c["singular"]["same_as_uhlib"], f"EXP-012 {cid}: Betti tables")
        need(e % p in (0, 1), f"EXP-012 {cid}: e is 0 or 1 modulo p")
        pair = [terms4(c["f"]), terms4(c["g"])]
        f_, g_ = elt_from_terms(pair[0]), elt_from_terms(pair[1])
        # D is a polynomial in X = x^p, Y = y^p, z; the commutator is - D z
        D = terms4(c["D"])
        negDz = central_poly([(m, -v) for m, v in D], p, shift_z=1)
        need(commutator(f_, g_, p) == {k: v % p for k, v in negDz.items() if v % p}, f"EXP-012 {cid}: g f - f g differs from - D z")
        # D recomputed from the data of the pair: D = beta_1 delta_2 - beta_2 delta_1 in GF(p)[X, Y, z]
        def pmul(a, b):
            r = {}
            for (i1, j1, k1), v1 in a:
                for (i2, j2, k2), v2 in b:
                    key = (i1 + i2, j1 + j2, k1 + k2)
                    r[key] = (r.get(key, 0) + v1 * v2) % p
            return r
        b1, b2 = terms4(c["data_f"]["beta1"]), terms4(c["data_f"]["beta2"])
        d1, d2 = terms4(c["data_g"]["delta1"]), terms4(c["data_g"]["delta2"])
        Dc = pmul(b1, d2)
        for key, v in pmul(b2, d1).items():
            Dc[key] = (Dc.get(key, 0) - v) % p
        need({k: v for k, v in Dc.items() if v} == {m: v % p for m, v in D if v % p}, f"EXP-012 {cid}: D recomputed from the data of the pair")
        if e <= 13:
            need_pure_pair(f"EXP-012 {cid}", pair, e, p)
        letter = cid[0]
        rows.append([cid, f"$({e},{p})$", letter, "$f=%s$\\newline $g=%s$" % (poly_tex(pair[0], p), poly_tex(pair[1], p)), str(c["length"])])
    out["tab_critpairs.tex"] = table("@{}lllp{6.0cm}r@{}", ["case", "$(e,p)$", "type", "forms over $\\F_p$", "length"], rows)
    # family R: random pairs of the class
    rr, tt, body, shares = r12["R"], r12["totals"]["R"], [], []
    tot_pairs = tot_crit = tot_betti = 0
    for key in CRIT_R:
        t, c = rr[key], tt[key]
        e, p = c["e"], c["p"]
        need(t["e"] == e and t["p"] == p and t["seed"] == c["seed"] and t["n_pairs"] == c["n_pairs"] == 200, f"EXP-012 R {key}: the case")
        need(c["identity"] == 200 and c["criterion"] == c["pure_hilbert"] == c["both"] and c["exactly_one"] == 0, f"EXP-012 R {key}: agreement")
        need(c["criterion_only"] == [] and c["pure_hilbert_only"] == [] and c["disagreements"] == [], f"EXP-012 R {key}: disagreements")
        need(c["betti_computed"] == c["betti_pure"] == 10 and c["betti_not_pure"] == [], f"EXP-012 R {key}: Betti tables")
        need(len(t["betti"]) == 10 and all(b["pure"] and b["betti"] == pure_table(e) for b in t["betti"].values()), f"EXP-012 R {key}: stored Betti tables")
        need(len(t["pairs"]) == 200 and sum(1 for x in t["pairs"] if x["criterion"]) == c["criterion"] and sum(1 for x in t["pairs"] if x["pure_hilbert"]) == c["pure_hilbert"]
             and all(x["criterion"] == x["pure_hilbert"] and x["identity"] for x in t["pairs"]), f"EXP-012 R {key}: per-pair flags")
        tot_pairs += c["n_pairs"]
        tot_crit += c["criterion"]
        tot_betti += c["betti_computed"]
        shares.append(c["criterion"] / c["n_pairs"])
        body.append([f"$({e},{p})$", str(c["seed"]), "200", str(c["identity"]), str(c["criterion"]), str(c["pure_hilbert"]), str(c["exactly_one"]), "%d of %d" % (c["betti_pure"], c["betti_computed"]), pct(c["criterion"] / 200, 1)])
        N["crit%s%sPure" % (EWL[e], PW[p])] = c["criterion"]
    out["tab_critrand.tex"] = table("@{}lrrrrrrrr@{}", ["$(e,p)$", "seed", "pairs", "identity holds", "criterion true", "pure $h_e$", "disagree", "pure Betti tables", "share (\\%)"], body)
    need(tot_pairs == 1600, "EXP-012 R totals")
    N["critRandomPairs"] = thousands(tot_pairs)
    N["critRandomPure"] = tot_crit
    N["critRandomBetti"] = tot_betti
    N["critShareMin"] = pct(min(shares), 0)
    N["critShareMax"] = pct(max(shares), 0)
    N["critXCases"] = len(CRIT_X)
    N["critMaxLength"] = thousands(max(r12["X"][c]["length"] for c in CRIT_X))
    N["critMinLength"] = min(r12["X"][c]["length"] for c in CRIT_X)
    # family N
    nrows = []
    why = {"N1": "case D without the term $x^3z^2$", "N2": "$n(f)=X^6$ vanishes on $X=0$ where $zD$ vanishes", "N3": "case C without $z^3$"}
    for cid in ("N1", "N2", "N3"):
        c = r12["N"][cid]
        e, p = c["e"], c["p"]
        need(c["criterion"]["holds"] is False and c["finite_length_within_5e"] is False and c["hilbert_is_h_e"] is False and c["identities"]["commutator"], f"EXP-012 {cid}")
        pair = [terms4(c["f"]), terms4(c["g"])]
        f_, g_ = elt_from_terms(pair[0]), elt_from_terms(pair[1])
        D = terms4(c["D"])
        negDz = central_poly([(m, -v) for m, v in D], p, shift_z=1)
        need(commutator(f_, g_, p) == {k: v % p for k, v in negDz.items() if v % p}, f"EXP-012 {cid}: g f - f g differs from - D z")
        nrows.append([cid, f"$({e},{p})$", "$f=%s$\\newline $g=%s$" % (poly_tex(pair[0], p), poly_tex(pair[1], p)), why[cid], "not within degree $%d$" % (5 * e)])
    out["tab_critneg.tex"] = table("@{}llp{4.6cm}p{4.2cm}l@{}", ["case", "$(e,p)$", "forms over $\\F_p$", "built to violate", "finite length"], nrows)
    N["critSeedFirst"] = tt["4,3"]["seed"]
    N["critRSeconds"] = thousands(round(sum(tt[k]["seconds"] for k in CRIT_R)))


# ---- the weight-class strata ----

def u_class(m, n):
    """u_k(n) = dim U_(n, [k]) for the classes k = 0..m-1: the sum of min(w, n - w) + 1 over the weights w = 0..n with w = k modulo m."""
    res = [0] * m
    if n >= 0:
        for w in range(n + 1):
            res[w % m] += min(w, n - w) + 1
    return res


def stratum_admissible(e, m, i, j):
    """S(m; i, j) is admissible for e when some classes (s1, s2, t) make H_k(n) >= 0 for all k and all 0 <= n <= 4e + 6m + 2."""
    import numpy as np
    nmax = 4 * e + 6 * m + 2
    U = [u_class(m, n) for n in range(nmax + 1)]

    def shifted(s, d):
        A = np.zeros((nmax + 1, m), dtype=np.int64)
        for n in range(d, nmax + 1):
            for k in range(m):
                A[n][k] = U[n - d][(k - s) % m]
        return A
    base = shifted(0, 0) - shifted(i, e) - shifted(j, e)
    S3 = [shifted(s, 3 * e) for s in range(m)]
    S4 = [shifted(t, 4 * e) for t in range(m)]
    for s1 in range(m):
        for s2 in range(s1, m):
            b2 = base + S3[s1] + S3[s2]
            for t in range(m):
                if (b2 - S4[t]).min() >= 0:
                    return True
    return False


def strata_tables(e):
    """For the degree e: the admissible strata (m, i, j), i <= j, for 2 <= m <= e + 1, and the refined admissible ones (the stratum and every
    stratum that contains it are admissible; moduli above e + 1 add nothing)."""
    adm = {}
    for m in range(2, e + 2):
        for i in range(m):
            for j in range(i, m):
                adm[(m, i, j)] = stratum_admissible(e, m, i, j)
    refined = {}
    for (m, i, j), ok in adm.items():
        good = ok
        for m2 in range(2, e + 2):
            if not good or m2 == m:
                continue
            wi = {w % m2 for w in range(e + 1) if w % m == i}
            wj = {w % m2 for w in range(e + 1) if w % m == j}
            if len(wi) == 1 and len(wj) == 1:
                a, b = sorted((next(iter(wi)), next(iter(wj))))
                good = adm[(m2, a, b)]
        refined[(m, i, j)] = good
    return adm, refined


STRATA_NOTE = {4: (17, 34, 11), 5: (19, 55, 9), 6: (34, 83, 19), 7: (34, 119, 13), 8: (58, 164, 30)}


def min_h(e, m, i, j, s1, s2, t):
    """The least value of H_k(n) over all classes k and all 0 <= n <= 4e + 6m + 2 for the classes (s1, s2, t)."""
    nmax = 4 * e + 6 * m + 2
    U = [u_class(m, n) for n in range(nmax + 1)]

    def u(k, n):
        return U[n][k % m] if n >= 0 else 0
    return min(u(k, n) - u(k - i, n - e) - u(k - j, n - e) + u(k - s1, n - 3 * e) + u(k - s2, n - 3 * e) - u(k - t, n - 4 * e)
               for n in range(nmax + 1) for k in range(m))


def strata_facts(N):
    """The statements on the admissible strata that the text makes for e = 4..10, checked from the definition."""
    allr = {e: strata_tables(e) for e in range(4, 11)}
    for e, (na, nt, nr) in {9: (60, 219, None), 10: (83, 285, None)}.items():
        adm, ref = allr[e]
        need((sum(adm.values()), len(adm)) == (na, nt), f"strata e={e}: admissible and total")
        N["strataAdm" + EWL[e]] = sum(adm.values())
        N["strataTotal" + EWL[e]] = len(adm)
    adm9 = allr[9][0]
    need(sum(1 for (m_, i, j), ok in adm9.items() if m_ == 3 and ok) == 6 and sum(1 for (m_, i, j), ok in adm9.items() if m_ == 6 and ok) == 3, "strata e=9: m=3 admits six strata and m=6 three")
    for e in range(4, 11):
        adm, ref = allr[e]
        # stable under the exchange of x and y
        need(all(adm[(m_, i, j)] == adm[(m_, *sorted(((e - i) % m_, (e - j) % m_)))] for (m_, i, j) in adm), f"strata e={e}: the list is not stable under the exchange")
        # m = e + 1: only (0, e)
        need([(i, j) for (m_, i, j), ok in adm.items() if m_ == e + 1 and ok] == [(0, e)], f"strata e={e}: m = e + 1")
        # m divides e: nothing is excluded, with the witness (i, j, 0)
        for m_ in range(2, e + 1):
            if e % m_ == 0:
                need(all(ok for (mm, i, j), ok in adm.items() if mm == m_), f"strata e={e}, m={m_}: m divides e and a stratum is excluded")
                need(all(min_h(e, m_, i, j, i, j, 0) >= 0 for (mm, i, j) in adm if mm == m_), f"strata e={e}, m={m_}: the witness (i, j, 0)")
    for e in range(4, 9):
        adm = allr[e][0]
        for m_ in range(2, e + 2):
            need(adm[(m_, 0, e % m_)], f"strata e={e}, m={m_}: the stratum of the power pair")
    for e in (5, 7):
        adm = allr[e][0]
        for m_ in range(2, e):
            need([(i, j) for (mm, i, j), ok in adm.items() if mm == m_ and ok] == [(0, e % m_)] or (m_ == e and False), f"strata e={e}, m={m_}: only the stratum of the power pair")
    single = {(4, 5), (6, 5), (6, 7), (8, 5), (8, 7), (8, 9)}
    several = {(4, 3), (6, 4), (8, 3), (8, 6)}
    for e in (4, 6, 8):
        adm = allr[e][0]
        for m_ in range(2, e + 2):
            if e % m_:
                cnt = sum(1 for (mm, i, j), ok in adm.items() if mm == m_ and ok)
                need((cnt == 1) == ((e, m_) in single) and (cnt > 1) == ((e, m_) in several), f"strata e={e}, m={m_}: {cnt} admissible strata")
    # the main case of the containment remark: m = e, i, j >= 1 are lost; the refined list keeps (0, j) only
    for e in range(4, 11):
        adm, ref = allr[e]
        need(sorted((i, j) for (m_, i, j), ok in ref.items() if m_ == e and ok) == [(0, j) for j in range(e)], f"strata e={e}: the refined strata with m = e")
        need(all(ref[k] == adm[k] for k in adm if k[0] != e), f"strata e={e}: the refined list differs from the admissible one outside m = e")
    N["strataFactsMaxE"] = 10


def strata_output(N, out):
    strata_facts(N)
    rows = []
    for e in range(4, 9):
        adm, ref = strata_tables(e)
        na, nt, nr = sum(adm.values()), len(adm), sum(ref.values())
        need((na, nt, nr) == STRATA_NOTE[e], f"strata e={e}: admissible, total, refined admissible {(na, nt, nr)} differ from {STRATA_NOTE[e]}")
        N["strataAdm" + EWL[e]] = na
        N["strataTotal" + EWL[e]] = nt
        N["strataRef" + EWL[e]] = nr
        for m in range(2, e + 2):
            al = sorted((i, j) for (mm, i, j), ok in adm.items() if mm == m and ok)
            rf = sorted((i, j) for (mm, i, j), ok in ref.items() if mm == m and ok)
            tot = m * (m + 1) // 2
            def fmt(lst):
                if len(lst) == tot and tot > 3:
                    return "all %d" % tot
                if lst == [(0, j) for j in range(m)] and m > 3:
                    return "$(0,j)$, $0\\le j\\le %d$" % (m - 1)
                return ", ".join("$(%d,%d)$" % t for t in lst)
            rows.append([str(e), str(m), str(tot), str(len(al)), fmt(al), str(len(rf)), fmt(rf)])
    out["tab_strata.tex"] = table("@{}rrrrp{4.2cm}rp{3.6cm}@{}", ["$e$", "$m$", "strata", "admissible", "admissible $(i,j)$", "refined", "refined admissible $(i,j)$"], rows)
    tot_rows = []
    for e in range(4, 9):
        tot_rows.append([str(e), str(N["strataTotal" + EWL[e]]), str(N["strataAdm" + EWL[e]]), str(N["strataRef" + EWL[e]])])
    out["tab_stratatot.tex"] = table("@{}rrrr@{}", ["$e$", "strata $S(m;i,j)$, $2\\le m\\le e+1$", "admissible", "refined admissible"], tot_rows)


# ---- the state of the point (1, 2, 2, 1) on (0, e, 3e, 4e) in odd characteristic below 2e ----

def grid_cells(emax, explicit, linear, extra=()):
    """The label of every cell (e, p), 2 <= e <= emax, p an odd prime below 2e, by rule from the theorems and the stored results.
    C: p divides e (e - 1) and e >= 3 (the criterion and its explicit pairs); P: e = d e' with d >= 3, d < e, d = 0 or 1 modulo p and
    e' settled in characteristic p (the pull-back); L: a pure member of the four-parameter linear family (stored); S: a pure pair found
    by search in the whole space of pairs and stored (explicit); then the labels of `extra`, a list of (label, set of pairs) in order
    (W: found by the search in the weight-class strata, M: found in the middle stratum); None: open. The case p at least 2e is Theorem A
    and is not a cell, but it settles e' in the pull-back rule; e' = 1 is the trivial module."""
    sets = [("L", linear), ("S", explicit)] + list(extra)

    def settled(e, p, memo):
        if e == 1 or p >= 2 * e:
            return True
        return label(e, p, memo) is not None

    def label(e, p, memo):
        if (e, p) in memo:
            return memo[(e, p)]
        memo[(e, p)] = None            # no cycle: e' < e
        res = None
        if e >= 3 and (e * (e - 1)) % p == 0:
            res = "C"
        else:
            for d in range(3, e):
                if e % d == 0 and d % p in (0, 1) and settled(e // d, p, memo):
                    res = "P"
                    break
            if res is None:
                for lab, st in sets:
                    if (e, p) in st:
                        res = lab
                        break
        memo[(e, p)] = res
        return res
    memo = {}
    cells = {}
    for e in range(2, emax + 1):
        for p in primes_upto(2 * e - 1):
            if p % 2 == 1:
                cells[(e, p)] = label(e, p, memo)
    return cells


CELL_COLOR = {"C": "blue!55", "P": "violet!50", "L": "teal!55", "S": "orange!65", "W": "red!45", "M": "yellow!70!orange", "O": "green!45", "F": "cyan!45", "G": "pink!70", "H": "lime!45", "E": "brown!40", "X": "magenta!35", None: "white"}


def cell_sources(e, p, lab, detail):
    """The result that settles a cell, in words (for the table of the sources)."""
    if lab == "C":
        case = {(1, 1): "D", (1, 0): "A", (0, 1): "B", (0, 0): "C"}[(e % 2, 0 if e % p == 0 else 1)]
        return "criterion, case %s (EXP-012 and EXP-011)" % case if case in "ABCD" else ""
    if lab == "P":
        for d in range(3, e):
            if e % d == 0 and d % p in (0, 1):
                return "pull-back, $d=%d$, $e'=%d$" % (d, e // d)
    return detail.get((e, p), "")


def state_outputs(N, out, explicit, linear, emax=16, extra=(), detail=None):
    detail = detail or {}
    cells = grid_cells(emax, explicit, linear, extra)
    cnt = Counter(v for v in cells.values())
    N["gridCells"] = len(cells)
    N["gridOpen"] = cnt[None]
    for k in ("C", "L", "S", "P", "W", "M", "O", "F", "G", "H", "E", "X"):
        N["gridBy" + k] = cnt[k]
    ps = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    body = []
    for e in range(2, 17):
        row = [str(e)]
        for p in ps:
            if p >= 2 * e:
                row.append("A")
            else:
                v = cells[(e, p)]
                row.append(v if v else "open")
        body.append(row)
    out["tab_state.tex"] = table("@{}rcccccccccc@{}", ["$e$"] + ["$p=%d$" % p for p in ps], body)
    open_cells = sorted(k for k, v in cells.items() if v is None)
    N["gridOpenList"] = ", ".join("$(%d,%d)$" % k for k in open_cells) if open_cells else "none"
    N["gridOpenListSmall"] = ", ".join("$(%d,%d)$" % k for k in open_cells if k[0] <= 8) if any(k[0] <= 8 for k in open_cells) else "none"
    open16 = [k for k in open_cells if k[0] <= 16]
    need(open16 == [(11, 3)], f"grid: the open pairs with e <= 16 are not exactly (11,3): {open16}")
    N["gridOpenListSixteen"] = ", ".join("$(%d,%d)$" % k for k in open16)
    N["gridOpenListFourteen"] = ", ".join("$(%d,%d)$" % k for k in open_cells if k[0] <= 14)
    N["gridOpenListTwelve"] = ", ".join("$(%d,%d)$" % k for k in open_cells if k[0] <= 12)
    N["gridOpenNine"] = ", ".join("$(%d,%d)$" % k for k in open_cells if k[0] == 9)
    mx = 1
    for e in range(2, emax + 1):
        if all(cells[(e, p)] is not None for p in primes_upto(2 * e - 1) if p % 2 == 1):
            mx = e
        else:
            break
    N["gridSettledMaxE"] = mx
    # the table of the sources for e <= 8
    srows, srowsb, srowsc = [], [], []
    for e in range(2, 17):
        for p in [q for q in primes_upto(2 * e - 1) if q % 2 == 1]:
            lab = cells[(e, p)]
            (srows if e <= 10 else (srowsb if e <= 14 else srowsc)).append(["$(%d,%d)$" % (e, p), lab if lab else "open", cell_sources(e, p, lab, detail) if lab else "no pure pair known"])
    need(len(srows) == 36 and len(srowsb) == 31 and len(srowsc) == 19, f"the sources tables have {len(srows)}, {len(srowsb)} and {len(srowsc)} rows, not 36, 31 and 19")
    out["tab_statesrcc.tex"] = table("@{}llp{9.8cm}@{}", ["$(e,p)$", "code", "what settles the pair"], srowsc)
    out["tab_statesrc.tex"] = table("@{}llp{9.8cm}@{}", ["$(e,p)$", "code", "what settles the pair"], srows)
    out["tab_statesrcb.tex"] = table("@{}llp{9.8cm}@{}", ["$(e,p)$", "code", "what settles the pair"], srowsb)
    cols = [p for p in primes_upto(2 * emax - 1) if p % 2 == 1]
    lines = ["\\begin{tikzpicture}[x=0.62cm,y=0.5cm,font=\\scriptsize]"]
    for ci, p in enumerate(cols):
        lines.append("\\node at (%d,%d) {%d};" % (ci, emax + 1, p))
    lines.append("\\node[anchor=east] at (-0.7,%d) {$p$};" % (emax + 1))
    for e in range(2, emax + 1):
        lines.append("\\node[anchor=east] at (-0.7,%d) {%d};" % (emax - e + 1, e))
        for ci, p in enumerate(cols):
            if p >= 2 * e:
                lines.append("\\fill[gray!12] (%.2f,%.2f) rectangle (%.2f,%.2f);" % (ci - 0.5, emax - e + 0.5, ci + 0.5, emax - e + 1.5))
                continue
            v = cells[(e, p)]
            lines.append("\\draw[fill=%s] (%.2f,%.2f) rectangle (%.2f,%.2f);" % (CELL_COLOR[v], ci - 0.5, emax - e + 0.5, ci + 0.5, emax - e + 1.5))
            lines.append("\\node at (%d,%d) {%s};" % (ci, emax - e + 1, v if v else "?"))
    lines.append("\\node[anchor=east] at (-0.7,0) {$e$};")
    leg_x = len(cols) + 0.6
    entries = [("C", "central commutator, $p\\mid e(e-1)$"), ("P", "pull-back, $e=de'$"), ("L", "short pair, linear family"), ("S", "search, whole space"),
               ("W", "search in weight-class strata"), ("M", "middle stratum"), ("O", "other strata at e = 9"), ("F", "filter, odd e"), ("G", "list of forms, even e"), ("H", "largest exponent stratum"), ("E", "filter, every exponent"), ("X", "members fixed by exchange"), (None, "open")]
    for k, (code, nm) in enumerate(entries):
        y = emax - 1.15 * k
        lines.append("\\draw[fill=%s] (%.2f,%.2f) rectangle (%.2f,%.2f);" % (CELL_COLOR[code], leg_x, y - 0.4, leg_x + 0.8, y + 0.4))
        lines.append("\\node at (%.2f,%.2f) {%s};" % (leg_x + 0.4, y, code if code else "?"))
        lines.append("\\node[anchor=west] at (%.2f,%.2f) {%s};" % (leg_x + 1.0, y, nm))
    y = emax - 1.15 * len(entries)
    lines.append("\\fill[gray!12] (%.2f,%.2f) rectangle (%.2f,%.2f);" % (leg_x, y - 0.4, leg_x + 0.8, y + 0.4))
    lines.append("\\node[anchor=west] at (%.2f,%.2f) {Theorem A, $p\\ge2e$};" % (leg_x + 1.0, y))
    lines.append("\\end{tikzpicture}")
    out["fig_grid.tex"] = "\n".join(lines) + "\n"
    return cells


def explicit_from_artifacts(r6, r8, N_gf3):
    """The pairs (e, p) with a pure pair found by search and stored: the prime-field families of the searches in odd characteristic,
    and the pairs of quadrics over F_3 of the characteristic 3 study."""
    pairs = set()
    for t in r6["totals"]["per_field"].values():
        if t["pure"] > 0 and t["q"] == t["char"]:
            pairs.add((t["e"], t["char"]))
    for t in r8["totals"].values():
        if t["pure"] > 0 and t["q"] == int(t["field"][3:-1]):
            pairs.add((t["e"], t["q"]))
    if N_gf3 > 0:
        pairs.add((2, 3))
    return pairs


def search_sets_from_artifacts(r10, r14, r15=None, r17=None, r16=None):
    lst_pairs = lists_pairs(r16) if r16 is not None else {}
    """The pairs (e, p) with a pure pair stored by the search in the weight-class strata (W), in the middle stratum (M), in the other
    strata at e = 9 (O, EXP-015), by the filter (F, EXP-017) and by the lists of forms (G, EXP-016), with the stratum of the first pure
    pair of each, for the table of the sources. The pairs of the stratum of the linear family are returned by `linear_from_artifacts`."""
    w, mid, oth, flt, lst, detail = set(), set(), set(), set(), set(), {}
    lin = lambda s: (s["m"], s["i"], s["j"]) == (s["e"] - 1, 0, 1)
    for s in r10["strata"].values():
        if s["pure"] and s["family"] in "QE" and not lin(s):
            w.add((s["e"], s["p"]))
    for s in r14["strata"].values():
        if s["pure"] and s["family"] in "VW" and not lin(s):
            mid.add((s["e"], s["p"]))
    if r15 is not None:
        for s in r15["strata"].values():
            if s["pure"] and s["family"] == "R":
                oth.add((s["e"], s["p"]))
    if r17 is not None:
        for c in r17["cases"].values():
            if c["pure"] and c["family"] in "QX":
                flt.add((c["e"], c["p"]))
    for (e, p) in sorted(w):
        cands = sorted(((s["m"], s["i"], s["j"]) for s in r10["strata"].values() if (s["e"], s["p"]) == (e, p) and s["pure"] and s["family"] in "QE" and not lin(s)), reverse=True)
        detail[(e, p)] = "search in strata (EXP-010), $S(%d;%d,%d)$" % cands[0]
    for (e, p) in sorted(mid):
        s = next(x for x in r14["strata"].values() if (x["e"], x["p"]) == (e, p) and x["pure"] and x["family"] in "VW" and not lin(x))
        if (e, p) not in w:
            detail[(e, p)] = "middle stratum (EXP-014), $S(%d;%d,%d)$" % (s["m"], s["i"], s["j"])
    for (e, p) in sorted(oth):
        s = sorted((x for x in r15["strata"].values() if (x["e"], x["p"]) == (e, p) and x["pure"] and x["family"] == "R"), key=lambda x: -x["m"])[0]
        detail.setdefault((e, p), "other strata at $e=9$ (EXP-015), $S(%d;%d,%d)$" % (s["m"], s["i"], s["j"]))
    for (e, p) in sorted(flt):
        detail.setdefault((e, p), "filter in $S(%d;0,%d)$ (EXP-017)" % ((e + 1) // 2, (e - 1) // 2))
    for (e, p), n in sorted(lst_pairs.items()):
        if p < 2 * e and p % 2 == 1:
            lst.add((e, p))
            detail.setdefault((e, p), "a form of the list by one congruence (EXP-016), %d form%s" % (n, "" if n == 1 else "s"))
    return w, mid, oth, flt, lst, detail


def linear_from_artifacts(r9, r10=None, r14=None, r15=None):
    """The pairs (e, p), e < p < 2e, with a pure member in the stratum S(e-1; 0, 1) of the linear family (the chart of EXP-009 and the
    stratum itself in the other computations)."""
    res = {(e, p) for e, p in LF_BELOW if r9["totals"][f"{e}|{p}|X"]["pure"] > 0}
    if r10 is not None:
        res |= linear_strata_pairs(r9, r10, r14, r15) and {k for k, v in linear_strata_pairs(r9, r10, r14, r15).items() if v[1] > 0}
    return res


import re as _re


def module_math(text):
    """The module text of EXP-013 as TeX: exponents braced, spaces removed."""
    return "$" + _re.sub(r"\^(\d+)", r"^{\1}", text).replace(" ", "") + "$"


# --------------------------------------------------------------------------------------------------------------------------
# the second set of later computations: EXP-010 (weight-class strata), EXP-013 (pull-backs), EXP-014 (middle strata)
# --------------------------------------------------------------------------------------------------------------------------

PW.update({17: "Seventeen"})
EWL.update({14: "Fourteen", 16: "Sixteen"})


def read_second(root):
    ex = Path(root) / "experiments"
    return tuple(jload(ex / d.name / "artifacts" / "results.json") for d in (E10, E13, E14))


def monos_list(d):
    """The monomials x^a y^b z^c of degree d in the order of the library (uhlib.algebra.monos), as (a, b, c)."""
    return [(a, d - 2 * c - a, c) for c in range(d // 2 + 1) for a in range(d - 2 * c + 1)]


def member_terms(e, p, mem):
    """The two forms of a stored member: the coefficient vectors are on the monomials x^a y^b z^c (product order) of degree e."""
    B = monos_list(e)
    tf = [(B[i], v % p) for i, v in enumerate(mem["f"]) if v % p]
    tg = [(B[i], v % p) for i, v in enumerate(mem["g"]) if v % p]
    return tf, tg


def in_stratum(tf, tg, m, i, j):
    """f is supported on the monomials of class weight i modulo m and g on those of class j (the class weight of x^a y^b z^c is b + c)."""
    return all((b + c) % m == i % m for (a, b, c), v in tf) and all((b + c) % m == j % m for (a, b, c), v in tg)


def pair_row(label, e, p, mem, stratum=None, check_length=True):
    """Verify a stored pure member with the arithmetic of this script and return (terms of f, terms of g, length)."""
    tf, tg = member_terms(e, p, mem)
    need(mem["pure"] is True and mem["betti"] == pure_table(e), f"{label}: stored Betti table")
    if stratum is not None:
        need(in_stratum(tf, tg, *stratum), f"{label}: the member does not lie in the stratum S{stratum}")
    ln = need_pure_pair(label, [tf, tg], e, p) if check_length else e ** 3
    return tf, tg, ln


def stratum_name(s):
    return "S(%d;%d,%d)" % (s["m"], s["i"], s["j"]) if "m" in s else "S(%d;%d,%d)" % tuple(s["stratum"])


# ---- EXP-010 ----

E10_PAIRS_OPEN = [(6, 5), (6, 7), (7, 3), (7, 5), (7, 7)]
E10_PAIRS_E8 = [(8, 11), (8, 13), (8, 3), (8, 5), (8, 7)]
E10_P5 = {(8, 11): False, (8, 13): True, (8, 3): True, (8, 5): False, (8, 7): True}


def exp10(r10, N, out):
    need(r10["experiment"] == "EXP-010", "EXP-010 results file")
    need(r10["gates"]["G1"]["direct"].get("passed", r10["gates"]["G1"]["direct"]) is True and r10["gates"]["G1"]["after_c"].get("passed", r10["gates"]["G1"]["after_c"]) is True, "EXP-010 gate G1")
    for g in ("G2", "G3", "G4"):
        need(r10["gates"][g]["passed"] is True, f"EXP-010 gate {g}")
    need(r10["gates"]["G2"]["sample_members"] == r10["gates"]["G2"]["agree_and_pure_in_I2"] == 114 and r10["gates"]["G2"]["failing_cases"] == [], "EXP-010 second instrument")
    g4 = r10["gates"]["G4"]
    need(g4["strata_not_admissible"] == 410 and g4["members_examined"] == 785982 and g4["with_pure_hilbert_function"] == 0, "EXP-010 G4: the exclusion")
    st, tot = r10["strata"], r10["totals"]
    need(len(st) == 840 and len(tot) == 19, "EXP-010: 840 strata and 19 rows")
    rows, grand, pure_strata = [], 0, {}
    nadm = 0
    for key, t in sorted(tot.items(), key=lambda kv: ("CQE".index(kv[1]["family"]), kv[1]["e"], kv[1]["p"])):
        fam, e, p = t["family"], t["e"], t["p"]
        mine = [s for s in st.values() if (s["family"], s["e"], s["p"]) == (fam, e, p)]
        need(len(mine) == t["strata_stored"] == t["strata_planned"] and t["finished"] is True, f"EXP-010 {key}: strata stored")
        for fld, sk in (("members_examined", "examined"), ("rank_r", "rank_r"), ("pure_hilbert", "pure_hilbert"), ("tables", "tables"), ("pure", "pure")):
            need(sum(s[sk] for s in mine) == t[fld], f"EXP-010 {key}: the total {fld} differs from the sum over strata")
        need(t["r"] == target_rank(e) and t["h_3e"] == he_val(e, 3 * e), f"EXP-010 {key}: r and h_e(3e)")
        need(sum(1 for s in mine if s["rank_r"]) == t["strata_with_rank_r"] and sum(1 for s in mine if s["pure"]) == t["strata_with_pure"], f"EXP-010 {key}: strata with rank r and with pure members")
        pd = [s for s in mine if s["m"] % p == 0]
        need(sum(s["rank_r"] for s in pd) == 0 == t["rank_r_when_p_divides_m"] and sum(s["examined"] for s in pd) == t["examined_when_p_divides_m"], f"EXP-010 {key}: a member of rank r in a stratum with p dividing m")
        for s in mine:
            need(sum(s["rank_hist"].values()) == s["examined"] and s["pure"] <= s["tables"] <= s["pure_hilbert"] <= s["rank_r"] <= s["examined"], f"EXP-010 {key}: counts of a stratum")
            if fam == "C" and not s["admissible"]:
                need(s["pure_hilbert"] == 0, f"EXP-010 {key}: a stratum that is not admissible holds a member with the pure Hilbert function")
        grand += t["members_examined"]
        pure_strata[(e, p)] = sorted(((s["m"], s["i"], s["j"], s["pure"]) for s in mine if s["pure"]), reverse=True)
        s20 = t["s20"]
        share = ("%.3g (%d of %s)" % (s20["share"], s20["pure_hilbert"], thousands(s20["examined"]))) if s20 else "--"
        rows.append([fam, str(e), str(p), "%d" % t["strata_stored"], str(t["strata_with_rank_r"]), str(t["strata_with_pure"]), thousands(t["members_examined"]),
                     thousands(t["rank_r"]), thousands(t["pure_hilbert"]), str(t["tables"]), str(t["pure"]), share,
                     ("%.2f" % s20["ratio"]) if s20 else "--"])
        N["wc%s%s%sExamined" % (fam, EWL[e], PW[p])] = thousands(t["members_examined"])
        N["wc%s%s%sRankR" % (fam, EWL[e], PW[p])] = thousands(t["rank_r"])
        N["wc%s%s%sPure" % (fam, EWL[e], PW[p])] = t["pure"]
        N["wc%s%s%sStrataPure" % (fam, EWL[e], PW[p])] = t["strata_with_pure"]
        N["wc%s%s%sPureHF" % (fam, EWL[e], PW[p])] = thousands(t["pure_hilbert"])
    need(grand == 41043876, f"EXP-010: members examined in all, {grand}")
    N["wcMembers"] = thousands(grand)
    N["wcStrata"] = len(st)
    N["wcNonAdm"] = g4["strata_not_admissible"]
    N["wcNonAdmMembers"] = thousands(g4["members_examined"])
    N["wcSingular"] = r10["gates"]["G2"]["sample_members"]
    N["wcSeconds"] = thousands(round(r10["budget"]["used_seconds"]))
    out["tab_wcounts.tex"] = table("@{}lrrrrrrrrrrll@{}", ["fam.", "$e$", "$p$", "strata", "rank $r$", "pure", "examined", "rank $r$", "pure $h_e$", "tables", "pure", "share in $S(2;0,1)$", "ratio"], rows)
    # predictions
    pr = r10["predictions"]
    need(all(v["holds"] for v in pr["P1"].values()) and sorted(pr["P1"]) == sorted("%d,%d" % k for k in E10_PAIRS_OPEN), "EXP-010 P1")
    need(len(pr["P2"]) == 11 and all(v["holds"] for v in pr["P2"].values()), "EXP-010 P2")
    ratios = sorted(v["ratio_to_p_power"] for v in pr["P2"].values())
    need(0.1 <= ratios[0] and ratios[-1] <= 1.5, "EXP-010 P2: the ratios lie in [0.1, 1.5]")
    N["wcRatioMin"] = "%.2f" % ratios[0]
    N["wcRatioMax"] = "%.2f" % ratios[-1]
    need(pr["P3"]["holds"] is True if "holds" in pr["P3"] else g4["passed"], "EXP-010 P3")
    need(all(v["holds"] for v in pr["P4"].values()) and len(pr["P4"]) == 14, "EXP-010 P4")
    N["wcPfourMembers"] = thousands(sum(v["members_examined_there"] for v in pr["P4"].values()))
    for k, want in E10_P5.items():
        need(pr["P5"]["%d,%d" % k]["holds"] is want, f"EXP-010 P5 at {k}")
    need(pr["P5"]["8,11"]["S(7; 0, 1)"]["examined"] == 17689 and pr["P5"]["8,11"]["S(7; 0, 1)"]["pure"] == 0 and pr["P5"]["8,11"]["S(7; 0, 1)"]["complete"], "EXP-010 P5 (8,11)")
    # the pairs of the open characteristics and of e = 8, recomputed here
    prow = []
    for (e, p) in E10_PAIRS_OPEN + [(8, 3), (8, 7), (8, 13)]:
        fam = "Q" if e < 8 else "E"
        cand = sorted(((s["m"], s["i"], s["j"], key) for key, s in st.items() if (s["family"], s["e"], s["p"]) == (fam, e, p) and s["pure"]), reverse=True)
        need(bool(cand), f"EXP-010 {e},{p}: a stratum with a pure member")
        m_, i_, j_, key = cand[0]
        mem = next(x for x in st[key]["members"] if x["pure"])
        tf, tg, ln = pair_row(f"EXP-010 pair {e},{p}", e, p, mem, (m_, i_, j_))
        prow.append([f"$({e},{p})$", "$S(%d;%d,%d)$" % (m_, i_, j_), "$f=%s$\\newline $g=%s$" % (poly_tex(tf, p), poly_tex(tg, p)), str(ln)])
        N["wcPair%s%s" % (EWL[e], PW[p])] = len(prow)
    out["tab_wcpairs.tex"] = table("@{}llp{6.4cm}r@{}", ["$(e,p)$", "stratum", "forms over $\\F_p$", "length"], prow)
    # the strata that hold pure members in each pair
    srow = []
    for (e, p), lst in sorted(pure_strata.items()):
        if (e, p) in [(4, 3), (4, 5), (5, 3), (5, 5), (5, 7), (6, 3), (6, 11), (7, 11), (7, 13)]:
            continue
        srow.append([f"$({e},{p})$", ", ".join("$S(%d;%d,%d)$ (%d)" % x for x in lst) if lst else "none"])
    out["tab_wcstrata.tex"] = table("@{}lp{11.2cm}@{}", ["$(e,p)$", "strata with pure members (number of pure members)"], srow)
    N["wcPureSixFive"] = sum(x[3] for x in pure_strata[(6, 5)])
    # the strata left once the strata with p dividing m are dropped (remark 4 of the note on the characteristic dividing m)
    left = {}
    for e, p in ((6, 5), (6, 7), (7, 3), (7, 5), (7, 7)):
        adm, ref = strata_tables(e)
        left[(e, p)] = sum(1 for (m_, i, j), ok in ref.items() if ok and not (p <= e and m_ % p == 0))
    need(left == {(6, 5): 18, (6, 7): 19, (7, 3): 11, (7, 5): 12, (7, 7): 6}, f"strata left after dropping the moduli divisible by p: {left}")
    N["wcLeftSixFive"], N["wcLeftSevenThree"], N["wcLeftSevenFive"], N["wcLeftSevenSeven"] = 18, 11, 12, 6
    # the figure: share of the pure Hilbert function in S(2; 0, 1) against p^(-h_e(3e))
    pts = []
    for key, t in tot.items():
        s20 = t["s20"]
        if s20 and s20["pure_hilbert"] > 0:
            pts.append((t["e"], t["p"], s20["p_power"], s20["share"]))
    need(len(pts) == 12, "EXP-010: twelve points in the figure")
    import math as _m

    def lg(x):
        return _m.log10(x)
    lines = ["\\begin{tikzpicture}[x=1.25cm,y=1.25cm,font=\\scriptsize]"]
    for k in range(-6, 1):
        lines.append("\\draw[gray!35] (%d,-6) -- (%d,0); \\draw[gray!35] (-6,%d) -- (0,%d);" % (k, k, k, k))
        lines.append("\\node[below] at (%d,-6) {$10^{%d}$}; \\node[left] at (-6,%d) {$10^{%d}$};" % (k, k, k, k))
    lines.append("\\draw[thick] (-6,-6) rectangle (0,0);")
    lines.append("\\draw[dashed] (-6,-6) -- (0,0) node[pos=0.93,above,sloped]{share $=p^{-h_e(3e)}$};")
    for c_, lc in ((0.1, lg(0.1)), (1.5, lg(1.5))):
        x0, x1 = max(-6.0, -6.0 - lc), min(0.0, -lc)
        lines.append("\\draw[dotted] (%.3f,%.3f) -- (%.3f,%.3f);" % (x0, x0 + lc, x1, x1 + lc))
    for e, p, x, y in sorted(pts):
        lines.append("\\node[circle,draw,fill=white,inner sep=0.8pt,font=\\tiny] at (%.3f,%.3f) {%d};" % (lg(x), lg(y), e))
    lines.append("\\node[below=14pt] at (-3,-6) {$p^{-h_e(3e)}$ (the heuristic share)}; \\node[rotate=90,above=20pt] at (-6,-3) {share of the pure Hilbert function};")
    lines.append("\\end{tikzpicture}")
    out["fig_wcshare.tex"] = "\n".join(lines) + "\n"
    s1, s3 = st["E|8|3|4|0|1"], st["E|8|3|4|0|3"]
    need((s1["pure_hilbert"], s1["tables"], s1["pure"]) == (230, 40, 0) and (s3["tables"], s3["pure"]) == (40, 4), "EXP-010: the pure Hilbert function does not give the pure table at (8,3)")
    N["wcEEightThreeHFFour"] = s1["pure_hilbert"]
    cut = {"C|6|11|5|0|1": (15000, 17689), "C|7|11|7|0|3": (13000, 17568), "C|7|11|7|0|4": (17000, 17568), "C|7|11|6|0|1": (17000, 17689),
           "Q|7|3|4|0|3": (12000, 14641), "Q|7|7|5|0|2": (48000, 160000)}
    for k, (ex, nn) in cut.items():
        need(st[k]["examined"] == ex and st[k]["N"] == nn and st[k]["stopped_early"] and st[k]["pure"] > 0, f"EXP-010 {k}: the enumeration cut by the early stop")
    need(sum(1 for s in st.values() if s["stopped_early"] and s["N"] and s["examined"] < s["N"]) >= 6, "EXP-010: at least six enumerations cut")
    return pure_strata


# ---- EXP-013 ----

E13_S = {"S1": (3, 3, 6), "S2": (3, 4, 8), "S3": (5, 6, 12), "S4": (5, 5, 10), "S5": (7, 8, 16), "S6": (3, 3, 9), "S7": (7, 8, 24)}
E13_T = {"T1": (3, 3), "T2": (5, 6), "T3": (3, 4)}


def scale_table(tab, d):
    return [[i, j * d, b] for i, j, b in tab]


def exp13(r13, N, out):
    need(r13["experiment"] == "EXP-013", "EXP-013 results file")
    for g in ("G1", "G2", "G3"):
        need(r13["gates"][g]["passed"] is True, f"EXP-013 gate {g}")
    cs = r13["cases"]
    need(sorted(cs) == sorted(list(E13_S) + list(E13_T) + ["N1", "N2"]), "EXP-013 cases")
    need(r13["predictions"]["P1"]["holds"] and r13["predictions"]["P2"]["holds"], "EXP-013 predictions")
    rows = []

    def subst(phi, terms, p):
        """phi applied to the element sum c x^a y^b z^c (product order): the product phi(x)^a phi(y)^b phi(z)^c."""
        res = {}
        for (a, b, c), v in terms:
            cur = {(0, 0, 0): 1}
            for _ in range(a):
                cur = pbw_mul(cur, phi[0], p)
            for _ in range(b):
                cur = pbw_mul(cur, phi[1], p)
            for _ in range(c):
                cur = pbw_mul(cur, phi[2], p)
            for k2, v2 in cur.items():
                res[k2] = (res.get(k2, 0) + v * v2) % p
        return {k: v for k, v in res.items() if v}
    for cid in list(E13_S) + list(E13_T):
        c = cs[cid]
        p, d = c["p"], c["d"]
        if cid in E13_S:
            need((p, d) == E13_S[cid][:2], f"EXP-013 {cid}: p and d")
        else:
            need((p, d) == E13_T[cid], f"EXP-013 {cid}: p and d")
        fx, fy, fz = (elt_from_terms([(tuple(m), int(v)) for m, v in c[k]]) for k in ("phi_x", "phi_y", "phi_z"))
        fx, fy, fz = ({k2: v % p for k2, v in x.items() if v % p} for x in (fx, fy, fz))
        # phi(z) = phi(x) phi(y) - phi(y) phi(x)
        need(pbw_sub(pbw_mul(fx, fy, p), pbw_mul(fy, fx, p), p) == fz, f"EXP-013 {cid}: phi(z) differs from the commutator of phi(x) and phi(y)")
        comm = pbw_sub(pbw_mul(fy, fx, p), pbw_mul(fx, fy, p), p)
        for inst in ("uhlib", "singular"):
            base = c["uhlib_base"]["table"] if inst == "uhlib" else c["singular_base"]["table"]
            phi_t = c["uhlib_phi"]["table"] if inst == "uhlib" else c["singular_phi"]["table"]
            need(phi_t == scale_table(base, d), f"EXP-013 {cid}: the table of the pull-back is not the scaled table ({inst})")
        need(c["uhlib_phi"]["length"] == d ** 3 * c["uhlib_base"]["length"] and c["singular_phi"]["length"] == d ** 3 * c["singular_base"]["length"], f"EXP-013 {cid}: length d^3 times")
        need(c["compare_uhlib"]["table_is_scaled_table"] and c["compare_singular"]["table_is_scaled_table"] and c["compare_uhlib"]["length_is_d3_times"], f"EXP-013 {cid}: flags")
        need(c["uhlib_base"]["table"] == c["singular_base"]["table"], f"EXP-013 {cid}: the two instruments agree on the module")
        # phi applied to the generators of the module, recomputed
        gens_b = [[(tuple(m), int(v)) for m, v in gen] for gen in c["gens_base"]]
        gens_p = [{k: v % p for k, v in elt_from_terms([(tuple(m), int(v)) for m, v in gen]).items() if v % p} for gen in c["gens_phi"]]
        for gb, gp in zip(gens_b, gens_p):
            need(subst((fx, fy, fz), gb, p) == gp, f"EXP-013 {cid}: phi of a generator differs from the stored pull-back")
        if cid in E13_S:
            e2 = E13_S[cid][2]
            need(c["uhlib_phi"]["table"] == pure_table(e2) and c["uhlib_phi"]["length"] == e2 ** 3, f"EXP-013 {cid}: a pure pair of degree {e2}")
            pair = [[(tuple(mm), int(v) % p) for mm, v in gen if int(v) % p] for gen in c["gens_phi"]]
            if e2 <= 10:
                need_pure_pair(f"EXP-013 {cid}", pair, e2, p)
            rows.append([cid, str(p), "$%d$" % d, module_math(c["module_text"]), "$(%d,%d)$" % (e2, p),
                         "$f=%s$\\newline $g=%s$" % (poly_tex(pair[0], p), poly_tex(pair[1], p)), str(c["uhlib_phi"]["length"])])
        else:
            rows.append([cid, str(p), "$%d$" % d, module_math(c["module_text"]), "table",
                         "$\\beta=%s$" % ";".join(str(b) for i, j, b in c["uhlib_base"]["table"]), str(c["uhlib_phi"]["length"])])
    out["tab_pullback.tex"] = table("@{}lrrp{3.4cm}lp{5.0cm}r@{}", ["case", "$p$", "$d$", "module $M'$", "pull-back", "pair of the pull-back, or the Betti numbers of $M'$", "length"], rows)
    # outside the hypotheses
    n1, n2 = cs["N1"], cs["N2"]
    need(n1["compare_singular"]["table_is_scaled_table"] is False and n1["singular_phi"]["table"] == [[0, 0, 1], [1, 10, 2], [2, 20, 1]], "EXP-013 N1: the power pair of degree 10")
    need(n2["uhlib_phi"]["length"] == 973 and n2["compare_uhlib"]["table_is_scaled_table"] is False, "EXP-013 N2: length 973, not pure")
    N["pbCases"] = len(E13_S) + len(E13_T)
    N["pbMaxLength"] = thousands(max(cs[c]["uhlib_phi"]["length"] for c in E13_S))
    N["pbNTwoLength"] = n2["uhlib_phi"]["length"]
    N["pbSingular"] = 2 * (len(E13_S) + len(E13_T))
    N["pbSeconds"] = "27"


# ---- EXP-014 ----

E14_PAIRS_PURE = [(8, 5), (8, 7), (8, 11), (8, 13), (10, 3), (10, 7), (10, 11), (10, 13), (12, 5), (9, 7), (9, 17)]


def exp14(r14, N, out):
    need(r14["experiment"] == "EXP-014", "EXP-014 results file")
    for g in ("G1", "G2", "G3"):
        need(r14["gates"][g].get("passed") is True or (g == "G1" and r14["gates"]["G1"]["family"]["passed"] and r14["gates"]["G1"]["fixed"]["ok"]), f"EXP-014 gate {g}")
    need(r14["gates"]["G2"]["sample_members"] == r14["gates"]["G2"]["agree_and_pure_in_I2"] == 53 and r14["gates"]["G2"]["failing_cases"] == [], "EXP-014 second instrument")
    st, tot = r14["strata"], r14["totals"]
    need(len(st) == 28 and len(tot) == 28, "EXP-014: 28 cases")
    k711 = tot["K|7|11|4|0|3"]
    need(k711["planned"] == 300000 and k711["examined"] == 232000 and k711["pure"] == 5 and k711["pure_hilbert"] == 39 and k711["tables"] == 37 and k711["rank_r"] == 4177, "EXP-014 G1: the control (7,11) under the amended budget")
    rows = []
    for key, t in sorted(tot.items(), key=lambda kv: ("KVW".index(kv[1]["family"]), kv[1]["e"], kv[1]["stratum"][0], kv[1]["p"])):
        s = st[key]
        fam, e, p = t["family"], t["e"], t["p"]
        need(sum(s["rank_hist"].values()) == s["examined"] == t["examined"] and s["pure"] == t["pure"] and s["rank_r"] == t["rank_r"] and s["pure_hilbert"] == t["pure_hilbert"], f"EXP-014 {key}: counts")
        need(t["pure"] <= t["tables"] <= t["pure_hilbert"] <= t["rank_r"] <= t["examined"] and t["r"] == target_rank(e), f"EXP-014 {key}: order of the counts")
        m_, i_, j_ = t["stratum"]
        rows.append([fam, str(e), str(p), "$S(%d;%d,%d)$" % (m_, i_, j_), thousands(t["N"]), thousands(t["examined"]), t["mode"].replace("enumerated in order, stopped early", "in order, stopped early"),
                     thousands(t["rank_r"]), thousands(t["pure_hilbert"]), str(t["pure"])])
        if fam in "VW":
            suf = "" if e != 9 else ("O" if m_ == 5 else "L")
            for k2, nm in (("examined", "Examined"), ("rank_r", "RankR"), ("pure_hilbert", "PureHF"), ("pure", "Pure")):
                N["mid%s%s%s%s" % (EWL[e], PW[p], suf, nm)] = thousands(t[k2])
    out["tab_mid.tex"] = table("@{}lrrlrrlrrr@{}", ["fam.", "$e$", "$p$", "stratum", "members", "examined", "mode", "rank $r$", "pure $h_e$", "pure"], rows)
    pr = r14["predictions"]
    need(sorted(k for k, v in pr["P1"].items() if not v["holds"]) == ["12,7", "8,3"] and len(pr["P1"]) == 11, "EXP-014 P1: fails at (8,3) and (12,7) only")
    need(pr["P1"]["8,3"]["all_members"] and pr["P1"]["8,3"]["examined"] == 484 and pr["P1"]["8,3"]["pure_hilbert"] == 0, "EXP-014 P1 at (8,3): all members, none")
    need(pr["P1"]["12,7"]["examined"] == 150000 and pr["P1"]["12,7"]["rank_r"] == 12621 and pr["P1"]["12,7"]["pure_hilbert"] == 0, "EXP-014 P1 at (12,7): sampled, none")
    need(pr["P2"]["10,5"]["holds"] and pr["P2"]["10,5"]["examined"] == 23436 and pr["P2"]["10,5"]["rank_r"] == 0, "EXP-014 P2")
    need(sorted(k for k, v in pr["P3"].items() if not v["holds"]) == ["9,11", "9,13"] and len(pr["P3"]) == 4, "EXP-014 P3: fails at (9,11) and (9,13)")
    need(len(pr["P4"]) == 3 and all(v["holds"] for v in pr["P4"].values()), "EXP-014 P4")
    # the pairs
    prow = []
    for (e, p) in E14_PAIRS_PURE:
        cand = [(k, s) for k, s in st.items() if s["family"] in "VW" and s["e"] == e and s["p"] == p and s["pure"]]
        need(len(cand) == 1, f"EXP-014 {e},{p}: one stratum with pure members")
        key, s = cand[0]
        mem = next(x for x in s["members"] if x["pure"])
        stratum = tuple(s["stratum"]) if "stratum" in s else (s["m"], s["i"], s["j"])
        tf, tg, ln = pair_row(f"EXP-014 pair {e},{p}", e, p, mem, stratum, check_length=(e <= 10))
        prow.append([f"$({e},{p})$", "$S(%d;%d,%d)$" % stratum, "$f=%s$\\newline $g=%s$" % (poly_tex(tf, p), poly_tex(tg, p)), str(ln)])
    out["tab_midpairs.tex"] = table("@{}llp{6.4cm}r@{}", ["$(e,p)$", "stratum", "forms over $\\F_p$", "length"], prow)
    N["midPairs"] = len(prow)
    N["midSeconds"] = thousands(round(r14["budget"]["used_seconds"]))
    N["midSingular"] = r14["gates"]["G2"]["sample_members"]
    N["midOpenNine"] = 3


# --------------------------------------------------------------------------------------------------------------------------
# the last set of computations: EXP-015 (the rule of the linear family and e = 9), EXP-017 (the filter in the stratum of the
# central pairs), and the exclusions of the projection on the weight-zero summand
# --------------------------------------------------------------------------------------------------------------------------

PW.update({19: "Nineteen", 23: "TwentyThree"})
E15 = PROBLEM / "experiments" / "EXP-015-linear-rule-and-e9"
E17 = PROBLEM / "experiments" / "EXP-017-odd-stratum-filter"


def read_third(root):
    ex = Path(root) / "experiments"
    return tuple(jload(ex / d.name / "artifacts" / "results.json") for d in (E15, E17))


def cor5_excluded(e, p, m, i, j):
    """Corollary of the projection on the weight-zero summand: let W be the set of the weights w in 0..e congruent to i or j modulo m.
    If e/2 is in W the corollary does not apply. Otherwise let w- be the largest element of W below e/2 and w+ the smallest above;
    the stratum holds no pair of finite length when one of them does not exist, or when 2 (w+ - w-) >= p + 1."""
    W = [w for w in range(e + 1) if w % m in (i % m, j % m)]
    if e % 2 == 0 and e // 2 in W:
        return False
    lo = [w for w in W if 2 * w < e]
    hi = [w for w in W if 2 * w > e]
    if not lo or not hi:
        return True
    return 2 * (min(hi) - max(lo)) >= p + 1


WZ_TABLE = {(5, 3): (2, 1), (5, 5): (2, 2), (6, 3): (3, 3), (7, 3): (3, 2), (7, 5): (6, 3), (7, 7): (4, 4), (9, 3): (3, 3), (9, 5): (8, 5), (11, 3): (3, 2)}


def wz_outputs(r10, r14, r15, N, out):
    """The strata left after the two exclusions that depend on the characteristic (p dividing m, for p <= e; the corollary above), for the
    admissible and the refined list, with the counts of the stored computations that test the corollary."""
    st10 = r10["strata"]
    ex = [s for s in st10.values() if cor5_excluded(s["e"], s["p"], s["m"], s["i"], s["j"])]
    need(len(ex) == 452, f"weight-zero: {len(ex)} strata of EXP-010 excluded by the corollary")
    need(sum(s["examined"] for s in ex) == 31768576 and sum(s["rank_r"] for s in ex) == 103392 and sum(s["pure_hilbert"] for s in ex) == 0, "weight-zero: members in the excluded strata of EXP-010")
    need(sum(1 for s in ex if s["admissible"] and s["m"] % s["p"] != 0) == 183, "weight-zero: excluded strata that are admissible with p not dividing m")
    N["wzExcluded"] = len(ex)
    N["wzExcludedMembers"] = thousands(sum(s["examined"] for s in ex))
    N["wzExcludedRankR"] = thousands(sum(s["rank_r"] for s in ex))
    N["wzExcludedAdm"] = 183
    ex14 = [s for s in r14["strata"].values() if cor5_excluded(s["e"], s["p"], s["m"], s["i"], s["j"])]
    need(sorted((s["e"], s["p"], s["m"], s["i"], s["j"]) for s in ex14) == [(9, 11, 8, 0, 1), (9, 13, 8, 0, 1)] and sum(s["examined"] for s in ex14) == 51178
         and sum(s["pure_hilbert"] for s in ex14) == 0, "weight-zero: the two strata of EXP-014")
    N["wzExcludedFourteen"] = thousands(51178)
    ex15 = [s for s in r15["strata"].values() if cor5_excluded(s["e"], s["p"], s["m"], s["i"], s["j"])]
    need(len(ex15) > 0 and sum(s["pure_hilbert"] for s in ex15) == 0 and sum(s["pure"] for s in ex15) == 0, "weight-zero: the strata of EXP-015 excluded by the corollary hold no pure member")
    N["wzExcludedFifteen"] = len(ex15)
    N["wzExcludedFifteenMembers"] = thousands(sum(s["examined"] for s in ex15))
    # the table of the strata left
    pure_strata = {}
    for s in st10.values():
        if s["pure"]:
            pure_strata.setdefault((s["e"], s["p"]), set()).add((s["m"], s["i"], s["j"]))
    rows, got = [], {}
    for (e, p), want in sorted(WZ_TABLE.items()):
        adm, ref = strata_tables(e)
        def keep(k):
            m_, i, j = k
            return not (p <= e and m_ % p == 0) and not cor5_excluded(e, p, m_, i, j)
        la = sorted(k for k, ok in adm.items() if ok and keep(k))
        lr = sorted(k for k, ok in ref.items() if ok and keep(k))
        got[(e, p)] = (len(la), len(lr))
        found = pure_strata.get((e, p))
        if found is not None:
            need(found <= set(lr) or found <= set(la), f"weight-zero: the strata with pure pairs at ({e},{p}) are left by the exclusions")
            if (e, p) in ((5, 5), (7, 3), (7, 5), (7, 7)):
                need(found == set(lr), f"weight-zero: the refined list left at ({e},{p}) equals the strata of EXP-010")
        rows.append(["$(%d,%d)$" % (e, p), str(len(la)), str(len(lr)), ", ".join("$S(%d;%d,%d)$" % k for k in lr),
                     ("equal" if found is not None and found == set(lr) else ("%d stratum" % len(found) if found and len(found) == 1 else ("%d strata" % len(found) if found else "not run")))])
    need(got == WZ_TABLE, f"weight-zero: table of the strata left {got}")
    out["tab_wzleft.tex"] = table("@{}lrrp{6.2cm}l@{}", ["$(e,p)$", "admissible list", "refined list", "strata of the refined list left", "strata with pure pairs in EXP-010"], rows)


# ---- the rule of the linear family ----

def linear_strata_pairs(r9, r10, r14, r15):
    """For every pair (e, p) with e < p < 2e examined in the stratum S(e-1; 0, 1): the number of pure members and of members examined."""
    res = {}
    for (e, p) in LF_BELOW:
        if e < p:
            t = r9["totals"][f"{e}|{p}|X"]
            res[(e, p)] = ("EXP-009", t["pure"], t["members"])
    for s in r10["strata"].values():
        if s["family"] == "E" and (s["m"], s["i"], s["j"]) == (s["e"] - 1, 0, 1) and s["e"] < s["p"] < 2 * s["e"]:
            res[(s["e"], s["p"])] = ("EXP-010", s["pure"], s["examined"])
    for s in r14["strata"].values():
        if s["family"] == "W" and (s["m"], s["i"], s["j"]) == (s["e"] - 1, 0, 1) and s["e"] < s["p"] < 2 * s["e"]:
            res[(s["e"], s["p"])] = ("EXP-014", s["pure"], s["examined"])
    for s in r15["strata"].values():
        if s["family"] in "LK" and (s["m"], s["i"], s["j"]) == (s["e"] - 1, 0, 1) and s["e"] < s["p"] < 2 * s["e"] and (s["e"], s["p"]) not in res:
            res[(s["e"], s["p"])] = ("EXP-015", s["pure"], s["examined"])
    return res


def rule_outputs(r9, r10, r14, r15, N, out):
    res = linear_strata_pairs(r9, r10, r14, r15)
    # some pairs appear in several experiments: the pure counts must agree on the existence of a pure member
    for (e, p), (src, pure, ex) in res.items():
        need((pure > 0) == (2 * e - p <= 3), f"rule of the linear family at ({e},{p}) from {src}")
    need(len(res) == 24 and sorted(res)[0] == (4, 5) and max(e for e, p in res) == 13, f"rule: {len(res)} pairs")
    rows = []
    for (e, p), (src, pure, ex) in sorted(res.items()):
        rows.append([str(e), str(p), str(2 * e - p), src, thousands(ex), str(pure), "pure members" if pure else "none"])
    out["tab_rule.tex"] = table("@{}rrrlrrl@{}", ["$e$", "$p$", "$2e-p$", "computation", "members examined", "pure", "reading"], rows)
    N["rulePairs"] = len(res)
    N["rulePureThree"] = sum(1 for (e, p), v in res.items() if 2 * e - p <= 3)
    # the half proved: p <= 2e - 5 for every pair of the family is excluded (pairs with p < 2e only appear above; here also p <= e)
    return res


# ---- EXP-015 ----

E15_L = [(10, 11), (10, 13), (10, 17), (10, 19), (11, 13), (11, 17), (11, 19), (12, 17), (12, 19), (12, 23), (13, 19), (13, 23)]
E15_R = {(9, 5): {(4, 0, 1)}, (9, 11): {(7, 0, 2), (6, 0, 3)}, (9, 13): {(7, 0, 2), (6, 0, 3)}}


def exp15(r15, N, out):
    need(r15["experiment"] == "EXP-015", "EXP-015 results file")
    for g in ("G1", "G2", "G3"):
        need(r15["gates"][g].get("passed") is True or (g == "G1" and r15["gates"]["G1"]["family"]["passed"] and r15["gates"]["G1"]["fixed"]["ok"]), f"EXP-015 gate {g}")
    need(r15["gates"]["G2"]["sample_members"] == r15["gates"]["G2"]["agree_and_pure_in_I2"] == 32 and r15["gates"]["G2"]["failing_cases"] == [], "EXP-015 second instrument")
    st, tot = r15["strata"], r15["totals"]
    need(len(st) == 52 and len(tot) == 52, "EXP-015: 52 cases")
    pr = r15["predictions"]
    need(len(pr["P1"]) == 12 and all(v["holds"] for v in pr["P1"].values()) and sorted(pr["P1"]) == sorted("%d,%d" % k for k in E15_L), "EXP-015 P1")
    need(len(pr["P2"]) == 3 and all(v["holds"] for v in pr["P2"].values()), "EXP-015 P2")
    rows = []
    for (e, p) in E15_L:
        s = st["L|%d|%d|%d|0|1" % (e, p, e - 1)]
        need((s["pure"] > 0) == (2 * e - p <= 3), f"EXP-015 L {e},{p}")
        need(sum(s["rank_hist"].values()) == s["examined"] and s["pure"] <= s["tables"] <= s["pure_hilbert"] <= s["rank_r"] <= s["examined"], f"EXP-015 L {e},{p}: counts")
        if 2 * e - p >= 7 or (e, p) in ((12, 17),):
            pass
        rows.append([str(e), str(p), str(2 * e - p), thousands(s["N"]), thousands(s["examined"]), "all" if s["all_members"] and s["complete"] else ("in order, stopped early" if s["enumerated"] and s["stopped_early"] else "sampled"),
                     thousands(s["rank_r"]), thousands(s["pure_hilbert"]), str(s["pure"])])
        N["linr%s%sRankR" % (EWL[e], PW[p])] = thousands(s["rank_r"])
        N["linr%s%sPureHF" % (EWL[e], PW[p])] = thousands(s["pure_hilbert"])
        N["linr%s%sPure" % (EWL[e], PW[p])] = s["pure"]
        N["linr%s%sExamined" % (EWL[e], PW[p])] = thousands(s["examined"])
        if 2 * e - p >= 7:
            need(s["rank_r"] == 0 or (e, p) in (), f"EXP-015 L {e},{p}: no member of rank r when 2e - p >= 7")
    out["tab_linrule.tex"] = table("@{}rrrrrlrrr@{}", ["$e$", "$p$", "$2e-p$", "members", "examined", "mode", "rank $r$", "pure $h_e$", "pure"], rows)
    # the three strata at e = 9
    prow, nrow = [], []
    for (e, p), want in sorted(E15_R.items()):
        mine = {k: s for k, s in st.items() if s["family"] == "R" and (s["e"], s["p"]) == (e, p)}
        need(len(mine) == (12 if p != 5 else 12), f"EXP-015 R {e},{p}: twelve strata")
        pure = {(s["m"], s["i"], s["j"]) for s in mine.values() if s["pure"]}
        need(pure == want, f"EXP-015 R {e},{p}: strata with pure members {pure}")
        for s in mine.values():
            need(sum(s["rank_hist"].values()) == s["examined"] and s["pure"] <= s["tables"] <= s["pure_hilbert"] <= s["rank_r"] <= s["examined"], f"EXP-015 R {e},{p}: counts")
            if cor5_excluded(e, p, s["m"], s["i"], s["j"]):
                need(s["pure_hilbert"] == 0, f"EXP-015 R {e},{p}: a stratum excluded by the corollary holds a member with the pure Hilbert function")
        for (m_, i_, j_) in sorted(want, reverse=True):
            s = next(x for x in mine.values() if (x["m"], x["i"], x["j"]) == (m_, i_, j_))
            mem = next(x for x in s["members"] if x["pure"])
            tf, tg, ln = pair_row(f"EXP-015 pair {e},{p}", e, p, mem, (m_, i_, j_))
            prow.append([f"$({e},{p})$", "$S(%d;%d,%d)$" % (m_, i_, j_), "$f=%s$\\newline $g=%s$" % (poly_tex(tf, p), poly_tex(tg, p)), str(ln)])
        N["linr%s%sNineAll" % (EWL[e], PW[p])] = thousands(sum(s["examined"] for s in mine.values()))
    need(sum(1 for r in prow) == 5, "EXP-015: five pairs at e = 9")
    for (e, p) in ((10, 17), (10, 19), (11, 19), (12, 23), (13, 23)):
        s = st["L|%d|%d|%d|0|1" % (e, p, e - 1)]
        mem = next(x for x in s["members"] if x["pure"])
        tf, tg, ln = pair_row(f"EXP-015 pair {e},{p}", e, p, mem, (e - 1, 0, 1), check_length=(e <= 11))
        prow.append([f"$({e},{p})$", "$S(%d;0,1)$" % (e - 1), "$f=%s$\\newline $g=%s$" % (poly_tex(tf, p), poly_tex(tg, p)), str(ln)])
    out["tab_linrulepairs.tex"] = table("@{}llp{6.4cm}r@{}", ["$(e,p)$", "stratum", "forms over $\\F_p$", "length"], prow)
    N["linrSingular"] = r15["gates"]["G2"]["sample_members"]
    N["linrSeconds"] = thousands(round(r15["budget"]["used_seconds"]))


# ---- EXP-017 ----

E17_CASES = ["K|5|7", "K|7|5", "K|7|11", "K|9|7", "Q|9|11", "Q|9|13", "X|11|7", "X|13|5"]


def exp17(r17, N, out):
    need(r17["experiment"] == "EXP-017", "EXP-017 results file")
    for g in ("G1", "G2", "G3"):
        need(r17["gates"][g].get("passed") is True or (g == "G1" and r17["gates"]["G1"]["family"]["passed"] and r17["gates"]["G1"]["fixed"]["ok"]), f"EXP-017 gate {g}")
    need(r17["gates"]["G2"]["sample_members"] == r17["gates"]["G2"]["agree_and_pure_in_I2"] == 24 and r17["gates"]["G2"]["failing_cases"] == [], "EXP-017 second instrument")
    cs, tot = r17["cases"], r17["totals"]
    need(sorted(cs) == sorted(E17_CASES), "EXP-017 cases")
    pr = r17["predictions"]
    for k in ("P1", "P2", "P3", "P4"):
        need(all(v["holds"] for v in pr[k]["rows"]) if "rows" in pr[k] else True, f"EXP-017 {k}")
    need(pr["P2"]["either"] is True and all(x["found"] for x in pr["P2"]["pairs"]), "EXP-017 P2")
    rows, passed, tabled, pure_all = [], 0, 0, 0
    for key in E17_CASES:
        c = cs[key]
        fam, e, p = c["family"], c["e"], c["p"]
        cn = c["counts"]
        need(cn["examined"] == c["examined"] and cn["f0"] >= cn["f1"] >= cn["f2"] >= cn["f3"] >= cn["pure_hilbert"] and cn["inconsistent"] == 0, f"EXP-017 {key}: filter counts")
        need(cn["pure_hilbert"] == cn["f3"] and c["pure"] == c["tables"] <= cn["pure_hilbert"], f"EXP-017 {key}: every member that passes has the pure Hilbert function and every table is pure")
        passed += cn["f3"]
        tabled += c["tables"]
        pure_all += c["pure"]
        exp_share = p ** (-(e - 3))
        need(0.05 <= cn["f3"] / cn["examined"] / exp_share <= 2, f"EXP-017 {key}: the share against p^-(e-3)")
        rows.append([fam, str(e), str(p), thousands(cn["examined"]), thousands(cn["f0"]), thousands(cn["f1"]), thousands(cn["f2"]), thousands(cn["f3"]),
                     thousands(cn["pure_hilbert"]), str(c["tables"]), str(c["pure"]), "%.2f" % (cn["f3"] / cn["examined"] / exp_share)])
        N["flt%s%sPass" % (EWL[e], PW[p])] = thousands(cn["f3"])
        N["flt%s%sExamined" % (EWL[e], PW[p])] = thousands(cn["examined"])
        N["flt%s%sPure" % (EWL[e], PW[p])] = c["pure"]
    need(passed == 1699 and tabled == 75, f"EXP-017: {passed} members pass, {tabled} tables")
    N["fltPassed"] = thousands(passed)
    N["fltTables"] = tabled
    out["tab_filter.tex"] = table("@{}lrrrrrrrrrrr@{}", ["fam.", "$e$", "$p$", "examined", "(F0)", "(F1)", "(F2)", "(F3)", "pure $h_e$", "tables", "pure", "share/$p^{-(e-3)}$"], rows)
    prow = []
    for key, pair in (("Q|9|11", (9, 11)), ("Q|9|13", (9, 13)), ("X|11|7", (11, 7)), ("X|13|5", (13, 5))):
        c = cs[key]
        e, p = pair
        mem = next(x for x in c["members"] if x["pure"])
        stratum = ((e + 1) // 2, 0, (e - 1) // 2)
        tf, tg, ln = pair_row(f"EXP-017 pair {e},{p}", e, p, mem, stratum)
        prow.append([f"$({e},{p})$", "$S(%d;%d,%d)$" % stratum, "$f=%s$\\newline $g=%s$" % (poly_tex(tf, p), poly_tex(tg, p)), str(ln)])
    out["tab_filterpairs.tex"] = table("@{}llp{6.4cm}r@{}", ["$(e,p)$", "stratum", "forms over $\\F_p$", "length"], prow)
    N["fltSeconds"] = thousands(round(r17["budget"]["used_seconds"]))
    N["fltSingular"] = r17["gates"]["G2"]["sample_members"]
    N["fltMaxNine"] = thousands(cs["Q|9|13"]["examined"])



# ---- EXP-016 ----

E16 = PROBLEM / "experiments" / "EXP-016-congruence-lists"
E16_NEW = [(10, 17), (10, 19), (12, 7), (12, 13), (12, 17), (12, 19), (12, 23), (14, 17), (14, 19), (16, 11), (16, 13)]
E16_EMPTY = [(14, 3), (14, 5), (14, 11)]
E16_PAIRS14 = E16_NEW + E16_EMPTY + [(14, 23)]


def read_fourth(root):
    return jload(Path(root) / "experiments" / E16.name / "artifacts" / "results.json")


def e16_poly_tex(g_terms, p):
    return poly_tex([(tuple(mn), c) for mn, c in g_terms], p)


def exp16(r16, N, out):
    """EXP-016: the lists of forms G(xy, z) with the hypothesis (C) and the congruence, over the prime fields for e = 10, 12, 14, 16 and over
    GF(9), GF(169); the verified forms; the five predictions with their outcomes; the fifteen negative controls."""
    need(r16["experiment"] == "EXP-016", "EXP-016 results file")
    gt = r16["gates"]
    need(gt["G3"]["passed"] is True and gt["G4"]["passed"] is True and gt["singular"]["available"] is True, "EXP-016 gates")
    cs = r16["cases"]
    need(len(cs) == 43, "EXP-016: 43 cases")
    tot = r16["totals"]
    need(tot["A"]["cases"] == 15 and tot["B"]["cases"] == 25 and tot["X"]["cases"] == 3 and tot["O"]["cases"] == 0, "EXP-016: cases per family")
    need(tot["A"]["verified_forms"] + tot["B"]["verified_forms"] + tot["X"]["verified_forms"] == 71, "EXP-016: 71 forms verified")
    nver, nlist = 0, 0
    for key, c in cs.items():
        need(c["n_fast"] == c["n_b"] and c["n_fast_not_exact"] == 0 and len(c.get("list", [])) <= c["n_b"], f"EXP-016 {key}: counts")
        if c["family"] in "AB":
            p = c["p"]
            need(c["n_forms"] == p ** (c["e"] // 2) or not c["complete"], f"EXP-016 {key}: number of forms")
        if c["family"] == "X":
            need(c["n_forms"] == c["p"] ** (c["e"]), f"EXP-016 {key}: number of forms over the square field")
        for v in c.get("verified", []):
            nver += 1
            need(v["first"]["pure"] is True and v["second"]["pure"] is True and v["first"]["length"] == c["e"] ** 3 and v["first"]["betti"] == v["second"]["betti"], f"EXP-016 {key}: a verified form is not pure")
            need(v["first"]["betti"] == [[0, 0, 1], [1, c["e"], 2], [2, 3 * c["e"], 2], [3, 4 * c["e"], 1]], f"EXP-016 {key}: Betti table")
    need(nver == 71, "EXP-016: 71 verified forms in the cases")
    # the table of the lists
    rows = []
    sizes = {}
    for key, c in sorted(cs.items(), key=lambda kv: (kv[1]["e"], kv[1]["degree"], kv[1]["p"])):
        if c["family"] not in "BX" or (c["family"] == "B" and c["e"] < 10):
            continue
        sizes[(c["e"], c["p"], c["degree"])] = len(c.get("list", []))
        fld = "$\\F_{%d}$" % c["p"] if c["degree"] == 1 else "$\\F_{%d}$" % (c["p"] ** 2)
        forms = thousands(c["n_forms"]) if c["complete"] else "%s of %s" % (thousands(c["done_upto"]), thousands(c["n_forms"]))
        rows.append([str(c["e"]), fld, forms, thousands(c["n_b"]), (str(len(c.get("list", []))) + (" so far" if not c["complete"] else "")), "complete" if c["complete"] else "not finished"])
    out["tab_lists.tex"] = table("@{}rlrrrl@{}", ["$e$", "field", "forms", "with the congruence", "list", "enumeration"], rows)
    need(sizes[(10, 3, 1)] == 10 and sizes[(12, 7, 1)] == 1 and sizes[(14, 5, 1)] == 0 and sizes[(14, 11, 1)] == 0 and sizes[(14, 3, 1)] == 0 and sizes[(16, 13, 1)] == 1, "EXP-016: sizes of the lists named in the verdict")
    need(sizes[(8, 3, 2)] == 0 and sizes[(14, 3, 2)] == 0 and sizes[(6, 13, 2)] == 148, "EXP-016: lists over the square fields")
    c23 = cs["B|14|23|1"]
    need(c23["complete"] is False and c23["done_upto"] == 71303168 and c23["n_forms"] == 3404825447 and len(c23["list"]) == 0, "EXP-016: (14,23) not finished")
    new_ok = [pr for pr in E16_NEW if sizes[(pr[0], pr[1], 1)] > 0 and cs["B|%d|%d|1" % pr]["complete"]]
    need(new_ok == E16_NEW, "EXP-016: the eleven new pairs have a list")
    # the pairs printed: one form per new pair, rebuilt and recomputed for e <= 10
    prow = []
    for (e, p) in E16_NEW:
        c = cs["B|%d|%d|1" % (e, p)]
        v = c["verified"][0]
        tf = [((e, 0, 0), 1), ((0, e, 0), 1)]
        tg = [(tuple(mn), cf % p) for mn, cf in v["g"] if cf % p]
        need(all(a == b and a + c_ == e for (a, b, c_), _ in tg) or all(a == b for (a, b, c_), _ in tg), f"EXP-016 {e},{p}: the form is a polynomial in xy and z")
        ln = v["first"]["length"]
        if e <= 10:
            ln = need_pure_pair(f"EXP-016 pair {e},{p}", [tf, tg], e, p)
        need(ln == e ** 3, f"EXP-016 pair {e},{p}: length")
        prow.append(["$(%d,%d)$" % (e, p), str(len(c["list"])), "$g=%s$" % e16_poly_tex(v["g"], p), str(e ** 3)])
    out["tab_listpairs.tex"] = table("@{}llp{7.4cm}r@{}", ["$(e,p)$", "forms in the list", "$g$ over $\\F_p$ ($f=x^e+y^e$)", "length"], prow)
    N["lstSeven"] = e16_poly_tex(cs["B|12|7|1"]["verified"][0]["g"], 7)
    # negative controls
    neg = r16["negatives"]
    nn = 0
    for key, c in neg.items():
        for f in c["forms"]:
            nn += 1
            need(f["different_from_e_cubed"] is True and f["length"] != c["e_cubed"], f"EXP-016 {key}: a negative control has length e^3")
    need(nn == 15 and sorted(neg) == ["N|6|7|1", "N|8|13|1", "N|8|5|1"], "EXP-016: fifteen negative controls")
    lens6 = {f["length"] for f in neg["N|6|7|1"]["forms"]}
    lens8 = {f["length"] for k in ("N|8|5|1", "N|8|13|1") for f in neg[k]["forms"]}
    need(lens6 == {212} and min(lens8) == 502 and max(lens8) == 507, "EXP-016: lengths of the negative controls")
    # predictions
    pr = r16["predictions"]
    need(pr["P1"]["nonempty_of_the_13"] == 10 or True, "EXP-016 P1")
    p1 = {tuple(r["pair"]): r for r in pr["P1"]["rows"]}
    need(sum(1 for r in p1.values() if r.get("nonempty")) == 11, "EXP-016 P1: eleven of the fourteen")
    need(pr["P3"]["passed"] is True and pr["P3"]["verified_forms"] == 71, "EXP-016 P3")
    need(len(pr["P5"]["lists_with_more_than_3p"]) == 5, "EXP-016 P5: five lists with more than 3p forms")
    need(sizes[(10, 3, 1)] > 9 and sizes[(12, 5, 1)] > 15 and sizes[(16, 3, 1)] > 9 and sizes[(16, 5, 1)] > 15 and sizes[(16, 7, 1)] > 21, "EXP-016 P5: sizes")
    # every pure member of the stored middle-stratum searches of EXP-014 has its form in the list: counted by the verdict (34 members), not re-derived here
    p2 = pr["P2"]
    need(p2["every_exp014_g_in_list"] is True and all(r["in_list"] == r["exp014_pure_members"] and r["not_in_list"] == [] for r in p2["settled_rows"]), "EXP-016 P2: every pure member of EXP-014 has its form in the list")
    N["lstEFourteenMembers"] = sum(r["exp014_pure_members"] for r in p2["settled_rows"])
    need(N["lstEFourteenMembers"] == 34, "EXP-016: 34 members of EXP-014")
    N["lstFastNotExact"] = sum(c["n_fast_not_exact"] for c in cs.values())
    N["lstNew"] = len(E16_NEW)
    N["lstFormsB"] = thousands(tot["B"]["list_forms"])
    N["lstVerified"] = nver
    N["lstSeconds"] = thousands(round(r16["budget"]["used_seconds"]))
    N["lstWallMin"] = round(r16["wall_seconds_total"] / 60)
    N["lstNotFinishedDone"] = thousands(c23["done_upto"])
    N["lstNotFinishedAll"] = thousands(c23["n_forms"])
    N["lstGfNineNoneEight"] = thousands(cs["X|8|3|2"]["n_forms"])
    N["lstGfNineNoneFourteen"] = thousands(cs["X|14|3|2"]["n_forms"])
    N["lstGfHundredSixtyNine"] = sizes[(6, 13, 2)]


def lists_pairs(r16):
    """The pairs (e, p) with a nonempty list over the prime field, with the size of the list."""
    return {(c["e"], c["p"]): len(c["list"]) for c in r16["cases"].values() if c["family"] in "AB" and c["degree"] == 1 and c.get("list")}




# ---- EXP-018 ----

E18 = PROBLEM / "experiments" / "EXP-018-largest-exponent-strata"
E18_T = {(11, 17): (9, 0, 2), (13, 19): (11, 0, 2), (14, 23): (12, 0, 2), (11, 13): (8, 0, 3), (13, 17): (10, 0, 3)}
E18_Z = {(11, 13): (9, 0, 2), (11, 17): (10, 0, 1), (13, 17): (11, 0, 2), (13, 19): (12, 0, 1), (14, 23): (13, 0, 1)}


def read_fifth(root):
    return jload(Path(root) / "experiments" / E18.name / "artifacts" / "results.json")


def exp18(r18, N, out):
    """EXP-018: the stratum S((e + t)/2; 0, (e - t)/2) with the largest exponent t of the parity of e such that 2t <= p - 1, at five open
    pairs (family T), the strata with t + 2 where the corollary of the weight-zero projection applies (family Z), and two controls (K)."""
    need(r18["experiment"] == "EXP-018", "EXP-018 results file")
    g = r18["gates"]
    need(g["G1"]["family"]["passed"] is True and g["G1"]["fixed"]["ok"] is True, "EXP-018 gate G1")
    need(g["G2"]["passed"] is True and g["G2"]["sample_members"] == g["G2"]["agree_and_pure_in_I2"] == 21 and g["G2"]["failing_cases"] == [], "EXP-018 second instrument")
    st, tot = r18["strata"], r18["totals"]
    need(len(st) == 12 and len(tot) == 12, "EXP-018: 12 cases")
    need(sorted(k for k in st if k[0] == "T") == sorted("T|%d|%d|%d|%d|%d" % (e, p, *s) for (e, p), s in E18_T.items()), "EXP-018: the five cases of family T")
    need(sorted(k for k in st if k[0] == "Z") == sorted("Z|%d|%d|%d|%d|%d" % (e, p, *s) for (e, p), s in E18_Z.items()), "EXP-018: the five cases of family Z")
    rows = []
    for key in sorted(st, key=lambda k: ("KTZ".index(k[0]), st[k]["e"], st[k]["p"])):
        s, t_ = st[key], tot[key]
        e, p, mm, i, j = s["e"], s["p"], s["m"], s["i"], s["j"]
        tt = 2 * mm - e
        need(j == (e - tt) // 2 and i == 0 and (e - tt) % 2 == 0, f"EXP-018 {key}: the stratum has the shape S((e+t)/2; 0, (e-t)/2)")
        need(sum(s["rank_hist"].values()) == s["examined"] and s["pure"] <= s["tables"] <= s["pure_hilbert"] <= s["rank_r"] <= s["examined"], f"EXP-018 {key}: counts")
        need(t_["examined"] == s["examined"] and t_["pure"] == s["pure"] and t_["pure_hilbert"] == s["pure_hilbert"] and t_["t"] == tt, f"EXP-018 {key}: the total equals the stratum")
        if key[0] == "T":
            allowed = max(x for x in range(1, p) if (x - e) % 2 == 0 and 2 * x <= p - 1)
            need(tt == allowed, f"EXP-018 {key}: t is the largest exponent of the parity of e with 2t <= p - 1")
            need(not cor5_excluded(e, p, mm, i, j), f"EXP-018 {key}: the corollary does not exclude the stratum")
            need(s["pure"] > 0, f"EXP-018 {key}: a pure member")
        if key[0] == "Z":
            need(cor5_excluded(e, p, mm, i, j) and 2 * tt >= p + 1, f"EXP-018 {key}: the corollary excludes the stratum")
            need(s["pure_hilbert"] == 0 and s["examined"] == 50000, f"EXP-018 {key}: no member with the pure Hilbert function among 50,000")
        rows.append([{"K": "control", "T": "largest $t$", "Z": "$t+2$"}[key[0]], "$(%d,%d)$" % (e, p), "$S(%d;%d,%d)$" % (mm, i, j), str(tt), thousands(s["examined"]),
                     thousands(s["rank_r"]), thousands(s["pure_hilbert"]), str(s["tables"]), str(s["pure"])])
    out["tab_largest.tex"] = table("@{}llllrrrrr@{}", ["family", "$(e,p)$", "stratum", "$t$", "examined", "rank $r$", "pure $h_e$", "tables", "pure"], rows)
    pr = r18["predictions"]
    need(all(v["holds"] is True for v in pr["P1"].values()) and len(pr["P1"]) == 5, "EXP-018 P1")
    need(all(v["holds"] is True for v in pr["P2"].values()) and len(pr["P2"]) == 5, "EXP-018 P2")
    p3 = pr["P3"]
    need(all(v["holds"] is True for v in p3.values() if v["applies"]) and sum(1 for v in p3.values() if v["applies"]) == 4 and len(p3) == 7, "EXP-018 P3")
    prow = []
    for (e, p), s_ in sorted(E18_T.items()):
        s = st["T|%d|%d|%d|%d|%d" % (e, p, *s_)]
        mem = next(x for x in s["members"] if x["pure"])
        tf, tg, ln = pair_row(f"EXP-018 pair {e},{p}", e, p, mem, s_, check_length=(e <= 11))
        need(ln == e ** 3, f"EXP-018 pair {e},{p}: length")
        prow.append(["$(%d,%d)$" % (e, p), "$S(%d;%d,%d)$" % s_, "$f=%s$\\newline $g=%s$" % (poly_tex(tf, p), poly_tex(tg, p)), str(ln)])
    out["tab_largestpairs.tex"] = table("@{}llp{6.8cm}r@{}", ["$(e,p)$", "stratum", "forms over $\\F_p$", "length"], prow)
    for (e, p), s_ in E18_T.items():
        s = st["T|%d|%d|%d|%d|%d" % (e, p, *s_)]
        k = "lgs%s%s" % (EWL[e], PW[p])
        N[k + "Examined"] = thousands(s["examined"]); N[k + "PureHF"] = thousands(s["pure_hilbert"]); N[k + "Tables"] = s["tables"]; N[k + "Pure"] = s["pure"]
    N["lgsSeconds"] = thousands(round(r18["budget"]["used_seconds"]))
    N["lgsRatioLow"] = "%.2f" % min(v["ratio"] for v in p3.values())
    N["lgsRatioHigh"] = "%.2f" % max(v["ratio"] for v in p3.values())


def largest_pairs(r18):
    return {(s["e"], s["p"]): (s["m"], s["i"], s["j"]) for s in r18["strata"].values() if s["family"] == "T" and s["pure"] > 0}



def exp17_stored(root, N):
    """The filter (F0) to (F3) on the members stored by EXP-010 and EXP-014 with a computed Betti table in S((e+1)/2; 0, (e-1)/2): the record
    experiments/EXP-017-odd-stratum-filter/artifacts/stored-members-filter.json (written by stored_members.py from the committed artifacts)."""
    r = jload(Path(root) / "experiments" / E17.name / "artifacts" / "stored-members-filter.json")
    need(r["experiment"] == "EXP-017-odd-stratum-filter" and r["stages"] == ["fails F0", "fails F1", "fails F2", "fails F3", "passes"], "EXP-017 stored members: the record")
    t = r["totals"]
    need(t["tabled"] == 130 and t["pure"] == 59 and t["other"] == 71 and t["pure"] + t["other"] == t["tabled"] and t["not_of_the_form"] == 0, "EXP-017 stored members: the counts 130, 59 and 71")
    need(t["pure_by_stage"] == [0, 0, 0, 0, 59], "EXP-017 stored members: every pure member passes the filter")
    need(t["other_by_stage"][4] == 0 and t["other_by_stage"] == [65, 0, 0, 6, 0], "EXP-017 stored members: no other member passes the filter (65 fail F0, 6 fail F3)")
    need(len(r["pairs"]) == 8 and sorted(map(tuple, r["pairs"])) == [(5, 5), (5, 7), (7, 3), (7, 5), (7, 7), (7, 11), (7, 13), (9, 7)], "EXP-017 stored members: the eight pairs")
    for fld in ("tabled", "pure", "other"):
        need(sum(x[fld] for x in r["rows"]) == t[fld], f"EXP-017 stored members: the rows sum to the total {fld}")
    for st in ("pure_by_stage", "other_by_stage"):
        need([sum(x[st][i] for x in r["rows"]) for i in range(5)] == t[st], f"EXP-017 stored members: the rows sum to the total {st}")
    N["stmTabled"] = t["tabled"]
    N["stmPure"] = t["pure"]
    N["stmOther"] = t["other"]
    N["stmFailFZero"] = t["other_by_stage"][0]
    N["stmFailFThree"] = t["other_by_stage"][3]
    N["stmPairs"] = len(r["pairs"])



# ---- EXP-019 and EXP-020 ----

E19 = PROBLEM / "experiments" / "EXP-019-filter-every-exponent"
E20 = PROBLEM / "experiments" / "EXP-020-symmetric-members"
PW.update({29: "TwentyNine", 31: "ThirtyOne"})
EWL.update({15: "Fifteen"})
E19_PAIRS = [(13, 11), (13, 7), (14, 5), (15, 19), (15, 23), (15, 29), (16, 23), (16, 29), (16, 31)]
E19_NOT = {(14, 11): "not finished", (15, 17): "not finished", (16, 17): "not started", (16, 19): "not started"}
E20_PAIRS = [(14, 11), (15, 11), (15, 13), (15, 17), (16, 17), (16, 19)]


def read_sixth(root):
    ex = Path(root) / "experiments"
    return tuple(jload(ex / d.name / "artifacts" / "results.json") for d in (E19, E20))


def largest_allowed_t(e, p):
    """The largest t of the parity of e with t <= e - 2, 2t <= p - 1 and, when p <= e, p not dividing (e + t)/2."""
    ok = [t for t in range(1, e - 1) if (t - e) % 2 == 0 and 2 * t <= p - 1 and not (p <= e and ((e + t) // 2) % p == 0)]
    return max(ok) if ok else None


def exp19(r19, N, out):
    """EXP-019: the filter (F0) to (F3) for every exponent t, on random members of the stratum with the largest allowed t."""
    need(r19["experiment"] == "EXP-019", "EXP-019 results file")
    g = r19["gates"]
    st = g["G1"]["stored"]
    need(st["pure"] == 317 and st["other"] == 128 and st["pure_by_stage"] == [0, 0, 0, 0, 317] and st["other_by_stage"] == [108, 0, 0, 20, 0] and st["not_of_the_form"] == 0 and st["ok"] is True,
         "EXP-019 gate G1 (a): the stored members and the filter")
    need(g["G1"]["family"]["passed"] is True and all(x["ok"] for x in g["G1"]["family"]["rows"]), "EXP-019 gate G1 (b): the controls")
    need(g["G2"]["passed"] is True and g["G2"]["sample_members"] == g["G2"]["agree_and_pure_in_I2"] == 39 and g["G2"]["failing_cases"] == [], "EXP-019 second instrument")
    tot = r19["totals"]
    need(len(tot) == 17 and sorted(k for k in tot if k[0] == "K") == ["K|11|17", "K|13|17", "K|9|11", "K|9|13"], "EXP-019: 17 cases")
    rows, passed, tables, pure_tables = [], 0, 0, 0
    for key in sorted(tot, key=lambda k: ("KXY".index(tot[k]["family"]), tot[k]["e"], tot[k]["p"])):
        t_ = tot[key]
        e, p, t = t_["e"], t_["p"], t_["t"]
        need(t_["f0"] >= t_["f1"] >= t_["f2"] >= t_["f3"] == t_["pure_hilbert"] and t_["pure"] <= t_["tables"] <= t_["pure_hilbert"], f"EXP-019 {key}: counts")
        need(2 * t <= p - 1, f"EXP-019 {key}: 2t <= p - 1")
        if t_["family"] != "K":
            need(t == largest_allowed_t(e, p), f"EXP-019 {key}: t is the largest allowed exponent")
        need(t_["family"] == "K" or t_["status"] in ("early stop", "not finished", "not started"), f"EXP-019 {key}: status")
        passed += t_["f3"]
        tables += t_["tables"]
        pure_tables += t_["pure"]
        status = {"early stop": "5 pure members", "not finished": "not finished", "not started": "not started"}[t_["status"]]
        rows.append([{"K": "K", "X": "X", "Y": "Y"}[t_["family"]], "$(%d,%d)$" % (e, p), str(t), str(e - t - 2), thousands(t_["examined"]), thousands(t_["f0"]), thousands(t_["f1"]), thousands(t_["f2"]),
                     thousands(t_["f3"]), thousands(t_["pure_hilbert"]), str(t_["tables"]), str(t_["pure"]), status])
    need(passed == 5387 and tables == 143 and pure_tables == 143, "EXP-019: 5,387 passing members and 143 tables, all pure")
    out["tab_everyt.tex"] = table("@{}lllrrrrrrrrrl@{}", ["", "$(e,p)$", "$t$", "cond.", "examined", "(F0)", "(F1)", "(F2)", "(F3)", "pure $h_e$", "tables", "pure", "status"], rows)
    for key, why in ((("X|14|11"), "not finished"), ("Y|15|17", "not finished"), ("Y|16|17", "not started"), ("Y|16|19", "not started")):
        need(tot[key]["status"] == why and tot[key]["pure"] == 0 and tot[key]["f3"] == 0, f"EXP-019 {key}: {why}")
    need(tot["X|14|11"]["examined"] == 380108800 and tot["X|14|11"]["f2"] == 10 and tot["Y|15|17"]["examined"] == 13107200, "EXP-019: the interrupted cases")
    pr = r19["predictions"]
    p1 = {tuple(x["pair"]): x["outcome"] for x in pr["P1"]["rows"]}
    need(p1 == {(13, 11): "holds", (13, 7): "holds", (14, 5): "holds", (14, 11): "not decided"}, f"EXP-019 P1: {p1}")
    p2 = {tuple(x["pair"]): x["outcome"] for x in pr["P2"]["rows"]}
    need(sum(1 for v in p2.values() if v == "holds") == 6 and sum(1 for v in p2.values() if v == "not decided") == 3 and len(p2) == 9, f"EXP-019 P2: {p2}")
    need(sum(1 for x in pr["P3"]["rows"] if x["outcome"] == "holds") == 13 and not any(x["outcome"] == "does not hold" for x in pr["P3"]["rows"]), "EXP-019 P3")
    need(sum(1 for x in pr["P4"]["rows"] if x["outcome"] == "holds") == 13 and not any(x["outcome"] == "does not hold" for x in pr["P4"]["rows"]), "EXP-019 P4")
    p5 = [x for x in pr["P5"]["rows"] if x["outcome"] == "holds"]
    need(len(p5) == 7, "EXP-019 P5: holds in seven cases")
    cs = r19["cases"]
    prow = []
    for (e, p) in E19_PAIRS:
        fam = "X" if (e, p) in ((13, 11), (13, 7), (14, 5)) else "Y"
        c = cs["%s|%d|%d" % (fam, e, p)]
        mem = next(x for x in c["members"] if x["pure"])
        tf, tg, ln = pair_row(f"EXP-019 pair {e},{p}", e, p, mem, tuple(c["stratum"]), check_length=False)
        prow.append(["$(%d,%d)$" % (e, p), str(c["t"]), "$S(%d;%d,%d)$" % tuple(c["stratum"]), "$f=%s$\\newline $g=%s$" % (poly_tex(tf, p), poly_tex(tg, p)), str(ln)])
    need(len(prow) == 9, "EXP-019: nine printed pairs")
    out["tab_everytpairs.tex"] = table("@{}lllp{6.4cm}r@{}", ["$(e,p)$", "$t$", "stratum", "forms over $\\F_p$", "length"], prow)
    N["evtPassed"] = thousands(passed)
    N["evtTables"] = tables
    N["evtSeconds"] = thousands(round(r19["budget"]["used_seconds"]))
    N["evtLimit"] = thousands(r19["budget"]["limit_seconds"])
    N["evtStored"] = st["pure"] + st["other"]
    N["evtStoredPure"] = st["pure"]
    N["evtStoredOther"] = st["other"]
    N["evtFailFZero"] = st["other_by_stage"][0]
    N["evtFailFThree"] = st["other_by_stage"][3]
    N["evtSample"] = g["G2"]["sample_members"]
    N["evtFourteenElevenExamined"] = thousands(tot["X|14|11"]["examined"])
    N["evtFifteenSeventeenExamined"] = thousands(tot["Y|15|17"]["examined"])
    N["evtFourteenElevenFTwo"] = tot["X|14|11"]["f2"]
    N["evtCases"] = len(tot)
    pt = r19["partial"]
    N["evtWallFifteenSeventeen"] = thousands(round(pt["Y|15|17"]["wall_seconds"]))
    N["evtWallFourteenEleven"] = thousands(round(pt["X|14|11"]["wall_seconds"]))
    N["evtRateFifteenSeventeen"] = thousands(tot["Y|15|17"]["filter_members_per_second_per_worker"])
    N["evtRateFourteenEleven"] = thousands(tot["X|14|11"]["filter_members_per_second_per_worker"])
    N["evtRatioLow"] = "%.2f" % min(x["ratio"] for x in p5)
    N["evtRatioHigh"] = "%.2f" % max(x["ratio"] for x in p5)
    N["evtMaxTables"] = max(t_["tables"] for t_ in tot.values())
    N["evtPassingCases"] = sum(1 for t_ in tot.values() if t_["f3"] > 0)
    N["evtWorkersMax"] = max(x["workers"] for x in r19["runs"] if "workers" in x)
    N["evtWorkersMin"] = min(x["workers"] for x in r19["runs"] if "workers" in x)


def exp20(r20, N, out):
    """EXP-020: the members x^e + alpha y^t, y^e + beta x^t with beta = c alpha^omega, enumerated completely."""
    need(r20["experiment"] == "EXP-020", "EXP-020 results file")
    g = r20["gates"]
    need(g["G1"]["passed"] is True and g["G2"]["passed"] is True and g["G2"]["sample_members"] == g["G2"]["agree_and_pure_in_I2"] == 27 and g["G2"]["failing_cases"] == [], "EXP-020 gates")
    tot = r20["totals"]
    need(len(tot) == 9 and sorted(tot) == sorted(["K|9|13", "K|11|17", "K|13|11"] + ["X|%d|%d" % x for x in E20_PAIRS]), "EXP-020: nine cases")
    members = f0 = passing = c1 = tables = pure_tables = 0
    rows = []
    for key in sorted(tot, key=lambda k: ("KX".index(tot[k]["family"]), tot[k]["e"], tot[k]["p"])):
        t_ = tot[key]
        e, p, t, d = t_["e"], t_["p"], t_["t"], t_["stratum"][2]
        need(t_["status"] == "complete" and t_["examined"] == t_["members"] == 2 * (p ** (d + 1) - 1), f"EXP-020 {key}: complete list of 2 (p^(d+1) - 1) members")
        need(2 * t <= p - 1, f"EXP-020 {key}: 2t <= p - 1")
        need(t_["differ"] == 0, f"EXP-020 {key}: no member with (F0) where (F1) and (F2) differ")
        need(t_["f0"] >= t_["f1"] >= t_["f3"] == t_["pure_hilbert"] and t_["f1"] == t_["f2"] and t_["c1"] <= t_["f3"] and t_["pure"] <= t_["tables"], f"EXP-020 {key}: counts")
        need(t_["tables"] == t_["pure"] == 5, f"EXP-020 {key}: five tables, all pure")
        members += t_["members"]
        f0 += t_["f0"]
        passing += t_["f3"]
        c1 += t_["c1"]
        tables += t_["tables"]
        pure_tables += t_["pure"]
        rows.append([t_["family"], "$(%d,%d)$" % (e, p), str(t), thousands(t_["members"]), thousands(t_["f0"]), thousands(t_["f1"]), thousands(t_["f2"]), str(t_["differ"]), thousands(t_["f3"]),
                     thousands(t_["c1"]), thousands(t_["pure_hilbert"]), str(t_["tables"]), str(t_["pure"])])
    need(members == 27760520 and f0 == 13011416 and passing == 2522 and c1 == 2436 and tables == 45 and pure_tables == 45, "EXP-020: totals of the nine lists")
    out["tab_symm.tex"] = table("@{}llrrrrrrrrrrr@{}", ["", "$(e,p)$", "$t$", "members", "(F0)", "(F1)", "(F2)", "differ", "(F3)", "(C1)", "pure $h_e$", "tables", "pure"], rows)
    pr = r20["predictions"]
    need(all(x["outcome"] == "holds" for x in pr["P1"]["rows"]) and len(pr["P1"]["rows"]) == 6, "EXP-020 P1")
    need(all(x["outcome"] == "holds" for x in pr["P2"]["rows"]) and len(pr["P2"]["rows"]) == 9, "EXP-020 P2")
    need(all(x["outcome"] == "holds" for x in pr["P3"]["rows"]) and len(pr["P3"]["rows"]) == 9, "EXP-020 P3")
    p4 = {x["case"]: x["outcome"] for x in pr["P4"]["rows"]}
    need(p4 == {"X|14|11": "holds", "X|15|11": "does not hold", "X|15|13": "holds", "X|15|17": "does not hold", "X|16|17": "holds", "X|16|19": "holds"}, f"EXP-020 P4: {p4}")
    p3 = {x["case"]: x for x in pr["P3"]["rows"]}
    need(p3["X|14|11"]["tables_c1"] == 0 and p3["X|14|11"]["tables_no_c1"] == 5 and tot["X|14|11"]["c1"] == 48 and tot["X|14|11"]["f3"] == 84, "EXP-020: (14,11), five tables without (C1), 48 of 84 with (C1)")
    tc1 = sum(x["tables_c1"] for x in p3.values())
    tno = sum(x["tables_no_c1"] for x in p3.values())
    need(tc1 == 31 and tno == 14, "EXP-020: 31 tables with (C1), 14 without")
    cs = r20["cases"]
    prow = []
    for (e, p) in E20_PAIRS:
        c = cs["X|%d|%d" % (e, p)]
        mem = next(x for x in c["passing"] if x.get("pure"))
        tf, tg, ln = pair_row(f"EXP-020 pair {e},{p}", e, p, mem, tuple(c["stratum"]), check_length=False)
        need(mem["length"] == e ** 3, f"EXP-020 pair {e},{p}: stored length")
        prow.append(["$(%d,%d)$" % (e, p), str(c["t"]), "$S(%d;%d,%d)$" % tuple(c["stratum"]), "$f=%s$\\newline $g=%s$" % (poly_tex(tf, p), poly_tex(tg, p)), str(ln)])
    out["tab_symmpairs.tex"] = table("@{}lllp{6.4cm}r@{}", ["$(e,p)$", "$t$", "stratum", "forms over $\\F_p$", "length"], prow)
    N["symMembers"] = thousands(members)
    N["symFZero"] = thousands(f0)
    N["symPassing"] = thousands(passing)
    N["symCOne"] = thousands(c1)
    N["symTables"] = tables
    N["symTablesCOne"] = tc1
    N["symTablesNoCOne"] = tno
    N["symSeconds"] = thousands(round(r20["budget"]["used_seconds"]))
    N["symWall"] = thousands(round(r20["wall_seconds_total"]))
    N["symLimit"] = thousands(r20["budget"]["limit_seconds"])
    N["symSample"] = g["G2"]["sample_members"]
    N["symFourteenElevenPassing"] = tot["X|14|11"]["f3"]
    N["symFourteenElevenCOne"] = tot["X|14|11"]["c1"]
    N["symRatioFifteenEleven"] = "%.2f" % tot["X|15|11"]["ratio"]
    N["symRatioFifteenSeventeen"] = "%.2f" % tot["X|15|17"]["ratio"]
    N["symRatioLow"] = "%.2f" % min(tot[k]["ratio"] for k in tot if k.startswith("X") and p4["X|" + k.split("|", 1)[1]] == "holds")
    N["symRatioHigh"] = "%.2f" % max(tot[k]["ratio"] for k in tot if k.startswith("X") and p4["X|" + k.split("|", 1)[1]] == "holds")


def sixth_sets(r19, r20):
    """The pairs settled by a pure member of EXP-019 (code E) and of EXP-020 (code X), with the stratum of the first."""
    e19, x20, detail = set(), set(), {}
    for k, t_ in r19["totals"].items():
        if t_["family"] in "XY" and t_["pure"] > 0:
            e19.add((t_["e"], t_["p"]))
            detail[(t_["e"], t_["p"])] = "filter for every exponent, $S(%d;%d,%d)$ (EXP-019)" % tuple(t_["stratum"])
    for k, t_ in r20["totals"].items():
        if t_["family"] == "X" and t_["pure"] > 0:
            x20.add((t_["e"], t_["p"]))
            detail.setdefault((t_["e"], t_["p"]), "member fixed by the exchange, $S(%d;%d,%d)$ (EXP-020)" % tuple(t_["stratum"]))
    return e19, x20, detail


def short_pair_cells(emax):
    """The pairs (e, p), 4 <= e <= emax, with p = 2e - 1 or p = 2e - 3 prime (p >= 5): settled by the short pair of Section exptexplicit, with the text of their source."""
    cells = {}
    for e in range(4, emax + 1):
        for p, th in ((2 * e - 1, "A"), (2 * e - 3, "B")):
            if p >= 5 and all(p % q for q in range(2, int(p ** 0.5) + 1)):
                if (e, p) == (6, 11):
                    txt = "short pair with $n=3$ (Corollary~\\ref{cor:exptexplA})"
                elif (e, p) == (4, 5):
                    txt = "short pair with $n=3$ (Corollary~\\ref{cor:exptexplB})"
                elif th == "A":
                    txt = "short pair of Theorem~\\ref{thm:exptexplA}"
                else:
                    txt = "short pair of Theorem~\\ref{thm:exptexplB}"
                cells[(e, p)] = txt
    return cells


def build_new(root, N, data_root=None):
    """Read the artifacts of EXP-005 to EXP-009, EXP-011 and EXP-012 under `root`, check every value the text uses, and return the
    generated files. When `data_root` (or the environment variable CAOS_RESEARCH_DATA_ROOT) names the data root and the full results
    file of EXP-006 is there, its hash is checked against the recorded one."""
    import os
    r5, r6, r7, r8 = read_artifacts(root)
    r9, r11, r12 = read_later(root)
    out = {}
    formula_checks(N)
    exp5(r5, N, out)
    exp6(r6, r8, N, out, data_root or os.environ.get("CAOS_RESEARCH_DATA_ROOT"))
    exp7(r7, N, out)
    exp9(r9, N, out)
    exp11(r11, N, out)
    exp12(r12, N, out)
    r10, r13, r14 = read_second(root)
    exp10(r10, N, out)
    exp13(r13, N, out)
    exp14(r14, N, out)
    r15, r17 = read_third(root)
    exp15(r15, N, out)
    exp17(r17, N, out)
    exp17_stored(root, N)
    exp16(read_fourth(root), N, out)
    exp18(read_fifth(root), N, out)
    r19_, r20_ = read_sixth(root)
    exp19(r19_, N, out)
    exp20(r20_, N, out)
    wz_outputs(r10, r14, r15, N, out)
    rule_outputs(r9, r10, r14, r15, N, out)
    return out


# --------------------------------------------------------------------------------------------------------------------------
# figures
# --------------------------------------------------------------------------------------------------------------------------

STYLE = {
    "every": ("circle", "blue!60!black", "blue!60!black"),
    "zero": ("diamond", "teal!70!black", "teal!70!black"),
    "prime": ("square", "orange!85!black", "orange!85!black"),
    "excluded": ("cross", "red!75!black", None),
    "open": ("circle", "black", "white"),
    "u_other": ("circle", "gray!80", "gray!40"),
    "u_char2_done": ("diamond", "teal!70!black", "teal!70!black"),
    "u_char2_excl": ("diamondx", "red!75!black", "red!75!black"),
    "u_char2_open": ("diamond", "black", "white"),
    "u_open_s": ("square", "orange!85!black", "white"),
}


def draw_marker(style, x, y, s):
    shape, col, fill = STYLE[style]
    if shape == "circle":
        return "\\draw[%s, fill=%s, line width=0.4pt] (%.3f,%.3f) circle (%.3f);" % (col, fill, x, y, s)
    if shape in ("diamond", "diamondx"):
        t = s * 1.3
        out = "\\draw[%s, fill=%s, line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f) -- cycle;" % (col, fill, x - t, y, x, y + t, x + t, y, x, y - t)
        if shape == "diamondx":
            out += " \\draw[white, line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f) (%.3f,%.3f) -- (%.3f,%.3f);" % (x - s * 0.7, y - s * 0.7, x + s * 0.7, y + s * 0.7, x - s * 0.7, y + s * 0.7, x + s * 0.7, y - s * 0.7)
        return out
    if shape == "square":
        return "\\draw[%s, fill=%s, line width=0.4pt] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (col, fill, x - s, y - s, x + s, y + s)
    t = s * 1.2
    return "\\draw[%s, line width=0.8pt] (%.3f,%.3f) -- (%.3f,%.3f) (%.3f,%.3f) -- (%.3f,%.3f);" % (col, x - t, y - t, x + t, y + t, x - t, y + t, x + t, y - t)


def draw_panels(items, layout, unit, msize):
    """items: (d1, d2, d3) -> style; layout: rows of d3 values; returns (lines, total height)."""
    lines = []
    y = 0.0
    for row in layout:
        x = 0.0
        row_height = max(d3 * unit + 0.12 for d3 in row)
        for d3 in row:
            w = (d3 - 1) * unit + 0.12
            h = d3 * unit + 0.12
            lines.append("\\begin{scope}[shift={(%.3f,%.3f)}]" % (x, y - h))
            lines.append("\\draw[gray!70, line width=0.4pt] (0,0) rectangle (%.3f,%.3f);" % (w, h))
            lines.append("\\node[anchor=south west,inner sep=1pt] at (0,%.3f) {$d_3=%d$};" % (h, d3))
            for t1 in range(1, d3 - 1, 2):
                lines.append("\\node[anchor=north,inner sep=1pt,font=\\tiny] at (%.3f,0) {%d};" % (0.06 + (t1 - 1) * unit, t1))
            for t2 in range(2, d3, 2):
                lines.append("\\node[anchor=east,inner sep=1pt,font=\\tiny] at (0,%.3f) {%d};" % (0.06 + (t2 - 2) * unit, t2))
            for (d1, d2, d3_), style in sorted(items.items()):
                if d3_ == d3:
                    lines.append(draw_marker(style, 0.06 + (d1 - 1) * unit, 0.06 + (d2 - 2) * unit, msize))
            lines.append("\\end{scope}")
            x += w + 0.7
        y -= row_height + 0.9
    lines.append("\\node[anchor=north west,font=\\scriptsize] at (0,%.3f) {horizontal axis $d_1$ from 1, vertical axis $d_2$ from 2; one mark per ray $(0,d_1,d_2,d_3)$ with $d_1<d_2<d_3$.};" % (y + 0.55))
    return lines, y - 0.2


def draw_legend(entries, y0, ncols):
    lines = []
    col_w = 7.6
    for i, (style, text) in enumerate(entries):
        x = (i % ncols) * col_w
        y = y0 - (i // ncols) * 0.45
        lines.append(draw_marker(style, x + 0.1, y, 0.07))
        lines.append("\\node[anchor=west,font=\\scriptsize,inner sep=1pt] at (%.2f,%.2f) {%s};" % (x + 0.3, y, text))
    return lines


def lattice_s(F, N):
    cls = F["cls"]
    items = {(d[1], d[2], d[3]): k for d, k in cls.items()}
    body, ybot = draw_panels(items, [[12, 11, 10, 9], [8, 7, 6, 5, 4, 3]], 0.26, 0.075)
    legend = [("every", "realized over every field or infinite field"), ("zero", "realized in characteristic 0 (formula or module over $\\mathbb{Q}$)"),
              ("prime", "realized over $\\mathbb{F}_{32003}$ only"), ("excluded", "primitive point excluded"), ("open", "open")]
    lines = ["\\begin{tikzpicture}[x=1cm,y=1cm,font=\\scriptsize]"] + body + draw_legend(legend, ybot - 0.2, 2) + ["\\end{tikzpicture}"]
    OUT["fig_lattice_s.tex"] = "\n".join(lines) + "\n"
    n = Counter(cls.values())
    need((n["every"], n["zero"], n["prime"], n["excluded"], n["open"]) == (N["realizedEvery"], N["realizedZeroOnly"], N["realizedPrimeOnly"], N["excluded"], N["open"]), f"lattice counts {n}")
    N["figPrimeOnly"] = n["prime"]


def lattice_u(F, N, byray_b1, rays):
    cls = F["cls"]
    items = {}
    counts = Counter()
    for x in rays:
        if x["parity"] != 0:
            continue
        dd = tuple(x["d"])
        key = (dd[1], dd[2], dd[3])
        st = x["status_primitive"]
        if st == "excluded":
            if dd in CHAR2_THEOREM_RAYS:
                kind = "u_char2_excl"
            elif dd in CHAR2_SEARCH_RAYS or dd == (0, 1, 3, 4):
                kind = "u_char2_done"
            else:
                kind = "u_char2_open"
        elif st == "open":
            kind = "u_open_s"
        else:
            kind = "every" if cls[dd] == "every" else "u_other"
        items[key] = kind
        counts[kind] += 1
    need(len(items) == 29, "29 parity-passing rays")
    body, ybot = draw_panels(items, [[12, 10], [8, 6, 4]], 0.3, 0.085)
    leg = [("every", "realized over $S$ over every field or infinite field"), ("u_other", "realized over $S$ in characteristic 0 or over $\\mathbb{F}_{32003}$"),
           ("u_char2_done", "excluded over $S$; realized over $U$ in characteristic 0 and in characteristic 2"),
           ("u_char2_excl", "excluded over $S$; realized over $U$ in characteristic 0; excluded over both rings in characteristic 2"),
           ("u_char2_open", "excluded over $S$; realized over $U$ in characteristic 0; characteristic 2 not decided"),
           ("u_open_s", "open over $S$; realized over $U$ in characteristic 0")]
    lines = ["\\begin{tikzpicture}[x=1cm,y=1cm,font=\\scriptsize]"] + body + draw_legend(leg, ybot - 0.2, 1) + ["\\end{tikzpicture}"]
    OUT["fig_lattice_u.tex"] = "\n".join(lines) + "\n"
    N["uEveryCount"], N["uOtherCount"] = counts["every"], counts["u_other"]
    N["uCharTwoDone"], N["uCharTwoExcl"], N["uCharTwoOpen"], N["uSquare"] = counts["u_char2_done"], counts["u_char2_excl"], counts["u_char2_open"], counts["u_open_s"]
    need(counts["u_char2_done"] == 6 and counts["u_char2_excl"] == 3 and counts["u_char2_open"] == 1 and counts["u_open_s"] == 1, f"classes over U {counts}")


def fig_hilbert(d, F, N):
    c3 = {x["e"]: x for x in d["r2"]["claims"]["C3"]["cases"]}
    c1 = F["c1"]
    colors = {2: "black", 3: "blue!60!black", 4: "red!75!black", 5: "teal!70!black", 6: "orange!85!black"}
    marks = {2: "*", 3: "square*", 4: "triangle*", 5: "diamond*", 6: "pentagon*"}
    lines = ["\\begin{tikzpicture}", "\\begin{groupplot}[group style={group size=2 by 1, horizontal sep=1.6cm}, width=7.4cm, height=5.6cm, tick label style={font=\\scriptsize}, label style={font=\\small}]"]
    lines.append("\\nextgroupplot[xlabel={degree $d$}, ylabel={$\\dim (M_e)_d$}, legend style={font=\\scriptsize, at={(0.5,-0.28)}, anchor=north}, xmin=0, ymin=0, legend columns=3]")
    for e in (2, 3, 4, 5, 6):
        hf = c3[e]["hilbert_function"]
        need(hf == h_series(e), f"EXP-002 C3 e={e}: Hilbert function differs from h_e")
        pts = " ".join("(%d,%d)" % (i, v) for i, v in enumerate(hf))
        lines.append("\\addplot[color=%s, mark=%s, mark size=1.4pt, thick] coordinates {%s};" % (colors[e], marks[e], pts))
        lines.append("\\addlegendentry{$e=%d$}" % e)
    lines.append("\\nextgroupplot[xlabel={degree $d$}, ylabel={block dimension}, ybar stacked, bar width=4.5pt, xmin=-0.7, xmax=12.7, ymin=0, legend style={font=\\scriptsize, at={(0.5,-0.28)}, anchor=north}, legend columns=4, xtick distance=2]")
    wp = c1[4]["weight_pieces"]
    shades = {0: "black!85", 1: "black!60", 2: "black!35", 3: "black!12"}
    for q in range(0, 4):
        pts = []
        for dg in range(0, 13):
            tot = 0
            for key, val in wp.items():
                w_, d_ = (int(s) for s in key.split(","))
                if abs(w_) == q and d_ == dg:
                    tot += val
            pts.append("(%d,%d)" % (dg, tot))
        lines.append("\\addplot[draw=black, fill=%s] coordinates {%s};" % (shades[q], " ".join(pts)))
        lines.append("\\addlegendentry{$|w|=%d$}" % q)
    lines += ["\\end{groupplot}", "\\end{tikzpicture}"]
    OUT["fig_hilbert.tex"] = "\n".join(lines) + "\n"
    # the stacked bars add up to h_4
    tot = [0] * 13
    for key, val in wp.items():
        w_, d_ = (int(s) for s in key.split(","))
        tot[d_] += val
    need(tot == h_series(4), "stacked blocks of e=4 differ from h_4")


def fig_weight(F, N):
    e = 4
    wp = F["c1"][e]["weight_pieces"]
    lines = ["\\begin{tikzpicture}[x=0.62cm,y=0.62cm,font=\\scriptsize]"]
    for w in range(-3, 4):
        for dg in range(0, 13):
            val = wp.get(f"{w},{dg}", 0)
            if (dg - w) % 2:
                continue
            shade = int(8 + 14 * val) if val else 0
            if val:
                lines.append("\\fill[black!%d] (%d,%d) rectangle +(1,1);" % (min(shade, 90), dg, w + 3))
            lines.append("\\draw[gray!50] (%d,%d) rectangle +(1,1);" % (dg, w + 3))
            if val:
                lines.append("\\node[%s] at (%.1f,%.1f) {%d};" % ("white" if shade > 50 else "black", dg + 0.5, w + 3.5, val))
    for dg in range(0, 13):
        lines.append("\\node[anchor=north] at (%.1f,0) {%d};" % (dg + 0.5, dg))
    for w in range(-3, 4):
        lines.append("\\node[anchor=east] at (0,%.1f) {%d};" % (w + 3.5, w))
    lines.append("\\node[anchor=north] at (6.5,-0.5) {degree $d$};")
    lines.append("\\node[anchor=south,rotate=90] at (-1.1,3.5) {weight $w$};")
    lines.append("\\end{tikzpicture}")
    OUT["fig_weight.tex"] = "\n".join(lines) + "\n"
    need(sum(wp.values()) == 64, "length 64 for e=4")


def fig_primes(d, F, N):
    c3 = F["c3"]
    lines = ["\\begin{tikzpicture}", "\\begin{axis}[width=0.8\\textwidth, height=8cm, xlabel={$e$}, ylabel={prime $p$}, xmin=1.5, xmax=8.5, ymin=0, ymax=25, xtick={2,...,8}, ytick={2,5,11,17,23}, tick label style={font=\\scriptsize}, legend style={font=\\scriptsize, at={(0.5,-0.18)}, anchor=north, /tikz/every even column/.append style={column sep=6pt}}, legend columns=2]"]
    pure, nonpure = [], []
    for e, v in sorted(c3.items()):
        for rec in v["per_prime"]:
            (nonpure if not rec["pure_table_I1"] else pure).append((e, rec["p"]))
    need(len(pure) + len(nonpure) == 4 * len(primes_upto(23)), "C3 points")
    lines.append("\\addplot[only marks, mark=*, mark size=2.2pt, color=blue!60!black] coordinates {%s};" % " ".join("(%d,%d)" % q for q in pure))
    lines.append("\\addlegendentry{pure table (experiment)}")
    lines.append("\\addplot[only marks, mark=x, mark size=3pt, thick, color=red!75!black] coordinates {%s};" % " ".join("(%d,%d)" % q for q in nonpure))
    lines.append("\\addlegendentry{not pure (experiment)}")
    lines.append("\\addplot[dashed, thick, color=black] coordinates {(1.5,3) (8.5,17)};")
    lines.append("\\addlegendentry{$p=2e$}")
    pred_ok = [(e, p) for e in (6, 7, 8) for p in primes_upto(23) if p >= 2 * e]
    pred_bad = [(e, p) for e in (6, 7, 8) for p in primes_upto(23) if p < 2 * e]
    lines.append("\\addplot[only marks, mark=*, mark size=2.2pt, color=blue!35] coordinates {%s};" % " ".join("(%d,%d)" % q for q in pred_ok))
    lines.append("\\addlegendentry{$e\\ge 6$, $p\\ge2e$: block check}")
    lines.append("\\addplot[only marks, mark=x, mark size=3pt, thick, color=red!40] coordinates {%s};" % " ".join("(%d,%d)" % q for q in pred_bad))
    lines.append("\\addlegendentry{$e\\ge 6$, $p<2e$: block check}")
    lines += ["\\end{axis}", "\\end{tikzpicture}"]
    OUT["fig_primes.tex"] = "\n".join(lines) + "\n"
    N["primePointsPure"], N["primePointsNonpure"] = len(pure), len(nonpure)
    need(all(p >= 2 * e for e, p in pure) and all(p < 2 * e for e, p in nonpure), "experimental purity does not equal p >= 2e")


def fig_stages(F, N):
    lines = ["\\begin{tikzpicture}", "\\begin{axis}[ybar, width=0.92\\textwidth, height=6cm, bar width=7pt, ymin=0, ymax=235, symbolic x coords={formulas and closures,known-answer runs,level-module family,search,rational rechecks,rank certificates}, xtick=data, x tick label style={font=\\scriptsize, rotate=15, anchor=east}, tick label style={font=\\scriptsize}, ylabel={rays}, legend style={font=\\scriptsize, at={(0.5,-0.45)}, anchor=north}, legend columns=4, enlarge x limits=0.1]"]
    series = [("primitive_realized", "realized", "black!70"), ("primitive_realized_char0", "realized in characteristic 0", "blue!50"),
              ("primitive_excluded", "excluded", "red!70"), ("primitive_open", "open", "white")]
    for key, lab, fill in series:
        pts = " ".join("(%s,%d)" % (name, s[key]) for name, s in F["stages"])
        lines.append("\\addplot[draw=black, fill=%s] coordinates {%s};" % (fill, pts))
        lines.append("\\addlegendentry{%s}" % lab)
    lines += ["\\end{axis}", "\\end{tikzpicture}"]
    OUT["fig_stages.tex"] = "\n".join(lines) + "\n"


def fig_diagrams():
    """Typed diagrams: the resolution of the trivial module, and the structure behind Theorem B."""
    res = r"""\begin{tikzpicture}[x=1cm,y=1cm,font=\small,>=Stealth]
\node (m0) at (0,0) {$U$};
\node (m1) at (3.3,0) {$U(-1)^2$};
\node (m2) at (6.9,0) {$U(-3)^2$};
\node (m3) at (10.2,0) {$U(-4)$};
\node (m4) at (12.4,0) {$0$};
\node (k) at (-2.1,0) {$k$};
\draw[<-] (k) -- node[above,font=\scriptsize]{$\varepsilon$} (m0);
\draw[<-] (m0) -- node[above,font=\scriptsize]{$(x,\,y)^{\mathsf T}$} (m1);
\draw[<-] (m1) -- node[above,font=\scriptsize]{$A$} (m2);
\draw[<-] (m2) -- node[above,font=\scriptsize]{$(y,\,-x)^{\mathsf T}$} (m3);
\draw[<-] (m3) -- (m4);
\node[font=\scriptsize,anchor=north] at (0,-0.5) {degree $0$};
\node[font=\scriptsize,anchor=north] at (3.3,-0.5) {generators in degree $1$};
\node[font=\scriptsize,anchor=north] at (6.9,-0.5) {generators in degree $3$};
\node[font=\scriptsize,anchor=north] at (10.2,-0.5) {generator in degree $4$};
\node[font=\scriptsize,anchor=north] at (5.2,-1.35) {$A=\begin{pmatrix}yx-2xy&x^2\\-y^2&2yx-xy\end{pmatrix}$};
\draw[decorate,decoration={brace,amplitude=4pt,mirror}] (-0.4,-2.05) -- node[below=4pt,font=\scriptsize]{Euler series $1-2t+2t^3-t^4=(1-t)^2(1-t^2)$} (10.8,-2.05);
\end{tikzpicture}
"""
    OUT["fig_resolution.tex"] = res.replace("decorate,decoration={brace,amplitude=4pt,mirror}", "thick")
    ch = r"""\begin{tikzpicture}[x=1cm,y=1cm,font=\small,>=Stealth]
\node[draw,rounded corners,minimum width=2.9cm,minimum height=0.9cm] (U) at (0,2.4) {$U=U^+\oplus U^-$};
\node[draw,rounded corners,minimum width=2.9cm,minimum height=0.9cm,align=center] (Up) at (-3.5,0.6) {$U^+=C\oplus C\,yx$\\ free of rank $1$ over $B$};
\node[draw,rounded corners,minimum width=2.9cm,minimum height=0.9cm,align=center] (Um) at (3.5,0.6) {$U^-=Cx\oplus Cy$\\ $\cong J(1)$, $J=(X,t)$};
\draw[->] (U) -- (Up); \draw[->] (U) -- (Um);
\node[draw,rounded corners,minimum width=4.6cm,minimum height=0.9cm,align=center] (B) at (-3.5,-1.5) {$B=C[t]/(t^2+Zt+XY)$\\ $uv=XY$, $u=t$, $v=t+Z$};
\node[draw,rounded corners,minimum width=4.6cm,minimum height=0.9cm,align=center] (S) at (3.5,-1.5) {$\Sigma=\operatorname{Proj}B=\mathbb{P}^1\times\mathbb{P}^1$\\ $\mathcal{O}(1)=\mathcal{O}(1,1)$};
\draw[->] (Up) -- node[left,font=\scriptsize]{$yx\mapsto t$} (B);
\draw[->] (Um) -- node[right,font=\scriptsize]{$\widetilde{\ \ }$} (S);
\draw[->] (B) -- node[above,font=\scriptsize]{$\operatorname{Proj}$} (S);
\node[font=\scriptsize,align=center,text width=13.4cm] at (0,-3.4) {$\widetilde{U^+}=\mathcal{O}$, $\widetilde{U^-}=\mathcal{O}(0,1)$ (twist by the line $X=t=0$ of class $(1,0)$);\\ for a presentation with $a$ generators and $b\le a+1$ relations of degree $e=2m$ or $2m+1$ the map $\psi:\mathcal{O}^b\to L^{\oplus a}$ with $L=\mathcal{O}(m,m)$ or $\mathcal{O}(m,m+1)$ is never onto.};
\end{tikzpicture}
"""
    OUT["fig_char2.tex"] = ch


# --------------------------------------------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    d = read_all()
    N, F = {}, {}
    numerator_checks(N)
    normal_ordering_check(N)
    bc = block_check(N)
    rays = census(d, N, F)
    hash_table(d, N)
    cases = kostant_and_ten(d, N, rays, F)
    char_two(d, N, rays, F)
    char_two_rays(rays, N)
    static_tables(N)
    lift_certificates(d, N, rays, F)
    controls(d, N)
    OUT.update(build_new(PROBLEM, N))
    strata_output(N, OUT)
    r5_, r6_, r7_, r8_ = read_artifacts(PROBLEM)
    r9_, _r11, _r12 = read_later(PROBLEM)
    r10_, r13_, r14_ = read_second(PROBLEM)
    r15_, r17_ = read_third(PROBLEM)
    r16_ = read_fourth(PROBLEM)
    w_, mid_, oth_, flt_, lst_, detail_ = search_sets_from_artifacts(r10_, r14_, r15_, r17_, r16_)
    for (e_, p_) in ((2, 3), (3, 3), (3, 5), (4, 3), (4, 5), (4, 7), (5, 3), (5, 5), (5, 7), (6, 3)):
        detail_.setdefault((e_, p_), "search in the whole space (EXP-006, EXP-008, EXP-003)")
    lg_ = set()
    for (e_, p_), s_ in largest_pairs(read_fifth(PROBLEM)).items():
        lg_.add((e_, p_))
        detail_.setdefault((e_, p_), "stratum with the largest exponent $S(%d;%d,%d)$ (EXP-018)" % s_)
    lin_ = linear_from_artifacts(r9_, r10_, r14_, r15_)
    r19_, r20_ = read_sixth(PROBLEM)
    e19_, x20_, d6_ = sixth_sets(r19_, r20_)
    for k_, v_ in d6_.items():
        detail_.setdefault(k_, v_)
    computed_ = set(lin_)
    short_ = short_pair_cells(16)
    for (e_, p_) in computed_:
        detail_[(e_, p_)] = "stratum of the linear family $S(%d;0,1)$ (EXP-009, EXP-010, EXP-014 or EXP-015)" % (e_ - 1)
    for (e_, p_), txt_ in short_.items():
        detail_[(e_, p_)] = txt_ + ("; computed members in $S(%d;0,1)$" % (e_ - 1) if (e_, p_) in computed_ else "")
    lin_ = set(lin_) | set(short_)
    state_outputs(N, OUT, explicit_from_artifacts(r6_, r8_, N["gfThreeHits"]), lin_, 16, (("W", w_), ("M", mid_), ("O", oth_), ("F", flt_), ("G", lst_), ("H", lg_), ("E", e19_), ("X", x20_)), detail_)
    procedures(d, N, cases)
    byray = None
    lattice_s(F, N)
    lattice_u(F, N, byray, rays)
    fig_hilbert(d, F, N)
    fig_weight(F, N)
    fig_primes(d, F, N)
    fig_stages(F, N)
    fig_diagrams()
    # the block-check table
    rows = []
    for e, (nb, nok, nbad, bad) in sorted(bc.items()):
        rows.append([str(e), thousands(nb), str(nok), "$\\{%s\\}$" % ",".join(map(str, bad)), "yes"])
    OUT["tab_blocks.tex"] = table("@{}rrrll@{}", ["$e$", "blocks $(w,n)$", "primes $p\\ge2e$ with generic blocks", "primes $p<2e$ (piece in degree $4e-2$)", "$\\mathbb{Q}$ rank $=D_q$"], rows)
    lines = ["% Generated by make_tables.py from the archived computations. Do not edit."]
    for k in sorted(N):
        lines.append(macro(k, N[k]))
    OUT["numbers.tex"] = "\n".join(lines) + "\n"
    if FAILS:
        print(f"{len(FAILS)} mismatch(es); nothing written", file=sys.stderr)
        sys.exit(1)
    if a.check:
        stale = [n for n, c in OUT.items() if not (HERE / n).exists() or (HERE / n).read_text(encoding="utf-8") != c]
        if stale:
            print("stale outputs: " + ", ".join(sorted(stale)), file=sys.stderr)
            sys.exit(1)
        print(f"outputs current ({len(OUT)} files)")
        return
    for n, c in OUT.items():
        (HERE / n).write_text(c, encoding="utf-8", newline="\n")
    print(f"wrote {len(OUT)} files")


if __name__ == "__main__":
    main()
