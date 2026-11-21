"""EXP-029: control of the weighted Chebyshev sum of the 2026-11-20 formal proof (hypothesis.md, declared before this code ran).

    S(x) = sum_{n <= x} Lambda(n) (x/n - 1),      G(x) = S(x) - x log x + (1 + gamma) x = x T(N) - psi(N) - x log x + (1 + gamma) x,
    N = floor(x),  T(N) = sum_{n <= N} Lambda(n)/n,  psi(N) = sum_{n <= N} Lambda(n).

Explicit formula with the zeros 1/2 + i g_j on the line (rho (rho - 1) = -(1/4 + g^2)):
    E(x) = 2 sqrt(x) sum_j cos(g_j log x)/(1/4 + g_j^2) + log 2 pi - sum_{k=1}^{20} x^(-2k)/(2k (2k + 1)).

Run from the repository root:
    python <this file> --zeros <path of Odlyzko's table zeros1> [--xmax 100000000] [--out artifacts/results.json]

The table of zeros is read from the path given on the command line (data root); no machine path is written to the results.
"""
import argparse
import hashlib
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
EULER_GAMMA = 0.57721566490153286060651209008240243104215933593992
LOG_2PI = math.log(2.0 * math.pi)
K_CONST = 2.0 + EULER_GAMMA - math.log(4.0 * math.pi)  # 2 + gamma - log 4 pi = sum over zeros of 1/|rho|^2 on the line
TRIVIAL_CONST = 1.0 - math.log(2.0)  # sum over k >= 1 of 1/(2k (2k + 1))
BLOCK = 5_000_000
N_ZEROS = 100_000


# ------------------------------------------------------------------ primes and the von Mangoldt function
def small_primes(limit):
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[:2] = False
    for p in range(2, int(limit ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p::p] = False
    return np.flatnonzero(sieve)


def mangoldt_block(a, b, base_primes):
    """Lambda(n) for a <= n < b as float64 (a >= 1): log p at the prime powers p^k, 0 elsewhere."""
    n = b - a
    is_prime = np.ones(n, dtype=bool)
    if a <= 1:
        is_prime[: 2 - a] = False
    lam = np.zeros(n, dtype=np.float64)
    top = math.isqrt(b - 1)
    for p in base_primes:
        p = int(p)
        if p > top:
            break
        start = max(p * p, ((a + p - 1) // p) * p)
        is_prime[start - a::p] = False
        q = p * p
        lp = math.log(p)
        while q < b:
            if q >= a:
                lam[q - a] = lp
            q *= p
    idx = np.flatnonzero(is_prime)
    lam[idx] = np.log((idx + a).astype(np.float64))
    return lam, int(idx.size)


class Sums:
    """Running T(N) and psi(N) with exact (fsum) carries between blocks; yields per block the arrays T(N), psi(N) for a <= N < b."""

    def __init__(self, xmax):
        self.xmax = xmax
        self.base = small_primes(math.isqrt(xmax) + 1)
        self.carry_t = 0.0
        self.carry_psi = 0.0
        self.pi = 0

    def blocks(self):
        a = 1
        while a <= self.xmax:
            b = min(a + BLOCK, self.xmax + 1)
            lam, npr = mangoldt_block(a, b, self.base)
            n = np.arange(a, b, dtype=np.float64)
            t = self.carry_t + np.cumsum(lam / n)
            psi = self.carry_psi + np.cumsum(lam)
            self.carry_t = math.fsum([self.carry_t, math.fsum((lam / n).tolist())])
            self.carry_psi = math.fsum([self.carry_psi, math.fsum(lam.tolist())])
            self.pi += npr
            yield a, b, n, t, psi
            a = b


def g_value(x, t_n, psi_n):
    """G(x) for floor(x) = N with T(N) = t_n and psi(N) = psi_n (arrays or scalars)."""
    return x * (t_n + EULER_GAMMA - np.log(x)) + (x - psi_n)


def interval_extremes(n, t, psi):
    """For each N of the arrays: (max, min) of G over [N, N + 1], the right end taken as the left limit.  G is concave there, so the
    maximum is at exp(T(N) + gamma) when that point is inside and at an end otherwise; the minimum is at an end."""
    left = g_value(n, t, psi)
    right = g_value(n + 1.0, t, psi)
    xs = np.exp(t + EULER_GAMMA)
    inside = (xs > n) & (xs < n + 1.0)
    crit = np.where(inside, xs - psi, -np.inf)  # G(x*) = x* - psi(N)
    return np.maximum(np.maximum(left, right), crit), np.minimum(left, right)


# ------------------------------------------------------------------ zeros and the explicit formula
def load_zeros(path, count=N_ZEROS):
    raw = Path(path).read_bytes()
    vals = np.array([float(tok) for tok in raw.split()[:count]], dtype=np.float64)
    return vals, hashlib.sha256(raw).hexdigest(), len(raw)


def explicit_formula(x, zeros):
    lx = math.log(x)
    s = float(np.sum(np.cos(zeros * lx) / (0.25 + zeros * zeros)))
    triv = sum(x ** (-2 * k) / (2 * k * (2 * k + 1)) for k in range(1, 21))
    return 2.0 * math.sqrt(x) * s + LOG_2PI - triv


def partial_constant(zeros):
    return float(np.sum(2.0 / (0.25 + zeros * zeros)))


# ------------------------------------------------------------------ high precision reference
def reference_values(points):
    """50-digit T(N), psi(N), G(N) at the given integers (increasing), by mpmath over the prime powers."""
    import mpmath as mp
    mp.mp.dps = 50
    top = max(points)
    primes = small_primes(top)
    gamma = mp.euler
    events = []
    for p in primes:
        p = int(p)
        lp = mp.log(p)
        q = p
        while q <= top:
            events.append((q, lp))
            q *= p
    events.sort(key=lambda e: e[0])
    out, t, psi, k = {}, mp.mpf(0), mp.mpf(0), 0
    for target in points:
        while k < len(events) and events[k][0] <= target:
            q, lp = events[k]
            t += lp / q
            psi += lp
            k += 1
        x = mp.mpf(target)
        out[target] = {"T": mp.nstr(t, 30), "psi": mp.nstr(psi, 30), "G": mp.nstr(x * t - psi - x * mp.log(x) + (1 + gamma) * x, 30)}
    return out


def refine_small(n_top, pieces):
    """The bound |G - log 2 pi| <= K sqrt(x) + (1 - log 2)/x^2 on [1, n_top), each unit interval cut into `pieces` pieces [a, b]:
    on a piece G is concave, so its maximum is at exp(T + gamma) when inside and at an end otherwise and its minimum at an end; the
    piece passes when K sqrt(a) + (1 - log 2)/b^2 - max |G - log 2 pi| >= 0."""
    base = small_primes(n_top + 1)
    lam, _ = mangoldt_block(1, n_top, base)
    t_all = np.cumsum(lam / np.arange(1, n_top, dtype=np.float64))
    psi_all = np.cumsum(lam)
    least, where, negative = math.inf, None, 0
    frac = np.arange(pieces + 1, dtype=np.float64) / pieces
    for k in range(n_top - 1):
        N, t, psi = float(k + 1), t_all[k], psi_all[k]
        edges = N + frac
        vals = g_value(edges, t, psi)
        a, b = edges[:-1], edges[1:]
        hi = np.maximum(vals[:-1], vals[1:])
        xs = math.exp(t + EULER_GAMMA)
        inside = (xs > a) & (xs < b)
        hi = np.where(inside, np.maximum(hi, xs - psi), hi)
        lo = np.minimum(vals[:-1], vals[1:])
        dev = np.maximum(np.abs(hi - LOG_2PI), np.abs(lo - LOG_2PI))
        margin = K_CONST * np.sqrt(a) + TRIVIAL_CONST / (b * b) - dev
        negative += int(np.sum(margin < 0.0))
        j = int(np.argmin(margin))
        if margin[j] < least:
            least, where = float(margin[j]), [float(a[j]), float(b[j])]
    return {"n_top": n_top, "pieces_per_unit": pieces, "least_margin": least, "piece": where, "negative_pieces": negative}


# ------------------------------------------------------------------ the run
def run(zeros_path, xmax, out_path):
    t0 = time.time()
    res = {"experiment": "EXP-029", "hypothesis": "hypothesis.md (declared before the run)", "xmax": xmax,
           "constants": {"K": K_CONST, "log_2pi": LOG_2PI, "trivial": TRIVIAL_CONST, "gamma": EULER_GAMMA}}

    # gate G3 and the constant (P4)
    zeros, zsha, zbytes = load_zeros(zeros_path)
    part = partial_constant(zeros)
    g_last = float(zeros[-1])
    tail_from_identity = K_CONST - part
    tail_from_density = (math.log(g_last / (2.0 * math.pi)) + 1.0) / (math.pi * g_last)
    res["zeros"] = {"count": int(zeros.size), "table_bytes": zbytes, "table_sha256": zsha, "first": float(zeros[0]), "last": g_last,
                    "increasing": bool(np.all(np.diff(zeros) > 0)), "partial_sum": part, "tail_from_identity": tail_from_identity,
                    "tail_from_density": tail_from_density}
    g3 = (zeros.size >= N_ZEROS and res["zeros"]["increasing"] and abs(zeros[0] - 14.134725142) < 1e-8
          and abs(g_last - 74920.827498994) < 1e-8)
    res["P4"] = {"sum_plus_density_tail": part + tail_from_density, "target": K_CONST, "difference": part + tail_from_density - K_CONST,
                 "holds": abs(part + tail_from_density - K_CONST) <= 1e-6}

    # the sweep: extremes, test points, reference points
    ref_points = [p for p in (10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7) if p <= xmax]
    grid = [math.exp(math.log(2.0) + i * (math.log(xmax) - math.log(2.0)) / 399.0) for i in range(400)]
    grid[-1] = min(grid[-1], float(xmax) - 1e-6)
    sums = Sums(xmax)
    at_ref, tests, powers = {}, [], []
    sup_all = {"value": -math.inf, "N": None}
    inf_all = {"value": math.inf, "N": None}
    sup_hi = {"value": -math.inf, "N": None}  # over [10^3, xmax]
    inf_hi = {"value": math.inf, "N": None}
    worst_margin = {"value": math.inf, "N": None}  # K sqrt(N) + trivial/(N+1)^2 - max|G - log 2 pi| over [N, N + 1]
    margin_hi = {"value": math.inf, "N": None}  # the same over N >= 1000 only
    decades = []
    gi = 0
    for a, b, n, t, psi in sums.blocks():
        gmax, gmin = interval_extremes(n, t, psi)
        dev_hi, dev_lo = gmax - LOG_2PI, gmin - LOG_2PI
        up = np.where(dev_hi >= 0, dev_hi / np.sqrt(n), dev_hi / np.sqrt(n + 1.0))
        lo = np.where(dev_lo <= 0, dev_lo / np.sqrt(n), dev_lo / np.sqrt(n + 1.0))
        margin = K_CONST * np.sqrt(n) + TRIVIAL_CONST / (n + 1.0) ** 2 - np.maximum(np.abs(dev_hi), np.abs(dev_lo))
        for store, arr, pick in ((sup_all, up, np.argmax), (inf_all, lo, np.argmin), (worst_margin, margin, np.argmin)):
            k = int(pick(arr))
            better = arr[k] > store["value"] if pick is np.argmax else arr[k] < store["value"]
            if better:
                store["value"], store["N"] = float(arr[k]), int(n[k])
        mask = n >= 1000.0
        if mask.any():
            for store, arr, pick in ((sup_hi, up, np.argmax), (inf_hi, lo, np.argmin), (margin_hi, margin, np.argmin)):
                sub = np.where(mask, arr, -np.inf if pick is np.argmax else np.inf)
                k = int(pick(sub))
                better = sub[k] > store["value"] if pick is np.argmax else sub[k] < store["value"]
                if better:
                    store["value"], store["N"] = float(sub[k]), int(n[k])
        for p in ref_points:
            if a <= p < b:
                k = p - a
                at_ref[p] = {"T": float(t[k]), "psi": float(psi[k]), "G": float(g_value(float(p), t[k], psi[k]))}
        while gi < len(grid) and grid[gi] < b:
            x = grid[gi]
            k = int(math.floor(x)) - a
            tests.append({"x": x, "G": float(g_value(x, t[k], psi[k]))})
            gi += 1
        if len(powers) < 60 and b > 10 ** 6:  # the first 30 prime powers q above 10^6: x = q and x = q - 1e-9
            jumps = np.flatnonzero(np.diff(psi) > 0) + 1  # indices k >= 1 with Lambda(n[k]) > 0
            for k in jumps:
                q = int(n[k])
                if q > 10 ** 6 and len(powers) < 60:
                    powers.append({"x": float(q), "G": float(g_value(float(q), t[k], psi[k]))})
                    xl = float(q) - 1e-9
                    powers.append({"x": xl, "G": float(g_value(xl, t[k - 1], psi[k - 1]))})
        decades.append({"upto": b - 1, "pi": sums.pi, "sup": sup_all["value"], "inf": inf_all["value"],
                        "seconds": round(time.time() - t0, 1)})
        print(f"up to {b - 1}: pi = {sums.pi}, sup {sup_all['value']:.6f} at {sup_all['N']}, inf {inf_all['value']:.6f} at "
              f"{inf_all['N']}, least margin {worst_margin['value']:.6f} at {worst_margin['N']} ({time.time() - t0:.0f} s)", flush=True)
    res["pi_xmax"] = sums.pi
    res["pi_1e6"] = int(small_primes(10 ** 6).size)
    res["G1"] = {"pi_1e6": res["pi_1e6"], "pi_xmax": sums.pi,
                 "passed": res["pi_1e6"] == 78498 and (sums.pi == 5761455 if xmax == 10 ** 8 else True)}

    # gate G2: precision against 50 digits
    ref = reference_values(ref_points)
    g2 = []
    for p in ref_points:
        diff = abs(at_ref[p]["G"] - float(ref[p]["G"]))
        g2.append({"N": p, "G_double": at_ref[p]["G"], "G_reference": ref[p]["G"], "difference": diff})
    res["G2"] = {"rows": g2, "passed": all(r["difference"] <= 1e-6 for r in g2)}
    res["G3"] = {"passed": bool(g3)}

    # P1: the explicit formula at the test points
    rows, worst = [], 0.0
    for kind, pts in (("grid", tests), ("prime power", powers)):
        for pt in pts:
            e = explicit_formula(pt["x"], zeros)
            bound = tail_from_identity * math.sqrt(pt["x"]) + 1e-6
            resid = abs(pt["G"] - e)
            worst = max(worst, resid / bound)
            rows.append({"kind": kind, "x": pt["x"], "G": pt["G"], "E": e, "residual": resid, "bound": bound, "ok": resid <= bound})
    res["P1"] = {"points": len(rows), "failures": sum(1 for r in rows if not r["ok"]), "largest_residual_over_bound": worst,
                 "holds": all(r["ok"] for r in rows), "sample": rows[::23]}
    fine = refine_small(1000, 4096)
    res["P2"] = {"unit_intervals_all_N": {"least_margin": worst_margin["value"], "at_N": worst_margin["N"]},
                 "unit_intervals_N_ge_1000": {"least_margin": margin_hi["value"], "at_N": margin_hi["N"]},
                 "refined_N_lt_1000": fine,
                 "holds": margin_hi["value"] >= 0.0 and fine["negative_pieces"] == 0,
                 "note": ("margin = K sqrt(a) + (1 - log 2)/b^2 - max |G - log 2 pi| over [a, b], a sufficient test of the bound on "
                          "[a, b]; unit intervals [N, N + 1] for N >= 1000, and 4096 pieces per unit interval for N < 1000, where "
                          "the term (1 - log 2)/x^2 matters and the unit-interval test is too coarse")}
    big = max(abs(sup_hi["value"]), abs(inf_hi["value"]))
    res["P3"] = {"sup_over_sqrt": sup_hi, "inf_over_sqrt": inf_hi, "largest_abs": big,
                 "holds": 0.012 <= big <= 0.0462 and sup_hi["value"] >= 0.008 and inf_hi["value"] <= -0.008}
    res["extremes_all"] = {"sup": sup_all, "inf": inf_all}
    res["progress"] = decades
    res["seconds"] = round(time.time() - t0, 1)
    res["PASS"] = bool(res["G1"]["passed"] and res["G2"]["passed"] and res["G3"]["passed"] and res["P1"]["holds"] and res["P2"]["holds"])
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: res[k] for k in ("G1", "G3", "P4", "PASS")}, indent=1))
    print("G2", res["G2"]["passed"], [r["difference"] for r in g2])
    print("P1", {k: res["P1"][k] for k in ("points", "failures", "largest_residual_over_bound", "holds")})
    print("P2", res["P2"]["unit_intervals_N_ge_1000"], res["P2"]["refined_N_lt_1000"], res["P2"]["holds"])
    print("P3", res["P3"]["sup_over_sqrt"], res["P3"]["inf_over_sqrt"], res["P3"]["holds"])
    return 0 if res["PASS"] else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zeros", required=True)
    ap.add_argument("--xmax", type=int, default=10 ** 8)
    ap.add_argument("--out", default=str(HERE / "artifacts" / "results.json"))
    a = ap.parse_args()
    sys.exit(run(a.zeros, a.xmax, a.out))


if __name__ == "__main__":
    main()
