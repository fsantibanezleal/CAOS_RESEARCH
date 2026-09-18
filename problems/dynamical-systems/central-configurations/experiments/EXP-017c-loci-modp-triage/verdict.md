# EXP-017c - Verdict: THE SCREEN IS DECISIVE, THE GROEBNER ROUTE TO THE LOCI BOUNDS IS CLOSED AT HUMAN BUDGETS (2026-08-02; all ten mod-p cells capped at both primes; the stratum theorem's remaining gap is a sign-analysis lemma, which is mathematics, not compute)

Hypothesis: `hypothesis.md`. Runner: `run.sh` (byte-identical reuse of the
archived EXP-017/017b scripts, only the ring characteristic changed).
Artifacts: the ten mod-p outputs and the screen table.

## Outcome

All ten cells (four loci rungs in the height formulation + the s-model base
ideal, at primes 32003 and 1073741789) hit the 300 s timeout. P1 (the screen
completes and yields a clean table) is CONFIRMED; P2 (the guess that the
smallest rung might complete mod p) is REFUTED. Per the declared decision
rule, NO cell earns the 6-hour QQ run: mod-p walls predict characteristic-
zero hopelessness at any human budget, in both formulations.

## What this closes and what it opens

CLOSED: the computational shortcut by which the stratum theorem would have
followed from Groebner dimension bounds alone, with no manual mathematics.
Three formulations were tried and measured (cleared height ring, s-variable
ring, and their mod-p shadows); the obstruction is structural (our reduced
block sums over mirror-pair members, so every minor presentation is heavy).

OPEN, and now the declared path: the Dias-Pan Prop 7.2 pattern, adapted. What
must be PROVED (by sign analysis over the stratum's shape inequalities, with
machine-assisted exact checks but no Groebner bases):

  LEMMA CANDIDATE (rank floor on physical fibers): at every point of the
  open stratum (positive distances, u, p > 0, q != v), the 6 x 4 mass
  matrix has rank at least 2, and off an explicitly described subvariety,
  rank at least 3.

Their version of this was half a page for the cross stratum, using the sign
definiteness of specific s-factors under the shape orderings. Ours has more
cases (two pairs interact) but the same architecture, and EXP-016/018 supply
three exact points where the answer is known (rank 4, 4, 3) to anchor the
case split. The k = 4 case additionally needs either a rank-4 CC witness
(EXP-018b: a less symmetric stratum CC via the census machinery) or the
image-dimension argument, both declared for the next round.

## Honesty

- Mod-p data is screen-only throughout (the pinned rule); nothing here
  asserts a dimension over any field.
- The theorem is NOT blocked; it has moved from compute to proof-writing
  with machine verification, which is the normal shape of this kind of
  result (Dias-Pan's own 7.2 was manual). No statement exists yet.
