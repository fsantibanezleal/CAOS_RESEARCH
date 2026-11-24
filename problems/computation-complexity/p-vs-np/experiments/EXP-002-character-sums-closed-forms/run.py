"""EXP-002: the closed forms of the character sums used in the note on Hilbert-space maps, against exhaustive counts.

For mu = 2, 3, 4 and B = diag(1^j, 0), j = 1..mu:
  p_1(j)  = fraction of rank-one W with <B, W> = 1; closed form 2^(2 mu - 1) (1 - 2^-j) / (2^mu - 1)^2
  S(j)    = sum over invertible W of (-1)^<B, W>;   closed form (-1)^j 2^(j(j-1)/2 + j(mu-j)) |GL_(mu-j)(F_2)|
  p_mu(j) = (1 - S(j)/|GL_mu|)/2;                    closed form (1 - (-1)^j / prod_{i<j} (2^(mu-i) - 1))/2
and the inequality p_mu(j)/p_1(j) <= 2 - 2^(1-mu) with equality only at j = 1.
The closed forms alone are then evaluated for mu up to 40 to check the inequality in exact arithmetic.
Usage: python -I run.py
"""
import sys
from fractions import Fraction


def rank_f2(rows):
    rows = list(rows)
    r = 0
    top = max(rows).bit_length() if rows and max(rows) else 0
    for bit in range(top):
        piv = next((i for i in range(r, len(rows)) if rows[i] >> bit & 1), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i] >> bit & 1:
                rows[i] ^= rows[r]
        r += 1
    return r


def gl_order(m):
    out = 1
    for i in range(m):
        out *= 2 ** m - 2 ** i
    return out


def closed(mu, j):
    p1 = Fraction(2 ** (2 * mu - 1) * (2 ** j - 1), 2 ** j * (2 ** mu - 1) ** 2)
    s = (-1) ** j * 2 ** (j * (j - 1) // 2 + j * (mu - j)) * gl_order(mu - j)
    prod = 1
    for i in range(j):
        prod *= 2 ** (mu - i) - 1
    pmu = (1 - Fraction((-1) ** j, prod)) / 2
    return p1, s, pmu


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ok = True
    for mu in (2, 3, 4):
        n = mu * mu
        rk = [rank_f2([(m >> (mu * i)) & ((1 << mu) - 1) for i in range(mu)]) for m in range(1 << n)]
        n1, nmu = rk.count(1), rk.count(mu)
        assert nmu == gl_order(mu)
        for j in range(1, mu + 1):
            B = sum(1 << (mu * i + i) for i in range(j))
            ones1 = sum(1 for m in range(1 << n) if rk[m] == 1 and bin(m & B).count("1") & 1)
            onesmu = sum(1 for m in range(1 << n) if rk[m] == mu and bin(m & B).count("1") & 1)
            p1, s, pmu = closed(mu, j)
            good = (Fraction(ones1, n1) == p1 and nmu - 2 * onesmu == s and Fraction(onesmu, nmu) == pmu
                    and (1 - Fraction(s, nmu)) / 2 == pmu)
            ok &= good
            print(f"mu={mu} j={j}: counted p_1={Fraction(ones1, n1)} S={nmu - 2 * onesmu} p_mu={Fraction(onesmu, nmu)}; "
                  f"closed p_1={p1} S={s} p_mu={pmu}; agree={good}")
    worst = None
    for mu in range(2, 41):
        top = Fraction(2 ** mu - 1, 2 ** (mu - 1))
        ratios = [closed(mu, j)[2] / closed(mu, j)[0] for j in range(1, mu + 1)]
        good = ratios[0] == top and all(r < top for r in ratios[1:])
        ok &= good
        gap = top - max(ratios[1:])
        worst = gap if worst is None or gap < worst else worst
        if mu <= 6 or not good:
            print(f"mu={mu}: ratio at j=1 is {ratios[0]} = 2 - 2^(1-mu): {ratios[0] == top}; "
                  f"largest ratio at j>=2: {float(max(ratios[1:])):.6f}; inequality strict: {good}")
    print(f"closed forms, mu = 2..40: inequality holds with equality only at j = 1: {ok}; smallest gap {float(worst):.6f}")
    print("ALL CHECKS PASS" if ok else "A CHECK FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
