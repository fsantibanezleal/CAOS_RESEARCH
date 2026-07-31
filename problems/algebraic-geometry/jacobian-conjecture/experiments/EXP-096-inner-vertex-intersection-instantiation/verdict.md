# EXP-096: Seven inner vertices and exact intersection number 21

## Result

The exact source instantiation passed. It produces two independent necessary
conditions for every original polynomial Keller pair in the GGHV open chain.

### Inner-vertex restriction

For the degree-72 component, the Lee--Li parameters are

\[
(a,b,m,n)=(2,3,16,56),\qquad
\mathfrak m=\frac{139}{39}.
\]

If its inner or innermost polynomial is nonzero, its northeastern vertex is one
of exactly seven points:

\[
(1,3),(2,7),(3,10),(4,14),(5,17),(6,21),(7,24).
\]

The three diagonal candidates are
\((2,7),(4,14),(6,21)\); the other four are off the diagonal. The stronger
Lee--Li diagonal corollary does not apply:

\[
\frac ba=\frac32\not> \frac{n-m}{a}-1=19.
\]

The alternative that the inner or innermost polynomial is zero remains
allowed.

### Exact intersection invariant

The open complete chain has

\[
(m,n)=(3,2),\quad A_1=(11/4,7),\quad k=1,\quad l=4.
\]

The forced fourth-power edge gives four final major approximate-root classes.
For each class, Proposition 3.21 gives

\[
|D_\tau^P|=mb=3\cdot7=21,\qquad
\lambda_\tau^Q=\frac{k}{l}=\frac14.
\]

Theorem 3.15 then gives

\[
I(P,Q)
=\deg_x\operatorname{Res}_y(P,Q)
=4\cdot21\cdot\frac14
=21.
\]

The four major classes account for \(84\) roots of the degree-108 component.
The remaining \(24=3\cdot8\) roots are minor, giving the exact partition

\[
108=84+24.
\]

## Adversarial validation

- The Lee--Li lattice region was enumerated with exact rational inequalities.
- A diagonal point passed; points above the diagonal, below the narrow strip,
  and on the excluded height boundary failed.
- The approximate-root calculation reproduced the paper's published F1
  smallest-member control \(I=9\).
- Major and minor root counts sum exactly to \(108\).
- The relevant theorem and worked-example pages were visually checked in both
  primary PDFs after the TeX formulas were inspected.

The artifact is `artifacts/results.json`, SHA-256
`C6CBBC8197B64CD0C999444B81762CF9127C085F2C1CCEAB8F55C7005FE0529E`.

## Verdict and scope

**CONFIRMED:** every original polynomial pair in the open chain must pass both
of these gates:

1. a nonzero inner vertex belongs to the seven-point set above;
2. \(\deg_x\operatorname{Res}_y(P,Q)=21\), with root partition \(84+24\).

These restrictions are not consequences of sampling the 51 reduced
coefficients. They come from the original Keller-pair structure and therefore
provide independent validation targets for any reconstruction.

They do not exclude the chain by themselves, prove any of the seven vertices
realizable, construct a counterexample, or raise the planar degree floor.

## Route decision

The approximate-root paper explicitly obtains only an inequality for its
minor-root formula, not the equality that would have discarded the targeted
infinite families. That exclusion route is retired unless a new proof repairs
the inequality.

The exact major-root formula remains valuable as the intersection-\(21\)
rejection gate. The next constructive question is whether the GGHV
original-to-Laurent transformation can express this resultant valuation or the
seven inner-vertex alternatives directly in the 51 reduced coefficients. If
that transport is not explicit at low cost, proceed to the small
certificate-module/chart-cover experiment while retaining these gates for
candidate reconstruction.

## How could this be wrong?

- The intersection calculation uses the verified open-chain data
  \(A_1=(11/4,7)\), \(k=1\), \(l=4\), and component factor \(m=3\).
- It uses four distinct major classes from the forced fourth-power edge over
  an algebraically closed characteristic-zero field.
- Lee--Li applies after polynomial rectangularization of the original pair,
  not to the final Laurent normalization. Transporting the inner polynomial
  itself to the 51 reduced parameters remains separate work.

