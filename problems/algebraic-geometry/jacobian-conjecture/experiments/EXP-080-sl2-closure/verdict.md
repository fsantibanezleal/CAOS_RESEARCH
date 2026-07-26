# EXP-080 - Verdict: the declared natural `sl2` triple is not well-defined

**Status: Stage-A premise REFUTED by exact invariant checks; Stage B NOT RUN.**

The experiment reached its declared either-way outcome without assembling matrix
commutators. The exact support gate in `run.py` completed in under one second;
its persisted output is `artifacts/output-2026-07-25.txt`.

## Exact results

1. **[MV, PASS]** The EXP-071 geometry was reconstructed exactly: there are 51
   active lower-monomial operators.
2. **[MV, REFUTED]** No nonzero monomial weight makes the full forced polynomial
   \[
   P_T=y^8(xy-1)^8+x
   \]
   homogeneous. Comparing the support points \((0,8),(1,9),(1,0)\) gives
   \(a+b=0\) and \(a-8b=0\); the coefficient determinant is \(-9\), so only
   \((a,b)=(0,0)\) works.
3. **[MV, REFUTED]** The phrase "\(h\) the \((v,1-u)\) weight" does not choose one
   grading on the nine-monomial edge. Its monomials
   \((u,v)=(k,8+k)\), \(0\leq k\leq8\), produce nine distinct candidates.
4. **[MV, REFUTED]** Grouping the 51 raw \(T_i\) by the sign of their shift does
   not produce single-degree raising and lowering operators. Every one of the
   nine vertex-derived candidate gradings mixes multiple positive or negative
   shift classes. Even the canonical edge-normal grading \((1,-1)\) gives raw
   shifts \(-7,-6,\ldots,1\), while \(P_T\) itself has degrees \(-8\) and \(1\).

## Why the bracket stage was stopped

For a grading operator \(h\), the relation \([h,e]=2e\) requires \(e\) to have one
degree (after an overall normalization); similarly \(f\) must have one opposite
degree. A sum of every positive-shift \(T_i\) is not such an operator. More
importantly, the operators proposed in the original declaration are
\(A_i=\sigma T_i\), not the raw \(T_i\). EXP-064's pivot right inverse \(\sigma\)
has a 165-dimensional gauge freedom and has never been shown to preserve any
grading. Raw shift labels therefore cannot simply be transferred to the pinned
\(A_i\).

Choosing a corner, a shift class, and a gauge after seeing this failure would
create a different experiment. The preflight correctly blocks that move.

## Scope of the null

This result refutes the **declared natural construction** and its premise that the
window already carries a canonical common weight. It does not prove:

- that no selected homogeneous subquotient admits an `sl2` action;
- that no other right-inverse gauge preserves a chosen grading;
- that no larger Lie algebra acts after additional choices; or
- anything against the Jacobian conjecture in dimension two.

A sound successor would first specify one grading, construct or prove a
grading-compatible right inverse, and select \(e\) and \(f\) from single shift
classes. Only then are exact commutators a meaningful test. This route is demoted;
the constructive full degree-3 covector solve (EXP-093) remains the primary next
action.
