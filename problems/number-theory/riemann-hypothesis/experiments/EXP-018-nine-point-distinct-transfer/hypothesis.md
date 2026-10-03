# EXP-018: source-conditioned nine-point distinct-strip transfer

Declared 2026-10-03 after EXP-017 result commit 411c2613, before any
candidate arithmetic or implementation. Read the nine-point preflight.

## Prediction

Under the explicit universal local inequality for the pinned nine-point
packet, the general r-gap mixed-Gram transfer has D=delta*(m-r),
a<=F_m(D)/m, beta=r*p*(m-r)/m and q=(1+H0-beta)/(2-a), with the
unchanged c/tau threshold and high-multiplicity/off-line residuals.
At r=8, delta=15211/2500000, p=1/2500, H0=3362285207/5000000000,
m=958,tau=2409/1000,c=3409/1000 the constraints pass and q>837/1000,
strictly improving EXP-017's attributed bound. No parameter search.

## Method and dependencies

Uniform window/partition counting proof plus exact Fraction capacity
checks on all 36 packet weights. Independent SymPy reconstruction of
the counting inequality, dimensions, source/packet hash and q arithmetic;
finite exact partition enumeration only checks the implementation.
EXP-017 supplies the envelope and pressure proof; EXP-016 confirms the
mixed residuals. Source window/energy and the nine-point universal local
inequality are explicit attributed assumptions. The log/candidate metadata
discrepancy prevents claiming independent local certification.

Invariant first: span capacities at most 2 certify the weighted-to-Gram
energy passage; the r(m-r)/m partition incidence gives the pressure tax.
PASS proves the conditional transfer and exact candidate arithmetic,
NOT the universal local inequality. FAIL refutes the packet compatibility
or candidate, not the global conjecture. Finite partition tests alone do
not establish the uniform theorem; its counting proof is required.

Adversarial controls: change one weight beyond capacity, change r, p,
delta, m, q or provenance hash; reject target/candidate mismatch. Retain
the source's stale verification-needed flag and missing packet-to-replay
binding. Deterministic CPU entry points, each budget 30 seconds. No GPU,
no full 116-million-node replay. A budget hit is inconclusive.

Publication decision: a source-conditioned arithmetic transfer with an
unclosed local provenance obligation stays a research record; a coherent
verified improvement with that obligation closed would trigger a focused
manuscript. No short-window onset, simple-critical record, or RH claim.
