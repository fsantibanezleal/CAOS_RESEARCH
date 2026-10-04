# EXP-028: charge one-dimensional chirp separation in the signed moment

Declared 2026-10-04 before any control computation. RH-F4 remains primary.
The target is a uniform shifted mollified second moment for
H=T^theta, 1/2<theta<1 and

    0<nu<min(1/2, (17/33)*(2theta-1)), M<=T^nu.

This would strictly enlarge EXP-010's nu<theta-1/2 range and potentially
improve its 0.534 onset. It is currently a conjectured analytic extension,
not an established result. No further fixed-input Gram tuning is admitted.

Route: use EXP-027's complete transformed sum. On dyadic dual n~N, p~P,
q~Q, the oscillatory profile depends on n/(pq). Estimate its normalized
one-dimensional Fourier/Mellin L1 norm by
(1+sqrt(N*T/(P*Q)))^(1/2), including all finite EXP-024 profile terms.
Retain the actual Mobius/polynomial coefficients and gcd/cutoff constraints.
Apply attributed Bettin-Chandee 1502.00769v1 Theorem 1 only after proving
that norm and tail estimates. The two proposed balanced error exponents are

    E1=(17/20)*(1-2theta)+(33/20)*nu,
    E2=1-2theta+(15/8)*nu.

P1: the archived Bettin-Chandee theorem, complete statement, parameter
factor and arbitrary complex coefficient scope are checked. The source
theorem is an attributed dependency, not independently reproved here.
DLMF 10.17 supplies classical large-positive-argument Hankel expansions
and remainder bounds; their differentiated uniform use must be justified.
EXP-024/027 give the existing exact representation; EXP-010 supplies
the residue/diagonal evaluation and the frozen detector/parity transfer.
P3: all shifts, both residues through coalescence, finite Hermite terms,
compact-window conversion, unbalanced p/q blocks and the g sum remain
proof obligations. There is no theorem substitution without these checks.
P5: the one-variable dependence and separation norm decide the possible
range before any larger computation.

One fixed conditional control: theta=5339/10000, nu=349/10000, and the
already certified EXP-010 detector at nu=349/10000. Recompute both exact
error exponents and the parity lower root at the new theta using its
certified kappa lower bound. Thirty seconds CPU, one worker, no optimization.
PASS proves only conditional arithmetic compatibility and positive parity,
not the analytic moment theorem. FAIL rejects this fixed consequence or
finds a normalization mismatch. A budget hit is inconclusive.

The substantive success gate is the full uniform moment proof, adversarial
review and independently certified resulting onset below 0.534. A coherent
validated theorem belongs in a new immutable version of short-interval-
levinson; no new standalone paper is triggered automatically. Missing weight
norm, tail, residue, shift, Q or unbalanced-block control leaves the candidate
unproved. The user's stopping condition remains unmet until those gates.
