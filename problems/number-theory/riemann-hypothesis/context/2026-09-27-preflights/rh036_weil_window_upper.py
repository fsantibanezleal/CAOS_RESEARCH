"""RH-036 bounded replay: Galerkin upper bound for Zhu's window infimum lambda*(L) (exploratory).

Zhu, arXiv:2608.24827v2, eqs. (2)-(3) and Lemma 2.5: for supp f in [-L, L], g = f * f~,
    Q(f) = 2 F(i/2)^2 + A(g) - sum_{log n < 2L} (2 Lambda(n)/sqrt(n)) g(log n),
    A(g) = -(gamma + log pi + log(1 - e^(-4L))) g(0) + int_0^{2L} 2[e^(-2x) g(0) - e^(-x/2) g(x)]/(1 - e^(-2x)) dx,
with F(i/2) = int f(x) e^(-x/2) dx. The minimum eigenvalue of Q on the span of the first N even
Legendre modes, orthonormalized in L^2[-L, L], is a variational upper bound for lambda*(L)
(geometric side only, no zeros, no RH). High working precision is essential: Zhu documents
spurious negative eigenvalues in float64. This replay is multiprecision, not interval-certified.

Target (Zhu): 8.9e-18 <= lambda*(0.8) <= 2.27e-17.
"""

from __future__ import annotations

import sys

import mpmath as mp
import sympy as sp


def run(n_modes: int = 16, l_num: int = 4, l_den: int = 5, dps: int = 80) -> None:
    mp.mp.dps = dps
    y, x = sp.symbols("y x")
    L = sp.Rational(l_num, l_den)
    basis = []
    for k in range(n_modes):
        p = sp.legendre(2 * k, y / L)
        norm = sp.sqrt(sp.Rational(4 * k + 1, 2) / L)  # orthonormal on [-L, L]
        basis.append(sp.expand(p * norm))
    Lm = mp.mpf(l_num) / l_den
    # g_ij(x) on [0, 2L]: int_{x-L}^{L} f_i(t) f_j(t - x) dt, a polynomial in x
    g = {}
    for i in range(n_modes):
        for j in range(i, n_modes):
            expr = sp.integrate(sp.expand(basis[i] * basis[j].subs(y, y - x)), (y, x - L, L))
            g[(i, j)] = sp.Poly(sp.expand(expr), x)
    fhalf = []
    for i in range(n_modes):
        poly = sp.Poly(basis[i], y)
        coeffs = [mp.mpf(str(sp.N(c, dps + 20))) for c in poly.all_coeffs()]
        fhalf.append(mp.quad(lambda t, c=coeffs: mp.polyval(c, t) * mp.exp(-t / 2), [-Lm, 0, Lm]))
    primes = [(2, mp.log(2)), (3, mp.log(3)), (4, mp.log(2)), (5, mp.log(5)), (7, mp.log(7)), (8, mp.log(2)), (9, mp.log(3))]
    primes = [(n, lam) for n, lam in primes if mp.log(n) < 2 * Lm]
    const = -(mp.euler + mp.log(mp.pi) + mp.log(1 - mp.exp(-4 * Lm)))
    M = mp.matrix(n_modes, n_modes)
    for (i, j), poly in g.items():
        c = [mp.mpf(str(sp.N(a, dps + 20))) for a in poly.all_coeffs()]

        def gx(t, c=c):
            return mp.polyval(c, t)

        g0 = gx(mp.mpf(0))
        arch = const * g0 + mp.quad(lambda t: 2 * (mp.exp(-2 * t) * g0 - mp.exp(-t / 2) * gx(t)) / (1 - mp.exp(-2 * t)), [0, Lm, 2 * Lm])
        prime = sum(2 * lam / mp.sqrt(n) * gx(mp.log(n)) for n, lam in primes)
        val = 2 * fhalf[i] * fhalf[j] + arch - prime
        M[i, j] = M[j, i] = val
    ev = mp.eigsy(M, eigvals_only=True)
    ev = sorted(ev)
    print(f"L={l_num}/{l_den} N={n_modes} dps={dps}: lambda_min={mp.nstr(ev[0], 6)} lambda_2={mp.nstr(ev[1], 6)}")


if __name__ == "__main__":
    run(int(sys.argv[1]) if len(sys.argv) > 1 else 16)
