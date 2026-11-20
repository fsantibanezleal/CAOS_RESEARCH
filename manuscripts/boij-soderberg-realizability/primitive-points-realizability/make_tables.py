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
        ["Search for pure pairs of forms (Algorithm~\\ref{alg:pairs})", "$\\mathbb{F}_q$, $q\\le27$", "%s spaces in 12 families and fields; %s s of summed process time, %s min wall time" % (N["sixSpacesTotal"], N["sixCpu"], N["sixWallMin"])],
        ["Tangent space of the rank locus (Algorithm~\\ref{alg:tangent})", "$\\mathbb{Q}$, $\\mathbb{F}_p$", "all cases of Section~\\ref{sec:resfamily}: %s s wall time" % N["sevenWall"]],
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
    return f"{100 * x:.{nd}f}"


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
            jload(ex / E7.name / "artifacts" / "results.json"))


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
    N["fiveOddHilbert"] = ",".join(str(x) for x in odd[0]["hilbert"][:9])
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
PAIRS6 = [("A1", "GF(3)", "index", 91), ("A2", "GF(5)", "seed", 20261122), ("B1", "GF(3)", "seed", 20261137),
          ("B1", "GF(5)", "seed", 20261156), ("B1", "GF(7)", "seed", 20261132), ("C", "GF(3)", "seed", 20263616)]


def pure_table(e):
    return [[0, 0, 1], [1, e, 2], [2, 3 * e, 2], [3, 4 * e, 1]]


def exp6(r6, N, out):
    need(r6["experiment"] == "EXP-006", "EXP-006 results file")
    for g in ("G1", "G2", "G3", "G4"):
        need(r6["gates"][g]["passed"] is True, f"EXP-006 gate {g}")
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
        key = FAMW[fam] + (FLDW.get(fld) or fld)
        N["six%sSpaces" % key] = thousands(x["spaces"])
        N["six%sPure" % key] = thousands(x["pure"])
        N["six%sPureHF" % key] = thousands(x["pure_hilbert"])
        N["six%sRank" % key] = thousands(x["rank_le_target"])
        N["six%sSharePure" % key] = pct(x["share_pure"], 1) if x["share_pure"] >= 0.01 else pct(x["share_pure"], 2)
        N["six%sShareRank" % key] = pct(x["share_rank_le_target"], 1)
        N["six%sRatioRank" % key] = f"{ratio:.1f}"
        N["six%sRatioPure" % key] = f"{x['share_pure'] / x['q_minus_2']:.2f}"
        N["six%sNonpure" % key] = thousands(nonpure)
        N["six%sTables" % key] = len(x["nonpure_tables"])
        rows3.append([str(e), fld_tex(fld), thousands(x["spaces"]), "%s (%s\\%%)" % (thousands(x["rank_le_target"]), pct(x["share_rank_le_target"], 1)),
                      thousands(x["pure_hilbert"]), thousands(x["pure"]), pct(x["share_pure"], 2) + "\\%", pct(x["q_minus_2"], 2) + "\\%",
                      f"{x['share_pure'] / x['q_minus_2']:.2f}"])
        rowsc.append([str(e), fld_tex(fld), thousands(x["pure_hilbert"]), thousands(x["pure"]), thousands(nonpure), str(len(x["nonpure_tables"])),
                      pct(nonpure / x["pure_hilbert"], 1) + "\\%"])
    out["tab_sixcounts.tex"] = table("@{}rrrrrrrrr@{}", ["$e$", "field", "spaces", "rank$\\,\\mu_{3e}\\le r$", "pure Hilbert function", "pure", "share pure", "$q^{-2}$", "pure$/q^{-2}$"], rows3)
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
    for fam, fld, kind, val in PAIRS6:
        e = FAM6[fam]
        pp, kk = fld_parse(fld)
        need(kk == 1, "explicit pairs are over prime fields")
        found = [s for k, c in chunks.items() if k.startswith(f"{fam}|{fld}|") for s in c["spaces"] if s.get(kind) == val]
        need(len(found) == 1, f"EXP-006 pair {fam}|{fld}|{kind} {val}: found {len(found)}")
        s = found[0]
        need(s["pure"] is True and s["betti"] == pure_table(e), f"EXP-006 pair {fam}|{fld}|{val}: Betti table")
        pair = [[(tuple(m), c) for m, c in f] for f in s["basis"]]
        hf = hilbert_pair(pair, e, pp, 4 * e - 3)
        need(hf == [he_val(e, n) for n in range(4 * e - 2)] and hf[-1] == 0 and sum(hf) == e ** 3, f"EXP-006 pair {fam}|{fld}|{val}: Hilbert function recomputed differs from h_e")
        need(hf == s["hilbert"][:4 * e - 2], f"EXP-006 pair {fam}|{fld}|{val}: stored Hilbert function")
        rows.append([str(e), fld_tex(fld), "$f=%s$\\newline $g=%s$" % (poly_tex(pair[0], pp), poly_tex(pair[1], pp)), str(e ** 3)])
        N["sixPairLength" + EW[e]] = e ** 3
    out["tab_sixpairs.tex"] = table("@{}rrp{9.6cm}r@{}", ["$e$", "field", "forms of degree $e$", "length"], rows)
    # figure: the share of pure spaces against q
    lines = ["\\begin{tikzpicture}",
             "\\begin{axis}[xmode=log, ymode=log, width=0.88\\textwidth, height=7cm, xlabel={field size $q$}, ylabel={share of random spaces}, "
             "xtick={3,5,7,9,11,13,25,27}, xticklabels={3,5,7,9,11,13,25,27}, minor xtick={}, ytick={0.001,0.01,0.1,1}, yticklabels={0.001,0.01,0.1,1}, minor ytick={}, "
             "tick label style={font=\\scriptsize}, label style={font=\\small}, grid=major, grid style={gray!25}, legend style={font=\\scriptsize, at={(0.5,-0.22)}, anchor=north}, legend columns=2]"]
    for key, mark, lab in (("pure3", "*", "pure, $e=3$"), ("pure4", "square*", "pure, $e=4$"), ("rank4", "triangle*", "rank$\\,\\mu_{12}\\le48$, $e=4$")):
        pts = " ".join("(%d,%.5f)" % (q, v) for q, v in sorted(fig[key]))
        lines.append("\\addplot[only marks, mark=%s, mark size=2pt] coordinates {%s};" % (mark, pts))
        lines.append("\\addlegendentry{%s}" % lab)
    lines.append("\\addplot[dashed, thick] coordinates {(3,%.5f) (27,%.7f)};" % (1 / 9.0, 1 / 729.0))
    lines.append("\\addlegendentry{$q^{-2}$}")
    lines.append("\\addplot[dotted, thick] coordinates {(3,%.5f) (27,%.6f)};" % (1 / 3.0, 1 / 27.0))
    lines.append("\\addlegendentry{$q^{-1}$}")
    lines += ["\\end{axis}", "\\end{tikzpicture}"]
    out["fig_sixshare.tex"] = "\n".join(lines) + "\n"


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


def build_new(root, N):
    """Read the artifacts of EXP-005 to EXP-007 under `root`, check every value the text uses, and return the generated files."""
    r5, r6, r7 = read_artifacts(root)
    out = {}
    formula_checks(N)
    exp5(r5, N, out)
    exp6(r6, N, out)
    exp7(r7, N, out)
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
