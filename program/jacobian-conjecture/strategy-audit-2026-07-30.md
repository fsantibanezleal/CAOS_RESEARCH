# Jacobian strategy audit after EXP-125

Date: 2026-07-30. This audit supersedes only the route ranking in the
2026-07-29 audit. All exact results and scope limits remain unchanged.

## Current bottleneck

EXP-124/125 reduce the selected EXP-123 graph residual to:

- positive-dimensional curves \(F_6=0\) and \(F_7=0\);
- 24 normalized principal-open values on \(F_3=0\), with 72 algebraic lifts;
- the finite base locus \(V(R,S)\);
- the separate boundary \(A=0\).

The full four-parameter restriction, 24-parameter core, 51-parameter family,
\((72,108)\), degree floor, and \(JC(2)\) remain open.

## Ranked routes

| Rank | Route | Proof value now | Cost and gate | Decision |
|---|---|---|---|---|
| P0 | Determinantal divisor on \(F_6\), then \(F_7\) | exact dense-open cover plus finite residual on an actual GGHV stratum | bounded SCC determinant plus quadratic/septic quotient arithmetic | run EXP-126 |
| P0-control | Multi-minor quotient gcd / Fitting atlas | can close a curve if several divisor sections have no common zero | reuse persisted bases; no ambient elimination | use if one divisor leaves a difficult finite set |
| P1 | Algebraic point charts for the finite \(F_3\) and base-locus schemes | exact closure of already zero-dimensional strata | bounded field extensions or resultants | run after positive-dimensional curves |
| P1 | Separate \(A=0\) boundary quotient | required for complete four-parameter coverage | new rank stratification; must not be folded into \(AS\ne0\) | run after graph strata |
| P2-conditional | Boundary-divisor reconstruction of intersection 21 | could transport an original-pair invariant | requires the complete swap/localization/inversion ledger | reopen only if graph recursion stalls |
| P3-hold | Newton resolution and Lee-Li generator/inner-vertex route | constrains original Keller pairs | no direct reduced-coefficient equation is typed | wait for a new proved restriction or transport |
| P3-hold | Jelonek/non-properness and bounded-degree component geometry | global conceptual organization | no map from the bracket-\(x^2\) reduced family to the required original-map space | wait for applicability bridge |
| retired | more coefficient slices or generic ambient Groebner bases | cannot close the complete family efficiently | high cost and weak scope | do not run |

## Why the divisor view is stronger than another raw determinant

A maximal minor is not treated as an isolated polynomial. Restricted to an
irreducible residual curve, it is a section whose nonzero class removes a
dense open and whose norm records a finite zero divisor. This provides:

1. a binary exact gate before elimination: zero or nonzero in the quotient;
2. a canonical univariate residual through the function-field norm;
3. a way to combine charts through gcds of divisor norms;
4. a finite endpoint at which algebraic point charts replace symbolic curve
   computation.

## EXP-126 decision tree

1. Reconstruct the persisted cross-prime \(F_6\) row basis exactly.
2. Stop if its largest cyclic block exceeds 60 or the worker reaches 300
   seconds.
3. Restrict its determinant to the EXP-123 graph with the exact denominator
   power recorded.
4. Reduce the numerator modulo \(F_6\) as \(U(B)X+V(B)\).
5. If the remainder is zero, refute this basis and choose another persisted
   \(F_6\) basis.
6. If nonzero, compute the norm by a Sylvester resultant and independently
   by multiplication in the quadratic quotient.
7. Separate roots belonging to \(A=0\), \(S=0\), singular projection values,
   or the EXP-123 base locus only with exact same-point ideal tests.
8. Persist the remaining finite divisor without claiming those points
   covered.

## Exploration result

The 2026-07-30 primary-source refresh found no current theorem that bypasses
the missing applicability bridges. The new deliverable is the
maximal-minor-ideal / curve-section / divisor-norm dictionary above. It
changes the object being accumulated from a list of determinant
factorizations to a finite divisor ledger on each residual curve.

