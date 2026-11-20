# EXP-008 preflight: the point (1,2,2,1) on (0, e, 3e, 4e) over U(H) at e = 5 in characteristics 5 and 7, and at e = 6 in characteristic 3

Date: 2026-11-20. Status: frozen before any computation of this experiment. CPU only. Exact arithmetic (integers
modulo a prime).

## Question

EXP-006 found pure pairs of forms of degree e in every odd characteristic below 2e for e = 3 and 4, and in
characteristic 3 for e = 5. With Theorems A and C the point (1,2,2,1) of (0, e, 3e, 4e) is then realized over U exactly
in the characteristics other than 2 for e = 2, 3, 4. Open: e = 5 in characteristics 5 and 7 (Theorem A covers 0 and at
least 11), and every e >= 6 in the odd characteristics below 2e.

Question: is there a pair of quintics over GF(5), and over GF(7), and a pair of sextics over GF(3), with the pure
Betti table? A pair over GF(p) settles the characteristic p.

## What is known before the run

- The pure spaces are open in the locus D_e = {rank mu_(3e)(W) <= r}, r = 2 u(2e) - 2, in every characteristic
  (reviewed note); a pure W has rank exactly r. D_e also contains the common-factor locus, of codimension h_e(3e), whose
  modules have infinite length. So the rank condition is a cheap first filter and most spaces that pass it are not
  pure.
- Counts of EXP-006 at e = 5 over GF(3): of 50,000 random spaces, 24,088 pass the rank filter, 191 have the pure
  Hilbert function and 63 are pure (share 1.26 per thousand). At e = 4 the share of pure spaces was 0.19, 0.41, 0.58
  times q^(-2) for q = 3, 5, 7; the expected codimension of the pure locus is 2 h_e(3e): 2 at e = 4, 4 at e = 5, 8 at
  e = 6.
- In characteristic 0 or at least 2e the pure locus has a component of dimension 4e - 4 through <x^e, y^e>. Below 2e
  that point is not pure and nothing is known about the dimension of the pure locus, or whether it is empty.
- The Hilbert function does not certify purity (EXP-006: about one third to one half of the spaces with the pure
  Hilbert function over GF(3) have another table).

## Cases (fixed here; a random space is drawn with the seed 20261120 + its index in its family and field, as a uniformly random 2 by u(e) matrix of rank 2, by the generator of EXP-006)

| Family | e | Field | Spaces | What is computed |
|---|---|---|---|---|
| A | 5 | GF(5) | 150,000 random | rank mu_15; when it is 70, the Hilbert function to degree 22; when it is h_5, the Betti table |
| B | 5 | GF(7) | 300,000 random | the same |
| C | 6 | GF(3) | 1,000,000 random | rank mu_18; when it is 96, the Hilbert function to degree 26; when it is h_6, the Betti table |

A family stops early once 40 pure spaces are found in it (the question is existence); the number of spaces done is
recorded and every share is stated over that number.

## Gates (a failed gate stops the run and no verdict is drawn until it is explained)

- G1 (known answers). The first three pure spaces of EXP-006 at e = 5 over GF(3) (rebuilt from their stored bases)
  are pure; <x^5, y^5> is pure over GF(11) and not over GF(5), GF(7); <x^6, y^6> is pure over GF(13) and not over
  GF(3); the routine's counts on the first 2,000 spaces of family C of EXP-006 (e = 5, GF(3)) equal the stored ones.
- G2 (second instrument). For every pure space reported (at most the first 20 per family), Singular 4.3.2 (Plural),
  with a script generated from the stored basis, gives the same Betti table.
- G3 (unit tests): h_6 and r at e = 6 against the formula; the rank routine at degree 18 against the module
  construction of `uhlib` on 10 random spaces over GF(3) and GF(13).

## Predictions

- P1. Pure pairs of quintics exist over GF(5) and are found in family A. Confidence 0.8.
- P2. Pure pairs of quintics exist over GF(7) and are found in family B. Confidence 0.75.
- P3. Pure pairs of sextics exist over GF(3) and are found in family C. Confidence 0.5: the expected codimension is
  8 and the share at e = 5 over GF(3) was a tenth of q^(-4).
- If P1 and P2 hold: for e = 5 the point is realized over U in every characteristic other than 2.

What would falsify, and what each outcome means: a family that ends without a pure space says only that the share
of pure spaces over that field is small (below about 3 divided by the number of spaces done, with 95 percent
confidence); it is not evidence that none exists, and the characteristic stays open. A pure space found and confirmed
by the second instrument settles its characteristic.

## Method and budget

- First instrument: the routine of EXP-006 (imported, not edited) on top of `code/uhlib`; second instrument: Singular
  4.3.2 with Plural through the generator of EXP-005.
- At most 8 worker processes and five hours of wall time; a family that does not finish is reported with the number of
  spaces done.
- Stored: per chunk the distribution of rank mu_(3e) and the counts; every space with the pure Hilbert function, with
  its seed, its table and, when pure, its basis.

## Outputs

`run.py`, its tests, `artifacts/results.json`, `artifacts/run.log`, `artifacts/singular/`, `results-summary.md`
generated from the results. The verdict is written by the coordinating session after its own re-check of the pure
pairs.
