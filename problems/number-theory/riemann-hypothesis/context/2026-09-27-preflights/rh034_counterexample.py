"""RH-034 counterexample to Q >= 2N + 3O - 4S for the Montgomery-Taylor window (40-digit check).

Window: eta^2 proportional to cos(sqrt2 u) on (-1/2, 1/2), K = (eta^2)^, K(0) = 1, in closed form
K(xi) = [sin((b-c)a)/(b-c) + sin((b+c)a)/(b+c)] / (2 sin(ab)/b), a = 1/2, b = sqrt2, c = 2 pi xi.
Configuration: six real triples and one simple conjugate pair (S = 0, O = 6, N = 20).
"""

from __future__ import annotations

import mpmath as mp

mp.mp.dps = 40
A = mp.mpf(1) / 2
B = mp.sqrt(2)
NORM = 2 * mp.sin(B * A) / B


def kernel(xi):
    c = 2 * mp.pi * xi

    def term(d):
        return A if abs(d) < mp.mpf("1e-30") else mp.sin(d * A) / d

    return (term(B - c) + term(B + c)) / NORM


REALS = ["0.949374", "1.9925", "3.03254", "-0.949373", "-1.9925", "-3.03254"]
Y = "0.24556"


def main() -> None:
    pts = [mp.mpc(mp.mpf(x)) for x in REALS] + [mp.mpc(0, mp.mpf(Y)), mp.mpc(0, -mp.mpf(Y))]
    mult = [3] * len(REALS) + [1, 1]
    q = mp.re(mp.fsum(mult[i] * mult[j] * kernel(pts[i] - pts[j]) ** 2 for i in range(len(pts)) for j in range(len(pts))))
    n, o, s = sum(mult), len(REALS), 0
    print(f"N={n} O={o} S={s} Q={mp.nstr(q, 20)} 2N+3O-4S={2 * n + 3 * o - 4 * s} slack={mp.nstr(q - (2 * n + 3 * o - 4 * s), 12)}")
    print(f"EXP-006 product check: (Q-S)(N-O)={mp.nstr((q - s) * (n - o), 15)} >= 2(N-S)^2={2 * (n - s) ** 2}")


if __name__ == "__main__":
    main()
