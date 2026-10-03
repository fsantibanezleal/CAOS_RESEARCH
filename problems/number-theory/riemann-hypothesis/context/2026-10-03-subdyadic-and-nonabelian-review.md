# Subdyadic support and non-abelian completion eligibility

This review continues RH-038's signed-moment investigation. It establishes
conversion requirements rather than a new moment estimate. Primary bytes and
content eligibility are in `source-manifest-20261003-subdyadic.json`.

## Withdrawn lead

The earlier September sweep mentioned arXiv:2601.00292 from search snippets.
The primary [v2 withdrawal notice](https://arxiv.org/abs/2601.00292v2), dated
5 January 2026, identifies a missing factor L^2 in equation (2.53). Its
authors state that the corrected argument supplies no claimed improvement.
The v1 improved saving and mollifier length are ineligible inputs. The
older sweep remains a historical search record with an explicit correction.
This is an author-reported withdrawal, distinct from the limited displayed
exponent inconsistency identified in the Das--Pujahari review.

## Short supports: preserve the support graph

[Wright, arXiv:2608.27732v1](https://arxiv.org/abs/2608.27732v1), Theorem 2.1,
bounds trilinear inverse-fraction sums when both variable supports lie in
intervals, or consecutive elements of a congruence class, of relative length
at most X^-eta. In addition to the unsaved A^(1/2) term, its A^(7/20) term
has a factor X^(-2eta/5). The norms are the actual restricted l2 norms.
Theorem 2.2 adds real coefficients, divisor bounds and a Siegel--Walfisz
hypothesis inherited from Theorem 1.1; it is not an arbitrary complex
short-window zeta theorem. Sections 2 and 3 were read from PDF and HTML,
including the amplifier and squarefree-removal reductions. The underlying
Bettin--Chandee proof was checked at its statement and outline; a complete
independent validation of all its estimates is not claimed.

There is a useful support-accounting criterion before trying to import a
short-support gain. Split two dyadic sequences into K=X^eta disjoint
intervals. Write u_b and v_c for the l2 norms of their restrictions. Suppose
the retained pairs of intervals form a bipartite support graph with maximum
row degree d_L and column degree d_R. Its adjacency matrix A satisfies

    sum_(b,c retained) u_b v_c
      <= ||A||_2 ||u||_2 ||v||_2
      <= sqrt(d_L*d_R) ||alpha||_2 ||beta||_2.

For the last inequality, Cauchy--Schwarz gives
sum_b (sum_c A_bc v_c)^2 <= d_L sum_c (sum_b A_bc) v_c^2
<= d_L*d_R ||v||_2^2. This is a classical operator-norm calculation.
If the graph has bounded degrees, summing the restricted bound keeps its
X^(-2eta/5) gain in the second term. If every pair is retained, the graph
norm is K and the same operation costs X^(3eta/5) in that term. Cutting
both variables into short intervals alone therefore supplies no gain.
The A^(1/2) term must also be below the desired error; it receives no
X^(-2eta/5) saving from this statement.

The Gaussian representation in EXP-024 concentrates H0*n/K0 near
T/(2*pi), with controlled tails, before the Estermann transformation.
The compact-window superposition widens the effective band to order H.
This is weighted concentration rather than exact support. That geometric
constraint suggests bounded-degree interval pairs for fixed n. However,
the required inverse-fraction variables occur after the transformation,
whose new weight and n-dependence must be derived first. No proof yet
shows that the useful support graph survives that transformation or that
coefficient norms and separation costs fit the moment budget. This is
the next conversion obligation, not a numerical replacement for it.

## Non-abelian analysis: Fourier completion has a cost

[Pascadi, arXiv:2511.08445v2](https://arxiv.org/abs/2511.08445v2) develops
non-abelian Fourier analysis on SL2 over a fixed composite modulus. The
[published version](https://doi.org/10.1007/s00039-026-00746-0) appeared on
21 August 2026. Its Theorems 1.1--1.2 bound bilinear Kloosterman sums with
both lengths about the square root of the modulus. A particularly useful
saving occurs for balanced two-prime moduli. These are complete
Kloosterman sums, not the inverse-fraction sum with a varying denominator.
The statement and strategy were reviewed; the full 54-page arXiv proof
has not been independently revalidated here.

With S(a,b;c)=sum_(x unit mod c) e((a*x^-1+b*x)/c), finite character
orthogonality gives the exact bridge

    e(a*m^-1/c) = (1/c) sum_(b mod c) S(a,b;c)e(-b*m/c),
    for gcd(m,c)=1.

Indeed the inner sum in b vanishes unless x=m modulo c. For a coefficient
sequence alpha supported on an interval, this completion replaces alpha
by its full discrete Fourier transform. Parseval gives
sum_b |alpha_hat(b)|^2 = c*sum_m |alpha(m)|^2, after viewing alpha as a
sequence on residues. Arbitrary coefficients have no established
concentration on a short frequency interval. If the original interval
spans multiple residue periods, folding coefficients onto residues has
an additional norm cost that must be controlled. Splitting all c frequencies
into about sqrt(c) intervals and using triangle/Cauchy--Schwarz can lose
c^(1/4), already larger than the stated generic c^(-1/700) saving.
Therefore completion alone does not import the non-abelian bound.
An additional frequency-localization or modulus-average argument is
required, together with all gcd restrictions and normalization factors.

The publisher download returned a Client Challenge HTML response, despite
HTTP success. That byte archive is explicitly ineligible mathematical
content; the arXiv v2 PDF/HTML supply the archived primary text. Search
results and document titles are not counted as proof verification.

## Consequence for the active work

These two routes connect support geometry and representation theory to the
signed arithmetic family. They identify testable analytic obligations but
prove no new cancellation, short-window onset or zero proportion. Neither
the withdrawal correction nor the classical support-norm argument triggers
a separate manuscript. The complete local cover remains the independent
EXP-023 gate; the global Riemann hypothesis remains open.
