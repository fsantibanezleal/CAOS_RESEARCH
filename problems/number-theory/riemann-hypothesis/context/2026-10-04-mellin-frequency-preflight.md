# Mellin frequency averaging: source and invariant preflight

This is an unproved route within RH-F4, following EXP-028's completed
short-window estimate. It has not changed the admitted onset or manuscript.
The intended gain is a larger uniform mollifier range using the same exact
transformation and counting problem, with less reliance on a deep trilinear
input. No detector search or GPU computation is needed for this first step.

## Primary-source refresh

The current [Wang record](https://arxiv.org/abs/2609.07918) still lists v1.
The [Das--Pujahari record](https://arxiv.org/abs/2104.10243) still lists v3,
revised May 2024. The existing late-source dossier already audits the
displayed exponent discrepancy and the separate shorter-window theorem.
The two 2024 journal articles are distinct publications; an inaccessible
publisher version is not evidence that either has no further applicable
result. Their wider overlap remains a limitation, not a new contradiction.

Natalie Evans, [Correlations of almost primes](https://doi.org/10.1017/S0305004122000251),
Section 7.3, Lemmas 7.6--7.7, supplies classical mean-value context for
arbitrary complex Dirichlet coefficients. Its character-averaged integer
frequencies cannot be substituted directly for our rational frequencies.
The end of its proof and bibliography were checked for a zeta-mollifier
claim; they concern almost-prime correlations. Montgomery's book is the
attributed source behind its mean-value statement. The proposed rational
frequency lemma below needs its own proof, rather than a guessed transfer.
The downloaded PDF is retained externally with its hash manifest.

Limited searches for short-interval mollified moments and Mellin mean-square
methods located no identical route. This does not establish worldwide novelty.
The original source-bound EXP-024/027 representation and EXP-028's complete
assembly remain the relevant dependencies; none is replaced by a web snippet.

## Distinguishing invariant

For a finite dyadic block p in [P,2P], q in [Q,2Q], n in [N,2N], group
the exact frequencies log(pq/n). Distinct frequencies are separated by at
least 1/(16PQN). Equal frequencies are genuinely present: pq/n=r/s in
lowest terms implies n=ks and pq=kr. Their multiplicity is bounded by
2N times the largest divisor count of an integer at most 4PQ. The N factor
must remain. Dropping it would turn a plausible gain into a false estimate.

A Gaussian Gram calculation may prove the classical separated-frequency
bound directly, for arbitrary complex grouped coefficients, with cost
L+O(PQN) on an interval of length L. The Fourier transform of the Gaussian
gives a positive exponentially decaying Gram matrix; its row sums admit a
Schur bound. This is the complementary harmonic-analysis lens.

If the common gamma/Mellin weight is independent of p,q,n after all fixed
small-shift powers have entered the coefficients, weighted Cauchy--Schwarz
on dyadic t bands may replace the absolute multiplier step. Set
K=T/H and A=T/H^2; these are different parameters. At Re u=1/2, the proposed
block cost is

    (H/g) * A^(1/2) * N^(1/2) * sqrt(1+PQN/K) * T^epsilon.

At N0=A*PQ this suggests, before summing gcd blocks,

    (H/g) * [A*(PQ)^(1/2) + A^(3/2)*K^(-1/2)*(PQ)^(3/2)].

The tentative balanced error exponents are

    1-2theta+nu,   1-(5/2)theta+3nu.

These calculations are predictions, not an admitted uniform theorem.
The proposed range is nu<min(1/2,2theta-1,(5theta-2)/6). It could improve
EXP-028 near theta=1/2. The existing trilinear route remains useful elsewhere.

## Gates before any run or new manuscript

Declare EXP-029 before computation, after recording its premise bindings,
one-sidedness, CPU budget and stop criterion. The first finite check should
test exact frequency collisions/spacing and exponent bookkeeping, including
unbalanced blocks. Passing those checks proves only those finite statements.

A positive theorem additionally requires a complete weighted mean-value
proof, coefficients independent of the Mellin variable, dyadic t tails,
every dual n block, N0<1, the nonoscillatory branch, residues/coalescence,
gcd sums, small shifts, fixed general Q and compact-window smoothing.
Unweighted Cauchy--Schwarz over the whole real line is invalid because the
Dirichlet sum does not have a finite unweighted L2 norm there.

Any validated extension belongs in a future version of short-interval-levinson.
The immutable published v0.02 remains unchanged. No new manuscript or Zenodo
version is warranted for this preflight alone. EXP-023 stays stopped.
