# tau-conjecture: RESUME (zero-loss handoff)

Updated 2026-08-01, round 2 close. First read for any fresh session, per
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
$$z_{\max}(\tau) = 1, 2, 3, 3, 4 \quad (\tau = 1..5).$$
Minimal $\tau$ for 4 distinct integer roots = 5 (EXP-002). Depth-5 records
= difference-of-squares splittings on the Chebyshev-conjugate map
$x^2 - 2$: $x^2 - (x^2-2)^2 = -(x-1)(x+1)(x-2)(x+2)$; all record 2-adic
spectra are $\{0,1\}$. Enumerator anchored to Markstroem 14/14.

## 2. Objects table

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

## 4. In flight

Nothing running. Minted, not yet declared: (a) TCB-016, the iterated
$x^2-2$ question: $F_k := $ ($k$-fold DOS tower); how many doublings keep
ALL roots integral and at what gate cost (the integer-vs-real divergence in
its purest form); (b) depth-6 census blocked on TCB-005 canonicalization
(naive ~25M state-ops).

## 5. Next actions, ordered

1. TCB-005: prove sign/reflection orbit reduction ($f(x) \sim \pm f(\pm x)$
   preserve $\tau$ and $z$) and dominated-state pruning; add sympy
   cross-check of a depth-5 state sample; THEN declare EXP-003 (depth-6
   census) with the reduced branching.
2. TCB-016 (RL-4): the $x^2-2$ tower lemma; pure algebra + small exact
   computations; likely a wiki/manuscript unit.
3. TCB-002: fetch + read Shub-Smale 1995 (Duke); upgrade dossier tags.
4. Wiki 02 (implication ladder) and 03 (census) transcription; census page
   carries the $z_{\max}$ table + record gallery + witness programs.
5. RL-5: integer frontier run design (addition-chain canonicalization
   import) once the polynomial frontier is unblocked.

Commands: tests
`.venv python -m pytest problems/computation-complexity/tau-conjecture/code/tclib -q`;
census runs from each experiment folder via the MAIN checkout venv
`D:\_Repos\Research_Caos\CAOS_RESEARCH\.venv\Scripts\python.exe run.py`.

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
