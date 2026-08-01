# tau-conjecture: RESUME (zero-loss handoff)

Updated 2026-08-01, round 3 close. First read for any fresh session, per
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
$$z_{\max}(\tau) = 1, 2, 3, 3, 4, 5 \quad (\tau = 1..6).$$
Minimal $\tau$: 4 roots at 5 (EXP-002), 5 roots at 6 (EXP-003:
$\mp x(x^2-1)(x^2-4)$, the depth-5 DOS record times $x$; multiplying by
the input adjoins the root 0 for one gate). Records track
$z = \tau - 1$ from $\tau = 3$. Depth-5/6 records are difference-of-
squares splittings on the Chebyshev-conjugate map $x^2 - 2$; all record
2-adic spectra are $\{0,1\}$. Enumerator anchored to Markstroem 14/14 and
cross-checked vs sympy 284/284.

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
| $z_{\max}(\tau)$ | max distinct integer roots at $\tau(f) \le \tau$ | EXP-001/002 |
| tclib | enum cores + exact roots + 2-adic spectra + tests | code/tclib (5 tests green) |
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

## 4. In flight

Nothing running. Standing question (TCB-019): does $z_{\max}(7) = 6$
(the $z = \tau - 1$ law)? BLOCKED on TCB-005: the last-gate scan needs
the depth-6 frontier (~20M states, not stored); construction target for
the lower side: shifted DOS blocks + the multiply-by-$x$ move.

## 5. Next actions, ordered

1. TCB-005: prove the sign/reflection orbit quotient
   ($f(x) \sim \pm f(\pm x)$: need the cost bookkeeping, substitution
   maps inputs to inputs only for $x \mapsto -x$ combined with the free
   $-1$; write the lemma carefully) and dominated-state pruning; or build
   a compiled/multiprocess backend; then EXP-004 = depth-7.
2. TCB-020: generalize the stall lemma to $x^2 - c$ / monic inner maps
   (finite stable core via escape bounds); wiki 04 unit.
3. RL-3 (TCB-018): $T(S)$ structure lemmas + the $T$ table from census
   data ($T(\{\pm1,\pm2\}) = 5$, $T(\{0,\pm1,\pm2\}) = 6$ now exact).
4. TCB-017 (RL-2): valuation-spectrum record hunt design.
5. TCB-004/008/009: the reading ladder (Cheng, KPT15, Lipton, Shamir).

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
- Depth-6 naive census exceeds comfortable Python budget; do NOT launch it
  without TCB-005 or a compiled/parallel backend (declared in EXP-002).
- Push via vault PAT with `credential.helper=` disabled (GCM hangs
  headless); gh via `GH_TOKEN`.

## Lenses ledger

| Round | Spine | Other lenses | Exploration yield |
|---|---|---|---|
| 2026-08-01 open | Census decided $\tau \le 4$ | Anatomy (consecutive triples; shift = 1 gate), invariant (degree cap useless here), dictionary (Markstroem import), audit (regression gate) | $z_{\max}$ niche identified; minimal-$\tau$-for-4 question minted |
| 2026-08-01 round 2 | Census decided $\tau = 5$ | External dialogue (Rojas full read), reformulation (dual $T(S)$ view B1; valuation-spectrum view B2), anatomy (DOS/Chebyshev-shadow mechanism, unpredicted), two-sided (records pile valuations: pressure on digit side) | Approaches ranking; RL-1..6 board; TCB-016 concrete lemma target |
| 2026-08-01 round 3 | Census decided $\tau = 6$ (last-gate scan; prediction refuted honestly) | Anatomy/theorem (tower lemma PROVED: constant integer yield of the doubling factory), method lens (last-gate lemma: one depth free), audit (smoke gate caught the input-accounting artifact; sympy 284/284) | The multiply-by-$x$ move; the $z = \tau - 1$ law question (TCB-019); stall-lemma generalization target (TCB-020) |
