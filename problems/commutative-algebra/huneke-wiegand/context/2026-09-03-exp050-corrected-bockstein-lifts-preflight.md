# EXP-050 preflight - provenance-preserving corrected Bockstein lifts

Date: 2026-09-03. Scope: HWB-076, the stable relative inclusions `58->59` and `58->62`.

## Source and novelty check

The fresh targeted search covered explicit Bockstein lifts, integer-chain torsion algorithms, and
integral Morse theory. It found no published construction for the CAOS relative matrices.

- The defining Bockstein calculation lifts a mod-two cycle `z`, divides its even integral boundary
  by two, and takes the resulting class modulo two. This standard construction identifies the
  bookkeeping that EXP-048 discarded after reduction.
- Stanley's Smith-normal-form survey, <https://arxiv.org/abs/1602.00166>, confirms that the exact
  claim belongs to the integer column lattice, not only to ranks over fields.
- Kozlov, <https://arxiv.org/abs/cs/0504090>, and Jollenbeck and Welker,
  <https://arxiv.org/abs/math/0501179>, support later chain-equivalent Morse compression over
  integer coefficients. Neither source provides the required matching or correction formulas.
- Autry et al., <https://arxiv.org/abs/1804.06632>, supplies the squarefree-divisor-complex
  setting but does not decide the relative connecting torsion.

EXP-049 proves that each literal zero-one chain `a` needs a nonzero even correction. Constructing
and classifying that correction is new work, not a repeated Smith or rank computation.

## Exact bookkeeping identity

For a binary kernel combination `z`, let `Rz=2b`. If quotient reduction removes an image vector
`Rw mod 2`, perform the same operation integrally:

```text
b' = b-Rw,       y' = z-2w,       Ry'=2b'.
```

If two Bockstein candidates are added during row reduction, add both their `b` and `y` witnesses.
At the end, each canonical parity vector `a` therefore carries an exact pair

```text
b=a+2c,       Ry=2b.
```

This is the cheapest route because it derives the witness during the already necessary binary
reduction. A second HNF or Smith solve would recover existence but erase the reduction provenance.

## Premises and one-sidedness

1. EXP-047 CONFIRMED FINITELY: the compact relative matrices have exact torsion `(Z/2)^2`.
2. EXP-048 REFUTED with retained formulas: the canonical parity vectors are the displayed
   `alpha/beta` chains.
3. EXP-049 REFUTED with P3 retained: the literal `a` vectors are not torsion, and bounded duals
   prove their finite independence.
4. Hypothesis: provenance-preserving reduction exposes corrections simple enough to transport in
   `p`. This is not implied by any prior verdict.

A pass of the exact identities supplies finite corrected representatives, not an all-parameter
theorem. A failure of the structural prediction rejects this canonical provenance section, not
the existence of other simple representatives.

## Adversarial route and budget

The primary runner uses low-pivot semantic quotient reduction with exact witness vectors. The
auditor will use reversed relation traversal and high-pivot reduction, then verify the two
Bockstein subspaces, all exact multiplications, and correction parity without trusting the stored
primary witnesses.

- Smoke: `p=8`, at most 180 seconds and 8 GiB.
- Full range: `p=8,...,11`, at most 900 seconds and 12 GiB, with an atomic checkpoint per
  inclusion.
- Stop on a premise hash mismatch, an odd lifted boundary, disagreement with the frozen EXP-048
  parity subspace, or any exact multiplication failure.
- A budget stop is inconclusive and does not validate a correction pattern.

## Exploration moment

The new viewpoint is that quotient reduction should be treated as a chain operation with
provenance, not as bit-vector cleanup. This may reveal the missing correction directly. If the
canonical corrections are still opaque, the bounded dual formulas remain the leading lower-bound
route and the primal task shifts to solving a small support-minimization problem modulo four.

No manuscript or Zenodo update is opened. The publication trigger remains a uniform construction
and upper bound, or a comparably transferable theorem.
