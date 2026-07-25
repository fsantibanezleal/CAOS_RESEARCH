# RESUME: unsplittable-flow cost conjecture (Goemans)

The single first-read for a fresh session on this problem (methodology/07). Updated
2026-07-24, session 1 close (opening plus round 1: EXP-001 and EXP-002 both CONFIRMED).
Labels: [MV] machine-verified in this repo, [D] derived by us on paper, [C] conjectural,
[VERIFIED]/[CLAIMED]/[UNVERIFIED] as in the dossiers.

## 1. State in one screen

The object. An SSUF instance is $(G=(V,A), s, T, d, x)$: digraph, source, terminals with
demands $d \in \mathbb{Q}_{\ge 0}^T$, and a feasible fractional flow $x$ routing $d_t$ to
each $t$. Capacities are taken to BE $x$ (the worst case, per TVZ24). An unsplittable flow
$\mathcal{P} = \{P^t\}$ picks one $s$-$t$ path per terminal and has load
$f^{\mathcal{P}}(a) = \sum_{t: a \in P^t} d_t$. Write $d_{\max} = \max_t d_t$.

Proved (DGG 1999): there is always $\mathcal{P}$ with
$$f^{\mathcal{P}}(a) \le x(a) + d_{\max} \quad \forall a. \qquad \text{[VERIFIED as a statement]}$$

Goemans' conjecture (STVZ25 Conjecture 1.2): additionally $c^T f^{\mathcal{P}} \le c^T x$
for a given $c \ge 0$. Neighbours: MS Conj 1.3 (two-sided
$x - d_{\max} \le f \le x + d_{\max}$, no cost, acyclic), MS Conj 1.4 (two-sided plus
cost), Conj 1.5 (two-sided at $2d_{\max}$ plus cost). Lattice: 1.4 implies 1.3 and 1.2
(Goemans is WLOG acyclic); STVZ25 Theorem 1.6: 1.3 implies 1.5.

Record entering 2026 [VERIFIED from primary sources]: Conj 1.2 open in general; proved for
series-parallel digraphs (MSW25, in the stronger convex-combination form with STRICT
deviation below $d_{\max}$) and for demands that are multiples of one another (Sku02);
planar known only at $2 d_{\max}$ (TVZ24). STVZ25 (2025-10-24): "it remains wide open
whether Goemans' conjecture holds even with a weaker capacity violation of $O(d_{\max})$".

**THE CONJECTURE IS FALSE [MV, EXP-002].** The 2026 claim (announced 2026-07-22/23 outside
peer review, no preprint and no expert confirmation found; Felipe supplied the artifact
bundle) was adjudicated here by our own exact enumeration and it VERIFIES. The instance:
$V = \{s, u, v, w, t_1, t_2, t_3\}$, $d = (15, 10, 15)$, $d_{\max} = 15$, nine arcs (table
in wiki 03 and in the counterexample dossier), $c^T x = 58$. Exactly two simple paths per
terminal, the expensive direct choice $E_i$ (cost 30 each) and the free detour $Z_i$ (cost
0), so eight routings. The four congestion-good ones cost 90, 60, 60, 60; the four
cost-good ones each violate a bound. The two sets are disjoint, so no routing is both.

The mechanism [MV for the numbers, D for the reading]: the three free choices are PAIRWISE
congestion-incompatible ($Z_1 Z_3$ overloads $u \to v$ with $30 > 29$; $Z_2 Z_3$ overloads
$v \to w$ with $25 > 24$; $Z_1 Z_2$ overloads $s \to u$ with $40 > 39$, because $t_3$ uses
that arc on either of its paths), so the conflict graph is a TRIANGLE with independence
number 1; every congestion-good routing pays for at least two expensive choices, and
$30 + 30 = 60 > 58$. Equivalently, with
$\rho_i = x(\text{free choice } i)/d_i = (1/3, 2/5, 1/3)$, the fractional flow buys
$\sum_i \rho_i = 16/15 > 1$ units of free routing while any integral congestion-good
routing buys at most 1: the stable-set LP-integrality gap on a triangle, separated by
nonnegative arc costs.

**The quantitative content, which the announcement did not state [MV]:**
$\alpha_{\mathrm{inst}} = 16/15$ exactly. A cost-preserving rounding of this instance needs
16 units of slack on one arc where the conjecture allows 15. The conjecture is refuted by
ONE unit, and the $O(d_{\max})$ question (the literature's named breakthrough target) is
untouched.

**Corollaries [D, hypothesis machine-checked]:** the digraph is acyclic, so Morell-Skutella
Conjecture 1.4 and the convex-combination form are false as well. **Survivors, each tested
directly on the instance [MV]:** the DGG theorem (4 congestion-good routings exist), Conj
1.3 (4 witnesses), Conj 1.5 and TVZ24 (the instance is planar and admits a cost-good
routing well within $2 d_{\max}$), Sku02 (demands 15 and 10 are not multiples of one
another), MSW25 (a $K_4$ subdivision on $\{s, u, v, w\}$ places the instance outside
series-parallel), and the two-layer case (longest path has 4 arcs).

**Two structural statements [MV ingredients, D readings]:** the class boundary is tight
(the conjecture holds on the series-parallel side of the $K_4$ boundary and fails at the
first structure past it), and the planar constant is pinched strictly between 1 (refuted
here) and 2 (TVZ24).

**And the instance is extremal, not typical [MV, EXP-004].** Maximised over ALL nonnegative
cost vectors the violation it can force is still exactly $16/15$, so the published prices
are optimal in that sense too; and over 3456 parameter points of the natural family
containing it, it is the ONLY counterexample, at exactly its published parameters (1 in 2448
at three terminals, 0 in 1008 at four). A larger forced violation needs a different conflict
structure, not different parameters.

**Published:** preprint on Zenodo 2026-07-25, v0.01, CC BY 4.0, version DOI
10.5281/zenodo.21554259, concept DOI 10.5281/zenodo.21554258. EXP-004's results are a
next-version trigger, not an edit.

## 2. The objects table

| Object | Definition | Owner |
|---|---|---|
| SSUF instance | $(G, s, T, d, x)$ with capacities equal to $x$ | context dossiers |
| congestion-good routing | $f^{\mathcal{P}}(a) \le x(a) + d_{\max}$ on every arc | `ufclib.decide` |
| cost-good routing | $c^T f^{\mathcal{P}} \le c^T x$ | `ufclib.decide` |
| $\alpha_{\mathrm{inst}}$ | $\min$ over cost-good routings of $\max_a (y_a - x_a)^+ / d_{\max}$: the violation an instance forces. Value $16/15$ on the 2026 instance | EXP-002 |
| $\alpha^\*$ | the infimum over ALL instances: the frontier constant. Known $\ge 16/15$ [MV], $\le 2$ for planar [VERIFIED], no finite bound in general | UF-P3 |
| conflict graph $H$, selection point $\rho$ | the stable-set reading: nodes are cheap choices, edges are pairwise congestion incompatibility, $\rho_i = x(\text{choice } i)/d_i$ | EXP-002, to be promoted to the library (UFB-023) |
| separation LP (SEP) | max $\delta$ s.t. $c^T(y - x) \ge \delta$ for all congestion-good $y$, $\sum c_a = 1$, $c \ge 0$; optimum $> 0$ iff some nonnegative cost makes the instance a counterexample. Re-derived and proved by us (both directions) in the EXP-003 hypothesis; implemented exactly in `ufclib.separation` | EXP-003 [MV] |
| C1-C9 battery | the consistency tests any valid counterexample must survive | literature dossier section 5; all nine passed in EXP-002 |

## 3. Experiment index

| EXP | Question | Verdict | Load-bearing output |
|---|---|---|---|
| EXP-001 | Does our own exact checker decide SSUF instances correctly on hand-built cases? | CONFIRMED | `ufclib` adopted as ground truth; P1-P8 hold on V1-V5; 14 pytest tests |
| EXP-002 | Is the 2026 claimed counterexample valid, and what does it force? | CONFIRMED | Conj 1.2 FALSE; $\alpha_{\mathrm{inst}} = 16/15$; C1-C9 pass; structural route agrees with enumeration |
| EXP-003 | Can we decide, without searching over cost vectors, whether an instance admits any counterexample cost vector? | CONFIRMED | The exact separation LP; optimum $2/7$ on the 2026 instance, attained by the published cost vector, so that vector is an OPTIMAL separator there; $k = 1$ theorem; the $k \le 2$ claim retracted and replaced |
| EXP-004 | How much violation can an instance force, maximised over ALL cost vectors, and can any relative of the 2026 instance force more? | CONFIRMED instruments, F4 REFUTED (null) | The frontier value $\alpha_{\max}$, equal to $16/15$ on the 2026 instance; and over 3456 family parameter points the ONLY counterexample is that instance at its published parameters |

## 3b. Lenses ledger (methodology/10)

| Lens | What it produced here |
|---|---|
| 1 exclusion (the spine) | Inverted into ADJUDICATION in round 1 (constrain a claimed object against every proved theorem, the C1-C9 battery), then into EXHAUSTION in round 3 (exclude counterexamples across a family box) |
| 2 anatomy | The dissection of the one known object: three free choices, pairwise incompatible, prices calibrated so the missing free mass costs more than the fractional saving |
| 3 recognition | The class boundary: series-parallel is $K_4$-minor-free, the instance is a $K_4$ subdivision, so it sits one structure past the proved class |
| 4 invariant (run first) | The conflict graph and $\rho$: the whole counterexample in one line, $\sum \rho_i = 16/15 > 1$; also gave the $k \le 2$ intuition that later proved WRONG as an argument, which is recorded |
| 6 two-sided | The exclusion failure read forwards: EXP-004's family sweep is the construction attempt, and its null result is evidence that the mechanism is extremal, not typical |
| 7 reformulation | Stable-set polytope and convex-hull separation; the frontier value as an LP over prices |
| 8 dimension ladder | The terminal ladder: $k = 1$ proved impossible, $k = 2$ open with a necessary condition, $k = 3$ realised |
| 10 adversarial | Two specification errors and one invalid derivation caught and recorded; a predicted tooling failure (UFB-033) materialised and was fixed with an independent implementation |
| 11 external dialogue | The claim itself, adjudicated rather than trusted; the separation LP re-derived in our own words before use |

## 4. In flight

Nothing is running. Rounds 1 to 3 closed: four experiments decided, the wiki transcribed,
the web page shipped, the preprint published, and one invalid derivation retracted in
writing.

**Round 3's exploration moment (methodology/11).** The new viewpoint minted this round is
that the frontier constant is measurable PER INSTANCE as an LP over prices, not only
estimable across a literature; and the null result converts the search for a larger forced
violation from a parameter question into a STRUCTURAL one, since a linear spine cannot
realise a genuine odd cycle of conflicts (UFB-037). That is a sharper next step than the
round-1 plan had.

Mid-derivation notes not yet in any verdict, to carry into the next hypothesis:

- **RETRACTED (EXP-003, G6).** The round-1 entry here claimed, as a derivation, that no
  counterexample exists with at most two terminals, via "a conflict graph on at most two
  nodes has no odd cycle". That argument is INVALID: a terminal may have many path choices,
  so the conflict graph is not a two-node graph, and the step from an integral stable-set
  polytope to the absence of a separating nonnegative cost vector was asserted rather than
  proved. What stands in its place, from the EXP-003 verdict: $k = 1$ is a THEOREM (every
  routing is congestion-good since $d \le x_a + d$, and the cheapest-path routing is
  cost-good by flow decomposition); at $k = 2$ the all-cheapest routing is always cost-good
  and is congestion-good exactly when every arc on BOTH cheapest paths carries
  $x_a \ge \min(d_1, d_2)$, so any two-terminal counterexample must contain a shared arc
  with $x_a < \min(d_1, d_2)$. A 184-instance sweep found none, which is evidence, not a
  proof. Whether $k = 2$ admits a counterexample is OPEN.
- **The open coincidence (UFB-032).** $\sum_i \rho_i = 16/15$ and
  $\alpha_{\mathrm{inst}} = 16/15$ on the 2026 instance. Structural or accidental? A general
  relation between the stable-set violation and the forced violation budget would be a
  theorem; a single instance where they differ settles it the other way and is probably
  cheap to find once the separation LP exists.
- **Why the third conflict is the interesting one.** $Z_1 Z_2$ conflict only because $t_3$
  enters through $s \to u$ regardless of its own choice. Conflicts can therefore be
  MEDIATED by a terminal that is not party to either choice, which means the conflict graph
  is not determined by the two chosen paths alone. Any generalisation to odd cycles
  (UFB-020) must handle mediated conflicts, and the EXP-002 implementation already defines
  a conflict as "every completion violates", which is the right definition.

## 5. Next actions, ordered

1. DONE (EXP-003): the exact rational separation LP. DONE (EXP-004): the frontier value,
   our own Bland-rule simplex, and the family sweep.
2. **UFB-037, the evidenced next step**: conflict structures that a linear spine cannot
   realise (a genuine odd cycle of length 5; conflicts mediated by two terminals). EXP-004
   showed parameter tuning inside the spine family is exhausted, so this is the only route
   left here to a larger forced violation. Design the digraph first, on paper, then declare.
3. UFB-036: choose the split fractions by LP rather than sampling a grid, so a counterexample
   needing an awkward $\rho$ cannot hide between grid points.
4. Declare the canonical form (UFB-011) with constraint generation (UFB-034), which together
   open the minimality exhaustion (UFB-012). Target: the smallest counterexample in
   terminals (open at $k = 2$, necessary condition in hand), vertices, arcs and $d_{\max}$.
5. Promote the conflict-graph instrument out of EXP-002 into `ufclib` (UFB-023) as the cheap
   pre-filter before any LP.
6. UFB-040: turn the same engine on the surviving cost-free two-sided conjecture.
6. Standing each round: UFB-060 literature re-search. This area is active and the authors of
   the positive results may respond publicly to the 2026 claim at any time; read primary
   sources, never coverage.
7. Reads that unlock blocked claims: UFB-002 (DGG99 Combinatorica, the augmentation
   technique) and UFB-003 (Martens-Salazar-Skutella, the convex-combination equivalence).

## 6. Where everything lives

| What | Path |
|---|---|
| Problem tree | `problems/optimization-geometry/unsplittable-flow-cost/` |
| Dossiers | `.../context/` (base review, literature status, claimed counterexample, references) |
| Experiments | `.../experiments/EXP-001-exact-instance-checker/`, `.../experiments/EXP-002-adjudicate-2026-claim/` |
| Code library | `.../code/ufclib/` with pytest tests in `.../code/ufclib/tests/` |
| Wiki | `.../wiki/` (README, 01-05, `assets/counterexample-instance.svg`) |
| History log | `.../history/log.md` (append-only) |
| Program files | `program/unsplittable-flow-cost/` (this file, plan, backlog, state, lenses, research lines) |
| Mirror (management repo) | `_CAOS_MANAGE/plans/caos-research/unsplittable-flow-cost/` (status, findings, history) |
| Sources and the claimed-counterexample bundle | `E:\_Datos\caos-research\unsplittable-flow-cost\` (hashed in the dossiers) |

## 7. Gotchas

- **Capacities are $x$, not a separate vector.** Every statement in this area measures
  violation against the fractional flow.
- **Path enumeration completeness is THE failure mode.** Never accept a supplied path list;
  always enumerate, always assert the count.
- **The proposer's verifier is archived but must never be executed or imported**, and the
  instance is re-entered by hand rather than parsed, so agreement is evidence.
- **No floats anywhere in this problem.** The constructor refuses them; a token scan keeps
  literals out.
- **A refutation of Goemans does not refute Conj 1.3 or Conj 1.5**, and does not touch the
  $O(d_{\max})$ question. Public coverage blurs this; our writing must not.
- **Statement-level claims and all external actions are gated on Felipe**, including any
  public statement about whether the celebrated counterexample stands. Nothing has left this
  repository.
- **Bash heredocs mangle backslashes here**: editing LaTeX-bearing markdown through
  `python - <<'PY'` corrupted `\rho` into a newline and `\to` into a tab in this very file.
  Use the Write or Edit tools for such files, not shell heredocs.
- Environment: repo `.venv` (Python 3.13.0, sympy 1.14.0 available but not needed so far;
  `fractions.Fraction` is the whole arithmetic stack). Temp on `E:\_Temp`. Rounds close with
  NO version bump (methodology/08).
