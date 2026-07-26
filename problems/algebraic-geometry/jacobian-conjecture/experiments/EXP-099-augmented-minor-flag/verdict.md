# EXP-099: The common strict flag is refuted

## Result

The prediction is **REFUTED**. The 26 normalized perturbation matrices do not
preserve a common strict flag.

The exact reconstruction recovered the EXP-059 base augmented minor, including
its right-hand-side column and its nonzero determinant. After normalization by
the inverse base matrix, the union-support graph already contains a self-loop.
The loop is labelled by the \((1,0)\) parameter and has exact trace \(16\).

All three adversarial mixed determinants differed from the base determinant.
The artifact reproduced byte-for-byte with SHA-256
`9AD70E0BE384D8903AE5057FCD6B10EC64367EF68A4B8585C2109199CF307B34`.

## Source-record correction

The declaration incorrectly stated that EXP-059 observed the same determinant
at 40 mixed samples. EXP-059's verdict says the opposite: its fixed minor varied
at every completed mixed sample while remaining nonzero. The EXP-099 run
reproduces that variation.

This was a preflight error: the declaration relied on a derived summary before
re-reading the owning verdict. The hypothesis remains unchanged as the
pre-run record; this verdict corrects the premise explicitly. No mathematical
claim depends on the false sentence.

## Consequence

Do not pursue multivariate constancy of this minor through a common strict
flag. The first cycle is structurally special because \((1,0)\) changes the
coefficient of the forced \(x\) vertex. EXP-100 therefore tests whether that
direction factors as a harmless forced-vertex scaling and whether a strict flag
survives after normalization.

This refutation does not imply that the selected minor vanishes at an admissible
point, nor that the reduced bracket system is consistent anywhere.

## How could this be wrong?

- The graph criterion is sufficient, not necessary, for determinant constancy.
  Its failure alone does not prove variation. Here the independent exact mixed
  determinant checks also prove variation.
- A different augmented minor can have a simpler flag even when this selected
  minor does not.

