# EXP-003 verdict: confirmed for odd-frame and pressure refinements

Date: 2026-09-12. Declaration committed and pushed before computation:
`8ed806d64e5df2b83ab1ad75cb9f17a5633208bc`. Paper proof and coordinating audit
committed as `e21618c`.

| Stage | Current outcome | Meaning |
|---|---|---|
| A: stronger assembly of the existing energy certificate | **confirmed** | Complete paper proof and independent reviews, exact identities and incidence checks, and a full replay of the existing finite certificate support a stronger short-interval bound |
| B: a new pressure certificate with more than 25% further gain | **confirmed** | The first frozen candidate passed exhaustive 160-bit construction and 256-bit replay, with a strictly positive margin over the declared gain target |

Both stages are confirmed within the theorem scope below. Their evidence is preserved
separately; the aggregate machine record is [artifacts/result.json](artifacts/result.json).

## Confirmed Stage A theorem

[D] For every fixed $\theta_0<\theta<1$, write

$$c(\theta)=2-\frac\theta2-\frac1{\sqrt2}\cot(\theta/\sqrt2).$$

If the doubled three-point kernel energy is at least $d>0$ for nonnegative gaps
of total span at most $R>2/c(\theta)$, then every integer $k>1$ with $kd\le1$
gives

$$
\liminf_{T\to\infty}\frac{N_0^s(T,T^\theta)}{N(T,T^\theta)}
\ge c_A=c(\theta)+\frac{kd}{2k+1-kd}\{c(\theta)-2/R\},
$$

with distinct-zero companion $(1+c_A)/2$. Here $N$ counts all zero copies,
$N_0^s$ counts simple critical-line zeros, and the distinct count counts each complex
zero once. These are asymptotic bounds for fixed exponents, not finite-height
guarantees at the exact displayed constants.

For the same $d,R$, the new gain coefficient exceeds EXP-002's coefficient by

$$
\frac{kd}{2k+1-kd}-\frac d{3-d}
=\frac{d(k-1)}{(2k+1-kd)(3-d)}>0.
$$

The explicit analytic energy input from EXP-002 has $0<d<1/4$, so $k=2$ is
available throughout its complete positive curve. This establishes a strict
whole-curve improvement, not merely a better isolated numerical illustration.

The mechanism is to place $k$ alternating triples inside a $(2k+1)$-point frame.
They share endpoints but no unordered pairs; their energies add without duplication
and their spans telescope. Spectral pinching applies between disjoint full frames.
The general pressure theorem and the signed finite-operator proof of the distinct
companion are in [the complete proof](mathematical-proof.md). The refutation attempts
and separate coordinating review are in [the adversarial audit](adversarial-audit.md).

## Stage A certified example and reproduction evidence

[D+MV] The already certified parameters $\theta=3/4$, $R=21/4$, $d=1/7000$
permit $k=7000$ and frame size $14001$. The exact result is

$$c_A=c(3/4)+\frac{c(3/4)-8/21}{14000}.$$

| Quantity | Enclosed value, displayed here with truncated digits |
|---|---:|
| Wang baseline $c(3/4)$ | $0.419075012975424333734553610698$ |
| EXP-002 simple-critical example | $0.419076828425303996736665787527$ |
| EXP-003 Stage A simple-critical bound | $0.419077736020568836833221725071$ |
| Stage A gain above Wang | $0.000002723045144503098668114373$ |
| Stage A distinct companion | $0.709538868010284418416610862535$ |

The gain ratio relative to EXP-002 is exactly $20999/14000$. It compares gains
above the same baseline, not the headline proportions or percentage points.

The Stage A runner checked two symbolic identities and 328 incidence/boundary cases
covering frame sizes $3,5,\ldots,17$ and sequence lengths zero through forty.
It independently counted pair usage, telescoping gap coefficients, all shifted frame
starts, and the $(M-1)$ gap-capacity bound. Exact arithmetic also checked
$\alpha=1/14001$, $\beta=8/294021$, and $\alpha/(1-\alpha)=1/14000$.

The entire EXP-002 certificate was replayed at 256 bits with the separately derived
sinc-Taylor evaluator: 48,761 nodes, 24,252 energy leaves, 129 outside leaves,
and zero unresolved boxes. The reused canonical certificate has SHA-256
`bd8254477c25124b6bf9fc01e0db88f7f5a16d1bc82357c6eb4cbd594a731463`.
The runner verifies that both that file and the hypothesis match the declaration
commit byte for byte before arithmetic. All new rational enclosures and source hashes
are retained in the [Stage A result](artifacts/stage-a/stage-a-result.json). The run took about 26.9 seconds,
inside its one-minute budget.

The numerical replay uses the same partition geometry, Lipschitz estimate, and Arb
library as the earlier construction, with an independent kernel evaluator. It is not
an independent complete verifier or an end-to-end Lean proof.

## Confirmed Stage B pressure certificate

[D] A complete all-gap inequality

$$E_3(u,v)+p(u+v)\ge\epsilon\qquad(u,v\ge0)$$

with $p,\epsilon>0$ and $k\epsilon\le1$ implies

$$
c_B=c(3/4)+\frac{k\{\epsilon c(3/4)-2p\}}{2k+1-k\epsilon},
\qquad\text{distinct companion}=\frac{1+c_B}{2}.
$$

Stage B requires its gain above Wang to be strictly greater than $5/4$ of the
confirmed Stage A gain. The pressure parameters must be rational, the derived cutoff
$\epsilon/p$ must be at most twelve, and a complete interval certificate must cover
the closed nonnegative triangle up to that cutoff. Pressure alone controls the rest
of the domain. A sampled minimum is not a certificate.

[D+MV] The first frozen candidate passed, with exact parameters

$$
p=\frac1{12500},\qquad \epsilon=\frac{443239}{10^9},\qquad
R_{\mathrm{cut}}=\frac{443239}{80000},\qquad k=2256,\qquad M=4513.
$$

The unit-cap condition is $k\epsilon=999947184/10^9<1$. The resulting
simple-critical bound and distinct companion are

$$
c_B=0.419087888170111727959091183775\ldots,\qquad
\frac{1+c_B}{2}=0.709543944085055863979545591887\ldots.
$$

The gain above Wang is $0.000012875194687394224537573076\ldots$.
Its excess over $5/4$ of the Stage A gain is enclosed strictly positively:

$$g_B-\frac54g_A=0.000009471388256765351202430110\ldots>0.$$

All rational endpoints are in the [candidate result](artifacts/stage-b/candidate-1/result.json).
The [pressure certificate](artifacts/stage-b/candidate-1/pressure-certificate.json)
has 16,797 nodes, 8,351 validated energy-plus-pressure leaves, 48 exact pressure-only
leaves, and zero unresolved boxes. Every accepted leaf was independently replayed with
the 256-bit sinc-Taylor evaluator after construction at 160 bits. The actual combined
construction-and-replay time was about 5.2 seconds, within the ten-minute budget.

The certificate verifier's canonical JSON-object digest is
`9cccc45eccf3d4e999e37f58b516d572fb2eec4c16854c4ddb144f053f2c9624`.
This digest uses sorted compact JSON plus LF and is distinguished from a pretty-printed
artifact's raw file-byte hash.

The declaration permits one floating design pass of at most sixty seconds and at most
three frozen rational candidates. The one design pass took about 0.25 seconds and
retained its [complete trials and ordered candidates](artifacts/candidates.json).
Each candidate had a combined ten-minute construction
and independent-replay budget and a two-million-node cap. An unresolved or interrupted
candidate is inconclusive. A valid certificate below the gain target is retained but
does not confirm this stage. Candidates two and three were not run after the highest-ranked
candidate succeeded. Their frozen parameters and explicit nonexecution outcomes remain
in the [Stage B record](artifacts/stage-b/stage-b-result.json); they are neither
confirmed nor refuted. These outcomes do not weaken the independently confirmed Stage A.

## Prior art, validation trust, and limits

The [dated source-complete review](../../context/2026-09-12-pressure-frame-prior-art.md)
attributes stability, pinching, pressure frames, and nonuniform capacities to Ainta,
trmdy, tawanerguo, and Yuhang Shi. The alternating schedule is a simple instance of
that known finite framework. The scoped contribution is the stronger short-interval
consequence, with complete limit and multiplicity accounting and certified reuse.
An identical short-interval consequence was not located in the inspected sources;
that search is not a guarantee against missed or concurrent work.

The code audit found no mathematical defect in the closed-square coverage or whole-cell
pressure lower bound. It identified and corrected a replay-budget issue, an unchecked
negative sample-witness coordinate, and insufficient binding of smoke receipts to the
current code. A regression now tests a fully forged completed checkpoint prefix with
matching hashes: arithmetic must still be replayed and the false leaf rejected.
The numerical owner reports 29 focused tests passing at the Stage A milestone.
The [smoke receipt](artifacts/smoke/smoke-result.json) records a forced stop at ten
construction nodes, successful resume equal to fresh construction, rejection of mismatched
parameters, and a 256-bit replay restart that rechecks the prefix.

Construction checkpoints preserve candidate proof state and do not independently
certify prior leaves. Final replay remains mandatory. Replay checkpoints validate
identity, reconstruct the prefix, and recheck all its arithmetic before continuing.
They provide a safe validated restart, not a claim to save the prefix's arithmetic
work. Restoration and rechecking count within the remaining combined time budget.

Canonical mathematical artifacts use UTF-8/LF and deterministic ordering. Timing
and progress are separate operational metadata. The EXP-002 certificate and frozen
published manuscript are unchanged.

How could this be wrong? The argument relies on Wang's inspected preprint and cited
classical analytic inputs; the paper reviews could share an overlooked error. The
two numerical evaluators share Arb and geometric logic. The source sweep could miss
prior art. None of these checks proves RH, improves the positivity exponent, provides
an effective height threshold, establishes uniformity near $\theta_0$, or claims a
global zero-proportion record. The result supplies no new prime-correlation theorem.

## Reproduction

Use the repository virtual environment with the problem's pinned requirements. From
the repository root, write each run to a fresh directory, for example:

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-003-odd-frame-pressure/run.py --stage A --output-dir tmp/riemann-exp003-replay-a
python -m pytest tests/test_riemann_pressure.py
```

To reproduce the pressure run using the frozen candidate list, first generate a fresh
smoke receipt and then run Stage B, keeping each command on one shell line:

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-003-odd-frame-pressure/run.py --stage smoke --output-dir tmp/riemann-exp003-replay-smoke
python problems/number-theory/riemann-hypothesis/experiments/EXP-003-odd-frame-pressure/run.py --stage B --output-dir tmp/riemann-exp003-replay-b --candidates problems/number-theory/riemann-hypothesis/experiments/EXP-003-odd-frame-pressure/artifacts/candidates.json --smoke-receipt tmp/riemann-exp003-replay-smoke/smoke-result.json
```

The floating design pass is discovery provenance and need not be repeated to verify
the fixed certificate or reproduce its mathematical outcome. Replays preserve historical
artifacts and use fresh output directories. Source hashes and operational elapsed times
are checked and reported separately from the exact mathematical enclosures.
