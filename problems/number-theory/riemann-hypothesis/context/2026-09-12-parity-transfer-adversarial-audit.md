# Independent adversarial audit of the odd-multiplicity transfer

Date: 2026-09-12. Scope: paper derivation and primary-source preflight before EXP-004 computation. This audit does not report a numerical experiment, a new certified decimal exponent, or an end-to-end formal proof.

## Verdict

No fatal gap was found in the transfer from a fixed positive density of distinct odd-multiplicity critical zeros to a qualitative extension of the short-interval simplicity positivity range. The finite inequalities, Karatsuba's count convention, the packing of seed intervals, and the order of the analytic limits support the deduction.

The supported claim is that **some fixed exponent strictly below the zero of Wang's cosine bound has a positive simple-critical proportion in every sufficiently high interval of that power length**. No usable numerical classical density constant or new decimal exponent is extracted here. Priority is not exhaustively established. The inherited finite stability theorem and Wang's recent arithmetic preprint remain substantive external inputs.

The proposed distinct-zero companion is correct. Replacing its constant by one half of one plus the improved simple-zero constant would be unjustified.

The independently reviewed companion dossier is [Critical mass, odd multiplicity, and the short-interval positivity threshold](2026-09-12-critical-mass-and-multiplicity-route.md). The finite and arithmetic interfaces are recorded in [EXP-003's proof](../experiments/EXP-003-odd-frame-pressure/mathematical-proof.md) and [the Wang transfer audit](2026-09-12-wang-transfer-audit.md). This document records independent checks and their limits rather than upgrading inherited inputs to new results.

## 1. Exact finite bookkeeping

Let the finite multiset of encoded zeros be invariant under complex conjugation, with equal multiplicity at conjugate points. Write:

- \(N\): total multiplicity, including off-line zeros;
- \(s\): number of simple real support points;
- \(r\): number of real support points of multiplicity at least two;
- \(b\): number of nonreal conjugate pairs of distinct support points;
- \(O\): number of distinct real support points of odd multiplicity;
- \(D_Z=s+r+2b\): total distinct complex support count.

Then

$$
E=N-s-2r-2b
=\sum_{\substack{x\in\mathbb R\\m_x\ge2}}(m_x-2)
+2\sum_{\{z,\bar z\}\not\subset\mathbb R}(m_z-1)\ge0.
$$

The first sum contains every multiple real support once; the second contains every nonreal conjugate pair once. A triple real zero contributes one to \(E\) and one to \(O\). A double real zero contributes zero to both. A simple off-line pair contributes two to \(N\), two to \(D_Z\), and zero to \(s,O,E\).

For the normalized nonnegative even density and direct Hilbert operator of EXP-003, let \(Q=\operatorname{tr}(A^2)\) and let \(\mathcal D=\operatorname{tr}\Psi(G_s)\ge0\) be the inherited simple-vector Gram defect. The established stable inequality is

$$
Q\ge4N-3s-4r-4b+\mathcal D
=2N-s+2E+\mathcal D.
$$

No new spectral lemma is needed to retain \(E\). Define its exact nonnegative slack

$$
F=Q-2N+s-2E-\mathcal D\ge0.
$$

Every nonsimple odd real point has multiplicity at least three, so \(s+E-O\ge0\). The proposed simple bound has the exact slack identity

$$
3s-(2N-Q+2O+\mathcal D)
=F+2(s+E-O)\ge0.
$$

This proves the finite parity transfer even when \(2N-Q\) is negative. It does not reinterpret odd multiplicity as simplicity.

The exact distinct identity is \(2D_Z=N+s-E+2b\). Combining it with the stable bound gives

$$
2D_Z-(3N-Q+\mathcal D)=F+E+2b\ge0,
$$

$$
6D_Z-(7N-2Q+O+2\mathcal D)
=2F+(s+E-O)+6b\ge0.
$$

These factorizations independently verify all coefficients and the favorable direction of the off-line contribution. The tempting inequality \(2D_Z\ge N+s\) is false for arbitrary multiplicities: one real triple point has \(N=3,s=0,D_Z=1\). Thus an improved simple lower bound cannot simply be inserted into the old half-sum formula. The separate stable distinct inequality is valid for its own reason.

No step requires termwise positivity of complex pair terms. The arithmetic kernel is squared as an ordinary complex number. Positivity applies to the complete Hilbert--Schmidt sum \(Q\). Discarding off-line atoms, replacing the square by an absolute square, or collapsing a conjugate pair into one zero changes the statement and is not allowed.

## 2. Primary-source seed: distinct odd supports

[Karatsuba's primary article](https://doi.org/10.1070/IM1985v024n03ABEH001246), *Zeros of the function \(\zeta(s)\) on short intervals of the critical line*, Math. USSR-Izv. 24 (1985), 523--537, supplies the seed. Its main theorem on printed p. 524 takes fixed \(0<\varepsilon\le0.001\), \(H=T^{27/82+\varepsilon}\), and gives a positive constant times \(H\log T\) odd-order critical zeros for every sufficiently large \(T\). The abstract's broader wording must not override this full-theorem parameter range.

The potentially fatal count ambiguity is resolved by printed p. 536, section 12. The proof constructs sign-change intervals, then extracts a disjoint subcollection of expanded intervals, each containing an odd-order critical zero. This counts support points once, irrespective of possible multiplicity conventions in other papers. The theorem and final counting text were independently read; the p. 536 argument was independently rendered and visually inspected.

The cached primary PDF has SHA-256:

    af5d1c40afeb3cbbe24286427a26dafefaa09c25618c371844b9923a2ec20c55

Its local path is [source-cache/karatsuba-1985-short-interval-odd-zeros.pdf](source-cache/karatsuba-1985-short-interval-odd-zeros.pdf); official metadata and access are at [MathNet](https://www.mathnet.ru/eng/im1456). The independent inspection image is retained privately at tmp/parity-independent-audit/karatsuba-p536.png.

For a fully specified fixed seed exponent one can choose

$$
\alpha=\frac{33}{100}
=\frac{27}{82}+\frac3{4100},
\qquad 0<\frac3{4100}<0.001.
$$

Alternatively, Selberg's theorem as restated in Karatsuba's Theorem B on p. 523 permits \(\alpha=0.51\). Either is below the target cosine threshold. The original Selberg article was not independently acquired in this audit; using Karatsuba directly avoids that additional source claim.

The classical analytic estimates are imported. This audit checks their relevant conclusion and count convention; it does not re-prove the trigonometric-sum estimates or compute their implicit constants.

## 3. Interval packing and normalization

Assume the fixed seed supplies constants \(a>0,U_a\) such that

$$
O(U,U^\alpha)\ge aU^\alpha\log U
\qquad(U\ge U_a),
$$

where the count uses \((U,U+U^\alpha]\). An open-endpoint theorem is sufficient after a reserve: at most two distinct support points change at the endpoints of a seed interval.

Fix \(\theta\in(\alpha,1)\), set \(H=T^\theta\), and recursively place complete seed intervals by \(U_0=T\), \(U_{j+1}=U_j+U_j^\alpha\). Stop with the largest \(J\) satisfying \(U_J\le T+H\). The intervals \((U_j,U_{j+1}]\), \(0\le j<J\), are disjoint. The omitted tail has length less than \((T+H)^\alpha\le(2T)^\alpha=o(H)\). Therefore

$$
\sum_{j<J}U_j^\alpha=H-o(H),
\qquad \log U_j\ge\log T,
$$

and summation gives \(O(T,H)\ge(a+o(1))H\log T\). Endpoint reserves cost \(O(J)\), with \(J\le H/T^\alpha\), so their ratio to \(H\log T\) tends to zero.

The ordinary zero-counting asymptotic gives

$$
N(T,H)=\frac{H\log T}{2\pi}+O(H+\log T)
\sim\frac{H\log T}{2\pi}.
$$

Consequently any suitably reserved \(0<\kappa<2\pi a\) works in

$$
\liminf_{T\to\infty}\frac{O(T,T^\theta)}{N(T,T^\theta)}
\ge\kappa
$$

for every fixed \(\theta\in(\alpha,1)\). The same \(\kappa\) can be selected from the fixed seed once. The onset height may depend on \(\theta\). This does not give uniformity for an exponent \(\theta(T)\) approaching \(\alpha\); no such uniformity is needed.

The functional equation maps \(\rho\) to \(1-\bar\rho\), preserving ordinate and multiplicity. Thus restriction to a half-open ordinate interval preserves the encoded conjugation symmetry. The denominator includes all zero copies, as required by Wang's theorem.

## 4. Legal analytic transfer

[Wang's arXiv:2609.07918v1](https://arxiv.org/abs/2609.07918v1), Theorem 2.2 and the subsequent weight-removal argument, apply to fixed support \(0<\lambda<\theta<1\). For each fixed smooth density the normalized error is

$$
O_f\!\left((\log T)^{-1}+T^{\lambda-\theta}\log T\right)=o(1).
$$

The rational pair weight is removed by an exact identity involving a test function and its second derivative, not by approximation. The inherited transfer audit records that identity and the all-zero multiplicity and complex-square conventions.

The cosine density has limiting functional value

$$
q(\lambda)=\frac\lambda2+\frac1{\sqrt2}\cot(\lambda/\sqrt2),
\qquad c(\lambda)=2-q(\lambda).
$$

The admissible positive density exists for every \(0<\lambda<1\). The sign of \(c(\lambda)\) is not a hypothesis of the arithmetic estimate.

Apply the finite inequalities at fixed smooth density, discard only \(\mathcal D\ge0\), and first let \(T\to\infty\). Improve the smooth approximation at fixed \(\lambda\), then let \(\lambda\uparrow\theta\). The lower bound on \(O/N\) does not depend on either test parameter. This yields, for every fixed \(\theta>\alpha\),

$$
\liminf\frac{S(T,T^\theta)}{N(T,T^\theta)}
\ge\max\left\{0,c(\theta),\frac{c(\theta)+2\kappa}{3}\right\},
$$

$$
\liminf\frac{D_Z(T,T^\theta)}{N(T,T^\theta)}
\ge\max\left\{\kappa,\frac{1+c(\theta)}2,
\frac{3+2c(\theta)+\kappa}{6}\right\}.
$$

Only elementary liminf/limsup inequalities at fixed tests are used. Substituting \(\lambda=\theta\) into the error term would be invalid. Just below the old positivity root, a fixed \(\lambda<\theta\) sufficiently close to \(\theta\) preserves the positive margin; no increased Fourier support is asserted.

## 5. Exact scope of the threshold conclusion

Let \(\theta_0\) be the unique root of \(c\) in \((0,1)\). Wang reports \(\theta_0=0.550193964744154\ldots\); this is an inherited decimal identifying the old root, not a newly computed output. Direct differentiation gives

$$
c'(\theta)=\frac12\cot^2(\theta/\sqrt2)>0.
$$

At \(\theta_0\) the new lower bound is at least \(2\kappa/3>0\). By continuity, some fixed \(\theta_1\in(\alpha,\theta_0)\) satisfies \(c(\theta_1)>-\kappa\), and therefore

$$
\liminf_{T\to\infty}
\frac{S(T,T^{\theta_1})}{N(T,T^{\theta_1})}
\ge\frac\kappa3>0.
$$

The declaration's choice \(\alpha=51/100\) also allows a wholly analytic root comparison, without treating the displayed decimal as a certificate. For \(x=\alpha/\sqrt2\), the positive lower bound \(\cos x\ge1-x^2/2\) and \(\sin x\le x\) imply

$$
c(\alpha)\le2-\frac1\alpha-\frac\alpha4
=-\frac{1801}{20400}<0.
$$

The inequality \(\tan x>x\) gives \(c(1)>1/2\), while
\(0<c'(\theta)<1/\theta^2\le10000/2601<4\) on \([\alpha,1]\). Thus \(\alpha<\theta_0<1\) and

$$
\delta=\min\{(\theta_0-\alpha)/2,\kappa/4\}>0,
\qquad \theta_1=\theta_0-\delta
$$

give \(c(\theta_1)>-\kappa\). These are paper comparisons; neither \(\theta_1\) nor \(\kappa\) is assigned a numerical value.

This is a strict extension of the cosine simplicity positivity range. It persists for each fixed larger exponent. Selecting \(\theta_1\) closer to \(\theta_0\), with \(c(\theta_1)>-\kappa/2\), also makes the distinct companion strictly greater than one half.

This does not assert positivity for every \(\theta>\alpha\): \(c(\theta)+2\kappa\) can remain negative away from the old root. It supplies no new decimal exponent, useful finite onset height, RH, universal simplicity, or improved global record. Nor does it improve the threshold for merely having a positive distinct proportion; the classical odd seed already does so on shorter intervals.

## 6. Prior-art and the short-mollifier challenge

The historical every-interval simplicity threshold \(0.552\) is stated in Steuding's [archived dissertation](https://webdoc.sub.gwdg.de/ebook/e/1999/steuding/253563305.pdf), printed p. 11, and is the comparator cited by Wang. Statements about one simple zero, possibly off the critical line, and statements for almost all intervals are not interchangeable with a positive critical proportion in every interval.

The competing lead [Conrey--Farmer--Kwan--Lin--Turnage-Butterbaugh, *Short mollifiers of the Riemann zeta-function*](https://arxiv.org/html/2508.11108v1), section 2.1, imports a critical-zero proportion. Theorem 1 optimizes that count with arbitrarily short mollifiers; section 7 does not introduce an every-short-interval simplicity theorem. High-degree derivative combinations are essential in the small-mollifier limit.

Primary sources confirm the count distinction. [Conrey--Iwaniec--Soundararajan](https://aimath.org/~kaur/publications/78.pdf), printed p. 176, explains that using only the function and first derivative permits a simple-zero conclusion. [Pratt--Robles--Zaharescu--Zeindler](https://link.springer.com/article/10.1007/s40687-019-0199-8) identifies the linear-\(Q\) specialization for simple critical zeros. Arbitrary degree cannot silently inherit this simplicity argument.

This closes the objection that the stated CFKL theorem already proves the proposed every-interval simplicity conclusion. It does not prove that no adaptation of CFKL could do so. Localization of its full moment formula and a multiplicity-sensitive detector would be separate work. Neither is an input here.

Version caution: the nominal arXiv v1 HTML inspected on 2026-09-12 displays a 2026 date; the [author-hosted PDF](https://aimath.org/~kaur/publications/110.pdf) displays August 18, 2025. Detailed replay should pin actual PDF bytes.

The bounded search combined Wang, Karatsuba, odd multiplicity, simple critical zeros, the old numerical threshold, and short mollifiers. It did not locate a primary statement of this parity transfer or its below-root conclusion. The combination is a candidate new deduction; this is not an exhaustive priority determination.

## 7. Declaration-ready validation boundaries

A scoped next experiment can test the exact slack identities, multiplicity cases, and declared symbolic transfer. Its claim should be the qualitative theorem above, with \(\kappa\) an unspecified positive constant from a fixed cited seed.

Meaningful adversarial cases include a real double point, a real triple point, a high odd multiplicity, a simple nonreal conjugate pair, a repeated nonreal pair, no simple real support, and mixtures. The wrong distinct half-sum claim has the explicit triple-point counterexample. Removing off-line multiplicity, interpreting \(O\) as weighted mass, or using the arithmetic estimate at \(\lambda=\theta\) must fail.

No numerical classical density constant should be invented by assigning an arbitrary small decimal. It requires a justified extraction from the analytic proof, including constants and onset height. No numerical experiment was run during this audit.
