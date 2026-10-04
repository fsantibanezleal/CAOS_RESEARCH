# Analytic and arithmetic refutation review

Review date: 2026-10-04. This is internal mathematical review, not an external
referee report or a formalization. Every imported theorem remains attributed.

## Exact re-derivation and distinguishing attacks

The first route uses the exact Hankel symbols and one-dimensional Fourier
separation. The second starts again from the gamma integral and bounds its
absolute multiplier norm before dyadic summation. They agree at the dominant
dual scale N0=T*P*Q/H^2, including the actual outer 1/(g*q) normalization.
They use different norm estimates: the Mellin bound is coarser below N0.
Neither needs a conjectural signed moment or an unproved uniform asymptotic
Bessel remainder. Both charge the separation loss; omitting it is ineligible.

The complete assembly was attacked at these points:

| obligation | refutation attempted | disposition and evidence |
|---|---|---|
| Phase/sign and composite nonunits | reverse inverse phase, change dual shifts, omit nonunits | EXP-027 exact integer DFT and full finite-Hurwitz controls reject these; its universal proof retains every class |
| Contour interchange | open the infinite dual series on Re u=1/4 | rejected; start in its absolute half-plane, shift finite dyadic blocks and recombine with summable tails |
| Uniform complex-order symbols | replace Hankel by an uncharged leading term | rejected; hankel-symbol-proof.md gives an exact integral and all fixed derivative bounds |
| Separation cost | charge three variable norms, or omit the chirp norm | one ratio suffices; both analytic routes recover its cost; doubled cost makes the candidate exponents positive |
| Unbounded dual n | call the entire dual range polynomial in T | rejected; charge n^epsilon for shifts/divisors and absorb it with a larger tail contour |
| Source range and imbalance | silently assume P~Q, or drop the growing parameter factor | primary Theorem 1 and its closing reciprocity argument cover both relative orders; actual factor is retained in both proofs and controls |
| Unit modulus | rely on an unspecified inverse modulo 1 | direct absolute larger-contour bound handles p=1 or q=1 because nu<2theta-1 |
| g and cutoffs | remove Mobius signs, original polynomial weights, or (g,pq)=1 | all remain in separate fixed-g coefficient sequences; g sums converge without an M loss |
| Nonoscillatory branch | discard it from an informal picture | absolute sum is O(H*(M^2/T)^sigma) for arbitrarily large fixed sigma; nu<1/2 gives the required saving |
| Residue coalescence | bound separate zeta poles by 1/(alpha+beta) | rejected; the combined contour is analytic, and maximum-modulus/Cauchy bounds cost fixed logarithms |
| Residue size | absolute outer sum introduces M | inverse gpq weights give only log powers; expansion errors are powers of H/T or T/H^2 |
| Compact window | use the original theta for narrower Gaussians | rejected and repaired explicitly: eta=1/100000; exponents at theta-eta stay negative |
| Compact-window circularity | use the desired moment to bound the inverse-heat remainder | coarse polynomial zeta and mollifier bounds suffice; fixed derivative orders absorb that bound |
| Logarithmic edge smoothing | apply a fixed-window lemma to a log-dependent cutoff without charging derivatives | all fixed powers of log T are retained; sigma_window*log T/H tends to zero; main mass is preserved exactly |
| General Q | use only a linear detector or pointwise gamma expansion | all fixed shift derivatives are obtained uniformly by Cauchy circles; the frozen degree-201 polynomial changes constants only |
| Frozen detector | silently optimize or alter its certified value | both arithmetic paths bind the exact EXP-010 receipt SHA256 and use its existing nu=349/10000 value |

The source theorem is Bettin-Chandee, 1502.00769v1, Theorem 1 (equation 1.2).
Its statement, proof outline, optimization, squarefree removal and final
reciprocity step in sections 5--7 were inspected. Arbitrary complex
coefficients and both variable orders are allowed. This does not assert
an independent reproof of the published amplifier estimates. DLMF's exact
identities supply the classical special-function inputs, with their contour
and differentiated use derived here. Young's arithmetic residue evaluation,
EXP-010's counting lemma and Wang's pair theorem remain explicit dependencies.

## Independent finite evidence

Native interval and independent standard-library rational parity controls
give h(5339/10000;kappa)>0.0003985233159135, with
kappa>=62587441630700832326901419310999470251/(25*10^38).
The exact dyadic control checks 7,430 configurations, reconstructs both
source monomials from the actual norms and confirms the all-N slope signs.
Its five wrong choices are rejected. Runtime: 0.15625 seconds CPU.

The finite grid is not the universal argument. In the universal argument
the two N slopes are positive below N0; after incrementing sigma by 4,
even the parameter growth leaves slopes -29/10 and -11/4. The p,q powers
after summing N are positive, so bounding both by M/g is valid for all
unbalanced blocks, and the two g exponents exceed one. Thus the finite
controls test a proof whose variable coverage is analytic, not inferred
from sampling.

Earlier receipts correctly retain analytic_moment_theorem_proved=false:
they certify only their conditional arithmetic. The later analytical
verdict is a separate assertion, with this review and both persisted proofs.

## Residual failure boundary

An overlooked analytic error in the published or internal inputs is still
possible. No complete Lean formalization, independent external referee,
effective starting height or empirical test of arbitrarily high zeta windows
is supplied. The source searches located no matching short-window onset,
but do not certify worldwide priority. These limits must travel with the
manuscript and application. They do not turn finite checks into a proof of RH.
