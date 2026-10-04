# EXP-029: retain Mellin frequency averaging before absolute summation

Declared 2026-10-04 before control computation. RH-F4 is retained; the
original RH statement remains open. This experiment targets the same uniform
shifted short-window moment and counting problem as EXP-028, with a different
harmonic-analysis estimate, not another detector or global Gram sweep.

Question: can the exact separated Mellin formula, grouped rational-frequency
mean-square bounds and weighted Cauchy--Schwarz prove the moment for

    1/2<theta<1,
    0<nu<min(1/2,2theta-1,(5theta-2)/6)?

This proposed range is unproved at declaration. Near theta=1/2 it would
enlarge the available mollifier range substantially and avoid the external
trilinear theorem in that range. EXP-028 remains useful for other ranges.
Motivation and source eligibility are in
`../../context/2026-10-04-mellin-frequency-preflight.md`.

Method: on a finite dyadic p,q,n block, group equal log(pq/n). Prove distinct
log frequencies separated by at least 1/(16PQN), retaining multiplicity
at most 2N max_{m<=4PQ}tau(m). Prove a Gaussian Gram/Schur mean-value bound
for arbitrary complex grouped coefficients. Use it with the common exact
gamma/Mellin multiplier on dyadic t bands; the whole-line unweighted L2
integral is forbidden. At Re u=1/2 predict the cost

    (H/g)*(T/H^2)^(1/2)*N^(1/2)*sqrt(1+PQN/(T/H)).

Retain all phases, coefficient restrictions, unbalanced blocks and gcd sums.
At N0=TPQ/H^2 predict relative errors TM/H^2 and TM^3/H^(5/2), namely
E1=1-2theta+nu and E2=1-(5/2)theta+3nu. Move each finite tail block's
contour right, without assuming a compact dual cutoff.

P1 source preflight: EXP-028's full Mellin formula and profile bounds,
EXP-024's complete signed representation/remainder and compact conversion,
EXP-027's full transformation/residues and their verdicts were checked.
The Evans mean-value lemmas and ending/bibliography are classical context,
not a directly applicable rational-frequency theorem. The rational lemma
must be independently derived. The existing Das--Pujahari dossier and current
arXiv v3 record retain the documented exponent issue and overlap limitation;
no matching uniform shifted short-window route was located in limited
primary-source searches. Worldwide novelty is unconfirmed.

P3 premises: EXP-024/027 supporting analytic verdicts; EXP-028's complete
internally reviewed profile/residue/general-Q/compact assembly; EXP-010's
frozen certified detector and counting/parity transfer; Wang 2609.07918v1
as an attributed pair theorem. The new weighted bound and its uniform
assembly are hypotheses, not existing premises. Earlier published sources,
receipts and runtime files remain immutable.

P5 invariant-first: exact rational-frequency collisions and spacing; their
cost distinguishes this route. Dropping the collision N factor, silently
requiring PQN<T/H, ignoring tails or counting a finite pass as an analytic
proof rejects the proposed derivation. No GPU is useful for this invariant.

First finite controls: fixed dyadic P,Q,N in {1,2,4,8,16,32}, with coprime
and unrestricted blocks, compare independent integer/Fraction grouping,
spacing and multiplicity. Check the exponent reduction on balanced and
unbalanced configurations. Then one conditional fixed endpoint
theta=527/1000, nu=499/10000, eta=1/100000 uses the already certified
EXP-010 detector. Prediction: both charged errors are negative and the
parity density is positive. There is no new detector optimization.
Native Arb and independent stdlib rational intervals cross-check it.

P4 one-sidedness: a finite PASS certifies only the enumerated arithmetic,
frequency and conditional endpoint calculations. It cannot prove the
uniform moment or a new onset. A FAIL refutes the tested bound, bookkeeping
or fixed endpoint prediction and must be recorded without changing targets.
Analytic admission needs a complete proof and adversarial review of every
retained term, shifts, general Q and narrower compact-window loss.

P6 budget: CPU only, at most 60 CPU seconds per control run, progress flushed
by block; finite output receipt is written only on successful completion.
No long run or heavy sweep is authorized by this declaration. A budget stop
is inconclusive; preserve outputs and do not automatically relaunch.

Success: the complete analytic derivation survives independent re-derivation,
all arithmetic/refutation gates pass and a certified onset improves 0.5339.
Failure: any missing dependence, coefficient restriction, multiplicity,
summability, residue, derivative or smoothing cost invalidates the claim.
Until success the admitted onset and published v0.02 stay unchanged.

Manuscript route: a validated stronger uniform moment and consequence belong
in a future short-interval-levinson version after coherence/overlap review.
The preflight alone is a research record; no new manuscript or DOI is warranted.
