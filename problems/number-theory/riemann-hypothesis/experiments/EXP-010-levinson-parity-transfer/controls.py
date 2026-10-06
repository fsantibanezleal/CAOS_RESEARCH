"""EXP-010 adversarial numerical controls for Prediction B (declared required check 7).

Device: CPU, four worker processes, mpmath. These controls are numerical evidence only; the
theorem is proved in mathematical-proof.md. With L = log T (the convention of the proof),
V = Q(-D/L) f, E_beta = beta f - V - chi(s) V(1-s) and Vt = V + E_beta/2, they check:

  1. identities at T = 1e4, 1e5, 1e6 for Q of degree 1, 3, 5 and 7 (beta = 1 and beta != 1):
     chi(s)V(1-s) evaluated directly equals the operator formula sum q_k L^-k (D+lambda)^k f;
     e^{i vartheta} E_beta is real on the line; beta Z = 2 Re(e^{i vartheta} Vt);
  2. the counting lemma on zeta windows: sign changes of Z, level crossings of the argument
     and the zero count agree, and the finite form of Lemma 3.1 holds;
  3. toy functions f = zeta * prod((s-1/2)^2+gamma_j^2)^e_j with planted double (e=1) and
     triple (e=2) critical zeros: the lemma holds, double zeros are never counted, and the
     strict variant that drops the on-line zeros of Vt fails for deg Q = 1.

Outputs controls.json and stdout.txt in a new output directory.
"""

from __future__ import annotations

import argparse
import cmath
import hashlib
import json
import math
import subprocess
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import mpmath as mp

MAX_SECONDS = 1800.0
WORKERS = 4
HERE = Path(__file__).resolve().parent


def git_identity() -> dict[str, object]:
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=HERE, capture_output=True, text=True
    ).stdout.strip()
    clean = (
        subprocess.run(["git", "diff", "--quiet"], cwd=HERE).returncode == 0
        and subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=HERE).returncode == 0
    )
    return {"head": head, "tracked_tree_clean": clean}


# Q(x) = beta/2 + sum_{j odd} b_j (1-2x)^j satisfies Q(x) + Q(1-x) = beta.
QSPECS = {
    "Q1": (1, {1: 0.5}, "1-x (Levinson)"),
    "Q1bcy": (0.97, {1: 0.515}, "1-1.03x (Bui-Conrey-Young)"),
    "Q3": (1, {1: 0.6, 3: -0.1}, "cubic"),
    "Q5przz": (0.980928, {1: 0.636851, 3: -0.159327, 5: 0.032011}, "PRZZ quintic"),
    "Q7con": (0.984, {1: 0.602, 3: -0.08, 5: -0.06, 7: 0.046}, "Conrey 1989 degree 7"),
}


def get_q(name: str):
    beta, odd, _ = QSPECS[name]
    degree = max(odd)
    q = [mp.mpf(0)] * (degree + 1)
    q[0] += mp.mpf(beta) / 2
    for j, b in odd.items():
        for k in range(j + 1):
            q[k] += mp.mpf(b) * mp.binomial(j, k) * (-2) ** k
    return mp.mpf(beta), q


def chi(s):
    return mp.exp((s - mp.mpf(1) / 2) * mp.log(mp.pi) + mp.loggamma((1 - s) / 2) - mp.loggamma(s / 2))


def lambda_taylor(s0, n: int):
    """Taylor coefficients of lambda = -chi'/chi = psi(s/2)/2 + psi((1-s)/2)/2 - log(pi) at s0."""
    out = []
    for j in range(n):
        value = (
            mp.psi(j, s0 / 2) * (mp.mpf(1) / 2) ** j / 2 + mp.psi(j, (1 - s0) / 2) * (-mp.mpf(1) / 2) ** j / 2
        )
        if j == 0:
            value -= mp.log(mp.pi)
        out.append(value / mp.factorial(j))
    return out


def cauchy(a, b, n: int):
    return [sum(a[i] * b[j - i] for i in range(j + 1) if i < len(a) and j - i < len(b)) for j in range(n)]


def toy_taylor(s0, toy, n: int):
    out = [mp.mpc(1)] + [mp.mpc(0)] * n
    for gamma, exponent in toy:
        base = [(s0 - mp.mpf(1) / 2) ** 2 + mp.mpf(gamma) ** 2, 2 * (s0 - mp.mpf(1) / 2), mp.mpc(1)]
        for _ in range(exponent):
            out = cauchy(out, base, n + 1)
    return out


def f_taylor(s0, degree: int, toy=None):
    coefficients = [mp.zeta(s0, 1, j) / mp.factorial(j) for j in range(degree + 1)]
    if toy:
        coefficients = cauchy(coefficients, toy_taylor(s0, toy, degree), degree + 1)
    return coefficients


def levinson_parts(c, lam, q, L, beta):
    """V, chi V(1-s) (operator formula), E_beta and Vt at s0 from Taylor data of f and lambda."""
    degree = len(q) - 1
    v = sum(q[k] * (-1 / L) ** k * mp.factorial(k) * c[k] for k in range(degree + 1))
    u = list(c[: degree + 1])
    chi_v1 = q[0] * u[0]
    for k in range(1, degree + 1):
        m = len(u) - 1
        du = [(j + 1) * u[j + 1] for j in range(m)]
        lu = cauchy(lam, u, m)
        u = [du[j] + lu[j] for j in range(m)]
        chi_v1 += q[k] * L ** (-k) * u[0]
    e = beta * c[0] - v - chi_v1
    return v, chi_v1, e, v + e / 2


# ------------------------------------------------------------------------------------------
# 1. identities
# ------------------------------------------------------------------------------------------
def identity_rows(log) -> list[dict[str, object]]:
    mp.mp.dps = 30
    rows = []
    plan = [
        (10**4, ["Q1", "Q1bcy", "Q3", "Q5przz", "Q7con"]),
        (10**5, ["Q1", "Q3", "Q5przz"]),
        (10**6, ["Q1", "Q3"]),
    ]
    R = mp.mpf("1.3")
    for height, names in plan:
        T = mp.mpf(height)
        H = T ** mp.mpf("0.55")
        L = mp.log(T)
        L_shift = mp.log(T / (2 * mp.pi))
        sigma0 = mp.mpf(1) / 2 - R / L
        points = [T + mp.mpf("0.137"), T + H / 2 + mp.mpf("0.137"), T + H - mp.mpf("0.863")]
        for name in names:
            beta, q = get_q(name)
            degree = len(q) - 1
            for t in points:
                for sigma in (mp.mpf("0.5"), sigma0, mp.mpf("0.8")):
                    s = mp.mpc(sigma, t)
                    c = f_taylor(s, degree)
                    lam = lambda_taylor(s, max(degree, 1))
                    v, chi_v1, e, vt = levinson_parts(c, lam, q, L, beta)
                    direct = chi(s) * sum(
                        q[k] * (-1 / L) ** k * mp.zeta(1 - s, 1, k) for k in range(degree + 1)
                    )
                    _, _, e_shift, _ = levinson_parts(c, lam, q, L_shift, beta)
                    row = {
                        "T": height,
                        "Q": name,
                        "degree": degree,
                        "beta": float(beta),
                        "t": float(t),
                        "sigma": float(sigma),
                        "rel_operator_vs_direct": float(abs(chi_v1 - direct) / abs(direct)),
                        "abs_E_over_abs_V_L_logT": float(abs(e) / abs(v)),
                        "abs_E_over_abs_V_L_logT_over_2pi": float(abs(e_shift) / abs(v)),
                        "H_over_TL": float(H / (T * L)),
                    }
                    if sigma == mp.mpf("0.5"):
                        omega = mp.expj(mp.siegeltheta(t))
                        z = mp.siegelz(t)
                        row["im_omega_E_over_abs_E"] = float(abs(mp.im(omega * e)) / abs(e))
                        row["identity_residual"] = float(abs(beta * z - 2 * mp.re(omega * vt)) / abs(z))
                    rows.append(row)
            log(f"  identity T={height:g} {name}: rows={len(rows)}")
    return rows


# ------------------------------------------------------------------------------------------
# 2-3. counting lemma on zeta windows and toy functions
# ------------------------------------------------------------------------------------------
_CFG: dict[str, object] = {}


def init_worker(cfg: dict[str, object]) -> None:
    _CFG.clear()
    _CFG.update(cfg)
    mp.mp.dps = int(cfg["dps"])


def _setup():
    beta, q = get_q(str(_CFG["Q"]))
    return beta, q, mp.log(mp.mpf(_CFG["T"]))


def vt_at(s0, q, L, beta, toy):
    degree = len(q) - 1
    c = f_taylor(s0, degree, toy)
    lam = lambda_taylor(s0, max(degree, 1))
    _, _, _, vt = levinson_parts(c, lam, q, L, beta)
    return c[0], vt


def eval_line(t):
    """(W0, Z_f) on the critical line, W0 = e^{i vartheta} Vt / prod (t-t_j)^{k_j}."""
    beta, q, L = _setup()
    t = mp.mpf(t)
    f0, vt = vt_at(mp.mpc(0.5, t), q, L, beta, _CFG.get("toy"))
    omega = mp.expj(mp.siegeltheta(t))
    p = mp.mpf(1)
    for gamma, order in _CFG.get("online", []):
        p *= (t - mp.mpf(gamma)) ** order
    return complex(omega * vt / p), float(mp.re(omega * f0))


def eval_point(point):
    beta, q, L = _setup()
    _, vt = vt_at(mp.mpc(point[0], point[1]), q, L, beta, _CFG.get("toy"))
    return complex(vt)


def track(pool, func, point_of, u0, u1, n0, key, max_angle=0.25, max_rel=0.6, min_du=1e-10, rounds=40):
    """Continuous argument of key(func(point_of(u))) on [u0,u1] with adaptive refinement."""
    us = [u0 + (u1 - u0) * i / n0 for i in range(n0 + 1)]
    values = dict(zip(us, pool.map(func, [point_of(u) for u in us])))
    warned = False
    for _ in range(rounds):
        ordered = sorted(values)
        new = []
        for a, b in zip(ordered, ordered[1:]):
            va, vb = key(values[a]), key(values[b])
            if va == 0 or vb == 0:
                new.append((a + b) / 2)
                continue
            if abs(cmath.phase(vb / va)) > max_angle or abs(vb - va) / min(abs(va), abs(vb)) > max_rel:
                if b - a > min_du:
                    new.append((a + b) / 2)
                else:
                    warned = True
        if not new:
            break
        for u, value in zip(new, pool.map(func, [point_of(u) for u in new])):
            values[u] = value
    ordered = sorted(values)
    total = sum(cmath.phase(key(values[b]) / key(values[a])) for a, b in zip(ordered, ordered[1:]))
    return ordered, [values[u] for u in ordered], total, warned


def sign_changes(values) -> int:
    count, previous = 0, None
    for value in values:
        if value == 0:
            continue
        sign = 1 if value > 0 else -1
        if previous is not None and sign != previous:
            count += 1
        previous = sign
    return count


def run_case(label, T, H, name, toy=None, online=None, sigma1=3.0, dps=20, per_unit=8):
    started = time.time()
    cfg = {"T": T, "Q": name, "toy": toy, "online": online or [], "dps": dps}
    mp.mp.dps = dps
    with Pool(WORKERS, initializer=init_worker, initargs=(cfg,)) as pool:
        _, line_values, d_line, w_line = track(
            pool, eval_line, lambda u: u, T, T + H, int(H * per_unit), key=lambda v: v[0]
        )
        _, _, d_bottom, w_b = track(pool, eval_point, lambda u: (u, T), 0.5, sigma1, 30, key=lambda v: v)
        _, _, d_right, w_r = track(
            pool, eval_point, lambda u: (sigma1, u), T, T + H, max(20, int(2 * H)), key=lambda v: v
        )
        _, _, d_top_up, w_t = track(pool, eval_point, lambda u: (u, T + H), 0.5, sigma1, 30, key=lambda v: v)
    z_values = [v[1] for v in line_values]
    phases = [cmath.phase(line_values[0][0])]
    for a, b in zip(line_values, line_values[1:]):
        phases.append(phases[-1] + cmath.phase(b[0] / a[0]))
    crossings = 0
    for pa, pb in zip(phases, phases[1:]):
        lo, hi = min(pa, pb), max(pa, pb)
        crossings += max(
            0, math.floor((hi - math.pi / 2) / math.pi) - math.ceil((lo - math.pi / 2) / math.pi) + 1
        )
    sc = sign_changes(z_values)
    mp.mp.dps = 25
    d_theta = float(mp.siegeltheta(T + H) - mp.siegeltheta(T))
    n_zeta = int(mp.nzeros(T + H) - mp.nzeros(T))
    K = sum(order for _, order in (online or []))
    d_brt = d_bottom + d_right - d_top_up
    n_right_real = (d_theta + d_brt - math.pi * K - d_line) / (2 * math.pi)
    n_right = round(n_right_real)
    n_f = n_zeta + sum(e for _, e in (toy or []))
    distinct_odd = n_zeta - sum(1 for _, e in (toy or []) if e % 2 == 1)
    base = (d_theta + d_brt) / math.pi
    exact_rhs = base - 2 * (n_right + K) - 1
    strict_rhs = base - 2 * n_right - 1
    return {
        "label": label,
        "T": T,
        "H": H,
        "Q": name,
        "degree": len(get_q(name)[1]) - 1,
        "toy": toy,
        "online_zeros_of_Vt": online or [],
        "N_zeta": n_zeta,
        "N_f_with_multiplicity": n_f,
        "distinct_odd_critical_zeros": distinct_odd,
        "sign_changes_Z": sc,
        "level_crossings": crossings,
        "N_right_real": n_right_real,
        "N_right_integrality_error": abs(n_right_real - n_right),
        "K_online": K,
        "N_Vt": n_right + K,
        "lemma_finite_rhs": exact_rhs,
        "lemma_N_form_rhs": n_f - 2 * (n_right + K),
        "strict_variant_rhs": strict_rhs,
        "lemma_holds": sc >= exact_rhs - 1e-6 and sc >= n_f - 2 * (n_right + K),
        "strict_variant_holds": sc >= strict_rhs - 1e-6,
        "double_zeros_not_counted": sc == distinct_odd,
        "tracking_warnings": [w_line, w_b, w_r, w_t],
        "elapsed_seconds": round(time.time() - started, 1),
    }


def toy_zeros(T: float, H: float):
    mp.mp.dps = 25
    n0, n1 = int(mp.nzeros(T)), int(mp.nzeros(T + H))
    mp.mp.dps = 30
    gammas = [mp.nstr(mp.zetazero(n).imag, 28) for n in range(n0 + 1, n1 + 1)]
    doubles = [gammas[i] for i in range(1, len(gammas) - 1, 4)][:7]
    triples = [gammas[i] for i in range(3, len(gammas) - 1, 7)][:3]
    return doubles, triples


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--budget-seconds", type=float, default=MAX_SECONDS)
    args = parser.parse_args()
    if args.budget_seconds <= 0 or args.budget_seconds > MAX_SECONDS:
        raise ValueError(f"budget must be in (0, {MAX_SECONDS}]")
    out = args.output_dir
    if out.exists() and any(out.iterdir()):
        raise FileExistsError("output directory must be new or empty")
    out.mkdir(parents=True, exist_ok=True)
    started = time.time()
    lines: list[str] = []

    def log(message: str) -> None:
        line = f"[{time.time() - started:8.2f}s] {message}"
        lines.append(line)
        print(line, flush=True)
        if time.time() - started > args.budget_seconds:
            raise TimeoutError("budget exceeded")

    log("stage 1/3: exact identities")
    identities = identity_rows(log)
    log("stage 2/3: zeta windows")
    cases = []
    for T, H, names in ((1.0e4, 25.0, ["Q1", "Q3"]), (1.0e5, 10.0, ["Q1", "Q3"]), (1.0e6, 5.0, ["Q1", "Q3"])):
        for name in names:
            case = run_case(f"zeta T={T:g}", T, H, name)
            cases.append(case)
            log(
                f"  {case['label']} {name}: N={case['N_zeta']} sc={case['sign_changes_Z']} "
                f"crossings={case['level_crossings']} N_>={case['N_right_real']:.6f} lemma={case['lemma_holds']}"
            )
    log("stage 3/3: toy functions with planted multiple zeros")
    T, H = 1.0e4, 25.0
    doubles, triples = toy_zeros(T, H)
    toy_a, toy_b = [(g, 1) for g in doubles], [(g, 2) for g in triples]
    for label, toy, name, online in (
        ("toy A double zeros", toy_a, "Q1", [(g, 1) for g in doubles]),
        ("toy A double zeros", toy_a, "Q3", []),
        ("toy B triple zeros", toy_b, "Q1", [(g, 2) for g in triples]),
        ("toy B triple zeros", toy_b, "Q3", []),
    ):
        case = run_case(label, T, H, name, toy=toy, online=online)
        cases.append(case)
        log(
            f"  {label} {name}: N_f={case['N_f_with_multiplicity']} sc={case['sign_changes_Z']} "
            f"N-form={case['lemma_N_form_rhs']} strict={case['strict_variant_rhs']:.3f} "
            f"lemma={case['lemma_holds']} strict_holds={case['strict_variant_holds']}"
        )
    zeta_cases = [c for c in cases if c["toy"] is None]
    toy_cases = [c for c in cases if c["toy"] is not None]
    checks = {
        "operator_identity": max(r["rel_operator_vs_direct"] for r in identities) < 1e-18,
        "omega_E_real": max(r["im_omega_E_over_abs_E"] for r in identities if "im_omega_E_over_abs_E" in r)
        < 1e-12,
        "beta_Z_identity": max(r["identity_residual"] for r in identities if "identity_residual" in r)
        < 1e-18,
        "zeta_sign_changes_equal_crossings_and_N": all(
            c["sign_changes_Z"] == c["level_crossings"] == c["N_zeta"] for c in zeta_cases
        ),
        "lemma_holds_everywhere": all(c["lemma_holds"] for c in cases),
        "N_right_integral": all(c["N_right_integrality_error"] < 1e-6 for c in cases),
        "double_zeros_never_counted": all(c["double_zeros_not_counted"] for c in toy_cases),
        "strict_variant_fails_for_degree_one_toys": all(
            not c["strict_variant_holds"] for c in toy_cases if c["degree"] == 1
        ),
        "no_tracking_warnings": not any(any(c["tracking_warnings"]) for c in cases),
    }
    accepted = all(checks.values())
    result = {
        "experiment": "EXP-010",
        "schema": "exp010-controls-v1",
        "convention": "L = log T; Q(x)+Q(1-x)=beta; Vt = V + E_beta/2",
        "git": git_identity(),
        "controls_py_sha256": hashlib.sha256(Path(__file__).resolve().read_bytes()).hexdigest(),
        "mpmath": mp.__version__,
        "identities": identities,
        "cases": cases,
        "checks": checks,
        "accepted": accepted,
        "elapsed_seconds": round(time.time() - started, 1),
    }
    (out / "controls.json").write_text(
        json.dumps(result, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n"
    )
    log(f"checks={checks}")
    log(f"accepted={accepted}")
    (out / "stdout.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return 0 if accepted else 1


if __name__ == "__main__":
    sys.exit(main())
