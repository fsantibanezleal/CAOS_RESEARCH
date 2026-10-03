# Height-weighted cycle bridge: finite obstruction preflight

Recorded before the exact control calculation, 2026-10-03. This is an
integrity preflight for an alternative route, not a new zero proportion or
a reason to stop EXP-020. It does not establish mathematical priority.

## The input mismatch

Rudnick and Sarnak, *Zeros of principal L-functions and random matrix theory*,
Theorem 3.1, equations (3.3)--(3.9), supplies smoothed all-index correlations
with entire height functions and total Fourier support below two for zeta.
Theorem 3.2 explicitly assumes RH for the corresponding unsmoothed sums.
The theorem pages 284--285 were inspected in the original PDF, not inferred
from OCR alone. The PDF is pinned in source-manifest-exp020-followups.json.

The finite signed-vector counting theorem uses integer multiplicities and
conjugate-pair contributions of common normalized mass. Multiplying each
pair by a different smooth height weight changes this premise. Analytic
correlation constants cannot simply be inserted into the unweighted count.

## Proposed discriminating example

Take an orthonormal basis e1,e2 and two normalized signed pairs:

    g1 = sqrt(5)/2 e1,   h1 = 1/2 e2,
    g2 = sqrt(2) e2,     h2 = e1.

Each g is orthogonal to its corresponding h and has squared norm difference
one. There are no simple real vectors. Give these two pairs positive weights
w1=1 and w2=1/2. Then

    A = 2 w1 (g1 g1^T - h1 h1^T)
        + 2 w2 (g2 g2^T - h2 h2^T) = (3/2) I.

The weighted trace mass is Nw=2(w1+w2)=3; tr(A^2)=9/2. Thus the proposed
naive lower bound s >= 2Nw-tr(A^2) would assert 0 >= 3/2, which is false.
Even replacing the first moment by squared weights fails: Nw2=2(w1^2+w2^2)
=5/2, so 2Nw2-tr(A^2)=1/2>0. Any weighted simple count is still zero.

For general w1>w2>0, choose b>0, c=(w1*b+(w1-w2)/2)/w2 and pairs with
squared norms (1+b,b), (1+c,c) in the same two orthogonal directions.
The weighted operator is (w1+w2)I; the squared-weight residual is exactly
2(w1-w2)^2. The obstruction is structural rather than a rounding effect.

## Control and consequence

Check the norm differences, orthogonality, weighted operator, both residuals
and their strict signs with exact SymPy expressions. Restore equal weights
as a negative control: its squared-weight residual is zero. Alter one pair's
normalization as a deliberately invalid case and require its premise to fail.
The test must retain these distinctions and never label the example as zeta
zeros or as a counterexample to Rudnick--Sarnak or Lamzouri.

A viable cycle route needs either a matched hard-height moment theorem or
a new counting theorem that retains varying height weights throughout.
The proposed quartic and mixed-observer routes remain open under their stated
analytic obligations. A finite obstruction here warrants no new manuscript
or Zenodo deposit; the stronger distinct-strip certificate remains in flight.
