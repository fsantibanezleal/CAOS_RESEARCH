# EXP-017b - Verdict: THE BASE IDEAL ITSELF CAPS IN THE S-MODEL (2026-08-02; the trade-off is measured from both sides; triage with the mod-p screen is the declared successor)

Hypothesis: `hypothesis.md`. Runner: `run.py`. Artifacts: results, run log,
the capped P0a script.

## Outcome

| Rung | Outcome | Facts |
|---|---|---|
| P0a (dim of shape + 22 s-relations, gauged, 600 s) | INCONCLUSIVE-CAP | the smoke gate itself walled: 30 generators in 34 variables with twenty-two degree-7 defining relations is already beyond the 600 s budget |
| P0b, P1..P4 | NOT RUN | the gate stopped everything before any minor was computed, exactly as declared |

## The two-sided measurement this completes

- EXP-017 (height ring, s-factors eliminated): tiny base ideal (dim 4 in one
  second) but minors of degree near 100; every bound rung capped.
- EXP-017b (s-variables retained): minors would have degree near 12, but the
  BASE ideal carrying the degree-7 defining relations already caps.

The cost lives on a see-saw: eliminate and the minors explode, retain and
the base explodes. Dias-Pan's success sat at a sweet spot our stratum does
not replicate directly: their matrix entries were single-term (each mass
appears in one product), so their distance-only pushed minors stayed near
degree 9; our reduced block sums over mirror-pair members, so every road
from it is heavier. This is now a measured structural fact about the
stratum, not a guess.

## Declared successor (EXP-017c): triage, then one long honest run

1. MOD-P SCREEN (msolve or Singular over a large prime; SCREEN-ONLY per the
   standing rule, never verdict-carrying): run all four loci systems in BOTH
   formulations at 300 s each over two primes. Mod-p Groebner cost is a
   reliable feasibility predictor for the QQ run; if a rung walls mod p, QQ
   is hopeless at any human budget and the sign-analysis lemma becomes the
   route for that k.
2. The most promising (formulation, rung) pair from the screen gets ONE
   long QQ run with a declared 6-hour cap, detached, overnight.
3. Whatever the screen says about the k = 2 case, the Dias-Pan Prop 7.2
   sign-analysis lemma (physical fibers avoid the low-rank locus by sign
   patterns) is prepared in parallel as the analytic fallback: it needs no
   Groebner bases at all.

## Soundness notes

- No mathematical claim was produced or consumed; the gate architecture
  (smoke before spend) did its job for the third time today.
- The 22 s-variables and their defining relations are archived; the
  enumeration is mechanical from the block structure and re-derivable.
