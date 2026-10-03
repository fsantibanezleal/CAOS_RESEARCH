# EXP-021: exact shifted composite character layer

Declared 2026-10-03 before implementation or machine controls. This bounded
layer belongs to the existing RH-F4/RH-038 reduction target; EXP-020's full
stronger interval run continues with its runtime source frozen.

## Mathematical target and value

For coprime positive integers a,h, let e(x)=exp(2*pi*i*x),
sigma_(alpha,beta)(n)=sum_(uv=n) u^(-alpha)*v^(-beta), and
D(s,a/h)=sum_n sigma_(alpha,beta)(n)*e(a*n/h)*n^(-s).
Prove an exact all-composite, shifted decomposition into characters modulo
every q=h/d, d|h, with all non-unit residue classes and Euler corrections
retained. The initial domain is absolute convergence,
Re(s+alpha)>1 and Re(s+beta)>1; any continuation must follow a proved identity.

Convert each induced character to its primitive conductor before applying
the functional equation. Retain parity, Gauss sums, gamma ratios and shift
dependence. In the squarefree outer-mollifier case, check which Möbius signs
cancel against induction Gauss factors; do not infer cancellation of the
remaining signed sum from that algebraic simplification.

This removes a precise arithmetic premise gap in the short-window route.
It is not the full shifted short-window reciprocity theorem, its uniform
error, a longer mollifier, a new onset, or a solution of RH. The mechanism is
classical character orthogonality and Euler products, with no priority claim.

## Predictions and invariant first

A. The gcd partition n=d*m, gcd(m,h/d)=1 gives the complete character sum.
Its coefficient is tau_q(bar(chi))*chi(a)/phi(q). Non-unit terms cannot be
discarded.

B. For p^b||d, the shifted local numerator is
sigma(p^b)-p^(-alpha-beta)*sigma(p^(b-1))*chi(p)*p^(-s)
when p does not divide q; it is sigma(p^b) when p divides q.
The two Euler denominators are those of L(s+alpha,chi)*L(s+beta,chi).
This formula has no division by sigma(p^b), avoiding zeros at complex shifts.

C. The unshifted prime case agrees with the arithmetic character split in
Tang's Section 3, including the principal and divisible terms. Composite
and unequal-shift coefficient controls distinguish deliberately omitted gcd
classes, wrong local signs and improper use of primitive Gauss normalization.

Read Tang's full pinned source and the established DLMF character/Gauss
identities before deriving the layer. Existing EXP-012 is inconclusive, and
EXP-014/015 concern phase resolution; none proves the needed signed reduction
or cancellation. The invariant is the exact prime-power recurrence for the
shifted divisor coefficients, paired with finite character orthogonality.

## Controls, cost and one-sidedness

Use symbolic formal prime-power coefficients and exact cyclotomic finite
character sums on small composite moduli (including non-cyclic unit groups),
plus a direct rational coefficient implementation at unequal integer shifts.
Restore alpha=beta=0 and prime moduli as known-input anchors. Include the
conductor-one convention explicitly. CPU only, one process, expected under
two minutes, five-minute compute budget. Emit flushed progress between
moduli and retain the receipt. If a control exceeds the budget, preserve
partial checks and mark it incomplete; the written proof must still be audited.

PASS requires a general derivation, exact non-unit and unequal-shift controls,
primitive-conductor functional-equation bookkeeping and discriminating
negative controls. It proves this supporting arithmetic layer only. FAIL
refutes a formula or implementation; it does not disprove the analytic route.
No numerical L-value average can establish this target. No separate manuscript
or Zenodo deposit is warranted unless a substantive uniform moment or
cancellation theorem is subsequently proved. This round cannot fulfill the
user's requested stopping condition by itself.
