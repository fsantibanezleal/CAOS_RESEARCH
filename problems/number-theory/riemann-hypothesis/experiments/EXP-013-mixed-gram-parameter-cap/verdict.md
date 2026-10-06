# EXP-013 verdict: confirmed fixed-input improvement and cap

Date: 2026-10-03. Declaration commit `8db97480` was pushed before implementation.
**Confirmed**: predictions A, B and C all pass. Exact fractions are the
authority; decimal bounds are directed rational enclosures, not float fits.

## Result and scope

The source choice `(m,tau,c)=(1298,12/5,17/5)` reproduces exactly
`16260119298029/19426831050000`. The feasible new choice
`(1310,2411/1000,3411/1000)` gives

    q = 62359683640669/74504434380000
      = 0.83699291404068236616012277684242718762050683727370...
    gain = 524086136423727/16082056213067461100000 > 0

The decimal display lies in a width-10^(-50) rational enclosure.
The block slack is `3601/1000000`; the off-line-pair slack is
`5497/26200000`. All other residuals are nonnegative.
The [proof](proof.md) eliminates c and tau and excludes *every* integer
m>=1311. Strict monotonicity of q then proves optimality over precisely
the fixed-input scalar-clipping assembly, rather than over a tested grid.

The zero-count consequence imports the energy and seven-point local
certificate of [Knausgard, arXiv:2609.33043v1](https://arxiv.org/abs/2609.33043v1).
It concerns distinct zeros anywhere in the strip. It is not a new
simple-critical proportion, an independent replay of the local certificate,
or a new zero-counting method. Upstream nine-point candidates are outside
this optimization. No worldwide-record or external peer-review claim follows.

## Independent and adversarial checks

The producer uses Fraction arithmetic; the [auditor](audit.py) independently
substitutes the constraints and uses SymPy to differentiate the bound and
derive the boundary polynomial. It does not import the producer.
At m=1400 a control satisfies the other constraints but violates the
off-line-pair residual: dropping that condition produces a false extension.
Tests reject corrupted inputs, bound, cap and directed enclosure; replay
is byte identical and checks the source/declaration/proof/code bindings.
These checks do not audit the external 2,168,370-node interval replay or Lean.

## Evidence and disposition

Canonical SHA-256: `c250ac76df06e8f66aaed2c720e292bf17e82923137a01ce56d9ced29d4f094b`.
Independent report: [artifacts/audit/audit.json](artifacts/audit/audit.json).
Source bytes: [additive manifest](../../context/source-manifest-20261003.json).
Research-record: a small parameter optimization of an attributed framework.
No standalone manuscript or Zenodo version is justified. RH and the onset
0.534 are unchanged. The fixed-input route RH-F6 closes at its proved cap.
