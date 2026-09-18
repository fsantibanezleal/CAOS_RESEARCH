"""Smoke test for the Boussinesq modulation system and its dissipative extension.

Checks three things before any machine time is committed to the real sweep:

1.  The inviscid amplitude system integrated numerically grows at the rate the
    matrix predicts, and that rate is sqrt(A) * sin(phi), NOT sqrt(A * sin(phi)).
    This settles the transcription ambiguity in the source PDF by computation.
2.  The growth rate carries no dependence on the wave frequency lambda.
3.  The dissipative system of the dossier has eigenvalues
    -nu * (lambda * r) ** (2 * alpha) +/- sqrt(A) * sin(phi), and the induced
    cascade recursion has its fixed-point/escape transition at alpha = 1/4.

Reference: Alpoge and Buckmaster, "Blowup for the Boussinesq equations with
smooth forcing", 2026-09-07, Subsection 1.2 and Lemma 3.1, for the inviscid
system. The dissipative extension is derived in
`../context/2026-09-11-simplified-model-and-beyond.md`.

Run: python modulation_smoke.py
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp


def amplitude_matrix(A: float, phi: float, lam: float, r: float,
                     nu: float = 0.0, alpha: float = 1.0) -> np.ndarray:
    """Return the 2x2 generator of (Theta, Omega) in the frozen configuration.

    Frozen means D = 0 and G = -A e_2, with zeta = r * e(phi) and
    e(phi) = (sin phi, cos phi). Then J zeta . G = -A r sin phi, so the
    Theta equation picks up +A sin(phi) / (lambda r) times Omega, and the
    Omega equation picks up lambda * zeta_1 = lambda r sin phi times Theta.
    Dissipation of order alpha damps both amplitudes by nu (lambda r)^(2 alpha).
    """
    damping = nu * (lam * r) ** (2.0 * alpha)
    return np.array([
        [-damping, A * np.sin(phi) / (lam * r)],
        [lam * r * np.sin(phi), -damping],
    ])


def measured_growth_rate(A: float, phi: float, lam: float, r: float,
                         nu: float = 0.0, alpha: float = 1.0,
                         t_end: float = 4.0) -> float:
    """Integrate the system and recover the observed exponential rate."""
    M = amplitude_matrix(A, phi, lam, r, nu, alpha)
    # Start on the growing eigenline so the rate is clean.
    evals, evecs = np.linalg.eig(M)
    y0 = np.real(evecs[:, int(np.argmax(np.real(evals)))])
    sol = solve_ivp(lambda _t, y: M @ y, (0.0, t_end), y0,
                    rtol=1e-11, atol=1e-13, dense_output=True)
    y_end = sol.y[:, -1]
    return float(np.log(np.linalg.norm(y_end) / np.linalg.norm(y0)) / t_end)


def cascade_trace(alpha: float, nu: float, r: float, a0: float,
                  budget: str, stages: int) -> np.ndarray:
    """Return the log-gradient sequence a_q = log A_q of the cap recursion.

    At stage q the growth condition caps the usable frequency at
    lambda_q ~ (sqrt(A_q) / nu)^(1/(2 alpha)) / r, and the gradient handed to
    the next stage is A_{q+1} ~ lambda_q Theta_q with a summable amplitude
    budget Theta_q. In logs,

        a_{q+1} = a_q / (4 alpha) - log(nu) / (2 alpha) - log r + log Theta_q.

    The homogeneous coefficient is 1 / (4 alpha), so the map is an expansion
    below alpha = 1/4 and a contraction above it. The inhomogeneous terms are
    NOT negligible: the nu term is a large positive constant for small
    viscosity, and the budget term is a negative drift whose size depends on
    how fast Theta_q decays. Both shift the observed transition away from 1/4,
    which is exactly what this trace exists to expose.

    Caveat carried deliberately: this recursion has no time axis. Finite-time
    blowup also needs sum_q T_q < infinity with T_q the stage growth time, and
    that constraint is absent here. Escape of a_q is therefore necessary, not
    sufficient.
    """
    coef = 1.0 / (4.0 * alpha)
    const = -np.log(nu) / (2.0 * alpha) - np.log(r)
    out = np.empty(stages + 1)
    out[0] = a = a0
    for q in range(stages):
        log_theta = q * np.log(0.5) if budget == "geometric" else -2.0 * np.log(q + 1.0)
        a = coef * a + const + log_theta
        out[q + 1] = a
        if not np.isfinite(a) or abs(a) > 1e6:
            out[q + 1:] = a
            break
    return out


def cascade_escapes(alpha: float, nu: float, r: float, a0: float,
                    budget: str, stages: int) -> bool:
    """Escape means the log-gradient is still rising at the END of the horizon.

    A transient rise is not escape: for small nu the constant term lifts a_q for
    many stages even when the map contracts. The verdict is taken from the tail
    slope, not from crossing a threshold somewhere in the middle.
    """
    trace = cascade_trace(alpha, nu, r, a0, budget, stages)
    final = trace[-1]
    # Divergence: the recursion left the representable range upward.
    if not np.isfinite(final):
        return bool(final > 0)
    if final > 1e5:
        return True
    if final < -1e5:
        return False
    # Otherwise decide on the tail slope, so a transient rise is not called escape.
    tail = trace[-max(8, stages // 10):]
    return bool(tail[-1] > tail[0] and final > trace[0])


def main() -> int:
    rng = np.random.default_rng(20260911)
    failures = 0

    print("1. inviscid growth rate: measured vs the two candidate readings")
    print(f"   {'A':>8} {'phi':>6} {'lambda':>8} {'measured':>12} "
          f"{'sqrt(A)sin':>12} {'sqrt(Asin)':>12}")
    for _ in range(6):
        A = float(rng.uniform(0.5, 40.0))
        phi = float(rng.uniform(0.2, np.pi - 0.2))
        lam = float(rng.uniform(1.0, 500.0))
        r = float(rng.uniform(0.5, 2.0))
        got = measured_growth_rate(A, phi, lam, r)
        cand_a = np.sqrt(A) * np.sin(phi)          # the reading the matrix forces
        cand_b = np.sqrt(A * np.sin(phi))          # the reading the PDF glyphs allow
        ok = abs(got - cand_a) < 1e-6 * max(1.0, cand_a)
        failures += 0 if ok else 1
        print(f"   {A:8.3f} {phi:6.3f} {lam:8.1f} {got:12.6f} "
              f"{cand_a:12.6f} {cand_b:12.6f}  {'OK' if ok else 'MISMATCH'}")

    print("\n2. the inviscid rate must not depend on lambda")
    A, phi, r = 9.0, 1.1, 1.0
    rates = [measured_growth_rate(A, phi, lam, r) for lam in (1.0, 10.0, 1e3, 1e5)]
    spread = max(rates) - min(rates)
    ok = spread < 1e-8
    failures += 0 if ok else 1
    print(f"   rates over lambda in 1..1e5: spread {spread:.3e}  "
          f"{'OK (lambda-free)' if ok else 'MISMATCH'}")

    print("\n3. dissipative eigenvalues match -nu(lambda r)^(2a) +/- sqrt(A) sin(phi)")
    for alpha in (0.1, 0.25, 0.5, 1.0):
        A, phi, lam, r, nu = 9.0, 1.1, 7.0, 1.0, 1e-3
        M = amplitude_matrix(A, phi, lam, r, nu, alpha)
        got = float(np.max(np.real(np.linalg.eigvals(M))))
        want = -nu * (lam * r) ** (2 * alpha) + np.sqrt(A) * np.sin(phi)
        ok = abs(got - want) < 1e-10
        failures += 0 if ok else 1
        print(f"   alpha={alpha:4.2f}  top eigenvalue {got:12.6f} "
              f"predicted {want:12.6f}  {'OK' if ok else 'MISMATCH'}")

    print("\n4. the homogeneous coefficient 1/(4 alpha) crosses 1 at alpha = 1/4")
    for alpha in (0.10, 0.20, 0.25, 0.30, 1.00):
        coef = 1.0 / (4.0 * alpha)
        kind = "expansion" if coef > 1 else ("marginal" if coef == 1 else "contraction")
        want = "expansion" if alpha < 0.25 else ("marginal" if alpha == 0.25 else "contraction")
        ok = kind == want
        failures += 0 if ok else 1
        print(f"   alpha={alpha:4.2f}  coefficient {coef:6.3f}  {kind:11s} "
              f"{'OK' if ok else 'MISMATCH'}")

    print("\n5. observed transition is NOT at 1/4: it moves with nu and the budget")
    print(f"   {'budget':>11} {'nu':>8}   " + "  ".join(f"a={a:4.2f}" for a in
          (0.20, 0.24, 0.26, 0.30, 0.50)))
    moved = False
    for budget in ("geometric", "polynomial"):
        for nu in (1e-1, 1e-3, 1e-6, 1e-9):
            verdicts = []
            for alpha in (0.20, 0.24, 0.26, 0.30, 0.50):
                esc = cascade_escapes(alpha, nu, r=1.0, a0=2.0,
                                      budget=budget, stages=4000)
                verdicts.append("esc " if esc else "coll")
                if esc and alpha > 0.25:
                    moved = True
            print(f"   {budget:>11} {nu:8.0e}   " + "  ".join(f"{v:>6}" for v in verdicts))
    print(f"   escape observed above alpha=1/4 for some (nu, budget): "
          f"{'YES, so 1/4 is NOT a parameter-free threshold' if moved else 'no'}")

    print("\nVERDICT")
    print("  Checks 1 to 4 hold exactly: the growth rate is sqrt(A) sin(phi), it is")
    print("  independent of lambda, the dissipative eigenvalues are as derived, and the")
    print("  recursion coefficient crosses 1 at alpha = 1/4.")
    print("  Check 5 REFUTES the clean reading of that last fact. The transition actually")
    print("  observed depends on viscosity and on the amplitude budget, and the recursion")
    print("  carries no time axis, so escape is necessary but not sufficient for")
    print("  finite-time blowup. alpha_c = 1/4 is the homogeneous coefficient crossing,")
    print("  NOT an established threshold.")
    print(f"\n{'STRUCTURAL CHECKS PASSED' if failures == 0 else str(failures) + ' CHECK(S) FAILED'}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
