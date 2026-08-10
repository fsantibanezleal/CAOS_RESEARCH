# 05: Open questions and the standing program board

Transcribed 2026-08-02 (round 7 close). Each question is stated with its
current exact status and the route assigned to it.

## Decided so far (for contrast)

$z_{\max}(1..7) = 1, 2, 3, 3, 4, 5, 5$; thresholds: 3 roots at 3 gates,
4 at 5, 5 at 6, **6 at exactly 8** (EXP-006, both directions machine-
verified); single-map towers bounded (stall theorems); the quadratic
family loophole empty; integer polynomial cycles have length at most 2.

## Open, with routes

1. **The exact value of $z_{\max}(8)$** (known: $\ge 6$). Includes: does
   an 8-gate SEVEN-rooter exist? Sub-question queued cheaply: among the
   408 EXP-006 hits, was any union of size 7 (the artifact truncated
   retention; a re-scan with full retention is ~2.4 h). Routes: hit
   re-scan; then the $\pm$ final-gate case via the SAT lane (design
   note 2026-08-02); full depth-8 census via TCB-005
   canonicalization/compiled backend (~$10^9$ states).
2. **The seven-root threshold** (known: $\ge 9$... precisely: $\ge 9$
   only if $z_{\max}(8) < 7$, currently unknown; upper witness needed).
   Route: moves calculus with the corrected cost model (chained
   subtraction sharing), then SAT.
3. **The bottom-law shape**: after plateaus at 4 and 7, does the growth
   function settle to steps of $\sim$2-3 gates per root (constant-
   building friction)? Data at depth 8+ needed.
4. **$N_2(s)$ growth** (Rojas' valuation-spectrum window
   $[s, s(s+1)/2]$, true rate open): our records so far concentrate on
   valuations $\{0, 1\}$. Route: RL-2 record hunt over enumerated
   additive-complexity classes.
5. **The p-adic factory question** (Rojas): does a p-adic analogue of
   the logistic root factory exist? Beyond our current tooling; tracked
   as a reading/dialogue item.
6. **Markstroem's integer frontier**: extend past length 11; his
   monotonicity question for $\tau(n!)$. Route: RL-5 with addition-chain
   canonicalization; multiprocess DFS.
7. **Non-consecutive record root sets** (EXP-006 discovery: five-rooters
   with holes, e.g. $\{-1,0,1,2,4\}$): what mechanism produces them,
   and do punctured sets become the norm at higher $z$? Route: anatomy
   pass over the EXP-006 hit gallery.
8. **Uniform stall bounds across map families** (V8): import
   Morton-Silverman/Doyle-Poonen uniform boundedness to make $Z(h)$
   uniform over families with bounded constant-cost. Route: reads
   first (TCB-023/024), then a derivation note.

## Standing honesty note

None of these decide the conjecture. The program's product is the exact
map of its bottom: thresholds, mechanisms, obstruction theorems, and
data where the literature has none, shipped as versioned Zenodo records
(concept DOI 10.5281/zenodo.21753438).
