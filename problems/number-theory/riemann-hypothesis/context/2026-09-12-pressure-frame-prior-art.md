# Pressure frames: prior art and the next short-interval question

Review date: 2026-09-12. This is a source preflight for a possible successor to
EXP-002, written before running a new experiment. It does not promote a new
constant to a validated result. The released version 0.01 preprint and its
frozen evidence remain unchanged.

The strongest feasible next question identified here is whether an alternating
cover by triples, assembled inside a larger Gram frame, improves the
short-interval consequence of the existing triangle certificate. Pressure
terms, larger frames, nonuniform edge weights, and boundary-aware packing all
have public global precedents. The prospective contribution is a stronger
short-interval consequence with complete normalization and certificate reuse,
not the invention of those finite methods.

Labels: **[V]** identifies a statement checked in a primary source, including
the exact scope of its proof; **[U]** identifies an external computation or
claim not independently reproduced here; **[C]** identifies the proposed new
local deduction awaiting its own experiment declaration and adversarial audit.
A source being archived is not a proof-verification event.

## 1. Immutable sources and review depth

The GitHub commit API was checked during this review. The first two heads
remain identical to the earlier source pins. Dates below are commit dates in
UTC, not claims about the first public appearance of every mathematical idea.

| Primary repository | Inspected head | Commit date | Relevant source |
|---|---|---|---|
| [Ainta](https://github.com/ainta/zeta-simple-zeros/tree/040c5e899e658aed7b56a2a87f501798fe10761d) | `040c5e899e658aed7b56a2a87f501798fe10761d` | August 11 | `docs/proof.md`, paper, triple gap and seven-point pressure |
| [trmdy](https://github.com/trmdy/zeta-simple-zeros-673137/tree/1610b97b7895ff34982260f8dcaf04a0f7b82cf7) | `1610b97b7895ff34982260f8dcaf04a0f7b82cf7` | August 12 | All proof, refined-deduction, nine-point, retuned-record and campaign-2 notes |
| [tawanerguo](https://github.com/tawanerguo-cn/zeta-simple-zeros/tree/45149f6d403059a71be73c5e3f884cee7cd62b20) | `45149f6d403059a71be73c5e3f884cee7cd62b20` | August 11 | Paper proof sections, trace envelope, Bellman certificate, global spectral dual |
| [npip99](https://github.com/npip99/zeta-zeros/tree/72a01ac5ea3837f2a4c4583d831f885d005f8af1) | `72a01ac5ea3837f2a4c4583d831f885d005f8af1` | August 12 | README and complete `docs/proof.md` |
| [Yuhang Shi](https://github.com/yuhangshi888/zeta-simple-zeros-673316977/tree/1aeda8e9f0678166a824c75313a813b09eb478cd) | `1aeda8e9f0678166a824c75313a813b09eb478cd` | September 11 | Paper's finite deduction, proof outline, claim ledger and formalization boundary |
| [teal-sea](https://github.com/teal-sea/zeta-lab/tree/c614e65188f0b5d73b342436383ae558fbd3aafd) | `c614e65188f0b5d73b342436383ae558fbd3aafd` | September 10 | Parametric bridge, four-point theorem and terminal pressure-tuning record |

The source-complete pass concerns the mathematical interfaces needed for the
proposed pressure-frame deduction. It does not mean that every source file or
every unrelated hunt in the large teal-sea tree was read. No upstream Lean
build, optimizer, or multi-million-box certificate was run in this preflight.

Two new complete MIT repository ZIPs, tawanerguo and Yuhang Shi, are preserved
with their licenses in `source-snapshots/`. Five additional primary documents
are in the ignored local `source-cache/`. Their immutable URLs, exact bytes and
SHA-256 hashes are appended to [the manifest](source-manifest.json). Earlier
document entries and earlier repository entries were preserved.

## 2. The finite interface already present in the global literature

For a positive-semidefinite unit-diagonal Gram matrix $G$ of size $m$, put

$$
E(G)=\operatorname{tr}(G-I)^2
=2\sum_{i<j}|G_{ij}|^2,\qquad
D(G)=\operatorname{tr}\Psi(G),
$$

where $\Psi(t)=(t-1)^2$ for $0\le t\le2$ and $\Psi(t)=2t-3$ for $t\ge2$.
The factor two in $E$ must be kept throughout any comparison with a triangle
certificate stated as a sum over three unordered pairs.

**[V] Ainta's global construction.** The source proves the stable rank-trace
inequality, the convex trace pinching inequality, and a triple root
obstruction for the cosine kernel. Its seven-point pressure functional uses
six nonnegative gaps and weights $2/(7-s)$ on pairs at index distance $s$.
The total coefficient available to each pair after summing translates is at
most two. It certifies the target $19/5000$ at gap pressure $1/3000$, then
assembles many windows in a larger frame. The elementary spectral lower
bound $D(G)\ge\min(1,E(G))$ is sufficient for that operating point.
[Primary proof](https://github.com/ainta/zeta-simple-zeros/blob/040c5e899e658aed7b56a2a87f501798fe10761d/docs/proof.md).

**[V] More than three points and nonuniform weights are prior art.** The
trmdy seven- and nine-point certificates assign rational position-dependent
weights to pairs. For every fixed index distance, the sum of the applicable
weights is at most two. This is the finite energy capacity needed when
translating the window inside a larger frame. These are deterministic
inequalities for arbitrary nonnegative gap vectors. They do not require a
formula for the seven- or nine-point correlation of actual zeta zeros.
[Seven-point deduction](https://github.com/trmdy/zeta-simple-zeros-673137/blob/1610b97b7895ff34982260f8dcaf04a0f7b82cf7/docs/proof.md),
[nine-point source](https://github.com/trmdy/zeta-simple-zeros-673137/blob/1610b97b7895ff34982260f8dcaf04a0f7b82cf7/docs/nine-point.md).

**[V] Frame pressure accounting is also prior art.** A window with $q$ gaps
occurs in exactly $m-q$ positions in an $m$-point frame. Averaging all shifted
partitions recovers that occurrence count. The refined deduction charges
pressure to those windows before bounding the total span, rather than
charging the largest possible coefficient to every gap of every frame.
The consequent generic formula, in the notation of that source, is

$$
\frac{mH_{\rm cert}-(m-q)qp}
     {m-\Phi_m(\varepsilon(m-q))}.
$$

This formula is used only after the appropriate local energy-plus-pressure
lemma is established. The source also handles unbounded frame spans by
letting pressure alone discharge the target and using compact-uniform Gram
asymptotics on the remaining bounded spans.
[Refined deduction](https://github.com/trmdy/zeta-simple-zeros-673137/blob/1610b97b7895ff34982260f8dcaf04a0f7b82cf7/docs/refined-deduction.md).

## 3. Trace-energy envelope: exact formula, careful proof scope

The finite-size envelope appearing in all three successor sources is

$$
\Phi_m(E)=
\begin{cases}
E,&0\le E\le m/(m-1),\\
2\sqrt{(m-1)E/m}-1+E/m,&E\ge m/(m-1).
\end{cases}
$$

It is algebraically identical to
$E-(\sqrt{(m-1)E/m}-1)_+^2$. Therefore presenting that formula by itself as a
new discovery would overlook the existing sources.

**[V] tawanerguo's actual proof.** Paper lines 259-300 and
`docs/trace_energy_envelope.md` prove the implication needed at the fixed
target $A=1.02129$: if $E+P\ge A$ and $P\ge0$, then
$D+P\ge\Phi_m(A)$. The argument separates zero, one, and at least two
eigenvalues greater than two. In the last case it obtains $D>2$, which is
enough because its target is below two. The paper explicitly avoids a claim
to classify a global minimizer.
[Envelope proof](https://github.com/tawanerguo-cn/zeta-simple-zeros/blob/45149f6d403059a71be73c5e3f884cee7cd62b20/docs/trace_energy_envelope.md),
[paper source](https://github.com/tawanerguo-cn/zeta-simple-zeros/blob/45149f6d403059a71be73c5e3f884cee7cd62b20/paper/riemann.tex).

**[V] Yuhang Shi's scaled pressure lemma.** Its stated hypotheses include
$A\ge m/(m-1)$ and $\Phi_m(A)<2$. The conclusion is
$D+(\Phi_m(A)/A)P\ge\Phi_m(A)$ whenever $E+P\ge A$ and $P\ge0$.
The restriction is explicit and must remain attached when citing that proof.
[Claim ledger, item 1](https://github.com/yuhangshi888/zeta-simple-zeros-673316977/blob/1aeda8e9f0678166a824c75313a813b09eb478cd/CLAIM_LEDGER.md).

There is no counterexample asserted here to the unrestricted envelope. A
separate direct proof using the squared norm of the excess eigenvalues has
been proposed during the present discussion, but its new local status belongs
in a declared experiment. Even if it removes the proof-range restriction,
the identical global formula is already asserted in trmdy's refined note.
The elementary $D\ge\min(1,E)$ suffices for the first proposed odd-frame
test and avoids any dependence on this distinction.

## 4. Current global constants and what was actually verified

These rows describe the inspected primary sources, not a independently
replayed ranking of all published mathematical claims. All ratios concern
simple critical-line zeros divided by all nontrivial zero copies, including
multiplicity, in a long interval.

| Source | Claimed or source-proved global lower bound | Finite input and audit boundary |
|---|---|---|
| Ainta | $0.673008527927\ldots$ | Seven-point pressure certificate; ordinary proof inspected, exhaustive interval run not replayed in this pass |
| tawanerguo | $0.6731929114731422535\ldots$ | Cosine frequency 1.47, Bellman coboundary, target $577/100000$, $m=183$; source reports directed MPFR/GMP checks |
| npip99 | $0.6731951989015205755\ldots$ | Seven-point target $509/100000$, pressure $1/2300$, $m=250$; uses the coarser square-root envelope |
| trmdy, refined seven-point | $0.6732425893558967029\ldots$ | Target $891/200000$, pressure $1/2736$, $m=235$ |
| trmdy, final nine-point | $0.6733127422722459981\ldots$ | Target $15211/2500000$, pressure $1/2500$, $m=177$; source reports 116,272,426 branch nodes across two hosts |
| Yuhang Shi, simultaneous seven/nine | $0.6733169771424713134\ldots$ | Both preceding trmdy inputs, $m=219$, supporting-plane combination; large upstream searches explicitly not replayed by that author |
| teal-sea, registered four-point | $0.6728470197666888\ldots$ | Parametric bridge plus a four-point finite certificate; source reports a complete Lean build and axiom audit; not rebuilt here |

The sources are the [tawanerguo certificate](https://github.com/tawanerguo-cn/zeta-simple-zeros/blob/45149f6d403059a71be73c5e3f884cee7cd62b20/BELLMAN_COBBOUNDARY_PROOF.md),
[npip99 proof](https://github.com/npip99/zeta-zeros/blob/72a01ac5ea3837f2a4c4583d831f885d005f8af1/docs/proof.md),
[trmdy refined note](https://github.com/trmdy/zeta-simple-zeros-673137/blob/1610b97b7895ff34982260f8dcaf04a0f7b82cf7/docs/refined-deduction.md),
[trmdy nine-point note](https://github.com/trmdy/zeta-simple-zeros-673137/blob/1610b97b7895ff34982260f8dcaf04a0f7b82cf7/docs/nine-point.md),
[Shi proof outline](https://github.com/yuhangshi888/zeta-simple-zeros-673316977/blob/1aeda8e9f0678166a824c75313a813b09eb478cd/PROOF_OUTLINE.md), and
[teal-sea four-point theorem](https://github.com/teal-sea/zeta-lab/blob/c614e65188f0b5d73b342436383ae558fbd3aafd/hunts/ainta_seven_point/FOUR-POINT.md).

Yuhang Shi's source archive version 0.1.0 is associated with
[DOI 10.5281/zenodo.21926962](https://doi.org/10.5281/zenodo.21926962).
The September 11 head records registration `PALOMAR-2026-08-29-000004` of a
local formal layer. The finite certificate inequalities and a trace-envelope
alternative remain explicit formal hypotheses. Its own ledger states that
the spectral derivation of that alternative is outside the formalized scope.
This is not an end-to-end formal verification of the improved zeta theorem.

The teal-sea four-point functional is explicitly

$$
\frac{g_1+g_2+g_3}{2500}
+\frac23\sum_{i=1}^3w(g_i)
+w(g_1+g_2)+w(g_2+g_3)+2w(g_1+g_2+g_3)
\ge\frac{2310}{10^6}.
$$

Its larger-frame parameter is $m=435$, giving
$(906250H_0-1085)/904171$. The source's September 5 pressure-tuning attempt
proposed the stronger expression $(14400000H_0-17240)/14366681$, but the
complete Lean build was canceled and every candidate proof step was skipped.
The repository explicitly retains the original registered constant. A
completed search tree or emitted-source preflight is not substituted for that
missing proof build.
[Terminal run record](https://github.com/teal-sea/zeta-lab/blob/c614e65188f0b5d73b342436383ae558fbd3aafd/hunts/four_point_pressure/RUNS.md).

## 5. Simultaneous certificates and nonuniform packing are not new concepts

**[V] Simultaneous seven- and nine-point inequalities.** Shi forms two
constraints on the same $219$-point energy:
$E+p_7W_6\ge A_7$ and $E+p_9W_8\ge A_9$, with
$A_7=189783/200000$ and $A_9=3209521/2500000$.
Writing $R_*=\Phi_{219}(A_9)$ and
$u=(R_*-A_7)/(A_9-A_7)$, the supporting-plane coefficients are
$\beta=(1-u)/2736$ and $\gamma=u/2500$.
The final bound uses

$$
\frac{219H_{\rm cert}-6\cdot213\beta-8\cdot211\gamma}
{219-R_*}.
$$

Thus mixing already available local certificates is itself prior art. The
ledger also quarantines an older additional operating point whose exact
36 rational weights were unavailable. Its headline cannot be used as an
extra certified constraint.
[Outline](https://github.com/yuhangshi888/zeta-simple-zeros-673316977/blob/1aeda8e9f0678166a824c75313a813b09eb478cd/PROOF_OUTLINE.md),
[ledger](https://github.com/yuhangshi888/zeta-simple-zeros-673316977/blob/1aeda8e9f0678166a824c75313a813b09eb478cd/CLAIM_LEDGER.md).

**[V] Bellman coboundaries.** tawanerguo's certified six-gap functional adds
a difference of two five-gap boundary potentials. Its nonuniform gap
pressures are $(946,1177,877,877,1177,946)/1920000$, summing to $1/320$.
Nearest-pair weights are also nonuniform. Boundary terms telescope when
windows are concatenated. This directly anticipates proposals to exploit
compatibility between neighboring windows rather than optimizing an isolated
window alone.
[Bellman proof](https://github.com/tawanerguo-cn/zeta-simple-zeros/blob/45149f6d403059a71be73c5e3f884cee7cd62b20/BELLMAN_COBBOUNDARY_PROOF.md).

**[V] Full-matrix capacitated matching.** The same repository's original
archive contains an explicit finite spectral dual. For any Hermitian $M\ge0$
with unit diagonal, it gives

$$
D(M)=\sup_{H=H^*,\ H\preceq2I}
\left\{\operatorname{tr}H(M-I)-\frac14\operatorname{tr}H^2\right\}.
$$

For nonnegative edge weights $q_{ij}$, set $a_{ij}=|M_{ij}|$ and
$d_i=\sum_jq_{ij}$. Its connection-Laplacian construction yields

$$
D(M)\ge2\sum_{i<j}q_{ij}a_{ij}
-\frac12\sum_{i<j}q_{ij}^2
-\frac14\sum_i(d_i-2)_+^2.
$$

With capacities $d_i\le2$ the last term vanishes. The source derives both a
concave matching optimization and its dual, permits edges across former
block boundaries, and supplies the automatic witness
$q_{ij}=2a_{ij}/\max(1,\sum_ka_{ik},\sum_ka_{jk})$.
It then proposes a finite-range Bellman subaction for an eventual global
zero-density bound. The document explicitly says that this final numerical
conversion was incomplete. A general proposal to remove fixed boundaries or
use adaptive capacity weights therefore cannot be claimed as new here.
[Global spectral dual, sections 2-8](https://github.com/tawanerguo-cn/zeta-simple-zeros/blob/45149f6d403059a71be73c5e3f884cee7cd62b20/archive/original/GLOBAL_SPECTRAL_DUAL.md).

## 6. Method ceilings and routes that cannot be imported

**[U] trmdy's campaign notes** report numerical ceilings for particular
six- and eight-gap families and a periodic binary-gap witness limiting a
broader pair-energy family near $0.674828$. They also describe an unfinished
off-line-pair composition route and a counterexample to naive additive
pricing. Those assertions were read but their auxiliary campaign artifacts
were not replayed in this pass. They neither prove a universal limitation on
all methods nor supply a valid shortcut to a larger unconditional bound.
[Campaign 2](https://github.com/trmdy/zeta-simple-zeros-673137/blob/1610b97b7895ff34982260f8dcaf04a0f7b82cf7/docs/campaign-2.md).

**[U] teal-sea's terminal record** cites a family-specific pressure ceiling
near $0.675142509660254$. That is a different family from trmdy's and is not
a contradictory number. This pass did not independently audit its full
family-wall proof or interval witnesses. Neither number should be called a
barrier for RH itself.

The previously quarantined 79.62 percent higher-moment claim remains outside
the valid dependency chain. A finite matrix inequality does not provide
unproved prime-correlation estimates or justify extending the proved Fourier
support. Deterministic blocks with many points should not be confused with
an arithmetic theorem evaluating unrestricted higher zero correlations.

## 7. What must change in a short-interval transfer

Wang's theorem is the arithmetic interface, already audited in
[the separate transfer dossier](2026-09-12-wang-transfer-audit.md). With
$H=T^\theta$ and a fixed support parameter $0<\lambda<\theta<1$, a fixed
smooth density has a pair-sum error which is $o(N(T,H))$. Smooth approximation
and $\lambda\uparrow\theta$ follow $T\to\infty$.

The limiting optimized density is

$$
f_\theta(t)=\frac{\cos(\sqrt2t)}{\sqrt2\sin(\theta/\sqrt2)}
\mathbf1_{[-\theta/2,\theta/2]}(t),\qquad
c(\theta)=2-\frac\theta2-\frac1{\sqrt2}\cot(\theta/\sqrt2).
$$

After the substitution $t=\theta s$, its profile on the unit interval is
proportional to $\cos(\sqrt2\theta s)$ and the Fourier phase contains
$\theta x$. This changes both the profile and the scale. It is not legitimate
to substitute a rescaled gap into a global trmdy or Ainta certificate and
keep the old numerical target unchanged. Either the test density and its
Wang functional must be recomputed consistently, or a new finite certificate
must be proved for the desired short-interval kernel.
[Wang, Theorem 2.2 and sections 3-4](https://arxiv.org/pdf/2609.07918v1).

The released EXP-002 triangle certificate is already for this correct
$\theta=3/4$ kernel. It is therefore a substantially cheaper next input than
an unproved transfer of a six- or eight-dimensional global certificate.
For actual critical simple zeros the direct Hilbert Gram entries are the
kernel values themselves; no sample-grid approximation is needed. The
available normalized span divided by $N(T,H)$ tends to one.

## 8. Proposed next question, with the priority boundary fixed in advance

**[C] Alternating triples inside an odd frame.** Suppose the doubled
three-point energy is at least $d>0$ on $u+v\le R$. Nonnegativity outside
that triangle immediately gives the global pressure inequality

$$
2\{K(u)^2+K(v)^2+K(u+v)^2\}
+\frac dR(u+v)\ge d,\qquad u,v\ge0.
$$

Inside a frame of $M=2k+1$ ordered points, consider triples beginning at
indices $1,3,\ldots,2k-1$. They share boundary vertices but no unordered
pair. Their spans sum to the span of the entire frame. This suggests
$E_{\rm frame}+(d/R)\operatorname{span}\ge kd$ and, when $kd\le1$,
$D_{\rm frame}+(d/R)\operatorname{span}\ge kd$ using the inherited elementary
spectral bound. Averaging shifted frame partitions would give the candidate
short-interval refinement

$$
c_k(\theta)=c(\theta)
+\frac{kd}{2k+1-kd}\{c(\theta)-2/R\}.
$$

For the existing exact threshold $d=1/7000$, taking $k=7000$ would give the
coefficient $d/2$ on $c(\theta)-2/R$, compared with $d/(3-d)$ in EXP-002.
No new numerical value was computed in this source preflight. The apparent
gain is a candidate until the experiment record independently checks the
finite inequality, shifted boundary accounting, denominator algebra, strict
smoothing margin and distinct-zero companion.

An earlier all-window assembly suggested coefficient $1/14001$ in this
special case. The alternating cover instead suggests $1/14000$. These are
different formulas and must not be conflated. The odd-frame proposal should
be tested directly, not justified by copying the earlier all-window result.

The exact alternating odd-frame formula was not located in the inspected
sources. Nonetheless, pair capacities and pressure-frame assembly belong to
the existing global framework, and the schedule is a simple choice within
that framework. The proposed novelty claim is therefore limited to the
stronger short-interval consequence and its complete proof, if validated.

The smallest informative next experiment is a symbolic pressure-frame
transfer using the frozen EXP-002 certificate. Expensive four-, seven- or
nine-point optimization is unnecessary for deciding that question. A later
new-kernel pressure optimization may improve the size of the gain, but must
have a separate bounded hypothesis and must credit the globally established
window, coboundary and mixed-frame constructions.

## 9. Dated novelty search and residual uncertainty

The fresh source sweep searched complete Markdown and TeX in the pinned
Ainta, trmdy, tawanerguo and Yuhang Shi snapshots for alternating, pair-disjoint,
odd-frame, nonuniform, capacitated, packing, short intervals, Wang and
`2609.07918`. Searches also inspected the relevant teal-sea bridge and
four-point notes. Occurrences of short intervals around roots in a numerical
kernel table were not mistaken for height intervals in the zeta theorem.

Online queries included `"2609.07918" "stability"`,
`"2609.07918" "pressure"`, `"zeta" "short-interval" "Gram"`,
`"Riemann" "short intervals" "four-point"`, and variants with Wang,
nonuniform packing and adaptive Gram blocks. They produced the Wang record,
global successor repositories, or unrelated correlation literature; no
primary source matching this short-interval pressure-frame consequence was
located. Search-engine coverage was poor for several exact phrases.

This is evidence of a bounded priority search, not a guarantee against
unpublished work, unindexed recent material, or a missed equivalent
formulation. The stronger local theorem must first survive its own
adversarial experiment. Publication, expert acceptance, and RH remain
separate questions.

## 10. Additional adversarial novelty check: what the parametric bridge covers

A second independent source pass on 2026-09-12 tested the strongest immediate
priority objection: perhaps teal-sea's parametric theorem already states the
proposed result for $H=T^\theta$, so that changing a few parameters would
already give the whole short-interval conclusion. Direct inspection of the
Lean declarations and their arithmetic passage does not support that
objection at the inspected head `c614e65188f0b5d73b342436383ae558fbd3aafd`.
This is a scope determination from source, not a new Lean build.

**[V] What is actually parameterized.**
[`Bridge/Main.lean`, lines 281-292](https://github.com/teal-sea/zeta-lab/blob/c614e65188f0b5d73b342436383ae558fbd3aafd/lean/bridge/Zeta23Ext/Bridge/Main.lean#L281)
quantifies the number of points $n$, certificate floor $c$, frame size $m$
and pressure denominator $p$. Its conclusion is explicitly about
`Ncount T (2 * T)` and `N0simple T (2 * T)`. It does not quantify an upper
endpoint, interval length, or short-interval exponent. The
[four-point corollary, lines 178-194](https://github.com/teal-sea/zeta-lab/blob/c614e65188f0b5d73b342436383ae558fbd3aafd/lean/bridge/FourPoint/Main.lean#L178)
retains those same endpoints.

**[V] The kernel and baseline are fixed.**
[`Bridge/Defs.lean`, lines 45-54](https://github.com/teal-sea/zeta-lab/blob/c614e65188f0b5d73b342436383ae558fbd3aafd/lean/bridge/Zeta23Ext/Bridge/Defs.lean#L45)
defines the overlap integral with $\cos(\sqrt2t)$ on $[-1/2,1/2]$.
Its `Phi_n` definition at lines 157-162 uses `HD 1`. Its `mtParams`
definition at lines 217-220 chooses the Montgomery-Taylor family at
$\lambda=1$. Consequently, replacing $n$, $c$, $m$ or $p$ does not
change the profile into $K_\theta$ or replace the baseline by Wang's
$c(\theta)$.

**[V] The arithmetic passage has the same dyadic scope.**
[`Bridge/S8.lean`, lines 39-84](https://github.com/teal-sea/zeta-lab/blob/c614e65188f0b5d73b342436383ae558fbd3aafd/lean/bridge/Zeta23Ext/Bridge/S8.lean#L39)
proves `tail_passage` for a `ZeroConfig` satisfying the imported
`PaperInputs`; its conclusion still counts $(T,2T]$ and carries `HD 1`.
The source's discussion of validity at $\lambda=1$ concerns this dyadic
analytic framework. It supplies no permission to replace Wang's required
fixed $\lambda<\theta$ by its endpoint. The two error analyses have
different interval lengths. An arbitrary finite-matrix lemma can be reused
on a short-interval Gram matrix, but the appropriate short-interval pair-sum
estimate and limit passage must still be supplied.

**[V] A potentially misleading derivative lead is also global.**
[`asymptotic_transfer.py`, lines 16-27 and 56-78](https://github.com/teal-sea/zeta-lab/blob/c614e65188f0b5d73b342436383ae558fbd3aafd/hunts/frontier_math/asymptotic_transfer.py#L16)
discusses the variable cosine profile, a density parameter, and derivatives
of `HD(lam)`. Its stated counting expression is `N0*(T,2T)`.
The identifier `theta` in that module denotes a retained spectral/census
factor, not Wang's interval exponent. The file explicitly stops short of
claiming a new zero proportion. It was read as source and was not executed.
Separately, [`docs/13-moments.md`, lines 292-295](https://github.com/teal-sea/zeta-lab/blob/c614e65188f0b5d73b342436383ae558fbd3aafd/docs/13-moments.md#L292)
explains that its short-window numerical normalization does not turn the
global moment theorem into a short-interval theorem.

The comparison is therefore stronger than a title search: a dyadic theorem
does not yield an every-short-interval theorem by renaming its parameter.
Simultaneously matching $T'=T$ and $2T'=T+T^\theta$ is impossible for
$0<\theta<1$ and large $T$. A global lower proportion also does not control
how that proportion is distributed among all shorter subintervals.

The audit additionally scanned 271 primary Markdown, TeX and bridge Lean
files, totaling 3,950,122 bytes, with zero retrieval failures. The scope was
`docs/`, all bridge step files, and the zeta-related Ainta, frontier-math,
family-wall, cycle-moment, quotient, rogue-frontier, prime-pair-error,
higher-xi, outband, overlap, effective-constant and wide-search dossiers.
Search terms were `short interval`, `short-interval`, `Wang`,
`2609.07918`, `odd-frame` and `pair-disjoint`. No Wang citation or matching
short-interval simple-critical theorem was located. The returned interval
references concerned kernel-root boxes, prime counts, moment statistics or
other explicitly different problems. This was a content scan plus direct
reading of the decisive theorem interfaces, not a claim to have fully
reviewed every mathematical argument in all 271 files.

The additional immutable source hashes are:

| Source under the inspected teal-sea head | Bytes | SHA-256 |
|---|---:|---|
| `lean/bridge/Zeta23Ext/Bridge/Defs.lean` | 13,708 | `258b242ffc96444237dd923e5843f8425148a46bb81359932a50dea814f4ede3` |
| `lean/bridge/Zeta23Ext/Bridge/Main.lean` | 23,196 | `82878d715638e695aeffe4867f337a6022793e568160d9eb6695483125d872ed` |
| `lean/bridge/Zeta23Ext/Bridge/S8.lean` | 4,866 | `c8dac20f89c4ac3335ca9a5af24dff2eb0d797d8ff27fa5be2e8097daaf9ceae` |
| `lean/bridge/FourPoint/Main.lean` | 9,998 | `4c0f7e675a936fc80c4cdfcc5e32f5414e37543a2833e251ebd604facd2bee40` |
| `hunts/frontier_math/asymptotic_transfer.py` | 41,110 | `06409e6cc1be2acff55f7165f6334f902488719497b8550ecb9f00fafa80ec77` |
| `docs/13-moments.md` | 25,614 | `fa64ee3e11f0eca7d00340740eee10b65f67a73d57ff45f1eccc02eb944f106d` |

The scoped novelty assessment is unchanged: the odd-frame result is a
modest, apparently new short-interval consequence of attributed finite
methods and Wang's arithmetic input, if the declared experiment validates
it. The simple choice of an alternating cover is not presented as a new
general packing theory or an advance in the underlying arithmetic estimates.
The exact formula may be absent from the sources yet remain an elementary
consequence of their finite framework. That distinction should remain
explicit in any manuscript. This pass found no already stated theorem
covering the same $H=T^\theta$ conclusion, but does not certify absolute
priority or publication significance.
