"""EXP-080 Stage A: invariant gate for the proposed sl2 closure.

This intentionally stops before matrix commutators unless the declared common
grading is well-defined. It uses only exact integer support arithmetic and
reconstructs the active EXP-071 perturbation operators.
"""

from math import comb


def hull_points(vertices):
    def cross(origin, point, query):
        return (
            (point[0] - origin[0]) * (query[1] - origin[1])
            - (point[1] - origin[1]) * (query[0] - origin[0])
        )

    points = sorted(set(vertices))
    lower = []
    for point in points:
        while (
            len(lower) >= 2
            and cross(lower[-2], lower[-1], point) <= 0
        ):
            lower.pop()
        lower.append(point)
    upper = []
    for point in reversed(points):
        while (
            len(upper) >= 2
            and cross(upper[-2], upper[-1], point) <= 0
        ):
            upper.pop()
        upper.append(point)
    hull = lower[:-1] + upper[:-1]

    def inside(query):
        return all(
            cross(hull[index], hull[(index + 1) % len(hull)], query) >= 0
            for index in range(len(hull))
        )

    max_x = max(x for x, _ in vertices)
    max_y = max(y for _, y in vertices)
    return [
        (x, y)
        for x in range(max_x + 1)
        for y in range(max_y + 1)
        if inside((x, y))
    ]


def in_pool(exponent):
    x, y = exponent
    return x - y <= 2 and x <= 24 and y <= 44


def bracket_is_active(p_exponent, q_support):
    p, q = p_exponent
    for alpha, beta in q_support:
        coefficient = p * beta - q * alpha
        output = (p + alpha - 1, q + beta - 1)
        if coefficient != 0 and in_pool(output):
            return True
    return False


def weight(exponent, grading):
    return exponent[0] * grading[0] + exponent[1] * grading[1]


def shift(exponent, grading):
    """Weight shift of J(x^p y^q, .) on the monomial window."""
    return weight((exponent[0] - 1, exponent[1] - 1), grading)


def print_check(label, result, detail):
    status = "PASS" if result else "REFUTED"
    print(f"[{status}] {label}: {detail}", flush=True)


np_vertices = [(0, 0), (1, 0), (8, 14), (8, 16), (0, 8)]
nq_vertices = [(0, 0), (2, 1), (12, 21), (12, 24), (0, 12)]
np_points = hull_points(np_vertices)
nq_points = sorted(hull_points(nq_vertices))
top_edge = {(k, 8 + k) for k in range(9)}
lower_support = [
    exponent
    for exponent in np_points
    if exponent not in top_edge and exponent != (0, 0)
]
active_operators = [
    exponent
    for exponent in lower_support
    if bracket_is_active(exponent, nq_points)
]

pt = {
    (k, 8 + k): comb(8, k) * (-1) ** (8 - k)
    for k in range(9)
}
pt[(1, 0)] = 1
pt_support = sorted(pt)

print("EXP-080 Stage A - exact invariant gate", flush=True)
print_check(
    "EXP-071 active-operator reconstruction",
    len(active_operators) == 51,
    f"{len(active_operators)} active lower monomials (expected 51)",
)

# Homogeneity equations from (1,9)-(0,8) and (1,0)-(0,8):
#     a + b = 0, a - 8b = 0.
# Their determinant is -9, so only the zero grading exists.
homogeneity_matrix = ((1, 1), (1, -8))
homogeneity_determinant = (
    homogeneity_matrix[0][0] * homogeneity_matrix[1][1]
    - homogeneity_matrix[0][1] * homogeneity_matrix[1][0]
)
nonzero_full_grading_exists = homogeneity_determinant == 0
print_check(
    "nonzero monomial grading for the full forced P_T",
    nonzero_full_grading_exists,
    (
        "difference equations have determinant "
        f"{homogeneity_determinant}; only grading (0,0) is possible"
    ),
)

edge_grading = (1, -1)
edge_degrees = sorted({weight(exponent, edge_grading) for exponent in top_edge})
full_edge_degrees = sorted(
    {weight(exponent, edge_grading) for exponent in pt_support}
)
print(
    "[EXACT] edge-normal grading (1,-1): "
    f"top-edge degrees={edge_degrees}; full-P_T degrees={full_edge_degrees}",
    flush=True,
)

candidate_gradings = {
    (u, v): (v, 1 - u)
    for u, v in sorted(top_edge)
}
print(
    "[EXACT] the nine top monomials select "
    f"{len(set(candidate_gradings.values()))} distinct (v,1-u) gradings",
    flush=True,
)

all_sign_groupings_mixed = True
for exponent, grading in candidate_gradings.items():
    pt_degrees = sorted({weight(term, grading) for term in pt_support})
    shifts = sorted({shift(term, grading) for term in active_operators})
    positive = [value for value in shifts if value > 0]
    negative = [value for value in shifts if value < 0]
    mixed = len(positive) > 1 or len(negative) > 1
    all_sign_groupings_mixed = all_sign_groupings_mixed and mixed
    print(
        "[CANDIDATE] "
        f"(u,v)={exponent}, h={grading}: "
        f"P_T degrees={len(pt_degrees)}, raw shifts={len(shifts)}, "
        f"positive classes={len(positive)}, negative classes={len(negative)}",
        flush=True,
    )

canonical_edge_shifts = sorted(
    {shift(term, edge_grading) for term in active_operators}
)
print(
    "[EXACT] edge-normal raw operator shifts: "
    f"{canonical_edge_shifts}",
    flush=True,
)
print_check(
    "sign grouping defines single-degree raising/lowering operators",
    not all_sign_groupings_mixed,
    "every vertex-derived candidate mixes multiple nonzero raw shift classes",
)

stage_a_pass = (
    nonzero_full_grading_exists
    and len(set(candidate_gradings.values())) == 1
    and not all_sign_groupings_mixed
)
print(
    "[DECISION] STAGE_A="
    f"{'PASS' if stage_a_pass else 'FAIL'}; "
    "STAGE_B="
    f"{'UNLOCKED' if stage_a_pass else 'NOT_RUN'}",
    flush=True,
)
if not stage_a_pass:
    print(
        "[SCOPE] The declared natural h,e,f triple is not well-defined. "
        "No claim is made against other chosen gradings, other right-inverse "
        "gauges, larger Lie algebras, or JC(2).",
        flush=True,
    )
