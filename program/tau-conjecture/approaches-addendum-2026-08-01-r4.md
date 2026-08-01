# tau-conjecture: approaches re-evaluation addendum (round 4, 2026-08-01)

Extends `approaches-evaluation-2026-08-01.md` after EXP-003's refutation of
our depth-6 prediction and this round's sweep. New sources pinned; three
new views minted (V5-V7 continuing B1-B4).

## Sweep results (fresh)

- **Cheng 2004 pinned** [V: publisher abstract]: assuming a standard
  conjecture on smooth numbers in short intervals, the ULTIMATE complexity
  of $n!$ is $\exp(c\sqrt{\log n \log\log n})$ (subexponential in
  $\log n$), with a RANDOMIZED algorithm constructing the short program.
  Route A4 gains a concrete algorithmic surface: implement Cheng's
  construction and MEASURE the programs it emits for small $n$ against
  Markstroem's exact table (a reproduction experiment with a real
  falsifiable target: does the constructed length beat $2\log_2 n!$ in
  practice at reachable $n$?).
- **SAT-based exact synthesis exists for the LINEAR case** [V: Fuhs,
  Schneider-Kamp, SAT 2010; EPFL exact-synthesis line]: shortest linear
  SLPs over GF(2) are found optimally by reducing "is there a program of
  length $k$" to SAT; the optimization problem is MaxSNP-complete. Nobody
  (found in this sweep) has applied the encoding to the INTEGER
  $\{+,-,\times\}$ model.

## New views (round-4 exploration deliverable)

### V5. The SAT/exact-synthesis lane (new computational attack)
Encode "$\exists$ SLP of length $k$ over inputs $\{-1,1,x\}$ computing a
polynomial that vanishes on the target set $S$" as SAT/SMT with bounded
coefficient width (coefficients of intermediate polynomials at depth $k$
are bounded by explicit constants, so the encoding is finite and sound
for a stated width; a width overflow flag keeps it honest). This attacks
the DUAL question $T(S) \le k$ per-target, which enumeration cannot reach
past the frontier, and it parallelizes trivially over candidate sets $S$.
Cost: encoding work; payoff: $T(S)$ values at depths 8-12 for structured
$S$ (arithmetic progressions: the dual Pochhammer-Wilkinson ladder).
ADOPTED as RL-7 (design first, EXP later).

### V6. The bottom-law object (our own falsifiable mini-conjecture)
The census says $z_{\max}(\tau) = \tau - 1$ for $3 \le \tau \le 6$. We
promote this to a NAMED object (the bottom law) and attack it in both
directions: EXP-004 decides $\tau = 7$ (our committed prediction, made
against the law after a failed hand-search for 7-gate 6-rooters, is that
the law BREAKS: $z_{\max}(7) = 5$; either outcome is a result). A proved
break would be the first measured nonlinearity of the growth function; a
continuation localizes where new-root constants come from (the census
records show new roots beyond the stable core $\{0,\pm1,\pm2\}$ need
BUILT constants, and constants cost gates).

### V7. The moves calculus (constructive upper-bound machine for T(S))
Formalize the observed mechanism moves with their proved gate costs:
multiply-by-$(x - a)$ given constant $a$ in state (+1 or +1+tau(a));
multiply-by-$x$ (+1, adjoins 0); DOS split $B^2 - A^2$ (+2 given $A, B$);
block translation (+1 per unit built); tower iterate (+2, but stall
theorem bounds its yield). A BFS over ROOT SETS using these moves yields
certified upper bounds $\hat{T}(S) \ge T(S)$ far past the census
frontier; census values calibrate the gap $\hat{T} - T$ (currently 0 at
every decided point except the tower-vs-shortcut gap found by EXP-003:
the calculus with the multiply-by-$x$ move would have found the 6-gate
5-rooter that our hand analysis missed). ADOPTED as RL-8 (cheap to
implement; feeds V6 constructions).

## Re-ranking after EXP-003

1. RL-1 census spine: EXP-004 (depth 7 via stage-1 frontier build + last-
   gate scan; engineering only, no unproved pruning; 48 GB / 24-core
   machine verified sufficient this round).
2. RL-4: the stall theorem GENERALIZED this round (see the new derivation
   note): single-map towers over ANY monic integer map of degree >= 2 are
   bounded independently of depth: they can never refute the conjecture.
3. RL-8 moves calculus (new), then RL-7 SAT lane design.
4. RL-2/RL-3 instrumentation continue inside census experiments.
5. Reading ladder: Cheng 2004 full read queued (publisher access needed);
   KPT15, Lipton, Shamir unchanged.
