# Sharp clipping envelope and pressure transfer

For m>=2 and a real zero-sum spectrum of energy E, the least possible
one-sided clipping sum equals E below tau^2*m/(m-1), and
E/m+2*tau*sqrt((m-1)*E/m)-tau^2 above it. One large positive displacement
and equal negative complementary entries realize equality. The envelope
is increasing and 1-Lipschitz, so E+pW>=D with p,W>=0 transfers directly
to clipped_energy+pW>=F(D), without an all-or-nothing energy cutoff.

The tau=1 expression and pressure transfer are due to upstream prior work:
[refined deduction](https://github.com/trmdy/zeta-simple-zeros-673137/blob/1610b97b7895ff34982260f8dcaf04a0f7b82cf7/docs/refined-deduction.md),
which attributes them to tawanerguo-cn. Scaling gives arbitrary tau.
EXP-017 supplies a uniform all-energy proof and an independent scalar
minorant. Its [verdict](../experiments/EXP-017-sharp-energy-envelope/verdict.md)
records the certified distinct-strip consequence 0.83699292567522... .
This small source-based improvement is a supporting record. The short-window
onset stays 0.534, RH remains open, and no worldwide novelty is claimed.
