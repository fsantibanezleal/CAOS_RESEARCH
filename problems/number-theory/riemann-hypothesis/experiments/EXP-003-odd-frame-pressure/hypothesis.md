# EXP-003: odd-frame amplification and a bounded pressure-certificate search

Declared: 2026-09-12. Device: CPU. Baseline: release `08660dc`.
Status at declaration: paper derivation independently checked; numerical stages unexecuted.
This declaration must be reviewed and committed before implementation or computation.

## Question, motivation, and falsifiable predictions

Can pair-disjoint triples inside a longer odd frame strengthen the complete positive
short-interval curve proved in [EXP-002](../EXP-002-short-interval-stability/verdict.md),
using the same certified kernel energy? After that improvement, can a new two-variable
pressure certificate increase the illustrative gain by more than 25%?

The two stages have separate outcomes. Stage A predicts a stronger theorem without a
new geometric search. Stage B predicts a further quantitative improvement under a fixed
search budget. Failure of Stage B does not invalidate an independently confirmed Stage A.
The motivation and imported analytic premises are recorded in the
[pressure-frame prior-art dossier](../../context/2026-09-12-pressure-frame-prior-art.md),
[successor review](../../context/2026-09-12-original-and-successor-review.md), and
[Wang transfer audit](../../context/2026-09-12-wang-transfer-audit.md).

Write

$$
c=c(\theta)=2-\frac\theta2-\frac1{\sqrt2}\cot(\theta/\sqrt2),
\qquad \theta_0<\theta<1,
$$

where $\theta_0$ is the unique zero of $c$ on $(0,1)$. Let $K_\theta$ be the
normalized cosine-density kernel defined in the EXP-002 proof, and put

$$
E_3(u,v)=2\{K_\theta(u)^2+K_\theta(v)^2+K_\theta(u+v)^2\},
\qquad u,v\ge0.
$$

These squares have real arguments. They must not be substituted for the distinct
complex-square convention in the full zero-pair sum $Q$.

Stage A assumes an already proved compact energy bound $E_3\ge d$ when $u+v\le R$,
with $0<d\le1$, $R>2/c$, and an integer $k>1$ satisfying $kd\le1$. Its prediction is

$$
\liminf_{T\to\infty}\frac{N_0^s(T,T^\theta)}{N(T,T^\theta)}
\ge c_A:=c+\frac{kd}{2k+1-kd}\left(c-\frac2R\right).
\tag{A}
$$

Here $N$ counts all zero copies in $(T,T+T^\theta]$, and $N_0^s$ counts simple
critical-line zeros. The predicted distinct-zero companion is $(1+c_A)/2$.
The existing EXP-002 coefficient is $d/(3-d)$, and the exact improvement test is

$$
\frac{kd}{2k+1-kd}-\frac d{3-d}
=\frac{d(k-1)}{(2k+1-kd)(3-d)}>0.
\tag{B}
$$

The explicit analytic $d$ supplied by EXP-002 is less than $1/4$: its $b\le q/2$
and $B>q$ imply $2(b/B)^2<1/2$. Thus $k=2$ is available throughout the complete
positive curve. This is the whole-curve prediction; a single numerical example is not
its proof.

The exact Stage A reproduction example is

$$
\theta=\frac34,\qquad R=\frac{21}4,\qquad d=\frac1{7000},\qquad
k=7000,\qquad M=2k+1=14001.
$$

It reuses EXP-002's 48,761-node certificate, with zero unresolved boxes, and predicts

$$
g_A:=c_A-c=\frac d2\left(c-\frac2R\right)
=\frac{c-8/21}{14000}.
\tag{C}
$$

EXP-001 already brackets $c(3/4)=0.4190750129754243337345536107\ldots$.
The published EXP-002 example is $0.4190768284253039967366657875\ldots$.
New decimal values are to be generated and enclosed only after this declaration is
committed. The frozen EXP-002 artifacts and published manuscript remain provenance inputs.

## Stage A: invariant-first derivation to be completed and audited

For a unit-diagonal positive semidefinite Gram matrix $G$, define

$$
D(G)=\operatorname{tr}\Psi(G),\qquad
\Psi(t)=\begin{cases}(t-1)^2,&0\le t\le2,\\2t-3,&t\ge2,\end{cases}
\qquad E(G)=\sum_{i\ne j}|G_{ij}|^2.
$$

The imported spectral facts are $D(G)\ge\min\{1,E(G)\}$ and superadditivity
under disjoint principal-block pinching. The finite zero-operator inequalities are
$s\ge2N-Q+D(G)$ and $2N^d\ge3N-Q+D(G)$. These facts are prior inputs,
not new lemmas claimed by this experiment.

The compact certificate implies the all-gap pressure inequality

$$E_3(u,v)+\frac dR(u+v)\ge d.$$

For span at most $R$ the energy suffices; for larger span the pressure suffices.
In a frame of $M=2k+1$ consecutive simple points, select the triples
$(1,2,3),(3,4,5),\ldots,(2k-1,2k,2k+1)$. Although adjacent triples share a
vertex, their unordered pairs are disjoint. Their energies therefore sum to at most
the frame energy, and their spans telescope to the frame span $L_F$. Consequently

$$
E(G_F)+\frac dR L_F\ge kd\le1,
\qquad D(G_F)+\frac dR L_F\ge kd.
\tag{D}
$$

The second inference uses the unit cap explicitly. If $E(G_F)\le1$, use $D\ge E$;
if $E(G_F)>1$, use $D\ge1\ge kd$. It does not add the defects of overlapping
triples, which would require a different argument.

Average the $M$ disjoint full-frame partitions with starting offsets modulo $M$.
Across all offsets there are exactly $(s-M+1)_+$ complete frames. For ordered
simple points with total span $L$, the sum of these frame spans is at most
$(M-1)L$. Thus, with $\alpha=kd/M$,

$$
D(G)\ge\alpha(s-M+1)-\frac{2\alpha}{R}L.
\tag{E}
$$

For $s<M$, the weaker displayed right-hand side is nonpositive and remains valid.
The small-index tests must cover $s<M$, $s=M$, offset endpoints, coincident gaps
in the certificate domain, pair incidence, and the exact span coefficients.

Combining (E) with the finite zero-operator inequalities, the fixed-test limit
$Q/N\to\mathcal C(f)$, and $L\le X_T\sim N$, and then taking the permitted
approximation limits $\mathcal C(f)\to2-c$, gives (A). The distinct companion must be
derived from the stronger finite inequality, not inferred by elementary counting
from the simple-critical result alone. The independently reviewed EXP-002 limiting
procedure remains mandatory: fix all parameters and a smooth kernel with Fourier
support $\lambda<\theta$, take $T\to\infty$, and only then approach the sharp
cosine profile and $\lambda\uparrow\theta$.

At the endpoint $kd=1$, keep $k$ fixed and first use every compact energy level
$0<\delta<d$. This gives $k\delta<1$ for smooth approximations; take the final
$\delta\uparrow d$ limit after the large-height and approximation limits.

## Stage B: a rational two-variable pressure certificate

At the same fixed $\theta=3/4$, search for positive rational $p,\epsilon$ such that

$$E_3(u,v)+p(u+v)\ge\epsilon\qquad(u,v\ge0).\tag{P}$$

The finite certification radius is derived internally as
$R_{\mathrm{cut}}=\epsilon/p$, not supplied independently. Exact pressure proves
(P) outside that radius. A certificate must exhaust the closed triangle
$u,v\ge0$, $u+v\le R_{\mathrm{cut}}$, including its boundary. For this bounded
campaign require $R_{\mathrm{cut}}\le12$. This retains a compact range suitable
for the existing rigorous sinc-Taylor remainder method; any insufficient remainder
bound produces an unresolved cell, never a silently relaxed enclosure.

For an integer $k\ge2$ with $k\epsilon\le1$, the same odd-frame proof predicts

$$
c_B=c+g_B,\qquad
g_B=\frac{k(\epsilon c-2p)}{2k+1-k\epsilon}.
\tag{F}
$$

A positive gain requires $\epsilon c>2p$. For fixed $p,\epsilon$ satisfying
this condition, the gain increases with admissible $k$, so the cap-optimal integer
is $k=\lfloor1/\epsilon\rfloor$. This exact invariant eliminates an unnecessary
integer search. Candidates with $\epsilon>1/2$ are outside this campaign.

The declared useful-improvement target is

$$g_B>\frac54g_A.\tag{G}$$

This compares gains above the same Wang baseline, not headline proportions. Exact
rational parameter checks and outward-rounded bounds for $c$ must establish (G)
before a candidate receives certification time. The terminal result must also
establish (G) with outward bounds; floating estimates cannot discharge this gate.

For smoothing, keep $p,\epsilon,k$ fixed and use every $\epsilon'<\epsilon$
close enough to retain positive gain. Uniform real-kernel convergence preserves
the pressure bound with $\epsilon'$ on the fixed compact triangle; outside it,
pressure alone is already at least $\epsilon$. Take fixed-test height limits and
smooth-approximation limits before $\epsilon'\uparrow\epsilon$. The predicted
distinct companion is $(1+c_B)/2$ by the same finite operator argument.

## Premise dependencies and source-complete gate

| Premise | Supporting record or required gate |
|---|---|
| Exact baseline and kernel algebra | [EXP-001 verdict](../EXP-001-source-and-constant-audit/verdict.md), with its canonical UTF-8/LF artifact and rational enclosures |
| Finite Hilbert stability, pinching, distinct inequality, lawful support limits | [EXP-002 proof](../EXP-002-short-interval-stability/mathematical-proof.md), [verdict](../EXP-002-short-interval-stability/verdict.md), and [adversarial audit](../EXP-002-short-interval-stability/adversarial-audit.md) |
| Reused $d=1/7000$ energy bound | EXP-002 `artifacts/triangle-certificate.json` and its 160-bit discovery plus 256-bit sinc-Taylor replay; verify committed source hashes before reuse |
| Wang pair-correlation theorem and normalization | [Wang transfer audit](../../context/2026-09-12-wang-transfer-audit.md), dependent on [arXiv:2609.07918v1](https://arxiv.org/abs/2609.07918v1) |
| Odd-frame assembly and resulting stronger short-interval theorem | This experiment's hypothesis; paper derivation checked independently, final proof, tests, and adversarial verdict still required |
| New pressure floor and more than 25% gain improvement | Unproved Stage B prediction; no numerical experiment has yet been run |
| Priority of the scoped odd-frame short-interval consequence | A source-search question, not a theorem; the [pressure-frame dossier](../../context/2026-09-12-pressure-frame-prior-art.md) reports no matching short-interval consequence in the inspected sources |

The known pressure framework and spectral defect are attributed explicitly to
[Ainta](https://github.com/ainta/zeta-simple-zeros/tree/040c5e899e658aed7b56a2a87f501798fe10761d),
[trmdy](https://github.com/trmdy/zeta-simple-zeros-673137/tree/1610b97b7895ff34982260f8dcaf04a0f7b82cf7),
[tawanerguo](https://github.com/tawanerguo-cn/zeta-simple-zeros/tree/45149f6d403059a71be73c5e3f884cee7cd62b20),
and the more recent
[Yuhang Shi inspected revision](https://github.com/yuhangshi888/zeta-simple-zeros-673316977/tree/1aeda8e9f0678166a824c75313a813b09eb478cd)
([earlier archived release DOI](https://doi.org/10.5281/zenodo.21926962)). Their global candidate
headlines and large imported certificates are not analytic premises of EXP-003.
The spectrum-energy envelope already asserted in this lineage is excluded from
new-theorem claims, even if an unrestricted proof is easier to give here.

The independent [source-complete report](../../context/2026-09-12-pressure-frame-prior-art.md)
has now recorded its inspection of the directly relevant pressure, refined deduction,
proof, closing remarks, claim ledger, and bibliography material in the pinned successor
sources. It treats the alternating schedule as a simple instance of known global
capacity methods and limits the prospective contribution to the stronger short-interval
consequence. The source reviewer also reports successful byte-count and SHA-256 checks
for all 26 documents and six licensed snapshots in the updated manifest. Before machine
work, commit the complete preflight with this declaration. A prior identical assembly
retracts the corresponding novelty claim even if the inequalities remain correct.

## Budget, checkpoints, and stop rules

1. Stage A uses exact symbolic identities, small-index incidence/span checks, and an
   existing-certificate replay. Its arithmetic-and-replay budget is one minute; any
   discrepancy stops the dependent stage until understood, and a budget stop is
   inconclusive for the replay. No fresh geometric search is needed for Stage A.
2. Stage B allows one deterministic floating exploration, seed zero where a seed is
   needed, capped at 60 seconds. It may propose at most three rational candidates.
   Persist the full candidate list and ordering before certification. A failed candidate
   is not replaced by an undeclared fourth attempt. Samples select parameters only.
3. Each candidate has a ten-minute combined construction-and-replay budget and at most
   two million subdivision nodes. There are at most three such attempts, so the
   expensive campaign is bounded by thirty minutes plus the one-minute exploration
   and cheap checks. No GPU run or larger-dimensional certificate is authorized here.
4. Before a run that could exceed five minutes, force a tiny run to stop after ten
   nodes. Confirm flushed progress within seconds, an exact resumable checkpoint,
   successful resume, and rejection of a checkpoint with mismatched parameters.
   Checkpoints must retain rational parameters, pending cells, proof-tree state,
   precision/evaluator metadata, and source identity. Flush a checkpoint and progress
   at least every ten seconds or every thousand nodes, whichever occurs first.
5. Construct complete certificates with outward-rounded Arb arithmetic at 160 bits.
   Replay every accepted cell at 256 bits using the independently derived sinc-Taylor
   evaluator and rigorous remainder. Shared geometric logic and shared Arb dependency
   must remain explicit; this is not an independent full verifier or a Lean proof.
6. On timeout, node cap, unresolved cell, malformed partition, insufficient precision,
   nonreal residue, mismatch, or failed replay, persist a checkpoint and an
   `inconclusive` or `refuted` candidate result as appropriate. Do not extend the
   budget automatically. A changed objective or expanded campaign requires a new
   committed declaration.

The runner must be headless, use the repository `.venv`, and exit nonzero on a failed
check or incomplete certification. All canonical mathematical outputs use explicit
UTF-8 and LF, deterministic ordering, and exact rational parameters. Elapsed-time and
progress logs are operational metadata; canonical result and certificate files do not
include nondeterministic timestamps. Runs write to a fresh output directory. They must not overwrite EXP-001,
EXP-002, their committed artifacts, or the frozen published manuscript.

## Adversarial checks, verdict meanings, and optional directions

The cheap decisive invariants are pair incidence, telescoping spans, the unit spectral
cap, and monotonicity in $k$. Plain shifted $m$-point span counting loses a factor
$m-1$ in total span and is not automatically an improvement. Summing overlapping
triple defects without a valid pinching argument is prohibited. In particular, the
odd-frame example has $M=14001$; the weaker all-consecutive-triple construction with
$M=14002$ has a different coefficient and cannot be conflated with it.

Stage A is `confirmed` only after a complete proof, exact formula and boundary tests,
verified reuse of the earlier certificate, independent adversarial review, and a
scoped prior-art audit. A counterexample or invalid inference refutes the proposed
assembly; failure to establish a premise is inconclusive. An already published matching
result makes the novelty outcome null without making the mathematics false.

Stage B is `confirmed` for its declared target only if at least one candidate has a
complete two-path certificate, lawful analytic transfer, and the strict gain comparison
(G). A valid certificate at or below that target is retained as a mathematical result but is
null for the useful-improvement prediction. A certified violating point refutes that
candidate, not all pressure inequalities. Exhausting the sampled design space or the
resource budget cannot prove that no stronger certificate exists. Stage outcomes must
be recorded separately, including rejected parameters and reasons.

The refutation attempt must inspect zero gaps, the cutoff boundary, removable kernel
singularities, small point counts, missing or duplicated pairs, offset endpoint losses,
the pressure coefficient, the condition $k\epsilon\le1$, the full complex-square
pair sum, distinct-zero multiplicities, smoothing, and the order of limits. The
three-point root obstruction and the known spectral and pressure tools retain their
source attribution throughout the proof and any later manuscript.

An optional four-point direction may be considered only after the two-variable stage
has demonstrated merit and a new rationally stated arithmetic-progression obstruction
criterion has been derived and adversarially checked. It does not authorize a heavy
four-point campaign. Any new numerical family or extra budget must first receive its
own committed hypothesis or amendment with explicit scope and stop rules.

Expected durable outputs after authorization are `mathematical-proof.md`, an independent
`adversarial-audit.md`, deterministic `run.py`, exact tests, candidate and certificate
artifacts with hashes, and a separate-stage `verdict.md`. Publication is a later decision
based on the completed evidence. The intended result is an asymptotic short-interval
refinement. It supplies no effective height threshold, no uniformity near $\theta_0$,
no better positivity exponent, no global record, and no solution of RH.
