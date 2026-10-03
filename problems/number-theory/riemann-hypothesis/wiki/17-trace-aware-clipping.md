# Retaining trace-zero energy in a clipped Gram block

For a unit-diagonal m by m block, the eigenvalue displacements sum to
zero. If one displacement s is at least tau, Jensen on the other m-1
displacements yields clipped energy at least

    2 tau s-tau^2+s^2/(m-1) >= tau^2 m/(m-1).

The equality spectrum is realized by a PSD equicorrelation matrix.
The complementary energy strengthens the source dichotomy to
delta(m-6)<=tau^2 m/(m-1). All mixed-multiplicity and count residuals
are unchanged. EXP-016 admits m=1311 and excludes every m>=1312
within this modified sufficient-condition assembly. Its exact bound is
69341429073721/82845897125000=0.83699291672944... for distinct zeros
anywhere in the strip, conditional on the source inputs.

This draws on the classical relation between spectral displacement and
variance, not a new matrix-method priority claim. It does not contradict
EXP-013's optimum for the original condition. Other convex estimates
and local inputs are outside both caps. Authority: [proof](../experiments/EXP-016-trace-aware-clipping/proof.md)
and [verdict](../experiments/EXP-016-trace-aware-clipping/verdict.md).
