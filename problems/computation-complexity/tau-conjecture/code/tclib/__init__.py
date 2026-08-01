"""tclib: exact tooling for the tau-conjecture program.

Constant-free SLP enumeration over Z[x] (inputs {-1, 1, x}) and over Z
(input {1}, Markstroem's setting), exact integer-root counting, and 2-adic
valuation spectra. Pure standard library; exact integer arithmetic only.
"""

from .enum import (
    INPUTS,
    P_MINUS1,
    P_ONE,
    P_X,
    census_polynomials,
    census_integers,
    divisors,
    integer_roots,
    padd,
    peval,
    pmul,
    psub,
    two_adic_valuations,
)

__all__ = [
    "INPUTS",
    "P_MINUS1",
    "P_ONE",
    "P_X",
    "census_polynomials",
    "census_integers",
    "divisors",
    "integer_roots",
    "padd",
    "peval",
    "pmul",
    "psub",
    "two_adic_valuations",
]
