# Nine-point distinct-strip transfer preflight

Pinned upstream: trmdy/zeta-simple-zeros-673137 at
1610b97b7895ff34982260f8dcaf04a0f7b82cf7. Fifteen source files,
including the complete MIT notice, are archived outside git with the
source-manifest-exp018.json bindings. The nine-point and refined-deduction
notes, candidate, nine_point.py, verifier documentation, and full
verify_general.py were read. Kernel and baseline modules are archived
but no whole-codebase line-by-line audit is claimed.

The packet uses the same perturbed window and H0 as the seven-point
input, with r=8 gaps, delta=15211/2500000, p=1/2500, 36 rational
weights of denominator 10^7 and eight stated span capacities equal to 2.
The local inequality quantifies over all nonnegative eight-gap vectors.
Finite samples cannot prove it. Upstream documentation reports a
116,272,426-node, depth-75 replay over all 96 shards. The source verifier
uses pressure, interval and certified convex-tangent pruning; no
tangent-free replay for the final nine-point packet was found.

## Provenance discrepancy and claim boundary

candidate-nine-point-final.json still labels the packet as awaiting
verification and has interval_certificate_needed=true. A separate
nine-point-final-grid4000.txt says verified=True for [0,64) and [64,96),
with identical kernel-table hashes. That log does not print a candidate
JSON hash, its target or weights. Table hashes bind the common window
tables rather than the weight/target packet. Documentation and nine_point.py
identify the final packet, but a cryptographic packet-to-run binding is
missing from the imported log. We cannot resolve this by rewriting the
upstream files. Archive the discrepancy and keep the universal local
inequality as an explicit premise of our transfer. No independent full
interval replay or unconditional mathematical acceptance is claimed.

## General transfer and value

Knausgard's seven-point block counting extends algebraically to any r+1
points whose weights have nonnegative span capacities at most 2. Each
block has m-r windows; each gap appears in at most r windows; each window
survives m-r of the m partitions. Thus D=delta*(m-r),
a<=F_m(D)/m, beta=r*p*(m-r)/m. The mixed-multiplicity and threshold
residuals are unchanged. This is a structural transfer, not a new local
certificate. A fixed m=958,tau=2409/1000,c=3409/1000 will be tested
for a conditional distinct-strip bound above 0.8370. The numerical value
is not computed in this preflight.

RH-F4 remains the sole active focus. Admit one bounded RH-F9 to decide
this source-based extension. Stop after exact capacity/counting checks,
an independent derivation and one candidate. A verified global theorem
with independently reproducible local premises would be a coherent
companion-paper candidate, separate from the two short-window papers.
A conditional substitution using a packet with incomplete replay binding
stays a supporting research record. Next value target, if successful,
is closing the certificate provenance/replay obligation, not more tuning.
