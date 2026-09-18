"""EXP-015 derivation script: the k = 2, p = 2 quotient system, exactly.

Coordinates: bodies 1, 2 on the reflection axis (0, a1), (0, a2); pair A =
bodies 3, 4 at (u, v), (-u, v); pair B = bodies 5, 6 at (p, q), (-p, q).
Everything below is exact sympy; the printed facts are transcribed into the
2026-08-01 stratum dossier and cited by the hypothesis.
"""
import sympy as sp
from itertools import combinations

a1, a2, u, v, p, q = sp.symbols("a1 a2 u v p q", real=True)
m = sp.symbols("m1:7", positive=True)
POS = {1: (sp.Integer(0), a1), 2: (sp.Integer(0), a2),
       3: (u, v), 4: (-u, v), 5: (p, q), 6: (-p, q)}


def r2(i, j):
    (xi, yi), (xj, yj) = POS[i], POS[j]
    return sp.expand((xi - xj) ** 2 + (yi - yj) ** 2)


def Delta(i, j, k):
    (xi, yi), (xj, yj), (xk, yk) = POS[i], POS[j], POS[k]
    return sp.expand(sp.Matrix([[1, 1, 1], [xi, xj, xk], [yi, yj, yk]]).det())


R = {(i, j): sp.sqrt(r2(i, j)) for i, j in combinations(range(1, 7), 2)}


def rr(i, j):
    return R[(min(i, j), max(i, j))]


def s(i, k, j):
    return rr(i, k) ** -3 - rr(j, k) ** -3


def L(i, j):
    return sum(m[k - 1] * s(i, k, j) * Delta(i, j, k)
               for k in range(1, 7) if k not in (i, j))


def main():
    print("== distance identities (all must be 0) ==")
    for lhs, rhs, tag in [((1, 3), (1, 4), "r13=r14"), ((1, 5), (1, 6), "r15=r16"),
                          ((2, 3), (2, 4), "r23=r24"), ((2, 5), (2, 6), "r25=r26"),
                          ((3, 5), (4, 6), "r35=r46"), ((3, 6), (4, 5), "r36=r45")]:
        print(f"  {tag}: {sp.expand(r2(*lhs) - r2(*rhs))}")
    print("== shape relation (u, p > 0): r36^2 - r35^2 - r34*r56 ==")
    print("  ", sp.expand(r2(3, 6) - r2(3, 5) - (2 * u) * (2 * p)))

    print("== pair-equality lemma ==")
    r35c, r36c = rr(3, 5), rr(3, 6)
    target34 = -2 * u * (m[4] - m[5]) * (q - v) * (r36c ** 3 - r35c ** 3) / (r35c ** 3 * r36c ** 3)
    target56 = 2 * p * (m[2] - m[3]) * (q - v) * (r36c ** 3 - r35c ** 3) / (r35c ** 3 * r36c ** 3)
    print("  L34 - closed form:", sp.simplify(L(3, 4) - target34))
    print("  L56 - closed form:", sp.simplify(L(5, 6) - target56))
    print("  (both zero: L34 and L56 factor exactly as stated; on the open")
    print("   stratum u, p != 0, q != v, r35 != r36 they force m5 = m6, m3 = m4;")
    print("   the q = v sub-stratum is NOT covered by these two equations)")

    print("== q = v sub-stratum probe: which L force pair equality there? ==")
    sub = {q: v}
    forced = []
    for i, j in combinations(range(1, 7), 2):
        val = sp.simplify(sp.expand(L(i, j)).subs(sub))
        d34 = sp.simplify(sp.diff(val, m[2]) + sp.diff(val, m[3]))
        has34 = sp.simplify(sp.diff(val, m[2]) - sp.diff(val, m[3]))
        has56 = sp.simplify(sp.diff(val, m[4]) - sp.diff(val, m[5]))
        if has34 != 0 or has56 != 0:
            forced.append(((i, j), has34 != 0, has56 != 0))
    print("  L_ij with antisymmetric mass dependence at q = v:",
          [(ij, a, b) for ij, a, b in forced])

    print("== the reduced Laura-Andoyer block at pair-equal masses ==")
    eq_masses = {m[3]: m[2], m[5]: m[4]}
    zero, pairs, nontrivial = [], [], []
    vals = {}
    for i, j in combinations(range(1, 7), 2):
        val = sp.simplify(sp.expand(L(i, j)).subs(eq_masses))
        vals[(i, j)] = val
        if val == 0:
            zero.append((i, j))
    seen = set()
    for k1 in vals:
        if k1 in seen or vals[k1] == 0:
            continue
        group = [k1]
        for k2 in vals:
            if k2 <= k1 or k2 in seen or vals[k2] == 0:
                continue
            d = sp.simplify(vals[k1] - vals[k2])
            sm = sp.simplify(vals[k1] + vals[k2])
            if d == 0 or sm == 0:
                group.append(k2)
                seen.add(k2)
        seen.add(k1)
        nontrivial.append(group)
    print("  identically zero L_ij:", zero)
    print("  equivalence groups (equal or opposite):", nontrivial)
    print("  independent equation count:", len(nontrivial))
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
