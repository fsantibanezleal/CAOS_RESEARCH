# tau-conjecture: RESUME (zero-loss handoff)

Updated 2026-08-01, rounds 4-5 close. First read for any fresh session, per
methodology 07. Derived view: on conflict, experiment verdicts win.

## 1. State in one screen

The problem: for $f \in \mathbb{Z}[x]$ computed by a constant-free SLP
(gates $+,-,\times$, free constants $-1,0,1$, input $x$, length $\tau(f)$ =
gate count), Shub-Smale (1995) conjecture
$$z(f) \le (1+\tau(f))^\kappa \quad (z = \#\text{distinct integer roots})$$
for a universal $\kappa \ge 1$. OPEN, even for $\kappa = 1$; fails for
$\kappa < 1$ by the geometric-progression factory
$(x-2)(x-4)\cdots(x-2^{2^j})$ (linear rate). [V: Rojas math/0304100 read in
full; Buergisser 2024 survey 4.6.]

Verified ladder [V]: conjecture $\Rightarrow P_{\mathbb{C}} \ne
NP_{\mathbb{C}}$ (SS95, via hard $(m_n n!)$); $\Rightarrow VP^0 \ne VNP^0$
(Buergisser 2009); permanent easy $\Rightarrow \tau(n!)$ polylog; with
division $n!$ IS easy (Shamir); real analogue FALSE (logistic factory:
$g_{j+1} = 4g_j(1-g_j)$, $g_j(x)-x$ has $2^j$ roots at $\tau = O(j)$);
p-adic Digit Conjecture (bound only roots with first p-adic digit 1, any
fixed prime) $\Rightarrow$ the full conjecture (Rojas Thm 1); valuation
spectrum $s \le N_p(s) \le s(s+1)/2$, growth open (Rojas Thm 2).

OUR results (exact, machine-verified, decision-complete):
$$z_{\max}(\tau) = 1, 2, 3, 3, 4, 5, 5 \quad (\tau = 1..7).$$
PLATEAUS at $\tau = 4$ and $\tau = 7$: the bottom law $z = \tau - 1$
holds only for $3 \le \tau \le 6$ and BREAKS at 7 (EXP-004). Minimal
$\tau$: 4 roots at 5 (EXP-002), 5 roots at 6 (EXP-003, multiply-by-$x$
move), 6 roots in $[8, 9]$ (EXP-004 + the 9-gate witness $q(q-2)(q-6)$,
$q = x^2 - x$). Records are DOS splittings on $x^2 - 2$; record 2-adic
spectra $\{0,1\}$. Enumerator anchored to Markstroem 14/14, sympy
284/284, and every prior census value re-derived by the interned engine
(EXP-004 internal gates). Family measurement (EXP-005): across
$x^2 - c$, $c \le 200$, max tower yield is 5, ONLY at $c = 2$; two
yield-4 series ($c = m(m+1)$: fixed/anti-fixed; $c = m^2{+}m{+}1$:
genuine integer 2-cycles); the classical cycle-length $\le 2$ ceiling
closes the iteration flank entirely.

PROVED (tower lemma, context note 2026-08-01, machine-checked): integer
periodic points of $C = x^2-2$ are exactly $\{2,-1\}$; $C^k(x)-x$ has 2
integer roots vs $2^k$ real roots at $\tau \le 2k+2$; DOS towers $G_k$
stall at $\{0,\pm1,\pm2\}$ for all $k \ge 2$ (stable integer preimage
core). METHOD (last-gate lemma, EXP-003): $z_{\max}(d+1)$ is computable
from the exhausted depth-$d$ frontier without storing depth $d+1$.

## 2. The objects table

| Object | Definition | Owner |
|---|---|---|
| $\tau(f)$ | min gates, constant-free SLP, inputs $\{-1,1,x\}$ (free-0 lemma) | EXP-001 hypothesis |
| $z_{\max}(\tau)$ | max distinct integer roots at $\tau(f) \le \tau$ | EXP-001..004 |
| tclib | enum cores + last-gate scan + exact roots + 2-adic spectra + tests | code/tclib (8 tests green) |
| DOS/Chebyshev factory | $B^2 - A^2$ splittings, inner map $x^2-2$ (doubling under $z + 1/z$) | EXP-002 verdict |
| $T(S)$ | dual set-function: min $\tau$ vanishing on $S$; conjecture = $T(S) \ge |S|^{1/\kappa} - 1$ | approaches-evaluation B1 |
| $N_p(s)$ | # distinct p-adic norms of roots at additive complexity $s$; window $[s, s(s+1)/2]$ | Rojas Thm 2 [V]; RL-2 |
| Markstroem anchors | Figure 1, arXiv:1306.3091v4 | context dossier section 5 |

## 3. Experiment index

| EXP | Question | Verdict | Load-bearing output |
|---|---|---|---|
| 001 | $z_{\max}(\tau \le 4)$ + integer regression gate | CONFIRMED | $z_{\max}(4) = 3$; gate 14/14 |
| 002 | $z_{\max}(5)$; minimal $\tau$ for 4 roots; spectra | CONFIRMED | $z_{\max}(5) = 4$; min $\tau$ = 5; DOS mechanism; spectra $\{0,1\}$ |
| 003 | $z_{\max}(6)$ via last-gate scan | census CONFIRMED; our "=4" prediction REFUTED | $z_{\max}(6) = 5$; min $\tau$ for 5 roots = 6; multiply-by-$x$ move |
| 004 | $z_{\max}(7)$: bottom law? | CONFIRMED (prediction right) | $z_{\max}(7) = 5$: second plateau; min $\tau$(6 roots) in $[8,9]$; 25.8M-state frontier exact |
| 005 | Family towers $x^2 - c$: loophole? | CONFIRMED (load-bearing); flagged clause refuted | Family max 5 only at $c = 2$; 2-cycle series $c = m^2{+}m{+}1$ discovered; cycle ceiling |

## 4. In flight

Nothing running. Standing decision-bearing question: the $[8, 9]$ window
for the minimal $\tau$ with 6 distinct integer roots. Depth-8 full
census is out of naive single-machine reach (frontier ~$10^9$ states);
declared routes: RL-8 moves-calculus construction hunt (cheap first),
RL-7 SAT-lane 8-gate decision, or TCB-005 canonicalization / compiled
backend.

## 5. Next actions, ordered

1. TCB-021: close the $[8,9]$ window (RL-8 construction hunt, then the
   RL-7 SAT encoding for the 8-gate decision if the hunt fails).
2. TCB-022: manuscript gate assessment (methodology 09): census 1-7 +
   three proved lemmas + two mechanism discoveries is likely past the
   replication-first threshold; plan before writing.
3. TCB-005: canonicalization or compiled backend (depth-8 census).
4. Reads before imports: Doyle-Poonen (TCB-024), Narkiewicz attribution
   (TCB-023), Cheng 2004 full, KPT15.
5. RL-2/RL-3: valuation-spectrum record hunt; $T(S)$ structure lemmas.

Commands: tests
`.venv python -m pytest problems/computation-complexity/tau-conjecture/code/tclib -q`;
census runs from each experiment folder via the repository checkout venv
`\.venv\Scripts\python.exe run.py`.

## 6. Where everything lives

- Dossiers: `problems/computation-complexity/tau-conjecture/context/`
  (deep-research 2026-08-01; references.md with read-status ladder)
- Approaches + lines: `program/tau-conjecture/approaches-evaluation-2026-08-01.md`,
  `research-lines-2026-08-01.md`
- Experiments: `.../experiments/EXP-001-small-tau-census/`,
  `.../experiments/EXP-002-census-depth5/` (census5.json has the full
  record gallery + witnesses)
- Code: `.../code/tclib/` (enum.py + test_tclib.py)
- Wiki: `.../wiki/` (README + 01-statement-and-history.md)
- History: `.../history/log.md` · Program: `program/tau-conjecture/`
- Mirror: `<CAOS_MANAGE>/plans/caos-research/tau-conjecture/`
- Worktree gotcha: this problem's sessions use the git worktree
  `E:\_Temp\caos-research-tau` (branch `work/tau-conjecture/open`); the
  main checkout belongs to the Jacobian session, never switch it.

## 7. Gotchas

- Worktrees carry no venv: run with the MAIN checkout venv (path above).
- Markstroem: integer model starts from 1 ONLY, positive normalized
  values; "reached at k" includes 1; his factorial tables are mostly
  $\tau'$ (ultimate complexity, min over multiples), not $\tau$.
- The free-0 elimination lemma is reasoning-verified only; revisit inside
  TCB-005.
- Depths 6-7 are DONE (interned engine + last-gate scan; EXP-004). The
  depth-8 census needs canonicalization, a compiled/parallel backend, or
  the SAT lane: do not launch it naively (frontier ~$10^9$ states).
- Tower-shape root counting: NEVER use divisor enumeration on iterated
  maps (constants reach $c^{2^k}$); use the proved escape-bound window
  (EXP-005 incident and fix).
- Push via vault PAT with `credential.helper=` disabled (GCM hangs
  headless); gh via `GH_TOKEN`.

## Lenses ledger

| Round | Spine | Other lenses | Exploration yield |
|---|---|---|---|
| 2026-08-01 open | Census decided $\tau \le 4$ | Anatomy (consecutive triples; shift = 1 gate), invariant (degree cap useless here), dictionary (Markstroem import), audit (regression gate) | $z_{\max}$ niche identified; minimal-$\tau$-for-4 question minted |
| 2026-08-01 round 2 | Census decided $\tau = 5$ | External dialogue (Rojas full read), reformulation (dual $T(S)$ view B1; valuation-spectrum view B2), anatomy (DOS/Chebyshev-shadow mechanism, unpredicted), two-sided (records pile valuations: pressure on digit side) | Approaches ranking; RL-1..6 board; TCB-016 concrete lemma target |
| 2026-08-01 round 3 | Census decided $\tau = 6$ (last-gate scan; prediction refuted honestly) | Anatomy/theorem (tower lemma PROVED: constant integer yield of the doubling factory), method lens (last-gate lemma: one depth free), audit (smoke gate caught the input-accounting artifact; sympy 284/284) | The multiply-by-$x$ move; the $z = \tau - 1$ law question (TCB-019); stall-lemma generalization target (TCB-020) |
| 2026-08-01 rounds 4-5 | Census decided $\tau = 7$ (z_max = 5: plateau; prediction right) | Theorem (monic stall: single-map towers bounded for ALL monic maps), arithmetic dynamics (V8: cycle-length ceiling explained the EXP-005 discovery), external dialogue (Cheng, adelic tau, SAT synthesis pinned), audit (EXP-005 tooling incident: divisor counting vs c^{2^k} constants; escape-bound finder cross-checked) | Views V5-V8; RL-7..9; the plateaus phenomenon; the $[8,9]$ window as first SAT target; family loophole resolved empty for quadratics |
