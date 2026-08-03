# tau-conjecture: RESUME (zero-loss handoff)

Updated 2026-08-02, round 8 close (seven-rooter times-case excluded; digit census). First read for any fresh session, per
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
move), 6 roots at EXACTLY 8 (EXP-006: 408 witnesses; e.g. the 8-gate
$q(q-2)(q-6)$, $q = x(x-1)$, via chained subtraction sharing), so
$z_{\max}(8) \ge 6$. Records are DOS splittings on $x^2 - 2$; record 2-adic
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
| tclib | enum cores + last-gate scan + exact roots + 2-adic spectra + tests | code/tclib (7 tests green) |
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
| 006 | The $[8,9]$ window | census CONFIRMED; our emptiness prediction REFUTED | **min $\tau$(6 roots) = 8** (408 witnesses; 3 replay-verified); five-rooter taxonomy: 7 patterns incl. non-consecutive; shipped as paper v0.02 |

## 4. In flight

Nothing running. $z_{\max}(8) = 6$ UNLESS a final-$\pm$ 8-gate 7-rooter
exists (EXP-007 excluded the $	imes$ case: max union 6 over all 408
hits): the single depth-8 unknown, SAT-shaped (TCB-029). Seven-root
threshold in $[8, 10]$. Digit ladders (V9) exact through $	au = 7$:
odd 1,2,2,2,2,3,4 (own record family: $(x^2-1)(x^2-9)$, 7 gates, roots
$\{\pm1,\pm3\}$); $p{=}3$: 1,1,1,2,2,3,3. Punctured five-rooters =
two-center DOS products (TCB-026 closed).

## 5. Next actions, ordered

1. TCB-029: the SAT final-$\pm$ decision at depth 8 (design note
   2026-08-02): resolves $z_{\max}(8)$ and the 8-gate 7-rooter question.
2. TCB-028: paper v0.03 ships WITH that resolution (deliberate).
3. TCB-027: mod-p Frobenius-ceiling instrumentation (V10/V9 pairing).
4. TCB-005: depth-8 backend (the larger census goal).
5. Reads: Doyle-Poonen (TCB-024), Cheng 2004 full, KPT15 PDF.

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
- Manuscript: `manuscripts/tau-conjecture/census/` (v0.02 PUBLISHED
  2026-08-02: version DOI 10.5281/zenodo.21763182; v0.01:
  10.5281/zenodo.21753439; concept 10.5281/zenodo.21753438 always
  latest; vault ledger `<CAOS_MANAGE>/manuscripts/tau-conjecture/deposits.json`;
  updates ship as Zenodo NEW VERSIONS, never edits)
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
| 2026-08-02 round 7 | Window CLOSED: min tau(6 roots) = 8 (times-case co-occurrence scan; emptiness prediction refuted, third time) | Method (case-split invariant: product roots = union), audit (smoke known-answer; witnesses replay-verified independently), anatomy (7 five-rooter patterns incl. punctured) | Paper v0.02 (DOI 10.5281/zenodo.21763182); TCB-025/026 minted; SAT lane rescoped to z_max(8) |
| 2026-08-02 round 8 | Seven-rooter times-case EXCLUDED (max union 6; first surviving emptiness prediction); digit ladders measured (odd prediction refuted: 4th refutation; own record family) | V9 digit census (the sufficient-form ladder), V10 three-worlds trichotomy, anatomy (two-center DOS punctures), audit (408 anchor reproduced) | z_max(8) pinned to the SAT residual (TCB-029); TCB-027/028 minted; KPT15 pinned |
