# EXP-016 verdict: confirmed trace-aware refinement

Date: 2026-10-03. Declaration 0ea1f332 was pushed before implementation.
**Confirmed**: predictions A, B and C pass, with exact arithmetic and a
uniform proof. The elementary Jensen/variance mechanism is prior art;
the consequence is a source-based refinement, not a new matrix method.

## Result

When sum x_i=0 and max x_i>=tau>0,
sum psi_tau(x_i)>=tau^2 m/(m-1). Equality has one displacement tau
and all others -tau/(m-1), realized by a PSD equicorrelation matrix.
This replaces the source's block condition delta(m-6)<=tau^2 by
delta(m-6)<=tau^2 m/(m-1), with no change to its other inputs.

The fixed choice m=1311,tau=2411/1000,c=3411/1000 gives

    q = 69341429073721/82845897125000
      = 0.83699291672944147624860426665335600951161768229810...
    gain over EXP-013 = 174695378807909/64972491642124138500000 > 0
    gain over source = 2271039924502817/64377329865322229250000 > 0

The directed decimal enclosure has width 10^(-50). The modified block
slack is 1564727/437000000 and the off-line-pair slack is
91673/437000000. A positive signed square test at 1312, together with
monotonicity, excludes every larger integer block in this revised
scalar-clipping assembly. Thus m=1311 is optimal for that assembly.
EXP-013's m=1310 optimum stays valid for its original block condition.

## Independent checks and failed attempt

The auditor independently derives the scalar derivative and block cap,
substitutes exact fractions, and computes the equality matrix's rational
eigenvalues. A control without trace zero violates the stronger bound;
tests also reject corrupted bound, cap, trace, condition and enclosure.
The 11 new tests plus the previous 20 focused controls pass, with
byte-identical replay and all code/proof/declaration/source bindings.

Audit attempt 1 failed a structural SymPy equality between algebraically
equivalent expressions. [The failed report](artifacts/audit/audit-run1-failed.json)
is retained. Replacing it by simplify(lhs-rhs)==0 fixes the comparison;
the derivative formula and producer certificate did not change.
The [independent audit](artifacts/audit/audit.json) now passes.
Canonical SHA-256: `7b0346f7e5122efc2a5d48dc6ceb6c28f0e8341cc8a5cf57be6863a16d1c2d74`.

## Attribution and disposition

The distinct count is strip-wide. Its zeta consequence inherits
Knausgard 2609.33043v1's analytic energy, smoothing/pinching and
seven-point interval input. No complete external interval replay or
Lean extension was performed. Classical trace/variance inequalities
are background, as recorded in the dated preflight; no worldwide
priority or external expert-review claim follows.

Supporting research-record, no standalone manuscript or Zenodo trigger.
It does not lower the 0.534 onset or prove RH. RH-F7 closes at its cap;
other convex block estimates, certificates and windows are outside the cap.
