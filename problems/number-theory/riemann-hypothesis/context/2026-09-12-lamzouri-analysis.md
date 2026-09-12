# Lamzouri mathematical review and independently derived barriers

Review date: 2026-09-12. Analyst: Codex research subagent. This is a working
research note, not a publication or a novelty certificate.

## Source snapshot

- [Lamzouri arXiv abstract](https://arxiv.org/abs/2609.02882): v1 submitted
  2026-09-02 17:56:49 UTC; v2 submitted 2026-09-08 17:55:54 UTC.
- [Version 2 HTML](https://arxiv.org/html/2609.02882v2), 17-page PDF.
- Downloaded v1/v2 PDFs and original source archives under `source-cache/`.
  Exact URLs, versions, retrieval dates, byte counts and SHA-256 hashes are in
  the portable `source-manifest.json` in this directory.
- arXiv license metadata: `http://arxiv.org/licenses/nonexclusive-distrib/1.0/`.
  This is the arXiv perpetual nonexclusive distribution license, not a Creative
  Commons grant. Retain this distinction in the repository source manifest.

## Source results and boundary (concise sourced summary)

Lamzouri v2 Theorem 1.1 establishes these unconditional limiting lower bounds:

\[
C_0=\frac32-\frac1{\sqrt2}\cot(1/\sqrt2),\quad
C_1=(1+C_0)/2,\quad
C_2=\frac{1+2\sqrt2+2C_0}{3+2\sqrt2}.
\]

They respectively bound simple critical zeros; distinct zeros and the average
of simple/critical proportions; and the union of simple or critical zeros.
The two latter simplicity/location tradeoffs were added in v2. The mechanism
is Proposition 2.1 plus Lemmas 3.1–3.2. Remark 3.4 records the optimality of its
Montgomery–Taylor kernel constant. Appendix A's formal theorem certificates
assume the unconditional pair-correlation input and Riemann–von Mangoldt
asymptotic. Thus this is not an assumption-free formalization of all zeta
analysis. Proposition 2.1 itself has an unconditional formal certificate.

The decisive earlier analytic source is
[Baluyot–Goldston–Suriajaya–Turnage-Butterbaugh](https://arxiv.org/abs/2306.04799),
Lemma 5 (published in Acta Arith. 214 (2024), 357–376). The extremal source is
[Carneiro–Chandee–Littmann–Milinovich](https://arxiv.org/pdf/1406.5462),
Section 3.5, Corollary 14, page 24 of the arXiv PDF. It solves the nonnegative
bandlimited one-delta problem, including uniqueness, and attributes the
original optimizer to Montgomery–Taylor.

## Independent audit: reconstructing the main mechanism

Write \(K=\widehat{\eta^2}\), with \(\eta\) real, even, compactly supported,
and \(\int\eta^2=1\). For a conjugation-invariant finite multiset \(Z\), put

\[
f_z(u)=\eta(u)e^{-2\pi iuz},\quad
F=\sum_{z\in Z}f_z\otimes f_z,\quad
Q=\sum_{z,s\in Z}K(z-s)^2.
\]

Conjugation invariance, not termwise positivity, gives \(Q=\|F\|^2\).
For nonreal \(z\), write \(f_z=g_z+ih_z\), where
\(g_z=(f_z+f_{\bar z})/2\), \(h_z=(f_z-f_{\bar z})/(2i)\).
Then \(\|g_z\|^2-\|h_z\|^2=1\). The additional identity
\(\langle g_z,h_z\rangle=0\) follows directly from evenness of \(\eta\):
the integrand is an imaginary multiple of an odd real function. This extra
identity is a possible place to look beyond aggregate trace constraints.

Let \(N=|Z|\) count copies, \(n\) count simple real points, \(r\) count distinct
multiple real points, and \(k\) count nonreal conjugate pairs. A nested
Gram–Schmidt basis has blocks of lengths \(d=r+k\), \(n\), and \(k\). Denote
the corresponding diagonal tensor coefficients by \(\alpha_j\), and their
block sums by \(S_U,S_M,S_-\). Direct projection identities give

\[
Q\ge\sum_j\alpha_j^2,\quad S_U\ge N-n\ge2d,\quad
S_M\le n,\quad\alpha_j\le0\ (j\text{ in last block}),\quad
S_U+S_M+S_-=N.
\]

The simple-real bound follows immediately by comparing squared coefficients
with affine tangents at 2 on the first block and 1 on the middle block.
No claim that \(K(z-s)^2\ge0\) term by term is used or valid in general.

For zeta zeros, the finite multiset is
\(Z_T=\{i(\rho-1/2)\log T/(2\pi):0<\operatorname{Im}\rho\le T\}\).
The functional equation supplies its conjugation symmetry. Real points of
\(Z_T\) are precisely critical-line zeros, so the translation is exact.

## Independent simplified derivation of the full aggregate envelope

For any \(t\ge1\), use \(a^2\ge2ta-t^2\) in the first block,
\(a^2\ge2a-1\) in the middle block, and \(a^2\ge2a\) for the nonpositive
last block. Hence

\[
Q\ge2N+(2t-2)S_U-t^2d-n
 \ge2tN-(2t-1)n-t^2d.
\]

If \(d>0\), optimize at \(t=(N-n)/d\ge2\):

\[
\boxed{Q\ge n+\frac{(N-n)^2}{d}.}
\]

For \(d=0\), \(N=n\), and \(Q\ge N\). This proof avoids differentiating
or optimizing a three-variable constrained program.

Set \(x=N-n\), \(\Delta=x-2d\ge0\). Then

\[
\Delta=\sum_{x\in Z\cap\mathbb R\atop m_x\ge2}(m_x-2)
  +2\sum_{\{z,\bar z\}\subset Z\setminus\mathbb R}(m_z-1),
\]

where the first sum and the pair sum count distinct locations/orbits. The
envelope has the exact scalar decomposition

\[
Q-N\ge(3+2\sqrt2)\Delta+
 \frac{\{x-(1+\sqrt2)\Delta\}^2}{x-\Delta}.
\]

Consequently \(\Delta\le(Q-N)/(3+2\sqrt2)\). If \(B_m\) counts copies at
nonreal locations having multiplicity at least \(m\ge2\), then

\[
B_m\le\frac{m}{m-1}\Delta
 \le\frac{m}{m-1}\frac{Q-N}{3+2\sqrt2}.
\]

The corresponding asymptotic zeta bound follows by substituting
\(Q/N\to C_{\rm MT}=2-C_0\). This is a useful joint-tail formulation,
but the generic parameter inequality is PRIOR ART, not our discovery: the
parallel formal-source auditor located `rank_trace_mult_k_le` and
`TightMult.lean` in the current Anthropic formal-math source. Those already
supply an arbitrary-parameter multiplicity inequality and abstract sharpness.
Moreover, the existing unrefereed
[low-multiplicity draft](https://raw.githubusercontent.com/zach7036/riemann-hypothesis-research/main/publication/low-multiplicity-zeta/THEOREM.md)
explicitly uses \((3-2\sqrt2)(C_{\rm MT}-1)\). Novelty must not be inferred
from its absence in Lamzouri's theorem statement.

## Why re-optimizing the three existing blocks cannot improve the union bound

Normalize \(N=1\), and let \(u\) be the mass of simple or real points.
Multiplicity bookkeeping gives \(d\le(1+u-2n)/4\). Therefore

\[
Q\ge n+\frac{4(1-n)^2}{1+u-2n}.
\]

With \(b=1-u\), \(x=1-n\), the right side equals
\(1+x+b+b^2/(2x-b)\). Its minimum occurs at
\(x=(1+\sqrt2)b/2\), and is

\[
1+(3/2+\sqrt2)b.
\]

This exactly recovers \(u\ge1-2(Q-1)/(3+2\sqrt2)\), i.e. Lamzouri's
\(C_2\). Thus there is no improvement available from solving the same
aggregate scalar optimization more accurately. To surpass it, retain new
exponential/Gram structure or stronger analytic information. The alternative
coefficient 3 (which would give \((2+C_0)/3\)) is not implied by these blocks.

## Independent elementary extremal proof and sharp stability

For normalized real \(f\in L^2(I)\), \(I=[-1/2,1/2]\), define

\[
\mathcal C(f)=\int_I f(x)^2\,dx+
 \iint_{I^2}|x-y|f(x)f(y)\,dx\,dy.
\]

For the even profiles in the paper this equals the convolution expression
\((f*f)(0)+2\int_0^1u(f*f)(u)\,du\). Consider

\[
f_*(x)=\frac{\cos(\sqrt2x)}{\sqrt2\sin(1/\sqrt2)}.
\]

Let \(J(x)=\int_I|x-y|f_*(y)\,dy\). Since \(J''=2f_*\) and
\(f_*''=-2f_*\), \(f_*+J\) is affine; evenness makes it constant. Evaluating
at \(x=1/2\), using \(\int f_*=1\) and \(\int yf_*(y)\,dy=0\), gives
\(f_*+J=C_{\rm MT}\).

For \(h=f-f_*\), \(\int h=0\), put \(H(x)=\int_{-1/2}^xh(y)\,dy\).
Integration by parts twice gives

\[
\iint |x-y|h(x)h(y)\,dx\,dy=-2\int H(x)^2\,dx.
\]

The cross term vanishes because \(f_*+J\) is constant. Therefore

\[
\boxed{\mathcal C(f)-C_{\rm MT}=\|h\|_2^2-2\|H\|_2^2.}
\]

For general real profiles, Dirichlet Poincare gives the sharp lower bound
\((1-2/\pi^2)\|h\|_2^2\). For EVEN profiles, \(H\) is odd, so its first
available Dirichlet frequency is \(2\pi\), and

\[
\boxed{\mathcal C(f)-C_{\rm MT}\ge
 (1-1/(2\pi^2))\|f-f_*\|_2^2.}
\]

Sharpness in the even class follows from \(h(x)=\epsilon\cos(2\pi x)\).
Small nonzero \(\epsilon\) preserves positivity of \(f_*+h\). This establishes
both optimality and a quantitative closeness certificate without numerical
optimization. It is an independently derived explanatory result, not a
certified new theorem: prior extremal/reproducing-kernel work may already
contain equivalent stability in another norm.

## Analytic audit of smoothing and deweighting

Let \(f=\eta^2\in C_c^\infty((-1/2,1/2))\) and \(P=f*f\). The pair-correlation
weight is \(w(d)=4/(4-d^2)\). With \(z=id\log T/(2\pi)\),

\[
\widehat{P-P''/[4(\log T)^2]}(z)\,w(d)=\widehat P(z)=K(z)^2.
\]

The legitimate use of the theorem is to apply it separately to the TWO FIXED
functions \(P\) and \(P''\), then combine the results. Directly applying an
\(O_f\) asymptotic to a \(T\)-dependent test function is not justified by its
statement. The smooth cutoff is also essential at this step: the limiting
cosine profile has nonzero endpoint values, so second derivatives after
extension by zero contain boundary distributions. One fixes the cutoff,
lets \(T\to\infty\), and only afterwards removes the cutoff.

The deweighting correction is small for each fixed profile, but its implied
constant grows as smoothing shrinks. None of these asymptotics gives an
explicit verified numerical height threshold. Checking zeros to a large
finite height cannot prove the limiting proportion.

## Further live primary-source leads

- [Wang arXiv:2609.07918](https://arxiv.org/abs/2609.07918), submitted September
  7, applies Lamzouri's inequality in short intervals. Another agent is auditing
  it; do not claim short-interval extension as new without comparison.
- [trmdy contributor manuscript](https://raw.githubusercontent.com/trmdy/zeta-simple-zeros-673137/main/paper/main.tex)
  currently presents a 0.673200117... candidate, with an explicit theorem
  boundary importing the arbitrary-window and stability interfaces. Its title,
  author/provenance record, and constant changed beyond what the repository
  slug suggests. It cites `ainta/zeta-simple-zeros`,
  `tawanerguo-cn/zeta-simple-zeros`, and `npip99/zeta-zeros`. These are research
  claims requiring mathematical and certificate audit, not established record
  replacements merely because they display more digits.

No numerical counterexample search or GPU computation was performed in this
subtask. Numerical feasibility checks alone would not certify any new zeta
bound.
