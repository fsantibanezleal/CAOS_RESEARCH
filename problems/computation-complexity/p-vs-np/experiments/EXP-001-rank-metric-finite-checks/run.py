"""PNP-001 checks: finite facts about the rank metric on Mat_mu(F_2) used in the note on the two cases.

Exact integer arithmetic only. For mu in the given list:
  (1) For a Hilbert-space-valued map F on Mat_mu(F_2) the quadratic forms D(r)^2 (mean of |F(a) - F(a+W)|^2 over a and
      W of rank r) are diagonal in the characters chi_B(W) = (-1)^<B,W>; the largest value of D(mu)^2 / D(1)^2 is the
      maximum over B != 0 of p_mu(B) / p_1(B), with p_r(B) the fraction of rank-r matrices W with <B,W> = 1.
  (2) rank is not of negative type (so sqrt(rank) is not a Euclidean metric): some B has sum_W rank(W) chi_B(W) > 0.
  (3) The rank-one matrices transversal to a fixed rank-one matrix span Mat_mu(F_2); the rank-one summands of a
      full-rank V (those W with rank(V - W) = mu - 1) span Mat_mu(F_2).
  (4) The maximal cliques of the rank-distance-1 graph through 0 (mu = 2 only): sizes and number.
Usage: python -I pnp001_rank_metric_checks.py 2 3 4
"""
import itertools
import sys
from fractions import Fraction


def rank_f2(rows):
    rows = list(rows)
    r = 0
    for bit in range(max(rows).bit_length() if rows and max(rows) else 0):
        piv = next((i for i in range(r, len(rows)) if rows[i] >> bit & 1), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i] >> bit & 1:
                rows[i] ^= rows[r]
        r += 1
    return r


def span_dim(vectors):
    return rank_f2(vectors) if vectors else 0


def main(mus):
    for mu in mus:
        n = mu * mu
        mats = range(1 << n)
        rows_of = lambda m: [(m >> (mu * i)) & ((1 << mu) - 1) for i in range(mu)]
        rk = [rank_f2(rows_of(m)) for m in mats]
        count = [rk.count(r) for r in range(mu + 1)]
        print(f"mu={mu}: matrices by rank {count}")
        # (1) and (2): characters B = diag(1^j, 0), one representative per rank j (the forms are GL x GL invariant)
        best = None
        for j in range(1, mu + 1):
            B = sum(1 << (mu * i + i) for i in range(j))
            ones = [0] * (mu + 1)
            for m in mats:
                if bin(m & B).count("1") & 1:
                    ones[rk[m]] += 1
            p = [Fraction(ones[r], count[r]) for r in range(mu + 1)]
            ratio = p[mu] / p[1]
            fourier = sum(r * (count[r] - 2 * ones[r]) for r in range(mu + 1))
            print(f"  rank(B)={j}: p_1={p[1]} p_mu={p[mu]} ratio p_mu/p_1={ratio} = {float(ratio):.4f}; "
                  f"sum rank*chi_B = {fourier}")
            best = ratio if best is None or ratio > best else best
        print(f"  (1) max over B of D(mu)^2/D(1)^2 for Hilbert-valued maps = {best} = {float(best):.4f}; mu = {mu}")
        # (3) spanning
        rank1 = [m for m in mats if rk[m] == 1]
        W = 1  # E_11
        transversal = [x for x in rank1 if rk[x ^ W] == 2]
        V = sum(1 << (mu * i + i) for i in range(mu))  # identity
        summands = [x for x in rank1 if rk[x ^ V] == mu - 1]
        print(f"  (3) rank-one matrices transversal to E11: {len(transversal)}, span dimension {span_dim(transversal)} of {n}; "
              f"rank-one summands of I: {len(summands)}, span dimension {span_dim(summands)} of {n}")
        # (4) cliques through 0 for mu = 2
        if mu == 2:
            maximal = []
            for size in range(len(rank1), 0, -1):
                for c in itertools.combinations(rank1, size):
                    if all(rk[x ^ y] == 1 for x, y in itertools.combinations(c, 2)):
                        if not any(set(c) < set(big) for big in maximal):
                            maximal.append(c)
            print(f"  (4) maximal cliques through 0: sizes {sorted(len(c) + 1 for c in maximal)} (with 0), count {len(maximal)}")
            pairs = [(x, y) for x, y in itertools.combinations(rank1, 2) if rk[x ^ y] == 2]
            tri = sum(1 for x, y, z in itertools.combinations(rank1, 3)
                      if rk[x ^ y] == 2 and rk[x ^ z] == 2 and rk[y ^ z] == 2)
            print(f"      transversal pairs of rank-one matrices: {len(pairs)}; pairwise transversal triples: {tri}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main([int(x) for x in sys.argv[1:]] or [2, 3])


def extra(mus):
    """(5) the invertible matrices span Mat_mu(F_2); the transversality graph on rank-one matrices is connected and
    contains a triangle; (6) the closed form 2 - 2^(1-mu) for the rank-one character ratio."""
    for mu in mus:
        n = mu * mu
        rows_of = lambda m: [(m >> (mu * i)) & ((1 << mu) - 1) for i in range(mu)]
        rk = [rank_f2(rows_of(m)) for m in range(1 << n)]
        inv = [m for m in range(1 << n) if rk[m] == mu]
        rank1 = [m for m in range(1 << n) if rk[m] == 1]
        adj = {x: [y for y in rank1 if rk[x ^ y] == 2] for x in rank1}
        seen, stack = {rank1[0]}, [rank1[0]]
        while stack:
            for y in adj[stack.pop()]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        triangle = any(z in adj[y] for x in rank1 for y in adj[x] for z in adj[x] if y < z)
        closed = Fraction(2 ** mu - 1, 2 ** (mu - 1))
        print(f"mu={mu}: (5) invertible matrices: {len(inv)}, span dimension {span_dim(inv)} of {n}; transversality "
              f"graph on {len(rank1)} rank-one matrices: connected={len(seen) == len(rank1)}, has a triangle={triangle}; "
              f"(6) 2 - 2^(1-mu) = {closed}")


if __name__ == "__main__":
    extra([int(x) for x in sys.argv[1:]] or [2, 3])
