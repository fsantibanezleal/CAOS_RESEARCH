# Longer mollifiers in short zeta windows

[D] EXP-028 proves, through Bettin-Chandee's attributed trilinear theorem,
the uniform small-shift mollified second moment for fixed P,Q,R and

    1/2<theta<1, 0<nu<min(1/2,(17/33)*(2theta-1)).

The transformed profile depends on n/(pq). Its exact Mellin multiplier can
be separated with one integral, whose absolute norm is charged explicitly.
An independent exact-Hankel/Sobolev derivation agrees at the dominant dual
scale. Both retain the full coefficients, composite residues and gcd classes;
neither silently imports a global theorem as a short-window moment.

The two error exponents before narrower-window smoothing are
(17/20)(1-2theta)+(33/20)nu and 1-2theta+(15/8)nu. Inverse-heat conversion
uses theta-eta with a fixed positive eta, chosen inside the strict margin.
Both residues remain through coalescence; fixed-degree Q follows by uniform
Cauchy differentiation. The proof is in the experiment's mellin-proof.md
and hankel-symbol-proof.md; its attacks and trust limits are in proof-review.md.

[D+MV] At theta=0.5339, nu=0.0349 and eta=0.00001, both corrected exponents
are negative. The unchanged EXP-010 detector and two independent interval
arithmetic paths give h>0.0003985233159135. The localized counting/parity
transfer gives positive simple-critical density for every fixed theta in
[0.5339,1), improving the repository's 0.534 onset internally.

The finite exponent controls check 7,430 boxes and reject five wrong choices;
they test normalization and do not replace the universal analytical proof.
Bettin-Chandee, Young and Wang remain attributed inputs. External peer review,
worldwide novelty and an effective height are not established. This does not
prove RH. The manuscript v0.02 is published at
[10.5281/zenodo.23132248](https://doi.org/10.5281/zenodo.23132248), with
all fourteen final pages reviewed and both public downloads verified. Its
80-member extracted source archive replays the three arithmetic auditors.
Research PR #370 is merged and its develop CI passes. The separate 0.76.000
app release remains a delivery step until its rendered and production gates pass.
