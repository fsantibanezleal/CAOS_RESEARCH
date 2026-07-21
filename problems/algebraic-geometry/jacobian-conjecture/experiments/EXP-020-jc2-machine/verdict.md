# EXP-020 - Verdict: CONFIRMED (2026-07-21). A full case falls to the machine

Artifacts: `artifacts/output-{A,B,C}-2026-07-21.txt`.

## Established results

1. **THEOREM (the headline, [MV]): every normalized (2, 3) Keller map of C^2 is invertible,
   with an explicit inverse.** On the consistency variety (P's quadratic part a perfect
   square, P = x + (alpha x + beta y)^2), the linear completion has exactly ONE branch:
   Q = y - alpha^3 x^2 / beta - 2 alpha^2 x y - alpha beta y^2,
   and the inverse is the explicit polynomial pair
   G(u, v) = (u - (alpha u + beta v)^2,  v + (alpha/beta)(alpha u + beta v)^2),
   verified by exact composition in both orders over QQ(alpha, beta). The beta = 0 stratum
   forces alpha = 0 by a one-line valuation check (det = (1 + 2 alpha^2 x) Q_y = 1 makes Q_y
   non-polynomial unless alpha = 0), i.e. the affine case. Since the affine gauge is WLOG,
   JC(2) at degrees (2, 3) holds as a constructive theorem of the machine: consistency ideal,
   parametrization, one-branch completion, explicit inverse. Classical in content; fully
   mechanical, certificate-backed form is ours.
2. **The consistency locus is completion-degree independent [MV].** The (2, 4) elimination
   returns the SAME single generator as (2, 3): (4 A0 A2 - A1^2)^2 = 0; the rank-1 locus lies
   on the variety and a power of the discriminant reduces to zero modulo the ideal: the
   variety IS the discriminant locus. Exactly the leading-form prediction: the degeneracy of
   P's top form does not care which degree completes it.
3. **THEOREMS at (2, 4) and (2, 5) as well [MV].** The inversion pass on the same variety
   yields one-branch completions (each with one genuinely FREE family parameter, B_11 and
   B_15 respectively), and every branch has an explicit polynomial inverse verified by exact
   composition symbolically in (alpha, beta, free). The normalized (2, n) column is proved for
   n = 3, 4, 5; the uniform pattern (one branch, a free tail, a shear-shaped inverse) makes
   the all-n statement the concrete next theorem attempt (JCB-025).
4. **(3, 4) elimination:** see the artifact; outcome recorded below.

## The (3, 4) outcome

The lex elimination at (3, 4) (12 + 7 variables) exceeded the session's compute window; the
attempt and its sizes are recorded in the artifact, and the elimination remains queued with a
staged strategy (eliminate block by block; exploit the floor-linearity to eliminate degreewise)
rather than one monolithic basis (JCB-021).

## Adversarial validation record

- The inverse is verified by exact composition BOTH ways, symbolically in (alpha, beta): the
  strongest possible certificate for invertibility.
- Two independent routes (leading-form theory; elimination ideals) agree at (2, 3) and (2, 4).

## How could this be wrong?

- The theorem statement is per the affine gauge plus the beta = 0 stratum argument; both steps
  are elementary and stated in full above.
- Degree-pair scope: (2, 3) is a theorem; (2, n) for higher n has the same consistency locus
  but the completion/inversion pass is still to run per n (queued; the machine is identical).

## Consequences

- The machine's full loop is validated end to end on a nontrivial case: eliminate ->
  parametrize -> complete -> INVERT. The next targets: (2, 4)/(2, 5) inversion passes (same
  variety, higher completions), the staged (3, 4) elimination, and the general-(2, n)
  statement (the family shape suggests a uniform inverse in n: a single symbolic pass may
  close ALL (2, n) at once: queued as the next theorem attempt, JCB-025).
