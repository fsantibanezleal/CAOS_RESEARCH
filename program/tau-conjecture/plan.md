# Shub-Smale tau conjecture (Smale 4): program plan

Opened 2026-08-01 from the full deep-research pass
(`problems/computation-complexity/tau-conjecture/context/2026-08-01-deep-research-dossier.md`).
Scoped 2026-07-20 in the portfolio scoping dossier. Feasibility A; GPU yes
(massive SLP enumeration in the deep-frontier stages).

## 1. The problem

For $f \in \mathbb{Z}[x]$ computed by a constant-free SLP of length
$\tau(f)$ (gates $+,-,\times$; free constants $-1,0,1$; input $x$), the
conjecture asserts $z(f) \le (1+\tau(f))^c$ for a universal $c$, where
$z(f)$ counts distinct integer roots. Open since 1995. It implies
$P_{\mathbb{C}} \ne NP_{\mathbb{C}}$ (Shub-Smale) and $VP^0 \ne VNP^0$
(Buergisser 2009); the single sequence $(n!)$ being hard to compute already
gives the Valiant separation. No nontrivial lower bound on $\tau(n!)$ is
known; the real-zeros analogue is false.

## 2. What an offline exact-computation program can genuinely contribute

1. **The polynomial census** (apparently unpublished): exact
   $z_{\max}(\tau) = \max \{ z(f) : \tau(f) \le \tau \}$ for small $\tau$,
   with extremal witnesses, via canonicalized exhaustive enumeration in
   exact arithmetic. The growth data and the WITNESS MECHANISMS are the
   experimental image of the conjecture.
2. **The integer census extension**: Markstroem 2014 exhausted length <= 11
   on 2013 hardware; extend the exact $\tau$/$\tau'$ tables for $n!$ and
   $p\#$, and probe his open Problem 2.1 (monotonicity of $\tau(n!)$).
3. **Mechanism anatomy**: classify the structural families that realize the
   records (shifted products, composed squarings, subtraction tricks) and
   measure whether their $z$-rate stalls linearly in $\tau$.
4. **Ceiling checks**: once Rojas 2003 is read in full, compute additive
   complexity alongside $\tau$ in the census and compare measured records
   against the $e^{O(s\log s)}$ 2-adic rational-root ceiling.
5. **Honest exposition**: the verified implication ladder (BSS, Valiant,
   factoring) as a wiki + web page with the census data visualized.

Non-claims: no finite computation decides the conjecture; a proof is not a
promised deliverable; null results (e.g. "records stay linear as far as we
can exhaust") are valid products.

## 3. Lenses (methodology 10; spine + at least two others)

- **Spine, lens 1 (exclusion/obstruction)**: exhaustive canonicalized
  enumeration per length = the census ladder; each completed length is a
  decided case (exact $z_{\max}$ value, machine-checked witnesses).
- **Lens 2 (anatomy/construction)**: reverse-engineer extremal witnesses;
  build candidate infinite families from observed mechanisms; their
  asymptotic $z(\tau)$ rate is the two-sided reading of the census.
- **Lens 4 (invariant-first)**: before any deep frontier push, check cheap
  deciders: degree caps ($\deg \le 2^\tau$), height/coefficient-size caps,
  2-adic valuation structure, additive-complexity subcounts. Each prunes
  the enumeration and may decide small cases without search.
- **Lens 7 (reformulation/dictionary)**: the real-tau and Newton-polygon
  variants translate root-counting into sparse-product and polygon
  combinatorics; PosSLP is the decision-side twin; Lipton's factoring
  bridge reads records as cryptographic evidence.
- **Lens 8 (parameter ladder)**: $z_{\max}(\tau)$ IS a dimension ladder;
  where does each mechanism's rate break?
- **Lens 10 (adversarial/audit)**: hypotheses before runs; independent
  verification of every witness (sympy exact root count + SLP replay);
  cross-check our integer table against Markstroem's published values
  before trusting our enumerator at the polynomial frontier.

## 4. Phases

- **TC-P0 Open + census tooling (EXP-001).** Build `tclib`: exact SLP
  evaluation over $\mathbb{Z}[x]$ (canonical dict/tuple polynomial rep),
  normalized-program enumeration with dedup (the polynomial analogue of
  Markstroem's range-isomorphism classes), exact integer-root counting
  (rational root theorem on content-reduced polynomials / sympy fallback),
  checkpointed BFS by length. Deliverable: exact $z_{\max}(\tau)$ for
  $\tau$ as far as the smoke budget allows (target $\tau \le 5$ first
  round), witness gallery, and a REGRESSION GATE: our enumerator must
  reproduce Markstroem's integer values (tau of small targets) on the
  integer restriction before its polynomial output is trusted.
- **TC-P1 Frontier push.** Canonicalization theory (prove the safe
  reductions: sign symmetry $x \mapsto -x$, program normalization lemmas)
  to cut the branching factor; push $z_{\max}(\tau)$ and the integer tables
  past Markstroem's length-11 frontier; checkpointed long runs; GPU or
  multiprocess DFS where it pays.
- **TC-P2 Mechanism anatomy.** Classify witnesses; candidate families;
  prove per-family rate theorems where reachable (these are real lemmas,
  e.g. "any family of shifted-linear products has $z \le a\tau + b$").
- **TC-P3 Ceilings and dictionaries.** Read Rojas / KPT15 / Dutta in full;
  additive-complexity co-census; 2-adic ceiling comparison; real-root
  analogue census for contrast (where the conjecture is false).
- **TC-P4 Consolidate + publish.** Wiki complete, manuscript per
  methodology 09 (replication-first: Markstroem extension + the new
  polynomial census), web problem page, diffusion.

## 5. First bounded experiment

EXP-001 (declared this round): the polynomial census at small length with
the integer regression gate. Budget: minutes-scale for $\tau \le 4$;
$\tau = 5$ only with checkpointing proven. Kill criterion and one-sidedness
in its hypothesis.md.

## 6. Adversarial validation routes

- Witness replay: every record polynomial is re-evaluated from its SLP in
  exact arithmetic and its integer roots re-counted independently
  (factorization route vs candidate-divisor route).
- Cross-tool: sympy vs pure-Fraction arithmetic on every record.
- External anchor: the integer restriction must reproduce Markstroem's
  published exact values; any mismatch stops the program (his data or our
  code is wrong; decide which with the printed witnesses in his Figures
  2-5).
- Two-sided reading: failure to beat linear-rate records at exhausted
  lengths is evidence FOR the conjecture at the bottom of the ladder, and
  is reported as such, never suppressed.

## 7. Exploration cadence

Per methodology 11: every round records an exploration moment (fresh
literature sweep on the tau-conjecture tag + arXiv, analogy scan to the
Jacobian census machinery and the addition-chain literature, invariant-first
probes) in the RESUME lenses ledger.
