# EXP-013 - Verdict: FULL SYSTEM CAPPED, MENU CONFIRMED AT DIM <= 5, AND THE PRODUCTS IDEAL'S EXACT DIMENSION IS 5 (2026-08-01; the entire n = 5 question is now localized to one algebraic event: whether Cayley-Menger cuts the top components)

Hypothesis: `hypothesis.md` (declared before any run). Runner: `run.py`.
Artifacts: `artifacts/` (all Singular scripts and outputs including the
COMPLETE Groebner basis of the products ideal, menu union leads, results,
run log).

## Outcomes against the declared predictions

| Prediction | Outcome | Facts |
|---|---|---|
| P1 (full-system grevlex basis at 600 s) | INCONCLUSIVE-CAP | 659 s wall at the 600 s inner cap; the fallback was declared and ran |
| P2 (growth menu pushes the union bound to <= 5) | CONFIRMED, d_pgb = 5 | 11 of 26 subideals completed; 4615 distinct leading monomials; independent set {r12, r13, r14, r15, r45}; the bound improves from EXP-012's 7 to 5 |
| P3 (cost cartography) | RECORDED, and sharp | every subideal WITHOUT Cayley-Menger completed in 1-9 s (all ten double-locals at about 600-670 leads each; the all-fifteen-products system in NINE seconds with a complete basis of 2436 leading monomials); every subideal WITH Cayley-Menger capped at 120 s (all five local+CM, all ten pair+CM). The hard direction is not the products, it is mixing them with CM |

## The analysis the completed basis makes exact

The all-fifteen-products run is not a subideal harvest: it is a COMPLETE
reduced grevlex Groebner basis of the products ideal (with the Rabinowitsch
saturation) over QQ. Its staircase dimension is therefore the TRUE Krull
dimension, not a bound:

    dim ( V(all 15 Dziobek products) intersect torus ) = 5, exactly,
    with maximal independent set {r12, r13, r14, r15, r45}.

This matches the parametrization count on the nondegenerate stratum (ten
distances constrained by S_ij = z_i z_j with five z-parameters: codimension
five), and it is consistent with the degenerate-strata inventory in the
EXP-011 hypothesis (patterns explored there reached dimension at most 3).

Consequence: the n = 5 spatial Dziobek cut (products AND Cayley-Menger)
satisfies 4 <= expected, and our confirmed bound is now dim <= 5 with the
whole remaining gap localized in ONE question: does Cayley-Menger vanish
identically on any top (5-dimensional) component of the products variety? If
it does not (the generic expectation), the cut has dimension exactly 4 on
those components and the lane's central quantity at n = 5 is decided. This is
a single incremental computation away: Singular can extend the COMPLETED
products basis by the one CM polynomial (std(S, cm)), which is typically far
cheaper than the from-scratch full system that capped as P1. That attempt is
EXP-014 territory, hypothesis first.

## Soundness notes

- All leading monomials are Singular-over-QQ grevlex with short=0 output;
  the parser was validated by EXP-012's controls two hours earlier on the
  same binaries.
- The exact-dimension claim for the products ideal uses the completeness of
  its basis (a terminated std() run), not the union-bound logic; the menu
  bound d_pgb = 5 is separately valid by the subideal argument.
- Caps enforced by timeout inside WSL; wall overshoots are WSL overhead.

## Consequences

1. EXP-014 (declared next): the incremental cut. Feed Singular the completed
   products basis and adjoin Cayley-Menger; if it terminates, read the exact
   dimension of the full cut with the same two-way agreement rule as here.
   Secondary rung: interreduce and inspect whether CM reduces to zero against
   the products basis (it must NOT, or the cut equals the products variety,
   which the EXP-011 smoke gate already refutes: the 4-simplex is on the
   products variety and off the cut).
2. The strata campaign inherits the cost law: quotient systems should keep
   CM-type realizability equations OUT of the Groebner core where possible
   and adjoin them incrementally.
3. CCB-034 witness sets remain the lower-bound route; nothing here changes
   that.
