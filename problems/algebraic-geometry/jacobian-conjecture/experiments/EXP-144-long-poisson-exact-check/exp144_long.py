"""Transcription of Long's polynomials (arXiv:2608.23777v1, equations (12)-(19)) and the bracket.

Bracket convention: equation (8), page 3: {f, g} = f_p g_x - f_x g_p + f_z g_q - f_q g_z, so {p, x} = {z, q} = 1.
Generator order (x, q, p, z). Source SHA-256 is checked by run.py, not here.
"""
from sympy import Rational as Q, symbols, expand, diff, Poly

x, q, p, z = symbols("x q p z")
GENS = (x, q, p, z)

# (12), (13)
a = 1 - 3 * x * q
B = 3 * x**2 * p + 2 * a * z
beta = expand(B - 9 * q**2)
y = expand(q - x * beta / 3)
u = expand(x * y)

# (14), (15), (16)
R = expand(2 * x - 3 * x**2 * y - x**3 * beta)
S = expand(y + 3 * x * (1 + u) ** 2 * beta + 3 * x * y**2 * (4 + 3 * u))
T = expand(-Q(1, 2) * ((1 + u) ** 3 * beta + y**2 * (1 + u) * (4 + 3 * u)))

# (17), (18), (19)
D0 = expand((1 + 3 * x * q) / 2 * p - 3 * q**2 * z)


def hamiltonian(c125=125):
    return expand(
        y**4 / 20 * (18 * u**2 + 78 * u + c125)
        + 3 * beta * y**2 / 10 * (u**3 + 5 * u**2 + 10 * u - 5)
        - beta**2 / 6 * (9 * u + 2)
        - x**2 * beta**3 / 6
    )


H = hamiltonian()
D = expand(D0 + H)
D_C2 = expand(D0 + hamiltonian(126))  # control C2: constant 125 -> 126


def D0_poly_as_D():
    """Control C1: the uncorrected D0 of (17) in the place of D."""
    return D0


def bracket(f, g):
    return expand(diff(f, p) * diff(g, x) - diff(f, x) * diff(g, p) + diff(f, z) * diff(g, q) - diff(f, q) * diff(g, z))


def bracket_matrix(F):
    return [[bracket(F[i], F[j]) for j in range(4)] for i in range(4)]


def target_matrix():
    return [[bracket(GENS[i], GENS[j]) for j in range(4)] for i in range(4)]


def poisson_symbolic(Rr, Tt, Dd, Ss):
    """Return (ok, mismatches): bracket matrix of (R,T,D,S) vs that of (x,q,p,z)."""
    F = (Rr, Tt, Dd, Ss)
    got, want = bracket_matrix(F), target_matrix()
    bad = [(i, j, got[i][j]) for i in range(4) for j in range(4) if expand(got[i][j] - want[i][j]) != 0]
    return (len(bad) == 0), bad


SIZE_TABLE = {  # printed under (19), page 5: name -> (terms, total degree)
    "beta": (4, 3), "y": (5, 4), "R": (2, 3), "S": (22, 11), "T": (47, 15), "H": (137, 23), "D": (139, 23),
}


def sizes():
    exprs = {"beta": beta, "y": y, "R": R, "S": S, "T": T, "H": H, "D": D}
    out = {}
    for k, e in exprs.items():
        P = Poly(e, *GENS)
        out[k] = (len(P.terms()), P.total_degree())
    return out
