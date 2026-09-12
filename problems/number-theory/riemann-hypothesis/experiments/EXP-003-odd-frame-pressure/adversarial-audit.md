# EXP-003 adversarial audit: finite operator and odd pressure frames

Date: 2026-09-12. Declaration: `8ed806d`.
Paper-audit outcome: no material defect found in the general pressure theorem or
the compact-certificate reuse deduction. Machine certificates and quantitative
acceptance are separate gates, recorded in the verdict and artifacts when available.

This record consolidates the independent finite-operator, frame-counting, and limit
checks supplied during the proof's development, together with a renewed inspection
of the inherited EXP-002 proof. The proof writer transcribed this record; the record
does not claim that transcription itself is an independent blind review. The
coordinating reviewer also inspected the completed proof, as recorded below. No
numerical experiment was run to establish the paper checks below.

Coordinating review completed on 2026-09-12: the reviewer read the full proof and this
audit and independently checked the rank-one operator products, signed positive-index
bound, min-max zero-eigenvalue accounting, odd-frame pair incidence, summed gap capacity,
distinct-zero lower-limit deduction, complex second-derivative weight removal,
$12\|f-f_\theta\|_1$ kernel-energy estimate, endpoint limit order, and explicit
triple numerator identity. No material mathematical defect was found. This completes
that paper-review gate; it does not certify a numerical search or replace its replay.

## 1. Exact finite operator: try to break the conjugation and signs

The inherited construction uses

$$
A=\sum_zm_z|v_z\rangle\langle v_{\bar z}|,
\qquad v_z(t)=\eta(t)e^{-2\pi izt},\qquad K=\widehat{\eta^2}.
$$

The conjugated index in the second slot is essential. With the inner product linear
in its second argument,

$$
\langle v_{\bar z},v_z\rangle=1,\qquad
\operatorname{tr}\bigl(|v_z\rangle\langle v_{\bar z}|
|v_w\rangle\langle v_{\bar w}|\bigr)
=K(w-z)K(z-w)=K(z-w)^2.
$$

These direct identities establish $\operatorname{tr}A=N$ and
$\operatorname{tr}A^2=Q$ with ordinary complex squares. Replacing the square by
$|K(z-w)|^2$ at nonreal arguments would change the analytic pair sum. No such
replacement occurs in the new proof.

The possible negative directions from off-line points were checked by expanding
a conjugate pair as $2m(|g\rangle\langle g|-|h\rangle\langle h|)$.
This gives at most one positive direction per pair. Together with the multiple-real
vectors it yields $n_+(A-P)\le r+b$. This bound does not require the off-line
points to be uniformly separated from the real axis, or the generating vectors to
be linearly independent.

Result: the inherited finite operator is valid for finite conjugation-invariant
multisets with arbitrary positive integer multiplicities. Positivity is asserted
only for the full Hilbert-Schmidt norm and the Gram matrix of simple real points.

## 2. Try singular matrices, extra zero eigenvalues, and large positive index

The min-max proof was checked with $m=\dim\mathcal H$ unrelated to the number
$s$ of simple columns. If $n_+(C)\le d<m$, the eigenvalue inequality is
$\lambda_i(P+C)\le p_{i+d}$ for $i\le m-d$. It implies

$$
\operatorname{tr}(P+C-2I)^2
\ge\sum_{j=1}^m(2-p_j)_+^2-4d.
$$

Every discarded summand is at most four because $p_j\ge0$. If $d\ge m$,
the same lower bound is nonpositive and therefore valid without a min-max step.
The identities

$$
(2-p)_+^2=\Psi(p)-2p+3,\qquad
\operatorname{tr}\Psi(P)-\operatorname{tr}\Psi(G)=m-s
$$

cancel the dimension terms exactly. The second identity includes all zero eigenvalues,
using $\Psi(0)=1$. It remains valid if $P$ or $G$ is singular, including $s=0$.

Result: no invertibility, rank equality, or hidden spectral-padding assumption is
needed. The stable inequality is the known Ainta inequality in the precise unit-column
case used here, not a new lemma.

## 3. Try to infer the distinct companion from a false count

The tempting inequality $D_Z\ge(N+s)/2$ is false for general multiplicities.
One support point of multiplicity three has $N=3$, $s=0$, and $D_Z=1<3/2$.
Thus the improved simple-critical proportion cannot by itself justify the proposed
distinct proportion by that shortcut.

The actual derivation retains the stronger finite inequality

$$Q\ge4N-3s-4r-4b+D(G).$$

Since $D_Z=s+r+2b$, the difference between its nondefect right-hand side and
$3N-2D_Z$ is exactly $N-s-2r\ge0$. Therefore

$$2D_Z\ge3N-Q+D(G).$$

If $D(G)\ge\alpha s-\beta L-O(1)$ and
$b_f=(c_f-\beta)/(1-\alpha)$ is the already proved simple bound, then

$$1+c_f+\alpha b_f-\beta=1+b_f.$$

Result: the distinct companion is valid through this signed finite operator argument.
The multiplicity counterexample refutes only the discarded shortcut.

## 4. Try to overcount overlapping triples

Convex pinching applies to disjoint principal blocks. It does not justify adding
defects of arbitrary overlapping triples. For example, in the four-by-four all-ones
Gram matrix, the full defect is eight, while the two consecutive three-by-three
all-ones blocks each have defect five. Their sum ten exceeds the full defect.
The spectral calculation is exact: an $m$-by-$m$ all-ones matrix has eigenvalues
$m,0,\ldots,0$, hence defect $\Psi(m)+(m-1)\Psi(0)$.

The odd-frame proof avoids this counterexample. Its triples have starts
$1,3,\ldots,2k-1$. They share at most one vertex and no unordered pair.
Only their pair energies are added, inside a single larger frame. Every selected
unordered pair consumes the same factor-two coefficient it has in the full frame
energy, at most once. The spans telescope to the entire frame span exactly.
Defect pinching is applied later, between disjoint full frames.

Result: there is no duplicated pair coefficient or unjustified overlapping-defect sum.
Zero gaps and coincident-point limits do not affect pair incidence or telescoping.

## 5. Try to misuse the unit spectral cap

The required implication is

$$E+P\ge A,\quad P\ge0,\quad0<A\le1\quad\Longrightarrow\quad D+P\ge A,$$

using $D\ge\min(1,E)$. The condition $k\epsilon\le1$ is therefore explicitly
required in every frame. It is not safe to infer $D\ge E$ for arbitrary frames.

An exact counterexample to that stronger inference is the three-by-three
equicorrelation matrix with all off-diagonal entries $3/5$. Its eigenvalues are
$11/5,2/5,2/5$, so

$$E=\frac{54}{25},\qquad D=\frac{53}{25}<E.$$

More elaborate known spectrum-energy envelopes could support other operating points,
but are not used or claimed as new in this experiment.

Result: the proof's unit cap is sufficient. The endpoint $k\epsilon=1$ is handled
through strict approximating targets, rather than applying an unsmoothed endpoint
directly to Wang's theorem.

## 6. Try to lose a shifted-frame factor or endpoint

There are $M=2k+1$ residue classes of frame starts modulo $M$. In one class, all
complete frames are disjoint. Across the classes, the start indices are exactly
$1,\ldots,s-M+1$ when $s\ge M$, and there are no complete frames otherwise.

Each adjacent global gap occurs in at most $M-1$ complete frame spans. Therefore

$$
\sum_F L_F\le(M-1)L,
\qquad
D(G)\ge\frac{k\epsilon}{M}(s-M+1)-\frac{(M-1)p}{M}L.
$$

For $s<M$, the displayed right-hand side is nonpositive; the nonnegativity of
$D(G)$ supplies the bound. For $s=M$, there is exactly one complete frame across
all offsets; averaging loses precisely a factor $M$, as the formula states.
Leftover singleton indices have zero defect and need no additional error term.

Solving the simple-zero inequality gives

$$c_{\mathrm{odd}}=c+\frac{k(\epsilon c-2p)}{2k+1-k\epsilon}.$$

With $d=1/7000$, $p=d/R$, and $k=7000$, the exact coefficient on $c-2/R$
is $1/14000$. The previously considered construction using all consecutive triples
has a different capacity cost and coefficient $1/14001$. Both are distinguishable;
the latter is not the proof of the former.

The independent frame-count reviewer obtained the same finite boundary loss and
coefficient. The planned small-index tests must verify incidence and gap counts,
including short and endpoint configurations, rather than simply restating the final
rational formula.

## 7. Try an illegal support limit or wrong normalized span

For each fixed smooth density with support strictly inside
$(-\lambda/2,\lambda/2)$, $\lambda<\theta$, Wang gives
$Q/N\to\mathcal C(f)$, not $Q/N\to2-c(\theta)$ directly. The latter main
term is obtained only after approximation to the limiting cosine density.

The normalized fixed-test error is
$O_f(1/\log T+T^{\lambda-\theta}\log T)=o(1)$. At $\lambda=\theta$
the displayed estimate would not vanish. The proof keeps $f,\lambda$ fixed during
each $T\to\infty$ limit and takes the approximation limits afterwards.

The actual normalized real span is at most $X_T=T^\theta\log T/(2\pi)$,
while $N=X_T+O(T^\theta+\log T)$ and hence $X_T/N\to1$. There is no extra
factor $\theta$, and no assumption that a sample-grid dimension differs from the
zero count by $O(\log T)$.

For pressure parameters $p,\epsilon$ with $k\epsilon\le1$, first fix
$\epsilon'<\epsilon$ and preserve $k,p$. Uniform kernel error at most
$\|f-f_\theta\|_1$ changes the triple energy by at most
$12\|f-f_\theta\|_1$. Thus the target $\epsilon'$ survives a sufficiently
close fixed smooth approximation. Finally let $\epsilon'\uparrow\epsilon$.
The denominator stays at least $M-1$, so the scalar limit is harmless.

Result: the proof is valid at the cap endpoint and gives a result for each fixed
$\theta$. It does not prove a uniform height threshold near $\theta_0$.

## 8. Try to overstate the whole-curve or numerical conclusion

For the EXP-002 analytic input, $d=(b/B)^2$ with $b\le q/2$ and $B>q$, so
$0<d<1/4$. Thus $k=2$ is admissible throughout the entire positive curve.
The exact difference of gain coefficients is

$$\frac{kd}{2k+1-kd}-\frac d{3-d}
=\frac{d(k-1)}{(2k+1-kd)(3-d)}>0.$$

This is a strict improvement relative to the same earlier compact energy input.
At $\theta=3/4$, the old certificate's bound $d=1/7000$, $R=21/4$ supplies an
exact Stage A corollary. A new floating-point optimization is unnecessary for that
claim, but the declared machine-replay and hash checks remain part of experiment
acceptance.

Stage B targets a gain strictly greater than $5/4$ of the Stage A gain. It does not
target a 25% increase in the whole proportion. Its rational cutoff is
$R_{\mathrm{cut}}=\epsilon/p$, and pressure alone controls larger spans.
The finite certificate must include all points of the closed triangle, including
zero gaps and its cutoff boundary. Kernel removable singularities must be evaluated
through a continuous formula, not a pole-containing quotient.

Result: the paper theorem explains what a complete Stage B certificate would imply.
It does not declare that such a certificate exists or that a sampled minimum proves it.
Partial coverage or exhausting three candidates cannot establish a universal negative
claim about pressure methods.

## 9. Numerical and publication gates that this audit does not replace

The numerical implementation is independently owned and must meet the committed
[hypothesis](hypothesis.md). In particular:

- Stage A must verify the inherited certificate and exact coefficients without
  modifying historical artifacts.
- Stage B must retain every candidate, enforce the fixed rational gain gate, and
  respect its combined ten-minute construction-and-replay budget and node cap.
- The old triangle verifier has no deadline/checkpoint interface for its full replay.
  The new pressure replay must therefore support the remaining budget and resumable
  state explicitly; copying an unbounded replay would violate the declaration.
- A flushed tiny-run checkpoint and valid resume must precede a potentially long run.
- The 160-bit construction and 256-bit sinc-Taylor replay must both cover every accepted
  leaf. They share geometric logic and Arb, so this is an independent evaluator rather
  than an independent full verifier.
- Canonical result bytes must be deterministic UTF-8/LF. Runtime progress belongs in
  separate operational logs.

These are outstanding validation requirements at the initial writing of this audit,
not reported completed tests. The verdict and artifacts are the source of truth for
their eventual outcome.

The [source-complete prior-art review](../../context/2026-09-12-pressure-frame-prior-art.md)
credits pressure, capacities, pinching, and spectral envelopes to the global successor
literature. It did not locate the exact stronger short-interval consequence, but the
alternating schedule is a simple instance of that existing framework. A missed or
concurrent equivalent result remains a priority risk.

The paper derivation survives the stated refutation attempts. Its analytic premises
remain Wang's inspected preprint and the cited classical zero-count and pair-correlation
inputs. The result does not solve RH, improve the positivity exponent, establish a
global record, or constitute an end-to-end formal verification. Publication should
follow the completed verdict, quantitative replay, and final proof review.
