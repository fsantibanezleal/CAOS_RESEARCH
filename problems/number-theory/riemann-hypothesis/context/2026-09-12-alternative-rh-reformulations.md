# Alternative RH reformulations: finite diagnostics and structural barriers

Date: 2026-09-12. Scope: source review and analytic question design only. No numerical experiment, optimizer run, new zero verification, or proof of RH was performed for this dossier.

Status notation: **[V]** means the stated source or elementary implication was checked at the indicated location; it does not mean every proof or numerical certificate in that source was independently replayed. **[U]** means a current claim remains unaudited. **[C]** marks a proposed research question, with no experimental verdict.

## 1. Research decision

The strongest change of direction is to investigate a quantitative bridge between finite approximation and its omitted arithmetic tail. This is a structural question, not another optimization of the proportion of simple zeros. The Nyman-Beurling route supplies an especially explicit version: approximation alone can already be achieved unconditionally in a generalized space, while a second, precisely stated tail condition remains necessary to transfer it to information about zeta zeros.

The immediate recommendation is the coupled approximation/tail problem in Section 6. Its two possible useful outcomes are an unconditional asymptotic estimate implying a new zero-free strip, or an obstruction theorem showing that a specified approximation family cannot deliver such an estimate. Neither outcome is promised. The finite diagnostic must certify both objectives; minimizing only the approximation error would miss the known difficulty.

The other strong candidate is a quantitative convergence or obstruction result for Suzuki's finite operator construction, reviewed in the companion [spectral alternatives dossier](2026-09-12-spectral-optimization-alternatives.md). A self-adjoint finite matrix, a successful finite positivity calculation, or an attractive spectral plot does not supply that convergence theorem.

## 2. Comparison of four routes

| Route | Exact infinite statement | What a finite success proves | What a finite failure proves | Practical cost and useful new result |
|---|---|---|---|---|
| Nyman-Beurling and Baez-Duarte | The distance of the indicator to the specified arithmetic span tends to zero if and only if RH holds. | An upper bound for one approximation distance, or a tradeoff between approximation and a tail norm. | A bad proposed approximant. A positive dual lower bound can reject an entire restricted support family. A single positive finite distance does not refute RH. | Dense Gram storage is quadratic and generic factorization cubic in the basis size; exact tails and conditioning govern precision. A new uniform approximation/tail estimate or a sharp family obstruction is useful. |
| Li and Weil positivity | All Li coefficients are positive; equivalently the Weil form is nonnegative on its full admissible test space. | Positivity of the tested coefficients or finite subspace, with rigorous truncation bounds. | A certified negative exact Li coefficient or admissible Weil quadratic form refutes RH. A negative approximation without a controlled remainder does not. | Taylor arithmetic or interval quadratic forms are feasible at moderate size. A quantitative witness-completeness theorem or an arithmetic positivity mechanism would be structural. |
| de Branges, Hilbert-Polya, screw kernels | A valid spectral realization with the correct divisor, or an equivalent global positivity/limit theorem, implies RH. Self-adjointness alone is not an equivalence. | A property of a finite operator or one aperture. | A counterexample to the particular sufficient positivity condition or limiting construction; usually not to RH. | Matrix spectra are cheap relative to rigorous control of an infinite-dimensional limit. A correct, noncircular convergence theorem or explicit obstruction to one proposed construction matters. |
| de Bruijn-Newman heat flow | RH is equivalent to $\Lambda=0$, using the proved lower bound $\Lambda\geq0$. | With an analytic infinite-tail theorem and a certified barrier, a finite computation can prove a global upper bound $\Lambda\leq b$. | Failure of that barrier or enclosure. It need not mean an actual nonreal zero exists. | Existing packages involve millions of interval rows. A tail/barrier theorem uniform toward zero heat time would be more relevant than changing the last digits of $b$. |

The operation counts are algorithm-design estimates, not measured runtime or promises of GPU acceleration. Floating-point GPU output could help discover coefficients; it cannot replace directed-rounding certificates or an analytic tail proof.

## 3. Exact formulations and normalization checks

### 3.1 Nyman-Beurling and Baez-Duarte

**[V]** Put $\rho_a(x)=\{1/(ax)\}$ and $\chi=\mathbf1_{(0,1)}$ in $L^2(0,\infty)$. Baez-Duarte's strengthening permits only integer $a\geq1$: RH is equivalent to $\chi$ belonging to the closure of their span. Its damped Mobius approximation and norm estimate assume RH. See [Baez-Duarte, math/0205003v1](https://arxiv.org/abs/math/0205003v1), pp. 1-2.

An equivalent Dirichlet-polynomial distance is

$$
d_N^2=\inf_{A_N}\frac1{2\pi}\int_{\mathbb R}
\frac{|1-\zeta(1/2+it)A_N(1/2+it)|^2}{1/4+t^2}\,dt,
\qquad A_N(s)=\sum_{n\leq N}a_n n^{-s}.
$$

The sharp-asymptotic discussion must retain multiplicities:

$$
\liminf_{N\to\infty}d_N^2\log N
\ \geq\sum_{\Re\rho=1/2}\frac{m(\rho)^2}{|\rho|^2},
$$

where distinct critical-line zeros index the sum. [Burnol, math/0103058v2](https://arxiv.org/abs/math/0103058v2), Theorem 1.3, proves the continuous-dilation lower bound; restricting to integer dilations gives the displayed consequence. [Bettin, Conrey and Farmer, 1211.5191v1](https://arxiv.org/abs/1211.5191v1), pp. 1-3, obtain the matching constant for a specific polynomial under RH and a reciprocal-derivative moment assumption, which also presupposes simple zeros. Their conditional constant is not a usable unconditional tail estimate.

### 3.2 Li and Weil

**[V]** With $\xi(s)=\tfrac12s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s)$,

$$
\lambda_n=\frac1{(n-1)!}
\left.\frac{d^n}{ds^n}\bigl[s^{n-1}\log\xi(s)\bigr]\right|_{s=1}
=\lim_{T\to\infty}\sum_{|\Im\rho|\leq T}
\left[1-\left(1-\rho^{-1}\right)^n\right].
$$

RH is equivalent to $\lambda_n>0$ for every $n\geq1$. The height-symmetric summation and multiplicities are essential. [Bombieri and Lagarias, *Complements to Li's criterion*](https://websites.umich.edu/~lagarias/doc/bombieri.pdf), pp. 1-4, establish the general multiset framework and the relation to Weil positivity. The downloaded PDF has a defective text encoding; pages 1 and 3 were rendered, and the general theorem on page 3 was visually inspected.

For a compactly supported smooth function $f$ and $\widehat f(z)=\int f(t)e^{izt}\,dt$, write $\gamma=i(\rho-1/2)$. A consistent Weil convention uses

$$
Q(f)=\sum_\gamma \widehat f(\gamma)
\overline{\widehat f(\bar\gamma)}.
$$

Under RH this becomes a sum of squares. Off RH it must not be replaced by $\sum|\widehat f(\gamma)|^2$: that substitution assumes the desired reality. The admissibility and passage to the full form are treated in [Suzuki, 2209.04658v3](https://arxiv.org/abs/2209.04658v3), pp. 2-6.

### 3.3 Screw functions and operator realizations

**[V]** Suzuki defines an explicit prime-sum function $\Psi$, sets $g=-\Psi$, and forms

$$
K(t,u)=g(t-u)-g(t)-g(-u)+g(0).
$$

RH is equivalent to this kernel being positive semidefinite for every finite point configuration on the real line. The continuous integral operator on $L^2(-a,a)$ is trace class unconditionally; positivity for every aperture is the unresolved condition. Pointwise $\Psi(t)\geq0$ for all $t$ is another exact equivalence. See [Suzuki, 2206.03682v4](https://arxiv.org/abs/2206.03682v4), Theorems 1.2-1.8, pp. 3-5.

The finite point test is particularly clean: a rational vector and rational sample points with a certified negative quadratic form would refute RH. Finitely many positive matrices do not imply positivity at the next aperture, nor at unsampled points. On $[-a,a]$, the prime formula needs terms up to $e^{2a}$ because differences reach $2a$; this creates an exponential arithmetic cost in the aperture.

### 3.4 Heat flow

**[V]** Use the Polymath convention

$$
H_t(z)=\int_0^\infty e^{tu^2}\Phi(u)\cos(zu)\,du,\qquad
H_0(z)=\tfrac18\xi(1/2+iz/2),\qquad
\partial_tH_t=-\partial_z^2H_t.
$$

Here $\Phi(u)=\sum_{n\geq1}(2\pi^2n^4e^{9u}-3\pi n^2e^{5u})e^{-\pi n^2e^{4u}}$.
Do not combine this parameter with papers using a differently scaled $\Xi$ without converting the heat time.

[Rodgers and Tao, 1801.05914v5](https://arxiv.org/abs/1801.05914v5), Theorem 1.1, prove $\Lambda\geq0$; therefore RH is equivalent to $\Lambda=0$.

[Polymath, 1904.12438v2](https://arxiv.org/abs/1904.12438v2), Theorem 1.2, pp. 2-3, proves $\Lambda\leq t_0+y_0^2/2$ from three separate inputs: finite initial zero exclusion to height $X/2$, a final-time infinite zero-free tail, and a zero-free barrier through all intermediate times. Theorem 1.3 supplies an effective approximation. A finite sampling plot supplies none of these quantified regions by itself.

## 4. Current prior art and barriers

### 4.1 Sparse Nyman-Beurling models need an arithmetic completeness audit

**[V]** [Carvill, 2510.18132v1](https://arxiv.org/abs/2510.18132v1), October 2025, proposes a $2^{-j}3^{-k}$ ladder and a Mellin smoothing argument. Its proof of Theorem 6.1 on p. 8 uses

$$
|(j-j')\log2+(k-k')\log3|
\geq\min(\log2,\log3)(|j-j'|+|k-k'|).
$$

This is false: $(j,k)=(1,0)$ and $(j',k')=(0,1)$ would require $\log(3/2)\geq2\log2$, contradicted by $3/2<4$. This is an exact symbolic rejection of that step, not an experimental result.

Further unsupported steps include inferring boundedness of an infinite matrix operator from bounded entries (p. 6), a shell-supremum monotonicity argument using nonnested shells (p. 6), and treating a general Fourier multiplier as automatically preserving the Mellin image of $L^2(0,1)$ (p. 7). These invalidate the supplied proof route. They do not prove the final unnormalized decay statement false.

**[V]** The more fundamental coefficient obstruction is established prior art. [Pyvovarov, 2607.12084v3](https://arxiv.org/abs/2607.12084v3), July 2026, Proposition 2.1, pp. 7-9, proves uniqueness of Mobius coefficients for its fixed-coefficient pointwise approximation. It explicitly says the natural sequence fails in $L^2$ and introduces damping. Its later global bilinear cancellation remains unresolved, pp. 62-64. The abstract has a measure typo; Section 1.1 correctly uses $dt/t^2$.

[Calderaro, Manzur, Noor and Santos, 2203.05030v4](https://arxiv.org/abs/2203.05030v4), pp. 2, 6 and 9-12, credit Vasyunin's earlier biorthogonal minimality result and prove a complete biorthogonal family in a Hardy-space formulation. Thus neither Mobius coefficient uniqueness nor the idea of rejecting an omitted coordinate is new.

### 4.2 Conditioning and smoothing do not remove the arithmetic tail

**[V]** [Alouges, Darses and Hillion, 2006.02953v2](https://arxiv.org/abs/2006.02953v2), Theorems 3 and 6, separate approximation from a tail condition and obtain an alternate Hankel Gram structure. Their Section 4.3.2 explains why making the seed compactly supported, which removes the tail, loses the available full-line polynomial-density argument. This is an existing structural uncertainty-principle barrier, not a new observation here.

The 2026 *Preprints.org* article [*Spectral and Analytic Structure of the Nyman-Beurling-Baez-Duarte Approximation*, v2](https://www.preprints.org/manuscript/202506.0772), is not adopted as a premise: its displayed Gram system for $\{kx\}$ is a different family from $\{1/(kx)\}$. Its formal coefficient arguments do not justify transferring results between those systems. Only the displayed source sections were inspected; a complete paper audit was not performed.

### 4.3 Li and positivity methods already have strong finite-limit warnings

**[V]** [Voros, math/0404213v2](https://arxiv.org/abs/math/0404213v2), pp. 2-4, explains the growing cancellation in coefficient formulas and the contrast between exponential oscillations caused by an off-line zero and RH-compatible behavior. This early version explicitly describes part of its saddle-point discussion as experimental. It is a source for the diagnostic limitation, not an unconditional asymptotic estimate imported here.

**[U]** A recent finite Xi-defect positivity program is already public at [LeonardSEO/certified-riemann-xi-positivity](https://github.com/LeonardSEO/certified-riemann-xi-positivity/tree/6d5f6ce7ad1031cee8740e47b044dda139dd497c), pinned July 20, 2026. The source claims a finite band $7.0362433<R_{10}<7.0362434$ and proves a bounded-radius obstruction for every fixed-width cross-endpoint hierarchy. Its [partition equivalence audit](https://github.com/LeonardSEO/certified-riemann-xi-positivity/blob/6d5f6ce7ad1031cee8740e47b044dda139dd497c/research/partition_monotonicity/rh_equivalence_audit_20260720.md) already distinguishes RH from RH plus simplicity at the boundary $y=0$. Refining partitions or increasing moment order is therefore not, by itself, a novel global positivity mechanism. Certificates were not replayed in this task.

### 4.4 de Branges: check the premise before building the operator

**[V]** [Conrey and Li, math/9812166v1](https://arxiv.org/abs/math/9812166v1), Section 3, exhibits failures of specific sufficient de Branges positivity conditions for zeta and a Dirichlet L-function. The concluding remark on p. 9 gives Sarnak's nonnumerical obstruction to the ratio-positivity condition. This rejects those particular sufficient conditions, not every possible de Branges construction.

**[U]** The current Suzuki operator paper, [2606.09096v1](https://arxiv.org/abs/2606.09096v1), and numerical follow-up [2607.24830v1](https://arxiv.org/abs/2607.24830v1), are audited separately in [the spectral alternatives dossier](2026-09-12-spectral-optimization-alternatives.md). The consequential missing input is the compact-uniform limiting identification in Suzuki's Corollary 1.6. The numerical paper's bounded-residual argument assumes RH. It cannot discharge that missing limit.

### 4.5 Heat-flow records are changing, but the zero-time obstacle remains

**[V as a registry entry; U as an independently replayed record]** [Tao's current optimization database](https://teorth.github.io/optimizationproblems/constants/21a.html) lists 2026 packages for $0.1965$ and $0.1875$, DOI [10.5281/zenodo.20724170](https://doi.org/10.5281/zenodo.20724170) and [10.5281/zenodo.21175533](https://doi.org/10.5281/zenodo.21175533). A statement that $0.2$ is the only currently public upper-bound claim is outdated. Database inclusion is not our certificate audit.

**[U]** [Gomila's repository](https://github.com/judegomila/dbn-lambda-01787854-candidate-audit/tree/a74738deb6d5e0f76887cb36901da08b68dca705), pinned August 21, 2026, presents a $0.1787854$ computer-assisted proof for independent review. The same commit contains a [lower-time completion dossier](https://github.com/judegomila/dbn-lambda-01787854-candidate-audit/blob/a74738deb6d5e0f76887cb36901da08b68dca705/research/lower_time_01782354/LOWER_TIME_01782354_PROOF_GAP.md) for $0.1782354$, explicitly classified as an unreviewed candidate. Both use the existing Polymath framework and a finite verification height, with parameter-specific interval certificates. We read the proof note, tail lemma, lower-time scope and license exceptions; we did not replay the full sweep.

Polymath already states that its normalized large-height asymptotic is not uniform as $t\to0$ (p. 4). Gomila's tail contraction uses strict positive-time inequalities. Neither can be extrapolated to time zero by continuity without a new uniform bound.

## 5. A rigorous rejection diagnostic for sparse denominator families

This is a derived diagnostic using classical biorthogonality, not a claimed new theorem about RH.

Work in $\mathcal H=L^2([1,\infty),dt/t^2)$ with
$\gamma_j(t)=\lfloor t/j\rfloor-\lfloor t\rfloor/j$, $j\geq2$.
Every finite combination $F=\sum_j a_j\gamma_j$ is constant on $[m,m+1)$; denote its value by $F_m$ and put $F_0=0$.
For $n\geq2$, define

$$
L_n(F)=\sum_{d\mid n}\mu(n/d)(F_d-F_{d-1}).
$$

Direct Mobius inversion gives $L_n(\gamma_j)=\delta_{nj}$, while $L_n(\mathbf1)=\mu(n)$. To check the first identity, take the difference of consecutive floor values: it equals $\mathbf1_{j\mid d}-1/j$. The constant cancels because $\sum_{d\mid n}\mu(n/d)=0$.

Let

$$
q_{n,m}=\sum_{d\mid n}\mu(n/d)
(\mathbf1_{m=d}-\mathbf1_{m=d-1}),\qquad
C_n=\sum_{m=1}^n m(m+1)q_{n,m}^2.
$$

The cell weight is exactly $\int_m^{m+1}t^{-2}dt=1/[m(m+1)]$. Weighted Cauchy-Schwarz therefore gives

$$
|\mu(n)-a_n|^2\leq C_n\|\mathbf1-F\|_{\mathcal H}^2.
$$

This inequality survives arbitrary changes in the other coefficients and arbitrary support size. Omitting any squarefree $n$ gives a strictly positive lower bound independent of the truncation. For a prime $p\geq3$, the three nonzero coefficients occur at $1,p-1,p$, so $C_p=2p^2+2$. In particular, every combination supported only on $2,3$-smooth denominators has

$$
\|\mathbf1-F\|_{\mathcal H}^2\geq 1/52
$$

because denominator $5$ is absent. This calculation uses exact identities, not a numerical experiment.

The point is to reject an inadmissible sparse replacement before expending resources on its Gram matrix. It says nothing adverse about RH: the full Baez-Duarte space is not restricted to that ladder. Multiple omitted coordinates could be combined by a finite dual Gram matrix, but the projection principle is standard and would not on its own justify a manuscript claiming a new RH approach.

## 6. Recommended falsifiable structural question

### 6.1 Specify the family and both obligations

**[C]** Consider the explicit exponential seed

$$
g_0(t)=te^{-t},\qquad
g_{k+1}(t)=-t g_k'(t)-\tfrac12g_k(t),\qquad
g_k^\times(t)=\int_0^\infty\{x/t\}g_k(x)\,\frac{dx}{x}.
$$

Use the target $\varphi(t)=e^{-t}$ and real coefficients
$c=(c_0,\ldots,c_{n-1})$. Set

$$
R_{n,c}(t)=\varphi(t)-\sum_{k<n}c_k g_k^\times(t),\qquad
P_{n,c}(t)=\sum_{k<n}c_k g_k(t).
$$

For a cutoff $M>1$, define the coupled objective

$$
J_{n,M}(c)=M^{1/2}\|R_{n,c}\|_2^2+
M^{-1/4}\int_M^\infty|P_{n,c}(t)|\,dt.
\tag{A}
$$

This is a concrete convex optimization problem: a positive quadratic approximation term plus the absolute integral of an explicitly known exponential polynomial. It is a proposed diagnostic built from the existing criterion, not an established new equivalence.

The seed obeys the endpoint conditions in Alouges-Darses-Hillion: choose any $0<\alpha<1$ at zero, and exponential decay controls infinity. Its Mellin transform is $\Gamma(s+1)$, while $\widehat\varphi(s)=\Gamma(s)$ has no zeros. Applying their Theorem 3 with $\sigma_0=3/4$ shows that a proved sequence with $M_n\to\infty$ and $J_{n,M_n}(c_n)\to0$ would imply

$$
\zeta(s)\ne0\qquad(1/2<\Re s\leq3/4).
\tag{B}
$$

Both terms in (A) are nonnegative, so their sum tending to zero supplies the two separate hypotheses. The strip conclusion (B) would be substantial. It is not asserted here, and this restricted strip alone is not RH.

### 6.2 Bounded first diagnostic, with an explicit rejection condition

Before computation, a new experiment must declare the finite dimensions and cutoffs, rational coefficient representation, precision escalation, and a proposed bound $J_{n,M}\leq\tau_{n,M}$. Produce rigorous upper bounds from actual coefficients and lower bounds from a convex dual or exact finite restriction. If a certified lower bound exceeds the declared $\tau_{n,M}$, the proposed coefficient schedule is falsified. Failure of one schedule does not falsify the seed family or RH.

The first diagnostic should compare the unconstrained approximation optimum with the coupled optimum at the same $n,M$. An enormous increase under the tail penalty is mathematically informative: it locates the loss incurred by transferring an easy generalized approximation into arithmetic information. A fitted downward trend, however convincing, is not the limiting theorem (B).

A meaningful subsequent result would prove one of:

1. A uniform positive-rate estimate for (A), with all coefficient and tail bounds explicit.
2. A nonzero limiting obstruction for a clearly specified cutoff law such as $M_n=n$, together with an explanation of why another law might evade it.
3. A quantitative lower bound forcing tail growth whenever the approximation residual is too small, valid for the whole seed family.

Generic least squares, the alternate Hankel structure, gamma-function decay, and the need for coefficient control are already prior art. Novelty must attach to the new quantitative tradeoff or obstruction.

### 6.3 Certification and resource boundaries

Each $g_k$ is $e^{-t}$ times a polynomial. Thus the second integral in (A) can be reduced to sign intervals of a polynomial and incomplete-gamma integrals, with root isolation and a rigorous infinite endpoint. The first term needs the true fractional-part convolution or its Mellin representation, including a certified tail. A sampled Gram matrix for a different sawtooth family is inadmissible.

The quadratic form requires approximately $n^2$ scalar products and ordinary dense optimization approximately $n^3$ arithmetic operations before conditioning and interval overhead. This is initially a CPU and arbitrary-precision task. A GPU is useful only if exploratory coefficient searches become dominant. No compute budget, convergence rate, or achievable dimension has yet been measured.

## 7. Other reachable questions, ranked below the coupled approximation problem

**Li/Weil diagnostic completeness.** Derive explicit witness complexity in terms of a hypothetical off-line zero's height and displacement, with a certified contribution from every omitted zero. A finite successful search would certify only its tested region. General multiset arguments and coefficient asymptotics already explain eventual detection; a new result needs sharper effective bounds or a genuinely smaller admissible arithmetic test class.

**Suzuki operator convergence.** Find an explicit tail or resolvent estimate sufficient for the limiting identification in the 2026 paper, or prove that a proposed boundary normalization cannot satisfy it. The finite spectra must not be constructed from the known zeta zeros themselves. This route has a strong conceptual connection to inverse spectral theory, but a much larger analytic uncertainty than (A).

**Heat-flow uniformity.** Formulate a zero-free-tail or barrier statement uniform over a sequence $t_j\downarrow0$, with all constants and initial-height requirements tracked. A finite set of successful positive times gives only finitely many upper bounds. A uniform theorem supplying arbitrarily small upper bounds would give RH using Rodgers-Tao; therefore it must not be smuggled in as a numerical extrapolation.

**Moment hierarchy obstructions.** Prove an analytic ceiling for a specified positivity hierarchy or quantify the mesh/order tradeoff needed to avoid one. The fixed cross-endpoint ceiling and the all-compacts positivity equivalence already appear in LeonardSEO's July 2026 source. Repeating those conclusions is not novel.

## 8. Source inventory, archival scope and limitations

The live source search covered exact names and formulas for Nyman-Beurling distance, squarefree/omitted denominators, Mobius coefficient uniqueness, biorthogonal systems, alternate Hankel matrices, Li asymptotics, de Branges positivity failures, screw functions, and 2026 heat-flow certificates. Searches included arXiv, author/institution pages, primary public repositories, and the current Tao optimization database. Secondary indexes were used to locate primary texts, not as theorem premises.

This is a source-complete review of the explicit claims and proposed diagnostic above, not an assertion that every RH paper, proof or public repository was read. Sections and theorem labels identify the inspected dependencies. Long papers were reviewed at the relevant statements, proofs and closing barriers; unrelated sections were not certified line by line. Current computational claims remain quarantined until an independent mathematical audit and certificate replay are separately declared.

| Primary item | Pinned version or publication | Inspected dependency |
|---|---|---|
| Baez-Duarte, *A strengthening ... 2* | math/0205003v1, 2002 | integer-dilation criterion and conditional approximant |
| Burnol, *A lower bound ...* | math/0103058v2, 2001; journal 2002 | multiplicity-sensitive distance lower bound |
| Bettin-Conrey-Farmer, *An optimal choice ...* | 1211.5191v1, 2012 | Theorem 1 and reciprocal-derivative hypothesis |
| Baez-Duarte, *Arithmetical aspects ...* | math/0011254v1, 2000; journal 2002 | natural approximants and failure of naive $L^2$ convergence |
| Alouges-Darses-Hillion, *Polynomial approximations ...* | 2006.02953v2, 2022; DOI 10.5802/jtnb.1227 | Theorems 3, 6; Sections 4.2-4.3 |
| Calderaro-Manzur-Noor-Santos, *Orthogonality questions ...* | 2203.05030v4, 2024 | biorthogonal minimality and Theorem 15 |
| Pyvovarov, *A few remarks ...* | 2607.12084v3, July 2026 | Proposition 2.1 and Section 9.6 |
| Carvill, *Beurling Nyman geometry ...* | 2510.18132v1, 2025 | rejected steps on pp. 6-9 |
| Bombieri-Lagarias, *Complements to Li's criterion* | author PDF; JNT77 (1999), 274-287 | Li normalization and general multiset theorem |
| Voros, *A sharpening of Li's criterion* | math/0404213v2, 2004 | conditioning and explicit limitation on asymptotic discussion |
| Conrey-Li, *A note on some positivity conditions ...* | math/9812166v1, 1998; IMRN2000, 929-940 | Section 3 and Sarnak's concluding obstruction |
| Suzuki, *Aspects of the screw function ...* | 2206.03682v4, 2023 | Theorems 1.2-1.8 |
| Suzuki, *The screw line ...* | 2209.04658v3, 2023 | Weil-form/screw-line equivalences |
| Rodgers-Tao, *The de Bruijn-Newman constant is non-negative* | 1801.05914v5 | exact heat convention and Theorem 1.1 |
| Polymath, *Effective approximation ...* | 1904.12438v2 | Theorems 1.2-1.3 and nonuniform zero-time limit |
| Gomila heat-flow source | a74738deb6d5e0f76887cb36901da08b68dca705 | proof note, tail lemma, lower-time candidate, licensing |
| LeonardSEO finite positivity source | 6d5f6ce7ad1031cee8740e47b044dda139dd497c | paper, obstruction proof, partition/RH audit, licensing |
| Tao optimization database | retrieved 2026-09-12 | dated registry of 2026 upper-bound packages |
| Suzuki and numerical follow-up, 2026 | 2606.09096v1; 2607.24830v1 | separate sibling audit and manifest entries |

Full PDFs and selected repository documents are persisted in the ignored local source cache, with URLs, byte counts, versions, licenses and SHA-256 values in [source-manifest.json](source-manifest.json). Existing rows are retained. The arXiv distribution license is not treated as a general republication license. Gomila's code is MIT and specified documentation is CC BY 4.0, but the authored manuscript and several third-party subtrees are expressly excluded. LeonardSEO's software is AGPL-3.0-only while scholarly materials are all rights reserved. Accordingly, these new mixed-license source collections are not added as public full-repository snapshots.

No result in this dossier closes RH, establishes a new global zero proportion, or upgrades an unreviewed computational candidate to an accepted theorem. The recommended next declaration should ask a precise question about (A) or the operator limit, record rejection thresholds, and preserve failed cases.
