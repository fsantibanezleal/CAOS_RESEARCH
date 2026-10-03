# Dual moment range and the missing cancellation theorem

EXP-012 is inconclusive: the imported prime-twist formula does not itself
give a longer signed composite mollifier. Its dual amplitude is H/sqrt(T),
with t-range T/H, producing about sqrt(h)sqrt(T) per pair. The trivial
assembly gives nu<(2/3)(theta-1/2), and the generic large-sieve sketch
returns only nu<theta-1/2. These are bounds on a proposed assembly,
not a proved barrier to the actual moment asymptotic.

The October review finds a hybrid CIS theorem, but its height is between
fixed powers of log Q. That is different from the required polynomial
height T/H. The central-value CIS theorem stops at twist exponent v<1;
its displayed error gives no endpoint power saving. Signed weights,
shifts, gamma/parity factors and composite twists remain separate obligations.

See the [EXP-012 verdict](../experiments/EXP-012-tang-short-window-moment/verdict.md)
and [current source audit](../context/2026-10-03-update-and-dual-family-preflight.md).
The positive next target is a complete reduction followed by a proved
cancellation estimate, not a numerical average of positive L-value squares.

## Exact shifted representation now available

[EXP-024](../experiments/EXP-024-gaussian-mellin-reduction/verdict.md)
derives the exact shifted Gaussian zeta-product identity, crossed residue
and rapidly decaying dual kernel. Its finite Hermite phase expansion and
off-band integration by parts have explicit remainder estimates. A finite
inverse Gaussian smoothing construction extends this to fixed smooth
compact windows, with representation error o(H) for every fixed
1/2<theta<1 and 0<nu<1, bounded coefficients and shifts O(1/log T).

The [proof](../experiments/EXP-024-gaussian-mellin-reduction/proof.md)
retains sigma_(alpha,-beta)(n), rather than the unaltered second shift of
the generic arithmetic layer. The [compact-window extension](../experiments/EXP-024-gaussian-mellin-reduction/compact-window-extension.md)
retains the signed mixture and all mollifier signs. The representation
does not provide an asymptotic evaluation of its main divisor sum.
After a further transformation the dual length is still T*h*k/sigma^2;
crossing the empty-dual-range threshold requires signed cancellation.

Independent enclosed Gaussian/Mellin kernel integrals, finite phase
remainders, symbolic Gaussian/heat identities and a full enclosed original
zeta moment check the normalizations, including rejection of the wrong
residue sign. The analytic uniform conclusion comes from the proof.
No enlarged moment range or short-window onset follows. This is supporting
research, with classical transforms explicitly acknowledged; a separate
paper or Zenodo deposit is not justified at this stage.

The [signed-character interface](../experiments/EXP-024-gaussian-mellin-reduction/signed-character-interface.md)
preserves the substituted second shift, both primitive Euler factors and
all gcd classes. Its unshifted additive-divisor residue recovers the exact
gcd(h,k)/(h*k) normalization. It distinguishes the whole Gaussian kernel's
Mellin factor from the phase-peeled profile; canceling a gamma factor absent
from the latter would be invalid. Both Mellin frequency signs remain.
This organizes the open signed estimate and does not evaluate it.

The [short-support and non-abelian review](../context/2026-10-03-subdyadic-and-nonabelian-review.md)
connects support geometry and representation theory to this missing estimate.
A bounded-degree support graph is needed to keep a subdyadic saving when
summing interval pieces; unrestricted subdivision loses it. Fourier completion
connects inverse fractions to Kloosterman sums but requires a new frequency
concentration argument. The January 2026 improved-fraction lead was withdrawn
and is excluded. Neither alternative has yielded a signed moment bound yet.
