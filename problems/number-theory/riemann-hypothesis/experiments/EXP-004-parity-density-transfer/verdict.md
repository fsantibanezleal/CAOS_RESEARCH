# EXP-004 verdict: confirmed qualitative interval-range improvement

Date: 2026-09-12. Declaration `e03413b2301bf45ca68ff6e945f25add9a1c3a89`
was committed and pushed before implementation or computation. The complete
paper proof and coordinating audit were committed in `6984177`. The single
declared full arithmetic run passed, followed by independent checks of every
stored census row. No failed full run, replacement search or budget extension
occurred.

**Verdict: confirmed.** The universal paper argument, verified primary-source
interfaces, exact computational controls and independent adversarial reviews
support the theorem below. Confirmation concerns the mathematical deduction
within those stated inputs; it does not establish exhaustive novelty priority,
external peer acceptance or an end-to-end formal proof.

## Confirmed theorem and the relevant improvement

[D] Define

$$c(\theta)=2-\theta/2-\cot(\theta/\sqrt2)/\sqrt2,$$

and let theta0 be its unique zero on (0,1). Set alpha=51/100. There exists a
fixed constant kappa>0 such that for every fixed theta in (alpha,1),

$$\liminf_{T\to\infty}\frac{S(T,T^\theta)}{N(T,T^\theta)}
\ge\max\{0,c(\theta),(c(\theta)+2\kappa)/3\},$$

$$\liminf_{T\to\infty}\frac{Z(T,T^\theta)}{N(T,T^\theta)}
\ge\max\{\kappa,(1+c(\theta))/2,(3+2c(\theta)+\kappa)/6\}.$$

N counts all nontrivial zero copies in (T,T+T^theta]; S counts simple critical
zeros; Z counts distinct complex zeros. The same kappa is obtained from one
fixed classical seed. The eventual height may depend on the fixed exponent.

Put

$$\delta=\min\{(\theta_0-\alpha)/2,\kappa/4\},
\qquad\theta_1=\theta_0-\delta.$$

Then alpha<theta1<theta0, and every fixed theta in [theta1,1) has simple-critical
lower asymptotic proportion at least kappa/3>0. At theta0 itself the lower
bound is at least 2kappa/3. This strictly extends the interval range where
Wang's displayed cosine bound establishes positive simple-critical density.
Wang reports theta0=0.550193964744154...; that inherited decimal identifies
the comparator and is not used as a numerical premise of this proof.

There is also a distinct-above-one-half consequence. Set

$$\delta_{\rm half}=\min\{(\theta_0-\alpha)/2,\kappa/16\},
\qquad\theta_{\rm half}=\theta_0-\delta_{\rm half}.$$

Every fixed theta in [theta_half,1) has distinct lower asymptotic proportion
at least 1/2+kappa/12. This is obtained from the separate distinct inequality.
It does not improve the classical threshold for merely having a positive
distinct proportion, which is already known on substantially shorter intervals.

No numerical value of kappa, theta1 or theta_half is established. An
unspecified positive classical constant suffices for this existence theorem;
assigning an arbitrary small decimal would not make it a certified constant.

## Mechanism and imported ingredients

[D] Let O count distinct odd-multiplicity critical support points in the finite
encoded zero multiset. Retain the multiplicity excess E=N-s-2r-2b from the
known stable Hilbert inequality. With D the nonnegative simple Gram defect and
sigma=Q-(4N-3s-4r-4b+D)>=0, the exact identities are

$$3s-(2N-Q+2O+D)=2(s+E-O)+\sigma,$$

$$6Z-(7N-2Q+O+2D)=(s+E-O)+6b+2\sigma.$$

The common charge s+E-O is nonnegative for every multiplicity atom. In
particular, a nonsimple odd real point costs at least one unit of excess.
This connects classical sign-change information to the second-moment estimate
without assuming that odd zeros are simple.

The finite operator/stability mechanism, the cosine functional, Selberg's odd
density theorem, Karatsuba's stronger classical theorem, and Wang's arithmetic
input are attributed prior work. The contribution is their short-interval
combination and the range extension. The [complete proof](mathematical-proof.md)
includes the signed operator, min-max dimension bookkeeping, atom argument,
packing, exact rational deweighting, smooth approximation, and limit order.

The classical count convention was verified in Karatsuba's primary paper,
including its disjoint sign-change argument on printed page 536. A fixed seed
at alpha is packed into longer intervals, losing only o(T^theta) length.
All test functions and Fourier supports lambda<theta are fixed before the
height limit; approximation and support limits follow it. The sign of c is
not a hypothesis of that arithmetic estimate.

Exact elementary comparisons give

$$c(51/100)\le-1801/20400<0<c(1),\qquad
c'(\theta)<1/\alpha^2=10000/2601<4$$

on the relevant interval. They prove alpha<theta0 and both delta conclusions
without a numerical root calculation.

## Exact validation and retained evidence

[MV] The [canonical result](artifacts/result.json) has schema
`riemann-exp004-results-v1` and SHA-256
`bc9e28ca1792657e24da77268e6e2108c3f52684b7e16504f07b32cfce014d6e`.
The fixed runner has SHA-256
`fa4392330a9f1bd2e2ba1216c9a6ad713440acd1aca22d10ee50f6320c490f52`.

| Check | Observed outcome |
|---|---|
| Universal residual identities | Two exact symbolic identities passed |
| Arbitrary multiplicity atom signs | Symbolic nonnegative families, with 24 single-atom regressions through multiplicity 12 |
| Declared count census | All 19,683 vectors in {0,1,2}^9; all 59,049 sigma evaluations passed |
| Relaxed scalar optimum | All 42 rational cases have matching feasible primal and dual witnesses |
| Sinc sharpness | All 36 simple/double-support configurations attain equality in both finite residuals |
| False distinct half-sum control | A real triple point gives residual -1 and rejects the proposed shortcut |
| Threshold comparison | Exact negative bound at alpha and derivative cap passed; unproved numerical constants remain null |
| Budget | One successful full run, 8.0353704 seconds, below the fixed 60-second cap |
| Focused software tests | 36 passed, including count tampering, exact-source bytes, budget-stop prefix preservation, negative/float inputs and overwrite refusal |
| Independent raw checks | Two reviewers separately parsed every census row using direct formulas without importing the runner; artifact hashes and null constants matched |

The full [census](artifacts/census.jsonl) is retained, 1,234,096 bytes, SHA-256
`03e3f42e3c887e729057e02b88b53c07673c171113f5389e0b7d92ee18acc421`.
The [execution receipt](artifacts/execution-receipt.json), original stdout,
source identities, symbolic records, primal/dual witnesses, sharpness controls
and checkpoint are preserved alongside it. Operational timing is separate from
the deterministic mathematical result. All original eight process-generated
files were copied byte for byte. The scalar sigma samples are not claimed to
be realizable zeta configurations.

Run from the repository root into a fresh directory:

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-004-parity-density-transfer/run.py --output tmp/riemann-parity-replay
pytest tests/test_riemann_parity.py
```

The census is a transcription and implementation check, not a proof of all
multiplicities or all heights. The universal atom argument and the imported
analytic theorems supply those quantifiers. The [adversarial record](adversarial-audit.md)
documents both the paper review and the computational checks. A separately
hashed [proof-review record](proof-review.json) binds the final scientific
documents and result for export; the runner never promotes its finite output
to an all-height theorem by itself.

## Prior art, alternatives and how this could be wrong

The dated source search and independent audit found no matching stated
short-interval parity combination. This is bounded evidence, not an absolute
priority guarantee. The finite accounting is not claimed as a newly invented
spectral inequality. Any earlier matching deduction would change attribution
and novelty assessment without invalidating the algebra.

The result would need correction if a substantive error were found in an
imported analytic theorem, the distinct odd seed convention, the fixed-support
transfer, or the universal proof. Those interfaces were specifically attacked.
Finite computation alone could not exclude such an analytic error. No RH
assumption or conjectural higher-moment estimate was introduced.

The high-degree short-mollifier route remains separate: its precise detected
count, a generalized localized moment and certified numerical seed would all
need proof. Weighted Gram, negative-spectrum, approximation/tail and heat-flow
routes retain their separate source reviews and missing inputs. Their finite
or source-level observations are not relabeled as confirmed zeta theorems.

This result meets the declared target of a more relevant parameter improvement
than constant tuning. General RH, an explicit new decimal exponent, an effective
starting height, global record and universal simplicity remain open here.
Manuscript publication, complete rendered replay QA, integration and deployment
are subsequent delivery gates and are not implied by this scientific verdict.
