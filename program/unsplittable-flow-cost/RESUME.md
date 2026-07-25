# RESUME: unsplittable-flow cost conjecture (Goemans)

The single first-read for a fresh session on this problem (methodology/07). Updated
2026-07-24, session 1 (opening). Labels: [MV] machine-verified in this repo, [D] derived
by us on paper, [C] conjectural, [VERIFIED]/[CLAIMED]/[UNVERIFIED] as in the dossiers.

## 1. State in one screen

The object. An SSUF instance is $(G=(V,A), s, T, d, x)$: digraph, source, terminals with
demands $d \in \mathbb{Q}_{\ge 0}^T$, and a feasible fractional flow $x$ routing $d_t$ to
each $t$. Capacities are taken to BE $x$ (the worst case, per TVZ24). An unsplittable flow
$\mathcal{P} = \{P^t\}$ picks one $s$-$t$ path per terminal and has load
$f^{\mathcal{P}}(a) = \sum_{t: a \in P^t} d_t$. Write $d_{\max} = \max_t d_t$.

Proved (DGG 1999): there is always $\mathcal{P}$ with
$$f^{\mathcal{P}}(a) \le x(a) + d_{\max} \quad \forall a. \qquad \text{[VERIFIED as a statement]}$$

Goemans' conjecture (STVZ25 Conjecture 1.2, verbatim in our dossier): additionally
$c^T f^{\mathcal{P}} \le c^T x$ for a given $c \ge 0$. Three neighbours: MS Conj 1.3
(two-sided $x - d_{\max} \le f \le x + d_{\max}$, no cost, acyclic), MS Conj 1.4
(two-sided plus cost), Conj 1.5 (two-sided at $2d_{\max}$ plus cost). Lattice:
1.4 $\Rightarrow$ 1.3 and 1.4 $\Rightarrow$ 1.2 (Goemans is WLOG acyclic); STVZ25
Theorem 1.6: 1.3 $\Rightarrow$ 1.5.

Status of the record entering 2026 [VERIFIED from primary sources]: Conj 1.2 open in
general; proved for series-parallel digraphs (MSW25, in the stronger convex-combination
form with STRICT deviation less than $d_{\max}$) and for demands that are multiples of one
another (Sku02); planar known only at $2 d_{\max}$ (TVZ24). STVZ25 (2025-10-24): "it
remains wide open whether Goemans' conjecture holds even with a weaker capacity violation
of $O(d_{\max})$".

The live claim [CLAIMED, unadjudicated as of this writing]: a 2026-07-22/23 announcement
(Rybin with GPT-5.6 Pro, amplified widely, no preprint, no expert confirmation found) of a
7-vertex planar counterexample. Felipe supplied the artifact bundle. Instance transcribed
exactly in the counterexample dossier; the key numbers are $d = (15, 10, 15)$,
$d_{\max} = 15$, $c^T x = 58$, and the assertion that every congestion-good routing costs
at least 60. Mechanism claimed: three zero-cost detours pairwise congestion-incompatible
(a conflict triangle) with fractional selection mass $1/3 + 2/5 + 1/3 = 16/15 > 1$.

Our reading of that mechanism, produced this round [D]: it is the LP-integrality gap of
the stable-set polytope on a triangle, transported into flow language. Build the CONFLICT
GRAPH $H$ on cheap choices (edge = cannot both be selected within budget), let
$\rho_i = x(\text{choice } i)/d_i$; a counterexample needs $\rho$ outside the stable-set
polytope of $H$ and that violated inequality separable by nonnegative arc costs.

What is decided in this repo so far: NOTHING by machine yet. Session 1 was the research
and planning pass. EXP-001 (the checker) is the shakedown; EXP-002 adjudicates the claim.

## 2. The objects table

| Object | Definition | Owner |
|---|---|---|
| SSUF instance | $(G, s, T, d, x)$ with capacities equal to $x$ | context/base-review, literature dossier |
| congestion-good routing | $f^{\mathcal{P}}(a) \le x(a) + d_{\max}$ on every arc | EXP-001 checker |
| cost-good routing | $c^T f^{\mathcal{P}} \le c^T x$ | EXP-001 checker |
| $\alpha_{\mathrm{inst}}$ | $\min_{\text{cost-good } y} \max_a (y_a - x_a)^+ / d_{\max}$: the violation an instance forces | EXP-002 (Q4) |
| $\alpha^\*$ | the infimum of $\alpha$ over ALL instances: the frontier constant, $\le 2$ for planar, otherwise unknown | UF-P3 |
| conflict graph $H$, selection point $\rho$ | the stable-set reading of an instance | UFB-023, RL1 |
| separation LP | max $\delta$ s.t. $c^T(y - x) \ge \delta$ for all congestion-good $y$, $\sum c_a = 1$, $c \ge 0$; optimum $> 0$ iff some nonnegative cost makes the instance a counterexample | UFB-010 [CLAIMED, to re-derive] |
| C1-C9 battery | the consistency tests any valid counterexample must survive | literature dossier section 5 |

## 3. Experiment index

| EXP | Question | Verdict |
|---|---|---|
| EXP-001 | Does our own exact checker decide SSUF instances correctly on hand-built cases with known answers? | declared, running |
| EXP-002 | Is the 2026 claimed counterexample valid, and what exactly does it force? | not yet declared |

## 4. In flight

EXP-001, the exact instance checker (UF-P0). Design decisions fixed before the run: exact
arithmetic only (`fractions.Fraction`, floats banned); paths enumerated by our own DFS
over simple paths, never taken from an input list; the routing enumeration is the full
Cartesian product over per-terminal path sets; every reported quantity is an exact
rational. Validation set: (V1) a single terminal with two paths, (V2) parallel paths from
$s$ to one terminal, (V3) a capacity-free instance where the cheapest routing is trivially
cost-good, (V4) a DGG-tight instance where congestion-goodness is achievable but only
barely, (V5) an instance with a cycle in the digraph to confirm the simple-path
enumeration terminates and is complete.

Mid-derivation note not yet in any verdict [D]: with at most two terminals, the conflict
graph has at most two nodes, hence no odd cycle, hence its stable-set polytope is integral
and $\rho$ cannot be separated by a nonnegative cost vector; so no counterexample can have
fewer than three terminals. This is the base rung of the minimality ladder (UFB-025) and
needs to be written up properly and machine-checked before it is claimed.

## 5. Next actions, ordered

1. Finish EXP-001: `.venv/Scripts/python.exe problems/optimization-geometry/unsplittable-flow-cost/experiments/EXP-001-exact-instance-checker/run.py`, artifacts tee'd, verdict written honouring the machine.
2. Declare EXP-002 (hypothesis BEFORE the run) with the pre-registered expectations already recorded in `state.md`: the instance verifies; $\alpha_{\mathrm{inst}} = 16/15$; Conj 1.3 and Conj 1.5 survive on it.
3. Run EXP-002; write the verdict including the corollary cascade (Conj 1.4 and the convex-combination form) with acyclicity CHECKED, not assumed.
4. Wiki 01-03 transcribed from the dossiers and the EXP-002 verdict, in the same session the verdict lands.
5. Then instruments: UFB-023 (conflict-graph invariant, cheapest), UFB-010 (exact rational separation LP), UFB-022 (series-parallel / $K_4$ recogniser), UFB-011 (canonical form) toward the minimality exhaustion (UFB-012) and the alpha frontier (UFB-030).
6. Standing every round: UFB-060 literature re-search (this area is active; the positive-result authors may respond publicly at any time), read primary sources only.

## 6. Where everything lives

| What | Path |
|---|---|
| Problem tree | `problems/optimization-geometry/unsplittable-flow-cost/` |
| Dossiers | `.../context/` (base review, literature status, claimed counterexample, references) |
| Experiments | `.../experiments/EXP-NNN-*/` |
| Code library | `.../code/ufclib/` with pytest tests |
| History log | `.../history/log.md` (append-only) |
| Wiki | `.../wiki/` |
| Program files | `program/unsplittable-flow-cost/` (this file, plan, backlog, state, lenses, research lines) |
| Mirror (management repo) | `_CAOS_MANAGE/plans/caos-research/unsplittable-flow-cost/` (status, findings, history) |
| Heavy artifacts and sources | `E:\_Datos\caos-research\unsplittable-flow-cost\` (sources, claimed-counterexample bundle), hashed in the dossiers |

## 7. Gotchas

- **Capacities are $x$, not a separate vector.** Every statement in this area measures
  violation against the fractional flow. Reading a theorem with a separate $u$ in mind
  silently changes it.
- **Path enumeration completeness is THE failure mode** in this problem. The proposer's own
  transcript records earlier candidates dying because only intended paths were checked.
  Never accept a supplied path list; always enumerate, always assert the count.
- **The proposer's verifier is archived but must never be executed or imported.** Agreement
  reached through shared code is not evidence.
- **No floats anywhere in this problem.** Every quantity is a rational of modest size; there
  is no exploration regime that needs them, so there is no exception to grant.
- **A refutation of Goemans does not refute Conj 1.3 or Conj 1.5**, and does not touch the
  $O(d_{\max})$ question. The public coverage blurs these; our writing must not.
- **Statement-level claims and all external actions are gated on Felipe.** This includes any
  public statement about whether the celebrated counterexample stands.
- Environment: repo `.venv` (Python 3.13.0, sympy 1.14.0). Temp on `E:\_Temp`. Rounds close
  with NO version bump (methodology/08).
