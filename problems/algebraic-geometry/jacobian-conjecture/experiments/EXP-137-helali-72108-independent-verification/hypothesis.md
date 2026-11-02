# EXP-137 hypothesis: independent verification of the claimed exclusion of (72,108)

Date: 2026-11-01. Frozen before any code is written or any external script is read for logic.

## Source preflight (methodology 12)

- Helali, "Exact Computer-Assisted Exclusion of the (72,108) Frontier in the Two-Dimensional Jacobian
  Problem", Zenodo record 21479814, version 1.0.1, 2026-07-21, archive
  `jc2-72-108-exact-certificates-v1.0.1.zip`, md5 `91255150c8c689b26dc6fb61f9d80aec` (matches the
  record). Held outside git in the data root under `caos-research/jacobian-conjecture/sources/helali-21479814/`.
  Read: the manuscript (sections 3 to 7) and the README. The author states the result is conditional on
  GGHV Proposition 4.3 being exhaustive and on a faithful transcription, and requests review.
- Transcription check already possible from our records: the two Newton configurations in Helali
  section 3 equal, vertex by vertex, our verbatim transcription of GGHV Proposition 4.3
  (`context/2026-07-22-gghv-72108-dossier.md` section 2.1, tex lines 1000 to 1007 of arXiv:2204.14178).
- Our planar programme (EXP-052 to EXP-136) never excluded `(72,108)`; it worked on a reduced linear
  system for one forced edge pattern and left simultaneous coverage open.
- The archive contains Python pickles. Pickles are code-bearing; they are never loaded with the standard
  unpickler. Certificate data are read only from text files or through a restricted unpickler whose
  class whitelist is fixed in advance (builtins and `fractions.Fraction` only), or not at all.

## Question

Do the two coefficient systems of GGHV Proposition 4.3 for `(72,108)` (Cases 1 and 2, `[P,Q] = x^2` in
`K[x, x^-1, y]`) have no common zero, as Helali's certificates claim, when every step that connects the
proposition to the certificates is re-derived by independent code?

## Falsifiable predictions

### P1: Laurent reduction, derived independently

With `t = x*y^2` and `z = y^-1`, independent symbolic code confirms `[t,z] = -1`, `x^2 = t^2 z^4`, and
derives the band equations of `[P,Q] = x^2` for the supports of Cases 1 and 2 from the polygons alone.
Its top band `J4: 2AD' - 3A'D = t^2` and the bands `J3` to `J0` agree with Helali's displayed
equations; for Case 1 it also produces the negative-band equations, and their count is compared with the
thirteen stated.

### P2: the first elimination step

With `A = t + a2 t^2 + ... + a7 t^7 + t^8` and `D = d2 t^2 + ... + d12 t^12`, `J4` determines `D` and
leaves compatibility equations in `a2..a7`. Independent exact elimination (Singular or a second CAS)
finds a zero-dimensional ideal whose eliminant in `a7` has degree 35 and is irreducible over `Q`, and it
equals Helali's `H(a7)` up to a non-zero constant when that polynomial is available in a text file.

### P3: certificate identities

Each serialized identity (Case 2: `1 = sum T_i R_i`; Case 1: the `h = 0` unit certificates on both
branches and the hard identity `h = sum T_i E_i` on `s = c`, with the involution to `s = -c`) holds when
re-evaluated by our own exact arithmetic over the stated number fields, with the generators `R_i`, `E_i`
recomputed or read from text and checked against the equations of P1 by ideal membership or exact
substitution wherever the elimination path is reproducible.

### P4: adverse controls

Corrupting one certificate coefficient, or one generator coefficient, makes the corresponding identity
fail; a deliberately wrong polygon (Case 2 with an extra vertex) changes the band equations.

## What PASS and FAIL prove

PASS of P1 to P3 gives an independent computational confirmation that both transcribed systems are
empty, conditional (as Helali states) on GGHV Proposition 4.3 being exhaustive. That is a verification
result with priority to Helali, not a CAOS discovery. A FAIL locates either an error in the claim or a
gap in the chain; either is publishable as a verification note. A step that cannot be reproduced is
reported as unverified, never assumed.

## Premise dependencies

GGHV Theorem 2.1 and Proposition 4.3 (arXiv:2204.14178) as transcribed in our dossier; Helali's
archive as data only.

## Invariant-first note

P1 and the polygon check decide whether the certificates can concern the right systems before any
identity is evaluated.

## Compute budget and kill criteria

At most 6 CPU-hours in total. Kill any single elimination that exceeds 2 hours, and report that step as
unverified with what was attempted.

## Manuscript gate

A PASS or a located FAIL updates the planar manuscript (`manuscripts/jacobian-conjecture/planar`) with a
section on the external exclusion claim and its independent verification status, and opens a strategic
review of the planar focus (JCB-098).
