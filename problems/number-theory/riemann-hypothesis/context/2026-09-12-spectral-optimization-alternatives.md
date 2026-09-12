# Full-operator spectral witnesses and alternatives to gap-energy optimization

Review date: 2026-09-12. Status: source review, finite paper deductions, and a
proposed preflight. No new numerical search, spectral experiment, or prime-side
computation was performed for this dossier. EXP-003 has its own completed
[arithmetic records](../experiments/EXP-003-odd-frame-pressure/artifacts/result.json)
and [proof](../experiments/EXP-003-odd-frame-pressure/mathematical-proof.md).

The most concrete alternative is to retain the negative spectrum of the **full
zero operator**, and use semidefinite dual witnesses or higher-moment localizing
matrices to measure it. This sees off-line points that the simple-zero Gram
matrix omits. An exact finite strengthening is derived below. It does not yet
improve a zeta-zero proportion: the missing step is an unconditional arithmetic
estimate for the new observable. A small-displacement example explains why a
uniform gain per off-line pair cannot follow from linear algebra alone.

This direction connects the existing inertia proof to quantum-information
witnesses, truncated moment problems, and sampling theory. These connections
are methodological. The zero operator is not asserted to be a quantum state,
and no quantum speedup or new Hilbert–Pólya realization is claimed.

## 1. Established sources and their boundaries

| Primary source and inspected part | Content relevant here | Boundary |
|---|---|---|
| [Lamzouri, 2609.02882v2](https://arxiv.org/pdf/2609.02882v2), finite Hilbert argument; [Ainta, pinned paper](https://github.com/ainta/zeta-simple-zeros/blob/040c5e899e658aed7b56a2a87f501798fe10761d/paper/riemann.tex), lines 131–174 | Exact conjugation-symmetric operator; stability with the simple-real Gram defect | Ainta's displayed lemma eliminates the perturbation's negative part during minimization. It does not state the full-operator remainder derived below. This comparison is not an exhaustive priority theorem. |
| [Bombieri, Remarks on Weil's quadratic functional… I, 2000](https://www.bdim.eu/item?id=RLIN_2000_9_11_3_183_0), archival abstract also at [EuDML](https://eudml.org/doc/252338) | Weil positivity, finite truncations, and negative eigenvalues long predate 2026. With finitely many off-line exceptions, sufficiently large truncations recover half their number as negative eigenvalues. | The abstract was inspected; the archival PDF fetch failed in this pass. No deduction relies on an uninspected proof detail. Merely counting negative directions is prior art. |
| [Chirre–Gonçalves–de Laat, 1810.08843v2](https://arxiv.org/html/1810.08843v2), Theorem 1, Corollary 2, Sections 4.1–4.2 | Sphere-packing-style Fourier optimization and SDP improve zero statistics; interval certificates validate numerical matrices. | Their simple-zero theorem assumes RH. Exterior Fourier-sign conditions cannot be imported into this unconditional argument without proof. |
| [Doherty–Parrilo–Spedalieri, A complete family of separability criteria](https://arxiv.org/pdf/quant-ph/0308032v3), Sections III and VI | SDP duals provide explicit witnesses; stronger finite tests form a hierarchy. | A model for certificate design, not an identification of zeta zeros with entanglement. Eventual detection at some finite level need not have a uniform finite stopping level. |
| [Landau, Necessary density conditions…, 1967](https://doi.org/10.1007/BF02395039) | Band-limited interpolation is constrained by density. | A warning about uniform conditioning, not directly a theorem about the moving finite zero configurations here. |
| [Conrey–Li, math/9812166v1](https://arxiv.org/pdf/math/9812166v1), introduction and explicit examples | Particular de Branges positivity conditions implying GRH fail for the proposed zeta and Dirichlet-function spaces. | An attractive sufficient positivity condition can be false. Test the exact condition before investing in an infinite-dimensional argument. |

Two recent sources were read in downloaded PDFs and entered into the
[source manifest](source-manifest.json):

* Masatoshi Suzuki, [Weil's quadratic form via the screw function,
  2606.09096v1](https://arxiv.org/pdf/2606.09096v1), 30 pages. Theorem 1.1 realizes
  the localized form through a Friedrichs extension. Corollary 1.6 requires a
  compact-uniform limit of characteristic functions; selfadjoint finite-interval
  operators alone do not prove it. The pinned PDF prints June 9; nominal-v1 web
  HTML displayed an August 24 date, so the PDF is the reference here.
* Taebong Kim and six coauthors, [A Numerical Realization of Suzuki's
  Weil-Quadratic-Form Operator…, 2607.24830v1](https://arxiv.org/pdf/2607.24830v1),
  18 pages. Section 3.1 labels the spectral-law derivation heuristic at the
  symbol level. Section 4 says the bounded-residual argument assumes RH and
  does not prove it. These computations were not independently replayed here.

Suzuki's PDF SHA-256 is
06e2abeb778d9414f98589d8654ecf06a7f6d9d0b9914961e88365a6b48b91b2;
the numerical paper's is
ab8e2ddab80764baca435ea245438236b871e5469a5d034dee833ebc6b93541f.
Originals and extracted text are in the ignored local source-cache. The public
manifest preserves URLs, licenses, hashes, and review scope.

## 2. Exact finite off-line inertia

Use the EXP-003 conventions. The distinct support points form a finite
conjugation-invariant set with equal positive integer multiplicities on
conjugate points. Let \(s\) count simple real points, \(r\) multiple real
points, \(b\) nonreal conjugate pairs, \(N\) total multiplicity, and
\(m=s+r+2b\) distinct points.

For real even compactly supported \(\eta\), normalized by \(\int\eta^2=1\),
define

$$
v_z(t)=\eta(t)e^{-2\pi izt},\qquad
A=\sum_z m_z|v_z\rangle\langle v_{\bar z}|,\qquad
Q=\operatorname{tr}A^2,\qquad\operatorname{tr}A=N.
$$

These are the existing exact finite objects. The pair sum for \(Q\) uses
ordinary complex squares, not absolute squares of complex kernel values.
Replacing those terms by positive ones would change the operator.

**Finite inertia identity.** On the span of all feature vectors,

$$
n_-(A)=b,\qquad n_+(A)=s+r+b,\qquad n_0(A)=0.                 \tag{1}
$$

Let \(F\) have the \(m\) distinct feature columns. They are independent:
an exponential polynomial vanishing after multiplication by \(\eta\) vanishes
on a positive-measure set, hence identically by analyticity. Differentiation
at one point yields an invertible Vandermonde system for distinct exponents.
Thus \(F\) is an isomorphism onto its range. The coefficient matrix \(C\)
in \(A=FCF^*\) has a positive scalar block \(m_x\) for each real point and
the block

$$
\begin{pmatrix}0&m_z\\m_z&0\end{pmatrix}
$$

for each nonreal pair. Sylvester's law proves (1). This is a finite consequence
of the known representation and classical inertia principle, not a new RH
positivity criterion. Independence supplies no uniform lower Gram bound:
the smallest Gram eigenvalue can approach zero.

## 3. Retaining negative spectral mass

Let \(P\) be the simple-real rank-one sum, \(G\) its unit-diagonal Gram matrix,
and \(d=r+b\). Write \(p_1\le\cdots\le p_m\) and \(a_1\le\cdots\le a_m\)
for the eigenvalues of \(P\) and \(A\). The existing min-max proof gives

$$
a_i\le p_{i+d}\qquad(1\le i\le m-d),
$$

because \(n_+(A-P)\le d\). Put \(A_-=(-A)_+\),
\(\nu=\operatorname{tr}A_-\), and \(\omega=\operatorname{tr}A_-^2\).
All \(b\) negative eigenvalues lie in this retained range:
\(m-d=s+b\ge b\). For each negative one,

$$
(2-a_i)^2\ge (2-p_{i+d})_+^2+4|a_i|+|a_i|^2,
$$

since \(p_{i+d}\ge0\) makes the first right-hand term at most four.
Other retained indices obey the usual inequality without the extra terms.
Restoring the \(d\) omitted \(p\)-terms at cost at most \(4d\) gives

$$
\operatorname{tr}(A-2I)^2
\ge\sum_{j=1}^m(2-p_j)_+^2-4d+4\nu+\omega.
$$

For the existing function

$$
\Psi(t)=\begin{cases}(t-1)^2&0\le t\le2,\\2t-3&t\ge2,\end{cases}
\qquad D(G)=\operatorname{tr}\Psi(G),
$$

use \((2-p)_+^2=\Psi(p)-2p+3\), \(\operatorname{tr}P=s\), and
\(\operatorname{tr}\Psi(P)=D(G)+m-s\), including zero padding. Expansion proves

$$
\boxed{Q\ge4N-3s-4(r+b)+D(G)+4\nu+\omega.}                  \tag{2}
$$

The nonnegative multiplicity excess is

$$
E=N-s-2r-2b
=\sum_{\substack{x\text{ real}\\m_x\ge2}}(m_x-2)
+2\sum_{\{z,\bar z\}}(m_z-1).
$$

Thus

$$
\boxed{s\ge2N-Q+D(G)+2E+4\nu+\omega.}                       \tag{3}
$$

The Lamzouri-analysis reviewer independently checked this paper deduction.
It has not been formally verified or used to assert a new asymptotic
constant. The displayed remainder was not found in the inspected Ainta lemma;
a comprehensive priority claim needs a broader search.

The short-interval arithmetic controls \(Q/N\), but supplies no positive
lower bound for \((4\nu+\omega)/N\). Equation (3) isolates missing information.
If such a density bound were independently proved, it would force a further
simple-critical-zero gain. No such density lower bound is proved here.

## 4. Two exact obstructions

### Small displacements destroy a uniform gain per off-line pair

Take one pair \(x\pm iy\), \(y>0\), each of multiplicity \(\mu\). Define

$$
M(y)=\int\eta(t)^2\cosh(4\pi yt)\,dt.
$$

Evenness makes the hyperbolic-cosine and hyperbolic-sine feature combinations
orthogonal. Their pair operator has eigenvalues

$$
\lambda_+=\mu(1+M(y)),\qquad\lambda_-=\mu(1-M(y)).            \tag{4}
$$

Although \(M(y)>1\) for \(y>0\), compact support gives

$$
M(y)-1=8\pi^2y^2\int t^2\eta(t)^2\,dt+O(y^4).
$$

Negative mass tends to zero quadratically while the off-line pair count stays
one. Therefore no universal bound \(\nu\ge c_0b\), \(c_0>0\), holds in this
finite class. Contributions from different pairs cannot simply be added as
negative eigenvalues after other positive directions are included.

For zeta zeros the normalized imaginary displacement is proportional to
\((\Re\rho-1/2)\log T\). Neither the functional equation nor the current
pair-correlation theorem supplies a positive lower bound for every such
off-line displacement.

### Two scalar moments cannot determine positivity

The matrices

$$
\operatorname{diag}(7/3,7/3,-2/3),\qquad
\operatorname{diag}(10/3,1/3,1/3)
$$

both have trace \(4\), squared Hilbert–Schmidt norm \(34/3\), and full rank
three. Exactly one has negative spectrum. This is an abstract matrix
counterexample, not a claim that both spectra arise from the zero-kernel
geometry. It defeats a shortcut based only on those moments and dimension.
Additional geometry or arithmetic must do substantive work.

Sampling theory supplies a related caution: fixed Fourier support limits
uniform interpolation density. The finite independence proof cannot be
promoted to a uniform lower Gram bound for increasingly dense families.
Applying Landau's theorem directly to moving short-interval zero sets would
require density and separation hypotheses not checked here.

## 5. A concrete SDP and higher-moment interface

For a finite Hermitian \(A\), the standard dual formula is

$$
\nu=\max_{0\preceq Y\preceq I}-\operatorname{tr}(AY)
=\min_{Z\succeq0,\ Z+A\succeq0}\operatorname{tr}Z.           \tag{5}
$$

Diagonalization proves (5): the maximizing \(Y\) projects onto the negative
eigenspaces. A rational feasible \(Y\), with exact PSD certificates for
\(Y\) and \(I-Y\), provides a portable lower-bound witness even if it is
not optimal. Interval evaluation must bound the trace in the correct
direction. Approximate floating feasibility is insufficient.

For a known orthonormal test family, use the compression
\(H=(\langle\psi_i,A\psi_j\rangle)\). A feasible witness for \(H\) embeds
as one for \(A\), so \(-\operatorname{tr}(HY)\le\nu\).
This lower-bound direction does not assert that the compression captures
the entire negative spectrum. A nonorthonormal basis requires its actual
mass matrix.

To identify the extra arithmetic, put \(m_j=\operatorname{tr}A^j\).
If \(A\succeq0\), then \(\operatorname{tr}(A p(A)^*p(A))\ge0\) for every
polynomial \(p\). Thus each localizing matrix

$$
L_d=(m_{i+j+1})_{0\le i,j\le d}
$$

is PSD. At degree one this requires

$$
N\operatorname{tr}A^3-Q^2\ge0.                             \tag{6}
$$

A strictly negative left side certifies off-line inertia for the finite
operator. For the isolated pair in (4), direct algebra gives

$$
N\operatorname{tr}A^3-Q^2
=4\mu^4M(y)^2(1-M(y)^2)<0.
$$

For any fixed finite matrix with negative spectrum, polynomial interpolation
can select a negative eigenvalue and vanish at the others; some finite
localizing matrix therefore fails positivity. The required degree can grow
with dimension. This is not a uniform finite criterion at all heights.

This hierarchy uses cyclic higher correlations:

$$
\operatorname{tr}A^j
=\sum_{z_1,\ldots,z_j}m_{z_1}\cdots m_{z_j}
\prod_{\ell=1}^jK(z_{\ell+1}-z_\ell),\qquad z_{j+1}=z_1.
$$

Wang's second-moment theorem supplies no third-moment asymptotic for this
cycle sum. Substituting random-matrix predictions would make the argument
conditional. A higher-moment theorem or direct prime-side witness estimate
is the specific missing input.

The full Weil form offers another interface: evaluate its matrix on smooth
test functions through the explicit formula and certify a negative Rayleigh
direction or a PSD lower bound. It bypasses the simple-zero subset, but is
**not the same operator** as the height-truncated \(A\). Transferring a
Weil-form witness to a quantitative bound on this \(\nu\) needs localization
and omitted-zero tail estimates. Positivity of one finite prime-side matrix
does not control its orthogonal complement or every aperture.

## 6. Comparison of cross-area directions

| Direction | Information added | First missing ingredient |
|---|---|---|
| Full-operator witnesses and localizing moments | Negative directions and off-line displacement | Arithmetic control of witness traces, cyclic moments, or localization tails |
| Fourier/SOS optimization from sphere packing | Larger certified test-function classes | Unconditional justification of every Fourier-sign condition |
| Additive-combinatorial gap words and weighted frame covers | Better use of span, pair capacity, and compatible local configurations | A stronger local certificate; this stays inside the pair-energy framework |
| Sampling/uncertainty bounds for exponential packets | Conditions under which witnesses are robust | Uniform separation/conditioning, including clustered points |
| Suzuki/Weil approximation | Explicit arithmetic operator and variational meaning | Complement/tail estimates or the conjectural limiting identity |

The first direction changes the observable. The weighted-real-point and
arithmetic zero-counting route under parallel review may have a more immediate
path to an unconditional proportion. Their hypotheses and evidence should
remain separate.

## 7. Proposed invariant-first preflight

This is a design for a future committed hypothesis, not a record of a run.

1. **Paper gate.** Recheck (1)–(6), mass-matrix conventions, and the distinction
   between the finite zero operator and full Weil form. Locate any earlier
   occurrence of (2). Amend the proposed claim if exact prior art is found.
2. **Frozen controls:** at most 32 instances, dimension at most eight.
   Include on-line-only points, one and two conjugate pairs, and collisions.
   Freeze rational coordinates and multiplicities. Check pair formulas and
   certified inertia; reject any universal gain per off-line pair.
3. **At most four witness problems.** Produce rational \(Y\) for (5), or
   coefficient vectors for \(L_d\), \(d\le3\). Retain unsuccessful attempts.
   Validate PSD constraints by rational factorization and directed interval
   residual bounds.
4. **Arithmetic gate.** State the extra zeta estimate, Fourier support, and
   height dependence. If only two scalar moments remain available, record
   insufficient arithmetic input. Synthetic configurations do not establish
   a new zeta-zero proportion.

An initial cap of ten CPU minutes, 256-bit interval validation, and no degree
or dimension escalation is proportionate to these controls. This is an
engineering estimate, not a benchmark. Dense floating optimization may
suggest witnesses; rational/interval validation is authoritative. A GPU
offers little value at these sizes. Large Galerkin matrices and prime sums
with support growing exponentially in aperture should wait for an analytic
reason their outputs address the missing estimate.

Meaningful success is a certified finite witness theorem with a stated
arithmetic interface, or a rigorous obstruction ruling out a precise
interface. Matching known zero ordinates, positive finite-mesh eigenvalues,
or random-matrix histograms would not meet that target. Neither prospective
outcome would by itself solve RH.
