"""Arb positive LDL and unconstrained quadratic lower enclosure, EXP-020."""

from flint import arb


def positive_ldl(matrix):
    n = len(matrix)
    if not n or any(len(row) != n for row in matrix):
        raise ValueError("nonempty square matrix required")
    lower = [[arb(0) for _ in range(n)] for _ in range(n)]
    diagonal = [arb(0) for _ in range(n)]
    for column in range(n):
        lower[column][column] = arb(1)
        pivot = matrix[column][column]
        for previous in range(column):
            pivot -= lower[column][previous]*lower[column][previous]*diagonal[previous]
        if not pivot > 0:
            return None
        diagonal[column] = pivot
        for row in range(column+1, n):
            entry = matrix[row][column]
            for previous in range(column):
                entry -= lower[row][previous]*lower[column][previous]*diagonal[previous]
            lower[row][column] = entry/pivot
    return lower, diagonal


def quadratic_lower(value, gradient, decomposition):
    lower, diagonal = decomposition
    n = len(gradient)
    if len(diagonal) != n or any(not p > 0 for p in diagonal):
        raise ValueError("positive factorization of matching dimension required")
    # If H=L D L^T, g^T H^-1 g = (L^-1 g)^T D^-1 (L^-1 g).
    solved = []
    loss = arb(0)
    for row in range(n):
        component = gradient[row]
        for previous in range(row):
            component -= lower[row][previous]*solved[previous]
        solved.append(component)
        loss += component*component/diagonal[row]
    return value-loss/2
