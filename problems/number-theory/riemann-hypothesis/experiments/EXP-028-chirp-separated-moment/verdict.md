# EXP-028 verdict: internally derived longer short-window mollifier

[D] The two persisted analytic derivations and the refutation review establish
the shifted mollified second moment, for fixed polynomials P,Q and R, in

    1/2<theta<1,
    0<nu<min(1/2,(17/33)*(2theta-1)).

The complete shifted composite transformation is EXP-027. Mellin multipliers
provide a simple independent route to the charged separation estimate; the
exact Hankel-symbol route also proves the original differentiated estimate.
All signed coefficients, both pole residues, coalescence, far tails,
unbalanced blocks, gcd sums and fixed-order general-Q derivatives are retained.
Compact-window conversion explicitly uses theta-eta and preserves the window
mass, including EXP-010's logarithmic edge smoothing. See mellin-proof.md,
hankel-symbol-proof.md and proof-review.md. Internal proof review is complete;
external review and worldwide priority remain unconfirmed.

[MV] For the frozen theta=5339/10000, nu=349/10000, eta=1/100000, the two
charged Gaussian exponents are -7/250000 and -937/400000. The un-narrowed
exponents are -9/200000 and -189/80000. The old nu<theta-1/2 range rejects
this nu. Exact rational dyadic controls pass 7,430 configurations and reject
five wrong alternatives. Native intervals and independent stdlib Fraction
intervals certify, using the unchanged EXP-010 detector,

    kappa >= 62587441630700832326901419310999470251/(25*10^38),
    h(5339/10000;kappa) > 0.0003985233159135.

[D+MV] EXP-010's existing counting and parity transfer therefore gives a
positive asymptotic proportion of simple critical zeros in every interval
(T,T+T^theta] for each fixed theta in [0.5339,1). This internally improves
the repository's established onset 0.534. It is a theorem through attributed
Bettin-Chandee, Young and Wang inputs, not an RH proof, an effective-height
claim or a global-record assertion. Monotonicity in theta keeps the same
fixed detector admissible for every larger theta below one.

Disposition: primary-manuscript, short-interval-levinson next immutable
version. The substantive gain is the analytic mollifier-range extension;
the decimal consequence is independently certified, without a new search.
Manuscript, publication, promotion and deployment remain open delivery work.
Earlier conditional receipts retain their original false theorem flags.

## How could this be wrong?

Finite controls do not prove the moment theorem. Its proof is the analytical
assembly and second derivation, which can still contain an overlooked error.
The attributed trilinear theorem and Wang's recent pair theorem were not
independently formalized here; the latter remains a recent preprint input.
An external specialist could identify a missed analytic or prior-art issue.
The tiny margin and very large fixed smoothing/detector constants provide no
practical finite-height verification. Public persistence will not constitute
peer review or establish worldwide novelty. RH remains open.
