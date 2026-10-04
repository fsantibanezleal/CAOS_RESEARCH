# EXP-027 verdict: complete shifted composite dual representation

[V] The finite Hurwitz expression and modular Fourier orthogonality derive
the full shifted functional equation with both inverse phases and all
residue classes. Mellin inversion gives the smooth-profile dual sum, both
pole terms, the coalescent residue and equivalent nonsingular Bessel profiles.
The proof specifies EXP-024's actual squarefree gcd family, coefficient
cutoff and both mollifier polynomial weights. This is a classical exact
transformation; no method priority or signed saving is claimed.

[V] 1,295 standard-library integer cyclotomic checks and 32 Arb functional-
equation controls pass, including q=1,3,6,8, unequal complex shifts and
equal shifts. Reversed inverse phase, reversed dual shift and omitted
composite nonunit classes are rejected. The interval paths share Arb;
the exact finite calculation and uniform analytic derivation are separate.
The declared controls used 0.15625 seconds CPU, within the 60-second budget.

The Bessel/Mellin identities are attributed DLMF inputs. Their use and
contour domains are derived in proof.md; no full independent reproof of
special-function theory is asserted. The complete Bessel weight depends on
one ratio, dual_integer/(p*q), apart from separate powers. Estimating its
Mellin separation norm is the next analytic obligation.

Disposition: research-record supporting RH-F4 / issue #360. No new moment
range, onset, zero proportion, manuscript or Zenodo version follows from
these normalization controls. A separately declared uniform weight-norm
and trilinear estimate is required before evaluating an onset gain.
