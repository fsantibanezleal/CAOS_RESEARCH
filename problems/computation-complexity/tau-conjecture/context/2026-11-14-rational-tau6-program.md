# The six-gate program of the tau = 6 rational record

Round of 2026-11-14 (census manuscript v0.07). The rational ladder note
(`2026-08-25-rational-ladder.md`) states the tau = 6 rational record

    8x^6 - 10x^4 + 2x^2 = 2x^2 (x-1)(x+1)(2x-1)(2x+1)

and `scripts/rational_census.py` prints its coefficient tuple as the rational witness of the
depth-6 run, but no record stores the straight-line program that computes it. The literal
`(0, 0, 2, 0, -10, 0, 8)` is held by `scripts/audit_paper_claims.py` (section "The rational record
at tau = 6"). This note stores the program and its replay.

## The program

Inputs {-1, 1, x}; six gates.

    g1 = x * x          = x^2
    g2 = g1 + g1        = 2x^2
    g3 = g2 - 1         = 2x^2 - 1
    g4 = g3 * g3        = 4x^4 - 4x^2 + 1
    g5 = g4 - g1        = 4x^4 - 5x^2 + 1
    g6 = g2 * g5        = 8x^6 - 10x^4 + 2x^2

It was found by algebra (the doubled square 2x^2 is one gate and carries both the factor 2x^2 and
the half-integer roots through g3), not by reading a record, then replayed.

## Replay

Script: `scripts/replay_rational_tau6.py` (tclib exact integer polynomial arithmetic; rational
roots by the rational root theorem over Z with `fractions.Fraction`, no floating point). Command,
run from the repository root with the CAOS_RESEARCH virtual environment:

    <CAOS_RESEARCH>/.venv/Scripts/python.exe problems/computation-complexity/tau-conjecture/scripts/replay_rational_tau6.py

Output (exit status 0):

    gates: 6
    g1 = x * x   -> x^2   coefficients (0, 0, 1)
    g2 = g1 + g1  -> 2*x^2   coefficients (0, 0, 2)
    g3 = g2 - 1   -> 2*x^2 - 1   coefficients (-1, 0, 2)
    g4 = g3 * g3  -> 4*x^4 - 4*x^2 + 1   coefficients (1, 0, -4, 0, 4)
    g5 = g4 - g1  -> 4*x^4 - 5*x^2 + 1   coefficients (1, 0, -5, 0, 4)
    g6 = g2 * g5  -> 8*x^6 - 10*x^4 + 2*x^2   coefficients (0, 0, 2, 0, -10, 0, 8)
    polynomial (constant term first): (0, 0, 2, 0, -10, 0, 8)
    polynomial: 8*x^6 - 10*x^4 + 2*x^2
    integer roots (3): [-1, 0, 1]
    rational roots (5): ['-1', '-1/2', '0', '1/2', '1']
    record literal in scripts/audit_paper_claims.py: (0, 0, 2, 0, -10, 0, 8)
    ok   program has 6 gates
    ok   program polynomial equals the record literal
    ok   program polynomial equals 2x^2(x-1)(x+1)(2x-1)(2x+1) expanded
    ok   context note carries the record formula
    ok   integer roots are [-1, 0, 1]
    ok   rational roots are 0, +-1/2, +-1
    replay: ok

## What the replay shows and what it does not

It shows that the six-gate program computes exactly the record polynomial, so tau(record) <= 6, and
that the record has five distinct rational roots and three distinct integer roots, as the ladder
note states. It does not show tau(record) >= 6, and it does not show that no polynomial with
tau <= 6 has more than five rational roots: both are the classification of the rational census
(`rational_census.py`: exhaustive through tau = 6, depth 6 by the last-gate lemma, gated by
reproducing the integer maximum zmax(6) = 5 on the same 134,494-polynomial set). The paper's [MV]
mark on the program refers to this replay; its mark on the ladder refers to the census.
